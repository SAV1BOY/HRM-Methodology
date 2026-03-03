---
id: output-format
name: "Output Format Control"
aliases:
  - output-format
  - format-control
  - structured-output
  - response-formatting
  - output-structure
  - format-specification
category: foundations
family: instruction-based
year: 2022
authors:
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
  - structured data extraction to JSON or XML
  - generating parseable machine-readable output
  - table generation for reports
  - enforcing consistent response structure
  - API response formatting
  - downstream pipeline integration
avoid_when:
  - open-ended creative tasks where format constrains expression
  - model consistently fails to follow the format without examples
  - format is so complex it confuses the model
  - natural conversational responses are preferred
  - format overhead exceeds the content value
composes_with:
  - zero-shot
  - few-shot
  - one-shot
  - role-prompting
  - prompt-scaffolding
  - context-stuffing
  - chain-of-thought
tags:
  - formatting
  - structured-output
  - instruction-based
  - foundational
  - parsing
  - machine-readable
---

# Output Format Control

> **One-line summary:** Explicitly specify the desired output structure -- JSON, XML, markdown, table, or custom format -- in the prompt instruction to ensure the model produces consistently parseable and predictable responses.

## Overview

Output format control is the practice of instructing a language model to produce its response in a specific structural format rather than free-form prose. This technique evolved organically alongside the development of instruction-tuned models and became a critical component of production AI systems where model outputs need to be parsed, stored, or consumed by downstream software. While no single paper introduced this technique, it is a foundational practice documented extensively in OpenAI's API documentation (2022 onwards), Anthropic's prompt engineering guides, and Google's Gemini best practices.

The motivation for output format control is straightforward: language models naturally generate free-text responses, but most production applications require structured data. A sentiment analysis pipeline needs JSON with specific fields, a reporting system needs markdown tables, a data extraction workflow needs consistently structured records. Without explicit format instructions, models produce variable output structures that break downstream parsers and require expensive post-processing. Format control transforms the model's output from unpredictable prose into reliable structured data.

Modern instruction-tuned models have been specifically trained to follow format directives, making this technique highly effective. Models like GPT-4, Claude, and Gemini can reliably produce valid JSON, XML, markdown tables, CSV, YAML, and custom delimited formats when properly instructed. Some API providers (OpenAI's structured outputs, Anthropic's tool use) now offer native format enforcement at the API level, guaranteeing syntactic validity. However, prompt-level format control remains essential for customizing the content structure within any format and for working with providers that lack native format enforcement.

## How It Works

1. **Choose the output format.** Select the format that best serves the downstream consumer: JSON for APIs, markdown tables for reports, XML for document processing, CSV for spreadsheets, YAML for configuration-like outputs.

2. **Define the schema explicitly.** Specify the exact fields, data types, nesting structure, and any constraints. The more precise the schema definition, the more consistent the output.

3. **Provide the format specification in the prompt.** Include the schema or format description as part of the instruction. For JSON, provide the exact key names and expected value types. For tables, specify column headers and data expectations.

4. **Optionally include a format example.** Combining format instructions with a one-shot example that demonstrates the format dramatically increases compliance. This bridges format control with one-shot prompting.

5. **Validate the output.** Parse the generated output to verify structural validity. Implement retry logic or fallback strategies for format failures.

### Diagram

```
┌─────────────────────────────────────────┐
│  TASK INSTRUCTION                        │
│  "Extract all mentioned products,        │
│   their prices, and availability."       │
├─────────────────────────────────────────┤
│  FORMAT SPECIFICATION                    │
│  "Respond in JSON format:               │
│   {                                      │
│     'products': [                        │
│       {                                  │
│         'name': string,                  │
│         'price': number,                 │
│         'currency': string,              │
│         'in_stock': boolean              │
│       }                                  │
│     ]                                    │
│   }"                                     │
├─────────────────────────────────────────┤
│  INPUT TEXT                              │
│  "The Widget Pro costs $49.99 and is     │
│   currently in stock. The Gadget Mini    │
│   at $29.99 is sold out."               │
├─────────────────────────────────────────┤
│             ▼                            │
│  ┌────────────────────┐                  │
│  │       MODEL         │                  │
│  │ (format-controlled) │                  │
│  └─────────┬──────────┘                  │
│             ▼                            │
│  OUTPUT (valid JSON):                    │
│  {                                       │
│    "products": [                         │
│      {"name": "Widget Pro",              │
│       "price": 49.99,                    │
│       "currency": "USD",                 │
│       "in_stock": true},                 │
│      {"name": "Gadget Mini",             │
│       "price": 29.99,                    │
│       "currency": "USD",                 │
│       "in_stock": false}                 │
│    ]                                     │
│  }                                       │
└─────────────────────────────────────────┘
```

## Template

**JSON output template:**

```
{task_instruction}

Respond in the following JSON format:
{json_schema}

Input: {input_text}
```

**Markdown table template:**

```
{task_instruction}

Present your response as a markdown table with the following columns:
| {column_1} | {column_2} | {column_3} | {column_4} |

{input_text}
```

**Multi-format template:**

```
{task_instruction}

Structure your response as follows:

## Summary
(2-3 sentence overview)

## Details
(bullet points with key findings)

## Data
(JSON object with extracted values)

## Confidence
(high/medium/low with brief justification)

Input: {input_text}
```

## Examples

### Example 1: Structured Data Extraction (JSON)

**Input prompt:**
```
Extract all person entities from the following text. For each person, capture their name, role, and organization.

Respond in this exact JSON format:
{
  "persons": [
    {
      "name": "Full Name",
      "role": "Their title or role",
      "organization": "Their company or organization"
    }
  ]
}

Text: "At the press conference, CEO Sarah Mitchell of Quantum Dynamics announced the partnership with Dr. James Park, head of AI research at Stanford University. CFO Lisa Chen noted that the deal's financial terms were reviewed by lead counsel Michael Torres from Baker & Associates."
```

**Expected output:**
```json
{
  "persons": [
    {
      "name": "Sarah Mitchell",
      "role": "CEO",
      "organization": "Quantum Dynamics"
    },
    {
      "name": "James Park",
      "role": "Head of AI Research",
      "organization": "Stanford University"
    },
    {
      "name": "Lisa Chen",
      "role": "CFO",
      "organization": "Quantum Dynamics"
    },
    {
      "name": "Michael Torres",
      "role": "Lead Counsel",
      "organization": "Baker & Associates"
    }
  ]
}
```

### Example 2: Comparison Table (Markdown)

**Input prompt:**
```
Compare the three database options described below. Present your analysis as a markdown table with columns: Feature, PostgreSQL, MongoDB, Redis. Include rows for: Data Model, Best Use Case, Scalability, ACID Compliance, and Learning Curve.

PostgreSQL is a relational database known for strong ACID compliance and complex query support. MongoDB is a document database ideal for flexible schemas and horizontal scaling. Redis is an in-memory key-value store optimized for caching and real-time applications.
```

**Expected output:**
```
| Feature          | PostgreSQL              | MongoDB                 | Redis                    |
|------------------|-------------------------|-------------------------|--------------------------|
| Data Model       | Relational (tables)     | Document (JSON/BSON)    | Key-Value (in-memory)    |
| Best Use Case    | Complex queries, joins  | Flexible schemas, CMS   | Caching, real-time data  |
| Scalability      | Vertical (read replicas)| Horizontal (sharding)   | Horizontal (clustering)  |
| ACID Compliance  | Full ACID               | Document-level ACID     | Limited (single-command) |
| Learning Curve   | Moderate (SQL knowledge)| Low-Moderate             | Low                      |
```

## When to Use

- **Machine-parseable output.** When downstream systems need to consume the model's output programmatically (APIs, data pipelines, databases).
- **Consistency across requests.** When processing many inputs and all outputs must conform to the same schema for batch processing.
- **Data extraction tasks.** When pulling structured information (entities, relationships, metrics) from unstructured text.
- **Report generation.** When producing formatted documents, tables, or dashboards from raw data.
- **API integration.** When the model output feeds directly into another service that expects a specific format.
- **Quality assurance.** Format constraints serve as a lightweight validation layer -- if the output does not parse correctly, it can be flagged for review.

## When to Avoid

- **Open-ended creative tasks.** Strict format requirements can constrain creative expression and produce stilted, template-like outputs.
- **Conversational interactions.** When the model should respond naturally, format specifications feel robotic and hinder engagement.
- **Complex nested formats.** Very deeply nested JSON schemas or intricate XML structures may confuse the model, leading to more format errors than they prevent.
- **Small models.** Smaller models (< 7B parameters) struggle with complex format compliance. For these models, simpler format requirements or post-processing may be more reliable.
- **When native enforcement is available.** If the API provides structured output mode (e.g., OpenAI's JSON mode, function calling), prefer native enforcement over prompt-level instructions for guaranteed validity.

## Cost & Performance

| Metric              | Value       | Notes                                                  |
|----------------------|-------------|--------------------------------------------------------|
| Token cost           | Low         | Format spec adds 20-100 tokens; output may be more verbose |
| Latency              | Low         | Negligible impact from format instructions              |
| API calls            | 1           | Single call per task                                    |
| Format compliance    | High        | 90-99% with modern instruction-tuned models             |
| Parsing success rate | High        | 85-98% valid parse rate; higher with native enforcement |
| Setup effort         | Low         | Define schema once, reuse across requests               |
| Maintenance          | Low         | Schema updates require only prompt changes              |

## Variants

- **JSON mode:** Instruct the model to produce valid JSON. Many providers offer native JSON mode at the API level for guaranteed validity. Schema-based variants (e.g., OpenAI's structured outputs) enforce specific key-value structures.
- **XML format:** Useful when output needs to integrate with XML-based systems or when hierarchical structure with attributes is important. Models generally produce valid XML with explicit instructions.
- **Markdown format:** Tables, headers, lists, and code blocks. Natural for report generation and documentation tasks. Most models handle markdown natively.
- **CSV/TSV format:** Tabular data in delimited format for spreadsheet consumption. Simpler than JSON for flat data structures but limited for nested data.
- **YAML format:** Human-readable structured data format. Useful for configuration-like outputs. Indentation sensitivity can cause issues with some models.
- **Custom delimited format:** Application-specific formats using custom delimiters (e.g., `|||`, `---`, `###`). Useful when standard formats do not fit the use case.
- **Hybrid format:** Combine free text with structured sections (e.g., prose explanation followed by JSON data block). Balances human readability with machine parseability.

## Composability

- **+ Zero-Shot:** The most common combination. A clear instruction plus format specification. "Classify the sentiment and respond in JSON: {'sentiment': ..., 'confidence': ...}."
- **+ One-Shot / Few-Shot:** Provide examples in the target format to demonstrate both the schema and the expected content patterns. This is the highest-reliability approach for format compliance.
- **+ Role Prompting:** Define an expert role and specify the output format. "You are a data analyst. Present your findings in the following table format..."
- **+ Prompt Scaffolding:** Use XML tags to separate format specification from instructions and input. `<format>JSON schema here</format> <input>Data here</input>`.
- **+ Context Stuffing:** Extract structured data from provided documents. Combine context injection with format specification for grounded, structured extraction.
- **+ Chain-of-Thought:** Ask the model to reason through the problem in a `<thinking>` section, then produce the final answer in the specified format. Separates reasoning from structured output.

## Limitations

- **Format vs. content trade-off.** Strict format requirements can cause the model to prioritize structural compliance over content quality, producing correctly formatted but shallow or incomplete responses.
- **Escaping and special characters.** JSON output may fail when the content contains quotes, backslashes, or Unicode characters that require escaping. Models sometimes produce invalid escape sequences.
- **Inconsistent null handling.** Models may represent missing values as `null`, `"N/A"`, `""`, `"unknown"`, or omit the field entirely, unless explicitly instructed on null handling.
- **Nested structure complexity.** Deeply nested formats (3+ levels) see increased error rates. Models may close brackets prematurely, duplicate fields, or produce inconsistent nesting.
- **Format drift in long outputs.** For outputs with many items (e.g., extracting 50+ entities into a JSON array), the model may gradually deviate from the specified format as the generation progresses.
- **Model-specific compliance.** Different models have varying levels of format instruction following ability. Prompts optimized for one model may not transfer to another without adjustment.

## Sources

**Primary:**
- OpenAI. (2022-2024). "OpenAI API Documentation: Structured Outputs." https://platform.openai.com/docs/guides/structured-outputs
- Anthropic. (2023-2024). "Prompt Engineering Guide: Output Formatting." https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering

**Secondary:**
- Jiang, D., et al. (2024). "StructuredRAG: JSON Response Generation with Large Language Models." arXiv:2404.12057. https://arxiv.org/abs/2404.12057
- Tam, D., Masber, A., Raffel, C., Bansal, M., & Srivastava, S. (2023). "Let's Verify Step by Step." arXiv:2305.20050. https://arxiv.org/abs/2305.20050
- Google. (2023-2024). "Gemini API: Structured Output." https://ai.google.dev/gemini-api/docs/structured-output
