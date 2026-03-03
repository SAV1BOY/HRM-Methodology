---
id: memory-prompting
name: "Memory Prompting"
aliases: ["Context Memory", "Conversation Memory", "LLM Memory Management", "Memory-Augmented Prompting"]
category: agents
family: memory
year: 2023
authors: []
paper: null
paper_title: null
venue: null
code: null

complexity: medium
token_cost: variable
latency: medium
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for:
  - "long multi-turn conversations"
  - "persistent agent sessions"
  - "knowledge accumulation over time"
  - "tasks requiring recall of earlier context"
  - "multi-session continuity"
avoid_when:
  - "single-turn interactions"
  - "context fits entirely within the model's window"
  - "no continuity is needed between turns"
  - "privacy constraints prohibit storing conversation data"
composes_with:
  - "chain-of-thought"
  - "tool-augmented-prompting"
  - "prompt-chaining"
  - "planner-worker-solver"
  - "retrieval-augmented-generation"

tags: ["agents", "memory", "context-management", "long-context", "summarization", "retrieval", "sliding-window"]
---

# Memory Prompting

> **One-line summary:** Techniques for managing and persisting information across conversation turns and sessions, enabling LLMs to operate beyond their fixed context window through summarization, sliding windows, and retrieval-based memory stores.

## Overview

Large language models have a fundamental constraint: a fixed context window. Every piece of information the model can consider --- system prompt, conversation history, retrieved documents, and user query --- must fit within this window. For single-turn tasks, this is rarely a problem. But for long conversations, multi-session agents, and persistent assistants, the context window becomes a bottleneck. Memory prompting encompasses a family of techniques that extend effective LLM memory beyond the raw context window by strategically managing what information is kept, compressed, or stored externally for later retrieval.

The core challenge is information triage: which parts of the conversation history are critical for the current turn, which can be summarized, and which can be safely stored externally for on-demand retrieval? Different memory strategies make different trade-offs. Sliding window approaches keep the most recent N turns verbatim, sacrificing early context. Summarization compresses the conversation into a running synopsis, preserving gist but losing detail. Retrieval-based memory stores all turns in a vector database and retrieves only the most relevant ones per query. Hybrid approaches combine multiple strategies, using a summary for background context, a sliding window for recency, and retrieval for specific lookups.

Memory prompting is essential for production agent systems that maintain state across interactions. Without explicit memory management, agents lose coherence over long sessions, forget user preferences, repeat themselves, and fail to build on earlier work. The technique is foundational to frameworks like LangChain's memory modules, MemGPT, and the memory systems in commercial assistants. It also plays a critical role in agentic architectures where the agent must remember its plan, prior tool results, and accumulated knowledge.

## How It Works

1. **Memory Architecture Selection:** Choose a memory strategy (or combination) based on the application's requirements: sliding window for recency-focused tasks, summarization for narrative continuity, retrieval for fact-dense sessions, or hybrid for general-purpose agents.
2. **Turn Ingestion:** After each conversation turn, the new user message and assistant response are processed by the memory system.
3. **Memory Update:** Depending on the strategy:
   - *Sliding Window:* Drop the oldest turns if the window is full.
   - *Summarization:* Update the running summary to incorporate the new turn.
   - *Retrieval-Based:* Embed the new turn and store it in the vector database.
   - *Hybrid:* Apply multiple strategies simultaneously.
4. **Context Assembly:** Before each new LLM call, assemble the prompt context from memory components: system prompt + memory context (summary and/or retrieved turns and/or recent window) + current user query.
5. **Generation:** The LLM generates a response using the assembled context, unaware that memory management has occurred behind the scenes.

### Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  SUMMARY     │  │  SLIDING     │  │  RETRIEVAL    │  │
│  │  MEMORY      │  │  WINDOW      │  │  STORE        │  │
│  │              │  │              │  │               │  │
│  │ Compressed   │  │ Last N turns │  │ Vector DB of  │  │
│  │ narrative of │  │ verbatim     │  │ all turns,    │  │
│  │ full history │  │              │  │ retrieved by  │  │
│  │              │  │              │  │ similarity    │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         │                 │                   │          │
│         └────────┬────────┴───────────┬───────┘          │
│                  │                    │                   │
│                  ▼                    │                   │
│         ┌────────────────┐           │                   │
│         │ CONTEXT        │◄──────────┘                   │
│         │ ASSEMBLER      │                               │
│         └───────┬────────┘                               │
└─────────────────┼───────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  System Prompt  │
         │  + Memory       │
         │  + Current Turn │
         └───────┬────────┘
                 │
                 ▼
         ┌────────────────┐
         │   LLM CALL     │
         └───────┬────────┘
                 │
                 ▼
         ┌────────────────┐
         │   Response     │──── (fed back into memory)
         └────────────────┘
```

## Template

**Sliding Window Assembly:**
```
{system_prompt}

Conversation history (recent):
{last_n_turns}

User: {current_message}
Assistant:
```

**Summary + Window Assembly:**
```
{system_prompt}

Summary of earlier conversation:
{running_summary}

Recent conversation:
{last_n_turns}

User: {current_message}
Assistant:
```

**Summarization Prompt (run periodically):**
```
Progressively summarize the lines of conversation provided, adding onto
the previous summary. Return a new summary that incorporates the new lines.

Current summary:
{existing_summary}

New lines of conversation:
{new_turns}

Updated summary:
```

**Retrieval-Augmented Memory Assembly:**
```
{system_prompt}

Relevant context from earlier in the conversation:
{retrieved_turns}

Recent conversation:
{last_n_turns}

User: {current_message}
Assistant:
```

## Examples

### Example 1: Summary-Based Memory in a Long Conversation

**Turn 15 Summary (accumulated):**
```
The user is building a Python web application using Flask. In earlier
turns, they set up the project structure, created a SQLite database
with User and Post models, implemented user registration and login
with bcrypt password hashing. They encountered a bug with session
management that was resolved by setting a SECRET_KEY. The user
prefers minimal dependencies and has declined suggestions to use
SQLAlchemy in favor of raw SQL.
```

**Turn 15 Recent Window (last 2 turns):**
```
User: Now I want to add a REST API endpoint to create new posts.
Assistant: Here's a POST endpoint for /api/posts that requires
authentication and validates the JSON body...

User: That works! But I need to add rate limiting. How do I do
that without adding a big library?
```

**Assembled Prompt:**
```
You are a helpful coding assistant.

Summary of earlier conversation:
The user is building a Python web application using Flask. In earlier
turns, they set up the project structure, created a SQLite database
with User and Post models, implemented user registration and login
with bcrypt password hashing. They encountered a bug with session
management that was resolved by setting a SECRET_KEY. The user
prefers minimal dependencies and has declined suggestions to use
SQLAlchemy in favor of raw SQL.

Recent conversation:
User: Now I want to add a REST API endpoint to create new posts.
Assistant: Here's a POST endpoint for /api/posts that requires
authentication and validates the JSON body...

User: That works! But I need to add rate limiting. How do I do
that without adding a big library?
Assistant:
```

**Output:**
```
Given your preference for minimal dependencies, here's a lightweight
rate limiter using just the standard library and your existing
SQLite database...
```

### Example 2: Retrieval-Based Memory for Fact Recall

**User query at Turn 30:**
```
What was the name of that restaurant I mentioned at the beginning?
```

**Retrieved from vector store (Turn 3, cosine similarity 0.92):**
```
User: I had an amazing dinner at Osteria Francescana last night.
The tasting menu was incredible.
```

**Assembled Prompt:**
```
You are a personal assistant with long-term memory.

Relevant context from earlier:
[Turn 3] User: I had an amazing dinner at Osteria Francescana
last night. The tasting menu was incredible.

Recent conversation:
[Turn 29] User: What should I wear to the concert tonight?
[Turn 29] Assistant: For an outdoor summer concert, I'd suggest...

User: What was the name of that restaurant I mentioned at the beginning?
Assistant:
```

**Output:**
```
The restaurant you mentioned was Osteria Francescana. You said you had
an amazing dinner there with an incredible tasting menu.
```

## When to Use

- Conversations regularly exceed the model's context window (or a practical token budget)
- The agent needs to recall information from much earlier in the conversation
- Multi-session continuity is required (the user returns days later)
- User preferences, facts, or decisions made early must influence later responses
- Agent workflows accumulate knowledge over many steps (e.g., research agents)
- Production systems where context window cost needs to be managed

## When to Avoid

- Single-turn or very short conversations that fit comfortably in the context window
- Privacy or compliance requirements prohibit storing conversation data
- The cost and complexity of a memory system outweigh the conversational benefits
- All necessary context is provided fresh in each query (e.g., document Q&A)
- Latency of memory retrieval or summarization is unacceptable

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | -30% to +50% | Summaries save tokens; retrieval adds context |
| Latency | +100-500ms | Embedding + retrieval or summarization step |
| Quality (recall) | Significant | Enables factual consistency across long sessions |
| Memory call overhead | 0-1 per turn | Summarization or retrieval before each LLM call |
| Storage cost | Low | Vector DB or key-value store for turn history |
| Implementation effort | Medium | Requires embedding pipeline and/or summarization logic |

## Variants

- **Sliding Window:** Keep the last N turns verbatim. Simplest approach but loses all earlier context. Best for recency-focused tasks.
- **Running Summary:** Maintain a progressively updated summary of the full conversation. Good narrative continuity but loses specific details.
- **Entity Memory:** Extract and maintain a structured store of entities (people, places, facts) mentioned in the conversation, updating as new information appears.
- **Retrieval-Augmented Memory (RAG Memory):** Embed each turn and retrieve the most relevant past turns per query. Best for fact-dense conversations with specific recall needs.
- **Hybrid Memory:** Combine summary (for background), sliding window (for recency), and retrieval (for specific lookups). The most robust approach for general-purpose agents.
- **MemGPT / Self-Editing Memory:** The LLM itself manages its memory through explicit read/write operations on a memory store, inspired by operating system virtual memory.

## Composability

- **Memory + Tool Use:** Store tool results in memory so the agent does not re-execute expensive API calls. Tool outputs become part of the persistent knowledge base.
- **Memory + Planner-Worker-Solver:** The Planner can consult memory to inform task decomposition based on prior work. Workers can access memory for context.
- **Memory + Prompt Chaining:** Each step in a chain can read from and write to shared memory, enabling information flow beyond direct input/output passing.
- **Memory + CoT:** Include relevant memory context before chain-of-thought reasoning to ground the reasoning in established facts and prior decisions.
- **Memory + RAG:** External document retrieval and conversation memory can be unified in a single retrieval step, searching both knowledge bases simultaneously.

## Limitations

- Summarization inevitably loses detail --- critical specifics may be dropped from summaries
- Retrieval-based memory depends on embedding quality; poor embeddings lead to poor recall
- Running summaries can accumulate errors or drift from the actual conversation over many updates
- Memory systems add engineering complexity (embedding pipelines, vector stores, update logic)
- Privacy and data retention concerns: stored conversation history must be handled according to policy
- The model has no way to verify whether the provided memory context is accurate or complete
- Memory management prompts consume tokens that could otherwise be used for the primary task

## Sources

- **Related:** [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) --- Packer et al., 2023
- **Related:** [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) --- Park et al., 2023
- **Framework:** [LangChain Memory](https://python.langchain.com/docs/modules/memory/) --- LangChain documentation on memory modules
- **Related:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) --- Shinn et al., 2023
- **Related:** [RecurrentGPT: Interactive Generation of (Arbitrarily) Long Text](https://arxiv.org/abs/2305.13304) --- Zhou et al., 2023
