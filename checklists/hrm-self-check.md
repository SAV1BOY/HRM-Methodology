# HRM Self-Verification Checklist

Run this checklist to verify the HRM Architect is operating correctly. Check each item as you progress through the steps.

---

## Phase 0: Startup Verification

- [ ] Step 0 executed and classified TYPE/DOMAIN/COMPLEXITY/ARTIFACT
- [ ] complexity_score calculated (0-10 range, not null)
- [ ] hrm_mode decided (TRIAGE | FULL_LIGHT | FULL)
- [ ] Bootstrap loaded correct files for the selected mode
- [ ] using-superpowers discovery executed (PASSO 0.5, parallel)

## Phase 0.7: Registry Verification

- [ ] Registry lookup executed (Step 0.7)
- [ ] `registry_matches.skills` has at least 1 matching skill
- [ ] `registry_matches.agents` has at least 1 matching agent
- [ ] Squad delegation detected if workstream domain matches squad domain
- [ ] MCP integrations identified if task requires external tools

## Phase 1: Analysis Verification (FULL_LIGHT and FULL only)

- [ ] Bloom level determined (1-6) with correct verb mapping
- [ ] Complexity assessment has all 5 dimensions scored
- [ ] Decomposability checked with pattern identified
- [ ] Methodology selected matching Bloom level and complexity
- [ ] Budget calculated with 60/30/10 allocation

## Phase 2: Decomposition Verification (FULL only)

- [ ] Workstreams <= 5 (maximum limit respected)
- [ ] Zero file ownership overlap between workstreams
- [ ] Dependencies form a DAG (no circular dependencies)
- [ ] Each workstream has weight >= 10%
- [ ] Interface contracts defined for communicating workstreams
- [ ] Archetypes assigned from registry (not hardcoded fallback)
- [ ] Hyperparameters set per domain config

## Phase 3: Plan Generation Verification

- [ ] ExecutionPlan generated with ALL mandatory fields:
  - [ ] task, bloom_level, complexity_score
  - [ ] decomposition with level_0 (objective, constraints, success_criteria)
  - [ ] quality_gates with verification_levels and threshold
  - [ ] loop_protocol with max_loops and backtracking_triggers
- [ ] prompt_generation_spec filled for each workstream
- [ ] squad_delegations defined if squads detected in registry
- [ ] mcp_integrations listed if MCPs relevant
- [ ] Plan version tagged (v1 = prototype)

## Phase 4: Prompt Generation Verification (FULL only)

- [ ] Prompts instantiated for each workstream (Step 9.5)
- [ ] Each prompt has: role, objective, scope, context, quality, budget
- [ ] Technique pipeline applied per archetype (from technique-mapper)
- [ ] Prompt validated against checklists/prompt-quality.md
- [ ] Squad briefs use squad-brief.yaml template (not agent-handoff)

## Phase 4.5: Prompt Forge Verification

- [ ] Forge tier determined for EACH dispatch point (not just top-level workstreams)
- [ ] technique_pipeline present in ALL prompts (even TRIAGE mode gets MICRO)
- [ ] Tier appropriate to mode and granularity (check against scaling matrix):
  - TRIAGE: all dispatch points → MICRO
  - FULL_LIGHT: tasks → QUICK, subtasks → MICRO
  - FULL: tasks → FULL, subtasks → QUICK, mini-tasks → MICRO
- [ ] technique-index.yaml loaded in bootstrap (TRIAGE+ mode)
- [ ] dispatch-profiles.yaml loaded in bootstrap (TRIAGE+ mode)
- [ ] Dispatch type profiles match: correct template selected for each type
- [ ] MICRO techniques capped at 2, QUICK at 5, FULL at 7
- [ ] Gate reviewers at level >= 3 upgraded from MICRO to QUICK
- [ ] Feedback targets always MICRO (regardless of mode)
- [ ] Escalation reports always MICRO with output-format only

## Phase 5: SET Verification

- [ ] SET shown to user before execution begins
- [ ] SET includes FASE 0 with hrm-architect [x] and using-superpowers [x]
- [ ] All planned skills listed in correct phase order
- [ ] SET matches ExecutionPlan workstreams

## Phase 6: Execution Verification (FULL only)

- [ ] Execution mode matches ExecutionPlan (single/parallel/swarm/teams/hybrid)
- [ ] Convergence monitoring active (Step 10)
- [ ] Gate checks executed at phase transitions
- [ ] Budget tracking within allocation limits

## Phase 7: Quality Gate Verification

- [ ] Verification cascade executed (Step 11)
- [ ] Correct number of levels checked per complexity:
  - complexity < 3: up to Level 2 (local)
  - complexity < 6: up to Level 3 (global)
  - complexity >= 6: all 4 levels
  - domain == security: all 4 levels always
- [ ] Results logged with score and pass/fail per level

## Phase 8: Backtracking Verification (if quality < threshold)

- [ ] Root-cause analysis performed before re-execution (Step 12A)
- [ ] Credit assignment identifies responsible workstream/agent (Step 12B)
- [ ] Backtracking is proportional to failure type (Step 12C)
- [ ] Plan evolved (v1 -> v2+) with documented changes
- [ ] Max 3 loops enforced before user escalation

## Phase 9: Delivery Verification

- [ ] All success_criteria from level_0 addressed
- [ ] All deliverables exist and are non-empty
- [ ] Self-check score >= domain threshold from config.yaml
- [ ] No TRIAGE-mode shortcuts used for FULL-mode tasks

## Phase 9.5: Evolution Layer Verification (Section 19)

> Applies when the squad has an active Evolution Layer (`evolution/` + `evolution.enabled: true`).
> Canonical gate detail lives in `checklists/evolution-gate.md`; this is the one-line self-check hook.

- [ ] Section 19 active: squad emitted an EVOLUTION SIGNAL with an auto-measurable `primary_kpi` +
      locked `metric_hash`, KPI delta appended to `lineage.jsonl`, and the harness
      (quality_gates + meta_metric) hash-verified UNCHANGED by an EXTERNAL verifier (git signed-tag hook / human).
- [ ] Liveness: `evolution/status.py` dashboard fresh (cron-heartbeat < 7d); loops firing; bootstrap stage sane.

---

## Scoring

Count checked items / total applicable items for current mode:

| Mode | Applicable Phases | Min Score to Pass |
|------|------------------|-------------------|
| TRIAGE | 0, 0.7, 4.5, 5, 9 | 100% (all simple checks) |
| FULL_LIGHT | 0, 0.7, 1, 3, 4.5, 5, 9 | >= 90% |
| FULL | 0-9 (all phases, including 4.5) | >= 85% |

If score < threshold: review missed items, identify pattern, correct before delivery.
