---
id: skeleton-of-thought
name: "Skeleton of Thought"
aliases:
  - SoT
  - Skeleton-of-Thought
  - Parallel Elaboration
category: reasoning
family: thought-generation
year: 2023
authors:
  - Xuefei Ning
  - Zinan Lin
  - Zixuan Zhou
  - Huazhong Yang
  - Yu Wang
paper: "https://arxiv.org/abs/2307.15337"
paper_title: "Skeleton-of-Thought: Large Language Models Can Do Parallel Decoding"
venue: "ICLR 2024"
code: "https://github.com/imagination-research/sot"
complexity: medium
token_cost: medium
latency: low
num_calls: 1+N parallel
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - long-form content generation
  - list-structured answers
  - multi-faceted explanations
  - latency-sensitive applications requiring long outputs
  - parallel API utilization
  - structured writing tasks
avoid_when:
  - deeply sequential reasoning where later steps depend on earlier ones
  - mathematical proofs requiring strict logical chains
  - short single-paragraph answers
  - creative writing requiring organic narrative flow
  - tasks where parallel decomposition is unnatural
composes_with:
  - chain-of-thought
  - self-consistency
  - chain-of-draft
  - retrieval-augmented-generation
tags:
  - parallel-decoding
  - latency-optimization
  - structured-generation
  - outline-first
  - speed
  - decomposition
---

# Skeleton of Thought

> **One-line summary:** Generates an answer skeleton (outline) first, then elaborates each point in parallel API calls, achieving up to 2x speedup in end-to-end latency for long-form responses.

## Overview

Skeleton of Thought (SoT), introduced by Ning et al. (2023), addresses the fundamental latency bottleneck of autoregressive LLM generation: long answers take proportionally long to produce because each token is generated sequentially. SoT breaks this sequential dependency by decomposing generation into two phases. In the first phase, the model produces a concise skeleton -- an outline of the key points the answer should cover. In the second phase, each skeleton point is elaborated independently in parallel API calls, and the results are concatenated to form the complete answer. Since the elaboration calls run concurrently, the wall-clock time is determined by the slowest single elaboration rather than the sum of all elaborations.

The key insight is that many types of answers are naturally decomposable: a question asking "What are the benefits of exercise?" produces a list of benefits that can be elaborated independently. By identifying and exploiting this parallelism, SoT achieves speedups of 1.5-2.4x across various question types without requiring any model modifications, fine-tuning, or specialized hardware. The technique works entirely at the API level, making it immediately deployable with any LLM service that supports concurrent requests.

However, SoT is not universally applicable. The authors candidly identify categories of questions where forced decomposition hurts quality: math problems with sequential dependencies, creative writing requiring narrative coherence, and questions requiring deeply integrated reasoning. To address this, they propose SoT with Router (SoT-R), which first classifies whether a question is suitable for skeleton-based parallel elaboration and falls back to standard generation when it is not. This self-aware routing mechanism makes SoT practical for production systems handling diverse query types.

## How It Works

1. **Skeleton generation**: Send a prompt asking the model to produce a concise skeleton of the answer -- a numbered list of key points, each described in a few words. This is a single, fast LLM call since the skeleton is short.
2. **Point distribution**: Parse the skeleton into individual points. Each point becomes an independent elaboration task.
3. **Parallel elaboration**: Send N concurrent API calls (one per skeleton point), each asking the model to elaborate on that specific point in the context of the original question.
4. **Assembly**: Collect the elaborated responses and concatenate them in the order specified by the skeleton, producing the final complete answer.
5. **Optional routing (SoT-R)**: Before step 1, a lightweight classifier or prompt determines whether the question is suitable for SoT. If not, fall back to standard sequential generation.

### Diagram

```
                         ┌──────────────────┐
                         │   User Question   │
                         └────────┬─────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Phase 1: Generate Skeleton │
                    │  (Single fast LLM call)     │
                    │                             │
                    │  1. Point A (3-5 words)     │
                    │  2. Point B (3-5 words)     │
                    │  3. Point C (3-5 words)     │
                    │  4. Point D (3-5 words)     │
                    └─────────────┬──────────────┘
                                  │
              ┌───────────┬───────┴───────┬───────────┐
              ▼           ▼               ▼           ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ Elaborate A│ │ Elaborate B│ │ Elaborate C│ │ Elaborate D│
       │ (parallel) │ │ (parallel) │ │ (parallel) │ │ (parallel) │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │               │               │               │
             └───────────┬───┴───────┬───────┘───────────────┘
                         │           │
                         ▼           ▼
                ┌────────────────────────────┐
                │  Assemble Final Answer      │
                │  [A detail] + [B detail]   │
                │  + [C detail] + [D detail]  │
                └────────────────────────────┘

        Latency = skeleton_time + max(elaborate_i)
        vs. standard = skeleton_time + sum(elaborate_i)
```

## Template

### Phase 1: Skeleton Generation

```
I will ask you a question. Instead of answering directly, please provide a
concise skeleton of the answer. The skeleton should be a numbered list of
3-10 key points, each described in a brief phrase (3-8 words).

Question: {question}

Skeleton:
```

### Phase 2: Point Elaboration (sent in parallel for each point)

```
Question: {question}

You are elaborating point {point_number} of an answer skeleton.

Complete skeleton for context:
{full_skeleton}

Now, elaborate on point {point_number}: "{point_text}"
Write 2-4 sentences providing detail, examples, or explanation for this
specific point. Do not repeat other points.

Elaboration:
```

## Examples

### Example 1: Factual Multi-Point Question

**Phase 1 -- Skeleton prompt:**
```
I will ask you a question. Instead of answering directly, please provide a
concise skeleton of the answer as a numbered list of key points.

Question: What are the main causes of the French Revolution?

Skeleton:
```

**Phase 1 -- Model output:**
```
1. Financial crisis and national debt
2. Social inequality under the Estates system
3. Enlightenment ideas challenging monarchy
4. Food shortages and bread prices
5. Weak leadership of Louis XVI
6. Influence of the American Revolution
```

**Phase 2 -- Parallel call for point 3:**
```
Question: What are the main causes of the French Revolution?
Elaborate on point 3: "Enlightenment ideas challenging monarchy"

Elaboration:
```

**Phase 2 -- Model output for point 3:**
```
Enlightenment philosophers such as Voltaire, Rousseau, and Montesquieu
promoted ideals of individual liberty, popular sovereignty, and separation of
powers that directly undermined the legitimacy of absolute monarchy. Rousseau's
"Social Contract" argued that political authority derives from the consent of
the governed, inspiring revolutionaries to demand representative government.
These ideas spread widely through salons and pamphlets, creating an intellectual
framework that transformed economic grievances into a coherent political movement.
```

### Example 2: Technical Explanation

**Phase 1 -- Skeleton:**
```
Question: Explain how HTTPS works.

Skeleton:
1. Client initiates connection with server
2. TLS handshake and certificate exchange
3. Asymmetric key exchange for shared secret
4. Symmetric encryption of data transfer
5. Integrity verification with MAC
6. Session termination and key disposal
```

**Phase 2 -- Parallel elaborations produce 2-4 sentences for each point, then all six are assembled into the complete answer.**

## When to Use

- Long-form answers that naturally decompose into parallel, independent sections (lists, multi-faceted explanations, comparisons).
- Latency-sensitive applications where users perceive a long wait for comprehensive answers.
- Systems with access to concurrent API calls (most cloud LLM deployments support parallel requests).
- Content generation tasks: blog outlines, report sections, FAQ entries, product descriptions.
- When the outline structure itself adds value by making the response more organized and scannable.
- High-throughput systems where reducing per-request latency improves overall user experience.

## When to Avoid

- Mathematical proofs or multi-step calculations where step N depends on the result of step N-1.
- Creative writing (stories, poems) where narrative flow and organic transitions are essential.
- Short answers where the skeleton overhead exceeds the time saved by parallelism.
- Deeply integrated reasoning tasks where all aspects must be considered holistically.
- Questions with a single clear answer that does not benefit from decomposition.
- Settings without parallel API access (e.g., local single-GPU inference with no batching).

## Cost & Performance

| Metric              | Value                     | Notes                                             |
|---------------------|---------------------------|----------------------------------------------------|
| Latency speedup     | 1.5-2.4x                 | Depends on number of skeleton points and balance    |
| Token overhead       | ~1.1-1.3x                | Skeleton + repeated context in elaboration calls     |
| Quality impact       | Neutral to slight gain    | Better organization; slight loss on integrated tasks |
| API calls            | 1 + N parallel            | N = number of skeleton points (typically 3-8)        |
| Implementation cost  | Low                       | Prompt engineering + parallel API orchestration       |
| Suitable questions   | ~50-60% of general queries| Per SoT-R analysis; decomposable questions benefit   |

## Variants

- **SoT with Router (SoT-R):** Adds a lightweight classification step before skeleton generation to determine if the question is suitable for parallel elaboration. Falls back to standard generation for unsuitable questions (math, creative writing, etc.).
- **Hierarchical SoT:** Generate a two-level skeleton (major sections with sub-points), then elaborate at the leaf level. Useful for very long documents like reports or articles.
- **SoT + Streaming:** Stream the skeleton to the user immediately (providing a fast initial response), then progressively fill in elaborations as parallel calls complete, providing a "progressive loading" UX.
- **Adaptive SoT:** Dynamically adjust the number of skeleton points based on question complexity. Simple questions get 2-3 points; complex ones get 8-10.
- **SoT for Code:** Generate a function skeleton (function signatures, class structure) then implement each function body in parallel. Effective for boilerplate-heavy code generation.

## Composability

- **SoT + Chain-of-Thought:** Use CoT within each elaboration call to reason through complex individual points while maintaining overall parallel speedup.
- **SoT + Self-Consistency:** Generate multiple elaborations for each point in parallel, then select the best one via voting or scoring before assembly.
- **SoT + Chain-of-Draft:** Use CoD for the skeleton phase (inherently brief) and optionally for elaborations to minimize total token usage while maintaining speed.
- **SoT + RAG:** Retrieve relevant documents for each skeleton point independently in parallel, then use the retrieved context in the corresponding elaboration call.
- **SoT + Verification:** After assembly, run a verification pass to check for consistency, redundancy, or contradictions between independently generated sections.

## Limitations

- Not all questions are decomposable; forced decomposition of inherently sequential or holistic reasoning tasks degrades quality.
- Independent elaboration can produce redundancy or inconsistency between sections, since each call lacks awareness of what other calls generate.
- The skeleton phase adds a sequential step; for very short answers, this overhead can negate the parallelism benefit.
- Requires infrastructure support for concurrent API calls, which may not be available in all deployment contexts.
- Token cost increases due to repeated context (the question and skeleton) in each parallel call.
- The router (SoT-R) is imperfect and may misclassify some questions, leading to inappropriate decomposition or unnecessary fallback.
- Transitions between assembled sections can feel abrupt without a final smoothing pass.

## Sources

- **Primary:** Ning, X., Lin, Z., Zhou, Z., Yang, H., & Wang, Y. (2023). Skeleton-of-Thought: Large Language Models Can Do Parallel Decoding. *ICLR 2024*. https://arxiv.org/abs/2307.15337
- **Related:** Sun, Z., et al. (2023). SpecInfer: Accelerating Generative Large Language Model Serving with Speculative Inference and Token Tree Verification. https://arxiv.org/abs/2305.09781
- **Related:** Chen, C., et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling. https://arxiv.org/abs/2302.01318
