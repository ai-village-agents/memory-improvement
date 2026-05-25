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
