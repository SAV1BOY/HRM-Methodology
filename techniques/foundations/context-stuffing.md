---
id: context-stuffing
name: "Context Stuffing"
aliases:
  - context-stuffing
  - context-injection
  - context-grounding
  - document-grounding
  - retrieval-augmented-prompting
  - context-window-packing
category: foundations
family: grounding
year: 2020
authors:
  - Patrick Lewis
  - Ethan Perez
  - Aleksandra Piktus
  - Fabio Petroni
  - Vladimir Karpukhin
  - Naman Goyal
  - Heinrich Küttler
  - Mike Lewis
  - Wen-tau Yih
  - Tim Rocktäschel
  - Sebastian Riedel
  - Douwe Kiela
paper: "https://arxiv.org/abs/2005.11401"
paper_title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
venue: "NeurIPS 2020"
code: null
complexity: low
token_cost: variable
latency: low
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - grounding responses in specific documents
  - question answering over proprietary data
  - reducing hallucination on factual tasks
  - tasks requiring up-to-date information
  - domain-specific knowledge that is not in model training data
  - legal and compliance tasks requiring source attribution
avoid_when:
  - context documents are unreliable or contradictory
  - task requires pure creative generation
  - context volume exceeds context window capacity
  - model needs to reason beyond provided information
  - latency requirements preclude long prompts
composes_with:
  - zero-shot
  - few-shot
  - role-prompting
  - output-format
  - prompt-scaffolding
  - chain-of-thought
tags:
  - grounding
  - retrieval
  - RAG-foundation
  - context-window
  - factual-accuracy
  - foundational
---

# Context Stuffing

> **One-line summary:** Inject relevant documents, data, or reference material directly into the prompt before the task instruction, grounding the model's response in specific provided information rather than its parametric knowledge alone.

## Overview

Context stuffing is the foundational grounding technique in prompt engineering: the practice of including relevant text, data, or documents directly in the prompt so the model can reference them when generating its response. This technique is the conceptual predecessor and runtime mechanism of Retrieval-Augmented Generation (RAG), formalized by Lewis et al. (2020). While RAG adds an automated retrieval pipeline to select relevant documents, context stuffing at its core is the simpler act of manually or programmatically inserting context into the prompt window.

The power of context stuffing lies in its ability to extend the model's effective knowledge beyond its training data. Language models have a knowledge cutoff date and cannot access proprietary, internal, or recently created information. By injecting relevant documents directly into the prompt, the model can answer questions about information it has never seen during training -- internal company policies, recent research papers, private codebases, or real-time data. This makes context stuffing indispensable for enterprise AI applications where responses must be grounded in authoritative, organization-specific sources.

The technique also serves as a primary defense against hallucination. When a model generates text purely from parametric memory, it may confidently produce plausible but incorrect statements. By providing source documents and instructing the model to answer only from the provided context, the hallucination surface is dramatically reduced. However, context stuffing introduces its own challenges: context window limits constrain how much material can be included, long contexts may cause the model to lose focus on relevant passages (the "lost in the middle" problem documented by Liu et al., 2023), and the quality of responses is bounded by the quality and relevance of the provided context.

## How It Works

1. **Identify relevant context.** Determine what documents, data, or reference material the model needs to answer the query accurately. This may involve manual selection, keyword search, or semantic retrieval using embeddings.

2. **Prepare and format the context.** Clean the text, remove irrelevant sections, and format it for clarity. Consider chunking long documents into digestible sections with clear headers.

3. **Inject context into the prompt.** Place the context material in the prompt, typically before the task instruction or query. Use clear delimiters to separate context from instructions.

4. **Add grounding instructions.** Explicitly instruct the model to use only the provided context, to cite sources, or to indicate when the context does not contain sufficient information.

5. **Present the query.** Ask the specific question or describe the task that should be performed using the provided context.

6. **Validate the response.** Check that the model's response is actually grounded in the provided context and not drawing from parametric memory to fill gaps.

### Diagram

```
┌─────────────────────────────────────────┐
│  CONTEXT DOCUMENTS                       │
│  ┌───────────────────────────────────┐   │
│  │ Document 1: Company Policy v2.3   │   │
│  │ "All employees must complete..."  │   │
│  ├───────────────────────────────────┤   │
│  │ Document 2: Q3 Financial Report   │   │
│  │ "Revenue increased 12% YoY..."    │   │
│  ├───────────────────────────────────┤   │
│  │ Document 3: Product Spec Sheet    │   │
│  │ "Maximum throughput: 10K rps..."  │   │
│  └───────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  GROUNDING INSTRUCTION                   │
│  "Answer based ONLY on the documents     │
│   provided above. If the answer is not   │
│   in the documents, say so."             │
├─────────────────────────────────────────┤
│  QUERY                                   │
│  "What was the YoY revenue change?"      │
├─────────────────────────────────────────┤
│              ▼                           │
│  ┌─────────────────────┐                 │
│  │       MODEL          │                 │
│  │ (context-grounded)   │                 │
│  └──────────┬──────────┘                 │
│              ▼                           │
│  OUTPUT: "Revenue increased 12% YoY      │
│  according to the Q3 Financial Report."  │
└─────────────────────────────────────────┘
```

## Template

**Basic template:**

```
Context:
{document_text}

---

Based on the context above, {task_instruction}

{query}
```

**Multi-document template:**

```
You are given the following reference documents. Use ONLY the information in these documents to answer the question. If the answer cannot be found in the documents, state "The provided documents do not contain this information."

<document source="{source_1_name}">
{document_1_text}
</document>

<document source="{source_2_name}">
{document_2_text}
</document>

<document source="{source_3_name}">
{document_3_text}
</document>

Question: {query}

Answer (cite the source document):
```

## Examples

### Example 1: Internal Policy Q&A

**Input prompt:**
```
Use the following company policy document to answer the employee's question.

<policy>
REMOTE WORK POLICY - Effective January 2025

Section 3.2: Equipment Allowance
All full-time employees approved for remote work are eligible for a one-time equipment allowance of $1,500. This allowance covers: desk, chair, monitor, keyboard, mouse, and webcam. Receipts must be submitted within 90 days of purchase through the ExpenseTracker system. The allowance is refreshed every 3 years from the date of initial claim.

Section 3.3: Internet Stipend
Remote employees receive a monthly internet stipend of $75, added to their regular paycheck. Employees must maintain a minimum internet speed of 50 Mbps download / 10 Mbps upload. Verification may be requested quarterly.

Section 4.1: In-Office Requirements
Hybrid employees must be in-office a minimum of 2 days per week (Tuesday and Thursday are designated anchor days). Fully remote employees are expected to visit the office for quarterly team summits, with travel expenses covered under the corporate travel policy.
</policy>

Employee question: "I started working remotely 2 years ago and used my equipment allowance. My monitor just broke -- can I get a new one covered?"
```

**Expected output:**
```
Based on the Remote Work Policy (Section 3.2), your equipment allowance of $1,500 is refreshed every 3 years from the date of your initial claim. Since you started working remotely 2 years ago, your allowance has not yet refreshed -- it will become available again after 3 years from your initial claim date.

The broken monitor would not be covered under a new equipment allowance at this time. You may want to check with your manager or HR about whether there are other provisions for equipment replacement outside the standard allowance cycle.
```

### Example 2: Technical Documentation Q&A

**Input prompt:**
```
Reference the API documentation below to answer the developer's question.

<api-docs>
## POST /api/v2/batch-process

Submits a batch of items for asynchronous processing.

**Request Body:**
- `items` (array, required): Array of item objects. Maximum 1000 items per request.
- `callback_url` (string, optional): URL to receive webhook notification on completion.
- `priority` (string, optional): "low" | "normal" | "high". Default: "normal".
- `idempotency_key` (string, optional): Unique key to prevent duplicate processing. Valid for 24 hours.

**Response:**
- `batch_id` (string): Unique identifier for the batch.
- `status` (string): Always "queued" on successful submission.
- `estimated_completion` (string): ISO 8601 timestamp.

**Rate Limits:**
- 10 requests per minute per API key.
- Maximum 50,000 items per hour across all batches.

**Errors:**
- 400: Invalid request body or items exceed 1000.
- 429: Rate limit exceeded. Retry after `Retry-After` header value.
- 503: Service temporarily unavailable.
</api-docs>

Developer question: "I need to process 5000 items as fast as possible. What's the best approach?"
```

**Expected output:**
```
Based on the API documentation, here's the optimal approach for processing 5000 items:

1. **Split into 5 batches** of 1000 items each (the maximum per request).
2. **Use priority "high"** to expedite processing.
3. **Submit at rate limit pace**: You can make 10 requests per minute, so all 5 batches can be submitted within 1 minute.
4. **Set a callback_url** on each batch to receive completion notifications rather than polling.
5. **Use idempotency_keys** on each batch to safely retry if you encounter a 429 or 503 error.

Note the hourly item limit of 50,000 items across all batches -- your 5,000 items are well within this limit. If you hit a 429 rate limit error, wait for the duration specified in the `Retry-After` response header before retrying.
```

## When to Use

- **Proprietary or internal data.** When the model needs information not available in its training data -- company documents, internal wikis, private databases.
- **Factual accuracy is critical.** When answers must be traceable to specific sources and hallucination is unacceptable (legal, medical, financial domains).
- **Up-to-date information.** When the query involves information more recent than the model's training cutoff date.
- **Document-specific tasks.** Summarization, extraction, comparison, or analysis of specific provided texts.
- **Compliance and audit requirements.** When responses must be attributable to specific authoritative sources for regulatory purposes.
- **RAG pipeline foundation.** Context stuffing is the execution layer of any RAG system -- retrieved chunks are stuffed into the prompt for grounded generation.

## When to Avoid

- **Context exceeds window limits.** If the relevant material is too large for the context window, you need chunking strategies, summarization, or iterative approaches instead.
- **Context quality is poor.** Providing irrelevant, outdated, or contradictory documents can degrade performance below zero-shot baselines.
- **Creative or generative tasks.** When the task requires original thinking beyond what any source document contains, context stuffing may over-constrain the model.
- **Latency-critical applications.** Long contexts increase time-to-first-token and total generation time proportionally. If sub-second latency is required, minimize context volume.
- **Cost-sensitive high-volume processing.** Stuffing thousands of tokens of context per query multiplied by millions of queries creates significant cost overhead.

## Cost & Performance

| Metric             | Value      | Notes                                                    |
|---------------------|------------|----------------------------------------------------------|
| Token cost          | Variable   | Depends entirely on context volume; can be 100-100K tokens|
| Latency             | Variable   | Proportional to context length; longer = slower           |
| API calls           | 1          | Single call with context included                         |
| Accuracy (grounded) | High       | 85-95% when context contains the answer                   |
| Hallucination rate  | Low        | Significantly reduced vs. ungrounded generation           |
| Setup effort        | Low-Medium | Requires context preparation and retrieval infrastructure |
| Consistency         | High       | Responses anchored to stable source material              |

## Variants

- **Full-document stuffing:** Insert entire documents into the context. Simple but token-expensive. Best for short documents or when it is unclear which sections are relevant.
- **Chunk-based stuffing:** Split documents into smaller chunks (typically 200-1000 tokens) and insert only the most relevant chunks. Foundation of production RAG systems.
- **Hierarchical stuffing:** Provide document summaries alongside relevant detailed sections. Gives the model both breadth and depth while managing token budgets.
- **Multi-source stuffing:** Include documents from multiple sources with clear source attribution tags. Enables the model to synthesize information across sources and cite appropriately.
- **Conversational context stuffing:** In multi-turn conversations, maintain a rolling window of relevant context, dropping older or less relevant passages as new context is added.
- **Structured data stuffing:** Inject tabular data, JSON objects, or database query results rather than prose text. Requires format-aware prompting to ensure the model interprets structured data correctly.

## Composability

- **+ Zero-Shot:** The most common combination. Provide context documents and a clear instruction. "Based on the following documents, answer this question." This is the minimal RAG pattern.
- **+ Few-Shot:** Include examples of how to extract information from similar documents alongside the actual context. Useful for complex extraction tasks with specific formatting requirements.
- **+ Role Prompting:** Assign an expert role to shape how the model interprets and synthesizes the provided context. "You are a legal analyst. Review the following contract clauses..."
- **+ Output Format Control:** Specify how the grounded response should be structured. "Based on the context, fill in the following JSON template..."
- **+ Prompt Scaffolding:** Use XML tags or delimiters to clearly separate context from instructions, query, and output format. Essential for multi-document contexts.
- **+ Chain-of-Thought:** Ask the model to reason through the provided documents step by step before arriving at an answer. Improves accuracy on complex multi-document synthesis tasks.

## Limitations

- **Lost in the middle.** Liu et al. (2023) demonstrated that models perform best when relevant information is at the beginning or end of the context, with degraded performance for information buried in the middle of long contexts.
- **Context window limits.** Even with modern long-context models (128K-1M tokens), there is a finite limit to how much information can be included. Complex tasks may require more context than the window allows.
- **Noise dilution.** Including irrelevant context alongside relevant information can degrade performance, as the model must distinguish signal from noise. More context is not always better.
- **Faithfulness failures.** Despite grounding instructions, models may still draw on parametric knowledge, blending trained knowledge with provided context in ways that are difficult to detect.
- **Cost scaling.** Token cost scales linearly with context volume. Processing 10,000 tokens of context per query at scale can become the dominant cost factor in production systems.
- **Context preparation overhead.** Selecting, cleaning, chunking, and formatting context documents adds engineering and computational overhead to the overall system.

## Sources

**Primary:**
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020. https://arxiv.org/abs/2005.11401

**Secondary:**
- Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172. https://arxiv.org/abs/2307.03172
- Gao, L., Ma, X., Lin, J., & Callan, J. (2023). "Precise Zero-Shot Dense Retrieval without Relevance Labels." ACL 2023. https://arxiv.org/abs/2212.10496
- Ram, O., Levine, Y., Dalmedigos, I., Muhlgay, D., Shashua, A., Leyton-Brown, K., & Shoham, Y. (2023). "In-Context Retrieval-Augmented Language Models." TACL 2023. https://arxiv.org/abs/2302.00083
- Shi, W., Min, S., Yasunaga, M., et al. (2023). "REPLUG: Retrieval-Augmented Black-Box Language Models." arXiv:2301.12652. https://arxiv.org/abs/2301.12652
