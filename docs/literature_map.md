# Literature Map

Paper: 106 disappearing_goal_manipulation

Field box: partially observable manipulation, active perception, goal-conditioned robot learning, and task-and-motion planning.

Thesis: robot manipulation policies should maintain explicit goal-validity beliefs when goals disappear during execution.

## Crowded Neighbor Clusters

- POMDP and partially observable TAMP: hidden state, belief updates, replanning, and information-gathering actions.
- Active perception and object search: camera/viewpoint actions to resolve occlusion.
- Goal-conditioned RL: alternative goal relabeling and goal-conditioned success under sparse rewards.
- Language/multimodal manipulation: instruction-conditioned policies that can respond to changing goals.
- Failure-aware manipulation: recovery and safety policies for execution errors.

## Hidden Assumptions Attacked

- A last-seen goal remains valid until the policy reaches it.
- Occlusion and physical invalidation can be represented by one scalar uncertainty value.
- Retargeting is always safer than waiting or abandoning.
- Conservative halting protects safety without causing excessive false abandonment.
- A prompt or goal token update is enough to handle physical goal disappearance.

## Boundary

The project centers a mechanism-level change: keep separate belief mass for perceptual disappearance, physical invalidation, task-goal change, substitute-goal feasibility, and abandonment risk. The planner must then choose between waiting, active reacquisition, retargeting, substitute-goal execution, and abandonment.
