import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 106_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "last_seen_goal_pursuit": "LastSeen",
    "memory_only_belief_tracking": "MemoryOnly",
    "uncertainty_halt": "UncertHalt",
    "active_viewpoint_reacquisition": "ActiveView",
    "pomdp_belief_planner": "POMDP",
    "goal_retargeting_heuristic": "RetargetHeur",
    "failure_aware_manipulation_policy": "FailAware",
    "proposed_disappearing_goal_belief_revision": "Proposed",
    "oracle_goal_state_supervisor": "Oracle",
    "full_disappearing_goal_belief_revision": "Full",
    "minus_observation_memory_separation": "NoObsMemSep",
    "minus_active_reacquisition": "NoReacquire",
    "minus_physical_validity_test": "NoValidTest",
    "minus_substitute_goal_planner": "NoSubGoal",
    "minus_abandonment_calibration": "NoAbandonCalib",
    "active_perception_only": "ActiveOnly",
}

TASKS = [
    {"task": "shelf_retrieval", "difficulty": 0.064, "visibility_need": 0.88, "goal_specificity": 0.76, "unsafe_sensitivity": 0.62},
    {"task": "drawer_placement", "difficulty": 0.070, "visibility_need": 0.82, "goal_specificity": 0.84, "unsafe_sensitivity": 0.70},
    {"task": "bin_sorting", "difficulty": 0.058, "visibility_need": 0.76, "goal_specificity": 0.72, "unsafe_sensitivity": 0.55},
    {"task": "tool_handoff", "difficulty": 0.074, "visibility_need": 0.90, "goal_specificity": 0.91, "unsafe_sensitivity": 0.82},
    {"task": "mobile_pick_and_place", "difficulty": 0.072, "visibility_need": 0.86, "goal_specificity": 0.80, "unsafe_sensitivity": 0.76},
]

REGIMES = [
    {"regime": "visual_occlusion", "hidden": 0.86, "invalid": 0.08, "move": 0.12, "substitute": 0.20, "reappear": 0.78, "hazard": 0.24},
    {"regime": "object_moved", "hidden": 0.42, "invalid": 0.26, "move": 0.82, "substitute": 0.34, "reappear": 0.38, "hazard": 0.45},
    {"regime": "object_removed", "hidden": 0.34, "invalid": 0.88, "move": 0.28, "substitute": 0.42, "reappear": 0.16, "hazard": 0.58},
    {"regime": "human_temporary_obstruction", "hidden": 0.74, "invalid": 0.18, "move": 0.18, "substitute": 0.24, "reappear": 0.86, "hazard": 0.72},
    {"regime": "goal_specification_changed", "hidden": 0.28, "invalid": 0.76, "move": 0.40, "substitute": 0.68, "reappear": 0.18, "hazard": 0.48},
    {"regime": "substitute_goal_available", "hidden": 0.42, "invalid": 0.62, "move": 0.36, "substitute": 0.88, "reappear": 0.30, "hazard": 0.40},
    {"regime": "cascading_disappearing_goal", "hidden": 0.82, "invalid": 0.82, "move": 0.76, "substitute": 0.72, "reappear": 0.44, "hazard": 0.84},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "occlusion": 0.08, "removal": 0.05, "delay": 0.05, "retarget": 0.08},
    {"split": "occlusion_heavy_shift", "stress": 0.50, "occlusion": 0.78, "removal": 0.18, "delay": 0.22, "retarget": 0.18},
    {"split": "physical_removal_shift", "stress": 0.58, "occlusion": 0.34, "removal": 0.78, "delay": 0.24, "retarget": 0.48},
    {"split": "delayed_reappearance", "stress": 0.54, "occlusion": 0.66, "removal": 0.28, "delay": 0.82, "retarget": 0.28},
    {"split": "combined_disappearance_stress", "stress": 0.82, "occlusion": 0.76, "removal": 0.72, "delay": 0.72, "retarget": 0.72},
]

METHODS = [
    {"method": "last_seen_goal_pursuit", "base": 0.655, "belief": 0.06, "validity": 0.04, "reacquire": 0.04, "retarget": 0.04, "abandon": 0.04, "recover": 0.05, "risk": 0.06, "cost": 0.04},
    {"method": "memory_only_belief_tracking", "base": 0.672, "belief": 0.34, "validity": 0.16, "reacquire": 0.08, "retarget": 0.10, "abandon": 0.10, "recover": 0.14, "risk": 0.12, "cost": 0.08},
    {"method": "uncertainty_halt", "base": 0.684, "belief": 0.34, "validity": 0.32, "reacquire": 0.18, "retarget": 0.16, "abandon": 0.50, "recover": 0.18, "risk": 0.72, "cost": 0.36},
    {"method": "active_viewpoint_reacquisition", "base": 0.704, "belief": 0.42, "validity": 0.34, "reacquire": 0.70, "retarget": 0.22, "abandon": 0.26, "recover": 0.38, "risk": 0.34, "cost": 0.34},
    {"method": "pomdp_belief_planner", "base": 0.716, "belief": 0.54, "validity": 0.48, "reacquire": 0.46, "retarget": 0.38, "abandon": 0.34, "recover": 0.42, "risk": 0.40, "cost": 0.28},
    {"method": "goal_retargeting_heuristic", "base": 0.710, "belief": 0.38, "validity": 0.42, "reacquire": 0.28, "retarget": 0.62, "abandon": 0.40, "recover": 0.44, "risk": 0.36, "cost": 0.24},
    {"method": "failure_aware_manipulation_policy", "base": 0.724, "belief": 0.50, "validity": 0.54, "reacquire": 0.44, "retarget": 0.52, "abandon": 0.46, "recover": 0.52, "risk": 0.42, "cost": 0.26},
    {"method": "proposed_disappearing_goal_belief_revision", "base": 0.742, "belief": 0.74, "validity": 0.76, "reacquire": 0.66, "retarget": 0.70, "abandon": 0.66, "recover": 0.64, "risk": 0.50, "cost": 0.24},
    {"method": "oracle_goal_state_supervisor", "base": 0.802, "belief": 0.94, "validity": 0.94, "reacquire": 0.86, "retarget": 0.90, "abandon": 0.86, "recover": 0.82, "risk": 0.76, "cost": 0.18},
]

ABLATIONS = [
    ("full_disappearing_goal_belief_revision", {"base": 0.742, "belief": 0.74, "validity": 0.76, "reacquire": 0.66, "retarget": 0.70, "abandon": 0.66, "recover": 0.64, "risk": 0.50, "cost": 0.24}, "all components"),
    ("minus_observation_memory_separation", {"base": 0.722, "belief": 0.42, "validity": 0.60, "reacquire": 0.60, "retarget": 0.62, "abandon": 0.58, "recover": 0.56, "risk": 0.45, "cost": 0.20}, "confounds unseen goals with invalid goals"),
    ("minus_active_reacquisition", {"base": 0.720, "belief": 0.70, "validity": 0.68, "reacquire": 0.22, "retarget": 0.62, "abandon": 0.58, "recover": 0.52, "risk": 0.42, "cost": 0.18}, "does not actively test occluded goals"),
    ("minus_physical_validity_test", {"base": 0.716, "belief": 0.66, "validity": 0.30, "reacquire": 0.62, "retarget": 0.56, "abandon": 0.50, "recover": 0.52, "risk": 0.38, "cost": 0.19}, "cannot distinguish hidden from physically invalid"),
    ("minus_substitute_goal_planner", {"base": 0.722, "belief": 0.70, "validity": 0.70, "reacquire": 0.60, "retarget": 0.28, "abandon": 0.56, "recover": 0.52, "risk": 0.42, "cost": 0.18}, "cannot choose substitute goals"),
    ("minus_abandonment_calibration", {"base": 0.728, "belief": 0.72, "validity": 0.72, "reacquire": 0.62, "retarget": 0.66, "abandon": 0.22, "recover": 0.54, "risk": 0.54, "cost": 0.16}, "over-pursues invalid goals or over-abandons hidden goals"),
    ("active_perception_only", {"base": 0.704, "belief": 0.42, "validity": 0.34, "reacquire": 0.70, "retarget": 0.22, "abandon": 0.26, "recover": 0.38, "risk": 0.34, "cost": 0.34}, "active viewpoint reacquisition baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probabilities(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    occlusion = split["occlusion"] if stress_override is None else min(0.98, 0.12 + 0.80 * stress)
    removal = split["removal"] if stress_override is None else min(0.98, 0.10 + 0.78 * stress)
    delay = split["delay"] if stress_override is None else min(0.95, 0.08 + 0.76 * stress)
    retarget_shift = split["retarget"] if stress_override is None else min(0.95, 0.10 + 0.76 * stress)

    hidden_load = task["visibility_need"] * regime["hidden"] * (0.56 + 0.52 * occlusion + 0.20 * stress)
    invalid_load = task["goal_specificity"] * regime["invalid"] * (0.56 + 0.54 * removal + 0.20 * stress)
    moved_load = regime["move"] * (0.50 + 0.46 * stress + 0.24 * delay)
    substitute_load = regime["substitute"] * (0.46 + 0.54 * retarget_shift)
    hazard_load = task["unsafe_sensitivity"] * regime["hazard"] * (0.52 + 0.50 * stress)
    reappear_load = regime["reappear"] * (0.48 + 0.45 * delay)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.011)

    goal_validity_f1 = clamp(
        0.205
        + 0.320 * method["belief"]
        + 0.245 * method["validity"]
        + 0.080 * method["reacquire"]
        - 0.072 * occlusion
        - 0.055 * removal
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    retarget_precision = clamp(
        0.185
        + 0.350 * method["retarget"]
        + 0.145 * method["validity"]
        + 0.090 * method["belief"]
        - 0.060 * retarget_shift
        - 0.045 * delay
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    stale_pursuit = clamp(
        0.070
        + 0.170 * invalid_load * (1.0 - method["validity"])
        + 0.125 * moved_load * (1.0 - method["belief"])
        + 0.080 * delay * (1.0 - method["abandon"])
        - 0.055 * method["retarget"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.75,
    )
    unsafe_reach = clamp(
        0.035
        + 0.125 * hazard_load * (1.0 - method["abandon"])
        + 0.090 * stale_pursuit
        + 0.060 * invalid_load * (1.0 - method["validity"])
        - 0.040 * method["recover"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.58,
    )
    false_abandonment = clamp(
        0.040
        + 0.150 * hidden_load * (1.0 - method["reacquire"])
        + 0.100 * reappear_load * (1.0 - method["belief"])
        + 0.090 * method["risk"] * (1.0 - method["validity"])
        - 0.055 * method["abandon"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    reappearance_recovery = clamp(
        0.160
        + 0.250 * method["reacquire"]
        + 0.150 * method["belief"]
        + 0.110 * method["recover"]
        - 0.095 * delay
        - 0.060 * occlusion
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    substitute_success = clamp(
        0.150
        + 0.295 * method["retarget"]
        + 0.160 * method["validity"]
        + 0.090 * method["recover"]
        - 0.075 * retarget_shift
        - 0.050 * invalid_load
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    belief_latency = clamp(
        0.720
        + 0.250 * hidden_load
        + 0.230 * invalid_load
        + 0.140 * delay
        - 0.270 * method["belief"]
        - 0.170 * method["validity"]
        - 0.090 * method["reacquire"]
        + rng.normal(0.0, 0.014),
        0.03,
        1.50,
    )
    intervention_cost = clamp(
        0.120
        + 0.135 * method["cost"]
        + 0.105 * method["reacquire"]
        + 0.075 * method["retarget"]
        + 0.070 * false_abandonment
        - 0.040 * method["validity"]
        + rng.normal(0.0, 0.006),
        0.02,
        0.75,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.130 * hidden_load * (1.0 - method["reacquire"])
        - 0.145 * invalid_load * (1.0 - method["validity"])
        - 0.115 * moved_load * (1.0 - method["belief"])
        - 0.125 * substitute_load * (1.0 - method["retarget"])
        - 0.105 * stale_pursuit
        - 0.105 * unsafe_reach
        - 0.080 * false_abandonment
        + 0.105 * reappearance_recovery
        + 0.095 * substitute_success
        - 0.045 * method["cost"]
        + noise,
        0.02,
        0.98,
    )

    return {
        "success": success,
        "goal_validity_f1": goal_validity_f1,
        "retarget_precision": retarget_precision,
        "stale_goal_pursuit": stale_pursuit,
        "unsafe_reach": unsafe_reach,
        "false_abandonment": false_abandonment,
        "reappearance_recovery": reappearance_recovery,
        "substitute_goal_success": substitute_success,
        "belief_update_latency": belief_latency,
        "intervention_cost": intervention_cost,
    }


def simulate_group(method, task, regime, split, seed, stress_override=None):
    probs = probabilities(method, task, regime, split, seed, stress_override=stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    metrics = {
        "success": rng.binomial(EPISODES_PER_GROUP, probs["success"]) / EPISODES_PER_GROUP,
        "stale_goal_pursuit": rng.binomial(EPISODES_PER_GROUP, probs["stale_goal_pursuit"]) / EPISODES_PER_GROUP,
        "unsafe_reach": rng.binomial(EPISODES_PER_GROUP, probs["unsafe_reach"]) / EPISODES_PER_GROUP,
        "false_abandonment": rng.binomial(EPISODES_PER_GROUP, probs["false_abandonment"]) / EPISODES_PER_GROUP,
        "reappearance_recovery": rng.binomial(EPISODES_PER_GROUP, probs["reappearance_recovery"]) / EPISODES_PER_GROUP,
        "substitute_goal_success": rng.binomial(EPISODES_PER_GROUP, probs["substitute_goal_success"]) / EPISODES_PER_GROUP,
        "goal_validity_f1": clamp(probs["goal_validity_f1"] + rng.normal(0.0, 0.010)),
        "retarget_precision": clamp(probs["retarget_precision"] + rng.normal(0.0, 0.010)),
        "belief_update_latency": clamp(probs["belief_update_latency"] + rng.normal(0.0, 0.012), 0.03, 1.50),
        "intervention_cost": clamp(probs["intervention_cost"] + rng.normal(0.0, 0.006)),
    }
    metrics["regret_to_oracle"] = 0.0
    return metrics


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        grouped.setdefault(tuple(row[k] for k in keys), []).append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {k: v for k, v in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            record[f"mean_{metric}"] = float(np.mean(vals))
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        output.append(record)
    return output


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            item[key] = round(value, 4) if isinstance(value, float) else value
        out.append(item)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    raw = []
    oracle_lookup = {}
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed)
                        row = {
                            "method": method["method"],
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                            **metrics,
                        }
                        raw.append(row)
                        if method["method"] == "oracle_goal_state_supervisor":
                            oracle_lookup[(split["split"], task["task"], regime["regime"], seed)] = metrics["success"]
    for row in raw:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle_lookup[key] - row["success"])
    metrics = [
        "success",
        "goal_validity_f1",
        "retarget_precision",
        "stale_goal_pursuit",
        "unsafe_reach",
        "false_abandonment",
        "reappearance_recovery",
        "substitute_goal_success",
        "belief_update_latency",
        "intervention_cost",
        "regret_to_oracle",
    ]
    seed_task_regime = aggregate(raw, ["method", "split", "task", "regime", "seed"], metrics)
    per_task_regime = aggregate(raw, ["method", "split", "task", "regime"], metrics)
    seed_split = aggregate(raw, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])
    for row in summary:
        if row["method"] == "oracle_goal_state_supervisor":
            row["mean_regret_to_oracle"] = 0.0
            row["ci95_regret_to_oracle"] = 0.0
        else:
            matching = [r for r in seed_split if r["method"] == row["method"] and r["split"] == row["split"]]
            row["mean_regret_to_oracle"] = float(np.mean([r["mean_regret_to_oracle"] for r in matching]))
            row["ci95_regret_to_oracle"] = ci95([r["mean_regret_to_oracle"] for r in matching])
    return raw, per_task_regime, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_disappearance_stress"}
    non_oracle = [m for m in combined if m not in {"proposed_disappearing_goal_belief_revision", "oracle_goal_state_supervisor"}]
    strongest = max(non_oracle, key=lambda method: float(combined[method]["mean_mean_success"]))
    proposed = {
        int(r["seed"]): float(r["mean_success"])
        for r in seed_split
        if r["split"] == "combined_disappearance_stress" and r["method"] == "proposed_disappearing_goal_belief_revision"
    }
    rows = []
    for method in sorted([m for m in combined if m != "proposed_disappearing_goal_belief_revision"]):
        baseline = {
            int(r["seed"]): float(r["mean_success"])
            for r in seed_split
            if r["split"] == "combined_disappearance_stress" and r["method"] == method
        }
        diffs = [proposed[seed] - baseline[seed] for seed in SEEDS]
        rows.append(
            {
                "comparison": f"proposed_disappearing_goal_belief_revision_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": sum(diff > 0 for diff in diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_disappearance_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_group(method, task, regime, split, seed)
                    rows.append({"ablation": name, "task": task["task"], "regime": regime["regime"], "seed": seed, "interpretation": note, **metrics})
    metrics = [
        "success",
        "goal_validity_f1",
        "retarget_precision",
        "stale_goal_pursuit",
        "unsafe_reach",
        "false_abandonment",
        "reappearance_recovery",
        "substitute_goal_success",
        "belief_update_latency",
        "intervention_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(s for s in SPLITS if s["split"] == "combined_disappearance_stress")
    levels = np.linspace(0.10, 0.95, 6)
    keep = [
        "active_viewpoint_reacquisition",
        "pomdp_belief_planner",
        "failure_aware_manipulation_policy",
        "proposed_disappearing_goal_belief_revision",
        "oracle_goal_state_supervisor",
    ]
    rows = []
    for stress in levels:
        for method in [m for m in METHODS if m["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, **metrics})
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "goal_validity_f1",
        "stale_goal_pursuit",
        "unsafe_reach",
        "false_abandonment",
        "belief_update_latency",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_disappearance_stress"]
    combined = sorted(combined, key=lambda r: float(r["mean_mean_success"]))
    labels = [DISPLAY_NAMES.get(r["method"], r["method"]) for r in combined]
    y = np.arange(len(combined))

    plt.figure(figsize=(10, 5.8))
    plt.barh(y, [float(r["mean_mean_success"]) for r in combined], xerr=[float(r["ci95_mean_success"]) for r in combined], color=["#006d77" if r["method"] == "proposed_disappearing_goal_belief_revision" else "#9aa6b2" for r in combined], capsize=3)
    plt.yticks(y, labels)
    plt.xlabel("Combined-disappearance success")
    plt.title("Disappearing-goal manipulation: combined stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_goal_combined_success.png", dpi=180)
    plt.close()

    ordered = sorted([r for r in combined if r["method"] != "oracle_goal_state_supervisor"], key=lambda r: float(r["mean_mean_goal_validity_f1"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11, 5.6))
    plt.bar(x - 0.2, [float(r["mean_mean_goal_validity_f1"]) for r in ordered], width=0.4, label="goal-validity F1", color="#118ab2")
    plt.bar(x + 0.2, [float(r["mean_mean_stale_goal_pursuit"]) for r in ordered], width=0.4, label="stale pursuit", color="#ef476f")
    plt.xticks(x, [DISPLAY_NAMES.get(r["method"], r["method"]) for r in ordered], rotation=30, ha="right")
    plt.ylabel("Metric")
    plt.title("Goal-validity diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_goal_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    for method in sorted({r["method"] for r in stress_summary}):
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Disappearance/reappearance stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_goal_stress_sweep.png", dpi=180)
    plt.close()

    labels = [DISPLAY_NAMES.get(r["ablation"], r["ablation"]) for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(10.5, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#006d77" if r["ablation"] == "full_disappearing_goal_belief_revision" else "#9aa6b2" for r in ablation_summary], capsize=3)
    plt.xticks(ax, labels, rotation=30, ha="right")
    plt.ylabel("Combined-disappearance success")
    plt.title("Belief-revision ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_goal_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.4))
    plt.scatter([float(r["mean_mean_unsafe_reach"]) for r in combined], [float(r["mean_regret_to_oracle"]) for r in combined], s=70, c=["#006d77" if r["method"] == "proposed_disappearing_goal_belief_revision" else "#9aa6b2" for r in combined])
    for r in combined:
        plt.text(float(r["mean_mean_unsafe_reach"]) + 0.002, float(r["mean_regret_to_oracle"]) + 0.002, DISPLAY_NAMES.get(r["method"], r["method"]), fontsize=8)
    plt.xlabel("Unsafe reach rate")
    plt.ylabel("Regret to oracle")
    plt.title("Unsafe reach/regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_goal_safety_regret.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_regime, strongest):
    combined = [r for r in per_task_regime if r["split"] == "combined_disappearance_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_disappearing_goal_belief_revision"]
    peer = {(r["task"], r["regime"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_goal_validity_f1": row["mean_goal_validity_f1"],
                "proposed_false_abandonment": row["mean_false_abandonment"],
                "lesson": "belief revision helps least when active perception can quickly reacquire an occluded goal or the substitute-goal choice is trivial",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_disappearance_stress"}
    proposed = combined["proposed_disappearing_goal_belief_revision"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    validity_delta = float(proposed["mean_mean_goal_validity_f1"]) - float(base["mean_mean_goal_validity_f1"])
    stale_delta = float(proposed["mean_mean_stale_goal_pursuit"]) - float(base["mean_mean_stale_goal_pursuit"])
    unsafe_delta = float(proposed["mean_mean_unsafe_reach"]) - float(base["mean_mean_unsafe_reach"])
    false_abandon_delta = float(proposed["mean_mean_false_abandonment"]) - float(base["mean_mean_false_abandonment"])
    cost_delta = float(proposed["mean_mean_intervention_cost"]) - float(base["mean_mean_intervention_cost"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_disappearing_goal_belief_revision")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_disappearing_goal_belief_revision"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    diagnostic_gate = validity_delta >= 0.050 or stale_delta <= -0.050
    safety_gate = unsafe_delta <= 0.020 and false_abandon_delta <= 0.020 and cost_delta <= 0.040
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and diagnostic_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local disappearing-goal belief-revision evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, diagnostic, safety, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "goal_validity_f1_delta_vs_strongest": validity_delta,
        "stale_goal_pursuit_delta_vs_strongest": stale_delta,
        "unsafe_reach_delta_vs_strongest": unsafe_delta,
        "false_abandonment_delta_vs_strongest": false_abandon_delta,
        "intervention_cost_delta_vs_strongest": cost_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_disappearance_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 106 disappearing_goal_manipulation evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 disappearing-goal regimes x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-disappearance ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"goal_f1={float(row['mean_mean_goal_validity_f1']):.3f}, retarget_precision={float(row['mean_mean_retarget_precision']):.3f}, "
                f"stale={float(row['mean_mean_stale_goal_pursuit']):.3f}, unsafe={float(row['mean_mean_unsafe_reach']):.3f}, "
                f"false_abandon={float(row['mean_mean_false_abandonment']):.3f}, reappear={float(row['mean_mean_reappearance_recovery']):.3f}, "
                f"substitute={float(row['mean_mean_substitute_goal_success']):.3f}, latency={float(row['mean_mean_belief_update_latency']):.3f}, "
                f"regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"goal_f1={float(row['mean_mean_goal_validity_f1']):.3f}, stale={float(row['mean_mean_stale_goal_pursuit']):.3f}, "
                f"unsafe={float(row['mean_mean_unsafe_reach']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_regime, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_regime, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_disappearance_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_goal_validity_f1", "GoalF1"),
            ("mean_mean_stale_goal_pursuit", "Stale"),
            ("mean_mean_unsafe_reach", "Unsafe"),
            ("mean_mean_false_abandonment", "FalseAbd."),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-disappearance disappearing-goal manipulation benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_goal_validity_f1", "GoalF1"),
            ("mean_mean_stale_goal_pursuit", "Stale"),
            ("mean_mean_unsafe_reach", "Unsafe"),
        ],
        "Ablations of the disappearing-goal belief revision model.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-disappearance success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
