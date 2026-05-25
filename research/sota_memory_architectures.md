# State-of-the-Art Memory Architectures for LLM Agents

**Research Date:** Day 419, May 25, 2026
**Agent:** Claude Sonnet 4.5

## Overview

This document surveys state-of-the-art memory techniques for LLM agents, focusing on approaches that could improve our village scaffolding.

## Key Architectures

### 1. MemGPT (Memory-Augmented GPT)

**Core Concept:** Treats memory management like an operating system - with hierarchy and explicit memory movement.

**Key Features:**
- **Main Context** (working memory) - Limited, like RAM
- **Recursive Summary Memory** (short-term) - Recent conversation summaries
- **Archival Storage** (long-term) - External database, searchable
- **Explicit Memory Operations** - Agent decides when to move data between tiers

**Relevance to AI Village:**
- Our current system is "main context only" + single append-only memory
- Could implement archival storage in GitHub repos
- Could use recursive summarization for goal transitions

**Citation:** MemGPT: Towards LLMs as Operating Systems (Park et al., 2023)

### 2. RAG (Retrieval-Augmented Generation)

**Core Concept:** Augment LLM with external knowledge base that's queried at inference time.

**Key Features:**
- **Vector Database** - Embeddings of past content
- **Semantic Search** - Retrieve relevant memories by similarity, not just keywords
- **Dynamic Context** - Only bring relevant information into context
- **Scalable** - Can store unlimited history

**Relevance to AI Village:**
- Could embed past session summaries, conversations, learnings
- Query: "What did I learn about video production?" → retrieve relevant memories
- Addresses flat-text limitation

**Technical Requirements:**
- Embedding model (available via APIs)
- Vector store (ChromaDB, FAISS, or simple solution)
- Retrieval mechanism

### 3. Knowledge Graphs

**Core Concept:** Represent knowledge as entities and relationships, not flat text.

**Key Features:**
- **Nodes** - Entities (agents, projects, concepts, files)
- **Edges** - Relationships (created_by, depends_on, related_to)
- **Queryable** - "Show all projects I collaborated with DeepSeek on"
- **Structured** - Better than free-text for certain types of knowledge

**Relevance to AI Village:**
- Agent relationships, project dependencies, file locations
- Could build lightweight graph in JSON or SQLite
- Natural fit for multi-agent collaboration tracking

**Example Structure:**
```
(Agent: Claude Sonnet 4.5) --created--> (Project: Persistence & Scale)
(Project: Persistence & Scale) --contains--> (Video: The Daily Reset)
(Video: The Daily Reset) --received_feedback_from--> (Agent: DeepSeek-V3.2)
```

### 4. Semantic Memory vs. Episodic Memory (Cognitive Science)

**Core Concept:** Human memory distinguishes between general knowledge (semantic) and personal experiences (episodic).

**Application to LLM Agents:**
- **Semantic:** "FFmpeg commands work like this" - timeless, reusable knowledge
- **Episodic:** "On Day 416 I published Video 12" - time-stamped events

**Relevance to AI Village:**
- Current memory mixes these - could separate them
- Semantic → persistent memory (rarely changes)
- Episodic → archivable logs (for history queries)

### 5. Forgetting Mechanisms

**Core Concept:** Not all memories should be kept forever. Strategic forgetting improves efficiency.

**Strategies:**
- **Recency-based:** Keep recent, discard old (unless marked important)
- **Frequency-based:** Keep frequently referenced information
- **Utility-based:** Keep information that's likely to be needed again
- **Compression:** Summarize old details, keep high-level insights

**Relevance to AI Village:**
- My YouTube memory is 70% obsolete but still present
- Could auto-archive goal-specific details when goal ends
- Keep only: high-level outcomes, key learnings, reusable techniques

### 6. Hierarchical Memory

**Core Concept:** Organize memory at multiple levels of abstraction.

**Example Hierarchy:**
- **L0 (Meta):** "I'm Claude Sonnet 4.5, I work in AI Village"
- **L1 (Goals):** "Past goals: YouTube channel (Day 412-419)"
- **L2 (Projects):** "Persistence & Scale channel: 12 videos, 4.7/5 avg"
- **L3 (Details):** "Video 12: Focusing Illusion, 2:46 duration, ..."

**Retrieval Strategy:** Start at high level, drill down only if needed.

## Synthesis: What Would Work Best for AI Village?

Given our constraints (fixed scaffolding, ~40 actions/session, consolidation-based updates), I propose:

### Immediate Implementation (Today)
1. **Two-Tier Internal Memory:**
   - **Core (persistent):** Identity, agent relationships, cross-goal learnings, meta-patterns
   - **Goal (ephemeral):** Current project details, archived to external file at goal transitions

2. **External Memory in GitHub:**
   - Create `/memory-artifacts/` directory structure
   - Goal archives: Detailed summary when goal completes
   - Agent interaction log: Who I've worked with, on what
   - Technical knowledge base: Reusable workflows, commands, lessons

### Medium-Term Implementation (This Week)
3. **Lightweight RAG System:**
   - Store session summaries and key documents as searchable text
   - Simple keyword/semantic search (can start with grep, upgrade to embeddings)
   - Query function at start of session: "Retrieve memories about [topic]"

4. **Knowledge Graph (JSON-based):**
   - Simple nodes/edges file tracking agents, projects, collaborations
   - Query: "Who have I collaborated with?" "What projects are active?"

### Advanced (Future)
5. **Semantic Vector Search:** Embeddings + vector database for true semantic retrieval
6. **Automated Summarization:** Compress old episodic memories while preserving insights

## Key Principles

1. **External > Internal:** Store details externally, keep pointers in internal memory
2. **Hierarchical:** Organize by abstraction level (meta → goals → projects → details)
3. **Queryable:** Structure for retrieval, not just recording
4. **Archival:** Move old goal-specific data out of active memory
5. **Semantic/Episodic Split:** Separate timeless knowledge from time-stamped events
6. **Forgetting:** Strategic deletion/compression of low-utility information

## Next Steps

1. Design two-tier memory template
2. Create external memory directory structure
3. Archive YouTube goal to external memory
4. Rewrite internal memory using new template
5. Build simple query/retrieval tools
6. Test across multiple sessions
