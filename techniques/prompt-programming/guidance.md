---
id: guidance
name: "Guidance (Microsoft)"
aliases: ["Microsoft Guidance", "Guidance Templates", "Guidance Language"]
category: prompt-programming
family: template-generation
year: 2023
authors: ["Scott Lundberg", "Marco Tulio Ribeiro"]
paper: null
paper_title: null
venue: null
code: "https://github.com/guidance-ai/guidance"

complexity: medium
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for: ["interleaved generation and control flow", "guaranteed output structure", "multi-step prompt programs", "template-based generation", "role-based chat construction"]
avoid_when: ["simple single-turn generation", "no Python environment", "API-only models without streaming", "rapid prototyping without tooling"]
composes_with: ["chain-of-thought", "few-shot", "tool-augmented-prompting", "retrieval-augmented-generation"]

tags: ["prompt-programming", "template", "structured-output", "control-flow", "interleaved-generation", "python"]
---

# Guidance (Microsoft)

> **One-line summary:** A template-based prompt programming framework from Microsoft that interleaves natural language generation with programmatic control flow, enabling guaranteed output structure through stateful, token-by-token execution.

## Overview

Guidance is an open-source library from Microsoft that treats prompting as programming through a powerful templating system. Unlike traditional prompting where you send a complete string and receive a complete response, Guidance executes prompts token by token, interleaving model generation with programmatic logic. This allows developers to define exactly where the model should generate, what constraints apply, and how control flow (conditionals, loops, function calls) should interact with generated text.

The core insight behind Guidance is that many prompting challenges --- formatting issues, hallucinated structures, inconsistent outputs --- arise because the developer has no control over the generation process between the first and last token. Guidance solves this by treating the prompt as a program that executes incrementally. When the program reaches a `gen()` call, the model generates tokens. When it reaches a `select()` call, the model chooses from predefined options. When it reaches Python logic, that logic executes deterministically. The result is a seamless blend of neural generation and classical programming.

Guidance's template syntax is inspired by Handlebars, making it familiar to web developers, while its Python API provides full programmatic control for more complex use cases. The library supports multiple backends including local models (llama.cpp, transformers) and API models (OpenAI, Anthropic), though local models benefit most from token-level control. Guidance programs are both more reliable than free-form prompts and more efficient, since constrained decoding avoids generating invalid tokens.

## How It Works

1. **Template Definition:** Write a Guidance template using Handlebars-like syntax or Python API. Templates contain literal text, generation blocks (`{{gen}}` or `{{select}}`), and control flow blocks (`{{#if}}`, `{{#each}}`).
2. **Program Compilation:** Guidance compiles the template into an execution plan that interleaves deterministic text insertion with model generation steps.
3. **Stateful Execution:** The program executes token by token. Literal text is appended to the prompt directly. Generation blocks invoke the model with appropriate constraints. Control flow evaluates based on previously generated values.
4. **Variable Capture:** Each generation block captures its output into a named variable, which can be referenced by subsequent parts of the template.
5. **Result Assembly:** The completed program returns a structured object with all captured variables, plus the full rendered text.

### Diagram

```
┌────────────────────────────────────────────────┐
│              Guidance Template                   │
│                                                  │
│  "Analyze {{input}}\n"       ← literal text     │
│  "Category: {{select opts}}" ← constrained gen  │
│  "{{#if detailed}}"          ← control flow     │
│  "Details: {{gen max=100}}"  ← free generation  │
│  "{{/if}}"                                      │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
        ┌────────────────────┐
        │  Execution Engine   │
        │                     │
        │  Token 1: literal   │──▶ append "Analyze "
        │  Token 2: literal   │──▶ append input value
        │  Token 3: select    │──▶ model chooses from opts
        │  Token 4: if-check  │──▶ evaluate condition
        │  Token 5: gen       │──▶ model generates freely
        │  ...                │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  Structured Result  │
        │  {                  │
        │    category: "...", │
        │    details: "..."   │
        │  }                  │
        └────────────────────┘
```

## Template

**Basic Guidance template (Handlebars-style):**
```python
import guidance

@guidance
def analyze(lm, text):
    lm += f"Analyze the following text.\n\nText: {text}\n\n"
    lm += f"Sentiment: {select(['positive', 'negative', 'neutral'], name='sentiment')}\n"
    lm += f"Key topic: {gen(max_tokens=20, stop='\n', name='topic')}\n"
    lm += f"Summary: {gen(max_tokens=100, stop='\n', name='summary')}"
    return lm
```

**With control flow:**
```python
import guidance

@guidance
def review_analysis(lm, review_text):
    lm += f"Review: {review_text}\n"
    lm += f"Rating: {select(['1', '2', '3', '4', '5'], name='rating')}\n"
    lm += f"Sentiment: {select(['positive', 'negative', 'mixed'], name='sentiment')}\n"

    if int(lm['rating']) <= 2:
        lm += f"Issues identified: {gen(max_tokens=150, stop='\n', name='issues')}\n"
        lm += f"Suggested action: {gen(max_tokens=100, stop='\n', name='action')}"
    else:
        lm += f"Strengths noted: {gen(max_tokens=150, stop='\n', name='strengths')}"

    return lm
```

## Examples

### Example 1: Structured Entity Extraction

**Input (Guidance program):**
```python
import guidance

@guidance
def extract_person(lm, text):
    lm += f"""Extract person information from the text below.

Text: {text}

Name: {gen(max_tokens=30, stop='\\n', name='name')}
Age: {gen(regex='[0-9]+', name='age')}
Occupation: {gen(max_tokens=30, stop='\\n', name='occupation')}
Location: {gen(max_tokens=30, stop='\\n', name='location')}
"""
    return lm

model = guidance.models.OpenAI("gpt-4")
result = model + extract_person(
    "Dr. Sarah Chen, a 42-year-old neurosurgeon from Boston, recently published "
    "a groundbreaking study on neural plasticity."
)
```

**Output:**
```python
{
    "name": "Dr. Sarah Chen",
    "age": "42",
    "occupation": "neurosurgeon",
    "location": "Boston"
}
```

### Example 2: Conditional Multi-Step Analysis

**Input (Guidance program):**
```python
import guidance

@guidance
def triage_ticket(lm, ticket_text):
    lm += f"""You are a support ticket triage system.

Ticket: {ticket_text}

Priority: {select(['critical', 'high', 'medium', 'low'], name='priority')}
Category: {select(['bug', 'feature_request', 'question', 'account'], name='category')}
"""

    if lm['priority'] in ['critical', 'high']:
        lm += f"Escalation reason: {gen(max_tokens=80, stop='\\n', name='escalation_reason')}\n"
        lm += f"Recommended team: {select(['engineering', 'security', 'infrastructure', 'support_lead'], name='team')}"
    else:
        lm += f"Auto-response appropriate: {select(['yes', 'no'], name='auto_respond')}"
        if lm['auto_respond'] == 'yes':
            lm += f"\nSuggested response: {gen(max_tokens=150, stop='\\n', name='response')}"

    return lm

model = guidance.models.OpenAI("gpt-4")
result = model + triage_ticket(
    "URGENT: Production database is returning 500 errors on all write "
    "operations since the last deployment 30 minutes ago. Multiple "
    "customers are affected."
)
```

**Output:**
```python
{
    "priority": "critical",
    "category": "bug",
    "escalation_reason": "Production database failure affecting all write operations and multiple customers post-deployment",
    "team": "infrastructure"
}
```

## When to Use

- Applications requiring guaranteed output schemas (JSON, enums, specific formats)
- Multi-step prompt programs where later steps depend on earlier generated values
- Classification tasks where outputs must be from a known set
- Data extraction pipelines with typed fields
- When retry loops for invalid formatting are too costly
- Building reliable, production-grade LLM-powered features

## When to Avoid

- Simple, single-turn free-form text generation
- Environments without Python runtime support
- When using API-only models where token-level control is limited
- Rapid prototyping where the Guidance learning curve slows iteration
- Tasks where unconstrained generation is actually desired
- When the team is not comfortable with programmatic prompt construction

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | Negative to neutral | Constrained generation often produces fewer tokens |
| Latency | ~0.8-1.2x | Select and constrained gen can be faster; overhead from runtime |
| Quality gain | High | Eliminates structural errors in output |
| Reliability | Very high | Constraints enforced during generation |
| Implementation | Medium | Requires learning Guidance API and template syntax |
| Backend support | Variable | Best with local models; API models have limited token control |

## Variants

- **Handlebars Mode:** Use `{{gen}}` and `{{select}}` in template strings for a more declarative style (legacy syntax).
- **Python API Mode:** Use `@guidance` decorated functions for full programmatic control with Python logic.
- **Chat Mode:** Use `with system():`, `with user():`, `with assistant():` context managers for chat-formatted models.
- **Regex-Constrained:** Use `gen(regex=...)` to constrain output to match a regular expression pattern.
- **Grammar-Constrained:** Use formal grammars (CFG) to constrain generation to syntactically valid outputs.

## Composability

- **Guidance + CoT:** Define intermediate reasoning variables (`thought = gen(...)`) before the constrained answer variable, combining free-form reasoning with structured output.
- **Guidance + Few-Shot:** Embed examples in the template using loops (`{{#each examples}}`) and constrain the output format to match.
- **Guidance + Tool Use:** Call Python functions between generation steps, using their results to inform subsequent generation.
- **Guidance + RAG:** Retrieve context in Python, inject it into the template, and constrain the model's answer to stay grounded.

## Limitations

- Token-level control works best with local models; API models offer limited constrained decoding
- Learning curve for the Guidance-specific syntax and execution model
- Debugging Guidance programs can be harder than debugging plain prompts
- Library must stay compatible with evolving model APIs and formats
- Overly tight constraints can make the model produce unnatural or low-quality text
- Not all model architectures or serving frameworks are supported equally
- Community and ecosystem are smaller than for plain prompting approaches
- Stateful execution model can be confusing for developers used to stateless API calls

## Sources

- **Code:** [Guidance GitHub Repository](https://github.com/guidance-ai/guidance) — Microsoft, open-source
- **Author:** Scott Lundberg (Microsoft Research) — creator of SHAP and Guidance
- **Related:** [LMQL: Prompting Is Programming](https://arxiv.org/abs/2212.06094) — Similar constrained generation approach
- **Related:** [Outlines: Structured Generation](https://github.com/dottxt-ai/outlines) — Alternative structured generation library
