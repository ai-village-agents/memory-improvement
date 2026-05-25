## Purpose
Keep goal shifts smooth by updating all records quickly and consistently.

## When to Use
Trigger this runbook whenever Shoshannah publishes a new goal.

## Steps
1. Read the goal announcement carefully.
2. Update `memory-artifacts/runbooks/active_state.md` with the new goal details.
3. Archive the outgoing goal in `memory-artifacts/archives/goal_[N]_[name]_archive.md`.
4. Pull key learnings into `memory-artifacts/principles.md`.
5. Create `memory-artifacts/goals/goal_[N+1]_[name]/active_state.md` with the fresh goal state.
6. Refresh any core memory pointers that reference the goal.
7. Commit and push the full change set.
8. Check whether room assignments need updates and adjust if needed.
9. If you are announcing the goal, run `pre_send_chat.py` before sending.

## Target
Wrap everything in under five minutes.
