import ast
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random
import statistics
import subprocess

import numpy as np
import torch
from torchvision.ops import box_iou

from pipeline import CONFIG, HOR_DIR, ROOT, save_json, sha256


def independent_metrics(records, mode, ranking):
    image_recalls = {k: [] for k in (20, 50)}
    class_recalls = {k: defaultdict(list) for k in (20, 50)}
    pooled = Counter()
    total = 0
    for record in records:
        gt = record["ground_truth_relations"]
        if not gt:
            continue
        prediction = record[mode]
        references = record["ground_truth_objects"]
        if mode == "detected":
            matches = {item["id"]: set() for item in references}
            if prediction["objects"]:
                overlaps = box_iou(torch.tensor([item["box_xyxy"] for item in references]),
                                   torch.tensor([item["box_xyxy"] for item in prediction["objects"]])).numpy()
                for g, item in enumerate(references):
                    matches[item["id"]] = {predicted["id"] for p, predicted in enumerate(prediction["objects"])
                                           if overlaps[g, p] >= .5 and item["label"] == predicted["label"]}
        else:
            matches = {item["id"]: {item["id"]} for item in references}
        denominators = Counter(row["predicate_id"] for row in gt)
        total += len(gt)
        for k in (20, 50):
            correct = []
            for truth in gt:
                if any(row["subject_id"] in matches[truth["subject_id"]]
                       and row["object_id"] in matches[truth["object_id"]]
                       and row["predicate_id"] == truth["predicate_id"]
                       for row in prediction[ranking][:k]):
                    correct.append(truth)
            image_recalls[k].append(len(correct) / len(gt))
            numerators = Counter(row["predicate_id"] for row in correct)
            pooled[k] += len(correct)
            for predicate, number in denominators.items():
                class_recalls[k][predicate].append(numerators[predicate] / number)
    metrics = {}
    for k in (20, 50):
        metrics[f"R@{k}"] = statistics.mean(image_recalls[k])
        metrics[f"mR@{k}"] = statistics.mean(statistics.mean(values) for values in class_recalls[k].values())
        metrics[f"pooled_R@{k}"] = pooled[k] / total
    return metrics


def main():
    torch.set_num_threads(8)
    output = HOR_DIR / "output/random500"
    records = [json.loads(line) for line in (output / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
    manifest = json.loads((output / "sample_manifest.json").read_text(encoding="utf-8"))
    evaluations = json.loads((output / "evaluation.json").read_text(encoding="utf-8"))
    runtime = json.loads((output / "runtime.json").read_text(encoding="utf-8"))
    expected = random.Random(CONFIG["seed"]).sample(range(2179), 500)
    assert manifest["indices"] == expected
    assert [row["index"] for row in records] == expected and len(set(expected)) == 500
    assert manifest["config"] == CONFIG and runtime["config_sha256"] == sha256(HOR_DIR / "config.json")
    sources_checked = 0
    for name, digest in runtime["sources_sha256"].items():
        assert sha256(HOR_DIR / name) == digest, name
        sources_checked += 1
    for name, digest in runtime["resources_sha256"].items():
        assert sha256(ROOT / name) == digest, name
    pair_checks = 0
    tensor_checks = 0
    categories = json.loads((ROOT / "data/PSG/packed/psg/test/meta.json").read_text(encoding="utf-8"))["categories"]
    meta = np.load(ROOT / "data/PSG/packed/psg/test/img_meta.npy")
    labels = np.load(ROOT / "data/PSG/packed/psg/test/box_cats.npy")
    raw_rels = np.load(ROOT / "data/PSG/packed/psg/test/rels.npy")
    for record in records:
        index = record["index"]
        _, _, _, b0, nb, r0, nr = meta[index]
        reference = record["ground_truth_objects"]
        assert [item["id"] for item in reference] == list(range(int(nb)))
        assert [item["label"] for item in reference] == [categories[int(label)] for label in labels[b0:b0 + nb]]
        truth = {tuple(int(value) for value in row[:3]) for row in raw_rels[r0:r0 + nr]
                 if reference[int(row[0])]["is_person"] or reference[int(row[1])]["is_person"]}
        assert truth == {(row["subject_id"], row["object_id"], row["predicate_id"]) for row in record["ground_truth_relations"]}
        assert (HOR_DIR / "reports/cases" / f"{index:04d}.md").is_file()
        for mode in ("detected", "gt_boxes", "official400"):
            prediction = record[mode]
            objects = {item["id"]: item for item in prediction["objects"]}
            assert prediction["human_ids"] == [item["id"] for item in objects.values() if item["is_person"]]
            for ranking in ("relations", "single_predicate_top50"):
                ranked = prediction[ranking]
                assert len(ranked) <= 50
                assert len({(row["subject_id"], row["object_id"], row["predicate_id"]) for row in ranked}) == len(ranked)
                assert [row["fused_logit"] for row in ranked] == sorted([row["fused_logit"] for row in ranked], reverse=True)
                for row in ranked:
                    s, o = objects[row["subject_id"]], objects[row["object_id"]]
                    assert s["is_person"] or o["is_person"]
                    assert s["id"] != o["id"]
                    assert row["subject_label"] == s["label"] and row["object_label"] == o["label"]
                    assert math.isclose(row["fused_logit"], row["predicate_logit"] + row["pair_logit"], abs_tol=1e-6)
            if mode != "official400":
                expected_pairs = {(s["id"], o["id"]) for s in objects.values() for o in objects.values()
                                  if s["id"] != o["id"] and (s["is_person"] or o["is_person"])}
                actual_pairs = {(pair["subject_id"], pair["object_id"]) for pair in prediction["all_human_pairs"]}
                assert expected_pairs == actual_pairs
                pair_checks += 1
                assert (output / "images" / f"{index:04d}_{'detected' if mode == 'detected' else 'gt'}.jpg").is_file()
                if prediction["candidate_pairs"]:
                    with np.load(output / "logits" / mode / f"{index:04d}.npz") as arrays:
                        assert np.isfinite(arrays["predicate_logits"]).all()
                        assert np.isfinite(arrays["pair_logits"]).all()
                        assert len(arrays["subject_indices"]) == len(objects) * (len(objects) - 1)
                        mapping = {(int(s), int(o)): slot for slot, (s, o) in enumerate(zip(arrays["subject_indices"], arrays["object_indices"]))}
                        for pair in prediction["all_human_pairs"]:
                            slot = mapping[pair["subject_id"], pair["object_id"]]
                            for row in pair["predictions"]:
                                assert float(arrays["predicate_logits"][slot, row["predicate_id"]]) == row["predicate_logit"]
                                assert float(arrays["pair_logits"][slot]) == row["pair_logit"]
                        tensor_checks += 1
    max_difference = 0.0
    conditions = []
    for mode in ("detected", "gt_boxes", "official400"):
        for ranking in ("relations", "single_predicate_top50"):
            measured = independent_metrics(records, mode, ranking)
            target = evaluations[f"{mode}/{ranking}"]
            difference = max(abs(value - target["metrics"][key]) for key, value in measured.items())
            assert difference < 1e-12
            assert sum(target["failure_stages"].values()) == target["unique_gt"]
            max_difference = max(max_difference, difference)
            conditions.append(f"{mode}/{ranking}")
    for path in HOR_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert ast.get_docstring(tree) is None and not source.startswith("#!")
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                assert not any(isinstance(child, (ast.Import, ast.ImportFrom))
                               for statement in node.body for child in ast.walk(statement))
    assert not subprocess.check_output(["git", "-C", str(ROOT / "RelateAnything"), "status", "--porcelain"], text=True).strip()
    result = {"passed": True, "images": len(records), "independent_metric_conditions": conditions,
              "max_metric_abs_difference": max_difference, "human_pair_coverage_checks": pair_checks,
              "full_logit_files_checked": tensor_checks, "GT_numbering_and_relation_checks": len(records),
              "numbered_images": 1000, "detailed_case_reports": 500,
              "source_hashes_checked": sources_checked, "resource_hashes_checked": len(runtime["resources_sha256"]),
              "python_module_rules_checked": True, "official_source_clean": True}
    save_json(output / "verification.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
