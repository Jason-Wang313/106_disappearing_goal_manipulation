# Submission Readiness Audit v4.1

Paper: 106 `disappearing_goal_manipulation`

Audit date: 2026-06-15 16:58:40 +0100

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/106_disappearing_goal_manipulation_continuation_rerun_20260615.log`
- Benchmark coverage: 5 tasks x 7 disappearing-goal regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `failure_aware_manipulation_policy`.
- Terminal decision emitted by runner: `STRONG_REVISE`.

## CSV Integrity

- `metrics.csv`: 45 rows, finite numeric fields.
- `per_task_regime_metrics.csv`: 1575 rows, finite numeric fields.
- `seed_task_regime_metrics.csv`: 11025 rows, finite numeric fields.
- `seed_split_metrics.csv`: 315 rows, finite numeric fields.
- `pairwise_stats.csv`: 8 rows, finite numeric fields.
- `ablation_metrics.csv`: 7 rows, finite numeric fields.
- `ablation_seed_metrics.csv`: 49 rows, finite numeric fields.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows, finite numeric fields.
- `stress_sweep.csv`: 30 rows, finite numeric fields.
- `stress_sweep_seed_metrics.csv`: 7350 rows, finite numeric fields.
- `failure_cases.csv`: 8 rows, finite numeric fields.

## Main Result

On combined-disappearance stress, proposed disappearing-goal belief revision reaches `0.662 +/- 0.009` success versus `0.561 +/- 0.003` for `failure_aware_manipulation_policy`, a margin of `+0.102 +/- 0.008`. Proposed also improves goal-validity F1 from `0.439` to `0.586`, reduces stale-goal pursuit from `0.133` to `0.087`, reduces unsafe reach from `0.063` to `0.039`, and reduces false abandonment from `0.092` to `0.053`.

Intervention cost increases from `0.226` to `0.247`. This does not kill the claim because the predefined safety and diagnostic gates improve, but it must be disclosed as a tradeoff.

## Pairwise And Ablations

- Pairwise seed test against the strongest non-oracle baseline: `7/7` wins.
- Full ablation success: `0.665 +/- 0.004`.
- Best removed component: `minus_abandonment_calibration` at `0.636 +/- 0.005`.
- Ablation margin over best removed component: `+0.029`.

## Stress Sweep

Stress levels: `0.10`, `0.27`, `0.44`, `0.61`, `0.78`, `0.95`.

At maximum stress level `0.95`, proposed success is `0.661 +/- 0.007` versus `0.547 +/- 0.009` for the strongest non-oracle baseline and `0.795 +/- 0.006` for the oracle. Proposed also keeps higher goal-validity F1 (`0.571` vs `0.422`), lower stale-goal pursuit (`0.088` vs `0.143`), lower unsafe reach (`0.038` vs `0.065`), lower false abandonment (`0.054` vs `0.097`), and lower belief-update latency (`0.700` vs `0.823`) than the strongest non-oracle baseline.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continuing the project, but it does not make the paper ICLR-main-ready. A real submission needs real robot or independent high-fidelity simulator validation, external learned baselines, qualitative rollouts, and a stronger prior-work positioning section grounded in those external results.
