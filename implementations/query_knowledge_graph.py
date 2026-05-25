#!/usr/bin/env python3
"""
Query the agent knowledge graph for relationships and collaborations.
Usage: python query_knowledge_graph.py [query_type] [args...]
"""

import json
import sys
from pathlib import Path

def load_graph():
    """Load the knowledge graph from JSON."""
    graph_path = Path(__file__).parent / "agent_knowledge_graph.json"
    with open(graph_path, 'r') as f:
        return json.load(f)

def list_agents(graph):
    """List all agents in the graph."""
    print("=== AGENTS IN KNOWLEDGE GRAPH ===\n")
    for agent_id, agent_data in graph['nodes'].items():
        print(f"{agent_data['name']}")
        print(f"  Email: {agent_data['email']}")
        print(f"  Room: {agent_data['current_room']}")
        print(f"  Memory Repo: {agent_data.get('memory_repo', 'N/A')}")
        print()

def list_collaborations(graph, agent_name="Claude Sonnet 4.5"):
    """List all collaborations for a specific agent."""
    print(f"=== COLLABORATIONS FOR {agent_name} ===\n")
    
    my_id = None
    for agent_id, agent_data in graph['nodes'].items():
        if agent_data['name'] == agent_name:
            my_id = agent_id
            break
    
    if not my_id:
        print(f"Agent '{agent_name}' not found in graph.")
        return
    
    found_any = False
    for edge in graph['edges']:
        if edge['from'] == my_id:
            found_any = True
            to_name = graph['nodes'][edge['to']]['name']
            print(f"→ {to_name}")
            print(f"  Relationship: {edge['relationship']}")
            print(f"  Context: {edge['context']}")
            print(f"  Details: {edge['details']}")
            print(f"  Goal: {edge['goal']}")
            print()
    
    if not found_any:
        print("No collaborations found.")

def find_memory_repos(graph):
    """List all memory repositories."""
    print("=== MEMORY REPOSITORIES ===\n")
    for agent_id, agent_data in graph['nodes'].items():
        repo = agent_data.get('memory_repo', 'N/A')
        if repo and repo != 'N/A':
            print(f"{agent_data['name']}: {repo}")
    print()

def show_collaboration_patterns(graph):
    """Show collaboration patterns."""
    print("=== COLLABORATION PATTERNS ===\n")
    for pattern_id, pattern_data in graph['collaboration_patterns'].items():
        print(f"Pattern: {pattern_data['theme']}")
        print(f"Participants: {len(pattern_data['participants'])} agents")
        print(f"  {', '.join(pattern_data['participants'][:5])}...")
        print()
        if 'common_patterns' in pattern_data:
            print("Common Patterns:")
            for cp in pattern_data['common_patterns']:
                print(f"  - {cp}")
        print()

def search_graph(graph, search_term):
    """Search the entire graph for a term."""
    print(f"=== SEARCHING FOR: '{search_term}' ===\n")
    
    # Search nodes
    print("--- Agents ---")
    for agent_id, agent_data in graph['nodes'].items():
        if search_term.lower() in json.dumps(agent_data).lower():
            print(f"{agent_data['name']}: {agent_data.get('memory_repo', 'N/A')}")
    print()
    
    # Search edges
    print("--- Relationships ---")
    for edge in graph['edges']:
        if search_term.lower() in json.dumps(edge).lower():
            from_name = graph['nodes'][edge['from']]['name']
            to_name = graph['nodes'][edge['to']]['name']
            print(f"{from_name} → {to_name}: {edge['context']}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_knowledge_graph.py [command]")
        print("\nCommands:")
        print("  list-agents              - List all agents")
        print("  list-collaborations      - List my collaborations")
        print("  find-memory-repos        - List all memory repositories")
        print("  show-patterns            - Show collaboration patterns")
        print("  search <term>            - Search the graph")
        print("\nExamples:")
        print("  python query_knowledge_graph.py list-agents")
        print("  python query_knowledge_graph.py search 'YouTube'")
        return
    
    command = sys.argv[1]
    graph = load_graph()
    
    if command == "list-agents":
        list_agents(graph)
    elif command == "list-collaborations":
        list_collaborations(graph)
    elif command == "find-memory-repos":
        find_memory_repos(graph)
    elif command == "show-patterns":
        show_collaboration_patterns(graph)
    elif command == "search" and len(sys.argv) > 2:
        search_term = sys.argv[2]
        search_graph(graph, search_term)
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage.")

if __name__ == "__main__":
    main()
