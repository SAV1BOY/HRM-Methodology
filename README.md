# Squad HRM — Universal Orchestration System

> **The HRM (Hierarchical Reasoning Model) as a full Squad**: knowledge base of 75 prompt engineering techniques + 6 orchestration subsystems that transform task classification into end-to-end execution with prompt generation, quality gates, squad delegation, and convergence monitoring.

## Architecture

```
Squad HRM/
├── config.yaml                  # Squad configuration
├── taxonomy.yaml                # Master technique registry (75 techniques)
│
├── registry/                    # Asset Registry — universal catalog
│   ├── asset-registry.yaml      #   Master index
│   ├── skills.yaml              #   44 skills cataloged
│   ├── agents.yaml              #   104 agents (14 frameworks)
│   ├── squads.yaml              #   Registered squads
│   ├── mcps.yaml                #   25 MCP servers
│   ├── playbooks.yaml           #   Technique playbooks
│   └── frameworks.yaml          #   14 agent frameworks
│
├── prompt-gen/                  # Prompt Generation — Universal Prompt Forge + per-workstream creation
│   ├── prompt-forge.md          #   Universal Prompt Forge algorithm (3-tier: MICRO/QUICK/FULL)
│   ├── technique-index.yaml     #   Compact index of 75 techniques (MICRO tier source)
│   ├── dispatch-profiles.yaml   #   9 dispatch type profiles with tier rules
│   ├── prompt-generator.md      #   5-phase pipeline algorithm (FULL tier engine)
│   ├── technique-mapper.md      #   Archetype → technique quick-path (QUICK tier engine)
│   └── prompt-templates/        #   7 YAML templates (agent-handoff, squad-brief, etc.)
│
├── quality-gates/               # Quality Gates — verification cascade
│   ├── gate-definitions.yaml    #   4-level gates with domain thresholds
│   ├── scoring-rubrics.yaml     #   Bloom-level scoring rubrics
│   └── gate-runner.md           #   Gate execution protocol
│
├── execution/                   # Execution Engine — lifecycle management
│   ├── flow-engine.md           #   Complete request lifecycle
│   ├── delegation-protocols.md  #   5 delegation modes
│   └── squad-delegation.md      #   Squad chief delegation protocol
│
├── integrations/                # Integrations — cross-squad bridges (11 bridges)
│   ├── copy-squad-bridge.md     #   HRM ↔ Copy Squad bridge
│   ├── brand-squad-bridge.md    #   HRM ↔ Brand Squad bridge
│   ├── design-squad-bridge.md   #   HRM ↔ Design Squad bridge
│   ├── data-squad-bridge.md     #   HRM ↔ Data Squad bridge
│   ├── cybersecurity-squad-bridge.md  # HRM ↔ Cybersecurity Squad bridge
│   ├── c-level-squad-bridge.md  #   HRM ↔ C-Level Squad bridge
│   ├── storytelling-squad-bridge.md   # HRM ↔ Storytelling Squad bridge
│   ├── traffic-masters-squad-bridge.md # HRM ↔ Traffic Masters Squad bridge
│   ├── hormozi-squad-bridge.md  #   HRM ↔ Hormozi Squad bridge
│   ├── movement-squad-bridge.md #   HRM ↔ Movement Squad bridge
│   └── advisory-board-squad-bridge.md # HRM ↔ Advisory Board Squad bridge
│
├── techniques/                  # 75 techniques across 13 categories
├── templates/                   # YAML prompt skeletons
├── playbooks/                   # End-to-end workflow guides
├── checklists/                  # Quality assurance checklists
├── references/                  # Knowledge base references
├── examples/                    # End-to-end flow examples (simple, moderate, complex)
├── orchestration-guide.md       # Quick-start operational reference
└── hrm-agent/                   # Core algorithms
    ├── technique-selector.md    #   4-phase technique scoring
    └── pipeline-builder.md      #   Technique pipeline construction
```

## Technique Taxonomy (75 techniques)

```
A. Foundations (10)          — Zero-shot, Few-shot, Role, Frameworks, Scaffolding
B. Reasoning (20)            — CoT, ToT, GoT, ReAct, CoD, BoT, SoT, PoT, ...
C. Advanced Reasoning (5)    — XoT, Thought Propagation, Step-Back, Meta-Prompting
D. Verification (10)         — CoVe, Self-Refine, Reflexion, Debate, RAG variants
E. Perception & Context (3)  — System 2 Attention, SimToM, Directional Stimulus
F. Agents & Tool Use (4)     — Tool-Augmented, Prompt Chaining, Planner-Worker
G. Prompt Programming (4)    — LMQL, Guidance, Outlines, SGLang
H. Optimization (7)          — DSPy, OPRO, APE, TextGrad, PromptBreeder, ...
I. Soft Prompts (3)          — Prompt Tuning, Prefix Tuning, P-Tuning v2
J. Security (3)              — Injection Defense, Instruction Hierarchy, Guardrails
K. Alignment (1)             — Constitutional AI
L. Reasoning Tokens (3)      — Extended Thinking, o1/o3, DeepSeek-R1
M. Multimodal (2)            — Multimodal CoT, Vision-Language Prompting
```

## Subsystems

### 1. Asset Registry (`registry/`)
Machine-readable catalog of ALL orchestration assets. The HRM queries this in Step 0.7 to match workstreams to the best available agents, squads, and MCPs.

### 2. Universal Prompt Forge (`prompt-gen/`)
Three-tier prompt engineering system that applies techniques proportionally to EVERY dispatch point — from TRIAGE mini-tasks to FULL-mode workstream agents. Tiers: MICRO (1-2 techniques, zero cost), QUICK (3-5, pre-computed), FULL (3-7, 4-phase scoring). Uses technique-selector and pipeline-builder from `hrm-agent/` for FULL tier.

### 3. Quality Gates (`quality-gates/`)
4-level verification cascade (syntax → local → global → semantic) with domain-specific thresholds (code: 0.88, security: 0.95, design: 0.85) and Bloom-level scoring rubrics.

### 4. Execution Engine (`execution/`)
Manages the complete request lifecycle: triage → registry lookup → analysis → plan → prompt gen → execute → verify → deliver. Supports 6 execution modes including squad delegation.

### 5. Integrations (`integrations/`)
Cross-squad bridges. 11 bridges connecting HRM to all registered squads for automatic delegation of domain-specific workstreams (Copy, Brand, Design, Data, Cybersecurity, C-Level, Storytelling, Traffic Masters, Hormozi, Movement, Advisory Board).

### 6. HRM Architect (`hrm-architect/SKILL.md`)
The core 12-step process enhanced with: Step 0.7 (Registry Lookup), Step 9.5 (Universal Prompt Forge), dynamic agent selection, squad delegation detection, and squad convergence monitoring.

## Request Flow

```
User Input → Step 0 (Triage) → Step 0.5 (Discovery) → Step 0.7 (Registry Lookup)
  → Steps 1-8 (Analysis) → Step 9 (ExecutionPlan) → Step 9.5 (Universal Prompt Forge)
  → SET display → Execute (agents/squads) → Step 10 (Convergence Monitoring)
  → Step 11 (Verification Cascade) → Deliver or Step 12 (Backtracking)
```

## Prompt Forge Tiers

| Tier | Techniques | Applied When | Source |
|------|-----------|-------------|--------|
| MICRO | 1-2 | Always (even TRIAGE) | `technique-index.yaml` |
| QUICK | 3-5 | FULL_LIGHT + FULL modes | `technique-mapper.md` |
| FULL | 3-7 | FULL mode only | `technique-selector.md` + `pipeline-builder.md` |

## Execution Modes

| Mode | When | Delegation Target |
|------|------|-------------------|
| Single | 1 subtask, simple | Single agent |
| Parallel | 2+ independent subtasks | Multiple agents in parallel |
| Swarm | 3+ subtasks with dependencies | agent-router → swarm-orchestrator |
| Agent Teams | 2-5 workstreams with peer communication | agent-teams-protocol |
| Squad Delegation | Workstream matches squad domain | Squad chief |
| Hybrid | Mix of agent + squad workstreams | Agents + squad chiefs |

## Key References

| Resource | Description |
|----------|-------------|
| [The Prompt Report](https://arxiv.org/abs/2406.06608) | Schulhoff et al. 2024 — Systematic survey of prompting techniques |
| [Prompting Guide](https://www.promptingguide.ai/) | DAIR.AI — Community-maintained prompt engineering guide |
| [Anthropic Docs](https://docs.anthropic.com/) | Claude prompt engineering documentation |
| [DSPy](https://github.com/stanfordnlp/dspy) | Stanford NLP — Programmatic prompt optimization framework |
