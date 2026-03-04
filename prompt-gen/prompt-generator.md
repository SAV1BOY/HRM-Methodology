# Prompt Generator

> Core algorithm for generating tailored prompts for each agent, squad chief, and reviewer in the ExecutionPlan. Takes the output of Step 9 and produces ready-to-use prompts per workstream.

---

## Overview

The Prompt Generator bridges the gap between the HRM's strategic ExecutionPlan and the tactical prompts each agent needs to execute. It applies prompt engineering techniques from the Squad HRM knowledge base to maximize agent performance.

---

## 5-Phase Pipeline

```
ExecutionPlan (Step 9)
    |
    v
Phase 1: EXTRACT PROFILES
    |  Map each workstream to a task_profile (technique-selector input)
    v
Phase 2: SELECT TECHNIQUES
    |  Run technique-selector.md 4-phase scoring for each workstream
    v
Phase 3: BUILD PIPELINE
    |  Run pipeline-builder.md to chain techniques into executable pipeline
    v
Phase 4: ENRICH CONTEXT
    |  Add project context, scope, contracts, budget, hyperparameters
    v
Phase 5: VALIDATE
    |  Check against checklists/prompt-quality.md
    |
    v
Output: {agent_prompt, chief_prompt, verification_prompt} per workstream
```

---

## Phase 1: Extract Profiles

For each workstream in the ExecutionPlan, create a task_profile compatible with `hrm-agent/technique-selector.md`:

```yaml
task_profile:
  raw_input: "<workstream objective from level_1>"
  primary_type: "<mapped from workstream archetype>"
  domain: "<from ExecutionPlan domain_config>"
  complexity: "<from workstream estimated_effort>"
  constraints:
    max_tokens: "<budget-derived>"
    max_calls: "<from workstream predicted_cost>"
    latency: "<from execution_mode>"
  quality_requirements:
    accuracy: "<from verification_threshold>"
    format: "<from deliverables spec>"
  context_available:
    examples: "<from reference materials>"
    tools: "<from agent tools_available>"
```

### Archetype -> Primary Type Mapping

| Archetype | primary_type |
|-----------|-------------|
| L-Architect | reasoning, creative |
| L-Builder-Frontend | code, creative |
| L-Builder-Backend | code |
| L-Builder-Test | code, verification |
| L-Builder-Infra | code |
| L-Critic | verification, evaluation |
| L-Researcher | research, extraction |
| L-Builder-Data | code, extraction |
| L-Optimizer | code, analysis |

---

## Phase 2: Select Techniques

For each task_profile, run the 4-phase technique selection from `hrm-agent/technique-selector.md`:

1. **Analyze**: Classify task profile
2. **Filter**: Remove techniques violating constraints (budget, latency, tools)
3. **Score**: Rank by fit (relevance, cost, compatibility)
4. **Compose**: Select compatible set and order

Output: ordered list of techniques per workstream.

### Quick-Path (technique-mapper.md)

For common archetypes, use pre-computed defaults from `technique-mapper.md` instead of full 4-phase scoring. Fall back to full scoring only if:
- Archetype is unusual or hybrid
- Constraints are non-standard
- Domain has special requirements

---

## Phase 3: Build Pipeline

For each technique set, run `hrm-agent/pipeline-builder.md`:

1. **Resolve dependencies** between techniques
2. **Load templates** from `templates/` directory
3. **Bind variables** (connect outputs to inputs across steps)
4. **Configure error handling** (retry, fallback)

Output: executable pipeline spec per workstream.

---

## Phase 4: Enrich Context

Inject concrete context into each prompt:

### For Agent Prompts (agent-handoff template)

```yaml
context_enrichment:
  project:
    tech_stack: "<from project analysis>"
    existing_patterns: "<from codebase scan>"
    constraints: "<from level_0>"
  scope:
    file_ownership: "<from workstream spec>"
    deliverables: "<from workstream spec>"
    dependencies: "<from interface_contracts>"
  contracts:
    inputs_from: "<what this workstream receives>"
    outputs_to: "<what this workstream produces>"
    format: "<contract format>"
  budget:
    tool_calls: "<allocated for this workstream>"
    time_estimate: "<if applicable>"
  hyperparameters:
    verification_threshold: "<domain-specific>"
    max_cycles: "<from domain config>"
  backtracking_triggers:
    - "<when to report problems>"
```

### For Chief Prompts (squad-brief template)

Add delegation-specific context:
- Full workstream decomposition
- Agent assignments per sub-task
- Internal quality gates
- Reporting protocol to HRM

### For Verification Prompts (quality-gate-review template)

Add verification-specific context:
- Success criteria to check
- Bloom-level rubric
- Specific checks to run
- Expected evidence format

---

## Phase 5: Validate

Before delivering prompts, validate against `checklists/prompt-quality.md`:

### Validation Checks

1. **Completeness**: Does the prompt include all 7 required handoff fields?
   - Context, scope, contracts, quality criteria, backtracking triggers, hyperparameters, budget
2. **Clarity**: Is the objective unambiguous?
3. **Constraint Coverage**: Are all constraints from the ExecutionPlan reflected?
4. **Technique Appropriateness**: Do selected techniques match the task profile?
5. **Budget Alignment**: Does estimated technique cost fit within allocated budget?
6. **No Conflicting Instructions**: No contradictions within the prompt

### If Validation Fails

- Identify which check failed
- Adjust prompt (add missing context, resolve conflicts, swap technique)
- Re-validate
- If still failing after 2 attempts, flag to HRM with details

---

## Output Specification

For each workstream, produce:

```yaml
prompt_output:
  workstream: "<name>"
  agent_prompt:
    role: "<from technique pipeline>"
    objective: "<clear, measurable>"
    context: "<enriched project context>"
    technique_pipeline: "<ordered techniques>"
    deliverables: "<expected outputs>"
    constraints: "<budget, quality, format>"
    verification: "<how success is measured>"
  chief_prompt:  # only for squad delegation mode
    brief: "<squad brief>"
    delegation_spec: "<internal architecture>"
    quality_gates: "<internal gates>"
    reporting: "<how/when to report to HRM>"
  verification_prompt:
    rubric: "<Bloom-level rubric>"
    checks: "<specific checks to run>"
    threshold: "<domain threshold>"
    evidence_format: "<what evidence to collect>"
```

---

## Integration Points

| Component | How Prompt Generator Uses It |
|-----------|----------------------------|
| `technique-selector.md` | Phase 2: technique selection algorithm |
| `pipeline-builder.md` | Phase 3: pipeline construction |
| `technique-mapper.md` | Phase 2 quick-path for common archetypes |
| `templates/` | Phase 3: prompt template loading |
| `checklists/prompt-quality.md` | Phase 5: validation |
| `registry/skills.yaml` | Phase 1: skill capability lookup |
| `registry/agents.yaml` | Phase 1: agent tool/capability lookup |
| `config.yaml` | Phase 4: domain thresholds and hyperparameters |

---

## Relationship with Universal Prompt Forge

The Prompt Generator is the **FULL tier** engine within the Universal Prompt Forge system (`prompt-gen/prompt-forge.md`).

### How They Relate

```
Universal Prompt Forge (prompt-forge.md)
  |
  +-- MICRO tier: technique-index.yaml lookup (zero cost)
  |
  +-- QUICK tier: technique-mapper.md pre-computed pipelines
  |
  +-- FULL tier: THIS file (prompt-generator.md)
         Phase 1: Extract profiles
         Phase 2: Select techniques (technique-selector.md)
         Phase 3: Build pipeline (pipeline-builder.md)
         Phase 4: Enrich context
         Phase 5: Validate
```

### Key Points

- The Forge calls this Prompt Generator **only** for FULL tier (top-level workstream agents in FULL mode)
- MICRO and QUICK tiers bypass this pipeline entirely, using cheaper alternatives
- The 5-Phase Pipeline documented above is unchanged — the Forge simply wraps it as one of three tier options
- For backward compatibility, calling this pipeline directly (outside the Forge) produces identical results
