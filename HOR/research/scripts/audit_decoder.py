import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.special import expit


ROOT = Path(__file__).resolve().parents[3]
STUDY = ROOT / "HOR/research"
EVIDENCE = STUDY / "reports/decoder/evidence"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def compare(value, reference, name):
    require(np.isclose(value, reference, rtol=1e-10, atol=1e-12),
            f"Independent decoder audit differs for {name}: {value}, {reference}")


def overlap(first, second):
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    intersection = max(right - left, 0) * max(bottom - top, 0)
    first_area = max(first[2] - first[0], 0) * max(first[3] - first[1], 0)
    second_area = max(second[2] - second[0], 0) * max(second[3] - second[1], 0)
    union = first_area + second_area - intersection
    require(union > 0, "A source bounding box has no positive area")
    return intersection / union


def relation_key(row):
    return row["subject_id"], row["object_id"], row["predicate_id"]


def matched_truths(row, record, correspondence):
    return {
        relation_key(truth)
        for truth in record["ground_truth_relations"]
        if truth["subject_id"] in correspondence[row["subject_id"]]
        and truth["object_id"] in correspondence[row["object_id"]]
        and truth["predicate_id"] == row["predicate_id"]
        and row["subject_id"] != row["object_id"]
    }


def summarize(truths_by_index, hits_by_index):
    image_values = []
    by_predicate = defaultdict(list)
    for index, truths in truths_by_index.items():
        if not truths:
            continue
        hits = hits_by_index[index] & truths
        image_values.append(len(hits) / len(truths))
        counts = Counter(key[2] for key in truths)
        recalled = Counter(key[2] for key in hits)
        for predicate, count in counts.items():
            by_predicate[predicate].append(recalled[predicate] / count)
    total = sum(map(len, truths_by_index.values()))
    hits = sum(len(hits_by_index[index] & truths) for index, truths in truths_by_index.items())
    return {"images_with_GT": len(image_values), "GT": total, "hits": hits,
            "R@50_image_macro": float(np.mean(image_values)),
            "mR@50_class_macro": float(np.mean([np.mean(values) for values in by_predicate.values()])),
            "pooled_R@50": hits / total}


def calibration_error(probabilities, labels, number):
    edges = np.linspace(0.0, 1.0, number + 1)
    counts, _ = np.histogram(probabilities, bins=edges)
    probability_sums, _ = np.histogram(probabilities, bins=edges, weights=probabilities)
    label_sums, _ = np.histogram(probabilities, bins=edges, weights=labels)
    require(int(counts.sum()) == len(labels), "Calibration bins did not cover every candidate")
    return float(np.abs(probability_sums - label_sums).sum() / len(labels))


def audit_calibration(rows, splits, config):
    result = read_json(EVIDENCE / "calibration_metrics.json")
    official = read_json(ROOT / config["official_calibration"])
    fit = result["fit"]
    for key in ("a", "b"):
        compare(official[key], result["official"][key], f"official calibration {key}")
    all_split_rows = [row for values in splits["splits"].values() for row in values]
    by_identity = defaultdict(list)
    for row in all_split_rows:
        by_identity[row["identity_key"]].append(row)
    canonical = {identity: min(values, key=lambda row: row["sample_position"])["index"]
                 for identity, values in by_identity.items()}
    merged_labels = defaultdict(int)
    for row in rows:
        key = (row["identity_key"], *relation_key(row))
        merged_labels[key] = max(merged_labels[key], row["annotation_match_proxy"])
    prepared = {}
    for name in ("train", "validation", "test"):
        selected = [row for row in rows if row["image_split"] == name
                    and (name != "train" or row["index"] == canonical[row["identity_key"]])]
        labels = np.asarray([
            merged_labels[(row["identity_key"], *relation_key(row))]
            if name == "train" else row["annotation_match_proxy"] for row in selected], dtype=float)
        logits = np.asarray([row["fused_logit"] for row in selected])
        expected = result["split_metrics"][name]
        require(len(selected) == expected["candidate_rows"], f"Candidate count differs in {name}")
        require(int(labels.sum()) == expected["positive_annotation_match_proxy_rows"],
                f"Merged proxy positives differ in {name}")
        compare(float(labels.mean()), expected["proxy_prevalence"], f"{name} prevalence")
        prepared[name] = (selected, logits, labels)
    _, train_logits, train_labels = prepared["train"]
    train_rate = float(train_labels.mean())
    compare(train_rate, fit["train_proxy_prevalence"], "training-only constant")
    residual = expit(fit["a"] * train_logits + fit["b"]) - train_labels
    gradient = np.asarray([np.mean(residual * train_logits) * fit["a"], residual.mean()])
    require(float(np.max(np.abs(gradient))) < 1e-4, "Fitted Platt parameters are not near a stationary point")
    _, logits, labels = prepared["test"]
    methods = {"raw_sigmoid": expit(logits),
               "official": expit(official["a"] * logits + official["b"]),
               "local_platt": expit(fit["a"] * logits + fit["b"]),
               "train_prevalence": np.full(len(logits), train_rate)}
    for name, scores in methods.items():
        expected = result["split_metrics"]["test"][name]
        compare(calibration_error(scores, labels, config["calibration_bins"]),
                expected["ECE_annotation_match_proxy"], f"{name} ECE")
        compare(float(np.mean((scores - labels) ** 2)), expected["Brier_annotation_match_proxy"],
                f"{name} Brier")
    return {"test_candidates": len(labels), "test_proxy_positives": int(labels.sum()),
            "train_candidates_after_identity_deduplication": len(train_labels),
            "maximum_platt_objective_gradient": float(np.max(np.abs(gradient)))}, prepared


def audit_selective(prepared, truths, fixed, records, correspondence):
    validation_rows = prepared["validation"][0]
    test_rows = prepared["test"][0]
    validation_margins = np.asarray([row["margin"] for row in validation_rows])
    choices = [(float(np.mean(validation_margins >= threshold)), float(threshold))
               for threshold in np.unique(validation_margins)] + [(0.0, float("inf"))]
    test_indices = {index for index in records
                    if records[index]["audit_split"] == "test"}
    for row in read_csv(EVIDENCE / "margin_selective_thresholds.csv"):
        target = float(row["target_coverage_from_validation"])
        coverage, threshold = min(choices, key=lambda item: (abs(item[0] - target), item[0]))
        compare(threshold, float(row["margin_threshold"]), "validation-only margin threshold")
        compare(coverage, float(row["validation_achieved_coverage"]), "validation threshold coverage")
        kept = [candidate for candidate in test_rows if candidate["margin"] >= threshold]
        require(len(kept) == int(row["test_kept_candidates"]), "Selective output count differs")
        kept_positive = sum(candidate["annotation_match_proxy"] for candidate in kept)
        require(kept_positive == int(row["test_annotation_match_candidates_retained"]),
                "Selective retained proxy positives differ")
        compare(len(kept) / len(test_rows), float(row["test_coverage"]), "test selective coverage")
        compare(kept_positive / len(kept), float(row["annotation_match_rate_proxy"]),
                "retained annotation-match rate")
        hit_keys = defaultdict(set)
        for candidate in kept:
            index = candidate["index"]
            hit_keys[index].update(matched_truths(candidate, records[index], correspondence[index]))
        for name, gt, field in (("all", truths, "test_GT"),
                                ("fixed", fixed, "test_valid_endpoint_GT")):
            denominator = sum(len(gt[index]) for index in test_indices)
            hits = sum(len(hit_keys[index] & gt[index]) for index in test_indices)
            denominator_field = "all_968_test_GT" if name == "all" else "test_valid_endpoint_GT"
            require(denominator == int(row[denominator_field]), f"Selective {name} GT count differs")
            require(hits == int(row[field + "_recalled"]), f"Selective {name} GT hits differ")
            compare(hits / denominator, float(row[field + "_pooled_recall"]),
                    f"Selective {name} pooled recall")


def main():
    config = read_json(STUDY / "configs/decoder_study.json")
    with (ROOT / config["input_predictions"]).open(encoding="utf-8") as handle:
        source = [json.loads(line) for line in handle if line.strip()]
    records = {row["index"]: row for row in source}
    require(len(records) == len(source) == 500, "Decoder source sample differs")
    splits = read_json(EVIDENCE / "calibration_image_splits.json")
    split_by_index = {row["index"]: name for name, values in splits["splits"].items() for row in values}
    for index, record in records.items():
        record["audit_split"] = split_by_index[index]
    truths = {index: {relation_key(row) for row in record["ground_truth_relations"]}
              for index, record in records.items()}
    fixed = {index: set() for index in records}
    for row in read_json(EVIDENCE / "fixed_valid_endpoint_gt.json")["relations"]:
        fixed[row["index"]].add(relation_key(row))
    correspondence = {}
    for index, record in records.items():
        correspondence[index] = {
            box["id"]: {truth["id"] for truth in record["ground_truth_objects"]
                        if box["label"] == truth["label"]
                        and overlap(box["box_xyxy"], truth["box_xyxy"]) >= config["iou_threshold"]}
            for box in record["detected"]["objects"]}
    rows = read_csv(EVIDENCE / "selected_candidates.csv")
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        for field in ("index", "sample_position", "subject_id", "object_id", "predicate_id",
                      "pair_local_rank", "annotation_match_proxy"):
            row[field] = int(row[field])
        for field in ("fused_logit", "margin"):
            row[field] = float(row[field])
        require(row["image_split"] == split_by_index[row["index"]], "Candidate split differs from image split")
        row_hits = matched_truths(row, records[row["index"]], correspondence[row["index"]])
        require(bool(row_hits) == bool(row["annotation_match_proxy"]), "Candidate proxy label differs from source boxes")
        grouped[row["method"]][row["index"]].append(row)
    expected = read_json(EVIDENCE / "decoding_metrics.json")
    require(set(grouped) == set(expected), "Decoder method set differs")
    for method, candidates in grouped.items():
        hits = defaultdict(set)
        for index, selected in candidates.items():
            require(len(selected) <= config["per_image_budget"], "Top-50 budget exceeded")
            require(len({relation_key(row) for row in selected}) == len(selected), "Duplicated relation output")
            for row in selected:
                hits[index].update(matched_truths(row, records[index], correspondence[index]))
        for name, reference_truths in (("all_968_GT", truths), ("fixed_530_valid_endpoint_GT", fixed)):
            measured = summarize(reference_truths, hits)
            for field, value in measured.items():
                compare(value, expected[method][name][field], f"{method}, {name}, {field}")
        require(sum(map(len, candidates.values())) == expected[method]["predictions_under_budget"],
                f"Total output budget differs for {method}")
    oracle_rows = read_csv(EVIDENCE / "gt_box_selected_candidates.csv")
    oracle_groups = defaultdict(lambda: defaultdict(set))
    oracle_counts = Counter()
    for row in oracle_rows:
        for field in ("index", "subject_id", "object_id", "predicate_id"):
            row[field] = int(row[field])
        oracle_groups[row["method"]][row["index"]].add(relation_key(row))
        oracle_counts[row["method"]] += 1
    oracle_expected = read_json(EVIDENCE / "fixed530_endpoint_oracle_metrics.json")["methods"]
    require(set(oracle_groups) == set(expected), "GT-box oracle method set differs")
    for method, candidates in oracle_groups.items():
        measured = summarize(fixed, candidates)
        for field, value in measured.items():
            compare(value, oracle_expected[method][field], f"{method} GT-box oracle {field}")
        require(oracle_counts[method] == oracle_expected[method]["predictions_under_budget"],
                "GT-box oracle output count differs")
        require(all(len(selected) <= config["per_image_budget"] for selected in candidates.values()),
                "GT-box oracle exceeded Top-50 budget")
    dual_rows = [row for row in rows if row["method"] == "dual"]
    calibration, prepared = audit_calibration(dual_rows, splits, config)
    audit_selective(prepared, truths, fixed, records, correspondence)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (EVIDENCE / "selected_candidates.csv", EVIDENCE / "decoding_metrics.json",
                           EVIDENCE / "calibration_metrics.json", EVIDENCE / "margin_selective_thresholds.csv")}
    print(json.dumps({"source_records": len(source), "verified_candidate_rows": len(rows),
                      "verified_GT_box_candidate_rows": len(oracle_rows),
                      "verified_decoding_methods": len(expected), "total_GT": sum(map(len, truths.values())),
                      "fixed_endpoint_GT": sum(map(len, fixed.values())), "calibration": calibration,
                      "selective_validation_and_test_counts": "passed", "evidence_sha256": hashes},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
