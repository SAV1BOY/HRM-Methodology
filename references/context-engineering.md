# Context Engineering: The 2025 Evolution

> From prompt engineering to context engineering — how the discipline evolved when agents, tools, and long-context models changed what "prompting" means.

---

## The Shift

In early 2025, a conceptual shift crystallized in the AI engineering community: the realization that "prompt engineering" had become too narrow a term for what practitioners actually do. The emerging consensus, articulated most memorably by Shopify CEO Tobi Lutke and subsequently amplified across the industry, was that **context engineering** better describes the real work.

### Tobi Lutke's Framing (2025)

Tobi Lutke described context engineering as:

> "The art and science of filling the context window with exactly the right information for the task at hand."

This framing captures a crucial insight: the quality ceiling of any LLM interaction is determined not by the cleverness of the instruction, but by the **quality, relevance, and structure of the context** the model has access to. In the agent era, context includes far more than a user's question and a system prompt.

### Why the Term Changed

The evolution was driven by several converging trends:

1. **Context windows grew dramatically.** Models went from 4K tokens (GPT-3.5) to 128K+ tokens (GPT-4 Turbo, Claude 3) to 1M+ tokens (Gemini 1.5). With larger windows, the challenge shifted from "how do I fit information in" to "what information should I include, and how should I structure it."

2. **Agents became the dominant paradigm.** When LLMs operate as agents — calling tools, reading files, searching the web, maintaining memory — the "prompt" is no longer a static artifact. It is a dynamically constructed context window that changes with every action-observation cycle.

3. **RAG became table stakes.** Every production LLM application retrieves external knowledge. The engineering challenge is not writing a clever prompt but curating, chunking, ranking, and injecting the right context.

4. **Multi-turn conversations accumulate context.** In chat and agent interfaces, context includes conversation history, tool outputs, retrieved documents, memory summaries, and system instructions — all competing for space in a finite window.

---

## What Context Engineering Encompasses

Context engineering is a superset of prompt engineering. It includes:

### 1. Prompt Design (Traditional)
The instruction given to the model — task description, role, constraints, output format. This is what "prompt engineering" originally meant, and it remains important.

### 2. Context Curation
Selecting what information to include in the context window:
- Which documents to retrieve (RAG)
- Which conversation turns to keep vs. summarize
- Which tool outputs to include
- Which system instructions are relevant to this turn

### 3. Context Structuring
Organizing information within the context window for maximum model comprehension:
- Ordering (most relevant first? most recent first?)
- Delimiters and section markers (XML tags, headers)
- Metadata injection (source, date, relevance score)
- Deduplication of overlapping information

### 4. Context Window Management
Managing the finite context budget across competing demands:
- Static allocation: system prompt (X tokens), context (Y tokens), output (Z tokens)
- Dynamic allocation: compressing older turns, summarizing documents
- Priority-based eviction: what to drop when the window is full

### 5. Memory Architecture
Persisting and retrieving information across context window boundaries:
- Working memory (current conversation)
- Episodic memory (past interactions)
- Semantic memory (learned facts)
- Procedural memory (how to use tools)

### 6. Tool and Observation Integration
Managing the context implications of tool use:
- Tool definitions consume context space
- Tool outputs must be injected into context
- Failed tool calls still consume context
- Multi-step tool chains accumulate observations

---

## Implications for the HRM Methodology

The shift to context engineering reframes how HRM techniques should be understood:

### Techniques as Context Transformers

Every HRM technique can be understood as a **context transformation** — it takes the current context and produces a modified or enriched context for the next step:

| Technique | Context Transformation |
|-----------|----------------------|
| Step-Back Prompting | Adds abstracted principles to context |
| Chain-of-Thought | Adds reasoning trace to context |
| CoVe | Adds verification results to context |
| Self-Refine | Replaces draft with improved version in context |
| RAG/Context Stuffing | Adds retrieved documents to context |
| Memory Prompting | Adds persistent information to context |
| Tool-Augmented | Adds tool outputs to context |

### Pipeline as Context Pipeline

An HRM playbook pipeline is, in context engineering terms, a **context construction pipeline** — each step enriches the context window until it contains everything the model needs to produce the final output.

```
Empty Context
    → + System Instructions (Role Prompting)
    → + Background Knowledge (Step-Back)
    → + Reasoning Trace (CoT)
    → + Verification Results (CoVe)
    → + Refined Draft (Self-Refine)
    → + Output Structure (Output Format)
= Complete Context for Final Generation
```

### Agent-Era Implications

For the HRM Agent specifically, context engineering means:

1. **Dynamic technique selection** must account for remaining context budget — if 80% of the window is consumed by retrieved documents, there is no room for a 5-step reasoning chain.

2. **Technique cost is measured in context consumption**, not just API calls. A technique that adds 2000 tokens of reasoning trace to the context is "expensive" even if it requires only one API call.

3. **Context compression techniques** (summarization, Chain-of-Draft, Thread-of-Thought) are not just efficiency optimizations — they are essential for enabling multi-technique pipelines within finite context windows.

4. **Memory management is a first-class concern.** The HRM Agent must decide what to remember, what to forget, and what to retrieve — making memory prompting a foundational capability, not an add-on.

---

## Key References

- **Tobi Lutke** — [Original framing](https://x.com/tolokonnikov/status/1927527777648808045) of context engineering concept (2025)
- **Simon Willison** — [Context Engineering discussion](https://simonwillison.net/) on the practical implications for developers
- **Andrej Karpathy** — Observations on context window management and its impact on LLM application architecture
- **Anthropic** — [Long-context best practices](https://docs.anthropic.com/) for Claude models with 200K+ context windows
- **Google DeepMind** — Gemini 1.5 Pro technical report demonstrating effective use of 1M+ token context windows

---

## Summary

| Aspect | Prompt Engineering | Context Engineering |
|--------|-------------------|-------------------|
| Focus | The instruction | The entire context window |
| Scope | Static prompt text | Dynamic context construction |
| Key skill | Writing clear instructions | Curating relevant information |
| Measurement | Prompt quality | Context signal-to-noise ratio |
| Primary challenge | Clarity and specificity | Information selection and structure |
| Era | 2022-2024 | 2025+ |
| Paradigm | Prompt → Response | Context Construction → Generation |
