# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added multi-seed synthetic diagnostics.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Rebuild

- Replaced the shared template script with a disappearing-goal manipulation benchmark.
- Added 5 tasks, 7 disappearance regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group.
- Added goal-validity F1, retarget precision, stale-goal pursuit, unsafe reach, false abandonment, reappearance recovery, substitute-goal success, latency, intervention cost, regret, paired tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Rewrote docs and manuscript around the actual evidence.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Submission Audit

- Added `docs/paper106_iclr_submission_execution_plan_20260615.md`.
- Reran `src/run_experiment.py` from source with the full benchmark and logged the run at `logs/106_disappearing_goal_manipulation_continuation_rerun_20260615.log`.
- Verified expected CSV coverage and finite numeric outputs.
- Reconfirmed the strongest non-oracle baseline as `failure_aware_manipulation_policy`.
- Disclosed the intervention-cost tradeoff while preserving the stronger success/diagnostic/safety result.
- Added terminal audit docs and rebuilt the numbered Downloads PDF.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
