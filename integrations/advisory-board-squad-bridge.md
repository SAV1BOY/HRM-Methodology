# Advisory Board Squad Bridge

> Integration bridge between HRM Architect and Advisory Board Squad. Defines when to delegate, how to map swarm workstreams to advisory tasks, brief format, and quality gate integration.

---

## Overview

The Advisory Board Squad Bridge enables the HRM to seamlessly delegate strategic advisory, governance, and leadership workstreams to the Advisory Board Squad instead of using generic agents. This produces higher quality strategic advice by leveraging the squad's 11-agent roster (Dalio, Munger, Naval, Thiel, Hoffman, Sinek, Brown, Lencioni, Sivers, Chouinard, Board Chair) covering strategy, capital, governance, leadership, culture, growth, and risk.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Advisory Board Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == PLAN AND domain is strategic advisory | "Get board-level strategic advice" |
| Keywords: "advisory", "conselho", "board", "investidor" | "Prepare for advisory board meeting" |
| Keywords: "cap table", "due diligence", "mentoria" | "Review cap table structure" |
| Keywords: "governanca", "fundraising", "exit strategy" | "Plan Series A fundraising strategy" |
| Keywords: "board meeting", "strategic review", "board deck" | "Prepare quarterly board deck" |
| Keywords: "first principles", "mental models", "contrarian" | "Apply first principles to market entry" |
| Workstream archetype includes strategy/advisory + multi-perspective | Build task with advisory workstream |

### Manual Override

User can explicitly request Advisory Board Squad: "Use the Advisory Board Squad for this" or "Delegate to advisory team".

### When NOT to Delegate

- Day-to-day operational decisions (use C-Level Squad)
- Marketing execution without strategic dimension (use other squads)
- Code implementation (use code agents)
- Routine financial reporting without strategic analysis (use Data Squad)

---

## Swarm-to-Advisory Mapping

When a multi-workstream task includes a strategic advisory component:

```yaml
# Example: Fundraising with strategic planning
workstreams:
  - name: "financial-model"
    archetype: L-Analyst
    execution: swarm_agent
  - name: "strategic-advisory"
    archetype: L-Advisor  # detected as advisory domain
    execution: squad_delegation  # -> Advisory Board Squad
  - name: "pitch-narrative"
    archetype: L-Storyteller
    execution: squad_delegation  # -> Storytelling Squad

interface_contracts:
  - between: ["strategic-advisory", "financial-model"]
    contract: "Strategic assumptions and growth scenarios delivered before financial modeling"
    owner: "strategic-advisory"
    delivery_checkpoint: "Before financial model construction"
  - between: ["strategic-advisory", "pitch-narrative"]
    contract: "Strategic positioning, competitive moats, and vision framework delivered before pitch creation"
    owner: "strategic-advisory"
    delivery_checkpoint: "Before pitch narrative drafting"
```

---

## Brief Format for Advisory Board Squad

### Minimum Required Fields

```yaml
advisory_brief:
  objective: "What strategic advice is needed (specific, measurable)"
  scope:
    type: "strategic_advice|board_preparation|fundraising|governance|leadership|crisis|growth_strategy"
    deliverables: "Expected output format and depth"
    urgency: "immediate|this_week|this_month|strategic_horizon"
  company_context:
    stage: "pre_seed|seed|series_a|series_b|growth|mature"
    industry: "Industry and market segment"
    key_metrics: "Revenue, growth rate, burn rate, runway"
    current_challenges: "Top 3 strategic challenges"
  advisory_context:
    what_type_of_advice: "Strategic direction, risk assessment, growth planning, etc."
    urgency: "How time-sensitive is this decision"
    previous_decisions: "Relevant past decisions and their outcomes"
  constraints:
    - "confidentiality requirements"
    - "regulatory considerations"
    - "stakeholder alignment needs"
```

### Optional Enrichment (from HRM context)

```yaml
advisory_enrichment:
  frameworks_to_use:
    - "dalio-principles"          # Bridgewater principles
    - "munger-mental-models"      # Latticework of mental models
    - "thiel-contrarian"          # Zero to One thinking
  decision_model:
    - "first-principles"          # Break down to fundamentals
    - "probabilistic-thinking"    # Expected value analysis
  market_data: "Relevant market intelligence and competitive landscape"
  board_materials: ["existing board decks, minutes, or strategic plans"]
```

---

## Quality Gate Integration

### Advisory Board Squad Internal Gates

The Advisory Board Squad chief (Board Chair) runs internal quality checks before delivering:

1. **Multi-perspective coverage**: Have at least 3 advisor perspectives been synthesized?
2. **Evidence quality**: Are recommendations supported by data, principles, or precedent?
3. **Actionability**: Are recommendations concrete and implementable?
4. **Risk assessment**: Have downside scenarios been thoroughly considered?
5. **Contrarian viewpoints**: Has at least one contrarian perspective been explored?

### HRM External Gates (after delivery)

The HRM verifies Advisory Board Squad output using these checks:

| Gate Level | Checks for Advisory |
|-----------|---------------------|
| Level 2 (Local) | Deliverables exist, format matches, all perspectives covered |
| Level 4 (Semantic) | Strategic depth, multi-perspective analysis, actionability of recommendations |

### Threshold

Advisory quality threshold: **0.85** (design domain threshold, as strategic advisory is creative intellectual work).

---

## Feedback Protocol

### HRM -> Advisory Board Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: ADVISORY REVISION ===
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

### Advisory Board Squad Chief -> HRM

Revision delivery:

```
=== ADVISORY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
==================================
```
