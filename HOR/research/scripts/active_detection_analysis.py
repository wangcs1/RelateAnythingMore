from collections import Counter, defaultdict
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from active_detection_study import (COMPARISONS, GROUPS, GROUP_LABELS, ROOT, SCOPES,
                                    read_json, read_lines, validate_preparation, write_lines)
from evaluation import endpoint_matches, evaluate
from pipeline import CONFIG, save_json, sha256


def identity_metadata(sources, config):
    data = read_json(ROOT / config["source_identity_metadata"])
    indexed = {row["index"]: row for values in data["splits"].values() for row in values}
    if len(indexed) != len(sources):
        raise ValueError("The source identity metadata must contain exactly the fixed 500 records")
    for row in sources:
        identity = indexed[row["index"]]
        if identity["file_name"] != row["file_name"] or identity["image_sha256"] != row["image_sha256"]:
            raise ValueError(f"Image identity mismatch at {row['index']}")
    if len({row["identity_key"] for row in indexed.values()}) != config["expected_unique_source_identities"]:
        raise ValueError("The fixed sample must retain its 499 independent source identities")
    return indexed


def audit_outputs(sources, predictions, plans, config):
    if [row["index"] for row in predictions] != [row["index"] for row in sources]:
        raise ValueError("Inference must contain all 500 records in the original fixed order")
    counts = Counter()
    exact_baseline = Counter()
    different_baseline = []
    coordinate_tolerance_pixels = 1e-3
    maximum_border_overflow = 0.0
    output_dir = ROOT / config["output_directory"]
    for source, prediction, plan in zip(sources, predictions, plans):
        if prediction["file_name"] != source["file_name"] or prediction["image_sha256"] != source["image_sha256"]:
            raise ValueError(f"Inference source identity mismatch at {source['index']}")
        if sha256(ROOT / config["image_directory"] / source["file_name"]) != source["image_sha256"]:
            raise ValueError(f"Source image bytes changed at {source['index']}")
        if set(prediction["groups"]) != set(GROUPS):
            raise ValueError(f"Incomplete group outputs at {source['index']}")
        if sorted(prediction["execution_order"]) != sorted(GROUPS):
            raise ValueError("All three groups must execute once for every record")
        for group in GROUPS:
            result = prediction["groups"][group]
            objects = result["objects"]
            indexed = {item["id"]: item for item in objects}
            if len(indexed) != len(objects) or len(objects) > 40 or result["candidate_pairs"] > 400 or len(result["relations"]) > 50:
                raise ValueError(f"A fair endpoint, pair, or output budget was violated at {source['index']}/{group}")
            if [item["id"] for item in objects] != list(range(len(objects))):
                raise ValueError("Model endpoint IDs must match their tensor positions")
            for item in objects:
                x1, y1, x2, y2 = item["box_xyxy"]
                width, height = source["image_size"]
                maximum_border_overflow = max(maximum_border_overflow, -x1, -y1, x2 - width, y2 - height)
                if not np.isfinite([x1, y1, x2, y2, item["detection_score"]]).all() or not (
                        -coordinate_tolerance_pixels <= x1 < x2 <= width + coordinate_tolerance_pixels
                        and -coordinate_tolerance_pixels <= y1 < y2 <= height + coordinate_tolerance_pixels):
                    raise ValueError(f"Invalid transformed endpoint at {source['index']}/{group}")
            expected_queries = [] if group == "baseline" else plan["queries"][group]
            if len(result["queries"]) != len(expected_queries):
                raise ValueError(f"Query-count mismatch at {source['index']}/{group}")
            for actual, expected in zip(result["queries"], expected_queries):
                if any(actual[key] != value for key, value in expected.items()):
                    raise ValueError(f"Inference crop differs from the signed plan at {source['index']}/{group}")
                left, top, right, bottom = actual["crop_box_xyxy"]
                if actual["input_pixels"] != (right - left) * (bottom - top) or actual["elapsed_seconds"] <= 0:
                    raise ValueError("Crop area and actual positive inference time must be recorded")
                for item in actual["detections"]:
                    x1, y1, x2, y2 = item["box_xyxy"]
                    if not (left - coordinate_tolerance_pixels <= x1 < x2 <= right + coordinate_tolerance_pixels
                            and top - coordinate_tolerance_pixels <= y1 < y2 <= bottom + coordinate_tolerance_pixels):
                        raise ValueError("A crop detection was not transformed into the original image frame")
                counts[f"{group}_queries"] += 1
            for rank, relation in enumerate(result["relations"], 1):
                if relation["rank"] != rank or relation["subject_id"] == relation["object_id"]:
                    raise ValueError("Invalid ranked relation identity")
                subject, obj = indexed[relation["subject_id"]], indexed[relation["object_id"]]
                if not (subject["is_person"] or obj["is_person"]):
                    raise ValueError("An output relation does not involve any person endpoint")
            pairs = result["all_human_pairs"]
            identities = {(item["subject_id"], item["object_id"]) for item in pairs}
            if len(identities) != len(pairs) or result["human_pairs_scored"] != len(pairs):
                raise ValueError("Duplicate or unaccounted scored human pair")
            array_path = output_dir / "logits" / group / f"{source['index']:04d}.npz"
            if result["candidate_pairs"]:
                with np.load(array_path, allow_pickle=False) as arrays:
                    n = result["candidate_pairs"]
                    sub, obj = arrays["subject_indices"], arrays["object_indices"]
                    logits, pair_logits = arrays["predicate_logits"], arrays["pair_logits"]
                    if sub.shape != (n,) or obj.shape != (n,) or logits.shape != (n, 56) or pair_logits.size != n:
                        raise ValueError(f"Incorrect retained logit dimensions at {source['index']}/{group}")
                    if not np.isfinite(logits).all() or not np.isfinite(pair_logits).all():
                        raise ValueError("Nonfinite retained model logits")
                    if len(set(zip(sub.tolist(), obj.tolist()))) != n or np.any(sub == obj) or np.any(sub >= len(objects)) or np.any(obj >= len(objects)):
                        raise ValueError("Retained candidate-pair tensor identities are invalid")
                    tensor_pairs = set(zip(sub.tolist(), obj.tolist()))
                    if not identities <= tensor_pairs:
                        raise ValueError("Human pair outputs do not belong to retained model logits")
                counts["logit_files_verified"] += 1
            elif array_path.exists():
                raise ValueError("An empty relation forward has an unexpected retained logit file")
            counts[f"{group}_records"] += 1
        baseline = prediction["groups"]["baseline"]
        stripped = [{key: value for key, value in item.items() if key != "source_kind"} for item in baseline["objects"]]
        if stripped != source["baseline_objects"]:
            raise ValueError("The internal baseline endpoints differ from frozen regional group A")
        original = source["guidance_relations"]
        current = baseline["relations"]
        if current == original:
            exact_baseline["complete_top50_equal"] += 1
        original_ids = [(item["subject_id"], item["object_id"], item["predicate_id"]) for item in original]
        current_ids = [(item["subject_id"], item["object_id"], item["predicate_id"]) for item in current]
        if original_ids == current_ids:
            exact_baseline["top50_identities_and_order_equal"] += 1
        else:
            different_baseline.append({"index": source["index"], "frozen_A_top50": original, "active_baseline_top50": current})
    expected = sum(bool(any(item["is_person"] for item in row["baseline_objects"])) for row in sources) * 2
    if any(counts[f"{group}_queries"] != expected for group in GROUPS[1:]):
        raise ValueError("The two active policies did not execute the same fixed query counts")
    return {"passed": True, "records": len(predictions), "source_images_sha256_verified": len(sources),
            "coordinate_tolerance_pixels": coordinate_tolerance_pixels,
            "maximum_retained_detector_border_overflow_pixels": maximum_border_overflow,
            "GT_not_used_in_query_selection": True, "validation_counts": dict(counts),
            "fixed_budgets": {"endpoints": 40, "relation_pairs": 400, "relations": 50,
                              "queries_per_detected_person_record": 2, "queries_without_detected_person": 0},
            "frozen_A_comparison": dict(exact_baseline), "baseline_different_records": different_baseline}


def evaluate_groups(sources, predictions):
    result = {group: {} for group in GROUPS}
    for group in GROUPS:
        for scope in SCOPES:
            rows = [{"index": source["index"], "ground_truth_objects": source["ground_truth_objects"],
                     "ground_truth_relations": source["ground_truth_relations"] if scope == SCOPES[0]
                     else source["fixed_endpoint_valid_relations"], "detected": prediction["groups"][group]}
                    for source, prediction in zip(sources, predictions)]
            result[group][scope] = evaluate(rows, "detected")
    return result


def relation_key(row):
    return row["subject_id"], row["object_id"], row["predicate"]


def bootstrap_comparisons(sources, evaluation, identities, config):
    result = {"method": "paired source-identity cluster bootstrap with replacement; all PSG rows of a sampled identity stay together",
              "seed": config["bootstrap_seed"], "repetitions": config["bootstrap_repetitions"],
              "point_estimate": "PSG-record-weighted image macro R; predicate image macro then predicate macro mR",
              "multiple_comparison_adjustment": "none; exploratory paired comparisons", "scopes": {}}
    source_indexed = {row["index"]: row for row in sources}
    rng = np.random.default_rng(config["bootstrap_seed"])
    for scope in SCOPES:
        per_group = {group: {row["index"]: row for row in evaluation[group][scope]["per_image"]} for group in GROUPS}
        evaluated_indices = sorted(per_group["baseline"])
        identity_keys = sorted({identities[index]["identity_key"] for index in evaluated_indices})
        cluster_id = {key: index for index, key in enumerate(identity_keys)}
        predicates = sorted(evaluation["baseline"][scope]["per_class"], key=int)
        predicate_id = {int(value): index for index, value in enumerate(predicates)}
        shape = (len(identity_keys), len(predicates))
        gt_counts = np.zeros(len(identity_keys))
        record_counts = np.zeros(len(identity_keys))
        predicate_record_counts = np.zeros(shape)
        local = {group: {"r": np.zeros(len(identity_keys)), "hits": np.zeros(len(identity_keys)),
                         "class_r": np.zeros(shape)} for group in GROUPS}
        for index in evaluated_indices:
            cluster = cluster_id[identities[index]["identity_key"]]
            source = source_indexed[index]
            gt = source["ground_truth_relations"] if scope == SCOPES[0] else source["fixed_endpoint_valid_relations"]
            names = {row["predicate"]: row["predicate_id"] for row in gt}
            denominators = Counter(row["predicate_id"] for row in gt)
            gt_counts[cluster] += len(gt)
            record_counts[cluster] += 1
            for predicate in denominators:
                predicate_record_counts[cluster, predicate_id[predicate]] += 1
            for group in GROUPS:
                detail = per_group[group][index]
                local[group]["r"][cluster] += detail["R@50"]
                local[group]["hits"][cluster] += detail["hits50"]
                hit_classes = Counter(names[row["predicate"]] for row in detail["diagnostics"] if row["stage"] == "hit50")
                for predicate, denominator in denominators.items():
                    local[group]["class_r"][cluster, predicate_id[predicate]] += hit_classes[predicate] / denominator
        weights = rng.multinomial(len(identity_keys), np.full(len(identity_keys), 1 / len(identity_keys)),
                                  size=config["bootstrap_repetitions"]).astype(np.float64)
        record_denominator = weights @ record_counts
        gt_denominator = weights @ gt_counts
        class_denominator = weights @ predicate_record_counts
        distributions = {}
        for group in GROUPS:
            class_numerator = weights @ local[group]["class_r"]
            class_scores = np.divide(class_numerator, class_denominator,
                                     out=np.zeros_like(class_numerator), where=class_denominator > 0)
            distributions[group] = {"R@50": (weights @ local[group]["r"]) / record_denominator,
                                    "pooled_R@50": (weights @ local[group]["hits"]) / gt_denominator,
                                    "mR@50": class_scores.sum(axis=1) / (class_denominator > 0).sum(axis=1)}
            point_mr = np.mean(local[group]["class_r"].sum(axis=0) / predicate_record_counts.sum(axis=0))
            if not np.isclose(point_mr, evaluation[group][scope]["metrics"]["mR@50"], rtol=0, atol=1e-12):
                raise ValueError("The bootstrap mR point estimate differs from the production evaluator")
        comparisons = {}
        for new, old in COMPARISONS:
            comparison = {}
            for metric in ("R@50", "mR@50", "pooled_R@50"):
                differences = distributions[new][metric] - distributions[old][metric]
                point = evaluation[new][scope]["metrics"][metric] - evaluation[old][scope]["metrics"][metric]
                bounds = np.quantile(differences, [0.025, 0.975]).tolist()
                comparison[metric] = {"point_difference": point, "percentile_95_CI": bounds,
                                      "CI_excludes_zero": bounds[0] > 0 or bounds[1] < 0}
            comparisons[f"{new}_minus_{old}"] = comparison
        result["scopes"][scope] = {"PSG_records_with_GT": len(evaluated_indices), "unique_source_identities": len(identity_keys),
                                   "predicate_classes": len(predicates), "comparisons": comparisons}
    return result


def endpoint_and_cost_summary(sources, predictions):
    coverage = {}
    costs = {}
    for group in GROUPS:
        counter = Counter()
        queries = []
        relation_times = []
        matches_by_index = {}
        for source, output in zip(sources, predictions):
            result = output["groups"][group]
            matches = endpoint_matches(result["objects"], source["ground_truth_objects"], False)
            matches_by_index[source["index"]] = matches
            people = [item for item in source["ground_truth_objects"] if item["is_person"]]
            person_detected = any(item["is_person"] for item in result["objects"])
            counter["GT_person_endpoints"] += len(people)
            counter["matched_person_endpoints"] += sum(bool(matches[item["id"]]) for item in people)
            counter["GT_person_records"] += bool(people)
            counter["detected_person_records"] += person_detected
            counter["GT_person_records_with_detection"] += bool(people and person_detected)
            endpoint_ids = {row[key] for row in source["ground_truth_relations"] for key in ("subject_id", "object_id")}
            counter["human_relation_unique_GT_endpoints"] += len(endpoint_ids)
            counter["matched_human_relation_GT_endpoints"] += sum(bool(matches[index]) for index in endpoint_ids)
            for truth in source["ground_truth_relations"]:
                a, b = matches[truth["subject_id"]], matches[truth["object_id"]]
                counter["relations_with_two_matching_endpoints"] += bool(a and b)
                counter["relations_with_distinct_matching_endpoints"] += any(x != y for x in a for y in b)
            counter["selected_endpoints"] += len(result["objects"])
            counter["selected_crop_endpoints"] += sum(item["source_kind"] == "crop" for item in result["objects"])
            counter["original_endpoints_not_selected"] += len(result["merge_audit"]["original_source_keys_not_selected"])
            counter["crop_detections_before_merge"] += result["merge_audit"]["crop_detection_count"]
            counter["endpoints_removed_by_NMS"] += len(result["merge_audit"]["removed_by_NMS"])
            counter["endpoints_removed_by_40_cap"] += len(result["merge_audit"]["removed_by_endpoint_cap"])
            counter["relation_forward_calls"] += bool(result["candidate_pairs"])
            counter["relation_candidate_pairs"] += result["candidate_pairs"]
            counter["human_relation_candidate_pairs"] += result["human_pairs_scored"]
            counter["returned_relations"] += len(result["relations"])
            counter["duplicate_crop_records"] += bool(result["queries"] and
                                                      len({tuple(row["crop_box_xyxy"]) for row in result["queries"]}) < len(result["queries"]))
            queries.extend(result["queries"])
            relation_times.append(result["relation_elapsed_seconds"])
        counter["person_box_recall"] = counter["matched_person_endpoints"] / counter["GT_person_endpoints"]
        counter["human_relation_endpoint_recall"] = counter["matched_human_relation_GT_endpoints"] / counter["human_relation_unique_GT_endpoints"]
        coverage[group] = {"summary": dict(counter), "matched_endpoint_ids_by_record": {
            str(index): {str(endpoint): sorted(values) for endpoint, values in matches.items()} for index, matches in matches_by_index.items()}}
        query_times = [row["elapsed_seconds"] for row in queries]
        pixels = [row["input_pixels"] for row in queries]
        costs[group] = {"additional_detector_calls": len(queries), "query_policy_sources": dict(Counter(row["policy_source"] for row in queries)),
                        "total_query_input_pixels": sum(pixels), "query_input_pixels_mean": float(np.mean(pixels)) if pixels else 0,
                        "query_seconds_total": sum(query_times), "query_seconds_mean": float(np.mean(query_times)) if query_times else 0,
                        "query_seconds_median": float(np.median(query_times)) if query_times else 0,
                        "query_seconds_p90": float(np.quantile(query_times, .9)) if query_times else 0,
                        "relation_seconds_total": sum(relation_times), "relation_seconds_mean_per_record": float(np.mean(relation_times)),
                        "relation_seconds_p90": float(np.quantile(relation_times, .9)),
                        "measured_query_plus_relation_seconds": sum(query_times) + sum(relation_times)}
    baseline = coverage["baseline"]["matched_endpoint_ids_by_record"]
    for group in GROUPS[1:]:
        recovered = []
        lost = []
        for source in sources:
            index = str(source["index"])
            related = {str(row[key]) for row in source["ground_truth_relations"] for key in ("subject_id", "object_id")}
            current = coverage[group]["matched_endpoint_ids_by_record"][index]
            for endpoint in related:
                if bool(current[endpoint]) and not baseline[index][endpoint]:
                    recovered.append({"index": source["index"], "GT_endpoint_id": int(endpoint), "new_endpoint_ids": current[endpoint]})
                elif baseline[index][endpoint] and not current[endpoint]:
                    lost.append({"index": source["index"], "GT_endpoint_id": int(endpoint), "old_endpoint_ids": baseline[index][endpoint]})
        coverage[group]["recovered_human_relation_endpoints"] = recovered
        coverage[group]["lost_human_relation_endpoints"] = lost
        coverage[group]["summary"]["recovered_human_relation_endpoint_count"] = len(recovered)
        coverage[group]["summary"]["lost_human_relation_endpoint_count"] = len(lost)
    coverage["baseline"]["summary"]["recovered_human_relation_endpoint_count"] = 0
    coverage["baseline"]["summary"]["lost_human_relation_endpoint_count"] = 0
    return coverage, costs


def relation_evidence(source, result, truth, diagnostic):
    objects = {row["id"]: row for row in result["objects"]}
    subject_ids, object_ids = set(diagnostic["matching_subject_ids"]), set(diagnostic["matching_object_ids"])
    return {"stage": diagnostic["stage"],
            "matching_subject_endpoints": [objects[index] for index in sorted(subject_ids)],
            "matching_object_endpoints": [objects[index] for index in sorted(object_ids)],
            "matching_pair_Top50": [row for row in result["relations"] if row["subject_id"] in subject_ids and row["object_id"] in object_ids],
            "correct_predicate_Top50": [row for row in result["relations"] if row["subject_id"] in subject_ids
                                         and row["object_id"] in object_ids and row["predicate_id"] == truth["predicate_id"]]}


def build_changes(sources, predictions, evaluation):
    result = {}
    for scope in SCOPES:
        indexed_details = {group: {row["index"]: {relation_key(item): item for item in row["diagnostics"]}
                                   for row in evaluation[group][scope]["per_image"]} for group in GROUPS}
        for new, old in COMPARISONS:
            rows = []
            stages = Counter()
            recovered, lost = 0, 0
            for source, output in zip(sources, predictions):
                gt_objects = {row["id"]: row for row in source["ground_truth_objects"]}
                truths = source["ground_truth_relations"] if scope == SCOPES[0] else source["fixed_endpoint_valid_relations"]
                for truth in truths:
                    key = relation_key(truth)
                    old_detail, new_detail = indexed_details[old][source["index"]][key], indexed_details[new][source["index"]][key]
                    old_hit, new_hit = old_detail["stage"] == "hit50", new_detail["stage"] == "hit50"
                    stages[f"{old_detail['stage']} -> {new_detail['stage']}"] += 1
                    if old_hit == new_hit:
                        continue
                    recovered += new_hit
                    lost += old_hit
                    rows.append({"index": source["index"], "file_name": source["file_name"], "change": "recovered" if new_hit else "lost",
                                 "GT_relation": truth, "GT_subject": gt_objects[truth["subject_id"]],
                                 "GT_object": gt_objects[truth["object_id"]],
                                 "old_group": old, "new_group": new,
                                 "old": relation_evidence(source, output["groups"][old], truth, old_detail),
                                 "new": relation_evidence(source, output["groups"][new], truth, new_detail)})
            recovered_rows = [row for row in rows if row["change"] == "recovered"]
            lost_rows = [row for row in rows if row["change"] == "lost"]
            crop_supported = 0
            crop_required = 0
            for row in recovered_rows:
                endpoints = {item["id"]: item for item in row["new"]["matching_subject_endpoints"] + row["new"]["matching_object_endpoints"]}
                uses_crop = [any(endpoints[relation[key]]["source_kind"] == "crop" for key in ("subject_id", "object_id"))
                             for relation in row["new"]["correct_predicate_Top50"]]
                crop_supported += any(uses_crop)
                crop_required += bool(uses_crop) and all(uses_crop)
            result[f"{scope}/{new}_minus_{old}"] = {
                "recovered": recovered, "lost": lost, "net_hits": recovered - lost,
                "recoveries_from_old_stages": dict(Counter(row["old"]["stage"] for row in recovered_rows)),
                "losses_to_new_stages": dict(Counter(row["new"]["stage"] for row in lost_rows)),
                "recoveries_with_at_least_one_crop_supported_Top50_match": crop_supported,
                "recoveries_where_all_correct_Top50_matches_use_crop_endpoint": crop_required,
                "all_GT_stage_transitions": dict(stages), "changed_GT_relations": rows}
    return result


def save_paired_outputs(sources, predictions, identities, report_dir):
    rows = []
    for source, output in zip(sources, predictions):
        rows.append({"index": source["index"], "file_name": source["file_name"], "image_sha256": source["image_sha256"],
                     "image_size": source["image_size"], "source_identity": identities[source["index"]]["identity_key"],
                     "ground_truth_objects": source["ground_truth_objects"], "ground_truth_relations": source["ground_truth_relations"],
                     "fixed_endpoint_valid_relations": source["fixed_endpoint_valid_relations"],
                     "groups": {group: {"objects": output["groups"][group]["objects"],
                                        "relations": output["groups"][group]["relations"],
                                        "queries": output["groups"][group]["queries"],
                                        "candidate_pairs": output["groups"][group]["candidate_pairs"],
                                        "human_pairs_scored": output["groups"][group]["human_pairs_scored"],
                                        "merge_audit": output["groups"][group]["merge_audit"]} for group in GROUPS}})
    write_lines(report_dir / "paired_outputs.jsonl", rows)


def markdown_table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in rows])


def box_string(item):
    return ", ".join(f"{value:.2f}" for value in item["box_xyxy"])


def case_studies(sources, predictions, changes, evaluation, report_dir, config):
    source_indexed = {row["index"]: row for row in sources}
    output_indexed = {row["index"]: row for row in predictions}
    selections = []
    used = set()
    categories = [("RA相对原始结果恢复", "RA_guided_minus_baseline", "recovered"),
                  ("RA相对几何补检测恢复", "RA_guided_minus_geometry", "recovered"),
                  ("几何补检测相对RA恢复", "RA_guided_minus_geometry", "lost"),
                  ("RA相对原始结果丢失", "RA_guided_minus_baseline", "lost"),
                  ("几何补检测相对原始结果恢复", "geometry_minus_baseline", "recovered"),
                  ("几何补检测相对原始结果丢失", "geometry_minus_baseline", "lost")]
    for name, comparison, kind in categories:
        candidates = [row for row in changes[f"{SCOPES[0]}/{comparison}"]["changed_GT_relations"]
                      if row["change"] == kind and row["index"] not in used]
        if candidates:
            candidates.sort(key=lambda row: (row["index"], row["GT_relation"]["subject_id"], row["GT_relation"]["object_id"], row["GT_relation"]["predicate_id"]))
            selections.append((name, candidates[0]))
            used.add(candidates[0]["index"])
    lines = ["# 主动补检测：三组完整案例", "", "案例按变化类型和PSG记录编号确定性选择，未使用人工看图进行筛选。下列判断均是PSG标注匹配代理。坐标均位于原始图片坐标系，格式为左、上、右、下。", "",
             "每个案例展示三组全部保留端点、两次查询计划及全部Top50输出。500条记录的同类证据完整保存在[paired_outputs.jsonl](paired_outputs.jsonl)。"]
    details = {group: {row["index"]: {relation_key(item): item for item in row["diagnostics"]}
                        for row in evaluation[group][SCOPES[0]]["per_image"]} for group in GROUPS}
    for number, (name, selected) in enumerate(selections[:config["example_image_count"]], 1):
        source = source_indexed[selected["index"]]
        output = output_indexed[selected["index"]]
        truth = selected["GT_relation"]
        lines.extend(["", f"## 案例{number}：{name}；记录{source['index']}，{source['file_name']}", "",
                      f"PSG标注关系：#{truth['subject_id']} {selected['GT_subject']['label']} → {truth['predicate']} → #{truth['object_id']} {selected['GT_object']['label']}。", "",
                      f"标注主语坐标：{box_string(selected['GT_subject'])}；标注宾语坐标：{box_string(selected['GT_object'])}。", ""])
        lines.append(markdown_table(["方法", "匹配阶段", "匹配主语编号", "匹配宾语编号", "正确关系名次"], [
            [GROUP_LABELS[group], details[group][source["index"]][relation_key(truth)]["stage"],
             details[group][source["index"]][relation_key(truth)]["matching_subject_ids"],
             details[group][source["index"]][relation_key(truth)]["matching_object_ids"],
             [row["rank"] for row in relation_evidence(source, output["groups"][group], truth,
                                                        details[group][source["index"]][relation_key(truth)])["correct_predicate_Top50"]]]
            for group in GROUPS]))
        for group in GROUPS:
            prediction = output["groups"][group]
            lines.extend(["", f"### {GROUP_LABELS[group]}", "", "全部保留端点：", "",
                          markdown_table(["编号", "类别", "原图坐标", "检测分数", "来源及编号"], [
                              [item["id"], item["label"], box_string(item), f"{item['detection_score']:.6f}", item["source_object_key"]]
                              for item in prediction["objects"]]), "", "局部检测查询：", ""])
            if prediction["queries"]:
                lines.append(markdown_table(["查询编号", "选择依据", "裁剪坐标", "引导关系", "检测数量", "秒数"], [
                    [query["query_id"], query["policy_source"], query["crop_box_xyxy"],
                     f"#{query['guidance_relation']['subject_id']} {query['guidance_relation']['predicate']} #{query['guidance_relation']['object_id']}" if query["guidance_relation"] else "几何身体高度规则",
                     len(query["detections"]), f"{query['elapsed_seconds']:.6f}"] for query in prediction["queries"]]))
            else:
                lines.append("原始方法没有新增检测查询。")
            lines.extend(["", "全部关系输出：", "", markdown_table(["名次", "主语", "谓词", "宾语", "谓词logit", "配对logit", "合成logit", "原始sigmoid"], [
                [row["rank"], f"#{row['subject_id']} {row['subject_label']}", row["predicate"], f"#{row['object_id']} {row['object_label']}",
                 f"{row['predicate_logit']:.6f}", f"{row['pair_logit']:.6f}", f"{row['fused_logit']:.6f}", f"{row['score']:.6f}"]
                for row in prediction["relations"]]), "",
                          f"合并审计：候选端点{prediction['merge_audit']['input_endpoint_count']}个，非极大值抑制后{prediction['merge_audit']['after_NMS_count']}个，最终{len(prediction['objects'])}个；未保留的原端点编号：{prediction['merge_audit']['original_source_keys_not_selected']}。"])
    (report_dir / "case_studies.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [{"category": name, "index": row["index"], "GT_relation": row["GT_relation"]} for name, row in selections]


def make_charts(evaluation, bootstrap, coverage, costs, report_dir):
    plt.rcParams.update({"font.size": 10, "svg.fonttype": "none"})
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    x = np.arange(3)
    colors = ["#526171", "#4693b6", "#d98741"]
    for axis, scope in zip(axes, SCOPES):
        width = .32
        axis.bar(x - width / 2, [evaluation[group][scope]["metrics"]["R@50"] * 100 for group in GROUPS],
                 width, label="R@50", color=colors)
        axis.bar(x + width / 2, [evaluation[group][scope]["metrics"]["mR@50"] * 100 for group in GROUPS],
                 width, label="mR@50", color=colors, alpha=.48)
        axis.set_xticks(x, ["Baseline", "Geometry", "RA-guided"])
        axis.set_ylabel("Recall (%)")
        axis.set_title("All 968 GT relations" if scope == SCOPES[0] else "Fixed 530 GT relations")
        axis.legend()
        axis.grid(axis="y", alpha=.2)
    figure.savefig(report_dir / "recall_comparison.png", dpi=160)
    figure.savefig(report_dir / "recall_comparison.svg")
    plt.close(figure)
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for position, (new, old) in enumerate(COMPARISONS):
        item = bootstrap["scopes"][SCOPES[0]]["comparisons"][f"{new}_minus_{old}"]["R@50"]
        point, bounds = item["point_difference"] * 100, np.array(item["percentile_95_CI"]) * 100
        axes[0].errorbar(point, position, xerr=[[point - bounds[0]], [bounds[1] - point]], fmt="o", capsize=4, color=colors[position])
    axes[0].set_yticks(range(3), ["Geometry − baseline", "RA − baseline", "RA − geometry"])
    axes[0].axvline(0, color="gray", linestyle="--")
    axes[0].set_xlabel("Paired R@50 difference (percentage points), 95% CI")
    axes[0].set_title("Source-identity bootstrap, all GT")
    axes[1].bar(x, [costs[group]["measured_query_plus_relation_seconds"] for group in GROUPS], color=colors)
    axes[1].set_xticks(x, ["Baseline", "Geometry", "RA-guided"])
    axes[1].set_ylabel("Measured query + relation seconds")
    axes[1].set_title("500 PSG records; query counts alone do not fix compute")
    figure.savefig(report_dir / "paired_gain_and_cost.png", dpi=160)
    figure.savefig(report_dir / "paired_gain_and_cost.svg")
    plt.close(figure)


def write_predicate_comparison(evaluation, report_dir):
    predicates = read_json(ROOT / "data/PSG/packed/psg/test/meta.json")["predicates"]
    lines = ["# 主动补检测：全部谓词的三方对照", "",
             "列出每个有标注谓词的全部结果。类别平均召回先在包含该谓词的PSG记录内计算召回，再跨记录平均；主表mR@50是这些列的跨类别平均。命中数量除以该类标注数量得到汇总召回，权重含义有所不同。", ""]
    for scope in SCOPES:
        lines.extend([f"## {scope}", ""])
        rows = []
        for key, value in evaluation["baseline"][scope]["per_class"].items():
            other = {group: evaluation[group][scope]["per_class"][key] for group in GROUPS}
            rows.append([predicates[int(key)], value["gt"]] + [other[group]["hits50"] for group in GROUPS] +
                        [f"{other[group]['image_macro_R@50']:.8f}" for group in GROUPS] +
                        [f"{other['RA_guided']['image_macro_R@50'] - other['baseline']['image_macro_R@50']:.8f}"])
        lines.extend([markdown_table(["谓词", "标注数量", "原始命中", "几何命中", "RA命中", "原始类别平均召回", "几何类别平均召回", "RA类别平均召回", "RA相对原始变化"], rows), ""])
    (report_dir / "per_predicate_comparison.md").write_text("\n".join(lines), encoding="utf-8")


def write_report(evaluation, bootstrap, coverage, costs, changes, runtime, audit, cases, report_dir, config):
    lines = ["# E：关系引导主动补检测，同查询次数对照", "",
             "本实验检查：当同一张图片允许两次局部目标检测时，使用RelateAnything已有关系选择观察区域，能否比人物几何规则恢复更多PSG人相关关系。使用固定500条PSG测试记录、499个独立来源身份、官方关系权重及本地Faster R-CNN权重，已经实际执行三组GPU推理。", "",
             "## 实验设计与预先固定规则", "",
             "原始方法保留区域实验A的Faster R-CNN thing端点，并重新执行关系推理。几何方法选择检测面积最大的人物，分别在人物高度30%与75%处观察。RA引导方法只读取冻结A方法的Top50预测，按融合logit排序：holding、carrying、wearing查询上身，riding、sitting on查询下身，standing on、walking on、running on查询脚部，其他受支持谓词采用配置指定高度。", "",
             "每个关系引导查询的中心由人物身体位置与预测对象中心按65%及35%混合。裁剪宽度为人物宽度的1.8倍，高度为人物高度的0.8倍，短边至少96像素，限制在原图边界内。只接受人物作为主语、非人物作为宾语、原始sigmoid≥0.5的候选。该分数没有解释为事件真实概率。优先选择不同的整数裁剪区域；不足时使用固定几何区域。边界裁剪可能让两个预定观察具有相同像素范围，仍真实执行两次查询，并记录重复数量。", "",
             "原检测结果包含人物的288条记录，两种补检测方法各执行576次真实局部Faster R-CNN调用；剩余212条记录两组均执行零次。完全漏检人物的图片无法通过此策略启动人物局部查询。选择裁剪区域的函数只接收检测端点、预测关系、图像尺寸与配置，不接收PSG标注。", "",
             "每次局部检测的坐标变换回原图，和原端点按类别进行IoU=0.6的非极大值抑制，再按检测分数保留最多40个端点。三组统一使用官方400个关系候选预算与最多50条输出；补检测可以替换原端点，所以收益和丢失都必须计入。三组执行顺序随样本位置轮换。", "",
             "本实验的same query budget表示两个主动方法的新增检测调用次数相同。裁剪像素面积、检测器缩放后的输入规模、返回端点及实际运行时间仍可能不同，计算成本单独报告。原始方法复用已有全图检测缓存，三组成本均不包含这一共有的全图检测费用。", "",
             "## 主结果", "",
             "R@50先计算包含标注关系的每条PSG记录的召回，再取平均；mR@50先按谓词计算包含该谓词的记录平均召回，再跨谓词平均；pooled_R@50直接使用命中关系总数除以标注总数。评测要求主语和宾语类别一致、各自IoU≥0.5、谓词一致。在每个评测范围内，三组使用同一固定分母；两个范围分别为全部968条标注及原始端点有效的固定530条子集，新增端点没有改变子集。", ""]
    rows = []
    for scope in SCOPES:
        for group in GROUPS:
            item = evaluation[group][scope]
            rows.append([scope, GROUP_LABELS[group], f"{item['hits'][50]}/{item['unique_gt']}",
                         f"{item['metrics']['R@50']:.8f}", f"{item['metrics']['mR@50']:.8f}",
                         f"{item['metrics']['pooled_R@50']:.8f}", item["scored_images"]])
    lines.extend([markdown_table(["评测范围", "方法", "命中/标注", "R@50", "mR@50", "pooled_R@50", "有标注记录"], rows), "",
                  "![三组两种评测范围的完整召回结果](recall_comparison.png)", "", "## 配对不确定性与独立来源身份", "",
                  "通过Visual Genome的COCO身份及图片SHA256合并来源；COCO404484对应两条PSG记录，保留不同关系标注，但重抽样时一起出现。全部标注范围包含252条记录、251个来源身份；固定530条范围包含214条记录、214个来源身份。执行20,000次按来源身份的配对自助抽样，三组在每次使用同一身份抽样权重，保持原始PSG记录加权的点估计。置信区间为百分位95%区间，多个比较未进行校正，作为探索性证据解释。", ""])
    rows = []
    for scope in SCOPES:
        for comparison, values in bootstrap["scopes"][scope]["comparisons"].items():
            for metric, value in values.items():
                rows.append([scope, comparison, metric, f"{value['point_difference']:.8f}",
                             "[" + ", ".join(f"{number:.8f}" for number in value["percentile_95_CI"]) + "]",
                             "是" if value["CI_excludes_zero"] else "否"])
    lines.extend([markdown_table(["范围", "比较", "指标", "差值", "95%置信区间", "区间排除零"], rows), "",
                  "![全部标注的配对收益与真实时间成本](paired_gain_and_cost.png)", "", "## 端点覆盖、来源与原端点替换", ""])
    coverage_fields = ["GT_person_endpoints", "matched_person_endpoints", "person_box_recall", "detected_person_records",
                       "human_relation_unique_GT_endpoints", "matched_human_relation_GT_endpoints", "human_relation_endpoint_recall",
                       "relations_with_two_matching_endpoints", "relations_with_distinct_matching_endpoints", "selected_endpoints",
                       "selected_crop_endpoints", "crop_detections_before_merge", "original_endpoints_not_selected",
                       "endpoints_removed_by_NMS", "endpoints_removed_by_40_cap", "duplicate_crop_records",
                       "recovered_human_relation_endpoint_count", "lost_human_relation_endpoint_count"]
    labels = ["全部标注人物端点", "匹配的标注人物端点", "人物端点召回", "检出人物记录", "关系涉及的唯一标注端点", "匹配的关系端点",
              "关系端点召回", "两个端点均可匹配的关系", "存在不同匹配端点的关系", "保留端点总数", "其中裁剪来源端点", "合并前裁剪检测数量",
              "未保留的原端点数量", "非极大值抑制删除端点", "40端点上限删除端点", "包含重复裁剪的记录", "相对原始方法恢复标注端点", "相对原始方法丢失标注端点"]
    lines.append(markdown_table(["统计量"] + [GROUP_LABELS[group] for group in GROUPS], [
        [label] + [f"{coverage[group]['summary'][field]:.8f}" if isinstance(coverage[group]["summary"][field], float)
                   else coverage[group]["summary"][field] for group in GROUPS] for field, label in zip(coverage_fields, labels)]))
    lines.extend(["", "原端点被同类别更高分局部检测替代时，来源变化本身不代表标注端点丢失。报告分别保存原端点编号未保留、标注端点恢复及标注端点丢失；完整坐标、检测分数和裁剪来源见[endpoint_coverage.json](endpoint_coverage.json)及[paired_outputs.jsonl](paired_outputs.jsonl)。", "", "## 实际预算与时间成本", ""])
    rows = []
    for group in GROUPS:
        item = costs[group]
        summary = coverage[group]["summary"]
        rows.append([GROUP_LABELS[group], item["additional_detector_calls"], item["total_query_input_pixels"],
                     f"{item['query_seconds_total']:.6f}", f"{item['query_seconds_mean']:.6f}", f"{item['query_seconds_p90']:.6f}",
                     summary["relation_forward_calls"], summary["relation_candidate_pairs"], f"{item['relation_seconds_total']:.6f}",
                     summary["returned_relations"]])
    lines.extend([markdown_table(["方法", "新增检测调用", "裁剪像素总数", "检测秒数", "调用平均秒数", "调用P90秒数", "关系前向次数", "候选对总数", "关系秒数", "输出关系数"], rows), "",
                  f"实际设备：{runtime['GPU']}；检测器采用{runtime['detector_dtype']}，关系模型采用{runtime['relation_dtype']}；峰值显存分配{runtime['peak_GPU_allocated_GiB']:.6f} GiB。本次推理阶段耗时{runtime['this_invocation_inference_seconds']:.6f}秒，逐条耗时另含坐标合并与输出文件写入，和分项计时的含义不同。", "",
                  f"RA方法的查询来源计数：{json.dumps(costs['RA_guided']['query_policy_sources'], ensure_ascii=False)}。完整调用中位数、P90、裁剪面积与关系时间见[costs.json](costs.json)。", "", "## 恢复、丢失和失败阶段", ""])
    rows = []
    for name, item in changes.items():
        rows.append([name, item["recovered"], item["lost"], item["net_hits"]])
    lines.append(markdown_table(["范围及比较", "新恢复关系", "丢失关系", "净命中变化"], rows))
    lines.extend(["", "恢复与丢失按照每条标注关系的命中状态变化统计；全部阶段迁移、双方对应框和Top50证据见[relation_changes.json](relation_changes.json)。", ""])
    all_stages = sorted({stage for group in GROUPS for stage in evaluation[group][SCOPES[0]]["failure_stages"]})
    lines.append(markdown_table(["全部968条标注的阶段"] + [GROUP_LABELS[group] for group in GROUPS], [
        [stage] + [evaluation[group][SCOPES[0]]["failure_stages"].get(stage, 0) for group in GROUPS] for stage in all_stages]))
    lines.extend(["", "恢复与丢失的具体阶段来源：", "", markdown_table(
        ["全部968条标注的比较", "恢复前失败阶段", "丢失后失败阶段", "恢复中至少一个正确配对使用裁剪端点", "恢复中全部正确配对使用裁剪端点"], [
            [f"{new}_minus_{old}", json.dumps(changes[f"{SCOPES[0]}/{new}_minus_{old}"]["recoveries_from_old_stages"], ensure_ascii=False),
             json.dumps(changes[f"{SCOPES[0]}/{new}_minus_{old}"]["losses_to_new_stages"], ensure_ascii=False),
             changes[f"{SCOPES[0]}/{new}_minus_{old}"]["recoveries_with_at_least_one_crop_supported_Top50_match"],
             changes[f"{SCOPES[0]}/{new}_minus_{old}"]["recoveries_where_all_correct_Top50_matches_use_crop_endpoint"]]
            for new, old in COMPARISONS]), ""])
    lines.extend(["", "endpoint_missing_or_wrong_class表示至少一个标注端点没有类别及IoU匹配；endpoints_collapsed_to_same_box表示两个标注端点只对应同一检测框；pair_not_selected表示两个不同端点存在但候选预算没有选择对应有向配对；wrong_predicate表示已选配对的空间/语义分组赢家都未命中标注谓词；rank_below50表示正确分组赢家存在但没有进入最终输出；hit50表示命中。阶段只解释PSG标注召回，未匹配预测仍可能描述真实但未标注关系。", "",
                  "## 结果解释", ""])
    for new, old in COMPARISONS:
        a, b = evaluation[new][SCOPES[0]], evaluation[old][SCOPES[0]]
        diff = bootstrap["scopes"][SCOPES[0]]["comparisons"][f"{new}_minus_{old}"]["R@50"]
        relation_change = changes[f"{SCOPES[0]}/{new}_minus_{old}"]
        lines.extend([f"{GROUP_LABELS[new]}相对{GROUP_LABELS[old]}：全部标注命中从{b['hits'][50]}变为{a['hits'][50]}，恢复{relation_change['recovered']}条、丢失{relation_change['lost']}条；R@50变化{diff['point_difference'] * 100:.4f}个百分点，95%区间[{diff['percentile_95_CI'][0] * 100:.4f}, {diff['percentile_95_CI'][1] * 100:.4f}]个百分点。" +
                      ("该区间包含零，当前固定样本支持的收益方向仍有不确定性。" if not diff["CI_excludes_zero"] else "该探索性区间排除零，解释时仍需考虑预先选择策略和多个比较。"), ""])
    ra_geometry = bootstrap["scopes"][SCOPES[0]]["comparisons"]["RA_guided_minus_geometry"]["R@50"]
    if ra_geometry["point_difference"] <= 0:
        lines.extend(["在本次固定预算和路由规则下，关系引导没有超过几何方法的R@50点估计。关系语义可能把观察集中于已有高分对象，裁剪合并也可能改变原端点和全局排名；这些机制需要从恢复/丢失证据分别核查。此结果支持把主动观察作为输入修复对照，当前证据没有建立RA路由的独特优势。", ""])
    else:
        lines.extend(["关系引导相对几何补检测获得更高的R@50点估计，但两种主动方法的R@50都低于原始baseline。RA相对几何方法的配对区间包含零，当前实验没有建立稳定优势。结论范围限于这组裁剪与预算规则，单次比较不能证明新的主动感知方法成立。", ""])
    original_stages = evaluation["baseline"][SCOPES[0]]["failure_stages"]
    ra_stages = evaluation["RA_guided"][SCOPES[0]]["failure_stages"]
    losses = changes[f"{SCOPES[0]}/RA_guided_minus_baseline"]["losses_to_new_stages"]
    time_ratio = costs["RA_guided"]["measured_query_plus_relation_seconds"] / costs["baseline"]["measured_query_plus_relation_seconds"]
    lines.extend([f"RA补检测把端点缺失阶段从{original_stages['endpoint_missing_or_wrong_class']}条变为{ra_stages['endpoint_missing_or_wrong_class']}条，错误谓词从{original_stages['wrong_predicate']}条变为{ra_stages['wrong_predicate']}条，名次落在50之后的关系从{original_stages['rank_below50']}条变为{ra_stages['rank_below50']}条。RA丢失关系的阶段包括：{json.dumps(losses, ensure_ascii=False)}。更多可匹配端点与更高最终召回之间没有必然关系；上下文端点变化、候选竞争和最终排名共同影响输出。", "",
                  f"两种主动方法的最大候选预算相同，但实际候选总数从baseline的{coverage['baseline']['summary']['relation_candidate_pairs']:,}增加到几何方法的{coverage['geometry']['summary']['relation_candidate_pairs']:,}与RA方法的{coverage['RA_guided']['summary']['relation_candidate_pairs']:,}。RA的新增检测及关系总时间约为原始关系推理时间的{time_ratio:.2f}倍，当前策略没有呈现召回与成本同时改善的证据。RA的mR@50点估计高于baseline，置信区间包含零；[per_predicate_comparison.md](per_predicate_comparison.md)展示全部谓词在三组中的标注数量、命中和类别平均召回，便于检查罕见谓词的影响。", ""])
    lines.extend(["## 完整比较与失败案例", "",
                  f"[case_studies.md](case_studies.md)包含{len(cases)}个确定性选择案例，每个案例完整展示三组全部端点、实际裁剪规则和全部Top50关系，方便核查对象编号、谓词与分数变化。全量500条记录的三组对应结果保存在[paired_outputs.jsonl](paired_outputs.jsonl)；[evaluation.json](evaluation.json)保存每个有标注记录的全部失败阶段诊断及逐谓词召回。案例与输出均不依赖人工视觉判断，未发布源图片。", "", "## 与原区域实验的关系", "",
                  f"内部baseline与冻结A方法：完整Top50字段完全相同的记录{audit['frozen_A_comparison'].get('complete_top50_equal', 0)}/500；关系身份及排名相同的记录{audit['frozen_A_comparison'].get('top50_identities_and_order_equal', 0)}/500。具体差异保存于[cache_audit.json](cache_audit.json)。主动补检测的所有增量都相对于本实验内部baseline计算，区域补全、解码策略与主动补检测的增益不能直接相加。", "",
                  "## 复算与证据清单", "", "在仓库根目录运行：", "", "```powershell",
                  ".venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\active_detection_study.py --prepare",
                  ".venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\active_detection_study.py --infer", "```", "",
                  "首次准备和推理拒绝覆盖已有推理输出；完整重做前将HOR/research/output/active_detection整个目录移动到Git忽略的归档目录。中断后使用--infer --resume继续已有完整记录。已存在全部结果时，默认命令只在CPU验收缓存和复算报告：", "", "```powershell",
                  ".venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\active_detection_study.py", "```", "",
                  "配置：[active_detection.json](../../configs/active_detection.json)；运行脚本：[active_detection_study.py](../../scripts/active_detection_study.py)；分析脚本：[active_detection_analysis.py](../../scripts/active_detection_analysis.py)。[prepared_inputs.json](prepared_inputs.json)记录裁剪计划及上游文件签名，[runtime.json](runtime.json)记录实际GPU运行信息，[artifact_manifest.json](artifact_manifest.json)记录配置、脚本、模型、输入、输出与报告证据签名。原始全候选logits在Git忽略的output/active_detection/logits目录供本地检查。", "",
                  "## 适用范围", "",
                  "本实验没有训练、没有VLM轮次生成、没有人工独立完整关系标注，也没有接触部位、深度或三维损害的真实性测量。PSG匹配代理不能解释为所有输出的真实性准确率。两次裁剪仍可能观察同一对象，预测关系的自我确认风险由同预算几何对照与失败证据暴露，未通过循环推理消除。固定500条样本的查询规则和结果共同定义当前实证范围。"])
    (report_dir / "E_主动补检测完整实验报告.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def artifact_manifest(report_dir, config, config_path):
    output_dir = ROOT / config["output_directory"]
    inputs = [config_path, Path(__file__), Path(__file__).with_name("active_detection_study.py"),
              ROOT / "HOR/pipeline.py", ROOT / "HOR/evaluation.py", ROOT / "HOR/config.json",
              ROOT / "data/PSG/packed/psg/test/meta.json",
              ROOT / config["source_region_predictions"], ROOT / config["source_region_runtime"],
              ROOT / config["source_region_evaluation"], ROOT / config["source_identity_metadata"], ROOT / config["sample_manifest"],
              ROOT / config["detector_weights"], ROOT / config["relation_weights"], ROOT / config["text_weights"]]
    outputs = [path for path in output_dir.rglob("*") if path.is_file()]
    reports = [path for path in report_dir.rglob("*") if path.is_file() and path.name != "artifact_manifest.json"]
    files = {path.relative_to(ROOT).as_posix(): {"sha256": sha256(path), "bytes": path.stat().st_size}
             for path in inputs + outputs + reports}
    save_json(report_dir / "artifact_manifest.json", {"study": config["study"], "files": files,
                                                     "source_images": "500 per-record byte hashes retained in paired_outputs.jsonl",
                                                     "published_source_images": 0, "human_visual_annotation_performed": False})


def analyze(sources, config, config_path):
    output_dir = ROOT / config["output_directory"]
    report_dir = ROOT / config["report_directory"]
    prepared, plans = validate_preparation(sources, config, config_path)
    predictions = read_lines(output_dir / "predictions.jsonl")
    runtime = read_json(output_dir / "runtime.json")
    identities = identity_metadata(sources, config)
    audit = audit_outputs(sources, predictions, plans, config)
    evaluation = evaluate_groups(sources, predictions)
    bootstrap = bootstrap_comparisons(sources, evaluation, identities, config)
    coverage, costs = endpoint_and_cost_summary(sources, predictions)
    changes = build_changes(sources, predictions, evaluation)
    report_dir.mkdir(parents=True, exist_ok=True)
    for filename, value in (("prepared_inputs.json", prepared), ("runtime.json", runtime), ("cache_audit.json", audit),
                            ("evaluation.json", evaluation), ("bootstrap.json", bootstrap), ("endpoint_coverage.json", coverage),
                            ("costs.json", costs), ("relation_changes.json", changes)):
        save_json(report_dir / filename, value)
    write_lines(report_dir / "crop_plans.jsonl", plans)
    save_paired_outputs(sources, predictions, identities, report_dir)
    cases = case_studies(sources, predictions, changes, evaluation, report_dir, config)
    write_predicate_comparison(evaluation, report_dir)
    make_charts(evaluation, bootstrap, coverage, costs, report_dir)
    write_report(evaluation, bootstrap, coverage, costs, changes, runtime, audit, cases, report_dir, config)
    artifact_manifest(report_dir, config, config_path)
    print(json.dumps({group: {scope: evaluation[group][scope]["metrics"] for scope in SCOPES} for group in GROUPS},
                     ensure_ascii=False, indent=2))
