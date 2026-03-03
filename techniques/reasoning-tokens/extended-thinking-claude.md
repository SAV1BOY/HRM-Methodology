---
id: extended-thinking-claude
name: "Extended Thinking (Claude)"
aliases: ["Claude Thinking Blocks", "Claude Extended Thinking", "Budget Tokens"]
category: reasoning-tokens
family: reasoning-budget
year: 2025
authors: ["Anthropic"]
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

best_for: ["complex reasoning tasks", "math and science problems", "code generation and debugging", "multi-step analysis", "tasks requiring deliberation"]
avoid_when: ["simple factual lookups", "low-latency requirements", "cost-sensitive high-volume applications", "tasks where reasoning overhead is unnecessary"]
composes_with: ["chain-of-thought", "self-consistency", "few-shot", "tool-use"]

tags: ["reasoning-tokens", "thinking", "claude", "anthropic", "budget-tokens", "extended-reasoning"]
---

# Extended Thinking (Claude)

> **One-line summary:** Anthropic's extended thinking feature gives Claude a visible thinking block with a configurable token budget, enabling deeper multi-step reasoning before producing a final answer.

## Overview

Extended thinking is a feature in Claude models (starting with Claude 3.5 Sonnet and enhanced in Claude 3.7 Sonnet and Claude 4 Opus) that allows the model to engage in explicit, structured reasoning before generating its response. When enabled, Claude produces a "thinking block" -- a stream of internal reasoning tokens that are visible to the developer but can be hidden from the end user. The developer controls the maximum reasoning budget via the `budget_tokens` parameter, allowing fine-grained control over the depth of reasoning vs. latency and cost tradeoffs.

The key insight behind extended thinking is that many complex tasks benefit from deliberate, step-by-step reasoning that goes beyond what fits naturally in a single response. By providing a dedicated space for reasoning, the model can explore multiple approaches, check its work, consider edge cases, and organize its thoughts before committing to a final answer. This is conceptually similar to how humans use scratch paper or think through problems before responding.

Unlike OpenAI's o1/o3 models where reasoning tokens are hidden, Claude's thinking blocks are transparent -- developers can see the full reasoning trace. This transparency is valuable for debugging, understanding model behavior, and building trust. The `budget_tokens` parameter (ranging from 1,024 to 128,000+) lets developers tune the reasoning depth: lower budgets for simpler tasks that need just a bit of deliberation, and higher budgets for complex multi-step problems that require extensive analysis.

## How It Works

1. **Enable Extended Thinking:** Set `thinking.type = "enabled"` and specify `budget_tokens` in the API request. The budget controls the maximum number of tokens Claude can use for reasoning.
2. **Model Reasons in Thinking Block:** Before generating the visible response, Claude produces a thinking block containing its step-by-step reasoning, exploration of approaches, self-correction, and analysis.
3. **Generate Final Response:** After the thinking block, Claude generates the final user-facing response, informed by its extended reasoning.
4. **Review Thinking (Optional):** Developers can inspect the thinking block for debugging, quality assurance, or understanding the model's reasoning process.
5. **Adjust Budget:** Based on task complexity and quality requirements, tune `budget_tokens` up or down for optimal cost/quality tradeoff.

### Diagram

```
API Request:
+------------------------------------------+
| model: "claude-sonnet-4-20250514"        |
| thinking:                                |
|   type: "enabled"                        |
|   budget_tokens: 10000                   |
| messages:                                |
|   - role: user                           |
|     content: "{complex_question}"        |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
| Claude Processing:                       |
|                                          |
| [Thinking Block] (up to 10000 tokens)   |
| "Let me work through this step by step. |
|  First, I need to identify...           |
|  Wait, that approach won't work because.|
|  Instead, let me try...                 |
|  Checking: does this satisfy all        |
|  constraints? Yes, because..."          |
|                                          |
| [Response Block]                         |
| "The answer is X because..."            |
+------------------------------------------+
                    |
                    v
API Response includes both blocks
(developer sees thinking; can hide from user)
```

## Template

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": {budget_tokens}  # 1024 to 128000+
    },
    messages=[{
        "role": "user",
        "content": "{complex_question_or_task}"
    }]
)

# Access thinking and response separately
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

## Examples

### Example 1: Complex Math Problem

**Input:**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{
        "role": "user",
        "content": "Find all positive integers n such that n^2 + 2n + 2 "
                   "divides n^3 + 4n^2 + 4n - 14."
    }]
)
```

**Output (Thinking Block):**
```
Let me work through this step by step.

I need to find positive integers n where (n^2 + 2n + 2) | (n^3 + 4n^2 + 4n - 14).

Let me perform polynomial division:
n^3 + 4n^2 + 4n - 14 = (n^2 + 2n + 2)(n + 2) + (-2n - 18)

Wait, let me verify: (n^2 + 2n + 2)(n + 2) = n^3 + 2n^2 + 2n + 2n^2 + 4n + 4
= n^3 + 4n^2 + 6n + 4

So the remainder is: (n^3 + 4n^2 + 4n - 14) - (n^3 + 4n^2 + 6n + 4)
= -2n - 18

For divisibility, we need (n^2 + 2n + 2) | (2n + 18).

Since n^2 + 2n + 2 > 2n + 18 for n >= 5, we only need to check n = 1,2,3,4.

n=1: 5 | 20? Yes.
n=2: 10 | 22? No.
n=3: 17 | 24? No.
n=4: 26 | 26? Yes.

So n = 1 and n = 4.
```

**Output (Response):**
```
The positive integers n satisfying the condition are n = 1 and n = 4.
```

### Example 2: Code Debugging with Extended Thinking

**Input:**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 12000},
    messages=[{
        "role": "user",
        "content": "This function should return the longest palindromic "
                   "substring but it's returning wrong results. Fix it:\n\n"
                   "def longest_palindrome(s):\n"
                   "    n = len(s)\n"
                   "    dp = [[False]*n for _ in range(n)]\n"
                   "    start, max_len = 0, 1\n"
                   "    for i in range(n): dp[i][i] = True\n"
                   "    for i in range(n-1):\n"
                   "        if s[i] == s[i+1]:\n"
                   "            dp[i][i+1] = True\n"
                   "            start, max_len = i, 2\n"
                   "    for length in range(3, n+1):\n"
                   "        for i in range(n-length):\n"
                   "            j = i + length - 1\n"
                   "            if s[i] == s[j] and dp[i+1][j-1]:\n"
                   "                dp[i][j] = True\n"
                   "                start, max_len = i, length\n"
                   "    return s[start:start+max_len]"
    }]
)
```

**Output (Thinking Block):**
```
Let me trace through this code carefully...

The DP approach looks correct in structure. Let me check the loop bounds.

For the length-3+ loop: range(n - length) should be range(n - length + 1)
to include the last valid starting position.

Example: s = "babad", n = 5, length = 3
range(n - length) = range(2) = [0, 1]
But i=2 with j=4 is valid (s[2:5] = "bad") -- missed!

This is the bug. The inner loop should be range(n - length + 1).
```

**Output (Response):**
```
The bug is in the inner loop bound. Change `range(n-length)` to
`range(n-length+1)` to avoid skipping the last valid starting position
for each substring length.
```

## When to Use

- Complex reasoning tasks: math, logic puzzles, multi-step analysis
- Code generation, debugging, and review requiring careful thought
- Tasks where you need to understand the model's reasoning process
- Problems with multiple possible approaches that need exploration
- Situations where accuracy is more important than speed

## When to Avoid

- Simple factual questions or lookups that do not require reasoning
- High-throughput, low-latency applications where thinking overhead is unacceptable
- Budget-constrained scenarios where the additional tokens significantly increase costs
- Tasks where the model already performs well without extended thinking

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 1K-128K+ thinking tokens | Controlled by budget_tokens parameter |
| Latency increase | 2-10x | Proportional to thinking budget |
| Quality improvement | +10-30% | On complex reasoning benchmarks |
| Cost multiplier | 1.5-5x | Thinking tokens billed at standard rates |
| Optimal budget range | 4K-16K | For most complex tasks |

## Variants

- **Low Budget (1K-4K):** Quick deliberation for moderately complex tasks. Good for structured output and simple reasoning.
- **Medium Budget (4K-16K):** Standard setting for complex analysis, math, and coding. Best quality/cost tradeoff.
- **High Budget (16K-128K+):** Deep exploration for very complex problems. Significant latency but highest accuracy.
- **Streaming Thinking:** Stream the thinking block in real-time so users can watch the model reason (useful for interactive applications).

## Composability

- **Extended Thinking + Tool Use:** Claude can reason about when and how to use tools within the thinking block before making tool calls.
- **Extended Thinking + Few-Shot:** Provide examples in the prompt; Claude uses the thinking block to reason about which example patterns apply.
- **Extended Thinking + Self-Consistency:** Generate multiple responses with thinking, then select the most consistent answer.
- **Extended Thinking + System Prompts:** System prompts can guide what Claude should focus on during thinking.

## Limitations

- Thinking tokens add significant cost and latency, especially at high budgets
- The model may use thinking tokens unproductively on simple tasks
- Thinking blocks cannot be cached or reused across requests
- The quality of reasoning is still bounded by the model's capabilities
- Not available on all Claude models; requires specific model versions
- Cannot directly control the structure or focus of thinking, only the budget
- Thinking content may occasionally contain false starts or unproductive reasoning paths

## Sources

- **Docs:** [Anthropic Extended Thinking Documentation](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) -- Anthropic, 2025
- **API:** [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) -- Anthropic
- **Blog:** [Introducing Extended Thinking](https://www.anthropic.com/news/claude-3-7-sonnet) -- Anthropic, 2025
