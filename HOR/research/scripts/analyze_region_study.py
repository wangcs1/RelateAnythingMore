import argparse
from collections import Counter
import csv
from datetime import datetime
import json
from pathlib import Path
import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
HOR_DIR = ROOT / "HOR"
RESEARCH_DIR = HOR_DIR / "research"
sys.path.insert(0, str(HOR_DIR))
from evaluation import endpoint_matches
from pipeline import save_json, sha256


GROUPS = [
    "A_fasterrcnn_thing",
    "B_mask2former_thing",
    "C_fasterrcnn_thing_plus_stuff",
    "D_mask2former_thing_plus_stuff"
]
GROUP_LABELS = ["A: Faster R-CNN", "B: Mask2Former", "C: Faster R-CNN + stuff", "D: Mask2Former + stuff"]
GROUP_COLORS = ["#31688e", "#35b779", "#d1495b", "#edc949"]
STAGE_ORDER = ["hit50", "endpoint_missing_or_wrong_class", "pair_not_selected",
               "endpoints_collapsed_to_same_box", "wrong_predicate", "rank_below50"]


def read_json_lines(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def row_index(evaluation):
    return {item["index"]: item for item in evaluation["per_image"]}


def diagnostic_index(evaluation):
    result = {}
    for image in evaluation["per_image"]:
        for row in image["diagnostics"]:
            key = (image["index"], row["subject_id"], row["object_id"], row["predicate"])
            result[key] = row
    return result


def endpoint_source_rows(prediction, ids):
    objects = {item["id"]: item for item in prediction["objects"]}
    return [{key: objects[object_id].get(key) for key in (
        "id", "label", "category_id", "source", "source_object_key", "detection_score",
        "source_detection_id", "source_segment_id", "box_xyxy")}
        for object_id in sorted(set(ids)) if object_id in objects]


def correct_relation_rank(prediction, diagnostic, predicate):
    subjects = set(diagnostic["matching_subject_ids"])
    objects = set(diagnostic["matching_object_ids"])
    rows = [row for row in prediction["relations"]
            if row["subject_id"] in subjects and row["object_id"] in objects and row["predicate"] == predicate]
    return min((row["rank"] for row in rows), default=None)


def hit_changes(records, evaluations, recovery_loss):
    record_by_index = {record["index"]: record for record in records}
    detector_reference = {
        "C_fasterrcnn_thing_plus_stuff": "A_fasterrcnn_thing",
        "D_mask2former_thing_plus_stuff": "B_mask2former_thing"
    }
    detailed = {"all_gt": {}, "fixed_baseline_endpoint_valid": {}}
    source_counts = {"all_gt": {}, "fixed_baseline_endpoint_valid": {}}
    for scope, group_changes in recovery_loss.items():
        evaluation_name = "all_gt" if scope == "all_gt" else "fixed_baseline_endpoint_valid"
        baseline_diagnostics = diagnostic_index(evaluations[GROUPS[0]][evaluation_name])
        for group_name, change in group_changes.items():
            group_diagnostics = diagnostic_index(evaluations[group_name][evaluation_name])
            detector_reference_group = detector_reference.get(group_name)
            detector_reference_diagnostics = diagnostic_index(
                evaluations[detector_reference_group][evaluation_name]) if detector_reference_group else {}
            recovered = []
            lost = []
            mechanisms = Counter()
            for status, output_rows in (("recovered", recovered), ("lost", lost)):
                for source_row in change[f"{status}_vs_A"]:
                    key = (source_row["index"], source_row["subject_id"], source_row["object_id"],
                           source_row["predicate"])
                    old = baseline_diagnostics.get(key)
                    new = group_diagnostics.get(key)
                    if old is None or new is None:
                        raise ValueError(f"Missing GT diagnostic for relation {key}")
                    record = record_by_index[key[0]]
                    subject = record["ground_truth_objects"][key[1]]
                    obj = record["ground_truth_objects"][key[2]]
                    prediction = record["groups"][group_name]
                    old_prediction = record["groups"][GROUPS[0]]
                    new_sources = endpoint_source_rows(
                        prediction, new["matching_subject_ids"] + new["matching_object_ids"])
                    old_sources = endpoint_source_rows(
                        old_prediction, old["matching_subject_ids"] + old["matching_object_ids"])
                    stuff_match = any(item["source"] == "mask2former_stuff" for item in new_sources)
                    selected_keys = {item["source_object_key"] for item in prediction["objects"]}
                    same_detector_diagnostic = detector_reference_diagnostics.get(key)
                    same_detector_prediction = record["groups"].get(detector_reference_group)
                    same_detector_sources = endpoint_source_rows(
                        same_detector_prediction,
                        same_detector_diagnostic["matching_subject_ids"] +
                        same_detector_diagnostic["matching_object_ids"]
                    ) if same_detector_diagnostic else []
                    same_detector_keys = {item["source_object_key"] for item in same_detector_sources}
                    removed_keys = sorted(same_detector_keys - selected_keys)
                    if status == "recovered":
                        mechanism = "stuff_endpoint_matches_PSG_GT" if stuff_match else "thing_pair_or_relation_ranking_change"
                        rank = correct_relation_rank(prediction, new, key[3])
                    elif removed_keys and new["stage"] == "endpoint_missing_or_wrong_class":
                        mechanism = "thing_endpoint_removed_when_stuff_occupied_cap_slots"
                        rank = None
                    elif new["stage"] == "endpoint_missing_or_wrong_class" and group_name in (
                            "B_mask2former_thing", "D_mask2former_thing_plus_stuff"):
                        mechanism = "Mask2Former_thing_endpoint_not_matched_to_PSG_GT"
                        rank = None
                    elif new["stage"] == "endpoint_missing_or_wrong_class":
                        mechanism = "FasterRCNN_endpoint_match_unavailable_in_combined_group"
                        rank = None
                    elif new["stage"] == "pair_not_selected":
                        mechanism = "pair_not_selected_by_400_budget"
                        rank = None
                    elif new["stage"] == "wrong_predicate":
                        mechanism = "relation_model_selected_wrong_predicate"
                        rank = None
                    elif new["stage"] == "rank_below50":
                        mechanism = "correct_predicate_below_top50"
                        rank = None
                    else:
                        mechanism = new["stage"]
                        rank = None
                    mechanisms[mechanism] += 1
                    output_rows.append({
                        "change": status,
                        "index": key[0],
                        "sample_position": record["sample_position"],
                        "file_name": record["file_name"],
                        "ground_truth_subject": {"id": subject["id"], "label": subject["label"],
                                                  "box_xyxy": subject["box_xyxy"]},
                        "ground_truth_predicate": key[3],
                        "ground_truth_object": {"id": obj["id"], "label": obj["label"],
                                                "box_xyxy": obj["box_xyxy"]},
                        "baseline_stage": old["stage"],
                        "comparison_stage": new["stage"],
                        "mechanism": mechanism,
                        "baseline_matching_endpoints": old_sources,
                        "comparison_matching_endpoints": new_sources,
                        "same_detector_reference_group": detector_reference_group,
                        "same_detector_reference_matching_endpoints": same_detector_sources,
                        "baseline_matched_source_keys_removed": removed_keys,
                        "comparison_correct_relation_rank": rank
                    })
            recovered.sort(key=lambda row: (row["index"], row["ground_truth_subject"]["id"],
                                            row["ground_truth_object"]["id"], row["ground_truth_predicate"]))
            lost.sort(key=lambda row: (row["index"], row["ground_truth_subject"]["id"],
                                       row["ground_truth_object"]["id"], row["ground_truth_predicate"]))
            detailed[scope][group_name] = {"recovered_count": len(recovered), "lost_count": len(lost),
                                           "net_hit_change": len(recovered) - len(lost),
                                           "recovered": recovered, "lost": lost,
                                           "mechanism_counts": dict(mechanisms)}
            source_counts[scope][group_name] = dict(mechanisms)
    return detailed, source_counts


def all_failures(records, evaluations):
    record_by_index = {record["index"]: record for record in records}
    failures = {name: [] for name in GROUPS}
    stages = {name: Counter() for name in GROUPS}
    for group_name in GROUPS:
        evaluation = evaluations[group_name]["all_gt"]
        for image in evaluation["per_image"]:
            record = record_by_index[image["index"]]
            prediction = record["groups"][group_name]
            for diagnostic in image["diagnostics"]:
                stages[group_name][diagnostic["stage"]] += 1
                if diagnostic["stage"] == "hit50":
                    continue
                subject_id, object_id = diagnostic["subject_id"], diagnostic["object_id"]
                gt_objects = record["ground_truth_objects"]
                failures[group_name].append({
                    "index": image["index"],
                    "sample_position": record["sample_position"],
                    "file_name": record["file_name"],
                    "ground_truth_subject": {"id": subject_id, "label": gt_objects[subject_id]["label"],
                                              "box_xyxy": gt_objects[subject_id]["box_xyxy"]},
                    "ground_truth_predicate": diagnostic["predicate"],
                    "ground_truth_object": {"id": object_id, "label": gt_objects[object_id]["label"],
                                            "box_xyxy": gt_objects[object_id]["box_xyxy"]},
                    "failure_stage": diagnostic["stage"],
                    "matching_subject_endpoints": endpoint_source_rows(
                        prediction, diagnostic["matching_subject_ids"]),
                    "matching_object_endpoints": endpoint_source_rows(
                        prediction, diagnostic["matching_object_ids"])
                })
    return failures, {group_name: dict(counter) for group_name, counter in stages.items()}


def source_identity_audit(records):
    metadata_path = RESEARCH_DIR / "reports/decoder/evidence/calibration_image_splits.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    indexed = {}
    for split_rows in metadata["splits"].values():
        for row in split_rows:
            if row["index"] in indexed:
                raise ValueError(f"Duplicate image index in source identity metadata: {row['index']}")
            indexed[row["index"]] = row
    if set(indexed) != {record["index"] for record in records}:
        raise ValueError("Source identity metadata and region predictions have different image indices")
    groups = {}
    coco_identity = {}
    hash_identity = {}
    for record in records:
        row = indexed[record["index"]]
        if row["file_name"] != record["file_name"] or row["image_sha256"] != record["image_sha256"]:
            raise ValueError(f"Source identity metadata does not match region record {record['index']}")
        identity = row["identity_key"]
        coco_id = row["coco_image_id"]
        image_hash = row["image_sha256"]
        if coco_id is not None and coco_identity.setdefault(coco_id, identity) != identity:
            raise ValueError(f"One COCO image ID has several source identities: {coco_id}")
        if hash_identity.setdefault(image_hash, identity) != identity:
            raise ValueError(f"One image file SHA256 has several source identities: {image_hash}")
        groups.setdefault(identity, []).append(dict(row))
    audit = {
        "identity_metadata": str(metadata_path.relative_to(ROOT)),
        "identity_metadata_sha256": sha256(metadata_path),
        "definition": "Records sharing a COCO ID or image file SHA256 use one source identity; all records in a group are resampled together.",
        "record_count": len(records),
        "unique_source_identity_count": len(groups),
        "all_filenames_and_file_sha256_match_region_records": True,
        "duplicate_identity_groups": {identity: rows for identity, rows in groups.items() if len(rows) > 1},
        "identity_groups": groups
    }
    return audit, {index: row["identity_key"] for index, row in indexed.items()}


def bootstrap_intervals(evaluations, identity_by_index, seed=20261104, repetitions=20000):
    rng = np.random.default_rng(seed)
    result = {"seed": seed, "repetitions": repetitions, "confidence_level": 0.95,
              "unit": "paired source-image identity resampling; all PSG records from one COCO/image-file-SHA256 identity travel together",
              "point_estimate": "original PSG-record-weighted image macro recall and pooled relation recall; annotations are retained",
              "identity_metadata": "HOR/research/reports/decoder/evidence/calibration_image_splits.json",
              "comparisons": {}}
    for scope, evaluation_name in (("all_gt", "all_gt"),
                                   ("fixed_baseline_endpoint_valid", "fixed_baseline_endpoint_valid")):
        paired = {}
        reference = row_index(evaluations[GROUPS[0]][evaluation_name])
        indices = sorted(reference)
        for group_name in GROUPS:
            rows = row_index(evaluations[group_name][evaluation_name])
            if sorted(rows) != indices:
                raise ValueError(f"Per-image recall denominator mismatch in {scope}/{group_name}")
            if any(rows[index]["gt_count"] != reference[index]["gt_count"] for index in indices):
                raise ValueError(f"GT relation count mismatch in {scope}/{group_name}")
            paired[group_name] = rows
        identity_groups = {}
        for index in indices:
            identity_groups.setdefault(identity_by_index[index], []).append(index)
        clusters = [identity_groups[identity] for identity in sorted(identity_groups)]
        cluster_record_counts = np.asarray([len(cluster) for cluster in clusters], dtype=np.float64)
        draws = rng.integers(0, len(clusters), size=(repetitions, len(clusters)))
        sampled_record_counts = cluster_record_counts[draws].sum(axis=1)
        cluster_denominators = np.asarray(
            [sum(reference[index]["gt_count"] for index in cluster) for cluster in clusters], dtype=np.float64)
        sampled_gt_counts = cluster_denominators[draws].sum(axis=1)
        scope_rows = {}
        for group_name in GROUPS[1:]:
            baseline_ratios = np.asarray([reference[index]["R@50"] for index in indices])
            variant_ratios = np.asarray([paired[group_name][index]["R@50"] for index in indices])
            baseline_hits = np.asarray([reference[index]["hits50"] for index in indices], dtype=np.float64)
            variant_hits = np.asarray([paired[group_name][index]["hits50"] for index in indices], dtype=np.float64)
            denominators = np.asarray([reference[index]["gt_count"] for index in indices], dtype=np.float64)
            cluster_ratio_differences = np.asarray([
                sum(paired[group_name][index]["R@50"] - reference[index]["R@50"] for index in cluster)
                for cluster in clusters])
            cluster_hit_differences = np.asarray([
                sum(paired[group_name][index]["hits50"] - reference[index]["hits50"] for index in cluster)
                for cluster in clusters], dtype=np.float64)
            macro_differences = cluster_ratio_differences[draws].sum(axis=1) / sampled_record_counts
            pooled_differences = cluster_hit_differences[draws].sum(axis=1) / sampled_gt_counts
            scope_rows[group_name] = {
                "images": len(indices),
                "unique_source_identities": len(clusters),
                "duplicate_identity_groups": {identity: grouped for identity, grouped in identity_groups.items()
                                               if len(grouped) > 1},
                "observed_macro_R@50_difference": float(variant_ratios.mean() - baseline_ratios.mean()),
                "macro_R@50_difference_95pct_CI": [float(value) for value in np.quantile(macro_differences, [0.025, 0.975])],
                "observed_pooled_R@50_difference": float(
                    variant_hits.sum() / denominators.sum() - baseline_hits.sum() / denominators.sum()),
                "pooled_R@50_difference_95pct_CI": [float(value) for value in np.quantile(pooled_differences, [0.025, 0.975])]
            }
        result["comparisons"][scope] = scope_rows
    return result


def baseline_difference_audit(records, evaluations, input_dir):
    baseline_dir = HOR_DIR / "output/random500"
    baseline = {row["index"]: row for row in read_json_lines(baseline_dir / "predictions.jsonl")}
    if set(baseline) != {record["index"] for record in records}:
        raise ValueError("Original HOR and region predictions have different image indices")
    original_evaluation = json.loads((baseline_dir / "evaluation.json").read_text(encoding="utf-8"))[
        "detected/relations"]
    original_diagnostics = diagnostic_index(original_evaluation)
    current_diagnostics = diagnostic_index(evaluations[GROUPS[0]]["all_gt"])
    original_runtime = json.loads((baseline_dir / "runtime.json").read_text(encoding="utf-8"))
    current_runtime = json.loads((input_dir / "runtime.json").read_text(encoding="utf-8"))
    predicates = json.loads((ROOT / "data/PSG/packed/psg/test/meta.json").read_text(
        encoding="utf-8"))["predicates"]
    spatial_names = json.loads((HOR_DIR / "config.json").read_text(encoding="utf-8"))["spatial_predicates"]
    spatial = [index for index, name in enumerate(predicates) if name in spatial_names]
    semantic = [index for index in range(len(predicates)) if index not in spatial]
    rows = []
    changed_truth = []
    cache_signatures = {}
    totals = Counter()
    for record in records:
        index = record["index"]
        old_record = baseline[index]
        if (old_record["file_name"], old_record["image_sha256"]) != (
                record["file_name"], record["image_sha256"]):
            raise ValueError(f"Original HOR source image differs at {index}")
        old = old_record["detected"]
        current = record["groups"][GROUPS[0]]
        source_ids = {item["id"]: item["source_detection_id"] for item in current["objects"]}
        old_objects = {item["id"]: item for item in old["objects"]}
        if len(old_objects) != len(source_ids):
            raise ValueError(f"Region A changed the Faster R-CNN endpoint count at {index}")
        for item in current["objects"]:
            reference = old_objects[item["source_detection_id"]]
            if any(item[key] != reference[key] for key in ("label", "is_person", "box_xyxy", "detection_score")):
                raise ValueError(f"Region A changed a Faster R-CNN endpoint at {index}")
        old_top50 = [(row["subject_id"], row["object_id"], row["predicate_id"]) for row in old["relations"]]
        new_top50 = [(source_ids[row["subject_id"]], source_ids[row["object_id"]], row["predicate_id"])
                     for row in current["relations"]]
        row = {"index": index, "file_name": record["file_name"], "same_source_image_and_detection_endpoints": True,
               "object_count": len(old_objects), "original_pair_policy": old["pair_policy"],
               "region_A_pair_policy": current["pair_policy"], "original_candidate_count": old["candidate_pairs"],
               "region_A_candidate_count": current["candidate_pairs"],
               "original_relation_tensor_length": len(old_objects) ** 2 if old["candidate_pairs"] else 0,
               "region_A_relation_tensor_length": 400 if current["candidate_pairs"] else 0,
               "top50_identity_and_order_equal": old_top50 == new_top50,
               "top50_added": [list(item) for item in new_top50 if item not in set(old_top50)],
               "top50_removed": [list(item) for item in old_top50 if item not in set(new_top50)]}
        totals["images_with_equal_top50_identity_and_order"] += old_top50 == new_top50
        totals["original_candidate_pairs"] += old["candidate_pairs"]
        totals["region_A_candidate_pairs"] += current["candidate_pairs"]
        truth_changes = [key for key in original_diagnostics if key[0] == index and
                         (original_diagnostics[key]["stage"] == "hit50") !=
                         (current_diagnostics[key]["stage"] == "hit50")]
        full_ranks = {}
        if truth_changes:
            for label, prediction, mapping in (("original", old, {item: item for item in old_objects}),
                                               ("region_A", current, source_ids)):
                proposals = sorted((item for pair in prediction["all_human_pairs"] for item in pair["predictions"]),
                                   key=lambda item: (-item["fused_logit"], item["subject_id"],
                                                     item["object_id"], item["predicate_id"]))
                full_ranks[label] = {(mapping[item["subject_id"]], mapping[item["object_id"]], item["predicate_id"]): rank
                                     for rank, item in enumerate(proposals, 1)}
        if old["candidate_pairs"] or current["candidate_pairs"]:
            old_path = baseline_dir / "logits/detected" / f"{index:04d}.npz"
            new_path = input_dir / "logits" / GROUPS[0] / f"{index:04d}.npz"
            for path in (old_path, new_path):
                cache_signatures[str(path.relative_to(ROOT))] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
            with np.load(old_path) as old_cache, np.load(new_path) as new_cache:
                old_pairs = {(int(subject), int(obj)): position for position, (subject, obj) in enumerate(
                    zip(old_cache["subject_indices"], old_cache["object_indices"]))}
                new_pairs = {(source_ids[int(subject)], source_ids[int(obj)]): position
                             for position, (subject, obj) in enumerate(
                                 zip(new_cache["subject_indices"], new_cache["object_indices"]))}
                if len(old_pairs) != old["candidate_pairs"] or len(new_pairs) != current["candidate_pairs"]:
                    raise ValueError(f"Cached candidate identities do not match saved predictions at {index}")
                if set(new_pairs) - set(old_pairs):
                    raise ValueError(f"Region A contains a pair outside the original exhaustive set at {index}")
                shared = sorted(new_pairs)
                old_slots = [old_pairs[pair] for pair in shared]
                new_slots = [new_pairs[pair] for pair in shared]
                old_logits = old_cache["predicate_logits"][old_slots]
                new_logits = new_cache["predicate_logits"][new_slots]
                old_pair_logits = old_cache["pair_logits"][old_slots]
                new_pair_logits = new_cache["pair_logits"][new_slots]
                difference = np.abs(old_logits - new_logits)
                pair_difference = np.abs(old_pair_logits - new_pair_logits)
                stream_changed = ((old_logits[:, spatial].argmax(axis=1) != new_logits[:, spatial].argmax(axis=1)) |
                                  (old_logits[:, semantic].argmax(axis=1) != new_logits[:, semantic].argmax(axis=1)))
                row.update({"candidate_sets_equal": set(old_pairs) == set(new_pairs),
                            "shared_candidate_pairs": len(shared),
                            "shared_predicate_logits_bitwise_equal": bool(np.array_equal(old_logits, new_logits)),
                            "shared_predicate_logits_max_abs_difference": float(difference.max()),
                            "shared_predicate_logits_mean_abs_difference": float(difference.mean()),
                            "shared_pair_logits_max_abs_difference": float(pair_difference.max()),
                            "shared_pairs_with_changed_spatial_or_semantic_winner": int(stream_changed.sum())})
                totals["forward_images"] += 1
                totals["forward_images_with_equal_candidate_sets"] += row["candidate_sets_equal"]
                totals["forward_images_with_equal_candidate_sets_and_equal_tensor_length"] += (
                    row["candidate_sets_equal"] and
                    row["original_relation_tensor_length"] == row["region_A_relation_tensor_length"])
                totals["forward_images_with_equal_candidate_sets_and_different_tensor_length"] += (
                    row["candidate_sets_equal"] and
                    row["original_relation_tensor_length"] != row["region_A_relation_tensor_length"])
                totals["forward_images_with_bitwise_equal_shared_predicate_logits"] += row[
                    "shared_predicate_logits_bitwise_equal"]
                totals["shared_candidate_pairs"] += len(shared)
                totals["shared_pairs_with_changed_spatial_or_semantic_winner"] += int(stream_changed.sum())
                for key in truth_changes:
                    previous = original_diagnostics[key]
                    following = current_diagnostics[key]
                    predicate_id = predicates.index(key[3])
                    stream = spatial if predicate_id in spatial else semantic
                    endpoint_pairs = [(subject, obj) for subject in previous["matching_subject_ids"]
                                      for obj in previous["matching_object_ids"] if subject != obj]
                    pair_evidence = []
                    for pair in endpoint_pairs:
                        item = {"source_subject_id": pair[0], "source_object_id": pair[1],
                                "in_original_candidates": pair in old_pairs, "in_region_A_candidates": pair in new_pairs}
                        for label, cache, mapping, predicted in (("original", old_cache, old_pairs, old_top50),
                                                                 ("region_A", new_cache, new_pairs, new_top50)):
                            if pair not in mapping:
                                continue
                            logits = cache["predicate_logits"][mapping[pair]]
                            pair_logit = float(cache["pair_logits"][mapping[pair]])
                            winner_id = stream[int(logits[stream].argmax())]
                            target = (pair[0], pair[1], predicate_id)
                            item[label] = {"GT_predicate_logit": float(logits[predicate_id]), "pair_logit": pair_logit,
                                           "GT_fused_logit": float(logits[predicate_id]) + pair_logit,
                                           "GT_predicate_stream_rank": int(np.count_nonzero(
                                               logits[stream] > logits[predicate_id])) + 1,
                                           "stream_winner": predicates[winner_id],
                                           "stream_winner_logit": float(logits[winner_id]),
                                           "global_rank_before_top50": full_ranks[label].get(target),
                                           "top50_rank": predicted.index(target) + 1 if target in predicted else None}
                        pair_evidence.append(item)
                    change = "recovered" if following["stage"] == "hit50" else "lost"
                    failure_stage = previous["stage"] if change == "recovered" else following["stage"]
                    mechanisms = {"pair_not_selected": "candidate_pair_budget_removed_matching_pair",
                                  "wrong_predicate": "spatial_or_semantic_predicate_winner_changed",
                                  "rank_below50": "global_top50_relation_ranking_changed"}
                    changed_truth.append({"change": change, "index": index, "file_name": record["file_name"],
                                          "GT_subject": record["ground_truth_objects"][key[1]],
                                          "GT_object": record["ground_truth_objects"][key[2]], "GT_predicate": key[3],
                                          "original_stage": previous["stage"], "region_A_stage": following["stage"],
                                          "original_candidate_count": old["candidate_pairs"],
                                          "region_A_candidate_count": current["candidate_pairs"],
                                          "candidate_sets_equal": row["candidate_sets_equal"],
                                          "original_relation_tensor_length": row["original_relation_tensor_length"],
                                          "region_A_relation_tensor_length": row["region_A_relation_tensor_length"],
                                          "observed_change_mechanism": mechanisms.get(failure_stage, failure_stage),
                                          "matching_detection_pair_evidence": pair_evidence})
        elif truth_changes:
            raise ValueError(f"A GT hit changed without cached relation candidates at {index}")
        rows.append(row)
    return {
        "comparison": "original HOR exhaustive pair baseline versus region-study A with 400-pair budget",
        "original_metrics": original_evaluation["metrics"],
        "region_A_metrics": evaluations[GROUPS[0]]["all_gt"]["metrics"],
        "original_hits50": sum(item["hits50"] for item in original_evaluation["per_image"]),
        "region_A_hits50": sum(item["hits50"] for item in evaluations[GROUPS[0]]["all_gt"]["per_image"]),
        "GT_recovered": sum(item["change"] == "recovered" for item in changed_truth),
        "GT_lost": sum(item["change"] == "lost" for item in changed_truth),
        "summary": dict(totals),
        "shared_predicate_logits_max_abs_difference": max(
            row.get("shared_predicate_logits_max_abs_difference", 0.0) for row in rows),
        "shared_predicate_logits_max_abs_difference_when_candidate_sets_equal": max(
            row.get("shared_predicate_logits_max_abs_difference", 0.0) for row in rows
            if row.get("candidate_sets_equal", False)),
        "shared_pair_logits_max_abs_difference": max(
            row.get("shared_pair_logits_max_abs_difference", 0.0) for row in rows),
        "source_controls": {
            "same_seed": json.loads((HOR_DIR / "config.json").read_text(encoding="utf-8"))["seed"] ==
                         json.loads((input_dir / "run_config.json").read_text(encoding="utf-8"))[
                             "study_config"]["dataset"]["seed"],
            "same_HOR_pipeline_source_sha256": original_runtime["sources_sha256"]["pipeline.py"] == sha256(HOR_DIR / "pipeline.py"),
            "same_HOR_configuration_sha256": original_runtime["config_sha256"] == sha256(HOR_DIR / "config.json"),
            "same_relation_weights_sha256": original_runtime["resources_sha256"]["models\\relsgg-vits16plus\\model.pth"] ==
                                               current_runtime["resources_sha256"]["relation_weights"],
            "same_text_embedding_weights_sha256": original_runtime["resources_sha256"]["models\\relsgg-vits16plus\\text_student.pt"] ==
                                                     current_runtime["resources_sha256"]["relation_text_embeddings"],
            "same_torch_version": original_runtime["torch"] == current_runtime["torch"],
            "same_dtype": original_runtime["relation_dtype"] == current_runtime["relation_dtype"]
        },
        "interpretation": [
            "原HOR使用exhaustive=True，geo_budget/final_budget设为对象数平方；区域A使用exhaustive=False，两项预算均为400。",
            "推理的targets=None，采样器采用几何与相关性topk；该路径没有随机抽样，随机种子配置相同。",
            "相同检测边界框、模型权重和源图像经过不同候选集合或填充长度的关系前向；缓存直接记录共享候选logits与谓词赢家是否变化。",
            "关系Transformer同时处理候选关系，预算变化会影响候选上下文；缓存没有保存共享视觉特征，未独立分离上下文、张量长度与BF16数值效应。",
            "区域C相对A的增量仅使用本区域实验基线；原HOR解码实验的增量需要单独解释，不能将两项增量相加。"
        ],
        "changed_GT_relations": changed_truth,
        "per_image": rows,
        "logit_cache_signatures": cache_signatures
    }


def endpoint_summary(records):
    result = {}
    class_aware_endpoint_totals = {}
    for group_name in GROUPS:
        counts = Counter()
        total_boxes = []
        relation_candidate_counts = []
        human_pair_counts = []
        valid_forward_count = 0
        gt_people = matched_people = 0
        person_gt_images = person_detected_images = person_correct_images = no_person_false_images = 0
        unique_human_gt_endpoints = matched_human_gt_endpoints = 0
        stuff_class_counts = Counter()
        for record in records:
            gt_objects = record["ground_truth_objects"]
            prediction = record["groups"][group_name]
            predicted_objects = prediction["objects"]
            total_boxes.append(len(predicted_objects))
            counts.update(item["source"] for item in predicted_objects)
            relation_candidate_counts.append(prediction["candidate_pairs"])
            human_pair_counts.append(prediction["human_pairs_scored"])
            valid_forward_count += prediction["status"] == "ok"
            gt_person_objects = [item for item in gt_objects if item["is_person"]]
            detected_person_objects = [item for item in predicted_objects if item["is_person"]]
            gt_people += len(gt_person_objects)
            person_gt_images += bool(gt_person_objects)
            person_detected_images += bool(detected_person_objects)
            no_person_false_images += not gt_person_objects and bool(detected_person_objects)
            matches = endpoint_matches(predicted_objects, gt_objects, False)
            matched_person_images = any(matches[item["id"]] for item in gt_person_objects)
            person_correct_images += bool(gt_person_objects and matched_person_images)
            for item in gt_person_objects:
                matched_people += bool(matches[item["id"]])
            relation_endpoint_ids = {row[key] for row in record["ground_truth_relations"]
                                     if record["ground_truth_objects"][row["subject_id"]]["is_person"] or
                                     record["ground_truth_objects"][row["object_id"]]["is_person"]
                                     for key in ("subject_id", "object_id")}
            unique_human_gt_endpoints += len(relation_endpoint_ids)
            matched_human_gt_endpoints += sum(bool(matches[object_id]) for object_id in relation_endpoint_ids)
            for item in predicted_objects:
                if item["source"] == "mask2former_stuff":
                    stuff_class_counts[item["label"]] += 1
        class_aware_endpoint_totals[group_name] = {
            "GT_human_relation_unique_endpoints": unique_human_gt_endpoints,
            "matched_GT_human_relation_endpoints": matched_human_gt_endpoints,
            "GT_human_relation_endpoint_recall": matched_human_gt_endpoints / unique_human_gt_endpoints
            if unique_human_gt_endpoints else None
        }
        result[group_name] = {
            "selected_source_counts": dict(counts),
            "selected_endpoints_total": int(sum(total_boxes)),
            "selected_endpoints_mean_per_image": float(np.mean(total_boxes)),
            "selected_endpoints_median_per_image": float(np.median(total_boxes)),
            "selected_endpoints_p90_per_image": float(np.quantile(total_boxes, 0.9)),
            "selected_endpoints_max_per_image": int(max(total_boxes)),
            "images_at_40_endpoint_cap": int(sum(value == 40 for value in total_boxes)),
            "GT_person_objects": gt_people,
            "matched_GT_person_objects_IoU05_class_aware": matched_people,
            "person_box_recall": matched_people / gt_people if gt_people else None,
            "GT_person_images": int(person_gt_images),
            "images_with_predicted_person": int(person_detected_images),
            "GT_person_images_with_matched_prediction": int(person_correct_images),
            "GT_person_image_recall": person_correct_images / person_gt_images if person_gt_images else None,
            "no_person_images_with_false_person_detection": int(no_person_false_images),
            "relation_model_forward_count": int(valid_forward_count),
            "relation_candidate_pairs_total": int(sum(relation_candidate_counts)),
            "relation_candidate_pairs_per_forward_mean": float(np.mean(
                [value for value in relation_candidate_counts if value > 0])) if any(relation_candidate_counts) else 0.0,
            "human_directed_pairs_scored_total": int(sum(human_pair_counts)),
            "stuff_class_counts": dict(stuff_class_counts),
            **class_aware_endpoint_totals[group_name]
        }
    return result


def predicate_comparison(evaluations, output_path):
    rows = []
    predicates = evaluations[GROUPS[0]]["all_gt"]["per_class"]
    predicate_names = json.loads((ROOT / "data/PSG/packed/psg/test/meta.json").read_text(
        encoding="utf-8"))["predicates"]
    for predicate_id, reference in predicates.items():
        row = {"predicate_id": predicate_id, "predicate": predicate_names[int(predicate_id)],
               "GT_count": reference["gt"]}
        for group_name in GROUPS:
            metrics = evaluations[group_name]["all_gt"]["per_class"].get(predicate_id)
            row[f"{group_name}_hits50"] = metrics["hits50"] if metrics else 0
            row[f"{group_name}_pooled_R@50"] = metrics["pooled_R@50"] if metrics else 0.0
            row[f"{group_name}_image_macro_R@50"] = metrics["image_macro_R@50"] if metrics else 0.0
        rows.append(row)
    rows.sort(key=lambda row: (-row["GT_count"], int(row["predicate_id"])))
    with Path(output_path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def plot_metrics(evaluations, output_dir):
    figure, axes = plt.subplots(1, 2, figsize=(15, 5.5), constrained_layout=True)
    positions = np.arange(len(GROUPS))
    width = 0.35
    for axis, scope, title in ((axes[0], "all_gt", "全部968条人相关GT关系"),
                               (axes[1], "fixed_baseline_endpoint_valid", "固定530条原检测端点有效GT关系")):
        recalls = [evaluations[group][scope]["metrics"]["R@50"] for group in GROUPS]
        mean_recalls = [evaluations[group][scope]["metrics"]["mR@50"] for group in GROUPS]
        axis.bar(positions - width / 2, recalls, width, label="R@50", color="#31688e")
        axis.bar(positions + width / 2, mean_recalls, width, label="mR@50", color="#edc949")
        axis.set_title(title.replace("全部968条人相关GT关系", "All 968 human-related GT relations")
                        .replace("固定530条原检测端点有效GT关系", "Fixed 530 endpoint-valid GT relations"))
        axis.set_ylabel("Recall")
        axis.set_ylim(0, 0.55)
        axis.set_xticks(positions, GROUP_LABELS, rotation=15, ha="right")
        axis.grid(axis="y", alpha=0.25)
        axis.legend(frameon=False)
        for x, value in zip(positions - width / 2, recalls):
            axis.text(x, value + 0.008, f"{value:.3f}", ha="center", fontsize=8)
        for x, value in zip(positions + width / 2, mean_recalls):
            axis.text(x, value + 0.008, f"{value:.3f}", ha="center", fontsize=8)
    figure.savefig(output_dir / "r50_mr50_comparison.png", dpi=180)
    plt.close(figure)


def plot_failure_stages(stage_summary, output_dir):
    counts = {group: stage_summary[group] for group in GROUPS}
    figure, axis = plt.subplots(figsize=(13, 6), constrained_layout=True)
    positions = np.arange(len(GROUPS))
    base = np.zeros(len(GROUPS))
    colors = {"hit50": "#35b779", "endpoint_missing_or_wrong_class": "#d1495b",
              "pair_not_selected": "#edc949", "endpoints_collapsed_to_same_box": "#756bb1",
              "wrong_predicate": "#31688e", "rank_below50": "#8c564b"}
    labels = {"hit50": "Top-50 hit", "endpoint_missing_or_wrong_class": "Endpoint miss/class mismatch",
              "pair_not_selected": "Not selected", "endpoints_collapsed_to_same_box": "Same-box collapse",
              "wrong_predicate": "Wrong predicate", "rank_below50": "Correct predicate below Top-50"}
    for stage in STAGE_ORDER:
        heights = np.asarray([counts[group].get(stage, 0) for group in GROUPS])
        axis.bar(positions, heights, bottom=base, label=labels[stage], color=colors[stage])
        base += heights
    axis.set_xticks(positions, GROUP_LABELS, rotation=12, ha="right")
    axis.set_ylabel("GT relation count")
    axis.set_title("Failure stage counts over all human-related GT relations")
    axis.grid(axis="y", alpha=0.2)
    axis.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    figure.savefig(output_dir / "failure_stage_counts.png", dpi=180)
    plt.close(figure)


def plot_stuff_classes(endpoint_stats, output_dir):
    counts = Counter(endpoint_stats[GROUPS[2]]["stuff_class_counts"])
    labels = [label for label, _ in counts.most_common(20)]
    values = [counts[label] for label in labels]
    figure, axis = plt.subplots(figsize=(11, 6), constrained_layout=True)
    axis.barh(labels[::-1], values[::-1], color="#d1495b")
    axis.set_xlabel("Selected stuff endpoints over 500 images")
    axis.set_title("Selected stuff endpoint classes in group C (top 20)")
    axis.grid(axis="x", alpha=0.2)
    figure.savefig(output_dir / "stuff_endpoint_class_counts.png", dpi=180)
    plt.close(figure)


def markdown_recovery_appendix(detailed, output_path):
    sections = ["# A组对照的新增与丢失GT关系清单", "",
                "变化以Top-50是否命中作为判断。每一行是一条PSG标注关系；索引、图片文件名、GT端点类别、谓词、A组阶段、比较组阶段和端点/预算机制均逐条列出。完整结构化记录见同目录 `recovery_loss_cases.json`。", ""]
    for scope, scope_label in (("all_gt", "全部968条人相关GT关系"),
                               ("fixed_baseline_endpoint_valid", "固定530条原检测端点有效GT关系")):
        sections.extend([f"## {scope_label}", ""])
        for group_name in GROUPS[1:]:
            group = detailed[scope][group_name]
            sections.extend([f"### {group_name}", "",
                             f"恢复{group['recovered_count']}条，丢失{group['lost_count']}条，命中净变化{group['net_hit_change']:+d}条。", "",
                             "|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|", "|---|---:|---:|---|---|---|---|---|---|---|"])
            for status in ("recovered", "lost"):
                for row in group[status]:
                    subject = row["ground_truth_subject"]
                    obj = row["ground_truth_object"]
                    sections.append(
                        f"|{status}|{row['sample_position']}|{row['index']}|{row['file_name']}|"
                        f"{subject['id']}:{subject['label']}|{row['ground_truth_predicate']}|"
                        f"{obj['id']}:{obj['label']}|{row['baseline_stage']}|{row['comparison_stage']}|"
                        f"{row['mechanism']}|")
            sections.append("")
    Path(output_path).write_text("\n".join(sections), encoding="utf-8")


def markdown_failure_appendix(failures, output_path):
    sections = ["# 全组失败关系逐条审计", "",
                "以下清单覆盖全部500张固定样本中未命中Top-50的人相关PSG关系。端点来源和候选框编号来自对应组实际输入。完整结构化文件见 `failure_cases.json`。", ""]
    for group_name in GROUPS:
        sections.extend([f"## {group_name}", "",
                         f"未命中{len(failures[group_name])}条。", "",
                         "|序号|索引|图片|GT主语|谓词|GT宾语|失败阶段|匹配主语候选|匹配宾语候选|",
                         "|---:|---:|---|---|---|---|---|---|---|"])
        for row in failures[group_name]:
            subject = row["ground_truth_subject"]
            obj = row["ground_truth_object"]
            subjects = "; ".join(f"{item['id']}:{item['label']}[{item['source']}]{item['source_object_key']}"
                                  for item in row["matching_subject_endpoints"])
            objects = "; ".join(f"{item['id']}:{item['label']}[{item['source']}]{item['source_object_key']}"
                                 for item in row["matching_object_endpoints"])
            sections.append(f"|{row['sample_position']}|{row['index']}|{row['file_name']}|"
                            f"{subject['id']}:{subject['label']}|{row['ground_truth_predicate']}|"
                            f"{obj['id']}:{obj['label']}|{row['failure_stage']}|{subjects}|{objects}|")
        sections.append("")
    Path(output_path).write_text("\n".join(sections), encoding="utf-8")


def write_runtime_evidence(records, input_dir, output_dir):
    runtime = json.loads((input_dir / "runtime.json").read_text(encoding="utf-8"))
    profile = json.loads((input_dir / "compute_profile.json").read_text(encoding="utf-8"))
    expected_inputs = {
        "region_predictions": input_dir / "region_predictions.jsonl",
        "panoptic_candidates": input_dir / "mask2former_candidates.jsonl",
        "fixed_manifest": ROOT / "HOR/output/random500/sample_manifest.json",
    }
    for name, path in expected_inputs.items():
        if profile["input_sha256"][name] != sha256(path):
            raise ValueError(f"Timing profile does not match the current input: {name}")
    if runtime["images"] != len(records) or profile["images"] != len(records):
        raise ValueError("Runtime and profile image counts differ from the region predictions")
    if profile["weights_sha256"] != runtime["resources_sha256"]["mask2former_weights"]:
        raise ValueError("Timing profile and main run used different Mask2Former weights")
    for name in GROUPS:
        predictions = [record["groups"][name] for record in records]
        actual_forwards = sum(prediction["candidate_pairs"] > 0 for prediction in predictions)
        actual_pairs = sum(prediction["candidate_pairs"] for prediction in predictions)
        group = profile["relation_group_times"][name]
        if group["model_forward_images"] != actual_forwards or group["candidate_pair_total"] != actual_pairs:
            raise ValueError(f"Timing counts differ from current region predictions: {name}")
    evidence_dir = output_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for name in ("runtime.json", "compute_profile.json"):
        shutil.copy2(input_dir / name, evidence_dir / name)
    detection = profile["mask2former_panoptic_detection"]
    relation_forward_seconds = sum(group["forward_time"]["total_seconds"]
                                   for group in profile["relation_group_times"].values())
    relation_pipeline_seconds = sum(group["all_image_relation_pipeline_time"]["total_seconds"]
                                    for group in profile["relation_group_times"].values())
    forward_count = sum(group["model_forward_images"] for group in profile["relation_group_times"].values())
    lines = ["# 区域实验运行成本与重复执行证据", "",
             "本附录由`analyze_region_study.py`读取当前主运行和独立计时JSON自动生成。完整原始数值见[主运行记录](evidence/runtime.json)和[独立计时记录](evidence/compute_profile.json)，两份文件均直接复制实际运行结果。", "",
             f"主运行记录时间为`{runtime['created']}`，独立计时记录时间为`{profile['created']}`。两者覆盖{len(records)}条固定图像记录；独立计时中的输入SHA256与当前关系预测、区域候选和固定清单逐项一致。", "",
             "## 计时范围", "",
             "两个总用时都从模型加载完成后开始。主运行总用时覆盖各张图像的推理和结果写入。独立计时按CUDA同步后的墙钟时间统计；检测用时覆盖预处理、模型前向、后处理及区域转边界框，单张图像的原始读取与RGB转换发生在该检测计时段之前。", "",
             "关系有效前向用时只汇总候选对非空的调用；全图像关系处理用时同时包含候选为空时的处理。独立计时总用时还包含图像读取、循环和与缓存比较等开销，这些开销没有分别计时。主运行与独立计时分别执行，表内两次总用时各自报告。", "",
             "## 当前运行数值", "", "| 指标 | 数值 |", "|---|---:|",
             f"| 主运行总用时 | {runtime['total_seconds']:.9f}秒 |",
             f"| 主运行平均每条记录用时 | {runtime['average_seconds_per_image']:.9f}秒 |",
             f"| 独立计时总用时 | {profile['total_profile_wall_seconds']:.9f}秒 |",
             f"| Mask2Former检测次数 | {detection['count']} |",
             f"| Mask2Former检测总用时 | {detection['total_seconds']:.9f}秒 |",
             f"| 检测平均 / 中位数 / P90 | {1000*detection['mean_seconds']:.6f} / {1000*detection['median_seconds']:.6f} / {1000*detection['p90_seconds']:.6f}毫秒 |",
             f"| 四组有效关系前向次数 | {forward_count} |",
             f"| 四组有效关系前向总用时 | {relation_forward_seconds:.9f}秒 |",
             f"| 四组全图像关系处理总用时 | {relation_pipeline_seconds:.9f}秒 |",
             f"| 主运行PyTorch峰值已分配显存 | {runtime['peak_GPU_allocated_GiB']:.9f} GiB |",
             f"| 独立计时PyTorch峰值已分配显存 | {profile['peak_GPU_allocated_GiB']:.9f} GiB |", "",
             "| 组别 | 有效前向次数 | 候选关系对总数 | 有效前向总用时（秒） | 平均 / 中位数 / P90（毫秒） | 全图像关系处理总用时（秒） |",
             "|---|---:|---:|---:|---|---:|"]
    for name in GROUPS:
        group = profile["relation_group_times"][name]
        timing = group["forward_time"]
        lines.append(f"| {name} | {group['model_forward_images']} | {group['candidate_pair_total']:,} | "
                     f"{timing['total_seconds']:.9f} | {1000*timing['mean_seconds']:.6f} / "
                     f"{1000*timing['median_seconds']:.6f} / {1000*timing['p90_seconds']:.6f} | "
                     f"{group['all_image_relation_pipeline_time']['total_seconds']:.9f} |")
    lines.extend(["", "P90为90%分位数；GiB为2的30次方字节。设备为`" + runtime["GPU"] + "`。",
                  f"独立计时在模型加载前记录的CUDA可用显存为{profile['cuda_free_bytes_before_models']:,}字节，设备可见总显存为{profile['cuda_total_bytes']:,}字节。PyTorch峰值已分配显存只描述该实验进程的张量分配，系统其他进程的显存占用未在本次记录中单独测量。", "",
                  "## 重复执行一致性", "", "| 检查项 | 与主运行一致的记录数或差值 |", "|---|---:|",
                  f"| 检测区域身份 | {profile['detector_topology_match_images']} / {profile['images']} |",
                  f"| 检测区域身份和边界框 | {profile['detector_topology_and_box_match_images']} / {profile['images']} |",
                  f"| 检测分数最大绝对差 | {profile['detector_max_abs_score_difference']} |"])
    for name in GROUPS:
        lines.append(f"| {name}：关系Top-50身份与排序 | {profile['relation_top50_identity_match_counts'][name]} / {profile['images']} |")
    lines.extend(["", "上述一致性描述当前版本、权重和未融合query区域协议下的重复执行，相关加载与后处理定义见[Mask2Former审计](mask2former_loading_and_postprocessing_audit.md)。", "",
                  "## 原始证据签名", "", "| 记录 | SHA256 |", "|---|---|"])
    for name in ("runtime.json", "compute_profile.json"):
        lines.append(f"| [{name}](evidence/{name}) | `{sha256(input_dir / name)}` |")
    lines.extend(["", "执行环境来自主运行记录：", "",
                  f"- Python {runtime['python']}；PyTorch {runtime['torch']}；torchvision {runtime['torchvision']}；Transformers {runtime['transformers']}。",
                  f"- 关系模型精度：`{runtime['relation_dtype']}`；Mask2Former精度：`{runtime['mask2former_dtype']}`。", "",
                  "```powershell", ".\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\analyze_region_study.py", "```", ""])
    (output_dir / "runtime_evidence.md").write_text("\n".join(lines), encoding="utf-8")
    return {"main_seconds": runtime["total_seconds"], "profile_seconds": profile["total_profile_wall_seconds"],
            "detection_seconds": detection["total_seconds"], "relation_pipeline_seconds": relation_pipeline_seconds,
            "generated_report": "runtime_evidence.md"}


def main():
    parser = argparse.ArgumentParser(description="Audit and visualize the completed 500-image region study")
    parser.add_argument("--input", default=str(RESEARCH_DIR / "output/regions"))
    parser.add_argument("--output", default=str(RESEARCH_DIR / "reports/regions"))
    args = parser.parse_args()
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = read_json_lines(input_dir / "region_predictions.jsonl")
    if len(records) != 500:
        raise ValueError(f"Expected 500 completed records, found {len(records)}")
    if len({record["index"] for record in records}) != 500:
        raise ValueError("Region prediction indices are not unique")
    evaluations = json.loads((input_dir / "evaluation.json").read_text(encoding="utf-8"))
    recovery_loss = json.loads((input_dir / "recovery_loss.json").read_text(encoding="utf-8"))
    run_summary = json.loads((input_dir / "run_summary.json").read_text(encoding="utf-8"))
    endpoint_stats = endpoint_summary(records)
    detailed_changes, change_mechanisms = hit_changes(records, evaluations, recovery_loss)
    failures, stage_summary = all_failures(records, evaluations)
    identity_audit, identity_by_index = source_identity_audit(records)
    bootstrap = bootstrap_intervals(evaluations, identity_by_index)
    baseline_difference = baseline_difference_audit(records, evaluations, input_dir)
    runtime_evidence = write_runtime_evidence(records, input_dir, output_dir)
    save_json(output_dir / "source_identity_audit.json", identity_audit)
    save_json(output_dir / "baseline_difference_audit.json", baseline_difference)
    class_rows = predicate_comparison(evaluations, output_dir / "predicate_comparison.csv")
    save_json(output_dir / "endpoint_audit.json", endpoint_stats)
    save_json(output_dir / "recovery_loss_cases.json", detailed_changes)
    save_json(output_dir / "recovery_mechanism_counts.json", change_mechanisms)
    save_json(output_dir / "failure_cases.json", failures)
    save_json(output_dir / "failure_stage_counts.json", stage_summary)
    save_json(output_dir / "bootstrap_intervals.json", bootstrap)
    save_json(output_dir / "predicate_comparison.json", class_rows)
    markdown_recovery_appendix(detailed_changes, output_dir / "recovery_loss_cases.md")
    markdown_failure_appendix(failures, output_dir / "failure_cases.md")
    plot_metrics(evaluations, output_dir)
    plot_failure_stages(stage_summary, output_dir)
    plot_stuff_classes(endpoint_stats, output_dir)
    for group_name in GROUPS:
        source_image = input_dir / "visuals" / group_name / "0295_objects.jpg"
        report_image = output_dir / "visuals" / group_name / source_image.name
        report_image.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, report_image)
    resource_paths = [
        HOR_DIR / "research/configs/region_study.json",
        HOR_DIR / "research/scripts/region_study.py",
        HOR_DIR / "research/scripts/analyze_region_study.py",
        HOR_DIR / "research/scripts/profile_region_study.py",
        HOR_DIR / "research/scripts/audit_mask2former.py",
        HOR_DIR / "pipeline.py",
        HOR_DIR / "config.json",
        HOR_DIR / "evaluation.py",
        HOR_DIR / "run_500.py",
        ROOT / "RelateAnything/relsgg/checkpoint.py",
        ROOT / "RelateAnything/relsgg/config.py",
        ROOT / "RelateAnything/relsgg/scoring.py",
        ROOT / "RelateAnything/relsgg/model/relsgg.py",
        ROOT / "RelateAnything/relsgg/model/backbone.py",
        ROOT / "RelateAnything/relsgg/model/deformable.py",
        ROOT / "RelateAnything/relsgg/model/geometry.py",
        ROOT / "RelateAnything/relsgg/model/pooling.py",
        ROOT / "RelateAnything/relsgg/model/sampler.py",
        ROOT / "RelateAnything/relsgg/model/transformer.py",
        ROOT / "RelateAnything/relsgg/model/vocab_head.py",
        ROOT / "RelateAnything/relsgg/text/student.py",
        ROOT / "RelateAnything/relsgg/vocabulary.py",
        ROOT / "HOR/output/random500/sample_manifest.json",
        ROOT / "HOR/output/random500/predictions.jsonl",
        ROOT / "HOR/output/random500/evaluation.json",
        ROOT / "HOR/output/random500/runtime.json",
        ROOT / "data/PSG/packed/psg/test/meta.json",
        RESEARCH_DIR / "reports/decoder/evidence/calibration_image_splits.json",
        RESEARCH_DIR / "data/visual_genome_metadata/image_data.json",
        RESEARCH_DIR / "data/coco_annotations/annotations/person_keypoints_val2017.json",
        ROOT / "models/relsgg-vits16plus/model.pth",
        ROOT / "models/relsgg-vits16plus/text_student.pt",
        HOR_DIR / "research/models/mask2former-swin-tiny-coco-panoptic/config.json",
        HOR_DIR / "research/models/mask2former-swin-tiny-coco-panoptic/preprocessor_config.json",
        HOR_DIR / "research/models/mask2former-swin-tiny-coco-panoptic/model.safetensors",
        input_dir / "run_config.json",
        input_dir / "run_summary.json",
        input_dir / "runtime.json",
        input_dir / "compute_profile.json",
        input_dir / "visualization_manifest.json",
        input_dir / "region_predictions.jsonl",
        input_dir / "mask2former_candidates.jsonl",
        input_dir / "evaluation.json",
        input_dir / "recovery_loss.json",
        output_dir / "endpoint_audit.json",
        output_dir / "bootstrap_intervals.json",
        output_dir / "source_identity_audit.json",
        output_dir / "baseline_difference_audit.json",
        output_dir / "rights_metadata.json",
        output_dir / "recovery_loss_cases.json",
        output_dir / "recovery_loss_cases.md",
        output_dir / "recovery_mechanism_counts.json",
        output_dir / "failure_cases.json",
        output_dir / "failure_cases.md",
        output_dir / "failure_stage_counts.json",
        output_dir / "predicate_comparison.csv",
        output_dir / "predicate_comparison.json",
        output_dir / "r50_mr50_comparison.png",
        output_dir / "failure_stage_counts.png",
        output_dir / "stuff_endpoint_class_counts.png",
        output_dir / "mask2former_loading_and_postprocessing_audit.md",
        output_dir / "mask2former_loading_audit.json",
        output_dir / "runtime_evidence.md",
        output_dir / "evidence/runtime.json",
        output_dir / "evidence/compute_profile.json",
        input_dir / "visuals/A_fasterrcnn_thing/0295_objects.jpg",
        input_dir / "visuals/B_mask2former_thing/0295_objects.jpg",
        input_dir / "visuals/C_fasterrcnn_thing_plus_stuff/0295_objects.jpg",
        input_dir / "visuals/D_mask2former_thing_plus_stuff/0295_objects.jpg",
        output_dir / "visuals/A_fasterrcnn_thing/0295_objects.jpg",
        output_dir / "visuals/B_mask2former_thing/0295_objects.jpg",
        output_dir / "visuals/C_fasterrcnn_thing_plus_stuff/0295_objects.jpg",
        output_dir / "visuals/D_mask2former_thing_plus_stuff/0295_objects.jpg",
        output_dir / "thing_stuff_region_study.md"
    ]
    artifact_manifest = {
        "study": "A_thing_stuff_region_comparison",
        "created_utc_or_local": datetime.now().astimezone().isoformat(),
        "500_image_run_seconds": run_summary["runtime_seconds"],
        "panoptic_region_protocol": {
            "definition": "unfused query regions; multiple regions of one stuff class are retained",
            "label_ids_to_fuse_argument_provided": False,
            "effective_fusion_label_ids": [],
            "audit_report": "mask2former_loading_and_postprocessing_audit.md"},
        "runtime_evidence": runtime_evidence,
        "artifacts": {str(path.relative_to(ROOT)): {"bytes": path.stat().st_size, "sha256": sha256(path)}
                      for path in resource_paths}
    }
    save_json(output_dir / "artifact_manifest.json", artifact_manifest)
    print(json.dumps({
        "images": len(records),
        "runtime_evidence": runtime_evidence,
        "metrics": {group: evaluations[group]["all_gt"]["metrics"] for group in GROUPS},
        "fixed530_metrics": {group: evaluations[group]["fixed_baseline_endpoint_valid"]["metrics"]
                             for group in GROUPS},
        "endpoint_audit": endpoint_stats,
        "bootstrap": bootstrap,
        "change_mechanisms": change_mechanisms,
        "failure_stages": stage_summary,
        "report_directory": str(output_dir)
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
