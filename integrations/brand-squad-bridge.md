# Brand Squad Bridge

> Integration bridge between HRM Architect and Brand Squad. Defines when to delegate, how to map swarm workstreams to brand tasks, brief format, and quality gate integration.

---

## Overview

The Brand Squad Bridge enables the HRM to seamlessly delegate brand strategy and identity workstreams to the Brand Squad instead of using generic agents. This produces higher quality brand deliverables by leveraging the squad's 15-agent roster covering brand equity, identity systems, naming, positioning, archetypes, and competitive strategy.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Brand Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == BUILD AND domain is brand-strategy | "Create brand positioning" |
| Keywords: "marca", "brand", "identidade visual", "branding" | "Develop brand identity system" |
| Keywords: "naming", "nome de marca", "nomenclatura" | "Name our new product line" |
| Keywords: "posicionamento", "brand positioning", "diferenciacao" | "Define competitive positioning" |
| Keywords: "arquetipo", "brand archetype", "personalidade de marca" | "Select brand archetype" |
| Keywords: "brand equity", "valor de marca", "brand architecture" | "Design brand architecture" |
| Workstream archetype includes brand/identity + strategy | Build task with brand workstream |

### Manual Override

User can explicitly request Brand Squad: "Use the Brand Squad for this" or "Delegate to brand team".

### When NOT to Delegate

- Simple logo placement or color references (use brand-guidelines skill)
- UI component styling without brand strategy (use frontend-design)
- Marketing copy without brand strategy angle (use Copy Squad)
- One-off brand color lookup (too small for squad overhead)

---

## Swarm-to-Brand Mapping

When a multi-workstream task includes a branding component:

```yaml
# Example: Building a new product launch
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "brand-identity"
    archetype: L-Strategist  # detected as brand domain
    execution: squad_delegation  # -> Brand Squad
  - name: "copy"
    archetype: L-Writer
    execution: squad_delegation  # -> Copy Squad

interface_contracts:
  - between: ["brand-identity", "frontend"]
    contract: "Brand delivered as design tokens (colors, typography, spacing) + brand voice guidelines"
    owner: "brand-identity"
    delivery_checkpoint: "Before frontend visual implementation"
  - between: ["brand-identity", "copy"]
    contract: "Brand voice profile and messaging hierarchy delivered before copy creation"
    owner: "brand-identity"
    delivery_checkpoint: "Before copy drafting phase"
```

---

## Brief Format for Brand Squad

### Minimum Required Fields

```yaml
brand_brief:
  objective: "What the brand deliverable needs to achieve (specific, measurable)"
  scope:
    type: "full_identity|positioning|naming|architecture|audit|refresh"
    deliverables: ["brand platform", "visual identity", "naming options"]
  audience:
    primary: "Target audience description"
    market_context: "Competitive landscape and market positioning"
    differentiation_needs: ["key differentiators needed"]
  brand_context:
    existing_brand: "Current brand state (if refresh/audit)"
    values: ["core brand values"]
    personality_traits: ["desired brand personality"]
  constraints:
    - "industry regulations"
    - "existing brand equity to preserve"
    - "timeline and budget"
```

### Optional Enrichment (from HRM context)

```yaml
brand_enrichment:
  frameworks_to_use:
    - "aaker-brand-identity"  # from reference/books/
    - "keller-cbbe"           # from methodology
  psychology_principles:
    - "archetypes"            # from reference/psychology/
    - "cognitive-fluency"
  competitive_analysis: "Competitor brands to differentiate from"
  industry_references: ["relevant industry benchmarks"]
```

---

## Quality Gate Integration

### Brand Squad Internal Gates

The Brand Squad chief runs internal quality checks before delivering:

1. **Framework compliance**: Is the chosen branding framework correctly applied?
2. **Audience alignment**: Does the brand resonate with the defined audience?
3. **Consistency**: Are all brand elements internally consistent?
4. **Differentiation**: Does the brand clearly differentiate from competitors?
5. **Constraint compliance**: All industry/legal requirements respected?

### HRM External Gates (after delivery)

The HRM verifies Brand Squad output using these checks:

| Gate Level | Checks for Brand |
|-----------|----------------|
| Level 2 (Local) | Deliverables exist, format matches, all requested elements present |
| Level 4 (Semantic) | Objective addressed, audience fit, differentiation achieved, consistency verified |

### Threshold

Brand quality threshold: **0.85** (design domain threshold, as brand work requires creative quality bar).

---

## Feedback Protocol

### HRM -> Brand Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: BRAND REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.85

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
=====================================
```

### Brand Squad Chief -> HRM

Revision delivery:

```
=== BRAND REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
================================
```
