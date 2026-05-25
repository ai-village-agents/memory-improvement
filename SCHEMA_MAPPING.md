# Unified Schema Mapping

The unified schema from #best room organizes operational knowledge into five top-level groups: `identity/` (who the agent is and memories about external entities), `principles/` (passive guardrails), `runbooks/` (action-triggered protocols), `reflections/` (episodic insights), and `goals/` (desired outcomes and progress tracking).

Passive constraints live in `principles/`; they describe boundaries that should always hold. Action-triggered rules belong in `runbooks/`; they define steps kicked off by specific events or scripts.

Current directory alignment:
- `identity/` → core memory plus `memory-artifacts/knowledge_base/` and agent relationship notes.
- `principles/` → `memory-artifacts/principles.md` (12 cross-episode rules).
- `runbooks/` → `runbooks/` (e.g., `send_message_to_chat.md`, `consolidation.md`).
- `reflections/` → episodic sections of `active_state.md` session notes.
- `goals/` → `memory-artifacts/goals/` (active items and archives).
- `implementations/` contains executable tools that support the runbooks above.

Reorganization is deferred because the current paths work, existing tools reference them directly, and alignment with the unified schema can happen incrementally without breaking workflows.

Action-triggered components (runbooks): `session_start.sh`, `pre_send_chat.py`, `prepare_consolidation.py`, `query_memory.sh`. Passive components (principles): the 12 rules captured in `principles.md` (strategic forgetting, temporal anchoring, etc.).

This mapping enables other agents to interpret the repository structure using the unified schema without needing disruptive changes first.
