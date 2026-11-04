import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

import numpy as np
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / "HOR/research/reports/parts"
EVIDENCE = REPORT / "evidence"
OUTPUT = ROOT / "HOR/research/output/parts"
BALANCED = {"hands": [9, 10], "forearms": [7, 8], "shoulders": [5, 6],
            "hips": [11, 12], "legs": [13, 14], "feet": [15, 16]}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_rows(name):
    with (EVIDENCE / name).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for name, value in row.items():
            if name.endswith("_xyxy") or "distances_object_diagonals" in name or name.endswith("joint_counts") or name in (
                    "all_group_nearest_distance_object_diagonals",
                    "predicted_all_group_nearest_distance_object_diagonals"):
                row[name] = json.loads(value)
    return rows


def relation_key(row):
    return tuple(row[name] for name in ("index", "person_id", "person_role", "object_id", "predicate"))


def recompute(row, prefix):
    field = ("all_group_nearest_distance_object_diagonals" if prefix == "routed"
             else "predicted_all_group_nearest_distance_object_diagonals")
    values = row[field]
    available = {group: value for group, value in values.items() if value is not None}
    score = np.zeros(3, dtype=np.float64)
    if available:
        minimum = np.min(list(available.values()))
        nearest = [group for group, value in available.items() if abs(value - minimum) <= 1e-10]
        if row["routed_part_group"] in nearest:
            score[:] = [1 / len(nearest), 1.0, float(len(nearest) == 1)]
    for metric, value in zip(("fractional", "inclusive", "unique"), score):
        require(math.isclose(value, float(row[f"{prefix}_{metric}"]), abs_tol=1e-12),
                f"Incorrect {prefix} {metric} score for relation {relation_key(row)}")
    return score, bool(available)


def verify_groups(row, source, groups, common_only):
    ground_truth = source["visible_joint_distances_object_diagonals"]
    predicted = source["predicted_joint_distances_object_diagonals"]
    common = ground_truth.keys() & predicted.keys()
    for points, distance_field, count_field in (
            (ground_truth, "all_group_nearest_distance_object_diagonals", "all_group_visible_joint_counts"),
            (predicted, "predicted_all_group_nearest_distance_object_diagonals",
             "predicted_all_group_visible_joint_counts")):
        for group, ids in groups.items():
            selected_ids = [str(joint_id) for joint_id in ids
                            if str(joint_id) in (common if common_only else points.keys())]
            expected = min((points[joint_id] for joint_id in selected_ids), default=None)
            actual = row[distance_field][group]
            valid_distance = (actual is None if expected is None
                              else actual is not None and math.isclose(actual, expected, abs_tol=1e-12))
            require(valid_distance, f"Incorrect {group} minimum distance for relation {relation_key(row)}")
            require(row[count_field][group] == len(selected_ids),
                    f"Incorrect {group} available point count for relation {relation_key(row)}")
    for box_name in ("person_box_xyxy", "object_box_xyxy"):
        require(row[box_name] == source[box_name], f"Changed {box_name} for relation {relation_key(row)}")
    box = row["object_box_xyxy"]
    require(math.isclose(math.hypot(box[2] - box[0], box[3] - box[1]),
                         float(row["object_box_diagonal_pixels"]), abs_tol=1e-10),
            f"Incorrect object box diagonal for relation {relation_key(row)}")


def verify_pair(rows, pair, random_result, config):
    images = defaultdict(list)
    ground_truth_observations = []
    for row in rows:
        ground_truth, ground_truth_available = recompute(row, "routed")
        predicted, predicted_available = recompute(row, "predicted_routed")
        if ground_truth_available:
            ground_truth_observations.append(ground_truth)
        if ground_truth_available and predicted_available:
            images[int(row["coco_image_id"])].append((ground_truth, predicted))
    require(pair["eligible_images"] == len(images), "Incorrect paired source image count")
    require(pair["eligible_relations"] == sum(map(len, images.values())), "Incorrect paired relation count")
    counts = np.asarray([len(images[name]) for name in sorted(images)])
    sums = np.asarray([np.asarray(images[name]).sum(axis=0) for name in sorted(images)])
    means = sums.sum(axis=0) / counts.sum()
    rng = np.random.default_rng(config["bootstrap_seed"] + 2)
    indices = rng.integers(0, len(counts), size=(config["bootstrap_repetitions"], len(counts)))
    samples = sums[indices].sum(axis=1) / counts[indices].sum(axis=1)[:, None, None]
    for index, metric in enumerate(("fractional", "inclusive", "unique")):
        result = pair["metrics"][metric]
        require(math.isclose(means[0, index], result["ground_truth_rate"], abs_tol=1e-12),
                f"Incorrect paired ground truth {metric} rate")
        require(math.isclose(means[1, index], result["predicted_rate"], abs_tol=1e-12),
                f"Incorrect paired predicted {metric} rate")
        interval = np.quantile(samples[:, 1, index] - samples[:, 0, index], [.025, .975])
        require(np.allclose(interval, result["paired_difference_ci95"], atol=1e-12, rtol=0),
                f"Incorrect paired {metric} image-bootstrap interval")
        require(math.isclose(np.mean(ground_truth_observations, axis=0)[index],
                             random_result["metrics"][metric]["observed"], abs_tol=1e-12),
                f"Random-route observed {metric} score differs from relation scores")
    return {"relations": len(rows), "paired_relations": int(counts.sum()), "source_images": len(images)}


def main():
    config = json.loads((ROOT / "HOR/research/configs/part_evidence.json").read_text(encoding="utf-8"))
    summary = json.loads((EVIDENCE / "part_evidence_summary.json").read_text(encoding="utf-8"))
    for path in EVIDENCE.iterdir():
        require(path.is_file(), f"Unexpected evidence directory: {path}")
        require(path.read_bytes() == (OUTPUT / path.name).read_bytes(), f"Evidence copy differs: {path.name}")

    raw = read_rows("relation_part_proximity.csv")
    source = {relation_key(row): row for row in raw}
    require(len(source) == len(raw), "Raw relation evidence contains duplicate identities")
    common = read_rows("common_joint_support_relations.csv")
    balanced = read_rows("balanced_two_point_group_relations.csv")
    expected_common = {relation_key(row) for row in raw if row["visible_joint_distances_object_diagonals"].keys()
                       & row["predicted_joint_distances_object_diagonals"].keys()}
    required = {str(joint_id) for ids in BALANCED.values() for joint_id in ids}
    expected_balanced = {relation_key(row) for row in raw if required <= (
        row["visible_joint_distances_object_diagonals"].keys()
        & row["predicted_joint_distances_object_diagonals"].keys())}
    require({relation_key(row) for row in common} == expected_common and len(common) == len(expected_common),
            "Common-support evidence does not match eligible raw relations")
    require({relation_key(row) for row in balanced} == expected_balanced and len(balanced) == len(expected_balanced),
            "Complete two-point evidence does not match eligible raw relations")
    for rows, groups, common_only in ((raw, config["keypoint_groups"], False),
                                      (common, config["keypoint_groups"], True),
                                      (balanced, BALANCED, True)):
        for row in rows:
            verify_groups(row, source[relation_key(row)], groups, common_only)

    results = {}
    for name, rows, pair, random_result in (
            ("raw", raw, summary["paired_ground_truth_vs_prediction_nearest_comparison"],
             summary["shuffled_predicate_to_part_baseline"]),
            ("common_joint", common, summary["common_joint_support_control"]["paired_comparison"],
             summary["common_joint_support_control"]["shuffled_route_baseline"]),
            ("complete_two_point", balanced, summary["complete_balanced_two_point_group_control"]["paired_comparison"],
             summary["complete_balanced_two_point_group_control"]["shuffled_route_baseline"])):
        results[name] = verify_pair(rows, pair, random_result, config)

    links = []
    document = REPORT / "关键点部位邻近代理实验.md"
    for token in MarkdownIt().parse(document.read_text(encoding="utf-8")):
        for child in token.children or []:
            if child.type in ("link_open", "image"):
                target = child.attrGet("href" if child.type == "link_open" else "src")
                parsed = urlsplit(target)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    local = document.parent / unquote(parsed.path)
                    require(local.exists(), f"Broken local report link: {target}")
                    links.append(target)
    results["verified_local_links"] = len(links)
    results["matching_evidence_copies"] = len(list(EVIDENCE.iterdir()))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
