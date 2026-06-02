# Traffic Masters Squad Bridge

> Integration bridge between HRM Architect and Traffic Masters Squad. Defines when to delegate, how to map swarm workstreams to traffic/ads tasks, brief format, and quality gate integration.

---

## Overview

The Traffic Masters Squad Bridge enables the HRM to seamlessly delegate paid traffic and customer acquisition workstreams to the Traffic Masters Squad instead of using generic agents. This produces higher quality campaign strategies by leveraging the squad's 16-agent roster covering paid traffic, customer acquisition, creative strategy, tracking, optimization, and scaling across Meta, Google, YouTube, TikTok, and LinkedIn.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Traffic Masters Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == BUILD AND domain is paid traffic | "Set up Meta Ads campaign" |
| Keywords: "trafego pago", "ads", "Meta Ads", "Google Ads" | "Create Google Ads campaign structure" |
| Keywords: "campanha", "CAC", "ROAS", "creative strategy" | "Optimize campaign ROAS" |
| Keywords: "tracking", "pixel", "conversao", "escala de trafego" | "Set up conversion tracking pixels" |
| Keywords: "YouTube Ads", "TikTok Ads", "LinkedIn Ads" | "Launch TikTok Ads creative testing" |
| Keywords: "CRO", "landing page optimization", "funnel ads" | "Optimize landing page conversion rate" |
| Workstream archetype includes traffic/acquisition + paid media | Build task with ads workstream |

### Manual Override

User can explicitly request Traffic Masters Squad: "Use the Traffic Masters Squad for this" or "Delegate to traffic team".

### When NOT to Delegate

- Organic content strategy without paid component (use Copy Squad)
- SEO without paid search integration (use doc-coauthoring or dedicated SEO)
- Brand strategy without advertising execution (use Brand Squad)
- Analytics without advertising context (use Data Squad)

---

## Swarm-to-Traffic Mapping

When a multi-workstream task includes a paid traffic component:

```yaml
# Example: Product launch with paid acquisition
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "paid-acquisition"
    archetype: L-TrafficMaster  # detected as traffic domain
    execution: squad_delegation  # -> Traffic Masters Squad
  - name: "sales-copy"
    archetype: L-Writer
    execution: squad_delegation  # -> Copy Squad

interface_contracts:
  - between: ["paid-acquisition", "frontend"]
    contract: "Landing page specs delivered with UTM structure, pixel placement, and conversion events"
    owner: "paid-acquisition"
    delivery_checkpoint: "Before frontend tracking integration"
  - between: ["paid-acquisition", "sales-copy"]
    contract: "Ad creative briefs with platform specs, audience targeting, and messaging angles"
    owner: "paid-acquisition"
    delivery_checkpoint: "Before ad copy creation phase"
```

---

## Brief Format for Traffic Masters Squad

### Minimum Required Fields

```yaml
traffic_brief:
  objective: "What the campaign needs to achieve (specific, measurable)"
  scope:
    type: "campaign_launch|creative_strategy|tracking_setup|optimization|scaling|audit"
    platforms: ["meta|google|youtube|tiktok|linkedin"]
    timeline: "campaign duration or audit period"
  campaign_context:
    platform: "Primary advertising platform"
    budget: "Daily/monthly budget range"
    target_audience: "Audience segments and targeting criteria"
    current_metrics: "Current CAC, ROAS, CTR, CVR if available"
  business_context:
    product: "Product or service being advertised"
    funnel_stage: "awareness|consideration|conversion|retention"
    conversion_goal: "Primary conversion event and value"
  constraints:
    - "platform compliance requirements"
    - "budget limits"
    - "brand guidelines for creatives"
```

### Optional Enrichment (from HRM context)

```yaml
traffic_enrichment:
  frameworks_to_use:
    - "creative-testing-framework"  # from methodology
    - "scaling-framework"           # from playbooks
  platform_specifics:
    - "meta-best-practices"         # platform-specific guidance
    - "google-quality-score"
  competitor_intelligence: "Known competitor ad strategies or spend levels"
  historical_data: ["previous campaign performance data"]
```

---

## Quality Gate Integration

### Traffic Masters Squad Internal Gates

The Traffic Masters Squad chief runs internal quality checks before delivering:

1. **Platform compliance**: Do all creatives and copy meet platform ad policies?
2. **Creative quality**: Are ad creatives compelling and properly formatted per platform?
3. **Tracking accuracy**: Are all pixels, events, and UTM parameters correctly configured?
4. **Budget efficiency**: Is budget allocation optimized across campaigns and ad sets?
5. **Targeting precision**: Are audience segments well-defined and non-overlapping?

### HRM External Gates (after delivery)

The HRM verifies Traffic Masters Squad output using these checks:

| Gate Level | Checks for Traffic |
|-----------|-------------------|
| Level 2 (Local) | Deliverables exist, format matches, all platforms covered |
| Level 4 (Semantic) | Strategy coherence, ROI potential, platform best practices followed |

### Threshold

Traffic quality threshold: **0.88** (code domain threshold, as tracking and technical implementation require precision).

---

## Feedback Protocol

### HRM -> Traffic Masters Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: TRAFFIC REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.88

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
=======================================
```

### Traffic Masters Squad Chief -> HRM

Revision delivery:

```
=== TRAFFIC REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
=================================
```
