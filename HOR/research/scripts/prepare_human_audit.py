import argparse
import csv
import hashlib
import json
import math
import random
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "HOR/research/configs/human_audit.json"


def read_records(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_signatures(config):
    paths = (Path(__file__).resolve(), CONFIG_PATH, ROOT / config["source_predictions"],
             ROOT / config["visual_genome_image_metadata"])
    return {path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}


def validate_inputs(manifest, config):
    if manifest["input_signatures"] != input_signatures(config):
        raise ValueError("Sampling configuration or source evidence changed after blind export")


def validate_box(value, image_row, field_name):
    box = json.loads(value)
    if not isinstance(box, list) or len(box) != 4:
        raise ValueError(f"{field_name} must contain a JSON array with four coordinates")
    if not all(isinstance(coordinate, (int, float)) and math.isfinite(coordinate)
               for coordinate in box):
        raise ValueError(f"{field_name} coordinates must be finite numbers")
    width = int(image_row["image_width"])
    height = int(image_row["image_height"])
    if not (0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height):
        raise ValueError(f"{field_name} must be a positive-area box within the original image")


def candidate_id(record, relation):
    identity = {
        "image_sha256": record["image_sha256"],
        "subject_id": relation["subject_id"],
        "object_id": relation["object_id"],
        "predicate_id": relation["predicate_id"],
    }
    payload = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=("blind", "freeze", "candidates"))
    args = parser.parse_args()
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    report_dir = ROOT / config["output_directory"]
    private_dir = ROOT / config["private_output_directory"]
    image_csv_path = report_dir / "images_blind.csv"
    relation_csv_path = report_dir / "relations_blind.csv"
    candidate_csv_path = report_dir / "candidate_review.csv"
    manifest_path = private_dir / "manifest.json"

    if args.stage == "freeze":
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_inputs(manifest, config)
        if manifest.get("phase1_frozen"):
            raise FileExistsError("Blind review is already frozen; its hashes cannot be replaced")
        image_rows = read_csv(image_csv_path)
        relation_rows = read_csv(relation_csv_path)
        if len(image_rows) != manifest["sample_size"] * 2:
            raise ValueError("Blind image table must have two independently completed rows per image")
        image_keys = {f"S{position:03d}" for position in manifest["sample_positions"]}
        expected = {(key, slot) for key in image_keys for slot in ("A", "B")}
        observed = {(row["image_key"], row["rater_slot"]) for row in image_rows}
        if observed != expected:
            raise ValueError("Blind image table must contain exactly one row per image and rater slot")
        rater_ids = {slot: set() for slot in ("A", "B")}
        for row in image_rows:
            if not row["rater_id"].strip() or row["image_review_status"] not in (
                    "complete", "not_assessable") or row["relation_review_status"] not in (
                        "complete_with_relations", "complete_no_relations", "not_assessable"):
                raise ValueError("Every blind image row needs a rater, review status, and relation status")
            datetime.fromisoformat(row["reviewed_at"])
            if not row["review_version"].strip() or row["saw_model_outputs"] != "no":
                raise ValueError("Blind review needs a version and confirmation that model outputs were hidden")
            if row["image_sha256"] != manifest["image_sha256"][row["image_key"]]:
                raise ValueError("Blind image identity differs from the frozen sampling inventory")
            if row["image_review_status"] == "not_assessable":
                if row["relation_review_status"] != "not_assessable" or not row["uncertainty_reason"].strip():
                    raise ValueError("Unassessable images need a consistent relation status and a reason")
            elif row["relation_review_status"] == "not_assessable":
                raise ValueError("Complete image review conflicts with unassessable relation status")
            if row["image_review_status"] == "complete":
                count = int(row["visible_person_count"])
                if count < 0:
                    raise ValueError("Visible person count must be nonnegative")
            rater_ids[row["rater_slot"]].add(row["rater_id"].strip())
        if len(rater_ids["A"]) != 1 or len(rater_ids["B"]) != 1 or rater_ids["A"] & rater_ids["B"]:
            raise ValueError("Rater slots A and B must belong to different independent reviewers")

        relation_keys = {(row["image_key"], row["rater_slot"]) for row in relation_rows}
        if relation_keys != expected:
            raise ValueError("Blind relation table must retain one or more rows per image and rater")
        images_by_key = {(row["image_key"], row["rater_slot"]): row for row in image_rows}
        support_labels = {"supported", "unknown_occluded", "unknown_resolution",
                          "ambiguous_instance", "not_observable"}
        for row in relation_rows:
            if not row["rater_id"].strip() or row["rater_slot"] not in ("A", "B"):
                raise ValueError("Every relation row must identify its independent reviewer")
            image_row = images_by_key[(row["image_key"], row["rater_slot"])]
            if row["rater_id"].strip() != image_row["rater_id"].strip():
                raise ValueError("Relation and image rows must identify the same independent reviewer")
            if row["relation_predicate"].strip():
                required = ("relation_subject_instance_id", "relation_object_instance_id",
                            "relation_subject_description", "relation_object_description",
                            "evidence_note", "visibility")
                if any(not row[name].strip() for name in required):
                    raise ValueError("Each independent relation needs endpoint identities, descriptions, and evidence")
                if row["visual_support"] not in support_labels:
                    raise ValueError("Each independent relation needs a supported or explicit unknown label")
                person_flags = (row["relation_subject_is_person"], row["relation_object_is_person"])
                if any(flag not in ("yes", "no") for flag in person_flags) or "yes" not in person_flags:
                    raise ValueError("Each human-related relation must identify at least one person endpoint")
                for name in ("relation_subject_box_xyxy", "relation_object_box_xyxy"):
                    validate_box(row[name], image_row, name)
                if row["visual_support"] != "supported" and not row["uncertainty_reason"].strip():
                    raise ValueError("Unknown relations need an explicit uncertainty reason")
        image_status = {(row["image_key"], row["rater_slot"]): row["relation_review_status"]
                        for row in image_rows}
        for key in expected:
            rows = [row for row in relation_rows
                    if (row["image_key"], row["rater_slot"]) == key]
            has_relation = any(row["relation_predicate"].strip() for row in rows)
            if image_status[key] == "complete_with_relations" and not has_relation:
                raise ValueError(f"No relation rows found for completed positive image {key}")
            if image_status[key] == "complete_no_relations" and has_relation:
                raise ValueError(f"No-relation status conflicts with rows for image {key}")
            if image_status[key] == "not_assessable" and has_relation:
                raise ValueError(f"Unassessable image conflicts with relation rows for image {key}")

        manifest["phase1_frozen"] = True
        manifest["phase1_rater_count"] = 2
        manifest["phase1_frozen_sha256"] = {
            "images_blind.csv": file_sha256(image_csv_path),
            "relations_blind.csv": file_sha256(relation_csv_path),
        }
        private_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
        print(json.dumps({"stage": "freeze", "sample_size": manifest["sample_size"],
                          "phase1_frozen_sha256": manifest["phase1_frozen_sha256"]}, ensure_ascii=False))
        return

    if args.stage == "candidates":
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        frozen_hashes = manifest.get("phase1_frozen_sha256")
        if not manifest.get("phase1_frozen") or not frozen_hashes:
            raise ValueError("Complete and freeze the independent image/relationship review first")
        validate_inputs(manifest, config)
        for name, path in (("images_blind.csv", image_csv_path),
                           ("relations_blind.csv", relation_csv_path)):
            if file_sha256(path) != frozen_hashes[name]:
                raise ValueError(f"Frozen phase-one input changed: {name}")
    else:
        manifest = None

    records = read_records(ROOT / config["source_predictions"])
    vg_metadata = json.loads((ROOT / config["visual_genome_image_metadata"]).read_text(encoding="utf-8"))
    metadata_by_id = {int(item["image_id"]): item for item in vg_metadata}
    if len(records) != 500:
        raise ValueError(f"Expected 500 source images, found {len(records)}")
    unique_records = []
    seen_hashes = set()
    seen_source_ids = set()
    duplicate_source_ids_excluded = 0
    for record in records:
        vg_id = int(Path(record["file_name"]).stem)
        metadata = metadata_by_id.get(vg_id)
        source_id = metadata.get("coco_id") if metadata else None
        if source_id is not None:
            if int(source_id) in seen_source_ids:
                duplicate_source_ids_excluded += 1
                continue
            seen_source_ids.add(int(source_id))
        if record["image_sha256"] not in seen_hashes:
            unique_records.append(record)
            seen_hashes.add(record["image_sha256"])

    sample_rng = random.Random(config["sample_seed"])
    selected = sample_rng.sample(unique_records, config["sample_size"])
    selected.sort(key=lambda record: record["sample_position"])
    if args.stage == "candidates":
        actual_positions = [record["sample_position"] for record in selected]
        actual_hashes = {f"S{record['sample_position']:03d}": record["image_sha256"]
                         for record in selected}
        if actual_positions != manifest["sample_positions"] or actual_hashes != manifest["image_sha256"]:
            raise ValueError("Candidate sample differs from the frozen blind image sample")
    image_rows = []
    blind_relation_rows = []
    candidate_rows = []
    audit_rng = random.Random(config["candidate_shuffle_seed"])
    candidate_total = 0

    for record in selected:
        image_path = Path("data/PSG/images/test") / record["file_name"]
        if args.stage == "blind":
            for slot in ("A", "B"):
                image_rows.append({
                    "image_key": f"S{record['sample_position']:03d}",
                    "dataset_index": record["index"],
                    "file_name": record["file_name"],
                    "image_path": image_path.as_posix(),
                    "image_sha256": record["image_sha256"],
                    "image_width": record["image_size"][0],
                    "image_height": record["image_size"][1],
                    "rater_slot": slot,
                    "rater_id": "",
                    "reviewed_at": "",
                    "review_version": "",
                    "saw_model_outputs": "",
                    "visible_person_count": "",
                    "image_review_status": "",
                    "relation_review_status": "",
                    "uncertainty_reason": "",
                })
                blind_relation_rows.append({
                    "image_key": f"S{record['sample_position']:03d}",
                    "file_name": record["file_name"],
                    "image_path": image_path.as_posix(),
                    "rater_slot": slot,
                    "rater_id": "",
                    "relation_subject_instance_id": "",
                    "relation_subject_description": "",
                    "relation_subject_is_person": "",
                    "relation_subject_box_xyxy": "",
                    "relation_predicate": "",
                    "relation_object_instance_id": "",
                    "relation_object_description": "",
                    "relation_object_is_person": "",
                    "relation_object_box_xyxy": "",
                    "visual_support": "",
                    "part_evidence": "",
                    "visibility": "",
                    "evidence_note": "",
                    "uncertainty_reason": "",
                })

        if args.stage != "candidates":
            continue

        detected = record["detected"]
        objects = {item["id"]: item for item in detected["objects"]}
        relations = detected["relations"][:config["candidate_limit"]]
        shuffled = list(relations)
        audit_rng.shuffle(shuffled)
        for relation in shuffled:
            subject = objects[relation["subject_id"]]
            obj = objects[relation["object_id"]]
            for slot in ("A", "B"):
                candidate_rows.append({
                    "audit_id": candidate_id(record, relation),
                    "image_key": f"S{record['sample_position']:03d}",
                    "file_name": record["file_name"],
                    "image_path": image_path.as_posix(),
                    "subject_box_id": relation["subject_id"],
                    "subject_label": subject["label"],
                    "subject_xyxy": json.dumps(subject["box_xyxy"], separators=(",", ":")),
                    "predicate": relation["predicate"],
                    "object_box_id": relation["object_id"],
                    "object_label": obj["label"],
                    "object_xyxy": json.dumps(obj["box_xyxy"], separators=(",", ":")),
                    "rater_slot": slot,
                    "rater_id": "",
                    "visual_judgment": "",
                    "supporting_part": "",
                    "target_region": "",
                    "visibility": "",
                    "evidence_note": "",
                    "uncertainty_reason": "",
                })
                candidate_total += 1

    if args.stage == "blind":
        if manifest_path.exists() and json.loads(manifest_path.read_text(encoding="utf-8")).get("phase1_frozen"):
            raise FileExistsError("Refusing to replace a frozen blind review package")
        for path in (image_csv_path, relation_csv_path):
            if path.exists() and path.stat().st_size > 0:
                existing_rows = read_csv(path)
                if any(value.strip() for row in existing_rows for key, value in row.items()
                       if key not in ("image_key", "dataset_index", "file_name", "image_path",
                                      "image_sha256", "image_width", "image_height", "rater_slot")):
                    raise ValueError(f"Refusing to overwrite completed blind annotations: {path}")
        write_csv(image_csv_path, list(image_rows[0]), image_rows)
        write_csv(relation_csv_path, list(blind_relation_rows[0]), blind_relation_rows)
        manifest = {
            "schema_version": 2,
            "input_signatures": input_signatures(config),
            "source": config["source_predictions"],
            "source_image_count": len(records),
            "unique_image_count": len(unique_records),
            "duplicate_image_count_excluded": len(records) - len(unique_records),
            "duplicate_coco_source_id_count_excluded": duplicate_source_ids_excluded,
            "sampling_identity": "COCO image ID when available; image SHA-256 otherwise.",
            "sample_size": len(selected),
            "sample_seed": config["sample_seed"],
            "candidate_shuffle_seed": config["candidate_shuffle_seed"],
            "candidate_limit": config["candidate_limit"],
            "sample_positions": [record["sample_position"] for record in selected],
            "image_sha256": {f"S{record['sample_position']:03d}": record["image_sha256"] for record in selected},
            "coco_image_ids": {f"S{record['sample_position']:03d}":
                               metadata_by_id[int(Path(record["file_name"]).stem)].get("coco_id")
                               for record in selected},
            "phase1_frozen": False,
            "protocol": "Complete independent image/relationship labels and freeze their hashes before candidate release.",
        }
        private_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    else:
        if candidate_csv_path.exists():
            raise FileExistsError(f"Refusing to overwrite candidate review labels: {candidate_csv_path}")
        write_csv(candidate_csv_path, list(candidate_rows[0]) if candidate_rows else [], candidate_rows)
        manifest["candidate_count"] = candidate_total // 2
        manifest["candidate_review_rows"] = candidate_total
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    print(json.dumps({
        "stage": args.stage,
        "sample_size": len(selected),
        "candidate_count": candidate_total // 2,
        "report_directory": str(report_dir),
        "manifest": str(manifest_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
