---
id: outlines
name: "Outlines (Structured Generation)"
aliases: ["Outlines", "dottxt Outlines", "FSM-Based Generation", "Structured Text Generation"]
category: prompt-programming
family: constrained-generation
year: 2023
authors: ["Brandon T. Willard", "Rémi Louf"]
paper: null
paper_title: null
venue: null
code: "https://github.com/dottxt-ai/outlines"

complexity: medium
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for: ["guaranteed valid JSON output", "regex-constrained generation", "schema-conformant structured data", "type-safe API responses", "data extraction with known schemas"]
avoid_when: ["free-form text generation", "no access to model logits", "API-only models without structured output support", "simple tasks not needing format guarantees"]
composes_with: ["chain-of-thought", "few-shot", "retrieval-augmented-generation", "tool-augmented-prompting"]

tags: ["prompt-programming", "structured-output", "json", "regex", "fsm", "constrained-decoding", "type-safety"]
---

# Outlines (Structured Generation)

> **One-line summary:** A structured generation library that uses finite-state machines (FSMs) to guarantee LLM outputs conform to JSON schemas, regular expressions, or context-free grammars by constraining token selection at decode time.

## Overview

Outlines, developed by .txt (dottxt-ai), takes a fundamentally different approach to the problem of getting LLMs to produce structured output. Instead of hoping the model follows formatting instructions and retrying when it doesn't, Outlines mathematically guarantees that every generated token is part of a valid output by using finite-state machines to mask the token vocabulary at each decoding step. If you need valid JSON matching a Pydantic schema, Outlines ensures that every single generation will be valid --- not 95% of the time, but 100%.

The technical mechanism is elegant: given a target structure (a JSON schema, a regular expression, or a context-free grammar), Outlines pre-compiles a finite-state machine (FSM) that represents all valid output strings. At each decoding step, the FSM determines which tokens could appear next while staying on a path to a valid completion. All other tokens have their logits set to negative infinity, effectively removing them from consideration. The model then samples from only the valid tokens, ensuring the output is structurally perfect by construction.

This approach separates two concerns that traditional prompting conflates: content generation (what to say) and structural compliance (how to format it). The LLM focuses entirely on generating semantically appropriate content, while the FSM handles all structural concerns. The result is outputs that are both semantically relevant (the model's strength) and structurally valid (the FSM's guarantee). This is particularly valuable in production systems where downstream code parses the output and cannot tolerate malformed data.

## How It Works

1. **Schema Definition:** Define the desired output structure as a JSON schema (via Pydantic model), a regular expression, or a context-free grammar.
2. **FSM Compilation:** Outlines compiles the structure definition into a finite-state machine. Each state in the FSM represents a position in the valid output, and transitions correspond to valid next tokens.
3. **Index Building:** For each FSM state, Outlines pre-computes the set of vocabulary tokens that represent valid transitions. This index is built once and cached.
4. **Constrained Decoding:** During generation, at each step the FSM state determines which tokens are valid. Invalid token logits are masked (set to -infinity). The model samples from the remaining valid tokens.
5. **State Advancement:** After each token is sampled, the FSM advances to the corresponding next state. The process repeats until the FSM reaches an accepting state (valid completion).

### Diagram

```
┌───────────────────────────┐
│  Structure Definition      │
│  (Pydantic / regex / CFG)  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  FSM Compiler              │
│  Structure → State Machine │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  Token Index Builder       │
│  State → Valid Token Sets  │
└─────────────┬─────────────┘
              │
              ▼
┌────────────────────────────────────────┐
│  Constrained Decoding Loop              │
│                                         │
│  ┌─────────┐   ┌──────────┐   ┌─────┐ │
│  │FSM State│──▶│Valid Mask │──▶│Model│ │
│  │  s_i    │   │(mask out  │   │picks│ │
│  └─────────┘   │ invalid)  │   │token│ │
│       ▲        └──────────┘   └──┬──┘ │
│       │                          │     │
│       └──── advance state ◀──────┘     │
│                                         │
└────────────────────┬───────────────────┘
                     │  (FSM reaches accept state)
                     ▼
         ┌───────────────────────┐
         │  Guaranteed Valid      │
         │  Structured Output     │
         └───────────────────────┘
```

## Template

**Pydantic schema-based generation:**
```python
from pydantic import BaseModel
from outlines import models, generate

class Character(BaseModel):
    name: str
    age: int
    occupation: str
    traits: list[str]

model = models.transformers("mistralai/Mistral-7B-v0.1")
generator = generate.json(model, Character)

prompt = "Create a character for a mystery novel set in 1920s London."
result = generator(prompt)
# result is guaranteed to be a valid Character instance
```

**Regex-constrained generation:**
```python
from outlines import models, generate

model = models.transformers("mistralai/Mistral-7B-v0.1")

# Generate a valid email address
email_pattern = r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"
generator = generate.regex(model, email_pattern)

result = generator("The user's email address is: ")
# result is guaranteed to match the email regex
```

**Choice-based generation:**
```python
from outlines import models, generate

model = models.transformers("mistralai/Mistral-7B-v0.1")
generator = generate.choice(model, ["positive", "negative", "neutral"])

result = generator("The sentiment of 'I love this product!' is: ")
# result is guaranteed to be one of the three choices
```

## Examples

### Example 1: Structured Data Extraction

**Input:**
```python
from pydantic import BaseModel, Field
from outlines import models, generate
from typing import Optional

class InvoiceItem(BaseModel):
    description: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

class Invoice(BaseModel):
    vendor: str
    invoice_number: str
    date: str
    items: list[InvoiceItem]
    total: float
    currency: str

model = models.transformers("mistralai/Mistral-7B-Instruct-v0.2")
generator = generate.json(model, Invoice)

prompt = """Extract invoice data from the following text:

"Invoice #INV-2024-0892 from Acme Supplies, dated March 15, 2024.
Items: 50 units of Widget A at $12.99 each, 25 units of Widget B at
$24.50 each. Total: $1,262.00 USD."

JSON:"""

result = generator(prompt)
```

**Output:**
```json
{
    "vendor": "Acme Supplies",
    "invoice_number": "INV-2024-0892",
    "date": "March 15, 2024",
    "items": [
        {
            "description": "Widget A",
            "quantity": 50,
            "unit_price": 12.99
        },
        {
            "description": "Widget B",
            "quantity": 25,
            "unit_price": 24.50
        }
    ],
    "total": 1262.00,
    "currency": "USD"
}
```

### Example 2: Regex-Constrained Code Generation

**Input:**
```python
from outlines import models, generate

model = models.transformers("codellama/CodeLlama-7b-hf")

# Constrain to valid Python function signatures
func_pattern = r"def [a-z_][a-z0-9_]*\([a-z_: ,=0-9\"']*\) -> [a-z_\[\], ]+:"
generator = generate.regex(model, func_pattern)

prompt = "Write a Python function signature for calculating compound interest: "
result = generator(prompt)
```

**Output:**
```
def calculate_compound_interest(principal: float, rate: float, years: int, n: int = 12) -> float:
```

## When to Use

- Any application parsing LLM output as structured data (JSON, XML, CSV)
- API backends where response schemas must be guaranteed
- Data extraction pipelines processing documents into database records
- When downstream systems will crash or behave incorrectly on malformed output
- High-volume applications where even 1% format failure rate is unacceptable
- Type-safe applications that need Pydantic model instances, not raw strings

## When to Avoid

- Free-form text generation (essays, stories, conversations)
- When using API-only models that do not expose logit access
- Extremely complex schemas where FSM compilation is prohibitively slow
- Tasks where the "structure" is the content itself (e.g., poetry with specific forms)
- When the overhead of loading a local model is not justified for the task
- Simple tasks where the model reliably produces the correct format without constraints

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | Negative | No wasted tokens on invalid structure; often fewer total tokens |
| Latency | ~1.0-1.3x | FSM lookup per token adds small overhead; saved by no retries |
| Quality gain | 100% structural | Zero format errors by mathematical guarantee |
| Retry cost | Zero | Never need retries for formatting issues |
| FSM compilation | 1-30 seconds | One-time cost per schema; cached for reuse |
| Implementation | Low-Medium | Simple Python API; requires local model or compatible backend |

## Variants

- **JSON Mode:** Generate output conforming to a Pydantic model or JSON schema. Most common use case.
- **Regex Mode:** Generate output matching an arbitrary regular expression. Useful for specific formats (dates, emails, codes).
- **Choice Mode:** Force the model to pick from a finite set of options. Simplest constrained generation.
- **Grammar Mode:** Use a context-free grammar (CFG) for more expressive constraints than regex (e.g., balanced parentheses, nested structures).
- **Format Mode:** Generate output matching Python's string format syntax.
- **Multi-Step Outlines:** Chain multiple constrained generation calls, where each step has its own schema based on previous outputs.

## Composability

- **Outlines + Few-Shot:** Include examples in the prompt to guide semantic content; Outlines guarantees structural compliance.
- **Outlines + CoT:** Generate free-form reasoning first (unconstrained), then generate the structured answer (constrained by schema).
- **Outlines + RAG:** Retrieve relevant documents, include them in the prompt, and constrain the extraction output to a known schema.
- **Outlines + Batch Processing:** Process many documents in parallel, each with guaranteed schema-conformant output, enabling reliable batch ETL pipelines.
- **Outlines + Serving (vLLM):** Integrate with vLLM for high-throughput production serving with constrained decoding.

## Limitations

- Requires access to model logits (not available through most cloud APIs)
- FSM compilation can be slow for very complex schemas (deep nesting, many fields)
- Structural validity does not guarantee semantic correctness (the JSON is valid but may have wrong values)
- Large schemas with many optional fields can create very large FSMs
- Limited to local model inference or compatible serving frameworks (vLLM, TGI)
- The FSM approach may not capture all constraints expressible in JSON Schema (e.g., cross-field dependencies)
- Token vocabulary differences between models require separate FSM index builds
- Generation may feel "forced" for very narrow constraints, reducing output quality

## Sources

- **Code:** [Outlines GitHub Repository](https://github.com/dottxt-ai/outlines) — .txt (dottxt-ai), open-source
- **Related:** [Efficient Guided Generation for Large Language Models](https://arxiv.org/abs/2307.09702) — Willard & Louf, 2023
- **Related:** [LMQL: Prompting Is Programming](https://arxiv.org/abs/2212.06094) — Alternative constrained generation approach
- **Integration:** [vLLM Structured Output](https://docs.vllm.ai/) — Production serving with Outlines integration
