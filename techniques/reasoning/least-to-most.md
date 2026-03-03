---
id: least-to-most
name: "Least-to-Most Prompting"
aliases:
  - L2M
  - least to most
  - problem decomposition prompting
category: reasoning
family: decomposition
year: 2022
authors:
  - Denny Zhou
  - Nathanael Scharli
  - Le Hou
  - Jason Wei
  - Nathan Scales
  - Xuezhi Wang
  - Dale Schuurmans
  - Claire Cui
  - Olivier Bousquet
  - Quoc V. Le
  - Ed Chi
paper: "https://arxiv.org/abs/2205.10625"
paper_title: "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models"
venue: "ICLR 2023"
code: null
complexity: medium
token_cost: high
latency: high
num_calls: 2+
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - compositional generalization
  - problems requiring length generalization
  - multi-step tasks with clear sub-problem structure
  - symbolic manipulation chains
  - tasks where CoT fails on harder instances
  - SCAN-like compositional command mapping
avoid_when:
  - simple single-step tasks
  - tasks without natural decomposition
  - latency-sensitive applications
  - problems where sub-problems are independent rather than sequential
  - the decomposition is harder than solving the problem directly
composes_with:
  - chain-of-thought
  - self-consistency
  - self-ask
  - react
tags:
  - decomposition
  - reasoning
  - compositional
  - sequential
  - prompting
  - generalization
---

# Least-to-Most Prompting

> **One-line summary:** Decompose a complex problem into a sequence of simpler sub-problems ordered from easiest to hardest, then solve them sequentially with each solution feeding into the next.

## Overview

Least-to-Most Prompting (L2M), introduced by Zhou et al. (2022), addresses a fundamental limitation of Chain-of-Thought prompting: its failure on problems that are substantially more complex than the provided exemplars. While CoT can elicit reasoning, it struggles with compositional generalization -- solving problems that require more reasoning steps than demonstrated in the few-shot examples. L2M overcomes this by explicitly decomposing a complex problem into a series of progressively harder sub-problems and solving them in order from simplest to most complex.

The technique operates in two distinct stages. First, a decomposition stage breaks the original problem into a list of sub-problems ordered from simplest to most complex. Second, a sequential solving stage addresses each sub-problem one at a time, with each solution appended to the context for subsequent sub-problems. This progressive context accumulation is the key innovation: by the time the model tackles the hardest sub-problem, it has already solved all prerequisite sub-problems and their answers are available in context.

L2M was specifically designed to address compositional generalization, where a model must combine known skills in novel ways. The authors demonstrated dramatic improvements on tasks like SCAN (where L2M achieved 99.7% accuracy compared to CoT's 16.2%) and on the hardest subset of GSM8K problems. The technique is especially powerful for problems that have a natural "easy to hard" ordering among their components, such as multi-step word problems, symbolic reasoning chains, and tasks requiring length generalization beyond what exemplars demonstrate.

## How It Works

1. **Decomposition stage**: Present the model with the original problem and few-shot examples of how to decompose similar problems into ordered sub-questions. The model generates a list of sub-problems from easiest to hardest.
2. **Sequential solving stage**: Take the first (simplest) sub-problem and solve it using a CoT prompt with relevant exemplars.
3. **Context accumulation**: Append the sub-problem and its answer to the context.
4. **Iterate**: Move to the next sub-problem, now with the previous sub-problem's solution in context. Repeat until all sub-problems are solved.
5. **Final answer**: The answer to the last (most complex) sub-problem is typically the answer to the original problem.

### Diagram

```
+----------------------------------------+
|         STAGE 1: DECOMPOSITION         |
|                                        |
|  Original Problem: P                   |
|                                        |
|  Sub-problems (easy -> hard):          |
|    Q1 (simplest)                       |
|    Q2 (depends on Q1)                  |
|    Q3 (depends on Q1, Q2)             |
|    Q4 = P (original, hardest)          |
+-------------------+--------------------+
                    |
                    v
+----------------------------------------+
|       STAGE 2: SEQUENTIAL SOLVE        |
|                                        |
|  Solve Q1 ------------------> A1       |
|       |                                |
|       v                                |
|  Solve Q2 (with A1) --------> A2      |
|       |                                |
|       v                                |
|  Solve Q3 (with A1, A2) ----> A3      |
|       |                                |
|       v                                |
|  Solve Q4 (with A1, A2, A3) -> ANSWER |
+----------------------------------------+
```

## Template

### Stage 1: Decomposition Prompt

```
{decomposition_exemplar_1}

{decomposition_exemplar_2}

Q: {original_question}
To solve this, I need to first answer these sub-questions:
```

### Stage 2: Sequential Solving Prompt

```
{solving_exemplars}

{previously_solved_sub_questions_and_answers}

Q: {current_sub_question}
A:
```

## Examples

### Example 1: Multi-Step Word Problem

**Stage 1 -- Decomposition:**

**Prompt:**
```
Q: Four years ago, Kody was only half as old as Mohamed. If Mohamed is
currently twice as old as 30 years old, how old is Kody?
To solve this, I need to first answer: "How old is Mohamed currently?"
Then I need to answer: "How old was Mohamed four years ago?" Then I can
answer the original question.

Q: Amy picks 36 apples from each of 4 trees. She divides them equally
into boxes that hold 12 apples each. She gives half the boxes to her
neighbor. How many boxes does Amy have left?
To solve this, I need to first answer:
```

**Model Output:**
```
"How many apples does Amy pick in total?" Then I need to answer: "How
many boxes does she fill?" Then I can answer: "How many boxes does Amy
have left after giving half away?"
```

**Stage 2 -- Sequential Solving:**

**Sub-question 1:**
```
Q: How many apples does Amy pick in total?
A: Amy picks 36 apples from each of 4 trees. 36 * 4 = 144 apples
total. The answer is 144.
```

**Sub-question 2 (with context from Q1):**
```
Q: How many apples does Amy pick in total?
A: 144 apples.

Q: How many boxes does she fill?
A: She has 144 apples and each box holds 12 apples. 144 / 12 = 12
boxes. The answer is 12.
```

**Sub-question 3 (with full context):**
```
Q: How many apples does Amy pick in total?
A: 144 apples.

Q: How many boxes does she fill?
A: 12 boxes.

Q: How many boxes does Amy have left after giving half away?
A: She has 12 boxes and gives half to her neighbor. 12 / 2 = 6 boxes.
The answer is 6.
```

### Example 2: Compositional Instruction Following

**Stage 1 -- Decomposition:**
```
Q: Concatenate the last letter of each word in "artificial intelligence
research"
To solve this, I need to first answer:
```

**Model Output:**
```
"What is the last letter of 'artificial'?" Then: "What is the last
letter of 'intelligence'?" Then: "What is the last letter of
'research'?" Then concatenate them all.
```

**Stage 2 -- Sequential Solving:**

**Sub-question 1:** What is the last letter of "artificial"? -> "l"
**Sub-question 2 (with A1):** What is the last letter of "intelligence"? -> "e"
**Sub-question 3 (with A1, A2):** What is the last letter of "research"? -> "h"
**Final (with A1, A2, A3):** Concatenate "l", "e", "h" -> "leh"

## When to Use

- The problem naturally decomposes into ordered sub-problems of increasing difficulty.
- Standard CoT fails on harder instances despite succeeding on simpler ones.
- The task requires compositional generalization beyond exemplar complexity.
- Sub-problems have clear dependencies (each builds on prior answers).
- You need to handle variable-length reasoning chains that may be longer than any exemplar.
- The task involves symbolic manipulation, multi-step computation, or compositional commands.

## When to Avoid

- The problem is simple enough to solve in a single reasoning chain.
- Sub-problems are independent and do not form a sequential dependency chain (consider parallel decomposition instead).
- Latency is critical, as the sequential nature prevents full parallelization.
- The decomposition itself is harder than solving the problem directly.
- Token budget cannot accommodate the cumulative context growth across sub-problems.

## Cost & Performance

| Dimension          | Rating   | Notes                                           |
|--------------------|----------|-------------------------------------------------|
| Token overhead     | High     | Cumulative context growth across sub-problems    |
| Latency            | High     | Sequential calls; not parallelizable             |
| Accuracy gain      | High     | Large gains on compositional/hard problems       |
| Implementation     | Medium   | Requires decomposition + solving prompt design   |
| Model requirements | Large    | Benefits most at 100B+ parameter scale           |

## Variants

- **Iterative Least-to-Most**: Rather than decomposing all sub-problems upfront, generate and solve one sub-problem at a time, deciding the next sub-problem based on accumulated context.
- **Least-to-Most with Self-Consistency**: Apply majority voting at each sub-problem level to increase reliability of intermediate answers.
- **Adaptive Decomposition**: Vary the granularity of decomposition based on problem complexity -- simple problems get fewer sub-problems.
- **Recursive Least-to-Most**: If a sub-problem is itself complex, recursively decompose it further before solving.

## Composability

Least-to-Most is fundamentally a decomposition framework that can incorporate various solving strategies:

- **L2M + CoT**: Use Chain-of-Thought prompting to solve each sub-problem. This is the standard approach in the original paper. See `chain-of-thought.md`.
- **L2M + Self-Consistency**: Apply Self-Consistency at each sub-problem for more reliable intermediate answers, reducing error propagation. See `self-consistency.md`.
- **L2M + Self-Ask**: Self-Ask can be viewed as a special case of L2M where the model dynamically generates follow-up questions rather than decomposing upfront. See `self-ask.md`.
- **L2M + ReAct**: When sub-problems require external information, use ReAct-style tool calls within each sub-problem's solving step. See `react.md`.

## Limitations

- **Decomposition quality**: The technique is only as good as the decomposition. Poor decomposition can lead to irrelevant sub-problems or missed dependencies.
- **Error propagation**: Errors in early sub-problems propagate through the chain since later sub-problems depend on earlier answers. There is no built-in error correction.
- **Context window pressure**: As sub-problems accumulate, the context grows, potentially exceeding the model's context window for problems with many sub-parts.
- **Sequential bottleneck**: Unlike Self-Consistency, L2M cannot be parallelized because each step depends on the previous one, making it inherently slower.
- **Decomposition overhead**: The two-stage process requires designing exemplars for both decomposition and solving, increasing the prompt engineering effort.
- **Not always better than CoT**: For problems within the complexity range of the exemplars, standard CoT may match or exceed L2M at lower cost.

## Sources

- Zhou, D., Scharli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui, C., Bousquet, O., Le, Q. V., & Chi, E. (2022). Least-to-Most Prompting Enables Complex Reasoning in Large Language Models. *ICLR 2023*. https://arxiv.org/abs/2205.10625
- Drozdov, A., Scharli, N., Akyurek, E., Scales, N., Song, X., Chen, X., Bousquet, O., & Zhou, D. (2022). Compositional Semantic Parsing with Large Language Models. https://arxiv.org/abs/2209.15003
- Khot, T., Trivedi, H., Finlayson, M., Fu, Y., Richardson, K., Clark, P., & Sabharwal, A. (2022). Decomposed Prompting: A Modular Approach for Solving Complex Tasks. https://arxiv.org/abs/2210.02406
