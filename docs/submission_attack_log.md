# Submission Attack Log

Paper: 106 disappearing_goal_manipulation

This v4 pass rebuilds the paper around a stronger local evidence package. The result is STRONG_REVISE, not main-track submission.

## Attack 1: This is just POMDP planning.

Verdict: Partly threatening, not fatal locally.

Action: The paper narrows the contribution to disappearing-goal validity states and reports a `pomdp_belief_planner` baseline. Proposed combined-stress success is `0.662 +/- 0.009` versus POMDP `0.538 +/- 0.007`.

## Attack 2: Active perception already solves hidden goals.

Verdict: Threatening but insufficient.

Action: Active viewpoint reacquisition is a baseline. It helps delayed reappearance but lacks physical invalidation and substitute-goal reasoning; combined-stress success is `0.504 +/- 0.006`.

## Attack 3: Retargeting heuristics already solve substitute goals.

Verdict: Threatening but insufficient.

Action: A goal-retargeting heuristic is included. Proposed success is higher, with better goal-validity F1 and lower stale-goal pursuit.

## Attack 4: The method may win by over-abandoning.

Verdict: Addressed locally.

Action: False abandonment decreases from `0.092` for the strongest non-oracle baseline to `0.053` for the proposed method.

## Attack 5: The method may win by unsafe stale pursuit.

Verdict: Addressed locally.

Action: Unsafe reach decreases from `0.063` to `0.039`; stale-goal pursuit decreases from `0.133` to `0.087`.

## Attack 6: Ablations may not support the mechanism.

Verdict: Passed locally.

Action: The full model reaches `0.665 +/- 0.004`; the best removed component, `minus_abandonment_calibration`, reaches `0.636 +/- 0.005`.

## Attack 7: The benchmark might be saturated.

Verdict: Not saturated.

Action: Oracle success remains higher at `0.803 +/- 0.007`, leaving a meaningful ceiling gap.

## Attack 8: No real robot or external simulator validates the result.

Verdict: Fatal for immediate submission.

Action: Mark STRONG_REVISE, not ready-to-submit. Require external validation before main-track submission.

## Terminal Condition

The paper earns continued development because the local gates pass, but it does not earn ICLR-main readiness. Terminal state for this pass: STRONG_REVISE.
