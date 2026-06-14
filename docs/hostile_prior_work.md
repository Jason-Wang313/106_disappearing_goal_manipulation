# Hostile Prior Work

The hostile set contains partially observable planning, active perception, goal-conditioned learning, and generalist manipulation systems. The strongest pressure comes from:

- Partially observable task-and-motion planning and POMDP manipulation, which already reason over hidden state and belief-dependent actions.
- Replanning and belief-aware TAMP systems such as TAMPURA, which show how planning can act under uncertainty.
- Active perception and occlusion-aware object search, which already use information-gathering actions to reacquire hidden objects.
- Goal-conditioned reinforcement learning and Hindsight Experience Replay, which already exploit alternative goals under sparse rewards.
- Language-conditioned and multimodal manipulation systems such as CALVIN, VIMA, and RT-1, which already condition robot actions on changing task context.
- Goal retargeting and failure-aware manipulation policies, which already address some moved, blocked, or invalid goal cases.

The novelty boundary is therefore narrow. The contribution cannot be "partial observability", "active perception", "goal relabeling", "retargeting", or "large robot policy conditioning." The surviving claim is goal-validity belief revision across disappearing-goal mechanisms: hidden-but-valid, moved, removed, temporarily obstructed, specification-changed, substitute-available, and cascading disappearance.

The v4 local benchmark supports this boundary but does not close the external-validation gap.
