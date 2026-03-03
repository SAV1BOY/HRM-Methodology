---
id: cumulative-reasoning
name: "Cumulative Reasoning"
aliases:
  - incremental reasoning
  - proposer-verifier
  - CR
category: reasoning
family: thought-generation
year: 2023
authors:
  - Yifan Zhang
  - Jingqin Yang
  - Yang Yuan
  - Andrew Chi-Chih Yao
paper: "https://arxiv.org/abs/2308.04371"
paper_title: "Cumulative Reasoning with Large Language Models"
venue: "arXiv 2023"
code: "https://github.com/iiis-ai/cumulative-reasoning"

complexity: high
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for:
  - complex logical proofs
  - multi-step mathematical reasoning
  - tasks requiring incremental construction
  - problems where each step builds on verified prior steps
  - theorem proving and formal reasoning
avoid_when:
  - simple single-step tasks
  - time-sensitive applications
  - budget-constrained scenarios
  - tasks that do not require incremental verification
composes_with:
  - chain-of-thought
  - self-consistency
  - tree-of-thoughts
  - chain-of-verification

tags:
  - reasoning
  - verification
  - multi-agent
  - incremental
  - proposer-verifier
  - high-complexity
---

# Cumulative Reasoning

> **One-line summary:** Cumulative Reasoning uses a three-component architecture — Proposer, Verifier, and Reporter — to incrementally build a chain of verified intermediate conclusions, where each new proposition is checked before being added to the cumulative context for subsequent reasoning steps.

## Overview

Cumulative Reasoning (CR), introduced by Zhang et al. (2023), addresses a fundamental weakness in standard chain-of-thought prompting: the lack of verification at intermediate steps. In standard CoT, once the model makes an error at step N, all subsequent steps are likely to be wrong because they build on the flawed intermediate result. Cumulative Reasoning solves this by decomposing the reasoning process into three specialized roles that operate iteratively: a **Proposer** that generates the next reasoning step, a **Verifier** that validates whether that step is logically sound given all previously verified steps, and a **Reporter** that determines when the accumulated conclusions are sufficient to answer the original question.

The key insight is inspired by how mathematical proofs are constructed: each line of a proof is justified by previously established results, and each new claim is verified before being accepted. CR mirrors this process by maintaining a growing set of verified propositions. At each iteration, the Proposer examines the current set of verified facts and proposes a new conclusion. The Verifier checks whether this conclusion follows logically from the verified set. If accepted, the conclusion is added to the verified set; if rejected, the Proposer tries a different reasoning path. The Reporter monitors the verified set and signals when the final answer can be extracted.

This architecture achieves state-of-the-art results on challenging logical reasoning benchmarks. On the FOLIO dataset (first-order logic), CR achieved 98.04% accuracy, surpassing both standard CoT and Tree-of-Thoughts. On the AutoTNLI benchmark, it reached 86.89%. The cumulative, verified approach is particularly effective for tasks requiring strict logical validity, where a single unverified error can invalidate an entire reasoning chain.

## How It Works

1. **Initialize:** Start with the problem statement and any given facts as the initial verified context.
2. **Propose:** The Proposer LLM examines the verified context and generates a candidate next step — a new intermediate conclusion or deduction.
3. **Verify:** The Verifier LLM evaluates whether the proposed step is logically valid given only the verified context. It returns ACCEPT or REJECT.
4. **Accumulate or Retry:** If accepted, the new conclusion is added to the verified context. If rejected, return to Step 2 for an alternative proposal.
5. **Report:** After each accumulation, the Reporter LLM checks whether the verified context now contains enough information to answer the original question. If yes, extract the final answer. If no, return to Step 2.
6. **Repeat** until the Reporter signals completion or a maximum iteration count is reached.

### Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Cumulative Reasoning                       │
│                                                              │
│  Verified Context: {given facts}                             │
│                                                              │
│  ┌────────────┐                                              │
│  │  PROPOSER   │──── "Given facts F1..Fn, I propose Fn+1"   │
│  └──────┬─────┘                                              │
│         v                                                    │
│  ┌────────────┐       ┌─────────┐                            │
│  │  VERIFIER   │──No──>│ REJECT  │──── (retry with new       │
│  │             │       │         │      proposal)             │
│  └──────┬─────┘       └─────────┘                            │
│         │ Yes                                                │
│         v                                                    │
│  ┌──────────────────┐                                        │
│  │ ADD to Verified   │                                        │
│  │ Context: F1..Fn+1 │                                        │
│  └──────┬───────────┘                                        │
│         v                                                    │
│  ┌────────────┐       ┌───────────────┐                      │
│  │  REPORTER   │──Yes─>│ FINAL ANSWER  │                      │
│  │ "Enough to  │       │ Extract from  │                      │
│  │  answer?"   │       │ verified set  │                      │
│  └──────┬─────┘       └───────────────┘                      │
│         │ No                                                 │
│         └──────── (loop back to PROPOSER)                    │
└─────────────────────────────────────────────────────────────┘
```

## Template

### Proposer Prompt
```
You are a logical reasoning assistant. Given the following verified facts,
propose ONE new logical conclusion that can be derived from them.

Verified Facts:
{verified_context}

Original Question: {question}

Propose a single new conclusion (one sentence). Only propose conclusions
that follow directly from the verified facts above.

New Conclusion:
```

### Verifier Prompt
```
You are a logical verification assistant. Determine whether the following
proposed conclusion is logically valid given ONLY the verified facts below.

Verified Facts:
{verified_context}

Proposed Conclusion: {proposal}

Is this conclusion logically valid? Answer ONLY "VALID" or "INVALID" and
give a one-line justification.
```

### Reporter Prompt
```
Given the following verified facts, can you definitively answer the
original question?

Verified Facts:
{verified_context}

Original Question: {question}

If yes, state the answer. If no, say "CONTINUE" — more reasoning is needed.
```

## Examples

### Example 1: Logical Deduction

**Problem:**
```
All mammals are warm-blooded. All whales are mammals. All warm-blooded
animals need oxygen. Is it true that whales need oxygen?
```

**Iteration 1:**
```
Proposer: "Since all whales are mammals and all mammals are warm-blooded,
           whales are warm-blooded."
Verifier: VALID — follows from premises 1 and 2 by syllogism.
Reporter: CONTINUE — not yet sufficient to answer the question.

Verified: {whales are mammals, mammals are warm-blooded, warm-blooded
           need oxygen, whales are warm-blooded}
```

**Iteration 2:**
```
Proposer: "Since whales are warm-blooded and all warm-blooded animals
           need oxygen, whales need oxygen."
Verifier: VALID — follows from verified fact + premise 3.
Reporter: YES — The answer is: True, whales need oxygen.

Final Verified Set: {whales are warm-blooded, whales need oxygen}
```

### Example 2: Math Problem with Verification

**Problem:**
```
If f(x) = 2x + 3 and g(x) = x² - 1, find g(f(2)).
```

**Iteration 1:**
```
Proposer: "f(2) = 2(2) + 3 = 7"
Verifier: VALID — correct substitution and arithmetic.
Reporter: CONTINUE

Verified: {f(2) = 7}
```

**Iteration 2:**
```
Proposer: "g(f(2)) = g(7) = 7² - 1 = 49 - 1 = 48"
Verifier: VALID — correct substitution of f(2)=7 into g(x).
Reporter: YES — g(f(2)) = 48
```

## When to Use

- Complex logical deduction chains where intermediate errors are catastrophic
- Theorem proving or formal reasoning tasks
- Multi-step math problems where each step must be verified
- Tasks requiring strict logical validity (legal reasoning, formal verification)
- High-stakes reasoning where confidence in each step matters

## When to Avoid

- Simple tasks that do not require multi-step reasoning
- Latency-sensitive applications (each iteration requires 3 LLM calls)
- Budget-constrained scenarios (token cost scales with number of iterations)
- Creative or open-ended tasks where "valid/invalid" does not apply
- Tasks where approximate reasoning is sufficient

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 5-20x base | 3 calls per iteration × N iterations |
| Latency | High | Sequential: propose → verify → report per step |
| Accuracy gain | +10-25% | On formal logic benchmarks (FOLIO, AutoTNLI) |
| Num calls | 3N | N iterations, each with Proposer + Verifier + Reporter |
| Best improvement | Logic tasks | Where strict validity checking matters most |

## Variants

- **Single-Model CR:** Use the same LLM for all three roles with different system prompts (simpler deployment but potentially less effective verification).
- **Multi-Model CR:** Use different models for proposing and verifying (e.g., a larger model for verification) to improve diversity.
- **Parallel Proposer:** Generate multiple candidate proposals simultaneously and verify all, accepting the first valid one.
- **CR with Retrieval:** The Proposer can retrieve relevant knowledge before making proposals, grounding reasoning in external facts.
- **Relaxed CR:** Use soft verification scores instead of binary accept/reject for tasks with uncertain reasoning.

## Composability

- **CR + Chain-of-Thought:** Use CoT within the Proposer to generate higher-quality proposals with explicit reasoning.
- **CR + Self-Consistency:** Run multiple CR chains and take the majority-vote final answer for improved robustness.
- **CR + Tree-of-Thoughts:** When the Verifier rejects a proposal, explore alternative branches (tree search) rather than just retrying.
- **CR + RAG:** Ground the Proposer's reasoning in retrieved documents to ensure factual accuracy alongside logical validity.

## Limitations

- High computational cost: each reasoning step requires three LLM calls (Proposer, Verifier, Reporter), making it 3N× more expensive than single-pass reasoning.
- The Verifier is itself an LLM and can make errors — it may accept invalid conclusions or reject valid ones, limiting the reliability of the verification.
- Sequential nature prevents parallelization of the core reasoning loop.
- For problems requiring many intermediate steps, latency can become prohibitive.
- The Proposer may get stuck in loops, proposing the same rejected conclusion repeatedly without finding a valid alternative.
- The Reporter may prematurely terminate reasoning or fail to recognize when sufficient conclusions have been reached.
- Calibrating the maximum iteration count requires task-specific tuning.

## Sources

- **Primary:** [Cumulative Reasoning with Large Language Models](https://arxiv.org/abs/2308.04371) — Zhang, Y., Yang, J., Yuan, Y., & Yao, A.C., 2023
- **Code:** [GitHub: iiis-ai/cumulative-reasoning](https://github.com/iiis-ai/cumulative-reasoning)
- **Related:** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — Yao et al., NeurIPS 2023
- **Related:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Madaan et al., 2023
