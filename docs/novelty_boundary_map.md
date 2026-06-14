# Novelty Boundary Map

## Crowded Territory

- Generic POMDP planning.
- Generic active perception.
- Generic goal-conditioned RL or HER-style relabeling.
- Prompt-conditioned VLA policies.
- Safety halting or failure-aware recovery without goal-validity structure.
- Benchmark-only contribution.

## Claimed Boundary

Disappearing-goal manipulation keeps separate goal-validity states for hidden, moved, removed, changed, substitutable, and cascading goals, then calibrates whether the robot should wait, reacquire, retarget, substitute, or abandon.

## What Would Falsify The Claim

If a POMDP planner, active-perception baseline, goal-retargeting heuristic, or failure-aware manipulation policy matches the proposed method on success, goal-validity F1, stale-goal pursuit, unsafe reach, false abandonment, and ablation robustness under external robot validation, the paper should be killed.
