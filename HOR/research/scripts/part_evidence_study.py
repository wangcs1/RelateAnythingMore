import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment


ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "HOR/research/configs/part_evidence.json"
JOINT_NAMES = (
    "nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder",
    "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist",
    "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle",
)
PART_GROUPS = ("hands", "forearms", "shoulders", "hips", "legs", "feet")
BALANCED_GROUPS = {"hands": [9, 10], "forearms": [7, 8], "shoulders": [5, 6],
                   "hips": [11, 12], "legs": [13, 14], "feet": [15, 16]}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_records(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        normalized_rows = ({key: json.dumps(value, ensure_ascii=False, sort_keys=True)
                            if isinstance(value, (dict, list)) else value
                            for key, value in row.items()} for row in rows)
        writer.writerows(normalized_rows)


def intersection_over_union(first, second):
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    intersection = max(0.0, right - left) * max(0.0, bottom - top)
    area_first = max(0.0, first[2] - first[0]) * max(0.0, first[3] - first[1])
    area_second = max(0.0, second[2] - second[0]) * max(0.0, second[3] - second[1])
    union = area_first + area_second - intersection
    return intersection / union if union > 0 else 0.0


def scale_box(box, scale_x, scale_y):
    return [box[0] * scale_x, box[1] * scale_y,
            box[2] * scale_x, box[3] * scale_y]


def point_box_distance(point, box):
    delta_x = max(box[0] - point[0], 0.0, point[0] - box[2])
    delta_y = max(box[1] - point[1], 0.0, point[1] - box[3])
    return math.hypot(delta_x, delta_y)


def match_people(psg_people, coco_people, scale_x, scale_y, threshold):
    if not psg_people or not coco_people:
        return {}
    overlaps = np.zeros((len(psg_people), len(coco_people)), dtype=np.float64)
    for person_index, person in enumerate(psg_people):
        for annotation_index, annotation in enumerate(coco_people):
            x, y, width, height = annotation["bbox"]
            coco_box = scale_box([x, y, x + width, y + height], scale_x, scale_y)
            overlaps[person_index, annotation_index] = intersection_over_union(
                person["box_xyxy"], coco_box
            )
    person_indices, annotation_indices = linear_sum_assignment(-overlaps)
    return {psg_people[person_index]["id"]: {
        "annotation": coco_people[annotation_index],
        "iou": float(overlaps[person_index, annotation_index]),
    } for person_index, annotation_index in zip(person_indices, annotation_indices)
        if overlaps[person_index, annotation_index] >= threshold}


def visible_group_points(annotation, group_ids, scale_x, scale_y, visible_only):
    keypoints = annotation["keypoints"]
    points = []
    for joint_id in group_ids:
        x, y, visibility = keypoints[joint_id * 3:joint_id * 3 + 3]
        if visibility == 0 or (visible_only and visibility != 2):
            continue
        points.append({"joint_id": joint_id, "joint": JOINT_NAMES[joint_id],
                       "x": x * scale_x, "y": y * scale_y,
                       "visibility": int(visibility)})
    return points


def predicted_group_points(annotation, group_ids, confidence_threshold):
    points = []
    for joint_id in group_ids:
        x, y, visibility = annotation["keypoints"][joint_id]
        confidence = annotation["keypoints_scores"][joint_id]
        if confidence < confidence_threshold:
            continue
        points.append({"joint_id": joint_id, "joint": JOINT_NAMES[joint_id],
                       "x": x, "y": y, "confidence": confidence, "visibility": visibility})
    return points


def route_scores(distances, route):
    available = {name: float(distance) for name, distance in distances.items() if distance is not None}
    if not available:
        return {"available_group_count": 0, "nearest_group_count": 0,
                "route_rank": None, "inclusive": 0.0, "unique": 0.0, "fractional": 0.0}
    minimum = min(available.values())
    closest = {name for name, value in available.items()
               if math.isclose(value, minimum, rel_tol=0.0, abs_tol=1e-10)}
    route_distance = available.get(route)
    rank = (1 + sum(value < route_distance - 1e-10 for value in available.values())
            if route_distance is not None else None)
    route_nearest = route in closest
    return {"available_group_count": len(available), "nearest_group_count": len(closest),
            "route_rank": rank, "inclusive": float(route_nearest),
            "unique": float(route_nearest and len(closest) == 1),
            "fractional": 1.0 / len(closest) if route_nearest else 0.0}


def apply_route_scores(row):
    route = row["routed_part_group"]
    for prefix, field in (("routed", "all_group_nearest_distance_object_diagonals"),
                           ("predicted_routed", "predicted_all_group_nearest_distance_object_diagonals")):
        scores = route_scores(row[field], route)
        row[f"{prefix}_group_rank_by_object_box_distance"] = scores["route_rank"]
        for key in ("available_group_count", "nearest_group_count", "inclusive", "unique", "fractional"):
            row[f"{prefix}_{key}"] = scores[key]
    return row


def relation_rows(records, vg_metadata, coco_images, coco_people, predicted_people_by_file, config):
    route = config["predicate_part_routes"]
    group_ids = config["keypoint_groups"]
    threshold = config["iou_threshold"]
    max_ratio_error = config["max_aspect_ratio_error"]
    relation_results = []
    image_results = []
    mapped_sample_images = 0
    compatible_images = 0
    annotated_images = 0
    psg_people_total = 0
    matched_people_total = 0
    mapped_people_with_keypoints = 0
    predicted_people_matched_total = 0
    considered_relations = 0
    predicted_routed_relations = 0
    skipped_unmatched_relations = 0
    duplicate_source_images = 0
    map_rows = []
    seen_coco_ids = set()

    for record in records:
        vg_id = int(Path(record["file_name"]).stem)
        metadata = vg_metadata.get(vg_id)
        if metadata is None or metadata.get("coco_id") is None:
            image_results.append({"index": record["index"], "file_name": record["file_name"],
                                  "status": "no_coco_id", "relation_count": 0})
            continue
        mapped_sample_images += 1
        coco_id = int(metadata["coco_id"])
        coco_image = coco_images.get(coco_id)
        if coco_id in seen_coco_ids:
            duplicate_source_images += 1
            image_results.append({"index": record["index"], "file_name": record["file_name"],
                                  "coco_id": coco_id, "status": "duplicate_coco_source_excluded",
                                  "relation_count": 0})
            map_rows.append({"vg_image_id": vg_id, "coco_image_id": coco_id,
                             "coco_split": coco_image["split"] if coco_image else "",
                             "local_width": record["image_size"][0],
                             "local_height": record["image_size"][1],
                             "coco_width": coco_image["width"] if coco_image else "",
                             "coco_height": coco_image["height"] if coco_image else "",
                             "aspect_ratio_error": "", "keypoint_annotations": 0,
                             "status": "duplicate_coco_source_excluded"})
            continue
        seen_coco_ids.add(coco_id)
        if coco_image is None:
            image_results.append({"index": record["index"], "file_name": record["file_name"],
                                  "coco_id": coco_id, "status": "no_coco_keypoint_image",
                                  "relation_count": 0})
            map_rows.append({"vg_image_id": vg_id, "coco_image_id": coco_id,
                             "coco_split": "", "local_width": record["image_size"][0],
                             "local_height": record["image_size"][1], "coco_width": "",
                             "coco_height": "", "aspect_ratio_error": "",
                             "keypoint_annotations": 0, "status": "no_coco_keypoint_image"})
            continue

        local_width, local_height = record["image_size"]
        coco_width, coco_height = coco_image["width"], coco_image["height"]
        local_ratio = local_width / local_height
        coco_ratio = coco_width / coco_height
        ratio_error = abs(local_ratio / coco_ratio - 1.0)
        scale_x = local_width / coco_width
        scale_y = local_height / coco_height
        annotations = coco_people.get(coco_id, [])
        if ratio_error > max_ratio_error:
            status = "aspect_ratio_mismatch"
        else:
            status = "compatible_geometry"
            compatible_images += 1
        if annotations:
            annotated_images += 1
        map_rows.append({"vg_image_id": vg_id, "coco_image_id": coco_id,
                         "coco_split": coco_image["split"], "local_width": local_width,
                         "local_height": local_height, "coco_width": coco_width,
                         "coco_height": coco_height, "aspect_ratio_error": ratio_error,
                         "keypoint_annotations": len(annotations), "status": status})

        people = [item for item in record["ground_truth_objects"] if item["is_person"]]
        psg_people_total += len(people)
        matches = match_people(people, annotations, scale_x, scale_y, threshold) if status == "compatible_geometry" else {}
        matched_people_total += len(matches)
        if status == "compatible_geometry":
            mapped_people_with_keypoints += len(annotations)
        person_map = {person["id"]: matches[person["id"]]["annotation"]
                      for person in people if person["id"] in matches}
        predicted_people = []
        for prediction_index, prediction in enumerate(predicted_people_by_file.get(record["file_name"], [])):
            x1, y1, x2, y2 = prediction["box_xyxy"]
            predicted_people.append({"id": prediction_index,
                                     "bbox": [x1, y1, x2 - x1, y2 - y1],
                                     "keypoints": prediction["keypoints"],
                                     "keypoints_scores": prediction["keypoints_scores"],
                                     "score": prediction["detection_score"]})
        predicted_matches = match_people(people, predicted_people, 1.0, 1.0, threshold)
        predicted_people_matched_total += len(predicted_matches)
        predicted_person_map = {person["id"]: predicted_matches[person["id"]]["annotation"]
                                for person in people if person["id"] in predicted_matches}
        image_relation_rows = 0
        for relation in record["ground_truth_relations"]:
            subject = next(item for item in record["ground_truth_objects"]
                           if item["id"] == relation["subject_id"])
            obj = next(item for item in record["ground_truth_objects"]
                       if item["id"] == relation["object_id"])
            person = subject if subject["is_person"] else obj if obj["is_person"] else None
            target = obj if person is subject else subject if person is obj else None
            if person is None or target is None:
                continue
            if person["id"] not in person_map or status != "compatible_geometry":
                skipped_unmatched_relations += 1
                continue
            predicate = relation["predicate"]
            routed_group = route.get(predicate)
            if routed_group is None:
                continue

            annotation = person_map[person["id"]]
            predicted_annotation = predicted_person_map.get(person["id"])
            target_box = target["box_xyxy"]
            target_diagonal = math.hypot(target_box[2] - target_box[0],
                                         target_box[3] - target_box[1])
            if target_diagonal <= 0:
                raise ValueError(f"Target object has zero diagonal: image {record['index']}, object {target['id']}")
            distances = {}
            predicted_distances = {}
            labelled_counts = {}
            visible_counts = {}
            predicted_visible_counts = {}
            visible_joint_distances = {}
            predicted_joint_distances = {}
            for part_group, joints in group_ids.items():
                labelled = visible_group_points(annotation, joints, scale_x, scale_y, False)
                visible = visible_group_points(annotation, joints, scale_x, scale_y, True)
                labelled_counts[part_group] = len(labelled)
                visible_counts[part_group] = len(visible)
                for point in visible:
                    visible_joint_distances[str(point["joint_id"])] = point_box_distance(
                        (point["x"], point["y"]), target_box) / target_diagonal
                distances[part_group] = min(
                    (point_box_distance((point["x"], point["y"]), target_box)
                     for point in visible), default=None
                )
                predicted_points = (predicted_group_points(
                    predicted_annotation, joints, config["keypoint_confidence_threshold"]
                ) if predicted_annotation else [])
                predicted_visible_counts[part_group] = len(predicted_points)
                for point in predicted_points:
                    predicted_joint_distances[str(point["joint_id"])] = point_box_distance(
                        (point["x"], point["y"]), target_box) / target_diagonal
                predicted_distances[part_group] = min(
                    (point_box_distance((point["x"], point["y"]), target_box)
                     for point in predicted_points), default=None
                )
            route_distance = distances[routed_group]
            predicted_route_distance = predicted_distances[routed_group]
            record_result = {
                "sample_position": record["sample_position"],
                "index": record["index"],
                "file_name": record["file_name"],
                "vg_image_id": vg_id,
                "coco_image_id": coco_id,
                "person_id": person["id"],
                "person_role": "subject" if person is subject else "object",
                "person_box_xyxy": person["box_xyxy"],
                "object_id": target["id"],
                "object_label": target["label"],
                "object_box_xyxy": target_box,
                "object_box_diagonal_pixels": target_diagonal,
                "predicate": predicate,
                "routed_part_group": routed_group,
                "person_box_iou": matches[person["id"]]["iou"],
                "routed_labeled_joint_count": labelled_counts[routed_group],
                "routed_visible_joint_count": visible_counts[routed_group],
                "routed_nearest_distance_pixels": route_distance,
                "routed_nearest_distance_object_diagonals":
                    route_distance / target_diagonal if route_distance is not None and target_diagonal > 0 else None,
                "all_group_nearest_distance_object_diagonals": {
                    name: distance / target_diagonal if distance is not None and target_diagonal > 0 else None
                    for name, distance in distances.items()
                },
                "predicted_person_box_iou": (predicted_matches[person["id"]]["iou"]
                                              if person["id"] in predicted_matches else None),
                "predicted_person_detection_score": (predicted_annotation["score"]
                                                     if predicted_annotation else None),
                "predicted_routed_visible_joint_count": predicted_visible_counts[routed_group],
                "predicted_routed_nearest_distance_object_diagonals":
                    predicted_route_distance / target_diagonal
                    if predicted_route_distance is not None and target_diagonal > 0 else None,
                "predicted_all_group_nearest_distance_object_diagonals": {
                    name: distance / target_diagonal if distance is not None and target_diagonal > 0 else None
                    for name, distance in predicted_distances.items()
                },
                "all_group_visible_joint_counts": visible_counts,
                "predicted_all_group_visible_joint_counts": predicted_visible_counts,
                "visible_joint_distances_object_diagonals": visible_joint_distances,
                "predicted_joint_distances_object_diagonals": predicted_joint_distances,
            }
            relation_results.append(apply_route_scores(record_result))
            image_relation_rows += 1
            considered_relations += 1
            predicted_routed_relations += int(predicted_annotation is not None)
        image_results.append({"index": record["index"], "file_name": record["file_name"],
                              "coco_id": coco_id, "status": status,
                              "aspect_ratio_error": ratio_error,
                              "psg_person_count": len(people),
                              "matched_psg_person_count": len(matches),
                              "coco_keypoint_person_count": len(annotations),
                              "routed_relation_count": image_relation_rows})

    summary = {
        "sample_images": len(records),
        "sample_images_with_coco_mapping": mapped_sample_images,
        "unique_coco_source_images_analyzed": len(seen_coco_ids),
        "duplicate_coco_source_images_excluded": duplicate_source_images,
        "geometry_compatible_images": compatible_images,
        "images_with_coco_person_keypoint_annotations": annotated_images,
        "psg_person_boxes": psg_people_total,
        "psg_person_boxes_matched_iou_threshold": threshold,
        "matched_psg_person_boxes": matched_people_total,
        "predicted_keypoint_model_matched_psg_person_boxes": predicted_people_matched_total,
        "coco_keypoint_person_annotations_on_compatible_images": mapped_people_with_keypoints,
        "routed_human_object_relations": considered_relations,
        "routed_relations_with_matched_predicted_person": predicted_routed_relations,
        "unmatched_or_incompatible_human_object_relations": skipped_unmatched_relations,
        "part_proxy_predicates": sorted(route),
    }
    return relation_results, image_results, map_rows, summary


def bootstrap_statistics(relation_rows, config, prefix="routed"):
    by_image = defaultdict(list)
    for row in relation_rows:
        by_image[row["coco_image_id"]].append(row)
    image_keys = sorted(by_image)
    if not image_keys:
        return {}
    rng = np.random.default_rng(config["bootstrap_seed"])
    repetitions = config["bootstrap_repetitions"]
    thresholds = config["proximity_thresholds_object_diagonals"]
    group_stats = {}
    predicates = sorted({row["predicate"] for row in relation_rows})
    for predicate in predicates:
        predicate_images = [key for key in image_keys
                            if any(row["predicate"] == predicate for row in by_image[key])]
        values = []
        distance_field = f"{prefix}_nearest_distance_object_diagonals"
        score_field = f"{prefix}_fractional"
        visible_field = f"{prefix}_visible_joint_count"
        groups_field = ("all_group_nearest_distance_object_diagonals" if prefix == "routed"
                        else "predicted_all_group_nearest_distance_object_diagonals")
        for key in predicate_images:
            rows = [row for row in by_image[key] if row["predicate"] == predicate]
            values.append({
                "nearest": sum(row[score_field] for row in rows
                                if any(distance is not None
                                       for distance in row[groups_field].values())),
                "inclusive": sum(row[f"{prefix}_inclusive"] for row in rows),
                "unique": sum(row[f"{prefix}_unique"] for row in rows),
                "ties": sum(row[f"{prefix}_nearest_group_count"] > 1 for row in rows
                            if row[f"{prefix}_available_group_count"] > 0),
                "n": sum(any(distance is not None for distance in row[groups_field].values())
                         for row in rows),
                "routed_available": sum(row.get(distance_field) is not None for row in rows),
                "visible": sum(row[visible_field] > 0 for row in rows),
                "total": len(rows),
                "within_threshold": {
                    str(threshold): sum(
                        row.get(distance_field) is not None and
                        row[distance_field] <= threshold for row in rows
                    ) for threshold in thresholds
                },
            })
        point_nearest = sum(item["nearest"] for item in values) / max(1, sum(item["n"] for item in values))
        point_visible = sum(item["visible"] for item in values) / max(1, sum(item["total"] for item in values))
        sampled = rng.integers(0, len(values), size=(repetitions, len(values)))
        samples_nearest = []
        samples_visible = []
        samples_thresholds = {str(threshold): [] for threshold in thresholds}
        for indices in sampled:
            chosen = [values[index] for index in indices]
            nearest_n = sum(item["n"] for item in chosen)
            nearest_hit = sum(item["nearest"] for item in chosen)
            visible_n = sum(item["total"] for item in chosen)
            visible_hit = sum(item["visible"] for item in chosen)
            samples_nearest.append(nearest_hit / nearest_n if nearest_n else math.nan)
            samples_visible.append(visible_hit / visible_n if visible_n else math.nan)
            for threshold in thresholds:
                key = str(threshold)
                samples_thresholds[key].append(
                    sum(item["within_threshold"][key] for item in chosen) /
                    max(1, visible_n)
                )
        threshold_stats = {}
        total_relations = sum(item["total"] for item in values)
        for threshold in thresholds:
            key = str(threshold)
            estimate = sum(item["within_threshold"][key] for item in values) / max(1, total_relations)
            threshold_stats[key] = {
                "relation_count_within_distance": sum(item["within_threshold"][key] for item in values),
                "rate": estimate,
                "ci95": [float(np.nanquantile(samples_thresholds[key], 0.025)),
                         float(np.nanquantile(samples_thresholds[key], 0.975))],
            }
        group_stats[predicate] = {
            "relation_count": sum(item["total"] for item in values),
            "relations_with_any_available_joint_group": sum(item["n"] for item in values),
            "relations_with_routed_joint_available": sum(item["routed_available"] for item in values),
            "relations_with_visible_routed_joint": sum(item["visible"] for item in values),
            "routed_joint_visibility_rate": point_visible,
            "routed_joint_visibility_rate_ci95": [
                float(np.nanquantile(samples_visible, 0.025)),
                float(np.nanquantile(samples_visible, 0.975)),
            ],
            "routed_part_group_nearest_among_available": point_nearest,
            "routed_part_group_fractional_score_sum": sum(item["nearest"] for item in values),
            "routed_part_group_nearest_inclusive_count": int(sum(item["inclusive"] for item in values)),
            "routed_part_group_nearest_inclusive_rate": sum(item["inclusive"] for item in values) /
            max(1, sum(item["n"] for item in values)),
            "routed_part_group_unique_nearest_count": int(sum(item["unique"] for item in values)),
            "routed_part_group_unique_nearest_rate": sum(item["unique"] for item in values) /
            max(1, sum(item["n"] for item in values)),
            "relations_with_tied_nearest_groups": sum(item["ties"] for item in values),
            "nearest_metric": "fractional credit 1 / number of tied nearest groups; missing routed group scores zero",
            "routed_part_group_nearest_ci95": [
                float(np.nanquantile(samples_nearest, 0.025)),
                float(np.nanquantile(samples_nearest, 0.975)),
            ],
            "routed_joint_proximity_thresholds_object_diagonals": threshold_stats,
        }
    return group_stats


def shuffled_route_baseline(relation_rows, config):
    predicates = sorted({row["predicate"] for row in relation_rows})
    if not predicates:
        return {"eligible_relations": 0, "observed_rate": None, "shuffled_rate_mean": None,
                "shuffled_rate_ci95": [None, None], "upper_tail_probability": None}
    rng = np.random.default_rng(config["bootstrap_seed"] + 1)
    group_names = list(config["keypoint_groups"])
    repetitions = config["bootstrap_repetitions"]
    observations = []
    for row in relation_rows:
        distances = row["all_group_nearest_distance_object_diagonals"]
        available = [(name, value) for name, value in distances.items() if value is not None]
        if not available:
            continue
        observations.append({"predicate": row["predicate"], "distances": distances,
                             "visible_group_count": len(available)})
    if not observations:
        return {"eligible_relations": 0, "observed_rate": None, "shuffled_rate_mean": None,
                "shuffled_rate_ci95": [None, None], "upper_tail_probability": None}
    lookup = np.asarray([[route_scores(item["distances"], group)[metric]
                          for metric in ("fractional", "inclusive", "unique")]
                         for item in observations for group in group_names], dtype=np.float64)
    lookup = lookup.reshape(len(observations), len(group_names), 3)
    predicate_indices = np.asarray([predicates.index(item["predicate"]) for item in observations])
    observed_routes = np.asarray([group_names.index(config["predicate_part_routes"][predicate])
                                  for predicate in predicates], dtype=np.int64)
    observed = lookup[np.arange(len(observations)), observed_routes[predicate_indices]].mean(axis=0)
    shuffled_rates = []
    marginal_preserving_rates = []
    for _ in range(repetitions):
        routes = rng.integers(0, len(group_names), size=len(predicates))
        shuffled_rates.append(lookup[np.arange(len(observations)), routes[predicate_indices]].mean(axis=0))
        permuted_routes = rng.permutation(observed_routes)
        marginal_preserving_rates.append(
            lookup[np.arange(len(observations)), permuted_routes[predicate_indices]].mean(axis=0))
    values = np.asarray(shuffled_rates, dtype=np.float64)
    fixed_marginal_values = np.asarray(marginal_preserving_rates, dtype=np.float64)
    per_metric = {}
    for metric_index, metric in enumerate(("fractional", "inclusive", "unique")):
        per_metric[metric] = {
            "observed": float(observed[metric_index]),
            "uniform_predicate_route_mean": float(values[:, metric_index].mean()),
            "uniform_predicate_route_ci95": [float(np.quantile(values[:, metric_index], 0.025)),
                                               float(np.quantile(values[:, metric_index], 0.975))],
            "uniform_route_upper_tail_probability": float(
                (1 + np.count_nonzero(values[:, metric_index] >= observed[metric_index])) / (repetitions + 1)),
            "route_marginal_preserving_mean": float(fixed_marginal_values[:, metric_index].mean()),
            "route_marginal_preserving_ci95": [float(np.quantile(fixed_marginal_values[:, metric_index], 0.025)),
                                                float(np.quantile(fixed_marginal_values[:, metric_index], 0.975))],
            "marginal_preserving_upper_tail_probability": float(
                (1 + np.count_nonzero(fixed_marginal_values[:, metric_index] >= observed[metric_index])) /
                (repetitions + 1))}
    return {
        "eligible_relations": len(observations),
        "observed_predicate_routed_group_nearest_rate": float(observed[0]),
        "shuffled_route_mean": float(values[:, 0].mean()),
        "shuffled_route_ci95": per_metric["fractional"]["uniform_predicate_route_ci95"],
        "upper_tail_probability": per_metric["fractional"]["uniform_route_upper_tail_probability"],
        "metric": "fractional credit over all groups tied at the shortest distance",
        "metrics": per_metric,
        "permutation_repetitions": repetitions,
        "null_definition": "One random keypoint-group assignment per predicate, shared by all its relations; groups sampled uniformly.",
        "interpretation_limit": "Both nulls are descriptive only. The second preserves route-group counts across predicate mappings, not relation-frequency weighted counts. Group point counts and visibility are controlled only in the complete two-point-group comparison.",
    }


def paired_nearest_comparison(relation_rows, config):
    by_image = defaultdict(list)
    for row in relation_rows:
        gt_available = any(distance is not None
                           for distance in row["all_group_nearest_distance_object_diagonals"].values())
        predicted_available = any(distance is not None
                                  for distance in row["predicted_all_group_nearest_distance_object_diagonals"].values())
        if gt_available and predicted_available:
            by_image[row["coco_image_id"]].append(row)
    image_keys = sorted(by_image)
    if not image_keys:
        return {"eligible_images": 0, "eligible_relations": 0}

    gt_routed_available = sum(row["routed_visible_joint_count"] > 0 for rows in by_image.values() for row in rows)
    predicted_routed_available = sum(row["predicted_routed_visible_joint_count"] > 0
                                     for rows in by_image.values() for row in rows)
    relation_count = sum(len(rows) for rows in by_image.values())
    rng = np.random.default_rng(config["bootstrap_seed"] + 2)
    sampled = rng.integers(0, len(image_keys), size=(config["bootstrap_repetitions"], len(image_keys)))
    metric_results = {}
    for metric in ("fractional", "inclusive", "unique"):
        gt_count = sum(row[f"routed_{metric}"] for rows in by_image.values() for row in rows)
        predicted_count = sum(row[f"predicted_routed_{metric}"] for rows in by_image.values() for row in rows)
        differences = []
        for indices in sampled:
            selected = [by_image[image_keys[index]] for index in indices]
            count = sum(len(rows) for rows in selected)
            gt_hits = sum(row[f"routed_{metric}"] for rows in selected for row in rows)
            predicted_hits = sum(row[f"predicted_routed_{metric}"] for rows in selected for row in rows)
            differences.append((predicted_hits - gt_hits) / count if count else math.nan)
        metric_results[metric] = {
            "ground_truth_score_sum": gt_count, "predicted_score_sum": predicted_count,
            "ground_truth_rate": gt_count / relation_count,
            "predicted_rate": predicted_count / relation_count,
            "predicted_minus_ground_truth_rate": (predicted_count - gt_count) / relation_count,
            "paired_difference_ci95": [float(np.nanquantile(differences, 0.025)),
                                        float(np.nanquantile(differences, 0.975))],
            "ground_truth_only_positive_count": sum(
                row[f"routed_{metric}"] > 0 and row[f"predicted_routed_{metric}"] == 0
                for rows in by_image.values() for row in rows),
            "predicted_only_positive_count": sum(
                row[f"predicted_routed_{metric}"] > 0 and row[f"routed_{metric}"] == 0
                for rows in by_image.values() for row in rows)}
    fractional = metric_results["fractional"]
    return {
        "eligible_images": len(image_keys),
        "eligible_relations": relation_count,
        "metric": "fractional credit among tied nearest groups",
        "metrics": metric_results,
        "ground_truth_keypoint_nearest_score_sum": fractional["ground_truth_score_sum"],
        "ground_truth_keypoint_nearest_rate": fractional["ground_truth_rate"],
        "ground_truth_routed_group_available_count": gt_routed_available,
        "ground_truth_routed_group_available_rate": gt_routed_available / relation_count,
        "predicted_keypoint_nearest_score_sum": fractional["predicted_score_sum"],
        "predicted_keypoint_nearest_rate": fractional["predicted_rate"],
        "predicted_routed_group_available_count": predicted_routed_available,
        "predicted_routed_group_available_rate": predicted_routed_available / relation_count,
        "predicted_minus_ground_truth_rate": fractional["predicted_minus_ground_truth_rate"],
        "paired_difference_ci95": fractional["paired_difference_ci95"],
        "bootstrap_unit": "source image",
        "bootstrap_repetitions": config["bootstrap_repetitions"],
    }


def controlled_support_rows(rows, config, require_complete_two_point_groups):
    group_ids = BALANCED_GROUPS if require_complete_two_point_groups else config["keypoint_groups"]
    result = []
    for row in rows:
        gt_points = row["visible_joint_distances_object_diagonals"]
        predicted_points = row["predicted_joint_distances_object_diagonals"]
        common_ids = set(gt_points) & set(predicted_points)
        if require_complete_two_point_groups and not all(
                str(joint_id) in common_ids for joint_ids in group_ids.values() for joint_id in joint_ids):
            continue
        gt_distances, predicted_distances, point_counts = {}, {}, {}
        for group, joint_ids in group_ids.items():
            selected = [str(joint_id) for joint_id in joint_ids if str(joint_id) in common_ids]
            point_counts[group] = len(selected)
            gt_distances[group] = min((gt_points[joint_id] for joint_id in selected), default=None)
            predicted_distances[group] = min((predicted_points[joint_id] for joint_id in selected), default=None)
        if not any(value is not None for value in gt_distances.values()):
            continue
        copied = dict(row)
        copied["all_group_nearest_distance_object_diagonals"] = gt_distances
        copied["predicted_all_group_nearest_distance_object_diagonals"] = predicted_distances
        copied["routed_visible_joint_count"] = point_counts[row["routed_part_group"]]
        copied["predicted_routed_visible_joint_count"] = point_counts[row["routed_part_group"]]
        copied["routed_nearest_distance_object_diagonals"] = gt_distances[row["routed_part_group"]]
        copied["predicted_routed_nearest_distance_object_diagonals"] = predicted_distances[row["routed_part_group"]]
        copied["routed_nearest_distance_pixels"] = (
            copied["routed_nearest_distance_object_diagonals"] * row["object_box_diagonal_pixels"]
            if copied["routed_nearest_distance_object_diagonals"] is not None else None)
        copied["all_group_visible_joint_counts"] = point_counts
        copied["predicted_all_group_visible_joint_counts"] = point_counts
        result.append(apply_route_scores(copied))
    return result


def availability_summary(rows):
    result = {}
    for prefix, group_field in (("routed", "all_group_visible_joint_counts"),
                                 ("predicted_routed", "predicted_all_group_visible_joint_counts")):
        eligible = [row for row in rows if row[f"{prefix}_available_group_count"] > 0]
        result[prefix] = {
            "relations_with_any_group": len(eligible),
            "nearest_tie_count": sum(row[f"{prefix}_nearest_group_count"] > 1 for row in eligible),
            "mean_available_groups": float(np.mean([row[f"{prefix}_available_group_count"]
                                                     for row in eligible])) if eligible else None,
            "per_group": {group: {
                "available_relations": sum(row[group_field][group] > 0 for row in rows),
                "minimum_available_points": min((row[group_field][group] for row in rows), default=None),
                "maximum_available_points": max((row[group_field][group] for row in rows), default=None),
                "mean_available_points": float(np.mean([row[group_field][group] for row in rows]))
                if rows else None} for group in PART_GROUPS}}
    return result


def controlled_analysis(rows, config, complete):
    controlled = controlled_support_rows(rows, config, complete)
    return {"definition": "six disjoint groups with exactly two identical visible joint IDs per side"
            if complete else "identical visible joint ID support in ground truth and prediction; original overlapping groups",
            "eligible_relations": len(controlled),
            "eligible_source_images": len({row["coco_image_id"] for row in controlled}),
            "paired_comparison": paired_nearest_comparison(controlled, config),
            "shuffled_route_baseline": shuffled_route_baseline(controlled, config),
            "availability": availability_summary(controlled)}, controlled


def verify_analysis_rows(rows):
    for row in rows:
        route = row["routed_part_group"]
        for prefix, field in (("routed", "all_group_nearest_distance_object_diagonals"),
                               ("predicted_routed", "predicted_all_group_nearest_distance_object_diagonals")):
            distances = row[field]
            scores = route_scores(distances, route)
            reversed_scores = route_scores(dict(reversed(list(distances.items()))), route)
            if scores != reversed_scores:
                raise ValueError("Nearest-group scores depend on group insertion order")
            if not 0 <= scores["unique"] <= scores["fractional"] <= scores["inclusive"] <= 1:
                raise ValueError("Nearest-group credit violates score bounds")
            total_credit = sum(route_scores(distances, group)["fractional"] for group in PART_GROUPS)
            expected = float(any(value is not None for value in distances.values()))
            if not math.isclose(total_credit, expected, abs_tol=1e-12):
                raise ValueError("Fractional nearest-group credits do not sum to one")
            if (row[f"{prefix}_group_rank_by_object_box_distance"] == 1) != bool(scores["inclusive"]):
                raise ValueError("Rank-one and inclusive nearest indicators disagree")


def build_report(payload, detector_metrics, config):
    summary = payload["data_and_method_summary"]
    gt = payload["ground_truth_keypoint_proxy_statistics"]
    predicted = payload["predicted_keypoint_proxy_statistics"]
    raw_pair = payload["paired_ground_truth_vs_prediction_nearest_comparison"]
    raw_random = payload["shuffled_predicate_to_part_baseline"]
    common = payload["common_joint_support_control"]
    balanced = payload["complete_balanced_two_point_group_control"]
    labels = {"hands": "手部", "forearms": "前臂", "shoulders": "肩部", "hips": "髋部",
              "legs": "腿部", "feet": "足部"}
    lines = ["# COCO关键点部位邻近代理实验", "", "## 研究问题", "",
             "本实验检查固定谓词到身体部位组的映射，与人物关键点到对象GT边界框的二维距离之间是否有关，并比较COCO标注关键点与预训练模型预测关键点。GT（Ground Truth）在此指数据集标注，GT边界框指数据集标注的矩形对象区域。评价对象是二维邻近代理，COCO关键点没有标注人与该对象的真实接触、对象表面区域或关系真假。", "",
             "谓词路由在实验前固定：`holding`、`carrying`对应手部；`sitting on`、`riding`对应髋部；`standing on`、`walking on`、`running on`、`kicking`对应足部；`leaning on`对应前臂。该映射是待检验的语义假设。", "",
             "## 数据和关键点预测", "",
             f"HOR的500条固定随机记录映射到499个不同COCO源图像身份。COCO ID `404484`有两条相同像素的PSG记录，本部位分析保留原样本顺序中的第一条，分析499个源图像。现有PSG标注文件保持原样。全部{summary['geometry_compatible_images']}个源图像通过2%宽高比误差限制，其中{summary['images_with_coco_person_keypoint_annotations']}个有至少一项COCO人物关键点标注。", "",
             f"{summary['psg_person_boxes']:,}个PSG人物GT边界框中，{summary['matched_psg_person_boxes']}个与COCO人物标注达到IoU≥0.5；本实验随后保留路由表覆盖的{summary['routed_human_object_relations']}条关系。关键点模型在其中{summary['routed_relations_with_matched_predicted_person']}条关系上匹配到人物。匹配采用一对一最大总IoU分配并施加0.5阈值。人物匹配前后、谓词过滤前后的分母分别保存在证据文件中。", "",
             "预测使用官方torchvision Keypoint R-CNN ResNet-50 FPN COCO_V1。每个关键点保存 `[x,y,v]` 和独立的 `keypoints_scores` 字段；部位可用性使用真实 `keypoints_scores≥0.5`。该分数是关键点热图峰值分数，未经概率校准，阈值0.5也不代表50%正确概率。COCO标注侧仅使用 `v=2` 的可见关键点。模型匹配、分数阈值和COCO标注可见性是三种不同条件。", "",
             "## 部位组、距离和并列处理", "",
             "| 部位组 | 原始组关键点 | 每组两个关键点、各组无重叠的对照 |", "|---|---|---|"]
    group_descriptions = {
        "hands": ("左、右腕部（9、10）", "左、右腕部（9、10）"),
        "forearms": ("左、右肘部和腕部（7–10）", "左、右肘部代表点（7、8）"),
        "shoulders": ("左、右肩部（5、6）", "左、右肩部（5、6）"),
        "hips": ("左、右髋部（11、12）", "左、右髋部（11、12）"),
        "legs": ("左、右髋部和膝部（11–14）", "左、右膝部代表点（13、14）"),
        "feet": ("左、右踝部（15、16）", "左、右踝部（15、16）")}
    for group in PART_GROUPS:
        original, control = group_descriptions[group]
        lines.append(f"| {labels[group]} | {original} | {control} |")
    lines.extend(["", "先计算每个可用关键点到对象GT边界框的最短欧氏距离，再以对象GT边界框对角线归一化，部位组取组内最小值。关键点落在对象GT边界框内部时距离为零。原始部位组有2点和4点两种预算，手部属于前臂组、髋部属于腿部组，因此并列具有结构性来源。", "",
                  "所有表格、配对比较和随机路由共享以下定义。距离相差不超过对象GT边界框对角线的`1e-10`视为并列；路由组没有可用点时得分为零。分母包含至少一个部位组可用的关系，只有GT与预测的共同分析使用两侧都可用的共同关系集合。", "",
                  "| 统计量 | 定义 |", "|---|---|",
                  "| 并列分摊得分（主指标） | 路由组处于k个并列最短组时得到1/k，其他情况为零 |",
                  "| 包含并列最短比例 | 路由组属于最短距离集合时得到1 |",
                  "| 唯一最短比例 | 路由组单独具有最短距离时得到1 |",
                  "| 竞争排名 | 1加上严格更近的可用部位组数；并列最短组均排名第一 |", "",
                  "主指标衡量平均分摊后的邻近一致性。它的分子为得分总和，可以是小数，不能写成整数命中数。全部关系都通过了顺序不变性、得分范围、并列分摊总分等于1、竞争排名第一与包含并列最短一致等核验。", "",
                  "## 逐谓词结果", "",
                  "本表分别使用GT和预测侧可用分母；表内分母已经明确列出。95%区间按COCO源图像进行2,000次bootstrap。预测侧对象区域同样使用PSG对象GT边界框。", "",
                  "| 谓词（路由） | 关系数 | GT路由点可用 / 总数 | GT分摊得分总和 / 可用关系数（比例；95%区间） | 预测路由点可用 / 总数 | 预测分摊得分总和 / 可用关系数（比例；95%区间） |", "|---|---:|---:|---|---:|---|"])
    for predicate in sorted(gt):
        a, b = gt[predicate], predicted[predicate]
        a_ci, b_ci = a["routed_part_group_nearest_ci95"], b["routed_part_group_nearest_ci95"]
        route_name = labels[config["predicate_part_routes"][predicate]]
        lines.append(f"| {predicate}（{route_name}） | {a['relation_count']} | "
                     f"{a['relations_with_routed_joint_available']}/{a['relation_count']} | "
                     f"{a['routed_part_group_fractional_score_sum']:.3f}/{a['relations_with_any_available_joint_group']} "
                     f"({a['routed_part_group_nearest_among_available']:.2%}; {a_ci[0]:.2%}, {a_ci[1]:.2%}) | "
                     f"{b['relations_with_routed_joint_available']}/{b['relation_count']} | "
                     f"{b['routed_part_group_fractional_score_sum']:.3f}/{b['relations_with_any_available_joint_group']} "
                     f"({b['routed_part_group_nearest_among_available']:.2%}; {b_ci[0]:.2%}, {b_ci[1]:.2%}) |")
    lines.extend(["", "| 谓词 | GT包含并列最短 / 唯一最短 | 预测包含并列最短 / 唯一最短 |", "|---|---:|---:|"])
    for predicate in sorted(gt):
        a, b = gt[predicate], predicted[predicate]
        lines.append(f"| {predicate} | {a['routed_part_group_nearest_inclusive_rate']:.2%} / "
                     f"{a['routed_part_group_unique_nearest_rate']:.2%} | "
                     f"{b['routed_part_group_nearest_inclusive_rate']:.2%} / "
                     f"{b['routed_part_group_unique_nearest_rate']:.2%} |")
    lines.extend(["", "![GT和预测关键点的路由点可用率及并列分摊邻近得分](part_keypoint_proximity_proxy.png)", "",
                  "## 共同关系上的配对比较", "",
                  "下面三组对照均使用同一条关系、同一对象GT边界框、同一谓词路由和按源图像配对重抽样。原始组允许两侧有不同的可用关键点；共同关键点对照只保留两侧均可用的同一个关键点编号；每组两个关键点的共同可用对照要求六个无重叠部位组的12个关键点在两侧全部可用，每组恰好两个关键点。这项对照同时固定可用组数量和关键点数量，分析集合因此更小。", "",
                  "| 对照 | 共同关系 / 源图像 | GT分摊得分 | 预测分摊得分 | 预测−GT（百分点；95%区间） | GT / 预测路由组可用 |", "|---|---:|---:|---:|---:|---:|"])
    comparisons = [("原始分组与各自关键点", raw_pair),
                   ("原始分组、共同关键点支持", common["paired_comparison"]),
                   ("六组各两个关键点、全部共同可用", balanced["paired_comparison"])]
    for title, comparison in comparisons:
        value = comparison["metrics"]["fractional"]
        ci = value["paired_difference_ci95"]
        lines.append(f"| {title} | {comparison['eligible_relations']} / {comparison['eligible_images']} | "
                     f"{value['ground_truth_rate']:.2%} | {value['predicted_rate']:.2%} | "
                     f"{100 * value['predicted_minus_ground_truth_rate']:+.2f} "
                     f"({100 * ci[0]:+.2f}, {100 * ci[1]:+.2f}) | "
                     f"{comparison['ground_truth_routed_group_available_count']} / "
                     f"{comparison['predicted_routed_group_available_count']} |")
    lines.extend(["", "| 对照与统计定义 | GT比例 | 预测比例 | 预测−GT（百分点；95%区间） |", "|---|---:|---:|---:|"])
    for title, comparison in comparisons:
        for metric, metric_title in (("inclusive", "包含并列最短"), ("unique", "唯一最短")):
            value = comparison["metrics"][metric]
            ci = value["paired_difference_ci95"]
            lines.append(f"| {title}：{metric_title} | {value['ground_truth_rate']:.2%} | "
                         f"{value['predicted_rate']:.2%} | {100 * value['predicted_minus_ground_truth_rate']:+.2f} "
                         f"({100 * ci[0]:+.2f}, {100 * ci[1]:+.2f}) |")
    lines.extend(["", "原始组、共同关键点对照及每组两个关键点的共同可用对照各自规定分析分母，不能把一项对照的点估计与另一项直接相减。配对差值仅在各自的同一关系集合内计算。原始组中两侧关键点可用率不同，可能影响得分；两项共同可用对照用于检查该影响。", "",
                  "## 可用性和并列分布", "",
                  "| 条件 | 至少一组可用关系 | 多组并列最短关系 | 平均可用组数 |", "|---|---:|---:|---:|"])
    for title, availability in (("原始组", payload["availability_and_ties"]),
                                ("共同关键点支持", common["availability"]),
                                ("每组两个关键点且全部共同可用", balanced["availability"])):
        for prefix, side in (("routed", "GT"), ("predicted_routed", "预测")):
            value = availability[prefix]
            lines.append(f"| {title} {side} | {value['relations_with_any_group']} | "
                         f"{value['nearest_tie_count']} | {value['mean_available_groups']:.3f} |")
    lines.extend(["", "各部位组的可用关系数、平均关键点数量和最小/最大关键点数量保存在统计JSON中。原始组包含两个与四个关键点的部位组，两者使用的关键点数量不同；每组两个关键点的共同可用对照固定每组两个关键点，且各组不共享关键点。", "",
                  "## 随机路由对照", "",
                  "所有随机对照与被比较的固定语义路由使用完全相同的关系分母和三种并列计分规则。均匀对照为每个谓词从六个部位组中随机选择一组，在该谓词所有关系上共享；频数固定对照打乱各自分析集合中出现的谓词的既有部位组分配，保留谓词映射层面的组频数。后者没有固定按关系条数加权的路由频数。", "",
                  "| 条件 | 关系数 | 固定语义路由分摊得分 | 均匀随机路由平均（95%范围） | 固定映射组频数平均（95%范围） |", "|---|---:|---:|---:|---:|"])
    for title, random in (("原始组GT", raw_random),
                           ("共同关键点支持GT", common["shuffled_route_baseline"]),
                           ("每组两个关键点且全部共同可用GT", balanced["shuffled_route_baseline"])):
        value = random["metrics"]["fractional"]
        ci, marginal_ci = value["uniform_predicate_route_ci95"], value["route_marginal_preserving_ci95"]
        lines.append(f"| {title} | {random['eligible_relations']} | {value['observed']:.2%} | "
                     f"{value['uniform_predicate_route_mean']:.2%} ({ci[0]:.2%}, {ci[1]:.2%}) | "
                     f"{value['route_marginal_preserving_mean']:.2%} "
                     f"({marginal_ci[0]:.2%}, {marginal_ci[1]:.2%}) |")
    lines.extend(["", "| 原始组GT计分定义 | 固定语义路由 | 均匀随机路由平均 |", "|---|---:|---:|"])
    for metric, title in (("fractional", "并列分摊"), ("inclusive", "包含并列最短"), ("unique", "唯一最短")):
        value = raw_random["metrics"][metric]
        lines.append(f"| {title} | {value['observed']:.2%} | {value['uniform_predicate_route_mean']:.2%} |")
    lines.extend(["", "随机分配的范围来自2,000次路由抽样，反映该随机机制的变化，不能与图像bootstrap置信区间混用。原始组受到关键点数量、分组重叠和可用性影响；每组两个关键点的共同可用对照在全部12个关键点共同可用的子集上控制这些因素。结果描述的是当前手工路由与边界框几何代理的关联，不能作为关系视觉真实性或独立接触标注准确率。", "",
                  "## 关键点检测器核验与运行", "",
                  f"在499个映射COCO val2017源图像上的关键点评测：AP={detector_metrics['metrics']['AP']:.4f}，AP50={detector_metrics['metrics']['AP50']:.4f}，AP75={detector_metrics['metrics']['AP75']:.4f}，AR={detector_metrics['metrics']['AR']:.4f}。该评测确认输出能够按COCO协议计算，属于COCO数据域检查。", "",
                  f"权重SHA256为`{detector_metrics['checkpoint_sha256']}`。GPU推理耗时{detector_metrics['inference_seconds']:.2f}秒，500条记录全部处理耗时{detector_metrics['elapsed_seconds']:.2f}秒，平均每张图像推理耗时{detector_metrics['mean_seconds_per_image']:.4f}秒，PyTorch峰值已分配显存{detector_metrics['peak_torch_cuda_memory_bytes']:,}字节。每张图像的GPU预测保留独立关键点分数字段；后续统计在CPU运行。", "",
                  "## 证据和适用范围", "",
                  "逐关系的人物与对象GT边界框端点、关键点编号距离、可用关键点数量、三种并列得分、对象类别与人物匹配IoU见[原始组关系证据](evidence/relation_part_proximity.csv)。[共同关键点支持证据](evidence/common_joint_support_relations.csv)和[每组两个关键点的共同可用证据](evidence/balanced_two_point_group_relations.csv)保留两项公平对照的完整关系。统计定义、配对差值、随机路由结果及各组关键点数量见[部位统计JSON](evidence/part_evidence_summary.json)。", "",
                  "[图像匹配汇总](evidence/image_matching_summary.csv)、[VG/COCO映射](evidence/vg_coco_image_mapping.csv)、[关键点COCO指标](evidence/keypoint_coco_metrics.json)与[缩放映射](evidence/keypoint_image_mappings.json)提供样本与模型来源。原始图像、COCO标注、模型权重和各张图像的预测保存在Git忽略目录，已有人工审计表不参与这些代理统计。", "",
                  "这些实验只检验二维关键点与对象GT边界框的邻近关系。对象矩形内部出现距离零，不能说明该点接触真实对象表面。手腕、肘部、踝部和膝部是人体部位的代表点，不能表达手指接触或对象功能区域。`kicking`仅2条、`leaning on`仅4条，不能用其点估计选择研究方向。指南所需的独立部位标注参考实验和真实候选准确性实验仍需部位—对象区域、可见性和视觉支持的独立人工标注。", "",
                  "## 复现", "",
                  "```powershell", ".\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\predict_coco_keypoints.py",
                  ".\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\part_evidence_study.py", "```", "",
                  "[模型配置](../../configs/keypoint_prediction.json)与[路由和统计配置](../../configs/part_evidence.json)固定权重、关键点分数阈值、路由和随机种子。", ""])
    return "\n".join(lines)


def main():
    config = read_json(CONFIG_PATH)
    records = read_records(ROOT / config["input_predictions"])
    predicted_records = read_records(ROOT / config["predicted_keypoints"])
    if len(predicted_records) != len(records):
        raise ValueError(f"Expected one keypoint prediction row per sample: {len(predicted_records)} != {len(records)}")
    record_files = {record["file_name"] for record in records}
    predicted_files = {record["file_name"] for record in predicted_records}
    if predicted_files != record_files:
        raise ValueError("Keypoint prediction filenames do not match the fixed sample")
    predicted_people_by_file = {record["file_name"]: record["people"]
                                for record in predicted_records}
    for record in predicted_records:
        for person in record["people"]:
            if len(person["keypoints_scores"]) != len(JOINT_NAMES):
                raise ValueError(f"Missing 17 genuine keypoint scores for {record['file_name']}")
    metadata = read_json(ROOT / config["visual_genome_image_metadata"])
    vg_metadata = {int(item["image_id"]): item for item in metadata}
    coco_images = {}
    coco_people = defaultdict(list)
    annotation_dir = ROOT / config["coco_keypoint_annotations"]
    for split in ("train", "val"):
        data = read_json(annotation_dir / f"person_keypoints_{split}2017.json")
        for image in data["images"]:
            coco_images[int(image["id"])] = {**image, "split": split}
        for annotation in data["annotations"]:
            if annotation["num_keypoints"] > 0:
                coco_people[int(annotation["image_id"])].append(annotation)

    relation_results, image_results, map_rows, summary = relation_rows(
        records, vg_metadata, coco_images, coco_people, predicted_people_by_file, config
    )
    summary["aspect_ratio_error_limit"] = config["max_aspect_ratio_error"]
    summary["minimum_person_box_iou"] = config["iou_threshold"]
    summary["keypoint_score_field"] = "keypoints_scores (raw heatmap peak score)"
    summary["keypoint_score_threshold"] = config["keypoint_confidence_threshold"]
    summary["keypoint_score_is_calibrated_probability"] = False
    summary["mapped_images_by_keypoint_split"] = {
        split: sum(row["coco_split"] == split for row in map_rows) for split in ("train", "val")
    }
    grouped = bootstrap_statistics(relation_results, config)
    predicted_grouped = bootstrap_statistics(relation_results, config, prefix="predicted_routed")
    paired = paired_nearest_comparison(relation_results, config)
    shuffled = shuffled_route_baseline(relation_results, config)
    common_support, common_rows = controlled_analysis(relation_results, config, False)
    balanced_support, balanced_rows = controlled_analysis(relation_results, config, True)
    verify_analysis_rows(relation_results)
    verify_analysis_rows(common_rows)
    verify_analysis_rows(balanced_rows)
    gt_any_count = sum(item["relations_with_any_available_joint_group"] for item in grouped.values())
    gt_credit_sum = sum(item["routed_part_group_fractional_score_sum"] for item in grouped.values())
    if not math.isclose(gt_credit_sum / gt_any_count,
                        shuffled["observed_predicate_routed_group_nearest_rate"], abs_tol=1e-12):
        raise ValueError("Per-predicate fractional credit and random-baseline observed credit disagree")
    output_dir = ROOT / config["output_directory"]
    report_dir = ROOT / config["report_directory"]
    evidence_dir = report_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    mapping_fields = ["vg_image_id", "coco_image_id", "coco_split", "local_width", "local_height",
                      "coco_width", "coco_height", "aspect_ratio_error", "keypoint_annotations", "status"]
    image_fields = ["index", "file_name", "coco_id", "status", "aspect_ratio_error",
                    "psg_person_count", "matched_psg_person_count", "coco_keypoint_person_count",
                    "routed_relation_count"]
    relation_fields = list(relation_results[0])
    write_csv(output_dir / "vg_coco_image_mapping.csv", map_rows, mapping_fields)
    write_csv(evidence_dir / "vg_coco_image_mapping.csv", map_rows, mapping_fields)
    write_csv(output_dir / "image_matching_summary.csv", image_results, image_fields)
    write_csv(evidence_dir / "image_matching_summary.csv", image_results, image_fields)
    write_csv(output_dir / "relation_part_proximity.csv", relation_results, relation_fields)
    write_csv(evidence_dir / "relation_part_proximity.csv", relation_results, relation_fields)
    write_csv(output_dir / "common_joint_support_relations.csv", common_rows, relation_fields)
    write_csv(evidence_dir / "common_joint_support_relations.csv", common_rows, relation_fields)
    write_csv(output_dir / "balanced_two_point_group_relations.csv", balanced_rows, relation_fields)
    write_csv(evidence_dir / "balanced_two_point_group_relations.csv", balanced_rows, relation_fields)
    summary_payload = {
        "data_and_method_summary": summary,
        "ground_truth_keypoint_proxy_statistics": grouped,
        "predicted_keypoint_proxy_statistics": predicted_grouped,
        "paired_ground_truth_vs_prediction_nearest_comparison": paired,
        "shuffled_predicate_to_part_baseline": shuffled,
        "common_joint_support_control": common_support,
        "complete_balanced_two_point_group_control": balanced_support,
        "availability_and_ties": availability_summary(relation_results),
        "metric_protocol": {
            "primary": "fractional credit: 1/k when the routed group is in k tied nearest groups; 0 otherwise",
            "secondary_inclusive": "binary credit if routed group is among all tied minima",
            "secondary_unique": "binary credit only if routed group is the unique nearest group",
            "rank": "competition rank 1 + number of strictly closer available groups; tied minima all rank one",
            "tie_absolute_tolerance_object_diagonals": 1e-10,
            "ground_truth_visibility": "COCO keypoint v=2",
            "prediction_availability": "keypoints_scores >= fixed threshold; keypoints third dimension retains visibility",
            "random_null": "same fractional/inclusive/unique definitions and same eligible relations as observed",
            "verified_on_actual_relations": "group order invariant; score bounds; nearest credits sum to one; rank-one equals inclusive minimum; aggregate/per-predicate scores agree"},
        "interpretation": "Descriptive keypoint-to-box proximity proxies only; COCO labels are an oracle-like geometry reference and model outputs are predictions. Neither is contact truth, an independent human audit, or a validated relation verifier.",
    }
    write_json(output_dir / "part_evidence_summary.json", summary_payload)
    write_json(evidence_dir / "part_evidence_summary.json", summary_payload)

    names = sorted(set(grouped) | set(predicted_grouped))
    counts = [grouped.get(name, predicted_grouped.get(name, {})).get("relation_count", 0)
              for name in names]
    figure, axes = plt.subplots(2, 1, figsize=(12, 9), layout="constrained", sharex=True)
    positions = np.arange(len(names))
    width = 0.2
    gt_visibility = [100 * grouped.get(name, {}).get("routed_joint_visibility_rate", 0.0)
                     for name in names]
    predicted_visibility = [100 * predicted_grouped.get(name, {}).get("routed_joint_visibility_rate", 0.0)
                            for name in names]
    gt_nearest = [100 * grouped.get(name, {}).get("routed_part_group_nearest_among_available", 0.0)
                  for name in names]
    predicted_nearest = [100 * predicted_grouped.get(name, {}).get("routed_part_group_nearest_among_available", 0.0)
                         for name in names]
    axes[0].bar(positions - width / 2, gt_visibility, width=width,
                color="#3478a8", label="COCO GT keypoint visibility")
    axes[0].bar(positions + width / 2, predicted_visibility, width=width,
                color="#d77a32", label="Predicted keypoint score availability")
    axes[0].set_ylabel("Relations (%)")
    axes[0].set_ylim(0, 100)
    axes[0].set_title("Predicate-routed joint availability")
    axes[0].legend(frameon=False)
    axes[1].bar(positions - width / 2, gt_nearest, width=width,
                color="#3478a8", label="COCO GT: routed group nearest")
    axes[1].bar(positions + width / 2, predicted_nearest, width=width,
                color="#d77a32", label="Prediction: routed group nearest")
    axes[1].set_ylabel("Relations (%)")
    axes[1].set_ylim(0, 100)
    axes[1].set_title("Routed-group nearest credit: fractional allocation over tied groups")
    axes[1].legend(frameon=False)
    axes[1].set_xticks(positions, [f"{name}\n(n={count})" for name, count in zip(names, counts)])
    for axis in axes:
        axis.grid(axis="y", color="#d9dde2", linewidth=0.7)
        axis.set_axisbelow(True)
    figure.savefig(report_dir / "part_keypoint_proximity_proxy.png", dpi=180)
    plt.close(figure)
    keypoint_metrics = read_json(evidence_dir / "keypoint_coco_metrics.json")
    report = build_report(summary_payload, keypoint_metrics, config)
    (report_dir / "关键点部位邻近代理实验.md").write_text(report, encoding="utf-8")

    print(json.dumps({"summary": summary,
                      "ground_truth_keypoint_proxy_statistics": grouped,
                      "predicted_keypoint_proxy_statistics": predicted_grouped,
                      "paired_ground_truth_vs_prediction_nearest_comparison": paired,
                      "shuffled_predicate_to_part_baseline": shuffled,
                      "common_joint_support_control": common_support,
                      "complete_balanced_two_point_group_control": balanced_support,
                      "outputs": str(output_dir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
