---
id: chain-of-verification
name: "Chain-of-Verification (CoVe)"
aliases: ["CoVe", "Verify-then-Revise"]
category: verification
family: verification
year: 2023
authors: ["Shehzaad Dhuliawala", "Mojtaba Komeili", "Jing Xu", "Roberta Raileanu", "Xian Li", "Asli Celikyilmaz", "Jason Weston"]
paper: "https://arxiv.org/abs/2309.11495"
paper_title: "Chain-of-Verification Reduces Hallucination in Large Language Model Responses"
venue: "Meta AI, arXiv 2023"
code: null

complexity: medium
token_cost: high
latency: high
num_calls: 4

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["reducing hallucinations", "factual question answering", "list-based responses", "knowledge-intensive tasks", "long-form factual generation"]
avoid_when: ["creative writing tasks", "opinion-based questions", "extremely latency-sensitive applications", "tasks where factual accuracy is not critical"]
composes_with: ["chain-of-thought", "retrieval-augmented-generation", "few-shot-prompting", "self-consistency"]

tags: ["hallucination-reduction", "verification", "self-correction", "factual-accuracy", "meta-reasoning"]
---

# Chain-of-Verification (CoVe)

> **One-line summary:** CoVe reduces hallucination by having the LLM generate an initial response, plan verification questions for its own claims, answer those questions independently, and then produce a revised response incorporating the verified facts.

## Overview

Chain-of-Verification (CoVe) directly targets the hallucination problem in LLMs by introducing a structured self-verification pipeline. When an LLM generates a response, it often includes plausible-sounding but incorrect factual claims. CoVe addresses this by decomposing the verification process into explicit steps: after generating an initial draft, the model formulates specific yes/no or short-answer verification questions about the claims in its response, answers each question independently (without seeing the original response, to avoid bias), and then uses the verified answers to revise the original response.

The critical design insight is the separation between the original response and the verification step. When the model answers verification questions while seeing its original response, it tends to simply confirm its earlier claims (confirmation bias). By answering verification questions independently -- without the biasing context of the original draft -- the model is more likely to catch errors. This "factored" verification approach significantly outperforms naive self-verification where the model simply asks "is my response correct?"

Developed by researchers at Meta AI, CoVe was shown to substantially reduce hallucination rates across several benchmarks including list-based questions (e.g., "Name politicians born in New York City"), where hallucinated list items are a common failure mode. The technique is entirely prompt-based, requires no fine-tuning, and works with any capable LLM.

## How It Works

1. **Baseline Response Generation:** The LLM generates an initial response to the user's question. This response may contain hallucinations or inaccuracies.

2. **Verification Planning:** The model analyzes its own response and generates a set of focused verification questions targeting specific factual claims. For example, if the response says "Albert Einstein was born in Munich," a verification question might be "Where was Albert Einstein born?"

3. **Independent Verification Execution:** Each verification question is answered independently, ideally without the original response in context. This prevents confirmation bias and allows the model to give fresh, more accurate answers.

4. **Revised Response Generation:** The model produces a final revised response, incorporating corrections based on the verification results. Claims that failed verification are removed or corrected; verified claims are retained.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│              Chain-of-Verification (CoVe)                │
│                                                          │
│  ┌────────────┐                                          │
│  │  Question   │                                          │
│  └──────┬─────┘                                          │
│         v                                                │
│  ┌────────────────────┐                                  │
│  │ Step 1: Generate   │                                  │
│  │ Baseline Response  │                                  │
│  └──────┬─────────────┘                                  │
│         v                                                │
│  ┌────────────────────┐     ┌─────────────────────────┐  │
│  │ Step 2: Plan       │────>│ Verification Questions  │  │
│  │ Verification       │     │ Q1: "Was X born in Y?"  │  │
│  │ Questions          │     │ Q2: "Did A happen in B?"│  │
│  └────────────────────┘     │ Q3: "Is C true of D?"   │  │
│                             └──────────┬──────────────┘  │
│                                        v                 │
│                             ┌─────────────────────────┐  │
│                             │ Step 3: Answer Each     │  │
│                             │ Question Independently  │  │
│                             │ (no original context)   │  │
│                             └──────────┬──────────────┘  │
│                                        v                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Step 4: Revise Original Response Using Verified    │  │
│  │ Answers (correct errors, remove hallucinations)    │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         v                                │
│                ┌─────────────────┐                       │
│                │  Final Verified  │                       │
│                │  Response        │                       │
│                └─────────────────┘                       │
└──────────────────────────────────────────────────────────┘
```

## Template

```
STEP 1 — Generate initial response:
{question}

[Generate your best answer]

STEP 2 — Plan verification:
Review your response above. For each factual claim, create a specific
verification question.

Verification questions:
1. {verification_q1}
2. {verification_q2}
3. {verification_q3}
...

STEP 3 — Verify independently:
Answer each verification question below using only your knowledge.
Do NOT refer back to your original response.

{verification_questions_listed}

STEP 4 — Produce revised response:
Based on the verification results, revise your original response.
Remove or correct any claims that failed verification.

Final verified response:
```

## Examples

### Example 1: Biographical Facts

**Input:**
```
Name five Nobel Prize winners in Physics from the 21st century and
their contributions.
```

**Step 1 (Baseline Response):**
```
1. Albert Einstein (2001) — Bose-Einstein condensates
2. Peter Higgs (2013) — Higgs boson prediction
3. Kip Thorne (2017) — Gravitational wave detection
4. Roger Penrose (2020) — Black hole formation
5. John Clauser (2022) — Quantum entanglement experiments
```

**Step 2 (Verification Questions):**
```
1. Did Albert Einstein win the Nobel Prize in Physics in 2001?
2. Did Peter Higgs win the Nobel Prize in Physics in 2013?
3. Did Kip Thorne win the Nobel Prize in 2017?
4. Did Roger Penrose win the Nobel Prize in 2020?
5. Did John Clauser win the Nobel Prize in 2022?
```

**Step 3 (Independent Verification):**
```
1. No. Albert Einstein won in 1921, not 2001. The 2001 Prize went to
   Eric Cornell, Wolfgang Ketterle, and Carl Wieman for BEC.
2. Yes. Peter Higgs shared the 2013 prize with Francois Englert.
3. Yes. Kip Thorne shared the 2017 prize with Rainer Weiss and
   Barry Barish for LIGO/gravitational waves.
4. Yes. Roger Penrose won half the 2020 prize for black hole theory.
5. Yes. John Clauser shared the 2022 prize with Alain Aspect and
   Anton Zeilinger.
```

**Step 4 (Revised Response):**
```
1. Eric Cornell, Wolfgang Ketterle, Carl Wieman (2001) — Bose-Einstein
   condensates in dilute gases
2. Peter Higgs (2013) — Theoretical prediction of the Higgs boson
3. Kip Thorne (2017) — LIGO detector and gravitational wave observation
4. Roger Penrose (2020) — Black hole formation as a robust prediction
   of general relativity
5. John Clauser (2022) — Experiments with entangled photons and
   Bell inequalities
```

### Example 2: Technical Claims

**Input:**
```
What are the key differences between REST and GraphQL APIs?
```

**Step 1 (Baseline):**
```
REST uses multiple endpoints; GraphQL uses a single endpoint. REST returns
fixed data structures; GraphQL lets clients specify exactly what data they
need. REST uses HTTP methods (GET, POST, PUT, DELETE) for CRUD; GraphQL
uses queries and mutations. REST was developed by Roy Fielding in 2000;
GraphQL was created by Twitter in 2012. GraphQL eliminates over-fetching
and under-fetching problems common in REST.
```

**Step 2 (Verification Questions):**
```
1. Does REST use multiple endpoints while GraphQL uses a single endpoint?
2. Was REST developed by Roy Fielding in 2000?
3. Was GraphQL created by Twitter in 2012?
4. Does GraphQL use queries and mutations instead of HTTP methods?
```

**Step 3 (Independent Verification):**
```
1. Yes, this is correct.
2. Yes, Roy Fielding's dissertation in 2000 defined REST.
3. No. GraphQL was created by Facebook (now Meta) in 2012 and
   open-sourced in 2015. Twitter is not involved.
4. Yes, GraphQL uses queries for reads and mutations for writes.
```

**Step 4 (Revised Response):**
```
REST uses multiple endpoints; GraphQL uses a single endpoint. REST returns
fixed data structures; GraphQL lets clients specify exactly what data they
need. REST uses HTTP methods (GET, POST, PUT, DELETE) for CRUD; GraphQL
uses queries and mutations. REST was developed by Roy Fielding in 2000;
GraphQL was created by Facebook in 2012 and open-sourced in 2015. GraphQL
eliminates over-fetching and under-fetching problems common in REST.
```

## When to Use

- Factual question answering where hallucination is a known risk
- List generation tasks (e.g., "Name all X that satisfy Y")
- Knowledge-intensive responses where specific claims can be individually verified
- High-stakes content where factual accuracy matters (medical, legal, financial)
- Long-form generation where errors compound without verification

## When to Avoid

- Creative writing, brainstorming, or opinion-based tasks where "correctness" is subjective
- Simple, well-known facts unlikely to be hallucinated
- Extremely latency-sensitive applications (four steps add significant delay)
- Tasks where the model's training data is insufficient for reliable self-verification
- When external verification sources (RAG, search) are available and more reliable

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 3-4x base | Baseline + questions + verification + revision |
| Latency | ~4x baseline | Four sequential steps (can partially parallelize step 3) |
| Hallucination reduction | 30-50% | On list-based and factual QA benchmarks |
| Num calls | 4 typical | Generate → Plan → Verify → Revise |
| Best improvement | List tasks | Where individual items can be independently verified |

## Variants

- **Joint CoVe:** Verification questions are answered in the same context as the original response (simpler but less effective due to confirmation bias).
- **Factored CoVe:** Verification questions are answered without seeing the original response (recommended; better at catching errors).
- **Two-Step CoVe:** Combines planning and verification into a single step for reduced latency.
- **CoVe with Retrieval:** Verification questions are answered using external search rather than the model's own knowledge, significantly improving reliability.

## Composability

- **CoVe + RAG:** Use retrieval to answer verification questions instead of relying on the model's parametric knowledge. Dramatically improves verification reliability.
- **CoVe + Chain-of-Thought:** Use CoT reasoning during the verification step for more thorough fact-checking.
- **CoVe + Self-Consistency:** Generate multiple baseline responses, verify each, and select the most consistently verified answer.
- **CoVe + Few-Shot:** Provide examples of good verification questions to improve the planning step.

## Limitations

- Self-verification is limited by the model's own knowledge: if the model does not know the correct answer, it cannot verify effectively
- The factored approach (independent verification) requires careful prompt engineering to prevent information leakage
- Four-step process significantly increases latency and token cost
- Verification questions may miss subtle errors or errors that require multi-step reasoning to detect
- Some types of hallucinations (e.g., fabricated but plausible statistics) are difficult to self-verify
- The model may generate superficial verification questions that miss the actual errors

## Sources

- **Primary:** [Chain-of-Verification Reduces Hallucination in Large Language Model Responses](https://arxiv.org/abs/2309.11495) — Dhuliawala et al., Meta AI, 2023
- **Related:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Madaan et al., 2023
- **Related:** [FacTool: Factuality Detection in Generative AI](https://arxiv.org/abs/2307.13528) — Chern et al., 2023
