# Final Audit

1. Chosen thesis: manipulation policies should distinguish perceptually hidden goals from physically invalid, moved, changed, delayed, obstructed, or substitutable goals before deciding whether to wait, reacquire, retarget, substitute, recover, or abandon.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v5-expanded.
4. Evidence: 6 tasks x 8 disappearing-goal regimes x 8 splits x 15 methods, 10 seeds, 6 episodes/cell.
5. Strongest non-oracle baseline: `proposed_disappearing_goal_belief_revision_v4`.
6. Main result: v5 hard-aggregate success `0.77454` vs strongest non-oracle `0.69618`.
7. Diagnostic result: goal-validity F1 `0.72880` vs `0.64239`; stale-goal pursuit `0.01238` vs `0.04468`.
8. Safety result: unsafe reach `0.00087` vs `0.01424`; false abandonment `0.00851` vs `0.03854`; intervention cost rises from `0.24998` to `0.27249`.
9. Calibration and utility: ECE `0.03356`; utility `0.70495` vs `0.55683`.
10. Ablation result: full v5 beats every removed-component variant on success or utility; closest success ablation is `minus_intervention_utility_model`.
11. Pairwise result: v5 beats the strongest non-oracle baseline in 10/10 paired seeds on success and utility.
12. Stress result: at maximum stress level `1.00`, v5 success `0.75208` vs `0.59861` for the strongest non-oracle stress reference.
13. Fixed-risk result: at budget `0.18`, v5 coverage `0.88403` and utility margin `0.18110` over the strongest fixed-risk non-oracle reference.
14. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
15. Exact Downloads PDF path: `C:/Users/wangz/Downloads/106.pdf`.
16. PDF SHA256: `E458C4C2F2B45D154801EE0D6F614E7097A4262B0AE56BB4360C9040BE825437`.
17. GitHub URL: https://github.com/Jason-Wang313/106_disappearing_goal_manipulation
18. Confirmation: no visible Desktop copy was requested or made.
