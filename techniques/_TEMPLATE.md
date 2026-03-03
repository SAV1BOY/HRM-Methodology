---
id: technique-id
name: "Full Technique Name"
aliases: ["alias1", "alias2"]
category: category-name
family: functional-family
year: YYYY
authors: ["Author 1", "Author 2"]
paper: "https://arxiv.org/abs/XXXX.XXXXX"
paper_title: "Paper Title"
venue: "Conference/Journal Year"
code: null

complexity: low  # low | medium | high
token_cost: low  # low | medium | high | variable
latency: low     # low | medium | high
num_calls: 1     # integer or "variable"

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["use case 1", "use case 2"]
avoid_when: ["anti-pattern 1", "anti-pattern 2"]
composes_with: ["technique-id-1", "technique-id-2"]

tags: ["tag1", "tag2"]
---

# Full Technique Name

> **One-line summary:** A single sentence capturing what this technique does and why.

## Overview

Two to three paragraphs explaining:
- What the technique is
- Why it was developed (what problem it solves)
- Key insight from the original paper

## How It Works

1. **Step 1 name:** Description
2. **Step 2 name:** Description
3. **Step 3 name:** Description

### Diagram

```
ASCII diagram showing the flow
```

## Template

```
Ready-to-use prompt template with {placeholders}
```

## Examples

### Example 1: {Domain}

**Input:**
```
The actual prompt
```

**Output:**
```
Expected model output
```

### Example 2: {Domain}

**Input:**
```
The actual prompt
```

**Output:**
```
Expected model output
```

## When to Use

- Scenario 1
- Scenario 2

## When to Avoid

- Anti-pattern 1
- Anti-pattern 2

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | X | ... |
| Latency | X | ... |
| Quality gain | X | ... |

## Variants

- **Variant Name:** Description

## Composability

- **This + Technique:** What you get when combining

## Limitations

- Limitation 1
- Limitation 2

## Sources

- **Primary:** [Paper Title](url) — Authors, Year
- **Secondary:** [Resource](url) — Description
