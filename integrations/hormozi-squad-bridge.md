# Hormozi Squad Bridge

> Integration bridge between HRM Architect and Hormozi Squad. Defines when to delegate, how to map swarm workstreams to business strategy tasks, brief format, and quality gate integration.

---

## Overview

The Hormozi Squad Bridge enables the HRM to seamlessly delegate offer creation, lead generation, and business scaling workstreams to the Hormozi Squad instead of using generic agents. This produces higher quality business strategies by leveraging the squad's 16-agent roster covering offers, leads, pricing, closing, retention, scaling, and business models using Alex Hormozi methodology ($100M Offers, $100M Leads).

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Hormozi Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == PLAN AND domain is business strategy | "Design a Grand Slam Offer" |
| Keywords: "oferta", "Grand Slam Offer", "value equation" | "Create irresistible offer using value equation" |
| Keywords: "leads", "aquisicao", "escala", "pricing" | "Build lead generation system" |
| Keywords: "$100M Offers", "lead magnet", "value ladder" | "Design value ladder for SaaS" |
| Keywords: "LTV", "churn", "upsell", "downsell" | "Reduce churn with retention strategy" |
| Keywords: "unit economics", "pricing strategy", "offer stack" | "Optimize pricing for maximum LTV" |
| Workstream archetype includes business strategy + monetization | Build task with offer/revenue workstream |

### Manual Override

User can explicitly request Hormozi Squad: "Use the Hormozi Squad for this" or "Delegate to Hormozi team".

### When NOT to Delegate

- Brand strategy without business model focus (use Brand Squad)
- Technical implementation of pricing systems (use code agents)
- Content creation without business strategy angle (use Copy Squad)
- Pure analytics without strategic recommendations (use Data Squad)

---

## Swarm-to-Hormozi Mapping

When a multi-workstream task includes a business strategy component:

```yaml
# Example: New product launch with offer design
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "offer-design"
    archetype: L-Strategist  # detected as business strategy domain
    execution: squad_delegation  # -> Hormozi Squad
  - name: "sales-copy"
    archetype: L-Writer
    execution: squad_delegation  # -> Copy Squad

interface_contracts:
  - between: ["offer-design", "sales-copy"]
    contract: "Offer structure with value stack, bonuses, guarantee, and pricing delivered before copy creation"
    owner: "offer-design"
    delivery_checkpoint: "Before sales copy drafting phase"
  - between: ["offer-design", "frontend"]
    contract: "Pricing tiers, feature matrix, and CTA structure delivered for UI implementation"
    owner: "offer-design"
    delivery_checkpoint: "Before frontend pricing page build"
```

---

## Brief Format for Hormozi Squad

### Minimum Required Fields

```yaml
hormozi_brief:
  objective: "What the business strategy needs to achieve (specific, measurable)"
  scope:
    type: "offer_creation|lead_generation|pricing_strategy|value_ladder|retention_system|scaling_audit"
    deliverables: "Expected output format and depth"
    timeline: "Implementation timeline or deadline"
  business_context:
    business_model: "SaaS|ecommerce|service|agency|info_product|hybrid"
    current_revenue: "Current MRR/ARR or revenue range"
    target_revenue: "Target MRR/ARR or revenue goal"
    industry: "Industry and market segment"
  customer_context:
    ideal_customer_profile: "Who the ideal customer is"
    current_acquisition_cost: "Current CAC if known"
    lifetime_value: "Current LTV if known"
  constraints:
    - "market positioning requirements"
    - "pricing boundaries"
    - "competitive landscape considerations"
```

### Optional Enrichment (from HRM context)

```yaml
hormozi_enrichment:
  frameworks_to_use:
    - "grand-slam-offer"        # from $100M Offers methodology
    - "value-equation"          # Dream Outcome x Perceived Likelihood / Time x Effort
  economics:
    - "pricing-psychology"      # from reference materials
    - "unit-economics"          # LTV:CAC ratios, payback periods
  competitor_offers: "Known competitor pricing and offer structures"
  market_data: ["relevant market size, trends, benchmarks"]
```

---

## Quality Gate Integration

### Hormozi Squad Internal Gates

The Hormozi Squad chief runs internal quality checks before delivering:

1. **Value equation validation**: Does the offer maximize dream outcome and perceived likelihood while minimizing time and effort?
2. **Offer differentiation**: Is the offer clearly differentiated from competitors?
3. **Economic viability**: Do unit economics support the business model at scale?
4. **Scalability assessment**: Can the offer/strategy scale without proportional cost increase?
5. **Constraint compliance**: All market positioning and pricing boundaries respected?

### HRM External Gates (after delivery)

The HRM verifies Hormozi Squad output using these checks:

| Gate Level | Checks for Hormozi |
|-----------|-------------------|
| Level 2 (Local) | Deliverables exist, format matches, all components covered |
| Level 4 (Semantic) | Business model coherence, value proposition strength, scalability potential |

### Threshold

Hormozi quality threshold: **0.85** (design domain threshold, as strategic and creative business work).

---

## Feedback Protocol

### HRM -> Hormozi Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: STRATEGY REVISION ===
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

### Hormozi Squad Chief -> HRM

Revision delivery:

```
=== STRATEGY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
==================================
```
