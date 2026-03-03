---
id: chain-of-thought
name: "Chain-of-Thought Prompting"
aliases:
  - CoT
  - few-shot CoT
  - chain of thought
category: reasoning
family: thought-generation
year: 2022
authors:
  - Jason Wei
  - Xuezhi Wang
  - Dale Schuurmans
  - Maarten Bosma
  - Brian Ichter
  - Fei Xia
  - Ed Chi
  - Quoc V. Le
  - Denny Zhou
paper: "https://arxiv.org/abs/2201.11903"
paper_title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
venue: "NeurIPS 2022"
code: null
complexity: low
token_cost: medium
latency: medium
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - arithmetic reasoning
  - commonsense reasoning
  - symbolic reasoning
  - multi-step problem solving
  - word problems
  - logical deduction
avoid_when:
  - simple factual recall
  - single-step tasks
  - latency-critical applications with tight token budgets
  - tasks with no clear sequential reasoning structure
composes_with:
  - self-consistency
  - least-to-most
  - self-ask
  - react
  - tree-of-thoughts
tags:
  - foundational
  - reasoning
  - few-shot
  - prompting
  - emergent-ability
---

# Chain-of-Thought Prompting

> **One-line summary:** Elicit multi-step reasoning in large language models by providing few-shot examples that include intermediate reasoning steps before the final answer.

## Overview

Chain-of-Thought (CoT) prompting is the foundational technique introduced by Wei et al. (2022) that dramatically improves the reasoning capabilities of large language models. Instead of prompting the model with input-output pairs alone, CoT augments each few-shot exemplar with a sequence of intermediate reasoning steps that lead to the final answer. This simple modification unlocks the ability of sufficiently large models to tackle complex, multi-step reasoning tasks that standard prompting fails on entirely.

The key insight behind CoT is that language models trained on large corpora have internalized reasoning patterns but need explicit demonstrations to activate them. By showing the model how to "think through" a problem step by step, the model learns to generate its own chain of reasoning for novel inputs. This is analogous to how a student benefits from seeing a teacher work through a problem on the board rather than just seeing the answer. The few-shot exemplars serve as a formatting guide that tells the model "show your work."

CoT prompting is particularly effective for tasks requiring arithmetic reasoning, commonsense reasoning, and symbolic manipulation. Importantly, the technique exhibits an emergent ability pattern: it provides substantial benefits only in models above a certain scale (roughly 100B+ parameters), while smaller models may produce fluent but logically incoherent reasoning chains. On the GSM8K benchmark, CoT improved PaLM 540B from 17.9% (standard prompting) to 56.9%, and on StrategyQA from 73.9% to 77.8%. This scale-dependence makes CoT a hallmark of emergent capabilities in large language models.

## How It Works

1. **Select representative examples**: Choose 3-8 exemplars from the target task that cover diverse problem types and difficulty levels.
2. **Annotate reasoning chains**: For each exemplar, write out the intermediate reasoning steps that lead from the question to the answer. Each step should be a logical, verifiable deduction.
3. **Format the prompt**: Present the exemplars as a sequence of (Question, Chain-of-Thought, Answer) triples in the prompt.
4. **Query the model**: Append the new question to the prompt and let the model generate its own chain of thought followed by the answer.
5. **Extract the answer**: Parse the final answer from the model's generated output, which follows its reasoning chain.

### Diagram

```
┌─────────────────────────────────────────────────┐
│                   PROMPT                        │
│                                                 │
│  Q1: [Example question 1]                       │
│  A1: [Step 1] -> [Step 2] -> ... -> [Answer 1]  │
│                                                 │
│  Q2: [Example question 2]                       │
│  A2: [Step 1] -> [Step 2] -> ... -> [Answer 2]  │
│                                                 │
│  Q3: [Example question 3]                       │
│  A3: [Step 1] -> [Step 2] -> ... -> [Answer 3]  │
│                                                 │
│  Q_new: [Test question]                         │
│  A_new:                                         │
├─────────────────────────────────────────────────┤
│               MODEL GENERATES                   │
│  [Step 1] -> [Step 2] -> ... -> [Final Answer]  │
└─────────────────────────────────────────────────┘
```

## Template

```
Solve the following problem step by step.

Q: {example_question_1}
A: {reasoning_step_1_for_example_1}. {reasoning_step_2_for_example_1}. {reasoning_step_3_for_example_1}. The answer is {answer_1}.

Q: {example_question_2}
A: {reasoning_step_1_for_example_2}. {reasoning_step_2_for_example_2}. {reasoning_step_3_for_example_2}. The answer is {answer_2}.

Q: {test_question}
A:
```

## Examples

### Example 1: Arithmetic Word Problem

**Prompt:**
```
Solve the following problem step by step.

Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can
has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. He bought 2 cans of 3 tennis balls each,
so he bought 2 * 3 = 6 tennis balls. Now he has 5 + 6 = 11 tennis balls.
The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought
6 more, how many apples do they have?
A: The cafeteria had 23 apples originally. They used 20 to make lunch, so
they had 23 - 20 = 3 apples. They bought 6 more, so they have 3 + 6 = 9.
The answer is 9.

Q: If there are 3 cars in the parking lot and 2 more cars arrive, then
1 car leaves, how many cars are in the parking lot?
A:
```

**Model Output:**
```
There are 3 cars originally. 2 more cars arrive, so there are 3 + 2 = 5
cars. 1 car leaves, so there are 5 - 1 = 4 cars in the parking lot.
The answer is 4.
```

### Example 2: Commonsense Reasoning

**Prompt:**
```
Answer the following questions with step-by-step reasoning.

Q: Would a peanut butter sandwich be safe for someone with a tree nut allergy?
A: Peanuts are legumes, not tree nuts. Tree nut allergies cover almonds,
cashews, walnuts, etc. However, cross-contamination is common in processing
facilities. While peanut butter itself does not contain tree nuts, many brands
are processed alongside tree nuts. Without certainty about the processing
environment, it may not be safe. The answer is: it depends on the specific
brand and processing conditions.

Q: Is it possible for a person born in January to have a birthday on
February 29th?
A:
```

**Model Output:**
```
February 29th only exists in leap years, occurring every 4 years. A person
born in January was born in January, not February. Their birthday is fixed
in January regardless of whether it is a leap year. February 29th is a
separate date entirely. The answer is: no, a person born in January cannot
have a birthday on February 29th.
```

## When to Use

- The task involves multiple reasoning steps (arithmetic, logic, planning).
- Standard few-shot prompting produces incorrect answers but the model has sufficient scale (100B+ parameters).
- You have high-quality exemplars with clear, annotatable reasoning paths.
- Interpretability of the model's reasoning process is important for debugging or trust.
- You need to verify the model's reasoning by inspecting intermediate steps.

## When to Avoid

- The task is simple factual retrieval or single-step classification.
- You are working with small models (under 10B parameters) where CoT may hurt performance.
- Token budget is extremely tight and the added reasoning tokens are prohibitive.
- The task does not have a clear sequential reasoning structure.
- You do not have exemplars to demonstrate the reasoning format (consider Zero-Shot CoT instead).

## Cost & Performance

| Dimension          | Rating  | Notes                                       |
|--------------------|---------|---------------------------------------------|
| Token overhead     | Medium  | 2-4x more tokens than standard few-shot     |
| Latency            | Medium  | Single call, but longer generation           |
| Accuracy gain      | High    | +10-30% on math/reasoning benchmarks         |
| Implementation     | Low     | Only requires prompt engineering              |
| Model requirements | Large   | Effective at 100B+ parameter scale            |

## Variants

- **Zero-Shot CoT**: Append "Let's think step by step" without exemplars (Kojima et al., 2022). See `zero-shot-cot.md`.
- **Auto-CoT**: Automatically generate chain-of-thought demonstrations using clustering and zero-shot CoT (Zhang et al., 2022).
- **Complex CoT**: Select exemplars with more complex (longer) reasoning chains, which tend to improve performance on harder tasks.
- **Contrastive CoT**: Include both correct and incorrect reasoning chains to help the model learn from mistakes.
- **Multimodal CoT**: Extend CoT to vision-language models by interleaving image descriptions in the reasoning chain.
- **Chain of Draft**: Compress each reasoning step to approximately five words for token efficiency. See `chain-of-draft.md`.

## Composability

Chain-of-Thought is one of the most composable techniques in the prompting toolkit:

- **CoT + Self-Consistency**: Sample multiple CoT paths and take the majority vote. This is the most common and effective composition, improving robustness significantly. See `self-consistency.md`.
- **CoT + Least-to-Most**: Use CoT within each sub-problem after decomposition. The decomposition provides structure while CoT handles individual reasoning steps. See `least-to-most.md`.
- **CoT + Self-Ask**: Generate sub-questions (Self-Ask) and answer each with CoT reasoning. See `self-ask.md`.
- **CoT + ReAct**: Interleave CoT reasoning with tool-use actions. The "Thought" step in ReAct is essentially a CoT step. See `react.md`.
- **CoT + Retrieval**: Augment the reasoning chain with retrieved facts to ground reasoning in evidence.

## Limitations

- **Scale dependence**: CoT only reliably improves performance in large models (100B+ parameters). Smaller models may generate plausible-sounding but incorrect reasoning chains.
- **Faithfulness**: The generated reasoning chain may not reflect the model's actual computation. The chain can be a post-hoc rationalization rather than a faithful trace of inference.
- **Exemplar sensitivity**: Performance can vary significantly based on the choice, ordering, and quality of the few-shot exemplars. Even the number of exemplars matters.
- **No self-correction**: A single CoT chain can go off-track early and propagate errors through subsequent steps. Self-consistency or verification techniques are needed to mitigate this.
- **Manual annotation**: Creating high-quality reasoning chain exemplars requires human effort and domain expertise.
- **Verbosity**: The model may generate unnecessarily long reasoning chains, consuming tokens without improving accuracy.

## Sources

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
- Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large Language Models are Zero-Shot Reasoners. *NeurIPS 2022*. https://arxiv.org/abs/2205.11916
- Zhang, Z., Zhang, A., Li, M., & Smola, A. (2022). Automatic Chain of Thought Prompting in Large Language Models. https://arxiv.org/abs/2210.03493
- Fu, Y., Peng, H., Sabharwal, A., Clark, P., & Khot, T. (2023). Complexity-Based Prompting for Multi-Step Reasoning. *ICLR 2023*. https://arxiv.org/abs/2210.00720
