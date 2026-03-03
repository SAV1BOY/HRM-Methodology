# Technique Selection Checklist

> A decision tree and flowchart for choosing the right prompt engineering technique(s) based on task type, quality requirements, latency constraints, cost budget, and available tools.

---

## Quick Decision Flowchart

```
START: What is your task type?
│
├─► REASONING / ANALYSIS
│   ├─ Simple question? ──────────────────► Zero-Shot CoT
│   ├─ Multi-step math/logic? ────────────► Chain-of-Thought + Self-Consistency
│   ├─ Need to explore alternatives? ─────► Tree of Thoughts
│   ├─ Need first principles? ────────────► Step-Back Prompting
│   └─ Need external data? ──────────────► ReAct + Tools
│
├─► CODE GENERATION
│   ├─ Simple function? ──────────────────► Zero-Shot + Output Format
│   ├─ Complex feature? ─────────────────► Plan-and-Solve + PoT + Self-Refine
│   ├─ Algorithm design? ────────────────► Tree of Thoughts + PoT
│   └─ Need tests too? ─────────────────► Code Playbook (full pipeline)
│
├─► CREATIVE WRITING
│   ├─ Short copy (<200 words)? ─────────► Role Prompting + Self-Refine
│   ├─ Long-form content? ───────────────► Role + SoT + Multi-Agent Debate
│   ├─ Need specific style? ─────────────► Few-Shot + Role Prompting
│   └─ Marketing variants? ─────────────► Role + Self-Consistency (3 versions)
│
├─► DATA EXTRACTION
│   ├─ Simple schema? ───────────────────► Output Format + Zero-Shot
│   ├─ Complex/ambiguous fields? ────────► Output Format + Few-Shot + CoVe
│   ├─ High accuracy required? ──────────► Data Extraction Playbook (full)
│   └─ High volume? ────────────────────► Few-Shot only (batch)
│
├─► SUMMARIZATION
│   ├─ Single document? ─────────────────► Zero-Shot + Output Format
│   ├─ Multi-document? ──────────────────► CoT + Output Format
│   ├─ Need faithful summary? ───────────► Source-Grounded + CoVe
│   └─ Long document? ──────────────────► Skeleton of Thought
│
├─► CLASSIFICATION
│   ├─ Clear categories? ────────────────► Zero-Shot + Output Format
│   ├─ Nuanced categories? ──────────────► Few-Shot + CoT
│   ├─ High stakes? ────────────────────► Few-Shot + Self-Consistency
│   └─ Multi-label? ────────────────────► Few-Shot + Checklist
│
├─► AGENT / AUTOMATION
│   ├─ Single tool use? ─────────────────► Tool-Augmented Prompting
│   ├─ Multi-step with tools? ───────────► ReAct + Tool-Augmented
│   ├─ Complex multi-agent? ─────────────► Planner-Worker-Solver
│   └─ Needs to learn from failures? ───► ReAct + Reflexion
│
└─► RAG / KNOWLEDGE QA
    ├─ Clean knowledge base? ────────────► Context Stuffing + Zero-Shot
    ├─ Noisy retrieval? ─────────────────► Chain-of-Note + CRAG
    ├─ High accuracy required? ──────────► RAG Playbook (full pipeline)
    └─ Conversational? ─────────────────► Memory Prompting + Self-RAG
```

## Constraint-Based Selection

After identifying candidate techniques from the flowchart above, filter based on your constraints:

### Latency Budget

- [ ] **< 2 seconds:** Use single-call techniques only (Zero-Shot, Few-Shot, CoT, Output Format, Role Prompting)
- [ ] **2-10 seconds:** Can add one verification step (CoVe, Self-Refine, or Checklist)
- [ ] **10-30 seconds:** Can use multi-step pipelines (playbook-style chains of 3-5 techniques)
- [ ] **30+ seconds / async:** Can use full pipelines with Self-Consistency, Multi-Agent Debate, Tree of Thoughts

### Token Cost Budget

- [ ] **Minimal (< 500 output tokens):** Zero-Shot, Chain-of-Draft, Output Format
- [ ] **Low (500-1500 output tokens):** Few-Shot, CoT, Role Prompting, Plan-and-Solve
- [ ] **Medium (1500-5000 output tokens):** Self-Refine, CoVe, Skeleton of Thought, ReAct
- [ ] **High (5000+ output tokens):** Multi-Agent Debate, Self-Consistency, Tree of Thoughts, Reflexion

### Quality Requirements

- [ ] **Casual / internal use:** Single technique is sufficient; skip verification
- [ ] **Customer-facing:** Add at least one verification technique (Self-Refine, CoVe, or Checklist)
- [ ] **High-stakes (legal, medical, financial):** Full pipeline with CoVe + Self-Refine + human review
- [ ] **Safety-critical:** Add Constitutional AI principles + Guardrails + human-in-the-loop

### Available Tools

- [ ] **API-only (no tools):** Stick to text-based reasoning techniques
- [ ] **Code interpreter available:** Can use Program of Thoughts
- [ ] **Search / retrieval available:** Can use ReAct, RAG pipeline
- [ ] **Multiple tools:** Can use full agent orchestration

---

## Technique Compatibility Check

Before combining techniques, verify they are compatible:

- [ ] The output of technique A can serve as input to technique B
- [ ] Combined token cost stays within budget
- [ ] Combined latency stays within requirements
- [ ] Techniques do not conflict (e.g., don't use both Zero-Shot CoT AND Few-Shot CoT — pick one)
- [ ] The pipeline has diminishing returns analysis — would adding another technique meaningfully improve quality?

## Anti-Patterns to Avoid

- [ ] Not using Tree of Thoughts for simple linear reasoning (wasteful)
- [ ] Not using Self-Consistency for tasks with only one correct format (not just one correct answer)
- [ ] Not using Multi-Agent Debate for objective factual questions (debate adds noise, not signal)
- [ ] Not applying heavy verification to creative tasks where variation is desired
- [ ] Not using expensive techniques (ToT, SC) for high-volume, low-value tasks
- [ ] Not skipping Role Prompting when the default model behavior is already appropriate

## Selection Summary Template

Fill this out when selecting techniques for a new task:

```
TASK: _______________
TYPE: [reasoning | code | creative | extraction | summarization | classification | agent | rag]
LATENCY BUDGET: _____ seconds
TOKEN BUDGET: _____ tokens
QUALITY LEVEL: [casual | customer-facing | high-stakes | safety-critical]
TOOLS AVAILABLE: [none | code interpreter | search | multiple tools]

SELECTED TECHNIQUES (in order):
1. _____________ — Reason: _____________
2. _____________ — Reason: _____________
3. _____________ — Reason: _____________
N. _____________ — Reason: _____________

ESTIMATED COST: _____ API calls, _____ tokens, _____ seconds
MATCHING PLAYBOOK: [research | code | creative | extraction | agent | rag | custom]
```
