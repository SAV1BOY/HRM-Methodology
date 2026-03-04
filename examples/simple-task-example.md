# Simple Task Example: HRM End-to-End Flow (TRIAGE Mode)

> Demonstrates the minimal HRM flow for a simple bug fix. TRIAGE mode skips Steps 1-12 and produces a final plan that does not evolve.

---

## User Input

> "Corrige o bug no login que nao valida email"

---

## Step 0: HRM Triage

```
=== HRM TRIAGE ===
Input: "Corrige o bug no login que nao valida email"
Timestamp: 2026-03-03T14:22:00Z

Classification:
  TIPO: FIX
  DOMINIO: WEB
  COMPLEXIDADE: SIMPLES
  ARTEFATO: CODIGO

Signals detected:
  TIPO=FIX: "corrige", "bug" -> FIX
  DOMINIO=WEB: "login" -> web form context
  COMPLEXIDADE=SIMPLES: 1 file expected (login validation), 1 concept (email regex), < 5 tool calls
  ARTEFATO=CODIGO: output will be source code fix

Complexity Assessment (quick):
  estimated_files: 1-2 (validation logic + possibly test)
  estimated_tool_calls: 3-5
  multi_domain: false
  parallelizable: false
  uncertainty: low

complexity_score: 2.0 / 10
hrm_mode: TRIAGE (score < 3.0)

Decision: TRIAGE mode. Steps 1-12 skipped.
HRM will NOT remain active as supervisor.
Plan v1 is FINAL (will not evolve).
==================
```

### Why TRIAGE Mode

The task meets all TRIAGE conditions:
- `complexity_score` = 2.0 (below the 3.0 threshold)
- Single file affected (login validation logic)
- Single concept (email validation)
- No creative work involved
- No multi-domain complexity
- Estimated 3-5 tool calls

---

## Step 0.5: Discovery (using-superpowers)

Runs in parallel with Step 0. For TRIAGE tasks, the discovery is lightweight -- it confirms which skills are available but does not produce a full agent/workflow catalog since the HRM will not be assigning workstreams to agents.

```yaml
discovery_result:
  status: complete
  skills_available: 44
  relevant_skills_for_FIX:
    - systematic-debugging (phase 2, development)
    - test-driven-development (phase 2, development)
    - verification-before-completion (phase 3, review)
  agents_available: 103
  squads_available: 2
  note: "TRIAGE mode -- full agent mapping not needed"
```

---

## Step 0.7: Registry Lookup (minimal)

For TRIAGE mode, the registry lookup is abbreviated. It only confirms skill availability; no agent assignment or squad delegation is needed.

```yaml
registry_matches:
  skills:
    - id: systematic-debugging
      phase: 2
      match_reason: "TIPO == FIX"
      trigger: "bug, error detected"
    - id: verification-before-completion
      phase: 3
      match_reason: "ARTEFATO == CODIGO, mandatory before completion"
      trigger: "always when code is present"
  agents: []  # Not assigned in TRIAGE mode
  squads: []  # No squad domain match needed
  mcps: []    # No MCP integration needed
```

---

## ExecutionPlan: Not Generated

In TRIAGE mode (`complexity_score < 3.0`), the HRM does **not** produce a full ExecutionPlan. Instead, it provides a simple skill recommendation list. Steps 1-12 are skipped entirely.

```yaml
triage_plan:
  mode: TRIAGE
  complexity_score: 2.0
  plan_version: "v1 (final, will not evolve)"
  supervisor_active: false
  recommended_skills:
    phase_0:
      - hrm-architect  # Already executed (this triage)
      - using-superpowers  # Already executed (discovery)
    phase_2:
      - systematic-debugging  # Root-cause the validation bug
    phase_3:
      - verification-before-completion  # Verify fix works
  estimated_total_cost: 8-12 tool calls
  quality_gates:
    max_level: 2  # Per auto_level_policy: complexity_score < 3 -> max level 2
    domain: code
    threshold: 0.88
```

---

## Step 9.5: Universal Prompt Forge

Even in TRIAGE mode, the Prompt Forge applies MICRO tier techniques (1-2 techniques, zero cost). This ensures every dispatch point receives technique-enhanced prompts.

```yaml
forge_output:
  dispatch_context:
    hrm_mode: TRIAGE
    dispatch_type: triage-agent
    granularity: task
    domain: code
  tier: MICRO
  techniques: [role-prompting, zero-shot-cot]
  template: agent-handoff
  estimated_tokens: 0  # zero extra reads, techniques from pre-loaded index

  injected_text: |
    Follow this approach:
    1. **Role**: You are an expert web developer specializing in form validation and authentication.
    2. **Reasoning**: Think through the problem step by step before implementing.
       - What is the current email validation behavior?
       - What is the expected behavior?
       - What is the minimal fix?
```

### Forge Explanation (TRIAGE)

In TRIAGE mode:
- **Tier**: Always MICRO (1-2 techniques)
- **Source**: `technique-index.yaml` micro_defaults for `code_fix` category
- **Techniques**: `role-prompting` (domain expertise persona) + `zero-shot-cot` (step-by-step reasoning)
- **Cost**: Zero additional file reads — techniques are injected from pre-loaded index
- **Template**: `agent-handoff` with MICRO-forged technique steps

This is the minimal technique application — it adds a domain-expert role and structured reasoning without any of the heavier QUICK or FULL tier machinery.

---

## SET (Skill Execution Timeline)

```
=== SKILL EXECUTION TIMELINE ===
Tarefa: Corrigir bug no login que nao valida email
Classificacao: TIPO=FIX DOMINIO=WEB COMPLEXIDADE=SIMPLES ARTEFATO=CODIGO
HRM Mode: TRIAGE | Complexity Score: 2.00/10
Plano: v1 (final, nao evolui)

FASE 0 (Startup -- OBRIGATORIO):
  [x] hrm-architect -- TRIAGE (PASSO 0: classificacao rapida, plano simples)
  [x] using-superpowers -- (PASSO 0.5: discovery de skills disponiveis)

FASE 2 (Execucao):
  [ ] systematic-debugging -- TIPO=FIX, investigar causa raiz do bug de validacao

FASE 3 (Revisao):
  [ ] verification-before-completion -- ARTEFATO=CODIGO, verificar fix antes de concluir
================================
```

**Note**: FASE 1 (Planning) is empty because SIMPLES tasks do not require planning skills. The task goes directly from triage to execution.

---

## Execution Flow

### What happens during execution:

**1. systematic-debugging executes:**

The debugging skill follows the ReAct pattern:

```
THOUGHT: The user reports that the login form does not validate email.
         I need to find the login component and its validation logic.

ACTION: Read the login form file (e.g., src/components/LoginForm.tsx)

OBSERVATION: The form has a handleSubmit function but no email format
             validation. It only checks if the email field is non-empty.

THOUGHT: The bug is clear -- there is no regex or format check for
         the email field. Users can submit "abc" as an email.

ACTION: Add email validation using a regex pattern or a validation
        library.

OBSERVATION: Fix applied -- added isValidEmail() function with
             standard email regex and integrated it into form validation.

ACTION: Write a test for the validation logic.

OBSERVATION: Test passes for valid emails (user@domain.com) and
             fails correctly for invalid ones (abc, @domain, user@).
```

**2. verification-before-completion executes:**

```
Verification Checklist (Level 1 - Syntax + Level 2 - Local):

Level 1 (Syntax):
  [PASS] syntax_valid: Code compiles without errors
  [PASS] no_parse_errors: No syntax errors in modified files
  [PASS] format_correct: TypeScript/JSX format maintained
  [PASS] files_exist: Modified file exists and is non-empty

Level 2 (Local):
  [PASS] unit_tests_pass: Email validation tests pass
  [PASS] deliverables_complete: Bug fix implemented
  [PASS] internal_consistency: Validation logic consistent

Result: ALL PASS
Score: 0.95 (above threshold 0.88 for code domain)
Verdict: READY TO DELIVER
```

---

## Quality Gates

Since `complexity_score < 3`, the auto_level_policy limits quality gates to **max level 2** (Syntax + Local). Levels 3 (Global) and 4 (Semantic) are not run.

```yaml
quality_gate_results:
  level_1_syntax:
    status: PASS
    checks:
      syntax_valid: PASS
      no_parse_errors: PASS
      format_correct: PASS
      files_exist: PASS
    estimated_cost: 2 tool calls

  level_2_local:
    status: PASS
    checks:
      unit_tests_pass: PASS
      deliverables_complete: PASS
      internal_consistency: PASS
    score: 0.95
    threshold: 0.88
    estimated_cost: 3 tool calls

  levels_3_4: SKIPPED (auto_level_policy: complexity_score < 3 -> max level 2)

  aggregate:
    passed: true
    total_cost: 5 tool calls
```

---

## Plan Evolution

**No evolution occurs.** In TRIAGE mode, the plan v1 is final.

```yaml
plan_evolution:
  - version: "v1"
    created_at: "Step 0 Triage"
    changes: "Initial and final plan"
    status: "FINAL -- TRIAGE mode, no evolution"
```

---

## Cost Summary

| Phase | Tool Calls | Notes |
|-------|-----------|-------|
| Step 0: Triage | 2 | Classification + mode decision |
| Step 0.5: Discovery | 1 | Lightweight skill scan |
| Step 0.7: Registry | 1 | Abbreviated lookup |
| Fase 2: systematic-debugging | 4 | Read code, identify bug, fix, test |
| Fase 3: verification | 3 | Syntax check + local check |
| **Total** | **~11** | Within budget (estimated 8-12) |

---

## Key Takeaways for TRIAGE Mode

1. **Minimal overhead**: Only ~4 tool calls for HRM infrastructure (Steps 0, 0.5, 0.7), the rest goes to actual work.
2. **No ExecutionPlan**: Full YAML plan is not generated; a simple skill recommendation list suffices.
3. **No supervisor**: HRM does not remain active to monitor execution.
4. **No plan evolution**: Plan v1 is final and does not iterate.
5. **Quality gates capped**: Auto-level policy limits to levels 1-2 for simple tasks.
6. **No agent assignment**: Skills execute directly; no agents are selected from the registry.
7. **Fast path**: Total flow is ~11 tool calls, completing in under 30 seconds.
