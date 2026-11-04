import argparse
from datetime import datetime
import json
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

import numpy as np
from PIL import Image
import torch
import torchvision

from pipeline import CONFIG, HOR_DIR, ROOT, HumanRelationPipeline, draw_objects, save_json, sha256
from evaluation import detection_summary, evaluate
from relsgg.data import RelationDataset


def reference_objects(dataset, index, size):
    _, _, _, start, number, _, _ = dataset.img_meta[index]
    number = int(number)
    labels = dataset.box_cats[start:start + number]
    width, height = size
    result = []
    for object_id, (box, label_id) in enumerate(zip(dataset.boxes[start:start + number], labels)):
        cx, cy, w, h = [float(value) for value in box]
        label = dataset.meta["categories"][int(label_id)]
        result.append({"id": object_id, "label": label, "category_id": int(label_id),
                       "is_person": label in CONFIG["human_categories"], "detection_score": None,
                       "source": "PSG_ground_truth", "box_xyxy": [(cx - w / 2) * width, (cy - h / 2) * height,
                                                                     (cx + w / 2) * width, (cy + h / 2) * height]})
    return result


def reference_relations(dataset, index, objects):
    _, _, _, _, _, start, number = dataset.img_meta[index]
    triples = sorted({tuple(int(value) for value in row[:3]) for row in dataset.rels[start:start + number]
                      if objects[int(row[0])]["is_person"] or objects[int(row[1])]["is_person"]})
    return [{"subject_id": s, "object_id": o, "predicate_id": p, "predicate": dataset.predicate_names[p]}
            for s, o, p in triples]


def main():
    parser = argparse.ArgumentParser(description="Run the fixed random 500-image HOR experiment")
    parser.add_argument("--limit", type=int, default=CONFIG["sample_size"])
    parser.add_argument("--output", default=str(HOR_DIR / "output/random500"))
    args = parser.parse_args()
    if args.limit < 1 or args.limit > CONFIG["sample_size"]:
        raise ValueError("limit must be between 1 and the fixed sample size")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    dataset = RelationDataset(str(ROOT / "data/PSG/packed/psg"), "test", resolution=CONFIG["resolution"])
    indices = random.Random(CONFIG["seed"]).sample(range(len(dataset)), CONFIG["sample_size"])
    manifest = {"seed": CONFIG["seed"], "population": len(dataset), "sample_size": len(indices),
                "indices": indices, "file_names": [dataset.file_names[index] for index in indices],
                "selection": CONFIG["sampling"], "config": CONFIG,
                "annotations_used_for_sampling": False, "relations_used_for_sampling": False}
    save_json(output / "sample_manifest.json", manifest)
    pipeline = HumanRelationPipeline()
    torch.cuda.reset_peak_memory_stats()
    records = []
    inference_started = time.perf_counter()
    with (output / "predictions.jsonl").open("w", encoding="utf-8") as stream:
        for position, index in enumerate(indices[:args.limit], 1):
            tick = time.perf_counter()
            image_path = dataset.img_dir / dataset.file_names[index]
            image = Image.open(image_path).convert("RGB")
            detected, arrays = pipeline.predict(image)
            objects = reference_objects(dataset, index, image.size)
            gt, gt_arrays = pipeline.relations(image, objects)
            official, _ = pipeline.relations(image, objects, exhaustive=False)
            record = {"index": index, "sample_position": position, "file_name": dataset.file_names[index],
                      "image_sha256": sha256(image_path), "image_size": list(image.size),
                      "ground_truth_objects": objects,
                      "ground_truth_relations": reference_relations(dataset, index, objects),
                      "detector_categories": pipeline.detector_categories,
                      "detected": detected, "gt_boxes": gt, "official400": official,
                      "elapsed_seconds": time.perf_counter() - tick}
            records.append(record)
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            for name, values in (("detected", arrays), ("gt_boxes", gt_arrays)):
                if values is not None:
                    tensor_dir = output / "logits" / name
                    tensor_dir.mkdir(parents=True, exist_ok=True)
                    np.savez_compressed(tensor_dir / f"{index:04d}.npz", **values)
            draw_objects(image, detected["objects"], output / "images" / f"{index:04d}_detected.jpg")
            draw_objects(image, objects, output / "images" / f"{index:04d}_gt.jpg")
            if position % 10 == 0 or position == 1:
                print(f"HOR {position}/{args.limit}; index={index}; GT_people={len(gt['human_ids'])}; "
                      f"det_people={len(detected['human_ids'])}; relations={len(detected['relations'])}; "
                      f"elapsed={time.perf_counter() - inference_started:.1f}s", flush=True)
    evaluations = {}
    for mode in ("detected", "gt_boxes", "official400"):
        for ranking in ("relations", "single_predicate_top50"):
            key = f"{mode}/{ranking}"
            evaluations[key] = evaluate(records, mode, ranking)
        for group in ("human_nonhuman", "human_human", "human_subject", "human_object"):
            evaluations[f"{mode}/{group}"] = evaluate(records, mode, group=group)
    evaluations["detected/class_agnostic"] = evaluate(records, "detected", class_aware=False)
    save_json(output / "evaluation.json", evaluations)
    save_json(output / "detection_summary.json", detection_summary(records))
    runtime = {"created": datetime.now().astimezone().isoformat(), "images": len(records),
               "total_seconds": time.perf_counter() - started,
               "inference_and_artifact_seconds": time.perf_counter() - inference_started,
               "peak_GPU_allocated_GiB": torch.cuda.max_memory_allocated() / 2 ** 30,
               "GPU": torch.cuda.get_device_name(), "python": platform.python_version(),
               "torch": torch.__version__, "torchvision": torchvision.__version__,
               "relation_dtype": "CUDA autocast BF16", "detector_dtype": "CUDA FP32",
               "verified_checkpoint_tensors": pipeline.loaded_tensor_count,
               "official_commit": subprocess.check_output(["git", "-C", str(ROOT / "RelateAnything"), "rev-parse", "HEAD"], text=True).strip(),
               "command": [sys.executable, *sys.argv], "config_sha256": sha256(HOR_DIR / "config.json"),
               "sources_sha256": {path.name: sha256(path) for path in HOR_DIR.glob("*.py")},
               "resources_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in (
                   HOR_DIR / "models/fasterrcnn_resnet50_fpn_v2_coco-dd69338a.pth",
                   ROOT / "models/relsgg-vits16plus/model.pth", ROOT / "models/relsgg-vits16plus/text_student.pt",
                   ROOT / "data/PSG/packed/psg/test/rels.npy", ROOT / "data/PSG/packed/psg/test/boxes.npy")}}
    save_json(output / "runtime.json", runtime)
    print(json.dumps({"images": len(records), "detected": evaluations["detected/relations"]["metrics"],
                      "GT_boxes": evaluations["gt_boxes/relations"]["metrics"],
                      "seconds": runtime["total_seconds"]}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
