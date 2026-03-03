---
id: buffer-of-thoughts
name: "Buffer of Thoughts"
aliases:
  - BoT
  - Thought Buffer
  - Meta-Buffer Reasoning
category: reasoning
family: thought-generation
year: 2024
authors:
  - Ling Yang
  - Zhaochen Yu
  - Tianjun Zhang
  - Shiyi Cao
  - Minkai Xu
  - Wentao Zhang
  - Joseph E. Gonzalez
  - Bin Cui
paper: "https://arxiv.org/abs/2406.04271"
paper_title: "Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models"
venue: "NeurIPS 2024 Spotlight"
code: "https://github.com/YangLing0818/buffer-of-thought-llm"
complexity: medium
token_cost: medium
latency: medium
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - mathematical reasoning
  - multi-step logic puzzles
  - game-theoretic problems (Game of 24, etc.)
  - tasks with recurring problem structures
  - benchmarks with diverse problem types
  - situations where few-shot exemplars are unavailable
avoid_when:
  - completely novel problem types with no structural precedent
  - simple single-step tasks
  - latency-critical one-off queries
  - tasks where the meta-buffer cannot be maintained
composes_with:
  - chain-of-thought
  - self-consistency
  - tree-of-thoughts
  - retrieval-augmented-generation
tags:
  - meta-reasoning
  - thought-templates
  - reusable-patterns
  - knowledge-distillation
  - efficiency
  - structured-reasoning
---

# Buffer of Thoughts

> **One-line summary:** Maintains a library of reusable high-level "thought templates" (a meta-buffer) that the model retrieves and instantiates to solve new problems, boosting accuracy and efficiency over single-query reasoning.

## Overview

Buffer of Thoughts (BoT), introduced by Yang et al. (2024) and recognized as a NeurIPS 2024 Spotlight paper, addresses a key inefficiency in existing prompting methods: every new query forces the model to reason from scratch, even when structurally similar problems have been solved before. BoT introduces the concept of a *meta-buffer* -- a persistent, growing library of distilled thought templates extracted from previously solved problems. When a new problem arrives, the system retrieves the most relevant thought template from the meta-buffer and instantiates it with the specific details of the new problem, enabling structured, high-quality reasoning without redundant cognitive work.

The technique draws inspiration from how expert problem-solvers approach new challenges: rather than deriving solutions from first principles each time, experts recognize structural patterns and apply known solution frameworks adapted to the specifics at hand. A mathematician recognizes a problem as a "constraint satisfaction" type and immediately activates the relevant mental schema. BoT operationalizes this insight by having the LLM first distill its reasoning on solved problems into abstract, reusable templates (e.g., "for problems involving X, decompose into sub-steps A, B, C with verification at each stage"), then retrieve and apply these templates to new problems.

Empirically, BoT achieves significant improvements across a range of benchmarks including Game of 24, Checkmate-in-One, and multiple math reasoning datasets. It matches or exceeds the performance of multi-query methods like Tree of Thoughts while requiring only a single LLM call per problem at inference time (after the meta-buffer is populated). The meta-buffer also grows over time, making the system progressively better as it encounters and distills more problem types. This combination of improved accuracy, single-call efficiency, and continual improvement makes BoT a compelling framework for production reasoning systems.

## How It Works

1. **Problem distillation (offline/incremental)**: For a set of seed problems, the LLM solves each one using detailed reasoning. The system then extracts and abstracts the reasoning pattern into a high-level *thought template* -- a structured schema describing the type of problem, the reasoning strategy, key sub-steps, and verification criteria.
2. **Meta-buffer storage**: Thought templates are stored in a meta-buffer (a structured knowledge base), indexed by problem type, domain, and key structural features for efficient retrieval.
3. **Template retrieval**: When a new problem arrives, the system analyzes its structure and retrieves the most relevant thought template from the meta-buffer using similarity matching on problem features.
4. **Template instantiation**: The retrieved thought template is instantiated with the specific values, constraints, and context of the new problem, producing a concrete reasoning plan.
5. **Reasoning execution**: The LLM follows the instantiated template to solve the problem, generating a structured reasoning trace that adheres to the template's prescribed steps and verification points.
6. **Buffer update (optional)**: If the solved problem reveals a new pattern not well-covered by existing templates, a new thought template is distilled and added to the meta-buffer, enabling continual improvement.

### Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        META-BUFFER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Template A   │  │  Template B   │  │  Template C   │  ...    │
│  │  "Constraint  │  │  "Optimize    │  │  "Combinat-   │         │
│  │   Satisfact." │  │   via bounds" │  │   orial enum" │         │
│  └──────┬───────┘  └──────────────┘  └──────────────┘           │
│         │  best match                                             │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────────┐
│  NEW PROBLEM ──► Analyze Structure ──► Retrieve Template A       │
│                                                                   │
│  Instantiate Template A with problem-specific values:             │
│    - Variables: {x=3, y=7, constraint=sum<20}                    │
│    - Sub-steps: [define vars, apply constraint, verify, solve]   │
│                                                                   │
│  Execute reasoning following instantiated template                │
│                                                                   │
│  ──► ANSWER + (optionally) distill new template if novel         │
└──────────────────────────────────────────────────────────────────┘
```

## Template

```
You have access to a library of thought templates for different problem types.

## Thought Template Library:
{meta_buffer_templates}

## Task:
1. Analyze the following problem and identify which thought template best applies.
2. Retrieve the matching template and instantiate it with the problem's specifics.
3. Follow the instantiated template step by step to solve the problem.
4. Verify your answer against the template's verification criteria.

Problem: {problem}

## Solution:
Selected template: [identify template]
Instantiation: [fill template with specifics]
Reasoning: [follow instantiated steps]
Verification: [apply checks]
Answer:
```

## Examples

### Example 1: Game of 24 (Arithmetic Constraint Satisfaction)

**Meta-buffer template (pre-stored):**
```
Template: "Arithmetic Target Construction"
Problem type: Given N numbers and arithmetic operations, reach a target value.
Strategy:
  1. List all given numbers and the target.
  2. Enumerate promising pairwise operations (prioritize multiplication/division
     for creating larger/smaller intermediates).
  3. After each operation, record the remaining number set.
  4. Recursively apply operations until one number remains.
  5. Verify: confirm the final value equals the target and all input numbers
     were used exactly once.
```

**Input problem:**
```
Use the numbers 1, 5, 5, 5 with +, -, *, / to make 24.
```

**Instantiated reasoning:**
```
Selected template: "Arithmetic Target Construction"
Given numbers: {1, 5, 5, 5}, Target: 24

Step 1: Numbers = {1, 5, 5, 5}; Target = 24
Step 2: 24 = 4! suggests factorial-like structure. 5*(5-1) = 20, not 24.
        Try: 5*(5 - 1/5) = 5*(24/5) = 24. Check: uses 5,5,1,5 = all four.
Step 3: Verify: 1/5 = 0.2; 5 - 0.2 = 4.8; 5 * 4.8 = 24. Correct.
Step 4: All four numbers {1, 5, 5, 5} used exactly once. Target reached.

Answer: 5 * (5 - 1/5) = 24
```

### Example 2: Multi-Step Mathematical Reasoning

**Meta-buffer template (pre-stored):**
```
Template: "Sequential Quantity Tracking"
Problem type: Track quantities through a series of transformations.
Strategy:
  1. Identify the initial quantity and list all transformation events in order.
  2. For each event, determine the operation (add, subtract, multiply, scale).
  3. Apply operations sequentially, recording the intermediate state after each.
  4. State the final quantity.
  5. Verify by checking that each operation is accounted for and arithmetic
     is correct via reverse computation.
```

**Input problem:**
```
A warehouse has 1,200 widgets. On Monday, they ship 30% to Store A. On Tuesday,
they receive 450 new widgets. On Wednesday, they ship half of the current
inventory to Store B. How many widgets remain?
```

**Instantiated reasoning:**
```
Selected template: "Sequential Quantity Tracking"

Step 1: Initial = 1200 widgets. Events: ship 30%, receive 450, ship 50%.
Step 2: Monday: 1200 * 0.30 = 360 shipped; 1200 - 360 = 840 remaining.
Step 3: Tuesday: 840 + 450 = 1290 remaining.
Step 4: Wednesday: 1290 / 2 = 645 shipped; 1290 - 645 = 645 remaining.
Step 5: Verify reverse: 645 * 2 = 1290; 1290 - 450 = 840; 840 / 0.7 = 1200. Correct.

Answer: 645 widgets
```

## When to Use

- Tasks with recurring problem structures where patterns can be recognized and reused across problems.
- Benchmark settings or production systems that encounter many structurally similar problems over time.
- Mathematical reasoning, logic puzzles, and game-theoretic problems with well-defined solution schemas.
- Situations where high reasoning accuracy is needed but few-shot exemplars are impractical to provide per-query.
- Systems that can maintain persistent state (the meta-buffer) across interactions.
- Domains where expert problem-solving strategies can be articulated as abstract templates.

## When to Avoid

- Completely novel problem types with no structural precedent in the meta-buffer.
- Simple single-step tasks where template retrieval overhead exceeds the reasoning benefit.
- One-off, latency-critical queries where the overhead of template matching is not justified.
- Systems without persistent state management capability to maintain the meta-buffer.
- Highly creative or open-ended tasks where rigid templates constrain useful divergent thinking.

## Cost & Performance

| Metric                 | Value                     | Notes                                              |
|------------------------|---------------------------|----------------------------------------------------|
| Token overhead         | ~1.5x direct, ~0.8x ToT  | Template context adds tokens but reduces reasoning  |
| Latency                | Medium                    | Single LLM call at inference after buffer populated |
| Game of 24 accuracy    | 82%+ (Llama3-70B)        | Significant improvement over CoT baseline            |
| Math reasoning gain    | +5-15% over CoT           | Larger gains on structured, pattern-rich tasks       |
| Calls per problem      | 1 (inference)             | vs. Tree of Thoughts which requires many calls       |
| Buffer maintenance     | Low (incremental)         | New templates added as novel patterns emerge          |

## Variants

- **Static BoT:** The meta-buffer is pre-populated once and never updated. Simpler to deploy but does not improve over time.
- **Dynamic BoT:** The meta-buffer grows continuously as new problem types are encountered and distilled. Enables lifelong learning.
- **Hierarchical BoT:** Templates are organized in a hierarchy (domain > problem type > variant), enabling coarse-to-fine retrieval for better matching.
- **BoT-Lite:** Instead of a separate retrieval step, the meta-buffer is included directly in the system prompt as a reference library. Simpler but limited by context window size.
- **Multi-Template BoT:** Retrieve the top-K templates and let the model select the best one or combine elements from multiple templates for hybrid problems.

## Composability

- **BoT + Self-Consistency:** Instantiate the same template multiple times with slight variations in reasoning path, then vote on the answer. Templates provide structural consistency while sampling provides robustness.
- **BoT + Chain-of-Thought:** Use CoT as the reasoning executor within each instantiated template step, combining the structural guidance of BoT with the detailed reasoning of CoT.
- **BoT + Tree-of-Thoughts:** Use templates to define the branching structure of the thought tree, constraining exploration to productive paths while still allowing branching at decision points.
- **BoT + RAG:** Retrieve relevant factual information to populate template variables, combining structural reasoning patterns with grounded external knowledge.
- **BoT + Verification:** After template-guided reasoning, apply a separate verification pass to confirm the answer satisfies all problem constraints.

## Limitations

- Requires initial investment to populate the meta-buffer with high-quality thought templates, either through manual curation or automated distillation from solved examples.
- Template retrieval quality depends heavily on the similarity metric and problem representation; poor matching leads to applying inappropriate reasoning schemas.
- Fixed templates may be too rigid for problems that blend multiple types or require novel reasoning approaches not captured in existing templates.
- The meta-buffer can grow unwieldy over time if not curated, leading to retrieval noise and template redundancy.
- Models may over-rely on retrieved templates even when the match is imperfect, forcing a problem into an ill-fitting schema rather than reasoning flexibly.
- Distilling high-quality abstract templates requires the model to generalize well from specific solutions to abstract patterns, which is itself a challenging reasoning task.
- The technique is relatively new with fewer independent replications across diverse tasks and models compared to established methods like CoT.

## Sources

- **Primary:** Yang, L., Yu, Z., Zhang, T., Cao, S., Xu, M., Zhang, W., Gonzalez, J. E., & Cui, B. (2024). Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models. *NeurIPS 2024 Spotlight*. https://arxiv.org/abs/2406.04271
- **Related:** Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *NeurIPS 2023*. https://arxiv.org/abs/2305.10601
- **Related:** Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
