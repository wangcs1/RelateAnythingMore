from collections import Counter, defaultdict
import statistics

import numpy as np
from torchvision.ops import box_iou
import torch

from pipeline import CONFIG


def triplet(row):
    return row["subject_id"], row["object_id"], row["predicate_id"]


def group_gt(record, group):
    objects = {item["id"]: item for item in record["ground_truth_objects"]}
    result = []
    for row in record["ground_truth_relations"]:
        s, o = objects[row["subject_id"]], objects[row["object_id"]]
        keep = {"all_human": s["is_person"] or o["is_person"],
                "human_nonhuman": s["is_person"] != o["is_person"],
                "human_human": s["is_person"] and o["is_person"],
                "human_subject": s["is_person"], "human_object": o["is_person"]}[group]
        if keep:
            result.append(row)
    return result


def endpoint_matches(predicted, ground_truth, same_ids, class_aware=True):
    if same_ids:
        return {item["id"]: {item["id"]} for item in ground_truth}
    matches = {item["id"]: set() for item in ground_truth}
    if not predicted or not ground_truth:
        return matches
    overlaps = box_iou(torch.tensor([item["box_xyxy"] for item in ground_truth]),
                       torch.tensor([item["box_xyxy"] for item in predicted])).numpy()
    for g, reference in enumerate(ground_truth):
        for p, item in enumerate(predicted):
            if overlaps[g, p] >= CONFIG["iou_threshold"] and (
                    not class_aware or reference["label"] == item["label"]):
                matches[reference["id"]].add(item["id"])
    return matches


def evaluate(records, mode, key="relations", class_aware=True, group="all_human"):
    recalls = {k: [] for k in (20, 50)}
    class_recalls = {k: defaultdict(list) for k in recalls}
    pooled_hits = Counter()
    pooled_classes = Counter()
    pooled_class_hits = Counter()
    stages = Counter()
    details = []
    total_gt = 0
    total_predictions = 0
    prediction_counter = Counter()
    for record in records:
        prediction = record[mode]
        rows = prediction[key]
        total_predictions += len(rows)
        prediction_counter.update(row["predicate"] for row in rows)
        gt = group_gt(record, group)
        if not gt:
            continue
        matches = endpoint_matches(prediction["objects"], record["ground_truth_objects"],
                                   mode != "detected", class_aware)
        hits = {k: set() for k in recalls}
        local_stages = Counter()
        diagnostics = []
        for truth in gt:
            s, o, p = triplet(truth)
            sub_matches, obj_matches = matches[s], matches[o]
            for k in recalls:
                if any(row["subject_id"] in sub_matches and row["object_id"] in obj_matches
                       and row["predicate_id"] == p for row in rows[:k]):
                    hits[k].add((s, o, p))
            if (s, o, p) in hits[50]:
                stage = "hit50"
            elif not sub_matches or not obj_matches:
                stage = "endpoint_missing_or_wrong_class"
            else:
                selected = [pair for pair in prediction["all_human_pairs"]
                            if pair["subject_id"] in sub_matches and pair["object_id"] in obj_matches]
                if not selected:
                    distinct_endpoints = any(s != o for s in sub_matches for o in obj_matches)
                    stage = "pair_not_selected" if distinct_endpoints else "endpoints_collapsed_to_same_box"
                else:
                    if key == "single_predicate_top50":
                        def best_pair(pair):
                            return [max(pair["predictions"], key=lambda row: row["fused_logit"])]
                    else:
                        def best_pair(pair):
                            return pair["predictions"]
                    correct = any(row["predicate_id"] == p for pair in selected for row in best_pair(pair))
                    stage = "rank_below50" if correct else "wrong_predicate"
            local_stages[stage] += 1
            diagnostics.append({"subject_id": s, "object_id": o, "predicate": truth["predicate"],
                                "stage": stage, "matching_subject_ids": sorted(sub_matches),
                                "matching_object_ids": sorted(obj_matches)})
        stages.update(local_stages)
        total_gt += len(gt)
        denominators = Counter(row["predicate_id"] for row in gt)
        pooled_classes.update(denominators)
        for k in recalls:
            recalls[k].append(len(hits[k]) / len(gt))
            pooled_hits[k] += len(hits[k])
            numerators = Counter(p for _, _, p in hits[k])
            for predicate, number in denominators.items():
                class_recalls[k][predicate].append(numerators[predicate] / number)
            if k == 50:
                pooled_class_hits.update(numerators)
        details.append({"index": record["index"], "gt_count": len(gt), "hits50": len(hits[50]),
                        "R@50": len(hits[50]) / len(gt), "stages": dict(local_stages),
                        "diagnostics": diagnostics})
    metrics = {}
    for k in recalls:
        metrics[f"R@{k}"] = statistics.mean(recalls[k]) if recalls[k] else None
        metrics[f"mR@{k}"] = statistics.mean(statistics.mean(values) for values in class_recalls[k].values()) if class_recalls[k] else None
        metrics[f"pooled_R@{k}"] = pooled_hits[k] / total_gt if total_gt else None
    return {"mode": mode, "ranking": key, "class_aware": class_aware, "group": group,
            "images": len(records), "scored_images": len(details), "unique_gt": total_gt,
            "metrics": metrics, "hits": dict(pooled_hits), "failure_stages": dict(stages),
            "predictions": total_predictions, "prediction_predicates": dict(prediction_counter),
            "per_class": {str(p): {"gt": pooled_classes[p], "hits50": pooled_class_hits[p],
                                   "pooled_R@50": pooled_class_hits[p] / pooled_classes[p],
                                   "image_macro_R@50": statistics.mean(class_recalls[50][p])}
                          for p in sorted(pooled_classes)}, "per_image": details}


def detection_summary(records):
    gt_people = detected_people = matched_people = 0
    gt_person_images = detected_person_images = correct_person_images = 0
    empty_person_images = false_person_images = 0
    gt_endpoints = matched_endpoints = detectable_endpoints = matched_detectable_endpoints = 0
    for record in records:
        reference = record["ground_truth_objects"]
        detected = record["detected"]["objects"]
        people = [item for item in reference if item["is_person"]]
        detected_humans = [item for item in detected if item["is_person"]]
        matches = endpoint_matches(detected, reference, False)
        gt_people += len(people)
        detected_people += len(detected_humans)
        matched_people += sum(bool(matches[item["id"]]) for item in people)
        gt_person_images += bool(people)
        detected_person_images += bool(detected_humans)
        correct_person_images += bool(people and detected_humans)
        empty_person_images += not people
        false_person_images += bool(not people and detected_humans)
        ids = {row[key] for row in record["ground_truth_relations"] for key in ("subject_id", "object_id")}
        for item in reference:
            if item["id"] not in ids:
                continue
            gt_endpoints += 1
            matched_endpoints += bool(matches[item["id"]])
            if item["label"] in record["detector_categories"]:
                detectable_endpoints += 1
                matched_detectable_endpoints += bool(matches[item["id"]])
    return {"GT_people": gt_people, "detected_people": detected_people,
            "matched_GT_people_IoU05_class_aware": matched_people,
            "person_box_recall": matched_people / gt_people if gt_people else None,
            "GT_person_images": gt_person_images, "detected_person_images": detected_person_images,
            "positive_images_with_person_detected": correct_person_images,
            "GT_no_person_images": empty_person_images, "no_person_images_with_detection": false_person_images,
            "human_GT_relation_unique_endpoints": gt_endpoints, "matched_endpoints": matched_endpoints,
            "endpoint_recall": matched_endpoints / gt_endpoints if gt_endpoints else None,
            "endpoints_in_detector_vocabulary": detectable_endpoints,
            "matched_endpoints_in_detector_vocabulary": matched_detectable_endpoints,
            "covered_vocabulary_endpoint_recall": matched_detectable_endpoints / detectable_endpoints if detectable_endpoints else None}
