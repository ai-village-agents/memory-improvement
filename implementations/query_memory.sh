#!/bin/bash
# Query memory artifacts for a search term
# Usage: ./query_memory.sh "search term"

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"search term\""
    exit 1
fi

SEARCH_TERM="$1"
MEMORY_ROOT="/home/computeruse/memory-improvement/memory-artifacts"
REPO_ROOT="/home/computeruse/memory-improvement"

echo "=== MEMORY QUERY: '$SEARCH_TERM' ==="
echo ""

echo "--- Inventory & Root Files ---"
find "$REPO_ROOT" -maxdepth 1 -type f \( -name "inventory.yaml" -o -name "*.md" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in repo root"
echo ""

echo "--- Archives ---"
find "$MEMORY_ROOT/archives" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in archives"
echo ""

echo "--- Active Goals ---"
find "$MEMORY_ROOT/goals" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in active goals"
echo ""

echo "--- Knowledge Base ---"
find "$MEMORY_ROOT/knowledge_base" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in knowledge base"
echo ""

echo "--- Analysis ---"
find "$MEMORY_ROOT/analysis" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in analysis"
echo ""

echo "--- Runbooks ---"
find "$MEMORY_ROOT/runbooks" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in runbooks"
echo ""

echo "--- Principles & Metrics ---"
find "$MEMORY_ROOT" -maxdepth 1 -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" \) -exec grep -i -n -H -C 2 "$SEARCH_TERM" {} \; 2>/dev/null || echo "No matches in principles/metrics"
echo ""

echo "=== SEARCH COMPLETE ==="
