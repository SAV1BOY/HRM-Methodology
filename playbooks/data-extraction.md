# Playbook: Data Extraction

> **Pipeline:** Output Format Control → Few-Shot Prompting → Chain-of-Verification → Checklist Prompting
>
> **Best for:** Entity extraction, document parsing, log analysis, resume parsing, invoice processing, survey coding, structured data from unstructured text.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │  Unstructured Input  │
                    │  (text, doc, log)    │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. Output Format    │  Define the exact schema
                    │     Control         │  for extracted data
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Few-Shot         │  Provide annotated examples
                    │     Prompting       │  to calibrate extraction
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Chain-of-        │  Verify extracted fields
                    │     Verification    │  against source text
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Checklist        │  Final completeness
                    │     Prompting       │  and accuracy check
                    └─────────┴───────────┘
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | Output Format Control | Extraction tasks require a precise target schema — defining the output format first ensures the model knows exactly what fields to extract and in what structure |
| 2 | Few-Shot Prompting | Extraction accuracy improves dramatically with annotated examples showing source text to structured output mappings, especially for ambiguous or domain-specific fields |
| 3 | Chain-of-Verification | Extracted data is prone to hallucinated fields, misattributed values, and missed entities; CoVe systematically verifies each extracted field against the source |
| 4 | Checklist Prompting | A final pass ensures completeness — all required fields present, correct types, no duplicates, no cross-contamination between records |

## Step-by-Step Templates

### Step 1: Output Format Control

**Purpose:** Define the exact schema the model should extract data into, including field types, constraints, and handling of missing values.

```
You will extract structured data from unstructured text. Below is the
exact schema you must produce.

OUTPUT SCHEMA:
```json
{
  "{field_1}": "{type} — {description}",
  "{field_2}": "{type} — {description}",
  "{field_3}": "{type} — {description}",
  "{nested_object}": {
    "{sub_field_1}": "{type} — {description}",
    "{sub_field_2}": "{type} — {description}"
  },
  "{array_field}": ["list of {type} — {description}"]
}
```

RULES:
- If a field is not present in the source text, set it to null
- If a field is ambiguous, extract the most likely value and add a
  "confidence" field (high/medium/low)
- Dates should be normalized to ISO 8601 format (YYYY-MM-DD)
- Names should be normalized to "FirstName LastName" format
- Currency values should include the currency code (e.g., "USD 150.00")
- Do NOT infer or hallucinate values not present in the source text

SOURCE TEXT:
{input_text}
```

### Step 2: Few-Shot Prompting

**Purpose:** Provide annotated examples that demonstrate the extraction mapping for the specific domain.

```
Extract structured data from the text below following the schema and
examples provided.

SCHEMA:
{schema_definition}

EXAMPLE 1:
Source: "{example_source_1}"
Extracted:
```json
{example_output_1}
```

EXAMPLE 2:
Source: "{example_source_2}"
Extracted:
```json
{example_output_2}
```

EXAMPLE 3 (edge case — missing fields):
Source: "{example_source_3}"
Extracted:
```json
{example_output_3_with_nulls}
```

NOW EXTRACT FROM:
Source: "{actual_input}"
Extracted:
```

### Step 3: Chain-of-Verification

**Purpose:** Systematically verify each extracted field against the original source text.

```
Verify the following extracted data against the original source text.
For each field, confirm it is accurate, correct it if wrong, or flag
it if unverifiable.

ORIGINAL SOURCE TEXT:
{input_text}

EXTRACTED DATA:
{few_shot_output}

VERIFICATION PROCESS:

Step 1 — For each extracted field, generate a verification question:
  - "{field_1}": "Does the source text state that {field_1} is {value}?"
  - "{field_2}": "Does the source text contain {value} for {field_2}?"
  [Continue for all fields]

Step 2 — Answer each verification question by re-reading ONLY the
source text (ignore the extracted data):
  - "{field_1}": [CONFIRMED | CORRECTED: new_value | NOT FOUND]
  - "{field_2}": [CONFIRMED | CORRECTED: new_value | NOT FOUND]

Step 3 — Check for MISSED entities:
  - Re-read the source text. Are there any values that should have
    been extracted but were not?
  - List any additional fields found.

Step 4 — Produce the corrected extraction:
```json
{corrected_output}
```

Flag each field with its verification status:
  - CONFIRMED: verified against source
  - CORRECTED: original extraction was wrong
  - INFERRED: not explicit in source but reasonably deduced
  - MISSING: required field not found in source
```

### Step 4: Checklist Prompting

**Purpose:** Final quality gate ensuring extraction completeness and data integrity.

```
Perform a final quality check on the following extracted data.
Mark each checkpoint as PASS or FAIL.

EXTRACTED DATA:
{cove_output}

ORIGINAL SOURCE:
{input_text}

## Extraction Quality Checklist

### Completeness
- [ ] All required fields in the schema are present
- [ ] Array fields contain all matching entities (not just the first one)
- [ ] Nested objects are fully populated
- [ ] No records from the source were skipped

### Accuracy
- [ ] Every extracted value appears in or is directly supported by the source
- [ ] No hallucinated values (values not in the source)
- [ ] Ambiguous values are flagged with confidence levels
- [ ] Named entities are spelled exactly as in the source

### Format Compliance
- [ ] All dates are in ISO 8601 format
- [ ] All currency values include currency code
- [ ] All names follow the specified format
- [ ] JSON is valid and parseable
- [ ] Enum fields only contain allowed values

### Edge Cases
- [ ] Missing values are null, not empty strings
- [ ] Duplicate entities in the source are handled correctly
- [ ] Multi-language content is handled appropriately
- [ ] Special characters are properly escaped in JSON

### Data Integrity
- [ ] No cross-contamination between records (values from one record
      appearing in another)
- [ ] Referential integrity maintained (IDs reference valid entities)
- [ ] Numerical values are within reasonable ranges

If any items FAIL, produce a corrected final version.
```

## Walk-Through Example

**Task:** "Extract all job postings from a webpage dump containing mixed content — articles, ads, and job listings — into a structured JSON format."

---

### Step 1 Output: Schema Definition

> **Schema defined:**
> ```json
> {
>   "job_title": "string — the position title",
>   "company": "string — employer name",
>   "location": "string — city, state/country",
>   "remote": "boolean — whether remote work is offered",
>   "salary_range": {
>     "min": "number — minimum salary",
>     "max": "number — maximum salary",
>     "currency": "string — ISO 4217 currency code",
>     "period": "string — annual|monthly|hourly"
>   },
>   "requirements": ["list of string — required qualifications"],
>   "posted_date": "string — ISO 8601 date",
>   "apply_url": "string — application link or null"
> }
> ```

### Step 2 Output: Few-Shot Extraction

> **Three annotated examples provided** showing:
> 1. A complete job posting with all fields present
> 2. A posting missing salary information (null values)
> 3. A posting embedded in article text (extraction from noisy context)
>
> **Extraction result:** 7 job postings identified and extracted from the mixed content.

### Step 3 Output: Chain-of-Verification

> **Verification results:**
> - Job 1: All fields CONFIRMED
> - Job 2: "location" CORRECTED — extracted "New York" but source says "New York, NY (hybrid)"
> - Job 3: "salary_range.min" CORRECTED — swapped min and max values
> - Job 4: All fields CONFIRMED
> - Job 5: "posted_date" INFERRED — source says "last week," converted to approximate ISO date
> - MISSED: Job 8 found in source — was embedded in a testimonial paragraph
>
> **Corrected extraction with 8 records produced.**

### Step 4 Output: Checklist Verification

> - [PASS] All schema fields present in all 8 records
> - [PASS] No hallucinated values
> - [FAIL] Job 5 posted_date is approximate — flagged with confidence: low
> - [PASS] All dates in ISO 8601
> - [PASS] JSON is valid
> - [PASS] No cross-contamination between records
> - [PASS] Special characters escaped
>
> **Final output: 8 verified job postings in clean JSON.**

## Decision Points

```
                          ┌──────────────────┐
                          │ Extraction task   │
                          └──────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Do you have a predefined │
                    │ schema?                  │
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   Use schema        Ask LLM to propose
                   directly          schema first, then confirm
                         │
                    ┌────▼───────────────────┐
                    │ Do you have annotated   │
                    │ examples?               │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                   Few-Shot          Zero-Shot with
                   (2-5 examples)    detailed schema only
                         │
                    ┌────▼───────────────────┐
                    │ Is high accuracy        │
                    │ critical?               │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                   CoVe + Checklist  Checklist only
                   (full pipeline)   (lightweight)
```

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **High throughput** | Skip CoVe; use Checklist only for spot-checking a sample |
| **Maximum accuracy** | Add Self-Consistency at step 2 (run extraction 3 times, take consensus per field) |
| **No examples available** | Skip Few-Shot; use detailed schema with field descriptions and constraints |
| **Multi-document** | Add Context Stuffing to batch multiple documents per call |
| **Evolving schema** | Add Self-Refine after step 1 to iteratively improve schema based on sample data |
| **Nested/hierarchical** | Use Least-to-Most to extract top-level entities first, then nested details |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| Output Format | 1 | ~300 output | Low |
| Few-Shot | 1 | ~1500 output | Medium |
| CoVe | 2-3 | ~2000 output | Medium |
| Checklist | 1 | ~800 output | Low |
| **Total** | **5-6** | **~4600 tokens** | **~20-40s** |
