# Experiment Rigor Checklist

## v5 Local Evidence

- [x] Plan-first hostile-review protocol frozen before code execution.
- [x] 6 task families.
- [x] 8 disappearing-goal regimes.
- [x] 8 splits including combined extreme.
- [x] 15 methods including v4, strong non-oracle baselines, and oracle ceiling.
- [x] 10 seeds.
- [x] 345,600 raw main rollout rows.
- [x] Paired seed comparisons against every comparator.
- [x] Goal-validity, stale-goal, unsafe-reach, false-abandonment, ECE, regret, and utility metrics.
- [x] 10 ablations.
- [x] 10-level stress sweep.
- [x] 4 fixed-risk deployment budgets.
- [x] 24 negative and boundary cases.
- [x] Generated figures and LaTeX tables.
- [x] 25-page PDF with bright boxed clickable citations.
- [x] Downloads-only numbered PDF validation.

## ICLR Main Bar Still Missing

- [ ] Real-robot validation.
- [ ] Accepted high-fidelity simulator benchmark.
- [ ] External disappearing-goal benchmark.
- [ ] Trained learned policy/model checkpoint.
- [ ] External implemented competing baselines.
- [ ] Qualitative robot rollouts or videos.

Decision: pass local mechanism-evidence gate; fail final main-track deployment-evidence gate; mark STRONG_REVISE.
