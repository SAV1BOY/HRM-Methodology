---
id: rephrase-and-respond
name: "Rephrase and Respond (RaR)"
aliases: ["RaR", "Question Rephrasing"]
category: advanced-reasoning
family: decomposition
year: 2023
authors: ["Yihe Deng", "Weitong Zhang", "Zixiang Chen", "Quanquan Gu"]
paper: "https://arxiv.org/abs/2311.04205"
paper_title: "Rephrase and Respond: Let Large Language Models Ask Better Questions for Themselves"
venue: "arXiv 2023"
code: null

complexity: low
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["ambiguous questions", "poorly worded queries", "questions with implicit assumptions", "benchmark-style questions with tricky phrasing", "improving comprehension before reasoning"]
avoid_when: ["already clear and well-structured questions", "tasks where rephrasing might change the intent", "creative writing prompts", "extremely simple queries"]
composes_with: ["chain-of-thought", "few-shot-prompting", "step-back-prompting", "self-consistency"]

tags: ["question-clarity", "rephrasing", "decomposition", "low-complexity", "self-improvement"]
---

# Rephrase and Respond (RaR)

> **One-line summary:** RaR instructs the LLM to rephrase the question in its own words for clarity before answering, improving comprehension and response accuracy with minimal overhead.

## Overview

Rephrase and Respond (RaR) addresses a deceptively simple but pervasive problem: LLMs often misunderstand questions due to ambiguous phrasing, implicit context, or unconventional wording. Rather than adding complex reasoning scaffolds, RaR takes the minimalist approach of asking the model to first restate the question in its own words, then answer the rephrased version. This self-directed clarification step is analogous to a student restating a test question to confirm understanding before writing an answer.

The key insight from Deng et al. is that the gap between human question phrasing and LLM comprehension is a significant source of errors, particularly on benchmarks. Questions designed by humans often contain idiomatic expressions, implicit constraints, or domain-specific shorthand that can trip up models. By having the model rephrase the question, it surfaces and resolves these comprehension gaps internally, producing a version of the question that is more aligned with its own processing strengths.

RaR comes in two flavors: a one-step version where rephrasing and answering happen in a single prompt, and a two-step version where rephrasing occurs first and the rephrased question is then answered separately. The one-step version is preferred for its simplicity and lower latency, adding negligible overhead while delivering consistent accuracy improvements across a wide range of tasks.

## How It Works

1. **Question Reception:** The original question is presented to the LLM along with an instruction to rephrase before answering.

2. **Rephrasing:** The model restates the question in its own words, resolving ambiguities, making implicit constraints explicit, and restructuring for clarity. This is not paraphrasing for style but genuine comprehension-focused reformulation.

3. **Answering:** The model answers its own rephrased version of the question. Because the rephrased version better aligns with the model's understanding, the answer tends to be more accurate.

4. **Output:** Both the rephrased question and the answer are returned, allowing the user to verify that the rephrasing preserved the original intent.

### Diagram

```
┌──────────────────────────────────────────┐
│          Rephrase and Respond            │
│                                          │
│  ┌────────────────────┐                  │
│  │ Original Question   │                  │
│  │ (possibly ambiguous)│                  │
│  └─────────┬──────────┘                  │
│            │                             │
│            v                             │
│  ┌────────────────────┐                  │
│  │ LLM Rephrases      │                  │
│  │ in its own words    │                  │
│  │ (resolves ambiguity)│                  │
│  └─────────┬──────────┘                  │
│            │                             │
│            v                             │
│  ┌────────────────────┐                  │
│  │ LLM Answers the    │                  │
│  │ rephrased question  │                  │
│  └─────────┬──────────┘                  │
│            │                             │
│            v                             │
│  ┌────────────────────┐                  │
│  │ Rephrased Q + Answer│                  │
│  └────────────────────┘                  │
│                                          │
│  (All in a single LLM call)             │
└──────────────────────────────────────────┘
```

## Template

```
Given the following question, first rephrase it in your own words to ensure
you understand it correctly, then provide your answer.

Original question: {question}

Rephrased question: [Restate the question clearly and unambiguously]

Answer: [Provide your answer to the rephrased question]
```

### Two-Step Variant Template

```
Step 1:
Rephrase the following question to make it clearer and more precise.
Make any implicit assumptions explicit.

Original: {question}

Rephrased:

---

Step 2:
Answer the following question:
{rephrased_question}

Answer:
```

## Examples

### Example 1: Ambiguous Temporal Reasoning

**Input:**
```
Given the following question, first rephrase it in your own words to ensure
you understand it correctly, then provide your answer.

Original question: "If a store is open from 9 AM to 5 PM and it takes
30 minutes to get there, and I need to spend at least 2 hours there,
what is the latest I can leave my house?"
```

**Output:**
```
Rephrased question: "A store operates between 9:00 AM and 5:00 PM. The
travel time from my house to the store is 30 minutes. I need to be inside
the store for a minimum of 2 hours. What is the latest departure time
from my house such that I arrive at the store and still have at least
2 full hours before closing?"

Answer:
- Store closes at 5:00 PM
- I need 2 hours inside: must arrive by 3:00 PM (5:00 PM - 2 hours)
- Travel takes 30 minutes: must leave by 2:30 PM (3:00 PM - 30 minutes)

The latest I can leave my house is 2:30 PM.
```

### Example 2: Tricky Logic Question

**Input:**
```
Given the following question, first rephrase it in your own words to ensure
you understand it correctly, then provide your answer.

Original question: "A farmer has 17 sheep. All but 9 die. How many sheep
does the farmer have left?"
```

**Output:**
```
Rephrased question: "A farmer initially has 17 sheep. After some sheep
die, all except 9 of them have died. How many living sheep remain?"

Answer: The phrase "all but 9 die" means that 9 sheep survive. The farmer
has 9 sheep left.

Note: This is a common trick question where people mistakenly subtract 9
from 17. The rephrasing makes it clear that "all but 9" directly states
the number of survivors.
```

## When to Use

- Questions with ambiguous phrasing, double negatives, or tricky wording
- Benchmark evaluations where precise question comprehension is critical
- User-submitted queries that may contain informal language or implicit assumptions
- Multi-part questions where the relationships between parts might be misunderstood
- Cross-lingual or translated questions where phrasing may be awkward
- As a cheap "always-on" enhancement that adds minimal overhead to any pipeline

## When to Avoid

- Questions that are already perfectly clear and precise
- Tasks where rephrasing might inadvertently change the intent (e.g., legal or contractual questions where exact wording matters)
- Creative prompts where the original phrasing is intentionally evocative or open-ended
- When using an already well-structured prompt template with clear formatting
- Extremely simple factual queries (e.g., "What is 2+2?")

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | ~10-30% | Rephrased question adds modest tokens |
| Latency | Negligible (1 call) | Single-call variant adds no extra round trips |
| Quality gain | +3-8% | Across diverse benchmarks (math, logic, commonsense) |
| Num calls | 1 (or 2) | One-step preferred; two-step for harder cases |
| Implementation | Trivial | Just prepend rephrasing instruction |

## Variants

- **One-Step RaR:** Rephrasing and answering in a single prompt (default, recommended). Lowest overhead.
- **Two-Step RaR:** Separate calls for rephrasing and answering. Allows human inspection of the rephrased question before proceeding.
- **RaR with Constraints:** Explicitly instruct the model to preserve specific constraints or key terms during rephrasing to prevent drift.
- **Multi-Rephrase:** Generate multiple rephrasings and answer each, then aggregate (combines with self-consistency).

## Composability

- **RaR + Chain-of-Thought:** Rephrase first, then apply CoT to the rephrased question. The clearer question leads to better reasoning chains.
- **RaR + Step-Back Prompting:** Rephrase the question, then step back to identify underlying principles. The rephrasing ensures the step-back question is well-targeted.
- **RaR + Few-Shot:** Include examples of good rephrasings alongside few-shot task examples to teach the model what effective rephrasing looks like.
- **RaR + Self-Consistency:** Rephrase the question multiple ways, answer each rephrasing, and vote on the final answer.

## Limitations

- Rephrasing can sometimes change the meaning of the question, especially for nuanced or context-dependent queries
- The improvement is modest on questions that are already well-phrased
- For highly technical or domain-specific questions, the model might oversimplify during rephrasing
- Does not help when the model lacks the knowledge to answer regardless of phrasing
- The two-step variant doubles latency for marginal additional benefit in most cases
- On some tasks, the rephrasing step adds tokens without meaningful accuracy improvement

## Sources

- **Primary:** [Rephrase and Respond: Let Large Language Models Ask Better Questions for Themselves](https://arxiv.org/abs/2311.04205) — Deng et al., 2023
- **Related:** [Large Language Models Are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910) — Zhou et al., 2022
- **Related:** [Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models](https://arxiv.org/abs/2310.06117) — Zheng et al., 2023
