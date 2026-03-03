---
id: self-rag
name: "Self-RAG"
aliases: ["Self-Reflective RAG", "Self-Reflective Retrieval-Augmented Generation"]
category: verification
family: grounding
year: 2023
authors: ["Akari Asai", "Zeqiu Wu", "Yizhong Wang", "Avirup Sil", "Hannaneh Hajishirzi"]
paper: "https://arxiv.org/abs/2310.11511"
paper_title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
venue: "ICLR 2024"
code: "https://github.com/AkariAsai/self-rag"

complexity: high
token_cost: medium
latency: medium
num_calls: variable

requires_examples: false
requires_tools: true
requires_training: true
model_agnostic: false

best_for: ["knowledge-intensive question answering", "fact verification", "long-form generation requiring factual accuracy", "tasks requiring adaptive retrieval decisions", "open-domain QA with diverse query types"]
avoid_when: ["creative writing where factual grounding is unnecessary", "tasks where retrieval is always or never needed", "environments without retrieval infrastructure", "when fine-tuning is not feasible"]
composes_with: ["chain-of-thought", "chain-of-note", "grounding-via-sources", "chain-of-verification"]

tags: ["rag", "self-reflection", "retrieval", "grounding", "reflection-tokens", "fine-tuning", "adaptive"]
---

# Self-RAG

> **One-line summary:** Self-RAG trains an LLM to adaptively decide when to retrieve, evaluate the relevance of retrieved passages, and assess whether its own generation is supported by the evidence, using special reflection tokens that enable self-regulated retrieval-augmented generation.

## Overview

Self-RAG fundamentally rethinks how retrieval-augmented generation should work. Standard RAG retrieves documents for every query regardless of whether retrieval is actually needed, and blindly incorporates retrieved content without evaluating its quality or relevance. Self-RAG instead trains the model to make these decisions itself using special "reflection tokens" that are generated inline during text generation.

The model learns four types of reflection tokens: (1) **Retrieve** -- whether retrieval is needed for the current generation step; (2) **IsRel** -- whether a retrieved passage is relevant to the query; (3) **IsSup** -- whether the generated text is supported by the retrieved passage; and (4) **IsUse** -- whether the generated text is a useful response to the query overall. These tokens are learned during fine-tuning using a critic model that annotates training data, allowing the generator to internalize the reflection capability.

Developed by Asai et al. and presented at ICLR 2024, Self-RAG achieved state-of-the-art results on multiple open-domain QA and fact verification benchmarks, outperforming both standard RAG approaches and proprietary models like ChatGPT on several tasks. The key advantage is adaptive retrieval: the model retrieves only when needed, evaluates what it retrieves, and verifies its own generations against the evidence. This produces higher-quality outputs while avoiding the failure modes of retrieving irrelevant content or generating unsupported claims.

## How It Works

1. **Retrieval Decision:** During generation, the model outputs a special `[Retrieve]` token indicating whether it needs external information to continue. If `[Retrieve=Yes]`, the system queries the retrieval engine; if `[Retrieve=No]`, the model continues generating from its parametric knowledge.

2. **Passage Retrieval:** When retrieval is triggered, the retriever returns top-K passages. The model generates a continuation for each retrieved passage in parallel.

3. **Relevance Assessment:** For each retrieved passage, the model generates an `[IsRel]` token indicating whether the passage is relevant to the query. Irrelevant passages can be filtered out.

4. **Generation with Support Check:** The model generates text based on the relevant passages and outputs `[IsSup]` tokens indicating whether each generated segment is fully supported, partially supported, or unsupported by the passage.

5. **Utility Assessment:** The model generates an `[IsUse]` token scoring the overall usefulness and quality of the complete response.

6. **Best Output Selection:** If multiple candidate outputs are generated (from different retrieved passages), the system selects the best one based on the reflection token scores, prioritizing supported and useful generations.

### Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                       Self-RAG Flow                          │
│                                                              │
│  ┌──────────┐                                                │
│  │  Query    │                                                │
│  └─────┬────┘                                                │
│        v                                                     │
│  ┌──────────────────┐                                        │
│  │ Generate...      │                                        │
│  │ [Retrieve=Yes?]  │──No──> Continue generating from        │
│  └────────┬─────────┘        parametric knowledge            │
│           │ Yes                                              │
│           v                                                  │
│  ┌──────────────────┐                                        │
│  │ Retrieve top-K   │                                        │
│  │ passages         │                                        │
│  └────────┬─────────┘                                        │
│    ┌──────┼──────┐                                           │
│    v      v      v                                           │
│  ┌────┐ ┌────┐ ┌────┐                                       │
│  │P_1 │ │P_2 │ │P_3 │  (passages)                           │
│  └──┬─┘ └──┬─┘ └──┬─┘                                       │
│     │      │      │                                          │
│     v      v      v                                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ For each passage:                                      │  │
│  │  [IsRel=?] → Generate text → [IsSup=?] → [IsUse=?]   │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         v                                    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Select best output based on:                         │    │
│  │   IsRel=Relevant ∧ IsSup=FullySupported ∧ IsUse=5   │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         v                                    │
│                ┌─────────────────┐                           │
│                │  Final Output   │                           │
│                └─────────────────┘                           │
└──────────────────────────────────────────────────────────────┘
```

## Template

```
Note: Self-RAG requires a fine-tuned model with reflection tokens.
The following illustrates the prompt structure the trained model uses
internally. For practical use, use the fine-tuned Self-RAG model.

---

Instruction: {query}

[Retrieve] {yes/no}

[If yes, for each retrieved passage:]
Retrieved passage: {passage_text}
[IsRel] {relevant/irrelevant}

Generated response segment: {generated_text}
[IsSup] {fully_supported/partially_supported/no_support}

[After complete generation:]
[IsUse] {1-5 utility score}

---

For prompt-only approximation (without fine-tuning):

Given the following query and retrieved passages, generate a response.
For each claim you make, assess:
1. Did you need the retrieved information, or could you answer from
   general knowledge?
2. Is the retrieved passage relevant to the query?
3. Is your generated text supported by the passage?
4. Is your overall response useful?

Query: {query}

Retrieved passages:
{passages}

Response (with inline assessments):
```

## Examples

### Example 1: Adaptive Retrieval (Retrieval Needed)

**Input:**
```
Query: What year did the Higgs boson discovery announcement occur?
```

**Self-RAG Internal Process:**
```
[Retrieve=Yes]  ← Model decides retrieval is needed for specific date

Retrieved passage: "On July 4, 2012, the ATLAS and CMS experiments at
CERN's Large Hadron Collider announced the discovery of a new particle
consistent with the Higgs boson, confirming a key prediction of the
Standard Model."

[IsRel=Relevant]  ← Passage directly addresses the question

Generated: "The Higgs boson discovery was announced on July 4, 2012,
by the ATLAS and CMS experiments at CERN."

[IsSup=Fully_Supported]  ← Generation matches passage content
[IsUse=5]  ← Response directly answers the question
```

**Output:**
```
The Higgs boson discovery was announced on July 4, 2012, by the
ATLAS and CMS experiments at CERN's Large Hadron Collider.
```

### Example 2: Adaptive Retrieval (No Retrieval Needed)

**Input:**
```
Query: What is the capital of France?
```

**Self-RAG Internal Process:**
```
[Retrieve=No]  ← Model decides this is common knowledge, no retrieval needed

Generated: "The capital of France is Paris."

[IsUse=5]  ← Response is correct and complete
```

**Output:**
```
The capital of France is Paris.
```

### Example 3: Handling Irrelevant Retrieval

**Input:**
```
Query: What is the half-life of Carbon-14?

Retrieved passages:
P1: "Carbon dating is used in archaeology to determine the age of
organic materials. The method was developed by Willard Libby in 1949."
P2: "Carbon-14 undergoes beta decay with a half-life of 5,730 years,
transforming into nitrogen-14."
P3: "The carbon cycle involves the exchange of carbon between the
atmosphere, biosphere, oceans, and geosphere."
```

**Self-RAG Internal Process:**
```
[Retrieve=Yes]

P1: [IsRel=Partially_Relevant]  ← Related topic but no half-life info
P2: [IsRel=Relevant]  ← Contains the specific answer
P3: [IsRel=Irrelevant]  ← About carbon cycle, not C-14 half-life

Generated (using P2): "The half-life of Carbon-14 is 5,730 years.
During this decay process, Carbon-14 transforms into Nitrogen-14
through beta decay."

[IsSup=Fully_Supported]  ← Matches P2 content exactly
[IsUse=5]
```

**Output:**
```
The half-life of Carbon-14 is 5,730 years. During this decay process,
Carbon-14 transforms into Nitrogen-14 through beta decay.
```

## When to Use

- Knowledge-intensive QA where retrieval relevance varies across queries
- Applications requiring high factual accuracy with verifiable sourcing
- Long-form generation where different sections may or may not need retrieval
- Systems where you want to minimize unnecessary retrieval calls (cost optimization)
- Fact verification tasks where evidence assessment is critical

## When to Avoid

- When fine-tuning is not feasible (Self-RAG requires trained reflection tokens)
- Creative writing or opinion tasks where grounding in sources is counterproductive
- When all queries uniformly require (or uniformly do not require) retrieval
- Environments without a retrieval system to query
- When model size or deployment constraints prevent using the fine-tuned model

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | Variable | Reflection tokens add ~10-20% when retrieving |
| Latency | Medium | Adaptive retrieval avoids unnecessary calls |
| Quality gain | +5-15% | Over standard RAG on PopQA, PubHealth, etc. |
| Training cost | Moderate | Fine-tuning with critic-annotated data |
| Retrieval efficiency | +30-50% fewer calls | Compared to always-retrieve RAG |

## Variants

- **Self-RAG-Lite:** Prompt-based approximation without fine-tuning. Less accurate reflection but no training required.
- **Self-RAG with Multiple Retrievers:** Uses different specialized retrievers (web, knowledge base, academic papers) and selects per-query.
- **Segment-Level Self-RAG:** Makes retrieval and support decisions at the paragraph level rather than the full-response level.
- **Self-RAG with Configurable Thresholds:** Allows adjusting the thresholds for retrieval, relevance, and support decisions at inference time.

## Composability

- **Self-RAG + Chain-of-Note:** Use CoN-style notes for passages that Self-RAG marks as partially relevant, extracting useful subsets.
- **Self-RAG + Chain-of-Thought:** Use CoT reasoning within the generation segments to improve reasoning quality between retrieval steps.
- **Self-RAG + Grounding via Sources:** Format the final output with explicit citations to the passages that received high IsSup scores.
- **Self-RAG + Chain-of-Verification:** After Self-RAG generates the response, CoVe can provide an additional verification layer.

## Limitations

- Requires fine-tuning, making it inaccessible for users of closed-source API-only models
- The critic model used for training data annotation may introduce biases
- Reflection token accuracy depends on the quality and diversity of training data
- The model may occasionally make incorrect retrieval decisions (retrieving when unnecessary or skipping when needed)
- Limited to the model architectures that were fine-tuned; not a drop-in enhancement for arbitrary LLMs
- The retrieval system's quality still fundamentally limits the quality of grounded information
- Training the reflection capability requires carefully curated datasets with critic annotations

## Sources

- **Primary:** [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511) — Asai et al., ICLR 2024
- **Code:** [github.com/AkariAsai/self-rag](https://github.com/AkariAsai/self-rag)
- **Related:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al., 2020
- **Related:** [Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models](https://arxiv.org/abs/2311.09210) — Yu et al., 2023
