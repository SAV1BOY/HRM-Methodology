# Contributing to HRM Methodology

## How to Add a New Technique

1. **Copy the template:** `cp techniques/_TEMPLATE.md techniques/<category>/<technique-id>.md`
2. **Place in the correct category folder** (see table below)
3. **Fill in ALL sections** — the HRM agent relies on complete metadata
4. **Add a YAML template** in `templates/<category>/<technique-id>.yaml`
5. **Update `taxonomy.yaml`** — add the technique entry under its category
6. **Update `glossary.md`** — add any new aliases

## Required YAML Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique kebab-case identifier |
| `name` | string | Full human-readable name |
| `aliases` | list | Alternative names for glossary lookup |
| `category` | string | Category folder name |
| `family` | string | Functional family (thought-generation, decomposition, etc.) |
| `year` | int | Year of publication |
| `authors` | list | Primary authors |
| `paper` | string | ArXiv or DOI URL |
| `complexity` | enum | low, medium, high |
| `token_cost` | enum | low, medium, high, variable |
| `num_calls` | string | Number of LLM calls required |
| `best_for` | list | Ideal use cases |
| `avoid_when` | list | Anti-patterns |
| `composes_with` | list | Technique IDs that compose well |

## Category Reference

| Code | Category | Folder |
|------|----------|--------|
| A | Foundations | `techniques/foundations/` |
| B | Reasoning | `techniques/reasoning/` |
| C | Advanced Reasoning | `techniques/advanced-reasoning/` |
| D | Verification & Grounding | `techniques/verification/` |
| E | Perception & Context | `techniques/perception/` |
| F | Agents & Tool Use | `techniques/agents/` |
| G | Prompt Programming | `techniques/prompt-programming/` |
| H | Optimization | `techniques/optimization/` |
| I | Soft Prompts | `techniques/soft-prompts/` |
| J | Security & Defense | `techniques/security/` |
| K | Alignment | `techniques/alignment/` |
| L | Reasoning Tokens | `techniques/reasoning-tokens/` |
| M | Multimodal | `techniques/multimodal/` |
