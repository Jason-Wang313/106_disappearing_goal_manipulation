# Hostile Reviewer Response

Paper: 106 Disappearing Goal Manipulation

## Strongest Technical Threats

- POMDP and partially observable task-and-motion planning already model hidden state and belief-aware action choice.
- Active perception and object-search methods already reacquire occluded goals through camera or viewpoint actions.
- Goal-conditioned RL and hindsight relabeling already use alternative goals and sparse reward relabeling.
- VLA and language-conditioned manipulation systems already condition policies on changing task prompts and scene context.
- Goal retargeting, robust MPC replanning, conformal validity filtering, learned goal-state classification, and failure-aware manipulation baselines already handle parts of the problem.

## v5 Response

The v5 rebuild narrows the claim to risk-calibrated goal-validity belief revision under mixed disappearance causes. It is not a generic POMDP planner, not pure active view selection, not just retargeting, and not just conservative halting. It separates hidden-valid, moved, removed, changed, delayed, human-obstructed, substitute-valid, and cascading cases, then chooses among continuing, waiting, reacquiring, retargeting, substituting, recovering, or abandoning under a fixed-risk utility rule.

The strongest non-oracle baseline is the previous v4 belief-revision method, not a weak strawman. V5 reaches hard success `0.77454` vs `0.69618`, goal-validity F1 `0.72880` vs `0.64239`, stale-goal pursuit `0.01238` vs `0.04468`, unsafe reach `0.00087` vs `0.01424`, false abandonment `0.00851` vs `0.03854`, and utility `0.70495` vs `0.55683`.

## Remaining Hostile Review

A hostile reviewer would still be right to reject a main-track submission today if it claimed deployment readiness. The evidence is local and CPU-only; the baselines are diagnostic executable models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator result.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, implemented learned baselines, calibrated logs, trained checkpoints, and qualitative rollouts.
