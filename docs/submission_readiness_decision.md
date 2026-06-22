# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5 expanded rebuild provides a paper-specific local benchmark for disappearing-goal manipulation, with strong synthetic baselines, the v4 method as the strongest non-oracle comparator, ablations, paired seed comparisons, stress sweeps, fixed-risk budgets, negative cases, finite CSV artifacts, generated figures/tables, and a validated 25-page PDF.

The evidence supports the mechanism locally: `risk_calibrated_goal_belief_revision_v5` reaches hard success `0.77454` versus `0.69618` for `proposed_disappearing_goal_belief_revision_v4`, improves goal-validity F1 from `0.64239` to `0.72880`, reduces stale-goal pursuit from `0.04468` to `0.01238`, reduces unsafe reach from `0.01424` to `0.00087`, reduces false abandonment from `0.03854` to `0.00851`, and improves utility from `0.55683` to `0.70495`.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, external benchmark evidence, trained checkpoints, calibrated deployment logs, and qualitative rollouts.
