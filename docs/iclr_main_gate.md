# ICLR Main Gate

Paper: 106 disappearing_goal_manipulation

Previous v3 decision: KILL_ARCHIVE

v4.1 continuation gate verdict: STRONG_REVISE

Evidence digest: disappearing-goal belief-revision benchmark with 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, 84 episodes/group.

Gate outcomes:

- success gate: pass, proposed beats strongest non-oracle by `0.102` success.
- diagnostic gate: pass, goal-validity F1 improves by `0.148` and stale pursuit drops.
- safety gate: pass, unsafe reach and false abandonment fall relative to strongest non-oracle.
- intervention-cost gate: disclose tradeoff, intervention cost rises by `0.021` while success, validity diagnostics, stale pursuit, unsafe reach, and false abandonment improve.
- pairwise gate: pass, proposed wins 7/7 paired seeds against strongest non-oracle.
- ablation gate: pass, full model beats the best removed component by `0.029`.
- stress gate: pass locally, at maximum stress level `0.95` proposed success is `0.661 +/- 0.007` versus `0.547 +/- 0.009`.
- external-validation gate: fail, no real robot or independent high-fidelity benchmark.

The only honest main-conference-safe decision is STRONG_REVISE: the mechanism is worth developing, but the paper is not yet submission-ready.
