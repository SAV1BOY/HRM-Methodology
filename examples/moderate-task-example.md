# Moderate Task Example: HRM End-to-End Flow (FULL_LIGHT Mode)

> Demonstrates the FULL_LIGHT flow for adding dark mode to a React dashboard. Steps 0, 1-5, and 9 execute. The ExecutionPlan is simplified but can evolve if quality gates fail.

---

## User Input

> "Adiciona dark mode ao dashboard React"

---

## Step 0: HRM Triage

```
=== HRM TRIAGE ===
Input: "Adiciona dark mode ao dashboard React"
Timestamp: 2026-03-03T14:35:00Z

Classification:
  TIPO: BUILD
  DOMINIO: REACT
  COMPLEXIDADE: MODERADA
  ARTEFATO: CODIGO

Signals detected:
  TIPO=BUILD: "adiciona" -> BUILD
  DOMINIO=REACT: "React", "dashboard" -> REACT
  COMPLEXIDADE=MODERADA: 2-4 files (theme config, context provider, component updates), 1 domain (frontend), 10-15 tool calls
  ARTEFATO=CODIGO: output will be React components and theme system

Complexity Assessment (quick):
  estimated_files: 3-4 (theme config, ThemeProvider, component updates, possibly CSS/tokens)
  estimated_tool_calls: 12-18
  multi_domain: false
  parallelizable: true (theme system + component migration are independent after theme is defined)
  uncertainty: low-medium (scope depends on how many components need updating)

complexity_score: 4.0 / 10
hrm_mode: FULL_LIGHT (3.0 <= score < 5.0)

Decision: FULL_LIGHT mode. Execute Steps 0, 1, 2, 3, 4, 5, 9.
HRM may remain active depending on uncertainty.
Plan v1 may evolve (v1 -> v2) if quality gates fail.
==================
```

---

## Step 0.5: Discovery (using-superpowers)

```yaml
discovery_result:
  status: complete
  skills_available: 44
  relevant_skills:
    phase_1:
      - brainstorming (TIPO=BUILD, DOMINIO=REACT)
    phase_2:
      - test-driven-development (TIPO=BUILD, ARTEFATO=CODIGO)
      - frontend-design (DOMINIO=REACT, TIPO=BUILD)
      - react-best-practices (DOMINIO=REACT)
      - ui-ux-pro-max (theme/design system context)
      - theme-factory ("tema/theme" implicit in dark mode)
    phase_3:
      - verification-before-completion (ARTEFATO=CODIGO)
  agents_relevant:
    - id: "01-wshobson-frontend-developer"
      archetype: L-Builder-Frontend
      domain_affinity: [WEB, REACT]
      cost_tier: medium
    - id: "01-wshobson-ui-designer"
      archetype: L-Builder-Frontend
      domain_affinity: [WEB, REACT, DESIGN]
      cost_tier: medium
  squads_relevant: []  # No squad domain match for this task
```

---

## Step 0.7: Registry Lookup

```yaml
registry_matches:
  skills:
    - id: brainstorming
      phase: 1
      match_reason: "TIPO=BUILD, DOMINIO=REACT"
    - id: frontend-design
      phase: 2
      match_reason: "DOMINIO=REACT, TIPO=BUILD"
    - id: react-best-practices
      phase: 2
      match_reason: "DOMINIO=REACT"
    - id: theme-factory
      phase: 2
      match_reason: "'dark mode' implies theming"
    - id: test-driven-development
      phase: 2
      match_reason: "TIPO=BUILD, ARTEFATO=CODIGO"
    - id: verification-before-completion
      phase: 3
      match_reason: "ARTEFATO=CODIGO, mandatory"
  agents:
    - id: "01-wshobson-frontend-developer"
      archetype: L-Builder-Frontend
      assigned_to: [theme-system, component-migration]
    - id: "01-wshobson-ui-designer"
      archetype: L-Builder-Frontend
      assigned_to: [theme-system]  # Backup/alternative
  squads: []
  mcps: []
```

---

## Step 1: Bloom Level Analysis

```yaml
bloom_analysis:
  user_request: "Adiciona dark mode ao dashboard React"
  bloom_level: 3
  bloom_name: "Aplicar (Apply)"
  rationale: |
    The user asks to APPLY a known pattern (dark mode theming) to an existing
    React dashboard. This is not pure recall (level 1-2), nor does it require
    novel analysis or evaluation (levels 4-5). It requires applying established
    React theming patterns (CSS variables, Context API, prefers-color-scheme)
    to an existing codebase.
  implications:
    - Scoring rubric: execution_validation (pass_rate, edge_cases, correct_approach)
    - Threshold: 0.90 (Bloom 3 threshold)
    - Technique selection: favor practical/implementation techniques over theoretical
```

---

## Step 2: Complexity Assessment (5 dimensions)

```yaml
complexity_assessment:
  dimension_1_cognitive:
    score: 3
    max: 10
    rationale: "Applying known patterns (CSS variables, Context API). No novel algorithms."
  dimension_2_scope:
    score: 4
    max: 10
    rationale: "3-4 files affected. Single domain (React frontend). Theme config + provider + component updates."
  dimension_3_uncertainty:
    score: 3
    max: 10
    rationale: "Well-understood problem. Main uncertainty: how many components need updating."
  dimension_4_interdependence:
    score: 4
    max: 10
    rationale: "Theme system must be defined before components can consume it. Sequential dependency between workstreams."
  dimension_5_quality_bar:
    score: 5
    max: 10
    rationale: "Production code. Must handle system preference detection, persist user choice, avoid flash of wrong theme."

  aggregate_score: 3.8 / 10
  adjusted_score: 4.0 / 10  # Rounded up due to sequential dependency
  mode_confirmation: FULL_LIGHT
```

---

## Step 3: Decomposability Check

```yaml
decomposability:
  is_decomposable: true
  decomposition_strategy: "sequential with parallel potential"
  workstreams:
    - name: theme-system
      description: "Create theme configuration, CSS variables/tokens, ThemeProvider context"
      independence: "fully independent, must execute first"
      estimated_files: 2 (theme.ts, ThemeProvider.tsx)
      estimated_effort: "8-10 tool calls"
    - name: component-migration
      description: "Update existing dashboard components to use theme tokens instead of hardcoded colors"
      independence: "depends on theme-system output (theme tokens)"
      estimated_files: 2-3 (existing components that use colors)
      estimated_effort: "6-8 tool calls"
  dependency_graph: "theme-system -> component-migration (sequential)"
  parallelizable: false  # component-migration depends on theme-system
  execution_mode_recommendation: "single or swarm (2 phases)"
```

---

## Step 4: Methodology Selection

```yaml
methodology:
  selected: "CoT Guiado por HRM (HRM-Guided Chain-of-Thought)"
  rationale: |
    For Bloom level 3 (Apply) with sequential workstreams in a single domain,
    a guided CoT approach works best. The HRM provides the decomposition and
    technique pipeline, and a single agent executes phase by phase.
  technique_pipeline_summary:
    theme-system:
      archetype: L-Builder-Frontend
      techniques: [role-prompting, plan-and-solve, few-shot, self-refine, checklist-prompting]
      source: "technique-mapper quick-path for L-Builder-Frontend"
    component-migration:
      archetype: L-Builder-Frontend
      techniques: [role-prompting, plan-and-solve, few-shot, self-refine, checklist-prompting]
      source: "technique-mapper quick-path for L-Builder-Frontend"
  domain_override_applied: "react: add output-format (JSX/TSX format control)"
```

---

## Step 5: Resource Calculation

```yaml
resource_calculation:
  workstreams:
    - name: theme-system
      archetype: L-Builder-Frontend
      agent_id: "01-wshobson-frontend-developer"
      predicted_cost: 10 tool calls
      budget_allocated: 12 tool calls (with 20% buffer)
      technique_cost: 5 technique steps
    - name: component-migration
      archetype: L-Builder-Frontend
      agent_id: "01-wshobson-frontend-developer"  # Same agent, phase 2
      predicted_cost: 8 tool calls
      budget_allocated: 10 tool calls (with 25% buffer)
      technique_cost: 5 technique steps
  overhead:
    hrm_triage: 3 tool calls
    discovery: 1 tool call
    registry_lookup: 1 tool call
    analysis_steps_1_5: 2 tool calls (FULL_LIGHT is lightweight)
    planning_skills: 3 tool calls (brainstorming)
    verification: 5 tool calls
  total_budget: 37 tool calls
  reserve: 5 tool calls (emergency)
  grand_total: 42 tool calls
```

---

## Step 9: ExecutionPlan (Simplified for FULL_LIGHT)

```yaml
execution_plan:
  version: "v1"
  mode: FULL_LIGHT
  complexity_score: 4.0
  bloom_level: 3  # Aplicar
  supervisor_active: false  # FULL_LIGHT: depends on uncertainty (low -> inactive)

  level_0:
    objective: "Add dark mode support to the existing React dashboard"
    success_criteria:
      - "Theme toggle works (light/dark switch in UI)"
      - "System preference detection (prefers-color-scheme)"
      - "User preference persists across sessions (localStorage)"
      - "No flash of wrong theme on page load (FOUC prevention)"
      - "All dashboard components respect theme tokens"
    constraints:
      - "Must use React Context API (no external state library)"
      - "Must use CSS custom properties for theme tokens"
      - "Must be accessible (sufficient contrast ratios in both themes)"
    domain_config:
      domain: code
      verification_threshold: 0.88
      max_cycles: 2

  level_1:
    workstreams:
      - name: theme-system
        objective: "Create the complete theming infrastructure"
        archetype: L-Builder-Frontend
        agent_id: "01-wshobson-frontend-developer"
        phase: 1  # Execute first
        file_ownership:
          - "src/theme/theme.ts"
          - "src/theme/ThemeProvider.tsx"
          - "src/theme/useTheme.ts"
        deliverables:
          - "Theme token definitions (colors, shadows, borders for light and dark)"
          - "ThemeProvider React context with toggle function"
          - "useTheme hook for consuming theme"
          - "System preference detection and localStorage persistence"
          - "FOUC prevention (script in HTML head or SSR handling)"
        estimated_effort: "10 tool calls"
        predicted_cost: 12
        verification: "Theme toggles correctly, persists, no FOUC"
        prompt_generation_spec:
          archetype_primary_type: "code, creative"
          technique_pipeline: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
          technique_source: "technique-mapper quick-path L-Builder-Frontend + react domain override"
          quality_checks: [syntax_valid, unit_tests_pass, deliverables_complete]
          bloom_rubric: "execution_validation (pass_rate >= 0.90)"

      - name: component-migration
        objective: "Update all dashboard components to consume theme tokens"
        archetype: L-Builder-Frontend
        agent_id: "01-wshobson-frontend-developer"
        phase: 2  # Execute after theme-system
        depends_on: [theme-system]
        file_ownership:
          - "src/components/Dashboard.tsx"
          - "src/components/Sidebar.tsx"
          - "src/components/Header.tsx"
          - "src/styles/*.css"
        deliverables:
          - "All hardcoded colors replaced with CSS custom properties"
          - "Components use useTheme hook where dynamic behavior needed"
          - "Theme toggle button added to dashboard header"
        estimated_effort: "8 tool calls"
        predicted_cost: 10
        verification: "Visual check in both themes, no hardcoded colors remain"
        prompt_generation_spec:
          archetype_primary_type: "code, creative"
          technique_pipeline: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
          technique_source: "technique-mapper quick-path L-Builder-Frontend + react domain override"
          quality_checks: [syntax_valid, unit_tests_pass, internal_consistency, deliverables_complete]
          bloom_rubric: "execution_validation (pass_rate >= 0.90)"

    interface_contracts:
      - source: theme-system
        target: component-migration
        contract: "ThemeProvider exports: ThemeProvider component, useTheme hook returning {theme, toggleTheme, isDark}"
        format: "TypeScript interface exported from src/theme/useTheme.ts"

  execution_mode: single  # Same agent, sequential phases (not parallel)
  execution_phases:
    - phase: 1
      workstreams: [theme-system]
      gate_after: true  # Run level 1-2 gate before proceeding
    - phase: 2
      workstreams: [component-migration]
      gate_after: true

  quality_gates:
    max_level: 3  # Per auto_level_policy: complexity_score < 6 -> max level 3
    levels: [syntax, local, global]
    domain_thresholds:
      level_2: 0.88
      level_3: 0.85

  loop_protocol:
    max_loops: 2
    backtracking_triggers:
      - "Theme tokens not consumable by components (contract broken)"
      - "FOUC detected on page load"
      - "Contrast ratio below WCAG AA in either theme"
      - "TypeScript compilation errors"
    escalation: "After 2 failed loops, report to user with diagnostic"

  plan_evolution:
    current: "v1"
    can_evolve: true
    evolution_triggers:
      - "Quality gate failure"
      - "More components discovered than estimated"
      - "Existing CSS architecture incompatible with CSS custom properties"
```

---

## Step 9.5: Universal Prompt Forge (QUICK Tier)

### Instantiated Agent-Handoff Prompt: Workstream "theme-system"

This is the actual prompt generated for the agent executing the theme-system workstream, using the `prompt-gen/prompt-templates/agent-handoff.yaml` template with all variables filled.

```markdown
You are a L-Builder-Frontend specialist working on the "theme-system" workstream.
Your expertise: frontend development, React component architecture, CSS custom properties, theming systems.

## Objective
Create the complete theming infrastructure for the React dashboard, enabling
light/dark mode switching with system preference detection and persistence.

### Success Criteria
- Theme toggle works (light/dark switch in UI)
- System preference detection (prefers-color-scheme media query)
- User preference persists across sessions (localStorage)
- No flash of wrong theme on page load (FOUC prevention)
- All theme tokens are accessible via CSS custom properties

## Scope
### File Ownership (ONLY modify these files)
- src/theme/theme.ts
- src/theme/ThemeProvider.tsx
- src/theme/useTheme.ts

### Deliverables
- Theme token definitions (colors, shadows, borders for light and dark)
- ThemeProvider React context with toggle function
- useTheme hook for consuming theme
- System preference detection and localStorage persistence
- FOUC prevention mechanism

## Project Context
- Tech stack: React, TypeScript, CSS Modules (existing dashboard)
- Existing patterns: Functional components with hooks, no state management library
- Constraints:
  - Must use React Context API (no external state library)
  - Must use CSS custom properties for theme tokens
  - Must be accessible (WCAG AA contrast ratios)

## Interface Contracts
### Outputs (to other workstreams)
- ThemeProvider component wrapping the app
- useTheme hook returning: { theme: 'light' | 'dark', toggleTheme: () => void, isDark: boolean }
- CSS custom properties: --color-bg-primary, --color-bg-secondary, --color-text-primary, --color-text-secondary, --color-border, --color-shadow, etc.

### Contract Format
TypeScript interface exported from src/theme/useTheme.ts

## Approach
Follow this technique pipeline:
1. **Role Prompting**: Act as a senior React developer specializing in design systems and theming
2. **Plan-and-Solve**: Before coding, plan the theme token structure and context architecture
3. **Few-Shot**: Reference existing patterns in the codebase (component style, hook patterns)
4. **Output Format**: Produce TypeScript (.ts/.tsx) with proper type annotations
5. **Self-Refine**: After initial implementation, review for edge cases (SSR, hydration, FOUC)
6. **Checklist Prompting**: Verify against accessibility checklist and deliverables list

## Quality Requirements
- Verification threshold: 0.88 (code domain)
- Bloom level: 3 (Aplicar)
- Key checks: syntax_valid, unit_tests_pass, deliverables_complete

## Budget
- Allocated tool calls: 12
- Maximum cycles: 2

## When to Report Problems
Report immediately to the HRM if:
- Theme tokens not consumable by components (contract broken)
- FOUC detected on page load despite prevention mechanism
- Contrast ratio below WCAG AA in either theme
- TypeScript compilation errors that cannot be resolved
```

### Technique Pipeline Explanation

The technique pipeline for this workstream was derived from the `technique-mapper.md` quick-path for the `L-Builder-Frontend` archetype:

```yaml
technique_derivation:
  archetype: L-Builder-Frontend
  base_pipeline: [role-prompting, plan-and-solve, few-shot, self-refine, checklist-prompting]
  domain_override: "react -> add output-format (JSX/TSX format control)"
  final_pipeline: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
  source: "prompt-gen/technique-mapper.md -> L-Builder-Frontend default + react override"
  full_scoring_needed: false  # Standard archetype + standard domain = quick-path sufficient
```

### Forge Context

```yaml
forge_output:
  dispatch_context:
    hrm_mode: FULL_LIGHT
    dispatch_type: workstream-agent
    granularity: task
    archetype: L-Builder-Frontend
    domain: react
  tier: QUICK
  techniques: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
  template: agent-handoff
  estimated_tokens: 0  # technique-mapper already loaded in bootstrap, zero extra reads

  tier_resolution:
    mode: FULL_LIGHT
    granularity: task
    matrix_result: QUICK
    profile: workstream-agent (MODE_DEPENDENT -> FULL_LIGHT -> QUICK)
    source: technique-mapper.md (L-Builder-Frontend + react domain override)
```

In FULL_LIGHT mode, the Forge uses the QUICK tier for top-level workstreams:
- **Source**: `technique-mapper.md` pre-computed pipeline for `L-Builder-Frontend` archetype
- **Domain override**: `react` adds `output-format` for JSX/TSX format control
- **Cost**: Zero extra reads — technique-mapper is already loaded in FULL_LIGHT bootstrap
- **Validation**: Lightweight (verify technique count <= 5, check for conflicts)

If this task had subtasks, they would receive MICRO tier (1-2 techniques from technique-index.yaml).

---

## SET (Skill Execution Timeline)

```
=== SKILL EXECUTION TIMELINE ===
Tarefa: Adicionar dark mode ao dashboard React
Classificacao: TIPO=BUILD DOMINIO=REACT COMPLEXIDADE=MODERADA ARTEFATO=CODIGO
HRM Mode: FULL_LIGHT | Complexity Score: 4.00/10
Plano: v1 (prototipo, pode evoluir se quality gates falham)

FASE 0 (Startup -- OBRIGATORIO):
  [x] hrm-architect -- FULL_LIGHT (PASSO 0: classificacao + Steps 1-5 + Step 9)
  [x] using-superpowers -- (PASSO 0.5: discovery de skills/agents)

FASE 1 (Planejamento):
  [ ] brainstorming -- TIPO=BUILD, DOMINIO=REACT (explorar abordagens de dark mode)

FASE 2 (Execucao):
  [ ] frontend-design -- DOMINIO=REACT, TIPO=BUILD (implementacao do tema + componentes)
  [ ] react-best-practices -- DOMINIO=REACT (padroes React para Context, hooks, memoization)
  [ ] theme-factory -- dark mode implica theming (tokens, variaveis CSS)
  [ ] test-driven-development -- TIPO=BUILD, ARTEFATO=CODIGO (testes para toggle, persistence)

FASE 3 (Revisao):
  [ ] verification-before-completion -- ARTEFATO=CODIGO (verificacao obrigatoria)
================================
```

---

## Execution Flow

### FASE 1: brainstorming

```
Brainstorming Output:
  Approaches considered:
    1. CSS Custom Properties + Context API (selected)
       - Pros: Native CSS, no runtime overhead, SSR friendly
       - Cons: Requires updating all color references
    2. Styled-components ThemeProvider
       - Pros: Tight React integration
       - Cons: Adds dependency, runtime CSS-in-JS overhead
    3. Tailwind dark: variant
       - Pros: Class-based, easy toggle
       - Cons: Requires Tailwind setup if not present

  Selected: Option 1 (CSS Custom Properties + Context API)
  Rationale: No new dependencies, best performance, works with existing CSS Modules
```

### FASE 2: Execution (sequential phases)

**Phase 1: theme-system workstream**

Agent receives the generated agent-handoff prompt (shown above) and executes:

```
Step 1 (Plan-and-Solve): Plan theme token structure
  - Define color tokens: bg-primary, bg-secondary, text-primary, text-secondary, etc.
  - Plan ThemeProvider: Context, localStorage, prefers-color-scheme listener
  - Plan FOUC prevention: data-theme attribute on <html>, blocking script

Step 2 (Few-Shot): Reference existing component patterns
  - Identified: components use CSS Modules with hardcoded hex colors
  - Pattern: functional components with named exports

Step 3 (Implementation): Write theme files
  - Created: src/theme/theme.ts (token definitions for light/dark)
  - Created: src/theme/ThemeProvider.tsx (context + provider + FOUC prevention)
  - Created: src/theme/useTheme.ts (hook with typed return)

Step 4 (Self-Refine): Review for edge cases
  - Added: prefers-color-scheme listener for live system changes
  - Added: SSR-safe check (typeof window !== 'undefined')
  - Fixed: FOUC prevention script runs before React hydration

Step 5 (Checklist): Verify deliverables
  - [PASS] Theme tokens defined for both modes
  - [PASS] ThemeProvider with toggle
  - [PASS] useTheme hook exported
  - [PASS] localStorage persistence
  - [PASS] System preference detection
  - [PASS] FOUC prevention
```

**Gate Check after Phase 1:**

```yaml
gate_check_phase_1:
  level_1_syntax: PASS (TypeScript compiles, no errors)
  level_2_local: PASS (score 0.92, above threshold 0.88)
  decision: PROCEED to Phase 2
  plan_status: "v1 remains valid, no evolution needed"
```

**Phase 2: component-migration workstream**

Agent continues with the same generated prompt structure for component-migration:

```
Step 1: Scan existing components for hardcoded colors
  - Found: Dashboard.tsx (5 color refs), Sidebar.tsx (8 color refs), Header.tsx (3 color refs)
  - Found: styles/dashboard.module.css, styles/sidebar.module.css

Step 2: Replace hardcoded colors with CSS custom properties
  - Replaced: all hex/rgb values with var(--color-*) references
  - Updated: CSS Modules to use theme tokens

Step 3: Add theme toggle button to Header
  - Added: ThemeToggle component in Header using useTheme hook
  - Styled: Toggle button with sun/moon icons using theme-aware colors

Step 4: Self-Refine
  - Verified: no hardcoded colors remain (grep confirms)
  - Fixed: one component used inline styles with hardcoded color
```

### FASE 3: verification-before-completion

```
Final Verification (Levels 1-3):

Level 1 (Syntax):
  [PASS] All TypeScript files compile
  [PASS] No parse errors
  [PASS] CSS custom properties syntax valid
  [PASS] All files exist and non-empty

Level 2 (Local):
  [PASS] Theme toggle unit test passes
  [PASS] localStorage persistence test passes
  [PASS] useTheme hook returns correct types
  [PASS] All deliverables present
  Score: 0.94

Level 3 (Global):
  [PASS] ThemeProvider wraps app correctly
  [PASS] All components consume theme tokens (no hardcoded colors)
  [PASS] Interface contract satisfied (useTheme returns correct shape)
  [PASS] No file ownership conflicts
  Score: 0.91

Aggregate: PASS (0.93 > 0.88 code threshold)
Verdict: READY TO DELIVER
```

---

## Quality Gates

```yaml
quality_gate_results:
  level_1_syntax:
    status: PASS
    checks:
      syntax_valid: PASS
      no_parse_errors: PASS
      format_correct: PASS
      files_exist: PASS
    cost: 2 tool calls

  level_2_local:
    status: PASS
    score: 0.94
    threshold: 0.88
    checks:
      unit_tests_pass: PASS (3/3 tests)
      deliverables_complete: PASS (all deliverables present)
      internal_consistency: PASS (no contradictions)
      interface_contract_output: PASS (useTheme exports match contract)
    cost: 5 tool calls

  level_3_global:
    status: PASS
    score: 0.91
    threshold: 0.85
    checks:
      integration_tests_pass: PASS (theme toggle + component rendering)
      no_file_conflicts: PASS (workstreams have distinct file ownership)
      interface_contracts_met: PASS (ThemeProvider/useTheme contract satisfied)
      dependency_graph_valid: PASS (theme-system -> component-migration executed in order)
    cost: 5 tool calls

  level_4_semantic: SKIPPED (auto_level_policy: complexity_score < 6 -> max level 3)

  bloom_rubric_check:
    bloom_level: 3 (Apply)
    rubric: execution_validation
    scores:
      pass_rate: 1.0 (all tests pass)
      edge_cases_handled: 0.85 (FOUC, SSR, system pref changes handled)
      correct_approach: 1.0 (CSS custom properties is correct approach)
      failed_cases_identified: 1.0 (no failures)
    aggregate: 0.96
    threshold: 0.90
    status: PASS

  aggregate:
    passed: true
    total_cost: 12 tool calls
```

---

## Plan Evolution

In this example, the plan did NOT evolve because all quality gates passed on the first attempt.

```yaml
plan_evolution:
  - version: "v1"
    created_at: "Step 9"
    changes: "Initial plan with 2 sequential workstreams"
    status: "FINAL (all gates passed, no evolution needed)"

  # Example of what v2 WOULD look like if a gate had failed:
  # - version: "v2"
  #   created_at: "Gate check after Phase 2"
  #   trigger: "quality_gate_failed: hardcoded colors found in 2 additional components"
  #   changes:
  #     - "Added 2 more files to component-migration file_ownership"
  #     - "Increased budget by 4 tool calls"
  #     - "Added checklist: grep for hex/rgb values across entire src/"
  #   cost_of_evolution: "~6 additional tool calls"
```

---

## Cost Summary

| Phase | Tool Calls | Notes |
|-------|-----------|-------|
| Step 0: Triage | 3 | Classification + complexity assessment |
| Step 0.5: Discovery | 1 | Skill/agent scan |
| Step 0.7: Registry | 1 | Skill + agent lookup |
| Steps 1-5: Analysis | 2 | FULL_LIGHT is lightweight |
| Step 9: ExecutionPlan | 1 | Plan generation |
| Step 9.5: Prompts | 1 | Prompt generation from templates |
| Fase 1: brainstorming | 3 | Approach exploration |
| Fase 2: theme-system | 10 | Implementation phase 1 |
| Fase 2: component-migration | 8 | Implementation phase 2 |
| Fase 3: verification | 12 | Level 1-3 gates + bloom rubric |
| **Total** | **~42** | Within budget (estimated 37 + 5 reserve) |

---

## Key Takeaways for FULL_LIGHT Mode

1. **Balanced overhead**: Analysis (Steps 1-5, 9) adds ~8 tool calls of planning overhead, which pays off by structuring the execution into clear phases.
2. **Simplified ExecutionPlan**: Steps 6-8 and 10-12 are skipped. The plan includes workstreams, contracts, and quality gates but not full hyperparameter tuning or convergence monitoring.
3. **Technique mapper quick-path**: For standard archetypes like `L-Builder-Frontend`, the technique pipeline comes from pre-computed defaults rather than running the full 4-phase technique selector.
4. **Sequential execution**: Even though two workstreams exist, they have a dependency (theme-system -> component-migration), so execution is sequential, not parallel.
5. **Quality gates up to level 3**: Auto-level policy allows Global-level checks (level 3) for moderate tasks, catching integration issues between workstreams.
6. **Plan evolution available**: Unlike TRIAGE mode, the plan CAN evolve if gates fail -- but in this example it did not need to.
7. **Supervisor optional**: HRM does not remain active as supervisor for FULL_LIGHT with low uncertainty.
