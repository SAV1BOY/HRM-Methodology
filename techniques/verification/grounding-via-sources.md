---
id: grounding-via-sources
name: "Grounding via Sources"
aliases: ["Cite-then-Conclude", "Source-Grounded Generation", "Citation Prompting"]
category: verification
family: grounding
year: null
authors: []
paper: null
paper_title: null
venue: null
code: null

complexity: low
token_cost: medium
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["factual question answering with provided sources", "reducing hallucination in RAG pipelines", "report generation from documents", "evidence-based analysis", "attributable generation"]
avoid_when: ["no source documents available", "creative writing tasks", "questions beyond the provided sources", "tasks requiring speculation or prediction"]
composes_with: ["retrieval-augmented-generation", "chain-of-thought", "chain-of-verification", "few-shot-prompting"]

tags: ["grounding", "citation", "attribution", "factual-accuracy", "rag", "verification"]
---

# Grounding via Sources

> **One-line summary:** Grounding via Sources instructs the LLM to explicitly cite provided source materials before drawing conclusions, ensuring every claim in the output is traceable to a specific reference and reducing hallucination.

## Overview

Grounding via Sources implements a "cite-then-conclude" pattern that reverses the common LLM tendency to generate fluent but unsupported claims. Instead of asking the model to answer a question and then optionally cite sources, this technique structures the prompt so that the model must first identify relevant passages from provided source documents, explicitly quote or reference them, and only then draw conclusions based on the cited evidence. This makes hallucination structurally harder because every claim must be anchored to a specific source.

The technique is rooted in academic writing conventions where claims require citations, adapted for LLM interaction. It is particularly valuable in Retrieval-Augmented Generation (RAG) pipelines where the model receives retrieved documents alongside a query. Without explicit grounding instructions, models often ignore or loosely paraphrase retrieved content, still defaulting to their parametric knowledge (which may be incorrect or outdated). Grounding via Sources forces the model to treat the provided documents as the primary knowledge source.

This approach is one of the most practical and widely deployed verification techniques because it requires no additional model calls, no special infrastructure, and no training modifications. It simply restructures the prompt to enforce a discipline of evidence-based reasoning. The technique also makes outputs more trustworthy for users, who can verify the model's claims by checking the cited sources -- a critical requirement for enterprise and professional applications.

## How It Works

1. **Source Presentation:** Provide the model with numbered or labeled source documents alongside the question. Each source should have a clear identifier (e.g., [Source 1], [Document A]).

2. **Evidence Extraction Instruction:** Instruct the model to first identify and quote the specific passages from the sources that are relevant to the question.

3. **Cite-then-Conclude:** The model must cite the source identifier alongside each piece of evidence, then draw its conclusion based only on the cited evidence.

4. **Unsupported Claim Handling:** Instruct the model to explicitly state when a claim cannot be supported by the provided sources rather than generating unsupported information.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│              Grounding via Sources                       │
│                                                          │
│  ┌──────────┐  ┌─────────────────────────────────────┐   │
│  │  Query   │  │  Source Documents                    │   │
│  │          │  │  [1] "Revenue grew 15% YoY..."      │   │
│  │          │  │  [2] "Operating costs declined..."   │   │
│  │          │  │  [3] "Market share expanded to..."   │   │
│  └────┬─────┘  └──────────────┬──────────────────────┘   │
│       │                       │                          │
│       └───────────┬───────────┘                          │
│                   v                                      │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Step 1: Extract Relevant Evidence                 │  │
│  │  "According to [1], revenue grew 15%..."           │  │
│  │  "[2] states that operating costs declined..."     │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         v                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Step 2: Draw Conclusions from Cited Evidence      │  │
│  │  "Based on [1] and [2], profitability improved..." │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         v                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Step 3: Flag Unsupported Areas                    │  │
│  │  "The sources do not address future projections."  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Template

```
You are given source documents and a question. Your answer must be
grounded in the provided sources.

SOURCES:
[1] {source_1_text}
[2] {source_2_text}
[3] {source_3_text}

QUESTION: {question}

INSTRUCTIONS:
1. First, identify the relevant passages from the sources that relate
   to the question. Quote them with their source numbers.
2. Then, provide your answer citing the specific sources that support
   each claim using [N] notation.
3. If the sources do not contain information to answer part of the
   question, explicitly state: "The provided sources do not address
   this aspect."
4. Do NOT include information that is not supported by the provided
   sources.

EVIDENCE:
[List relevant quoted passages with source numbers]

ANSWER:
[Your source-grounded answer with inline citations]
```

## Examples

### Example 1: Financial Analysis

**Input:**
```
SOURCES:
[1] "Acme Corp reported Q3 2024 revenue of $4.2 billion, up 12% year-
over-year. The growth was driven primarily by the cloud services
division, which saw 28% growth."

[2] "Operating expenses for Q3 were $3.1 billion, a 5% increase from
Q3 2023. The company achieved an operating margin of 26.2%, compared
to 21.6% in the prior year quarter."

[3] "Acme Corp CEO Jane Smith stated: 'We expect continued momentum
in cloud services, though macroeconomic headwinds may moderate growth
in enterprise licensing.'"

QUESTION: How is Acme Corp performing financially, and what is the
outlook?
```

**Output:**
```
EVIDENCE:
- [1]: "Revenue of $4.2 billion, up 12% year-over-year" and "cloud
  services division, which saw 28% growth"
- [2]: "Operating margin of 26.2%, compared to 21.6% in the prior year"
  and "Operating expenses... a 5% increase"
- [3]: CEO expects "continued momentum in cloud services" but
  "macroeconomic headwinds may moderate growth in enterprise licensing"

ANSWER:
Acme Corp is performing strongly. Revenue grew 12% YoY to $4.2 billion
[1], with cloud services as the primary driver at 28% growth [1].
Profitability improved significantly, with operating margins expanding
from 21.6% to 26.2% [2], reflecting revenue growing faster than
expenses (revenue +12% vs. expenses +5%) [1][2].

The outlook is mixed: the CEO expressed confidence in continued cloud
services momentum but cautioned about potential headwinds in enterprise
licensing from macroeconomic conditions [3].

The provided sources do not address cash flow, debt levels, or specific
guidance figures for upcoming quarters.
```

### Example 2: Research Synthesis

**Input:**
```
SOURCES:
[1] "Smith et al. (2023) found that regular exercise (150+ minutes/week)
reduced the risk of cardiovascular disease by 35% in a cohort of 50,000
adults over 10 years."

[2] "The WHO recommends at least 150 minutes of moderate-intensity
aerobic activity per week for adults aged 18-64."

[3] "Johnson & Lee (2022) reported that combining exercise with
Mediterranean diet adherence reduced cardiovascular risk by 52%,
suggesting synergistic effects between physical activity and diet."

QUESTION: What does the evidence say about exercise and heart disease
prevention?
```

**Output:**
```
EVIDENCE:
- [1]: "regular exercise (150+ minutes/week) reduced the risk of
  cardiovascular disease by 35%" in a large cohort study
- [2]: WHO recommends "at least 150 minutes of moderate-intensity
  aerobic activity per week"
- [3]: "combining exercise with Mediterranean diet adherence reduced
  cardiovascular risk by 52%"

ANSWER:
The evidence strongly supports exercise as a protective factor against
cardiovascular disease. A large-scale study of 50,000 adults found that
exercising 150+ minutes per week reduced cardiovascular disease risk by
35% over 10 years [1]. This exercise threshold aligns with WHO
recommendations of at least 150 minutes of moderate-intensity aerobic
activity weekly [2].

The benefits may be amplified when exercise is combined with dietary
interventions. Research by Johnson & Lee found that pairing exercise
with Mediterranean diet adherence achieved a 52% risk reduction [3],
suggesting synergistic effects [3].

The provided sources do not address optimal exercise intensity, the
effects for specific age groups beyond 18-64, or the role of resistance
training specifically.
```

## When to Use

- RAG pipelines where retrieved documents should be the primary knowledge source
- Report generation from provided data or documents
- Legal, medical, or financial analysis where claims must be traceable
- Customer support responses that should cite product documentation
- Any application where users need to verify the model's claims
- When reducing hallucination is a top priority

## When to Avoid

- No source documents are available (the technique is meaningless without sources)
- Creative writing, brainstorming, or opinion tasks where grounding is counterproductive
- Questions that intentionally go beyond the provided sources
- When the model should use its parametric knowledge rather than being constrained to documents
- Tasks where the overhead of citation formatting is unnecessary

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | +20-40% | Citations and evidence extraction add tokens |
| Latency | Negligible | Single call, no extra round trips |
| Hallucination reduction | 40-70% | Highly effective when sources are relevant |
| Num calls | 1 | Everything in a single prompt |
| User trust | High | Verifiable citations build confidence |

## Variants

- **Inline Citation:** Citations are woven into the text naturally (e.g., "According to [1], revenue grew..."). Most readable.
- **Footnote Style:** Claims are numbered and citations are collected at the end. Better for formal documents.
- **Quote-then-Synthesize:** The model must quote exact passages before synthesizing, providing even stronger grounding.
- **Confidence-Annotated:** Each citation includes a confidence tag based on how directly the source supports the claim.
- **Multi-Source Triangulation:** The model is instructed to prefer claims supported by multiple sources.

## Composability

- **Grounding + RAG:** The natural pairing. RAG retrieves sources; Grounding via Sources ensures the model uses them faithfully.
- **Grounding + Chain-of-Thought:** Use CoT to reason about the evidence before drawing conclusions, making the reasoning process transparent and verifiable.
- **Grounding + Chain-of-Verification:** After grounding, verify that the citations actually support the claims made.
- **Grounding + Checklist Prompting:** Add a checklist verifying that all major claims have citations and no unsupported claims exist.

## Limitations

- Only works when relevant source documents are provided; cannot ground in absent information
- The model may cite sources selectively, ignoring contradictory evidence
- Quoted passages may be taken out of context, changing their meaning
- The model may fabricate citations that appear correct but do not actually match the source text
- Quality depends on the relevance and quality of the provided sources
- May refuse to answer legitimate questions if they go slightly beyond the literal source text (over-conservative)

## Sources

- **Primary:** Practical technique widely used in RAG systems and enterprise AI; no single originating paper
- **Related:** [ALCE: Automatic LLM Citation Evaluation](https://arxiv.org/abs/2305.14627) — Gao et al., 2023
- **Related:** [Attributed Question Answering: Evaluation and Modeling for Attributed Large Language Models](https://arxiv.org/abs/2212.08037) — Bohnet et al., 2022
- **Related:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al., 2020
