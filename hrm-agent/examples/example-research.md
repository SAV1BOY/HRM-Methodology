# Example Session: Research Task

> **User Task:** "Research transformer architecture innovations since 2023 and summarize the top 5 most impactful papers."

## Task Analysis

```yaml
task_type: research-and-analysis
complexity: moderate
constraints:
  latency: relaxed
  token_budget: large
  quality: high
  tools_available: [web_search]
output_format: structured summary
```

## Technique Selection

The agent scores techniques from `taxonomy.yaml` against the task profile:

| Rank | Technique | Score | Rationale |
|------|-----------|-------|-----------|
| 1 | Step-Back Prompting | 0.92 | Abstracts the research question into broader principles first |
| 2 | Chain-of-Thought | 0.88 | Multi-step reasoning needed for evaluation and ranking |
| 3 | Source-Grounded Generation | 0.95 | Research task requires citing actual papers |
| 4 | Self-Refine | 0.82 | Iterative improvement of the summary quality |
| 5 | Checklist Prompting | 0.78 | Final verification of completeness |

## Pipeline Design

```
Step-Back Prompting → ReAct (search) → Source-Grounded Generation → Self-Refine → Checklist
```

```
┌─────────────────────┐
│   Research Task      │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  1. Step-Back        │  "What are the fundamental challenges in
│     Prompting        │   transformer architectures that drive
│                      │   innovation?"
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  2. ReAct            │  Search → Read → Evaluate → Search...
│     (with search)    │  Gather papers and key findings
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  3. Source-Grounded  │  Synthesize findings with citations
│     Generation       │  from verified sources
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  4. Self-Refine      │  Review for accuracy, completeness,
│                      │  and clarity
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  5. Checklist        │  Verify: all 5 papers cited,
│     Prompting        │  impact explained, limitations noted
└─────────┴───────────┘
```

## Execution Trace

### Step 1: Step-Back Prompting

**Prompt:**
```
Before researching specific transformer innovations, let's step back and
consider the broader question:

What are the fundamental challenges and limitations in transformer
architectures that motivate ongoing research? Think about:
- Computational efficiency (quadratic attention)
- Context length limitations
- Training data requirements
- Inference speed and cost
- Architectural rigidity

Based on these fundamental challenges, what categories of innovation
should we look for in recent papers?
```

**Output:**
```
The fundamental challenges driving transformer innovation are:

1. Quadratic attention complexity — O(n^2) makes long sequences expensive
2. Fixed context windows — limits reasoning over long documents
3. Inefficient inference — autoregressive decoding is sequential
4. Parameter efficiency — models are growing but with diminishing returns
5. Architectural flexibility — standard transformers treat all tokens equally

Categories to investigate:
- Efficient attention mechanisms (linear, sparse, local-global)
- Extended context architectures (RoPE extensions, ring attention)
- Mixture-of-Experts for parameter efficiency
- State-space model hybrids (Mamba-style)
- Speculative and parallel decoding for inference speed
```

### Step 2: ReAct (Search Loop)

**Cycle 1:**
```
Thought: I need to find highly-cited transformer papers from 2023-2024.
         Let me start with efficient attention and state-space models.
Action: search("transformer architecture innovations 2023 2024 survey")
Observation: Found survey papers covering Mamba, Mixtral, Ring Attention,
             GQA, and flash attention improvements.

Thought: These are strong candidates. Let me verify citations and impact.
Action: search("Mamba state space model Gu Dao 2023 citations")
Observation: Mamba (Gu & Dao, 2023) — 1200+ citations, introduced selective
             state spaces as transformer alternative.

Thought: Let me also check MoE architectures.
Action: search("Mixtral mixture of experts 2024 impact")
Observation: Mixtral 8x7B (Jiang et al., 2024) — demonstrated MoE at scale
             with open weights, outperforming GPT-3.5.

Thought: I should check Grouped Query Attention from the LLaMA papers.
Action: search("grouped query attention GQA Ainslie 2023")
Observation: GQA (Ainslie et al., 2023) — adopted by LLaMA 2, reduces KV
             cache by 8x while maintaining quality.
```

**Cycle 2:**
```
Thought: I have 3 strong candidates. Need 2 more. Let me check context
         extension and inference innovations.
Action: search("ring attention context extension 2023 Liu")
Observation: Ring Attention (Liu et al., 2023) — enables context lengths
             of 1M+ tokens via blockwise attention across devices.

Action: search("flash attention 2 Dao 2023 impact inference")
Observation: FlashAttention-2 (Dao, 2023) — 2x faster than original,
             adopted as default in nearly all major frameworks.

Thought: I now have 5 high-impact papers with verified details.
         Ready to synthesize.
```

### Step 3: Source-Grounded Generation

**Prompt:**
```
Based on the following verified research findings, write a structured
summary of the top 5 most impactful transformer architecture innovations
since 2023.

For each paper, you MUST:
1. Cite the exact paper with authors, year, and venue
2. Explain the core innovation
3. Quantify the impact (benchmarks, adoption, citations)
4. Note limitations

VERIFIED FINDINGS:
{react_output}

Format each entry as:
### [Rank]. [Paper Title]
- **Authors:** ...
- **Innovation:** ...
- **Impact:** ...
- **Limitations:** ...
```

**Output:**
```
### 1. Mamba: Linear-Time Sequence Modeling with Selective State Spaces
- **Authors:** Gu, A. & Dao, T. (2023)
- **Innovation:** Replaces attention with a selective state-space mechanism
  that processes sequences in linear time O(n) instead of quadratic O(n^2),
  while maintaining the ability to selectively remember or forget information.
- **Impact:** 1200+ citations. Spawned a family of SSM-transformer hybrids
  (Jamba, Mamba-2). Demonstrated competitive performance with transformers
  on language modeling at 3B scale with 5x higher throughput.
- **Limitations:** Underperforms transformers on tasks requiring precise
  in-context retrieval. Less effective for few-shot learning patterns.

### 2. Mixtral 8x7B: Sparse Mixture of Experts
- **Authors:** Jiang, A. et al. (Mistral AI, 2024)
- **Innovation:** Scales transformers via sparse MoE where each token is
  routed to 2 of 8 expert FFN layers, achieving 47B total parameters but
  only 13B active per token.
- **Impact:** Outperformed GPT-3.5 and LLaMA 2 70B on most benchmarks
  while using 6x less compute per token. Released with open weights,
  enabling widespread adoption.
- **Limitations:** Requires specialized infrastructure for efficient MoE
  serving. Load balancing across experts remains challenging.

### 3. FlashAttention-2: Faster Attention with Better Parallelism
- **Authors:** Dao, T. (2023), Princeton / Together AI
- **Innovation:** Optimizes the attention computation kernel by reducing
  non-matmul FLOPs and improving GPU occupancy through better work
  partitioning across thread blocks and warps.
- **Impact:** 2x faster than FlashAttention-1, reaching 50-73% of
  theoretical peak FLOPS. Adopted as default in PyTorch, HuggingFace,
  and virtually all major LLM training frameworks.
- **Limitations:** Requires CUDA-compatible GPUs. Custom attention patterns
  (sparse, cross) require additional implementation effort.

### 4. GQA: Training Generalized Multi-Query Transformer Models
- **Authors:** Ainslie, J. et al. (Google, 2023)
- **Innovation:** Grouped Query Attention interpolates between multi-head
  attention (1 KV head per query head) and multi-query attention (1 KV head
  total), using an intermediate number of KV heads (typically 8).
- **Impact:** Adopted in LLaMA 2, Mistral, and most subsequent open models.
  Reduces KV cache memory by 4-8x with minimal quality loss (<1% on
  benchmarks), enabling longer context and higher batch sizes in production.
- **Limitations:** Requires uptraining from multi-head attention checkpoints.
  Optimal number of groups is model-size dependent.

### 5. Ring Attention with Blockwise Transformers
- **Authors:** Liu, H. et al. (UC Berkeley, 2023)
- **Innovation:** Distributes the attention computation across multiple
  devices by partitioning the sequence into blocks and rotating KV blocks
  in a ring topology, enabling near-infinite context lengths.
- **Impact:** Demonstrated 1M+ token context lengths. Key enabler for
  long-context models (Gemini 1.5's 10M context). Overlaps communication
  with computation for near-linear scaling.
- **Limitations:** Requires multi-device setup. Communication overhead
  becomes significant for small sequence blocks.
```

### Step 4: Self-Refine

**Critique:**
```
Issues Found:
- [LOW] Mamba entry could mention the Mamba-2 follow-up for completeness
- [LOW] Should note that FlashAttention-2 also supports AMD GPUs via Triton
- [MEDIUM] Missing a "Common Themes" synthesis section tying innovations together

Improved: Added synthesis paragraph and minor corrections.
```

### Step 5: Checklist Verification

```
Research Quality Checklist:
- [PASS] 5 papers identified and ranked
- [PASS] All citations include authors, year, and venue
- [PASS] Impact quantified with metrics (citations, benchmarks, adoption)
- [PASS] Limitations noted for each paper
- [PASS] No hallucinated paper titles or author names
- [PASS] Innovations are distinct (no overlap between entries)
- [PASS] Ranking justified by impact evidence
```

## Pipeline Cost Summary

| Step | API Calls | Tokens Used | Latency |
|------|-----------|------------|---------|
| Step-Back | 1 | ~600 | ~3s |
| ReAct (search) | 6 | ~3000 | ~15s |
| Source-Grounded | 1 | ~2000 | ~8s |
| Self-Refine | 2 | ~1500 | ~6s |
| Checklist | 1 | ~500 | ~2s |
| **Total** | **11** | **~7600** | **~34s** |
