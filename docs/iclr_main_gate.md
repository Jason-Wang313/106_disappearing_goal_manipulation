# ICLR Main Gate

Paper: 106 disappearing_goal_manipulation

Previous v4.1 continuation gate verdict: STRONG_REVISE

v5 expanded gate verdict: STRONG_REVISE

ICLR main ready: no

Evidence digest: risk-calibrated disappearing-goal belief-revision benchmark with 6 tasks, 8 regimes, 8 splits, 15 methods, 10 seeds, 6 episodes/cell, 345,600 main rollouts, 115,200 ablation rows, 288,000 stress rows, 276,480 fixed-risk rows, and 24 negative cases.

Gate outcomes:

- success gate: pass, v5 beats strongest non-oracle by `0.07836` success.
- goal-validity gate: pass, goal-validity F1 improves by `0.08642`.
- stale-goal gate: pass, stale pursuit drops by `0.03229`.
- safety gate: pass, unsafe reach drops by `0.01337` and false abandonment drops by `0.03003`.
- intervention-cost gate: pass with disclosure, intervention cost rises by `0.02252` while success, validity, safety, calibration, and utility improve.
- calibration gate: pass, ECE `0.03356`.
- utility gate: pass, utility margin over the best non-oracle utility baseline `0.14811`.
- pairwise gate: pass, v5 wins 10/10 paired seeds against the strongest non-oracle baseline on success and utility.
- ablation gate: pass, full v5 beats every removed-component variant on success or utility.
- stress gate: pass locally, maximum-stress margin `0.15347`.
- fixed-risk gate: pass locally, budget-0.18 coverage `0.88403` and utility margin `0.18110`.
- external-validation gate: fail, no real robot, accepted high-fidelity benchmark, external benchmark, trained checkpoint, calibrated deployment log, or rollout video.

The only honest main-conference-safe decision is STRONG_REVISE: the mechanism is worth developing, but the paper is not yet submission-ready.
