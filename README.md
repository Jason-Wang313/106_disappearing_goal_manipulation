# 106 Disappearing Goal Manipulation

Submission-hardening version: v5-expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready-to-submit.

This rebuild expands the v4.1 disappearing-goal manipulation audit into a 25-page hostile-review v5 package. The central claim is narrow: robot manipulation policies should separate perceptually hidden goals from physically invalid, moved, semantically changed, temporarily obstructed, delayed-reappearing, or substitutable goals before choosing whether to continue, wait, actively reacquire, retarget, substitute, recover, or abandon.

The v5 benchmark uses 6 task families, 8 disappearing-goal regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per factorial cell. It writes 345,600 main rollout rows, 3,840 dataset-summary rows, 57,600 main group rows, 150 main seed rows, 120 method/split metric rows, 150 hard-aggregate seed rows, 15 hard-aggregate metric rows, 14 hard pairwise comparisons, 115,200 ablation rows, 288,000 stress rows, 276,480 fixed-risk rows, and 24 negative cases.

The strongest non-oracle baseline is `proposed_disappearing_goal_belief_revision_v4`. The v5 method `risk_calibrated_goal_belief_revision_v5` reaches hard-aggregate success `0.77454` versus `0.69618` for v4, goal-validity F1 `0.72880` versus `0.64239`, stale-goal pursuit `0.01238` versus `0.04468`, unsafe reach `0.00087` versus `0.01424`, false abandonment `0.00851` versus `0.03854`, ECE `0.03356`, and utility `0.70495` versus `0.55683`. It passes the frozen success, diagnostic, safety, calibration, utility, pairwise, ablation, stress, and fixed-risk local gates.

The honest limitation is still material: this is CPU-only local diagnostic evidence, not real robot or independently validated high-fidelity simulator evidence. The scope gate fails because there is no real robot study, accepted high-fidelity benchmark, external disappearing-goal benchmark, trained checkpoint, calibrated deployment log, or rollout video.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/106.pdf`

Final PDF SHA256: `E458C4C2F2B45D154801EE0D6F614E7097A4262B0AE56BB4360C9040BE825437`
