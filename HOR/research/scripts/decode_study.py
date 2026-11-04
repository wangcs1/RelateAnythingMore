import argparse
import csv
import json
import math
from pathlib import Path
import shutil
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "HOR/research/configs/decoder_study.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sigmoid(values):
    values = np.asarray(values, dtype=np.float64)
    return np.exp(-np.logaddexp(0.0, -values))


def safe_nanmean(values, axis):
    values = np.asarray(values, dtype=np.float64)
    valid = np.isfinite(values)
    counts = valid.sum(axis=axis)
    totals = np.nansum(values, axis=axis)
    return np.divide(totals, counts, out=np.full_like(totals, np.nan, dtype=np.float64), where=counts > 0)


def box_iou(first, second):
    if not first or not second:
        return np.zeros((len(first), len(second)), dtype=np.float64)
    a = np.asarray([row["box_xyxy"] for row in first], dtype=np.float64)
    b = np.asarray([row["box_xyxy"] for row in second], dtype=np.float64)
    left_top = np.maximum(a[:, None, :2], b[None, :, :2])
    right_bottom = np.minimum(a[:, None, 2:], b[None, :, 2:])
    intersection = np.maximum(right_bottom - left_top, 0).prod(axis=2)
    area_a = np.maximum(a[:, 2:] - a[:, :2], 0).prod(axis=1)
    area_b = np.maximum(b[:, 2:] - b[:, :2], 0).prod(axis=1)
    union = area_a[:, None] + area_b[None, :] - intersection
    return np.divide(intersection, union, out=np.zeros_like(intersection), where=union > 0)


def endpoint_matches(predicted, ground_truth, threshold):
    overlaps = box_iou(ground_truth, predicted)
    result = {item["id"]: set() for item in ground_truth}
    for gt_index, truth in enumerate(ground_truth):
        for pred_index, detection in enumerate(predicted):
            if truth["label"] == detection["label"] and overlaps[gt_index, pred_index] >= threshold:
                result[truth["id"]].add(detection["id"])
    return result


def stable_rows(rows):
    return sorted(rows, key=lambda row: (-row["fused_logit"], row["subject_id"],
                                         row["object_id"], row["predicate_id"]))


def pair_candidates(record, arrays, predicates, spatial_ids, method, local_m=None):
    objects = {item["id"]: item for item in record[method]["objects"]}
    subjects = arrays["subject_indices"].astype(np.int64)
    objects_by_pair = arrays["object_indices"].astype(np.int64)
    pred_logits = arrays["predicate_logits"].astype(np.float64)
    pair_logits = arrays["pair_logits"].astype(np.float64)
    if not (len(subjects) == len(objects_by_pair) == len(pred_logits) == len(pair_logits)):
        raise ValueError(f"Mismatched logit rows for image {record['index']} in {method}")
    spatial_ids = np.asarray(spatial_ids, dtype=np.int64)
    semantic_ids = np.asarray(sorted(set(range(len(predicates))) - set(spatial_ids)), dtype=np.int64)
    human_pair_ids = {item["id"] for item in record[method]["objects"] if item["is_person"]}
    result = {"top1": [], "top2": [], "top3": [], "top5": [], "dual": [], "single": []}
    rank_map = {}
    pair_map = {}
    for slot, (subject_id, object_id) in enumerate(zip(subjects, objects_by_pair)):
        subject_id, object_id = int(subject_id), int(object_id)
        if subject_id not in human_pair_ids and object_id not in human_pair_ids:
            continue
        logits = pred_logits[slot] + pair_logits[slot]
        pred_order = sorted(range(len(predicates)), key=lambda pid: (-float(logits[pid]), pid))
        spatial_order = sorted(spatial_ids.tolist(), key=lambda pid: (-float(logits[pid]), pid))
        semantic_order = sorted(semantic_ids.tolist(), key=lambda pid: (-float(logits[pid]), pid))
        ranks = {predicate_id: rank + 1 for rank, predicate_id in enumerate(pred_order)}
        rank_map[(subject_id, object_id)] = ranks
        group_orders = {"spatial": spatial_order, "semantic": semantic_order}
        group_ranks = {name: {predicate_id: rank + 1 for rank, predicate_id in enumerate(order)}
                       for name, order in group_orders.items()}
        rows = []
        for rank, predicate_id in enumerate(pred_order):
            rows.append({"index": record["index"], "sample_position": record["sample_position"],
                         "file_name": record["file_name"], "subject_id": subject_id,
                         "subject_label": objects[subject_id]["label"], "object_id": object_id,
                         "object_label": objects[object_id]["label"], "predicate_id": predicate_id,
                         "predicate": predicates[predicate_id], "fused_logit": float(logits[predicate_id]),
                         "pair_local_rank": rank + 1,
                         "margin": float(logits[predicate_id] - logits[pred_order[rank + 1]])
                         if rank + 1 < len(pred_order) else math.inf,
                         "stream": "spatial" if predicate_id in spatial_ids else "semantic"})
        pair_map[(subject_id, object_id)] = rows
        result["single"].append(rows[0])
        for count in (1, 2, 3, 5):
            result[f"top{count}"].extend(rows[:count])
        for stream, order in group_orders.items():
            first = order[0]
            second = order[1]
            result["dual"].append({"index": record["index"], "sample_position": record["sample_position"],
                                   "file_name": record["file_name"], "subject_id": subject_id,
                                   "subject_label": objects[subject_id]["label"], "object_id": object_id,
                                   "object_label": objects[object_id]["label"], "predicate_id": first,
                                   "predicate": predicates[first], "fused_logit": float(logits[first]),
                                   "pair_local_rank": ranks[first],
                                   "margin": float(logits[first] - logits[second]), "stream": stream,
                                   "group_rank": 1})
    for key in result:
        result[key] = stable_rows(result[key])
    return result, rank_map, pair_map


def exact_gt_hit_counts(rows, truths, predicate_count):
    predicted = {(row["subject_id"], row["object_id"], row["predicate_id"]) for row in rows}
    hits = np.zeros(predicate_count, dtype=np.int64)
    hit_keys = set()
    for truth in truths:
        key = (truth["subject_id"], truth["object_id"], truth["predicate_id"])
        if key in predicted:
            hits[truth["predicate_id"]] += 1
            hit_keys.add(key)
    return hits, hit_keys


def annotation_labels(rows, ground_truth, matches):
    labels = []
    for row in rows:
        labels.append(int(any(
            row["predicate_id"] == truth["predicate_id"]
            and row["subject_id"] in matches[truth["subject_id"]]
            and row["object_id"] in matches[truth["object_id"]]
            and row["subject_id"] != row["object_id"]
            for truth in ground_truth)))
    return np.asarray(labels, dtype=np.int64)


def hit_counts(rows, labels, predicate_count):
    hits = np.zeros(predicate_count, dtype=np.int64)
    for row, label in zip(rows, labels):
        if label:
            hits[row["predicate_id"]] += 1
    return hits


def gt_hit_counts(rows, ground_truth, matches, predicate_count):
    hit_triples = set()
    lookup = {(row["subject_id"], row["object_id"], row["predicate_id"]) for row in rows}
    for truth in ground_truth:
        subject_matches = matches.get(truth["subject_id"], set())
        object_matches = matches.get(truth["object_id"], set())
        if any((subject_id, object_id, truth["predicate_id"]) in lookup
               for subject_id in subject_matches for object_id in object_matches
               if subject_id != object_id):
            hit_triples.add((truth["subject_id"], truth["object_id"], truth["predicate_id"]))
    counts = np.zeros(predicate_count, dtype=np.int64)
    for _, _, predicate_id in hit_triples:
        counts[predicate_id] += 1
    return counts, hit_triples


def metric_summary(per_image, predicate_count, valid_only=False):
    image_recall = []
    image_predicate_recall = []
    total_hit = 0
    total_gt = 0
    class_hits = np.zeros(predicate_count, dtype=np.float64)
    class_gt = np.zeros(predicate_count, dtype=np.float64)
    for item in per_image:
        gt = item["valid_gt_counts"] if valid_only else item["gt_counts"]
        hits = item["valid_hits"] if valid_only else item["hits"]
        count = int(gt.sum())
        if count == 0:
            continue
        image_recall.append(float(hits.sum() / count))
        image_predicate_recall.append(np.divide(hits, gt, out=np.full(predicate_count, np.nan), where=gt > 0))
        total_hit += int(hits.sum())
        total_gt += count
        class_hits += hits
        class_gt += gt
    class_present = class_gt > 0
    macro_recall = float(np.mean(image_recall)) if image_recall else None
    image_class_matrix = np.asarray(image_predicate_recall, dtype=np.float64)
    per_class_values = safe_nanmean(image_class_matrix, axis=0) if image_recall else np.full(predicate_count, np.nan)
    return {"images_with_GT": len(image_recall), "GT": total_gt, "hits": total_hit,
            "R@50_image_macro": macro_recall,
            "mR@50_class_macro": float(np.nanmean(per_class_values)) if class_present.any() else None,
            "pooled_R@50": total_hit / total_gt if total_gt else None,
            "class_gt": class_gt.astype(np.int64), "class_hits": class_hits.astype(np.int64),
            "image_recall": np.asarray(image_recall, dtype=np.float64),
            "image_predicate_recall": np.asarray(image_predicate_recall, dtype=np.float64)}


def calibration_bins(probabilities, labels, count):
    bins = []
    ece = 0.0
    for bin_index in range(count):
        lower = bin_index / count
        upper = (bin_index + 1) / count
        selected = ((probabilities >= lower) & (probabilities < upper if bin_index + 1 < count
                                                  else probabilities <= upper))
        number = int(selected.sum())
        mean_probability = float(probabilities[selected].mean()) if number else None
        match_rate = float(labels[selected].mean()) if number else None
        if number:
            ece += number / len(labels) * abs(mean_probability - match_rate)
        bins.append({"bin": bin_index + 1, "lower": lower, "upper": upper, "count": number,
                     "mean_confidence": mean_probability, "annotation_match_rate": match_rate})
    return float(ece), bins


def fit_platt(logits, labels):
    if len(np.unique(labels)) != 2:
        raise ValueError("Platt fitting needs both proxy-label classes in train images")

    def objective(parameters):
        slope = math.exp(float(parameters[0]))
        transformed = slope * logits + parameters[1]
        return float(np.mean(np.logaddexp(0.0, transformed) - labels * transformed))

    fit = minimize(objective, np.asarray([math.log(0.5), -2.0]), method="L-BFGS-B",
                   bounds=[(-8.0, 8.0), (-20.0, 20.0)])
    if not fit.success:
        raise RuntimeError(f"Platt optimization failed: {fit.message}")
    return {"a": math.exp(float(fit.x[0])), "b": float(fit.x[1]),
            "train_candidate_rows": int(len(labels)), "train_positive_rows": int(labels.sum()),
            "train_proxy_prevalence": float(labels.mean()), "optimizer_message": str(fit.message)}


def image_identity_map(records, metadata_path):
    metadata = read_json(metadata_path)
    vg_by_id = {}
    for row in metadata:
        image_id = int(row["image_id"])
        if image_id in vg_by_id:
            raise ValueError(f"Duplicate Visual Genome image_id in identity metadata: {image_id}")
        vg_by_id[image_id] = row
    image_rows = {}
    for record in records:
        vg_image_id = int(Path(record["file_name"]).stem)
        vg_row = vg_by_id.get(vg_image_id)
        coco_id = int(vg_row["coco_id"]) if vg_row is not None and vg_row.get("coco_id") is not None else None
        image_rows[record["index"]] = {"index": record["index"],
                                       "sample_position": record["sample_position"],
                                       "file_name": record["file_name"],
                                       "vg_image_id": vg_image_id if vg_row is not None else None,
                                       "coco_image_id": coco_id,
                                       "image_sha256": record["image_sha256"]}
    parents = {index: index for index in image_rows}

    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(first, second):
        first_root, second_root = find(first), find(second)
        if first_root != second_root:
            parents[max(first_root, second_root)] = min(first_root, second_root)

    coco_owner = {}
    hash_owner = {}
    for index, row in image_rows.items():
        coco_id = row["coco_image_id"]
        sha256 = row["image_sha256"]
        if coco_id is not None:
            if coco_id in coco_owner:
                union(index, coco_owner[coco_id])
            else:
                coco_owner[coco_id] = index
        if sha256 in hash_owner:
            union(index, hash_owner[sha256])
        else:
            hash_owner[sha256] = index
    grouped = defaultdict(list)
    for index in image_rows:
        grouped[find(index)].append(index)
    for indices in grouped.values():
        coco_ids = sorted({image_rows[index]["coco_image_id"] for index in indices
                           if image_rows[index]["coco_image_id"] is not None})
        hashes = sorted({image_rows[index]["image_sha256"] for index in indices})
        identity_key = f"coco:{coco_ids[0]}" if coco_ids else f"sha256:{hashes[0]}"
        identity_source = "coco_id" if coco_ids else "pixel_sha256"
        for index in indices:
            image_rows[index]["identity_key"] = identity_key
            image_rows[index]["identity_source"] = identity_source
    return image_rows


def image_splits(records, config, identity_by_index):
    sizes = config["split_sizes"]
    unique_sizes = config["unique_identity_split_sizes"]
    if sum(sizes.values()) != len(records):
        raise ValueError("Calibration record split sizes must cover every sampled image exactly once")
    groups = defaultdict(list)
    for record in records:
        groups[identity_by_index[record["index"]]["identity_key"]].append(record["index"])
    if sum(unique_sizes.values()) != len(groups):
        raise ValueError("Unique identity split sizes must cover every source-image identity")
    fixed_coco_ids = set(config["fixed_train_coco_ids"])
    fixed_keys = {key for key, indices in groups.items()
                  if any(identity_by_index[index]["coco_image_id"] in fixed_coco_ids for index in indices)}
    if len(fixed_keys) != len(fixed_coco_ids):
        raise ValueError("A fixed train COCO image identity is absent or mapped to multiple groups")
    if len(fixed_keys) > unique_sizes["train"]:
        raise ValueError("Fixed train identities exceed the train identity target")
    remaining = [key for key in groups if key not in fixed_keys]
    permutation = np.random.default_rng(config["split_seed"]).permutation(len(remaining))
    shuffled = [remaining[position] for position in permutation]
    train_end = unique_sizes["train"] - len(fixed_keys)
    validation_end = train_end + unique_sizes["validation"]
    identity_assignment = {key: "train" for key in fixed_keys}
    identity_assignment.update({key: "train" for key in shuffled[:train_end]})
    identity_assignment.update({key: "validation" for key in shuffled[train_end:validation_end]})
    identity_assignment.update({key: "test" for key in shuffled[validation_end:]})
    result = {name: [] for name in ("train", "validation", "test")}
    for record in records:
        identity = identity_by_index[record["index"]]
        split = identity_assignment[identity["identity_key"]]
        result[split].append(dict(identity))
    record_counts = {name: len(items) for name, items in result.items()}
    identity_counts = {name: len({item["identity_key"] for item in items})
                       for name, items in result.items()}
    if record_counts != sizes:
        raise ValueError(f"Grouped record split sizes differ from target: {record_counts}")
    if identity_counts != unique_sizes:
        raise ValueError(f"Grouped identity split sizes differ from target: {identity_counts}")
    return result


def split_identity_audit(splits):
    identity_sets = {name: {item["identity_key"] for item in items} for name, items in splits.items()}
    coco_sets = {name: {item["coco_image_id"] for item in items if item["coco_image_id"] is not None}
                 for name, items in splits.items()}
    hash_sets = {name: {item["image_sha256"] for item in items} for name, items in splits.items()}
    names = ("train", "validation", "test")
    overlaps = {}
    for first_index, first in enumerate(names):
        for second in names[first_index + 1:]:
            overlaps[f"{first}_{second}"] = {
                "identity_keys": sorted(identity_sets[first] & identity_sets[second]),
                "coco_image_ids": sorted(coco_sets[first] & coco_sets[second]),
                "sha256": sorted(hash_sets[first] & hash_sets[second])}
    duplicate_groups = {}
    grouped = defaultdict(list)
    for items in splits.values():
        for item in items:
            grouped[item["identity_key"]].append(item)
    for key, items in grouped.items():
        if len(items) > 1:
            duplicate_groups[key] = [{"index": item["index"], "file_name": item["file_name"],
                                      "coco_image_id": item["coco_image_id"],
                                      "image_sha256": item["image_sha256"],
                                      "split": next(name for name, rows in splits.items()
                                                    if item in rows)} for item in items]
    return {"record_counts": {name: len(items) for name, items in splits.items()},
            "unique_identity_counts": {name: len(identity_sets[name]) for name in names},
            "unique_coco_id_counts": {name: len(coco_sets[name]) for name in names},
            "unique_pixel_sha256_counts": {name: len(hash_sets[name]) for name in names},
            "cross_split_overlaps": overlaps,
            "all_identity_keys_disjoint": all(not value["identity_keys"] for value in overlaps.values()),
            "all_coco_ids_disjoint": all(not value["coco_image_ids"] for value in overlaps.values()),
            "all_pixel_hashes_disjoint": all(not value["sha256"] for value in overlaps.values()),
            "duplicate_identity_groups": duplicate_groups}


def grouped_bootstrap_arrays(items, predicate_count):
    groups = defaultdict(list)
    for item in items:
        groups[item["identity_key"]].append(item)
    keys = sorted(groups)
    image_recall_sum = []
    image_recall_count = []
    predicate_recall_sum = []
    predicate_recall_count = []
    annotation_count = []
    annotation_hits = []
    for key in keys:
        rows = groups[key]
        recalls = np.asarray([row["image_recall"] for row in rows], dtype=np.float64)
        predicate_recalls = np.asarray([row["image_predicate_recall"] for row in rows], dtype=np.float64)
        image_recall_sum.append(float(np.nansum(recalls)))
        image_recall_count.append(int(np.isfinite(recalls).sum()))
        predicate_recall_sum.append(np.nansum(predicate_recalls, axis=0))
        predicate_recall_count.append(np.isfinite(predicate_recalls).sum(axis=0))
        annotation_count.append(sum(row["annotation_count"] for row in rows))
        annotation_hits.append(sum(row["annotation_hits"] for row in rows))
    return {"identity_keys": keys,
            "image_recall_sum": np.asarray(image_recall_sum, dtype=np.float64),
            "image_recall_count": np.asarray(image_recall_count, dtype=np.float64),
            "predicate_recall_sum": np.asarray(predicate_recall_sum, dtype=np.float64).reshape(-1, predicate_count),
            "predicate_recall_count": np.asarray(predicate_recall_count, dtype=np.float64).reshape(-1, predicate_count),
            "annotation_count": np.asarray(annotation_count, dtype=np.float64),
            "annotation_hits": np.asarray(annotation_hits, dtype=np.float64)}


def bootstrap_group_weights(identity_count, config, seed_offset=0):
    repetitions = config["bootstrap_repetitions"]
    rng = np.random.default_rng(config["bootstrap_seed"] + seed_offset)
    sampled = rng.integers(0, identity_count, size=(repetitions, identity_count), dtype=np.int64)
    weights = np.zeros((repetitions, identity_count), dtype=np.float64)
    np.add.at(weights, (np.arange(repetitions)[:, None], sampled), 1.0)
    return weights


def per_image_bootstrap(per_image_by_method, method_names, config):
    repetitions = config["bootstrap_repetitions"]
    predicate_count = len(next(iter(per_image_by_method.values()))[0]["gt_counts"])
    output = []
    for method in method_names:
        items = per_image_by_method[method]
        grouped = grouped_bootstrap_arrays(items, predicate_count)
        weights = bootstrap_group_weights(len(grouped["identity_keys"]), config)
        base = metric_summary(items, predicate_count)
        image_n = weights @ grouped["image_recall_count"]
        samples_r = np.divide(weights @ grouped["image_recall_sum"], image_n,
                              out=np.full(repetitions, np.nan), where=image_n > 0)
        class_count = weights @ grouped["predicate_recall_count"]
        class_sum = weights @ grouped["predicate_recall_sum"]
        class_recall = np.divide(class_sum, class_count, out=np.full_like(class_sum, np.nan),
                                 where=class_count > 0)
        samples_mr = safe_nanmean(class_recall, axis=1)
        candidate_count = weights @ grouped["annotation_count"]
        candidate_hits = weights @ grouped["annotation_hits"]
        samples_annotation = np.divide(candidate_hits, candidate_count,
                                        out=np.full(repetitions, np.nan), where=candidate_count > 0)
        for metric_name, observed, samples in (
                ("R@50_image_macro", base["R@50_image_macro"], samples_r),
                ("mR@50_class_macro", base["mR@50_class_macro"], samples_mr)):
            output.append({"method": method, "metric": metric_name, "estimate": observed,
                           "bootstrap_95pct_low": float(np.nanquantile(samples, 0.025)),
                           "bootstrap_95pct_high": float(np.nanquantile(samples, 0.975)),
                           "repetitions": repetitions, "unit": "source_image_identity_cluster"})
        output.append({"method": method, "metric": "annotation_match_rate_proxy",
                       "estimate": float(grouped["annotation_hits"].sum() /
                                         grouped["annotation_count"].sum())
                       if grouped["annotation_count"].sum() else None,
                       "bootstrap_95pct_low": float(np.nanquantile(samples_annotation, 0.025)),
                       "bootstrap_95pct_high": float(np.nanquantile(samples_annotation, 0.975)),
                       "repetitions": repetitions, "unit": "source_image_identity_cluster"})
    return output


def paired_bootstrap(per_image_by_method, baseline, method_names, config):
    repetitions = config["bootstrap_repetitions"]
    predicate_count = len(per_image_by_method[baseline][0]["gt_counts"])
    output = []
    base_items = per_image_by_method[baseline]
    base_grouped = grouped_bootstrap_arrays(base_items, predicate_count)
    weights = bootstrap_group_weights(len(base_grouped["identity_keys"]), config, seed_offset=1)
    for method in method_names:
        if method == baseline:
            continue
        method_items = per_image_by_method[method]
        method_grouped = grouped_bootstrap_arrays(method_items, predicate_count)
        if method_grouped["identity_keys"] != base_grouped["identity_keys"]:
            raise ValueError("Paired bootstrap methods do not share the same source-image identities")
        baseline_summary = metric_summary(base_items, predicate_count)
        method_summary = metric_summary(method_items, predicate_count)
        baseline_r = np.divide(weights @ base_grouped["image_recall_sum"],
                                weights @ base_grouped["image_recall_count"],
                                out=np.full(repetitions, np.nan),
                                where=(weights @ base_grouped["image_recall_count"]) > 0)
        method_r = np.divide(weights @ method_grouped["image_recall_sum"],
                             weights @ method_grouped["image_recall_count"],
                             out=np.full(repetitions, np.nan),
                             where=(weights @ method_grouped["image_recall_count"]) > 0)
        baseline_class_count = weights @ base_grouped["predicate_recall_count"]
        method_class_count = weights @ method_grouped["predicate_recall_count"]
        baseline_class = np.divide(weights @ base_grouped["predicate_recall_sum"], baseline_class_count,
                                   out=np.full_like(baseline_class_count, np.nan),
                                   where=baseline_class_count > 0)
        method_class = np.divide(weights @ method_grouped["predicate_recall_sum"], method_class_count,
                                 out=np.full_like(method_class_count, np.nan), where=method_class_count > 0)
        deltas = (("R@50_image_macro", method_r - baseline_r),
                  ("mR@50_class_macro", safe_nanmean(method_class, axis=1) -
                   safe_nanmean(baseline_class, axis=1)))
        for name, samples in deltas:
            estimate = method_summary[name] - baseline_summary[name]
            output.append({"comparison": f"{method} - {baseline}", "metric": name,
                           "estimate_delta": estimate,
                           "bootstrap_delta_95pct_low": float(np.nanquantile(samples, 0.025)),
                           "bootstrap_delta_95pct_high": float(np.nanquantile(samples, 0.975)),
                           "repetitions": repetitions, "unit": "paired_source_image_identity_cluster"})
    return output


def predicate_rank_rows(records, per_record, predicates, valid_endpoint_ids):
    rows = []
    for record in records:
        result = per_record[record["index"]]
        gt_objects = {item["id"]: item for item in record["ground_truth_objects"]}
        matches = result["matches"]
        pair_ranks = result["rank_map"]
        group_ranks = result["group_rank_map"]
        for truth in record["ground_truth_relations"]:
            subject_ids = matches[truth["subject_id"]]
            object_ids = matches[truth["object_id"]]
            valid = any(subject_id != object_id for subject_id in subject_ids for object_id in object_ids)
            possible_pairs = [(subject_id, object_id) for subject_id in subject_ids for object_id in object_ids
                              if subject_id != object_id]
            full_values = [pair_ranks[(s, o)][truth["predicate_id"]] for s, o in possible_pairs
                           if (s, o) in pair_ranks]
            group_values = [group_ranks[(s, o)][truth["predicate_id"]] for s, o in possible_pairs
                            if (s, o) in group_ranks]
            best_global = result["method_global_rank"].get((truth["subject_id"], truth["object_id"],
                                                              truth["predicate_id"]))
            rows.append({"index": record["index"], "sample_position": record["sample_position"],
                         "file_name": record["file_name"], "subject_id": truth["subject_id"],
                         "subject_label": gt_objects[truth["subject_id"]]["label"],
                         "object_id": truth["object_id"], "object_label": gt_objects[truth["object_id"]]["label"],
                         "predicate_id": truth["predicate_id"], "predicate": truth["predicate"],
                         "valid_detected_endpoints": valid, "fixed_530_subset":
                         (record["index"], truth["subject_id"], truth["object_id"], truth["predicate_id"])
                         in valid_endpoint_ids,
                         "matching_directed_pairs": len(possible_pairs),
                         "best_pair_local_rank_all_56": min(full_values) if full_values else None,
                         "best_pair_local_rank_correct_group": min(group_values) if group_values else None,
                         "global_rank_dual_before_budget": best_global})
    return rows


def rank_histograms(rank_rows, predicates):
    buckets = ((1, 1, "1"), (2, 2, "2"), (3, 3, "3"), (4, 5, "4-5"),
               (6, 10, "6-10"), (11, 10 ** 9, ">10"))
    result = []
    for predicate_id, predicate in enumerate(predicates):
        selected = [row for row in rank_rows if row["predicate_id"] == predicate_id and row["fixed_530_subset"]]
        for field, label in (("best_pair_local_rank_all_56", "all_56"),
                             ("best_pair_local_rank_correct_group", "correct_group")):
            values = [row[field] for row in selected if row[field] is not None]
            missing = len(selected) - len(values)
            for lower, upper, bucket in buckets:
                result.append({"predicate_id": predicate_id, "predicate": predicate, "rank_scope": label,
                               "rank_bucket": bucket, "count": sum(lower <= value <= upper for value in values),
                               "GT_in_fixed_subset": len(selected), "no_matching_candidate": missing})
            result.append({"predicate_id": predicate_id, "predicate": predicate, "rank_scope": label,
                           "rank_bucket": "missing", "count": missing,
                           "GT_in_fixed_subset": len(selected), "no_matching_candidate": missing})
    return result


def matched_gt_keys(index, row, gt_by_image, matches_by_image):
    result = set()
    for truth in gt_by_image[index]:
        if truth["predicate_id"] != row["predicate_id"]:
            continue
        subject_ids = matches_by_image[index][truth["subject_id"]]
        object_ids = matches_by_image[index][truth["object_id"]]
        if row["subject_id"] in subject_ids and row["object_id"] in object_ids and row["subject_id"] != row["object_id"]:
            result.add((index, truth["subject_id"], truth["object_id"], truth["predicate_id"]))
    return result


def make_selective_curve(rows, labels, gt_by_image, matches_by_image):
    ordered = sorted(zip(rows, labels.tolist()), key=lambda item: (-item[0]["margin"],
                                                                   -item[0]["fused_logit"],
                                                                   item[0]["index"], item[0]["subject_id"],
                                                                   item[0]["object_id"], item[0]["predicate_id"]))
    output = []
    kept = []
    cursor = 0
    gt_total = sum(len(rows) for rows in gt_by_image.values())
    hit_gt = set()
    while cursor < len(ordered):
        margin = ordered[cursor][0]["margin"]
        stop = cursor + 1
        while stop < len(ordered) and ordered[stop][0]["margin"] == margin:
            stop += 1
        kept.extend(ordered[cursor:stop])
        for row, label in ordered[cursor:stop]:
            if label:
                hit_gt.update(matched_gt_keys(row["index"], row, gt_by_image, matches_by_image))
        output.append({"margin_threshold": margin, "kept_candidates": len(kept),
                       "coverage": len(kept) / len(rows) if rows else 0.0,
                       "annotation_match_rate_proxy": float(np.mean([label for _, label in kept])) if kept else None,
                       "annotation_risk_proxy": 1.0 - float(np.mean([label for _, label in kept])) if kept else None,
                       "recalled_GT_relations": len(hit_gt), "GT_total": gt_total,
                       "pooled_R50": len(hit_gt) / gt_total if gt_total else None})
        cursor = stop
    return output


def plot_calibration(path, bins_by_method):
    fig, axis = plt.subplots(figsize=(7.4, 5.6))
    axis.plot([0, 1], [0, 1], color="#4b5563", linestyle="--", label="Perfect calibration")
    colors = {"raw_sigmoid": "#cc4b37", "official": "#167d75", "local_platt": "#3867a8",
              "train_prevalence": "#8057a1"}
    for name, bins in bins_by_method.items():
        points = [row for row in bins if row["count"]]
        axis.plot([row["mean_confidence"] for row in points],
                  [row["annotation_match_rate"] for row in points], marker="o",
                  color=colors[name], label=name)
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Confidence", ylabel="PSG annotation-match rate",
             title="Reliability on the held-out image split")
    axis.grid(alpha=0.22)
    axis.legend(frameon=False)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_risk_coverage(path, curve):
    fig, axis = plt.subplots(figsize=(7.4, 5.6))
    axis.plot([row["coverage"] for row in curve], [row["annotation_risk_proxy"] for row in curve],
              color="#b44a3a", linewidth=1.8)
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Candidate coverage",
             ylabel="Unmatched annotation rate (risk proxy)",
             title="Margin-based selective output")
    axis.grid(alpha=0.22)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="在固定HOR500 logits上比较人相关关系解码与选择性输出")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    args = parser.parse_args()
    config = read_json(Path(args.config))
    input_path = ROOT / config["input_predictions"]
    logits_root = ROOT / config["input_logits"]
    output_dir = ROOT / config["output_directory"]
    report_dir = ROOT / config["report_directory"]
    predicates = read_json(ROOT / config["predicates_metadata"])["predicates"]
    spatial_ids = [predicates.index(name) for name in config["spatial_predicates"]]
    official = read_json(ROOT / config["official_calibration"])
    records = [json.loads(line) for line in input_path.read_text(encoding="utf-8").splitlines() if line]
    if len(records) != 500 or len({record["index"] for record in records}) != 500:
        raise ValueError("The fixed input must contain 500 unique image records")
    if sum(len(record["ground_truth_relations"]) for record in records) != 968:
        raise ValueError("The fixed HOR500 input must contain exactly 968 human-involving GT relations")
    identity_by_index = image_identity_map(records, ROOT / config["vg_identity_metadata"])
    splits = image_splits(records, config, identity_by_index)
    split_names = {image["index"]: split for split, items in splits.items() for image in items}
    if len(split_names) != 500:
        raise ValueError("Image split sets overlap or omit an image")
    identity_audit = split_identity_audit(splits)
    if not identity_audit["all_identity_keys_disjoint"]:
        raise ValueError("Source image identities overlap across calibration splits")
    if not identity_audit["all_coco_ids_disjoint"]:
        raise ValueError("COCO image IDs overlap across calibration splits")
    if not identity_audit["all_pixel_hashes_disjoint"]:
        raise ValueError("Pixel SHA256 identities overlap across calibration splits")
    fixed_train_ids = set(config["fixed_train_coco_ids"])
    if not fixed_train_ids.issubset({item["coco_image_id"] for item in splits["train"]}):
        raise ValueError("A fixed train COCO image identity was assigned outside train")
    write_json(output_dir / "calibration_image_splits.json", {
        "definition": "Visual Genome image_data.json maps image_id to coco_id; records sharing a COCO ID or pixel SHA256 form one identity group. The repeated COCO ID 404484 group is fixed to train. Remaining unique groups are assigned by NumPy default_rng(split_seed) to the configured unique-identity targets; candidate rows inherit the group split.",
        "identity_metadata": config["vg_identity_metadata"],
        "fallback_identity": "pixel SHA256 when VG metadata has no COCO ID; shared pixel hashes also merge groups for the disjointness check",
        "records_with_vg_coco_id": sum(item["coco_image_id"] is not None for item in identity_by_index.values()),
        "records_using_sha256_fallback": sum(item["coco_image_id"] is None for item in identity_by_index.values()),
        "fixed_train_coco_ids": sorted(fixed_train_ids),
        "seed": config["split_seed"], "split_record_targets": config["split_sizes"],
        "split_unique_identity_targets": config["unique_identity_split_sizes"],
        "identity_audit": identity_audit,
        "splits": splits})

    methods = ("top1", "top2", "top3", "top5", "dual", "single")
    all_candidates = {name: [] for name in methods}
    per_image_by_method = {name: [] for name in methods}
    oracle_candidates_by_method = {name: [] for name in methods}
    oracle_per_image_by_method = {name: [] for name in methods}
    oracle_selected_export = []
    per_record = {}
    frozen_valid_gt = []
    gt_images_by_index = {}
    matches_by_index = {}
    human_predicate_counts = np.zeros(len(predicates), dtype=np.int64)
    oracle_rank_records = []
    candidate_export = []
    for record in records:
        index = record["index"]
        candidate_path = logits_root / "detected" / f"{index:04d}.npz"
        detected_candidates = {name: [] for name in methods}
        detected_rank_map = {}
        detected_pair_map = {}
        if candidate_path.exists():
            with np.load(candidate_path, allow_pickle=False) as arrays:
                decoded, detected_rank_map, detected_pair_map = pair_candidates(
                    record, arrays, predicates, spatial_ids, "detected")
                detected_candidates = {name: decoded[name][:config["per_image_budget"]] for name in methods}
        gt_candidate_path = logits_root / "gt_boxes" / f"{index:04d}.npz"
        gt_box_candidates = {name: [] for name in methods}
        if gt_candidate_path.exists():
            with np.load(gt_candidate_path, allow_pickle=False) as arrays:
                gt_decoded, _, _ = pair_candidates(record, arrays, predicates, spatial_ids, "gt_boxes")
                gt_box_candidates = {name: gt_decoded[name][:config["per_image_budget"]] for name in methods}
        matches = endpoint_matches(record["detected"]["objects"], record["ground_truth_objects"],
                                   config["iou_threshold"])
        matches_by_index[index] = matches
        gt = record["ground_truth_relations"]
        gt_images_by_index[index] = gt
        gt_counts = np.bincount([row["predicate_id"] for row in gt], minlength=len(predicates))
        human_predicate_counts += gt_counts
        valid_gt = []
        invalid_endpoint = 0
        collapsed = 0
        ground_truth_objects = {item["id"]: item for item in record["ground_truth_objects"]}
        for truth in gt:
            subject_ids = matches[truth["subject_id"]]
            object_ids = matches[truth["object_id"]]
            pairs = [(s, o) for s in subject_ids for o in object_ids if s != o]
            in_detector_vocabulary = all(
                ground_truth_objects[endpoint]["label"] in record["detector_categories"]
                for endpoint in (truth["subject_id"], truth["object_id"]))
            if pairs and in_detector_vocabulary:
                valid_gt.append(truth)
                frozen_valid_gt.append((index, truth["subject_id"], truth["object_id"], truth["predicate_id"]))
            elif not subject_ids or not object_ids:
                invalid_endpoint += 1
            else:
                collapsed += 1
        valid_gt_counts = np.bincount([row["predicate_id"] for row in valid_gt], minlength=len(predicates))
        method_data = {}
        for name in methods:
            rows = detected_candidates[name]
            labels = annotation_labels(rows, gt, matches)
            hits, hit_triples = gt_hit_counts(rows, gt, matches, len(predicates))
            valid_hits, valid_hit_triples = gt_hit_counts(rows, valid_gt, matches, len(predicates))
            method_data[name] = {"rows": rows, "labels": labels, "hits": hits,
                                 "hit_triples": hit_triples, "valid_hits": valid_hits,
                                 "valid_hit_triples": valid_hit_triples}
            all_candidates[name].extend(rows)
            image_recall = float(hits.sum() / gt_counts.sum()) if gt_counts.sum() else math.nan
            image_predicate_recall = np.divide(hits, gt_counts, out=np.full(len(predicates), np.nan),
                                               where=gt_counts > 0)
            labels_count = len(labels)
            per_image_by_method[name].append({"index": index,
                                              "identity_key": identity_by_index[index]["identity_key"],
                                              "gt_counts": gt_counts,
                                              "valid_gt_counts": valid_gt_counts, "hits": hits,
                                              "valid_hits": valid_hits, "image_recall": image_recall,
                                              "image_predicate_recall": image_predicate_recall,
                                              "annotation_count": labels_count,
                                              "annotation_hits": int(labels.sum())})
            for row, label in zip(rows, labels):
                candidate_export.append({**row, "evaluation_mode": "detected", "method": name,
                                         "image_split": split_names[index],
                                         "identity_key": identity_by_index[index]["identity_key"],
                                         "coco_image_id": identity_by_index[index]["coco_image_id"],
                                         "image_sha256": identity_by_index[index]["image_sha256"],
                                         "annotation_match_proxy": int(label)})
            oracle_rows = gt_box_candidates[name]
            oracle_hits, _ = exact_gt_hit_counts(oracle_rows, valid_gt, len(predicates))
            oracle_counts = valid_gt_counts.copy()
            oracle_recall = float(oracle_hits.sum() / oracle_counts.sum()) if oracle_counts.sum() else math.nan
            oracle_image_class_recall = np.divide(oracle_hits, oracle_counts,
                                                  out=np.full(len(predicates), np.nan),
                                                  where=oracle_counts > 0)
            oracle_per_image_by_method[name].append({"index": index,
                                                     "identity_key": identity_by_index[index]["identity_key"],
                                                     "gt_counts": oracle_counts,
                                                     "valid_gt_counts": oracle_counts, "hits": oracle_hits,
                                                     "valid_hits": oracle_hits,
                                                     "image_recall": oracle_recall,
                                                     "image_predicate_recall": oracle_image_class_recall,
                                                     "annotation_count": 0, "annotation_hits": 0})
            oracle_candidates_by_method[name].extend(oracle_rows)
            for row in oracle_rows:
                oracle_selected_export.append({**row, "method": name})
        if len(detected_candidates["dual"]) != len(record["detected"]["relations"]):
            raise ValueError(f"Dual output count differs from original for image {index}")
        expected = [(row["subject_id"], row["object_id"], row["predicate_id"])
                    for row in record["detected"]["relations"]]
        actual = [(row["subject_id"], row["object_id"], row["predicate_id"])
                  for row in detected_candidates["dual"]]
        if expected != actual:
            raise ValueError(f"Reconstructed dual output differs from original ordering for image {index}")
        expected_single = [(row["subject_id"], row["object_id"], row["predicate_id"])
                           for row in record["detected"]["single_predicate_top50"]]
        actual_single = [(row["subject_id"], row["object_id"], row["predicate_id"])
                         for row in detected_candidates["single"]]
        if expected_single != actual_single:
            raise ValueError(f"Reconstructed single output differs from original ordering for image {index}")
        global_ranks = {}
        full_dual = decoded["dual"] if candidate_path.exists() else []
        for rank, row in enumerate(full_dual, 1):
            global_ranks[(row["subject_id"], row["object_id"], row["predicate_id"])] = rank
        group_rank_map = {}
        if candidate_path.exists():
            for pair, rows in detected_pair_map.items():
                scores_by_predicate = {row["predicate_id"]: row["fused_logit"] for row in rows}
                spatial_order = sorted(spatial_ids, key=lambda pid: (-scores_by_predicate[pid], pid))
                semantic_ids = sorted(set(range(len(predicates))) - set(spatial_ids))
                semantic_order = sorted(semantic_ids, key=lambda pid: (-scores_by_predicate[pid], pid))
                group_rank_map[pair] = {**{pid: rank + 1 for rank, pid in enumerate(spatial_order)},
                                        **{pid: rank + 1 for rank, pid in enumerate(semantic_order)}}
        rank_info = {"matches": matches, "rank_map": detected_rank_map,
                     "group_rank_map": group_rank_map, "method_global_rank": global_ranks}
        per_record[index] = rank_info
        for truth in gt:
            exact_pair = (truth["subject_id"], truth["object_id"])
            oracle_path = logits_root / "gt_boxes" / f"{index:04d}.npz"
            if not oracle_path.exists():
                oracle_rank_records.append({"index": index, "subject_id": truth["subject_id"],
                                            "object_id": truth["object_id"], "predicate_id": truth["predicate_id"],
                                            "predicate": truth["predicate"], "rank_all_56": None,
                                            "rank_correct_group": None, "gt_logit_file_present": False})
                continue
            with np.load(oracle_path, allow_pickle=False) as arrays:
                row_indices = np.where((arrays["subject_indices"] == exact_pair[0]) &
                                       (arrays["object_indices"] == exact_pair[1]))[0]
                if len(row_indices) != 1:
                    raise ValueError(f"GT-box logits have no unique candidate pair for image {index}: {exact_pair}")
                slot = int(row_indices[0])
                scores = arrays["predicate_logits"][slot].astype(np.float64) + float(arrays["pair_logits"][slot])
                ordered = sorted(range(len(predicates)), key=lambda pid: (-scores[pid], pid))
                spatial_order = sorted(spatial_ids, key=lambda pid: (-scores[pid], pid))
                semantic_order = sorted(set(range(len(predicates))) - set(spatial_ids),
                                        key=lambda pid: (-scores[pid], pid))
                pred_id = truth["predicate_id"]
                group_order = spatial_order if pred_id in spatial_ids else semantic_order
                oracle_rank_records.append({"index": index, "subject_id": truth["subject_id"],
                                            "object_id": truth["object_id"], "predicate_id": pred_id,
                                            "predicate": truth["predicate"],
                                            "rank_all_56": ordered.index(pred_id) + 1,
                                            "rank_correct_group": group_order.index(pred_id) + 1,
                                            "gt_logit_file_present": True})
    frozen_valid_gt_set = set(frozen_valid_gt)
    if len(frozen_valid_gt_set) != 530:
        raise ValueError(f"Expected 530 frozen valid-endpoint GT relations; found {len(frozen_valid_gt_set)}")
    if sum(len(record["ground_truth_relations"]) for record in records) - len(frozen_valid_gt_set) != 438:
        raise ValueError("Endpoint failure decomposition does not total the expected 438 GT relations")
    metric_rows = []
    metric_json = {}
    for method in methods:
        all_summary = metric_summary(per_image_by_method[method], len(predicates))
        valid_summary = metric_summary(per_image_by_method[method], len(predicates), valid_only=True)
        metric_json[method] = {"all_968_GT": {key: all_summary[key] for key in
                                               ("images_with_GT", "GT", "hits", "R@50_image_macro",
                                                "mR@50_class_macro", "pooled_R@50")},
                               "fixed_530_valid_endpoint_GT": {key: valid_summary[key] for key in
                                                               ("images_with_GT", "GT", "hits",
                                                                "R@50_image_macro", "mR@50_class_macro",
                                                                "pooled_R@50")},
                               "predictions_under_budget": len(all_candidates[method])}
        # 逐谓词保留GT数、命中数和两种召回分母，便于检查宏平均差异。
        for predicate_id, predicate in enumerate(predicates):
            metric_rows.append({"method": method, "predicate_id": predicate_id, "predicate": predicate,
                                "GT_all_968": int(all_summary["class_gt"][predicate_id]),
                                "hits_all_968": int(all_summary["class_hits"][predicate_id]),
                                "pooled_recall_all_968": float(all_summary["class_hits"][predicate_id] /
                                                                all_summary["class_gt"][predicate_id])
                                if all_summary["class_gt"][predicate_id] else None,
                                "GT_fixed_530": int(valid_summary["class_gt"][predicate_id]),
                                "hits_fixed_530": int(valid_summary["class_hits"][predicate_id]),
                                "pooled_recall_fixed_530": float(valid_summary["class_hits"][predicate_id] /
                                                                  valid_summary["class_gt"][predicate_id])
                                if valid_summary["class_gt"][predicate_id] else None})
    write_json(output_dir / "decoding_metrics.json", metric_json)
    write_csv(output_dir / "per_predicate_recall.csv", metric_rows, list(metric_rows[0]))
    write_csv(output_dir / "selected_candidates.csv", candidate_export, list(candidate_export[0]))
    write_csv(output_dir / "gt_box_selected_candidates.csv", oracle_selected_export,
              list(oracle_selected_export[0]))

    oracle_metric_json = {}
    oracle_predicate_rows = []
    paired_fixed_data = {}
    for method in methods:
        oracle_summary = metric_summary(oracle_per_image_by_method[method], len(predicates))
        oracle_metric_json[method] = {key: oracle_summary[key] for key in
                                      ("images_with_GT", "GT", "hits", "R@50_image_macro",
                                       "mR@50_class_macro", "pooled_R@50")}
        oracle_metric_json[method]["predictions_under_budget"] = len(oracle_candidates_by_method[method])
        detected_fixed = [{**item, "gt_counts": item["valid_gt_counts"],
                           "hits": item["valid_hits"], "image_recall":
                           float(item["valid_hits"].sum() / item["valid_gt_counts"].sum())
                           if item["valid_gt_counts"].sum() else math.nan,
                           "image_predicate_recall": np.divide(
                               item["valid_hits"], item["valid_gt_counts"],
                               out=np.full(len(predicates), np.nan), where=item["valid_gt_counts"] > 0)}
                          for item in per_image_by_method[method]]
        paired_fixed_data[f"detected_{method}"] = detected_fixed
        paired_fixed_data[f"gt_boxes_{method}"] = oracle_per_image_by_method[method]
        for predicate_id, predicate in enumerate(predicates):
            oracle_predicate_rows.append({"method": method, "predicate_id": predicate_id,
                                          "predicate": predicate,
                                          "GT_fixed_530": int(oracle_summary["class_gt"][predicate_id]),
                                          "GT_hits_fixed_530": int(oracle_summary["class_hits"][predicate_id]),
                                          "pooled_recall_fixed_530":
                                          float(oracle_summary["class_hits"][predicate_id] /
                                                oracle_summary["class_gt"][predicate_id])
                                          if oracle_summary["class_gt"][predicate_id] else None})
    oracle_pair_intervals = []
    for method in methods:
        oracle_pair_intervals.extend(paired_bootstrap(
            paired_fixed_data, f"detected_{method}", [f"gt_boxes_{method}"], config))
    write_json(output_dir / "fixed530_endpoint_oracle_metrics.json", {
        "subset_definition": "same 530 GT relations whose subject and object labels both occur in the historical detector vocabulary and whose endpoints both match same-class detections at IoU >= 0.5 with at least one distinct ordered detection pair",
        "evaluation_role": "GT-box endpoint oracle diagnostic; not end-to-end evaluation",
        "fixed_subset_GT": 530, "images_with_fixed_subset_GT": 214,
        "methods": oracle_metric_json})
    write_csv(output_dir / "fixed530_gtbox_per_predicate.csv", oracle_predicate_rows,
              list(oracle_predicate_rows[0]))
    write_csv(output_dir / "fixed530_endpoint_oracle_paired_deltas.csv", oracle_pair_intervals,
              list(oracle_pair_intervals[0]))

    rank_rows_all = predicate_rank_rows(records, per_record, predicates, frozen_valid_gt_set)
    rank_hist = rank_histograms(rank_rows_all, predicates)
    write_csv(output_dir / "gt_predicate_ranks.csv", rank_rows_all, list(rank_rows_all[0]))
    write_csv(output_dir / "per_predicate_rank_histograms.csv", rank_hist, list(rank_hist[0]))
    write_csv(output_dir / "gt_box_oracle_pair_ranks.csv", oracle_rank_records, list(oracle_rank_records[0]))
    write_json(output_dir / "fixed_valid_endpoint_gt.json", {
        "total_human_involving_GT": 968, "valid_detected_endpoint_GT": 530,
        "endpoint_missing_or_wrong_class_GT": 437, "collapsed_to_same_detection_GT": 1,
        "detector_vocabulary_restricted": True,
        "definition": "A GT relation is valid when both endpoint labels occur in the historical detector vocabulary, both GT endpoints have at least one same-class detected box with IoU >= 0.5, and at least one distinct ordered detected subject/object pair exists.",
        "relations": [{"index": index, "subject_id": subject, "object_id": object_id,
                       "predicate_id": predicate_id} for index, subject, object_id, predicate_id
                      in sorted(frozen_valid_gt_set)]})

    dual_rows = all_candidates["dual"]
    dual_labels = np.asarray([row["annotation_match_proxy"] for row in candidate_export
                              if row["method"] == "dual"], dtype=np.int64)
    dual_export_rows = [row for row in candidate_export if row["method"] == "dual"]
    if len(dual_rows) != len(dual_labels):
        raise ValueError("Calibration candidate and label row counts differ")
    duplicate_identity_groups = identity_audit["duplicate_identity_groups"]
    candidate_signatures = defaultdict(list)
    for row in dual_export_rows:
        candidate_signatures[(row["identity_key"], row["index"])].append(
            (row["subject_id"], row["object_id"], row["predicate_id"], row["fused_logit"]))
    for identity_key, group in duplicate_identity_groups.items():
        signatures = [candidate_signatures[(identity_key, item["index"])] for item in group]
        if any(signature != signatures[0] for signature in signatures[1:]):
            raise ValueError(f"Candidate rows differ within repeated source identity {identity_key}")
    positions_by_split = {name: {item["index"] for item in items} for name, items in splits.items()}
    records_by_identity = defaultdict(list)
    for items in splits.values():
        for item in items:
            records_by_identity[item["identity_key"]].append(item)
    canonical_index_by_identity = {
        identity: min(items, key=lambda item: item["sample_position"])["index"]
        for identity, items in records_by_identity.items()}
    train_identity_keys = {item["identity_key"] for item in splits["train"]}
    train_canonical_indices = {canonical_index_by_identity[key] for key in train_identity_keys}
    train_mask = np.asarray([row["image_split"] == "train" and
                             row["index"] in train_canonical_indices for row in dual_export_rows])
    validation_mask = np.asarray([row["index"] in positions_by_split["validation"] for row in dual_export_rows])
    test_mask = np.asarray([row["index"] in positions_by_split["test"] for row in dual_export_rows])
    if np.any(train_mask & validation_mask) or np.any(train_mask & test_mask) or np.any(validation_mask & test_mask):
        raise ValueError("Candidate image splits overlap")
    identity_annotation_labels = {}
    for row in dual_export_rows:
        candidate_key = (row["identity_key"], row["subject_id"], row["object_id"], row["predicate_id"])
        identity_annotation_labels[candidate_key] = max(
            identity_annotation_labels.get(candidate_key, 0), row["annotation_match_proxy"])
    calibration_labels = np.asarray([
        identity_annotation_labels[(row["identity_key"], row["subject_id"],
                                    row["object_id"], row["predicate_id"])]
        if row["image_split"] == "train" else row["annotation_match_proxy"]
        for row in dual_export_rows], dtype=np.int64)
    logits = np.asarray([row["fused_logit"] for row in dual_export_rows], dtype=np.float64)
    fit = fit_platt(logits[train_mask], calibration_labels[train_mask])
    fit["train_unique_source_identities"] = len(train_identity_keys)
    fit["train_record_images"] = len(splits["train"])
    fit["duplicate_identity_candidate_rows_removed"] = int(
        sum(row["image_split"] == "train" for row in dual_export_rows) - train_mask.sum())
    fit["duplicate_identity_match_labels_merged"] = True
    a_official, b_official = float(official["a"]), float(official["b"])
    if a_official <= 0 or fit["a"] <= 0:
        raise ValueError("Calibration slopes must preserve strict ranking order")
    calibration_rows = []
    bins_by_method = {}
    calibration_metrics = {}
    for split_name, mask in (("train", train_mask), ("validation", validation_mask), ("test", test_mask)):
        split_labels = calibration_labels[mask]
        split_logits = logits[mask]
        source_identity_count = len({item["identity_key"] for item in splits[split_name]})
        record_candidate_rows = sum(row["image_split"] == split_name for row in dual_export_rows)
        calibration_metrics[split_name] = {"record_images": len(splits[split_name]),
                                           "unique_source_images": source_identity_count,
                                           "images": source_identity_count,
                                           "record_candidate_rows": record_candidate_rows,
                                           "candidate_rows": int(mask.sum()),
                                           "positive_annotation_match_proxy_rows": int(split_labels.sum()),
                                           "proxy_prevalence": float(split_labels.mean()) if len(split_labels) else None}
        if split_name != "test":
            continue
        predicted = {"raw_sigmoid": sigmoid(split_logits),
                     "official": sigmoid(a_official * split_logits + b_official),
                     "local_platt": sigmoid(fit["a"] * split_logits + fit["b"]),
                     "train_prevalence": np.full_like(split_logits, fit["train_proxy_prevalence"])}
        for name, scores in predicted.items():
            ece, bins = calibration_bins(scores, split_labels, config["calibration_bins"])
            calibration_metrics[split_name][name] = {"ECE_annotation_match_proxy": ece,
                                                     "Brier_annotation_match_proxy": float(np.mean((scores - split_labels) ** 2)),
                                                     "calibration_slope": fit["a"] if name == "local_platt" else
                                                     (a_official if name == "official" else
                                                      (0.0 if name == "train_prevalence" else 1.0)),
                                                     "calibration_intercept": fit["b"] if name == "local_platt" else
                                                     (b_official if name == "official" else
                                                      (math.log(fit["train_proxy_prevalence"] /
                                                                (1 - fit["train_proxy_prevalence"]))
                                                       if name == "train_prevalence" else 0.0))}
            bins_by_method[name] = bins
            for row in bins:
                calibration_rows.append({"method": name, "split": split_name, **row})
    official_scores = sigmoid(a_official * logits[test_mask] + b_official)
    local_scores = sigmoid(fit["a"] * logits[test_mask] + fit["b"])
    order_official = np.lexsort((np.asarray([row["predicate_id"] for row in dual_export_rows])[test_mask],
                                 np.asarray([row["object_id"] for row in dual_export_rows])[test_mask],
                                 np.asarray([row["subject_id"] for row in dual_export_rows])[test_mask],
                                 np.asarray([row["index"] for row in dual_export_rows])[test_mask],
                                 -official_scores))
    order_local = np.lexsort((np.asarray([row["predicate_id"] for row in dual_export_rows])[test_mask],
                              np.asarray([row["object_id"] for row in dual_export_rows])[test_mask],
                              np.asarray([row["subject_id"] for row in dual_export_rows])[test_mask],
                              np.asarray([row["index"] for row in dual_export_rows])[test_mask],
                              -local_scores))
    if not np.array_equal(order_official, order_local):
        raise ValueError("Positive affine calibration changed candidate ranking")
    calibration_metrics["test"]["official_vs_local_ranking_identical"] = True
    calibration_metrics["test"]["official_calibration_provenance"] = official["fit_on"]
    calibration_metrics["test"]["target_interpretation"] = "PSG annotation-match proxy; unmatched predictions are unknown with respect to visual truth."
    write_json(output_dir / "calibration_metrics.json", {"fit": fit, "official": official,
                                                          "split_metrics": calibration_metrics})
    write_csv(output_dir / "calibration_bins.csv", calibration_rows, list(calibration_rows[0]))
    plot_calibration(report_dir / "calibration_reliability.png", bins_by_method)

    dual_test_rows = [row for row in dual_export_rows if split_names[row["index"]] == "test"]
    dual_test_labels = np.asarray([row["annotation_match_proxy"] for row in dual_test_rows], dtype=np.int64)
    curve_gt = {index: rows for index, rows in gt_images_by_index.items()
                if index in positions_by_split["test"]}
    curve_matches = {index: matches for index, matches in matches_by_index.items()
                     if index in positions_by_split["test"]}
    curve = make_selective_curve(dual_test_rows, dual_test_labels, curve_gt, curve_matches)
    write_csv(output_dir / "margin_risk_coverage_curve.csv", curve, list(curve[0]))
    plot_risk_coverage(report_dir / "margin_risk_coverage.png", curve)
    validation_rows = [row for row in dual_export_rows if split_names[row["index"]] == "validation"]
    validation_margins = np.asarray([row["margin"] for row in validation_rows], dtype=np.float64)
    validation_labels = np.asarray([row["annotation_match_proxy"] for row in validation_rows], dtype=np.int64)
    test_margins = np.asarray([row["margin"] for row in dual_test_rows], dtype=np.float64)
    test_labels = np.asarray([row["annotation_match_proxy"] for row in dual_test_rows], dtype=np.int64)
    test_gt = [record for record in records if record["index"] in positions_by_split["test"]]
    test_indices = [record["index"] for record in test_gt]
    test_position = {index: position for position, index in enumerate(test_indices)}
    test_candidate_counts = np.bincount([test_position[row["index"]] for row in dual_test_rows],
                                        minlength=len(test_indices))
    test_gt_counts = np.asarray([len(gt_images_by_index[index]) for index in test_indices], dtype=np.int64)
    test_valid_gt_counts = np.asarray([
        sum((index, truth["subject_id"], truth["object_id"], truth["predicate_id"])
            in frozen_valid_gt_set for truth in gt_images_by_index[index])
        for index in test_indices], dtype=np.int64)
    bootstrap_rng = np.random.default_rng(config["bootstrap_seed"] + 2)
    selective_bootstrap_indices = bootstrap_rng.integers(
        0, len(test_indices), size=(config["bootstrap_repetitions"], len(test_indices)), dtype=np.int64)
    selective_rows = []
    for target_coverage in config["selective_coverages"]:
        possible = np.unique(np.concatenate((validation_margins, np.asarray([math.inf]))))
        choices = []
        for threshold in possible:
            coverage = float(np.mean(validation_margins >= threshold))
            choices.append((abs(coverage - target_coverage), coverage, float(threshold)))
        _, val_coverage, threshold = min(choices, key=lambda item: (item[0], item[1]))
        keep = test_margins >= threshold
        kept = [row for row, is_kept in zip(dual_test_rows, keep) if is_kept]
        hits = set()
        for row in kept:
            if row["annotation_match_proxy"]:
                hits.update(matched_gt_keys(row["index"], row, curve_gt, curve_matches))
        kept_candidate_counts = np.bincount([test_position[row["index"]] for row in kept],
                                            minlength=len(test_indices))
        annotation_hit_counts = np.bincount(
            [test_position[row["index"]] for row in kept if row["annotation_match_proxy"]],
            minlength=len(test_indices))
        recalled_gt_counts = np.bincount([test_position[index] for index, _, _, _ in hits],
                                         minlength=len(test_indices))
        recalled_valid_gt_counts = np.bincount(
            [test_position[index] for index, subject, obj, predicate in hits
             if (index, subject, obj, predicate) in frozen_valid_gt_set],
            minlength=len(test_indices))
        sampled_indices = selective_bootstrap_indices
        bootstrap_match_rate = np.divide(
            annotation_hit_counts[sampled_indices].sum(axis=1),
            kept_candidate_counts[sampled_indices].sum(axis=1),
            out=np.full(config["bootstrap_repetitions"], np.nan),
            where=kept_candidate_counts[sampled_indices].sum(axis=1) > 0)
        bootstrap_all_recall = np.divide(
            recalled_gt_counts[sampled_indices].sum(axis=1), test_gt_counts[sampled_indices].sum(axis=1),
            out=np.full(config["bootstrap_repetitions"], np.nan),
            where=test_gt_counts[sampled_indices].sum(axis=1) > 0)
        bootstrap_valid_recall = np.divide(
            recalled_valid_gt_counts[sampled_indices].sum(axis=1),
            test_valid_gt_counts[sampled_indices].sum(axis=1),
            out=np.full(config["bootstrap_repetitions"], np.nan),
            where=test_valid_gt_counts[sampled_indices].sum(axis=1) > 0)
        total_gt = sum(len(record["ground_truth_relations"]) for record in test_gt)
        valid_total = sum(1 for record in test_gt for truth in record["ground_truth_relations"]
                          if (record["index"], truth["subject_id"], truth["object_id"],
                              truth["predicate_id"]) in frozen_valid_gt_set)
        kept_valid_hits = sum(1 for record in test_gt for truth in record["ground_truth_relations"]
                              if (record["index"], truth["subject_id"], truth["object_id"],
                                  truth["predicate_id"]) in frozen_valid_gt_set and
                              (record["index"], truth["subject_id"], truth["object_id"],
                               truth["predicate_id"]) in hits)
        selective_rows.append({"target_coverage_from_validation": target_coverage,
                               "validation_achieved_coverage": val_coverage,
                               "margin_threshold": threshold,
                               "test_candidates": len(dual_test_rows), "test_kept_candidates": int(keep.sum()),
                               "test_coverage": float(keep.mean()) if len(keep) else 0.0,
                               "test_annotation_match_candidates_total": int(test_labels.sum()),
                               "test_annotation_match_candidates_retained": int(test_labels[keep].sum()),
                               "test_annotation_match_candidates_dropped":
                               int(test_labels.sum() - test_labels[keep].sum()),
                               "annotation_match_rate_proxy": float(test_labels[keep].mean()) if keep.any() else None,
                               "annotation_match_rate_proxy_bootstrap_95pct_low":
                               float(np.nanquantile(bootstrap_match_rate, 0.025)),
                               "annotation_match_rate_proxy_bootstrap_95pct_high":
                               float(np.nanquantile(bootstrap_match_rate, 0.975)),
                               "annotation_risk_proxy": 1.0 - float(test_labels[keep].mean()) if keep.any() else None,
                               "all_968_test_GT": total_gt,
                               "test_GT_recalled": len(hits),
                               "test_GT_pooled_recall": len(hits) / total_gt if total_gt else None,
                               "test_GT_pooled_recall_bootstrap_95pct_low":
                               float(np.nanquantile(bootstrap_all_recall, 0.025)),
                               "test_GT_pooled_recall_bootstrap_95pct_high":
                               float(np.nanquantile(bootstrap_all_recall, 0.975)),
                               "test_valid_endpoint_GT": valid_total,
                               "test_valid_endpoint_GT_recalled": kept_valid_hits,
                               "test_valid_endpoint_GT_pooled_recall":
                               kept_valid_hits / valid_total if valid_total else None,
                               "test_valid_endpoint_GT_pooled_recall_bootstrap_95pct_low":
                               float(np.nanquantile(bootstrap_valid_recall, 0.025)),
                               "test_valid_endpoint_GT_pooled_recall_bootstrap_95pct_high":
                               float(np.nanquantile(bootstrap_valid_recall, 0.975))})
    write_csv(output_dir / "margin_selective_thresholds.csv", selective_rows, list(selective_rows[0]))

    bootstrap_rows = per_image_bootstrap(per_image_by_method, methods, config)
    bootstrap_rows.extend(paired_bootstrap(per_image_by_method, "dual", methods, config))
    write_csv(output_dir / "bootstrap_intervals.csv", bootstrap_rows, list(bootstrap_rows[0]))
    diagnostics = {
        "images": 500, "human_involving_GT": 968, "valid_detected_endpoint_GT": 530,
        "endpoint_missing_or_wrong_class_GT": 437, "collapsed_same_detection_GT": 1,
        "methods": methods, "per_image_budget": config["per_image_budget"],
        "output_counts": {name: len(all_candidates[name]) for name in methods},
        "gt_box_output_counts": {name: len(oracle_candidates_by_method[name]) for name in methods},
        "calibration_split_sizes": {name: len(items) for name, items in splits.items()},
        "calibration_unique_identity_sizes": identity_audit["unique_identity_counts"],
        "calibration_identity_audit": identity_audit,
        "split_overlap": not identity_audit["all_identity_keys_disjoint"],
        "all_candidates_are_original_pair_logits": True,
        "dual_decoding_reconstructed_exactly": True,
        "single_decoding_reconstructed_exactly": True,
        "fixed530_subset_requires_detector_vocabulary": True,
        "annotation_label_warning": "An unmatched PSG relation candidate is not proven visually false; all match rates, ECE and risks are annotation-match proxies.",
    }
    write_json(output_dir / "run_diagnostics.json", diagnostics)
    report_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = report_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_files = (
        "bootstrap_intervals.csv", "calibration_bins.csv", "calibration_image_splits.json",
        "calibration_metrics.json", "decoding_metrics.json", "fixed530_endpoint_oracle_metrics.json",
        "fixed530_endpoint_oracle_paired_deltas.csv", "fixed530_gtbox_per_predicate.csv",
        "fixed_valid_endpoint_gt.json", "gt_box_oracle_pair_ranks.csv",
        "gt_box_selected_candidates.csv", "gt_predicate_ranks.csv",
        "margin_risk_coverage_curve.csv", "margin_selective_thresholds.csv",
        "per_predicate_rank_histograms.csv", "per_predicate_recall.csv",
        "run_diagnostics.json", "selected_candidates.csv")
    for filename in evidence_files:
        shutil.copy2(output_dir / filename, evidence_dir / filename)
    report = build_report(metric_json, oracle_metric_json, oracle_pair_intervals,
                          calibration_metrics, fit, selective_rows, bootstrap_rows,
                          rank_hist, diagnostics, config)
    (report_dir / "解码校准与选择性输出实验.md").write_text(report, encoding="utf-8")
    print(json.dumps({"diagnostics": diagnostics, "decoding_metrics": metric_json,
                      "calibration": calibration_metrics, "selective": selective_rows},
                     ensure_ascii=False, indent=2))


def build_report(metrics, oracle_metrics, oracle_intervals, calibration, fit, selective,
                 bootstrap, rank_hist, diagnostics, config):
    method_titles = {"top1": "每对物体 Top1", "top2": "每对物体 Top2", "top3": "每对物体 Top3",
                     "top5": "每对物体 Top5", "dual": "空间与语义各取一项",
                     "single": "每对物体单赢家"}
    train_calibration = calibration["train"]
    validation_calibration = calibration["validation"]
    test_calibration = calibration["test"]
    lines = ["# 解码、校准与选择性输出实验", "",
             "## 实验问题", "",
             "在同一500张随机图像、同一检测边界框、同一完整56类谓词 logits 和每张图像最多50条输出的条件下，比较涉及人物的每个有向物体对保留Top1、Top2、Top3、Top5谓词与现用空间/语义各选一项的规则。随后检验官方校准参数在本数据上的标注匹配代理表现，并用按源图像隔离的训练、验证和测试拆分拟合单调 Platt 校准。间隔拒绝实验根据验证图像确定阈值，在测试图像报告覆盖与标注匹配风险代理。", "",
             "## 数据和评价范围", "",
             "输入沿用 `HOR/output/random500` 的500张固定随机样本与保存的完整关系 logits，不重新运行视觉模型。样本含968条涉及人的唯一PSG关系。有效检测端点子集要求两个GT端点类别都属于旧检测器词表、各自至少匹配一个同类别检测框，且至少存在一组不同检测编号的有向主体—宾语；该集合固定为530条，余下438条由437条端点缺失或类别不符、1条两个端点只映射到同一检测框组成。", "",
             "每个解码方法先按物体对内规则选出候选，再按融合 logit 降序及主体编号、宾语编号、谓词编号打破并列，每张图像最多保留50条。R@50为含GT关系的各张图像召回率的宏平均；mR@50先计算每个谓词在包含该类GT的图像上的召回，再对出现的谓词类别等权平均；pooled R@50以关系条数加权。指标分别报告全部968条GT与固定530条有效端点GT。", "",
             "未匹配PSG标注的预测不能直接认定为视觉错误，PSG中也可能存在未标注关系。下文的匹配比例、校准误差和风险均以“是否匹配现有PSG标注”为目标代理，不能解释为人工准确率、真实精确率或幻觉比例。", "",
             "## 固定预算解码结果", "",
             "| 解码方式 | 输出条数 | 全部968条：命中 / R@50 / mR@50 / pooled R@50 | 有效530条：命中 / R@50 / mR@50 / pooled R@50 |", "|---|---:|---|---|"]
    for method in ("top1", "top2", "top3", "top5", "dual", "single"):
        item = metrics[method]
        full, valid = item["all_968_GT"], item["fixed_530_valid_endpoint_GT"]
        lines.append(f"| {method_titles[method]} | {item['predictions_under_budget']} | "
                     f"{full['hits']} / {full['R@50_image_macro']:.4f} / {full['mR@50_class_macro']:.4f} / {full['pooled_R@50']:.4f} | "
                     f"{valid['hits']} / {valid['R@50_image_macro']:.4f} / {valid['mR@50_class_macro']:.4f} / {valid['pooled_R@50']:.4f} |")
    lines.extend(["", "在全部968条GT上，Top5较双赢家多命中95条（315对220），图像宏平均R@50从0.2448升至0.3517，mR@50从0.1993升至0.3341；两者在每张图像上仍受50条上限约束。Top5共有12,530条输出，双赢家共有10,824条，增加1,706条。该结果说明保留每对物体更多谓词可找回部分低排名GT，代价是输出增加；它没有单独检验新增输出是否符合图像内容。", "",
                  "每个谓词类别的GT数、命中数和两类子集召回见 [`per_predicate_recall.csv`](evidence/per_predicate_recall.csv)。逐条候选及其原始分数、物体编号、分组、图像拆分和标注匹配代理标签见 [`selected_candidates.csv`](evidence/selected_candidates.csv)。", "",
                  "重建的空间/语义双赢家和单赢家输出在每张图像、每条记录上与原实验对应字段比较，数量、排序和关系编号完全相同。各方法在每张图像上的输出均不超过50条。530条冻结关系及端点匹配定义见 [`fixed_valid_endpoint_gt.json`](evidence/fixed_valid_endpoint_gt.json)。", "",
                  "## 固定端点的GT边界框oracle比较", "",
                  "本表只在旧检测器词表中、且两个端点都被检测边界框匹配的同一530条GT关系上比较。检测边界框组和GT边界框组使用同一组GT、每张图像50条预算、相同解码规则；差值按源图像身份成对重抽样，置信区间使用1000次bootstrap。GT边界框组将输入端点替换为PSG标注边界框和类别，属于端点oracle诊断，不代表端到端检测结果。", "",
                  "| 解码方式 | 检测边界框：命中 / R@50 / mR@50 / pooled R@50 | GT边界框：命中 / R@50 / mR@50 / pooled R@50 | ΔR@50点估计（95%区间） | ΔmR@50点估计（95%区间） |", "|---|---|---|---:|---:|"])
    interval_map = {(row["comparison"], row["metric"]): row for row in oracle_intervals}
    for method in ("top1", "top2", "top3", "top5", "dual", "single"):
        detected = metrics[method]["fixed_530_valid_endpoint_GT"]
        oracle = oracle_metrics[method]
        delta_r = interval_map[(f"gt_boxes_{method} - detected_{method}", "R@50_image_macro")]
        delta_mr = interval_map[(f"gt_boxes_{method} - detected_{method}", "mR@50_class_macro")]
        lines.append(f"| {method_titles[method]} | {detected['hits']} / {detected['R@50_image_macro']:.4f} / "
                     f"{detected['mR@50_class_macro']:.4f} / {detected['pooled_R@50']:.4f} | "
                     f"{oracle['hits']} / {oracle['R@50_image_macro']:.4f} / "
                     f"{oracle['mR@50_class_macro']:.4f} / {oracle['pooled_R@50']:.4f} | "
                     f"{delta_r['estimate_delta']:+.4f} ({delta_r['bootstrap_delta_95pct_low']:.4f}, {delta_r['bootstrap_delta_95pct_high']:.4f}) | "
                     f"{delta_mr['estimate_delta']:+.4f} ({delta_mr['bootstrap_delta_95pct_low']:.4f}, {delta_mr['bootstrap_delta_95pct_high']:.4f}) |")
    lines.extend(["", "六种解码的ΔR@50和ΔmR@50区间均覆盖零，当前样本没有显示GT边界框端点使解码召回稳定上升。该判断只适用于旧检测器词表覆盖且端点可匹配的530条关系；另外438条GT不在这个条件比较的分母内。按源图像与谓词统计的成对差值区间见 [`fixed530_endpoint_oracle_paired_deltas.csv`](evidence/fixed530_endpoint_oracle_paired_deltas.csv)，固定子集上的逐谓词GT边界框命中数见 [`fixed530_gtbox_per_predicate.csv`](evidence/fixed530_gtbox_per_predicate.csv)，对应的GT边界框候选见 [`gt_box_selected_candidates.csv`](evidence/gt_box_selected_candidates.csv)。完整指标和oracle定义见 [`fixed530_endpoint_oracle_metrics.json`](evidence/fixed530_endpoint_oracle_metrics.json)。", "",
                  "## GT谓词排名", "",
                  "对每条GT关系，在其所有可匹配有向检测物体对中，记录GT谓词在全部56类排序及其正确空间/语义分组中的最佳局部排名，并记录双赢家规则下的图像级候选排名。在固定530关系中，GT谓词在全部56类里的最佳排名为第1/2/3名的数量分别是192/101/42，前三名共335条（63.2%）；限制到正确空间或语义组内后，第1/2/3名分别为246/108/34，前三名共388条（73.2%）。这说明组内竞争能把一部分正确谓词排得更靠前，但图像级Top50还要与不同物体对竞争。530条固定子集的逐条排名见 [`gt_predicate_ranks.csv`](evidence/gt_predicate_ranks.csv)，逐谓词排名1、2、3、4–5、6–10、10名之后及无候选计数见 [`per_predicate_rank_histograms.csv`](evidence/per_predicate_rank_histograms.csv)。GT边界框下对应物体对的逐条排名保存在 [`gt_box_oracle_pair_ranks.csv`](evidence/gt_box_oracle_pair_ranks.csv)，可用于分开观察端点质量和谓词排序。", "",
                  "## 校准", "",
                  f"图像身份根据 Visual Genome `image_data.json` 的 `image_id → coco_id` 映射确定；缺少COCO ID时使用图像SHA256，相同SHA256也会合并身份组。随机种子 `{config['split_seed']}` 用于分配其余身份组，COCO ID `404484` 固定进入训练集。最终拆分为训练/验证/测试各300/100/100条记录，对应299/100/100个唯一源图像身份；404484组的两条记录都留在训练集。三份拆分之间的COCO ID与SHA256交集均为空。每张图像的身份、分组和互斥核验见 [`calibration_image_splits.json`](evidence/calibration_image_splits.json)。", "",
                  "这两条重复源图像记录的检测结果相同，PSG对象相同而关系标注不同；现有标注证据均保留。为避免同一像素图在Platt拟合中重复加权，训练时只保留该身份组一份预测候选，并对这组现有关系标注匹配代理标签取并集。训练记录数仍为300，Platt拟合使用299个唯一源图像身份；验证集用于选择间隔拒绝阈值，测试集仅报告结果。", "",
                  f"拟合斜率 a={fit['a']:.6f}、截距 b={fit['b']:.6f}。", "",
                  f"训练、验证、测试集上的双赢家候选匹配PSG标注比例分别为{train_calibration['positive_annotation_match_proxy_rows']}/{train_calibration['candidate_rows']:,}（{train_calibration['proxy_prevalence']:.2%}）、{validation_calibration['positive_annotation_match_proxy_rows']}/{validation_calibration['candidate_rows']:,}（{validation_calibration['proxy_prevalence']:.2%}）和{test_calibration['positive_annotation_match_proxy_rows']}/{test_calibration['candidate_rows']:,}（{test_calibration['proxy_prevalence']:.2%}）。官方参数来自RelateAnything已人工裁定候选上的拟合；本实验检查它在当前PSG匹配代理上的行为。标签集合、候选集合和标注完整度均不同，因此官方参数原本的人工概率含义不能直接转移到这里。ECE使用15个等宽分箱，按各箱样本数加权；可靠性图与分箱数值使用100个测试源图像身份。", "",
                  "| 测试集分数 | ECE（PSG匹配代理） | Brier（PSG匹配代理） |", "|---|---:|---:|"])
    for name, title in (("raw_sigmoid", "原始 sigmoid"), ("official", "官方校准"),
                        ("local_platt", "独立图像拆分 Platt"), ("train_prevalence", "训练集正例率常数")):
        value = calibration["test"][name]
        lines.append(f"| {title} | {value['ECE_annotation_match_proxy']:.5f} | {value['Brier_annotation_match_proxy']:.5f} |")
    lines.extend(["", "![](calibration_reliability.png)", "",
                  f"常数基线始终输出训练集去重候选的PSG匹配率，参数不使用验证或测试标签。本次测试候选的PSG匹配率为{test_calibration['proxy_prevalence']:.2%}，常数也能取得较低的ECE与Brier；本地Platt相对它的收益需要结合两项差值判断。低ECE本身不证明候选辨别能力，也不证明图像关系真实性。", "",
                  "正斜率仿射变换通过排序不变性检查；官方和本地 Platt 概率排序与原始融合 logit 一致，校准只改变置信度值。分箱置信度、样本数和标注匹配比例见 [`calibration_bins.csv`](evidence/calibration_bins.csv)，拟合与拆分统计见 [`calibration_metrics.json`](evidence/calibration_metrics.json)。", "",
                  "## 间隔拒绝", "",
                  "间隔定义为同一物体对、同一谓词组中第一名与第二名融合 logit 的差。对双赢家每条输出分别保存所属组的间隔。验证图像按目标覆盖选择阈值，测试图像不参与阈值选择；表格中的“风险”是输出候选中未匹配PSG关系标注的比例。", "",
                  "| 验证目标覆盖 | 验证实际覆盖 | 间隔阈值 | 测试保留数 / 总数 | 测试保留标注匹配数 / 总数 | 测试丢弃标注匹配数 | 测试覆盖 | 标注匹配率代理（95%图像bootstrap区间） | 标注风险代理 | 测试有效端点GT命中 / 总数（pooled R及区间） |", "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for row in selective:
        lines.append(f"| {row['target_coverage_from_validation']:.0%} | {row['validation_achieved_coverage']:.3f} | "
                     f"{row['margin_threshold']:.5f} | {row['test_kept_candidates']} / {row['test_candidates']} | "
                     f"{row['test_annotation_match_candidates_retained']} / {row['test_annotation_match_candidates_total']} | "
                     f"{row['test_annotation_match_candidates_dropped']} | "
                     f"{row['test_coverage']:.3f} | {row['annotation_match_rate_proxy']:.4f} "
                     f"({row['annotation_match_rate_proxy_bootstrap_95pct_low']:.4f}, "
                     f"{row['annotation_match_rate_proxy_bootstrap_95pct_high']:.4f}) | "
                     f"{row['annotation_risk_proxy']:.4f} | "
                     f"{row['test_valid_endpoint_GT_recalled']} / {row['test_valid_endpoint_GT']} "
                     f"({row['test_valid_endpoint_GT_pooled_recall']:.4f}; "
                     f"{row['test_valid_endpoint_GT_pooled_recall_bootstrap_95pct_low']:.4f}, "
                     f"{row['test_valid_endpoint_GT_pooled_recall_bootstrap_95pct_high']:.4f}) |")
    lines.extend(["", "![](margin_risk_coverage.png)", "",
                  "完整测试风险—覆盖轨迹及各阈值细节见 [`margin_risk_coverage_curve.csv`](evidence/margin_risk_coverage_curve.csv)；在验证图像确定的阈值和测试评估统计见 [`margin_selective_thresholds.csv`](evidence/margin_selective_thresholds.csv)。低覆盖可能主要移除困难候选，因此需要同时看保留数量、被移除的标注匹配候选以及GT召回，不能只看匹配比例变化。", "",
                  "## 不确定性和可复查材料", "",
                  f"使用499个唯一源图像身份为重抽样单位进行 {config['bootstrap_repetitions']} 次 bootstrap；同身份组内的所有记录在每次抽样中一起保留，输出R@50、mR@50和候选标注匹配比例代理的95%区间。Top1、Top2、Top3和Top5相对双赢家，以及检测边界框相对GT边界框的差值都按同一身份组配对重抽样。区间表见 [`bootstrap_intervals.csv`](evidence/bootstrap_intervals.csv) 和 [`fixed530_endpoint_oracle_paired_deltas.csv`](evidence/fixed530_endpoint_oracle_paired_deltas.csv)。这些区间反映固定500条记录、499个身份样本的抽样变化，不包含人工标注误差。", "",
                  "## 结果边界", "",
                  "该实验隔离了解码选择、已知检测端点覆盖和当前PSG标注的匹配关系。固定530条GT能减少端点缺失对解码方法比较的影响，但检测边界框仍可能有重复实例或定位偏差。GT边界框排名提供一个端点条件参考。标注匹配代理也无法审计PSG未覆盖关系的视觉真实性。", "",
                  "## 复现", "",
                  "运行环境需提供仓库既有 `.venv-eval` 中的 numpy、scipy、matplotlib，以及本地 `HOR/research/data/visual_genome_metadata/image_data.json`。该Visual Genome文件提供 `image_id → coco_id` 来源映射；脚本运行时不下载文件、不调用GPU，只读取已生成的500条记录的原始logits。当前拆分的身份字段和交集核验随报告保存在证据目录。", "",
                  "```powershell", ".\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\decode_study.py", "```", "",
                  "输出配置：[`decoder_study.json`](../../configs/decoder_study.json)。全部表格、拆分清单与逐候选证据随报告保存在 [`evidence/`](evidence/)；原始可再生成结果位于本机忽略目录 `HOR/research/output/decoder/`。", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    main()
