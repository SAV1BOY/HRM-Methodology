---
id: promptbreeder
name: "PromptBreeder: Self-Referential Self-Improvement via Prompt Evolution"
aliases: ["PromptBreeder", "Prompt Breeder", "self-referential-evolution"]
category: optimization
family: evolutionary-optimization
year: 2023
authors: ["Chrisantha Fernando", "Dylan Banarse", "Henryk Michalewski", "Simon Osindero", "Tim Rocktäschel"]
paper: "https://arxiv.org/abs/2309.16797"
paper_title: "PromptBreeder: Self-Referential Self-Improvement Via Prompt Evolution"
venue: "arXiv preprint"
code: null
complexity: high
token_cost: high
latency: high
num_calls: variable
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for: ["open-ended prompt discovery", "tasks with non-obvious instruction strategies", "research exploration", "complex reasoning tasks"]
avoid_when: ["limited compute budget", "simple well-understood tasks", "need for interpretable optimization", "time-sensitive deployment"]
composes_with: ["chain-of-thought", "self-consistency", "few-shot-prompting"]
tags: ["optimization", "evolutionary", "self-referential", "meta-prompting", "mutation"]
---

# PromptBreeder: Self-Referential Self-Improvement via Prompt Evolution

> **One-line summary:** An evolutionary algorithm that co-evolves both task prompts and the mutation operators used to generate new prompts, enabling open-ended self-improvement of prompt strategies.

## Overview

PromptBreeder introduces a self-referential approach to prompt optimization inspired by biological evolution. Unlike standard evolutionary prompt methods that only evolve task prompts, PromptBreeder simultaneously evolves both the **task prompts** (which directly instruct the LLM on the task) and the **mutation prompts** (which instruct the LLM on *how to mutate* the task prompts). This two-level evolution creates a system capable of open-ended self-improvement, where the search strategy itself adapts over generations.

The method maintains a population of "units," each consisting of a task prompt paired with a mutation prompt. In each generation, mutation operators are applied to produce offspring. The key innovation is that the mutation operators themselves are subject to evolution -- a concept borrowed from self-referential systems in theoretical computer science. This prevents the optimization from getting stuck in local optima by continuously discovering new ways to explore the prompt space.

PromptBreeder was developed at Google DeepMind and demonstrated strong results across arithmetic reasoning, commonsense reasoning, and other benchmarks. It outperformed earlier methods like APE and often discovered surprising, non-intuitive prompts that humans would be unlikely to design manually. The approach is computationally expensive but reveals that LLMs can serve as their own prompt engineers when given the right evolutionary framework.

## How It Works

1. **Initialize Population**: Create an initial population of units, each containing a task prompt (TP) and a mutation prompt (MP). Task prompts are seeded from simple instructions; mutation prompts describe how to modify prompts.

2. **Evaluate Fitness**: Run each unit's task prompt on a batch of training examples and compute a fitness score (e.g., accuracy on the batch).

3. **Apply Mutation Operators**: For each unit, apply one of several mutation strategies:
   - **Direct Mutation**: Use the MP to generate a new TP (the LLM rewrites the task prompt guided by the mutation prompt).
   - **Estimation of Distribution (EDA) Mutation**: Generate a new TP conditioned on the best-performing TPs in the population.
   - **Hypermutation**: Use a "hyper-mutation prompt" to mutate the MP itself, creating a new mutation strategy.
   - **Lamarckian Mutation**: Feed a correct working-out from a training example back to improve the TP.
   - **Prompt Crossover**: Combine elements from two different TPs.
   - **Zero-order Hypermutation**: Generate entirely new MPs from the problem description.

4. **Selection**: Evaluate offspring fitness. Replace parent units with offspring if the offspring have higher fitness (binary tournament selection).

5. **Iterate**: Repeat for multiple generations until convergence or budget exhaustion.

6. **Select Best**: Return the highest-fitness task prompt from the final population.

### Diagram

```
Generation 0:
+------------------+    +------------------+    +------------------+
| Unit 1           |    | Unit 2           |    | Unit N           |
| TP: "Solve step  |    | TP: "Think about |    | TP: "Calculate   |
|      by step"    |    |      the problem"|    |      carefully"  |
| MP: "Make the    |    | MP: "Add more    |    | MP: "Simplify    |
|      prompt more |    |      detail to   |    |      the         |
|      specific"   |    |      the prompt" |    |      instruction"|
+--------+---------+    +--------+---------+    +--------+---------+
         |                       |                       |
    [Mutate TP using MP]   [Mutate TP using MP]    [Mutate TP using MP]
    [Maybe mutate MP too]  [Maybe mutate MP too]   [Maybe mutate MP too]
         |                       |                       |
         v                       v                       v
    [Evaluate Fitness]     [Evaluate Fitness]      [Evaluate Fitness]
         |                       |                       |
    [Selection: keep better of parent vs offspring]
         |
         v
Generation 1: ... (repeat)
```

## Template

```
--- Mutation Prompt (MP) applied to generate new Task Prompt ---

MUTATION INSTRUCTION: {mutation_prompt}

CURRENT TASK PROMPT: {current_task_prompt}

PROBLEM DESCRIPTION: {problem_description}

Generate an improved version of the CURRENT TASK PROMPT that would
help an AI solve the problem better. Only output the new prompt text.

IMPROVED TASK PROMPT:

--- Task Prompt (TP) applied to solve the problem ---

{evolved_task_prompt}

Q: {question}
A:

--- Hyper-mutation: evolving the mutation prompt itself ---

INSTRUCTION: {hyper_mutation_prompt}

CURRENT MUTATION PROMPT: {current_mutation_prompt}

Please summarize and improve the CURRENT MUTATION PROMPT.

IMPROVED MUTATION PROMPT:
```

## Examples

### Example 1: Arithmetic Reasoning (GSM8K)

**Task**: Evolve prompts for grade-school math word problems.

**Initial Population (Generation 0)**:
- Unit 1: TP="Solve this math problem step by step." / MP="Make the instruction more specific."
- Unit 2: TP="Think carefully about each step." / MP="Add examples of good reasoning."
- Unit 3: TP="Calculate the answer." / MP="Encourage breaking down the problem."

**After 25 Generations**:
- Best evolved TP: "Approach this problem by first identifying all the quantities mentioned and their relationships. Set up equations to represent these relationships. Solve the equations one variable at a time, showing your arithmetic clearly. Verify your answer by substituting back."
- Its MP had evolved to: "Transform the prompt to emphasize mathematical structure identification and verification steps."
- **Result**: Accuracy improved from 65% (best initial TP) to 78% on the evaluation set.

### Example 2: Commonsense Reasoning (StrategyQA)

**Task**: Evolve prompts for multi-hop yes/no questions requiring world knowledge.

**Initial Population (Generation 0)**:
- Unit 1: TP="Answer yes or no with reasoning." / MP="Add detail."
- Unit 2: TP="Think about this carefully." / MP="Make it more structured."

**After 20 Generations**:
- Best evolved TP: "Decompose this question into sub-questions. For each sub-question, state what you know to be true. Then combine your answers to reach a final yes or no conclusion. State your confidence level."
- Evolved MP: "Restructure prompts to require explicit decomposition and evidence gathering before reaching conclusions."
- **Result**: Accuracy improved from 71% to 82%, with the evolved prompts discovering a decomposition strategy without being explicitly seeded with one.

## When to Use

- You are exploring a novel task where optimal prompt strategies are unknown
- You have sufficient compute budget for hundreds of LLM evaluations
- You want to discover non-obvious, creative prompt strategies
- The task has a clear, automatable fitness metric
- You are conducting research on prompt optimization methods

## When to Avoid

- You have a tight compute budget or deployment timeline
- The task is well-understood with known effective prompt strategies
- You need interpretable, auditable optimization decisions
- A simpler method like APE or OPRO already achieves sufficient performance
- The evaluation metric is noisy or expensive to compute

## Cost & Performance

| Dimension          | Value                      | Notes                                         |
|---------------------|----------------------------|-----------------------------------------------|
| Population size     | 50-100 units typical       | Each unit = 1 task prompt + 1 mutation prompt |
| Generations         | 20-50                      | Convergence depends on task complexity        |
| LLM calls/gen      | 200-500                    | Evaluation + mutation calls                   |
| Total LLM calls    | 5,000-25,000               | Can be reduced with smaller populations       |
| Accuracy gain       | +5-15% over baselines      | Compared to hand-crafted or APE prompts       |
| Wall-clock time     | 4-24 hours                 | Depends on model speed and population size    |

## Variants

- **Standard PromptBreeder**: Full self-referential evolution with all mutation operators.
- **PromptBreeder-Lite**: Reduced population and mutation operators for faster convergence.
- **Without Hypermutation**: Evolves only task prompts (no mutation-prompt evolution) -- often a strong baseline.
- **EDA-only**: Uses only estimation-of-distribution mutation, generating new prompts conditioned on the best existing ones.

## Composability

- Can be combined with **Chain-of-Thought**: Evolve CoT-style prompts specifically.
- Works with **few-shot demonstrations**: Evolve the instruction prefix while keeping fixed demonstrations.
- Can feed into **DSPy**: Use PromptBreeder-discovered prompts as seeds for DSPy compilation.
- Complements **self-consistency**: Apply majority voting on top of the best evolved prompt.

## Limitations

- Very high computational cost -- thousands of LLM calls per optimization run
- Evolved prompts can be brittle and may not transfer across models
- The self-referential aspect, while theoretically elegant, adds complexity without always improving over simpler evolution
- No guarantee of convergence; population can cycle or degrade
- Difficult to reproduce exact results due to stochastic nature
- Evolved prompts are sometimes verbose or oddly phrased, making them hard to interpret

## Sources

- Fernando, C. et al. (2023). "PromptBreeder: Self-Referential Self-Improvement Via Prompt Evolution." *arXiv:2309.16797*. https://arxiv.org/abs/2309.16797
- Guo, Q. et al. (2023). "Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers." *arXiv:2309.08532*.
- Zhou, Y. et al. (2022). "Large Language Models Are Human-Level Prompt Engineers." *arXiv:2211.01910*.
