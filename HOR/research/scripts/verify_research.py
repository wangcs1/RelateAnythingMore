import ast
import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from markdown_it import MarkdownIt
from PIL import Image
import torch


ROOT = Path(__file__).resolve().parents[3]
STUDY = ROOT / "HOR/research"
REPORTS = STUDY / "reports"
VERIFICATION_PATH = REPORTS / "delivery_verification.json"
MANIFEST_PATH = REPORTS / "delivery_manifest.json"
ENVIRONMENT_PATH = REPORTS / "environment_snapshot.json"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite_constant)


def reject_nonfinite_constant(value):
    raise ValueError(f"Nonstandard nonfinite JSON constant: {value}")


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ignore_status(path):
    result = subprocess.run(["git", "check-ignore", "--quiet", "--", str(path.relative_to(ROOT))],
                            cwd=ROOT, check=False)
    require(result.returncode in (0, 1), f"Cannot query ignore status: {path}")
    return result.returncode == 0


def verify_delivery_scope():
    guide = STUDY / "configs/研究方向评估_输入.md"
    expected_guide = "050b8358124f48f73dd2c75a83c422298fb710ecf0c046c0d31d4d2cea0d45a4"
    require(digest(guide) == expected_guide, "The verbatim input guide differs from its recorded source")
    local_directories = [STUDY / name for name in ("models", "data", "output", ".work")]
    local_examples = [ROOT / "HOR/reports/assets" / f"0295_{kind}.jpg" for kind in ("detected", "gt")]
    local_examples.extend((REPORTS / "regions/visuals").rglob("*.jpg"))
    for path in local_directories + local_examples:
        require(ignore_status(path), f"A local-only resource is missing its ignore rule: {path}")
    require(ignore_status(STUDY / "reports/generated.html"), "Generated HTML must stay ignored")
    tracked = subprocess.run(["git", "ls-files", "-z", "--", "HOR/research"], cwd=ROOT,
                             capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    for relative in filter(None, tracked):
        path = ROOT / relative
        require(not any(path.is_relative_to(folder) for folder in local_directories),
                f"A local model, input, or raw cache is tracked: {relative}")
        require(path.suffix.lower() not in (".html", ".htm", ".mhtml", ".pth", ".pt", ".safetensors"),
                f"An excluded artifact is tracked in research: {relative}")
    return {"verbatim_guide_sha256": expected_guide,
            "local_only_directories_verified": len(local_directories),
            "restricted_local_examples_verified": len(local_examples),
            "generated_HTML_ignored": True}


def markdown_targets(path, parser, allow_generated=False):
    targets = []
    for token in parser.parse(path.read_text(encoding="utf-8")):
        for child in token.children or []:
            value = child.attrGet("src") if child.type == "image" else child.attrGet("href")
            if value is None:
                continue
            url = urlparse(value)
            if url.scheme or not url.path:
                continue
            destination = (path.parent / unquote(url.path)).resolve()
            scheduled = allow_generated and destination in (MANIFEST_PATH, VERIFICATION_PATH, ENVIRONMENT_PATH)
            require(destination.exists() or scheduled, f"Broken local Markdown target: {path}: {value}")
            require(destination.is_relative_to(ROOT), f"Markdown target leaves the workspace: {value}")
            targets.append({"report": path.relative_to(ROOT).as_posix(), "target": value,
                            "local_only": ignore_status(destination)})
    return targets


def audit_blind_materials():
    folder = REPORTS / "human_audit"
    images = read_csv(folder / "images_blind.csv")
    relations = read_csv(folder / "relations_blind.csv")
    require(len(images) == len(relations) == 200, "Empty blind forms must contain 100 images and two reviewer slots")
    identity_fields = {"image_key", "dataset_index", "file_name", "image_path", "image_sha256",
                       "image_width", "image_height", "rater_slot"}
    label_count = sum(bool(value.strip()) for rows in (images, relations) for row in rows
                      for key, value in row.items() if key not in identity_fields)
    require(label_count == 0, "Blind forms now contain labels; update the evidence state before publishing")
    require(not (folder / "candidate_review.csv").exists(), "Candidate review must remain hidden before blind review is frozen")
    manifest = read_json(STUDY / "output/human_audit/manifest.json")
    require(not manifest["phase1_frozen"], "Blank review forms cannot be frozen")
    require(len({row["image_sha256"] for row in images}) == 100, "Blind sample contains duplicated images")
    for stage in ("freeze", "candidates"):
        result = subprocess.run([sys.executable, str(STUDY / "scripts/prepare_human_audit.py"),
                                 "--stage", stage], cwd=ROOT, capture_output=True, text=True,
                                encoding="utf-8", check=False)
        require(result.returncode != 0, f"Blank blind forms incorrectly allowed stage {stage}")
        required_message = ("Every blind image row needs a rater" if stage == "freeze"
                            else "Complete and freeze the independent image/relationship review first")
        require(required_message in result.stderr, f"Stage {stage} failed for an unexpected reason: {result.stderr}")
    require(not (folder / "candidate_review.csv").exists(), "Guard checks released a candidate file")
    return {"images": 100, "reviewer_slots": 2, "filled_label_cells": label_count,
            "freeze_guard_rejected_blank_forms": True, "candidate_guard_rejected_unfrozen_forms": True}


def verify_identity_split():
    payload = read_json(REPORTS / "decoder/evidence/calibration_image_splits.json")
    audit = payload["identity_audit"]
    metadata = read_json(ROOT / payload["identity_metadata"])
    metadata_by_id = {int(item["image_id"]): item for item in metadata}
    with (ROOT / "HOR/output/random500/predictions.jsonl").open("r", encoding="utf-8") as handle:
        source_rows = [json.loads(line) for line in handle if line.strip()]
    source_by_index = {row["index"]: row for row in source_rows}
    require(len(source_by_index) == len(source_rows) == 500, "Source records have changed")
    for row in source_rows:
        image_path = ROOT / "data/PSG/images/test" / row["file_name"]
        require(digest(image_path) == row["image_sha256"], f"Source image bytes changed: {image_path}")
    sets_by_split = {}
    indices = []
    for split_name, rows in payload["splits"].items():
        sets = {"identity_keys": set(), "coco_image_ids": set(), "sha256": set()}
        for row in rows:
            source = source_by_index[row["index"]]
            metadata_entry = metadata_by_id[int(Path(source["file_name"]).stem)]
            require(row["file_name"] == source["file_name"] and row["image_sha256"] == source["image_sha256"],
                    f"Split identity differs from source: {row['index']}")
            require(row["coco_image_id"] == metadata_entry["coco_id"], "COCO source mapping differs")
            indices.append(row["index"])
            sets["identity_keys"].add(row["identity_key"])
            sets["coco_image_ids"].add(row["coco_image_id"])
            sets["sha256"].add(row["image_sha256"])
        require(len(rows) == audit["record_counts"][split_name], "Recorded split size differs")
        require(len(sets["identity_keys"]) == audit["unique_identity_counts"][split_name],
                "Recorded unique identity count differs")
        sets_by_split[split_name] = sets
    require(len(indices) == len(set(indices)) == 500 and set(indices) == set(source_by_index),
            "Split record coverage differs from the fixed source")
    for name in ("all_identity_keys_disjoint", "all_coco_ids_disjoint", "all_pixel_hashes_disjoint"):
        require(audit[name], f"Identity split failed: {name}")
    require(audit["unique_identity_counts"] == {"train": 299, "validation": 100, "test": 100},
            "Calibration identity counts changed")
    for pair, entries in audit["cross_split_overlaps"].items():
        require(not any(entries.values()), f"Identity overlap exists: {pair}")
    names = list(sets_by_split)
    for position, first in enumerate(names):
        for second in names[position + 1:]:
            for field in ("identity_keys", "coco_image_ids", "sha256"):
                require(not sets_by_split[first][field] & sets_by_split[second][field],
                        f"Recomputed source identity overlap: {first}, {second}, {field}")
    return audit


def verify_region_manifest():
    manifest = read_json(REPORTS / "regions/artifact_manifest.json")
    for relative, metadata in manifest["artifacts"].items():
        path = ROOT / relative
        require(path.is_file(), f"Missing region evidence: {relative}")
        require(path.stat().st_size == metadata["bytes"] and digest(path) == metadata["sha256"],
                f"Stale region signature: {relative}")
    return len(manifest["artifacts"])


def verify_copies():
    counts = {}
    for name in ("decoder", "parts"):
        count = 0
        for path in (REPORTS / name / "evidence").iterdir():
            if not path.is_file():
                continue
            source = STUDY / "output" / name / path.name
            require(source.is_file(), f"Missing local source for report evidence: {path}")
            require(digest(path) == digest(source), f"Evidence differs from local output: {path}")
            count += 1
        counts[name] = count
    return counts


def verify_mask2former_audit():
    audit = read_json(REPORTS / "regions/mask2former_loading_audit.json")
    protocol = audit["postprocessing_protocol"]
    checks = audit["checkpoint_checks"]
    signatures = audit["source_files"] + [audit["checkpoint"][name]
                                         for name in ("weights", "config", "preprocessor_config")]
    signatures.extend(protocol[name] for name in ("configuration_source", "region_call_source"))
    signatures.append(audit["unfused_candidate_inventory"]["source"])
    for signature in signatures:
        path = ROOT / signature["path"]
        require(path.is_file() and path.stat().st_size == signature["bytes"]
                and digest(path) == signature["sha256"], f"Mask2Former audit source changed: {path}")
    loading = audit["actual_cpu_loading"]
    require(loading["parameter_device_types"] == ["cpu"]
            and len(loading["missing_keys"]) == 2 and len(loading["unexpected_keys"]) == 12
            and not loading["mismatched_keys"] and not loading["error_msgs"],
            "Mask2Former loading evidence differs")
    require(loading["final_layernorm_weight_unique"] == [1.0]
            and loading["final_layernorm_bias_unique"] == [0.0], "Unconsumed final norm initialization differs")
    for name, count, flag in (("relative_position_indices", 12, "equal_after_flatten"),
                              ("learned_relative_bias_tables", 12, "equal"),
                              ("stage_output_normalizations", 8, "equal")):
        require(len(checks[name]) == count and all(item[flag] for item in checks[name]),
                f"Mask2Former checkpoint comparison failed: {name}")
    require(not protocol["label_ids_to_fuse_argument_provided"] and protocol["effective_fusion_label_ids"] == [],
            "Region results require the recorded unfused query protocol")
    require(audit["feature_path"]["pixel_decoder_uses_backbone_feature_maps"]
            and not audit["feature_path"]["final_swin_layernorm_output_consumed_by_feature_maps"],
            "Mask2Former feature path differs")
    require(audit["execution_scope"]["image_forward_passes"] == 0
            and audit["execution_scope"]["pixel_images_opened"] == 0, "CPU audit execution scope differs")
    for name in ("runtime.json", "compute_profile.json"):
        require(digest(REPORTS / "regions/evidence" / name) == digest(STUDY / "output/regions" / name),
                f"Region runtime evidence differs: {name}")
    return {"source_signatures": len(signatures), "matching_position_indices": 12,
            "matching_learned_bias_tables": 12, "matching_stage_norm_tensors": 8,
            "postprocessing": "unfused query regions", "image_forward_passes": 0}


def run_evidence_audit(script_name):
    result = subprocess.run([sys.executable, str(STUDY / "scripts" / script_name)],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(result.stdout, parse_constant=reject_nonfinite_constant)


def environment_snapshot():
    packages = {distribution.metadata["Name"]: distribution.version
                for distribution in importlib.metadata.distributions()}
    require(torch.cuda.is_available(), "This delivery records CUDA results and requires the recorded CUDA device")
    device = torch.cuda.get_device_properties(0)
    return {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "python_executable": sys.executable,
            "platform": platform.platform(), "pytorch_cuda": torch.version.cuda,
            "device": {"name": device.name, "total_memory_bytes": device.total_memory,
                       "compute_capability": [device.major, device.minor]},
            "packages": dict(sorted(packages.items(), key=lambda item: item[0].lower()))}


def main():
    scripts = sorted((STUDY / "scripts").glob("*.py"))
    for path in scripts:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        require(ast.get_docstring(tree) is None, f"Module-level docstring violates the coding convention: {path}")
        require(not path.read_text(encoding="utf-8-sig").startswith("#!"), f"Unexpected shebang: {path}")
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                require(not any(isinstance(item, (ast.Import, ast.ImportFrom))
                                for item in ast.walk(node)), f"Import protected by try/except: {path}")
    json_paths = sorted((STUDY / "configs").glob("*.json")) + sorted(REPORTS.rglob("*.json"))
    for path in json_paths:
        read_json(path)
    parser = MarkdownIt("commonmark").enable("table")
    navigation = [ROOT / "README.md", ROOT / "HOR/README.md", STUDY / "README.md"]
    markdown_paths = sorted(REPORTS.rglob("*.md")) + navigation
    targets = [target for path in markdown_paths for target in markdown_targets(path, parser, allow_generated=True)]
    image_paths = sorted(REPORTS.rglob("*.png")) + sorted(REPORTS.rglob("*.jpg"))
    for path in image_paths:
        with Image.open(path) as artifact:
            artifact.verify()
    identity = verify_identity_split()
    delivery_scope = verify_delivery_scope()
    artifact_count = verify_region_manifest()
    copies = verify_copies()
    mask2former = verify_mask2former_audit()
    blind = audit_blind_materials()
    independent_audits = {"decoder": run_evidence_audit("audit_decoder.py"),
                          "active_detection": run_evidence_audit("audit_active_detection.py"),
                          "parts": run_evidence_audit("audit_part_evidence.py"),
                          "controlled_3d": run_evidence_audit("audit_controlled_3d.py")}
    write_json(ENVIRONMENT_PATH, environment_snapshot())
    evidence = [path for directory in (STUDY / "scripts", STUDY / "configs", REPORTS)
                for path in directory.rglob("*")
                if path.is_file() and not ignore_status(path)
                and path not in (MANIFEST_PATH, VERIFICATION_PATH)]
    evidence.extend(navigation)
    evidence.extend((ROOT / ".gitignore", ROOT / "HOR/export_reports.py"))
    entries = {path.relative_to(ROOT).as_posix(): {"bytes": path.stat().st_size, "sha256": digest(path)}
               for path in sorted(set(evidence))}
    write_json(MANIFEST_PATH, {"artifacts": entries, "artifact_count": len(entries),
                               "excluded": "Git-ignored models, data, raw outputs, caches, and restricted example JPEGs"})
    verification = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
                    "syntax_checked_scripts": len(scripts), "parsed_json_files": len(json_paths),
                    "markdown_files_checked": len(markdown_paths), "markdown_local_targets": len(targets),
                    "local_only_targets": [target for target in targets if target["local_only"]],
                    "image_files_decoded_without_visual_review": len(image_paths),
                    "region_artifacts_verified": artifact_count, "report_evidence_copies_verified": copies,
                    "mask2former_loading_and_protocol_audit": mask2former,
                    "source_identity_counts": identity["unique_identity_counts"],
                    "delivery_scope": delivery_scope,
                    "blind_review": blind,
                    "independent_numeric_audits": independent_audits,
                    "delivery_artifacts": len(entries),
                    "scope": "Scientific evidence and integrity checks; this does not label images or validate unrun real 3D studies"}
    write_json(VERIFICATION_PATH, verification)
    for path in markdown_paths:
        markdown_targets(path, parser)
    print(json.dumps(verification, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
