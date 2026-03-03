---
id: graph-of-thoughts
name: Graph of Thoughts
aliases:
  - GoT
  - graph-of-thought
  - thought graph
category: reasoning
family: thought-structure
year: 2023
authors:
  - Maciej Besta
  - Nils Blach
  - Ales Kubicek
  - Robert Gerstenberger
  - Michal Podstawski
  - Lukas Gianinazzi
  - Joanna Gajda
  - Tomasz Lehmann
  - Hubert Niewiadomski
  - Piotr Nyczyk
  - Torsten Hoefler
paper: https://arxiv.org/abs/2308.09687
paper_title: "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"
venue: arXiv 2023
code: https://github.com/spcl/graph-of-thoughts
complexity: high
token_cost: high
latency: high
num_calls: variable
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - tasks requiring merging partial solutions
  - sorting and set operations
  - document merging and synthesis
  - problems where independent sub-solutions need combination
  - tasks benefiting from iterative refinement of thoughts
avoid_when:
  - simple sequential reasoning tasks
  - budget-constrained applications
  - problems without natural merge operations
  - latency-critical applications
composes_with:
  - tree-of-thoughts
  - chain-of-thought
  - self-consistency
  - self-ask
tags:
  - search
  - reasoning
  - graph-structure
  - merge-refine
  - advanced
---

# Graph of Thoughts

> Model reasoning as an arbitrary directed graph where thoughts can be generated, evaluated, merged, and refined, enabling operations impossible in linear or tree structures.

## Overview

Graph of Thoughts (GoT), introduced by Besta et al. (2023), extends the paradigm of structured reasoning beyond chains (CoT) and trees (ToT) into arbitrary graph topologies. The fundamental insight is that human reasoning is not strictly linear or tree-shaped -- we often generate ideas independently, merge the best aspects of different ideas, refine previous thoughts based on new information, and loop back to reconsider earlier decisions. GoT captures these patterns by representing the reasoning process as a directed graph where nodes are thoughts (LLM-generated reasoning units) and edges represent dependencies between them.

The most significant new operation that GoT introduces beyond ToT is thought aggregation (merging). In a tree structure, branches can never recombine -- each path is independent. GoT allows multiple reasoning paths to converge at aggregation nodes, where the model synthesizes the best elements from several partial solutions into a superior combined solution. This is particularly valuable for tasks like sorting (merge independently sorted sublists), document synthesis (combine separately generated sections), and any problem where divide-and-conquer strategies benefit from a merge step.

GoT formalizes reasoning as a system with four fundamental operations: Generate (create new thoughts from existing ones), Aggregate (merge multiple thoughts into one), Refine (improve a thought in-place), and Evaluate (score a thought's quality). These operations compose to form arbitrary graph topologies, from simple chains to complex DAGs with feedback loops. The framework includes a Graph of Operations (GoO) abstraction that allows users to define the graph topology declaratively, and a Graph Reasoning State (GRS) that tracks the evolving state of all thoughts during execution. GoT demonstrated improvements over ToT on sorting, set intersection, keyword counting, and document merging tasks while often using fewer LLM calls.

## How It Works

1. **Define the graph topology**: Design a Graph of Operations (GoO) that specifies which thought operations to apply and in what order. This is the "blueprint" for the reasoning process.
2. **Generate initial thoughts**: Create the starting nodes of the graph by generating candidate thoughts (solutions or partial solutions) from the LLM.
3. **Transform thoughts**: Apply operations to thoughts according to the GoO:
   - **Generate**: Create new thoughts branching from existing ones.
   - **Aggregate**: Merge multiple thoughts into a single improved thought.
   - **Refine**: Iteratively improve a thought by asking the LLM to enhance it.
   - **Evaluate**: Score thoughts to determine which to keep, merge, or discard.
4. **Manage the graph state**: The Graph Reasoning State (GRS) tracks all thoughts, their scores, and their relationships as the graph evolves.
5. **Extract the final answer**: Select the best-scoring thought from the graph as the final output, or follow a designated path to the output node.

### Diagram

```
    [Input Problem]
     /     |     \
    v      v      v
  [T1]   [T2]   [T3]       <- Generate: 3 independent thoughts
   |       |       |
   v       v       v
  [T1']  [T2']  [T3']      <- Refine: improve each thought
    \      |      /
     \     |     /
      v    v    v
     [T_merged]             <- Aggregate: merge best aspects
          |
          v
     [T_refined]            <- Refine: polish merged result
          |
          v
     [Evaluate]             <- Evaluate: score final output
          |
          v
     [Final Answer]

    Key operations:
    Generate  = create new thought nodes
    Refine    = improve existing thought in-place
    Aggregate = merge multiple thoughts into one
    Evaluate  = score thought quality
```

## Template

### Generation Prompt

```
Given the problem: {problem}

Generate a solution approach. Think carefully and provide your answer.

Solution:
```

### Aggregation (Merge) Prompt

```
Given the problem: {problem}

Here are {n} candidate solutions:

Solution 1: {thought_1}
Solution 2: {thought_2}
Solution 3: {thought_3}

Combine the best elements of these solutions into a single improved solution. Take the strongest aspects of each and resolve any conflicts.

Merged solution:
```

### Refinement Prompt

```
Given the problem: {problem}

Current solution: {current_thought}

Review this solution for errors, omissions, or areas of improvement. Provide an improved version.

Improved solution:
```

### Evaluation Prompt

```
Given the problem: {problem}

Solution: {thought}

Rate this solution on a scale of 1-10, considering correctness, completeness, and quality. Explain your rating briefly.

Rating:
```

## Examples

### Example 1: Sorting via Merge

**Problem:** Sort the list [7, 2, 9, 1, 5, 3, 8, 4, 6] in ascending order.

**Phase 1 -- Generate (split into sub-problems):**
```
Sub-list A: [7, 2, 9]  -> Generate thought to sort -> [2, 7, 9]
Sub-list B: [1, 5, 3]  -> Generate thought to sort -> [1, 3, 5]
Sub-list C: [8, 4, 6]  -> Generate thought to sort -> [4, 6, 8]
```

**Phase 2 -- Aggregate (merge sorted sub-lists):**
```
Merge prompt: "Merge these sorted lists into one sorted list:
  List 1: [2, 7, 9]
  List 2: [1, 3, 5]
  List 3: [4, 6, 8]
Merged result: [1, 2, 3, 4, 5, 6, 7, 8, 9]"
```

**Phase 3 -- Evaluate:**
```
Is [1, 2, 3, 4, 5, 6, 7, 8, 9] correctly sorted? Yes. Score: 10/10.
```

**Final Answer:** [1, 2, 3, 4, 5, 6, 7, 8, 9]

This approach works because sorting sub-lists is easier (fewer elements, less chance of error) and merging sorted lists is a well-defined operation that LLMs handle reliably.

### Example 2: Document Synthesis

**Problem:** Synthesize three perspectives on renewable energy into a balanced summary.

**Phase 1 -- Generate (parallel):**
```
Thought 1 (Economic): "Renewable energy investment reached $500B globally..."
Thought 2 (Environmental): "Solar and wind reduce carbon emissions by..."
Thought 3 (Technological): "Battery storage costs fell 90% since 2010..."
```

**Phase 2 -- Aggregate:**
```
Merge prompt: Combine these three perspectives into a cohesive summary.
Merged thought: "Renewable energy is advancing on three fronts: economically
  ($500B in investment), environmentally (measurable emissions reduction),
  and technologically (90% cost drop in battery storage)..."
```

**Phase 3 -- Refine:** Improve for coherence and highlight tensions between perspectives.

**Phase 4 -- Evaluate:** Score: 9/10. Balanced, well-integrated.

## When to Use

- The task naturally involves merging or synthesizing independently generated content.
- Divide-and-conquer strategies would help but ToT cannot recombine branches.
- Iterative refinement of partial solutions is valuable.
- The problem has a natural graph structure (e.g., document sections, sorted sublists, multi-perspective analysis).
- You need more flexibility than tree-structured search provides.

## When to Avoid

- The task is simple enough for CoT or even ToT to handle effectively.
- The problem does not benefit from merging operations.
- Budget or latency constraints prohibit the many LLM calls required.
- The problem has a naturally linear or tree-shaped solution path.
- You lack the engineering infrastructure to implement graph-based orchestration.

## Cost & Performance

| Dimension          | Rating     | Notes                                             |
|---------------------|------------|---------------------------------------------------|
| Token overhead      | Very High  | Multiple generate + aggregate + refine calls       |
| Latency             | Very High  | Multi-phase pipeline; some phases parallelizable   |
| Accuracy gain       | High       | Significant on sorting (+62%), merging, synthesis   |
| Implementation      | Very High  | Requires graph orchestration framework              |
| Model requirements  | Large      | Needs strong instruction-following for merge/refine |

## Variants

- **GoT with fixed topology**: Pre-define the exact graph structure for a specific task type (e.g., always split into 3 parts, sort each, merge). Simplest to implement.
- **GoT with adaptive topology**: Dynamically adjust the graph structure based on intermediate results. More flexible but harder to implement.
- **GoT with feedback loops**: Allow refined thoughts to feed back into earlier stages for iterative improvement cycles.
- **Lightweight GoT**: Reduce the number of operations by combining generate-and-evaluate in a single prompt, or skipping refinement for simpler tasks.
- **GoT + MCTS**: Combine graph-based reasoning with Monte Carlo Tree Search for exploration in the graph space.

## Composability

GoT is designed as a generalization that subsumes simpler techniques:

- **GoT subsumes CoT**: A chain of thoughts is a degenerate graph with no branching or merging -- a simple path.
- **GoT subsumes ToT**: A tree is a graph without merge operations. GoT adds aggregation.
- **GoT + Self-Consistency**: Use Self-Consistency at the generation phase (sample multiple initial thoughts) and at the evaluation phase (vote on merged results).
- **GoT + CoT**: Use Chain-of-Thought reasoning within each node's generation and refinement operations.
- **GoT + ReAct**: Incorporate tool-use actions as special nodes in the graph, allowing thoughts to be grounded in retrieved or computed information.

## Limitations

- **Implementation complexity**: GoT requires significant engineering infrastructure to manage graph state and orchestrate operations.
- **Topology design burden**: Choosing the right graph topology for a task requires expertise. A poor topology wastes computation without improving results.
- **Merge quality dependence**: The aggregation operation is only as good as the LLM's ability to synthesize multiple inputs coherently.
- **Cost**: The additional merge and refine operations add cost beyond what ToT requires.
- **Limited empirical validation**: GoT was primarily evaluated on constrained tasks (sorting, set operations). Effectiveness on diverse reasoning tasks is less established.

## Sources

- Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Podstawski, M., Gianinazzi, L., Gajda, J., Lehmann, T., Niewiadomski, H., Nyczyk, P., & Hoefler, T. (2023). Graph of Thoughts: Solving Elaborate Problems with Large Language Models. https://arxiv.org/abs/2308.09687
- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *NeurIPS 2023*. https://arxiv.org/abs/2305.10601
- Lei, B., Lin, Z., Wang, P., Guha, A., & Li, L. (2023). Boosting Logical Reasoning in Large Language Models through a New Framework: The Graph of Thought. https://arxiv.org/abs/2308.08614
