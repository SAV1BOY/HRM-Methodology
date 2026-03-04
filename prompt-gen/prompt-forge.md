# Universal Prompt Forge

> Every dispatch point in the HRM system passes through the Prompt Forge before execution. The Forge applies prompt engineering techniques proportionally -- from a 2-technique micro-injection for TRIAGE dispatches to a full 7-technique scored pipeline for FULL-mode workstreams.

---

## Motivation

Before the Forge, only workstream-level agents in FULL mode (Step 9.5) received technique-enhanced prompts. All other dispatch points -- TRIAGE agents, swarm members, team members, squad chiefs, gate reviewers, feedback loops, escalation reports -- received prompts WITHOUT technique application. The Forge closes this gap universally.

---

## Three-Tier System

### MICRO (1-2 techniques, zero extra reads)

**Applied**: ALWAYS, including TRIAGE mode.

**Source**: `prompt-gen/technique-index.yaml` (micro_defaults section or dispatch-profile-specific techniques).

**Cost**: Zero additional file reads. Techniques injected from pre-loaded index.

**Use for**: Mini-tasks, feedback loops, escalation reports, TRIAGE dispatches, gate reviewers (level 1-2).

### QUICK (3-5 techniques, technique-mapper lookup)

**Applied**: FULL_LIGHT and FULL modes.

**Source**: `prompt-gen/technique-mapper.md` (pre-computed pipelines by archetype + domain overrides).

**Cost**: No additional file reads beyond bootstrap. Technique-mapper is already loaded in FULL_LIGHT+.

**Use for**: Subtasks, swarm members, team members, gate reviewers (level 3-4), squad chiefs, team leads.

### FULL (3-7 techniques, 4-phase scoring)

**Applied**: FULL mode only.

**Source**: `hrm-agent/technique-selector.md` (4-phase scoring) + `hrm-agent/pipeline-builder.md` (dependency resolution).

**Cost**: Full prompt generation pipeline from `prompt-gen/prompt-generator.md`.

**Use for**: Top-level workstream agents (current Step 9.5 behavior).

---

## Scaling Matrix

| HRM Mode | Task (top-level) | Subtask | Mini-task |
|----------|-----------------|---------|-----------|
| TRIAGE | MICRO (1-2) | N/A | N/A |
| FULL_LIGHT | QUICK (3-5) | MICRO (1-2) | MICRO (1-2) |
| FULL | FULL (3-7) | QUICK (3-5) | MICRO (1-2) |

---

## Dispatch Type Profiles

| Dispatch Type | Default Tier | Technique Affinity | Template |
|--------------|-------------|-------------------|----------|
| triage-agent | MICRO | role-prompting + zero-shot-cot | agent-handoff |
| workstream-agent | mode-dependent | archetype-mapped | agent-handoff |
| swarm-member | QUICK | archetype-mapped | agent-handoff |
| team-member | QUICK | archetype-mapped | agent-handoff |
| team-lead | QUICK + overlay | planner-worker-solver + checklist | team-kickoff |
| squad-chief | QUICK + overlay | step-back + plan-and-solve + checklist | squad-brief |
| gate-reviewer | MICRO (QUICK if level >= 3) | chain-of-verification + checklist | quality-gate-review |
| feedback-target | MICRO | self-refine + checklist | feedback-loop |
| escalation-report | MICRO | output-format | escalation-report |

Full profile definitions: `prompt-gen/dispatch-profiles.yaml`

---

## Core Algorithm: `forge(dispatch_context)`

Every entity passes through this function before being dispatched.

### Input: dispatch_context

```yaml
dispatch_context:
  hrm_mode: TRIAGE | FULL_LIGHT | FULL
  dispatch_type: triage-agent | workstream-agent | swarm-member | team-member | team-lead | squad-chief | gate-reviewer | feedback-target | escalation-report
  granularity: task | subtask | mini_task
  archetype: L-Architect | L-Builder-Frontend | L-Builder-Backend | ...  # if applicable
  domain: code | security | design | documentation | ...
  gate_level: 1-4  # only for gate-reviewer type
  task_profile: { ... }  # only for FULL tier
```

### Algorithm

```
FUNCTION forge(dispatch_context):

  // Step 1: Resolve tier
  tier = resolve_tier(dispatch_context)

  // Step 2: Select techniques based on tier
  IF tier == MICRO:
    profile = dispatch_profiles[dispatch_context.dispatch_type]
    IF profile.micro_techniques exists:
      techniques = profile.micro_techniques
    ELSE:
      techniques = technique_index.micro_defaults[classify(dispatch_context)]
    // Cap at 2 techniques
    techniques = techniques[:2]

  ELIF tier == QUICK:
    // Look up pre-computed pipeline from technique-mapper
    techniques = technique_mapper.get_pipeline(dispatch_context.archetype, dispatch_context.domain)
    // Apply overlays if dispatch type has them
    profile = dispatch_profiles[dispatch_context.dispatch_type]
    IF profile.technique_overlays:
      techniques += profile.technique_overlays.always_add
    // Cap at 5 techniques
    techniques = techniques[:5]

  ELIF tier == FULL:
    // Run full 4-phase scoring from technique-selector
    task_profile = build_task_profile(dispatch_context)
    techniques = technique_selector.score_and_select(task_profile)
    // Chain via pipeline-builder
    techniques = pipeline_builder.chain(techniques)
    // Cap at 7 techniques
    techniques = techniques[:7]

  // Step 3: Select template
  template = dispatch_profiles[dispatch_context.dispatch_type].template

  // Step 4: Generate technique steps text
  technique_steps = format_technique_steps(techniques)

  // Step 5: Inject into template
  prompt = inject_into_template(template, technique_steps, dispatch_context)

  // Step 6: Validate (QUICK and FULL only)
  IF tier >= QUICK:
    validation = validate_prompt(prompt)
    IF validation.failed:
      // Adjust: swap expensive technique for cheaper alternative
      techniques = adjust_techniques(techniques, validation.issues)
      prompt = inject_into_template(template, format_technique_steps(techniques), dispatch_context)

  // Step 7: Return
  RETURN ForgeOutput(
    prompt: prompt,
    techniques: techniques,
    tier: tier,
    template: template,
    estimated_tokens: estimate_token_cost(techniques)
  )
```

---

## Tier Resolution Logic

```
FUNCTION resolve_tier(ctx):

  // 1. Check dispatch-profile override
  profile = dispatch_profiles[ctx.dispatch_type]
  IF profile.default_tier == "MICRO" AND profile.tier_ceiling == "MICRO":
    RETURN MICRO  // feedback-target, escalation-report: always MICRO

  // 2. Check tier upgrade conditions
  IF ctx.dispatch_type == "gate-reviewer" AND ctx.gate_level >= 3:
    RETURN QUICK  // global/semantic gates get QUICK

  // 3. Mode-dependent dispatch types
  IF profile.default_tier == "MODE_DEPENDENT":
    RETURN profile.tier_map[ctx.hrm_mode]

  // 4. Apply scaling matrix (mode x granularity)
  matrix = {
    TRIAGE:     { task: MICRO,  subtask: MICRO, mini_task: MICRO },
    FULL_LIGHT: { task: QUICK,  subtask: MICRO, mini_task: MICRO },
    FULL:       { task: FULL,   subtask: QUICK, mini_task: MICRO }
  }
  resolved = matrix[ctx.hrm_mode][ctx.granularity]

  // 5. Apply ceiling from profile
  IF profile.tier_ceiling AND tier_rank(resolved) > tier_rank(profile.tier_ceiling):
    resolved = profile.tier_ceiling

  RETURN resolved
```

---

## MICRO Tier: Index Lookup

Zero extra LLM calls. Zero file reads beyond bootstrap.

```
FUNCTION micro_select(dispatch_type, task_classification):
  profile = dispatch_profiles[dispatch_type]

  IF profile.micro_techniques:
    // Profile specifies exact techniques (gate-reviewer, feedback-target, etc.)
    RETURN profile.micro_techniques

  // Fall back to universal defaults from technique-index.yaml
  category = classify_micro(task_classification)  // -> code_fix, code_build, review, document, creative
  RETURN technique_index.micro_defaults[category]
```

### Micro Classification

| Task Signals | Category | Default Techniques |
|-------------|----------|-------------------|
| TIPO=FIX, ARTEFATO=CODIGO | code_fix | role-prompting, zero-shot-cot |
| TIPO=BUILD, ARTEFATO=CODIGO | code_build | role-prompting, zero-shot-cot |
| TIPO=REVIEW | review | role-prompting, checklist-prompting |
| ARTEFATO=DOCUMENTO | document | role-prompting, output-format |
| TIPO=DESIGN or creative context | creative | role-prompting, zero-shot-cot |
| All other | universal | role-prompting, zero-shot-cot |

---

## QUICK Tier: Technique-Mapper Delegation

Delegates to `prompt-gen/technique-mapper.md` for pre-computed archetype pipelines.

```
FUNCTION quick_select(archetype, domain, dispatch_type):
  // 1. Get default pipeline for archetype
  pipeline = technique_mapper.default_pipelines[archetype]

  // 2. Apply domain overrides
  IF domain IN pipeline.domain_overrides:
    pipeline.techniques += pipeline.domain_overrides[domain].add

  // 3. Apply dispatch-type overlays
  profile = dispatch_profiles[dispatch_type]
  IF profile.technique_overlays:
    FOR tech IN profile.technique_overlays.always_add:
      IF tech NOT IN pipeline.techniques:
        pipeline.techniques.append(tech)

  // 4. Cap at 5 techniques
  RETURN pipeline.techniques[:5]
```

---

## FULL Tier: Technique-Selector + Pipeline-Builder

Delegates to the existing Step 9.5 system (unchanged behavior):

1. **Phase 1**: Extract task_profile from dispatch_context
2. **Phase 2**: Run `hrm-agent/technique-selector.md` 4-phase scoring
3. **Phase 3**: Run `hrm-agent/pipeline-builder.md` for dependency resolution
4. **Phase 4**: Enrich with project context
5. **Phase 5**: Validate against prompt-quality checklist

This is exactly what Step 9.5 does today for workstream-level agents. The Forge simply makes this the FULL tier option within a unified system.

---

## Template Injection Format

Techniques are injected into the `{technique_steps}` placeholder in each template.

### Format for MICRO (1-2 techniques)

```
Follow this approach:
1. **{technique_1_name}**: {technique_1_instruction}
2. **{technique_2_name}**: {technique_2_instruction}
```

### Format for QUICK (3-5 techniques)

```
Follow this technique pipeline:
1. **{technique_1_name}**: {technique_1_instruction}
   Expected output: {technique_1_output}
2. **{technique_2_name}**: {technique_2_instruction}
   Expected output: {technique_2_output}
...
```

### Format for FULL (3-7 techniques)

Full pipeline specification from pipeline-builder, including:
- Technique steps with dependencies
- Variable bindings between steps
- Error handling and fallback instructions
- Expected output format per step

---

## Concrete Examples

### Example 1: TRIAGE dispatch (MICRO)

```yaml
dispatch_context:
  hrm_mode: TRIAGE
  dispatch_type: triage-agent
  granularity: task
  domain: code
forge_output:
  tier: MICRO
  techniques: [role-prompting, zero-shot-cot]
  template: agent-handoff
  injected_text: |
    Follow this approach:
    1. **Role**: You are an expert developer specializing in this domain.
    2. **Reasoning**: Think through the problem step by step before implementing.
```

### Example 2: Swarm member in FULL mode (QUICK)

```yaml
dispatch_context:
  hrm_mode: FULL
  dispatch_type: swarm-member
  granularity: subtask
  archetype: L-Builder-Frontend
  domain: react
forge_output:
  tier: QUICK
  techniques: [role-prompting, plan-and-solve, few-shot, self-refine, checklist-prompting]
  template: agent-handoff
  injected_text: |
    Follow this technique pipeline:
    1. **Role**: You are an expert frontend developer specializing in React.
       Expected output: domain-specific perspective throughout
    2. **Plan-and-Solve**: Plan the component structure before coding.
       Expected output: component tree with props and state
    3. **Few-Shot**: Follow existing patterns from the codebase.
       Expected output: consistent code style
    4. **Self-Refine**: Review your output and iterate on quality.
       Expected output: polished implementation
    5. **Checklist**: Verify accessibility, responsiveness, and performance.
       Expected output: all checks passed
```

### Example 3: Gate reviewer upgrade (MICRO -> QUICK)

```yaml
dispatch_context:
  hrm_mode: FULL
  dispatch_type: gate-reviewer
  granularity: task
  gate_level: 3  # global level
  domain: code
forge_output:
  tier: QUICK  # upgraded from MICRO because gate_level >= 3
  techniques: [chain-of-verification, contrastive-cot, checklist-prompting, output-format]
  template: quality-gate-review
  injected_text: |
    Follow this technique pipeline:
    1. **Chain-of-Verification**: Generate verification questions, answer independently, reconcile.
       Expected output: verified claims with evidence
    2. **Contrastive CoT**: Compare correct vs incorrect patterns in the deliverables.
       Expected output: identified deviations from expected behavior
    3. **Checklist**: Systematically verify all quality criteria.
       Expected output: scored checklist
    4. **Output Format**: Structure your findings in the required YAML format.
       Expected output: verification_result YAML block
```

### Example 4: Squad chief (QUICK + overlay)

```yaml
dispatch_context:
  hrm_mode: FULL
  dispatch_type: squad-chief
  granularity: task
  domain: documentation
forge_output:
  tier: QUICK
  techniques: [step-back-prompting, plan-and-solve, checklist-prompting]
  template: squad-brief
  injected_text: |
    Follow this technique pipeline:
    1. **Step-Back**: Abstract the requirements to identify core principles first.
       Expected output: high-level strategy before diving into details
    2. **Plan-and-Solve**: Create a structured plan for your squad's deliverables.
       Expected output: phased execution plan with milestones
    3. **Checklist**: Verify completeness against the brief requirements.
       Expected output: all acceptance criteria addressed
```

### Example 5: Feedback target (MICRO, always)

```yaml
dispatch_context:
  hrm_mode: FULL
  dispatch_type: feedback-target
  granularity: subtask
forge_output:
  tier: MICRO
  techniques: [self-refine, checklist-prompting]
  template: feedback-loop
  injected_text: |
    Follow this approach:
    1. **Self-Refine**: Review your previous output against the feedback, then revise.
    2. **Checklist**: Verify all failed checks now pass before resubmitting.
```

---

## Budget Tracking Integration

The Forge tracks technique costs as part of the overall budget:

```yaml
forge_budget:
  micro_cost: 0  # zero extra reads or calls
  quick_cost: 0  # technique-mapper already loaded in bootstrap
  full_cost: variable  # depends on technique-selector scoring depth
```

The `estimated_tokens` in ForgeOutput allows the HRM to account for technique instructions in the prompt budget. If the combined forge cost exceeds the workstream budget, the Forge downgrades to a cheaper tier automatically.

---

## Integration Points

| Component | How Forge Uses It |
|-----------|------------------|
| `technique-index.yaml` | MICRO tier: technique lookup (loaded in TRIAGE+ bootstrap) |
| `dispatch-profiles.yaml` | All tiers: profile lookup for dispatch type (loaded in TRIAGE+ bootstrap) |
| `technique-mapper.md` | QUICK tier: pre-computed archetype pipelines (loaded in FULL_LIGHT+ bootstrap) |
| `technique-selector.md` | FULL tier: 4-phase technique scoring |
| `pipeline-builder.md` | FULL tier: dependency resolution and chaining |
| `prompt-generator.md` | FULL tier: orchestrates the 5-phase prompt generation pipeline |
| `prompt-templates/*.yaml` | All tiers: template selection per dispatch type |
| `config.yaml` | Domain thresholds for validation |

---

## Backward Compatibility

The Forge is a superset of the existing Step 9.5 behavior:

- **FULL mode, workstream-agent, task granularity** → FULL tier → identical to current Step 9.5 pipeline
- **All other dispatch points** → NEW behavior (MICRO or QUICK tier applied where none existed before)

No existing behavior changes. The Forge only adds technique application where it was previously absent.
