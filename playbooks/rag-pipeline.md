# Playbook: RAG Pipeline

> **Pipeline:** Context Engineering → Chain-of-Note → Corrective RAG → Self-RAG
>
> **Best for:** Knowledge-grounded QA, document-based chatbots, enterprise search, technical documentation assistants, legal/medical research, customer support with knowledge bases.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │   User Query        │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. Context          │  Engineer the retrieval
                    │     Engineering     │  context window
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Chain-of-Note    │  Evaluate relevance of
                    │     (CoN)           │  each retrieved document
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Corrective RAG   │  Assess retrieval quality;
                    │     (CRAG)          │  trigger web search if poor
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Self-RAG         │  Generate with self-
                    │                     │  reflection tokens
                    └─────────┴───────────┘
                              │
                         ┌────▼──────┐
                         │ Grounded? │──No──→ Re-retrieve
                         └────┬──────┘        or abstain
                              │ Yes
                              ▼
                         Final Answer
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | Context Engineering | The quality of the retrieved context determines the ceiling of the answer — careful chunking, metadata injection, query transformation, and context ordering maximize signal-to-noise |
| 2 | Chain-of-Note | Before generating, evaluate each retrieved document with a structured note assessing its relevance — this prevents the model from being misled by superficially relevant but actually irrelevant passages |
| 3 | Corrective RAG | When retrieved documents score poorly on relevance, CRAG triggers corrective actions — web search fallback, query reformulation, or knowledge refinement — rather than generating from weak context |
| 4 | Self-RAG | During generation, the model self-reflects on whether it needs retrieval, whether retrieved passages support its claims, and whether the output is grounded — producing calibrated, cited answers |

## Step-by-Step Templates

### Step 1: Context Engineering

**Purpose:** Transform the user query, retrieve documents, and engineer the context window for maximum answer quality.

```
CONTEXT ENGINEERING PIPELINE:

Phase 1 — Query Analysis and Transformation:
Original query: {user_query}

a) Classify query type:
   - Factual lookup / Multi-hop reasoning / Comparative analysis /
     Procedural / Opinion-seeking

b) Generate search queries (up to 3 variations):
   - Rewrite 1: {semantic_rewrite} (broader/alternative phrasing)
   - Rewrite 2: {specific_rewrite} (more precise/technical terms)
   - Rewrite 3: {decomposed_subquery} (if multi-hop, break into parts)

c) Identify required context metadata:
   - Time sensitivity: {does answer change over time?}
   - Source authority: {what sources are most authoritative?}
   - Scope: {what should be included/excluded?}

Phase 2 — Retrieval (executed by retrieval system):
[Retrieve top-K documents for each query variation]

Phase 3 — Context Window Construction:
Arrange retrieved documents in this order:
1. Most relevant documents first (recency/relevance scored)
2. Include source metadata: [SOURCE: {title} | DATE: {date} | RELEVANCE: {score}]
3. Deduplicate overlapping passages
4. Total context budget: {max_context_tokens} tokens
5. Reserve {answer_budget} tokens for the answer

CONSTRUCTED CONTEXT:
<context>
[Document 1 — relevance: {score}]
{passage_1}

[Document 2 — relevance: {score}]
{passage_2}

[Document N — relevance: {score}]
{passage_n}
</context>
```

### Step 2: Chain-of-Note

**Purpose:** Evaluate each retrieved document's relevance and utility before generating the answer.

```
You are a research librarian evaluating retrieved documents for relevance
to a user's question. For each document, write a structured reading note.

QUESTION: {user_query}

RETRIEVED DOCUMENTS:
{context_documents}

For each document, write a note:

DOCUMENT 1: "{title_or_id}"
- RELEVANCE: [Directly relevant | Partially relevant | Not relevant]
- KEY INFORMATION: What specific facts/claims in this document help
  answer the question?
- LIMITATIONS: What is this document missing or wrong about?
- CONFIDENCE: How reliable is this source? [High | Medium | Low]
- QUOTE: The single most useful passage (verbatim).

[Repeat for each document]

SYNTHESIS NOTE:
- Which documents together provide a complete answer?
- Are there contradictions between documents? If so, which is more
  authoritative and why?
- What information is STILL MISSING after reviewing all documents?
- Overall retrieval quality: [Sufficient | Partial | Insufficient]
```

### Step 3: Corrective RAG

**Purpose:** Based on the Chain-of-Note assessment, take corrective action if retrieval quality is insufficient.

```
Based on the document evaluation below, determine whether the retrieved
context is sufficient to answer the question accurately.

QUESTION: {user_query}
RETRIEVAL QUALITY ASSESSMENT: {chain_of_note_output}

DECISION TREE:

IF overall retrieval quality is "Sufficient":
  → Proceed to generation with current context
  → Action: GENERATE

IF overall retrieval quality is "Partial":
  → Refine the query and retrieve additional documents
  → Generate a refined search query targeting the missing information
  → Action: REFINE_AND_RETRIEVE
  → Refined query: "{refined_query}"

IF overall retrieval quality is "Insufficient":
  → Fall back to web search for fresh information
  → Action: WEB_SEARCH
  → Web query: "{web_search_query}"
  → After web results, re-run Chain-of-Note on combined context

IF the question is unanswerable even with web search:
  → Action: ABSTAIN
  → Response: "I don't have sufficient information to answer this
    question reliably. Here's what I found: {partial_findings}.
    For a definitive answer, consult {recommended_source}."

CORRECTIVE ACTION TAKEN: {action}

CORRECTED CONTEXT (if retrieval was refined):
{updated_context}
```

### Step 4: Self-RAG

**Purpose:** Generate the answer with built-in self-reflection on retrieval necessity, passage support, and output grounding.

```
Generate an answer to the following question using the provided context.
At each stage, reflect on the quality of your generation.

QUESTION: {user_query}

VERIFIED CONTEXT:
{corrected_context}

DOCUMENT NOTES:
{chain_of_note_output}

GENERATION WITH SELF-REFLECTION:

[Retrieve] Do I need additional retrieval to answer this question?
  → {yes_retrieve_more | no_sufficient_context}

[Generate] Answer the question using ONLY information from the context:
{generated_answer}

[ISREL] For each claim in my answer, is it supported by a retrieved passage?
  - Claim 1: "{claim}" → Supported by Document {N}: "{quote}" [SUPPORTED]
  - Claim 2: "{claim}" → Not found in any document [UNSUPPORTED — remove or flag]
  - Claim 3: "{claim}" → Partially supported [PARTIAL — qualify the claim]

[ISUSE] Is each cited passage actually useful for this answer?
  - Document {N}: [USEFUL | NOT USEFUL — remove citation]

[ISGRD] Is my complete answer grounded in the retrieved documents?
  → {fully_grounded | partially_grounded | not_grounded}

If partially or not grounded:
  → Remove unsupported claims
  → Add qualifiers ("Based on the available documents...")
  → Flag gaps: "Note: I could not find information about {gap}"

FINAL GROUNDED ANSWER:
{final_answer_with_citations}

CONFIDENCE: {high | medium | low}
SOURCES: [{source_1}, {source_2}, ...]
```

## Walk-Through Example

**Task:** "What are the best practices for chunking strategies in RAG pipelines, and how does chunk size affect retrieval quality?"

---

### Step 1 Output: Context Engineering

> **Query analysis:**
> - Type: Procedural + Comparative analysis
> - Search queries generated:
>   1. "RAG chunking strategies best practices 2024 2025"
>   2. "chunk size impact retrieval quality embedding search"
>   3. "semantic chunking vs fixed-size chunking comparison"
>
> **Retrieval:** 8 documents retrieved across the 3 queries, deduplicated to 6 unique passages.
>
> **Context window:** 6 passages ordered by relevance, totaling ~3200 tokens, with 1800 tokens reserved for the answer.

### Step 2 Output: Chain-of-Note

> **Document 1** (LangChain docs — chunking guide):
> - RELEVANCE: Directly relevant
> - KEY INFO: Lists 5 chunking strategies with trade-offs
> - CONFIDENCE: Medium (vendor docs, may be biased toward their tools)
>
> **Document 2** (research paper on chunk size vs. recall):
> - RELEVANCE: Directly relevant
> - KEY INFO: Empirical data showing 256-512 tokens is optimal for most embedding models
> - CONFIDENCE: High (peer-reviewed)
>
> **Document 3** (blog post about semantic chunking):
> - RELEVANCE: Partially relevant — focuses only on semantic chunking
> - KEY INFO: Describes how semantic chunking preserves meaning boundaries
> - CONFIDENCE: Medium
>
> **SYNTHESIS:** Documents 1+2+3 provide a comprehensive answer. Missing: impact of overlapping chunks and multi-vector retrieval strategies.
> **Overall retrieval quality: Partial** (missing overlap and multi-vector info).

### Step 3 Output: Corrective RAG

> **Decision: REFINE_AND_RETRIEVE**
> **Refined query:** "chunk overlap sliding window impact on RAG retrieval recall"
> **Additional retrieval:** 2 new documents about overlapping windows and parent-child chunk strategies.
> **Updated context:** 8 passages, retrieval quality now assessed as Sufficient.

### Step 4 Output: Self-RAG

> **Generated answer with self-reflection:**
>
> Best practices for RAG chunking strategies include:
>
> 1. **Size selection (256-512 tokens)** — Empirical studies show this range maximizes recall for most embedding models [SUPPORTED: Document 2].
>
> 2. **Semantic chunking** — Split on meaning boundaries (paragraphs, sections) rather than fixed character counts [SUPPORTED: Documents 1, 3].
>
> 3. **Overlapping windows (10-20%)** — Add overlap between chunks to prevent information loss at boundaries [SUPPORTED: Document 7].
>
> 4. **Parent-child retrieval** — Retrieve small chunks for precision, then expand to parent chunks for context [SUPPORTED: Document 8].
>
> [ISREL check: All 4 claims supported. ISGRD: Fully grounded.]
>
> **Confidence: High**
> **Sources: [Doc 1, Doc 2, Doc 3, Doc 7, Doc 8]**

## Decision Points

```
                          ┌──────────────────┐
                          │ RAG query         │
                          └──────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Is the knowledge base    │
                    │ high-quality and curated?│
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   Skip CRAG         Full pipeline
                   (trust retrieval) (include CRAG)
                         │
                    ┌────▼───────────────────┐
                    │ Are retrieved docs       │
                    │ potentially noisy?       │
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   Chain-of-Note     Direct generation
                   (evaluate docs)   with context
                         │
                    ┌────▼───────────────────┐
                    │ Is hallucination risk    │
                    │ high (medical, legal)?   │
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   Self-RAG with     Standard RAG
                   full reflection   generation
```

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **Low latency** | Skip CoN and CRAG; use direct generation with context stuffing |
| **Maximum accuracy** | Add CoVe after Self-RAG to verify all citations; add Self-Consistency (3 generations, take consensus) |
| **Conversational** | Add Memory Prompting for multi-turn context; use Thread-of-Thought for long conversation histories |
| **Multi-index** | Add query routing before Context Engineering to select the right index/collection |
| **Agentic RAG** | Wrap entire pipeline in ReAct loop — agent decides when to retrieve, what to retrieve, and when to stop |
| **Hybrid search** | Extend Context Engineering with both dense (embedding) and sparse (BM25/keyword) retrieval, then fuse results |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| Context Engineering | 1-2 | ~500 output | Low-Medium |
| Chain-of-Note | 1 | ~1000 output | Medium |
| Corrective RAG | 0-2 | ~500 output | Low-Medium |
| Self-RAG | 1-2 | ~1500 output | Medium |
| **Total** | **3-7** | **~3500 tokens** | **~15-45s** |
