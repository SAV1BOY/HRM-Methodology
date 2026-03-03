---
id: deepseek-r1
name: "DeepSeek-R1"
aliases:
  - R1 reasoning
  - open-source reasoning
  - DeepSeek R1
  - R1
category: reasoning-tokens
family: reasoning-budget
year: 2025
authors:
  - DeepSeek-AI
paper: "https://arxiv.org/abs/2501.12948"
paper_title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
venue: "arXiv 2025"
code: "https://github.com/deepseek-ai/DeepSeek-R1"

complexity: low
token_cost: variable
latency: high
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for:
  - complex mathematical reasoning
  - competitive programming
  - scientific problem solving
  - tasks requiring extended deliberation
  - open-source and self-hosted deployments
avoid_when:
  - simple factual lookups
  - low-latency requirements
  - tasks where reasoning overhead is unnecessary
  - need for proprietary API guarantees (SLAs, support)
composes_with:
  - chain-of-thought
  - self-consistency
  - few-shot
  - tool-augmented-prompting

tags:
  - reasoning-tokens
  - thinking
  - open-source
  - reinforcement-learning
  - deepseek
  - self-hosted
---

# DeepSeek-R1

> **One-line summary:** DeepSeek-R1 is an open-weight reasoning model that uses reinforcement learning to develop native chain-of-thought reasoning within extended `<think>` blocks, achieving performance competitive with OpenAI's o1 on math, code, and science benchmarks.

## Overview

DeepSeek-R1, released by DeepSeek-AI in January 2025, represents a major milestone in open-source reasoning models. It demonstrates that extended chain-of-thought reasoning capabilities — previously exclusive to proprietary models like OpenAI's o1 — can be developed through reinforcement learning (RL) without requiring supervised fine-tuning on human-annotated reasoning traces. The model generates a visible `<think>...</think>` block containing its step-by-step reasoning before producing the final answer, similar to Claude's extended thinking and OpenAI's o1 reasoning tokens.

The key technical contribution is the training methodology. DeepSeek-R1-Zero, the precursor model, was trained purely with RL (using Group Relative Policy Optimization, GRPO) starting from the DeepSeek-V3 base model — no supervised CoT data was used. Remarkably, the model spontaneously developed reasoning behaviors including self-verification, reflection, and exploration of alternative approaches. Building on this, DeepSeek-R1 adds a cold-start phase with curated long-CoT data before RL, which stabilizes training and improves readability of the reasoning process.

The results are striking: DeepSeek-R1 achieves 79.8% on AIME 2024 (competitive mathematics), 97.3% on MATH-500, and 2029 Elo on Codeforces, placing it on par with OpenAI's o1-1217. Crucially, the full model weights are released under an MIT license, and distilled versions (1.5B to 70B parameters) are available for deployment on consumer hardware. The distilled models (e.g., DeepSeek-R1-Distill-Qwen-32B) achieve surprisingly strong performance — the 32B distilled model outperforms OpenAI's o1-mini on several benchmarks, demonstrating that reasoning capabilities can be effectively transferred to smaller models through knowledge distillation.

## How It Works

1. **Input:** Provide the problem or question to the model via standard chat interface or API.
2. **Extended Reasoning (`<think>` block):** The model generates a potentially long reasoning trace within `<think>` tags. This block contains step-by-step analysis, self-correction, exploration of multiple approaches, and verification of intermediate results.
3. **Final Answer:** After the `<think>` block closes, the model generates the concise final answer.
4. **Post-processing:** The `<think>` block can be displayed to the user for transparency or hidden to show only the final answer.

### Diagram

```
User Input:
┌─────────────────────────────────────────┐
│  "Solve: Find all primes p such that   │
│   p² + 2 is also prime."               │
└─────────────────┬───────────────────────┘
                  │
                  v
DeepSeek-R1 Processing:
┌─────────────────────────────────────────┐
│ <think>                                 │
│ Let me consider small primes first.     │
│                                         │
│ p=2: p²+2 = 6 = 2×3, not prime.        │
│ Wait, let me reconsider...              │
│ p=2: 4+2=6, not prime.                  │
│ p=3: 9+2=11, prime! ✓                  │
│ p=5: 25+2=27=3³, not prime.            │
│ p=7: 49+2=51=3×17, not prime.          │
│                                         │
│ For p>3, p mod 3 ∈ {1,2}:              │
│ If p≡1(mod 3): p²≡1, p²+2≡0(mod 3)   │
│ If p≡2(mod 3): p²≡1, p²+2≡0(mod 3)   │
│ So for p>3, p²+2 is divisible by 3,    │
│ hence not prime (since p²+2 > 3).      │
│                                         │
│ Therefore p=3 is the only solution.     │
│ </think>                                │
│                                         │
│ The only prime p such that p²+2 is     │
│ also prime is **p = 3**.                │
└─────────────────────────────────────────┘
```

## Template

### API Usage (OpenAI-Compatible)
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",  # or self-hosted endpoint
    api_key="{api_key}"
)

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "{problem}"}
    ]
)

# Reasoning content is in the reasoning_content field
reasoning = response.choices[0].message.reasoning_content
answer = response.choices[0].message.content
```

### Self-Hosted (vLLM)
```bash
vllm serve deepseek-ai/DeepSeek-R1 \
    --tensor-parallel-size 8 \
    --max-model-len 32768
```

### Distilled Model (Consumer Hardware)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
)

messages = [{"role": "user", "content": "{problem}"}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")
outputs = model.generate(inputs, max_new_tokens=8192)
print(tokenizer.decode(outputs[0]))
```

## Examples

### Example 1: Competitive Mathematics (AIME-level)

**Input:**
```
Let S be the set of positive integers n such that n divides the sum of all
positive divisors of n (i.e., n | σ(n)). These are called multiply perfect
numbers. Find the three smallest elements of S.
```

**Output (`<think>`):**
```
I need to find positive integers n where n divides σ(n), where σ(n) is
the sum of all positive divisors.

For n=1: σ(1) = 1. Does 1 | 1? Yes. ✓

For n=2: σ(2) = 1+2 = 3. Does 2 | 3? No.
For n=3: σ(3) = 1+3 = 4. Does 3 | 4? No.
For n=4: σ(4) = 1+2+4 = 7. Does 4 | 7? No.
For n=5: σ(5) = 1+5 = 6. Does 5 | 6? No.
For n=6: σ(6) = 1+2+3+6 = 12. Does 6 | 12? Yes! 12/6=2. ✓

This makes 6 a multiply perfect number (specifically, 2-perfect or
perfect number).

Continuing: n=7 through n=27...
For n=28: σ(28) = 1+2+4+7+14+28 = 56. Does 28 | 56? Yes! 56/28=2. ✓

So 28 is also a perfect number (2-perfect).
```

**Output (Answer):**
```
The three smallest multiply perfect numbers are 1, 6, and 28.
```

### Example 2: Code Generation

**Input:**
```
Implement a function to find the longest increasing subsequence in O(n log n).
```

**Output (`<think>`):**
```
I need to implement the patience sorting approach for LIS.

Key idea: maintain an array tails[] where tails[i] is the smallest
possible tail element for an increasing subsequence of length i+1.

For each element, binary search in tails:
- If element > all tails, extend the sequence
- Otherwise, replace the first tail >= element

The length of tails is the LIS length. To reconstruct, I need to track
predecessors...
```

**Output (Answer):**
```python
import bisect

def longest_increasing_subsequence(nums):
    if not nums:
        return []

    tails = []
    indices = []
    predecessors = [-1] * len(nums)

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
            indices.append(i)
        else:
            tails[pos] = num
            indices[pos] = i
        predecessors[i] = indices[pos - 1] if pos > 0 else -1

    # Reconstruct
    result = []
    k = indices[len(tails) - 1]
    while k != -1:
        result.append(nums[k])
        k = predecessors[k]
    return result[::-1]
```

## When to Use

- Complex mathematical proofs and problem-solving requiring extended reasoning
- Competitive programming and algorithmic challenges
- Scientific reasoning across physics, chemistry, and biology
- Tasks where open-source / self-hosted deployment is required
- Scenarios where reasoning transparency (`<think>` block visibility) is valuable
- Cost-sensitive applications (DeepSeek API pricing is significantly lower than competitors)

## When to Avoid

- Simple factual questions where reasoning overhead is wasteful
- Low-latency applications where extended thinking adds unacceptable delay
- Tasks requiring strong instruction following or safety alignment (R1's RL training may produce less controlled outputs)
- When proprietary API SLAs, support, and guaranteed uptime are requirements
- Multilingual tasks where the model may default to Chinese in the reasoning trace

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Thinking tokens | 1K-64K+ | Variable; model decides reasoning depth |
| AIME 2024 | 79.8% pass@1 | Competitive with o1-1217 (79.2%) |
| MATH-500 | 97.3% | State-of-the-art for open-source |
| Codeforces | 2029 Elo | Competitive programming rating |
| API cost | ~$0.55/M input, $2.19/M output | Via DeepSeek API (significantly cheaper than o1) |
| Distilled 32B | Outperforms o1-mini | On math benchmarks; runs on single GPU |
| Model sizes | 1.5B - 671B (MoE) | Distilled Qwen/Llama variants available |

## Variants

- **DeepSeek-R1-Zero:** Pure RL model without cold-start SFT data. Exhibits emergent reasoning but less readable output.
- **DeepSeek-R1 (Full):** 671B MoE model with cold-start + RL. Best performance but requires multi-GPU serving.
- **DeepSeek-R1-Distill-Qwen-32B:** Distilled into Qwen2.5-32B. Strong reasoning on single GPU.
- **DeepSeek-R1-Distill-Llama-70B:** Distilled into Llama-3.1-70B for Llama-ecosystem compatibility.
- **DeepSeek-R1-Distill-Qwen-1.5B:** Smallest distilled model; runs on consumer hardware with reduced performance.

## Composability

- **R1 + Self-Consistency:** Generate multiple reasoning traces and majority-vote the final answer. Especially effective given R1's diverse exploration within `<think>` blocks.
- **R1 + Tool Use:** Route tool-calling tasks to R1 for complex planning, letting the model reason about which tools to call and in what order.
- **R1 + Few-Shot:** Provide examples to guide the output format (R1's reasoning is self-directed, but few-shot helps control response structure).
- **R1 + RAG:** Combine retrieved context with R1's reasoning for knowledge-grounded, deeply reasoned answers.

## Limitations

- The `<think>` block may contain reasoning in Chinese, even when the input and expected output are in English, due to training data composition.
- Language mixing within the reasoning trace can be distracting or unusable for non-Chinese-speaking developers.
- The model requires significant compute for the full 671B MoE variant (8× A100 or similar for serving).
- Reasoning depth is not directly controllable — unlike Claude's `budget_tokens`, there is no parameter to set a reasoning budget.
- RL-trained reasoning may occasionally produce verbose, repetitive, or circular reasoning patterns.
- Safety alignment is less robust than proprietary models; the model may be more susceptible to jailbreaks.
- The distilled models trade reasoning quality for accessibility — complex tasks may see degraded performance at smaller scales.
- Token-level streaming of the `<think>` block may not be supported by all serving frameworks.

## Sources

- **Primary:** [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) — DeepSeek-AI, 2025
- **Code:** [GitHub: deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)
- **Blog:** [DeepSeek-R1 Release](https://api-docs.deepseek.com/news/news250120) — DeepSeek, January 2025
- **Related:** [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) — DeepSeek-AI, 2024
- **Related:** [OpenAI o1 System Card](https://openai.com/index/openai-o1-system-card/) — OpenAI, 2024
