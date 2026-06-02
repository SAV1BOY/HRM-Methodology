# C-Level Squad Bridge

> Integration bridge between HRM Architect and C-Level Squad. Defines when to delegate, how to map swarm workstreams to executive strategy tasks, brief format, and quality gate integration.

---

## Overview

The C-Level Squad Bridge enables the HRM to seamlessly delegate executive strategy and governance workstreams to the C-Level Squad instead of using generic agents. This produces higher quality strategic deliverables by leveraging the squad's 6-agent roster (CEO/Visionary, COO, CMO, CTO, CIO, CAIO) covering executive strategy, operational excellence, and governance.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the C-Level Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO in [PLAN, REVIEW] AND domain is executive strategy | "Define company strategy" |
| Keywords: "estrategia executiva", "executive strategy" | "Develop 3-year strategic plan" |
| Keywords: "board meeting", "board presentation", "board report" | "Prepare board meeting materials" |
| Keywords: "decisao estrategica", "strategic decision" | "Evaluate market entry decision" |
| Keywords: "governance", "governanca", "corporate governance" | "Set up governance framework" |
| Keywords: "OKR executivo", "executive OKR", "company OKR" | "Define company-level OKRs" |
| Keywords: "planejamento estrategico", "strategic planning" | "Annual strategic planning session" |
| Keywords: "visao", "vision", "mission", "purpose" | "Refine company vision and mission" |
| Keywords: "roadmap executivo", "executive roadmap" | "Build executive technology roadmap" |
| Keywords: "operating model", "modelo operacional" | "Design new operating model" |
| Workstream archetype includes strategy/executive + governance | Build task with executive workstream |

### Manual Override

User can explicitly request C-Level Squad: "Use the C-Level Squad for this" or "Delegate to executive team".

### When NOT to Delegate

- Day-to-day project management (use planning skills or project management tools)
- Individual team decisions without cross-functional impact
- Tactical marketing campaigns (use Traffic Masters Squad)
- Code reviews or technical implementation decisions (use development skills)
- Operational tasks that don't require strategic perspective

---

## Swarm-to-C-Level Mapping

When a multi-workstream task includes a strategic/executive component:

```yaml
# Example: Company pivot strategy
workstreams:
  - name: "market-analysis"
    archetype: L-Analyst
    execution: swarm_agent
  - name: "executive-strategy"
    archetype: L-Strategist-Executive  # detected as executive domain
    execution: squad_delegation  # -> C-Level Squad
  - name: "operational-plan"
    archetype: L-Planner
    execution: squad_delegation  # -> C-Level Squad (same squad, COO focus)

interface_contracts:
  - between: ["market-analysis", "executive-strategy"]
    contract: "Market research and competitive analysis delivered before strategic decision framework"
    owner: "market-analysis"
    delivery_checkpoint: "Before strategic option evaluation"
  - between: ["executive-strategy", "operational-plan"]
    contract: "Strategic direction and priorities defined before operational planning"
    owner: "executive-strategy"
    delivery_checkpoint: "Before operational model design"
```

---

## Brief Format for C-Level Squad

### Minimum Required Fields

```yaml
clevel_brief:
  objective: "What the strategic deliverable needs to achieve (specific, measurable)"
  scope:
    type: "strategic_decision|board_preparation|operating_model|okr_setting|governance_review|cross_squad_alignment"
    deliverables: ["strategic plan", "board deck", "operating model", "OKR framework", "governance charter"]
  strategic_context:
    company_stage: "pre-seed|seed|series-a|growth|mature|turnaround"
    market_position: "Current market standing and competitive landscape"
    key_challenges: ["top strategic challenges to address"]
  stakeholders:
    who_decides: ["decision makers and their roles"]
    who_is_affected: ["teams/departments impacted by decisions"]
  constraints:
    - "budget and resource limitations"
    - "regulatory environment"
    - "timeline for strategic decisions"
    - "board expectations and reporting cadence"
```

### Optional Enrichment (from HRM context)

```yaml
clevel_enrichment:
  frameworks_to_use:
    - "eos-traction"          # from reference/management/
    - "objectives-key-results" # from methodology
    - "balanced-scorecard"     # from reference/strategy/
  decision_model: "RAPID|RACI|DACI"
  industry_context: ["relevant industry trends and disruptions"]
  financial_data: ["revenue metrics", "burn rate", "runway"]
  previous_decisions: ["relevant prior strategic decisions and outcomes"]
```

---

## Quality Gate Integration

### C-Level Squad Internal Gates

The C-Level Squad chief runs internal quality checks before delivering:

1. **Strategic alignment**: Are recommendations aligned with company vision and values?
2. **Evidence-based reasoning**: Are decisions backed by data and market evidence?
3. **Stakeholder coverage**: Have all affected stakeholders been considered?
4. **Feasibility assessment**: Are recommendations practically achievable?
5. **Risk evaluation**: Have strategic risks been identified and mitigated?

### HRM External Gates (after delivery)

The HRM verifies C-Level Squad output using these checks:

| Gate Level | Checks for C-Level |
|-----------|-------------------|
| Level 2 (Local) | Deliverables exist, format matches, all requested strategic elements present |
| Level 4 (Semantic) | Strategic coherence verified, evidence quality sufficient, recommendations actionable |

### Threshold

C-Level quality threshold: **0.85** (design domain threshold for strategic/creative work requiring judgment and synthesis).

---

## Feedback Protocol

### HRM -> C-Level Squad Chief

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

### C-Level Squad Chief -> HRM

Revision delivery:

```
=== STRATEGY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
===================================
```
