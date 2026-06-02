# Design Squad Bridge

> Integration bridge between HRM Architect and Design Squad. Defines when to delegate, how to map swarm workstreams to design tasks, brief format, and quality gate integration.

---

## Overview

The Design Squad Bridge enables the HRM to seamlessly delegate UX/UI and design system workstreams to the Design Squad instead of using generic agents. This produces higher quality design deliverables by leveraging the squad's 8-agent roster covering UX research, UI design, design systems, design ops, accessibility, user research, and prototyping.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Design Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO in [BUILD, DESIGN] AND domain is UX/UI | "Design the onboarding flow" |
| Keywords: "UI", "UX", "user interface", "user experience" | "Improve the checkout UX" |
| Keywords: "design system", "componente", "component library" | "Build a design system" |
| Keywords: "prototipo", "prototype", "wireframe", "mockup" | "Create wireframes for the dashboard" |
| Keywords: "acessibilidade", "accessibility", "a11y", "WCAG" | "Audit accessibility compliance" |
| Keywords: "user research", "pesquisa de usuario", "usability test" | "Conduct user research for feature X" |
| Keywords: "design tokens", "handoff", "design-to-dev" | "Set up design token pipeline" |
| Workstream archetype includes design/UX + multi-component | Build task with design workstream |

### Manual Override

User can explicitly request Design Squad: "Use the Design Squad for this" or "Delegate to design team".

### When NOT to Delegate

- Pure brand strategy without UI deliverables (use Brand Squad)
- Marketing copy without design component (use Copy Squad)
- Algorithmic art or generative visuals (use algorithmic-art skill)
- Simple CSS changes or minor style tweaks (use frontend-design skill)
- One-off icon or color lookup (too small for squad overhead)

---

## Swarm-to-Design Mapping

When a multi-workstream task includes a design component:

```yaml
# Example: Building a SaaS dashboard
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "ux-design"
    archetype: L-Designer  # detected as design domain
    execution: squad_delegation  # -> Design Squad
  - name: "backend-api"
    archetype: L-Builder-Backend
    execution: swarm_agent

interface_contracts:
  - between: ["ux-design", "frontend"]
    contract: "Design delivered as Figma specs + design tokens + component API definitions"
    owner: "ux-design"
    delivery_checkpoint: "Before frontend component implementation"
  - between: ["ux-design", "backend-api"]
    contract: "User flows and data requirements documented before API design"
    owner: "ux-design"
    delivery_checkpoint: "Before API endpoint definition"
```

---

## Brief Format for Design Squad

### Minimum Required Fields

```yaml
design_brief:
  objective: "What the design deliverable needs to achieve (specific, measurable)"
  scope:
    type: "ux_research|ui_design|design_system|prototype|audit|handoff"
    deliverables: ["wireframes", "high-fidelity mockups", "design tokens", "component specs"]
  user_context:
    personas: ["primary user persona descriptions"]
    journey_stage: "Where in the user journey this design applies"
    accessibility_needs: ["WCAG level", "specific assistive technology support"]
  design_context:
    existing_design_system: "Current design system state (if any)"
    platform: "web|mobile|desktop|responsive"
    breakpoints: ["mobile", "tablet", "desktop"]
  constraints:
    - "existing brand guidelines to follow"
    - "technical limitations of target platform"
    - "timeline and review cycles"
```

### Optional Enrichment (from HRM context)

```yaml
design_enrichment:
  frameworks_to_use:
    - "atomic-design"         # from methodology
    - "double-diamond"        # from reference/design-process/
  tools:
    - "Figma"                 # design tool
    - "Storybook"             # component documentation
  accessibility_standard: "WCAG 2.1 AA"
  interaction_patterns: ["relevant interaction pattern references"]
  competitive_references: ["competitor design benchmarks"]
```

---

## Quality Gate Integration

### Design Squad Internal Gates

The Design Squad chief runs internal quality checks before delivering:

1. **Usability heuristics**: Does the design pass Nielsen's 10 heuristics?
2. **Accessibility compliance**: WCAG level met for all components?
3. **Design system consistency**: All components follow established patterns?
4. **Responsive behavior**: Design works across all specified breakpoints?
5. **Handoff readiness**: Specs, tokens, and assets ready for development?

### HRM External Gates (after delivery)

The HRM verifies Design Squad output using these checks:

| Gate Level | Checks for Design |
|-----------|------------------|
| Level 2 (Local) | Deliverables exist, format matches, all requested screens/components present |
| Level 4 (Semantic) | User needs addressed, accessibility met, design system consistency, responsive behavior verified |

### Threshold

Design quality threshold: **0.85** (design domain threshold, requiring creative and usability quality bar).

---

## Feedback Protocol

### HRM -> Design Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: DESIGN REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.85

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
======================================
```

### Design Squad Chief -> HRM

Revision delivery:

```
=== DESIGN REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
=================================
```
