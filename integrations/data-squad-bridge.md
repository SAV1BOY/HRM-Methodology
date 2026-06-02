# Data Squad Bridge

> Integration bridge between HRM Architect and Data Squad. Defines when to delegate, how to map swarm workstreams to data tasks, brief format, and quality gate integration.

---

## Overview

The Data Squad Bridge enables the HRM to seamlessly delegate analytics, growth metrics, and experimentation workstreams to the Data Squad instead of using generic agents. This produces higher quality data deliverables by leveraging the squad's 7-agent roster covering analytics, growth metrics, customer success, community metrics, experimentation, and data governance.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Data Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO in [BUILD, PLAN] AND domain is analytics/metrics | "Set up analytics pipeline" |
| Keywords: "analytics", "metricas", "metric definition" | "Define our north star metric" |
| Keywords: "dashboard", "KPI", "reporting" | "Build an executive KPI dashboard" |
| Keywords: "coorte", "cohort", "retention", "churn" | "Analyze user cohort retention" |
| Keywords: "funil", "funnel", "conversion" | "Optimize signup funnel" |
| Keywords: "growth metrics", "AARRR", "pirate metrics" | "Set up growth metric tracking" |
| Keywords: "data pipeline", "ETL", "dbt", "instrumentacao" | "Build data transformation pipeline" |
| Keywords: "A/B test", "experimento", "experiment design" | "Design A/B test for pricing page" |
| Keywords: "segmentacao", "segmentation", "cohort analysis" | "Segment users by behavior" |
| Workstream archetype includes data/analytics + strategy | Build task with data workstream |

### Manual Override

User can explicitly request Data Squad: "Use the Data Squad for this" or "Delegate to data team".

### When NOT to Delegate

- Simple spreadsheet creation without analysis (use xlsx skill)
- Database schema design without analytics context (use database-architect agent)
- Data visualization only without underlying analysis (use frontend-design skill)
- One-off SQL query (too small for squad overhead)

---

## Swarm-to-Data Mapping

When a multi-workstream task includes a data/analytics component:

```yaml
# Example: Building a growth analytics platform
workstreams:
  - name: "frontend-dashboard"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "data-analytics"
    archetype: L-Analyst  # detected as data domain
    execution: squad_delegation  # -> Data Squad
  - name: "backend-api"
    archetype: L-Builder-Backend
    execution: swarm_agent

interface_contracts:
  - between: ["data-analytics", "frontend-dashboard"]
    contract: "Metric definitions, query specs, and data schemas delivered before dashboard implementation"
    owner: "data-analytics"
    delivery_checkpoint: "Before dashboard component design"
  - between: ["data-analytics", "backend-api"]
    contract: "Event tracking schema and instrumentation requirements defined before API development"
    owner: "data-analytics"
    delivery_checkpoint: "Before event tracking implementation"
```

---

## Brief Format for Data Squad

### Minimum Required Fields

```yaml
data_brief:
  objective: "What the data deliverable needs to achieve (specific, measurable)"
  scope:
    type: "analytics_setup|dashboard|experiment|cohort_analysis|metric_definition|growth_audit"
    deliverables: ["metric definitions", "dashboard specs", "experiment design", "analysis report"]
  data_context:
    data_sources: ["list of available data sources"]
    current_metrics: "What is currently being tracked (if anything)"
    tools: ["SQL", "dbt", "Amplitude", "Mixpanel", "BigQuery"]
  business_context:
    growth_stage: "pre-seed|seed|series-a|growth|mature"
    key_questions: ["business questions the data needs to answer"]
  constraints:
    - "data privacy requirements (GDPR, CCPA)"
    - "available data infrastructure"
    - "timeline for insights delivery"
```

### Optional Enrichment (from HRM context)

```yaml
data_enrichment:
  frameworks_to_use:
    - "north-star-metric"     # from methodology
    - "pirate-metrics-AARRR"  # from reference/growth/
  tools:
    - "SQL"                   # query language
    - "dbt"                   # transformation
    - "Amplitude"             # product analytics
  statistical_method: "bayesian|frequentist"
  visualization_preferences: ["chart types", "color schemes"]
  benchmark_references: ["industry benchmarks for comparison"]
```

---

## Quality Gate Integration

### Data Squad Internal Gates

The Data Squad chief runs internal quality checks before delivering:

1. **Metric validity**: Are metric definitions clear, unambiguous, and correctly calculated?
2. **Statistical rigor**: Are statistical methods appropriate and correctly applied?
3. **Actionability**: Do insights lead to clear, actionable recommendations?
4. **Data quality**: Are data sources reliable and transformations correct?
5. **Governance compliance**: Are data privacy and governance requirements met?

### HRM External Gates (after delivery)

The HRM verifies Data Squad output using these checks:

| Gate Level | Checks for Data |
|-----------|----------------|
| Level 2 (Local) | Deliverables exist, format matches, all requested analyses/metrics present |
| Level 4 (Semantic) | Business questions answered, statistical validity confirmed, insights are actionable |

### Threshold

Data quality threshold: **0.88** (code domain threshold, since data work involves pipelines, queries, and statistical rigor).

---

## Feedback Protocol

### HRM -> Data Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: DATA REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.88

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
====================================
```

### Data Squad Chief -> HRM

Revision delivery:

```
=== DATA REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
===============================
```
