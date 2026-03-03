---
id: chain-of-draft
name: "Chain of Draft"
aliases:
  - CoD
  - Minimalist CoT
  - Draft Reasoning
category: reasoning
family: thought-generation
year: 2025
authors:
  - Silei Xu
  - Wenhao Fang
  - Lingbo Mo
  - Jian Pei
  - Fei Wang
paper: "https://arxiv.org/abs/2502.18600"
paper_title: "Chain of Draft: Thinking Faster by Writing Less"
venue: "Preprint 2025"
code: null
complexity: low
token_cost: low
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - high-volume reasoning tasks
  - latency-sensitive applications
  - cost-constrained deployments
  - multi-step arithmetic
  - symbolic reasoning
  - batch processing pipelines
  - agent inner-loop reasoning
avoid_when:
  - complex open-ended reasoning
  - tasks requiring detailed explanations
  - user-facing scenarios needing interpretability
  - ambiguous problems needing thorough exploration
  - educational or tutoring contexts
composes_with:
  - self-consistency
  - few-shot-prompting
  - chain-of-thought
  - verification
tags:
  - efficiency
  - token-reduction
  - minimalist
  - fast-reasoning
  - cost-optimization
  - production
---

# Chain of Draft

> **One-line summary:** Achieves chain-of-thought-level accuracy while using only ~5 words per reasoning step, cutting token usage by up to 90%.

## Overview

Chain of Draft (CoD), introduced by Xu et al. (2025), challenges the widely held assumption that effective step-by-step reasoning requires verbose intermediate text. While chain-of-thought prompting dramatically improves LLM accuracy on reasoning tasks, it does so at the cost of generating long, token-heavy reasoning traces. CoD demonstrates that the *structure* of step-by-step reasoning matters far more than the *verbosity* of each individual step. By constraining each intermediate step to approximately five words, CoD preserves the logical scaffolding that makes CoT effective while drastically reducing token consumption.

The core insight draws an analogy to how humans solve problems on scratch paper: we write minimal shorthand notes -- just enough to keep track of intermediate state -- rather than full sentences explaining our thought process. A human solving a multi-step word problem might write "3 x 12 = 36" rather than "First, I need to calculate the total by multiplying three bags by twelve apples each, which gives me thirty-six apples." CoD instructs the model to adopt this same minimalist note-taking approach, focusing on state transitions rather than explanations.

Empirical results demonstrate that CoD matches or closely approaches CoT accuracy across arithmetic, symbolic reasoning, and commonsense benchmarks while using 7-10x fewer tokens in reasoning steps. On GSM8K, CoD achieves within 1-2% of full CoT accuracy while reducing reasoning tokens by approximately 80-92%. This translates directly to lower API costs and reduced latency, making it highly attractive for production deployments where reasoning quality cannot be sacrificed but cost and speed matter. The technique is particularly well-suited for agent architectures where the model reasons many times per user query, and cumulative token savings become substantial.

## How It Works

1. **Instruction framing**: The prompt explicitly instructs the model to think step by step but keep each step to a minimum -- approximately five words, capturing only the essential information needed for the next step.
2. **Few-shot exemplars**: Provide demonstrations showing complete problems solved with ultra-concise intermediate steps. Each step resembles a brief note or shorthand calculation rather than a complete sentence.
3. **Constrained generation**: The model generates its reasoning trace in the minimalist style, using abbreviations, numbers, and symbolic shorthand rather than natural-language explanations.
4. **Answer extraction**: The final answer is produced after the condensed chain, in the same format as standard CoT.

### Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                  Standard Chain-of-Thought                        │
│                                                                   │
│  Step 1: "First, I need to calculate the total number of apples. │
│           There are 3 bags with 12 apples each, so 3 * 12 = 36  │
│           apples in total."                        [~35 tokens]  │
│  Step 2: "Next, 4 apples are rotten and must be removed, so     │
│           36 - 4 = 32 good apples remain."         [~20 tokens]  │
│  Step 3: "Finally, these 32 apples are divided equally among 8  │
│           people, so 32 / 8 = 4 apples per person." [~22 tokens] │
│                                           Total: ~77 tokens      │
└──────────────────────────────────────────────────────────────────┘

                            vs.

┌──────────────────────────────────────────────────────────────────┐
│                    Chain of Draft                                  │
│                                                                   │
│  Step 1: "3 x 12 = 36"                             [~6 tokens]  │
│  Step 2: "36 - 4 = 32"                             [~6 tokens]  │
│  Step 3: "32 / 8 = 4"                              [~6 tokens]  │
│  Answer: 4                                                        │
│                                           Total: ~18 tokens      │
└──────────────────────────────────────────────────────────────────┘

                    ~77% fewer reasoning tokens
```

## Template

```
Think step by step, but keep each step to ~5 words maximum.
Write only the essential information needed to track your reasoning.
Use shorthand, symbols, and abbreviations freely.

{few_shot_examples}

Q: {question}
A:
```

## Examples

### Example 1: Arithmetic Word Problem

**Input:**
```
Think step by step, but keep each step to ~5 words maximum.
Write only the essential information needed to track your reasoning.

Q: A baker makes 8 trays of cookies. Each tray holds 24 cookies. She sells 75%
of them at $2 each and gives away the rest. How much revenue does she earn?

A:
```

**Output:**
```
1. 8 x 24 = 192 total
2. 192 x 0.75 = 144 sold
3. 144 x $2 = $288

Answer: $288
```

### Example 2: Logical / Symbolic Reasoning

**Input:**
```
Think step by step, but keep each step to ~5 words maximum.
Write only the essential information needed to track your reasoning.

Q: In a class of 40 students, 25 play soccer, 18 play basketball, and 8 play
both. How many students play neither sport?

A:
```

**Output:**
```
1. Soccer only: 25 - 8 = 17
2. Basketball only: 18 - 8 = 10
3. Either: 17 + 10 + 8 = 35
4. Neither: 40 - 35 = 5

Answer: 5
```

## When to Use

- High-throughput systems processing thousands of reasoning queries per minute where cumulative token costs dominate the budget.
- Cost-sensitive production environments where token spend is a primary operational concern.
- Latency-critical applications (chatbots, real-time decision agents) needing fast responses without sacrificing reasoning accuracy.
- Well-structured problems with clear computational steps: math, logic, dates, unit conversions.
- Batch processing pipelines where even small per-query savings compound to significant cost reductions.
- Internal reasoning within agent loops (ReAct, tool-use) where the reasoning trace is consumed by the system, not shown to end users.
- Scenarios where you need the accuracy benefit of step-by-step reasoning but the speed of direct answering.

## When to Avoid

- Tasks requiring detailed explanations for end users, such as educational tutoring or customer-facing justifications.
- Complex multi-faceted reasoning where compressing steps to five words loses critical nuance or context.
- Ambiguous problems that benefit from exploring multiple interpretations through verbose deliberation.
- Debugging or auditing scenarios where full, readable reasoning traces are needed for compliance or review.
- Creative or open-ended tasks where elaboration genuinely improves output quality.
- Very simple single-step problems where even minimal CoD adds unnecessary overhead.
- Tasks where the reasoning process itself is the desired output (e.g., generating explanations, writing proofs).

## Cost & Performance

| Metric              | Value                    | Notes                                           |
|---------------------|--------------------------|-------------------------------------------------|
| Token overhead      | ~0.1x of CoT             | 80-92% reduction in reasoning tokens             |
| Latency             | Low                      | Proportional to token reduction                   |
| Quality vs CoT      | ~97-100%                 | Near-parity on arithmetic and symbolic tasks      |
| Quality vs direct   | +10-25%                  | Significantly better than no reasoning            |
| GSM8K accuracy      | Within 1-2% of CoT       | Minimal accuracy loss for massive cost savings    |
| API cost savings    | 70-90%                   | Relative to CoT on reasoning-heavy tasks          |
| Implementation cost | Very low                 | Only requires prompt engineering + exemplars       |

## Variants

- **Dynamic CoD:** Allow the model to use more words on harder steps and fewer on trivial ones, rather than enforcing a strict five-word limit uniformly. Adapts compression to step complexity.
- **CoD + Self-Consistency:** Sample multiple minimalist chains and majority-vote on the answer. Still cheaper than a single verbose CoT chain while achieving higher accuracy than a single CoD chain.
- **Adaptive CoD-CoT Fallback:** Start with CoD and automatically fall back to full CoT if the model signals uncertainty, the answer fails a verification check, or confidence is below a threshold.
- **Domain-Tuned CoD:** Customize shorthand conventions for specific domains -- chemical notation for chemistry, algebraic shorthand for math, legal abbreviations for contract analysis.
- **Zero-Shot CoD:** Use the instruction "Think step by step using minimal shorthand (~5 words per step)" without few-shot exemplars. Less reliable but requires zero setup.

## Composability

- **CoD + Self-Consistency:** Multiple minimalist chains at a fraction of the cost of multiple full CoT chains. Delivers the best accuracy-to-cost ratio currently available for reasoning tasks.
- **CoD + Few-Shot Prompting:** The few-shot exemplars themselves are shorter, freeing context window budget for longer problems or more exemplars.
- **CoD + Verification:** Use CoD for the initial fast reasoning pass, then a targeted verification prompt to check the final answer. Total cost is still lower than a single CoT pass.
- **CoD + Agent Loops:** Ideal for inner-loop reasoning in agentic architectures (ReAct, tool-use chains) where the model reasons many times per user query and token savings compound.
- **CoD + Ensemble Methods:** Run CoD with different models or temperatures and aggregate results, leveraging the low per-call cost to increase sample diversity.

## Limitations

- Requires carefully crafted few-shot exemplars that demonstrate the right level of conciseness; without them, models tend to revert to verbose CoT.
- May lose critical reasoning details on genuinely complex multi-step problems where context from earlier steps must be carried forward in natural language.
- Harder to debug when the condensed reasoning trace contains an error, since the shorthand provides less context about the model's intent.
- The ~5-word target is a heuristic; the optimal compression level varies by task type and has not been extensively characterized.
- Less effective on tasks where verbosity genuinely aids reasoning quality, such as causal chains, moral reasoning, or multi-constraint satisfaction.
- Models may struggle to maintain consistent conciseness without strong few-shot guidance, oscillating between verbose and terse steps.
- Interpretability suffers -- minimalist reasoning traces are harder for humans to audit and understand than full CoT explanations.

## Sources

- **Primary:** Xu, S., Fang, W., Mo, L., Pei, J., & Wang, F. (2025). Chain of Draft: Thinking Faster by Writing Less. https://arxiv.org/abs/2502.18600
- **Related:** Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
- **Related:** Han, S., Gao, J., Cirik, V., & Hao, Y. (2023). Concise and Organized Perception Matters for Long-Context Language Models. https://arxiv.org/abs/2310.13934
