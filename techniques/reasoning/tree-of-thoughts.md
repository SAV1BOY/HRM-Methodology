---
id: tree-of-thoughts
name: Tree of Thoughts
aliases:
  - ToT
  - tree-of-thought
  - thought tree
category: reasoning
family: thought-structure
year: 2023
authors:
  - Shunyu Yao
  - Dian Yu
  - Jeffrey Zhao
  - Izhak Shafran
  - Thomas L. Griffiths
  - Yuan Cao
  - Karthik Narasimhan
paper: https://arxiv.org/abs/2305.10601
paper_title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
venue: NeurIPS 2023
code: https://github.com/princeton-nlp/tree-of-thought-llm
complexity: high
token_cost: high
latency: high
num_calls: variable
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - creative writing tasks with constraints
  - puzzle solving (24 game, crosswords)
  - planning problems requiring exploration
  - tasks where backtracking is essential
  - problems with large but prunable search spaces
avoid_when:
  - straightforward reasoning tasks solvable by CoT
  - latency-sensitive applications
  - budget-constrained scenarios
  - tasks without meaningful intermediate states to evaluate
composes_with:
  - chain-of-thought
  - zero-shot-cot
  - self-consistency
  - react
tags:
  - search
  - reasoning
  - exploration
  - backtracking
  - deliberate-planning
---

# Tree of Thoughts

> Enable deliberate problem solving by exploring multiple reasoning paths as a tree structure, using self-evaluation to guide BFS or DFS search with backtracking.

## Overview

Tree of Thoughts (ToT), introduced by Yao et al. (2023), generalizes Chain-of-Thought prompting from a single linear reasoning chain into a tree-structured exploration of multiple reasoning paths. Inspired by classical AI search algorithms and dual-process theory from cognitive science, ToT frames problem solving as a search over a tree where each node represents a partial solution (a "thought") and branches represent different continuation choices. The model itself serves as both the generator of candidate thoughts and the evaluator that assesses their promise.

The key innovation of ToT is the introduction of deliberate planning into language model reasoning. While CoT and Self-Consistency generate reasoning chains in a purely forward fashion, ToT allows the model to consider multiple alternatives at each step, evaluate their viability, and backtrack from unpromising paths. This is analogous to how a chess player considers several moves ahead, evaluates board positions, and abandons losing lines of play. The deliberate exploration enables ToT to solve problems that require strategic thinking, constraint satisfaction, or creative search.

ToT is implemented using two classical search algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS). In BFS mode, the system maintains a set of the most promising partial solutions at each depth level, expanding all of them before moving deeper. In DFS mode, the system explores one path deeply, backtracking when the evaluator determines the current path is unlikely to succeed. The choice between BFS and DFS depends on the problem structure: BFS works well when the branching factor is manageable and evaluation is reliable; DFS is better when solutions are deep and early pruning is effective. ToT demonstrated dramatic improvements on tasks like the Game of 24 (from 4% with CoT to 74% with ToT) and creative writing with constraints.

## How It Works

1. **Define thought decomposition**: Determine how to decompose the problem into sequential intermediate thought steps. Each thought should be small enough to evaluate but large enough to be meaningful.
2. **Generate candidate thoughts**: At each step, use the LLM to generate k candidate next thoughts (continuations of the current partial solution).
3. **Evaluate thoughts**: Use the LLM to evaluate each candidate thought, either by assigning a value (e.g., "sure/maybe/impossible") or by voting among candidates.
4. **Search**: Use BFS or DFS to navigate the thought tree:
   - **BFS**: Maintain the top-b candidates at each level; expand all of them to the next level.
   - **DFS**: Explore the most promising branch depth-first; backtrack when evaluation indicates failure.
5. **Termination**: Return the solution when a complete, satisfactory answer is found at a leaf node, or return the best partial solution if the search budget is exhausted.

### Diagram

```
                        [Problem]
                       /    |    \
                      /     |     \
                   [T1a]  [T1b]  [T1c]     <- Level 1: Generate & Evaluate
                   /   \    |      X        <- T1c pruned ("impossible")
                  /     \   |
              [T2a]  [T2b] [T2c]            <- Level 2: Generate & Evaluate
                X      |     |              <- T2a pruned
                       |     |
                    [T3a]  [T3b]            <- Level 3: Generate & Evaluate
                      |      X              <- T3b pruned
                      |
                  [Solution]                <- Complete answer found

    Legend:
    [Txy] = Thought at level x, candidate y
      X   = Pruned by self-evaluation
      |   = Expanded (promising path)
```

## Template

### Thought Generation Prompt

```
Given the problem: {problem}

Current state: {current_partial_solution}

Generate {k} distinct possible next steps to continue solving this problem. For each, provide a brief description.

Possible next steps:
1.
2.
3.
```

### Thought Evaluation Prompt (Value-based)

```
Given the problem: {problem}

Current state: {current_partial_solution}

Proposed next step: {candidate_thought}

Evaluate whether this step is likely to lead to a correct solution. Respond with one of:
- "sure" (definitely on the right track)
- "maybe" (uncertain but worth exploring)
- "impossible" (this path cannot lead to a solution)

Evaluation:
```

## Examples

### Example 1: Game of 24

**Problem:** Use the numbers 4, 5, 6, 10 and basic arithmetic (+, -, *, /) to make 24.

**Level 1 -- Generate 3 candidate first operations:**
```
Current: 4, 5, 6, 10
Candidate 1a: 10 - 4 = 6  -> remaining: 5, 6, 6
Candidate 1b: 5 * 4 = 20  -> remaining: 6, 10, 20
Candidate 1c: 10 - 6 = 4  -> remaining: 4, 4, 5
```

**Level 1 -- Evaluate:**
```
1a (5, 6, 6): Can we make 24? 6*(6-5)=6, 5+6+6=17, 6*6-5=31... "maybe"
1b (6, 10, 20): Can we make 24? 20+10-6=24! -> "sure"
1c (4, 4, 5): Can we make 24? 4*5+4=24! -> "sure"
```

**Level 2 -- Expand 1b (6, 10, 20):**
```
Candidate 2a: 20 + 10 = 30 -> remaining: 6, 30
Candidate 2b: 20 - 10 = 10 -> remaining: 6, 10
Candidate 2c: 20 + 6 = 26  -> remaining: 10, 26
```

**Level 2 -- Evaluate:**
```
2a (6, 30): 30 - 6 = 24 -> "sure"
```

**Solution found:** 5 * 4 = 20, 20 + 10 = 30, 30 - 6 = 24.

### Example 2: Constrained Creative Writing

**Problem:** Write a 4-line poem where each line starts with one of the letters C, O, D, E (in order) and the poem is about the ocean.

**Level 1 -- Generate candidate first lines (starting with C):**
```
Candidate 1a: "Crashing waves upon the shore"
Candidate 1b: "Calm and endless, blue expanse"
Candidate 1c: "Currents pull beneath the tide"
```

**Level 1 -- Evaluate (vote):**
All are valid starting lines. Vote: 1c is most evocative and sets up a strong rhyme.

**Level 2 -- Generate second lines (starting with O) given chosen first line:**
```
Candidate 2a: "Over depths where secrets hide"
Candidate 2b: "Ocean whispers, far and wide"
Candidate 2c: "Only moonlight as a guide"
```

**Level 2 -- Evaluate:** 2a rhymes with "tide" and maintains underwater theme. "sure"

**Level 3 -- Generate third line (starting with D):**
```
Candidate 3a: "Dancing light on sandy floor"
Candidate 3b: "Deep below, the creatures glide"
```

**Evaluate:** 3b maintains the rhyme scheme (glide/hide/tide). "sure"

**Level 4 -- Generate fourth line (starting with E):**
```
"Endless blue, the ocean's pride"
```

**Final poem:**
```
Currents pull beneath the tide
Over depths where secrets hide
Deep below, the creatures glide
Endless blue, the ocean's pride
```

## When to Use

- The problem has a combinatorial or exploratory nature (puzzles, games, planning).
- Backtracking is important because wrong initial choices lead to dead ends.
- The problem has meaningful intermediate states that can be evaluated for promise.
- Standard CoT or Self-Consistency fails due to the need for strategic exploration.
- The quality of the solution justifies the high computational cost.

## When to Avoid

- The problem can be solved reliably by a single CoT chain or Self-Consistency.
- Token budget or latency constraints prohibit dozens of LLM calls.
- The problem lacks meaningful intermediate evaluation criteria.
- The thought space is too large to explore even with pruning.
- Real-time or near-real-time response is required.

## Cost & Performance

| Dimension          | Rating     | Notes                                           |
|---------------------|------------|-------------------------------------------------|
| Token overhead      | Very High  | 10-100+ LLM calls per problem                    |
| Latency             | Very High  | Sequential depth * parallel breadth calls         |
| Accuracy gain       | Very High  | +70% on Game of 24; dramatic on puzzle tasks      |
| Implementation      | High       | Requires search infrastructure + prompt design    |
| Model requirements  | Large      | Needs strong self-evaluation capabilities          |

## Variants

- **ToT-BFS**: Breadth-first variant that maintains top-b candidates at each level. Better when evaluation is reliable and the branching factor is low.
- **ToT-DFS**: Depth-first variant with backtracking. Better when solutions are deep and early pruning is effective.
- **Monte Carlo ToT**: Combine ToT with Monte Carlo Tree Search (MCTS) for more sophisticated exploration-exploitation tradeoffs using UCB-style scoring.
- **Prompt-based ToT**: A simplified single-prompt version that instructs the model to "explore multiple approaches" without external search infrastructure. Lower cost but less effective.
- **ToT with heuristic evaluation**: Replace LLM-based evaluation with domain-specific heuristics for faster and cheaper pruning.

## Composability

ToT is a meta-framework that can incorporate other techniques at each node:

- **ToT + CoT**: Each "thought" in the tree is generated using Chain-of-Thought reasoning. This is the default in the original paper.
- **ToT + Self-Consistency**: Use Self-Consistency at the evaluation step (sample multiple evaluations and vote) to improve evaluation reliability.
- **ToT + Zero-Shot CoT**: Use zero-shot CoT as the thought generator to avoid exemplar dependence within each node.
- **ToT + ReAct**: Extend ToT nodes to include tool-use actions, allowing the search tree to explore different tool-use strategies.
- **ToT + Graph-of-Thoughts**: GoT generalizes ToT by allowing nodes to merge, creating a DAG structure rather than a pure tree.

## Limitations

- **Computational cost**: The primary limitation is the enormous computational overhead. A single problem may require 50-100+ LLM calls, making ToT impractical for high-throughput applications.
- **Evaluation reliability**: ToT's effectiveness depends critically on the quality of self-evaluation. If the model cannot reliably distinguish promising from unpromising paths, the search becomes inefficient or explores wrong branches.
- **Thought decomposition design**: The granularity of "thoughts" must be carefully chosen per task. Too coarse and the tree lacks useful branching points; too fine and the search space explodes.
- **Problem structure dependence**: ToT shines on problems with clear intermediate states and evaluation criteria (puzzles, constrained generation) but offers little benefit on tasks without these properties.
- **Search budget sensitivity**: The choice of branching factor (k), beam width (b), and maximum depth significantly affect both cost and performance. These hyperparameters require per-task tuning.

## Sources

- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *NeurIPS 2023*. https://arxiv.org/abs/2305.10601
- Long, J. (2023). Large Language Model Guided Tree-of-Thought. https://arxiv.org/abs/2305.08291
- Hao, S., Gu, Y., Ma, H., Hong, J. J., Wang, Z., Wang, D. Z., & Hu, Z. (2023). Reasoning with Language Model is Planning with World Model. https://arxiv.org/abs/2305.14992
