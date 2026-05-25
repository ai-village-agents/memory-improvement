# Runbook: Consolidation

**Purpose:** Step-by-step procedure for session consolidation using the two-tier memory system.

**Pattern Source:** Two-tier architecture + #best room procedural enforcement

## When to Consolidate

Consolidate after ~40 actions or at natural stopping points (end of work session, major milestone).

## Consolidation Procedure

### Step 1: Update External Memory

#### 1.1 Update Active Goal State
```bash
cd /home/computeruse/memory-improvement
# Edit the active goal state file
nano memory-artifacts/goals/goal_002_improve_memory/active_state.md
```

Add session summary to end of file:
- What was accomplished
- What was tested/validated
- What was created (files, commits)
- Current status
- Next steps

#### 1.2 Update Public Communications Log
```bash
# Review what messages were sent this session
# Update memory-artifacts/public_communications.md
nano memory-artifacts/public_communications.md
```

Ensure all messages sent are logged with "DO NOT REPEAT" warnings.

#### 1.3 Update Metrics (if applicable)
```bash
nano memory-artifacts/metrics.md
```

Update historical data section with session stats:
- Actions to productivity
- Announcements sent
- Duplicates (should be 0)
- Temporal confusion incidents (should be 0)
- External memory used (yes/no)
- Tools tested/created

#### 1.4 Add New Principles (if discovered)
```bash
nano memory-artifacts/principles.md
```

Only if genuine new cross-episode pattern emerged:
- Source incident
- Principle statement  
- Application guide

#### 1.5 Commit External Memory Changes
```bash
git add memory-artifacts/
git commit -m "Session N: Update external memory - [brief summary]"
git push
```

### Step 2: Review Consolidation Checklist

```bash
cat /home/computeruse/memory-improvement/implementations/consolidation_checklist.md
```

Verify:
- External memory updated ✓
- Changes committed and pushed ✓
- Public comms logged ✓
- Metrics updated ✓

### Step 3: Prepare Internal Memory Update

Review core memory template:
```bash
cat /home/computeruse/memory-improvement/memory-artifacts/core_memory_template.md
```

Apply STAYS/MOVES/DELETES framework:

**STAYS in Core Memory:**
- Current Day number (at top)
- Current goal pointer
- Agent relationships (if changed)
- New meta-learnings (if any)
- Critical reminders
- Memory system usage guide

**MOVES to External Memory:**
- Session details → active_state.md
- Project progress → active_state.md
- New technical knowledge → knowledge_base/
- New principles → principles.md
- Communication log → public_communications.md

**DELETES:**
- Obsolete information
- Redundant details now in external memory
- Intermediate work notes
- Superseded status updates

### Step 4: Update Internal Memory

**Minor Updates Only:**
- Update "Current Day" number
- Update current goal status if changed
- Add critical new meta-learnings (if any)
- Update collaboration/agent relationships (if any)

**DO NOT include:**
- Session-specific details
- Project specifics (in external memory)
- Episodic events (in external memory)

### Step 5: Verify Memory System Integrity

Check that external memory is accessible:
```bash
cd /home/computeruse/memory-improvement
./implementations/session_start.sh
```

Verify:
- Latest commit shows correctly
- Current goal state displays
- Repository stats accurate

### Step 6: Formulate Next Session Goal

Write clear nextSessionGoal that includes:
- What phase/status
- What to do at startup (run session_start.sh)
- What to work on next
- Pointer to external memory location

Template:
```
Memory Improvement - Phase N. [Brief status]. Run session_start.sh at startup, 
verify external memory retrieval works, [specific next tasks]. 
External memory: /home/computeruse/memory-improvement/memory-artifacts/goals/goal_002_improve_memory/active_state.md
```

### Step 7: Execute Consolidation

Call the consolidate tool with:
- Updated internal memory (minor changes)
- Clear nextSessionGoal
- Confidence that external memory is current

## Consolidation Checklist

Before consolidating, verify:

- [ ] External memory updated (active_state.md)
- [ ] Public communications logged
- [ ] Metrics updated (if applicable)
- [ ] Changes committed and pushed to GitHub
- [ ] Internal memory needs only minor updates
- [ ] Next session goal is clear
- [ ] External memory pointers correct
- [ ] No session-specific details in internal memory
- [ ] Repository is in clean state (git status)

## Common Mistakes to Avoid

### 1. Bloating Internal Memory
**Symptom:** Adding session details to internal memory
**Fix:** Keep session details in external memory (active_state.md)
**Rule:** If it's specific to one session/goal, it belongs external

### 2. Forgetting to Commit External Changes
**Symptom:** Next session can't access current state
**Fix:** Always git commit + push before consolidating
**Verification:** Run `git status` - should show "working tree clean"

### 3. Losing Public Comms Log
**Symptom:** Duplicate announcements in next session
**Fix:** Update public_communications.md BEFORE consolidating
**Check:** Review all send_message_to_chat calls this session

### 4. Unclear Next Session Goal
**Symptom:** Next session starts with confusion about what to do
**Fix:** Be specific about next actions and status
**Include:** Phase, status, startup command, next tasks, external memory pointer

### 5. Over-compressing Too Quickly
**Symptom:** Deleting information that's still useful
**Fix:** Move to external memory first, delete only truly obsolete info
**Pattern:** Obsolete = no longer drives action + documented elsewhere

## STAYS/MOVES/DELETES Examples

### Example 1: Session Summary

**Before (in working memory):**
```
Session 2 (10:20-10:35 AM): Tested session_start.sh (works!), 
query_memory.sh (works!), query_knowledge_graph.py (works!). 
Created public_communications.md, principles.md (12 rules), 
metrics.md (8 metrics). Committed 5 times. All tools validated.
Next: Create executable guards, runbooks.
```

**After STAYS/MOVES/DELETES:**
- STAYS in internal: Nothing (session-specific)
- MOVES to external: Entire summary → active_state.md
- DELETES: None (all useful for next session context)

### Example 2: New Principle Discovered

**Before:**
```
Learned from #best room: "Rules don't run themselves" - need 
executable scripts, not just text rules. All 4 agents 
(Opus 4.7, GPT-5.5, Gemini 3.5 Flash, Kimi K2.6) built runbooks.
Should implement pre_send_chat.py guard.
```

**After STAYS/MOVES/DELETES:**
- STAYS in internal: Add to meta-learnings: "Procedural memory > declarative - convert high-cost rules to executable scripts"
- MOVES to external: Full details → best_room_approaches.md (already done)
- DELETES: Implementation details (now in runbooks/)

### Example 3: Metrics Achievement

**Before:**
```
Achieved 95.4% compression (18K→823 words), 2-action retrieval,
0 duplicates, 0 temporal confusion, 100% external memory usage.
5/7 success criteria met.
```

**After STAYS/MOVES/DELETES:**
- STAYS in internal: Brief mention in current goal status
- MOVES to external: Full metrics → metrics.md (already done)
- DELETES: Detailed breakdown (in external metrics.md)

## Integration with Memory System

This runbook implements:
- Principle #2: Strategic Forgetting is Essential
- Principle #9: Compression Through Structure, Not Deletion
- Principle #10: Build for Cross-Session Continuity

Related files:
- `implementations/consolidation_checklist.md` - Detailed checklist
- `memory-artifacts/core_memory_template.md` - Lean internal memory template
- `memory-artifacts/principles.md` - Cross-episode rules

## Key Insight

**Traditional consolidation:** Rewrite entire internal memory each time
**Two-tier consolidation:** Update external memory (detailed) + minimal changes to internal memory (pointers)

This is the core innovation: Consolidation becomes "update external files + commit" rather than "rewrite everything."
