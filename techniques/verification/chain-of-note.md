---
id: chain-of-note
name: "Chain-of-Note (CoN)"
aliases: ["CoN", "Reading Notes for RAG", "Note-then-Answer"]
category: verification
family: grounding
year: 2023
authors: ["Wenhao Yu", "Hongming Zhang", "Xiaoman Pan", "Kaixin Ma", "Hongwei Wang", "Dong Yu"]
paper: "https://arxiv.org/abs/2311.09210"
paper_title: "Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models"
venue: "arXiv 2023"
code: null

complexity: medium
token_cost: medium
latency: medium
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["noisy retrieval settings", "open-domain QA with imperfect retrieval", "questions where retrieved docs are partially relevant", "reducing over-reliance on irrelevant retrieved content", "improving RAG robustness"]
avoid_when: ["no retrieved documents available", "documents are guaranteed to be highly relevant", "simple lookups where note-taking adds unnecessary overhead", "creative tasks not requiring document analysis"]
composes_with: ["retrieval-augmented-generation", "chain-of-thought", "grounding-via-sources", "self-consistency"]

tags: ["grounding", "rag", "reading-notes", "robustness", "retrieval", "note-taking"]
---

# Chain-of-Note (CoN)

> **One-line summary:** Chain-of-Note instructs the model to generate sequential "reading notes" for each retrieved document, assessing its relevance and extracting useful information before formulating an answer, improving RAG robustness when retrieval quality is imperfect.

## Overview

Chain-of-Note (CoN) addresses a critical weakness in standard Retrieval-Augmented Generation (RAG) systems: when retrieved documents are noisy, partially relevant, or completely irrelevant, the model may either hallucinate by over-relying on poor retrievals or ignore useful information buried in noisy documents. CoN introduces an intermediate "note-taking" step where the model generates a structured reading note for each retrieved document before attempting to answer the question.

The core insight is that by explicitly annotating each document's relevance and extracting its key information into a concise note, the model develops a clearer picture of what evidence is actually available. This acts as a filter and organizer: irrelevant documents are flagged as such (preventing their influence on the answer), partially relevant documents have their useful portions extracted, and highly relevant documents have their key information highlighted. The model then answers based on the curated notes rather than the raw documents.

CoN was developed by Yu et al. to improve the robustness of RAG across three scenarios: when retrieved documents directly contain the answer, when they provide only indirect context, and when they are entirely irrelevant to the query. In the last case, CoN enables the model to recognize that the retrieved information is unhelpful and fall back on its parametric knowledge or simply acknowledge uncertainty, rather than forcing a (likely hallucinated) answer from irrelevant content.

## How It Works

1. **Document Reception:** The model receives a question along with K retrieved documents (typically from a retrieval pipeline like DPR or BM25).

2. **Sequential Note Generation:** For each retrieved document, the model generates a "reading note" that includes: (a) a relevance assessment (relevant / partially relevant / irrelevant), (b) key information extracted from the document if relevant, and (c) how the document relates to the question.

3. **Note Synthesis:** The model reviews all notes holistically to determine whether sufficient evidence exists to answer the question, and if so, which notes provide the strongest support.

4. **Grounded Answer Generation:** Based on the synthesized notes, the model generates its final answer. If the notes indicate insufficient evidence, the model can acknowledge this rather than hallucinating.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   Chain-of-Note (CoN)                    │
│                                                          │
│  ┌──────────┐  ┌─────────────────────────────────────┐   │
│  │ Question  │  │ Retrieved Documents                 │   │
│  └─────┬────┘  │ Doc 1, Doc 2, Doc 3, ... Doc K      │   │
│        │       └──────────────┬────────────────────────┘   │
│        │                     │                            │
│        └──────────┬──────────┘                            │
│                   v                                       │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Generate Reading Notes:                           │    │
│  │                                                   │    │
│  │ Note 1 (Doc 1): RELEVANT - "Doc states that..."  │    │
│  │ Note 2 (Doc 2): IRRELEVANT - "Discusses unrelated │    │
│  │                  topic of..."                     │    │
│  │ Note 3 (Doc 3): PARTIAL - "Mentions X but not    │    │
│  │                  the specific detail asked about" │    │
│  └──────────────────────┬────────────────────────────┘    │
│                         v                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Synthesize Notes:                                 │    │
│  │ "Docs 1 and 3 provide partial evidence.           │    │
│  │  Doc 2 is not useful. Sufficient to answer."      │    │
│  └──────────────────────┬────────────────────────────┘    │
│                         v                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Generate Answer Based on Notes                    │    │
│  │ (or acknowledge insufficient evidence)            │    │
│  └───────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Template

```
You are given a question and several retrieved documents. Before
answering, generate a reading note for each document assessing its
relevance and extracting useful information.

QUESTION: {question}

RETRIEVED DOCUMENTS:
[Doc 1]: {document_1}
[Doc 2]: {document_2}
[Doc 3]: {document_3}

READING NOTES:
For each document, write a note with:
- Relevance: RELEVANT / PARTIALLY RELEVANT / IRRELEVANT
- Key information: What useful facts does this document contain?
- Relation to question: How does this help (or not) answer the question?

Note for Doc 1:
Note for Doc 2:
Note for Doc 3:

SYNTHESIS:
Based on the reading notes, is there sufficient evidence to answer
the question? If so, which notes support the answer?

ANSWER:
Based on the relevant notes, provide your answer. If the documents
do not contain sufficient information, state what is missing.
```

## Examples

### Example 1: Noisy Retrieval (Mixed Relevance)

**Input:**
```
QUESTION: When was the Eiffel Tower first illuminated with electric lights?

[Doc 1]: "The Eiffel Tower was built for the 1889 World's Fair in Paris.
Gustave Eiffel's company designed and built the structure over two years.
It stands 330 meters tall and was the world's tallest structure until 1930."

[Doc 2]: "In 1925, the Eiffel Tower was fitted with illuminated advertising
by Citroen, with 250,000 light bulbs spelling out the company name on three
sides of the tower. However, the tower first used electric illumination
for the 1889 World's Fair itself, with gas lamps and early electric
arc lights."

[Doc 3]: "Paris is known as the City of Light, a nickname dating to the
Age of Enlightenment and later reinforced by its early adoption of street
lighting. The city was among the first in Europe to implement large-scale
gas lighting in the 1820s."
```

**Output:**
```
READING NOTES:

Note for Doc 1: PARTIALLY RELEVANT
Key information: The Eiffel Tower was built for the 1889 World's Fair.
Relation to question: Provides construction date context but does not
specifically address electric illumination.

Note for Doc 2: RELEVANT
Key information: The tower first used electric illumination for the
1889 World's Fair with gas lamps and early electric arc lights. In 1925,
Citroen added 250,000 advertising bulbs.
Relation to question: Directly answers when electric lights were first
used on the tower.

Note for Doc 3: IRRELEVANT
Key information: Paris's "City of Light" nickname and history of street
lighting.
Relation to question: Discusses Paris lighting in general but not the
Eiffel Tower specifically.

SYNTHESIS:
Doc 2 directly addresses the question. Doc 1 provides supporting context.
Doc 3 is not useful. Sufficient evidence exists to answer.

ANSWER:
The Eiffel Tower was first illuminated with electric lights for the
1889 World's Fair, its inaugural year, using early electric arc lights
alongside gas lamps [Doc 2]. A more dramatic electric illumination came
in 1925 when Citroen installed 250,000 light bulbs for advertising
on three sides of the tower [Doc 2].
```

### Example 2: Irrelevant Retrieval (Graceful Degradation)

**Input:**
```
QUESTION: What is the melting point of hafnium?

[Doc 1]: "Hafnium is used in nuclear reactor control rods due to its
high neutron absorption cross-section. It was named after Hafnia, the
Latin name for Copenhagen."

[Doc 2]: "Zirconium and hafnium are chemically similar and difficult
to separate. Hafnium is found in zirconium ores and was not recognized
as a separate element until 1923."

[Doc 3]: "Titanium has a melting point of 1,668°C and is widely used
in aerospace applications due to its high strength-to-weight ratio."
```

**Output:**
```
READING NOTES:

Note for Doc 1: PARTIALLY RELEVANT
Key information: Hafnium is used in nuclear control rods, high neutron
absorption, named after Copenhagen.
Relation to question: Discusses hafnium properties but not melting point.

Note for Doc 2: PARTIALLY RELEVANT
Key information: Hafnium is similar to zirconium, discovered 1923.
Relation to question: Background on hafnium but no melting point data.

Note for Doc 3: IRRELEVANT
Key information: Titanium melting point (1,668°C).
Relation to question: About titanium, not hafnium. The melting point
given is for the wrong element.

SYNTHESIS:
None of the documents contain the melting point of hafnium. Doc 3 mentions
a melting point but for titanium, not hafnium. I should use my parametric
knowledge while noting the retrieval gap.

ANSWER:
The retrieved documents do not contain the melting point of hafnium.
Based on general chemistry knowledge, hafnium has a melting point of
approximately 2,233°C (4,051°F). Note: this value comes from parametric
knowledge as the retrieved documents only discuss hafnium's nuclear
applications [Doc 1] and chemical similarity to zirconium [Doc 2],
without providing thermal properties.
```

## When to Use

- RAG pipelines where retrieval quality is variable or unpredictable
- Open-domain question answering with large, noisy document corpora
- Settings where retrieved documents may be tangentially related but not directly answering the question
- When you need the model to distinguish between supported and unsupported claims
- High-reliability applications where relying on irrelevant retrievals could cause harm

## When to Avoid

- When retrieved documents are consistently high-quality and highly relevant (the note-taking adds overhead without benefit)
- Tasks without any retrieved documents (the technique is specific to RAG settings)
- Simple lookup tasks where the answer is clearly present or clearly absent
- Creative tasks where document analysis is not relevant

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | +30-60% | Notes + synthesis before answering |
| Latency | ~1.5x baseline | Single call but longer generation |
| Robustness gain | +8-15% | On noisy retrieval benchmarks (e.g., NQ, TriviaQA) |
| Hallucination reduction | 20-35% | Especially on irrelevant retrieval cases |
| Num calls | 1 | All note-taking happens within single generation |

## Variants

- **Binary CoN:** Notes only classify documents as relevant or irrelevant without extracting information. Simpler but less informative.
- **Scored CoN:** Assigns numerical relevance scores (0-10) to each document, enabling quantitative thresholding.
- **Hierarchical CoN:** For very long documents, generates paragraph-level notes before document-level notes.
- **Comparative CoN:** Notes explicitly compare information across documents, flagging contradictions.

## Composability

- **CoN + RAG:** The natural combination. CoN adds the note-taking layer between retrieval and generation.
- **CoN + Grounding via Sources:** Notes identify which documents to cite; grounding ensures citations are used in the final answer.
- **CoN + Self-Consistency:** Generate multiple sets of notes and answers, then vote on the final answer for improved reliability.
- **CoN + Chain-of-Thought:** Use CoT reasoning within each note to more carefully assess relevance and extract information.

## Limitations

- Adds token overhead that scales with the number of retrieved documents
- The model may still be influenced by irrelevant documents despite noting their irrelevance
- Note quality depends on the model's ability to assess relevance, which is not perfect
- When falling back on parametric knowledge (all documents irrelevant), the answer may still hallucinate
- The technique assumes the model can distinguish relevant from irrelevant content, which fails for subtle misinformation
- Does not improve retrieval quality itself; it only improves the model's use of retrieved content

## Sources

- **Primary:** [Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models](https://arxiv.org/abs/2311.09210) — Yu et al., 2023
- **Related:** [When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories](https://arxiv.org/abs/2212.10511) — Mallen et al., 2023
- **Related:** [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511) — Asai et al., 2023
