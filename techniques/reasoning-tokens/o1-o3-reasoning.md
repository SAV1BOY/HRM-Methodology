---
id: o1-o3-reasoning
name: "OpenAI o1/o3 Reasoning Models"
aliases: ["o1 Reasoning", "o3 Reasoning", "OpenAI Reasoning Tokens", "Reasoning Effort"]
category: reasoning-tokens
family: reasoning-budget
year: 2024
authors: ["OpenAI"]
paper: null
paper_title: null
venue: null
code: null

complexity: low
token_cost: high
latency: high
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for: ["math and science competitions", "complex coding problems", "multi-step logical reasoning", "tasks requiring deliberate exploration"]
avoid_when: ["simple factual queries", "latency-sensitive applications", "cost-sensitive high-volume workloads", "tasks requiring system prompts or few-shot examples"]
composes_with: ["tool-use", "structured-output", "self-consistency"]

tags: ["reasoning-tokens", "openai", "o1", "o3", "hidden-reasoning", "reasoning-effort"]
---

# OpenAI o1/o3 Reasoning Models

> **One-line summary:** OpenAI's o1 and o3 model families use hidden internal chain-of-thought reasoning tokens to deliberate before responding, with a `reasoning_effort` parameter that controls the depth of thinking.

## Overview

OpenAI's o1 and o3 series represent a paradigm shift in LLM architecture, introducing models specifically trained to perform extended internal reasoning before generating a response. Unlike standard GPT models that produce output token-by-token in a single pass, o1/o3 models generate hidden "reasoning tokens" -- an internal chain of thought that the model uses to break down problems, explore approaches, verify solutions, and self-correct. These reasoning tokens are not visible to the user (unlike Claude's thinking blocks) but significantly improve performance on complex tasks.

The key innovation is training the model to "think longer" when problems are harder. The o1 model (released September 2024) demonstrated remarkable performance on math competitions, coding challenges, and scientific reasoning, often matching or exceeding PhD-level human performance. The o3 and o3-mini variants (released early 2025) further refined this approach with the `reasoning_effort` parameter that lets developers control how much internal deliberation the model performs, offering a tradeoff between accuracy and cost/latency.

The reasoning effort parameter accepts values of "low", "medium", or "high", controlling how many internal reasoning tokens the model generates. On easy tasks, "low" effort suffices and saves cost. On competition-level math or complex coding, "high" effort can unlock substantially better performance. The o3-mini variant offers an efficient alternative for tasks that benefit from reasoning but do not require the full o3 model's capabilities.

## How It Works

1. **Submit Query:** Send a message to the o1/o3 model through the API. Optionally specify `reasoning_effort` ("low", "medium", or "high").
2. **Internal Reasoning:** The model generates hidden reasoning tokens -- an internal chain of thought that explores the problem, considers approaches, and verifies solutions. These tokens are not visible in the API response.
3. **Generate Response:** After internal deliberation, the model produces the visible response, informed by its extended reasoning.
4. **Token Accounting:** The API response includes `completion_tokens_details.reasoning_tokens` showing how many hidden tokens were used for reasoning, in addition to the visible completion tokens.
5. **Adjust Effort:** Based on the task complexity and cost/quality requirements, tune the `reasoning_effort` parameter for subsequent requests.

### Diagram

```
API Request:
+------------------------------------------+
| model: "o3-mini"                         |
| reasoning_effort: "high"                 |
| messages:                                |
|   - role: user                           |
|     content: "{complex_problem}"         |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
| Internal Processing (hidden):            |
|                                          |
| [Hidden Reasoning Tokens]                |
| (NOT visible in API response)            |
| The model internally deliberates,        |
| explores multiple approaches,            |
| checks its work, backtracks if           |
| needed, and verifies the solution.       |
|                                          |
| Token count reported in usage stats.     |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
| Visible Response:                        |
| "The answer is X."                       |
|                                          |
| Usage:                                   |
|   completion_tokens: 150                 |
|   reasoning_tokens: 8,432               |
|   total_tokens: 8,582                   |
+------------------------------------------+

Reasoning Effort Levels:
  low    --> fewer reasoning tokens, faster, cheaper
  medium --> balanced reasoning depth (default)
  high   --> maximum reasoning, slowest, most expensive
```

## Template

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="{model_name}",  # "o1", "o3-mini", "o3"
    reasoning_effort="{effort_level}",  # "low", "medium", "high"
    messages=[
        {
            "role": "user",
            "content": "{complex_question}"
        }
    ]
)

print(response.choices[0].message.content)
print(f"Reasoning tokens: {response.usage.completion_tokens_details.reasoning_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
```

## Examples

### Example 1: Competition Math with High Reasoning

**Input:**
```python
response = client.chat.completions.create(
    model="o3-mini",
    reasoning_effort="high",
    messages=[{
        "role": "user",
        "content": "Let f(x) = x^3 - 3x + 1. Prove that f has exactly "
                   "three real roots and find the sum of the cubes of "
                   "these roots."
    }]
)
```

**Output:**
```
To prove f(x) = x^3 - 3x + 1 has exactly three real roots:

1. f'(x) = 3x^2 - 3 = 3(x-1)(x+1), so critical points at x = -1, 1.
2. f(-1) = -1 + 3 + 1 = 3 > 0
3. f(1) = 1 - 3 + 1 = -1 < 0
4. Since f is a cubic with positive leading coefficient, f(-inf) = -inf
   and f(+inf) = +inf.
5. By IVT: one root in (-inf, -1), one in (-1, 1), one in (1, +inf).

For the sum of cubes of roots: By Vieta's formulas for roots r1, r2, r3:
- r1 + r2 + r3 = 0
- r1*r2 + r1*r3 + r2*r3 = -3
- r1*r2*r3 = -1

Using Newton's identity: r1^3 + r2^3 + r3^3 = (r1+r2+r3)^3 -
3(r1+r2+r3)(r1r2+r1r3+r2r3) + 3*r1*r2*r3
= 0 - 0 + 3(-1) = -3.

But since each ri satisfies ri^3 = 3ri - 1:
r1^3 + r2^3 + r3^3 = 3(r1+r2+r3) - 3 = 0 - 3 = -3.

The sum of the cubes of the roots is -3.

Usage: reasoning_tokens=4,218, completion_tokens=285
```

### Example 2: Coding Challenge with Medium Reasoning

**Input:**
```python
response = client.chat.completions.create(
    model="o3-mini",
    reasoning_effort="medium",
    messages=[{
        "role": "user",
        "content": "Write an efficient Python function to find the length "
                   "of the longest substring without repeating characters."
    }]
)
```

**Output:**
```python
def length_of_longest_substring(s: str) -> int:
    char_index = {}
    max_length = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length

# Time: O(n), Space: O(min(n, alphabet_size))
# Uses sliding window with hash map for O(1) character lookups.

Usage: reasoning_tokens=1,847, completion_tokens=132
```

## When to Use

- Competition-level math, science, and logic problems
- Complex coding challenges requiring careful algorithm design
- Tasks where accuracy is paramount and latency is acceptable
- Problems requiring multi-step reasoning with verification
- Scenarios where the model needs to explore multiple solution approaches

## When to Avoid

- Simple factual questions or basic text generation
- Real-time or low-latency applications (reasoning adds significant delay)
- High-volume applications where cost per query must be minimized
- Tasks requiring extensive system prompts or few-shot examples (o1 has limited support)
- Creative writing or conversational tasks where deliberation adds no value

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Reasoning tokens (low) | 500-2K | Minimal deliberation |
| Reasoning tokens (medium) | 2K-10K | Balanced reasoning |
| Reasoning tokens (high) | 10K-50K+ | Deep exploration |
| Latency (low) | 2-5 seconds | Typical for simple tasks |
| Latency (high) | 10-60 seconds | Can be much longer for hard problems |
| Quality vs GPT-4o | +10-40% | On math/reasoning benchmarks |
| Cost vs GPT-4o | 2-10x | Depending on reasoning effort |

## Variants

- **o1:** The original reasoning model. Strong general reasoning, but more expensive.
- **o1-mini:** Smaller, faster version optimized for STEM tasks. Good cost/performance ratio.
- **o3:** Latest reasoning model with improved capabilities and reasoning_effort parameter.
- **o3-mini:** Efficient reasoning model. Best balance of cost, speed, and reasoning quality for most tasks.
- **o1-pro:** Premium tier with more compute per query for the hardest problems.

## Composability

- **o1/o3 + Tool Use:** o3 models support function calling, allowing reasoned tool use.
- **o1/o3 + Structured Output:** Request JSON mode or structured outputs for programmatic consumption of reasoned answers.
- **o1/o3 + Self-Consistency:** Generate multiple responses with reasoning and vote on the most common answer.
- **o1/o3 + Multi-Turn:** Use multi-turn conversations to break complex problems into sub-problems.

## Limitations

- Reasoning tokens are hidden and not inspectable (unlike Claude's thinking blocks)
- Limited system prompt support in early o1 versions (improved in o3)
- No streaming of reasoning tokens; must wait for complete response
- Significantly more expensive per query than standard models due to reasoning token costs
- May "overthink" simple problems, wasting tokens on unnecessary deliberation
- Reasoning effort parameter is coarse-grained (only three levels)
- Cannot provide few-shot examples in the same way as standard chat models
- Model may still produce incorrect reasoning despite extended thinking

## Sources

- **Docs:** [OpenAI o1/o3 Documentation](https://platform.openai.com/docs/guides/reasoning) -- OpenAI, 2024-2025
- **Blog:** [Learning to Reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) -- OpenAI, 2024
- **Blog:** [OpenAI o3-mini](https://openai.com/index/openai-o3-mini/) -- OpenAI, 2025
- **Benchmark:** [ARC-AGI Results](https://arcprize.org/) -- o3 performance on ARC benchmark
