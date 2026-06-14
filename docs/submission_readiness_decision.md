# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild provides a paper-specific local benchmark for disappearing-goal manipulation, with strong synthetic baselines, ablations, paired seed comparisons, stress sweeps, failure cases, finite CSV artifacts, and generated figures/tables. The evidence supports the mechanism: on combined disappearance stress, `proposed_disappearing_goal_belief_revision` reaches `0.662 +/- 0.009` success versus `0.561 +/- 0.003` for the strongest non-oracle baseline, `failure_aware_manipulation_policy`.

Diagnostic evidence also supports the mechanism. Goal-validity F1 improves from `0.439` to `0.586`; stale-goal pursuit falls from `0.133` to `0.087`; unsafe reach falls from `0.063` to `0.039`; false abandonment falls from `0.092` to `0.053`; and paired seed comparisons favor the proposed method over the strongest baseline in 7/7 seeds.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, and external benchmark evidence.
