---
id: thought-propagation
name: "Thought Propagation"
aliases: ["TP", "Analogous Problem Solving"]
category: advanced-reasoning
family: thought-structure
year: 2023
authors: ["Junchi Yu", "Ran He", "Rex Ying"]
paper: "https://arxiv.org/abs/2310.03965"
paper_title: "Thought Propagation: An Analogous Approach to Complex Reasoning with Large Language Models"
venue: "arXiv 2023"
code: null

complexity: high
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["complex multi-step reasoning", "graph-based problems", "shortest path problems", "problems with analogous sub-structures", "tasks benefiting from transfer of reasoning patterns"]
avoid_when: ["simple factual questions", "unique problems with no analogues", "token-constrained environments", "low-latency requirements", "problems with no structural similarity to other instances"]
composes_with: ["chain-of-thought", "tree-of-thoughts", "self-consistency", "self-refine"]

tags: ["analogical-reasoning", "thought-structure", "problem-decomposition", "graph-reasoning", "transfer"]
---

# Thought Propagation

> **One-line summary:** Thought Propagation solves complex problems by first identifying and solving analogous simpler problems, then propagating those solution strategies to the original problem.

## Overview

Thought Propagation (TP) draws on the human cognitive strategy of analogical reasoning: when faced with a difficult problem, we often recall similar problems we have already solved and adapt those solutions. In the LLM context, TP first prompts the model to generate a set of analogous problems that share structural similarities with the input problem, solves those analogous problems, and then uses those solutions as reasoning scaffolds to tackle the original challenge.

The key insight is that complex problems often contain sub-structures or patterns that appear in simpler variants. By explicitly constructing and solving these simpler analogues, the LLM builds up a library of reasoning strategies that can be composed or adapted. This is particularly powerful for graph-based reasoning tasks such as shortest-path computation, where the structure of the problem naturally decomposes into smaller, analogous subproblems.

Unlike Tree-of-Thoughts or Graph-of-Thoughts, which explore different reasoning branches for the same problem, Thought Propagation explores different but related problems. This cross-problem exploration surfaces reasoning patterns that might not emerge from single-problem exploration alone, effectively allowing the model to "learn" within the prompt context by building experience across analogous instances.

## How It Works

1. **Analogous Problem Generation:** Given the input problem, the LLM is prompted to generate a set of structurally similar but potentially simpler problems. These analogues preserve key features of the original while varying complexity or specific parameters.

2. **Analogous Problem Solving:** Each generated analogous problem is solved independently, typically using Chain-of-Thought reasoning. The solutions include detailed reasoning traces that capture the strategies employed.

3. **Solution Propagation:** The solutions and reasoning strategies from the analogous problems are collected and presented to the LLM alongside the original problem. The model is instructed to identify which strategies transfer and how to adapt them.

4. **Final Synthesis:** The LLM applies the propagated strategies to solve the original problem, using the analogous solutions as templates and adapting them to account for differences in the original problem's specifics.

5. **Optional Refinement:** If the initial solution is unsatisfactory, the model can generate additional analogues or refine the propagation step.

### Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 Thought Propagation Pipeline                 │
│                                                             │
│  ┌────────────┐                                             │
│  │  Original   │                                             │
│  │  Problem P  │──────┬──────────────────────────────┐       │
│  └────────────┘      │                              │       │
│                      v                              │       │
│            ┌──────────────────┐                      │       │
│            │ Generate Analogous│                      │       │
│            │ Problems          │                      │       │
│            └────────┬─────────┘                      │       │
│         ┌───────────┼───────────┐                    │       │
│         v           v           v                    │       │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐              │       │
│    │ Solve   │ │ Solve   │ │ Solve   │              │       │
│    │ P_a1    │ │ P_a2    │ │ P_a3    │              │       │
│    └────┬────┘ └────┬────┘ └────┬────┘              │       │
│         │           │           │                    │       │
│         v           v           v                    v       │
│    ┌──────────────────────────────────────────────────────┐  │
│    │        Propagate Solutions to Original Problem        │  │
│    │   (adapt strategies from analogues to solve P)       │  │
│    └──────────────────────────┬───────────────────────────┘  │
│                               v                              │
│                        ┌─────────────┐                       │
│                        │ Final Answer│                       │
│                        └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Template

```
You are solving a complex problem by first exploring analogous problems.

ORIGINAL PROBLEM:
{original_problem}

STEP 1 — Generate Analogous Problems:
Think of {num_analogues} problems that are structurally similar to the
original but potentially simpler. They should share key features (e.g.,
same type of reasoning, similar structure) but differ in specific details.

STEP 2 — Solve Each Analogue:
For each analogous problem, solve it step by step, explaining your
reasoning strategy clearly.

STEP 3 — Propagate Solutions:
Now examine the strategies you used for the analogous problems.
Identify which strategies apply to the original problem and how
they need to be adapted.

STEP 4 — Solve the Original:
Apply the propagated strategies to solve the original problem.
Show your work and explain how each analogous solution informed
your approach.

Final Answer:
```

## Examples

### Example 1: Graph Shortest Path

**Input:**
```
ORIGINAL PROBLEM:
Find the shortest path from node A to node F in the following graph:
A-B: 4, A-C: 2, B-D: 5, C-D: 1, C-E: 7, D-F: 3, E-F: 2

STEP 1 — Generate Analogous Problems:
Think of 2 simpler problems structurally similar to this shortest path
problem.

STEP 2 — Solve each analogue.
STEP 3 — Propagate solutions.
STEP 4 — Solve the original.
```

**Output:**
```
STEP 1 — Analogous Problems:

Analogue 1: Find shortest path A→D in subgraph A-B: 4, A-C: 2, B-D: 5, C-D: 1
Analogue 2: Find shortest path D→F in subgraph D-F: 3, D-E: (via C-E: 7 minus
C-D: 1 is not direct)... Simpler: D-F: 3, E-F: 2, D-E: 8

STEP 2 — Solving Analogues:

Analogue 1 (A→D):
  Path A→B→D = 4 + 5 = 9
  Path A→C→D = 2 + 1 = 3  ← shortest
  Strategy: Going through C is much cheaper than through B.

Analogue 2 (D→F):
  Path D→F = 3 (direct)  ← shortest
  Strategy: Direct path wins when available.

STEP 3 — Propagation:
From Analogue 1: Route through C to D is optimal (cost 3).
From Analogue 2: Direct D→F costs 3.
Combining: A→C→D→F might be strong (2 + 1 + 3 = 6).

STEP 4 — Solve Original:
Candidate paths:
  A→B→D→F = 4 + 5 + 3 = 12
  A→C→D→F = 2 + 1 + 3 = 6  ← informed by propagation
  A→C→E→F = 2 + 7 + 2 = 11

Final Answer: A → C → D → F with total cost 6.
```

### Example 2: Combinatorial Optimization

**Input:**
```
ORIGINAL PROBLEM:
A delivery driver must visit 5 locations (L1-L5) starting and ending at
the depot (D). Distances: D-L1:10, D-L2:15, D-L3:20, L1-L2:8, L1-L3:12,
L2-L3:5, L2-L4:9, L3-L4:6, L3-L5:7, L4-L5:3, D-L4:25, D-L5:30,
L1-L4:18, L1-L5:22, L2-L5:14.

Find a short (not necessarily optimal) route visiting all locations.

STEP 1-4: Use thought propagation approach.
```

**Output:**
```
STEP 1 — Analogous Problems:

Analogue 1: Visit L2, L3, L4 only (subset, 3 locations).
Analogue 2: Visit L3, L4, L5 only (different subset, 3 locations).

STEP 2 — Solving Analogues:

Analogue 1 (D→{L2,L3,L4}→D):
  D→L2→L3→L4→D = 15+5+6+25 = 51
  D→L3→L2→L4→D = 20+5+9+25 = 59
  D→L2→L4→L3→D = 15+9+6+20 = 50 ← best
  Strategy: Nearest-neighbor from L2 helps. L2-L4-L3 cluster is tight.

Analogue 2 (D→{L3,L4,L5}→D):
  D→L3→L4→L5→D = 20+6+3+30 = 59
  D→L3→L5→L4→D = 20+7+3+25 = 55 ← best
  Strategy: L4-L5 are very close (3). Always keep them adjacent.

STEP 3 — Propagation:
- Keep L4 and L5 adjacent (cost only 3).
- L2-L3 cluster is tight (cost 5).
- Start with nearest to depot: L1 (cost 10).

STEP 4 — Solve Original:
Applying strategies: D→L1→L2→L3→L4→L5→D
= 10 + 8 + 5 + 6 + 3 + 30 = 62

Try: D→L1→L2→L3→L5→L4→D
= 10 + 8 + 5 + 7 + 3 + 25 = 58 ← better (L4 closer to D than L5)

Final Answer: D → L1 → L2 → L3 → L5 → L4 → D, total distance 58.
```

## When to Use

- Problems with natural sub-structure that appears in simpler variants (e.g., graph problems, optimization)
- Tasks where reasoning strategies transfer across related problem instances
- Complex multi-step problems where direct approaches fail but simpler analogues succeed
- Educational settings where showing analogical reasoning is pedagogically valuable
- Benchmarking scenarios where you want the LLM to demonstrate transfer learning within context

## When to Avoid

- Simple problems that do not benefit from analogical reasoning overhead
- Highly unique problems with no meaningful analogues (e.g., extremely domain-specific)
- Token-constrained settings, as generating and solving multiple analogues is expensive
- Real-time applications where latency from multiple LLM calls is unacceptable
- Problems where the analogy generation step is likely to produce misleading parallels

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 3-5x base | Generating + solving analogues before the main problem |
| Latency | High | Multiple sequential LLM calls (analogues → propagation → final) |
| Quality gain | +10-25% | On graph reasoning and combinatorial tasks vs. CoT |
| Num calls | 3-6 typical | Depends on number of analogues generated |
| Scaling | Sublinear | More analogues yield diminishing returns after 3-4 |

## Variants

- **Adaptive TP:** Dynamically determines how many analogous problems to generate based on estimated problem difficulty.
- **Hierarchical TP:** Generates analogues at multiple levels of simplification, building up from trivial to moderate to the full problem.
- **Selective Propagation:** Uses an explicit scoring step to evaluate which analogous solutions are actually useful before propagation, discarding unhelpful ones.

## Composability

- **TP + Chain-of-Thought:** CoT is used internally to solve each analogous problem; TP structures the higher-level reasoning across problems.
- **TP + Tree-of-Thoughts:** ToT can be used within each analogous problem to explore multiple solution paths, with the best paths propagated.
- **TP + Self-Consistency:** Generate multiple propagation paths and vote on the final answer for improved reliability.
- **TP + Self-Refine:** After the initial propagated solution, use Self-Refine to iteratively improve the final answer.

## Limitations

- Quality of analogues is critical: poor analogues can mislead rather than help
- The LLM must be capable of generating structurally relevant analogues, which requires strong meta-cognitive abilities
- High token cost from solving multiple problems makes it impractical for high-throughput use cases
- Transfer of strategies between analogues and the original problem is not always straightforward
- No formal guarantee that the analogous solutions will improve performance on the target problem
- The approach assumes the LLM can accurately assess structural similarity between problems

## Sources

- **Primary:** [Thought Propagation: An Analogous Approach to Complex Reasoning with Large Language Models](https://arxiv.org/abs/2310.03965) — Yu et al., 2023
- **Related:** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — Yao et al., 2023
- **Related:** [Graph of Thoughts: Solving Elaborate Problems with Large Language Models](https://arxiv.org/abs/2308.09687) — Besta et al., 2023
