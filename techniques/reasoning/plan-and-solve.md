---
id: plan-and-solve
name: "Plan-and-Solve Prompting"
aliases:
  - PS
  - PS+
  - plan and solve
  - PS+ prompting
category: reasoning
family: decomposition
year: 2023
authors:
  - Lei Wang
  - Wanyu Xu
  - Yihuai Lan
  - Zhiqiang Hu
  - Yunshi Lan
  - Roy Ka-Wei Lee
  - Ee-Peng Lim
paper: "https://arxiv.org/abs/2305.04091"
paper_title: "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models"
venue: "ACL 2023"
code: "https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting"
complexity: medium
token_cost: medium
latency: medium
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - multi-step math word problems
  - zero-shot reasoning improvement
  - tasks where Zero-Shot CoT produces calculation errors
  - structured problem solving
  - tasks requiring explicit variable tracking
  - reducing missing-step errors in reasoning
avoid_when:
  - simple single-step questions
  - tasks where few-shot CoT is feasible and preferred
  - creative or open-ended generation
  - tasks without clear planning structure
composes_with:
  - self-consistency
  - zero-shot-cot
  - chain-of-thought
  - least-to-most
tags:
  - decomposition
  - reasoning
  - zero-shot
  - planning
  - prompting
  - variable-extraction
---

# Plan-and-Solve Prompting

> **One-line summary:** Improve zero-shot reasoning by instructing the model to first devise a step-by-step plan, then execute it with explicit variable extraction and calculation verification.

## Overview

Plan-and-Solve (PS) Prompting, introduced by Wang et al. (2023), is an evolution of Zero-Shot Chain-of-Thought that addresses three critical failure modes: calculation errors, missing-step errors, and semantic misunderstanding errors. While "Let's think step by step" effectively triggers reasoning, the resulting chains often skip steps, make arithmetic mistakes, or misinterpret quantities in the problem. PS prompting replaces the generic trigger with a structured directive that instructs the model to first devise a plan and then carry it out.

The basic PS prompt appends "Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step" to the question. The enhanced variant, PS+, adds three additional instructions: (1) extract relevant variables and their values, (2) calculate intermediate results explicitly, and (3) state what quantity needs to be computed. These additions constrain the model's reasoning to be more methodical and less prone to skipping critical steps or making arithmetic mistakes.

PS+ achieves performance competitive with or superior to few-shot CoT on several benchmarks, all without requiring any exemplars. On GSM8K, PS+ with GPT-3.5 scored 58.7% compared to Zero-Shot CoT's 52.9% and Manual-CoT's 58.4%. This is significant because it means high-quality reasoning can be elicited zero-shot, dramatically reducing the prompt engineering effort required. The technique is particularly effective on math word problems (GSM8K, AQuA, SVAMP, MultiArith) where the structured plan-then-execute approach naturally fits the problem structure and prevents the most common error types.

## How It Works

1. **Understand the problem**: The model reads the problem and identifies what is being asked.
2. **Extract variables**: (PS+ only) The model explicitly lists the relevant quantities and their values from the problem statement.
3. **Devise a plan**: The model outlines a step-by-step plan for solving the problem before performing any calculations.
4. **Execute the plan**: The model follows its own plan, performing calculations and reasoning at each step.
5. **State the final answer**: After executing all plan steps, the model states the computed answer explicitly.

### Diagram

```
+----------------------------------------------+
|                 INPUT                        |
|  Q: {problem}                                |
|                                              |
|  Let's first understand the problem and      |
|  devise a plan to solve it. Then, let's      |
|  carry out the plan to solve the problem     |
|  step by step.                               |
+------------------+---------------------------+
                   |
                   v
+----------------------------------------------+
|           MODEL OUTPUT (PS+)                 |
|                                              |
|  1. UNDERSTAND:                              |
|     - Identify what we need to find          |
|                                              |
|  2. EXTRACT VARIABLES:                       |
|     - var1 = value1                          |
|     - var2 = value2                          |
|                                              |
|  3. PLAN:                                    |
|     Step 1: Calculate X using var1           |
|     Step 2: Calculate Y using X and var2     |
|     Step 3: Compute final answer from Y      |
|                                              |
|  4. EXECUTE:                                 |
|     Step 1: X = ... = result1                |
|     Step 2: Y = ... = result2                |
|     Step 3: Answer = ... = final             |
|                                              |
|  The answer is: {final}                      |
+----------------------------------------------+
```

## Template

### Basic PS Prompt

```
Q: {question}

Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step.
```

### Enhanced PS+ Prompt

```
Q: {question}

Let's first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and target what is being asked), and solve the problem step by step.
```

## Examples

### Example 1: Multi-Step Math Problem

**PS+ Prompt:**
```
Q: A bookstore sells novels for $12 each and textbooks for $45 each.
On Monday, they sold 15 novels and 8 textbooks. On Tuesday, they sold
22 novels and 5 textbooks. What was their total revenue for both days?

Let's first understand the problem, extract relevant variables and
their corresponding numerals, and devise a complete plan. Then, let's
carry out the plan, calculate intermediate variables (pay attention to
correct numerical calculation and target what is being asked), and
solve the problem step by step.
```

**Model Output:**
```
Understanding: We need to find the total revenue from selling novels
and textbooks over two days.

Variables:
- Price of novel = $12
- Price of textbook = $45
- Monday novels sold = 15
- Monday textbooks sold = 8
- Tuesday novels sold = 22
- Tuesday textbooks sold = 5

Plan:
Step 1: Calculate Monday's novel revenue
Step 2: Calculate Monday's textbook revenue
Step 3: Calculate Monday's total revenue
Step 4: Calculate Tuesday's novel revenue
Step 5: Calculate Tuesday's textbook revenue
Step 6: Calculate Tuesday's total revenue
Step 7: Calculate total revenue for both days

Execution:
Step 1: Monday novel revenue = 15 * $12 = $180
Step 2: Monday textbook revenue = 8 * $45 = $360
Step 3: Monday total = $180 + $360 = $540
Step 4: Tuesday novel revenue = 22 * $12 = $264
Step 5: Tuesday textbook revenue = 5 * $45 = $225
Step 6: Tuesday total = $264 + $225 = $489
Step 7: Total revenue = $540 + $489 = $1,029

The answer is $1,029.
```

### Example 2: Rate and Proportion Problem

**PS+ Prompt:**
```
Q: A factory produces 240 widgets per hour with 6 machines running.
If 2 machines break down, how many widgets will the factory produce
in a 10-hour shift?

Let's first understand the problem, extract relevant variables and
their corresponding numerals, and devise a complete plan. Then, let's
carry out the plan, calculate intermediate variables (pay attention to
correct numerical calculation and target what is being asked), and
solve the problem step by step.
```

**Model Output:**
```
Understanding: We need to find the total production over 10 hours
with reduced machine capacity.

Variables:
- Normal production rate = 240 widgets/hour
- Normal number of machines = 6
- Machines that break down = 2
- Shift duration = 10 hours

Plan:
Step 1: Calculate production rate per machine
Step 2: Calculate number of working machines after breakdown
Step 3: Calculate new hourly production rate
Step 4: Calculate total production over the shift

Execution:
Step 1: Rate per machine = 240 / 6 = 40 widgets per machine per hour
Step 2: Working machines = 6 - 2 = 4 machines
Step 3: New hourly rate = 4 * 40 = 160 widgets per hour
Step 4: Total production = 160 * 10 = 1,600 widgets

The answer is 1,600 widgets.
```

## When to Use

- You want zero-shot reasoning that is more reliable than "Let's think step by step."
- Math word problems and quantitative reasoning tasks are the primary use case.
- You want the model to explicitly show variable extraction and a plan before solving.
- You do not have few-shot exemplars or want to avoid the effort of constructing them.
- Tasks where Zero-Shot CoT produces calculation errors or skips intermediate steps.
- You need structured, auditable reasoning with a clear plan-execution separation.

## When to Avoid

- You have well-curated few-shot CoT exemplars that outperform zero-shot methods.
- The task has no natural planning structure (e.g., sentiment classification, simple retrieval).
- The problem is trivially simple and planning would add unnecessary overhead.
- Open-ended creative tasks where rigid planning constrains generation quality.
- The problem domain is non-quantitative where variable extraction does not apply.

## Cost & Performance

| Dimension          | Rating    | Notes                                          |
|--------------------|-----------|-------------------------------------------------|
| Token overhead     | Medium    | More than basic CoT due to plan + execute phases |
| Latency            | Medium    | Single call; longer generation than Zero-Shot CoT|
| Accuracy gain      | High      | Matches or beats few-shot CoT on math benchmarks  |
| Implementation     | Very Low  | Just a prompt modification; no exemplars needed    |
| Model requirements | Large     | Best at 100B+ scale; moderate gains at 10B+        |

## Variants

- **PS (basic)**: "Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step."
- **PS+**: Adds explicit variable extraction, intermediate calculation focus, and target identification to the basic PS prompt.
- **PS+ with verification**: Extends PS+ by adding "Verify each calculation step before proceeding to the next" to catch arithmetic errors inline.
- **Domain-adapted PS+**: Customize the planning instruction for specific domains (e.g., "First, draw a free body diagram" for physics, "First, identify the chemical species" for chemistry).
- **PS+ with few-shot**: Combine the PS+ instruction with few-shot exemplars that demonstrate the plan-then-execute format for maximum guidance.

## Composability

Plan-and-Solve naturally extends other reasoning techniques:

- **PS+ + Self-Consistency**: Sample multiple PS+ reasoning chains and majority vote. The structured planning reduces variance across samples, making voting more effective. See `self-consistency.md`.
- **PS+ + Least-to-Most**: PS+ can serve as the solving strategy within each sub-problem of a Least-to-Most decomposition. See `least-to-most.md`.
- **PS+ + CoT**: Combine PS+ planning instructions with few-shot CoT exemplars that demonstrate the plan-then-execute format for maximum guidance. See `chain-of-thought.md`.
- **PS+ + Verification**: Add a verification step after plan execution to check the answer against the plan and problem constraints.

## Limitations

- **Planning overhead for simple problems**: For straightforward single-step problems, the explicit planning phase wastes tokens without benefit.
- **Plan fidelity**: The model may generate a plan but then deviate from it during execution, especially on harder problems where the plan proves insufficient.
- **Limited to plannable tasks**: Not all tasks have a natural sequential plan structure. Abstract reasoning, analogy, and creative tasks may not benefit.
- **Variable extraction errors**: If the model misidentifies variables or assigns wrong values during extraction, the entire solution is compromised from the start.
- **Single attempt**: Like basic CoT, a single PS+ chain can still err. Combining with Self-Consistency is recommended for important tasks.
- **Prompt length**: The PS+ instruction is substantially longer than "Let's think step by step," consuming more of the context window for the instruction itself.

## Sources

- Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R. K.-W., & Lim, E.-P. (2023). Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models. *ACL 2023*. https://arxiv.org/abs/2305.04091
- Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large Language Models are Zero-Shot Reasoners. *NeurIPS 2022*. https://arxiv.org/abs/2205.11916
