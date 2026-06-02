# Movement Squad Bridge

> Integration bridge between HRM Architect and Movement Squad. Defines when to delegate, how to map swarm workstreams to movement/culture tasks, brief format, and quality gate integration.

---

## Overview

The Movement Squad Bridge enables the HRM to seamlessly delegate movement marketing, culture building, and community activation workstreams to the Movement Squad instead of using generic agents. This produces higher quality cultural strategies by leveraging the squad's 7-agent roster covering movement marketing, culture building, community activation, manifestos, memetics, and identity creation.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Movement Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == BUILD AND domain is community/culture | "Design a brand movement" |
| Keywords: "movimento", "comunidade", "cultura de marca" | "Build community-driven brand culture" |
| Keywords: "ativacao", "manifesto", "tribo" | "Write brand manifesto for community" |
| Keywords: "movimento social", "community building", "cultural strategy" | "Create cultural strategy for launch" |
| Keywords: "memetics", "rituais de marca", "identity creation" | "Design brand rituals and identity markers" |
| Keywords: "movement design", "cause marketing", "cultural tension" | "Identify and activate cultural tension" |
| Workstream archetype includes culture/community + identity | Build task with movement workstream |

### Manual Override

User can explicitly request Movement Squad: "Use the Movement Squad for this" or "Delegate to movement team".

### When NOT to Delegate

- Standard community management without movement angle (too tactical, use operational tools)
- Brand guidelines without cultural movement strategy (use Brand Squad)
- Social media posting and scheduling (use Copy Squad)
- PR campaigns without cultural movement component (use internal-comms)

---

## Swarm-to-Movement Mapping

When a multi-workstream task includes a movement/culture component:

```yaml
# Example: Brand launch with cultural movement
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "movement-design"
    archetype: L-MovementDesigner  # detected as culture domain
    execution: squad_delegation  # -> Movement Squad
  - name: "brand-narrative"
    archetype: L-Storyteller
    execution: squad_delegation  # -> Storytelling Squad

interface_contracts:
  - between: ["movement-design", "brand-narrative"]
    contract: "Cultural tension, cause, and identity markers delivered before narrative creation"
    owner: "movement-design"
    delivery_checkpoint: "Before storytelling narrative phase"
  - between: ["movement-design", "frontend"]
    contract: "Community identity elements, rituals, and visual language delivered for UI integration"
    owner: "movement-design"
    delivery_checkpoint: "Before frontend brand experience build"
```

---

## Brief Format for Movement Squad

### Minimum Required Fields

```yaml
movement_brief:
  objective: "What the movement needs to achieve (specific, measurable)"
  scope:
    type: "movement_design|manifesto|community_activation|cultural_strategy|identity_creation|impact_measurement"
    deliverables: "Expected output format and depth"
    timeline: "Implementation timeline or campaign period"
  movement_context:
    cause: "The core cause or belief the movement rallies around"
    cultural_tension: "The societal or industry tension being addressed"
    existing_community: "Current community size, engagement level, platforms"
  audience:
    believers: "Already-converted supporters and their characteristics"
    skeptics: "Resistant audience and their objections"
    potential_converts: "Reachable audience that could be activated"
  constraints:
    - "brand alignment requirements"
    - "cultural sensitivity boundaries"
    - "ethical guidelines"
```

### Optional Enrichment (from HRM context)

```yaml
movement_enrichment:
  frameworks_to_use:
    - "movement-lifecycle"       # from methodology
    - "memetic-engineering"      # from techniques
  cultural_references:
    - "successful-movements"     # case studies to learn from
    - "counter-narratives"       # opposing forces to address
  community_data: "Existing community analytics and engagement patterns"
  identity_assets: ["existing brand assets, symbols, language"]
```

---

## Quality Gate Integration

### Movement Squad Internal Gates

The Movement Squad chief runs internal quality checks before delivering:

1. **Cultural authenticity**: Does the movement feel genuine and not manufactured?
2. **Community resonance**: Will the target audience connect with and share this?
3. **Movement sustainability**: Can this movement sustain itself beyond initial launch?
4. **Message potency**: Is the core message memorable and shareable?
5. **Ethical alignment**: Does the movement respect cultural boundaries and avoid harm?

### HRM External Gates (after delivery)

The HRM verifies Movement Squad output using these checks:

| Gate Level | Checks for Movement |
|-----------|---------------------|
| Level 2 (Local) | Deliverables exist, format matches, all components covered |
| Level 4 (Semantic) | Cultural impact potential, community fit, sustainability assessment |

### Threshold

Movement quality threshold: **0.85** (design domain threshold, as creative and cultural work).

---

## Feedback Protocol

### HRM -> Movement Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: MOVEMENT REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.85

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
========================================
```

### Movement Squad Chief -> HRM

Revision delivery:

```
=== MOVEMENT REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
==================================
```
