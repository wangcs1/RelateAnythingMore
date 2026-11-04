import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np
from PIL import Image
import torch
import torchvision
import transformers
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation


ROOT = Path(__file__).resolve().parents[3]
HOR_DIR = ROOT / "HOR"
RESEARCH_DIR = HOR_DIR / "research"
CONFIG_PATH = RESEARCH_DIR / "configs/region_study.json"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
sys.path.insert(0, str(HOR_DIR))
from evaluation import endpoint_matches, evaluate
from pipeline import HumanRelationPipeline, draw_objects, save_json, sha256


def read_json_lines(path):
    path = Path(path)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def psg_categories(root):
    path = root / "data/PSG/packed/psg/test/meta.json"
    return json.loads(path.read_text(encoding="utf-8"))["categories"]


def object_summary(item):
    return {key: item[key] for key in (
        "id", "label", "category_id", "source", "source_object_key", "detection_score",
        "source_detection_id", "source_segment_id", "box_xyxy", "mask_area_pixels") if key in item}


class PanopticRegionDetector:
    def __init__(self, root, device, categories):
        model_dir = root / CONFIG["detector"]["local_directory"]
        weight_path = model_dir / CONFIG["detector"]["weights_file"]
        if not weight_path.is_file():
            raise FileNotFoundError(f"Official Mask2Former weights are missing: {weight_path}")
        actual_sha = sha256(weight_path)
        expected_sha = CONFIG["detector"]["weights_sha256"]
        if actual_sha != expected_sha:
            raise ValueError(f"Mask2Former weight SHA256 mismatch: {actual_sha} != {expected_sha}")
        self.processor = AutoImageProcessor.from_pretrained(model_dir, local_files_only=True)
        self.model = Mask2FormerForUniversalSegmentation.from_pretrained(
            model_dir, local_files_only=True).to(device).eval()
        self.device = device
        self.categories = categories
        self.category_ids = {name: index for index, name in enumerate(categories)}
        labels = {int(index): label for index, label in self.model.config.id2label.items()}
        aliases = CONFIG["detector"]["stuff_label_aliases"]
        if len(labels) != CONFIG["detector"]["panoptic_class_count"]:
            raise ValueError(f"Expected 133 model labels, found {len(labels)}")
        if len(categories) != CONFIG["detector"]["panoptic_class_count"]:
            raise ValueError(f"Expected 133 PSG categories, found {len(categories)}")
        for category_id, raw_label in labels.items():
            label = aliases.get(raw_label, raw_label)
            if category_id >= CONFIG["detector"]["thing_class_count"] and label not in self.category_ids:
                raise ValueError(f"Unmapped Mask2Former stuff label {raw_label!r} at {category_id}")
            if category_id < CONFIG["detector"]["thing_class_count"] and label != categories[category_id]:
                raise ValueError(f"Mask2Former thing class mismatch at {category_id}: {label!r}")
            if category_id >= CONFIG["detector"]["thing_class_count"] and self.category_ids[label] != category_id:
                raise ValueError(f"Mask2Former stuff class mismatch at {category_id}: {label!r}")
        self.labels = labels
        self.sha256 = actual_sha

    @torch.inference_mode()
    def detect(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {name: value.to(self.device) for name, value in inputs.items()}
        with torch.autocast("cuda", dtype=torch.bfloat16):
            outputs = self.model(**inputs)
        result = self.processor.post_process_panoptic_segmentation(
            outputs,
            target_sizes=[(image.height, image.width)],
            threshold=CONFIG["detector"]["score_threshold"],
            mask_threshold=CONFIG["detector"]["mask_threshold"],
            overlap_mask_area_threshold=CONFIG["detector"]["overlap_mask_area_threshold"])[0]
        segmentation = result["segmentation"].cpu()
        candidates = []
        for segment in result["segments_info"]:
            label_id = int(segment["label_id"])
            if label_id not in self.labels:
                raise ValueError(f"Mask2Former produced unknown label id {label_id}")
            raw_label = self.labels[label_id]
            label = CONFIG["detector"]["stuff_label_aliases"].get(raw_label, raw_label)
            category_id = self.category_ids[label]
            segment_id = int(segment["id"])
            ys, xs = torch.where(segmentation == segment_id)
            if not len(xs):
                continue
            x1, x2 = int(xs.min()), int(xs.max()) + 1
            y1, y2 = int(ys.min()), int(ys.max()) + 1
            if x2 <= x1 or y2 <= y1:
                raise ValueError(f"Invalid panoptic mask extent for segment {segment_id}")
            kind = "thing" if label_id < CONFIG["detector"]["thing_class_count"] else "stuff"
            candidates.append({
                "id": -1,
                "label": label,
                "model_label": raw_label,
                "category_id": category_id,
                "is_person": label == "person",
                "box_xyxy": [x1, y1, x2, y2],
                "detection_score": float(segment["score"]),
                "source": f"mask2former_{kind}",
                "source_category_id": label_id,
                "source_segment_id": segment_id,
                "source_object_key": f"mask2former:{label_id:03d}:{segment_id:06d}",
                "mask_area_pixels": int(len(xs))
            })
        return candidates


def normalize_fasterrcnn_objects(objects, categories):
    category_ids = {name: index for index, name in enumerate(categories)}
    normalized = []
    for source in objects:
        item = dict(source)
        if item["label"] not in category_ids:
            raise ValueError(f"Faster R-CNN label is outside PSG vocabulary: {item['label']}")
        item["source_category_id"] = item["category_id"]
        item["category_id"] = category_ids[item["label"]]
        item["source"] = "fasterrcnn_thing"
        item["source_detection_id"] = int(source["id"])
        item["source_object_key"] = f"fasterrcnn:{int(source['id']):06d}"
        item["id"] = -1
        normalized.append(item)
    return normalized


def ranked(objects):
    return sorted(objects, key=lambda item: (-float(item["detection_score"]), item["source_object_key"]))


def select_endpoints(thing_candidates, stuff_candidates, include_stuff):
    max_endpoints = CONFIG["detector"]["max_endpoints"]
    thing_ranked = ranked(thing_candidates)
    if not include_stuff:
        selected = thing_ranked[:max_endpoints]
        stuff_selected = []
    else:
        stuff_ranked = ranked(stuff_candidates)
        stuff_selected = stuff_ranked[:CONFIG["detector"]["stuff_endpoint_reserve"]]
        thing_selected = thing_ranked[:max_endpoints - len(stuff_selected)]
        selected = thing_selected + stuff_selected
    selected = [dict(item) for item in sorted(selected, key=lambda item: item["source_object_key"])]
    for object_id, item in enumerate(selected):
        item["id"] = object_id
    selected_keys = {item["source_object_key"] for item in selected}
    selected_thing_keys = {item["source_object_key"] for item in selected if item["source"] != "mask2former_stuff"}
    dropped_things = [item for item in thing_ranked if item["source_object_key"] not in selected_thing_keys]
    dropped_stuff = [item for item in ranked(stuff_candidates) if item["source_object_key"] not in selected_keys]
    return selected, dropped_things, dropped_stuff


def selection_record(group_name, thing_candidates, stuff_candidates, selected, dropped_things, dropped_stuff,
                     thing_only_selected):
    selected_thing_keys = {item["source_object_key"] for item in selected if item["source"] != "mask2former_stuff"}
    selected_stuff = [item for item in selected if item["source"] == "mask2former_stuff"]
    thing_only_keys = {item["source_object_key"] for item in thing_only_selected}
    replaced = [item for item in thing_only_selected if item["source_object_key"] not in selected_thing_keys]
    replacement_pairs = []
    for thing, stuff in zip(sorted(replaced, key=lambda item: item["source_object_key"]), selected_stuff):
        replacement_pairs.append({"removed_thing": object_summary(thing), "added_stuff": object_summary(stuff)})
    return {
        "group": group_name,
        "candidate_thing_count": len(thing_candidates),
        "candidate_stuff_count": len(stuff_candidates),
        "selected_thing_count": len(selected_thing_keys),
        "selected_stuff_count": len(selected_stuff),
        "endpoint_count": len(selected),
        "endpoint_limit": CONFIG["detector"]["max_endpoints"],
        "stuff_reserve_limit": CONFIG["detector"]["stuff_endpoint_reserve"],
        "selected_endpoints": [object_summary(item) for item in selected],
        "dropped_things_at_endpoint_cap": [object_summary(item) for item in dropped_things],
        "dropped_stuff_at_endpoint_cap": [object_summary(item) for item in dropped_stuff],
        "replacements_relative_to_thing_only": replacement_pairs,
        "thing_only_selected_keys": sorted(thing_only_keys)
    }


def fixed_endpoint_valid_relations(record):
    matches = endpoint_matches(record["detected"]["objects"], record["ground_truth_objects"], False)
    valid = []
    for truth in record["ground_truth_relations"]:
        subject_id, object_id = truth["subject_id"], truth["object_id"]
        subject = record["ground_truth_objects"][subject_id]
        obj = record["ground_truth_objects"][object_id]
        if not (subject["is_person"] or obj["is_person"]):
            continue
        if matches[subject_id] and matches[object_id] and any(
                subject_match != object_match
                for subject_match in matches[subject_id]
                for object_match in matches[object_id]):
            valid.append(truth)
    return valid


def evaluation_records(records, group_name, fixed_valid=False):
    result = []
    for source in records:
        record = {key: value for key, value in source.items() if key != "groups"}
        record["detected"] = source["groups"][group_name]
        if fixed_valid:
            record["ground_truth_relations"] = source["fixed_endpoint_valid_relations"]
        result.append(record)
    return result


def hit_map(details):
    hits = {}
    for image in details:
        for row in image["diagnostics"]:
            key = (image["index"], row["subject_id"], row["object_id"], row["predicate"])
            hits[key] = row
    return hits


def contrast_hit_changes(records, evaluations, group_names, fixed_valid):
    baseline_name = group_names[0]
    evaluation_name = "fixed_baseline_endpoint_valid" if fixed_valid else "all_gt"
    baseline_eval = evaluations[baseline_name][evaluation_name]
    baseline = hit_map(baseline_eval["per_image"])
    changes = {}
    index_names = {record["index"]: record["file_name"] for record in records}
    for group_name in group_names[1:]:
        evaluation = evaluations[group_name][evaluation_name]
        current = hit_map(evaluation["per_image"])
        keys = sorted(set(baseline) | set(current))
        recovered = []
        lost = []
        for key in keys:
            previous_stage = baseline.get(key, {}).get("stage")
            current_stage = current.get(key, {}).get("stage")
            was_hit = previous_stage == "hit50"
            is_hit = current_stage == "hit50"
            if is_hit and not was_hit:
                recovered.append({"index": key[0], "file_name": index_names[key[0]], "subject_id": key[1],
                                  "object_id": key[2], "predicate": key[3],
                                  "previous_stage": previous_stage, "current_stage": current_stage})
            if was_hit and not is_hit:
                lost.append({"index": key[0], "file_name": index_names[key[0]], "subject_id": key[1],
                             "object_id": key[2], "predicate": key[3],
                             "previous_stage": previous_stage, "current_stage": current_stage})
        changes[group_name] = {"recovered_vs_A": recovered, "lost_vs_A": lost,
                               "recovered_count": len(recovered), "lost_count": len(lost)}
    return changes


def summarize_evaluations(records, group_names, output_dir):
    evaluations = {}
    for group_name in group_names:
        all_gt_records = evaluation_records(records, group_name)
        fixed_records = evaluation_records(records, group_name, fixed_valid=True)
        evaluations[group_name] = {
            "all_gt": evaluate(all_gt_records, "detected", key="relations", group="all_human"),
            "all_gt_single_predicate": evaluate(all_gt_records, "detected", key="single_predicate_top50", group="all_human"),
            "fixed_baseline_endpoint_valid": evaluate(fixed_records, "detected", key="relations", group="all_human"),
            "human_nonhuman": evaluate(all_gt_records, "detected", key="relations", group="human_nonhuman"),
            "human_human": evaluate(all_gt_records, "detected", key="relations", group="human_human")
        }
    group_names = list(group_names)
    recoveries = {"all_gt": contrast_hit_changes(records, evaluations, group_names, False),
                  "fixed_baseline_endpoint_valid": contrast_hit_changes(records, evaluations, group_names, True)}
    save_json(output_dir / "evaluation.json", evaluations)
    save_json(output_dir / "recovery_loss.json", recoveries)
    stuff_counts = Counter()
    selection_summaries = {}
    for record in records:
        for group_name in group_names:
            details = record["selection"][group_name]
            if details["selected_stuff_count"]:
                stuff_counts.update(item["label"] for item in details["selected_endpoints"]
                                    if item["source"] == "mask2former_stuff")
            summary = selection_summaries.setdefault(group_name, {
                "images": 0, "endpoints": 0, "things": 0, "stuff": 0, "dropped_things": 0,
                "dropped_stuff": 0, "replaced_thing_slots": 0, "candidate_things": 0, "candidate_stuff": 0,
                "images_with_person_endpoint": 0, "images_with_stuff_endpoint": 0})
            summary["images"] += 1
            summary["endpoints"] += details["endpoint_count"]
            summary["things"] += details["selected_thing_count"]
            summary["stuff"] += details["selected_stuff_count"]
            summary["dropped_things"] += len(details["dropped_things_at_endpoint_cap"])
            summary["dropped_stuff"] += len(details["dropped_stuff_at_endpoint_cap"])
            summary["replaced_thing_slots"] += len(details["replacements_relative_to_thing_only"])
            summary["candidate_things"] += details["candidate_thing_count"]
            summary["candidate_stuff"] += details["candidate_stuff_count"]
            summary["images_with_person_endpoint"] += any(
                item["label"] == "person" for item in details["selected_endpoints"])
            summary["images_with_stuff_endpoint"] += bool(details["selected_stuff_count"])
    save_json(output_dir / "endpoint_selection_summary.json", {
        "groups": selection_summaries,
        "selected_stuff_by_psg_class": dict(stuff_counts),
        "all_image_selection_details_in_predictions": True})
    return evaluations, recoveries, selection_summaries, stuff_counts


def main():
    parser = argparse.ArgumentParser(description="Run the four-group PSG thing/stuff region comparison")
    parser.add_argument("--limit", type=int, default=CONFIG["dataset"]["expected_images"])
    parser.add_argument("--output", default=str(RESEARCH_DIR / "output/regions"))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--visualization-count", type=int, default=CONFIG["visualization"]["positive_images"])
    args = parser.parse_args()
    if args.limit < 1 or args.limit > CONFIG["dataset"]["expected_images"]:
        raise ValueError("limit must be between 1 and the fixed sample size")
    if args.visualization_count < 0:
        raise ValueError("visualization-count must be nonnegative")
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("The region study requires CUDA with BF16 support")
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = output_dir / "region_predictions.jsonl"
    detector_cache_path = output_dir / "mask2former_candidates.jsonl"
    if predictions_path.exists() and not args.resume:
        raise FileExistsError(f"Refusing to overwrite prior predictions without --resume: {predictions_path}")
    baseline_path = ROOT / CONFIG["dataset"]["baseline_predictions"]
    manifest_path = ROOT / CONFIG["dataset"]["sample_manifest"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    baseline_rows = read_json_lines(baseline_path)
    baseline = {int(record["index"]): record for record in baseline_rows}
    indices = manifest["indices"][:args.limit]
    file_names = manifest["file_names"]
    if len(indices) != args.limit or len(baseline) != CONFIG["dataset"]["expected_images"]:
        raise ValueError("Fixed random500 manifest or baseline prediction coverage is incomplete")
    for index in indices:
        if index not in baseline or baseline[index]["file_name"] != file_names[manifest["indices"].index(index)]:
            raise ValueError(f"Baseline record does not match fixed manifest at index {index}")
    prior_records = read_json_lines(predictions_path) if args.resume else []
    prior_detector_rows = read_json_lines(detector_cache_path) if args.resume else []
    records_by_index = {int(record["index"]): record for record in prior_records}
    detector_by_index = {int(record["index"]): record["candidates"] for record in prior_detector_rows}
    invalid_prior = set(records_by_index) - set(indices)
    if invalid_prior:
        raise ValueError(f"Resume output contains indices outside current manifest range: {sorted(invalid_prior)}")
    if set(records_by_index) and not detector_cache_path.is_file():
        raise FileNotFoundError("Resume predictions exist without the Mask2Former detector cache")
    categories = psg_categories(ROOT)
    device = torch.device("cuda")
    torch.set_num_threads(8)
    torch.manual_seed(CONFIG["dataset"]["seed"])
    torch.cuda.synchronize()
    free_before, total_memory = torch.cuda.mem_get_info()
    pipeline = HumanRelationPipeline(with_detector=False)
    detector = PanopticRegionDetector(ROOT, device, categories)
    torch.cuda.reset_peak_memory_stats()
    group_names = list(CONFIG["groups"])
    visualization_indices = []
    for index in indices:
        record = baseline[index]
        if any(item["is_person"] for item in record["ground_truth_objects"]) and record["ground_truth_relations"]:
            visualization_indices.append(index)
        if len(visualization_indices) >= args.visualization_count:
            break
    save_json(output_dir / "run_config.json", {
        "study_config": CONFIG,
        "study_config_sha256": sha256(CONFIG_PATH),
        "fixed_manifest_sha256": sha256(manifest_path),
        "baseline_predictions_sha256": sha256(baseline_path),
        "panoptic_weights_sha256": detector.sha256,
        "panoptic_weights_revision": CONFIG["detector"]["revision"],
        "transformers": transformers.__version__,
        "torch": torch.__version__,
        "torchvision": torchvision.__version__,
        "python": platform.python_version(),
        "gpu": torch.cuda.get_device_name(),
        "endpoint_cap": CONFIG["detector"]["max_endpoints"],
        "stuff_reserve": CONFIG["detector"]["stuff_endpoint_reserve"],
        "relation_pair_budget": CONFIG["relation_model"]["candidate_pair_budget"],
        "visualization_indices": visualization_indices,
        "visualization_selection_uses_GT_only_for_examples": True,
        "gpu_free_bytes_before_models": free_before,
        "gpu_total_bytes": total_memory,
        "resume_existing_indices": sorted(records_by_index)})
    image_dir = ROOT / CONFIG["dataset"]["image_directory"]
    relation_mode = "a" if predictions_path.exists() and args.resume else "w"
    detector_mode = "a" if detector_cache_path.exists() and args.resume else "w"
    started = time.perf_counter()
    inference_started = time.perf_counter()
    with predictions_path.open(relation_mode, encoding="utf-8") as prediction_stream, \
            detector_cache_path.open(detector_mode, encoding="utf-8") as detector_stream:
        for position, index in enumerate(indices, 1):
            if index in records_by_index:
                continue
            tick = time.perf_counter()
            source_record = baseline[index]
            image_path = image_dir / source_record["file_name"]
            image = Image.open(image_path).convert("RGB")
            if list(image.size) != source_record["image_size"]:
                raise ValueError(f"Image size changed for {image_path}")
            faster_things = normalize_fasterrcnn_objects(source_record["detected"]["objects"], categories)
            if index in detector_by_index:
                panoptic_candidates = detector_by_index[index]
            else:
                panoptic_candidates = detector.detect(image)
                detector_stream.write(json.dumps({"index": index, "file_name": source_record["file_name"],
                                                 "candidates": panoptic_candidates}, ensure_ascii=False) + "\n")
                detector_stream.flush()
                detector_by_index[index] = panoptic_candidates
            panoptic_things = [item for item in panoptic_candidates if item["source"] == "mask2former_thing"]
            panoptic_stuff = [item for item in panoptic_candidates if item["source"] == "mask2former_stuff"]
            groups = {}
            selections = {}
            combinations = (
                ("A_fasterrcnn_thing", faster_things, [], False),
                ("B_mask2former_thing", panoptic_things, [], False),
                ("C_fasterrcnn_thing_plus_stuff", faster_things, panoptic_stuff, True),
                ("D_mask2former_thing_plus_stuff", panoptic_things, panoptic_stuff, True))
            thing_only_cache = {}
            for group_name, things, stuff, include_stuff in combinations:
                selected, dropped_things, dropped_stuff = select_endpoints(things, stuff, include_stuff)
                if not include_stuff:
                    thing_only_cache[group_name] = selected
                paired_thing_group = {
                    "C_fasterrcnn_thing_plus_stuff": "A_fasterrcnn_thing",
                    "D_mask2former_thing_plus_stuff": "B_mask2former_thing"}.get(group_name)
                thing_only = thing_only_cache.get(paired_thing_group, []) if paired_thing_group else selected
                selections[group_name] = selection_record(group_name, things, stuff, selected,
                                                          dropped_things, dropped_stuff, thing_only)
                prediction, arrays = pipeline.relations(image, selected, exhaustive=False)
                prediction["group"] = group_name
                prediction["candidate_pair_budget"] = CONFIG["relation_model"]["candidate_pair_budget"]
                prediction["endpoint_limit"] = CONFIG["detector"]["max_endpoints"]
                prediction["selection"] = selections[group_name]
                groups[group_name] = prediction
                if arrays is not None:
                    logits_dir = output_dir / "logits" / group_name
                    logits_dir.mkdir(parents=True, exist_ok=True)
                    np.savez_compressed(logits_dir / f"{index:04d}.npz", **arrays)
            fixed_valid = fixed_endpoint_valid_relations(source_record)
            if index not in visualization_indices:
                visualize = False
            else:
                visualize = True
            record = {
                "index": index,
                "sample_position": position,
                "file_name": source_record["file_name"],
                "image_sha256": source_record["image_sha256"],
                "image_size": source_record["image_size"],
                "ground_truth_objects": source_record["ground_truth_objects"],
                "ground_truth_relations": source_record["ground_truth_relations"],
                "fixed_endpoint_valid_relations": fixed_valid,
                "groups": groups,
                "selection": selections,
                "mask2former_candidate_count": len(panoptic_candidates),
                "mask2former_thing_candidate_count": len(panoptic_things),
                "mask2former_stuff_candidate_count": len(panoptic_stuff),
                "elapsed_seconds": time.perf_counter() - tick
            }
            prediction_stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            prediction_stream.flush()
            records_by_index[index] = record
            if visualize:
                for group_name in group_names:
                    target = output_dir / "visuals" / group_name / f"{index:04d}_objects.jpg"
                    draw_objects(image, groups[group_name]["objects"], target)
            torch.cuda.synchronize()
            if position == 1 or position % 10 == 0:
                elapsed = time.perf_counter() - inference_started
                done = len(records_by_index)
                average = elapsed / done
                print(f"regions {done}/{args.limit}; index={index}; panoptic={len(panoptic_candidates)}; "
                      f"A-D endpoints={[len(groups[name]['objects']) for name in group_names]}; "
                      f"avg={average:.2f}s/image; elapsed={elapsed:.1f}s; "
                      f"peak={torch.cuda.max_memory_allocated() / 2**30:.2f}GiB", flush=True)
    ordered_records = [records_by_index[index] for index in indices if index in records_by_index]
    if len(ordered_records) != args.limit:
        raise ValueError(f"Expected {args.limit} region records, found {len(ordered_records)}")
    expected_relations = sum(len(record["ground_truth_relations"]) for record in ordered_records)
    expected_human_relations = sum(sum(
        record["ground_truth_objects"][row["subject_id"]]["is_person"] or
        record["ground_truth_objects"][row["object_id"]]["is_person"]
        for row in record["ground_truth_relations"]) for record in ordered_records)
    fixed_relations = sum(len(record["fixed_endpoint_valid_relations"]) for record in ordered_records)
    if args.limit == CONFIG["dataset"]["expected_images"]:
        if expected_human_relations != CONFIG["dataset"]["expected_human_gt_relations"]:
            raise ValueError(f"Expected 968 human GT relations, found {expected_human_relations}")
        if fixed_relations != CONFIG["dataset"]["expected_baseline_endpoint_valid_relations"]:
            raise ValueError(f"Expected 530 fixed baseline endpoint-valid relations, found {fixed_relations}")
    evaluations, recoveries, selection_summaries, stuff_counts = summarize_evaluations(
        ordered_records, group_names, output_dir)
    runtime = {
        "created": datetime.now().astimezone().isoformat(),
        "images": len(ordered_records),
        "human_gt_relations": expected_human_relations,
        "fixed_baseline_endpoint_valid_relations": fixed_relations,
        "all_gt_relation_rows": expected_relations,
        "total_seconds": time.perf_counter() - started,
        "inference_and_artifact_seconds": time.perf_counter() - inference_started,
        "average_seconds_per_image": (time.perf_counter() - inference_started) / len(ordered_records),
        "peak_GPU_allocated_GiB": torch.cuda.max_memory_allocated() / 2**30,
        "GPU": torch.cuda.get_device_name(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torchvision": torchvision.__version__,
        "transformers": transformers.__version__,
        "relation_dtype": CONFIG["relation_model"]["inference_dtype"],
        "mask2former_dtype": "CUDA autocast BF16",
        "verified_relation_checkpoint_tensors": pipeline.loaded_tensor_count,
        "mask2former_repository": CONFIG["detector"]["repository"],
        "mask2former_revision": CONFIG["detector"]["revision"],
        "mask2former_weights_sha256": detector.sha256,
        "command": [sys.executable, *sys.argv],
        "config_sha256": sha256(CONFIG_PATH),
        "source_sha256": sha256(Path(__file__)),
        "input_sha256": {
            "manifest": sha256(manifest_path),
            "baseline_predictions": sha256(baseline_path),
            "psg_categories": sha256(ROOT / "data/PSG/packed/psg/test/meta.json")
        },
        "resources_sha256": {
            "mask2former_weights": detector.sha256,
            "relation_weights": sha256(ROOT / "models/relsgg-vits16plus/model.pth"),
            "relation_text_embeddings": sha256(ROOT / "models/relsgg-vits16plus/text_student.pt")
        },
        "group_selection_summary": selection_summaries,
        "selected_stuff_by_psg_class": dict(stuff_counts),
        "recoveries_and_losses": {group: {
            "all_gt_recovered": values["recovered_count"],
            "all_gt_lost": values["lost_count"],
            "fixed530_recovered": recoveries["fixed_baseline_endpoint_valid"][group]["recovered_count"],
            "fixed530_lost": recoveries["fixed_baseline_endpoint_valid"][group]["lost_count"]}
            for group, values in recoveries["all_gt"].items()}
    }
    save_json(output_dir / "runtime.json", runtime)
    save_json(output_dir / "visualization_manifest.json", {
        "selection_rule": CONFIG["visualization"]["selection"],
        "indices": visualization_indices,
        "groups": group_names,
        "metrics_use_visualization_selection": False})
    save_json(output_dir / "run_summary.json", {
        "images": len(ordered_records),
        "human_gt_relations": expected_human_relations,
        "fixed_baseline_endpoint_valid_relations": fixed_relations,
        "metrics": {group: evaluations[group]["all_gt"]["metrics"] for group in group_names},
        "fixed530_metrics": {group: evaluations[group]["fixed_baseline_endpoint_valid"]["metrics"]
                             for group in group_names},
        "recoveries_and_losses": runtime["recoveries_and_losses"],
        "runtime_seconds": runtime["total_seconds"],
        "peak_GPU_allocated_GiB": runtime["peak_GPU_allocated_GiB"]})
    print(json.dumps(json.loads((output_dir / "run_summary.json").read_text(encoding="utf-8")),
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
