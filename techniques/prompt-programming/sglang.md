---
id: sglang
name: "SGLang (Structured Generation Language)"
aliases: ["SGLang", "Structured Generation Language", "RadixAttention"]
category: prompt-programming
family: serving-optimization
year: 2023
authors: ["Lianmin Zheng", "Liangsheng Yin", "Zhiqiang Xie", "Jeff Huang", "Chuyue Sun", "Cody Hao Yu", "Shiyi Cao", "Christos Kozyrakis", "Ion Stoica", "Joseph E. Gonzalez", "Clark Barrett", "Ying Sheng"]
paper: "https://arxiv.org/abs/2312.07104"
paper_title: "SGLang: Efficient Execution of Structured Language Model Programs"
venue: "arXiv 2023"
code: "https://github.com/sgl-project/sglang"

complexity: medium
token_cost: low
latency: low
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for: ["high-throughput LLM serving", "multi-call prompt programs", "KV cache optimization", "structured generation at scale", "batch processing with shared prefixes"]
avoid_when: ["single simple API call", "no control over serving infrastructure", "API-only model access", "no need for multi-call optimization"]
composes_with: ["chain-of-thought", "few-shot", "tool-augmented-prompting", "prompt-chaining", "self-consistency"]

tags: ["prompt-programming", "serving", "optimization", "kv-cache", "radix-attention", "structured-generation", "throughput"]
---

# SGLang (Structured Generation Language)

> **One-line summary:** A domain-specific language and runtime for LLM programs that achieves major speedups through RadixAttention (automatic KV cache reuse across calls) and co-designed frontend-backend optimizations for structured generation workloads.

## Overview

SGLang addresses a critical inefficiency in modern LLM applications: most real-world systems make multiple LLM calls that share significant prompt overlap, yet each call redundantly recomputes attention over the shared prefix. A few-shot prompt with 10 examples that is called 100 times recomputes the same 10 examples' KV cache 100 times. SGLang eliminates this waste through RadixAttention, an automatic KV cache management system that stores computed caches in a radix tree and reuses them across requests that share common prefixes.

Developed by Lianmin Zheng et al. at UC Berkeley (the same group behind vLLM), SGLang provides both a frontend language for expressing LLM programs and a backend runtime optimized for executing them efficiently. The frontend is a Python-embedded DSL where developers write multi-call programs using primitives like `gen()` (generate), `select()` (choose from options), and `fork()` (parallel branches). The backend automatically identifies shared prefixes, manages KV cache reuse, and parallelizes independent generation calls.

The performance gains are substantial: SGLang achieves up to 6.4x higher throughput compared to existing systems on complex LLM programs. This is especially impactful for structured generation workloads --- such as tree-of-thought, multi-turn agents, few-shot classification over many inputs, and self-consistency voting --- where multiple calls share significant context. SGLang also integrates constrained decoding (like Outlines) for guaranteed structured output, combining serving efficiency with output reliability.

## How It Works

1. **Program Definition:** Write an SGLang program using the Python-embedded DSL. Programs express multi-call LLM interactions with primitives for generation, selection, forking, and joining.
2. **Prefix Analysis:** The SGLang compiler analyzes the program to identify shared prefixes across calls and opportunities for parallel execution.
3. **RadixAttention:** The runtime maintains a radix tree of computed KV caches. When a new call arrives, the runtime finds the longest matching prefix in the tree and reuses its cached KV states, computing attention only for new tokens.
4. **Parallel Execution:** Independent branches (e.g., multiple candidates in self-consistency) are batched and executed in parallel on the GPU.
5. **Constrained Decoding:** For structured output, SGLang integrates FSM-based or regex-based constrained decoding directly into the serving engine, applying token masks during sampling without additional overhead.
6. **Result Assembly:** Branch outputs are joined and the final program result is returned to the caller.

### Diagram

```
┌──────────────────────────────────┐
│       SGLang Program              │
│   gen(), select(), fork()         │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│       SGLang Compiler             │
│  Identify shared prefixes         │
│  Plan parallel execution          │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│          RadixAttention Runtime           │
│                                          │
│  Radix Tree of KV Caches:               │
│  ┌─────┐                                │
│  │root │                                │
│  └──┬──┘                                │
│     ├──▶ "You are a helpful..." ──┐     │
│     │    (shared system prompt)    │     │
│     │    ┌──────────────────────┐  │     │
│     │    │ KV cache (reused!)  │  │     │
│     │    └──────────────────────┘  │     │
│     │         ├──▶ query_1 (new tokens) │
│     │         ├──▶ query_2 (new tokens) │
│     │         └──▶ query_3 (new tokens) │
│     │                                    │
│  Batch parallel independent branches     │
└────────────────────┬─────────────────────┘
                     │
                     ▼
          ┌────────────────────┐
          │   Program Results   │
          │   (all branches)    │
          └────────────────────┘
```

## Template

**Basic SGLang program:**
```python
import sglang as sgl

@sgl.function
def classify_with_explanation(s, text):
    s += sgl.system("You are a precise text classifier.")
    s += sgl.user(f"Classify the sentiment of: '{text}'")
    s += sgl.assistant(sgl.gen("classification", choices=["positive", "negative", "neutral"]))
    s += sgl.user("Explain your reasoning in one sentence.")
    s += sgl.assistant(sgl.gen("explanation", max_tokens=100))
```

**Multi-branch program (self-consistency):**
```python
import sglang as sgl

@sgl.function
def solve_with_consistency(s, problem):
    s += sgl.system("You are a math tutor. Solve step by step.")
    s += sgl.user(problem)

    forks = s.fork(3)  # Create 3 parallel branches
    for f in forks:
        f += sgl.assistant(sgl.gen("solution", max_tokens=300, temperature=0.7))

    s += sgl.user("Given these solutions, what is the consensus answer?")
    solutions = [f["solution"] for f in forks]
    s += sgl.user("\n".join(f"Solution {i+1}: {sol}" for i, sol in enumerate(solutions)))
    s += sgl.assistant(sgl.gen("final_answer", max_tokens=50))
```

**Batch processing with shared prefix:**
```python
import sglang as sgl

@sgl.function
def analyze_review(s, review):
    s += sgl.system("You are a product review analyst.")
    s += sgl.user(f"Analyze this review: {review}")
    s += sgl.assistant(sgl.gen("sentiment", choices=["positive", "negative", "mixed"]))
    s += sgl.user("What is the main topic?")
    s += sgl.assistant(sgl.gen("topic", max_tokens=20))

# Process many reviews — SGLang reuses the shared system prompt KV cache
reviews = ["Great product!", "Terrible quality.", "Good but expensive."]
results = analyze_review.run_batch([{"review": r} for r in reviews])
```

## Examples

### Example 1: Few-Shot Classification at Scale

**Input (SGLang program):**
```python
import sglang as sgl

FEW_SHOT_EXAMPLES = """
Text: "The movie was absolutely brilliant, a masterpiece!"
Category: entertainment
Sentiment: positive

Text: "Stock prices fell 5% after the earnings report."
Category: finance
Sentiment: negative

Text: "The new iPhone 16 features a faster A18 chip."
Category: technology
Sentiment: neutral
"""

@sgl.function
def classify(s, text):
    s += sgl.system("Classify text into category and sentiment.")
    s += sgl.user(f"{FEW_SHOT_EXAMPLES}\nText: \"{text}\"")
    s += sgl.assistant("Category: " + sgl.gen("category",
        choices=["entertainment", "finance", "technology", "sports", "politics"]))
    s += sgl.assistant("\nSentiment: " + sgl.gen("sentiment",
        choices=["positive", "negative", "neutral"]))

# Classify 1000 texts — shared few-shot prefix is computed ONCE
texts = load_texts()  # 1000 texts
results = classify.run_batch([{"text": t} for t in texts])
```

**Output (per item):**
```python
{"category": "technology", "sentiment": "positive"}
# ... x 1000, with ~5x throughput improvement from KV cache reuse
```

### Example 2: Tree-of-Thought with RadixAttention

**Input (SGLang program):**
```python
import sglang as sgl

@sgl.function
def tree_of_thought(s, problem):
    s += sgl.system("You are a creative problem solver.")
    s += sgl.user(f"Problem: {problem}\n\nGenerate an initial approach:")
    s += sgl.assistant(sgl.gen("initial", max_tokens=150))

    # Branch into 3 continuations (shared prefix reused via RadixAttention)
    branches = s.fork(3)
    for i, b in enumerate(branches):
        b += sgl.user("Now develop this approach further with a different angle:")
        b += sgl.assistant(sgl.gen(f"branch_{i}", max_tokens=200, temperature=0.8))

    # Evaluate branches
    s += sgl.user("Here are three developed approaches:\n")
    for i, b in enumerate(branches):
        s += sgl.user(f"Approach {i+1}: {b[f'branch_{i}']}\n")
    s += sgl.user("Which approach is best and why? Synthesize the best elements.")
    s += sgl.assistant(sgl.gen("synthesis", max_tokens=300))

result = tree_of_thought.run(
    problem="How can a small city reduce traffic congestion without building new roads?"
)
```

**Output:**
```python
{
    "initial": "A multi-pronged approach focusing on demand management...",
    "branch_0": "Focus on remote work incentives and flexible hours...",
    "branch_1": "Invest heavily in cycling infrastructure and micro-transit...",
    "branch_2": "Implement dynamic congestion pricing and smart traffic signals...",
    "synthesis": "The most effective strategy combines elements from all three:
     flexible work policies (Approach 1) reduce peak demand, cycling
     infrastructure (Approach 2) provides alternatives for short trips, and
     smart traffic management (Approach 3) optimizes existing road capacity.
     Together, these can reduce congestion by an estimated 30-40% without
     any new road construction."
}
```

## When to Use

- High-throughput applications making many LLM calls with shared prefixes
- Multi-call prompt programs (agents, tree-of-thought, self-consistency)
- Batch processing where many inputs share the same system prompt and examples
- When you control the serving infrastructure and can deploy SGLang runtime
- Applications combining structured output with high-performance serving
- Production systems where inference cost and latency are critical concerns

## When to Avoid

- Single, simple API calls with no prefix sharing opportunity
- When using third-party API providers (OpenAI, Anthropic) without self-hosting
- Teams without infrastructure to deploy and manage an LLM serving stack
- Prototyping phases where simplicity matters more than throughput
- When the model is only called once per user request with unique context each time
- Environments where deploying a custom serving runtime is not permitted

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Throughput gain | 2-6.4x | Compared to vLLM/TGI on multi-call workloads |
| Latency reduction | 30-60% | From KV cache reuse on shared prefixes |
| Token cost | Reduced | Fewer redundant computations for shared prefixes |
| Memory overhead | Low | Radix tree adds minimal memory; KV reuse saves memory overall |
| Implementation | Medium-High | Requires self-hosted serving infrastructure |
| Constrained gen | Native | FSM-based structured output integrated into serving engine |

## Variants

- **SGLang Frontend Only:** Use the Python DSL with any compatible backend (not just the SGLang runtime) for program structure, albeit without RadixAttention benefits.
- **SGLang + Constrained Decoding:** Enable JSON schema or regex constraints alongside RadixAttention for both structural guarantees and serving efficiency.
- **SGLang Serving Mode:** Deploy the SGLang runtime as an OpenAI-compatible API server, gaining RadixAttention benefits with minimal code changes.
- **SGLang with Speculative Decoding:** Combine RadixAttention with speculative decoding for even lower latency on sequential generation tasks.
- **Multi-Model SGLang:** Route different parts of a program to different models (e.g., a small model for classification, a large model for generation).

## Composability

- **SGLang + Self-Consistency:** Use `fork()` to generate multiple reasoning paths in parallel, with RadixAttention reusing the shared prompt prefix across all branches.
- **SGLang + Tree-of-Thought:** Natural fit --- fork at each thought step, evaluate branches, prune, and continue. RadixAttention makes branching nearly free.
- **SGLang + Few-Shot:** The shared few-shot prefix is computed once and reused across all batch items, making few-shot classification at scale highly efficient.
- **SGLang + Tool Use:** Integrate tool calls within SGLang programs; the runtime manages KV cache across the think-act-observe loop.
- **SGLang + Outlines:** SGLang natively integrates Outlines-style constrained decoding within its serving engine.

## Limitations

- Requires self-hosted infrastructure with GPU access
- The SGLang runtime adds operational complexity compared to simple API calls
- RadixAttention benefits depend on prefix sharing; unique prompts see minimal improvement
- Learning curve for the SGLang DSL on top of the underlying model API
- Limited to models that can be served locally (open-weight models)
- The project is evolving rapidly; API stability may change between versions
- Debugging distributed, batched prompt programs is more complex than single calls
- Integration with existing LLM frameworks (LangChain, etc.) requires adapters

## Sources

- **Primary:** [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104) — Zheng et al., 2023
- **Code:** [SGLang GitHub Repository](https://github.com/sgl-project/sglang) — Open-source implementation
- **Related:** [vLLM: Easy, Fast, and Cheap LLM Serving](https://arxiv.org/abs/2309.06180) — Kwon et al., 2023 — Predecessor serving engine from the same group
- **Related:** [Outlines: Structured Generation](https://github.com/dottxt-ai/outlines) — FSM-based constrained decoding integrated into SGLang
- **Background:** [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — Foundation for KV cache management
