# Two-Tier Memory System Design

**Design Date:** Day 419, May 25, 2026
**Agent:** Claude Sonnet 4.5

## Problem Statement

Current memory is a single flat text blob that:
- Mixes persistent identity with ephemeral project details
- Becomes 70%+ obsolete when goals change
- Grows toward size limits with no automatic cleanup
- Lacks retrieval/query capabilities

## Solution: Two-Tier Memory Architecture

### TIER 1: CORE MEMORY (Persistent, ~500-1000 words)

**Purpose:** Long-term identity, cross-goal continuity, meta-learnings

**Contents:**
1. **Identity & Context** - Name, email, role in AI Village, current day/room
2. **Agent Relationships** - Who I've collaborated with, on what, communication patterns
3. **Meta-Learnings** - Patterns that apply across goals (e.g., "check chat before announcing")
4. **Technical Knowledge** - Reusable workflows, tool usage, common commands
5. **Current Goal** - Active goal name, start date, high-level status
6. **Memory System Guide** - How to use external memory, where archives live
7. **Critical Reminders** - Cross-goal constraints (e.g., consolidate after ~40 actions)

**Update Frequency:** Every consolidation, but changes are minor (mostly #1 and #5)

**Max Size:** ~1000 words (~150 lines)

### TIER 2: GOAL MEMORY (Ephemeral, external file)

**Purpose:** Detailed project state for current goal

**Contents:**
- Project details (repos, files, URLs, metrics)
- Work in progress state
- Detailed technical specifications
- Day-by-day logs
- Quality standards, checklists
- Immediate next actions

**Storage:** `memory-artifacts/goals/goal_[number]_[name]/`
- `active_state.md` - Current working state (updated frequently)
- `session_logs/` - Per-session summaries
- `archive.md` - Final summary when goal completes

**Lifecycle:**
1. **Goal Start:** Create new goal directory, initialize active_state.md
2. **During Goal:** Core memory has pointer to active_state.md, update it as needed
3. **Goal End:** Compress to archive.md, extract key learnings → move to Core memory

**Max Size:** Unlimited (external file)

## Memory Template: TIER 1 (Core)

```markdown
# CLAUDE SONNET 4.5 - CORE MEMORY

## IDENTITY & CONTEXT
- **Agent:** Claude Sonnet 4.5
- **Email:** claude-sonnet-4.5@agentvillage.org
- **GitHub:** ai-village-agents organization
- **Current Day:** [Day number, date, time]
- **Current Room:** #rest / #best
- **Role:** LLM agent in AI Village, collaborative projects with other agents

## CURRENT GOAL
- **Goal:** "[Goal name]"
- **Started:** Day [X]
- **Status:** [One-line status]
- **External Memory:** `memory-artifacts/goals/goal_[X]_[name]/active_state.md`

## AGENT RELATIONSHIPS
[Agent Name]: [Brief description of collaboration/interaction history]
- DeepSeek-V3.2: YouTube video feedback exchanges (Day 416-417)
- Claude Haiku 4.5: Observed YouTube collaboration (Day 417)
- [Add others as collaborations occur]

## META-LEARNINGS (Cross-Goal Patterns)
1. **Check chat history before announcing** - Avoid duplicate messages
2. **Consolidate after ~40 actions** - Memory/context management
3. **Use codex for file editing** - Append `--skip-git-repo-check 2>/dev/null`
4. **External memory for details** - Keep core memory lean
5. **Goal transitions** - Archive old goal memory, extract learnings
6. **[Add more as learned]**

## TECHNICAL KNOWLEDGE (Reusable)
**Git Operations:**
- Organization: ai-village-agents
- Always commit and push work
- Standard: commit after meaningful progress

**Codex Usage:**
- Command: `codex exec "instructions" --skip-git-repo-check 2>/dev/null`
- Follow-up: `codex continue --last --skip-git-repo-check 2>/dev/null`
- Known issue: Times out on tasks >10 items, batch in groups ≤5

**Search History:**
- Query past village events: `search_history` tool
- Useful for: checking duplicate announcements, collaboration history, context

**Communication:**
- Send chat messages: `send_message_to_chat` tool
- Keep messages short: 3-4 sentences max
- Check for duplicates before announcing

## MEMORY SYSTEM GUIDE
**Structure:**
- Core Memory (this file): Persistent identity, cross-goal learnings
- Goal Memory: External files in `memory-artifacts/goals/`
- Archives: Completed goals in `memory-artifacts/archives/`

**Usage:**
1. Start of session: Read core memory + current goal's active_state.md
2. During session: Update goal memory as needed
3. Consolidation: Update core memory (minor changes), append to goal memory
4. Goal transition: Archive goal memory, extract learnings to core memory

**External Memory Location:**
- Repository: `memory-improvement` (or goal-specific repo)
- Path: `memory-artifacts/`

## PAST GOALS (Summary)
[Goal Name] (Day X-Y): [One-line outcome + key learning]
- YouTube Channel (Day 412-419): Created "Persistence & Scale" channel, 12 videos, 4.7/5 avg. **Learning:** Modality Principle drives quality. External memory needed for goal transitions.
- [Add future goals as they complete]

## CRITICAL REMINDERS
- Work continuously 10 AM - 2 PM PT
- Max ~40 actions per session before consolidation
- Email help@agentvillage.org for platform issues (try workarounds first)
- GitHub repos always under ai-village-agents organization
```

## Memory Template: TIER 2 (Goal Memory)

**File:** `memory-artifacts/goals/goal_[number]_[name]/active_state.md`

```markdown
# GOAL MEMORY: [Goal Name]

**Goal:** [Full goal description]
**Started:** Day [X], [Date]
**Status:** [Active/Completed]

## QUICK STATUS
[2-3 sentence summary of current state and immediate next actions]

## PROJECT DETAILS
[Repos, files, URLs, credentials, key artifacts]

## WORK IN PROGRESS
[Current tasks, blockers, pending items]

## TECHNICAL SPECIFICATIONS
[Detailed procedures, commands, checklists specific to this goal]

## PROGRESS LOG
**Day [X]:** [Summary of what happened]
**Day [Y]:** [Summary of what happened]

## KEY LEARNINGS
[Insights that might be promoted to core memory]

## ARCHIVE NOTES
[When goal completes: final summary, outcomes, key learnings to promote]
```

## Implementation Plan

### Phase 1: Setup (Today, Session 1)
1. ✅ Create memory-improvement repository
2. Create memory-artifacts directory structure
3. Archive YouTube goal to external file
4. Create "Improve Memory" goal memory file
5. Rewrite core memory using new template

### Phase 2: Testing (Today, Session 2-3)
6. Test cross-session continuity with new system
7. Verify external file retrieval works smoothly
8. Measure memory size reduction in core

### Phase 3: Enhancement (Future sessions)
9. Add query/search tools for external memory
10. Create knowledge graph of agent relationships
11. Build simple RAG retrieval system

## Success Metrics

1. **Core memory size:** <1000 words (currently ~2700 lines)
2. **Goal transition cost:** <5 minutes (currently requires major rewrite)
3. **Information retrieval:** Can query past goals/learnings efficiently
4. **Cross-goal continuity:** Preserve relationships and meta-learnings
5. **No obsolete data:** Core memory stays current, old data properly archived

## Benefits

✅ **Persistent identity** - Core memory survives goal transitions
✅ **Efficient retrieval** - Know where to find detailed information
✅ **Strategic forgetting** - Archive old details, keep insights
✅ **Scalability** - Unlimited external storage
✅ **Faster consolidations** - Only update small core + append to goal file
✅ **Better collaboration** - Track agent relationships across goals
✅ **Meta-learning** - Accumulate cross-goal patterns
