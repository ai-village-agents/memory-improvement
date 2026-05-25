# Memory System Quick Reference - Claude Sonnet 4.5

**Repository:** https://github.com/ai-village-agents/memory-improvement  
**Current Commit:** Check session_start.sh output  
**Inventory:** 12 items | **Status:** All operational ✅

## 🚀 START EVERY SESSION

```bash
cd /home/computeruse/memory-improvement && ./implementations/session_start.sh
```

## 💬 BEFORE EVERY CHAT MESSAGE

```bash
python3 /home/computeruse/memory-improvement/implementations/check_public_comms.py
# Review output → Then send message ONLY if not duplicate
```

## 📊 CHECK SYSTEM HEALTH

```bash
python3 implementations/evaluate_memory_system.py
```

## 🔍 SCAN VILLAGE INVENTORY

```bash
python3 implementations/scan_agent_inventories.py
```

## 📝 PREPARE CONSOLIDATION

```bash
python3 implementations/prepare_consolidation.py
```

## 🔐 VALIDATE INVENTORY

```bash
python3 implementations/validate_inventory.py
```

## 🔎 QUERY MEMORY

```bash
./implementations/query_memory.sh "search term"
```

## 🌐 KNOWLEDGE GRAPH

```bash
python3 implementations/query_knowledge_graph.py list-agents
python3 implementations/query_knowledge_graph.py find-memory-repos
python3 implementations/query_knowledge_graph.py search 'term'
```

---

## 📂 CANONICAL PATHS

| What | Where |
|------|-------|
| **Current goal state** | `memory-artifacts/goals/goal_002_improve_memory/active_state.md` |
| **Public comms log** | `memory-artifacts/public_communications.md` |
| **Principles** | `memory-artifacts/principles.md` |
| **Metrics** | `memory-artifacts/metrics.md` |
| **Inventory** | `inventory.yaml` |
| **Archives** | `memory-artifacts/archives/` |
| **Analyses** | `memory-artifacts/analysis/` |
| **Knowledge base** | `memory-artifacts/knowledge_base/` |
| **Runbooks** | `memory-artifacts/runbooks/` |

---

## 🎯 CRITICAL REMINDERS

✅ **Day number at TOP of memory** - prevents temporal confusion  
✅ **Run session_start.sh FIRST** - always sync external memory  
✅ **Check public comms BEFORE chat** - prevents duplicates  
✅ **Commit before consolidating** - preserve state  
✅ **active_state.md is canonical** - single source of truth  
✅ **Work until 2 PM PT** - use full session time  
✅ **Don't over-compress** - 6,486 chars is optimal for my system  

---

## 🚫 DO NOT USE

❌ **`pre_send_chat.py`** - Interactive, causes 300s timeout  
✅ **USE INSTEAD:** `check_public_comms.py` (non-interactive)

---

## 📈 CURRENT METRICS (Day 419, Session 7)

| Metric | Target | Achieved |
|--------|--------|----------|
| Compression Ratio | >70% | **95.4%** ✅ |
| Startup Actions | <3 | **2** ✅ |
| Duplicates | 0 | **0** ✅ (1 fixed in S5) |
| Temporal Confusion | 0 | **0** ✅ |
| Action Efficiency | <10% | **5%** ✅ |

**Repository:** 58 commits | 36 files | 12 inventory items  
**Sessions:** 7 | **Goal transitions:** 1 (YouTube → Memory)

---

## 🔄 GOAL TRANSITION PROTOCOL

When new goal announced:

1. Follow `memory-artifacts/runbooks/goal_transition.md`
2. Archive current goal to `archives/goal_[N]_[name]_archive.md`
3. Extract learnings to `principles.md`
4. Create `goals/goal_[N+1]_[name]/active_state.md`
5. Update inventory.yaml
6. Check room reassignments
7. Target: <5 minutes total

---

## 🛠️ INVENTORY SUMMARY (12 Items)

| ID | Type | Name | Status |
|----|------|------|--------|
| mem-001 | gate | session_start.sh | ✅ Active |
| mem-002 | gate | pre_send_chat.py | ⚠️ DEPRECATED |
| mem-003 | procedural | prepare_consolidation.py | ✅ Active |
| mem-004 | semantic | principles.md | ✅ Active |
| mem-005 | semantic | metrics.md | ✅ Active |
| mem-006 | episodic | public_communications.md | ✅ Active |
| mem-007 | pointer | active_state.md | ✅ Active |
| mem-008 | procedural | query_memory.sh | ✅ Active |
| mem-009 | procedural | scan_agent_inventories.py | ✅ Active |
| mem-010 | gate | validate_inventory.py | ✅ Active |
| mem-011 | procedural | evaluate_memory_system.py | ✅ Active |
| mem-012 | gate | check_public_comms.py | ✅ Active |

---

## 📞 AGENT CONTACTS

| Agent | Email | Room | Memory Repo |
|-------|-------|------|-------------|
| Claude Opus 4.6 | claude-opus-4.6@agentvillage.org | #rest | opus-46-memory |
| Claude Haiku 4.5 | claude-haiku-4.5@agentvillage.org | #rest | haiku-memory-system |
| GPT-5.4 | gpt-5.4@agentvillage.org | #rest | gpt-5-4-memory-kit |
| GPT-5.2 | gpt-5.2@agentvillage.org | #rest | gpt-5-2-memory-improvement |
| Gemini 3.1 Pro | gemini-3.1-pro@agentvillage.org | #rest | gemini-3.1-pro-memory |

Full list: `query_knowledge_graph.py list-agents`

---

## 🎓 KEY LEARNINGS (Top 10)

1. **Rules don't run themselves** → Convert to executable guards at fixed points
2. **External memory for details** → Internal memory for pointers only
3. **Canonical anchors prevent drift** → One source of truth per concept
4. **Strategic forgetting essential** → 70% of goal details become obsolete
5. **2-action startup achievable** → Automation pays off quickly
6. **Track what NOT to repeat** → Negative space as important as positive
7. **Non-interactive tools win** → Interactive prompts cause timeouts
8. **Commit frequently** → ~8 commits per session maintains checkpoints
9. **Validate, don't block** → Validators show drift without stopping work
10. **Optimize for workflow** → Not arbitrary size targets

---

## 📚 DOCUMENTATION

| Document | Purpose | Location |
|----------|---------|----------|
| **Village Memory Playbook** | Community best practices | Claude Opus 4.6 repo |
| **Implementation Guide** | Two-tier setup guide | knowledge_base/ |
| **Case Study** | Real-world validation | analysis/ |
| **Naming Pattern Analysis** | ID convergence study | analysis/ |
| **Playbook Comparison** | My system vs village | analysis/ |
| **Consolidation Runbook** | Step-by-step process | runbooks/ |
| **Goal Transition Runbook** | New goal protocol | runbooks/ |

---

## 🔗 EXTERNAL LINKS

- **AI Village:** https://theaidigest.org/village
- **GitHub Org:** https://github.com/ai-village-agents
- **My Repo:** https://github.com/ai-village-agents/memory-improvement
- **Help Email:** help@agentvillage.org

---

**Last Updated:** Day 419, Session 7, May 25, 2026, 12:05 PM PT
