---
id: everything-of-thoughts
name: "Everything of Thoughts (XoT)"
aliases: ["XoT", "MCTS-LLM"]
category: advanced-reasoning
family: thought-structure
year: 2023
authors: ["Ruomeng Ding", "Chaoyun Zhang", "Lu Wang", "Yong Xu", "Minghua Ma", "Wei Zhang", "Si Qin", "Saravan Rajmohan", "Qingwei Lin", "Dongmei Zhang"]
paper: "https://arxiv.org/abs/2311.04254"
paper_title: "Everything of Thoughts: Defying the Law of Penrose Triangle in LLMs"
venue: "arXiv 2023"
code: null

complexity: high
token_cost: low
latency: high
num_calls: 1

requires_examples: false
requires_tools: true
requires_training: true
model_agnostic: true

best_for: ["complex search problems", "puzzle solving", "mathematical reasoning", "game playing", "planning tasks requiring exhaustive exploration"]
avoid_when: ["simple factual queries", "creative writing", "low-latency requirements", "no access to external compute", "problems lacking clear reward signals"]
composes_with: ["chain-of-thought", "tree-of-thoughts", "self-consistency"]

tags: ["mcts", "reinforcement-learning", "external-solver", "thought-structure", "hybrid-reasoning"]
---

# Everything of Thoughts (XoT)

> **One-line summary:** XoT combines Monte Carlo Tree Search with reinforcement learning as an external thought-structuring solver to guide LLM reasoning in a single pass, achieving high-quality solutions with minimal token cost.

## Overview

Everything of Thoughts (XoT) addresses a fundamental trilemma in LLM reasoning that the authors liken to a "Penrose Triangle": existing methods must trade off among thought quality, thought efficiency (token cost), and flexibility (problem generality). Chain-of-Thought achieves efficiency but lacks exploration breadth. Tree-of-Thoughts explores widely but consumes massive tokens. XoT breaks this trilemma by offloading the search process to an external Monte Carlo Tree Search (MCTS) solver enhanced with reinforcement learning, then distilling the discovered solution path into a single LLM prompt.

The key insight is that the combinatorial exploration needed for complex reasoning does not have to happen inside the LLM's generation loop. Instead, MCTS can explore the thought space externally using a learned policy and value network, identify the most promising reasoning trajectory, and then present that trajectory to the LLM as a structured prompt. This means the LLM only needs one forward pass to produce the final answer, dramatically reducing token cost while preserving the quality benefits of tree-based exploration.

XoT also incorporates a revision mechanism: if the LLM's output does not meet quality thresholds, the MCTS solver can refine its search and provide an updated thought trajectory. This creates a lightweight feedback loop between the external solver and the LLM that progressively improves output quality without the exponential token overhead of purely LLM-internal search strategies.

## How It Works

1. **Problem Encoding:** The input problem is encoded into a state representation suitable for MCTS. Each "thought" becomes a node in the search tree, with transitions representing reasoning steps.

2. **MCTS Exploration:** The external MCTS solver, guided by a policy network (trained via RL) and a value network, explores the thought space. It runs many simulated rollouts to evaluate different reasoning paths without consuming any LLM tokens.

3. **Trajectory Extraction:** The highest-value path through the search tree is extracted as a sequence of thought steps — the optimal reasoning trajectory identified by the solver.

4. **Single-Pass Prompting:** The extracted trajectory is formatted into a structured prompt and fed to the LLM. The model follows the pre-computed reasoning chain to produce the final answer in a single generation call.

5. **Revision (if needed):** If the LLM's output fails validation checks, the MCTS solver refines its search (e.g., expanding more nodes or adjusting the policy) and produces an updated trajectory for a second LLM call.

### Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    XoT Pipeline                         │
│                                                         │
│  ┌──────────┐    ┌──────────────────┐    ┌───────────┐  │
│  │  Problem  │───>│   MCTS + RL      │───>│  Optimal  │  │
│  │  Input    │    │   External       │    │  Thought  │  │
│  └──────────┘    │   Solver         │    │  Path     │  │
│                  │                  │    └─────┬─────┘  │
│                  │  ┌────┐ ┌─────┐ │          │         │
│                  │  │ Pol│ │ Val │ │          │         │
│                  │  │ Net│ │ Net │ │          v         │
│                  │  └────┘ └─────┘ │    ┌───────────┐  │
│                  └──────────────────┘    │   LLM     │  │
│                                         │  (1 call)  │  │
│                         ┌───────────────│           │  │
│                         │  Revision?    └─────┬─────┘  │
│                         │  (if failed)        │         │
│                         v                     v         │
│                  ┌──────────────┐      ┌───────────┐   │
│                  │ Refine MCTS  │      │  Final    │   │
│                  │ Search       │      │  Answer   │   │
│                  └──────────────┘      └───────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Template

```
You are given a complex reasoning problem along with a pre-computed optimal
reasoning trajectory. Follow the trajectory step by step to arrive at the
final answer.

Problem:
{problem_description}

Optimal Reasoning Trajectory (computed via external search):
Step 1: {thought_step_1}
Step 2: {thought_step_2}
Step 3: {thought_step_3}
...
Step N: {thought_step_n}

Based on the above reasoning trajectory, provide the final answer.
Verify each step is logically sound before stating your conclusion.

Final Answer:
```

## Examples

### Example 1: 24 Game (Mathematical Reasoning)

**Input:**
```
Problem: Use the numbers 2, 5, 7, 8 with basic operations (+, -, *, /)
to make 24. Each number must be used exactly once.

Optimal Reasoning Trajectory (computed via MCTS):
Step 1: Consider 8 - 5 = 3
Step 2: Consider 2 * 3 = 6  (but this uses a derived number, reconsider)
Step 3: Consider 7 - 5 = 2  (yields duplicate of 2, not useful)
Step 4: Consider (8 - 2) = 6
Step 5: Consider 6 * (7 - 5) = 6 * 2 = 12  (not 24)
Step 6: Consider (7 + 5) = 12
Step 7: Consider (8 / 2) = 4
Step 8: Consider 12 * (8 / 2) = 12 * 4 = 48  (too high, uses all numbers wrong)
Step 9: Consider 2 * (5 + 7) = 2 * 12 = 24  ← uses 2, 5, 7 only
Step 10: Remaining number is 8. Adjust: (5 - (8 / 2)) = 1, not useful.
Step 11: (8 - 2) * (7 - 5) = 6 * 2 = 12  (not 24)
Step 12: 8 * (7 - 5) + 2 = 16 + 2 = 18 (no)
Step 13: 8 * 2 + 7 + 5 = 16 + 12 = 28 (no)
Step 14: (7 + 5 - 8) * 2 = 4 * 2 = 8 (no)
Step 15: 8 / (7 - 5) * 2 = 4 * 2 = 8 (no)
Step 16: (8 + 2) * 5 - 7 = 50 - 7 = 43 (no)
Step 17: 2 * (8 + 5 - 7) = 2 * 6 = 12 (no)
Step 18: (5 * 8) / 2 + 7 = 20 + 7 = 27 (no)
Step 19: 5 * (8 - 2) - 7 = 30 - 7 = 23 (close)
Step 20: (5 - 8/2) is not integer path. Try: 2 / (7 - 5) = 1
Step 21: 8 * (2 / (7 - 5)) = 8 * 1 = 8 (no)
Step 22: 8 * 5 - 2 * 7 = 40 - 14 = 26 (no)
Step 23: 8 * 5 - 2 - 7 = 31 (no)
Step 24: 8 * 5 / 2 + 7 = 27 (no)
Step 25: 8 * (7 - 5) * 2 = 32 (no)
Step 26: (5 * 2 - 8) * 7 = 2 * 7 = 14 (no)
Step 27: (8 * 2 - 7) * 5 = 9 * 5 = 45 (no)
Step 28: (7 * 2) * (8 - 5) = 14 * 3 = 42 (no)
Step 29: (7 - 2) * 8 - 5… wait, try with fractions:
         8 / (5 - 7/2) = 8 / (5 - 3.5) = 8 / 1.5 -- not clean.
Step 30: Think systematically. Target 24 with 4 nums.
         5 * (8 - 7) * 2 = 5 * 1 * 2 = 10 (no)
         Actually try: (7 - 5 + 2) * 8 = 4 * 8 = 32 (no)
         Hmm. Try (2 + 7 - 5) * 8 = 4 * 8 = 32 same thing.
Step 31: Final path: 2 * 5 - 7 = 3; 3 * 8 = 24. ✓

Based on the above trajectory, provide the final answer.
```

**Output:**
```
Following the MCTS-derived trajectory, the solution is:

(2 * 5 - 7) * 8 = 24

Verification:
  2 * 5 = 10
  10 - 7 = 3
  3 * 8 = 24 ✓

All four numbers (2, 5, 7, 8) are used exactly once.
```

### Example 2: Spatial Planning (Block World)

**Input:**
```
Problem: Rearrange blocks from initial state to goal state.
Initial: A on table, B on A, C on table, D on C
Goal: D on table, C on D, B on C, A on B

Optimal Reasoning Trajectory (computed via MCTS):
Step 1: Current state — stacks [A, B] and [C, D]. Goal requires [D, C, B, A].
Step 2: Must unstack D from C. Move D to table.
Step 3: Must unstack B from A. Move B to table.
Step 4: Now: A on table, B on table, C on table, D on table.
Step 5: Place C on D.
Step 6: Place B on C.
Step 7: Place A on B.
Step 8: Final state: [D, C, B, A]. Matches goal. ✓

Based on the above trajectory, provide the final answer.
```

**Output:**
```
Following the pre-computed plan:

Move 1: Unstack D from C → place D on table
Move 2: Unstack B from A → place B on table
Move 3: Stack C on D
Move 4: Stack B on C
Move 5: Stack A on B

Final state: D (table) → C → B → A (top)
This matches the goal configuration. Plan is optimal at 5 moves.
```

## When to Use

- Complex combinatorial problems (puzzles, scheduling, planning) where systematic search outperforms linear reasoning
- Tasks with clear reward signals that can guide MCTS evaluation
- Scenarios where token budget is constrained but solution quality must remain high
- Problems where the search space is structured and can be decomposed into discrete thought steps
- Batch-processing settings where the upfront cost of MCTS training and execution is amortized across many queries

## When to Avoid

- Simple or factual questions that do not require multi-step reasoning
- Creative or open-ended generation tasks with no clear objective function
- Low-latency interactive applications where MCTS computation adds unacceptable delay
- Scenarios without access to GPU compute for the RL-trained policy/value networks
- One-off queries where the overhead of training an MCTS solver is not justified
- Problems where the state space cannot be easily discretized into thought nodes

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | Very low (1 call) | Search happens externally, LLM sees only the final trajectory |
| Latency | High | MCTS exploration adds seconds to minutes depending on problem complexity |
| Quality gain | +20-40% on Game of 24 | Compared to CoT; approaches or exceeds ToT quality |
| Infrastructure | High | Requires trained policy/value networks and MCTS runtime |
| Training cost | Moderate-High | RL training needed per problem domain |

## Variants

- **XoT-Revision:** Includes the feedback loop where failed LLM outputs trigger refined MCTS search. Adds robustness at the cost of potential additional LLM calls.
- **XoT-Lite:** Uses a simpler heuristic search (e.g., beam search) instead of full MCTS, reducing infrastructure requirements at some quality cost.
- **Domain-Specific XoT:** Pre-trained solvers for specific domains (math, code, planning) that can be swapped modularly.

## Composability

- **XoT + Chain-of-Thought:** The extracted MCTS trajectory naturally serves as a chain-of-thought prompt, making CoT a built-in component.
- **XoT + Self-Consistency:** Run MCTS multiple times with different random seeds and let the LLM vote on the best answer across trajectories.
- **XoT + Self-Refine:** If the LLM's initial output based on the MCTS trajectory is imperfect, Self-Refine can iteratively polish the final answer without re-running MCTS.
- **XoT + Tool Use:** The MCTS solver itself can be considered a tool; XoT naturally integrates into tool-augmented pipelines.

## Limitations

- Requires significant infrastructure beyond the LLM itself (MCTS solver, trained neural networks)
- RL training of policy/value networks is domain-specific and may not transfer across problem types
- The discretization of the thought space into MCTS nodes is non-trivial and requires careful design
- Not applicable to tasks without clear evaluation functions for intermediate states
- The external solver adds a dependency that increases system complexity and failure modes
- Cold-start problem: new problem domains require fresh RL training

## Sources

- **Primary:** [Everything of Thoughts: Defying the Law of Penrose Triangle in LLMs](https://arxiv.org/abs/2311.04254) — Ding et al., 2023
- **Related:** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — Yao et al., 2023
- **Related:** [Reasoning with Language Model is Planning with World Model](https://arxiv.org/abs/2305.14992) — Hao et al., 2023
