import hashlib
import json
import os
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
os.environ["TORCH_HOME"] = str(ROOT / "HOR/research/models/torchhub")

import numpy as np
import torch
from PIL import Image
from pycocotools.cocoeval import COCOeval
from pycocotools.coco import COCO
from torchvision.models.detection import keypointrcnn_resnet50_fpn
from torchvision.transforms.functional import pil_to_tensor


CONFIG_PATH = ROOT / "HOR/research/configs/keypoint_prediction.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_records(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def verify_weights(path, prefix):
    if not path.is_file():
        raise FileNotFoundError(f"Missing official Keypoint R-CNN weights: {path}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if not digest.startswith(prefix):
        raise ValueError(f"Checkpoint SHA-256 prefix mismatch: {digest}")
    return digest


def build_scaled_ground_truth(records, metadata, coco_data):
    coco_images = {int(row["id"]): row for row in coco_data["images"]}
    annotations_by_image = {}
    for annotation in coco_data["annotations"]:
        annotations_by_image.setdefault(int(annotation["image_id"]), []).append(annotation)

    images = []
    annotations = []
    seen_coco_ids = set()
    image_ids = []
    annotation_id = 1
    metadata_rows = []
    duplicate_images = []
    for record in records:
        vg_id = int(Path(record["file_name"]).stem)
        source = metadata.get(vg_id)
        if source is None or source.get("coco_id") is None:
            continue
        coco_id = int(source["coco_id"])
        source_image = coco_images.get(coco_id)
        if source_image is None:
            continue
        if coco_id in seen_coco_ids:
            duplicate_images.append({"vg_image_id": vg_id, "coco_image_id": coco_id,
                                     "file_name": record["file_name"], "excluded": True})
            continue
        seen_coco_ids.add(coco_id)
        image_ids.append(coco_id)
        local_width, local_height = record["image_size"]
        scale_x = local_width / source_image["width"]
        scale_y = local_height / source_image["height"]
        images.append({"id": coco_id, "file_name": record["file_name"],
                       "width": local_width, "height": local_height})
        for source_annotation in annotations_by_image.get(coco_id, []):
            annotation = dict(source_annotation)
            x, y, width, height = annotation["bbox"]
            annotation["bbox"] = [x * scale_x, y * scale_y,
                                  width * scale_x, height * scale_y]
            annotation["area"] = float(annotation.get("area", width * height) * scale_x * scale_y)
            keypoints = annotation["keypoints"]
            annotation["keypoints"] = [
                coordinate * scale_x if index % 3 == 0 else
                coordinate * scale_y if index % 3 == 1 else coordinate
                for index, coordinate in enumerate(keypoints)
            ]
            annotation["id"] = annotation_id
            annotation_id += 1
            annotation["image_id"] = coco_id
            annotations.append(annotation)
        metadata_rows.append({"vg_image_id": vg_id, "coco_image_id": coco_id,
                              "local_width": local_width, "local_height": local_height,
                              "coco_width": source_image["width"],
                              "coco_height": source_image["height"]})

    ground_truth = {"info": coco_data.get("info", {}),
                    "licenses": coco_data.get("licenses", []),
                    "images": images, "annotations": annotations,
                    "categories": coco_data["categories"]}
    return ground_truth, image_ids, metadata_rows, duplicate_images


def to_coco_results(image_rows, allowed_image_ids):
    results = []
    seen_image_ids = set()
    for image in image_rows:
        if image["coco_image_id"] not in allowed_image_ids or image["coco_image_id"] in seen_image_ids:
            continue
        seen_image_ids.add(image["coco_image_id"])
        for person in image["people"]:
            x1, y1, x2, y2 = person["box_xyxy"]
            results.append({"image_id": image["coco_image_id"], "category_id": 1,
                            "bbox": [x1, y1, x2 - x1, y2 - y1],
                            "area": max(0.0, x2 - x1) * max(0.0, y2 - y1),
                            "score": person["detection_score"],
                            "keypoints": [coordinate for joint in person["keypoints"]
                                          for coordinate in joint]})
    return results


def main():
    config = read_json(CONFIG_PATH)
    checkpoint = ROOT / config["model_weights_file"]
    checkpoint_sha256 = verify_weights(checkpoint, config["model_weights_sha256_prefix"])
    records = read_records(ROOT / config["input_predictions"])
    metadata_rows = read_json(ROOT / config["visual_genome_image_metadata"])
    metadata = {int(row["image_id"]): row for row in metadata_rows}
    coco_data = read_json(ROOT / config["coco_keypoint_annotations"])
    ground_truth, image_ids, image_mappings, duplicate_images = build_scaled_ground_truth(
        records, metadata, coco_data
    )

    model = keypointrcnn_resnet50_fpn(weights=None, weights_backbone=None)
    state_dict = torch.load(checkpoint, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict, strict=True)
    device = torch.device(config["device"])
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    model.to(device).eval()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    output_dir = ROOT / config["output_directory"]
    report_dir = ROOT / config["report_directory"] / "evidence"
    image_outputs = []
    started = time.perf_counter()
    inference_seconds = 0.0
    peak_memory_bytes = 0
    for position, record in enumerate(records, 1):
        vg_id = int(Path(record["file_name"]).stem)
        source = metadata.get(vg_id)
        coco_id = int(source["coco_id"]) if source and source.get("coco_id") else None
        image_path = ROOT / "data/PSG/images/test" / record["file_name"]
        image = Image.open(image_path).convert("RGB")
        tensor = pil_to_tensor(image).to(dtype=torch.float32).div_(255.0).to(device)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        inference_started = time.perf_counter()
        with torch.inference_mode():
            output = model([tensor])[0]
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            peak_memory_bytes = max(peak_memory_bytes, torch.cuda.max_memory_allocated(device))
        inference_seconds += time.perf_counter() - inference_started

        person_ids = torch.where(output["labels"].detach().cpu() == 1)[0].tolist()
        boxes = output["boxes"].detach().cpu().tolist()
        scores = output["scores"].detach().cpu().tolist()
        keypoint_tensor = output["keypoints"].detach().cpu()
        if keypoint_tensor.ndim != 3 or keypoint_tensor.shape[1:] != (17, 3):
            raise ValueError(f"Unexpected Keypoint R-CNN tensor shape: {tuple(keypoint_tensor.shape)}")
        keypoint_scores_tensor = output["keypoints_scores"].detach().cpu()
        if keypoint_scores_tensor.shape != keypoint_tensor.shape[:2]:
            raise ValueError(f"Unexpected keypoint score shape: {tuple(keypoint_scores_tensor.shape)}")
        if not torch.isfinite(keypoint_scores_tensor).all():
            raise ValueError("Keypoint R-CNN returned nonfinite keypoint scores")
        keypoints = keypoint_tensor.tolist()
        keypoint_scores = keypoint_scores_tensor.tolist()
        people = []
        for person_id in person_ids:
            people.append({
                "box_xyxy": [float(value) for value in boxes[person_id]],
                "detection_score": float(scores[person_id]),
                "keypoints": [[float(value) for value in point]
                              for point in keypoints[person_id]],
                "keypoints_scores": [float(value) for value in keypoint_scores[person_id]],
            })
        image_outputs.append({"index": record["index"], "sample_position": record["sample_position"],
                              "file_name": record["file_name"], "coco_image_id": coco_id,
                              "image_size": record["image_size"], "people": people})
        if position % 50 == 0 or position == len(records):
            print(f"Keypoint R-CNN {position}/{len(records)}; images={len(image_outputs)}")

    elapsed = time.perf_counter() - started
    write_jsonl(output_dir / "keypoint_predictions.jsonl", image_outputs)
    write_json(output_dir / "keypoint_ground_truth_scaled.json", ground_truth)
    write_json(output_dir / "keypoint_image_mappings.json", image_mappings)
    write_json(report_dir / "keypoint_image_mappings.json", image_mappings)

    coco_gt = COCO()
    coco_gt.dataset = ground_truth
    coco_gt.createIndex()
    results = to_coco_results(image_outputs, set(image_ids))
    coco_dt = coco_gt.loadRes(results)
    evaluator = COCOeval(coco_gt, coco_dt, iouType="keypoints")
    evaluator.params.imgIds = image_ids
    evaluator.evaluate()
    evaluator.accumulate()
    evaluator.summarize()
    metric_names = ["AP", "AP50", "AP75", "AP_medium", "AP_large",
                    "AR", "AR50", "AR75", "AR_medium", "AR_large"]
    if len(evaluator.stats) != len(metric_names):
        raise ValueError(f"Unexpected COCO keypoint metric count: {len(evaluator.stats)}")
    metrics = {name: float(value) for name, value in zip(metric_names, evaluator.stats)}
    metrics_summary = {
        "model": "torchvision Keypoint R-CNN ResNet-50 FPN COCO_V1",
        "checkpoint_url": config["model_weights_url"],
        "checkpoint_sha256": checkpoint_sha256,
        "device": str(device),
        "images_in_sample": len(records),
        "images_in_coco_keypoint_eval": len(image_ids),
        "duplicate_source_images_excluded_from_coco_eval": duplicate_images,
        "gt_person_annotations": len(ground_truth["annotations"]),
        "predicted_person_detections": len(results),
        "inference_seconds": inference_seconds,
        "elapsed_seconds": elapsed,
        "mean_seconds_per_image": inference_seconds / max(1, len(records)),
        "peak_torch_cuda_memory_bytes": peak_memory_bytes,
        "keypoint_confidence_threshold_for_part_proxy": config["keypoint_confidence_threshold"],
        "part_proxy_score_field": "keypoints_scores (raw heatmap peak scores; not calibrated probabilities)",
        "metrics": metrics,
    }
    write_json(output_dir / "keypoint_coco_metrics.json", metrics_summary)
    write_json(report_dir / "keypoint_coco_metrics.json", metrics_summary)


if __name__ == "__main__":
    main()
