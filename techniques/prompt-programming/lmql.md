---
id: lmql
name: "LMQL (Language Model Query Language)"
aliases: ["LMQL", "Language Model Query Language", "LM Query Language"]
category: prompt-programming
family: constrained-generation
year: 2023
authors: ["Luca Beurer-Kellner", "Marc Fischer", "Martin Vechev"]
paper: "https://arxiv.org/abs/2212.06094"
paper_title: "Prompting Is Programming: A Query Language for Large Language Models"
venue: "PLDI 2023"
code: "https://github.com/eth-sri/lmql"

complexity: medium
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for: ["structured output generation", "constrained decoding", "multi-variable prompts", "type-safe LLM outputs", "conditional prompt logic"]
avoid_when: ["simple free-form generation", "no Python environment available", "model API does not expose logits", "rapid prototyping without tooling"]
composes_with: ["chain-of-thought", "few-shot", "tool-augmented-prompting", "retrieval-augmented-generation"]

tags: ["prompt-programming", "constrained-generation", "query-language", "structured-output", "type-safety", "python"]
---

# LMQL (Language Model Query Language)

> **One-line summary:** An SQL-inspired query language for LLMs that combines natural language prompts with programmatic constraints, type annotations, and control flow to guarantee structured, valid outputs.

## Overview

LMQL (Language Model Query Language) reimagines prompting as programming. Developed by Beurer-Kellner et al. at ETH Zurich, LMQL provides a Python-superset language where developers write prompts that seamlessly interleave natural language template strings with variables, constraints, and control flow. The key innovation is that constraints on output variables (e.g., "this must be one of these options" or "this must be a valid integer") are enforced during decoding through token masking, not through post-hoc validation and retry.

Traditional prompting treats the LLM as a black box: you send a string and hope the output conforms to your expectations. When it doesn't, you retry, parse and fix, or add more instructions. LMQL shifts this paradigm by giving developers compile-time and decode-time guarantees about output structure. A constraint like `STOPS_AT(answer, '.')` ensures generation halts at the first period, while `answer in ['yes', 'no', 'maybe']` restricts the output vocabulary at each token to only tokens that could lead to one of these valid completions.

The language compiles LMQL programs into optimized inference procedures that minimize the number of tokens generated and the number of LLM calls. By eagerly pruning invalid token continuations, LMQL can be both more reliable and more efficient than unconstrained generation followed by validation. The trade-off is that LMQL requires a Python runtime and model access that supports token-level probability inspection or constrained decoding.

## How It Works

1. **Query Definition:** Write an LMQL query that combines a prompt template with typed output variables (marked with `[VARIABLE_NAME]` syntax in the prompt string).
2. **Constraint Specification:** Define constraints on output variables using a `where` clause. Constraints can restrict values to sets, patterns, lengths, or custom predicates.
3. **Compilation:** The LMQL compiler analyzes the query and constraints, generating an optimized decoding strategy that enforces constraints at the token level.
4. **Constrained Decoding:** During inference, at each decoding step, the runtime masks out tokens that would violate constraints, ensuring only valid continuations are sampled.
5. **Result Extraction:** Output variables are returned as structured Python objects that are guaranteed to satisfy all specified constraints.

### Diagram

```
┌─────────────────────────────────────────┐
│           LMQL Query                     │
│  ┌─────────────────────────────────┐    │
│  │  Prompt template with           │    │
│  │  [VARIABLE] placeholders        │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  where VARIABLE constraints     │    │
│  │  (type, set, regex, length)     │    │
│  └─────────────────────────────────┘    │
└────────────────┬────────────────────────┘
                 │
                 ▼
      ┌────────────────────┐
      │   LMQL Compiler    │
      │   Analyze & plan   │
      │   decoding         │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │  Constrained       │
      │  Token-by-Token    │
      │  Decoding          │
      │  ┌──────────────┐  │
      │  │ Token mask:  │  │
      │  │ valid tokens │  │
      │  │ only         │  │
      │  └──────────────┘  │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │  Structured Output │
      │  Variables with    │
      │  guaranteed types  │
      └────────────────────┘
```

## Template

**Basic LMQL query structure:**
```python
import lmql

@lmql.query
def classify_sentiment(text):
    '''lmql
    "Review: {text}\n"
    "Sentiment: [SENTIMENT]"
    where SENTIMENT in ["positive", "negative", "neutral"]
    '''

@lmql.query
def extract_info(document):
    '''lmql
    "Extract information from the following document.\n"
    "Document: {document}\n"
    "Name: [NAME]\n"
    "Age: [AGE]\n"
    "Occupation: [OCCUPATION]"
    where STOPS_AT(NAME, "\n") and
          INT(AGE) and
          STOPS_AT(OCCUPATION, "\n")
    '''
```

## Examples

### Example 1: Constrained Classification

**Input (LMQL query):**
```python
import lmql

@lmql.query
def classify_intent(user_message):
    '''lmql
    "Classify the following customer message into a support category.\n\n"
    "Message: {user_message}\n\n"
    "Category: [CATEGORY]\n"
    "Confidence: [CONFIDENCE]\n"
    "Requires escalation: [ESCALATION]"
    where CATEGORY in ["billing", "technical", "account", "general"] and
          CONFIDENCE in ["high", "medium", "low"] and
          ESCALATION in ["yes", "no"]
    '''

result = classify_intent("I was charged twice for my subscription last month")
```

**Output:**
```python
{
    "CATEGORY": "billing",
    "CONFIDENCE": "high",
    "ESCALATION": "no"
}
```

### Example 2: Multi-Step Reasoning with Constraints

**Input (LMQL query):**
```python
import lmql

@lmql.query
def math_reasoning(problem):
    '''lmql
    "Solve the following math problem step by step.\n\n"
    "Problem: {problem}\n\n"
    "Step 1: [STEP1]\n"
    "Step 2: [STEP2]\n"
    "Step 3: [STEP3]\n"
    "Final answer: [ANSWER]"
    where STOPS_AT(STEP1, "\n") and len(STEP1) < 200 and
          STOPS_AT(STEP2, "\n") and len(STEP2) < 200 and
          STOPS_AT(STEP3, "\n") and len(STEP3) < 200 and
          INT(ANSWER)
    '''

result = math_reasoning(
    "A store sells apples at $2 each. If you buy 5 or more, you get a 20% "
    "discount. How much do 8 apples cost?"
)
```

**Output:**
```python
{
    "STEP1": "The base price for 8 apples is 8 x $2 = $16.",
    "STEP2": "Since 8 >= 5, the 20% discount applies: $16 x 0.20 = $3.20 discount.",
    "STEP3": "The final price is $16 - $3.20 = $12.80.",
    "ANSWER": 12
}
```

## When to Use

- Applications requiring guaranteed output structure (JSON schemas, enumerations)
- Classification tasks where the output must be one of a known set of values
- Multi-variable extraction where each field has type constraints
- Pipelines where downstream code depends on output conforming to a specific format
- When retry-on-invalid-output loops are too costly or unreliable
- Building production systems that need deterministic output structure

## When to Avoid

- Open-ended creative generation with no structural requirements
- Quick prototyping where the overhead of LMQL syntax is not justified
- Models accessed only through APIs that do not support logit manipulation
- Teams without Python expertise
- Simple single-variable extraction where a regex on free-form output suffices
- When the constraint space is so complex that token masking becomes too restrictive

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | Negative | Constraints often reduce tokens by stopping early |
| Latency | ~0.8-1.0x | Constrained decoding can be faster due to early stopping |
| Quality gain | High | Eliminates format errors and invalid outputs entirely |
| Reliability | Very high | Constraints are enforced at decode time, not post-hoc |
| Implementation | Medium | Requires LMQL runtime and compatible model backend |
| Learning curve | Medium | New syntax on top of Python, but well-documented |

## Variants

- **Scripted LMQL:** Use Python control flow (if/else, for loops) within LMQL queries to create dynamic, conditional prompts.
- **Nested LMQL:** Call LMQL queries from within other LMQL queries for modular, composable prompt programs.
- **Distribution LMQL:** Use `distribution` clause to get probability distributions over constrained outputs rather than single samples.
- **Beam Search LMQL:** Combine constraints with beam search to find the highest-probability valid completion.
- **Chat LMQL:** Use LMQL with chat-formatted models, constraining assistant responses within a multi-turn conversation.

## Composability

- **LMQL + Chain-of-Thought:** Define intermediate reasoning variables with length constraints, followed by a constrained answer variable.
- **LMQL + Few-Shot:** Embed examples in the prompt template while constraining the output format, combining the benefits of both.
- **LMQL + Tool Use:** Use Python functions within LMQL queries to call tools, then constrain how the model uses tool results.
- **LMQL + RAG:** Retrieve context dynamically in the Python portion, inject it into the LMQL prompt, and constrain the answer format.

## Limitations

- Requires model backends that expose token-level logits (not all APIs support this)
- Learning curve for developers unfamiliar with the LMQL syntax
- Overly tight constraints can degrade output quality by restricting the model too much
- Limited ecosystem compared to plain prompt engineering --- fewer community examples
- Debugging constrained decoding issues can be non-trivial
- Performance overhead of the LMQL runtime itself (compilation and constraint checking)
- Not all models are equally well-supported by the LMQL backend
- Constraint violations at the semantic level (factual correctness) are still not caught

## Sources

- **Primary:** [Prompting Is Programming: A Query Language for Large Language Models](https://arxiv.org/abs/2212.06094) — Beurer-Kellner, Fischer & Vechev, 2023
- **Code:** [LMQL GitHub Repository](https://github.com/eth-sri/lmql) — Open-source implementation
- **Documentation:** [LMQL Documentation](https://lmql.ai/docs/) — Official docs and tutorials
- **Venue:** PLDI 2023 (ACM SIGPLAN Conference on Programming Language Design and Implementation)
