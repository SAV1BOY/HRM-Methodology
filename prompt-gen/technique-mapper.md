# Technique Mapper

> Quick-path mapping from HRM archetypes to default technique pipelines. Bypasses full 4-phase scoring for common cases.

---

## Overview

The Technique Mapper provides pre-computed technique pipelines for standard archetype + domain combinations. Use this as a fast path when the workstream fits a known pattern. Fall back to full `technique-selector.md` scoring when the combination is unusual.

---

## Default Pipelines by Archetype

### L-Architect (Design/Planning)

```yaml
default_pipeline:
  techniques:
    - step-back-prompting    # Abstract first, then detail
    - chain-of-thought       # Structured reasoning
    - tree-of-thoughts       # Explore alternatives (if complexity >= 5)
    - checklist-prompting    # Verify completeness
  domain_overrides:
    security:
      add: [chain-of-verification]
      threshold: 0.95
    infrastructure:
      add: [plan-and-solve]
      threshold: 0.90
```

### L-Builder-Frontend (Frontend Development)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert frontend developer persona
    - plan-and-solve          # Plan component structure
    - few-shot                # Show existing patterns from codebase
    - self-refine             # Iterate on quality
    - checklist-prompting     # Verify accessibility, responsiveness
  domain_overrides:
    react:
      add: [output-format]   # JSX/TSX format control
    design:
      add: [analogical-prompting]  # Reference design system patterns
```

### L-Builder-Backend (Backend Development)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert backend developer persona
    - plan-and-solve          # Plan API/service structure
    - program-of-thoughts     # Code-based reasoning for algorithms
    - self-refine             # Iterate on implementation
    - checklist-prompting     # Verify security, performance
  domain_overrides:
    database:
      add: [chain-of-thought]  # Complex query reasoning
    api:
      add: [output-format]     # Schema validation
```

### L-Builder-Test (Testing)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert QA engineer persona
    - least-to-most           # Simple tests first, complex later
    - chain-of-thought        # Reason about edge cases
    - checklist-prompting     # Test coverage checklist
  domain_overrides:
    security:
      add: [chain-of-verification]
      threshold: 0.95
```

### L-Builder-Infra (Infrastructure)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert DevOps persona
    - plan-and-solve          # Plan infrastructure layout
    - chain-of-thought        # Reason about dependencies
    - checklist-prompting     # Security, reliability checks
  domain_overrides:
    kubernetes:
      add: [output-format]    # YAML format control
    terraform:
      add: [few-shot]         # Show existing modules
```

### L-Critic (Code Review / Quality)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert reviewer persona
    - chain-of-verification   # Systematic verification
    - contrastive-cot         # Show correct vs incorrect patterns
    - checklist-prompting     # Review checklist
  domain_overrides:
    security:
      add: [step-back-prompting]  # Abstract security principles first
      threshold: 0.95
```

### L-Researcher (Research / Exploration)

```yaml
default_pipeline:
  techniques:
    - step-back-prompting     # Abstract the question first
    - self-ask                # Decompose into sub-questions
    - chain-of-thought        # Reason through findings
    - grounding-via-sources   # Cite evidence
    - chain-of-verification   # Verify conclusions
  domain_overrides:
    academic:
      add: [few-shot]         # Show citation format
```

### L-Builder-Data (Database / Data Engineering)

```yaml
default_pipeline:
  techniques:
    - role-prompting          # Expert data engineer persona
    - plan-and-solve          # Plan schema/pipeline
    - program-of-thoughts     # SQL/query reasoning
    - output-format           # Schema format control
    - checklist-prompting     # Data integrity checks
```

### L-Optimizer (Performance Optimization)

```yaml
default_pipeline:
  techniques:
    - step-back-prompting     # Identify bottleneck category first
    - chain-of-thought        # Analyze performance characteristics
    - analogical-prompting    # Reference similar optimization patterns
    - self-refine             # Iterate on optimization
    - checklist-prompting     # Verify no regressions
```

---

## When to Use Full Scoring Instead

Use the full `technique-selector.md` 4-phase scoring when:

1. **Hybrid archetype**: Workstream combines 2+ archetypes (e.g., L-Builder-Frontend + L-Architect)
2. **Unusual domain**: Domain doesn't match any override above
3. **Tight budget**: Need to minimize technique count due to budget constraints
4. **High uncertainty**: Uncertainty score >= 7 in complexity assessment
5. **Novel task**: No clear precedent in existing pipelines
6. **Squad delegation**: Chief prompt needs domain-specific technique selection

---

## Quick Lookup Table

| Archetype | Core Techniques (always) | Budget (min) |
|-----------|------------------------|-------------|
| L-Architect | step-back, CoT, checklist | 8 |
| L-Builder-Frontend | role, plan-and-solve, few-shot, self-refine, checklist | 12 |
| L-Builder-Backend | role, plan-and-solve, PoT, self-refine, checklist | 12 |
| L-Builder-Test | role, least-to-most, CoT, checklist | 8 |
| L-Builder-Infra | role, plan-and-solve, CoT, checklist | 8 |
| L-Critic | role, CoVe, contrastive-CoT, checklist | 8 |
| L-Researcher | step-back, self-ask, CoT, grounding, CoVe | 12 |
| L-Builder-Data | role, plan-and-solve, PoT, output-format, checklist | 10 |
| L-Optimizer | step-back, CoT, analogical, self-refine, checklist | 10 |

---

## Dispatch Type Extensions (Prompt Forge)

When the Prompt Forge requests QUICK-tier technique selection for non-archetype dispatch types, use these extensions instead of the archetype-based pipelines above:

### Gate Reviewer (dispatch_type: gate-reviewer, tier: QUICK)

```yaml
pipeline:
  techniques:
    - chain-of-verification   # Systematic verification protocol
    - contrastive-cot          # Compare correct vs incorrect patterns
    - checklist-prompting      # Structured check execution
    - output-format            # YAML verification_result format
  notes: "Activated when gate_level >= 3 (global/semantic gates)"
```

### Team Lead (dispatch_type: team-lead, tier: QUICK)

```yaml
pipeline:
  techniques:
    - role-prompting           # Team coordination persona
    - planner-worker-solver    # Decompose and delegate to teammates
    - plan-and-solve           # Structure the team's execution plan
    - checklist-prompting      # Verify completeness of delegation
  notes: "Overlay techniques added to base archetype pipeline for coordination"
```

### Squad Chief (dispatch_type: squad-chief, tier: QUICK)

```yaml
pipeline:
  techniques:
    - step-back-prompting      # Abstract requirements to core principles
    - plan-and-solve           # Create phased execution plan
    - checklist-prompting      # Verify brief completeness
  notes: "Strategic overlay for squad-level orchestration"
```

### Feedback Target (dispatch_type: feedback-target, tier: MICRO)

```yaml
pipeline:
  techniques:
    - self-refine              # Review and revise based on feedback
    - checklist-prompting      # Verify failed checks now pass
  notes: "Always MICRO tier, even in FULL mode — feedback is targeted, not exploratory"
```

---

## Forge Integration

The Technique Mapper serves as the primary engine for the **QUICK tier** in the Universal Prompt Forge:

| Forge Tier | Source | This File's Role |
|-----------|--------|-----------------|
| MICRO | technique-index.yaml | Not used (index handles directly) |
| QUICK | **technique-mapper.md** | **Primary: pre-computed pipelines + dispatch extensions** |
| FULL | technique-selector.md + pipeline-builder.md | Not used (full scoring handles) |

When the Forge calls `quick_select(archetype, domain, dispatch_type)`:
1. Look up archetype pipeline from Default Pipelines above
2. Apply domain overrides if applicable
3. Apply dispatch type overlays from Dispatch Type Extensions
4. Cap at 5 techniques
5. Return ordered pipeline
