---
id: corrective-rag
name: "Corrective RAG (CRAG)"
aliases: ["CRAG", "Corrective Retrieval-Augmented Generation"]
category: verification
family: grounding
year: 2024
authors: ["Shi-Qi Yan", "Jia-Chen Gu", "Yun Zhu", "Zhen-Hua Ling"]
paper: "https://arxiv.org/abs/2401.15884"
paper_title: "Corrective Retrieval Augmented Generation"
venue: "arXiv 2024"
code: null

complexity: medium
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: true
requires_training: false
model_agnostic: true

best_for: ["improving RAG quality when retrieval is unreliable", "open-domain QA with web fallback", "knowledge-intensive tasks requiring high accuracy", "systems with access to both static corpus and web search", "reducing hallucination from poor retrieval"]
avoid_when: ["retrieval is consistently high quality", "no access to web search as a fallback", "extremely low-latency requirements", "simple tasks where retrieval is unnecessary"]
composes_with: ["retrieval-augmented-generation", "chain-of-note", "grounding-via-sources", "self-refine", "chain-of-thought"]

tags: ["rag", "corrective", "retrieval-evaluation", "web-search", "grounding", "knowledge-refinement"]
---

# Corrective RAG (CRAG)

> **One-line summary:** CRAG evaluates the quality of retrieved documents using a lightweight retrieval evaluator, and when documents are deemed incorrect or ambiguous, triggers corrective actions including web search and knowledge refinement to ensure high-quality grounded generation.

## Overview

Corrective RAG (CRAG) addresses the Achilles' heel of standard RAG systems: blind trust in retrieved documents. In typical RAG pipelines, if the retriever returns irrelevant, outdated, or incorrect documents, the generator has no mechanism to detect this and will dutifully incorporate the bad information into its response. CRAG introduces an explicit retrieval quality evaluation step and a corrective action framework that activates when the initial retrieval is deemed insufficient.

The system works by classifying retrieved documents into three categories -- Correct, Incorrect, or Ambiguous -- using a lightweight retrieval evaluator. Based on this assessment, CRAG takes different corrective actions: if the retrieval is Correct, the documents are refined to extract the most relevant information before generation; if Incorrect, the system falls back to web search to find better sources; if Ambiguous (partially relevant), the system combines both the refined original documents and web search results. This tri-level response ensures that the generator always has the best available information.

Developed by Yan et al. in 2024, CRAG also introduces a "knowledge refinement" step that decomposes retrieved documents into fine-grained knowledge strips and filters them for relevance. This prevents the common failure mode where a relevant document contains mostly irrelevant content (e.g., a long Wikipedia article where only one sentence answers the query). By stripping away noise before generation, CRAG significantly improves the signal-to-noise ratio of the information the generator works with.

## How It Works

1. **Initial Retrieval:** Standard retrieval (e.g., dense retrieval, BM25) returns top-K documents for the query from the primary corpus.

2. **Retrieval Evaluation:** A lightweight evaluator assesses the confidence that each retrieved document is relevant to the query. Documents are scored and the overall retrieval quality is classified as Correct (high confidence), Incorrect (low confidence), or Ambiguous (mixed confidence).

3. **Corrective Action:**
   - **If Correct:** Proceed to knowledge refinement with retrieved documents.
   - **If Incorrect:** Discard retrieved documents and perform web search for better sources.
   - **If Ambiguous:** Combine knowledge-refined documents with web search results.

4. **Knowledge Refinement:** Relevant documents (from retrieval or web search) are decomposed into fine-grained "knowledge strips" (individual facts or sentences). Each strip is scored for relevance, and only high-relevance strips are retained.

5. **Grounded Generation:** The generator produces the final answer using only the refined, high-relevance knowledge strips as context.

### Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    Corrective RAG (CRAG)                       │
│                                                                │
│  ┌──────────┐     ┌───────────────┐                            │
│  │  Query    │────>│  Retrieve     │                            │
│  └──────────┘     │  top-K docs   │                            │
│                   └───────┬───────┘                            │
│                           v                                    │
│                   ┌───────────────────┐                         │
│                   │ Retrieval         │                         │
│                   │ Evaluator         │                         │
│                   │ (Confidence Score)│                         │
│                   └────────┬──────────┘                         │
│                            │                                   │
│              ┌─────────────┼─────────────┐                     │
│              v             v             v                     │
│        ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│        │ CORRECT  │  │ AMBIGUOUS│  │ INCORRECT│               │
│        │          │  │          │  │          │               │
│        │ Refine   │  │ Refine + │  │ Discard  │               │
│        │ docs     │  │ Web      │  │ docs →   │               │
│        │          │  │ Search   │  │ Web      │               │
│        │          │  │          │  │ Search   │               │
│        └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│             │             │             │                      │
│             └─────────────┼─────────────┘                      │
│                           v                                    │
│                   ┌───────────────────┐                         │
│                   │ Knowledge         │                         │
│                   │ Refinement        │                         │
│                   │ (decompose →      │                         │
│                   │  score strips →   │                         │
│                   │  filter)          │                         │
│                   └────────┬──────────┘                         │
│                            v                                   │
│                   ┌───────────────────┐                         │
│                   │ Generator         │                         │
│                   │ (uses refined     │                         │
│                   │  knowledge only)  │                         │
│                   └────────┬──────────┘                         │
│                            v                                   │
│                   ┌───────────────────┐                         │
│                   │ Final Answer      │                         │
│                   └───────────────────┘                         │
└────────────────────────────────────────────────────────────────┘
```

## Template

```
You are given a query and retrieved documents that have been evaluated
for quality. Follow the corrective RAG process.

QUERY: {query}

RETRIEVED DOCUMENTS:
{retrieved_documents}

STEP 1 — Evaluate Retrieval Quality:
For each document, assess whether it contains information relevant
to answering the query. Classify overall retrieval as:
- CORRECT: Documents clearly contain the answer
- AMBIGUOUS: Documents are partially relevant
- INCORRECT: Documents are not relevant to the query

Retrieval assessment: {correct/ambiguous/incorrect}

STEP 2 — Corrective Action:
If CORRECT: Extract relevant knowledge strips from documents.
If AMBIGUOUS: Extract what you can + note what is missing (would
  need web search for: {missing_information}).
If INCORRECT: Indicate that web search is needed for: {search_query}.

STEP 3 — Knowledge Refinement:
From the available sources, extract individual factual statements
(knowledge strips) relevant to the query. Score each 1-5 for
relevance and retain only those scoring 4+.

Relevant knowledge strips:
1. {strip_1} (relevance: {score})
2. {strip_2} (relevance: {score})
...

STEP 4 — Generate Answer:
Using only the refined knowledge strips above, answer the query.
Do not introduce information not present in the strips.

Answer:
```

## Examples

### Example 1: Correct Retrieval (Refinement Only)

**Input:**
```
QUERY: What is the boiling point of ethanol?

RETRIEVED DOCUMENTS:
[Doc 1]: "Ethanol (C2H5OH) is a volatile, flammable, colorless liquid
with a slight characteristic odor. It has a boiling point of 78.37°C
(173.1°F) at standard atmospheric pressure. Ethanol is widely used as
a solvent, fuel additive, and the intoxicating ingredient in alcoholic
beverages. It is produced by fermentation of sugars by yeast. Ethanol
has a molecular weight of 46.07 g/mol and a density of 0.789 g/cm3."
```

**Output:**
```
STEP 1 — Retrieval Assessment: CORRECT
Doc 1 explicitly contains the boiling point of ethanol.

STEP 2 — No corrective action needed.

STEP 3 — Knowledge Refinement:
Knowledge strips from Doc 1:
1. "Ethanol has a boiling point of 78.37°C (173.1°F) at standard
   atmospheric pressure." (relevance: 5)
2. "Ethanol (C2H5OH) is a volatile, flammable, colorless liquid."
   (relevance: 2 — descriptive but not answering the question)
3. "Ethanol has a molecular weight of 46.07 g/mol." (relevance: 1)

Retained: Strip 1 only.

STEP 4 — Answer:
The boiling point of ethanol is 78.37°C (173.1°F) at standard
atmospheric pressure.
```

### Example 2: Incorrect Retrieval (Web Search Fallback)

**Input:**
```
QUERY: Who won the 2024 Academy Award for Best Picture?

RETRIEVED DOCUMENTS:
[Doc 1]: "The Academy Awards, or Oscars, are the most prestigious awards
in the film industry. The ceremony has been held annually since 1929.
The award is presented by the Academy of Motion Picture Arts and Sciences."

[Doc 2]: "In 2023, 'Everything Everywhere All at Once' won the Academy
Award for Best Picture at the 95th ceremony, along with six other awards
including Best Director for Daniel Kwan and Daniel Scheinert."
```

**Output:**
```
STEP 1 — Retrieval Assessment: INCORRECT
Doc 1 describes the Oscars generally but has no 2024 winner information.
Doc 2 discusses the 2023 winner, not 2024. Neither document answers
the query about the 2024 ceremony.

STEP 2 — Corrective Action:
Web search needed for: "2024 Academy Award Best Picture winner 96th Oscars"

[Web search results]:
"Oppenheimer won Best Picture at the 96th Academy Awards held on
March 10, 2024. The film, directed by Christopher Nolan, also won
Best Director, Best Actor (Cillian Murphy), and four other awards."

STEP 3 — Knowledge Refinement:
1. "Oppenheimer won Best Picture at the 96th Academy Awards on
   March 10, 2024." (relevance: 5)
2. "Directed by Christopher Nolan." (relevance: 3)
3. "Also won Best Director, Best Actor (Cillian Murphy)."
   (relevance: 2 — related but not asked)

Retained: Strip 1.

STEP 4 — Answer:
Oppenheimer won the 2024 Academy Award for Best Picture at the 96th
Academy Awards ceremony held on March 10, 2024.
```

### Example 3: Ambiguous Retrieval (Combined Sources)

**Input:**
```
QUERY: What are the health benefits and recommended daily intake of
vitamin D?

RETRIEVED DOCUMENTS:
[Doc 1]: "Vitamin D is essential for calcium absorption and bone health.
Deficiency can lead to rickets in children and osteomalacia in adults.
The vitamin is produced in the skin upon exposure to UVB radiation."

[Doc 2]: "A 2022 meta-analysis found that vitamin D supplementation
reduced the risk of respiratory infections by 12% and may have modest
benefits for mood regulation, though evidence for cancer prevention
remains inconclusive."
```

**Output:**
```
STEP 1 — Retrieval Assessment: AMBIGUOUS
Documents cover health benefits well but do not include recommended
daily intake values.

STEP 2 — Corrective Action:
Refine existing documents for benefits + web search for:
"recommended daily intake vitamin D IU adults"

[Web search results]:
"The NIH recommends 600 IU (15 mcg) daily for adults aged 19-70
and 800 IU (20 mcg) for adults over 70. The Endocrine Society
suggests higher intakes of 1,500-2,000 IU for adults at risk of
deficiency."

STEP 3 — Knowledge Refinement:
From retrieved docs:
1. "Vitamin D is essential for calcium absorption and bone health."
   (relevance: 5)
2. "Deficiency can lead to rickets in children and osteomalacia in
   adults." (relevance: 4)
3. "Vitamin D supplementation reduced respiratory infection risk
   by 12%." (relevance: 4)

From web search:
4. "NIH recommends 600 IU daily for adults 19-70, 800 IU for 70+."
   (relevance: 5)
5. "Endocrine Society suggests 1,500-2,000 IU for at-risk adults."
   (relevance: 4)

STEP 4 — Answer:
Vitamin D provides several health benefits:
- Essential for calcium absorption and bone health; deficiency causes
  rickets (children) and osteomalacia (adults)
- Supplementation reduces respiratory infection risk by approximately
  12% according to meta-analysis

Recommended daily intake:
- Adults aged 19-70: 600 IU (15 mcg) per the NIH
- Adults over 70: 800 IU (20 mcg)
- Adults at risk of deficiency: 1,500-2,000 IU per the Endocrine Society
```

## When to Use

- RAG systems where retrieval quality is inconsistent or unpredictable
- Applications with access to both a primary knowledge base and web search as fallback
- Open-domain QA where the primary corpus may not cover all queries
- High-accuracy requirements where blindly trusting retrieval is unacceptable
- Systems serving diverse query types (some in-corpus, some out-of-corpus)

## When to Avoid

- When retrieval is consistently high-quality (the evaluation step adds overhead without benefit)
- No access to web search or alternative knowledge sources for the corrective fallback
- Extremely latency-sensitive applications where the evaluation + potential web search adds too much delay
- Simple tasks where retrieval is not needed at all
- When the corrective action (web search) might introduce its own quality issues (e.g., unreliable web sources)

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 1.5-3x base | Evaluation + potential web search + refinement |
| Latency | 1.5-3x baseline | Evaluation step + conditional web search |
| Quality gain | +8-15% | On PopQA, TriviaQA compared to standard RAG |
| Retrieval efficiency | Adaptive | Only does web search when primary retrieval fails |
| Knowledge strips | 60-80% filtered | Typical reduction from refinement step |

## Variants

- **CRAG-Lite:** Simpler binary evaluation (good/bad retrieval) without the ambiguous category. Faster but less nuanced.
- **Multi-Source CRAG:** Instead of just web search fallback, routes to different specialized sources (medical database, legal corpus, etc.) based on query type.
- **Iterative CRAG:** If web search results are also unsatisfactory, iterates with refined queries until quality threshold is met.
- **Cached CRAG:** Caches retrieval evaluations for common query patterns, reducing repeated evaluation overhead.

## Composability

- **CRAG + Chain-of-Note:** Use CoN to generate reading notes that inform the retrieval evaluation step, providing more nuanced quality assessment.
- **CRAG + Grounding via Sources:** After knowledge refinement, format the answer with citations to the specific knowledge strips used.
- **CRAG + Chain-of-Thought:** Use CoT reasoning in the final generation step to produce well-reasoned answers from the refined knowledge.
- **CRAG + Self-Refine:** After initial CRAG generation, use Self-Refine to iteratively improve the answer quality.
- **CRAG + Self-RAG:** Combine CRAG's external evaluation with Self-RAG's internal reflection tokens for a comprehensive quality control system.

## Limitations

- The retrieval evaluator's accuracy directly limits the system's effectiveness; misclassifying good retrieval as bad (or vice versa) degrades performance
- Web search fallback assumes web sources are more reliable than the primary corpus, which is not always true
- Knowledge refinement may discard relevant information if the decomposition is too aggressive
- The multi-stage pipeline increases system complexity and potential failure points
- Latency increases are significant when web search is triggered, creating variable response times
- The system cannot self-correct if both the primary retrieval and web search fail to surface relevant information
- Requires careful calibration of the confidence thresholds for Correct/Ambiguous/Incorrect classification

## Sources

- **Primary:** [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884) — Yan et al., 2024
- **Related:** [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511) — Asai et al., 2023
- **Related:** [Active Retrieval Augmented Generation](https://arxiv.org/abs/2305.06983) — Jiang et al., 2023
- **Related:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al., 2020
