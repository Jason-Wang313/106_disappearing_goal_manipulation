# Hostile Reviewer Response

Paper: 106 Disappearing Goal Manipulation

## Strongest Technical Threats

- POMDP and partially observable task-and-motion planning already model hidden state and belief-aware action choice.
- Active perception and object-search methods already reacquire occluded goals through camera or viewpoint actions.
- Goal-conditioned RL and hindsight relabeling already use alternative goals and sparse reward relabeling.
- VLA and language-conditioned manipulation systems already condition policies on changing task prompts and scene context.
- Goal retargeting and failure-aware manipulation baselines already handle some moved, blocked, or invalid goals.

## ICLR Main Response

The v4 rebuild narrows the claim to goal-validity belief revision under disappearance. The proposed method is not a generic POMDP planner, not a pure active-view baseline, and not just goal relabeling. It explicitly separates "unseen but still valid" from "physically invalid or changed", and it calibrates when to wait, reacquire, retarget, use a substitute goal, or abandon.

The local benchmark supports that narrower boundary: proposed combined-disappearance success is `0.662 +/- 0.009` versus `0.561 +/- 0.003` for `failure_aware_manipulation_policy`; goal-validity F1 improves by `0.148`; stale-goal pursuit drops by `0.046`; unsafe reach and false abandonment both decrease; and the strongest-baseline paired comparison is 7/7 seeds in favor of the proposed method.

## Remaining Hostile Review

A hostile reviewer would still be right to reject a main-track submission today if it claimed deployment readiness. The evidence is local and synthetic; the baselines are diagnostic executable models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator result.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, implemented learned baselines, and qualitative rollouts.
