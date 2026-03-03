---
id: analogical-prompting
name: "Analogical Prompting"
aliases:
  - self-generated examples
  - analogical reasoning
  - analogy-based prompting
category: reasoning
family: thought-generation
year: 2023
authors:
  - Michihiro Yasunaga
  - Xinyun Chen
  - Yujia Li
  - Panupong Pasupat
  - Jure Leskovec
  - Percy Liang
  - Ed H. Chi
  - Denny Zhou
paper: "https://arxiv.org/abs/2310.01714"
paper_title: "Large Language Models as Analogical Reasoners"
venue: "ICLR 2024"
code: null

complexity: medium
token_cost: medium
latency: medium
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for:
  - novel problems without curated examples
  - math and code generation
  - tasks where few-shot exemplar curation is expensive
  - complex reasoning that benefits from worked examples
  - situations where example diversity matters
avoid_when:
  - high-quality curated few-shot examples already exist
  - very simple tasks where examples are unnecessary
  - token budget is very tight
  - tasks requiring domain-specific examples the model may lack
composes_with:
  - chain-of-thought
  - self-consistency
  - self-refine
  - plan-and-solve

tags:
  - reasoning
  - self-generated
  - few-shot
  - analogical
  - zero-resource
---

# Analogical Prompting

> **One-line summary:** Analogical Prompting instructs the LLM to self-generate relevant exemplars and reasoning chains before solving the target problem, achieving few-shot CoT-level performance without any manually curated examples.

## Overview

Analogical Prompting, introduced by Yasunaga et al. (2023), addresses a fundamental bottleneck in few-shot Chain-of-Thought prompting: the need for manually curated, high-quality exemplars. In standard few-shot CoT, a human must carefully select representative problems and write out their reasoning chains — a process that is time-consuming, requires domain expertise, and may introduce selection bias. Analogical Prompting eliminates this dependency by prompting the LLM to recall or construct relevant analogous problems and their solutions before attempting the target problem.

The key insight is that large language models, trained on vast corpora, have internalized a huge library of problem-solving patterns. Rather than relying on human-curated exemplars in the prompt, the model can be instructed to generate its own exemplars that are specifically relevant to the problem at hand. This is analogous to how an expert mathematician, when faced with a new problem, first recalls similar problems they have solved before and uses those solutions as guides. The self-generated examples are often more relevant than static few-shot exemplars because the model tailors them to the specific problem structure.

On mathematical reasoning benchmarks (GSM8K, MATH), code generation tasks (Codeforces), and other reasoning benchmarks, Analogical Prompting matches or surpasses the performance of carefully curated few-shot CoT prompts. Critically, it achieves this in a zero-resource setting — no human-annotated examples are required. This makes it particularly valuable when deploying to new domains where exemplar curation has not been done, or when the diversity of problems makes static exemplars insufficient.

## How It Works

1. **Present the target problem:** Provide the problem to the model along with an instruction to first recall relevant exemplars.
2. **Self-generate analogous problems:** The model generates 2-3 problems that are structurally similar to the target, along with their complete solutions (including reasoning chains).
3. **Solve the target:** Using its self-generated exemplars as context, the model then solves the target problem following the same reasoning patterns demonstrated in its own examples.
4. **Extract the answer:** The final answer follows naturally from the reasoning chain guided by the analogous examples.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   PROMPT                                  │
│                                                           │
│  "Before solving the following problem, recall 2-3        │
│   relevant and distinct problems that are analogous.      │
│   For each, provide the problem statement and a           │
│   step-by-step solution. Then solve the target problem."  │
│                                                           │
│  Target Problem: {problem}                                │
├──────────────────────────────────────────────────────────┤
│               MODEL GENERATES                             │
│                                                           │
│  Recalled Problem 1: [analogous problem + solution]       │
│  Recalled Problem 2: [analogous problem + solution]       │
│  Recalled Problem 3: [analogous problem + solution]       │
│                                                           │
│  ─────────────────────────────────────                    │
│                                                           │
│  Now solving the target problem:                          │
│  [step-by-step reasoning guided by recalled patterns]     │
│  → Final Answer                                           │
└──────────────────────────────────────────────────────────┘
```

## Template

```
# Relevant Problems and Solutions

Before solving the problem below, first recall {k} relevant and distinct
problems that are analogous to it. For each recalled problem:
1. State the problem
2. Provide a complete step-by-step solution

Then, using the patterns from these examples, solve the target problem
step by step.

## Target Problem

{problem}
```

## Examples

### Example 1: Mathematical Reasoning

**Prompt:**
```
Before solving the problem below, first recall 2 relevant and distinct
problems that are analogous. For each, state the problem and provide a
step-by-step solution. Then solve the target problem.

Target Problem: A rectangular garden has a perimeter of 56 meters. If the
length is 4 meters more than twice the width, find the dimensions.
```

**Model Output:**
```
## Recalled Problem 1
Problem: A rectangle has a perimeter of 40 cm. The length is 3 times
the width. Find the dimensions.

Solution:
- Let width = w, length = 3w
- Perimeter: 2(w + 3w) = 40
- 2(4w) = 40 → 8w = 40 → w = 5
- Length = 3(5) = 15
- Dimensions: 5 cm × 15 cm

## Recalled Problem 2
Problem: The sum of two numbers is 30. One number is 6 more than the
other. Find both numbers.

Solution:
- Let smaller number = x, larger = x + 6
- x + (x + 6) = 30
- 2x + 6 = 30 → 2x = 24 → x = 12
- Numbers: 12 and 18

## Solving the Target Problem
- Let width = w, length = 2w + 4
- Perimeter: 2(w + 2w + 4) = 56
- 2(3w + 4) = 56
- 6w + 8 = 56
- 6w = 48
- w = 8
- Length = 2(8) + 4 = 20
- Dimensions: 8 meters × 20 meters
```

### Example 2: Code Generation

**Prompt:**
```
Before solving the problem below, first recall 2 relevant and distinct
coding problems that are analogous. For each, state the problem and
provide a solution. Then solve the target problem.

Target Problem: Write a function that finds the length of the longest
substring without repeating characters.
```

**Model Output:**
```
## Recalled Problem 1
Problem: Find the maximum sum of a contiguous subarray (sliding window).

Solution:
```python
def max_subarray_sum(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```
Key pattern: sliding window with fixed/variable size.

## Recalled Problem 2
Problem: Find the smallest window containing all characters of a target.

Solution: Use a variable-size sliding window with a hash map to track
character frequencies. Expand right pointer to include characters, shrink
left pointer when window satisfies the condition.

Key pattern: variable-size sliding window with hash-based tracking.

## Solving the Target Problem
This combines both patterns: a variable-size sliding window with a set to
track character presence.

```python
def length_of_longest_substring(s: str) -> int:
    char_set = set()
    left = 0
    max_length = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    return max_length
```

The answer uses the sliding window pattern from both recalled problems,
with a set instead of a counter for O(1) duplicate detection.
```

## When to Use

- You face a novel problem and do not have curated few-shot examples available
- Exemplar curation is too expensive or time-consuming for the domain
- The problem space is diverse and static exemplars cannot cover all variations
- You want the benefits of few-shot CoT without manual annotation effort
- The model has strong domain knowledge (trained on relevant data) to generate good analogies

## When to Avoid

- High-quality, curated few-shot exemplars are already available and outperform self-generation
- The domain is highly specialized and the model's training data may lack relevant analogues
- Token budget is very constrained (self-generated examples add significant tokens)
- Very simple tasks where zero-shot performance is already sufficient
- Tasks where incorrect self-generated examples could mislead the model

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 2-3x zero-shot | Self-generated examples add ~200-500 tokens |
| Latency | Medium | Single call, but longer generation |
| Accuracy gain | +5-15% | Over zero-shot CoT; matches curated few-shot CoT |
| Implementation | Trivial | Just modify the prompt instruction |
| Model requirements | Large | Needs models with strong internal knowledge (GPT-4+) |

## Variants

- **Single Analogy:** Recall just one analogous problem for reduced token cost with moderate gains.
- **Problem-Only Recall:** Recall only the analogous problem statement (not the solution) to prime the model's pattern-matching.
- **Domain-Constrained:** Instruct the model to recall analogies from a specific domain (e.g., "recall similar physics problems").
- **Graded Analogy:** Recall analogies in increasing difficulty — a simple one first, then one closer in difficulty to the target.

## Composability

- **Analogical + Self-Consistency:** Generate multiple sets of analogies and solutions; majority-vote the final answer for improved robustness.
- **Analogical + Self-Refine:** After solving, have the model critique its solution by comparing against the patterns in its recalled examples.
- **Analogical + Chain-of-Thought:** The recalled examples naturally contain CoT; this composition is inherent in the technique.
- **Analogical + Plan-and-Solve:** First plan the approach, then recall analogies relevant to each plan step.

## Limitations

- The quality of self-generated exemplars is bounded by the model's training data — models may generate incorrect or misleading analogies for unfamiliar domains.
- Self-generated examples sometimes lack diversity, with the model producing variations of the same pattern rather than structurally distinct analogies.
- Token cost is significant: 2-3 complete worked examples plus the target solution.
- For specialized domains (advanced mathematics, niche engineering), the model may fabricate plausible but wrong analogies.
- The technique assumes the model's internal knowledge is sufficient for generating relevant analogues.
- Smaller models may generate low-quality or irrelevant analogies that hurt rather than help performance.

## Sources

- **Primary:** [Large Language Models as Analogical Reasoners](https://arxiv.org/abs/2310.01714) — Yasunaga, M., Chen, X., Li, Y., Pasupat, P., Leskovec, J., Liang, P., Chi, E.H., & Zhou, D., ICLR 2024
- **Related:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) — Wei et al., NeurIPS 2022
- **Related:** [Automatic Chain of Thought Prompting in Large Language Models](https://arxiv.org/abs/2210.03493) — Zhang et al., 2022
