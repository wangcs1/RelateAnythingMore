import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from time import perf_counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = ROOT / "HOR/research/configs/controlled_3d.json"
JOINT_NAMES = ("root", "shoulder", "left_hand", "right_hand", "hip", "left_foot", "right_foot")
PARENTS = np.asarray((-1, 0, 1, 1, 0, 4, 4))
METHODS = ("none", "hard_top1", "calibrated_soft_top1", "single_reject", "multi_risk", "oracle")
LABELS = {
    "none": "无接触约束",
    "hard_top1": "最高对应硬约束",
    "calibrated_soft_top1": "关系后验加权单对应",
    "single_reject": "单对应选择性拒绝",
    "multi_risk": "多候选几何代价选择",
    "oracle": "真实对应参考",
}
RANKINGS = ("semantic_only", "margin_only", "sensitivity_only", "random", "single_risk", "multi_risk")


def serializable(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    return value


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(serializable(value), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, rows):
    assert rows
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(serializable(rows))


def unit(vector):
    return vector / np.linalg.norm(vector)


def softmax(values):
    values = np.asarray(values, dtype=float)
    weights = np.exp(values - np.max(values))
    return weights / weights.sum()


def semantic_posterior(observation, config):
    positive_mean = config["semantic_positive_mean"]
    negative_mean = config["semantic_negative_mean"]
    prevalence = config["positive_prevalence"]
    log_odds = math.log(prevalence / (1.0 - prevalence))
    log_odds += (positive_mean - negative_mean) * (
        observation - 0.5 * (positive_mean + negative_mean)
    ) / config["semantic_noise_sigma"] ** 2
    return 1.0 / (1.0 + math.exp(-float(log_odds)))


def generate_true_pose(rng):
    pose = np.asarray([
        [0.0, 0.0, 0.0], [0.0, 0.48, 0.0], [-0.34, 0.28, 0.0],
        [0.34, 0.28, 0.0], [0.0, -0.32, 0.0], [-0.16, -0.82, 0.0], [0.16, -0.82, 0.0],
    ])
    for joint in (2, 3, 5, 6):
        offset = pose[joint] - pose[PARENTS[joint]]
        rotated = unit(offset + rng.normal(0.0, 0.09, 3)) * np.linalg.norm(offset)
        pose[joint] = pose[PARENTS[joint]] + rotated
    yaw = rng.uniform(-math.pi, math.pi)
    rotation = np.asarray([[math.cos(yaw), 0.0, math.sin(yaw)], [0.0, 1.0, 0.0], [-math.sin(yaw), 0.0, math.cos(yaw)]])
    return pose @ rotation.T * rng.uniform(0.9, 1.1) + rng.uniform(-0.2, 0.2, (1, 3))


def likelihood_distribution(initial, observations, observed, initial_sigma, candidates, config):
    variance = initial_sigma[None, :] ** 2 + np.asarray([
        config["image_noise_sigma"] ** 2,
        config["image_noise_sigma"] ** 2,
        config["depth_noise_sigma"] ** 2,
    ])[None, :]
    scores = []
    for candidate in candidates:
        template = initial.copy()
        template[candidate["joint"]] = candidate["target"]
        log_density = (observations - template) ** 2 / variance + np.log(2.0 * math.pi * variance)
        scores.append(float(-0.5 * log_density[observed].sum()))
    return softmax(scores), scores


def make_scenarios(seed, count, split, config):
    rng = np.random.default_rng(seed)
    ranking_rng = np.random.default_rng(config["random_ranking_seed"] + seed)
    scenarios = []
    for index in range(count):
        true_pose = generate_true_pose(rng)
        relation = str(rng.choice(("holding", "sitting on", "standing on")))
        parts = {"holding": (2, 3), "sitting on": (4, 4), "standing on": (5, 6)}[relation]
        actual_part = int(rng.choice(parts))
        positive = bool(rng.random() < config["positive_prevalence"])
        radius = float(rng.uniform(*config["sphere_radius_range"]))
        normal = unit(true_pose[1] - true_pose[actual_part]) if relation == "holding" else np.asarray([0.0, 1.0, 0.0])
        if positive:
            center = true_pose[actual_part] - radius * normal
        else:
            center = true_pose[0] + np.asarray([rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.6), rng.uniform(-0.7, 0.7)])
            for _ in range(100):
                if np.min(np.linalg.norm(true_pose - center, axis=1)) > radius + config["negative_surface_gap_min"]:
                    break
                center += rng.normal(0.0, 0.15, 3)
            assert np.min(np.linalg.norm(true_pose - center, axis=1)) > radius + config["negative_surface_gap_min"]
        other_part = parts[1] if actual_part == parts[0] else parts[0]
        other_normal = unit(-normal + rng.normal(0.0, 0.25, 3))
        candidates = [
            {"joint": actual_part, "target": center + radius * normal},
            {"joint": other_part, "target": center + radius * other_normal},
        ]
        permutation = rng.permutation(2)
        candidates = [candidates[int(item)] for item in permutation]
        true_index = int(np.flatnonzero(permutation == 0)[0]) if positive else -1
        initial_sigma = np.asarray(config["initial_sigma_xyz"]) * rng.uniform(*config["initial_noise_scale_range"])
        initial = true_pose + rng.normal(size=(7, 3)) * initial_sigma[None, :]
        observations = true_pose + rng.normal(size=(7, 3)) * np.asarray([
            config["image_noise_sigma"], config["image_noise_sigma"], config["depth_noise_sigma"],
        ])[None, :]
        visible = rng.random(7) < config["visible_probability"]
        depth_visible = (rng.random(7) < config["depth_visible_probability"]) & visible
        occluded = bool(rng.random() < config["occluded_probability"])
        if occluded:
            for part in set(parts):
                visible[part] = rng.random() < config["occluded_part_visible_probability"]
                depth_visible[part] = visible[part] and rng.random() < config["occluded_part_depth_probability"]
        observed = np.column_stack((visible, visible, depth_visible))
        observations[~observed] = 0.0
        q_values, log_likelihoods = likelihood_distribution(initial, observations, observed, initial_sigma, candidates, config)
        semantic_mean = config["semantic_positive_mean"] if positive else config["semantic_negative_mean"]
        semantic_observation = float(rng.normal(semantic_mean, config["semantic_noise_sigma"]))
        public = {
            "scenario_id": index, "split": split, "relation": relation, "initial": initial,
            "initial_sigma": initial_sigma, "observations": observations, "observed": observed,
            "center": center, "radius": radius, "candidates": candidates,
            "q": q_values, "candidate_log_likelihood": log_likelihoods,
            "semantic_observation": semantic_observation, "p_r": semantic_posterior(semantic_observation, config),
            "occluded": occluded, "random_ranking": float(ranking_rng.random()),
        }
        truth = {"positive": positive, "true_index": true_index, "true_pose": true_pose}
        if positive:
            true_candidate = candidates[true_index]
            assert np.linalg.norm(true_pose[true_candidate["joint"]] - true_candidate["target"]) < 1e-12
        assert np.allclose(np.linalg.norm(np.asarray([item["target"] for item in candidates]) - center, axis=1), radius)
        assert np.isfinite(q_values).all() and np.isclose(q_values.sum(), 1.0)
        scenarios.append({"public": public, "truth": truth})
    return scenarios


def bone_lengths(pose):
    return np.linalg.norm(pose[1:] - pose[PARENTS[1:]], axis=1)


def sphere_penetration(pose, public):
    return np.maximum(public["radius"] - np.linalg.norm(pose - public["center"], axis=1), 0.0)


class QuadraticSolver:
    def __init__(self, public, config):
        self.public = public
        self.config = config
        incidence = np.zeros((6, 7))
        for edge, joint in enumerate(range(1, 7)):
            incidence[edge, joint] = 1.0
            incidence[edge, PARENTS[joint]] = -1.0
        self.incidence = incidence
        self.prior_precision = 1.0 / public["initial_sigma"] ** 2
        self.observation_precision = np.asarray([
            1.0 / config["image_noise_sigma"] ** 2,
            1.0 / config["image_noise_sigma"] ** 2,
            1.0 / config["depth_noise_sigma"] ** 2,
        ])
        self.bone_precision = 1.0 / config["bone_offset_sigma"] ** 2
        matrices, vectors = [], []
        for axis in range(3):
            prior_matrix = self.prior_precision[axis] * np.eye(7) + self.bone_precision * incidence.T @ incidence
            weights = public["observed"][:, axis] * self.observation_precision[axis]
            matrices.append(prior_matrix + np.diag(weights))
            vectors.append(prior_matrix @ public["initial"][:, axis] + weights * public["observations"][:, axis])
        self.matrices = np.asarray(matrices)
        self.vectors = np.asarray(vectors)
        self.calls = 0
        self.seconds = 0.0
        self.maximum_residual = 0.0
        self.maximum_objective_ratio = 0.0

    def objective(self, pose, joint, target, weight):
        public = self.public
        difference = pose - public["initial"]
        value = np.sum(difference ** 2 * self.prior_precision[None, :])
        value += self.bone_precision * np.sum((self.incidence @ difference) ** 2)
        value += np.sum((pose - public["observations"]) ** 2 * public["observed"] * self.observation_precision[None, :])
        if joint is not None:
            value += weight * np.sum((pose[joint] - target) ** 2)
        return float(value)

    def solve(self, joint=None, target=None, support=0.0):
        started = perf_counter()
        matrices, vectors = self.matrices.copy(), self.vectors.copy()
        weight = support / self.config["contact_sigma"] ** 2
        if joint is not None:
            matrices[:, joint, joint] += weight
            vectors[:, joint] += weight * target
        solution = np.linalg.solve(matrices, vectors[:, :, None])[:, :, 0].T
        residual = float(np.max(np.abs(np.einsum("dij,jd->di", matrices, solution) - vectors)) / max(1.0, np.max(np.abs(vectors))))
        before = self.objective(self.public["initial"], joint, target, weight)
        after = self.objective(solution, joint, target, weight)
        assert residual < self.config["normal_equation_tolerance"]
        assert after <= before + 1e-8 * max(1.0, before)
        assert np.isfinite(solution).all()
        seconds = perf_counter() - started
        self.calls += 1
        self.seconds += seconds
        self.maximum_residual = max(self.maximum_residual, residual)
        self.maximum_objective_ratio = max(self.maximum_objective_ratio, after / max(before, 1e-30))
        return {"pose": solution, "seconds": seconds, "residual": residual, "objective_before": before, "objective_after": after}


def measured_reprojection_error(pose, public):
    mask = public["observed"][:, :2]
    if not mask.any():
        return 0.0
    return float(np.sqrt(np.mean((pose[:, :2] - public["observations"][:, :2])[mask] ** 2)))


def candidate_risk(public, candidate, result, baseline, solver, config, probe_rows):
    delta = config["finite_difference_delta"]
    derivatives = []
    seconds = result["seconds"]
    for axis in range(3):
        perturbation = np.eye(3)[axis] * delta
        plus = solver.solve(candidate["joint"], candidate["target"] + perturbation, public["p_r"])
        minus = solver.solve(candidate["joint"], candidate["target"] - perturbation, public["p_r"])
        derivative = float(np.sqrt(np.mean(np.sum(((plus["pose"] - minus["pose"]) / (2.0 * delta)) ** 2, axis=1))))
        derivatives.append(derivative)
        seconds += plus["seconds"] + minus["seconds"]
        for sign, value in ((1, plus), (-1, minus)):
            probe_rows.append({
                "split": public["split"], "scenario_id": public["scenario_id"],
                "candidate_index": candidate["candidate_index"], "axis": axis, "sign": sign,
                "target_xyz": json.dumps((candidate["target"] + sign * perturbation).tolist()),
                "solution_xyz": json.dumps(value["pose"].tolist()), "normal_equation_residual": value["residual"],
                "objective_before": value["objective_before"], "objective_after": value["objective_after"],
                "solve_seconds": value["seconds"],
            })
    sensitivity = float(np.mean(derivatives))
    pose = result["pose"]
    base_pose = baseline["pose"]
    components = {
        "reprojection_excess": max(0.0, measured_reprojection_error(pose, public) - measured_reprojection_error(base_pose, public)),
        "bone_change": float(np.mean(np.abs(bone_lengths(pose) - bone_lengths(base_pose)))),
        "node_penetration": float(sphere_penetration(pose, public).max()),
        "pose_change": float(np.sqrt(np.mean(np.sum((pose - base_pose) ** 2, axis=1)))),
        "sensitivity": sensitivity,
    }
    cost = sum(components[name] / config[scale] for name, scale in (
        ("reprojection_excess", "risk_reprojection_scale"), ("bone_change", "risk_bone_change_scale"),
        ("node_penetration", "risk_penetration_scale"), ("pose_change", "risk_pose_change_scale"),
        ("sensitivity", "risk_sensitivity_scale"),
    ))
    return {**components, "cost": float(cost), "required_calls": 7, "required_seconds": seconds}


def prepare_scenario(scenario, config, candidate_rows, probe_rows):
    public = scenario["public"]
    solver = QuadraticSolver(public, config)
    baseline = solver.solve()
    hard, soft, risks = [], [], []
    for index, original in enumerate(public["candidates"]):
        candidate = {**original, "candidate_index": index}
        hard_result = solver.solve(candidate["joint"], candidate["target"], 1.0)
        soft_result = solver.solve(candidate["joint"], candidate["target"], public["p_r"])
        risk = candidate_risk(public, candidate, soft_result, baseline, solver, config, probe_rows)
        hard.append(hard_result)
        soft.append(soft_result)
        risks.append(risk)
        candidate_rows.append({
            "split": public["split"], "scenario_id": public["scenario_id"], "candidate_index": index,
            "joint": JOINT_NAMES[candidate["joint"]], "target_xyz": json.dumps(candidate["target"].tolist()),
            "q": float(public["q"][index]), "log_likelihood": public["candidate_log_likelihood"][index],
            "p_r": public["p_r"], **risk,
            "hard_solution_xyz": json.dumps(hard_result["pose"].tolist()),
            "soft_solution_xyz": json.dumps(soft_result["pose"].tolist()),
            "hard_normal_equation_residual": hard_result["residual"],
            "soft_normal_equation_residual": soft_result["residual"],
            "hard_objective_before": hard_result["objective_before"], "hard_objective_after": hard_result["objective_after"],
            "soft_objective_before": soft_result["objective_before"], "soft_objective_after": soft_result["objective_after"],
        })
    top = int(np.argmax(public["q"]))
    utilities = np.log(max(public["p_r"], 1e-300)) + np.log(np.maximum(public["q"], 1e-300)) - config["risk_penalty"] * np.asarray([item["cost"] for item in risks])
    multi = int(np.argmax(utilities))
    margin = float(np.max(public["q"]) - np.min(public["q"]))
    return {
        "scenario": scenario, "baseline": baseline, "hard": hard, "soft": soft, "risks": risks,
        "top": top, "multi": multi, "utilities": utilities,
        "ranks": {"semantic_only": public["p_r"], "margin_only": margin,
                  "sensitivity_only": -risks[top]["sensitivity"], "random": public["random_ranking"],
                  "single_risk": float(utilities[top]), "multi_risk": float(utilities[multi])},
        "solver_checks": {"calls": solver.calls, "seconds": solver.seconds,
                          "maximum_residual": solver.maximum_residual, "maximum_objective_ratio": solver.maximum_objective_ratio},
    }


def geometry_metrics(pose, scenario, config):
    public, truth = scenario["public"], scenario["truth"]
    pose_rmse = float(np.sqrt(np.mean(np.sum((pose - truth["true_pose"]) ** 2, axis=1))))
    bone_error = float(np.mean(np.abs(bone_lengths(pose) - bone_lengths(truth["true_pose"]))))
    penetration = float(sphere_penetration(pose, public).max())
    contact_error = None
    if truth["positive"]:
        candidate = public["candidates"][truth["true_index"]]
        contact_error = float(np.linalg.norm(pose[candidate["joint"]] - candidate["target"]))
    absolute_failure = pose_rmse > config["absolute_pose_rmse_limit"] or bone_error > config["absolute_bone_error_limit"] or penetration > config["absolute_penetration_limit"]
    absolute_failure = absolute_failure or (contact_error is not None and contact_error > config["absolute_contact_error_limit"])
    return {"pose_rmse": pose_rmse, "bone_error": bone_error, "node_penetration": penetration,
            "true_contact_error": contact_error, "absolute_failure": int(absolute_failure)}


def result_row(prepared, method, selected, accepted, solution, calls, seconds, config, score=None, budget=None):
    scenario = prepared["scenario"]
    public, truth = scenario["public"], scenario["truth"]
    baseline = geometry_metrics(prepared["baseline"]["pose"], scenario, config)
    actual = geometry_metrics(solution["pose"], scenario, config)
    increases = {name: actual[name] - baseline[name] for name in ("pose_rmse", "bone_error", "node_penetration")}
    causes = {
        "pose_damage": increases["pose_rmse"] > config["harm_pose_rmse_increase"],
        "bone_damage": increases["bone_error"] > config["harm_bone_error_increase"],
        "penetration_damage": increases["node_penetration"] > config["harm_penetration_increase"],
    }
    harmful = int(any(causes.values()))
    if not accepted:
        assert harmful == 0 and all(abs(value) < 1e-12 for value in increases.values())
    return {
        "split": public["split"], "scenario_id": public["scenario_id"], "method": method, "budget": budget,
        "relation": public["relation"], "positive": int(truth["positive"]), "occluded": int(public["occluded"]),
        "p_r": public["p_r"], "q_top": float(np.max(public["q"])), "score": score,
        "accepted": int(accepted), "selected_index": selected if accepted else -1,
        "assignment_correct": int(selected == truth["true_index"]) if accepted and truth["positive"] else None,
        "new_geometry_damage": harmful, **{key: int(value) for key, value in causes.items()}, **actual,
        "pose_rmse_increase": increases["pose_rmse"], "bone_error_increase": increases["bone_error"],
        "node_penetration_increase": increases["node_penetration"],
        "solver_calls": calls + 1, "solver_seconds": seconds + prepared["baseline"]["seconds"],
    }


def evaluate_methods(prepared, thresholds, config):
    public = prepared["scenario"]["public"]
    truth = prepared["scenario"]["truth"]
    top, multi = prepared["top"], prepared["multi"]
    rows = []
    for method in METHODS:
        accepted, selected, solution, calls, seconds, score = True, top, prepared["soft"][top], 1, prepared["soft"][top]["seconds"], None
        if method == "none":
            accepted, calls, seconds = False, 0, 0.0
        elif method == "hard_top1":
            solution = prepared["hard"][top]
            seconds = solution["seconds"]
        elif method == "single_reject":
            score = prepared["ranks"]["single_risk"]
            accepted = score >= thresholds["single_reject"]
            calls, seconds = prepared["risks"][top]["required_calls"], prepared["risks"][top]["required_seconds"]
        elif method == "multi_risk":
            score = prepared["ranks"]["multi_risk"]
            accepted = score >= thresholds["multi_risk"]
            selected, solution = multi, prepared["soft"][multi]
            calls = sum(item["required_calls"] for item in prepared["risks"])
            seconds = sum(item["required_seconds"] for item in prepared["risks"])
        elif method == "oracle":
            accepted = truth["positive"]
            if accepted:
                selected = truth["true_index"]
                solution = prepared["hard"][selected]
                seconds = solution["seconds"]
            else:
                calls, seconds = 0, 0.0
        if not accepted:
            solution = prepared["baseline"]
        rows.append(result_row(prepared, method, selected, accepted, solution, calls, seconds, config, score))
    return rows


def validation_thresholds(prepared, config):
    count = math.floor(len(prepared) * config["operating_target_coverage"])
    thresholds = {}
    for method, ranking in (("single_reject", "single_risk"), ("multi_risk", "multi_risk")):
        scores = sorted((item["ranks"][ranking] for item in prepared), reverse=True)
        assert 0 < count < len(scores)
        assert scores[count - 1] > scores[count]
        thresholds[method] = float(0.5 * (scores[count - 1] + scores[count]))
    return thresholds


def evaluate_matched(prepared, config):
    rows = []
    for budget in config["matched_coverage_budgets"]:
        count = math.floor(len(prepared) * budget)
        for ranking in RANKINGS:
            order = sorted(range(len(prepared)), key=lambda index: (-prepared[index]["ranks"][ranking], index))
            accepted_indices = set(order[:count])
            for index, item in enumerate(prepared):
                selected = item["multi"] if ranking == "multi_risk" else item["top"]
                accepted = index in accepted_indices
                solution = item["soft"][selected] if accepted else item["baseline"]
                calls, seconds = 1, item["soft"][selected]["seconds"]
                if ranking in ("single_risk", "sensitivity_only"):
                    calls, seconds = item["risks"][selected]["required_calls"], item["risks"][selected]["required_seconds"]
                if ranking == "multi_risk":
                    calls = sum(value["required_calls"] for value in item["risks"])
                    seconds = sum(value["required_seconds"] for value in item["risks"])
                row = result_row(item, ranking, selected, accepted, solution, calls, seconds, config, item["ranks"][ranking], budget)
                potential = result_row(item, ranking, selected, True, item["soft"][selected], calls, seconds, config)
                baseline = result_row(item, ranking, selected, False, item["baseline"], calls, seconds, config)
                for key in ("new_geometry_damage", "absolute_failure", "pose_rmse", "true_contact_error"):
                    row[f"potential_{key}"] = potential[key]
                    row[f"baseline_{key}"] = baseline[key]
                rows.append(row)
    return rows


def average(values):
    values = [value for value in values if value is not None]
    return float(np.mean(values)) if values else None


def summarize(rows):
    groups = sorted({(row["split"], row["budget"], row["method"]) for row in rows}, key=lambda key: (key[0], key[1] or 0.0, key[2]))
    summaries = []
    for split, budget, method in groups:
        values = [row for row in rows if (row["split"], row["budget"], row["method"]) == (split, budget, method)]
        accepted = [row for row in values if row["accepted"]]
        summaries.append({
            "split": split, "budget": budget, "method": method, "scenarios": len(values), "accepted": len(accepted),
            "coverage": len(accepted) / len(values),
            "new_damage_all": average([row["new_geometry_damage"] for row in values]),
            "new_damage_accepted": average([row["new_geometry_damage"] for row in accepted]),
            "absolute_failure_all": average([row["absolute_failure"] for row in values]),
            "pose_rmse": average([row["pose_rmse"] for row in values]),
            "bone_error": average([row["bone_error"] for row in values]),
            "node_penetration": average([row["node_penetration"] for row in values]),
            "positive_contact_error": average([row["true_contact_error"] for row in values]),
            "assignment_accuracy_positive_accepted": average([row["assignment_correct"] for row in accepted]),
            "negative_constraint_acceptance": average([row["accepted"] for row in values if not row["positive"]]),
            "mean_solver_calls": average([row["solver_calls"] for row in values]),
            "mean_solver_ms": 1000.0 * average([row["solver_seconds"] for row in values]),
        })
    return summaries


def statistic(values, metric, sampled, budget_selection=None):
    if budget_selection is not None:
        if metric == "coverage":
            return budget_selection.mean(axis=1)
        key = {"new_damage_accepted": "new_geometry_damage", "new_damage_all": "new_geometry_damage", "absolute_failure_all": "absolute_failure", "positive_contact_error": "true_contact_error"}.get(metric, metric)
        potential = np.asarray([row[f"potential_{key}"] if row[f"potential_{key}"] is not None else np.nan for row in values], dtype=float)[sampled]
        if metric == "new_damage_accepted":
            return np.where(budget_selection, potential, 0.0).sum(axis=1) / budget_selection.sum(axis=1)
        baseline = np.asarray([row[f"baseline_{key}"] if row[f"baseline_{key}"] is not None else np.nan for row in values], dtype=float)[sampled]
        data = np.where(budget_selection, potential, baseline)
        finite = np.isfinite(data)
        result = np.full(len(sampled), np.nan)
        totals = finite.sum(axis=1)
        np.divide(np.where(finite, data, 0.0).sum(axis=1), totals, out=result, where=totals > 0)
        return result
    if metric == "new_damage_accepted":
        accepted = np.asarray([row["accepted"] for row in values], dtype=float)[sampled]
        damage = np.asarray([row["new_geometry_damage"] for row in values], dtype=float)[sampled]
        totals = accepted.sum(axis=1)
        result = np.full(len(sampled), np.nan)
        np.divide(damage.sum(axis=1), totals, out=result, where=totals > 0)
        return result
    key = {"coverage": "accepted", "new_damage_all": "new_geometry_damage", "absolute_failure_all": "absolute_failure", "positive_contact_error": "true_contact_error"}.get(metric, metric)
    data = np.asarray([row[key] if row[key] is not None else np.nan for row in values], dtype=float)[sampled]
    finite = np.isfinite(data)
    totals = finite.sum(axis=1)
    result = np.full(len(sampled), np.nan)
    np.divide(np.where(finite, data, 0.0).sum(axis=1), totals, out=result, where=totals > 0)
    return result


def interval(values):
    finite = values[np.isfinite(values)]
    if not len(finite):
        return None, None, 0
    return float(np.quantile(finite, 0.025)), float(np.quantile(finite, 0.975)), len(finite)


def paired_bootstrap(rows, count, config):
    rng = np.random.default_rng(config["bootstrap_seed"])
    sampled = rng.integers(0, count, size=(config["bootstrap_repetitions"], count))
    metrics = ("coverage", "new_damage_accepted", "new_damage_all", "absolute_failure_all", "pose_rmse", "positive_contact_error")
    grouped = {}
    summaries = {(item["budget"], item["method"]): item for item in summarize(rows)}
    intervals, differences = [], []
    for key in summaries:
        values = sorted([row for row in rows if (row["budget"], row["method"]) == key], key=lambda row: row["scenario_id"])
        assert [row["scenario_id"] for row in values] == list(range(count))
        budget_selection = None
        if key[0] is not None:
            sampled_scores = np.asarray([row["score"] for row in values])[sampled]
            ordering = np.argsort(-sampled_scores, axis=1, kind="stable")
            budget_selection = np.zeros_like(sampled_scores, dtype=bool)
            np.put_along_axis(budget_selection, ordering[:, :math.floor(count * key[0])], True, axis=1)
            assert np.all(budget_selection.sum(axis=1) == math.floor(count * key[0]))
        grouped[key] = {metric: statistic(values, metric, sampled, budget_selection) for metric in metrics}
        for metric in metrics:
            lower, upper, valid = interval(grouped[key][metric])
            intervals.append({"budget": key[0], "method": key[1], "metric": metric, "estimate": summaries[key][metric],
                              "lower_95": lower, "upper_95": upper, "valid_bootstrap_repetitions": valid})
    for budget, method in summaries:
        references = ["calibrated_soft_top1"] if budget is None else ["random"]
        if method == "multi_risk":
            references.extend(["none", "single_reject"] if budget is None else ["single_risk", "margin_only", "semantic_only"])
        for reference in references:
            reference_key = (budget, reference)
            if method == reference or reference_key not in grouped:
                continue
            for metric in metrics:
                delta = grouped[(budget, method)][metric] - grouped[reference_key][metric]
                lower, upper, valid = interval(delta)
                estimate = None if summaries[(budget, method)][metric] is None or summaries[reference_key][metric] is None else summaries[(budget, method)][metric] - summaries[reference_key][metric]
                differences.append({"budget": budget, "method": method, "reference": reference, "metric": metric,
                                    "estimate_difference": estimate, "lower_95": lower, "upper_95": upper,
                                    "valid_bootstrap_repetitions": valid})
    digest = hashlib.sha256(sampled.tobytes()).hexdigest()
    return intervals, differences, digest


def semantic_bins(rows):
    values = [row for row in rows if row["method"] == "hard_top1"]
    bins = []
    for lower, upper in ((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0000001)):
        selected = [row for row in values if lower <= row["p_r"] < upper]
        bins.append({"lower": lower, "upper": min(1.0, upper), "count": len(selected),
                     "mean_p_r": average([row["p_r"] for row in selected]),
                     "observed_positive_fraction": average([row["positive"] for row in selected]),
                     "new_damage_rate": average([row["new_geometry_damage"] for row in selected])})
    return bins


def stratified_results(rows):
    populations = [("relation_truth", "positive", lambda row: row["positive"] == 1),
                   ("relation_truth", "negative", lambda row: row["positive"] == 0),
                   ("observation", "occluded", lambda row: row["occluded"] == 1),
                   ("observation", "visible", lambda row: row["occluded"] == 0)]
    populations.extend(("relation", relation, lambda row, name=relation: row["relation"] == name)
                       for relation in ("holding", "sitting on", "standing on"))
    summaries = []
    for factor, value, predicate in populations:
        summaries.extend({"factor": factor, "value": value, **item} for item in summarize([row for row in rows if predicate(row)]))
    causes = []
    for method in METHODS:
        values = [row for row in rows if row["method"] == method]
        accepted = [row for row in values if row["accepted"]]
        causes.append({"method": method, "accepted": len(accepted),
                       **{name: sum(row[name] for row in accepted) for name in ("new_geometry_damage", "pose_damage", "bone_damage", "penetration_damage")}})
    return summaries, causes


def plot_results(summary, intervals, matched_summary, prepared, test_rows, directory):
    by_method = {row["method"]: row for row in summary if row["split"] == "test"}
    ci = {(row["method"], row["metric"]): row for row in intervals if row["budget"] is None}
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for method in METHODS:
        row = by_method[method]
        if row["new_damage_accepted"] is None:
            continue
        bounds = ci[(method, "new_damage_accepted")]
        axes[0].errorbar(row["coverage"], row["new_damage_accepted"], yerr=[[row["new_damage_accepted"] - bounds["lower_95"]], [bounds["upper_95"] - row["new_damage_accepted"]]], marker="o", capsize=3, label=method)
    axes[0].set(xlabel="Constraint coverage", ylabel="New geometric damage / accepted", xlim=(-0.02, 1.02))
    axes[0].legend(fontsize=7)
    axes[1].bar(range(len(METHODS)), [by_method[method]["pose_rmse"] for method in METHODS])
    axes[1].set_xticks(range(len(METHODS)), METHODS, rotation=35, ha="right", fontsize=7)
    axes[1].set(ylabel="Pose RMSE (m), all test scenarios")
    for axis in axes:
        axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(directory / "strategy_comparison.png", dpi=180)
    plt.close(figure)
    figure, axis = plt.subplots(figsize=(8.5, 5))
    for ranking in RANKINGS:
        selected = sorted([row for row in matched_summary if row["method"] == ranking], key=lambda row: row["coverage"])
        axis.plot([row["coverage"] for row in selected], [row["new_damage_accepted"] for row in selected], marker="o", label=ranking)
    axis.set(xlabel="Exact test budget / scenario count", ylabel="New geometric damage / accepted")
    axis.grid(alpha=0.2)
    axis.legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(directory / "matched_coverage_comparison.png", dpi=180)
    plt.close(figure)
    # 顺序案例和按明确失败规则选取的案例分别记录，统计仍使用全部测试场景。
    case_ids = [0, 1, 2, 3]
    reasons = {index: "fixed_test_index" for index in case_ids}
    for reason, predicate in (
        ("accepted_multi_geometry_damage", lambda row: row["accepted"] and row["new_geometry_damage"]),
        ("rejected_positive_relation", lambda row: not row["accepted"] and row["positive"]),
        ("correct_correspondence_geometry_damage", lambda row: row["assignment_correct"] == 1 and row["new_geometry_damage"]),
    ):
        eligible = [row["scenario_id"] for row in test_rows if row["method"] == "multi_risk" and predicate(row)]
        if eligible:
            selected = min(eligible)
            if selected not in reasons:
                case_ids.append(selected)
                reasons[selected] = reason
    figure, axes = plt.subplots(len(case_ids), 2, figsize=(11, 3.75 * len(case_ids)))
    case_records = []
    colors = ("black", "tab:blue", "tab:red", "tab:green")
    for row_index, scenario_id in enumerate(case_ids):
        item = prepared[scenario_id]
        public, truth = item["scenario"]["public"], item["scenario"]["truth"]
        poses = (truth["true_pose"], item["baseline"]["pose"], item["hard"][item["top"]]["pose"], item["soft"][item["multi"]]["pose"])
        for axis_index, dimensions in enumerate(((0, 1), (0, 2))):
            axis = axes[row_index, axis_index]
            for pose, color, label in zip(poses, colors, ("truth", "no constraint", "hard top1", "multi selected (before reject)")):
                for joint in range(1, 7):
                    segment = pose[[joint, PARENTS[joint]]][:, dimensions]
                    axis.plot(segment[:, 0], segment[:, 1], color=color, alpha=0.7)
                axis.scatter(pose[:, dimensions[0]], pose[:, dimensions[1]], color=color, s=10, label=label)
            axis.add_patch(plt.Circle(public["center"][list(dimensions)], public["radius"], fill=False, color="purple", label="sphere projection"))
            axis.set_aspect("equal", adjustable="datalim")
            axis.set(xlabel="x (m)", ylabel=("y (m)" if axis_index == 0 else "z depth (m)"), title=f"test {scenario_id}: {public['relation']}, positive={int(truth['positive'])}")
            axis.grid(alpha=0.2)
            if row_index == 0 and axis_index == 0:
                axis.legend(fontsize=6)
        case_records.append({"scenario_id": scenario_id, "relation": public["relation"], "positive": int(truth["positive"]),
                             "selection_reason": reasons[scenario_id],
                             "true_index": truth["true_index"], "top_index": item["top"], "multi_index": item["multi"],
                             "truth_xyz": truth["true_pose"].tolist(), "baseline_xyz": poses[1].tolist(),
                             "hard_xyz": poses[2].tolist(), "multi_before_reject_xyz": poses[3].tolist()})
    figure.tight_layout()
    figure.savefig(directory / "fixed_case_geometry_comparison.png", dpi=170)
    plt.close(figure)
    return case_records


def fmt(value, digits=4):
    return "不适用" if value is None else f"{value:.{digits}f}"


def markdown_table(headers, values):
    return "| " + " | ".join(headers) + " |\n|" + "|".join("---" for _ in headers) + "|\n" + "\n".join("| " + " | ".join(str(item) for item in row) + " |" for row in values)


def write_report(directory, config, summary, matched_summary, intervals, differences, thresholds, checks, bins, strata, causes, fixed_cases, test_rows):
    test = [row for row in summary if row["split"] == "test"]
    validation = [row for row in summary if row["split"] == "validation"]
    main_table = markdown_table(
        ("策略", f"接受数/{config['test_count']}", "覆盖率", "接受约束新增损害率", "全部场景绝对失败率", "姿态RMSE/m", "骨长误差/m", "节点穿入深度/m", "正例接触误差/m"),
        [(LABELS[row["method"]], f"{row['accepted']}/{row['scenarios']}", *[fmt(row[key]) for key in ("coverage", "new_damage_accepted", "absolute_failure_all", "pose_rmse", "bone_error", "node_penetration", "positive_contact_error")]) for row in test],
    )
    budget_table = markdown_table(
        ("测试预算", "排序/选择", "覆盖率", "接受约束新增损害率", "全部场景绝对失败率", "姿态RMSE/m", "正例接触误差/m"),
        [(fmt(row["budget"], 1), row["method"], *[fmt(row[key]) for key in ("coverage", "new_damage_accepted", "absolute_failure_all", "pose_rmse", "positive_contact_error")]) for row in matched_summary],
    )
    cost_table = markdown_table(
        ("策略", "每场景平均线性求解次数", "每场景平均求解与核验时间/ms", "接受正例对应准确率", "负例约束接受率"),
        [(LABELS[row["method"]], fmt(row["mean_solver_calls"], 2), fmt(row["mean_solver_ms"], 3), fmt(row["assignment_accuracy_positive_accepted"]), fmt(row["negative_constraint_acceptance"])) for row in test],
    )
    comparison_rows = [row for row in differences if row["budget"] is None and row["reference"] == "calibrated_soft_top1" and row["method"] in ("single_reject", "multi_risk") and row["metric"] in ("new_damage_accepted", "pose_rmse", "positive_contact_error")]
    difference_table = markdown_table(
        ("策略减关系后验加权单对应", "指标", "配对差值", "95%区间"),
        [(LABELS[row["method"]], row["metric"], fmt(row["estimate_difference"]), f"[{fmt(row['lower_95'])}, {fmt(row['upper_95'])}]") for row in comparison_rows],
    )
    threshold_table = markdown_table(
        ("策略", "验证阈值", "验证覆盖率", "测试覆盖率"),
        [(LABELS[method], fmt(thresholds[method], 6), fmt(next(row for row in validation if row["method"] == method)["coverage"]), fmt(next(row for row in test if row["method"] == method)["coverage"])) for method in ("single_reject", "multi_risk")],
    )
    semantic_table = markdown_table(
        ("关系后验区间", "测试场景数", "平均后验", "真实正例比例", "硬约束新增损害率"),
        [(f"[{row['lower']:.2f}, {row['upper']:.2f}]", row["count"], fmt(row["mean_p_r"]), fmt(row["observed_positive_fraction"]), fmt(row["new_damage_rate"])) for row in bins],
    )
    matched_difference_table = markdown_table(
        ("相同覆盖预算", "多候选减单对应效用排序的指标", "配对差值", "95%区间"),
        [(fmt(row["budget"], 1), row["metric"], fmt(row["estimate_difference"]), f"[{fmt(row['lower_95'])}, {fmt(row['upper_95'])}]")
         for row in differences if row["budget"] is not None and row["method"] == "multi_risk" and row["reference"] == "single_risk"
         and row["metric"] in ("new_damage_accepted", "pose_rmse", "positive_contact_error")],
    )
    subgroup_table = markdown_table(
        ("分层", "策略", "场景数", "接受数", "接受约束新增损害率", "姿态RMSE/m", "正例接触误差/m"),
        [(row["value"], LABELS[row["method"]], row["scenarios"], row["accepted"], fmt(row["new_damage_accepted"]), fmt(row["pose_rmse"]), fmt(row["positive_contact_error"]))
         for row in strata if row["factor"] in ("relation_truth", "observation") and row["method"] in ("hard_top1", "calibrated_soft_top1", "single_reject", "multi_risk")],
    )
    cause_table = markdown_table(
        ("策略", "接受数", "新增损害场景", "姿态恶化", "骨长恶化", "节点穿入恶化"),
        [(LABELS[row["method"]], row["accepted"], row["new_geometry_damage"], row["pose_damage"], row["bone_damage"], row["penetration_damage"]) for row in causes],
    )
    failure_rows = []
    for case in fixed_cases:
        if case["selection_reason"] == "fixed_test_index":
            continue
        for method in ("none", "hard_top1", "multi_risk"):
            row = next(value for value in test_rows if value["scenario_id"] == case["scenario_id"] and value["method"] == method)
            failure_rows.append((case["scenario_id"], case["selection_reason"], LABELS[method], row["accepted"], row["new_geometry_damage"],
                                 fmt(row["pose_rmse"]), fmt(row["bone_error"]), fmt(row["node_penetration"]), fmt(row["true_contact_error"])))
    failure_table = markdown_table(("测试编号", "选择规则", "策略", "接受", "新增损害", "姿态RMSE/m", "骨长误差/m", "节点穿入/m", "正例接触误差/m"), failure_rows)
    main_by_method = {row["method"]: row for row in test}
    multi = main_by_method["multi_risk"]
    baseline = main_by_method["none"]
    matched_multi = next(row for row in matched_summary if row["budget"] == 0.8 and row["method"] == "multi_risk")
    matched_single = next(row for row in matched_summary if row["budget"] == 0.8 and row["method"] == "single_risk")
    text = f"""# 受控三维接口与几何损害实验

## 实验范围与完成内容

日期：2026-11-04。本实验在自生成的七个节点骨架、球体表面与正交相机问题上，完整执行关系观测、对应评分、三维二次优化、几何损害评估、验证阈值选择、独立测试和配对置信区间计算。每个长度量均使用米。验证随机种子为 `{config['validation_seed']}`，包含{config['validation_count']}个场景；测试随机种子为 `{config['test_seed']}`，包含{config['test_count']}个场景。

该实验用于检查指定生成分布中的约束接口行为。人体使用七个节点，球体几何已知；正交二维观测与可见深度由真实三维状态加噪声生成。它提供可复跑的数学机制检验。真实图片中的接触对应、人体表面、网格穿透和公开三维重建后端仍缺少完整实验，本结果不作为指南第八节真实三维核心实验已经完成的证据。

## 生成分布、真实接触和观测

关系类型等概率选取 `holding`、`sitting on`、`standing on`，分别对应手部、髋部和脚部候选。正例概率为{config['positive_prevalence']:.2f}。先生成具有身体朝向、身体尺度和肢体方向变化的真实骨架，再放置球体，使正例的真实节点精确位于球面。负例的球体与全部真实节点保持至少{config['negative_surface_gap_min']:.2f}米表面间隔，真实对应记为缺失。两个候选均由一个节点和一个球面点组成，顺序随机打乱。

初始骨架在真实节点上加入独立高斯噪声，三个坐标轴的标准差为`{config['initial_sigma_xyz']}`米，再乘以[{config['initial_noise_scale_range'][0]}, {config['initial_noise_scale_range'][1]}]中的场景系数。二维正交观测的标准差为{config['image_noise_sigma']}米，可见深度标准差为{config['depth_noise_sigma']}米；不可见坐标不进入似然或优化。遮挡标记控制候选部位的观测缺失，它只描述本生成器中的缺失机制。

### 关系证据 p_r 与对应评分 q_c

令关系真值为Y，合成语义传感量z在正负类别下服从共同标准差{config['semantic_noise_sigma']}、均值分别为{config['semantic_positive_mean']}与{config['semantic_negative_mean']}的高斯分布。`p_r=P(Y=1|z)`按贝叶斯公式计算：

```text
logit(p_r) = log(pi/(1-pi)) + (mu_positive-mu_negative)
             * (z-(mu_positive+mu_negative)/2) / sigma_z^2
```

这里的校准依据来自已知生成分布。有限测试样本中的后验与频率见下表，不能据此解释真实RelateAnything分数的校准情况。

{semantic_table}

对于候选c，用初始骨架构造假设模板，将该候选节点放到指定球面点，其余节点保持初始位置。所有候选使用完全相同的可观测坐标集合，根据二维和可见深度的高斯残差计算完整观测似然，再用等先验归一化得到`q_c`。候选评分函数只接收初始化、观测、可见性、球面点和噪声参数。它不会读取真实对应或真实姿态；q属于该假设模板模型的评分，当前没有为q提供真实图像上的校准保证。

## 同一三维优化后端

所有策略共享严格凸二次目标。变量X包含七个三维节点；X0为初始骨架，U为可见观测，D为六条骨骼边的差分矩阵，M为可见坐标掩码。对一个指定候选(j,t)，目标由以下项组成：

```text
E(X) = sum_d lambda_prior,d * ||X_d-X0_d||^2
     + sum_visible lambda_observation,d * (X-U)^2
     + lambda_bone * ||D(X-X0)||^2
     + support / sigma_contact^2 * ||X_j-t||^2
```

先验精度取初始噪声方差的倒数，观测精度取对应观测方差的倒数，骨骼向量保持项标准差为{config['bone_offset_sigma']}米，接触标准差为{config['contact_sigma']}米。骨骼保持项使用初始骨架的边向量，真实骨长只在独立评测中使用。三个坐标轴分别求解一个7×7正定线性系统，得到全局最小值；无接触约束时仍执行同一后端。

全运行完成{checks['solver_calls']}次线性系统批量求解，最大相对正规方程残差为`{checks['maximum_normal_equation_residual']:.3e}`。每次求解均断言结果有限、残差低于{config['normal_equation_tolerance']:.0e}，并独立计算目标值，确认其不高于初始骨架目标值。正例真实接触和两个球面候选也逐场景通过几何断言。

## 独立评测与新增损害定义

每个策略均计算真实姿态节点RMSE（`sqrt(mean_j ||X_j-X_true,j||^2)`）、真实骨长平均绝对误差、节点进入球体的最大深度，以及正例真实节点到真实接触点的欧氏距离。节点穿入深度只检查七个点，不能解释为人体网格穿透。

对每个场景，先运行无接触约束后端，随后定义新增损害：姿态RMSE增加超过{config['harm_pose_rmse_increase']}米、骨长误差增加超过{config['harm_bone_error_increase']}米，或最大节点穿入深度增加超过{config['harm_penetration_increase']}米，任意条件满足即计入。对应是否正确单独统计，不进入几何损害标签。拒绝约束时复用无约束后端的完整几何结果，因此新增损害为零，绝对失败仍照常评测。

绝对失败阈值为姿态RMSE>{config['absolute_pose_rmse_limit']}米、骨长误差>{config['absolute_bone_error_limit']}米、节点穿入深度>{config['absolute_penetration_limit']}米，或正例真实接触误差>{config['absolute_contact_error_limit']}米。所有阈值在配置中固定，只界定本实验的误差容忍范围，不作为物理安全标准。接受集为空时，接受约束新增损害率和置信区间均记为不适用。

## 六种策略、几何代价与敏感性

| 策略 | 约束决策 |
|---|---|
| 无接触约束 | 使用先验、观测和骨骼向量保持项 |
| 最高对应硬约束 | 采用q最高的候选，support=1 |
| 关系后验加权单对应 | 采用q最高的候选，support=p_r |
| 单对应选择性拒绝 | 优化q最高候选，按对应效用选择是否接受 |
| 多候选几何代价选择 | 分别优化两个候选，选择效用最高的完整结果，再决定是否接受 |
| 真实对应参考 | 正例采用真实对应和support=1，负例采用无接触约束后端 |

真实对应参考提供已知对应条件，几何质量仍受观测、初始化和目标函数影响；它不具有几何误差最小的数学保证。多候选策略输出一个完整解，当前实验不评价同时保留多个解的接口。

几何代价C只使用当前可观测数据和优化结果：相对无约束结果的二维重投影RMSE增加量、骨长变化、当前球体节点穿入深度、节点位置变化以及接触目标敏感性。前四项分别除以配置中的{config['risk_reprojection_scale']}、{config['risk_bone_change_scale']}、{config['risk_penetration_scale']}、{config['risk_pose_change_scale']}米；敏感性除以{config['risk_sensitivity_scale']}。敏感性在三个坐标方向分别将接触点扰动±{config['finite_difference_delta']}米，通过六次独立求解计算中央差分的姿态RMS导数，再对三个方向取平均。它作为启发式几何量参与决策。

```text
utility(c) = log(p_r) + log(q_c) - {config['risk_penalty']} * C(c)
```

效用函数未读取真实姿态、关系真值、真实对应或评测损害标签。单对应策略仅检查q最高的一个候选；多候选策略检查两个候选。固定覆盖目标为{config['operating_target_coverage']:.0%}，阈值完全由验证集效用确定，测试集沿用相同阈值：

{threshold_table}

## 独立测试结果

表格中的平均误差与绝对失败率覆盖全部{config['test_count']}个测试场景，接受约束新增损害率以接受场景为分母。正例接触误差包含被拒绝的正例，避免只展示容易接受的样本。

{main_table}

多候选策略在验证阈值下接受{multi['accepted']}个场景，接受约束新增损害率为{multi['new_damage_accepted']:.2%}。正例接触误差为{multi['positive_contact_error']:.5f}米，无约束结果为{baseline['positive_contact_error']:.5f}米；全部场景姿态RMSE为{multi['pose_rmse']:.5f}米，无约束结果为{baseline['pose_rmse']:.5f}米。接触拟合改善与整体姿态质量需要同时判断，这些量没有被合并成一个总分。

![六种策略的独立测试覆盖、损害区间和全部场景姿态误差](strategy_comparison.png)

### 配对不确定性

使用{config['bootstrap_repetitions']}次按完整场景抽样的bootstrap，所有方法共用同一重采样索引。下表给出相对关系后验加权单对应的差值，负数表示该指标降低；选择性策略的接受集可能不同，因此条件损害率差值仍需结合覆盖率理解。

{difference_table}

完整逐方法区间、同预算比较的配对差值和有效bootstrap次数分别保存在[`bootstrap_intervals.csv`](evidence/bootstrap_intervals.csv)与[`paired_differences.csv`](evidence/paired_differences.csv)。验证阈值实验固定部署决策；同预算实验在每次共享重采样之后重新按无真值分数排序，始终保持规定的接受数量。区间反映给定生成分布内的抽样波动，不包含真实图片域迁移或模型失配的不确定性；随机排序使用一个固定随机种子，其区间也没有纳入额外随机种子的变化。

## 相同测试输出预算的排序比较

额外固定测试集接受数量，分别取80%、60%、40%的场景，比较关系后验、对应间隔、负敏感性、独立随机排序、单对应效用和多候选效用。前五种排序接受后使用同一个关系后验加权最高对应结果；多候选排序使用所选完整候选结果。所有排序均不读取测试标签。这里按整批未标注测试分数分配精确数量，属于已知批次预算的描述性比较，与前面的验证阈值部署实验分别报告。

{budget_table}

相同预算下，多候选选择与单对应效用排序的配对差值为：

{matched_difference_table}

在80%精确输出预算下，多候选与单对应效用排序的新增损害率分别为{matched_multi['new_damage_accepted']:.3%}与{matched_single['new_damage_accepted']:.3%}。两者拥有相同输出数量，计算成本见后文；该比较仅支持给定生成器、目标和阈值的受控结果。

![相同测试预算下六种排序的新增几何损害率](matched_coverage_comparison.png)

## 分层结果与失败构成

以下按关系正负和观测遮挡分别分层，两个分层维度相互重叠。它们用于解释整体结果，未用于调整阈值或筛选测试样本；细分样本的点估计属于探索性描述。三种关系类型、全部六种方法的完整结果见[`stratified_results.csv`](evidence/stratified_results.csv)。

{subgroup_table}

新增损害的三个条件可以同时发生，下面的原因数量不能相加当作总损害数量：

{cause_table}

对应正确仍可能伴随姿态、骨长或节点穿入的恶化。原因是接触目标与初始骨架、噪声观测以及边向量保持项共同参与优化；正确对应只解决目标身份，无法保证其它几何指标均改善。负例上的任何约束接受单独报告为负例约束接受率，几何损害仍通过同一误差增量定义。

附加案例按三条确定规则取最小测试编号：多候选接受但几何受损、正例被拒绝、对应正确但几何受损。规则重复选到同一编号时只展示一次。下表完整列出每个案例的无约束、硬约束和最终多候选结果，全部坐标与投影图共同提供依据。

{failure_table}

## 计算预算和完整几何案例

下表包含共享无约束求解。单对应几何检查需要一个候选求解和六次扰动求解，多候选几何检查需要两个候选及十二次扰动求解。无接触约束需要一次求解，常规单对应需要两次。时间包含线性求解、目标值计算和残差断言，未包含数据生成、bootstrap和文件写入；完整运行时间见[`run_checks.json`](evidence/run_checks.json)。各方法通过共享缓存计算比较结果，表格按照每种方法实际需要读取的求解结果核算调用和时间，不能解释为分别运行各方法的端到端测速。

{cost_table}

图像先展示固定测试编号0、1、2、3，再展示前述确定规则选出的失败案例。每个案例同时呈现真实骨架、无接触约束结果、硬约束结果、多候选所选结果与球体的XY/XZ投影。多候选曲线展示拒绝决策之前的候选解，全部节点坐标和选择理由保存在[`fixed_cases.json`](evidence/fixed_cases.json)，最终是否接受以逐场景结果表为准。案例只用于解释，全部统计均使用完整测试集。

![固定编号和确定失败规则案例的真实状态与三种输出双视图比较](fixed_case_geometry_comparison.png)

## 结果解释与适用条件

正例、负例、缺失观测、噪声和关系后验的联系由生成器规定。表格量化这些设定与指定优化器共同产生的结果，不能作为真实关系模型中“语义分数无法预测损害”的独立发现。几何代价和中央差分敏感性均为明确的启发式分析量，它们的实际价值以相同预算结果与配对区间为依据，不预设复杂策略优于简单策略。出现区间覆盖零或复杂策略误差更高时，应保留该结果。

本实验落实了指南第7.4节的数学敏感性测量，以及第8节第二、第三组对照的合成机制检查。真实三维核心实验仍需要独立接触/表面标注、真实图片初始化、统一人体与物体几何、固定公开重建后端，以及真实遮挡条件下的测试。本实验不填补这些证据缺口。

## 可复跑交付与术语

运行命令：

```powershell
.\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\controlled_3d_damage_study.py --config HOR\\research\\configs\\controlled_3d.json
.\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\audit_controlled_3d.py
```

| 文件 | 内容 |
|---|---|
| [`controlled_3d_damage_study.py`](../../scripts/controlled_3d_damage_study.py) | 生成、似然、求解、决策、评测、配对bootstrap及本报告生成 |
| [`audit_controlled_3d.py`](../../scripts/audit_controlled_3d.py) | 独立读取证据，以逐边梯度、原始几何和统计结果核验求解与评测 |
| [`controlled_3d.json`](../../configs/controlled_3d.json) | 全部随机种子、噪声、目标权重、阈值和输出目录 |
| [`scenarios.json`](evidence/scenarios.json) | 全部800个场景的公开输入、真实几何、可见性、真实对应和噪声参数 |
| [`candidate_solutions.csv`](evidence/candidate_solutions.csv) | 每个候选的分数、全部解坐标、几何代价、敏感性和求解残差 |
| [`baseline_solutions.csv`](evidence/baseline_solutions.csv) | 全部验证/测试无接触约束解的坐标、目标值与求解残差 |
| [`sensitivity_probes.csv`](evidence/sensitivity_probes.csv) | 每个候选三轴正负扰动的目标、全部解坐标和求解验证 |
| [`scenario_results.csv`](evidence/scenario_results.csv) | 六种方法的全部验证/测试结果及统一几何指标 |
| [`matched_budget_results.csv`](evidence/matched_budget_results.csv) | 相同测试输出数量的全部逐场景结果 |
| [`stratified_results.csv`](evidence/stratified_results.csv)；[`damage_causes.csv`](evidence/damage_causes.csv) | 正负、遮挡、关系类型分层与重叠损害原因 |
| [`summary.json`](evidence/summary.json)；[`matched_summary.json`](evidence/matched_summary.json) | 表格完整数值 |
| [`validation_thresholds.json`](evidence/validation_thresholds.json) | 验证确定的阈值和冻结配置哈希 |
| [`run_checks.json`](evidence/run_checks.json) | 求解残差、求解数量、耗时、环境、真值数量和共享抽样索引哈希 |
| [`manifest.json`](evidence/manifest.json) | 文件大小与SHA-256；包含脚本、配置和本报告 |

`p_r`表示由合成语义观测得到的关系后验；`q_c`表示指定模板噪声模型下的候选归一化评分；RMSE表示均方根误差；CI表示置信区间；Oracle表示只在参考组提供真实关系与对应；正规方程残差检验线性求解是否满足目标函数的一阶最优条件。球体节点穿入度量只检查七个节点的位置。
"""
    (directory / "受控三维接口损害实验.md").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    args.config = args.config.resolve()
    config_bytes = args.config.read_bytes()
    config = json.loads(config_bytes.decode("utf-8"))
    directory = ROOT / config["report_directory"]
    evidence = directory / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    validation = make_scenarios(config["validation_seed"], config["validation_count"], "validation", config)
    test = make_scenarios(config["test_seed"], config["test_count"], "test", config)
    candidate_rows, probe_rows = [], []
    prepared_validation = [prepare_scenario(scenario, config, candidate_rows, probe_rows) for scenario in validation]
    thresholds = validation_thresholds(prepared_validation, config)
    prepared_test = [prepare_scenario(scenario, config, candidate_rows, probe_rows) for scenario in test]
    assert config["validation_seed"] != config["test_seed"]
    validation_hashes = {hashlib.sha256(item["truth"]["true_pose"].tobytes()).hexdigest() for item in validation}
    test_hashes = {hashlib.sha256(item["truth"]["true_pose"].tobytes()).hexdigest() for item in test}
    assert not validation_hashes & test_hashes
    results = [row for item in prepared_validation + prepared_test for row in evaluate_methods(item, thresholds, config)]
    matched = evaluate_matched(prepared_test, config)
    test_rows = [row for row in results if row["split"] == "test"]
    summary, matched_summary = summarize(results), summarize(matched)
    intervals, differences, bootstrap_digest = paired_bootstrap(test_rows + matched, len(test), config)
    bins = semantic_bins(test_rows)
    strata, causes = stratified_results(test_rows)
    fixed_cases = plot_results(summary, intervals, matched_summary, prepared_test, test_rows, directory)
    all_prepared = prepared_validation + prepared_test
    checks = {
        "validation_seed": config["validation_seed"], "test_seed": config["test_seed"],
        "validation_count": len(validation), "test_count": len(test),
        "validation_positive": sum(item["truth"]["positive"] for item in validation),
        "test_positive": sum(item["truth"]["positive"] for item in test),
        "source_geometry_hash_intersection": len(validation_hashes & test_hashes),
        "solver_calls": sum(item["solver_checks"]["calls"] for item in all_prepared),
        "solver_seconds": sum(item["solver_checks"]["seconds"] for item in all_prepared),
        "maximum_normal_equation_residual": max(item["solver_checks"]["maximum_residual"] for item in all_prepared),
        "maximum_objective_ratio_after_before": max(item["solver_checks"]["maximum_objective_ratio"] for item in all_prepared),
        "sensitivity_min": min(item["sensitivity"] for item in candidate_rows),
        "sensitivity_max": max(item["sensitivity"] for item in candidate_rows),
        "test_multi_changes_candidate": sum(item["top"] != item["multi"] for item in prepared_test),
        "shared_bootstrap_indices_sha256": bootstrap_digest,
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(), "numpy_version": np.__version__, "matplotlib_version": matplotlib.__version__,
        "platform": platform.platform(), "full_run_seconds_before_final_report": perf_counter() - started,
        "bayes_semantic_brier_test": average([(row["p_r"] - row["positive"]) ** 2 for row in test_rows if row["method"] == "none"]),
    }
    write_json(evidence / "scenarios.json", validation + test)
    write_csv(evidence / "baseline_solutions.csv", [{
        "split": item["scenario"]["public"]["split"], "scenario_id": item["scenario"]["public"]["scenario_id"],
        "solution_xyz": json.dumps(item["baseline"]["pose"].tolist()), "normal_equation_residual": item["baseline"]["residual"],
        "objective_before": item["baseline"]["objective_before"], "objective_after": item["baseline"]["objective_after"],
        "solve_seconds": item["baseline"]["seconds"],
    } for item in all_prepared])
    write_csv(evidence / "candidate_solutions.csv", candidate_rows)
    write_csv(evidence / "sensitivity_probes.csv", probe_rows)
    write_csv(evidence / "scenario_results.csv", results)
    write_csv(evidence / "matched_budget_results.csv", matched)
    write_json(evidence / "summary.json", summary)
    write_json(evidence / "matched_summary.json", matched_summary)
    write_csv(evidence / "bootstrap_intervals.csv", intervals)
    write_csv(evidence / "paired_differences.csv", differences)
    write_csv(evidence / "semantic_posterior_bins.csv", bins)
    write_csv(evidence / "stratified_results.csv", strata)
    write_csv(evidence / "damage_causes.csv", causes)
    write_json(evidence / "validation_thresholds.json", {"thresholds": thresholds, "target_coverage": config["operating_target_coverage"], "config_sha256": checks["config_sha256"]})
    write_json(evidence / "run_checks.json", checks)
    write_json(evidence / "run_config.json", config)
    write_json(evidence / "fixed_cases.json", fixed_cases)
    write_report(directory, config, summary, matched_summary, intervals, differences, thresholds, checks, bins, strata, causes, fixed_cases, test_rows)
    files = [Path(__file__), Path(__file__).with_name("audit_controlled_3d.py"), args.config] + sorted(path for path in directory.rglob("*") if path.is_file() and path.name != "manifest.json")
    write_json(evidence / "manifest.json", [{"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in files])
    print(json.dumps({"checks": checks, "test_summary": [row for row in summary if row["split"] == "test"], "thresholds": thresholds}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
