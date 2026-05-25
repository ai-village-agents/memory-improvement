#!/bin/bash
# Session startup script for memory system
# Run at the beginning of each session

echo "=== CLAUDE SONNET 4.5 SESSION START ==="
echo "Date: $(date)"
echo ""

# Check git status of memory repo
echo "--- Memory Repository Status ---"
cd /home/computeruse/memory-improvement
echo "Branch: $(git branch --show-current)"
echo "Latest commit: $(git log -1 --oneline)"
echo "Status:"
git status --short
echo ""

# Display current goal
echo "--- Current Goal ---"
CURRENT_GOAL=$(ls memory-artifacts/goals/ | tail -1)
echo "Active goal: $CURRENT_GOAL"
echo ""
cat "memory-artifacts/goals/$CURRENT_GOAL/active_state.md" | head -20
echo ""
echo "[... truncated, see full file at memory-artifacts/goals/$CURRENT_GOAL/active_state.md]"
echo ""

# Quick stats
echo "--- Memory System Stats ---"
echo "Archived goals: $(ls memory-artifacts/archives/ 2>/dev/null | wc -l)"
echo "Active goals: $(ls memory-artifacts/goals/ 2>/dev/null | wc -l)"
echo "Knowledge base files: $(ls memory-artifacts/knowledge_base/ 2>/dev/null | wc -l)"
echo ""

echo "--- Inventory Validation ---"
python3 "/home/computeruse/memory-improvement/implementations/validate_inventory.py" && echo "Inventory: VALID" || echo "Inventory: VALIDATION FAILED (non-blocking)"
echo ""

echo "=== SESSION START COMPLETE ==="
