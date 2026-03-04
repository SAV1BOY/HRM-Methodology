# Squad HRM Orchestration Guide

Quick-start operational reference for any HRM agent instance. Read this to understand how to operate the Squad HRM system end-to-end.

---

## Quick Start: 3-Step Bootstrap

```
Step 1: Read config.yaml          → Understand system structure and thresholds
Step 2: Read registry/asset-registry.yaml → Know what assets are available
Step 3: Execute Step 0 (Triage)   → Classify task and determine hrm_mode
```

After Step 3, load additional subsystems based on the mode (see Mode-Specific Loading below).

---

## Decision Tree

```
User Request Arrives
       |
       v
  STEP 0: TRIAGE
  Classify: TYPE / DOMAIN / COMPLEXITY / ARTIFACT
  Calculate: complexity_score (0-10)
       |
       +-- score < 3.0 ──────> MODE: TRIAGE
       |                         Load: config.yaml + asset-registry.yaml
       |                         Execute: Step 0 only
       |                         Output: classification + skills_recomendadas
       |                         Supervisor: OFF
       |
       +-- score 3.0-4.9 ────> MODE: FULL_LIGHT
       |                         Load: + skills.yaml, agents.yaml, technique-mapper.md, gate-definitions.yaml
       |                         Execute: Steps 0, 0.7, 1-5, 9
       |                         Output: simplified ExecutionPlan
       |                         Supervisor: depends on uncertainty
       |
       +-- score >= 5.0 ─────> MODE: FULL
                                Load: ALL subsystems
                                Execute: Steps 0, 0.7, 1-12
                                Output: full ExecutionPlan with prompts, quality gates
                                Supervisor: ON (Supreme Squad Chief)
```

---

## Mode-Specific Operation

### TRIAGE Mode (complexity_score < 3.0)

**Files to load:**
| File | Purpose |
|------|---------|
| `config.yaml` | System structure, thresholds |
| `registry/asset-registry.yaml` | Quick lookup of available assets |

**Steps to execute:** Step 0 only

**Prompt Forge tier:** MICRO (1-2 techniques from technique-index.yaml)

**Templates to use:** agent-handoff with MICRO-forged technique steps

**Quality gates:** None (direct execution)

**What to produce:**
1. HRM TRIAGE output (classification + skills_recomendadas)
2. SET in compact mode
3. Return control to skill-router

---

### FULL_LIGHT Mode (complexity_score 3.0-4.9)

**Files to load:**
| File | Purpose |
|------|---------|
| `config.yaml` | System structure, thresholds |
| `registry/asset-registry.yaml` | Asset index |
| `registry/skills.yaml` | Skills matching by domain/phase |
| `registry/agents.yaml` | Agent options by archetype |
| `prompt-gen/technique-mapper.md` | Quick-path technique pipelines |
| `quality-gates/gate-definitions.yaml` | Threshold definitions |

**Steps to execute:** 0, 0.7, 1, 2, 3, 4, 5, 9

**Prompt Forge tier:** QUICK (3-5 techniques from technique-mapper.md)

**Templates to use:** `agent-handoff.yaml` with QUICK-forged technique pipelines

**Quality gates:** Up to Level 3 (global)

**What to produce:**
1. Bloom analysis (Step 1)
2. Complexity assessment (Step 2)
3. Decomposability check (Step 3)
4. Methodology selection (Step 4)
5. Budget allocation (Step 5)
6. Simplified ExecutionPlan (Step 9)
7. SET with phases 0-3

---

### FULL Mode (complexity_score >= 5.0)

**Files to load:**
| File | Purpose |
|------|---------|
| `config.yaml` | System structure, thresholds |
| `registry/asset-registry.yaml` | Asset index |
| `registry/skills.yaml` | Skills matching |
| `registry/agents.yaml` | Agent options |
| `registry/squads.yaml` | Squad delegation targets |
| `registry/mcps.yaml` | MCP integrations |
| `registry/frameworks.yaml` | Framework selection |
| `prompt-gen/prompt-generator.md` | Full prompt generation algorithm |
| `prompt-gen/technique-mapper.md` | Technique pipeline defaults |
| `quality-gates/gate-definitions.yaml` | Thresholds |
| `quality-gates/scoring-rubrics.yaml` | Bloom scoring rubrics |
| `quality-gates/gate-runner.md` | Gate execution protocol |
| `execution/flow-engine.md` | Execution lifecycle |
| `execution/delegation-protocols.md` | Mode selection |
| `execution/squad-delegation.md` | Squad delegation flow |
| `checklists/hrm-self-check.md` | Self-verification |

**Steps to execute:** 0, 0.7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9.5, 10, 11, 12

**Prompt Forge tier:** FULL (3-7 techniques via technique-selector + pipeline-builder)
  - Top-level workstreams: FULL tier
  - Subtask agents (swarm/team members): QUICK tier
  - Mini-tasks, feedback, escalation: MICRO tier

**Templates to use:**
- `agent-handoff.yaml` for individual agent workstreams
- `squad-brief.yaml` for squad delegations
- `swarm-dispatch.yaml` for swarm coordination
- `team-kickoff.yaml` for agent teams
- `quality-gate-review.yaml` for verification prompts
- `feedback-loop.yaml` for revision cycles
- `escalation-report.yaml` for user escalation

**Quality gates:** All 4 levels (syntax, local, global, semantic)

**What to produce:**
1. Complete analysis (Steps 1-8)
2. Full ExecutionPlan with prompt_generation_spec, squad_delegations, mcp_integrations (Step 9)
3. Instantiated prompts per workstream (Step 9.5)
4. SET with all phases
5. Convergence monitoring during execution (Step 10)
6. Verification cascade results (Step 11)
7. Backtracking decisions if needed (Step 12)

---

## Reference Table: "If you need X, read Y"

| Need | File | When |
|------|------|------|
| System config and thresholds | `config.yaml` | Always (bootstrap) |
| Available skills by domain | `registry/skills.yaml` | FULL_LIGHT+ |
| Agent options by archetype | `registry/agents.yaml` | FULL_LIGHT+ |
| Squad delegation targets | `registry/squads.yaml` | FULL only |
| MCP tool integrations | `registry/mcps.yaml` | FULL only |
| Framework recommendations | `registry/frameworks.yaml` | FULL only |
| Playbook for specific domain | `playbooks/*.md` | When domain matches |
| Technique pipeline defaults | `prompt-gen/technique-mapper.md` | FULL_LIGHT+ |
| Full prompt generation algo | `prompt-gen/prompt-generator.md` | FULL only |
| Prompt Forge algorithm | `prompt-gen/prompt-forge.md` | Step 9.5 (all modes) |
| Compact technique index | `prompt-gen/technique-index.yaml` | TRIAGE+ (bootstrap) |
| Dispatch type profiles | `prompt-gen/dispatch-profiles.yaml` | TRIAGE+ (bootstrap) |
| Prompt YAML templates | `prompt-gen/prompt-templates/*.yaml` | Step 9.5 |
| Quality gate thresholds | `quality-gates/gate-definitions.yaml` | FULL_LIGHT+ |
| Bloom scoring rubrics | `quality-gates/scoring-rubrics.yaml` | FULL only |
| How to run quality gates | `quality-gates/gate-runner.md` | FULL only |
| Execution state machine | `execution/flow-engine.md` | FULL only |
| Delegation mode flowchart | `execution/delegation-protocols.md` | FULL only |
| Squad delegation protocol | `execution/squad-delegation.md` | When squad detected |
| Self-verification checklist | `checklists/hrm-self-check.md` | Before completing |
| Prompt quality checklist | `checklists/prompt-quality.md` | Step 9.5 validation |
| Technique deep-dive | `techniques/<category>/<technique>.md` | When technique-selector needs detail |
| End-to-end flow examples | `examples/*.md` | Learning / debugging |

---

## Execution Lifecycle

```
PHASE 0: STARTUP
  hrm-architect (Step 0: Triage) ──parallel──> using-superpowers (Discovery)
  hrm-architect (Step 0.7: Registry Lookup)
       |
       v
PHASE 1: ANALYSIS (FULL_LIGHT / FULL only)
  Steps 1-8: Bloom → Complexity → Decomposability → Methodology → Budget → Decomposition → Hyperparams → Mode
       |
       v
PHASE 2: PLANNING
  Step 9: Generate ExecutionPlan v1
  Step 9.5: Universal Prompt Forge (ALL modes — MICRO/QUICK/FULL per dispatch point)
  Present to user → await confirmation
       |
       v
PHASE 3: EXECUTION
  Delegate to: agent-router / swarm-orchestrator / agent-teams-protocol / squad chiefs
  Step 10: Convergence monitoring (FULL only, supervisor stays active)
       |
       v
PHASE 4: VERIFICATION
  Step 11: Verification cascade (syntax → local → global → semantic)
  If passed → deliver result
  If failed → Step 12: Backtracking
       |
       v
PHASE 5: DELIVERY or BACKTRACKING
  Step 12: Root-cause analysis → credit assignment → targeted re-execution
  Plan evolves: v1 → v2 → vN
  Max 3 loops before user escalation
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Skipping Step 0 | No classification = wrong mode | Always triage first |
| Loading ALL files in TRIAGE mode | Wastes context window | Load only config + asset-registry |
| Generating ExecutionPlan in TRIAGE | Overkill for simple tasks | Return classification + skills only |
| Accepting first result without verification | Quality may be below threshold | Always run verification cascade |
| Re-executing without root-cause analysis | Repeats same error | Step 12A first, then targeted fix |
| Using Agent Teams for 2-file tasks | 5x cost for no benefit | Use single agent or parallel |
| Ignoring squad delegation when detected | Missing specialized expertise | Delegate per squad-delegation.md |
| Generating prompts without technique-mapper | Generic prompts, low quality | Always consult technique-mapper |
| Skipping self-check before delivery | May miss systematic errors | Run checklists/hrm-self-check.md |
| Not evolving the plan on quality failure | Stuck in loops | Refine plan v1→v2 with feedback |

---

## Glossary

| Term | Meaning |
|------|---------|
| **HRM** | Hierarchical Reasoning Model - the core analytical framework |
| **SET** | Skill Execution Timeline - ordered list of skills to invoke |
| **Bloom Level** | Cognitive complexity (1=Remember, 6=Create) |
| **Archetype** | Agent role pattern (L-Architect, L-Builder-Frontend, etc.) |
| **Workstream** | Independent unit of work within a decomposition |
| **Quality Gate** | Verification checkpoint (4 levels: syntax, local, global, semantic) |
| **Squad Delegation** | Sending a workstream to a specialized squad chief |
| **Plan Evolution** | Refining ExecutionPlan based on execution feedback (v1→v2→vN) |
| **Credit Assignment** | Identifying which agent/workstream caused a quality failure |
| **Convergence** | Progress toward meeting quality thresholds |
