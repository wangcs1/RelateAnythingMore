import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.transforms.functional import pil_to_tensor


ROOT = Path(__file__).resolve().parents[1]
HOR_DIR = ROOT / "HOR"
CONFIG = json.loads((HOR_DIR / "config.json").read_text(encoding="utf-8"))
CACHE = HOR_DIR / ".cache"
CACHE.mkdir(exist_ok=True)
tempfile.tempdir = str(CACHE)
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.insert(0, str(ROOT / "RelateAnything"))
from relsgg.checkpoint import build_model_from_ckpt, load_checkpoint
from relsgg.text.student import encode_texts_student
from relsgg.vocabulary import TRAIN_TEMPLATES


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 ** 2), b""):
            digest.update(chunk)
    return digest.hexdigest()


def human_pair(subject, obj):
    return subject["is_person"] or obj["is_person"]


def normalized_boxes(objects, image_size):
    width, height = image_size
    xyxy = torch.tensor([item["box_xyxy"] for item in objects], dtype=torch.float32)
    return torch.stack(((xyxy[:, 0] + xyxy[:, 2]) / (2 * width),
                        (xyxy[:, 1] + xyxy[:, 3]) / (2 * height),
                        (xyxy[:, 2] - xyxy[:, 0]) / width,
                        (xyxy[:, 3] - xyxy[:, 1]) / height), dim=-1)


def relation_record(subject, obj, predicate_id, logit, pair_logit, predicates, stream):
    fused = float(logit + pair_logit)
    return {"subject_id": subject["id"], "subject_label": subject["label"],
            "predicate_id": predicate_id, "predicate": predicates[predicate_id],
            "object_id": obj["id"], "object_label": obj["label"],
            "person_ids": [item["id"] for item in (subject, obj) if item["is_person"]],
            "human_human": subject["is_person"] and obj["is_person"],
            "stream": stream, "predicate_logit": float(logit), "pair_logit": float(pair_logit),
            "fused_logit": fused, "score": float(torch.sigmoid(torch.tensor(fused)))}


class HumanRelationPipeline:
    def __init__(self, with_detector=True):
        if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
            raise RuntimeError("HOR requires CUDA with BF16 support")
        torch.set_num_threads(8)
        torch.manual_seed(CONFIG["seed"])
        self.device = torch.device("cuda")
        self.predicates = json.loads((ROOT / "data/PSG/packed/psg/test/meta.json").read_text(
            encoding="utf-8"))["predicates"]
        checkpoint = load_checkpoint(str(ROOT / "models/relsgg-vits16plus/model.pth"))
        if checkpoint.get("stripped_weights") != "ema" or not checkpoint.get("backbone_config"):
            raise ValueError("Published EMA weights and embedded backbone config required")
        self.model = build_model_from_ckpt(checkpoint, weights="raw", strict=True)
        loaded = self.model.state_dict()
        differences = [key for key, value in checkpoint["model"].items()
                       if not torch.equal(loaded[key].cpu(), value.cpu())]
        if differences:
            raise ValueError(f"Checkpoint tensor mismatch: {differences}")
        self.loaded_tensor_count = len(checkpoint["model"])
        del loaded, checkpoint
        self.model = self.model.to(self.device).eval()
        embeddings = encode_texts_student(self.predicates, str(ROOT / "models/relsgg-vits16plus/text_student.pt"),
                                          templates=TRAIN_TEMPLATES)
        self.model.vocab_head.set_vocabulary_matrix(self.predicates, embeddings)
        self.model.reparameterize()
        self.detector = None
        self.detector_categories = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT.meta["categories"]
        if with_detector:
            weight_path = HOR_DIR / "models/fasterrcnn_resnet50_fpn_v2_coco-dd69338a.pth"
            if not weight_path.is_file():
                raise FileNotFoundError(f"Download detector weights first: {weight_path}")
            self.detector = fasterrcnn_resnet50_fpn_v2(
                weights=None, weights_backbone=None,
                min_size=CONFIG["detector_min_size"], max_size=CONFIG["detector_max_size"],
                box_score_thresh=CONFIG["detection_score_threshold"],
                box_detections_per_img=CONFIG["max_detections"])
            self.detector.load_state_dict(torch.load(weight_path, map_location="cpu", weights_only=True), strict=True)
            self.detector = self.detector.to(self.device).eval()
        self.spatial_indices = [index for index, name in enumerate(self.predicates)
                                if name in CONFIG["spatial_predicates"]]
        self.semantic_indices = [index for index in range(len(self.predicates)) if index not in self.spatial_indices]

    @torch.inference_mode()
    def detect(self, image):
        if self.detector is None:
            raise RuntimeError("Detector was not loaded")
        tensor = pil_to_tensor(image).to(self.device).float().div_(255)
        detected = self.detector([tensor])[0]
        boxes = detected["boxes"].cpu().tolist()
        labels = detected["labels"].cpu().tolist()
        scores = detected["scores"].cpu().tolist()
        objects = []
        for box, category, score in zip(boxes, labels, scores):
            label = self.detector_categories[category]
            if score < CONFIG["detection_score_threshold"]:
                continue
            if box[2] <= box[0] or box[3] <= box[1]:
                raise ValueError(f"Invalid detected box: {box}")
            objects.append({"id": len(objects), "label": label, "category_id": category,
                            "is_person": label in CONFIG["human_categories"],
                            "box_xyxy": box, "detection_score": score, "source": "detector"})
        return objects

    @torch.inference_mode()
    def relations(self, image, objects, exhaustive=True):
        if len({item["id"] for item in objects}) != len(objects):
            raise ValueError("Object IDs must be unique")
        human_ids = [item["id"] for item in objects if item["is_person"]]
        result = {"objects": objects, "human_ids": human_ids, "relations": [],
                  "single_predicate_top50": [], "all_human_pairs": [],
                  "status": "ok", "candidate_pairs": 0, "human_pairs_scored": 0,
                  "expected_human_pairs": sum(human_pair(s, o) for s in objects for o in objects if s["id"] != o["id"]),
                  "pair_policy": "all_pairs" if exhaustive else "official_400"}
        if not human_ids or len(objects) < 2:
            result["status"] = "no_person" if not human_ids else "no_other_object"
            return result, None
        width, height = image.size
        for item in objects:
            x1, y1, x2, y2 = item["box_xyxy"]
            if not all(np.isfinite([x1, y1, x2, y2])) or x2 < x1 or y2 < y1:
                raise ValueError(f"Invalid box: {item}")
        boxes = normalized_boxes(objects, (width, height)).unsqueeze(0).to(self.device)
        pixels = image.resize((CONFIG["resolution"], CONFIG["resolution"]), Image.Resampling.BILINEAR)
        pixels = pil_to_tensor(pixels).float().div_(255).unsqueeze(0).to(self.device)
        count = len(objects)
        budget = count * count if exhaustive else 400
        self.model.sampler.geo_budget = budget
        self.model.sampler.final_budget = budget
        with torch.autocast("cuda", dtype=torch.bfloat16):
            output = self.model(pixels, boxes, torch.tensor([count], device=self.device), targets=None)
        valid = output["valid_mask"][0]
        subject = output["sub_idx"][0][valid].cpu().tolist()
        obj = output["obj_idx"][0][valid].cpu().tolist()
        logits = output["logits"][0][valid].float().cpu()
        pair_logits = output["pair_logits"][0][valid].float().cpu()
        if not torch.isfinite(logits).all() or not torch.isfinite(pair_logits).all():
            raise ValueError("Nonfinite relation logits")
        result["candidate_pairs"] = len(subject)
        if len(set(zip(subject, obj))) != len(subject) or any(s == o for s, o in zip(subject, obj)):
            raise ValueError("Duplicate or self candidate pairs")
        if exhaustive and len(subject) != count * (count - 1):
            raise ValueError("Exhaustive pair coverage failed")
        candidates = []
        single = []
        for slot, (s, o) in enumerate(zip(subject, obj)):
            sub_object, obj_object = objects[s], objects[o]
            if not human_pair(sub_object, obj_object):
                continue
            result["human_pairs_scored"] += 1
            pair_record = {"subject_id": sub_object["id"], "object_id": obj_object["id"], "predictions": []}
            for stream, indices in (("spatial", self.spatial_indices), ("semantic", self.semantic_indices),
                                    ("single", list(range(len(self.predicates))))):
                predicate_id = indices[int(logits[slot, indices].argmax())]
                row = relation_record(sub_object, obj_object, predicate_id, float(logits[slot, predicate_id]),
                                      float(pair_logits[slot]), self.predicates, stream)
                if stream == "single":
                    single.append(row)
                else:
                    candidates.append(row)
                    pair_record["predictions"].append(row)
            result["all_human_pairs"].append(pair_record)
        key = lambda row: (-row["fused_logit"], row["subject_id"], row["object_id"], row["predicate_id"])
        result["relations"] = sorted([row for row in candidates if row["score"] >= CONFIG["relation_score_floor"]], key=key)[:CONFIG["relation_topk"]]
        result["single_predicate_top50"] = sorted([row for row in single if row["score"] >= CONFIG["relation_score_floor"]], key=key)[:CONFIG["relation_topk"]]
        for rank, row in enumerate(result["relations"], 1):
            row["rank"] = rank
        if exhaustive and result["human_pairs_scored"] != result["expected_human_pairs"]:
            raise ValueError("Human pair coverage failed")
        arrays = {"subject_indices": np.asarray(subject), "object_indices": np.asarray(obj),
                  "predicate_logits": logits.numpy(), "pair_logits": pair_logits.numpy()}
        return result, arrays

    def predict(self, image):
        started = time.perf_counter()
        objects = self.detect(image)
        result, arrays = self.relations(image, objects)
        torch.cuda.synchronize()
        result["elapsed_seconds"] = time.perf_counter() - started
        return result, arrays


def draw_objects(image, objects, path):
    canvas = image.copy()
    canvas.thumbnail((1400, 1000))
    sx, sy = canvas.width / image.width, canvas.height / image.height
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    for item in objects:
        color = "#ed174c" if item["is_person"] else "#0070c0"
        x1, y1, x2, y2 = item["box_xyxy"]
        box = (max(0, x1 * sx), max(0, y1 * sy), min(canvas.width - 1, x2 * sx), min(canvas.height - 1, y2 * sy))
        if box[2] < box[0] or box[3] < box[1]:
            continue
        draw.rectangle(box, outline=color, width=3 if item["is_person"] else 2)
        text = f'#{item["id"]} {item["label"]}'
        bounds = draw.textbbox((box[0], box[1]), text, font=font)
        draw.rectangle(bounds, fill=color)
        draw.text((box[0], box[1]), text, fill="white", font=font)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, quality=88)
