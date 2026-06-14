# 106 Disappearing Goal Manipulation

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready-to-submit.

This rebuild replaces the v3 archive with a paper-specific disappearing-goal manipulation benchmark. The central claim is that a robot policy should distinguish goals that are merely hidden from goals that have moved, been removed, changed, or become replaceable by a substitute goal. The proposed method, `proposed_disappearing_goal_belief_revision`, maintains goal-validity belief state and chooses among waiting, active reacquisition, retargeting, substitute-goal execution, or abandonment.

The local evidence supports the mechanism. On combined disappearance stress, the proposed method reaches `0.662 +/- 0.009` success versus `0.561 +/- 0.003` for the strongest non-oracle baseline, `failure_aware_manipulation_policy`. It also improves goal-validity F1 from `0.439` to `0.586`, reduces stale-goal pursuit from `0.133` to `0.087`, wins 7/7 paired seeds, and survives all removed-component ablations.

The honest limitation is still material: this is a local executable diagnostic benchmark, not real robot or independently validated high-fidelity simulator evidence. The paper should be revised with external robot validation before main-track submission.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

Generated artifacts:

- `results/metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/failure_cases.csv`
- `figures/disappearing_goal_*.png`
- `paper/main.tex`

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/106.pdf`
