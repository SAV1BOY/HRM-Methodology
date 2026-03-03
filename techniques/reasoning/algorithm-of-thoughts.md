---
id: algorithm-of-thoughts
name: "Algorithm of Thoughts"
aliases:
  - AoT
  - Algorithm-of-Thoughts
  - DFS Reasoning
category: reasoning
family: thought-generation
year: 2023
authors:
  - Bilgehan Sel
  - Ahmad Al-Tawaha
  - Vanshaj Khattar
  - Lu Wang
  - Ruoxi Jia
  - Ming Jin
paper: "https://arxiv.org/abs/2308.10379"
paper_title: "Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models"
venue: "Preprint 2023"
code: null
complexity: medium
token_cost: medium
latency: medium
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - problems requiring exploration of multiple solution paths
  - puzzles and constraint satisfaction (Game of 24, Sudoku)
  - tasks where Tree of Thoughts is too expensive
  - search-like reasoning in a single generation
  - problems with clear branching and backtracking structure
  - creative problem solving with dead-end elimination
avoid_when:
  - simple linear reasoning tasks
  - problems with a single clear solution path
  - tasks where exhaustive exploration is unnecessary
  - very short or factual questions
  - latency-critical applications needing minimal generation
composes_with:
  - chain-of-thought
  - self-consistency
  - tree-of-thoughts
  - few-shot-prompting
tags:
  - search-algorithm
  - depth-first-search
  - exploration
  - backtracking
  - single-call
  - efficiency
  - tree-search
---

# Algorithm of Thoughts

> **One-line summary:** Embeds depth-first-search-like algorithmic exploration within a single LLM call, enabling systematic idea exploration with backtracking while avoiding the multi-call overhead of Tree of Thoughts.

## Overview

Algorithm of Thoughts (AoT), introduced by Sel et al. (2023), bridges the gap between the simplicity of chain-of-thought (a single linear reasoning path) and the power of tree-of-thoughts (multi-path exploration with evaluation and backtracking). The key insight is that LLMs, trained on vast corpora that include algorithmic problem-solving content, can internalize search algorithms like depth-first search (DFS) and execute them *within a single generation*. Instead of requiring an external orchestrator to manage multiple LLM calls for branching, evaluation, and backtracking (as ToT does), AoT teaches the model to perform this exploration natively.

The technique works by structuring the prompt to demonstrate DFS-like behavior: exploring a promising path, recognizing when it hits a dead end, backtracking to a previous decision point, and trying an alternative path. The few-shot exemplars show the model how to maintain a mental stack of decision points, how to evaluate whether a current path is viable, and how to systematically abandon unpromising directions. This produces a single, coherent generation that contains the entire exploration trace -- including abandoned branches -- ultimately arriving at a solution.

AoT is particularly compelling because it achieves performance comparable to Tree of Thoughts on benchmarks like the Game of 24 while using only a single LLM call instead of dozens. This represents a dramatic reduction in API costs and latency. The tradeoff is that AoT relies on the model's ability to faithfully execute the search algorithm internally, which requires sufficiently capable models and well-crafted exemplars. On simpler models, the search behavior may degrade to superficial backtracking without genuine exploration. Nevertheless, for capable models, AoT demonstrates that algorithmic thinking can be elicited through prompting alone, without external orchestration infrastructure.

## How It Works

1. **Problem framing**: Present the problem along with few-shot exemplars that demonstrate DFS-like exploration behavior: trying a path, evaluating it, backtracking when stuck, and exploring alternatives.
2. **Path exploration**: The model begins exploring a promising solution path, making a sequence of decisions.
3. **Viability evaluation**: At each step, the model evaluates whether the current partial solution can lead to a valid complete solution. This mirrors the "pruning" step in tree search.
4. **Backtracking**: When the model determines that a path is unviable (dead end), it explicitly backtracks to a previous decision point and tries an alternative branch.
5. **Solution discovery**: The exploration continues with branching and backtracking until the model finds a valid solution path or exhausts the search space.
6. **Answer extraction**: The final valid solution is extracted from the exploration trace.

### Diagram

```
┌──────────────────────────────────────────────────────────────┐
│          DFS-LIKE EXPLORATION IN A SINGLE LLM CALL           │
│                                                               │
│  Start: Numbers = {4, 9, 10, 13}, Target = 24                │
│                                                               │
│  Path 1: Try 13 - 9 = 4                                      │
│    → Remaining: {4, 4, 10}                                    │
│    → Try 4 * 10 = 40... too large, no way to get 24          │
│    ✗ Dead end. Backtrack.                                     │
│                                                               │
│  Path 2: Try 10 - 4 = 6                                      │
│    → Remaining: {6, 9, 13}                                    │
│    → Try 13 - 9 = 4                                           │
│      → Remaining: {6, 4}                                      │
│      → 6 * 4 = 24 ✓ FOUND!                                   │
│                                                               │
│  Solution: (10 - 4) * (13 - 9) = 6 * 4 = 24                 │
└──────────────────────────────────────────────────────────────┘

Comparison:
  CoT:  ──────────────────────► (single path, may miss solution)
  ToT:  ═══╦═══╦═══╦═══        (multi-call branching, expensive)
            ╠   ╠   ╠
  AoT:  ───┬──✗ ┬──✓           (single call, internal branching)
            └────┘
```

## Template

```
Solve the following problem using a systematic search approach. Explore
promising paths. If a path leads to a dead end, explicitly backtrack and
try a different approach. Show your exploration process.

{few_shot_exemplar_with_dfs_behavior}

Problem: {problem}

Exploration:
```

### Detailed Template with DFS Instructions

```
Solve this problem by exploring solution paths like a depth-first search:
1. Start with a promising operation or decision.
2. After each step, evaluate: can this partial solution still reach the goal?
3. If yes, continue deeper.
4. If no (dead end), backtrack to the last decision point and try another option.
5. Continue until you find a valid solution.

Show all explored paths, including dead ends, using this format:
- "Trying: [operation]" to explore
- "→ Result: [state]" to show the new state
- "✗ Dead end: [reason]. Backtracking." to abandon a path
- "✓ Solution found!" when successful

{few_shot_examples}

Problem: {problem}

Exploration:
```

## Examples

### Example 1: Game of 24

**Input:**
```
Use +, -, *, / to make 24 from the given numbers. Use each number exactly once.
Explore paths systematically; backtrack from dead ends.

Example:
Numbers: 2, 3, 4, 8
Trying: 8 / 2 = 4 → Remaining: {4, 3, 4}
  Trying: 4 + 4 = 8 → Remaining: {8, 3}
    8 * 3 = 24 ✓ Solution: (8 / 2 + 4) * 3 = 24

Numbers: 1, 3, 8, 11
Exploration:
```

**Output:**
```
Trying: 11 - 8 = 3 → Remaining: {1, 3, 3}
  Trying: 3 * 3 = 9 → Remaining: {1, 9}
    1 + 9 = 10 ≠ 24. 1 * 9 = 9 ≠ 24. 9 - 1 = 8 ≠ 24.
  ✗ Dead end. Backtracking to {1, 3, 3}.
  Trying: 3 + 3 = 6 → Remaining: {1, 6}
    6 * 1 = 6 ≠ 24. 6 + 1 = 7 ≠ 24.
  ✗ Dead end. Backtracking to start.

Trying: 11 - 3 = 8 → Remaining: {1, 8, 8}
  Trying: 8 * 8 = 64 → Remaining: {1, 64}
    64 - 1 = 63 ≠ 24. Too large.
  ✗ Dead end. Backtracking to {1, 8, 8}.
  Trying: 8 + 8 = 16 → Remaining: {1, 16}
    16 + 1 = 17 ≠ 24.
  ✗ Dead end. Backtracking to start.

Trying: 8 * 3 = 24 → Remaining: {1, 11, 24}
  Need to get 24 using identity. 24 * 1 = 24, but 11 is unused.
  Trying: 11 - 1 = 10. Doesn't help.
  Trying: 1 * 11 = 11. Doesn't help.
  ✗ Dead end. Must use all numbers. Backtracking.

Trying: 8 * (11 - 3) = 8 * 8 = 64. Too large. Skip.
Trying: 8 / (11 - 3) = 8 / 8 = 1 → Remaining: {1, 1}
  1 + 1 = 2 ≠ 24. ✗ Dead end.

Trying: 3 * 8 * 1 = 24 → but 11 unused. Need 11 * 1 or 11 - 11 = 0.
Trying: (11 - 8) * (3 - 1) = 3 * 2 = 6. ≠ 24. ✗

Trying: (3 - 1) = 2. 8 * 2 = 16. 16 + 11 = 27. ✗
Trying: 3 * (1 + 8) = 27. 27 - 11 = 16. ✗
Trying: 3 * 11 = 33. 33 - 8 - 1 = 24. ✓ Solution found!

✓ Solution: 3 * 11 - 8 - 1 = 33 - 8 - 1 = 24
Verification: 3 * 11 = 33; 33 - 8 = 25; 25 - 1 = 24. All four numbers used. ✓
```

### Example 2: Constraint Satisfaction

**Input:**
```
Solve by exploring paths; backtrack from dead ends.

Problem: Place the numbers 1-4 in a 2x2 grid such that no two adjacent cells
(horizontally or vertically) have consecutive numbers.

Exploration:
```

**Output:**
```
Grid positions: [A1, A2, B1, B2]
Adjacencies: A1-A2 (horiz), B1-B2 (horiz), A1-B1 (vert), A2-B2 (vert)

Trying: A1 = 1
  Trying: A2 = 3 (skip 2, consecutive to 1)
    Trying: B1 = 3 → but A2=3 already. Try B1 = 4
      ✗ B1=4, A1=1: |4-1|=3, OK. B2 must be 2. Check: B2=2 adj to A2=3: |2-3|=1 consecutive.
    ✗ Dead end. Backtracking.
    Trying: B1 = 2 → |2-1|=1, consecutive to A1. ✗ Invalid. Backtrack.
  Trying: A2 = 4 (skip 2, consecutive to 1)
    Trying: B1 = 3. |3-1|=2, OK with A1. Remaining: B2 = 2.
      Check B2=2: adj to A2=4: |2-4|=2, OK. Adj to B1=3: |2-3|=1, consecutive. ✗
    Trying: B1 = 2. |2-1|=1, consecutive to A1. ✗ Invalid.
  ✗ Dead end for A1=1. Backtracking.

Trying: A1 = 2
  Trying: A2 = 4 (skip 3, consecutive to 2)
    Trying: B1 = 4 → already used. B1 = 1. |1-2|=1, consecutive to A1. ✗
    Trying: B1 = 3. |3-2|=1, consecutive to A1. ✗
  ✗ Dead end.

Trying: A1 = 3
  Trying: A2 = 1 (skip 2,4 consecutive to 3)
    Trying: B1 = 1 → already used. B1 = 2. |2-3|=1, consecutive to A1. ✗
  ✗ Dead end.

Trying: A1 = 1, A2 = 3, B1 = 4, B2 = 2:
  A1-A2: |1-3|=2 OK. B1-B2: |4-2|=2 OK. A1-B1: |1-4|=3 OK. A2-B2: |3-2|=1 ✗

Trying: A1 = 2, A2 = 4, B1 = 4... no, used.
Trying: A1 = 1, A2 = 4, B1 = 3, B2 = 2:
  A1-A2: |1-4|=3 OK. A1-B1: |1-3|=2 OK. A2-B2: |4-2|=2 OK. B1-B2: |3-2|=1 ✗

Trying: A1 = 3, A2 = 1, B1 = 1... used.
Trying: A1 = 2, A2 = 4, B1 = 4... no.

This puzzle may have no solution. After exhaustive DFS, all placements violate
the adjacency constraint. ✓ Answer: No valid arrangement exists.
```

## When to Use

- Puzzle-like problems requiring exploration of multiple solution paths (Game of 24, Sudoku, constraint satisfaction).
- Situations where Tree of Thoughts is effective but too expensive due to multiple API calls.
- Problems with a clear branching structure where dead ends can be recognized and abandoned.
- Creative problem-solving tasks that benefit from systematic exploration of alternatives.
- Settings where you want the reasoning trace to include the search process itself (failed attempts and corrections).
- Tasks where a single linear reasoning chain frequently gets stuck on suboptimal paths.

## When to Avoid

- Simple linear reasoning tasks where there is one clear solution path and no branching is needed.
- Factual retrieval or classification tasks where exploration adds no value.
- Very time-sensitive applications where the extended generation (including dead-end exploration) is too slow.
- Tasks where the model cannot reliably evaluate path viability, leading to either no pruning or incorrect pruning.
- Problems with extremely large search spaces where even DFS-style exploration within a single call is insufficient.

## Cost & Performance

| Metric              | Value                     | Notes                                             |
|---------------------|---------------------------|----------------------------------------------------|
| Token overhead       | ~2-4x vs CoT             | Exploration trace includes dead ends                |
| Latency              | Medium                    | Single call, but longer generation                   |
| API calls            | 1                         | vs ToT's 10-50+ calls per problem                    |
| Game of 24 accuracy  | ~78-85% (GPT-4)          | Comparable to ToT at ~74% with much lower cost       |
| Cost vs ToT          | ~10-50x cheaper           | Single call vs many calls with evaluations            |
| Implementation cost  | Low                       | Prompt engineering with DFS-style exemplars            |

## Variants

- **BFS-Style AoT:** Instead of depth-first exploration, structure the exploration breadth-first: evaluate all options at one level before going deeper. Better for problems where the first few decisions are most critical.
- **Bounded AoT:** Set an explicit limit on exploration depth or number of backtracks to prevent the model from generating excessively long exploration traces.
- **AoT + Heuristic Guidance:** Inject domain-specific heuristics into the prompt to guide the search toward more promising paths first, reducing the number of dead ends explored.
- **Iterative AoT:** If the first AoT call fails to find a solution (exhausts its exploration budget), provide the failed trace as context for a second call that explores different initial paths.
- **AoT with Pruning Rules:** Explicitly state pruning criteria in the prompt (e.g., "if the running total exceeds the target, backtrack immediately") to make evaluation more reliable.

## Composability

- **AoT + Self-Consistency:** Run multiple AoT explorations with different random seeds or initial paths, then take the solution that appears most frequently or passes verification.
- **AoT + Chain-of-Thought:** Use CoT for the evaluation step within each AoT branch, providing more rigorous viability assessment before deciding to continue or backtrack.
- **AoT + Tree-of-Thoughts:** Use AoT for the initial exploration in a single call, then selectively apply ToT's multi-call approach to refine the most promising paths identified by AoT.
- **AoT + Few-Shot Selection:** Dynamically select the most structurally similar exemplar from a library of AoT demonstrations based on the problem type.
- **AoT + Verification:** After AoT finds a solution, apply a separate verification prompt to confirm correctness, since the exploration process may contain errors.

## Limitations

- Relies on the model's ability to faithfully simulate DFS-like behavior, which requires capable models (GPT-4 level or above for reliable results).
- The exploration trace can become very long for problems with large search spaces, potentially exceeding the model's effective reasoning span.
- Models may perform "shallow" backtracking -- appearing to explore alternatives while actually making minimal changes from the previous path.
- The quality of pruning decisions depends heavily on the model's ability to evaluate partial solutions, which is not always reliable.
- Few-shot exemplars must carefully demonstrate the exploration and backtracking pattern; poorly designed exemplars lead to superficial search behavior.
- Unlike true tree search with external orchestration, AoT cannot guarantee completeness -- the model may miss valid solutions that it happened not to explore.
- The technique is less well-studied than CoT or ToT, with limited empirical results across diverse task categories.

## Sources

- **Primary:** Sel, B., Al-Tawaha, A., Khattar, V., Wang, L., Jia, R., & Jin, M. (2023). Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models. https://arxiv.org/abs/2308.10379
- **Related:** Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *NeurIPS 2023*. https://arxiv.org/abs/2305.10601
- **Related:** Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
