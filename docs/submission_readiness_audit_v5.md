# Submission Readiness Audit v5

Paper: 106 `disappearing_goal_manipulation`

Audit date: 2026-06-22

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Benchmark coverage: 6 tasks x 8 disappearing-goal regimes x 8 splits x 15 methods.
- Repeats: 10 seeds, 6 episodes per factorial cell.
- Strongest non-oracle baseline: `proposed_disappearing_goal_belief_revision_v4`.
- Terminal decision emitted by runner: `STRONG_REVISE`.

## CSV Integrity

- `dataset_summary.csv`: 3,840 rows.
- `rollouts.csv`: 345,600 rows.
- `main_group_metrics.csv`: 57,600 rows.
- `metrics.csv`: 120 rows.
- `hard_aggregate_seed_metrics.csv`: 150 rows.
- `hard_aggregate_metrics.csv`: 15 rows.
- `pairwise_stats.csv`: 14 rows.
- `ablation_rollouts.csv`: 115,200 rows.
- `stress_sweep_raw.csv`: 288,000 rows.
- `fixed_risk_raw.csv`: 276,480 rows.
- `failure_cases.csv`: 24 rows.

## Main Result

V5 reaches hard success `0.77454` versus `0.69618` for v4, a margin of `0.07836`. It improves goal-validity F1 from `0.64239` to `0.72880`, stale-goal pursuit from `0.04468` to `0.01238`, unsafe reach from `0.01424` to `0.00087`, false abandonment from `0.03854` to `0.00851`, and utility from `0.55683` to `0.70495`.

Intervention cost increases from `0.24998` to `0.27249`. This is disclosed as a safety/validity/utility tradeoff, not a free efficiency gain.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continued work, but it does not make the paper ICLR-main-ready. A real submission needs real robot or independent high-fidelity simulator validation, external learned baselines, qualitative rollouts, trained checkpoints, calibrated logs, and stronger manual prior-work positioning.
