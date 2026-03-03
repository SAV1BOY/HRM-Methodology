---
id: prompt-scaffolding
name: "Prompt Scaffolding"
aliases:
  - prompt-scaffolding
  - xml-tagging
  - delimiter-prompting
  - structured-prompting
  - section-headers
  - prompt-structure
category: foundations
family: instruction-based
year: 2023
authors:
  - Anthropic
  - OpenAI
paper: null
paper_title: null
venue: null
code: null
complexity: low
token_cost: low
latency: low
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - complex multi-section prompts
  - separating instructions from data
  - preventing prompt injection
  - multi-document prompts requiring clear boundaries
  - system prompts with multiple behavioral rules
  - prompts mixing examples with context and instructions
avoid_when:
  - prompt is short and simple
  - scaffolding overhead exceeds content length
  - model does not respond well to XML or delimiters
  - task requires a natural conversational flow
composes_with:
  - zero-shot
  - few-shot
  - role-prompting
  - output-format
  - context-stuffing
  - chain-of-thought
  - prompt-repetition
tags:
  - structure
  - xml-tags
  - delimiters
  - instruction-based
  - foundational
  - prompt-organization
  - injection-defense
---

# Prompt Scaffolding

> **One-line summary:** Use XML tags, delimiters, section headers, and other structural markers to organize complex prompts into clearly delineated sections, improving model comprehension and preventing confusion between instructions, context, examples, and user input.

## Overview

Prompt scaffolding is the practice of using structural markers -- XML tags, triple backticks, dashes, section headers, or custom delimiters -- to organize a prompt into clearly separated sections. The technique was popularized by Anthropic's prompt engineering documentation (2023), which demonstrated that XML-tagged prompts significantly improve Claude's ability to distinguish between instructions, context, examples, and user input. OpenAI similarly recommends delimiters in their prompt engineering best practices for GPT models.

The core problem that scaffolding solves is ambiguity in complex prompts. When a prompt contains multiple components -- a system instruction, reference documents, few-shot examples, format specifications, and the actual user query -- the model must infer where each component begins and ends. Without structural markers, the model may treat a passage from a reference document as an instruction, interpret an example output as the actual task, or confuse the user's input with the system's rules. Scaffolding eliminates this ambiguity by providing explicit structural boundaries.

Beyond clarity, prompt scaffolding serves as a defense mechanism against prompt injection attacks. When user input is wrapped in clearly delimited tags (e.g., `<user_input>...</user_input>`), the model can more easily distinguish between trusted system instructions and potentially adversarial user content. While not a complete security solution, scaffolding is a recommended layer in defense-in-depth strategies for production AI applications. The technique also improves prompt maintainability: well-scaffolded prompts are easier to read, modify, debug, and version-control than monolithic text blocks.

## How It Works

1. **Identify prompt components.** Enumerate all distinct sections of the prompt: system instructions, role definition, context documents, examples, format specification, constraints, and user query.

2. **Choose a scaffolding style.** Select the structural markers appropriate for the model and use case: XML tags (most explicit), markdown headers (human-readable), triple backticks (code-friendly), or custom delimiters (application-specific).

3. **Wrap each component.** Enclose each prompt section in its chosen structural markers with descriptive labels. Use consistent naming conventions across prompts for maintainability.

4. **Order sections logically.** Place components in a natural progression: role/system instructions first, then context, then examples, then constraints, then the query. This mirrors how a human would process the information.

5. **Test boundary adherence.** Verify that the model correctly treats each section according to its role -- that it follows instructions, references context, mimics examples, and responds to the query without crossing boundaries.

### Diagram

```
┌──────────────────────────────────────────┐
│  <system>                                 │
│    Role definition and behavioral rules   │
│  </system>                                │
├──────────────────────────────────────────┤
│  <context>                                │
│    Reference documents and data           │
│  </context>                               │
├──────────────────────────────────────────┤
│  <examples>                               │
│    <example>                              │
│      Input: ... → Output: ...             │
│    </example>                             │
│  </examples>                              │
├──────────────────────────────────────────┤
│  <constraints>                            │
│    Output format and rules                │
│  </constraints>                           │
├──────────────────────────────────────────┤
│  <query>                                  │
│    The actual user question or task       │
│  </query>                                 │
├──────────────────────────────────────────┤
│              ▼                            │
│  ┌─────────────────────┐                  │
│  │       MODEL          │                  │
│  │  (scaffold-parsed)   │                  │
│  └──────────┬──────────┘                  │
│              ▼                            │
│  <response>                               │
│    Structured output following rules      │
│  </response>                              │
└──────────────────────────────────────────┘
```

## Template

**XML tag scaffolding:**

```
<system>
{role_and_behavioral_instructions}
</system>

<context>
{reference_documents_or_data}
</context>

<examples>
<example>
<input>{example_input_1}</input>
<output>{example_output_1}</output>
</example>
</examples>

<constraints>
{output_format_and_rules}
</constraints>

<query>
{user_question_or_task}
</query>
```

**Markdown header scaffolding:**

```
## System Instructions
{role_and_behavioral_instructions}

## Reference Context
{reference_documents_or_data}

## Examples
### Example 1
Input: {example_input}
Output: {example_output}

## Output Requirements
{format_and_constraints}

## Task
{user_question_or_task}
```

**Delimiter scaffolding:**

```
{role_and_instructions}

---CONTEXT START---
{reference_documents}
---CONTEXT END---

---EXAMPLES START---
{examples}
---EXAMPLES END---

---TASK---
{user_question}
```

## Examples

### Example 1: Complex RAG Prompt with Multiple Documents

**Input prompt:**
```
<system>
You are a compliance analyst at a financial services firm. Answer questions using ONLY the provided regulatory documents. If the documents do not contain sufficient information, state this clearly. Always cite the specific document and section number.
</system>

<documents>
<document id="reg-101" title="KYC Requirements v4.2">
Section 2.1: All new customer accounts require identity verification through two forms of government-issued identification. Verification must be completed within 30 business days of account opening.

Section 2.3: Enhanced due diligence (EDD) is required for customers classified as high-risk, including politically exposed persons (PEPs), customers from high-risk jurisdictions, and accounts with expected transaction volumes exceeding $1M annually.

Section 3.1: Customer risk ratings must be reviewed annually. Any material change in customer activity triggers an immediate re-review regardless of the annual schedule.
</document>

<document id="reg-205" title="Transaction Monitoring Standards">
Section 1.2: All transactions exceeding $10,000 must be automatically flagged for review. Suspicious activity reports (SARs) must be filed within 30 days of detection.

Section 1.5: Wire transfers to jurisdictions on the restricted list require pre-approval from the compliance officer and cannot be processed automatically.
</document>
</documents>

<constraints>
- Answer in 2-3 sentences maximum
- Cite specific document IDs and section numbers
- If information is not in the documents, say: "This information is not covered in the provided regulatory documents."
</constraints>

<query>
A new high-risk customer opened an account last week. What verification requirements apply, and how soon must they be completed?
</query>
```

**Expected output:**
```
Per reg-101, Section 2.1, the customer requires identity verification through two forms of government-issued identification, which must be completed within 30 business days of account opening. Additionally, since the customer is classified as high-risk, Section 2.3 requires enhanced due diligence (EDD) procedures to be applied.
```

### Example 2: Scaffolded Few-Shot with Format Control

**Input prompt:**
```
<instructions>
Convert natural language date descriptions into ISO 8601 format (YYYY-MM-DD). Handle relative dates, holidays, and informal expressions. If the date is ambiguous, provide the most likely interpretation and note the ambiguity.
</instructions>

<examples>
<example>
<input>next Tuesday</input>
<output>{"date": "2025-03-11", "confidence": "high", "note": null}</output>
</example>

<example>
<input>the last day of February this year</input>
<output>{"date": "2025-02-28", "confidence": "high", "note": "2025 is not a leap year"}</output>
</example>

<example>
<input>Christmas</input>
<output>{"date": "2025-12-25", "confidence": "high", "note": "Assumed current year"}</output>
</example>
</examples>

<format>
Respond with a JSON object containing:
- "date": ISO 8601 date string
- "confidence": "high" | "medium" | "low"
- "note": clarifying note or null
</format>

<input>
two weeks from yesterday
</input>
```

**Expected output:**
```json
{"date": "2025-03-18", "confidence": "high", "note": "Calculated as yesterday (2025-03-04) plus 14 days"}
```

## When to Use

- **Complex multi-section prompts.** When the prompt contains 3 or more distinct components (instructions, context, examples, constraints, query) that could be confused with each other.
- **Multi-document contexts.** When injecting multiple reference documents, XML tags with `id` and `title` attributes help the model distinguish and cite sources accurately.
- **Prompt injection defense.** When user input is untrusted, wrapping it in explicit tags helps the model distinguish user content from system instructions.
- **Few-shot with long examples.** When examples contain multi-line or complex content, delimiters prevent the model from confusing example content with instructions.
- **Team-maintained prompts.** Well-scaffolded prompts are significantly easier for multiple developers to read, modify, and review.
- **System prompts in production.** Long system prompts with behavioral rules, constraints, and context benefit enormously from structural organization.

## When to Avoid

- **Short, simple prompts.** "Translate 'hello' to French" does not need XML scaffolding. The overhead adds unnecessary complexity.
- **Conversational interfaces.** In casual chat interactions, heavy scaffolding feels robotic and disrupts natural conversation flow.
- **Token-constrained environments.** XML tags and delimiters add token overhead (typically 5-20% for well-scaffolded prompts). In extreme token-constrained scenarios, this overhead matters.
- **Models that ignore scaffolding.** Some smaller or non-instruction-tuned models may not interpret XML tags or delimiters meaningfully, reducing the technique to wasted tokens.

## Cost & Performance

| Metric              | Value     | Notes                                                    |
|----------------------|-----------|----------------------------------------------------------|
| Token cost           | Low       | Tags add 5-20% overhead; negligible for long prompts     |
| Latency              | Low       | Minimal impact from structural markers                   |
| API calls            | 1         | Single call per task                                     |
| Comprehension boost  | High      | Significant improvement on multi-section prompts         |
| Injection resistance | Moderate  | Improves boundary detection but not a complete defense    |
| Maintainability      | High      | Well-scaffolded prompts are much easier to modify        |
| Debugging            | High      | Clear sections make it easy to isolate issues            |

## Variants

- **XML scaffolding:** Using XML tags (`<system>`, `<context>`, `<query>`). Most explicit and well-supported by models like Claude. Supports attributes for metadata (e.g., `<document id="1" source="policy.pdf">`).
- **Markdown scaffolding:** Using markdown headers (`## Instructions`, `## Context`, `## Task`). Human-readable and familiar to developers. Less explicit boundary detection than XML.
- **Delimiter scaffolding:** Using custom delimiters (`---`, `===`, `###`, `'''`). Lightweight and model-agnostic. Less structured than XML but lower token overhead.
- **Triple-backtick scaffolding:** Using code fences to delineate content blocks. Natural for code-heavy prompts and technical content. Well-supported across models.
- **Nested scaffolding:** Multi-level structural hierarchy (e.g., `<documents><document><section>`). Useful for complex prompts but increases complexity and token cost.
- **Attributed scaffolding:** XML tags with metadata attributes (e.g., `<source url="..." date="..." relevance="high">`). Provides the model with additional context about each section.

## Composability

Prompt scaffolding is the universal composability enabler -- it helps other techniques work together cleanly:

- **+ Zero-Shot:** Wrap instructions in `<instructions>` tags and input in `<input>` tags. Simple but effective for preventing boundary confusion.
- **+ Few-Shot:** Wrap each example in `<example>` tags with `<input>` and `<output>` sub-tags. Critical for examples containing complex content that could be confused with instructions.
- **+ Role Prompting:** Place the role definition in a `<system>` or `<role>` tag, clearly separated from the task instruction.
- **+ Context Stuffing:** Wrap each document in `<document>` tags with identifying attributes. Enables source citation and prevents document content from being interpreted as instructions.
- **+ Output Format Control:** Use a `<format>` or `<output_requirements>` section to isolate format specifications from other prompt components.
- **+ Chain-of-Thought:** Define `<thinking>` tags for the reasoning section and `<answer>` tags for the final output, cleanly separating reasoning traces from conclusions.
- **+ Prompt Repetition:** Scaffolding sections allow critical instructions to be repeated at the beginning and end of specific sections without creating confusion.

## Limitations

- **Model-dependent effectiveness.** XML scaffolding works best with models explicitly trained on XML-tagged prompts (Claude). Other models may benefit more from markdown or delimiter styles.
- **Over-scaffolding risk.** Excessive structural markers can fragment the prompt into disconnected pieces, making it harder for the model to synthesize information across sections.
- **Not a security guarantee.** While scaffolding improves boundary detection for prompt injection, it is not a reliable security boundary. Determined adversaries can still craft inputs that override scaffolding.
- **Token overhead for short prompts.** On very short prompts, the tags themselves may constitute a significant percentage of the total token count.
- **Inconsistent tag interpretation.** Models may sometimes include scaffolding tags in their output (e.g., outputting `<response>` tags), requiring post-processing to strip structural markers.
- **Maintenance complexity.** Deeply nested scaffolding structures can become difficult to maintain, especially when prompt changes affect multiple nested sections.

## Sources

**Primary:**
- Anthropic. (2023-2024). "Prompt Engineering Guide: Use XML Tags." https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags

**Secondary:**
- OpenAI. (2023-2024). "Prompt Engineering Best Practices: Use Delimiters." https://platform.openai.com/docs/guides/prompt-engineering
- Riley Goodside. (2022-2023). Various posts on prompt injection defense through structural prompting. https://twitter.com/goodaborea
- Simon Willison. (2023). "Prompt Injection: What's the Worst That Can Happen?" https://simonwillison.net/2023/Apr/14/worst-that-can-happen/
- Google. (2024). "Gemini API: Prompt Design Strategies." https://ai.google.dev/gemini-api/docs/prompting-strategies
