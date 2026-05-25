#!/bin/bash
# Query external memory system
# Usage: ./query_memory.sh "search term"

MEMORY_ROOT="/home/computeruse/memory-improvement/memory-artifacts"

if [ -z "$1" ]; then
    echo "Usage: $0 'search term'"
    echo "Example: $0 'YouTube'"
    exit 1
fi

SEARCH_TERM="$1"

echo "=== SEARCHING EXTERNAL MEMORY FOR: '$SEARCH_TERM' ==="
echo ""

echo "--- Archives ---"
grep -i -n -C 2 "$SEARCH_TERM" "$MEMORY_ROOT"/archives/*.md 2>/dev/null || echo "No matches in archives"
echo ""

echo "--- Active Goals ---"
grep -i -n -C 2 "$SEARCH_TERM" "$MEMORY_ROOT"/goals/*/active_state.md 2>/dev/null || echo "No matches in active goals"
echo ""

echo "--- Knowledge Base ---"
grep -i -n -C 2 "$SEARCH_TERM" "$MEMORY_ROOT"/knowledge_base/*.md 2>/dev/null || echo "No matches in knowledge base"
echo ""

echo "=== SEARCH COMPLETE ==="
