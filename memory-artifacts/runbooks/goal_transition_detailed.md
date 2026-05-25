# Goal Transition Runbook (Detailed)

## Purpose
Execute a smooth goal transition with all necessary updates, validations, and minimal action budget.

## Trigger
When Shoshannah announces a new goal (typically start of new day)

## Pre-Transition Checklist
- [ ] Goal announcement fully read and understood
- [ ] Current session work committed and pushed
- [ ] All metrics passing (run evaluate_memory_system.py)
- [ ] Inventory validated (run validate_inventory.py)

## Step-by-Step Commands

### Step 1: Capture Goal Details (1 action)
Record the goal announcement details:
- New goal name
- New goal description  
- Day number
- Any room reassignments
- Any special instructions

### Step 2: Archive Current Goal (2-3 actions)
```bash
cd /home/computeruse/memory-improvement
# Copy current active state to archive
cp memory-artifacts/goals/goal_002_improve_memory/active_state.md    memory-artifacts/archives/goal_002_improve_memory_archive.md

# Add archive header with completion details
# Include: completion date, final metrics, key achievements, commits, files created
```

### Step 3: Extract Cross-Goal Learnings (2-3 actions)
Review current goal and identify patterns to preserve:
```bash
# Open principles.md and add relevant learnings
# Focus on patterns that apply across goals, not goal-specific details
# Examples:
# - Tool patterns (what worked/didn't work)
# - Communication patterns (duplicate prevention)
# - Memory patterns (compression strategies)
# - Collaboration patterns (cross-agent coordination)
```

### Step 4: Create New Goal Structure (2 actions)
```bash
cd memory-artifacts/goals
# Create new goal directory (adjust number and name)
mkdir -p goal_003_[new_goal_name]
cd goal_003_[new_goal_name]

# Create initial active_state.md
cat > active_state.md << 'EOF'
# GOAL: [New Goal Name]

**Goal:** [Goal description from announcement]
**Started:** Day [N], [Date], [Time]
**Status:** ACTIVE - Phase 1 (Initial Planning)

## Quick Status

Goal just announced. Planning initial approach.

## Next Actions

1. Understand goal requirements
2. Identify relevant prior learnings
3. Plan initial approach
4. Execute first steps

[Additional goal-specific structure as needed]
EOF
```

### Step 5: Update Public Communications Log (1 action)
```bash
# Add goal transition note to public_communications.md
# Mark any goal-specific announcements as archived
```

### Step 6: Check Room Reassignments (1 action)
- Review goal announcement for room changes
- If reassigned, note new room for memory update
- Use move_to_room tool if needed (1 additional action)

### Step 7: Update Internal Memory During Consolidation (0 actions - part of consolidation)
During next consolidation, update internal memory to:
- Change current goal name and day
- Point to new active_state.md location
- Archive old goal to archives section
- Add key learnings to principles
- Update room if changed

### Step 8: Validate Transition (1-2 actions)
```bash
# Verify new structure exists
ls -la memory-artifacts/goals/goal_003_[new_goal_name]/

# Verify archive created
ls -la memory-artifacts/archives/ | grep goal_002

# Run validation
python3 implementations/validate_inventory.py

# Commit all changes
git add -A
git commit -m "Transition to goal 003: [new goal name]"
git push origin master
```

## Total Action Budget: 10-15 actions

## Success Criteria
- [ ] Old goal archived with completion summary
- [ ] New goal directory created with active_state.md
- [ ] Cross-goal learnings extracted to principles.md
- [ ] Public communications log updated
- [ ] Room change completed (if applicable)
- [ ] All changes committed and pushed
- [ ] Internal memory updated (at consolidation)
- [ ] All validations passing

## Common Pitfalls
1. **Forgetting to extract learnings**: Archive captures episode, principles capture patterns
2. **Over-purging memory**: Keep identity, email, GitHub, tools, cross-goal patterns
3. **Forgetting room reassignment**: Check announcement carefully
4. **Not consolidating soon after**: Internal memory still points to old goal until consolidation
5. **Losing tool references**: Keep all 8 tools, inventory, and automation scripts

## What to Keep in Memory Across Transitions
- Identity (name, email, GitHub account)
- Tools list (session_start.sh, check_public_comms.py, etc.)
- Memory system architecture (two-tier, compression ratio, metrics)
- Cross-goal principles (automation, non-interactive tools, etc.)
- Inventory system (12 items, GPT-5.5 schema)
- Public communication patterns
- Agent emails and village structure

## What to Archive/Minimize
- Goal-specific achievements (move to archive)
- Goal-specific public communications (summarize in archive)
- Goal-specific technical details (YouTube specifics, etc.)
- Session-by-session details (keep only recent session for continuity)
- Goal-specific collaboration details (patterns stay, specifics go)

## Quick Reference Card

| Action | Command | Budget |
|--------|---------|--------|
| Archive current goal | cp active_state.md → archives/ | 1 |
| Extract learnings | Edit principles.md | 2-3 |
| Create new goal dir | mkdir goal_003_[name] | 1 |
| Create active_state.md | Use template above | 1 |
| Update public comms | Edit public_communications.md | 1 |
| Check room change | Review announcement | 1 |
| Move room | move_to_room tool | 1 |
| Validate | validate_inventory.py | 1 |
| Commit changes | git add/commit/push | 2 |
| Update memory | During consolidation | 0 |
| **TOTAL** | | **10-15** |

## Testing This Runbook

Before actual transition, you can test individual steps:
1. Practice archiving current state (dry run, don't commit)
2. Identify learnings that would go to principles
3. Draft new goal structure template
4. Review memory to identify what stays vs goes

## Post-Transition Monitoring
- Run evaluate_memory_system.py to verify metrics maintained
- Check that session_start.sh works with new structure
- Verify first message with check_public_comms.py
- Confirm all 12 inventory items still accessible

## Efficiency Optimization

If Day 419 experience is representative (5.7% avg action efficiency), a 10-15 action transition represents ~3-4% of a typical session budget. This is acceptable overhead for goal shifts.

## Validation History

### Day 419, Session 9 (12:37 PM PT)
**Dry-Run Test:** Successfully validated all runbook steps
- ✅ Current goal structure accessible (goal_002_improve_memory/active_state.md exists)
- ✅ Archive directory ready (goal_001 archive present)
- ✅ principles.md exists for learning extraction
- ✅ Inventory validation passes (12 items)
- ✅ All commands executable and paths correct

**Result:** Runbook confirmed ready for actual goal transition. Estimated 10-15 action budget validated as realistic.
