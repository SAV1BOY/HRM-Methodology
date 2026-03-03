# Playbook: Research & Analysis

> **Pipeline:** Step-Back Prompting → Chain-of-Thought → Chain-of-Verification → Self-Refine → Output Format
>
> **Best for:** Literature reviews, market analysis, technical deep-dives, policy research, investigative reports.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │   User Question     │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. Step-Back        │  Extract high-level principles
                    │     Prompting        │  and background concepts
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Chain-of-Thought │  Systematic reasoning through
                    │     (CoT)           │  the research question
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Chain-of-        │  Generate verification
                    │     Verification    │  questions & fact-check
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Self-Refine      │  Critique & improve the
                    │                     │  analysis iteratively
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  5. Output Format    │  Structure final output
                    │     Control         │  (report, table, JSON)
                    └─────────┴───────────┘
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | Step-Back Prompting | Research questions are often narrow; stepping back surfaces the broader context and first principles needed for thorough analysis |
| 2 | Chain-of-Thought | Complex research requires multi-step reasoning — connecting evidence, comparing sources, building arguments |
| 3 | Chain-of-Verification | Research outputs are prone to hallucination; CoVe systematically generates and answers verification questions |
| 4 | Self-Refine | First drafts of analysis benefit from iterative critique on completeness, accuracy, and nuance |
| 5 | Output Format Control | Research deliverables need consistent structure — sections, citations, tables, executive summaries |

## Step-by-Step Templates

### Step 1: Step-Back Prompting

**Purpose:** Before diving into the specific research question, extract the higher-level principles and background knowledge needed.

```
You are a research methodologist. Before answering the specific question below,
first identify the broader principles, frameworks, and background knowledge
needed to answer it thoroughly.

SPECIFIC QUESTION:
{user_question}

Step 1 — Identify the high-level concepts:
- What field(s) does this question belong to?
- What are the foundational principles relevant here?
- What background context would a domain expert consider essential?

Step 2 — Now answer the specific question using those principles as your foundation.
```

### Step 2: Chain-of-Thought Reasoning

**Purpose:** Work through the research question systematically, connecting evidence and building the argument.

```
Using the background principles identified above, now conduct a thorough
analysis of the research question. Think step by step.

BACKGROUND PRINCIPLES:
{step_back_output}

RESEARCH QUESTION:
{user_question}

Work through this systematically:
1. Define the scope and key terms
2. Identify the major dimensions/factors to examine
3. For each dimension, analyze the evidence
4. Identify patterns, contradictions, and gaps
5. Synthesize findings into a coherent narrative
6. State your conclusions with confidence levels

Show your reasoning at each step.
```

### Step 3: Chain-of-Verification

**Purpose:** Generate targeted verification questions and fact-check the analysis.

```
Review the following research analysis and identify claims that need verification.

ANALYSIS:
{cot_output}

Step 1 — List all factual claims, statistics, dates, and attributions made.

Step 2 — For each claim, generate a specific verification question:
  - "Is it true that [specific claim]?"
  - "What is the actual [statistic/date/attribution]?"

Step 3 — Answer each verification question independently (without looking at the
original analysis).

Step 4 — Compare your independent answers to the original claims. Flag any
discrepancies or unverifiable claims.

Step 5 — Produce a corrected version of the analysis, noting:
  - CONFIRMED: claims verified as accurate
  - CORRECTED: claims that needed updating
  - UNCERTAIN: claims that could not be verified
```

### Step 4: Self-Refine

**Purpose:** Iteratively improve the verified analysis for completeness, clarity, and nuance.

```
You are a senior research reviewer. Critique the following analysis, then
produce an improved version.

ANALYSIS:
{cove_output}

CRITIQUE DIMENSIONS:
1. Completeness — Are there missing perspectives, counterarguments, or evidence?
2. Accuracy — Are claims properly qualified? Are confidence levels appropriate?
3. Depth — Is the analysis superficial anywhere? Where could it go deeper?
4. Balance — Are multiple viewpoints represented fairly?
5. Clarity — Is the argument structure logical and easy to follow?
6. Actionability — Does the conclusion lead to clear next steps or recommendations?

First, provide your critique. Then produce a revised version that addresses
every issue identified.
```

### Step 5: Output Format Control

**Purpose:** Structure the final deliverable in the requested format.

```
Format the following research analysis into a structured report.

REFINED ANALYSIS:
{self_refine_output}

OUTPUT FORMAT:
## Executive Summary
(3-5 sentences capturing the key findings)

## Background & Context
(The step-back principles and framing)

## Methodology
(How the analysis was conducted)

## Findings
### Finding 1: {title}
(Evidence, analysis, confidence level)

### Finding 2: {title}
(Evidence, analysis, confidence level)

[Continue for all major findings]

## Discussion
(Patterns, contradictions, implications)

## Limitations
(What this analysis cannot address, uncertainties)

## Recommendations
(Numbered, actionable recommendations)

## Sources & References
(All cited sources with links where available)
```

## Walk-Through Example

**Task:** "Analyze the impact of mixture-of-experts (MoE) architectures on LLM scaling efficiency from 2022-2025."

---

### Step 1 Output: Step-Back

> **Broader principles identified:**
> - Scaling laws for neural language models (Kaplan et al. 2020, Chinchilla)
> - Conditional computation and sparse models (Shazeer et al. 2017)
> - The compute-efficiency frontier: achieving target quality with minimum FLOPs
> - Dense vs. sparse parameter counts and their distinct scaling behaviors
>
> **Background context:** MoE is a conditional computation paradigm where only a subset of model parameters ("experts") activate per input token, governed by a routing mechanism. This decouples total parameter count from per-inference compute cost...

### Step 2 Output: Chain-of-Thought

> **Scope:** MoE architectures in transformer-based LLMs, 2022-2025.
>
> **Dimension 1: Compute efficiency.** The core promise of MoE is that you can increase model capacity (parameters) without proportionally increasing FLOPs. Mixtral 8x7B demonstrated that an MoE model with ~47B total parameters but ~13B active parameters could match or exceed dense models of similar active parameter count...
>
> **Dimension 2: Routing mechanisms.** Early top-k routing suffered from load imbalance. Recent work on expert-choice routing (Zhou et al. 2022), hash routing, and learned routing has improved utilization...
>
> **Dimension 3: Training stability.** MoE training remains more fragile than dense training. Switch Transformer showed that simplified routing (top-1) could stabilize training...
>
> [Continues through all dimensions]

### Step 3 Output: Chain-of-Verification

> **Claim:** "Mixtral 8x7B has ~47B total parameters with ~13B active."
> **Verification:** Mixtral 8x7B uses 8 experts per layer with top-2 routing. Each expert has ~7B parameters total across all layers. Active parameters per token are ~13B. Total parameters are ~46.7B. **CONFIRMED** (minor rounding).
>
> **Claim:** "Expert-choice routing was introduced by Zhou et al. 2022."
> **Verification:** The paper "Mixture-of-Experts with Expert Choice Routing" by Zhou et al. appeared in NeurIPS 2022. **CONFIRMED.**
>
> [Continues for all claims]

### Step 4 Output: Self-Refine

> **Critique:**
> 1. *Completeness:* Missing discussion of inference serving challenges (memory bandwidth for loading all experts).
> 2. *Balance:* Overly optimistic about MoE — should include failure modes and cases where dense models remain preferred.
> 3. *Depth:* The routing mechanism section could benefit from quantitative comparisons.
>
> **Revised analysis:** [Improved version incorporating all critique points]

### Step 5 Output: Formatted Report

> ## Executive Summary
> Mixture-of-experts architectures have emerged as the dominant approach to compute-efficient LLM scaling between 2022 and 2025. By activating only a fraction of total parameters per token, MoE models achieve 2-4x compute savings at equivalent quality...
>
> [Full structured report follows]

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **Speed priority** | Skip Self-Refine (step 4); use single-pass CoVe |
| **Maximum rigor** | Add Self-Consistency to step 2 (sample 3 CoT paths, vote on findings) |
| **With external sources** | Insert a RAG retrieval step between Step-Back and CoT |
| **Collaborative review** | Replace Self-Refine with Multi-Agent Debate (3 reviewer personas) |
| **Budget-constrained** | Replace CoVe with Checklist Prompting for lightweight verification |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| Step-Back | 1 | ~500 output | Low |
| CoT | 1 | ~1500 output | Medium |
| CoVe | 3-4 | ~2000 output | Medium |
| Self-Refine | 2-3 | ~2000 output | Medium |
| Output Format | 1 | ~1000 output | Low |
| **Total** | **8-10** | **~7000 tokens** | **~30-60s** |
