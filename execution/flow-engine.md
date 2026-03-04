# Execution Flow Engine

> Complete lifecycle specification for processing a user request from input to delivery. Defines the end-to-end flow that the HRM Architect orchestrates.

---

## Complete Flow

```
USER INPUT
    |
    v
[Step 0] TRIAGE
    |  Classify: TIPO/DOMINIO/COMPLEXIDADE/ARTEFATO
    |  Calculate: complexity_score
    |  Decide: hrm_mode (TRIAGE/FULL_LIGHT/FULL)
    |                                          |
    |  [Step 0.5] DISCOVERY (parallel)         |
    |  using-superpowers scans all assets       |
    v                                          v
[Step 0.7] REGISTRY LOOKUP (NEW)
    |  Load asset-registry.yaml
    |  Query: skills by phase + domain
    |  Query: agents by archetype + domain
    |  Query: squads by domain coverage
    |  Query: mcps by capability match
    |  Return: registry_matches
    |
    |--- If TRIAGE mode (score < 3.0) -------> [SIMPLE PATH]
    |                                            MICRO Forge (1-2 techniques from index)
    |                                            Generate SET
    |                                            Execute with MICRO-forged prompt
    |                                            Verify (level 1-2)
    |                                            Deliver
    |
    v
[Steps 1-8] FULL ANALYSIS
    |  Step 1: Bloom level analysis
    |  Step 2: 5-dimension complexity assessment
    |  Step 3: Decomposability check
    |  Step 4: Methodology selection
    |  Step 5: Resource calculation
    |  Step 6: Hierarchical decomposition
    |  Step 7: Domain hyperparameter tuning
    |  Step 8: Execution mode mapping
    v
[Step 9] GENERATE EXECUTION PLAN v1
    |  Compile all analysis into ExecutionPlan
    |  Map workstreams to agents from registry
    |  Define interface contracts
    |  Set quality gates and thresholds
    v
[Step 9.5] UNIVERSAL PROMPT FORGE
    |  For EACH dispatch point (not just top-level workstreams):
    |    1. Build dispatch_context (hrm_mode, dispatch_type, granularity, archetype, domain)
    |    2. Resolve tier: MICRO | QUICK | FULL (from mode x granularity matrix)
    |    3. Select techniques per tier:
    |       MICRO: technique-index.yaml lookup (1-2 techniques, zero cost)
    |       QUICK: technique-mapper.md pre-computed pipeline (3-5 techniques)
    |       FULL:  technique-selector + pipeline-builder (3-7 techniques, 4-phase scoring)
    |    4. Inject into dispatch-appropriate template
    |    5. Validate (QUICK and FULL tiers only)
    |  Output: ForgeOutput per dispatch point (prompt, techniques, tier, template)
    v
[SET] PRESENT TO USER
    |  Show Skill Execution Timeline
    |  Show workstreams, agents, estimated cost
    v
[FASE 1] PLANNING EXECUTION
    |  Execute planning skills (brainstorming, planning-with-files, etc.)
    |  Gate check: planning quality OK?
    |  Plan evolution: v1 -> v2 if needed
    v
[FASE 2] MAIN EXECUTION
    |  Route by execution_mode:
    |
    |  SINGLE -----> Agent with generated prompt
    |  PARALLEL ---> dispatching-parallel-agents with prompts
    |  SWARM ------> agent-router -> swarm-orchestrator with prompts
    |  TEAMS ------> agent-teams-protocol with prompts
    |  SQUAD ------> Delegation to squad chief with brief (NEW)
    |
    |  [Step 10] CONVERGENCE MONITORING (continuous)
    |    Monitor all agents/squads
    |    Detect stagnation
    |    Reallocate budget if needed
    v
[Step 11] VERIFICATION CASCADE
    |  Run gate-runner: syntax -> local -> global -> semantic
    |  Score against domain threshold and Bloom rubric
    |
    +-- PASS ---------> [FASE 3]
    |
    +-- FAIL ---------> [Step 12] BACKTRACKING
                          Root-cause analysis
                          Credit assignment
                          Targeted re-execution
                          Plan evolution: vN -> v(N+1)
                          Loop back to Step 11
                          Max 3 loops, then escalate
    v
[FASE 3] REVIEW AND DELIVERY
    |  Run review skills (code-review, verification-before-completion)
    |  Final quality check
    |  MCP integrations if applicable (deploy, notify, etc.)
    v
DELIVER TO USER
```

---

## Decision Points

### Mode Selection (Step 0)

| complexity_score | Mode | Steps | Supervisor |
|-----------------|------|-------|-----------|
| < 3.0 | TRIAGE | 0 only | No |
| 3.0 - 4.9 | FULL_LIGHT | 0-5, 9 | Maybe |
| >= 5.0 | FULL | 0-12 | Yes |

### Execution Mode (Step 8)

| Criteria | Mode | Target |
|----------|------|--------|
| 1 subtask, simple | Single Agent | Direct agent dispatch |
| 2+ independent tasks | Parallel | dispatching-parallel-agents |
| 3+ tasks, dependencies | Swarm | swarm-orchestrator |
| 2-5 workstreams, peer comm | Teams | agent-teams-protocol |
| Domain covered by squad | Squad | Squad chief delegation |

### Backtracking Depth (Step 12)

| Failure Type | Action | Cost |
|-------------|--------|------|
| Syntax error | Refine prompt, re-run 1 agent | ~10% |
| Local failure | Re-run workstream | ~20% |
| Integration failure | Fix contracts, re-run affected | ~30% |
| Workstream failure | Reset with different agent | ~40% |
| Global inconsistency | Re-decompose | ~50% |
| Systematic failure | New methodology | ~100% |

---

## State Machine

```
IDLE -> TRIAGE -> ANALYSIS -> PLANNING -> EXECUTING -> VERIFYING -> DELIVERING
                                  ^          |             |
                                  |          v             |
                                  +--- BACKTRACKING <------+
                                  |
                                  +--- ESCALATING (to user)
```

### State Transitions

- IDLE -> TRIAGE: User input received
- TRIAGE -> ANALYSIS: complexity_score >= 3.0
- TRIAGE -> EXECUTING: complexity_score < 3.0 (simple path)
- ANALYSIS -> PLANNING: ExecutionPlan generated
- PLANNING -> EXECUTING: Planning phase complete, gate passed
- EXECUTING -> VERIFYING: All workstreams reported complete
- VERIFYING -> DELIVERING: All gates passed
- VERIFYING -> BACKTRACKING: Gate failed
- BACKTRACKING -> EXECUTING: Re-execution with refined plan
- BACKTRACKING -> ESCALATING: Max loops exceeded
- ESCALATING -> IDLE: User provides guidance

---

## Budget Tracking

Throughout execution, track:

```yaml
budget_tracker:
  total_allocated: <N>
  used:
    triage: <n>
    analysis: <n>
    planning: <n>
    execution: <n>
    verification: <n>
    backtracking: <n>
  remaining: <N - sum(used)>
  reserve_status: "healthy|warning|critical"
  emergency_mode: false
```

Trigger emergency mode when `remaining < 20% of total`.

---

## Plan Evolution Log

```yaml
plan_evolution:
  - version: "v1"
    created_at: "Step 9"
    changes: "Initial plan"
  - version: "v2"
    created_at: "Gate check after Phase 1"
    changes: "Added systematic-debugging (test failure detected)"
    trigger: "quality_gate_failed"
  - version: "v3"
    created_at: "Backtracking Loop 1"
    changes: "Replaced agent for auth workstream"
    trigger: "credit_assignment_identified_underperformer"
```
