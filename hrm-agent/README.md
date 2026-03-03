# HRM Agent

> The HRM Agent is an AI orchestrator that uses the HRM Methodology knowledge base to automatically select, chain, and apply prompt engineering techniques for complex tasks.

---

## What It Is

The HRM Agent is a meta-layer that sits on top of any LLM and uses the 75-technique catalog in this repository to:

1. **Analyze** a user's task to determine its type, constraints, and quality requirements
2. **Select** the optimal set of prompt engineering techniques from the catalog
3. **Chain** those techniques into an executable pipeline
4. **Execute** the pipeline, passing output from each technique as input to the next
5. **Reflect** on the results and improve for future tasks

Instead of relying on a single monolithic prompt, the HRM Agent decomposes tasks into technique-enhanced steps — each step using the best-known method for that type of work.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        HRM AGENT                                │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Task        │    │  Technique   │    │  Pipeline    │      │
│  │   Analyzer    │───►│  Selector    │───►│  Builder     │      │
│  │              │    │              │    │              │      │
│  │ - Classify    │    │ - Score      │    │ - Chain      │      │
│  │ - Decompose   │    │ - Filter     │    │ - Template   │      │
│  │ - Constrain   │    │ - Rank       │    │ - Validate   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │              │
│         │            ┌──────▼──────┐             │              │
│         │            │  Knowledge  │             │              │
│         │            │  Base       │             │              │
│         │            │             │             │              │
│         │            │ taxonomy.yaml│             │              │
│         │            │ techniques/ │             │              │
│         │            │ templates/  │             │              │
│         │            │ playbooks/  │             │              │
│         │            └─────────────┘             │              │
│         │                                        │              │
│  ┌──────▼────────────────────────────────────────▼──────┐      │
│  │                Pipeline Executor                      │      │
│  │                                                       │      │
│  │  Step 1          Step 2          Step 3       Step N  │      │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐  ┌─────┐ │      │
│  │  │Technique│───►│Technique│───►│Technique│─►│ ... │ │      │
│  │  │  A      │    │  B      │    │  C      │  │     │ │      │
│  │  └─────────┘    └─────────┘    └─────────┘  └─────┘ │      │
│  │       │              │              │                 │      │
│  │       ▼              ▼              ▼                 │      │
│  │   [output_a]    [output_b]    [output_c]     [final] │      │
│  └───────────────────────────────────────────────────────┘      │
│                              │                                   │
│                     ┌────────▼────────┐                         │
│                     │   Reflector     │                         │
│                     │                 │                         │
│                     │ - Evaluate      │                         │
│                     │ - Learn         │                         │
│                     │ - Store         │                         │
│                     └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Task Analyzer
Examines the user's request and produces a structured task profile:
- **Task type:** reasoning, code, creative, extraction, agent, RAG, etc.
- **Complexity:** simple, moderate, complex
- **Constraints:** latency budget, token budget, quality level
- **Available tools:** code interpreter, search, databases, etc.

See: [technique-selector.md](technique-selector.md) for the analysis algorithm.

### 2. Technique Selector
Uses the task profile to score and rank candidate techniques from `taxonomy.yaml`:
- Matches task type to `best_for` fields
- Filters by constraints (latency, cost, complexity)
- Checks `composes_with` metadata for compatibility
- Returns an ordered list of recommended techniques

See: [technique-selector.md](technique-selector.md) for the scoring algorithm.

### 3. Pipeline Builder
Chains selected techniques into an executable pipeline:
- Resolves dependencies between techniques
- Instantiates prompt templates from `templates/`
- Validates that outputs from step N can feed step N+1
- Estimates total cost and latency

See: [pipeline-builder.md](pipeline-builder.md) for the construction algorithm.

### 4. Pipeline Executor
Runs the pipeline step by step:
- For each step: fill template with inputs, call LLM, capture output
- Passes output from step N as input to step N+1
- Handles errors and retries
- Tracks token usage and latency

### 5. Reflector
After pipeline completion, evaluates the result:
- Did the output meet the quality requirements?
- Was the technique selection optimal?
- What should be stored in memory for future tasks?
- Implements the Reflexion pattern for continuous improvement

---

## How It Uses This Repository

```
1. Agent receives task
        │
2. Load taxonomy.yaml ──────► Get all 75 techniques with metadata
        │
3. Score techniques ─────────► Use best_for, avoid_when, complexity,
        │                       token_cost fields
4. Check playbooks/ ─────────► Does a pre-built pipeline match?
        │
5. Load technique docs ──────► Get detailed instructions from
        │                       techniques/{category}/{id}.md
6. Load templates ───────────► Get prompt skeletons from
        │                       templates/{category}/{id}.yaml
7. Build pipeline
        │
8. Execute pipeline
        │
9. Evaluate with checklists/ ► Run quality checks from
        │                       checklists/prompt-quality.md
10. Reflect and store
```

---

## Example Sessions

Detailed worked examples showing actual prompts and outputs:

- [Research Example](examples/example-research.md) — "Research transformer architecture innovations"
- [Coding Example](examples/example-coding.md) — "Build rate-limiting middleware"
- [Analysis Example](examples/example-analysis.md) — "Analyze customer support tickets"

---

## Key Design Principles

1. **Minimum effective technique.** Always start with the simplest technique that might work. Add complexity only when measurement shows it's needed.

2. **Composability over monoliths.** Multiple focused techniques chained together outperform single mega-prompts.

3. **Machine-readable metadata.** Every technique has YAML metadata enabling programmatic selection and composition.

4. **Playbook reuse.** Common patterns are captured as playbooks — the agent checks for a matching playbook before building a custom pipeline.

5. **Continuous learning.** The Reflector component enables the agent to improve its technique selection over time through Reflexion.
