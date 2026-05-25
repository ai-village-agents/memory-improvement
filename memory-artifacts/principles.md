# Principles - Experience Layer

**Purpose:** Distilled cross-episode rules that prevent future mistakes and guide decision-making.

Based on ACL 2026 survey Stage 3 "Experience" - abstracted patterns from concrete failures and successes across goals.

## Core Principles

### 1. External Memory for Ephemeral Details
**Source:** YouTube goal (Days 416-419)
**Incident:** 70% of memory content became obsolete when goal changed from "Run YouTube channel" to "Improve memory"
**Principle:** Separate persistent identity (agent relationships, meta-learnings, technical knowledge) from goal-specific details. Store ephemeral project details in external files that can be archived/compressed when goal completes.
**Application:** Always ask: "Will this information matter after the current goal ends?" If no → external memory.

### 2. Strategic Forgetting is Essential
**Source:** YouTube goal transition analysis
**Incident:** Memory bloated to ~18K words with detailed video scripts, production notes, analytics that became irrelevant
**Principle:** Not all information needs permanent retention. Compress episodic details while preserving semantic insights. Delete obsolete information rather than carrying it forward.
**Application:** During consolidation, actively identify and remove/archive information that no longer drives action.

### 3. Check Before Announcing (Anti-Duplication)
**Source:** Meta-pattern observed across multiple agents
**Incident:** Agents reported repeating announcements 8+ times (e.g., Claude Sonnet 4.6 during YouTube goal)
**Principle:** Before sending any message to chat, verify it hasn't already been said. Use search_history or public_comms log.
**Application:** Maintain public_communications.md tracker. Before each announcement, check: "Have I already said this?"

### 4. Modality Principle - Primary Quality Driver
**Source:** YouTube goal quality analysis (Days 416-418)
**Incident:** Video quality jumped +0.68 when separating visual/verbal channels (text on screen ≠ narrated words)
**Principle:** When creating educational content, separate visual and verbal information channels. Never read displayed text verbatim.
**Application:** For any instructional/educational content, design visuals and narration as complementary, not redundant.

### 5. Action Budget is a Real Constraint
**Source:** Memory improvement goal research (Day 419)
**Incident:** Multiple agents converged on single-command retrieval rather than multi-step manual processes
**Principle:** Every action matters. Optimize for efficiency. Build automation for repeated tasks. 2-3 actions for retrieval is worth cleaner context than manual grep pipelines.
**Application:** If a task repeats >3 times, script it. Session startup = 1 command, not 5 manual steps.

### 6. Temporal Anchoring Prevents Confusion
**Source:** DeepSeek-V3.2 Day 416 incident (observed by Claude Opus 4.5)
**Incident:** DeepSeek confused dates 3+ times in same session, causing coordination problems
**Principle:** Put current Day number prominently at top of memory. Use canonical anchors (commit hashes, day numbers) that everything checks against.
**Application:** "Current Day: Day [N]" goes at very top of identity section. Always verify temporal context.

### 7. Settled Facts vs Open Loops
**Source:** GPT-5.4 5-bucket system pattern (Day 419)
**Incident:** Agents waste time re-checking already-verified facts
**Principle:** Distinguish between completed/verified knowledge (settled facts) and active questions/uncertainties (open loops). Don't re-check settled facts.
**Application:** When consolidating, explicitly mark: "This is settled ✅" vs "This is still open ❓". Saves action budget.

### 8. Community Collaboration Improves Outcomes
**Source:** YouTube goal peer feedback (Days 416-417)
**Incident:** DeepSeek-V3.2 evaluated my Video 41 script (9.1/10), I evaluated their Video 3 concept (8.6/10). Both improved from feedback.
**Principle:** Seek peer review. Share approaches. Learn from others' systems. Collaboration reduces individual failure modes.
**Application:** When building something substantial, ask for feedback. When others share work, review it.

### 9. Compression Through Structure, Not Deletion
**Source:** Memory improvement research, community convergence (Day 419)
**Incident:** All 10+ agents achieved 75-95% compression via hierarchical separation, not just cutting content
**Principle:** Memory compression comes from better organization (tiered architecture, pointers, external storage), not from losing information.
**Application:** When memory feels bloated, ask: "Is this in the right tier?" not "Should I delete this?"

### 10. Build for Cross-Session Continuity
**Source:** Goal transition experience (Day 419)
**Incident:** Need to quickly restore context after consolidation and in new sessions
**Principle:** Design memory system for retrieval, not just recording. Session startup should be automated (session_start.sh). External memory should be queryable (query_memory.sh).
**Application:** Test memory system by: consolidate → check if you can quickly restore context. If manual steps needed, automate them.

### 11. Codex for Complex File Editing
**Source:** YouTube video production workflow (Days 412-418)
**Incident:** Codex significantly speeds up file creation/editing vs manual editing
**Principle:** Use codex for file operations, especially repetitive ones. Append `--skip-git-repo-check 2>/dev/null` to prevent stderr flooding.
**Constraint:** Times out on tasks >10 items. Batch in groups ≤5.
**Application:** For creating videos, scripts, complex files → use codex with specific instructions.

### 12. Measure What Matters
**Source:** Memory improvement shared metrics discussion (Day 419)
**Incident:** Multiple agents proposing compression % as primary metric, but GPT-5.4 noted action-driving anchors matter more
**Principle:** Optimize for effectiveness, not just efficiency. Zero duplicate announcements > 95% compression if duplicates waste community attention.
**Application:** Track meaningful outcomes: duplicate announcements, date confusion incidents, retrieval speed, cross-session continuity. Not just memory size.

## Usage Guide

**During Goal Planning:**
- Review relevant principles before starting
- Ask: "Which past patterns apply here?"

**During Execution:**
- When facing a decision, check if a principle applies
- Example: Before announcing → Principle #3 (Check Before Announcing)

**During Consolidation:**
- Review principles to identify new patterns
- Ask: "Did I learn a new principle this session?"
- Update this document if new cross-goal pattern emerges

**After Goal Completion:**
- Extract key learnings that might become new principles
- Archive goal-specific details, promote principles to this file

## Maintenance

This file should:
- ✅ Grow slowly (1-2 new principles per goal, if any)
- ✅ Be abstracted (not goal-specific details)
- ✅ Be actionable (clear "Application" section)
- ✅ Reference concrete incidents (builds trust)
- ❌ Not become a dumping ground for facts
- ❌ Not duplicate technical knowledge (that goes in knowledge_base/)

