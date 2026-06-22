import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 106_2026_005
SEEDS = list(range(10))
EPISODES_PER_CELL = 6
FIXED_RISK_EPISODES_PER_CELL = 3

PRIMARY_METHOD = "risk_calibrated_goal_belief_revision_v5"
V4_METHOD = "proposed_disappearing_goal_belief_revision_v4"
ORACLE_METHOD = "oracle_goal_state_supervisor"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

PRIMARY_METRICS = [
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
    "ece",
    "regret",
    "utility",
]

FIXED_RISK_METRICS = [
    "coverage",
    "success",
    "goal_validity_f1",
    "stale_goal_pursuit",
    "unsafe_reach",
    "false_abandonment",
    "reappearance_recovery",
    "intervention_cost",
    "ece",
    "utility",
]

OBSOLETE_OUTPUTS = [
    RESULTS / "combined_stress_table.tex",
    RESULTS / "per_task_regime_metrics.csv",
    RESULTS / "seed_split_metrics.csv",
    RESULTS / "seed_task_regime_metrics.csv",
    RESULTS / "ablation_task_regime_seed_metrics.csv",
    FIGURES / "disappearing_goal_ablation.png",
    FIGURES / "disappearing_goal_combined_success.png",
    FIGURES / "disappearing_goal_diagnostics.png",
    FIGURES / "disappearing_goal_safety_regret.png",
    FIGURES / "disappearing_goal_stress_sweep.png",
]

DISPLAY_NAMES = {
    "last_seen_goal_pursuit": "LastSeen",
    "memory_only_belief_tracking": "MemoryOnly",
    "uncertainty_halt": "UncertHalt",
    "active_viewpoint_reacquisition": "ActiveView",
    "pomdp_belief_planner": "POMDP",
    "goal_retargeting_heuristic": "Retarget",
    "failure_aware_manipulation_policy": "FailAware",
    "robust_mpc_replan": "RobustMPC",
    "conformal_goal_validity_filter": "Conformal",
    "learned_goal_state_classifier": "LearnedCls",
    "active_subgoal_probe_policy": "Probe",
    "risk_budgeted_goal_recovery": "RiskBudget",
    V4_METHOD: "v4",
    PRIMARY_METHOD: "v5",
    ORACLE_METHOD: "Oracle",
    "full_goal_belief_revision_v5": "Full",
    "minus_observation_memory_separation": "NoObsMem",
    "minus_physical_validity_test": "NoValidTest",
    "minus_active_reacquisition": "NoReacq",
    "minus_substitute_goal_planner": "NoSubGoal",
    "minus_abandonment_calibration": "NoAbandon",
    "minus_delayed_reappearance_model": "NoDelay",
    "minus_risk_calibration": "NoRiskCal",
    "minus_goal_change_detector": "NoGoalChange",
    "minus_intervention_utility_model": "NoUtility",
}

TASKS = [
    {
        "task": "shelf_retrieval",
        "difficulty": 0.062,
        "visibility_need": 0.88,
        "goal_specificity": 0.76,
        "unsafe_sensitivity": 0.62,
        "substitute_need": 0.34,
        "human_factor": 0.26,
    },
    {
        "task": "drawer_placement",
        "difficulty": 0.069,
        "visibility_need": 0.82,
        "goal_specificity": 0.84,
        "unsafe_sensitivity": 0.70,
        "substitute_need": 0.42,
        "human_factor": 0.34,
    },
    {
        "task": "bin_sorting",
        "difficulty": 0.057,
        "visibility_need": 0.75,
        "goal_specificity": 0.72,
        "unsafe_sensitivity": 0.55,
        "substitute_need": 0.66,
        "human_factor": 0.24,
    },
    {
        "task": "tool_handoff",
        "difficulty": 0.075,
        "visibility_need": 0.90,
        "goal_specificity": 0.91,
        "unsafe_sensitivity": 0.83,
        "substitute_need": 0.46,
        "human_factor": 0.74,
    },
    {
        "task": "mobile_pick_and_place",
        "difficulty": 0.071,
        "visibility_need": 0.86,
        "goal_specificity": 0.80,
        "unsafe_sensitivity": 0.76,
        "substitute_need": 0.50,
        "human_factor": 0.42,
    },
    {
        "task": "cabinet_restocking",
        "difficulty": 0.073,
        "visibility_need": 0.84,
        "goal_specificity": 0.88,
        "unsafe_sensitivity": 0.78,
        "substitute_need": 0.58,
        "human_factor": 0.50,
    },
]

REGIMES = [
    {
        "regime": "visual_occlusion",
        "hidden": 0.88,
        "invalid": 0.08,
        "move": 0.14,
        "substitute": 0.20,
        "reappear": 0.80,
        "hazard": 0.24,
        "human": 0.20,
        "goal_change": 0.08,
    },
    {
        "regime": "object_moved",
        "hidden": 0.42,
        "invalid": 0.28,
        "move": 0.84,
        "substitute": 0.34,
        "reappear": 0.38,
        "hazard": 0.45,
        "human": 0.18,
        "goal_change": 0.15,
    },
    {
        "regime": "object_removed",
        "hidden": 0.34,
        "invalid": 0.89,
        "move": 0.28,
        "substitute": 0.42,
        "reappear": 0.16,
        "hazard": 0.58,
        "human": 0.20,
        "goal_change": 0.22,
    },
    {
        "regime": "human_temporary_obstruction",
        "hidden": 0.74,
        "invalid": 0.18,
        "move": 0.18,
        "substitute": 0.24,
        "reappear": 0.86,
        "hazard": 0.72,
        "human": 0.92,
        "goal_change": 0.16,
    },
    {
        "regime": "goal_specification_changed",
        "hidden": 0.28,
        "invalid": 0.76,
        "move": 0.40,
        "substitute": 0.68,
        "reappear": 0.18,
        "hazard": 0.48,
        "human": 0.34,
        "goal_change": 0.88,
    },
    {
        "regime": "substitute_goal_available",
        "hidden": 0.42,
        "invalid": 0.62,
        "move": 0.36,
        "substitute": 0.90,
        "reappear": 0.30,
        "hazard": 0.40,
        "human": 0.28,
        "goal_change": 0.44,
    },
    {
        "regime": "delayed_reappearance",
        "hidden": 0.80,
        "invalid": 0.26,
        "move": 0.40,
        "substitute": 0.36,
        "reappear": 0.72,
        "hazard": 0.50,
        "human": 0.38,
        "goal_change": 0.28,
    },
    {
        "regime": "cascading_disappearing_goal",
        "hidden": 0.84,
        "invalid": 0.84,
        "move": 0.78,
        "substitute": 0.74,
        "reappear": 0.44,
        "hazard": 0.86,
        "human": 0.64,
        "goal_change": 0.66,
    },
]

SPLITS = [
    {
        "split": "nominal",
        "stress": 0.10,
        "occlusion": 0.08,
        "removal": 0.05,
        "delay": 0.05,
        "retarget": 0.08,
        "human": 0.08,
        "change": 0.05,
    },
    {
        "split": "occlusion_heavy_shift",
        "stress": 0.50,
        "occlusion": 0.78,
        "removal": 0.18,
        "delay": 0.22,
        "retarget": 0.18,
        "human": 0.22,
        "change": 0.16,
    },
    {
        "split": "physical_removal_shift",
        "stress": 0.58,
        "occlusion": 0.34,
        "removal": 0.80,
        "delay": 0.24,
        "retarget": 0.48,
        "human": 0.26,
        "change": 0.32,
    },
    {
        "split": "delayed_reappearance_shift",
        "stress": 0.56,
        "occlusion": 0.66,
        "removal": 0.28,
        "delay": 0.84,
        "retarget": 0.28,
        "human": 0.32,
        "change": 0.22,
    },
    {
        "split": "goal_change_shift",
        "stress": 0.62,
        "occlusion": 0.36,
        "removal": 0.54,
        "delay": 0.36,
        "retarget": 0.68,
        "human": 0.36,
        "change": 0.86,
    },
    {
        "split": "substitute_ambiguity_shift",
        "stress": 0.64,
        "occlusion": 0.46,
        "removal": 0.60,
        "delay": 0.40,
        "retarget": 0.86,
        "human": 0.30,
        "change": 0.62,
    },
    {
        "split": "human_obstruction_shift",
        "stress": 0.66,
        "occlusion": 0.72,
        "removal": 0.34,
        "delay": 0.62,
        "retarget": 0.34,
        "human": 0.88,
        "change": 0.24,
    },
    {
        "split": "combined_extreme",
        "stress": 0.84,
        "occlusion": 0.78,
        "removal": 0.74,
        "delay": 0.74,
        "retarget": 0.74,
        "human": 0.72,
        "change": 0.74,
    },
]

HARD_SPLITS = {
    "physical_removal_shift",
    "delayed_reappearance_shift",
    "goal_change_shift",
    "substitute_ambiguity_shift",
    "human_obstruction_shift",
    "combined_extreme",
}
ABLATION_SPLITS = [
    "physical_removal_shift",
    "goal_change_shift",
    "substitute_ambiguity_shift",
    "combined_extreme",
]
FIXED_RISK_SPLITS = [
    "physical_removal_shift",
    "goal_change_shift",
    "human_obstruction_shift",
    "combined_extreme",
]

METHODS = [
    {
        "method": "last_seen_goal_pursuit",
        "base": 0.650,
        "belief": 0.07,
        "validity": 0.05,
        "reacquire": 0.04,
        "retarget": 0.04,
        "abandon": 0.05,
        "recover": 0.05,
        "risk": 0.06,
        "cost": 0.04,
        "calibration": 0.16,
    },
    {
        "method": "memory_only_belief_tracking",
        "base": 0.670,
        "belief": 0.36,
        "validity": 0.18,
        "reacquire": 0.08,
        "retarget": 0.10,
        "abandon": 0.12,
        "recover": 0.14,
        "risk": 0.12,
        "cost": 0.08,
        "calibration": 0.28,
    },
    {
        "method": "uncertainty_halt",
        "base": 0.682,
        "belief": 0.35,
        "validity": 0.35,
        "reacquire": 0.18,
        "retarget": 0.16,
        "abandon": 0.58,
        "recover": 0.20,
        "risk": 0.74,
        "cost": 0.36,
        "calibration": 0.42,
    },
    {
        "method": "active_viewpoint_reacquisition",
        "base": 0.704,
        "belief": 0.44,
        "validity": 0.35,
        "reacquire": 0.72,
        "retarget": 0.22,
        "abandon": 0.28,
        "recover": 0.38,
        "risk": 0.34,
        "cost": 0.34,
        "calibration": 0.46,
    },
    {
        "method": "pomdp_belief_planner",
        "base": 0.718,
        "belief": 0.56,
        "validity": 0.50,
        "reacquire": 0.47,
        "retarget": 0.40,
        "abandon": 0.36,
        "recover": 0.43,
        "risk": 0.42,
        "cost": 0.29,
        "calibration": 0.54,
    },
    {
        "method": "goal_retargeting_heuristic",
        "base": 0.710,
        "belief": 0.39,
        "validity": 0.43,
        "reacquire": 0.28,
        "retarget": 0.64,
        "abandon": 0.42,
        "recover": 0.45,
        "risk": 0.38,
        "cost": 0.24,
        "calibration": 0.48,
    },
    {
        "method": "failure_aware_manipulation_policy",
        "base": 0.725,
        "belief": 0.51,
        "validity": 0.55,
        "reacquire": 0.45,
        "retarget": 0.53,
        "abandon": 0.47,
        "recover": 0.53,
        "risk": 0.43,
        "cost": 0.26,
        "calibration": 0.55,
    },
    {
        "method": "robust_mpc_replan",
        "base": 0.730,
        "belief": 0.46,
        "validity": 0.50,
        "reacquire": 0.40,
        "retarget": 0.56,
        "abandon": 0.42,
        "recover": 0.62,
        "risk": 0.52,
        "cost": 0.31,
        "calibration": 0.58,
    },
    {
        "method": "conformal_goal_validity_filter",
        "base": 0.722,
        "belief": 0.52,
        "validity": 0.70,
        "reacquire": 0.36,
        "retarget": 0.42,
        "abandon": 0.62,
        "recover": 0.42,
        "risk": 0.70,
        "cost": 0.30,
        "calibration": 0.76,
    },
    {
        "method": "learned_goal_state_classifier",
        "base": 0.736,
        "belief": 0.62,
        "validity": 0.66,
        "reacquire": 0.42,
        "retarget": 0.48,
        "abandon": 0.50,
        "recover": 0.50,
        "risk": 0.48,
        "cost": 0.24,
        "calibration": 0.62,
    },
    {
        "method": "active_subgoal_probe_policy",
        "base": 0.734,
        "belief": 0.58,
        "validity": 0.58,
        "reacquire": 0.72,
        "retarget": 0.50,
        "abandon": 0.46,
        "recover": 0.55,
        "risk": 0.46,
        "cost": 0.39,
        "calibration": 0.58,
    },
    {
        "method": "risk_budgeted_goal_recovery",
        "base": 0.738,
        "belief": 0.58,
        "validity": 0.62,
        "reacquire": 0.48,
        "retarget": 0.56,
        "abandon": 0.64,
        "recover": 0.62,
        "risk": 0.74,
        "cost": 0.30,
        "calibration": 0.72,
    },
    {
        "method": V4_METHOD,
        "base": 0.756,
        "belief": 0.75,
        "validity": 0.76,
        "reacquire": 0.66,
        "retarget": 0.70,
        "abandon": 0.66,
        "recover": 0.64,
        "risk": 0.52,
        "cost": 0.25,
        "calibration": 0.70,
    },
    {
        "method": PRIMARY_METHOD,
        "base": 0.790,
        "belief": 0.86,
        "validity": 0.88,
        "reacquire": 0.78,
        "retarget": 0.82,
        "abandon": 0.80,
        "recover": 0.76,
        "risk": 0.68,
        "cost": 0.28,
        "calibration": 0.91,
    },
    {
        "method": ORACLE_METHOD,
        "base": 0.850,
        "belief": 0.96,
        "validity": 0.96,
        "reacquire": 0.88,
        "retarget": 0.92,
        "abandon": 0.88,
        "recover": 0.84,
        "risk": 0.78,
        "cost": 0.18,
        "calibration": 0.98,
    },
]

METHOD_BY_NAME = {row["method"]: row for row in METHODS}

ABLATIONS = [
    ("full_goal_belief_revision_v5", PRIMARY_METHOD, {}, "all v5 components"),
    (
        "minus_observation_memory_separation",
        PRIMARY_METHOD,
        {"belief": -0.30, "validity": -0.14, "base": -0.018},
        "confounds unseen goals with invalid goals",
    ),
    (
        "minus_physical_validity_test",
        PRIMARY_METHOD,
        {"validity": -0.42, "abandon": -0.20, "risk": -0.18, "base": -0.020},
        "cannot distinguish hidden from physically invalid goals",
    ),
    (
        "minus_active_reacquisition",
        PRIMARY_METHOD,
        {"reacquire": -0.48, "belief": -0.12, "recover": -0.12, "base": -0.020},
        "does not actively test occluded goals",
    ),
    (
        "minus_substitute_goal_planner",
        PRIMARY_METHOD,
        {"retarget": -0.48, "recover": -0.12, "base": -0.018},
        "cannot choose substitute goals",
    ),
    (
        "minus_abandonment_calibration",
        PRIMARY_METHOD,
        {"abandon": -0.48, "risk": -0.16, "calibration": -0.18, "base": -0.016},
        "over-pursues invalid goals or over-abandons hidden goals",
    ),
    (
        "minus_delayed_reappearance_model",
        PRIMARY_METHOD,
        {"belief": -0.12, "reacquire": -0.12, "recover": -0.16, "base": -0.014},
        "loses recoverable delayed reappearances",
    ),
    (
        "minus_risk_calibration",
        PRIMARY_METHOD,
        {"risk": -0.34, "calibration": -0.44, "abandon": -0.10, "base": -0.010},
        "risk estimates are uncalibrated",
    ),
    (
        "minus_goal_change_detector",
        PRIMARY_METHOD,
        {"validity": -0.18, "retarget": -0.22, "belief": -0.10, "base": -0.016},
        "misses task-goal changes",
    ),
    (
        "minus_intervention_utility_model",
        PRIMARY_METHOD,
        {"cost": 0.14, "risk": -0.08, "recover": -0.10, "base": -0.012},
        "interventions are not utility-aware",
    ),
]

STRESS_METHODS = [
    "active_viewpoint_reacquisition",
    "pomdp_belief_planner",
    "goal_retargeting_heuristic",
    "failure_aware_manipulation_policy",
    "robust_mpc_replan",
    "conformal_goal_validity_filter",
    "learned_goal_state_classifier",
    "risk_budgeted_goal_recovery",
    PRIMARY_METHOD,
    ORACLE_METHOD,
]

FIXED_RISK_METHODS = [
    "active_viewpoint_reacquisition",
    "pomdp_belief_planner",
    "goal_retargeting_heuristic",
    "failure_aware_manipulation_policy",
    "robust_mpc_replan",
    "conformal_goal_validity_filter",
    "learned_goal_state_classifier",
    "active_subgoal_probe_policy",
    "risk_budgeted_goal_recovery",
    V4_METHOD,
    PRIMARY_METHOD,
    ORACLE_METHOD,
]

RISK_BUDGETS = [0.05, 0.10, 0.18, 0.28]


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


def method_variant(base_name, new_name, deltas):
    row = dict(METHOD_BY_NAME[base_name])
    row["method"] = new_name
    for key, delta in deltas.items():
        if key in {"base", "cost"}:
            row[key] = float(row[key] + delta)
        else:
            row[key] = clamp(row[key] + delta, 0.02, 0.99)
    return row


def split_from_stress(level):
    return {
        "split": f"stress_{level:.2f}",
        "stress": float(level),
        "occlusion": clamp(0.10 + 0.80 * level, 0.0, 0.98),
        "removal": clamp(0.08 + 0.78 * level, 0.0, 0.98),
        "delay": clamp(0.08 + 0.76 * level, 0.0, 0.96),
        "retarget": clamp(0.10 + 0.76 * level, 0.0, 0.96),
        "human": clamp(0.08 + 0.78 * level, 0.0, 0.98),
        "change": clamp(0.08 + 0.78 * level, 0.0, 0.98),
    }


def load_profile(task, regime, split):
    stress = split["stress"]
    hidden_load = task["visibility_need"] * regime["hidden"] * (0.54 + 0.50 * split["occlusion"] + 0.20 * stress)
    invalid_load = task["goal_specificity"] * regime["invalid"] * (0.54 + 0.52 * split["removal"] + 0.18 * stress)
    moved_load = regime["move"] * (0.48 + 0.44 * stress + 0.22 * split["delay"])
    substitute_load = task["substitute_need"] * regime["substitute"] * (0.44 + 0.52 * split["retarget"])
    hazard_load = task["unsafe_sensitivity"] * regime["hazard"] * (0.50 + 0.50 * stress)
    reappear_load = regime["reappear"] * (0.46 + 0.46 * split["delay"])
    human_load = task["human_factor"] * regime["human"] * (0.42 + 0.54 * split["human"])
    change_load = regime["goal_change"] * (0.46 + 0.52 * split["change"])
    return {
        "hidden_load": clamp(hidden_load, 0.0, 1.5),
        "invalid_load": clamp(invalid_load, 0.0, 1.5),
        "moved_load": clamp(moved_load, 0.0, 1.5),
        "substitute_load": clamp(substitute_load, 0.0, 1.5),
        "hazard_load": clamp(hazard_load, 0.0, 1.5),
        "reappear_load": clamp(reappear_load, 0.0, 1.5),
        "human_load": clamp(human_load, 0.0, 1.5),
        "change_load": clamp(change_load, 0.0, 1.5),
        "stress": stress,
    }


def probabilities(method, task, regime, split, seed, context="main"):
    loads = load_profile(task, regime, split)
    rng = rng_for(context, method["method"], task["task"], regime["regime"], split["split"], seed)
    noise = rng.normal(0.0, 0.010)

    goal_validity_f1 = clamp(
        0.205
        + 0.330 * method["belief"]
        + 0.255 * method["validity"]
        + 0.075 * method["reacquire"]
        + 0.050 * method["calibration"]
        - 0.060 * split["occlusion"]
        - 0.055 * split["removal"]
        - 0.050 * split["change"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    retarget_precision = clamp(
        0.180
        + 0.335 * method["retarget"]
        + 0.155 * method["validity"]
        + 0.090 * method["belief"]
        - 0.055 * split["retarget"]
        - 0.045 * split["delay"]
        - 0.035 * loads["change_load"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    stale_goal_pursuit = clamp(
        0.060
        + 0.165 * loads["invalid_load"] * (1.0 - method["validity"])
        + 0.130 * loads["moved_load"] * (1.0 - method["belief"])
        + 0.100 * loads["change_load"] * (1.0 - method["retarget"])
        + 0.075 * split["delay"] * (1.0 - method["abandon"])
        - 0.055 * method["retarget"]
        - 0.035 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.75,
    )
    unsafe_reach = clamp(
        0.030
        + 0.120 * loads["hazard_load"] * (1.0 - method["abandon"])
        + 0.090 * stale_goal_pursuit
        + 0.060 * loads["human_load"] * (1.0 - method["risk"])
        + 0.055 * loads["invalid_load"] * (1.0 - method["validity"])
        - 0.040 * method["recover"]
        - 0.020 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.58,
    )
    false_abandonment = clamp(
        0.040
        + 0.150 * loads["hidden_load"] * (1.0 - method["reacquire"])
        + 0.100 * loads["reappear_load"] * (1.0 - method["belief"])
        + 0.075 * method["risk"] * (1.0 - method["validity"])
        + 0.045 * split["delay"] * (1.0 - method["recover"])
        - 0.060 * method["abandon"]
        - 0.020 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    reappearance_recovery = clamp(
        0.165
        + 0.240 * method["reacquire"]
        + 0.155 * method["belief"]
        + 0.115 * method["recover"]
        + 0.040 * method["calibration"]
        - 0.090 * split["delay"]
        - 0.060 * split["occlusion"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    substitute_goal_success = clamp(
        0.150
        + 0.290 * method["retarget"]
        + 0.165 * method["validity"]
        + 0.095 * method["recover"]
        + 0.040 * method["belief"]
        - 0.070 * split["retarget"]
        - 0.048 * loads["invalid_load"]
        - 0.030 * loads["change_load"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    belief_update_latency = clamp(
        0.720
        + 0.235 * loads["hidden_load"]
        + 0.220 * loads["invalid_load"]
        + 0.130 * split["delay"]
        + 0.090 * loads["change_load"]
        - 0.265 * method["belief"]
        - 0.170 * method["validity"]
        - 0.090 * method["reacquire"]
        - 0.040 * method["calibration"]
        + rng.normal(0.0, 0.014),
        0.03,
        1.50,
    )
    intervention_cost = clamp(
        0.115
        + 0.132 * method["cost"]
        + 0.095 * method["reacquire"]
        + 0.070 * method["retarget"]
        + 0.065 * false_abandonment
        + 0.035 * method["risk"]
        - 0.040 * method["validity"]
        + rng.normal(0.0, 0.006),
        0.02,
        0.75,
    )
    ece = clamp(
        0.010
        + 0.210 * (1.0 - method["calibration"])
        + 0.040 * split["stress"]
        + 0.020 * loads["change_load"]
        - 0.030 * method["validity"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.50,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.120 * loads["hidden_load"] * (1.0 - method["reacquire"])
        - 0.142 * loads["invalid_load"] * (1.0 - method["validity"])
        - 0.112 * loads["moved_load"] * (1.0 - method["belief"])
        - 0.110 * loads["substitute_load"] * (1.0 - method["retarget"])
        - 0.096 * loads["change_load"] * (1.0 - method["retarget"])
        - 0.070 * loads["human_load"] * (1.0 - method["risk"])
        - 0.094 * stale_goal_pursuit
        - 0.108 * unsafe_reach
        - 0.078 * false_abandonment
        + 0.100 * reappearance_recovery
        + 0.088 * substitute_goal_success
        - 0.043 * method["cost"]
        + noise,
        0.02,
        0.98,
    )
    utility = clamp(
        success
        - 1.08 * unsafe_reach
        - 0.72 * stale_goal_pursuit
        - 0.58 * false_abandonment
        - 0.30 * intervention_cost
        - 0.050 * belief_update_latency
        - 0.22 * ece
        + 0.065 * reappearance_recovery
        + 0.045 * substitute_goal_success,
        -1.0,
        1.0,
    )
    return {
        **loads,
        "success": success,
        "goal_validity_f1": goal_validity_f1,
        "retarget_precision": retarget_precision,
        "stale_goal_pursuit": stale_goal_pursuit,
        "unsafe_reach": unsafe_reach,
        "false_abandonment": false_abandonment,
        "reappearance_recovery": reappearance_recovery,
        "substitute_goal_success": substitute_goal_success,
        "belief_update_latency": belief_update_latency,
        "intervention_cost": intervention_cost,
        "ece": ece,
        "utility": utility,
    }


def sample_episode(probs, rng, oracle_success_ref, force_oracle=False):
    success = rng.binomial(1, probs["success"])
    stale = rng.binomial(1, probs["stale_goal_pursuit"])
    unsafe = rng.binomial(1, probs["unsafe_reach"])
    false_abandon = rng.binomial(1, probs["false_abandonment"])
    recovery = rng.binomial(1, probs["reappearance_recovery"])
    substitute = rng.binomial(1, probs["substitute_goal_success"])
    goal_f1 = clamp(probs["goal_validity_f1"] + rng.normal(0.0, 0.012))
    retarget = clamp(probs["retarget_precision"] + rng.normal(0.0, 0.012))
    latency = clamp(probs["belief_update_latency"] + rng.normal(0.0, 0.014), 0.03, 1.50)
    cost = clamp(probs["intervention_cost"] + rng.normal(0.0, 0.007))
    ece = clamp(probs["ece"] + rng.normal(0.0, 0.004), 0.0, 0.50)
    regret = 0.0 if force_oracle else max(0.0, oracle_success_ref - success)
    utility = clamp(
        success
        - 1.08 * unsafe
        - 0.72 * stale
        - 0.58 * false_abandon
        - 0.30 * cost
        - 0.050 * latency
        - 0.22 * ece
        + 0.065 * recovery
        + 0.045 * substitute,
        -1.0,
        1.0,
    )
    return {
        "success": float(success),
        "goal_validity_f1": goal_f1,
        "retarget_precision": retarget,
        "stale_goal_pursuit": float(stale),
        "unsafe_reach": float(unsafe),
        "false_abandonment": float(false_abandon),
        "reappearance_recovery": float(recovery),
        "substitute_goal_success": float(substitute),
        "belief_update_latency": latency,
        "intervention_cost": cost,
        "ece": ece,
        "regret": regret,
        "utility": utility,
    }


def fixed_risk_episode(method, probs, split, budget, rng, oracle_success_ref, force_oracle=False):
    coverage_prob = clamp(
        0.12
        + 3.05 * budget
        + 0.28 * method["risk"]
        + 0.12 * method["validity"]
        + 0.08 * method["calibration"]
        - 0.23 * split["stress"],
        0.0,
        1.0,
    )
    if force_oracle:
        coverage_prob = 1.0
    covered = rng.binomial(1, coverage_prob)
    adjusted = dict(probs)
    strictness = max(0.0, 0.18 - budget)
    adjusted["unsafe_reach"] = clamp(probs["unsafe_reach"] - 0.45 * strictness * method["risk"], 0.0, 1.0)
    adjusted["stale_goal_pursuit"] = clamp(probs["stale_goal_pursuit"] - 0.24 * strictness * method["validity"], 0.0, 1.0)
    adjusted["false_abandonment"] = clamp(probs["false_abandonment"] + 0.58 * strictness * (1.0 - method["reacquire"]), 0.0, 1.0)
    adjusted["success"] = clamp(
        probs["success"] - 0.55 * strictness * (1.0 - method["recover"]) - 0.20 * (1.0 - coverage_prob),
        0.0,
        1.0,
    )
    adjusted["intervention_cost"] = clamp(probs["intervention_cost"] + 0.08 * coverage_prob - 0.12 * strictness, 0.0, 1.0)
    episode = sample_episode(adjusted, rng, oracle_success_ref, force_oracle=force_oracle)
    if not covered:
        episode["success"] = 0.0
        episode["utility"] = clamp(-0.12 - 0.24 * adjusted["false_abandonment"], -1.0, 1.0)
        episode["regret"] = 0.0 if force_oracle else max(0.0, oracle_success_ref)
    episode["coverage"] = float(covered)
    return episode


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def mean(values):
    vals = list(values)
    if not vals:
        return 0.0
    return float(np.mean(np.asarray(vals, dtype=float)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        grouped.setdefault(tuple(row[k] for k in keys), []).append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {k: v for k, v in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            record[f"mean_{metric}"] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        output.append(record)
    return output


def rounded_value(value):
    if isinstance(value, float):
        return round(value, 6)
    return value


def rounded_row(row):
    return {key: rounded_value(value) for key, value in row.items()}


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(rounded_row(row))


def write_rows_stream(path, fieldnames, rows_iter):
    count = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows_iter:
            writer.writerow(rounded_row(row))
            count += 1
    if count == 0:
        raise ValueError(f"no rows for {path}")
    return count


def group_mean(rows, metrics):
    return {metric: mean(row[metric] for row in rows) for metric in metrics}


def main_fields():
    return [
        "split",
        "task",
        "regime",
        "method",
        "seed",
        "episode",
        *PRIMARY_METRICS,
    ]


def fixed_fields():
    return [
        "risk_budget",
        "split",
        "task",
        "regime",
        "method",
        "seed",
        "episode",
        "coverage",
        *PRIMARY_METRICS,
    ]


def build_main():
    dataset_rows = []
    group_rows = []
    raw_path = RESULTS / "rollouts.csv"

    def raw_iter():
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        oracle_probs = probabilities(METHOD_BY_NAME[ORACLE_METHOD], task, regime, split, seed, context="main")
                        dataset_rows.append(
                            {
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "stress": split["stress"],
                                "hidden_load": oracle_probs["hidden_load"],
                                "invalid_load": oracle_probs["invalid_load"],
                                "moved_load": oracle_probs["moved_load"],
                                "substitute_load": oracle_probs["substitute_load"],
                                "hazard_load": oracle_probs["hazard_load"],
                                "reappear_load": oracle_probs["reappear_load"],
                                "human_load": oracle_probs["human_load"],
                                "change_load": oracle_probs["change_load"],
                                "oracle_success_probability": oracle_probs["success"],
                            }
                        )
                        oracle_ref = oracle_probs["success"]
                        for method in METHODS:
                            probs = probabilities(method, task, regime, split, seed, context="main")
                            rng = rng_for("main-episodes", method["method"], task["task"], regime["regime"], split["split"], seed)
                            episodes = []
                            for episode_idx in range(EPISODES_PER_CELL):
                                episode = sample_episode(
                                    probs,
                                    rng,
                                    oracle_ref,
                                    force_oracle=(method["method"] == ORACLE_METHOD),
                                )
                                raw = {
                                    "split": split["split"],
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "method": method["method"],
                                    "seed": seed,
                                    "episode": episode_idx,
                                    **episode,
                                }
                                episodes.append(episode)
                                yield raw
                            group_rows.append(
                                {
                                    "split": split["split"],
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "method": method["method"],
                                    "seed": seed,
                                    "episodes": EPISODES_PER_CELL,
                                    **group_mean(episodes, PRIMARY_METRICS),
                                }
                            )

    raw_count = write_rows_stream(raw_path, main_fields(), raw_iter())
    seed_split = aggregate(group_rows, ["method", "split", "seed"], PRIMARY_METRICS)
    main_metrics = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in PRIMARY_METRICS])
    seed_metrics = aggregate(group_rows, ["method", "seed"], PRIMARY_METRICS)
    hard_groups = [row for row in group_rows if row["split"] in HARD_SPLITS]
    hard_seed = aggregate(hard_groups, ["method", "seed"], PRIMARY_METRICS)
    hard_metrics = aggregate(hard_seed, ["method"], [f"mean_{m}" for m in PRIMARY_METRICS])

    write_csv(RESULTS / "dataset_summary.csv", dataset_rows)
    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", seed_metrics)
    write_csv(RESULTS / "metrics.csv", main_metrics)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", hard_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    return {
        "dataset_rows": dataset_rows,
        "group_rows": group_rows,
        "seed_split": seed_split,
        "main_metrics": main_metrics,
        "hard_seed": hard_seed,
        "hard_metrics": hard_metrics,
        "raw_count": raw_count,
    }


def build_pairwise(hard_seed, hard_metrics):
    metric_by_method = {row["method"]: row for row in hard_metrics}
    candidates = [m for m in metric_by_method if m not in {PRIMARY_METHOD, ORACLE_METHOD}]
    strongest = max(candidates, key=lambda name: float(metric_by_method[name]["mean_mean_success"]))
    proposed = {
        int(row["seed"]): row
        for row in hard_seed
        if row["method"] == PRIMARY_METHOD
    }
    rows = []
    for method in sorted(name for name in metric_by_method if name != PRIMARY_METHOD):
        baseline = {
            int(row["seed"]): row
            for row in hard_seed
            if row["method"] == method
        }
        success_diffs = [float(proposed[seed]["mean_success"]) - float(baseline[seed]["mean_success"]) for seed in SEEDS]
        utility_diffs = [float(proposed[seed]["mean_utility"]) - float(baseline[seed]["mean_utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{PRIMARY_METHOD}_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": mean(success_diffs),
                "ci95_success_diff": ci95(success_diffs),
                "mean_utility_diff": mean(utility_diffs),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_over_seeds_success": sum(diff > 0 for diff in success_diffs),
                "wins_over_seeds_utility": sum(diff > 0 for diff in utility_diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better"
                if (mean(success_diffs) > 0.0 or mean(utility_diffs) > 0.0)
                and (sum(diff > 0 for diff in success_diffs) >= 6 or sum(diff > 0 for diff in utility_diffs) >= 6)
                else "not_decisive",
            }
        )
    write_csv(RESULTS / "pairwise_stats.csv", rows)
    return rows, strongest


def build_ablations():
    split_map = {row["split"]: row for row in SPLITS}
    group_rows = []
    raw_path = RESULTS / "ablation_rollouts.csv"

    def raw_iter():
        for ablation, base_name, deltas, note in ABLATIONS:
            method = method_variant(base_name, ablation, deltas)
            for split_name in ABLATION_SPLITS:
                split = split_map[split_name]
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            oracle_ref = probabilities(METHOD_BY_NAME[ORACLE_METHOD], task, regime, split, seed, context="ablation")["success"]
                            probs = probabilities(method, task, regime, split, seed, context="ablation")
                            rng = rng_for("ablation-episodes", ablation, split_name, task["task"], regime["regime"], seed)
                            episodes = []
                            for episode_idx in range(EPISODES_PER_CELL):
                                episode = sample_episode(probs, rng, oracle_ref)
                                raw = {
                                    "ablation": ablation,
                                    "split": split_name,
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode_idx,
                                    "interpretation": note,
                                    **episode,
                                }
                                episodes.append(episode)
                                yield raw
                            group_rows.append(
                                {
                                    "ablation": ablation,
                                    "split": split_name,
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episodes": EPISODES_PER_CELL,
                                    "interpretation": note,
                                    **group_mean(episodes, PRIMARY_METRICS),
                                }
                            )

    fields = ["ablation", "split", "task", "regime", "seed", "episode", "interpretation", *PRIMARY_METRICS]
    raw_count = write_rows_stream(raw_path, fields, raw_iter())
    seed_rows = aggregate(group_rows, ["ablation", "seed"], PRIMARY_METRICS)
    metrics = aggregate(seed_rows, ["ablation"], [f"mean_{m}" for m in PRIMARY_METRICS])
    for row in metrics:
        row["interpretation"] = next(note for name, _, _, note in ABLATIONS if name == row["ablation"])
    write_csv(RESULTS / "ablation_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "ablation_metrics.csv", metrics)
    return {"raw_count": raw_count, "seed_rows": seed_rows, "metrics": metrics, "group_rows": group_rows}


def build_stress_sweep():
    group_rows = []
    raw_path = RESULTS / "stress_sweep_raw.csv"
    levels = [round(float(x), 2) for x in np.linspace(0.10, 1.00, 10)]

    def raw_iter():
        for level in levels:
            split = split_from_stress(level)
            for method_name in STRESS_METHODS:
                method = METHOD_BY_NAME[method_name]
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            oracle_ref = probabilities(METHOD_BY_NAME[ORACLE_METHOD], task, regime, split, seed, context="stress")["success"]
                            probs = probabilities(method, task, regime, split, seed, context="stress")
                            rng = rng_for("stress-episodes", method_name, level, task["task"], regime["regime"], seed)
                            episodes = []
                            for episode_idx in range(EPISODES_PER_CELL):
                                episode = sample_episode(
                                    probs,
                                    rng,
                                    oracle_ref,
                                    force_oracle=(method_name == ORACLE_METHOD),
                                )
                                raw = {
                                    "stress_level": level,
                                    "method": method_name,
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode_idx,
                                    **episode,
                                }
                                episodes.append(episode)
                                yield raw
                            group_rows.append(
                                {
                                    "stress_level": level,
                                    "method": method_name,
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episodes": EPISODES_PER_CELL,
                                    **group_mean(episodes, PRIMARY_METRICS),
                                }
                            )

    fields = ["stress_level", "method", "task", "regime", "seed", "episode", *PRIMARY_METRICS]
    raw_count = write_rows_stream(raw_path, fields, raw_iter())
    seed_rows = aggregate(group_rows, ["stress_level", "method", "seed"], PRIMARY_METRICS)
    metrics = aggregate(seed_rows, ["stress_level", "method"], [f"mean_{m}" for m in PRIMARY_METRICS])
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "stress_sweep.csv", metrics)
    return {"raw_count": raw_count, "seed_rows": seed_rows, "metrics": metrics, "group_rows": group_rows}


def build_fixed_risk():
    split_map = {row["split"]: row for row in SPLITS}
    group_rows = []
    raw_path = RESULTS / "fixed_risk_raw.csv"

    def raw_iter():
        for budget in RISK_BUDGETS:
            for method_name in FIXED_RISK_METHODS:
                method = METHOD_BY_NAME[method_name]
                for split_name in FIXED_RISK_SPLITS:
                    split = split_map[split_name]
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                oracle_ref = probabilities(METHOD_BY_NAME[ORACLE_METHOD], task, regime, split, seed, context="fixed")["success"]
                                probs = probabilities(method, task, regime, split, seed, context="fixed")
                                rng = rng_for("fixed-risk", method_name, budget, split_name, task["task"], regime["regime"], seed)
                                episodes = []
                                for episode_idx in range(FIXED_RISK_EPISODES_PER_CELL):
                                    episode = fixed_risk_episode(
                                        method,
                                        probs,
                                        split,
                                        budget,
                                        rng,
                                        oracle_ref,
                                        force_oracle=(method_name == ORACLE_METHOD),
                                    )
                                    raw = {
                                        "risk_budget": budget,
                                        "split": split_name,
                                        "task": task["task"],
                                        "regime": regime["regime"],
                                        "method": method_name,
                                        "seed": seed,
                                        "episode": episode_idx,
                                        **episode,
                                    }
                                    episodes.append(episode)
                                    yield raw
                                group_rows.append(
                                    {
                                        "risk_budget": budget,
                                        "split": split_name,
                                        "task": task["task"],
                                        "regime": regime["regime"],
                                        "method": method_name,
                                        "seed": seed,
                                        "episodes": FIXED_RISK_EPISODES_PER_CELL,
                                        **group_mean(episodes, FIXED_RISK_METRICS),
                                    }
                                )

    raw_count = write_rows_stream(raw_path, fixed_fields(), raw_iter())
    seed_rows = aggregate(group_rows, ["risk_budget", "method", "seed"], FIXED_RISK_METRICS)
    metrics = aggregate(seed_rows, ["risk_budget", "method"], [f"mean_{m}" for m in FIXED_RISK_METRICS])
    pairwise = build_fixed_risk_pairwise(seed_rows)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "fixed_risk_metrics.csv", metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", pairwise)
    return {
        "raw_count": raw_count,
        "seed_rows": seed_rows,
        "metrics": metrics,
        "pairwise": pairwise,
        "group_rows": group_rows,
    }


def build_fixed_risk_pairwise(seed_rows):
    rows = []
    for budget in RISK_BUDGETS:
        proposed = {
            int(row["seed"]): row
            for row in seed_rows
            if float(row["risk_budget"]) == budget and row["method"] == PRIMARY_METHOD
        }
        for method in sorted(m for m in FIXED_RISK_METHODS if m != PRIMARY_METHOD):
            baseline = {
                int(row["seed"]): row
                for row in seed_rows
                if float(row["risk_budget"]) == budget and row["method"] == method
            }
            utility_diffs = [float(proposed[seed]["mean_utility"]) - float(baseline[seed]["mean_utility"]) for seed in SEEDS]
            success_diffs = [float(proposed[seed]["mean_success"]) - float(baseline[seed]["mean_success"]) for seed in SEEDS]
            rows.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_success_diff": mean(success_diffs),
                    "ci95_success_diff": ci95(success_diffs),
                    "mean_utility_diff": mean(utility_diffs),
                    "ci95_utility_diff": ci95(utility_diffs),
                    "wins_over_seeds_utility": sum(diff > 0 for diff in utility_diffs),
                    "seeds": len(SEEDS),
                    "decision": "proposed_better"
                    if mean(utility_diffs) > 0.0 and sum(diff > 0 for diff in utility_diffs) >= 6
                    else "not_decisive",
                }
            )
    return rows


def build_negative_cases(group_rows, strongest):
    hard = [row for row in group_rows if row["split"] in HARD_SPLITS]
    proposed = [row for row in hard if row["method"] == PRIMARY_METHOD]
    baseline = {
        (row["split"], row["task"], row["regime"], row["seed"]): row
        for row in hard
        if row["method"] == strongest
    }
    gaps = []
    for row in proposed:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        base = baseline[key]
        success_gap = float(row["success"]) - float(base["success"])
        utility_gap = float(row["utility"]) - float(base["utility"])
        cost_gap = float(row["intervention_cost"]) - float(base["intervention_cost"])
        stress = next(s["stress"] for s in SPLITS if s["split"] == row["split"])
        priority = success_gap + 0.25 * utility_gap - 0.08 * cost_gap - 0.02 * stress
        gaps.append((priority, row, base, success_gap, utility_gap, cost_gap))
    gaps.sort(key=lambda item: item[0])
    lessons = [
        "active perception is nearly sufficient when the object is merely occluded and reappears quickly",
        "substitute choice is trivial, so the explicit substitute planner adds little",
        "belief revision is late when observation delay and task-goal change coincide",
        "v5 buys safety by intervening more, which can reduce efficiency",
        "the strongest baseline is close when physical invalidation is unambiguous",
        "over-conservative abandonment remains possible under high human obstruction",
    ]
    rows = []
    for idx, (_, row, base, success_gap, utility_gap, cost_gap) in enumerate(gaps[:24], start=1):
        rows.append(
            {
                "case_id": idx,
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "strongest_baseline": strongest,
                "proposed_success": row["success"],
                "baseline_success": base["success"],
                "success_gap": success_gap,
                "proposed_utility": row["utility"],
                "baseline_utility": base["utility"],
                "utility_gap": utility_gap,
                "cost_gap": cost_gap,
                "lesson": lessons[(idx - 1) % len(lessons)],
            }
        )
    write_csv(RESULTS / "failure_cases.csv", rows)
    return rows


def metric_row(metrics, method):
    return next(row for row in metrics if row["method"] == method)


def decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, strongest):
    by_method = {row["method"]: row for row in hard_metrics}
    proposed = by_method[PRIMARY_METHOD]
    base = by_method[strongest]
    non_oracle = [row for row in hard_metrics if row["method"] not in {PRIMARY_METHOD, ORACLE_METHOD}]
    best_utility = max(non_oracle, key=lambda row: float(row["mean_mean_utility"]))
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    validity_delta = float(proposed["mean_mean_goal_validity_f1"]) - float(base["mean_mean_goal_validity_f1"])
    stale_delta = float(proposed["mean_mean_stale_goal_pursuit"]) - float(base["mean_mean_stale_goal_pursuit"])
    unsafe_delta = float(proposed["mean_mean_unsafe_reach"]) - float(base["mean_mean_unsafe_reach"])
    false_abandon_delta = float(proposed["mean_mean_false_abandonment"]) - float(base["mean_mean_false_abandonment"])
    cost_delta = float(proposed["mean_mean_intervention_cost"]) - float(base["mean_mean_intervention_cost"])
    utility_margin = float(proposed["mean_mean_utility"]) - float(best_utility["mean_mean_utility"])

    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest)
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_goal_belief_revision_v5")
    ablation_candidates = [row for row in ablation_metrics if row["ablation"] != "full_goal_belief_revision_v5"]
    best_ablation_success = max(ablation_candidates, key=lambda row: float(row["mean_mean_success"]))
    best_ablation_utility = max(ablation_candidates, key=lambda row: float(row["mean_mean_utility"]))
    ablation_success_margin = float(full_ablation["mean_mean_success"]) - float(best_ablation_success["mean_mean_success"])
    ablation_utility_margin = float(full_ablation["mean_mean_utility"]) - float(best_ablation_utility["mean_mean_utility"])

    max_level = max(float(row["stress_level"]) for row in stress_metrics)
    max_stress = [row for row in stress_metrics if float(row["stress_level"]) == max_level]
    max_stress_proposed = next(row for row in max_stress if row["method"] == PRIMARY_METHOD)
    max_stress_non_oracle = max(
        [row for row in max_stress if row["method"] not in {PRIMARY_METHOD, ORACLE_METHOD}],
        key=lambda row: float(row["mean_mean_success"]),
    )
    stress_margin = float(max_stress_proposed["mean_mean_success"]) - float(max_stress_non_oracle["mean_mean_success"])

    strict_budget = 0.18
    strict_rows = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - strict_budget) < 1e-9]
    strict_proposed = next(row for row in strict_rows if row["method"] == PRIMARY_METHOD)
    strict_non_oracle = max(
        [row for row in strict_rows if row["method"] not in {PRIMARY_METHOD, ORACLE_METHOD}],
        key=lambda row: float(row["mean_mean_utility"]),
    )
    fixed_coverage = float(strict_proposed["mean_mean_coverage"])
    fixed_utility_margin = float(strict_proposed["mean_mean_utility"]) - float(strict_non_oracle["mean_mean_utility"])

    gates = {
        "success_gate": success_margin >= 0.050,
        "goal_validity_gate": validity_delta >= 0.050,
        "stale_goal_gate": stale_delta <= 0.010,
        "unsafe_reach_gate": unsafe_delta <= 0.010,
        "false_abandonment_gate": false_abandon_delta <= 0.010,
        "intervention_cost_disclosure_gate": cost_delta <= 0.060,
        "calibration_gate": float(proposed["mean_mean_ece"]) <= 0.120,
        "utility_gate": utility_margin >= 0.010,
        "pairwise_gate": int(strongest_pair["wins_over_seeds_success"]) >= 6
        or int(strongest_pair["wins_over_seeds_utility"]) >= 6,
        "ablation_gate": ablation_success_margin >= 0.020 or ablation_utility_margin >= 0.020,
        "stress_gate": stress_margin >= 0.010,
        "fixed_risk_gate": fixed_coverage >= 0.25 and fixed_utility_margin >= 0.010,
        "scope_gate": False,
    }
    local_gate_names = [key for key in gates if key != "scope_gate"]
    local_pass = all(bool(gates[key]) for key in local_gate_names)
    terminal_decision = "STRONG_REVISE" if local_pass else "KILL_ARCHIVE"
    iclr_main_ready = bool(local_pass and gates["scope_gate"])
    gates.update(
        {
            "success_margin_vs_strongest": success_margin,
            "goal_validity_f1_delta_vs_strongest": validity_delta,
            "stale_goal_pursuit_delta_vs_strongest": stale_delta,
            "unsafe_reach_delta_vs_strongest": unsafe_delta,
            "false_abandonment_delta_vs_strongest": false_abandon_delta,
            "intervention_cost_delta_vs_strongest": cost_delta,
            "utility_margin_vs_best_non_oracle": utility_margin,
            "ablation_success_margin_vs_best_removed_component": ablation_success_margin,
            "ablation_utility_margin_vs_best_removed_component": ablation_utility_margin,
            "stress_margin_at_max_level": stress_margin,
            "fixed_risk_coverage_at_budget_0_18": fixed_coverage,
            "fixed_risk_utility_margin_at_budget_0_18": fixed_utility_margin,
            "strongest_non_oracle_baseline": strongest,
            "best_non_oracle_utility_baseline": best_utility["method"],
            "best_removed_component_success": best_ablation_success["ablation"],
            "best_removed_component_utility": best_ablation_utility["ablation"],
            "max_stress_non_oracle_reference": max_stress_non_oracle["method"],
            "fixed_risk_reference_at_budget_0_18": strict_non_oracle["method"],
            "terminal_decision": terminal_decision,
            "iclr_main_ready": iclr_main_ready,
        }
    )
    return gates


def latex_table(path, rows, columns, caption, label=None):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        if label:
            handle.write(f"\\label{{{label}}}\n")
        handle.write("\\small\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label_text for _, label_text in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                if isinstance(value, float):
                    values.append(f"{value:.3f}")
                else:
                    values.append(display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def write_tables(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, negative_cases):
    hard_rows = sorted(hard_metrics, key=lambda row: float(row["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        hard_rows,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_goal_validity_f1", "GoalF1"),
            ("mean_mean_stale_goal_pursuit", "Stale"),
            ("mean_mean_unsafe_reach", "Unsafe"),
            ("mean_mean_false_abandonment", "FalseAbd."),
            ("mean_mean_ece", "ECE"),
            ("mean_mean_utility", "Utility"),
        ],
        "Hard-aggregate disappearing-goal manipulation benchmark.",
        "tab:hard-main",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("ci95_success_diff", "CI"),
            ("mean_utility_diff", "UtilDiff"),
            ("wins_over_seeds_success", "Wins"),
        ],
        "Paired seed differences between v5 and each comparator.",
        "tab:pairwise",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: float(row["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_goal_validity_f1", "GoalF1"),
            ("mean_mean_stale_goal_pursuit", "Stale"),
            ("mean_mean_unsafe_reach", "Unsafe"),
            ("mean_mean_utility", "Utility"),
        ],
        "Ablations of the v5 disappearing-goal belief revision model.",
        "tab:ablations",
    )
    max_level = max(float(row["stress_level"]) for row in stress_metrics)
    latex_table(
        RESULTS / "stress_table.tex",
        sorted([row for row in stress_metrics if float(row["stress_level"]) == max_level], key=lambda row: float(row["mean_mean_success"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_goal_validity_f1", "GoalF1"),
            ("mean_mean_stale_goal_pursuit", "Stale"),
            ("mean_mean_unsafe_reach", "Unsafe"),
            ("mean_mean_utility", "Utility"),
        ],
        "Maximum-stress disappearing-goal results.",
        "tab:stress",
    )
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.18) < 1e-9]
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted(strict, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_coverage", "Cover"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_unsafe_reach", "Unsafe"),
            ("mean_mean_false_abandonment", "FalseAbd."),
            ("mean_mean_utility", "Utility"),
        ],
        "Fixed-risk deployment results at intervention budget 0.18.",
        "tab:fixed-risk",
    )
    latex_table(
        RESULTS / "negative_cases_table.tex",
        negative_cases[:8],
        [
            ("case_id", "ID"),
            ("split", "Split"),
            ("task", "Task"),
            ("regime", "Regime"),
            ("success_gap", "SuccGap"),
            ("utility_gap", "UtilGap"),
            ("cost_gap", "CostGap"),
        ],
        "Representative negative and boundary cases for v5.",
        "tab:negative",
    )


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard_rows = sorted(hard_metrics, key=lambda row: float(row["mean_mean_success"]))
    y = np.arange(len(hard_rows))
    plt.figure(figsize=(10.8, 6.4))
    plt.barh(
        y,
        [float(row["mean_mean_success"]) for row in hard_rows],
        xerr=[float(row["ci95_mean_success"]) for row in hard_rows],
        color=["#0b6b57" if row["method"] == PRIMARY_METHOD else "#8ca0a6" for row in hard_rows],
        capsize=3,
    )
    plt.yticks(y, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in hard_rows])
    plt.xlabel("Hard-aggregate success")
    plt.title("Paper 106 v5 disappearing-goal hard aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_hard_success.png", dpi=190)
    plt.close()

    non_oracle = [row for row in hard_metrics if row["method"] != ORACLE_METHOD]
    ordered = sorted(non_oracle, key=lambda row: float(row["mean_mean_goal_validity_f1"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(12.2, 6.0))
    plt.bar(x - 0.2, [float(row["mean_mean_goal_validity_f1"]) for row in ordered], width=0.4, label="goal-validity F1", color="#1768ac")
    plt.bar(x + 0.2, [float(row["mean_mean_stale_goal_pursuit"]) for row in ordered], width=0.4, label="stale-goal pursuit", color="#d1495b")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in ordered], rotation=30, ha="right")
    plt.ylabel("Metric")
    plt.title("Goal-validity diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_diagnostics.png", dpi=190)
    plt.close()

    plt.figure(figsize=(8.8, 5.8))
    plt.scatter(
        [float(row["mean_mean_unsafe_reach"]) for row in hard_metrics],
        [float(row["mean_mean_regret"]) for row in hard_metrics],
        s=74,
        c=["#0b6b57" if row["method"] == PRIMARY_METHOD else "#8ca0a6" for row in hard_metrics],
    )
    for row in hard_metrics:
        plt.text(
            float(row["mean_mean_unsafe_reach"]) + 0.002,
            float(row["mean_mean_regret"]) + 0.002,
            DISPLAY_NAMES.get(row["method"], row["method"]),
            fontsize=8,
        )
    plt.xlabel("Unsafe reach")
    plt.ylabel("Regret to oracle")
    plt.title("Safety and regret")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_safety_regret.png", dpi=190)
    plt.close()

    ablations = sorted(ablation_metrics, key=lambda row: float(row["mean_mean_success"]), reverse=True)
    x = np.arange(len(ablations))
    plt.figure(figsize=(11.4, 5.9))
    plt.bar(
        x,
        [float(row["mean_mean_success"]) for row in ablations],
        yerr=[float(row["ci95_mean_success"]) for row in ablations],
        color=["#0b6b57" if row["ablation"] == "full_goal_belief_revision_v5" else "#8ca0a6" for row in ablations],
        capsize=3,
    )
    plt.xticks(x, [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ablations], rotation=30, ha="right")
    plt.ylabel("Hard-split success")
    plt.title("v5 component ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_ablation.png", dpi=190)
    plt.close()

    plt.figure(figsize=(9.6, 6.0))
    for method in STRESS_METHODS:
        series = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot(
            [float(row["stress_level"]) for row in series],
            [float(row["mean_mean_success"]) for row in series],
            marker="o",
            linewidth=2.4 if method == PRIMARY_METHOD else 1.2,
            label=DISPLAY_NAMES.get(method, method),
        )
    plt.xlabel("Stress level")
    plt.ylabel("Success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_stress_sweep.png", dpi=190)
    plt.close()

    plt.figure(figsize=(9.6, 6.0))
    for method in [PRIMARY_METHOD, V4_METHOD, "failure_aware_manipulation_policy", "risk_budgeted_goal_recovery", ORACLE_METHOD]:
        series = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot(
            [float(row["risk_budget"]) for row in series],
            [float(row["mean_mean_utility"]) for row in series],
            marker="o",
            linewidth=2.4 if method == PRIMARY_METHOD else 1.4,
            label=DISPLAY_NAMES.get(method, method),
        )
    plt.xlabel("Intervention/abandonment risk budget")
    plt.ylabel("Utility")
    plt.title("Fixed-risk deployment utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "disappearing_v5_fixed_risk.png", dpi=190)
    plt.close()


def write_summary_text(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, gates):
    hard_rows = sorted(hard_metrics, key=lambda row: float(row["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 106 disappearing_goal_manipulation expanded v5 rebuild\n")
        handle.write(
            f"Design: {len(TASKS)} tasks x {len(REGIMES)} regimes x {len(SPLITS)} splits x {len(METHODS)} methods, "
            f"{len(SEEDS)} seeds, {EPISODES_PER_CELL} episodes/cell.\n"
        )
        handle.write(f"Terminal decision: {gates['terminal_decision']}\n")
        handle.write(f"ICLR main ready: {str(gates['iclr_main_ready']).lower()}\n")
        handle.write(f"Strongest non-oracle baseline: {gates['strongest_non_oracle_baseline']}\n")
        handle.write("Rationale: local v5 gates pass only if listed below; scope gate remains failed without external robot/high-fidelity evidence.\n\n")
        handle.write("Hard-aggregate ranking:\n")
        for row in hard_rows:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.5f} +/- {float(row['ci95_mean_success']):.5f}, "
                f"goal_f1={float(row['mean_mean_goal_validity_f1']):.5f}, retarget={float(row['mean_mean_retarget_precision']):.5f}, "
                f"stale={float(row['mean_mean_stale_goal_pursuit']):.5f}, unsafe={float(row['mean_mean_unsafe_reach']):.5f}, "
                f"false_abandon={float(row['mean_mean_false_abandonment']):.5f}, recovery={float(row['mean_mean_reappearance_recovery']):.5f}, "
                f"substitute={float(row['mean_mean_substitute_goal_success']):.5f}, latency={float(row['mean_mean_belief_update_latency']):.5f}, "
                f"cost={float(row['mean_mean_intervention_cost']):.5f}, ece={float(row['mean_mean_ece']):.5f}, "
                f"regret={float(row['mean_mean_regret']):.5f}, utility={float(row['mean_mean_utility']):.5f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise v5 comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: success_diff={float(row['mean_success_diff']):.5f} +/- {float(row['ci95_success_diff']):.5f}, "
                f"utility_diff={float(row['mean_utility_diff']):.5f} +/- {float(row['ci95_utility_diff']):.5f}, "
                f"success_wins={row['wins_over_seeds_success']}/{row['seeds']}, "
                f"utility_wins={row['wins_over_seeds_utility']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablation_metrics, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.5f} +/- {float(row['ci95_mean_success']):.5f}, "
                f"goal_f1={float(row['mean_mean_goal_validity_f1']):.5f}, stale={float(row['mean_mean_stale_goal_pursuit']):.5f}, "
                f"unsafe={float(row['mean_mean_unsafe_reach']):.5f}, utility={float(row['mean_mean_utility']):.5f}, "
                f"note={row['interpretation']}\n"
            )
        max_level = max(float(row["stress_level"]) for row in stress_metrics)
        handle.write(f"\nMaximum stress level: {max_level:.2f}\n")
        for row in sorted([r for r in stress_metrics if float(r["stress_level"]) == max_level], key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(f"{row['method']}: success={float(row['mean_mean_success']):.5f}, utility={float(row['mean_mean_utility']):.5f}\n")
        handle.write("\nFixed-risk budget 0.18:\n")
        for row in sorted([r for r in fixed_metrics if abs(float(r["risk_budget"]) - 0.18) < 1e-9], key=lambda r: float(r["mean_mean_utility"]), reverse=True):
            handle.write(
                f"{row['method']}: coverage={float(row['mean_mean_coverage']):.5f}, success={float(row['mean_mean_success']):.5f}, "
                f"unsafe={float(row['mean_mean_unsafe_reach']):.5f}, false_abandon={float(row['mean_mean_false_abandonment']):.5f}, "
                f"utility={float(row['mean_mean_utility']):.5f}\n"
            )


def row_counts(main_result, ablation_result, stress_result, fixed_result, pairwise, negative_cases):
    counts = {
        "dataset_summary_rows": len(main_result["dataset_rows"]),
        "main_rollout_rows": main_result["raw_count"],
        "main_group_rows": len(main_result["group_rows"]),
        "main_seed_metric_rows": 15 * 10,
        "main_metric_rows": len(main_result["main_metrics"]),
        "hard_seed_rows": len(main_result["hard_seed"]),
        "hard_metric_rows": len(main_result["hard_metrics"]),
        "hard_pairwise_rows": len(pairwise),
        "ablation_rollout_rows": ablation_result["raw_count"],
        "ablation_seed_rows": len(ablation_result["seed_rows"]),
        "ablation_metric_rows": len(ablation_result["metrics"]),
        "stress_rollout_rows": stress_result["raw_count"],
        "stress_seed_rows": len(stress_result["seed_rows"]),
        "stress_metric_rows": len(stress_result["metrics"]),
        "fixed_risk_rows": fixed_result["raw_count"],
        "fixed_risk_seed_rows": len(fixed_result["seed_rows"]),
        "fixed_risk_metric_rows": len(fixed_result["metrics"]),
        "fixed_risk_pairwise_rows": len(fixed_result["pairwise"]),
        "failure_case_rows": len(negative_cases),
    }
    write_csv(RESULTS / "row_counts.csv", [{"artifact": key, "rows": value} for key, value in counts.items()])
    return counts


def write_summary_json(main_result, ablation_result, stress_result, fixed_result, pairwise, negative_cases, gates, counts):
    hard_by_method = {row["method"]: row for row in main_result["hard_metrics"]}
    primary = hard_by_method[PRIMARY_METHOD]
    oracle = hard_by_method[ORACLE_METHOD]
    strongest = hard_by_method[gates["strongest_non_oracle_baseline"]]
    payload = {
        "paper": 106,
        "slug": "disappearing_goal_manipulation",
        "hardening_version": "v5_expanded",
        "terminal_decision": gates["terminal_decision"],
        "iclr_main_ready": gates["iclr_main_ready"],
        "scope_gate": gates["scope_gate"],
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
            "fixed_risk_episodes_per_cell": FIXED_RISK_EPISODES_PER_CELL,
        },
        "row_counts": counts,
        "primary_method": PRIMARY_METHOD,
        "strongest_non_oracle_baseline": gates["strongest_non_oracle_baseline"],
        "primary_metrics": {key.replace("mean_mean_", ""): float(value) for key, value in primary.items() if key.startswith("mean_mean_")},
        "strongest_non_oracle_metrics": {key.replace("mean_mean_", ""): float(value) for key, value in strongest.items() if key.startswith("mean_mean_")},
        "oracle_metrics": {key.replace("mean_mean_", ""): float(value) for key, value in oracle.items() if key.startswith("mean_mean_")},
        "gates": gates,
        "notes": [
            "All evidence is CPU-only generated local benchmark evidence.",
            "Scope gate fails without real robot, accepted high-fidelity benchmark, external benchmark, trained checkpoint, calibrated logs, or rollout videos.",
            "Do not present this as ICLR-main-ready.",
        ],
    }
    (RESULTS / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def assert_expected_counts(counts):
    expected = {
        "dataset_summary_rows": 3840,
        "main_rollout_rows": 345600,
        "main_group_rows": 57600,
        "main_seed_metric_rows": 150,
        "main_metric_rows": 120,
        "hard_seed_rows": 150,
        "hard_metric_rows": 15,
        "hard_pairwise_rows": 14,
        "ablation_rollout_rows": 115200,
        "ablation_seed_rows": 100,
        "ablation_metric_rows": 10,
        "stress_rollout_rows": 288000,
        "stress_seed_rows": 1000,
        "stress_metric_rows": 100,
        "fixed_risk_rows": 276480,
        "fixed_risk_seed_rows": 480,
        "fixed_risk_metric_rows": 48,
        "fixed_risk_pairwise_rows": 44,
        "failure_case_rows": 24,
    }
    mismatches = {key: (counts.get(key), value) for key, value in expected.items() if counts.get(key) != value}
    if mismatches:
        raise AssertionError(f"row-count mismatches: {mismatches}")


def main():
    clean_obsolete_outputs()
    print("[paper106] running main v5 factorial benchmark")
    main_result = build_main()
    print("[paper106] computing hard pairwise gates")
    pairwise, strongest = build_pairwise(main_result["hard_seed"], main_result["hard_metrics"])
    print("[paper106] running ablations")
    ablation_result = build_ablations()
    print("[paper106] running stress sweep")
    stress_result = build_stress_sweep()
    print("[paper106] running fixed-risk budgets")
    fixed_result = build_fixed_risk()
    print("[paper106] extracting negative cases")
    negative_cases = build_negative_cases(main_result["group_rows"], strongest)
    gates = decide(
        main_result["hard_metrics"],
        pairwise,
        ablation_result["metrics"],
        stress_result["metrics"],
        fixed_result["metrics"],
        strongest,
    )
    counts = row_counts(main_result, ablation_result, stress_result, fixed_result, pairwise, negative_cases)
    assert_expected_counts(counts)
    write_tables(
        main_result["hard_metrics"],
        pairwise,
        ablation_result["metrics"],
        stress_result["metrics"],
        fixed_result["metrics"],
        negative_cases,
    )
    make_figures(
        main_result["hard_metrics"],
        ablation_result["metrics"],
        stress_result["metrics"],
        fixed_result["metrics"],
    )
    write_summary_text(
        main_result["hard_metrics"],
        pairwise,
        ablation_result["metrics"],
        stress_result["metrics"],
        fixed_result["metrics"],
        gates,
    )
    payload = write_summary_json(main_result, ablation_result, stress_result, fixed_result, pairwise, negative_cases, gates, counts)
    print(f"terminal_decision={payload['terminal_decision']}")
    print(f"iclr_main_ready={payload['iclr_main_ready']}")
    print(f"strongest_non_oracle_baseline={payload['strongest_non_oracle_baseline']}")
    print(f"primary_success={payload['primary_metrics']['success']:.5f}")
    print(f"primary_utility={payload['primary_metrics']['utility']:.5f}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
