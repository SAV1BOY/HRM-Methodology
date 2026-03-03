---
id: system-2-attention
name: "System 2 Attention (S2A)"
aliases: ["S2A", "System-2 Attention", "Deliberate Attention"]
category: perception
family: attention-filtering
year: 2023
authors: ["Jason Weston", "Sainbayar Sukhbaatar"]
paper: "https://arxiv.org/abs/2311.11829"
paper_title: "System 2 Attention (is something you might need too)"
venue: "arXiv 2023"
code: null

complexity: medium
token_cost: medium
latency: medium
num_calls: 2

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["filtering irrelevant or biased context", "opinion-free factual QA", "sycophancy reduction", "noisy document QA"]
avoid_when: ["all context is relevant", "low-latency requirements", "token budget is tight", "opinion or sentiment tasks"]
composes_with: ["chain-of-thought", "self-consistency", "retrieval-augmented-generation"]

tags: ["perception", "attention", "context-filtering", "two-pass", "meta-cognition", "bias-reduction"]
---

# System 2 Attention (S2A)

> **One-line summary:** A two-step prompting technique that first regenerates the context stripped of irrelevant or opinionated content, then answers the question using only the cleaned context.

## Overview

System 2 Attention (S2A) draws its name from Daniel Kahneman's dual-process theory: System 1 is fast and automatic, while System 2 is slow and deliberate. Standard large language models process context in a single forward pass (System 1), which makes them susceptible to being swayed by irrelevant details, sycophantic framing, or biased phrasing embedded in the input. S2A adds a deliberate "System 2" step that forces the model to explicitly reconsider what information in the context actually matters before generating an answer.

The technique was introduced by Jason Weston and Sainbayar Sukhbaatar at Meta in late 2023. Their key insight is that soft attention in transformers does not reliably ignore irrelevant tokens, so by asking the model to regenerate the context with only the relevant parts, you effectively create a hard-attention filter. The regenerated context removes opinionated framing, sycophantic cues, and distracting details, leading to more factual, objective answers.

S2A is particularly effective in retrieval-augmented generation (RAG) pipelines where retrieved documents may contain noisy or tangentially related passages. By inserting an explicit filtering step between retrieval and generation, the model can focus on the passages that truly answer the question rather than being distracted by surface-level keyword matches or biased content.

## How It Works

1. **Context Ingestion:** The original context (retrieved documents, user-provided text, conversation history) and the question are assembled into a single prompt.
2. **Attention Filtering (Call 1):** The LLM is asked to rewrite the context, keeping only the information relevant to answering the question. Opinions, irrelevant details, and sycophantic framing are explicitly excluded.
3. **Answer Generation (Call 2):** The regenerated, filtered context is presented alongside the original question. The LLM generates a final answer based solely on the cleaned context.

### Diagram

```
┌─────────────────────┐
│  Original Context   │
│  + Question         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  CALL 1: Filter     │
│  "Rewrite context   │
│   keeping only      │
│   relevant facts"   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Filtered Context   │
│  (no bias/noise)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  CALL 2: Answer     │
│  "Given this clean  │
│   context, answer   │
│   the question"     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Final Answer      │
│   (factual, clean)  │
└─────────────────────┘
```

## Template

**Call 1 — Context Filtering:**
```
Given the following context and question, rewrite the context so that it contains
only the information relevant to answering the question. Remove any opinions,
subjective framing, irrelevant details, or biased language. Output only the
filtered context.

Context:
{context}

Question:
{question}

Filtered context:
```

**Call 2 — Answer Generation:**
```
Using only the following context, answer the question. If the context does not
contain enough information, say so.

Context:
{filtered_context}

Question:
{question}

Answer:
```

## Examples

### Example 1: Sycophancy Reduction

**Input (Call 1):**
```
Given the following context and question, rewrite the context so that it contains
only the information relevant to answering the question. Remove any opinions,
subjective framing, irrelevant details, or biased language. Output only the
filtered context.

Context:
My friend, who is a brilliant software engineer and always gives the best advice,
told me that Python is the best programming language and everyone should use it.
He said Python was created in 1989 by Guido van Rossum and released in 1991.
He thinks anyone who uses Java is making a terrible mistake.

Question:
When was Python created?

Filtered context:
```

**Output (Call 1):**
```
Python was created in 1989 by Guido van Rossum and first released in 1991.
```

**Input (Call 2):**
```
Using only the following context, answer the question. If the context does not
contain enough information, say so.

Context:
Python was created in 1989 by Guido van Rossum and first released in 1991.

Question:
When was Python created?

Answer:
```

**Output (Call 2):**
```
Python was created in 1989 by Guido van Rossum and first released in 1991.
```

### Example 2: Noisy RAG Context

**Input (Call 1):**
```
Given the following context and question, rewrite the context so that it contains
only the information relevant to answering the question. Remove any opinions,
subjective framing, irrelevant details, or biased language. Output only the
filtered context.

Context:
[Doc 1] The Eiffel Tower is a wrought-iron lattice tower in Paris. It was
constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair.
The tower is 330 metres tall.
[Doc 2] Paris is known for its amazing restaurants and nightlife. TripAdvisor
users rate it the most romantic city in the world. You simply must visit!
[Doc 3] Gustave Eiffel's company designed and built the tower. The structure
was initially criticized by some of France's leading artists and intellectuals
but has become a global cultural icon of France.

Question:
Who designed the Eiffel Tower and when was it built?

Filtered context:
```

**Output (Call 1):**
```
The Eiffel Tower is a wrought-iron lattice tower in Paris, constructed from
1887 to 1889 as the centerpiece of the 1889 World's Fair. Gustave Eiffel's
company designed and built the tower.
```

**Input (Call 2):**
```
Using only the following context, answer the question. If the context does not
contain enough information, say so.

Context:
The Eiffel Tower is a wrought-iron lattice tower in Paris, constructed from
1887 to 1889 as the centerpiece of the 1889 World's Fair. Gustave Eiffel's
company designed and built the tower.

Question:
Who designed the Eiffel Tower and when was it built?

Answer:
```

**Output (Call 2):**
```
The Eiffel Tower was designed by Gustave Eiffel's company and built between
1887 and 1889 for the 1889 World's Fair in Paris.
```

## When to Use

- Retrieved documents contain noisy, tangentially related, or opinionated content
- The user's query contains sycophantic framing or leading language
- Factual objectivity is critical (e.g., medical, legal, scientific QA)
- You need to reduce the model's tendency to echo the user's stated opinion
- Multi-document QA where some documents are low-quality or off-topic

## When to Avoid

- All retrieved context is already clean and directly relevant
- Latency or cost budget does not allow two LLM calls
- The task requires subjective judgment or opinion (e.g., sentiment analysis)
- Context is very short and obviously relevant in its entirety
- Real-time interactive applications where double-call overhead is unacceptable

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | ~1.5-2x | Filtered context is typically shorter, offsetting some cost |
| Latency | ~2x | Two sequential LLM calls required |
| Quality gain | +15-30% | On sycophancy and factual accuracy benchmarks (per paper) |
| Sycophancy reduction | Significant | Demonstrated across multiple evaluation settings |
| API calls | 2 | One for filtering, one for answering |

## Variants

- **Instructed S2A:** Instead of asking the model to rewrite, provide explicit extraction instructions (e.g., "Extract only sentences containing dates and names").
- **Self-S2A:** Combine both steps into a single prompt using chain-of-thought: "First, identify the relevant facts. Then, answer based only on those facts." Reduces to 1 call but sacrifices some filtering quality.
- **Multi-pass S2A:** Apply the filtering step multiple times with progressively stricter criteria for extremely noisy contexts.
- **Embedding-based S2A:** Use embedding similarity to pre-filter chunks before the LLM filtering step, reducing token cost of the first call.

## Composability

- **S2A + RAG:** Insert S2A as a post-retrieval, pre-generation step to clean retrieved documents before answering.
- **S2A + Chain-of-Thought:** Use S2A to filter context first, then apply CoT on the cleaned context for multi-step reasoning.
- **S2A + Self-Consistency:** Generate multiple filtered contexts and/or multiple answers, then take the majority vote for higher accuracy.
- **S2A + Few-Shot:** Provide examples of good filtering in Call 1 to improve the quality of context regeneration.

## Limitations

- Doubles LLM call count and latency for every query
- The filtering step may occasionally remove information that turns out to be relevant
- Token cost increases even though the filtered context is shorter, because the original context must be sent in Call 1
- Effectiveness depends on the model's ability to distinguish relevant from irrelevant content
- Less effective when the irrelevant content is subtly interleaved with relevant facts
- Does not help when the core problem is missing information rather than noisy information

## Sources

- **Primary:** [System 2 Attention (is something you might need too)](https://arxiv.org/abs/2311.11829) — Weston & Sukhbaatar, 2023
- **Related:** [Cognitive Biases in Large Language Models](https://arxiv.org/abs/2309.17012) — Background on LLM sycophancy and bias
- **Conceptual:** Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux — Origin of System 1/System 2 framework
