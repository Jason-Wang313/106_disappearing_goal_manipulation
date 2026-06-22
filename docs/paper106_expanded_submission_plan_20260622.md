# Paper 106 Expanded Submission Plan

Date: 2026-06-22

Paper: `106_disappearing_goal_manipulation`

Target: rebuild the v4.1 local audit into a 25+ page hostile-review v5 evidence package. The paper must test whether disappearing-goal manipulation needs explicit goal-validity belief revision, rather than last-seen pursuit, active perception alone, POMDP-style belief planning, retargeting heuristics, conservative halting, failure-aware recovery, or risk-filtered deployment.

## Frozen Claim

Manipulation goals can disappear for different physical reasons: perceptual occlusion, moved objects, removed objects, temporary human obstruction, task-goal changes, substitute-goal availability, delayed reappearance, or coupled cascades. A robust robot policy must separate perceptual absence from physical invalidation, motion, task change, substitute feasibility, and abandonment risk.

The v5 method must beat strong non-oracle baselines while reporting the cost of extra interventions honestly. The paper must not claim ICLR-main readiness unless external robot or accepted high-fidelity validation exists. Local CPU-only evidence can support only `STRONG_REVISE`.

## Frozen Design

The v5 runner will use a RAM-light streaming design with raw rollout persistence:

- 6 tasks: `shelf_retrieval`, `drawer_placement`, `bin_sorting`, `tool_handoff`, `mobile_pick_and_place`, `cabinet_restocking`.
- 8 disappearing-goal regimes: `visual_occlusion`, `object_moved`, `object_removed`, `human_temporary_obstruction`, `goal_specification_changed`, `substitute_goal_available`, `delayed_reappearance`, `cascading_disappearing_goal`.
- 8 splits: `nominal`, `occlusion_heavy_shift`, `physical_removal_shift`, `delayed_reappearance_shift`, `goal_change_shift`, `substitute_ambiguity_shift`, `human_obstruction_shift`, `combined_extreme`.
- 15 methods: `last_seen_goal_pursuit`, `memory_only_belief_tracking`, `uncertainty_halt`, `active_viewpoint_reacquisition`, `pomdp_belief_planner`, `goal_retargeting_heuristic`, `failure_aware_manipulation_policy`, `robust_mpc_replan`, `conformal_goal_validity_filter`, `learned_goal_state_classifier`, `active_subgoal_probe_policy`, `risk_budgeted_goal_recovery`, `proposed_disappearing_goal_belief_revision_v4`, `risk_calibrated_goal_belief_revision_v5`, `oracle_goal_state_supervisor`.
- 10 seeds.
- 6 episodes per factorial cell.

Expected main coverage:

- Dataset summaries: 3,840 rows.
- Raw main rollouts: 345,600 rows.
- Main group metrics: 57,600 rows.
- Main seed metrics: 150 rows.
- Main split metrics: 120 rows.
- Hard aggregate seed metrics: 150 rows.
- Hard aggregate metrics: 15 rows.
- Pairwise tests: 14 comparisons.

## Frozen Additional Experiments

- Ablations: full v5 plus removals of observation-memory separation, physical-validity test, active reacquisition, substitute-goal planner, abandonment calibration, delayed-reappearance model, risk calibration, goal-change detector, and intervention-utility model.
- Stress sweep: occlusion, physical removal, goal motion, delay, substitute ambiguity, human obstruction, and task-change pressure across 10 levels.
- Fixed-risk deployment budgets: strict intervention/abandonment budgets with coverage, success, stale-goal pursuit, unsafe reach, false abandonment, recovery, calibration, and utility reported honestly.
- Negative cases: at least 24 generated cases where simpler active perception is enough, substitutes are trivial, the v5 method over-intervenes, or delayed observations make belief revision late.

## Frozen Metrics

Primary metrics:

- Task success.
- Goal-validity F1.
- Retarget precision.
- Stale-goal pursuit.
- Unsafe reach.
- False abandonment.
- Reappearance recovery.
- Substitute-goal success.
- Belief-update latency.
- Intervention cost.
- Calibration ECE.
- Regret to oracle.
- Utility.

Fixed-risk metrics:

- Coverage.
- Conditional success.
- Stale-goal pursuit.
- Unsafe reach.
- False abandonment.
- Recovery success.
- Intervention cost.
- Utility.

## Frozen Gates

Local `STRONG_REVISE` requires all of the following:

- v5 hard-aggregate success beats the strongest non-oracle baseline by at least 0.05.
- v5 goal-validity F1 beats the strongest non-oracle baseline by at least 0.05.
- v5 stale-goal pursuit, unsafe reach, and false abandonment are no worse than the strongest non-oracle success reference.
- v5 intervention cost increase is explicitly reported and must be justified by better success, validity, and safety.
- v5 ECE is below 0.12.
- v5 utility beats the best non-oracle utility baseline.
- Paired seed tests against every non-oracle baseline are positive on success or utility; v5 is expected to lose to the oracle.
- Full v5 beats every removed-component ablation on hard-aggregate success or utility.
- Maximum-stress v5 remains above the strongest non-oracle success reference.
- Strict fixed-risk deployment keeps nontrivial coverage and better utility than the strongest non-oracle fixed-risk reference.

The paper remains `not ICLR-main-ready` unless at least one accepted scope-evidence source exists:

- real robot experiments,
- an accepted high-fidelity simulator benchmark,
- an external benchmark with trained policies,
- calibrated real disappearing-goal logs,
- released trained checkpoints, or
- rollout videos from a real or high-fidelity system.

## Execution Order

1. Replace the v4.1 aggregate runner with the frozen v5 streaming runner.
2. Run the full CPU-only experiment and keep memory bounded by streaming raw rollouts to CSV.
3. Generate all tables, figures, summaries, stress tests, fixed-risk results, and negative cases from CSV/JSON outputs only.
4. Generate a 25+ page manuscript with bright boxed clickable citations and an explicit scope-gate decision.
5. Compile LaTeX, copy only `C:/Users/wangz/Downloads/106.pdf`, and do not place any PDF on the visible Desktop.
6. Validate row counts, finite values, PDF page count, SHA256, boxed citation settings, stale documentation, and GitHub public push.
7. Update root ledgers only after the child repo, canonical PDF, and GitHub checks pass.

## Expected Terminal Honesty

If v5 passes local gates but lacks external validation, the terminal state is `STRONG_REVISE`, `ICLR main ready: no`.

If any local gate fails, the terminal state becomes `KILL_ARCHIVE`, even if the manuscript is 25+ pages.
