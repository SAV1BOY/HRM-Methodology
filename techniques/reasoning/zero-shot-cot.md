---
id: zero-shot-cot
name: "Zero-Shot Chain-of-Thought"
aliases:
  - Zero-Shot CoT
  - "Let's think step by step"
  - 0-shot CoT
category: reasoning
family: thought-generation
year: 2022
authors:
  - Takeshi Kojima
  - Shixiang Shane Gu
  - Machel Reid
  - Yutaka Matsuo
  - Yusuke Iwasawa
paper: "https://arxiv.org/abs/2205.11916"
paper_title: "Large Language Models are Zero-Shot Reasoners"
venue: "NeurIPS 2022"
code: null
complexity: low
token_cost: medium
latency: medium
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - arithmetic reasoning without exemplars
  - quick reasoning improvements
  - general-purpose reasoning elicitation
  - prototyping before crafting few-shot examples
  - commonsense inference
  - rapid baseline establishment
avoid_when:
  - high-stakes tasks requiring maximum accuracy
  - domain-specific reasoning needing curated exemplars
  - small models under 10B parameters
  - tasks where few-shot CoT exemplars are readily available
composes_with:
  - self-consistency
  - plan-and-solve
  - tree-of-thoughts
  - react
tags:
  - foundational
  - reasoning
  - zero-shot
  - prompting
  - trigger-phrase
---

# Zero-Shot Chain-of-Thought

> **One-line summary:** Unlock step-by-step reasoning from large language models without any exemplars by simply appending "Let's think step by step" to the prompt.

## Overview

Zero-Shot Chain-of-Thought (Zero-Shot CoT) is a remarkably simple yet powerful technique discovered by Kojima et al. (2022). The core finding is that large language models already possess latent reasoning capabilities that can be activated with a single trigger phrase: "Let's think step by step." Unlike standard Chain-of-Thought prompting, which requires carefully crafted few-shot exemplars with reasoning chains, Zero-Shot CoT requires no examples at all, making it the most accessible reasoning enhancement technique available.

The discovery emerged from an investigation into whether the reasoning abilities unlocked by few-shot CoT were a property of the exemplars themselves or of the model's intrinsic capabilities. By testing various trigger phrases, the authors found that "Let's think step by step" consistently outperformed standard zero-shot prompting across a wide range of reasoning benchmarks. On MultiArith, Zero-Shot CoT improved InstructGPT accuracy from 17.7% to 78.7%, and on GSM8K it went from 12.5% to 40.7%. This suggests that large models have internalized reasoning patterns from their training data and simply need a nudge to deploy them.

Zero-Shot CoT uses a two-stage process: first, the trigger phrase elicits a reasoning chain, and then a second prompt extracts the final answer from that chain. While it does not match the performance of well-crafted few-shot CoT on most benchmarks, it provides a strong baseline that requires zero human effort in exemplar construction. This makes it an ideal starting point for any reasoning task and a critical building block for more sophisticated techniques like Self-Consistency and Plan-and-Solve.

## How It Works

1. **Append trigger phrase**: Add "Let's think step by step" (or a similar reasoning trigger) to the end of the original question or instruction.
2. **Generate reasoning chain**: The model produces a step-by-step reasoning chain in response to the augmented prompt.
3. **Extract answer (Stage 2)**: Optionally, send a second prompt that includes the generated reasoning and asks the model to extract the final answer in a specific format (e.g., "Therefore, the answer is ___").
4. **Parse the final answer**: Extract the structured answer from the second-stage output.

### Diagram

```
                    STAGE 1                          STAGE 2
┌──────────────────────────────┐   ┌──────────────────────────────┐
│                              │   │                              │
│  Q: {question}               │   │  Q: {question}               │
│                              │   │                              │
│  A: Let's think step by     │   │  A: {generated_reasoning}    │
│     step.                    │   │                              │
│                              │   │  Therefore, the answer       │
│  ──── Model Generates ────  │   │  (number/choice) is:         │
│                              │   │                              │
│  {reasoning_chain}           │   │  ──── Model Generates ────  │
│                              │   │                              │
└──────────────┬───────────────┘   │  {final_answer}              │
               │                   │                              │
               └──────────────────>└──────────────────────────────┘
```

## Template

### Stage 1: Reasoning Elicitation

```
Q: {question}

A: Let's think step by step.
```

### Stage 2: Answer Extraction

```
Q: {question}

A: Let's think step by step.
{generated_reasoning_from_stage_1}

Therefore, the answer is:
```

### Single-Pass Variant

```
Q: {question}

Think step by step and then provide your final answer after "####".

A: Let's think step by step.
```

## Examples

### Example 1: Multi-Step Arithmetic

**Stage 1 Prompt:**
```
Q: A store had 45 books. They sold 12 on Monday, 8 on Tuesday, and then
received a shipment of 30 books on Wednesday. How many books does the
store have now?

A: Let's think step by step.
```

**Stage 1 Model Output:**
```
The store started with 45 books.
On Monday, they sold 12 books: 45 - 12 = 33 books.
On Tuesday, they sold 8 books: 33 - 8 = 25 books.
On Wednesday, they received 30 books: 25 + 30 = 55 books.
So the store now has 55 books.
```

**Stage 2 Prompt:**
```
Q: A store had 45 books. They sold 12 on Monday, 8 on Tuesday, and then
received a shipment of 30 books on Wednesday. How many books does the
store have now?

A: Let's think step by step. The store started with 45 books. On Monday,
they sold 12 books: 45 - 12 = 33 books. On Tuesday, they sold 8 books:
33 - 8 = 25 books. On Wednesday, they received 30 books: 25 + 30 = 55 books.
So the store now has 55 books.

Therefore, the answer (arabic numerals) is:
```

**Stage 2 Model Output:**
```
55
```

### Example 2: Logical Reasoning

**Stage 1 Prompt:**
```
Q: All roses are flowers. Some flowers fade quickly. Can we conclude that
some roses fade quickly?

A: Let's think step by step.
```

**Stage 1 Model Output:**
```
We know that all roses are flowers. This means roses are a subset of flowers.
We also know that some flowers fade quickly. This tells us there exist
flowers that fade quickly.
However, the flowers that fade quickly might not include any roses. The
"some flowers" that fade quickly could be entirely non-rose flowers like
daisies or tulips.
Since we cannot guarantee that the quickly-fading flowers overlap with
roses, we cannot logically conclude that some roses fade quickly.
This is a classic syllogistic fallacy known as the fallacy of the
undistributed middle.
```

**Stage 2 Prompt:**
```
Q: All roses are flowers. Some flowers fade quickly. Can we conclude that
some roses fade quickly?

A: Let's think step by step. [reasoning from above]

Therefore, the answer is:
```

**Stage 2 Model Output:**
```
No, we cannot conclude that some roses fade quickly. This is an invalid
syllogistic inference.
```

## When to Use

- You need a quick reasoning boost without investing time in exemplar construction.
- You are prototyping a solution and want to evaluate baseline reasoning quality before crafting few-shot examples.
- The task is general-purpose and does not require domain-specific exemplars.
- You are working with a large model (100B+ parameters) and want the simplest possible intervention.
- You want to combine with Self-Consistency (multiple zero-shot CoT samples with majority vote).
- You need to establish a reasoning baseline for comparison against more sophisticated techniques.

## When to Avoid

- You have high-quality few-shot exemplars available; few-shot CoT typically outperforms zero-shot CoT by 10-20%.
- The task requires domain-specific reasoning patterns that the model may not generate spontaneously.
- You are using smaller models where the trigger phrase may not reliably elicit structured reasoning.
- Token budget is very tight and the two-stage process is too costly.
- The task is simple enough that direct answering is sufficient.

## Cost & Performance

| Dimension          | Rating    | Notes                                          |
|--------------------|-----------|-------------------------------------------------|
| Token overhead     | Medium    | 2-4x more tokens than direct answering           |
| Latency            | Medium    | 1-2 calls (with optional answer extraction)      |
| Accuracy gain      | Moderate  | +5-20% on reasoning tasks; less than few-shot CoT|
| Implementation     | Very Low  | Single phrase addition to prompt                  |
| Model requirements | Large     | Best results at 100B+ parameters                  |

## Variants

- **"Let's work this out in a step by step way to be sure we have the right answer"**: An optimized trigger phrase found by Zhou et al. (2022) in the APE (Automatic Prompt Engineer) work, sometimes outperforming the original.
- **"Take a deep breath and work on this problem step-by-step"**: Another effective trigger phrase discovered through optimization, notably used by Google in PaLM 2 evaluations.
- **Role-based triggers**: Prefixing with "You are a brilliant mathematician." or similar role-setting before the trigger phrase to prime domain expertise.
- **Structured Zero-Shot CoT**: Adding formatting instructions like "Number each step" or "Show your work in a table" to constrain the reasoning format.

## Composability

Zero-Shot CoT serves as a lightweight drop-in reasoning enhancer for many techniques:

- **Zero-Shot CoT + Self-Consistency**: Sample multiple zero-shot CoT chains and take the majority vote. This is extremely effective and requires no exemplars at all. See `self-consistency.md`.
- **Zero-Shot CoT + Plan-and-Solve**: Plan-and-Solve extends zero-shot CoT by first generating an explicit plan, then executing it. PS+ adds variable extraction and calculation verification. See `plan-and-solve.md`.
- **Zero-Shot CoT + Tree-of-Thoughts**: Use zero-shot CoT as the thought generator within each node of the tree, with self-evaluation to prune branches. See `tree-of-thoughts.md`.
- **Zero-Shot CoT + ReAct**: The "Thought" component in ReAct can use zero-shot CoT reasoning before deciding on an action. See `react.md`.

## Limitations

- **Lower ceiling than few-shot CoT**: Without exemplars to guide the reasoning format and style, zero-shot CoT typically produces less consistent and sometimes less accurate chains.
- **Trigger phrase sensitivity**: Performance varies across different trigger phrases, and the optimal phrase may differ by task and model.
- **Error propagation**: A single reasoning chain can accumulate errors step by step with no correction mechanism. Self-consistency mitigates this.
- **Verbosity variation**: The model may produce overly verbose or overly terse reasoning depending on the question, making answer extraction harder.
- **Language and cultural bias**: The trigger phrase effectiveness has been primarily studied in English. Effectiveness may vary across languages.
- **Harmful reasoning risk**: On sensitive topics, eliciting step-by-step reasoning can produce more convincingly wrong or harmful outputs.

## Sources

- Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large Language Models are Zero-Shot Reasoners. *NeurIPS 2022*. https://arxiv.org/abs/2205.11916
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
- Zhou, Y., Muresanu, A. I., Han, Z., Paster, K., Pitis, S., Chan, H., & Ba, J. (2022). Large Language Models Are Human-Level Prompt Engineers. *ICLR 2023*. https://arxiv.org/abs/2211.01910
