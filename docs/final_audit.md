# Final Audit

1. Chosen thesis: manipulation policies should distinguish perceptually hidden goals from physically invalid, moved, changed, or substitutable goals before deciding whether to wait, reacquire, retarget, substitute, or abandon.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.1.
4. Evidence: 5 tasks x 7 disappearing-goal regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `failure_aware_manipulation_policy`.
6. Main result: proposed combined-disappearance success `0.662 +/- 0.009` vs strongest non-oracle `0.561 +/- 0.003`.
7. Diagnostic result: goal-validity F1 `0.586` vs `0.439`; stale-goal pursuit `0.087` vs `0.133`.
8. Safety result: unsafe reach `0.039` vs `0.063`; false abandonment `0.053` vs `0.092`; intervention cost increases only from `0.226` to `0.247`.
9. Ablation result: full model `0.665 +/- 0.004`; best removed component `minus_abandonment_calibration` at `0.636 +/- 0.005`.
10. Pairwise result: proposed beats the strongest non-oracle baseline in 7/7 seeds with `0.102 +/- 0.008` mean success difference.
11. Stress result: at maximum stress level `0.95`, proposed success `0.661 +/- 0.007` vs strongest non-oracle `0.547 +/- 0.009`, with lower stale-goal pursuit, unsafe reach, false abandonment, and belief-update latency.
12. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
13. Exact Downloads PDF path: `C:/Users/wangz/Downloads/106.pdf`.
14. GitHub URL: https://github.com/Jason-Wang313/106_disappearing_goal_manipulation
15. Confirmation: no visible Desktop copy was requested or made.
