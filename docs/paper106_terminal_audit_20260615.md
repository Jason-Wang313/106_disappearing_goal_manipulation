# Paper 106 Terminal Audit

Date: 2026-06-15 16:58:40 +0100

## Terminal Decision

STRONG_REVISE

## Why Not KILL_ARCHIVE

The regenerated full local benchmark clears the predefined mechanism gates. The proposed method beats the strongest non-oracle baseline on combined-disappearance success by `+0.102 +/- 0.008`, wins `7/7` paired seeds, improves goal-validity F1 by `+0.148`, reduces stale-goal pursuit by `-0.046`, reduces unsafe reach by `-0.024`, and reduces false abandonment by `-0.039`. Core ablations remain below the full model.

## Necessary Caveat

The proposed method increases intervention cost by `+0.021` relative to the strongest non-oracle baseline. The claim should therefore be framed as a safety and goal-validity tradeoff, not as a free efficiency improvement.

## Why Not ICLR Main Ready

The evidence is still local and synthetic. The repo does not contain real-robot deployment, independent high-fidelity simulator validation, learned policy checkpoints, training curves, external benchmark comparisons, or rollout videos. The correct action is to preserve the paper as a strong-revise candidate, not to represent it as submission-ready.

## Required Next Evidence

- Real robot or independent high-fidelity simulator evaluation.
- Implemented learned baselines for POMDP planning, active perception, retargeting, and failure-aware manipulation.
- Qualitative rollouts showing hidden, removed, moved, changed, and substitutable goal states.
- External benchmark split such as LIBERO, RLBench, Meta-World, BridgeData, CALVIN, or a comparable hardware manipulation suite.
- A revised related-work section tied to those external results.
