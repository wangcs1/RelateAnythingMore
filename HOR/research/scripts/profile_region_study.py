from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import platform
import statistics
import sys
import time

import numpy as np
from PIL import Image
import torch
import transformers


ROOT = Path(__file__).resolve().parents[3]
HOR_DIR = ROOT / "HOR"
RESEARCH_DIR = HOR_DIR / "research"
sys.path.insert(0, str(RESEARCH_DIR / "scripts"))
from region_study import CONFIG, PanopticRegionDetector, psg_categories, read_json_lines
sys.path.insert(0, str(HOR_DIR))
from pipeline import HumanRelationPipeline, sha256


GROUPS = list(CONFIG["groups"])


def candidate_signature(candidates):
    return [(item["source_object_key"], item["label"], item["source_category_id"],
             item["source_segment_id"], item["box_xyxy"]) for item in candidates]


def group_signature(prediction):
    return [(row["subject_id"], row["object_id"], row["predicate_id"], row["stream"])
            for row in prediction["relations"]]


def distribution(values):
    return {"count": len(values), "total_seconds": float(sum(values)),
            "mean_seconds": float(statistics.mean(values)) if values else None,
            "median_seconds": float(statistics.median(values)) if values else None,
            "p90_seconds": float(np.quantile(values, 0.9)) if values else None,
            "min_seconds": float(min(values)) if values else None,
            "max_seconds": float(max(values)) if values else None}


def main():
    output_dir = RESEARCH_DIR / "output/regions"
    prediction_path = output_dir / "region_predictions.jsonl"
    detector_path = output_dir / "mask2former_candidates.jsonl"
    records = read_json_lines(prediction_path)
    detector_rows = read_json_lines(detector_path)
    expected_images = CONFIG["dataset"]["expected_images"]
    if len(records) != expected_images or len(detector_rows) != expected_images:
        raise ValueError("Timing profile requires the complete cached 500-image study")
    records_by_index = {int(record["index"]): record for record in records}
    detector_by_index = {int(record["index"]): record["candidates"] for record in detector_rows}
    if set(records_by_index) != set(detector_by_index):
        raise ValueError("Prediction and panoptic cache image indices differ")
    manifest_path = ROOT / CONFIG["dataset"]["sample_manifest"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    indices = manifest["indices"]
    if set(indices) != set(records_by_index):
        raise ValueError("Prediction rows do not match the fixed random500 manifest")
    categories = psg_categories(ROOT)
    device = torch.device("cuda")
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("The timing profile requires CUDA with BF16 support")
    torch.set_num_threads(8)
    torch.manual_seed(CONFIG["dataset"]["seed"])
    torch.cuda.synchronize()
    free_before, total_memory = torch.cuda.mem_get_info()
    pipeline = HumanRelationPipeline(with_detector=False)
    detector = PanopticRegionDetector(ROOT, device, categories)
    torch.cuda.reset_peak_memory_stats()
    image_dir = ROOT / CONFIG["dataset"]["image_directory"]
    detector_times = []
    group_times = {name: [] for name in GROUPS}
    group_image_times = {name: [] for name in GROUPS}
    relation_match_counts = defaultdict(Counter)
    detector_topology_matches = 0
    detector_box_matches = 0
    detector_score_max_differences = []
    relation_candidate_counts = Counter()
    started = time.perf_counter()
    for position, index in enumerate(indices, 1):
        record = records_by_index[index]
        image_path = image_dir / record["file_name"]
        image = Image.open(image_path).convert("RGB")
        torch.cuda.synchronize()
        tick = time.perf_counter()
        candidates = detector.detect(image)
        torch.cuda.synchronize()
        detector_times.append(time.perf_counter() - tick)
        cached_candidates = detector_by_index[index]
        current_signature = candidate_signature(candidates)
        cached_signature = candidate_signature(cached_candidates)
        topology_match = [(row[:4]) for row in current_signature] == [(row[:4]) for row in cached_signature]
        detector_topology_matches += topology_match
        boxes_match = topology_match and all(
            np.allclose(current[4], cached[4], rtol=0, atol=1e-5)
            for current, cached in zip(current_signature, cached_signature))
        detector_box_matches += boxes_match
        if len(candidates) != len(cached_candidates):
            raise ValueError(f"Mask2Former candidate count changed for dataset index {index}")
        if not topology_match or not boxes_match:
            raise ValueError(f"Mask2Former segment identities or boxes changed for dataset index {index}")
        detector_score_max_differences.extend(
            abs(float(current["detection_score"]) - float(cached["detection_score"]))
            for current, cached in zip(candidates, cached_candidates))
        for group_name in GROUPS:
            saved_prediction = record["groups"][group_name]
            torch.cuda.synchronize()
            tick = time.perf_counter()
            prediction, _ = pipeline.relations(image, saved_prediction["objects"], exhaustive=False)
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - tick
            group_image_times[group_name].append(elapsed)
            relation_candidate_counts[group_name] += prediction["candidate_pairs"]
            if prediction["candidate_pairs"]:
                group_times[group_name].append(elapsed)
            output_match = group_signature(prediction) == group_signature(saved_prediction)
            relation_match_counts[group_name]["images"] += 1
            relation_match_counts[group_name]["matching_output_images"] += output_match
            relation_match_counts[group_name]["forward_images"] += prediction["candidate_pairs"] > 0
            if prediction["candidate_pairs"] != saved_prediction["candidate_pairs"]:
                raise ValueError(f"Relation candidate count changed for {group_name}, index {index}")
        if position == 1 or position % 100 == 0:
            elapsed = time.perf_counter() - started
            print(f"profile {position}/{expected_images}; elapsed={elapsed:.1f}s; "
                  f"peak={torch.cuda.max_memory_allocated() / 2**30:.2f}GiB", flush=True)
    profile = {
        "created": datetime.now().astimezone().isoformat(),
        "images": len(records),
        "GPU": torch.cuda.get_device_name(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda_free_bytes_before_models": free_before,
        "cuda_total_bytes": total_memory,
        "peak_GPU_allocated_GiB": torch.cuda.max_memory_allocated() / 2**30,
        "weights_sha256": detector.sha256,
        "input_sha256": {
            "region_predictions": sha256(prediction_path),
            "panoptic_candidates": sha256(detector_path),
            "fixed_manifest": sha256(manifest_path)
        },
        "timing_scope": "synchronized CUDA wall time for image preprocessing, model inference, and postprocessing",
        "mask2former_panoptic_detection": distribution(detector_times),
        "relation_group_times": {
            name: {
                "model_forward_images": relation_match_counts[name]["forward_images"],
                "candidate_pair_total": int(relation_candidate_counts[name]),
                "forward_time": distribution(group_times[name]),
                "all_image_relation_pipeline_time": distribution(group_image_times[name]),
                "saved_top50_identity_match_images": relation_match_counts[name]["matching_output_images"]
            } for name in GROUPS
        },
        "total_profile_wall_seconds": time.perf_counter() - started,
        "detector_topology_match_images": detector_topology_matches,
        "detector_topology_and_box_match_images": detector_box_matches,
        "detector_max_abs_score_difference": max(detector_score_max_differences, default=0.0),
        "relation_top50_identity_match_counts": {
            name: relation_match_counts[name]["matching_output_images"] for name in GROUPS
        },
        "script_sha256": sha256(Path(__file__))
    }
    profile_path = output_dir / "compute_profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(profile, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
