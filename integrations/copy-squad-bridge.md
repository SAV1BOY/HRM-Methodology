# Copy Squad Bridge

> Integration bridge between HRM Architect and Squad de Copy. Defines when to delegate, how to map swarm workstreams to copy tasks, brief format, and quality gate integration.

---

## Overview

The Copy Squad Bridge enables the HRM to seamlessly delegate copywriting workstreams to the Squad de Copy instead of using generic agents. This produces higher quality copy by leveraging the squad's 138-file reference library of psychology, frameworks, and swipe files.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Copy Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == WRITE AND domain is copywriting | "Write sales page copy" |
| Keywords: "copy", "headline", "hook", "sales page", "email sequence" | "Create email sequence for onboarding" |
| Keywords: "persuasion", "conversion copy", "CTA" | "Optimize landing page for conversion" |
| Keywords: "swipe file", "copywriting framework" | "Use PAS framework for ad copy" |
| Workstream archetype includes copy/writing + persuasion | Build task with copy workstream |

### Manual Override

User can explicitly request Copy Squad: "Use the Copy Squad for this" or "Delegate to copy team".

### When NOT to Delegate

- Technical documentation (use doc-coauthoring)
- Internal communications without persuasion (use internal-comms)
- UI microcopy under 50 words (too small for squad overhead)
- Pure editing/proofreading (use humanizer)

---

## Swarm-to-Copy Mapping

When a multi-workstream task includes a copywriting component:

```yaml
# Example: Building a landing page
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "sales-copy"
    archetype: L-Writer  # detected as copy domain
    execution: squad_delegation  # -> Copy Squad
  - name: "backend-api"
    archetype: L-Builder-Backend
    execution: swarm_agent

interface_contracts:
  - between: ["sales-copy", "frontend"]
    contract: "Copy delivered as structured markdown with sections: hero, benefits, social_proof, cta"
    owner: "sales-copy"
    delivery_checkpoint: "Before frontend integration phase"
```

---

## Brief Format for Copy Squad

### Minimum Required Fields

```yaml
copy_brief:
  objective: "What the copy needs to achieve (specific, measurable)"
  audience:
    primary: "Target audience description"
    awareness_level: "unaware|problem_aware|solution_aware|product_aware|most_aware"
    pain_points: ["specific pain point 1", "specific pain point 2"]
    desires: ["desired outcome 1", "desired outcome 2"]
  format:
    type: "sales_page|email|headline_set|ad_copy|landing_page|product_description"
    length: "word count or section count"
    structure: "required sections or format"
  tone:
    voice: "authoritative|friendly|urgent|conversational|professional"
    brand_constraints: "any brand voice requirements"
  constraints:
    - "compliance requirements"
    - "word limits"
    - "must include / must not include"
```

### Optional Enrichment (from HRM context)

```yaml
copy_enrichment:
  frameworks_to_use:
    - "hormozi-offer-framework"  # from reference/frameworks/
    - "aida"                      # from copy methodology
  psychology_principles:
    - "scarcity"                  # from reference/psychology/
    - "social-proof"
  competitor_context: "What competitors say, how to differentiate"
  swipe_references: ["relevant swipe file IDs"]
  conversion_goal: "Specific CTA or conversion metric"
```

---

## Quality Gate Integration

### Copy Squad Internal Gates

The Copy Squad chief runs internal quality checks before delivering:

1. **Framework compliance**: Is the chosen framework correctly applied?
2. **Audience alignment**: Does the copy speak to the defined audience?
3. **Tone consistency**: Does voice match requirements throughout?
4. **Persuasion mechanics**: Are psychological triggers present and effective?
5. **Constraint compliance**: All must-include/must-not-include respected?

### HRM External Gates (after delivery)

The HRM verifies Copy Squad output using these checks:

| Gate Level | Checks for Copy |
|-----------|----------------|
| Level 2 (Local) | Deliverables exist, format matches, length within bounds |
| Level 4 (Semantic) | Objective addressed, audience fit, tone accurate, persuasion effective |

### Threshold

Copy quality threshold: **0.85** (from design domain threshold, as copy is subjective but must meet creative quality bar).

---

## Feedback Protocol

### HRM -> Copy Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: COPY REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.85

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
===================================
```

### Copy Squad Chief -> HRM

Revision delivery:

```
=== COPY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
================================
```

---

## Available Copy Squad Resources

### Reference Library (for brief enrichment)

| Category | Count | Path | Use For |
|----------|-------|------|---------|
| Psychology principles | 24 | reference/psychology/ | Selecting triggers |
| Copywriting books | 96 | reference/books/ | Framework selection |
| Persuasion frameworks | 14 | frameworks/ | Structural guidance |
| Swipe files | varies | swipe-files/ | Example inspiration |
| Voice profiles | varies | voice/ | Tone matching |

### Framework Quick Reference

| Framework | Best For |
|-----------|---------|
| hormozi-offer-framework | Offer structuring, value stacking |
| aida | Attention -> Interest -> Desire -> Action flow |
| pas | Problem -> Agitate -> Solution |
| bab | Before -> After -> Bridge |
| 4ps | Promise -> Picture -> Proof -> Push |
| star-story-solution | Narrative-based selling |
