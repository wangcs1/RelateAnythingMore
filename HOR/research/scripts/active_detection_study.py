import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
import math
from pathlib import Path
import platform
import shutil
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
HOR_DIR = ROOT / "HOR"
RESEARCH_DIR = HOR_DIR / "research"
CONFIG_PATH = RESEARCH_DIR / "configs/active_detection.json"
sys.path.insert(0, str(HOR_DIR))
from evaluation import endpoint_matches, evaluate
from pipeline import save_json, sha256


GROUPS = ["baseline", "geometry", "RA_guided"]
GROUP_LABELS = {"baseline": "Baseline", "geometry": "Geometry crops", "RA_guided": "RA-guided crops"}
SCOPES = ["all_968_GT", "fixed_530_GT"]
COMPARISONS = [("geometry", "baseline"), ("RA_guided", "baseline"), ("RA_guided", "geometry")]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_lines(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_lines(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_sources(config):
    manifest = read_json(ROOT / config["sample_manifest"])
    records = []
    with (ROOT / config["source_region_predictions"]).open(encoding="utf-8") as stream:
        for line in stream:
            source = json.loads(line)
            baseline = source["groups"]["A_fasterrcnn_thing"]
            records.append({key: source[key] for key in (
                "index", "sample_position", "file_name", "image_sha256", "image_size",
                "ground_truth_objects", "ground_truth_relations", "fixed_endpoint_valid_relations")})
            records[-1]["baseline_objects"] = baseline["objects"]
            records[-1]["guidance_relations"] = baseline["relations"]
    if len(records) != config["expected_records"] or [row["index"] for row in records] != manifest["indices"]:
        raise ValueError("The active-detection inputs must match all 500 fixed PSG records in manifest order")
    if sum(len(row["ground_truth_relations"]) for row in records) != config["expected_human_GT_relations"]:
        raise ValueError("The source predictions do not contain the fixed 968 human-related GT relations")
    if sum(len(row["fixed_endpoint_valid_relations"]) for row in records) != config["expected_fixed_endpoint_valid_GT_relations"]:
        raise ValueError("The source predictions do not contain the fixed 530 endpoint-valid GT relations")
    for row in records:
        if len(row["baseline_objects"]) > config["endpoint_cap"]:
            raise ValueError(f"Too many frozen baseline endpoints at {row['index']}")
        if not (ROOT / config["image_directory"] / row["file_name"]).is_file():
            raise FileNotFoundError(row["file_name"])
    return records


def crop_box(person, image_size, fraction, config, object_box=None):
    image_width, image_height = image_size
    x1, y1, x2, y2 = person["box_xyxy"]
    width, height = x2 - x1, y2 - y1
    center_x, center_y = (x1 + x2) / 2, y1 + fraction * height
    if object_box is not None:
        mix = config["guidance_object_center_mix"]
        center_x = (1 - mix) * center_x + mix * (object_box[0] + object_box[2]) / 2
        center_y = (1 - mix) * center_y + mix * (object_box[1] + object_box[3]) / 2
    crop_width = min(image_width, max(config["crop_min_side_pixels"],
                                     width * config["crop_width_person_multiplier"]))
    crop_height = min(image_height, max(config["crop_min_side_pixels"],
                                       height * config["crop_height_person_multiplier"]))
    left = min(max(0, center_x - crop_width / 2), image_width - crop_width)
    top = min(max(0, center_y - crop_height / 2), image_height - crop_height)
    box = [int(math.floor(left)), int(math.floor(top)),
           min(image_width, int(math.ceil(left + crop_width))),
           min(image_height, int(math.ceil(top + crop_height)))]
    if box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError(f"An invalid crop was produced from a detector endpoint: {box}")
    return box


def query_plans(objects, relations, image_size, config):
    people = [item for item in objects if item["is_person"]]
    if not people:
        return {"geometry": [], "RA_guided": []}
    people.sort(key=lambda item: (-(item["box_xyxy"][2] - item["box_xyxy"][0]) *
                                  (item["box_xyxy"][3] - item["box_xyxy"][1]), item["source_object_key"]))
    person = people[0]
    geometry = [{"policy_source": "geometry_default", "person_id": person["id"],
                 "person_source_key": person["source_object_key"], "body_fraction": fraction,
                 "crop_box_xyxy": crop_box(person, image_size, fraction, config), "guidance_relation": None}
                for fraction in config["geometry_body_fractions"]]
    indexed = {item["id"]: item for item in objects}
    routed = []
    for relation in sorted(relations, key=lambda item: (-item["fused_logit"], item["subject_id"],
                                                       item["object_id"], item["predicate_id"])):
        predicate = relation["predicate"]
        if predicate not in config["guidance_body_fractions"] or relation["score"] < config["guidance_min_raw_sigmoid_score"]:
            continue
        subject, obj = indexed[relation["subject_id"]], indexed[relation["object_id"]]
        if not subject["is_person"] or obj["is_person"]:
            continue
        fraction = config["guidance_body_fractions"][predicate]
        routed.append({"policy_source": "RA_relation_route", "person_id": subject["id"],
                       "person_source_key": subject["source_object_key"], "body_fraction": fraction,
                       "crop_box_xyxy": crop_box(subject, image_size, fraction, config, obj["box_xyxy"]),
                       "guidance_relation": dict(relation)})
    selected = []
    for query in routed + geometry:
        if query["crop_box_xyxy"] not in [item["crop_box_xyxy"] for item in selected]:
            selected.append(query)
        if len(selected) == config["queries_per_detected_person_image"]:
            break
    if len(selected) < 2:
        selected.extend(geometry[len(selected):2])
    if len(geometry) != 2 or len(selected) != 2:
        raise ValueError("Every detected-person record must have exactly two usable queries in both policies")
    return {group: [dict(query, query_id=position) for position, query in enumerate(queries)]
            for group, queries in (("geometry", geometry), ("RA_guided", selected))}


def prepare(records, config, config_path):
    output_dir = ROOT / config["output_directory"]
    if (output_dir / "predictions.jsonl").exists():
        raise FileExistsError("Preparation refuses to replace plans belonging to existing inference results")
    output_dir.mkdir(parents=True, exist_ok=True)
    plans = [{"index": row["index"], "file_name": row["file_name"], "image_size": row["image_size"],
              "image_sha256": row["image_sha256"],
              "queries": query_plans(row["baseline_objects"], row["guidance_relations"], row["image_size"], config)}
             for row in records]
    write_lines(output_dir / "crop_plans.jsonl", plans)
    source_paths = [config_path, ROOT / config["source_region_predictions"], ROOT / config["source_region_runtime"],
                    ROOT / config["source_region_evaluation"],
                    ROOT / config["sample_manifest"], ROOT / config["source_identity_metadata"]]
    save_json(output_dir / "prepared_inputs.json", {
        "created": datetime.now().astimezone().isoformat(), "study": config["study"],
        "config_sha256": sha256(config_path), "records": len(records), "GT_used_to_select_crops": False,
        "plan_sha256": sha256(output_dir / "crop_plans.jsonl"),
        "inputs_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in source_paths},
        "source_region_runtime": read_json(ROOT / config["source_region_runtime"]),
        "detected_person_records": sum(bool(row["queries"]["geometry"]) for row in plans),
        "planned_queries": {group: sum(len(row["queries"][group]) for row in plans) for group in GROUPS[1:]},
        "RA_routed_queries": sum(query["policy_source"] == "RA_relation_route" for row in plans
                                  for query in row["queries"]["RA_guided"])
    })
    return plans


def validate_preparation(records, config, config_path):
    output_dir = ROOT / config["output_directory"]
    prepared = read_json(output_dir / "prepared_inputs.json")
    if prepared["config_sha256"] != sha256(config_path) or prepared["plan_sha256"] != sha256(output_dir / "crop_plans.jsonl"):
        raise ValueError("The current configuration or crop plans differ from their prepared input signatures")
    for relative_path, expected in prepared["inputs_sha256"].items():
        if sha256(ROOT / relative_path) != expected:
            raise ValueError(f"A prepared upstream input changed: {relative_path}")
    plans = read_lines(output_dir / "crop_plans.jsonl")
    if [row["index"] for row in plans] != [row["index"] for row in records]:
        raise ValueError("Prepared crop plans do not cover the fixed source records in order")
    for source, plan in zip(records, plans):
        expected = query_plans(source["baseline_objects"], source["guidance_relations"], source["image_size"], config)
        if expected != plan["queries"]:
            raise ValueError(f"Stored crop queries do not follow the declared prediction-only policy at {source['index']}")
    return prepared, plans


def merge_endpoints(original, detected, config):
    import torch
    from torchvision.ops import batched_nms

    candidates = [dict(item, source_kind="existing") for item in original] + detected
    candidates.sort(key=lambda item: (-item["detection_score"], item["source_kind"] != "existing", item["source_object_key"]))
    boxes = torch.tensor([item["box_xyxy"] for item in candidates], dtype=torch.float32).reshape(-1, 4)
    scores = torch.tensor([item["detection_score"] for item in candidates], dtype=torch.float32)
    categories = torch.tensor([item["category_id"] for item in candidates], dtype=torch.int64)
    kept = batched_nms(boxes, scores, categories, config["classwise_merge_nms_iou"]).tolist()
    selected_indices = kept[:config["endpoint_cap"]]
    selected = [dict(candidates[index]) for index in selected_indices]
    selected.sort(key=lambda item: item["source_object_key"])
    for index, item in enumerate(selected):
        item["id"] = index
    selected_keys = {item["source_object_key"] for item in selected}
    return selected, {
        "input_endpoint_count": len(candidates), "crop_detection_count": len(detected), "after_NMS_count": len(kept),
        "selected_endpoint_count": len(selected),
        "removed_by_NMS": [item for index, item in enumerate(candidates) if index not in set(kept)],
        "removed_by_endpoint_cap": [candidates[index] for index in kept[config["endpoint_cap"]:]],
        "original_source_keys_not_selected": [item["source_object_key"] for item in original
                                               if item["source_object_key"] not in selected_keys]
    }


def infer(records, config, config_path, resume):
    import torch
    import torchvision
    from pipeline import HumanRelationPipeline

    loaded_script_sha256 = sha256(Path(__file__))
    output_dir = ROOT / config["output_directory"]
    prediction_path = output_dir / "predictions.jsonl"
    if prediction_path.exists() and not resume:
        raise FileExistsError("Existing inference results require --resume; archive the directory for a full rerun")
    if not (output_dir / "prepared_inputs.json").exists():
        prepare(records, config, config_path)
    prepared, plans = validate_preparation(records, config, config_path)
    previous = read_lines(prediction_path) if prediction_path.exists() else []
    completed = {row["index"] for row in previous}
    if len(completed) != len(previous) or completed - {row["index"] for row in records}:
        raise ValueError("Existing inference records have duplicate or unexpected indices")
    for label in ("detector", "relation", "text"):
        if sha256(ROOT / config[f"{label}_weights"]) != config[f"{label}_weights_sha256"]:
            raise ValueError(f"The {label} weights do not match the fixed experiment")
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("Active detection requires the existing CUDA/BF16 evaluation environment")
    pipeline = HumanRelationPipeline(with_detector=True)
    categories = read_json(ROOT / "data/PSG/packed/psg/test/meta.json")["categories"]
    category_ids = {name: index for index, name in enumerate(categories)}
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    with prediction_path.open("a" if prediction_path.exists() else "w", encoding="utf-8") as stream:
        for position, (source, plan) in enumerate(zip(records, plans), 1):
            if source["index"] in completed:
                continue
            tick = time.perf_counter()
            image_path = ROOT / config["image_directory"] / source["file_name"]
            if sha256(image_path) != source["image_sha256"]:
                raise ValueError(f"The source image bytes changed at index {source['index']}")
            image = Image.open(image_path).convert("RGB")
            if list(image.size) != source["image_size"]:
                raise ValueError(f"The source image size changed at index {source['index']}")
            groups = {}
            offset = (position - 1) % len(GROUPS)
            execution_order = GROUPS[offset:] + GROUPS[:offset]
            for group in execution_order:
                query_rows = []
                detected = []
                if group == "baseline":
                    objects = [dict(item, source_kind="existing") for item in source["baseline_objects"]]
                    merge = {"input_endpoint_count": len(objects), "crop_detection_count": 0,
                             "after_NMS_count": len(objects), "selected_endpoint_count": len(objects),
                             "removed_by_NMS": [], "removed_by_endpoint_cap": [], "original_source_keys_not_selected": []}
                else:
                    for query in plan["queries"][group]:
                        torch.cuda.synchronize()
                        query_started = time.perf_counter()
                        left, top, right, bottom = query["crop_box_xyxy"]
                        crop_objects = pipeline.detect(image.crop((left, top, right, bottom)))
                        mapped = []
                        for item in crop_objects:
                            x1, y1, x2, y2 = item["box_xyxy"]
                            mapped.append(dict(item, category_id=category_ids[item["label"]],
                                               box_xyxy=[max(0, x1 + left), max(0, y1 + top),
                                                         min(image.width, x2 + left), min(image.height, y2 + top)],
                                               source="crop_fasterrcnn", source_kind="crop",
                                               source_crop_policy=group, source_query_id=query["query_id"],
                                               source_crop_xyxy=query["crop_box_xyxy"], source_crop_detection_id=item["id"],
                                               source_object_key=f"crop:{group}:{query['query_id']}:{item['id']:06d}"))
                        torch.cuda.synchronize()
                        query_rows.append(dict(query, detections=mapped, elapsed_seconds=time.perf_counter() - query_started,
                                               input_pixels=(right - left) * (bottom - top)))
                        detected.extend(mapped)
                    objects, merge = merge_endpoints(source["baseline_objects"], detected, config)
                torch.cuda.synchronize()
                relation_started = time.perf_counter()
                prediction, arrays = pipeline.relations(image, objects, exhaustive=False)
                torch.cuda.synchronize()
                prediction["relation_elapsed_seconds"] = time.perf_counter() - relation_started
                prediction["queries"] = query_rows
                prediction["merge_audit"] = merge
                groups[group] = prediction
                if arrays is not None:
                    directory = output_dir / "logits" / group
                    directory.mkdir(parents=True, exist_ok=True)
                    np.savez_compressed(directory / f"{source['index']:04d}.npz", **arrays)
            row = {"index": source["index"], "file_name": source["file_name"], "image_sha256": source["image_sha256"],
                   "execution_order": execution_order, "groups": groups, "elapsed_seconds": time.perf_counter() - tick}
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            completed.add(source["index"])
            if position == 1 or position % 25 == 0:
                print(f"active_detection {len(completed)}/500; elapsed={time.perf_counter() - started:.1f}s", flush=True)
    save_json(output_dir / "runtime.json", {
        "created": datetime.now().astimezone().isoformat(), "records": len(completed),
        "python": platform.python_version(), "torch": torch.__version__, "torchvision": torchvision.__version__,
        "GPU": torch.cuda.get_device_name(), "relation_dtype": "CUDA autocast BF16", "detector_dtype": "CUDA FP32",
        "peak_GPU_allocated_GiB": torch.cuda.max_memory_allocated() / 1024 ** 3,
        "this_invocation_inference_seconds": time.perf_counter() - started,
        "resume_skipped_records": len(previous), "config_sha256": sha256(config_path),
        "script_sha256": loaded_script_sha256, "prepared_inputs_sha256": sha256(output_dir / "prepared_inputs.json"),
        "latest_region_source_runtime": prepared["source_region_runtime"]
    })
    del pipeline
    torch.cuda.empty_cache()


def analyze(records, config, config_path):
    from active_detection_analysis import analyze as analyze_outputs

    analyze_outputs(records, config, config_path)


def main():
    parser = argparse.ArgumentParser(description="Same-query-budget active detection; default mode audits existing caches on CPU")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--prepare", action="store_true", help="Prepare and sign prediction-only crop plans without using the GPU")
    mode.add_argument("--infer", action="store_true", help="Run the real detector and relation model on the GPU, then audit on CPU")
    parser.add_argument("--resume", action="store_true", help="With --infer, skip existing completed image records")
    args = parser.parse_args()
    if args.resume and not args.infer:
        parser.error("--resume requires --infer")
    config_path = Path(args.config).resolve()
    config = read_json(config_path)
    if (config["queries_per_detected_person_image"], config["endpoint_cap"], config["relation_pair_budget"],
            config["relation_top_k"]) != (2, 40, 400, 50):
        raise ValueError("This experiment fixes 2 local queries, 40 endpoints, 400 pairs, and Top-50 output")
    records = read_sources(config)
    if args.prepare:
        prepare(records, config, config_path)
        print(json.dumps(read_json(ROOT / config["output_directory"] / "prepared_inputs.json"), ensure_ascii=False, indent=2))
        return
    if args.infer:
        infer(records, config, config_path, args.resume)
    analyze(records, config, config_path)


if __name__ == "__main__":
    main()
