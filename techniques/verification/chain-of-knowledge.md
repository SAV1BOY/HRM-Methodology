---
id: chain-of-knowledge
name: "Chain-of-Knowledge (CoK)"
aliases: ["CoK", "Progressive Knowledge Grounding"]
category: verification
family: grounding
year: 2023
authors: ["Xingxuan Li", "Ruochen Zhao", "Yew Ken Chia", "Bosheng Ding", "Shafiq Joty", "Soujanya Poria", "Lidong Bing"]
paper: "https://arxiv.org/abs/2305.13269"
paper_title: "Chain-of-Knowledge: Grounding Large Language Models via Dynamic Knowledge Adapting over Heterogeneous Sources"
venue: "arXiv 2023"
code: null

complexity: high
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: true
requires_training: false
model_agnostic: true

best_for: ["knowledge-intensive question answering", "multi-source fact verification", "questions requiring diverse knowledge types", "reducing hallucination with external grounding", "complex queries spanning structured and unstructured data"]
avoid_when: ["simple factual queries answerable from single source", "creative or opinion tasks", "no access to external knowledge sources", "low-latency requirements"]
composes_with: ["chain-of-thought", "retrieval-augmented-generation", "grounding-via-sources", "step-back-prompting"]

tags: ["grounding", "knowledge-retrieval", "multi-source", "progressive-reasoning", "tool-use", "verification"]
---

# Chain-of-Knowledge (CoK)

> **One-line summary:** Chain-of-Knowledge progressively grounds each step of LLM reasoning by dynamically selecting and querying the most appropriate knowledge source (knowledge graph, database, web search, or documents) for each reasoning step, reducing hallucination through step-wise evidence anchoring.

## Overview

Chain-of-Knowledge (CoK) addresses a fundamental challenge in knowledge-grounded generation: different parts of a complex question may require different types of knowledge from different sources. A question like "Which company founded by a Stanford dropout has the highest market cap?" requires both structured data (company founders, market caps) and unstructured knowledge (educational histories). CoK dynamically selects the appropriate knowledge source for each reasoning step, rather than relying on a single retrieval system.

The key innovation in CoK is the concept of "knowledge adapting," where the framework identifies what type of knowledge is needed at each reasoning step and routes the query to the most suitable source. This might be a knowledge graph for relational facts, a structured database for numerical data, a search engine for recent events, or a document corpus for detailed explanations. By matching knowledge needs to sources, CoK achieves more reliable grounding than approaches that use a single retrieval pipeline for all knowledge types.

CoK operates through a three-phase process at each reasoning step: first, the LLM generates a preliminary reasoning step with potential knowledge needs identified; second, the system selects and queries the appropriate knowledge source; third, the LLM adapts its reasoning based on the retrieved evidence. This progressive grounding ensures that each claim in the final answer chain is supported by externally verified information, dramatically reducing the hallucination rate compared to purely parametric reasoning.

## How It Works

1. **Reasoning Preparation:** The LLM begins reasoning about the question and generates the first step of a chain-of-thought. It also identifies what knowledge is needed to verify or complete this step.

2. **Knowledge Source Selection:** Based on the knowledge need, the system selects the most appropriate source: knowledge graph (for relational facts), structured database (for numerical/tabular data), web search (for recent or dynamic information), or document retrieval (for detailed context).

3. **Knowledge Retrieval:** The selected source is queried with a targeted query derived from the current reasoning step. The retrieved evidence is presented to the LLM.

4. **Knowledge-Grounded Reasoning:** The LLM incorporates the retrieved evidence into its reasoning, correcting or confirming its preliminary step. The grounded step is added to the reasoning chain.

5. **Progressive Iteration:** Steps 1-4 repeat for each subsequent reasoning step until the question is fully answered. Each step builds on previously grounded steps and adds new verified knowledge.

### Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                  Chain-of-Knowledge (CoK)                     │
│                                                               │
│  ┌──────────┐                                                 │
│  │ Question  │                                                 │
│  └─────┬────┘                                                 │
│        v                                                      │
│  ┌─────────────────┐                                          │
│  │ Step 1: Reason  │──> What knowledge is needed?             │
│  │ (preliminary)   │                                          │
│  └────────┬────────┘                                          │
│           v                                                   │
│  ┌────────────────────┐    ┌──────────────────────────────┐   │
│  │ Select Knowledge   │    │ Available Sources:            │   │
│  │ Source              │───>│  ● Knowledge Graph          │   │
│  │                    │    │  ● Structured Database       │   │
│  └────────┬───────────┘    │  ● Web Search               │   │
│           │                │  ● Document Retrieval        │   │
│           v                └──────────────────────────────┘   │
│  ┌────────────────────┐                                       │
│  │ Retrieve Evidence  │                                       │
│  └────────┬───────────┘                                       │
│           v                                                   │
│  ┌────────────────────┐                                       │
│  │ Grounded Step 1    │──┐                                    │
│  │ (verified claim)   │  │                                    │
│  └────────────────────┘  │                                    │
│                          v                                    │
│  ┌────────────────────┐  │                                    │
│  │ Step 2: Reason     │──> Select source → Retrieve → Ground  │
│  │ (builds on Step 1) │  │                                    │
│  └────────────────────┘  │                                    │
│                          v                                    │
│               ┌────────────────────┐                          │
│               │  Final Grounded    │                          │
│               │  Answer            │                          │
│               └────────────────────┘                          │
└───────────────────────────────────────────────────────────────┘
```

## Template

```
You are reasoning step by step about a question, grounding each step in
external knowledge.

QUESTION: {question}

For each reasoning step:
1. State what you need to figure out next.
2. Identify the type of knowledge needed:
   - FACTUAL_RELATION: Use knowledge graph
   - NUMERICAL_DATA: Use structured database
   - RECENT_EVENT: Use web search
   - DETAILED_CONTEXT: Use document retrieval
3. Formulate a specific query for the selected source.
4. [SYSTEM: Query the selected source and return evidence]
5. Incorporate the evidence into your reasoning step.

Reasoning Chain:

Step 1:
Need to know: {what_info_needed}
Source type: {source_type}
Query: {query}
Evidence: {retrieved_evidence}
Grounded conclusion: {verified_step}

Step 2:
...

Final Answer (grounded in evidence from all steps):
```

## Examples

### Example 1: Multi-Source Factual Question

**Input:**
```
QUESTION: What is the GDP per capita of the country where the
inventor of the World Wide Web was born?

Step 1:
Need to know: Who invented the World Wide Web?
Source type: FACTUAL_RELATION
Query: "inventor of World Wide Web"
```

**Evidence Retrieved:** Knowledge Graph: Tim Berners-Lee invented the World Wide Web.

```
Grounded conclusion: Tim Berners-Lee invented the World Wide Web. [KG]

Step 2:
Need to know: Where was Tim Berners-Lee born?
Source type: FACTUAL_RELATION
Query: "Tim Berners-Lee birthplace"
```

**Evidence Retrieved:** Knowledge Graph: Tim Berners-Lee was born in London, United Kingdom.

```
Grounded conclusion: Tim Berners-Lee was born in the United Kingdom. [KG]

Step 3:
Need to know: What is the GDP per capita of the United Kingdom?
Source type: NUMERICAL_DATA
Query: "United Kingdom GDP per capita latest"
```

**Evidence Retrieved:** Database: UK GDP per capita (2023): approximately $46,125 (current USD, World Bank).

```
Grounded conclusion: The UK's GDP per capita is approximately
$46,125 USD (2023). [DB: World Bank]

Final Answer: The inventor of the World Wide Web (Tim Berners-Lee)
was born in the United Kingdom, which has a GDP per capita of
approximately $46,125 USD as of 2023.

Sources: Knowledge Graph (Steps 1-2), World Bank Database (Step 3).
```

### Example 2: Current Events + Historical Context

**Input:**
```
QUESTION: How has the population of the city hosting the 2024 Summer
Olympics changed over the last century?

Step 1:
Need to know: Which city hosted the 2024 Summer Olympics?
Source type: RECENT_EVENT
Query: "2024 Summer Olympics host city"
```

**Evidence Retrieved:** Web: The 2024 Summer Olympic Games were held in Paris, France.

```
Grounded conclusion: Paris hosted the 2024 Summer Olympics. [Web]

Step 2:
Need to know: Population of Paris historically and currently.
Source type: NUMERICAL_DATA
Query: "Paris population 1924 vs 2024"
```

**Evidence Retrieved:** Database: Paris city proper population: ~2.9 million (1921 census), ~2.1 million (2021 census). Metropolitan area: ~5 million (1920s est.), ~12.3 million (2021).

```
Grounded conclusion: Paris city proper has actually decreased from
~2.9M to ~2.1M, while the metropolitan area grew from ~5M to ~12.3M. [DB]

Step 3:
Need to know: Why did city proper population decrease?
Source type: DETAILED_CONTEXT
Query: "Paris population decline city proper suburbanization"
```

**Evidence Retrieved:** Document: Post-WWII suburbanization, rent control effects, and expansion of the Paris metro system led to population redistribution from the city core to suburbs (banlieues).

```
Grounded conclusion: Suburbanization and urban policy shifted
population to surrounding suburbs while the metro area grew
significantly. [Doc]

Final Answer: Paris (host of the 2024 Olympics) shows a split trend
over the last century: the city proper population declined from ~2.9M
(1920s) to ~2.1M (2020s) due to suburbanization, while the greater
metropolitan area expanded from ~5M to ~12.3M, reflecting urban
sprawl enabled by transportation infrastructure.

Sources: Web search (Step 1), Population database (Step 2),
Historical analysis documents (Step 3).
```

## When to Use

- Complex questions requiring multiple types of knowledge (relational, numerical, contextual)
- Tasks where different claims need verification from different source types
- Knowledge-intensive QA where single-source retrieval is insufficient
- When accuracy requires cross-referencing structured and unstructured data
- Multi-hop reasoning where each hop may require a different knowledge source

## When to Avoid

- Simple questions answerable from a single source or the model's parametric knowledge
- Creative, opinion-based, or speculative tasks where external grounding is inappropriate
- When external knowledge sources are not available or not accessible
- Low-latency applications where multiple sequential retrievals are too slow
- Tasks where the overhead of source selection adds complexity without benefit

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 3-5x base | Multiple retrieval + reasoning steps |
| Latency | High | Sequential source queries at each reasoning step |
| Hallucination reduction | 40-60% | Each step grounded in external evidence |
| Num calls | 2-6 typical | Depends on number of reasoning steps |
| Infrastructure | Moderate | Requires access to multiple knowledge sources |

## Variants

- **CoK-Lite:** Uses only one or two knowledge sources instead of the full heterogeneous suite. Simpler but less flexible.
- **Parallel CoK:** Retrieves from all sources simultaneously for each step and lets the model select the most relevant evidence. Faster but potentially noisier.
- **Adaptive CoK:** The model dynamically decides whether external retrieval is needed for each step or whether its parametric knowledge suffices. Reduces unnecessary queries.
- **Verified CoK:** Adds a verification step after each retrieval to check whether the retrieved evidence actually answers the query.

## Composability

- **CoK + Chain-of-Thought:** CoT provides the reasoning structure; CoK adds external grounding at each reasoning step.
- **CoK + Grounding via Sources:** After all steps are grounded, format the final answer with explicit source citations for user verification.
- **CoK + Step-Back Prompting:** Use step-back to identify the abstract knowledge needed before selecting specific sources.
- **CoK + Self-Refine:** After the initial grounded chain, refine the reasoning by re-querying sources for steps that seem weak.

## Limitations

- Requires access to and integration with multiple heterogeneous knowledge sources
- Source selection accuracy is critical; choosing the wrong source for a step produces irrelevant evidence
- Sequential querying at each step creates high latency for multi-step questions
- The quality of retrieved evidence varies by source and query formulation
- Cannot handle questions where no available source contains the needed information
- The system's complexity (multiple sources, routing logic) increases maintenance burden
- Errors in early steps propagate through the chain, compounding with each subsequent step

## Sources

- **Primary:** [Chain-of-Knowledge: Grounding Large Language Models via Dynamic Knowledge Adapting over Heterogeneous Sources](https://arxiv.org/abs/2305.13269) — Li et al., 2023
- **Related:** [Verify-and-Edit: A Knowledge-Enhanced Chain-of-Thought Framework](https://arxiv.org/abs/2305.03268) — Zhao et al., 2023
- **Related:** [REACT: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al., 2022
