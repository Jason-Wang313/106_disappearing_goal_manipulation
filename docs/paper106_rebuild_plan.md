# Paper 106 Rebuild Plan: Disappearing Goal Manipulation

Started: 2026-06-15 00:31:00 +0100

## Goal

Rebuild Paper 106 from a v3 archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that a manipulation policy can reason about goals that disappear during execution, distinguishing perceptual disappearance from physical invalidation and safely retargeting, waiting, or abandoning when necessary.

## Claimed Mechanism

The proposed method, `proposed_disappearing_goal_belief_revision`, maintains a goal-validity belief graph over:

- object/goal occlusion;
- moved targets;
- removed targets;
- temporary human obstruction;
- task-goal invalidation;
- stale memory of last-seen goals;
- substitute-goal feasibility;
- abandonment and retargeting costs.

It should avoid blindly pursuing stale goals, but also avoid over-abandoning goals that are merely occluded or temporarily unavailable.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 tasks: shelf retrieval, drawer placement, bin sorting, tool handoff, and mobile pick-and-place.
- 7 disappearing-goal regimes: visual occlusion, object moved, object removed, human temporary obstruction, goal specification changed, substitute goal available, and cascading disappearing goal.
- 5 splits: nominal, occlusion-heavy shift, physical-removal shift, delayed reappearance, and combined disappearance stress.
- 9 methods: last-seen goal pursuit, memory-only belief tracking, uncertainty halt, active viewpoint reacquisition, POMDP belief planner, goal retargeting heuristic, failure-aware manipulation policy, proposed disappearing-goal belief revision, and oracle goal-state supervisor.
- 7 random seeds with independent task/regime groups.
- 84 episodes per task/regime/split/method group.

## Evidence Requirements

The rebuild must produce:

- Task success, goal-validity F1, retarget precision, stale-goal pursuit rate, unsafe reach rate, false abandonment rate, reappearance recovery, substitute-goal success, belief update latency, intervention cost, and regret to oracle.
- Per-task/per-regime breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over disappearance/reappearance intensity.
- Ablations for observation-memory separation, active reacquisition, physical-validity test, substitute-goal planner, and abandonment calibration.
- Failure cases explaining where retargeting is unnecessary, too conservative, or dominated by active perception.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-disappearance task success by at least 0.030.
- Improves goal-validity F1 or reduces stale-goal pursuit over the strongest non-oracle baseline by at least 0.050.
- Does not buy success by increasing unsafe reaches, false abandonment, or intervention cost.
- Wins paired seed comparisons against the strongest non-oracle baseline in at least 5/7 seeds.
- Survives core ablations: removing observation-memory separation, active reacquisition, physical-validity testing, substitute-goal planning, or abandonment calibration must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared v3 probability script with a paper-specific disappearing-goal manipulation benchmark.
2. Generate metrics, seed metrics, per-task/per-regime tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `106.pdf` to `C:/Users/wangz/Downloads/106.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, regimes, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.
