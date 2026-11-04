import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "HOR/research/reports/controlled_3d/evidence"
PARENTS = (-1, 0, 1, 1, 0, 4, 4)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(name):
    with (EVIDENCE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def key(row):
    return row["split"], int(row["scenario_id"])


def assert_close(actual, expected):
    assert np.allclose(actual, expected, atol=1e-10, rtol=1e-9), (actual, expected)


def independent_objective_and_gradient(scenario, pose, joint, target, support, config):
    public = scenario["public"]
    initial = np.asarray(public["initial"])
    observations = np.asarray(public["observations"])
    observed = np.asarray(public["observed"])
    prior_precision = 1.0 / np.asarray(public["initial_sigma"]) ** 2
    observation_precision = 1.0 / np.asarray([config["image_noise_sigma"], config["image_noise_sigma"], config["depth_noise_sigma"]]) ** 2
    difference = pose - initial
    value = float(np.sum(difference ** 2 * prior_precision))
    gradient = 2.0 * difference * prior_precision
    value += float(np.sum((pose - observations) ** 2 * observed * observation_precision))
    gradient += 2.0 * (pose - observations) * observed * observation_precision
    for child in range(1, 7):
        parent = PARENTS[child]
        residual = difference[child] - difference[parent]
        value += float(np.dot(residual, residual) / config["bone_offset_sigma"] ** 2)
        force = 2.0 * residual / config["bone_offset_sigma"] ** 2
        gradient[child] += force
        gradient[parent] -= force
    if joint is not None:
        residual = pose[joint] - target
        value += float(support * np.dot(residual, residual) / config["contact_sigma"] ** 2)
        gradient[joint] += 2.0 * support * residual / config["contact_sigma"] ** 2
    assert np.max(np.abs(gradient)) < 1e-8
    return value, float(np.max(np.abs(gradient)))


def independent_geometry(scenario, pose, config):
    public, truth = scenario["public"], scenario["truth"]
    actual = np.asarray(truth["true_pose"])
    pose_error = float(np.sqrt(np.sum((pose - actual) ** 2) / 7.0))
    length_differences = []
    for child in range(1, 7):
        parent = PARENTS[child]
        length_differences.append(abs(np.linalg.norm(pose[child] - pose[parent]) - np.linalg.norm(actual[child] - actual[parent])))
    bone_error = float(np.mean(length_differences))
    penetration = float(max(0.0, max(public["radius"] - np.linalg.norm(node - public["center"]) for node in pose)))
    contact = None
    if truth["positive"]:
        correspondence = public["candidates"][truth["true_index"]]
        contact = float(np.linalg.norm(pose[correspondence["joint"]] - correspondence["target"]))
    failure = pose_error > config["absolute_pose_rmse_limit"] or bone_error > config["absolute_bone_error_limit"] or penetration > config["absolute_penetration_limit"]
    failure = failure or (contact is not None and contact > config["absolute_contact_error_limit"])
    return {"pose_rmse": pose_error, "bone_error": bone_error, "node_penetration": penetration,
            "true_contact_error": contact, "absolute_failure": int(failure)}


def main():
    config = read_json(ROOT / "HOR/research/configs/controlled_3d.json")
    checks = read_json(EVIDENCE / "run_checks.json")
    scenarios = {key(item["public"]): item for item in read_json(EVIDENCE / "scenarios.json")}
    baselines = {key(row): row for row in read_csv("baseline_solutions.csv")}
    candidates = {(row["split"], int(row["scenario_id"]), int(row["candidate_index"])): row for row in read_csv("candidate_solutions.csv")}
    assert len(scenarios) == config["validation_count"] + config["test_count"]
    verified_solutions = 0
    maximum_gradient = 0.0
    for scenario_key, scenario in scenarios.items():
        public, truth = scenario["public"], scenario["truth"]
        z = public["semantic_observation"]
        positive_density = np.exp(-0.5 * ((z - config["semantic_positive_mean"]) / config["semantic_noise_sigma"]) ** 2) * config["positive_prevalence"]
        negative_density = np.exp(-0.5 * ((z - config["semantic_negative_mean"]) / config["semantic_noise_sigma"]) ** 2) * (1.0 - config["positive_prevalence"])
        assert_close(public["p_r"], positive_density / (positive_density + negative_density))
        likelihoods = []
        observed = np.asarray(public["observed"], dtype=bool)
        variance = np.asarray(public["initial_sigma"]) ** 2 + np.asarray([config["image_noise_sigma"], config["image_noise_sigma"], config["depth_noise_sigma"]]) ** 2
        for index, candidate in enumerate(public["candidates"]):
            assert_close(np.linalg.norm(np.asarray(candidate["target"]) - public["center"]), public["radius"])
            template = np.asarray(public["initial"]).copy()
            template[candidate["joint"]] = candidate["target"]
            terms = (np.asarray(public["observations"]) - template) ** 2 / variance + np.log(2.0 * np.pi * variance)
            likelihoods.append(float(-0.5 * terms[observed].sum()))
            row = candidates[(*scenario_key, index)]
            for prefix, support in (("hard", 1.0), ("soft", public["p_r"])):
                pose = np.asarray(json.loads(row[f"{prefix}_solution_xyz"]))
                objective, gradient = independent_objective_and_gradient(scenario, pose, candidate["joint"], np.asarray(candidate["target"]), support, config)
                assert_close(objective, float(row[f"{prefix}_objective_after"]))
                maximum_gradient = max(maximum_gradient, gradient)
                verified_solutions += 1
        expected_q = np.exp(np.asarray(likelihoods) - max(likelihoods))
        assert_close(public["q"], expected_q / expected_q.sum())
        if truth["positive"]:
            actual = public["candidates"][truth["true_index"]]
            assert_close(np.asarray(truth["true_pose"])[actual["joint"]], actual["target"])
        else:
            assert truth["true_index"] == -1
            assert np.min(np.linalg.norm(np.asarray(truth["true_pose"]) - public["center"], axis=1)) > public["radius"] + config["negative_surface_gap_min"]
        baseline = baselines[scenario_key]
        pose = np.asarray(json.loads(baseline["solution_xyz"]))
        objective, gradient = independent_objective_and_gradient(scenario, pose, None, None, 0.0, config)
        assert_close(objective, float(baseline["objective_after"]))
        maximum_gradient = max(maximum_gradient, gradient)
        verified_solutions += 1
    for row in read_csv("sensitivity_probes.csv"):
        scenario = scenarios[key(row)]
        candidate = scenario["public"]["candidates"][int(row["candidate_index"])]
        pose = np.asarray(json.loads(row["solution_xyz"]))
        target = np.asarray(json.loads(row["target_xyz"]))
        objective, gradient = independent_objective_and_gradient(scenario, pose, candidate["joint"], target, scenario["public"]["p_r"], config)
        assert_close(objective, float(row["objective_after"]))
        maximum_gradient = max(maximum_gradient, gradient)
        verified_solutions += 1
    assert verified_solutions == checks["solver_calls"]
    result_rows = read_csv("scenario_results.csv") + read_csv("matched_budget_results.csv")
    for row in result_rows:
        scenario = scenarios[key(row)]
        baseline_pose = np.asarray(json.loads(baselines[key(row)]["solution_xyz"]))
        accepted = int(row["accepted"])
        if accepted:
            candidate = candidates[(*key(row), int(row["selected_index"]))]
            prefix = "hard" if row["method"] in ("hard_top1", "oracle") else "soft"
            pose = np.asarray(json.loads(candidate[f"{prefix}_solution_xyz"]))
        else:
            pose = baseline_pose
        baseline = independent_geometry(scenario, baseline_pose, config)
        metrics = independent_geometry(scenario, pose, config)
        for name, expected in metrics.items():
            if expected is None:
                assert row[name] == ""
            else:
                assert_close(float(row[name]), expected)
        damage = int(metrics["pose_rmse"] - baseline["pose_rmse"] > config["harm_pose_rmse_increase"]
                     or metrics["bone_error"] - baseline["bone_error"] > config["harm_bone_error_increase"]
                     or metrics["node_penetration"] - baseline["node_penetration"] > config["harm_penetration_increase"])
        assert damage == int(row["new_geometry_damage"])
    thresholds = read_json(EVIDENCE / "validation_thresholds.json")["thresholds"]
    for method in ("single_reject", "multi_risk"):
        validation = [row for row in result_rows if row["split"] == "validation" and row["method"] == method]
        scores = sorted((float(row["score"]) for row in validation), reverse=True)
        selected_count = int(config["validation_count"] * config["operating_target_coverage"])
        assert_close(thresholds[method], 0.5 * (scores[selected_count - 1] + scores[selected_count]))
    for row in read_csv("bootstrap_intervals.csv"):
        if row["method"] == "none" and row["metric"] == "new_damage_accepted":
            assert row["estimate"] == row["lower_95"] == row["upper_95"] == ""
        if row["budget"] and row["metric"] == "coverage":
            expected = int(config["test_count"] * float(row["budget"])) / config["test_count"]
            assert_close(float(row["lower_95"]), expected)
            assert_close(float(row["upper_95"]), expected)
    for item in read_json(EVIDENCE / "manifest.json"):
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    print(json.dumps({"verified_scenarios": len(scenarios), "verified_solutions": verified_solutions,
                      "verified_result_rows": len(result_rows), "maximum_absolute_objective_gradient": maximum_gradient,
                      "posterior_likelihood_geometry_thresholds_bootstrap_and_manifest": "passed"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
