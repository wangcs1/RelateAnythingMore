import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
STUDY = ROOT / "HOR/research"
GROUPS = ("baseline", "geometry", "RA_guided")
SCOPES = ("all_968_GT", "fixed_530_GT")
BORDER_TOLERANCE_PIXELS = 1e-3


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject_nonfinite(value):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)


def read_lines(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line, parse_constant=reject_nonfinite) for line in handle if line.strip()]


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def compare(value, expected, name):
    require(np.isclose(value, expected, rtol=1e-10, atol=1e-12),
            f"Independent active-detection value differs for {name}: {value}, {expected}")


def overlap(first, second):
    intersection = max(min(first[2], second[2]) - max(first[0], second[0]), 0) * max(
        min(first[3], second[3]) - max(first[1], second[1]), 0)
    first_area = max(first[2] - first[0], 0) * max(first[3] - first[1], 0)
    second_area = max(second[2] - second[0], 0) * max(second[3] - second[1], 0)
    union = first_area + second_area - intersection
    require(union > 0, "A source endpoint has no positive bounding-box area")
    return intersection / union


def relation_key(row):
    return row["subject_id"], row["object_id"], row["predicate_id"]


def border_overflow(box, bounds):
    return max(bounds[0] - box[0], bounds[1] - box[1], box[2] - bounds[2], box[3] - bounds[3], 0)


def correspondences(objects, truths, threshold):
    return {truth["id"]: {item["id"] for item in objects
                          if item["label"] == truth["label"]
                          and overlap(item["box_xyxy"], truth["box_xyxy"]) >= threshold}
            for truth in truths}


def verify_inputs(config, sources, regions, predictions, plans, prepared):
    count = config["expected_records"]
    manifest = read_json(ROOT / config["sample_manifest"])
    expected_indices = manifest["indices"]
    for name, rows in (("source", sources), ("regions", regions), ("predictions", predictions), ("plans", plans)):
        require(len(rows) == len({row["index"] for row in rows}) == count,
                f"The {name} records do not contain 500 unique sample indices")
        require([row["index"] for row in rows] == expected_indices, f"The {name} sample order changed")
    require(prepared["records"] == count and prepared["GT_used_to_select_crops"] is False,
            "The prepared input records or GT-selection declaration changed")
    config_path = STUDY / "configs/active_detection.json"
    output = ROOT / config["output_directory"]
    require(digest(config_path) == prepared["config_sha256"], "The active-detection configuration changed")
    require(digest(output / "crop_plans.jsonl") == prepared["plan_sha256"], "The signed crop plans changed")
    signed_inputs = {str((ROOT / relative).resolve()): value for relative, value in prepared["inputs_sha256"].items()}
    required_paths = [config_path, ROOT / config["source_region_predictions"],
                      ROOT / config["source_region_runtime"], ROOT / config["source_region_evaluation"],
                      ROOT / config["sample_manifest"], ROOT / config["source_identity_metadata"]]
    require(set(signed_inputs) == {str(path.resolve()) for path in required_paths}, "Prepared input signature set changed")
    for path in required_paths:
        require(digest(path) == signed_inputs[str(path.resolve())], f"An upstream input changed: {path}")
    runtime = read_json(output / "runtime.json")
    require(runtime["records"] == count, "Active-detection inference is incomplete")
    require(runtime["config_sha256"] == digest(config_path), "Inference used a different configuration")
    require(runtime["prepared_inputs_sha256"] == digest(output / "prepared_inputs.json"), "Prepared inputs differ from inference")
    require(runtime["script_sha256"] == digest(STUDY / "scripts/active_detection_study.py"),
            "The inference script differs from the source recorded during model execution")
    require(runtime["latest_region_source_runtime"] == prepared["source_region_runtime"], "The baseline runtime provenance differs")
    require(prepared["source_region_runtime"] == read_json(ROOT / config["source_region_runtime"]),
            "The frozen baseline runtime differs from its source")
    require(prepared["source_region_runtime"]["input_sha256"]["baseline_predictions"] ==
            digest(ROOT / "HOR/output/random500/predictions.jsonl"), "The historical 500-record source changed")
    for label in ("detector", "relation", "text"):
        require(digest(ROOT / config[f"{label}_weights"]) == config[f"{label}_weights_sha256"],
                f"The fixed {label} checkpoint differs")
    hashes = set()
    for position, (source, region, row, plan) in enumerate(zip(sources, regions, predictions, plans), 1):
        for key in ("file_name", "image_sha256"):
            require(source[key] == region[key] == row[key] == plan[key], f"Image identity differs at {source['index']}")
        for key in ("image_size", "ground_truth_objects", "ground_truth_relations"):
            require(source[key] == region[key], f"Historical GT differs at {source['index']}: {key}")
        require(plan["image_size"] == source["image_size"], "A crop plan uses a different image size")
        image_path = ROOT / config["image_directory"] / source["file_name"]
        require(digest(image_path) == source["image_sha256"], f"Image bytes changed: {image_path}")
        with Image.open(image_path) as image:
            require(list(image.size) == source["image_size"], "A source image dimension differs")
        hashes.add(source["image_sha256"])
        offset = (position - 1) % len(GROUPS)
        require(row["execution_order"] == list(GROUPS[offset:] + GROUPS[:offset]), "The inference order was not rotated")
        require(set(row["groups"]) == set(GROUPS), "An inference group is absent or unexpected")
    require(len(hashes) == config["expected_unique_source_identities"], "Source-image identity count changed")
    return runtime


def fixed_truths(source, threshold):
    objects = {item["id"]: item for item in source["ground_truth_objects"]}
    matches = correspondences(source["detected"]["objects"], source["ground_truth_objects"], threshold)
    vocabulary = set(source["detector_categories"])
    return {relation_key(row) for row in source["ground_truth_relations"]
            if objects[row["subject_id"]]["label"] in vocabulary
            and objects[row["object_id"]]["label"] in vocabulary
            and any(subject != obj for subject in matches[row["subject_id"]] for obj in matches[row["object_id"]])}


def verify_truths(config, sources, regions, threshold):
    stored = read_json(STUDY / "reports/decoder/evidence/fixed_valid_endpoint_gt.json")
    fixed_reference = defaultdict(set)
    for row in stored["relations"]:
        fixed_reference[row["index"]].add(relation_key(row))
    full, fixed = {}, {}
    for source, region in zip(sources, regions):
        index = source["index"]
        keys = {relation_key(row) for row in source["ground_truth_relations"]}
        require(len(keys) == len(source["ground_truth_relations"]), f"Duplicated historical GT at {index}")
        endpoints = {item["id"]: item for item in source["ground_truth_objects"]}
        require(all(endpoints[subject]["is_person"] or endpoints[obj]["is_person"] for subject, obj, _ in keys),
                "A nonhuman relation entered the human-related GT scope")
        full[index] = keys
        fixed[index] = fixed_truths(source, threshold)
        require(fixed[index] == fixed_reference[index] == {relation_key(row) for row in region["fixed_endpoint_valid_relations"]},
                f"The fixed endpoint-valid GT scope differs at {index}")
    require(sum(map(len, full.values())) == config["expected_human_GT_relations"], "The 968-GT scope changed")
    require(sum(map(len, fixed.values())) == config["expected_fixed_endpoint_valid_GT_relations"], "The fixed 530-GT scope changed")
    return {SCOPES[0]: full, SCOPES[1]: fixed}


def expected_crop(person, size, fraction, config, object_box=None):
    width, height = size
    x1, y1, x2, y2 = person["box_xyxy"]
    center = [(x1 + x2) / 2, y1 + fraction * (y2 - y1)]
    if object_box is not None:
        mix = config["guidance_object_center_mix"]
        center = [(1 - mix) * center[axis] + mix * (object_box[axis] + object_box[axis + 2]) / 2 for axis in range(2)]
    sides = [min(width, max(config["crop_min_side_pixels"], (x2 - x1) * config["crop_width_person_multiplier"])),
             min(height, max(config["crop_min_side_pixels"], (y2 - y1) * config["crop_height_person_multiplier"]))]
    origin = [min(max(0, center[axis] - sides[axis] / 2), limit - sides[axis])
              for axis, limit in enumerate((width, height))]
    return [math.floor(origin[0]), math.floor(origin[1]), min(width, math.ceil(origin[0] + sides[0])),
            min(height, math.ceil(origin[1] + sides[1]))]


def expected_plans(region, config):
    baseline = region["groups"]["A_fasterrcnn_thing"]
    objects = {item["id"]: item for item in baseline["objects"]}
    people = [item for item in objects.values() if item["is_person"]]
    if not people:
        return {"geometry": [], "RA_guided": []}
    person = min(people, key=lambda item: (-(item["box_xyxy"][2] - item["box_xyxy"][0]) *
                                         (item["box_xyxy"][3] - item["box_xyxy"][1]), item["source_object_key"]))
    geometry = [{"policy_source": "geometry_default", "person_id": person["id"],
                 "person_source_key": person["source_object_key"], "body_fraction": fraction,
                 "crop_box_xyxy": expected_crop(person, region["image_size"], fraction, config), "guidance_relation": None}
                for fraction in config["geometry_body_fractions"]]
    routed = []
    candidates = sorted(baseline["relations"], key=lambda item: (-item["fused_logit"], item["subject_id"],
                                                               item["object_id"], item["predicate_id"]))
    for relation in candidates:
        predicate = relation["predicate"]
        if predicate not in config["guidance_body_fractions"] or relation["score"] < config["guidance_min_raw_sigmoid_score"]:
            continue
        subject, obj = objects[relation["subject_id"]], objects[relation["object_id"]]
        if not subject["is_person"] or obj["is_person"]:
            continue
        fraction = config["guidance_body_fractions"][predicate]
        routed.append({"policy_source": "RA_relation_route", "person_id": subject["id"],
                       "person_source_key": subject["source_object_key"], "body_fraction": fraction,
                       "crop_box_xyxy": expected_crop(subject, region["image_size"], fraction, config, obj["box_xyxy"]),
                       "guidance_relation": relation})
    guided = []
    for candidate in routed + geometry:
        if all(candidate["crop_box_xyxy"] != selected["crop_box_xyxy"] for selected in guided):
            guided.append(candidate)
        if len(guided) == config["queries_per_detected_person_image"]:
            break
    if len(guided) < 2:
        guided.extend(geometry[len(guided):2])
    return {group: [dict(query, query_id=index) for index, query in enumerate(queries)]
            for group, queries in (("geometry", geometry), ("RA_guided", guided))}


def verify_queries(region, row, plan, config):
    expected = expected_plans(region, config)
    require(plan["queries"] == expected, f"The crop plan uses undeclared information at {row['index']}")
    require(row["groups"]["baseline"]["queries"] == [], "Baseline unexpectedly used a crop query")
    people = any(item["is_person"] for item in region["groups"]["A_fasterrcnn_thing"]["objects"])
    expected_count = config["queries_per_detected_person_image"] if people else config["no_detected_person_queries"]
    for group in GROUPS[1:]:
        queries = row["groups"][group]["queries"]
        require(len(queries) == expected_count, "The two active policies have different per-image query budgets")
        for query, reference in zip(queries, expected[group]):
            require({key: query[key] for key in reference} == reference, "Executed crop differs from its signed plan")
            left, top, right, bottom = query["crop_box_xyxy"]
            width, height = region["image_size"]
            require(0 <= left < right <= width and 0 <= top < bottom <= height, "A crop leaves its source image")
            require(query["input_pixels"] == (right - left) * (bottom - top), "Crop pixel accounting differs")
            require(query["elapsed_seconds"] >= 0, "Negative detector execution time")
            require(len(query["detections"]) <= config["endpoint_cap"], "A crop detector exceeded the common endpoint budget")
            for item in query["detections"]:
                x1, y1, x2, y2 = item["box_xyxy"]
                require(np.isfinite([x1, y1, x2, y2, item["detection_score"]]).all()
                        and x1 < x2 and y1 < y2
                        and border_overflow(item["box_xyxy"], (left, top, right, bottom)) <= BORDER_TOLERANCE_PIXELS,
                        "A crop detection does not lie within its declared source crop")
                require(item["source_kind"] == "crop" and item["source_crop_policy"] == group,
                        "Crop endpoint provenance differs")
                require(item["source_query_id"] == query["query_id"] and item["source_crop_xyxy"] == query["crop_box_xyxy"],
                        "A crop endpoint was attributed to the wrong query")
                require(item["source_object_key"] == f"crop:{group}:{query['query_id']}:{item['source_crop_detection_id']:06d}",
                        "Crop endpoint source key differs")


def verify_merge(region, prediction, group, config):
    original = region["groups"]["A_fasterrcnn_thing"]["objects"]
    objects = prediction["objects"]
    width, height = region["image_size"]
    require(all(border_overflow(item["box_xyxy"], (0, 0, width, height)) <= BORDER_TOLERANCE_PIXELS for item in objects),
            "A selected endpoint leaves its original image beyond the numerical tolerance")
    require(len(objects) <= config["endpoint_cap"], "An active group exceeded the common 40-endpoint cap")
    require([item["id"] for item in objects] == list(range(len(objects))), "Endpoint IDs are not consecutive")
    keys = [item["source_object_key"] for item in objects]
    require(len(set(keys)) == len(keys) and keys == sorted(keys), "Selected endpoint source keys are duplicated or reordered")
    existing = [dict(item, source_kind="existing") for item in original]
    if group == "baseline":
        require(objects == existing, "Baseline endpoints differ from the frozen region-A input")
    detected = [item for query in prediction["queries"] for item in query["detections"]]
    candidates = existing + detected
    candidate_by_key = {item["source_object_key"]: item for item in candidates}
    require(len(candidate_by_key) == len(candidates), "Candidate source keys are duplicated")
    merge = prediction["merge_audit"]
    removed = merge["removed_by_NMS"]
    capped = merge["removed_by_endpoint_cap"]
    partitions = objects + removed + capped
    require(len(partitions) == len(candidates) and {item["source_object_key"] for item in partitions} == set(candidate_by_key),
            "Endpoint merge partitions do not cover their input exactly once")
    for item in partitions:
        reference = candidate_by_key[item["source_object_key"]]
        require({key: value for key, value in item.items() if key != "id"} ==
                {key: value for key, value in reference.items() if key != "id"}, "Endpoint merge changed candidate data")
    require(merge["input_endpoint_count"] == len(candidates) and merge["crop_detection_count"] == len(detected),
            "Endpoint input counts differ")
    kept = objects + capped
    require(merge["after_NMS_count"] == len(kept) and merge["selected_endpoint_count"] == len(objects),
            "Endpoint selection counts differ")
    require(len(objects) == min(len(kept), config["endpoint_cap"]), "The common endpoint cap was applied differently")
    if group != "baseline":
        for first_position, first in enumerate(kept):
            for second in kept[first_position + 1:]:
                require(first["category_id"] != second["category_id"] or
                        overlap(first["box_xyxy"], second["box_xyxy"]) <= config["classwise_merge_nms_iou"] + 1e-6,
                        "Two same-class NMS survivors overlap above the declared threshold")
        for item in removed:
            require(any(other["category_id"] == item["category_id"]
                        and other["detection_score"] >= item["detection_score"]
                        and overlap(other["box_xyxy"], item["box_xyxy"]) > config["classwise_merge_nms_iou"] - 1e-6
                        for other in kept), "An NMS removal has no valid surviving suppressor")
        if objects and capped:
            require(min(item["detection_score"] for item in objects) >= max(item["detection_score"] for item in capped),
                    "The endpoint cap discarded a higher-score NMS survivor")
    original_missing = [item["source_object_key"] for item in original if item["source_object_key"] not in set(keys)]
    require(merge["original_source_keys_not_selected"] == original_missing, "Original endpoint loss accounting differs")


def verify_relation_budget(row, group, config):
    prediction = row["groups"][group]
    objects = {item["id"]: item for item in prediction["objects"]}
    require(all(np.isfinite(item["box_xyxy"]).all() and item["box_xyxy"][0] < item["box_xyxy"][2]
                and item["box_xyxy"][1] < item["box_xyxy"][3] for item in objects.values()),
            "A selected endpoint has invalid geometry")
    people = {item["id"] for item in objects.values() if item["is_person"]}
    require(set(prediction["human_ids"]) == people, "Person endpoint IDs differ")
    pairs = prediction["all_human_pairs"]
    pair_keys = [(item["subject_id"], item["object_id"]) for item in pairs]
    require(len(set(pair_keys)) == len(pair_keys) == prediction["human_pairs_scored"], "Human candidate pairs are duplicated")
    require(all(subject != obj and subject in objects and obj in objects and (subject in people or obj in people)
                for subject, obj in pair_keys), "A candidate pair is invalid or unrelated to people")
    expected_pairs = sum(subject != obj and (subject in people or obj in people) for subject in objects for obj in objects)
    require(prediction["expected_human_pairs"] == expected_pairs, "Possible human-pair count differs")
    require(len(pairs) <= prediction["candidate_pairs"] <= config["relation_pair_budget"], "The common 400-pair budget was exceeded")
    require(prediction["pair_policy"] == "official_400", "An active group used a different pair policy")
    selected = prediction["relations"]
    require(len(selected) <= config["relation_top_k"], "The common Top-50 output cap was exceeded")
    require(len({relation_key(item) for item in selected}) == len(selected), "The output contains duplicate triplets")
    candidates = [item for pair in pairs for item in pair["predictions"]]
    ordered = sorted(candidates, key=lambda item: (-item["fused_logit"], *relation_key(item)))[:config["relation_top_k"]]
    require(selected == ordered, "The Top-50 output differs from its ranked spatial/semantic candidates")
    require([item["rank"] for item in selected] == list(range(1, len(selected) + 1)), "Output ranks are not consecutive")
    for item in selected:
        require(np.isfinite([item["fused_logit"], item["score"]]).all(), "A relation score is nonfinite")
    path = ROOT / config["output_directory"] / "logits" / group / f"{row['index']:04d}.npz"
    if prediction["candidate_pairs"]:
        with np.load(path, allow_pickle=False) as arrays:
            subject = arrays["subject_indices"]
            obj = arrays["object_indices"]
            logits = arrays["predicate_logits"]
            pair_logits = arrays["pair_logits"]
            require(len(subject) == len(obj) == len(logits) == len(pair_logits) == prediction["candidate_pairs"],
                    "The saved model output does not follow its reported pair budget")
            require(np.isfinite(logits).all() and np.isfinite(pair_logits).all(), "Saved relation logits are nonfinite")
            all_keys = set(zip(subject.tolist(), obj.tolist()))
            require(len(all_keys) == len(subject) and all(s != o and s in objects and o in objects for s, o in all_keys),
                    "Saved model candidate pairs are duplicated or invalid")
            require({key for key in all_keys if key[0] in people or key[1] in people} == set(pair_keys),
                    "Human candidate filtering differs from the saved model output")
    else:
        require(not path.exists(), "Unexpected logits for an unexecuted relation model")


def evaluate_independently(sources, predictions, group, truths, threshold):
    metrics_by_k = {20: [], 50: []}
    classes_by_k = {20: defaultdict(list), 50: defaultdict(list)}
    total_hits, stages, class_gt, class_hits, prediction_predicates = Counter(), Counter(), Counter(), Counter(), Counter()
    per_image = []
    predicted_count = 0
    for source, row in zip(sources, predictions):
        prediction = row["groups"][group]
        selected = prediction["relations"]
        predicted_count += len(selected)
        prediction_predicates.update(item["predicate"] for item in selected)
        keys = truths[source["index"]]
        if not keys:
            continue
        correspondence = correspondences(prediction["objects"], source["ground_truth_objects"], threshold)
        gt_rows = [item for item in source["ground_truth_relations"] if relation_key(item) in keys]
        local_hits = {20: set(), 50: set()}
        local_stages = Counter()
        diagnostics = []
        for truth in gt_rows:
            subject, obj, predicate = relation_key(truth)
            sub_matches, obj_matches = correspondence[subject], correspondence[obj]
            for k in local_hits:
                if any(item["subject_id"] in sub_matches and item["object_id"] in obj_matches
                       and item["predicate_id"] == predicate for item in selected[:k]):
                    local_hits[k].add((subject, obj, predicate))
            if (subject, obj, predicate) in local_hits[50]:
                stage = "hit50"
            elif not sub_matches or not obj_matches:
                stage = "endpoint_missing_or_wrong_class"
            else:
                pairs = [pair for pair in prediction["all_human_pairs"]
                         if pair["subject_id"] in sub_matches and pair["object_id"] in obj_matches]
                if not pairs:
                    stage = "pair_not_selected" if any(s != o for s in sub_matches for o in obj_matches) else "endpoints_collapsed_to_same_box"
                else:
                    stage = "rank_below50" if any(item["predicate_id"] == predicate for pair in pairs for item in pair["predictions"]) else "wrong_predicate"
            local_stages[stage] += 1
            diagnostics.append({"subject_id": subject, "object_id": obj, "predicate": truth["predicate"], "stage": stage,
                                "matching_subject_ids": sorted(sub_matches), "matching_object_ids": sorted(obj_matches)})
        denominators = Counter(key[2] for key in keys)
        class_gt.update(denominators)
        stages.update(local_stages)
        for k, recalled in local_hits.items():
            metrics_by_k[k].append(len(recalled) / len(keys))
            total_hits[k] += len(recalled)
            numerator = Counter(key[2] for key in recalled)
            for predicate, denominator in denominators.items():
                classes_by_k[k][predicate].append(numerator[predicate] / denominator)
            if k == 50:
                class_hits.update(numerator)
        per_image.append({"index": source["index"], "gt_count": len(keys), "hits50": len(local_hits[50]),
                          "R@50": len(local_hits[50]) / len(keys), "stages": dict(local_stages), "diagnostics": diagnostics})
    denominator = sum(map(len, truths.values()))
    metrics = {}
    for k in metrics_by_k:
        metrics[f"R@{k}"] = float(np.mean(metrics_by_k[k]))
        metrics[f"mR@{k}"] = float(np.mean([np.mean(values) for values in classes_by_k[k].values()]))
        metrics[f"pooled_R@{k}"] = total_hits[k] / denominator
    return {"images": len(sources), "scored_images": len(per_image), "unique_gt": denominator, "metrics": metrics,
            "hits": {str(key): value for key, value in total_hits.items()}, "failure_stages": dict(stages),
            "predictions": predicted_count, "prediction_predicates": dict(prediction_predicates),
            "per_class": {str(predicate): {"gt": class_gt[predicate], "hits50": class_hits[predicate],
                                           "pooled_R@50": class_hits[predicate] / class_gt[predicate],
                                           "image_macro_R@50": float(np.mean(classes_by_k[50][predicate]))}
                          for predicate in sorted(class_gt)}, "per_image": per_image}


def compare_tree(value, expected, name):
    if isinstance(value, dict):
        require(set(value) == set(expected), f"Independent result fields differ at {name}")
        for key in value:
            compare_tree(value[key], expected[key], f"{name}.{key}")
    elif isinstance(value, list):
        require(len(value) == len(expected), f"Independent list size differs at {name}")
        for index, (item, reference) in enumerate(zip(value, expected)):
            compare_tree(item, reference, f"{name}[{index}]")
    elif isinstance(value, (int, float)):
        compare(value, expected, name)
    else:
        require(value == expected, f"Independent result differs at {name}: {value}, {expected}")


def verify_costs(predictions, reports):
    expected = read_json(reports / "costs.json")
    require(set(expected) == set(GROUPS), "The reported cost groups differ")
    for group in GROUPS:
        queries = [query for row in predictions for query in row["groups"][group]["queries"]]
        pixels = [query["input_pixels"] for query in queries]
        query_times = [query["elapsed_seconds"] for query in queries]
        relation_times = [row["groups"][group]["relation_elapsed_seconds"] for row in predictions]
        measured = {"additional_detector_calls": len(queries),
                    "query_policy_sources": dict(Counter(query["policy_source"] for query in queries)),
                    "total_query_input_pixels": sum(pixels), "query_input_pixels_mean": float(np.mean(pixels)) if pixels else 0,
                    "query_seconds_total": sum(query_times), "query_seconds_mean": float(np.mean(query_times)) if query_times else 0,
                    "query_seconds_median": float(np.median(query_times)) if query_times else 0,
                    "query_seconds_p90": float(np.percentile(query_times, 90)) if query_times else 0,
                    "relation_seconds_total": sum(relation_times), "relation_seconds_mean_per_record": float(np.mean(relation_times)),
                    "relation_seconds_p90": float(np.percentile(relation_times, 90)),
                    "measured_query_plus_relation_seconds": sum(query_times) + sum(relation_times)}
        compare_tree(measured, expected[group], f"costs.{group}")
    return {group: expected[group]["measured_query_plus_relation_seconds"] for group in GROUPS}


def verify_manifest(reports, config):
    path = reports / "artifact_manifest.json"
    manifest = read_json(path)
    require(manifest["study"] == config["study"], "The active-detection evidence manifest belongs to another study")
    required = {"HOR/research/configs/active_detection.json", "HOR/research/scripts/active_detection_study.py",
                "HOR/research/scripts/active_detection_analysis.py", "HOR/pipeline.py", "HOR/evaluation.py",
                "HOR/config.json", "data/PSG/packed/psg/test/meta.json"}
    require(required <= set(manifest["files"]), "The manifest omits a required inference or analysis source")
    for relative, metadata in manifest["files"].items():
        artifact = (ROOT / relative).resolve()
        require(artifact.is_relative_to(ROOT) and artifact.is_file(), f"Missing or invalid active-detection artifact: {relative}")
        require(artifact.stat().st_size == metadata["bytes"] and digest(artifact) == metadata["sha256"],
                f"The active-detection evidence manifest is stale: {relative}")
    require(manifest["published_source_images"] == 0 and manifest["human_visual_annotation_performed"] is False,
            "The evidence state differs from the image-free, unannotated delivery")
    return len(manifest["files"])


def verify_public_evidence(regions, predictions, plans, prepared, runtime, reports, config):
    require(read_json(reports / "prepared_inputs.json") == prepared, "Published prepared-input evidence differs from inference")
    require(read_json(reports / "runtime.json") == runtime, "Published runtime evidence differs from inference")
    require(read_lines(reports / "crop_plans.jsonl") == plans, "Published crop plans differ from executed plans")
    paired = read_lines(reports / "paired_outputs.jsonl")
    require(len(paired) == len(regions), "Published paired output does not contain all source records")
    metadata = read_json(ROOT / config["source_identity_metadata"])
    identities = {row["index"]: row["identity_key"] for values in metadata["splits"].values() for row in values}
    for region, prediction, evidence in zip(regions, predictions, paired):
        for key in ("index", "file_name", "image_sha256", "image_size", "ground_truth_objects", "ground_truth_relations",
                    "fixed_endpoint_valid_relations"):
            require(evidence[key] == region[key], f"Published source/GT evidence differs at {region['index']}: {key}")
        require(evidence["source_identity"] == identities[region["index"]], "Published paired identity differs")
        require(set(evidence["groups"]) == set(GROUPS), "Published group set differs")
        for group in GROUPS:
            for key in ("objects", "relations", "queries", "candidate_pairs", "human_pairs_scored", "merge_audit"):
                require(evidence["groups"][group][key] == prediction["groups"][group][key],
                        f"Published paired evidence differs at {region['index']}/{group}/{key}")
    return len(paired)


def verify_bootstrap(sources, truth_scopes, measured_evaluation, reports, config):
    reference = read_json(reports / "bootstrap.json")
    require(reference["seed"] == config["bootstrap_seed"] and
            reference["repetitions"] == config["bootstrap_repetitions"] == 20000,
            "The bootstrap seed or repetition count changed")
    split_metadata = read_json(ROOT / config["source_identity_metadata"])
    identity_rows = [row for values in split_metadata["splits"].values() for row in values]
    identities = {row["index"]: row for row in identity_rows}
    require(len(identities) == len(identity_rows) == len(sources), "Bootstrap identity metadata does not cover all records once")
    vg_metadata = read_json(ROOT / split_metadata["identity_metadata"])
    vg_by_id = {int(row["image_id"]): row for row in vg_metadata}
    by_identity, by_coco, by_hash = defaultdict(set), defaultdict(set), defaultdict(set)
    for source in sources:
        identity = identities[source["index"]]
        coco_id = vg_by_id[int(Path(source["file_name"]).stem)]["coco_id"]
        require(identity["file_name"] == source["file_name"] and identity["image_sha256"] == source["image_sha256"],
                "A bootstrap identity points to a different image")
        require(identity["coco_image_id"] == coco_id and coco_id is not None,
                "The bootstrap COCO identity differs from Visual Genome metadata")
        by_identity[identity["identity_key"]].add(coco_id)
        by_coco[coco_id].add(identity["identity_key"])
        by_hash[source["image_sha256"]].add(identity["identity_key"])
    require(len(by_identity) == config["expected_unique_source_identities"] and
            all(len(values) == 1 for collection in (by_identity, by_coco, by_hash) for values in collection.values()),
            "The bootstrap clusters do not preserve shared COCO and image-byte identities")
    rng = np.random.default_rng(config["bootstrap_seed"])
    summaries = {}
    comparisons = (("geometry", "baseline"), ("RA_guided", "baseline"), ("RA_guided", "geometry"))
    for scope in SCOPES:
        truths = truth_scopes[scope]
        indices = sorted(index for index, rows in truths.items() if rows)
        cluster_names = sorted({identities[index]["identity_key"] for index in indices})
        clusters = {key: index for index, key in enumerate(cluster_names)}
        predicate_names = sorted({key[2] for index in indices for key in truths[index]})
        predicates = {key: index for index, key in enumerate(predicate_names)}
        reference_scope = reference["scopes"][scope]
        require((reference_scope["PSG_records_with_GT"], reference_scope["unique_source_identities"],
                 reference_scope["predicate_classes"]) == (len(indices), len(clusters), len(predicates)),
                f"The bootstrap unit or predicate counts differ in {scope}")
        records_per_cluster = np.zeros(len(clusters))
        gt_per_cluster = np.zeros(len(clusters))
        class_records_per_cluster = np.zeros((len(clusters), len(predicates)))
        image_recalls = {group: np.zeros(len(clusters)) for group in GROUPS}
        relation_hits = {group: np.zeros(len(clusters)) for group in GROUPS}
        class_recalls = {group: np.zeros_like(class_records_per_cluster) for group in GROUPS}
        details = {group: {row["index"]: row for row in measured_evaluation[group][scope]["per_image"]}
                   for group in GROUPS}
        source_by_index = {source["index"]: source for source in sources}
        for index in indices:
            cluster = clusters[identities[index]["identity_key"]]
            records_per_cluster[cluster] += 1
            gt_per_cluster[cluster] += len(truths[index])
            denominator_by_class = Counter(key[2] for key in truths[index])
            names = {row["predicate"]: row["predicate_id"] for row in source_by_index[index]["ground_truth_relations"]}
            for predicate in denominator_by_class:
                class_records_per_cluster[cluster, predicates[predicate]] += 1
            for group in GROUPS:
                detail = details[group][index]
                image_recalls[group][cluster] += detail["R@50"]
                relation_hits[group][cluster] += detail["hits50"]
                hit_by_class = Counter(names[row["predicate"]] for row in detail["diagnostics"] if row["stage"] == "hit50")
                for predicate, number in denominator_by_class.items():
                    class_recalls[group][cluster, predicates[predicate]] += hit_by_class[predicate] / number
        require(int(gt_per_cluster.sum()) == sum(map(len, truths.values())), "A fixed bootstrap GT denominator changed")
        weights = rng.multinomial(len(clusters), np.full(len(clusters), 1 / len(clusters)),
                                  size=config["bootstrap_repetitions"]).astype(np.float64)
        require(np.all(weights.sum(axis=1) == len(clusters)), "A bootstrap draw changed the number of source identities")
        record_denominator = weights @ records_per_cluster
        gt_denominator = weights @ gt_per_cluster
        class_denominator = weights @ class_records_per_cluster
        distributions = {}
        for group in GROUPS:
            numerator = weights @ class_recalls[group]
            scores = np.divide(numerator, class_denominator, out=np.zeros_like(numerator), where=class_denominator > 0)
            distributions[group] = {"R@50": (weights @ image_recalls[group]) / record_denominator,
                                    "pooled_R@50": (weights @ relation_hits[group]) / gt_denominator,
                                    "mR@50": scores.sum(axis=1) / np.count_nonzero(class_denominator, axis=1)}
        verified_comparisons = {}
        require(set(reference_scope["comparisons"]) == {f"{new}_minus_{old}" for new, old in comparisons},
                "The bootstrap comparison set differs")
        for new, old in comparisons:
            comparison = {}
            for metric in ("R@50", "mR@50", "pooled_R@50"):
                difference = distributions[new][metric] - distributions[old][metric]
                bounds = np.percentile(difference, [2.5, 97.5]).tolist()
                point = measured_evaluation[new][scope]["metrics"][metric] - measured_evaluation[old][scope]["metrics"][metric]
                result = {"point_difference": point, "percentile_95_CI": bounds,
                          "CI_excludes_zero": bounds[0] > 0 or bounds[1] < 0}
                compare_tree(result, reference_scope["comparisons"][f"{new}_minus_{old}"][metric],
                             f"bootstrap.{scope}.{new}_minus_{old}.{metric}")
                comparison[metric] = result
            verified_comparisons[f"{new}_minus_{old}"] = comparison
        summaries[scope] = {"source_identity_clusters": len(clusters), "PSG_records": len(indices),
                            "fixed_GT_count": int(gt_per_cluster.sum()), "repetitions": len(weights),
                            "shared_pairing_weights_for_all_methods": True,
                            "verified_metrics_per_comparison": ["R@50", "mR@50", "pooled_R@50"],
                            "RA_guided_minus_geometry_R@50": verified_comparisons["RA_guided_minus_geometry"]["R@50"]}
    return summaries


def main():
    config = read_json(STUDY / "configs/active_detection.json")
    hor_config = read_json(ROOT / "HOR/config.json")
    require((config["queries_per_detected_person_image"], config["endpoint_cap"], config["relation_pair_budget"],
             config["relation_top_k"]) == (2, 40, 400, 50), "The fixed active-detection budgets changed")
    require(hor_config["relation_topk"] == 50 and hor_config["relation_score_floor"] == 0.0,
            "The common relation output configuration changed")
    output = ROOT / config["output_directory"]
    reports = ROOT / config["report_directory"]
    sources = read_lines(ROOT / "HOR/output/random500/predictions.jsonl")
    regions = read_lines(ROOT / config["source_region_predictions"])
    predictions = read_lines(output / "predictions.jsonl")
    plans = read_lines(output / "crop_plans.jsonl")
    prepared = read_json(output / "prepared_inputs.json")
    runtime = verify_inputs(config, sources, regions, predictions, plans, prepared)
    truth_scopes = verify_truths(config, sources, regions, hor_config["iou_threshold"])
    totals = {group: Counter() for group in GROUPS}
    border_errors = {group: {"selected_endpoint_pixels": 0.0, "crop_detection_pixels": 0.0} for group in GROUPS}
    for region, row, plan in zip(regions, predictions, plans):
        verify_queries(region, row, plan, config)
        for group in GROUPS:
            prediction = row["groups"][group]
            verify_merge(region, prediction, group, config)
            verify_relation_budget(row, group, config)
            width, height = region["image_size"]
            border_errors[group]["selected_endpoint_pixels"] = max(
                [border_errors[group]["selected_endpoint_pixels"]] +
                [border_overflow(item["box_xyxy"], (0, 0, width, height)) for item in prediction["objects"]])
            border_errors[group]["crop_detection_pixels"] = max(
                [border_errors[group]["crop_detection_pixels"]] +
                [border_overflow(item["box_xyxy"], query["crop_box_xyxy"]) for query in prediction["queries"]
                 for item in query["detections"]])
            totals[group].update({"endpoints": len(prediction["objects"]), "candidate_pairs": prediction["candidate_pairs"],
                                  "human_pairs_scored": prediction["human_pairs_scored"], "relations": len(prediction["relations"]),
                                  "queries": len(prediction["queries"]),
                                  "crop_input_pixels": sum(query["input_pixels"] for query in prediction["queries"]),
                                  "RA_routed_queries": sum(query["policy_source"] == "RA_relation_route" for query in prediction["queries"])})
    require(totals["geometry"]["queries"] == totals["RA_guided"]["queries"], "The two active policies used unequal detector-query budgets")
    require(prepared["detected_person_records"] * 2 == totals["geometry"]["queries"], "Detected-person query accounting differs")
    for group in GROUPS[1:]:
        require(prepared["planned_queries"][group] == totals[group]["queries"], "An executed query is absent from its plan")
    require(prepared["RA_routed_queries"] == totals["RA_guided"]["RA_routed_queries"], "RA-routed query accounting differs")
    expected = read_json(reports / "evaluation.json")
    require(set(expected) == set(GROUPS), "The reported evaluation groups differ")
    summary = {}
    measured_evaluation = {group: {} for group in GROUPS}
    diagnostics_checked = 0
    for group in GROUPS:
        require(set(expected[group]) == set(SCOPES), "The reported GT scopes differ")
        summary[group] = {}
        for scope in SCOPES:
            measured = evaluate_independently(sources, predictions, group, truth_scopes[scope], hor_config["iou_threshold"])
            measured_evaluation[group][scope] = measured
            for key, value in measured.items():
                compare_tree(value, expected[group][scope][key], f"{group}.{scope}.{key}")
            diagnostics_checked += measured["unique_gt"]
            summary[group][scope] = {"GT": measured["unique_gt"], "hits50": measured["hits"]["50"],
                                     "R@50": measured["metrics"]["R@50"], "mR@50": measured["metrics"]["mR@50"],
                                     "failure_stages": measured["failure_stages"]}
    verified_costs = verify_costs(predictions, reports)
    verified_published_records = verify_public_evidence(regions, predictions, plans, prepared, runtime, reports, config)
    verified_bootstrap = verify_bootstrap(sources, truth_scopes, measured_evaluation, reports, config)
    manifest_entries = verify_manifest(reports, config)
    signed_paths = [output / "predictions.jsonl", output / "crop_plans.jsonl", output / "prepared_inputs.json",
                    output / "runtime.json", reports / "evaluation.json"]
    print(json.dumps({"source_records": len(sources), "unique_source_image_hashes": len({row['image_sha256'] for row in sources}),
                      "independently_verified_GT_diagnostics": diagnostics_checked,
                      "verified_input_signatures": len(prepared["inputs_sha256"]), "verified_checkpoint_signatures": 3,
                      "crop_plans_recomputed_without_GT": True, "group_budgets": {key: dict(value) for key, value in totals.items()},
                      "coordinate_tolerance_pixels": BORDER_TOLERANCE_PIXELS, "maximum_border_overflow_pixels": border_errors,
                      "verified_compute_seconds": verified_costs, "verified_manifest_entries": manifest_entries,
                      "verified_published_paired_records": verified_published_records,
                      "independent_cluster_bootstrap": verified_bootstrap,
                      "metrics": summary, "runtime_peak_GPU_allocated_GiB": runtime["peak_GPU_allocated_GiB"],
                      "evidence_sha256": {path.relative_to(ROOT).as_posix(): digest(path) for path in signed_paths}},
                     ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
