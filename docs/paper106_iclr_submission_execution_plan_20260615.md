# Paper 106 ICLR Submission-Readiness Execution Plan

Started: 2026-06-15 16:58:40 +0100

## Objective

Re-audit Paper 106, `disappearing_goal_manipulation`, under the stricter continuation-pass standard. The goal is to decide from regenerated evidence whether the disappearing-goal belief-revision mechanism remains a `STRONG_REVISE` candidate or must be downgraded to `KILL_ARCHIVE`.

## Evidence To Regenerate

- Compile-check `src/run_experiment.py`.
- Run the full benchmark with all tasks, regimes, splits, baselines, seeds, ablations, stress sweeps, and failure cases intact.
- Preserve a root-level rerun log at `logs/106_disappearing_goal_manipulation_continuation_rerun_20260615.log`.
- Verify that all result CSVs are finite and have the expected coverage.
- Identify the strongest non-oracle baseline from regenerated combined-disappearance results.
- Recompute paired seed comparisons, goal-validity diagnostics, stale-goal/safety tradeoffs, ablation margins, and stress-sweep behavior from CSVs.

## Submission Gates

The paper can remain `STRONG_REVISE` only if the proposed method:

- beats the strongest non-oracle baseline on combined-disappearance success by at least `0.030`;
- wins at least `5/7` paired seed comparisons;
- improves goal-validity F1 or stale-goal pursuit by at least `0.050`;
- does not buy success by materially increasing unsafe reach or false abandonment;
- keeps intervention-cost increases explicit and justified by the diagnostic/safety gains;
- survives all named core ablations;
- states plainly that local synthetic evidence is not ICLR-main-ready without real-robot or independent high-fidelity validation.

If those gates fail, the terminal decision must become `KILL_ARCHIVE`.

## Artifacts To Update

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/submission_readiness_audit_v4_1.md`
- `docs/paper106_terminal_audit_20260615.md`
- `paper/main.tex`
- `C:/Users/wangz/Downloads/106.pdf`

## Externalization And Reporting

- Build the PDF with a clean LaTeX/BibTeX log and copy only the numbered PDF to Downloads.
- Do not copy the PDF to Desktop.
- Commit and push the child repository to its public GitHub repo.
- Update root ledgers: `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md`.
