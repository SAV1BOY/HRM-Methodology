# Squad Delegation

> Detailed protocol for how the HRM Architect delegates workstreams to specialized squads. Covers detection, briefing, internal execution, delivery, and verification.

---

## Overview

When a workstream's domain matches a registered squad, the HRM delegates to the squad chief instead of spawning individual agents. This leverages the squad's specialized knowledge base, internal processes, and domain expertise.

---

## Delegation Flow

```
HRM Step 0.7 (Registry Lookup)
    |
    v
DETECT: workstream.domain matches squad.domain in registry/squads.yaml
    |
    v
PREPARE: Generate squad-brief from prompt-gen/prompt-templates/squad-brief.yaml
    |  Fill: objective, audience, tone, format, constraints, references
    v
DELEGATE: Send brief to squad chief
    |
    v
CHIEF RECEIVES brief and executes internally:
    |  1. Analyze brief requirements
    |  2. Select internal resources (frameworks, swipe files, templates)
    |  3. Apply squad-specific methodology
    |  4. Produce deliverables
    |  5. Run internal quality gates
    |  6. Prepare delivery report
    v
DELIVERY: Chief sends results + self-assessment to HRM
    |
    v
HRM VERIFY: Run verification cascade on deliverables
    |
    +-- PASS -> Integrate with other workstream results
    |
    +-- FAIL -> Send feedback-loop to chief for revision
```

---

## Detection Rules

### When to Delegate to Squad

A workstream should be delegated to a squad when:

1. **Domain match**: workstream domain is covered by a registered squad
2. **Sufficient scope**: workstream is substantial enough to warrant squad expertise
3. **Quality advantage**: squad's internal process will produce better results than a generic agent

### Current Squad-Domain Mapping

| Squad | Domain Keywords | When to Delegate |
|-------|----------------|-----------------|
| Squad de Copy | copywriting, sales page, email sequence, headlines, hooks, persuasion, conversion copy | Any workstream requiring persuasive or marketing copy |
| Squad HRM | orchestration, prompt engineering, technique selection | Self-delegation (HRM handles internally) |
| Brand Squad | marca, brand, identidade visual, branding, naming, posicionamento, brand equity, brand architecture, arquetipo | Any workstream requiring brand strategy, identity, or positioning |
| Design Squad | UI, UX, design system, componente, prototipo, wireframe, acessibilidade, user research, design tokens, handoff | Any workstream requiring UX/UI design, prototyping, or design systems |
| Data Squad | analytics, metricas, dashboard, KPI, coorte, funil, growth metrics, data pipeline, A/B test, experimento, instrumentacao, segmentacao, retention | Any workstream requiring data analysis, metrics, or experimentation |
| Cybersecurity Squad | seguranca, pentest, vulnerabilidade, red team, blue team, AppSec, compliance, OWASP, threat model, incident response, SOC, hardening, secure coding | Any workstream requiring security assessment, compliance, or incident response |
| C-Level Squad | estrategia executiva, board meeting, decisao estrategica, governance, OKR executivo, planejamento estrategico, visao, roadmap executivo, operating model | Any workstream requiring executive strategy, governance, or cross-squad alignment |
| Storytelling Squad | narrativa, storytelling, historia da marca, pitch, case study, keynote, manifesto, origin story, brand story | Any workstream requiring narrative design, pitches, or story-driven content |
| Traffic Masters Squad | trafego pago, ads, Meta Ads, Google Ads, campanha, CAC, ROAS, creative strategy, tracking, pixel, conversao, escala de trafego | Any workstream requiring paid traffic, ad campaigns, or performance marketing |
| Hormozi Squad | oferta, Grand Slam Offer, value equation, leads, aquisicao, escala, pricing, $100M Offers, lead magnet, value ladder, LTV, churn | Any workstream requiring offer creation, lead generation, or business growth strategy |
| Movement Squad | movimento, comunidade, cultura de marca, ativacao, manifesto, tribo, community building, cultural strategy, memetics, rituais | Any workstream requiring movement design, cultural strategy, or community activation |
| Advisory Board Squad | advisory, conselho, board, investidor, cap table, due diligence, mentoria, governanca, fundraising, exit strategy | Any workstream requiring strategic advisory, board preparation, or governance |

### When NOT to Delegate

- One-line copy edits (too small for squad overhead)
- Technical writing without persuasion angle (use doc-coauthoring skill instead)
- Mixed workstreams where the squad's domain is < 20% of the work
- Simple CSS changes or color lookups (use skills directly)
- Routine tasks that don't need specialized squad expertise

---

## Brief Construction

### Required Fields (from squad-brief template)

1. **Objective**: What the copy/content needs to achieve
   - Be specific: "Write a sales page that converts free trial users to paid"
   - Include measurable success criteria

2. **Audience**: Who the content is for
   - Demographics, psychographics, awareness level
   - Pain points and desires

3. **Tone**: Voice and style requirements
   - Formal/informal, authoritative/friendly
   - Brand voice constraints

4. **Format**: Deliverable specifications
   - Type: email, sales page, headline set, ad copy, etc.
   - Length constraints
   - Structure requirements

5. **Constraints**: Non-negotiable requirements
   - Brand guidelines
   - Compliance/legal requirements
   - Word limits

6. **Reference Materials**: Relevant squad assets to use
   - Specific frameworks (e.g., "Use Hormozi Offer Framework")
   - Swipe file examples
   - Psychological principles to apply

### Optional Fields

- **Competitor examples**: What to differentiate from
- **Conversion goal**: Specific CTA or metric target
- **Psychological triggers**: Specific principles (scarcity, social proof, etc.)

---

## Internal Execution (Squad Side)

The HRM does NOT manage the squad's internal process. The chief owns it.

### Copy Squad Internal Flow (example)

```
1. Brief received from HRM
2. Chief analyzes: audience, tone, format, constraints
3. Chief selects resources:
   - Frameworks: hormozi-offer-framework, aida-framework, etc.
   - Psychology: scarcity, social-proof, commitment-consistency
   - Swipe files: relevant examples for the format
   - Voice profiles: matching tone requirements
4. Chief produces deliverables using squad methodology
5. Chief runs internal quality checks:
   - Persuasion framework applied correctly?
   - Voice/tone matches requirements?
   - All constraints respected?
   - Psychological triggers present?
6. Chief prepares delivery report
```

---

## Delivery Report Format

```
=== SQUAD DELIVERY REPORT ===
Squad: {squad_name}
Brief ID: {workstream_name}

Deliverables:
  - {deliverable_1}: COMPLETE
  - {deliverable_2}: COMPLETE

Self-Assessment: {score}/{threshold}
  - Objective alignment: X/10
  - Audience fit: X/10
  - Tone accuracy: X/10
  - Constraint compliance: X/10

Frameworks Applied:
  - {framework_1}
  - {framework_2}

Psychology Principles Used:
  - {principle_1}: {how_applied}
  - {principle_2}: {how_applied}

Issues: {issues_or_none}
Notes: {additional_context}
==============================
```

---

## HRM Verification of Squad Output

After receiving the delivery report:

1. **Level 2 (Local)**: Check deliverables exist and match requested format
2. **Level 4 (Semantic)**: Verify content meets success criteria
   - Does copy address the objective?
   - Is audience targeting correct?
   - Are constraints respected?
   - Is quality bar met?

Level 1 (Syntax) and Level 3 (Global) are typically not applicable for copy content (no code compilation or cross-module integration).

### If Verification Fails

Send feedback-loop template to squad chief:
- Identify specific quality gap
- Reference the specific check that failed
- Provide acceptance criteria for revision
- Budget remaining for revision

---

## Hybrid Mode: Squad + Swarm

When a task has both code and copy workstreams:

```
ExecutionPlan:
  Workstream 1: Frontend (code) -> Swarm agent
  Workstream 2: Sales Copy       -> Squad de Copy delegation
  Workstream 3: Backend (code)   -> Swarm agent

Integration:
  - Squad delivers copy content
  - Frontend agent integrates copy into UI
  - Interface contract: copy content format (markdown/JSON with sections)
```

The HRM coordinates the handoff by ensuring:
- Squad delivers before frontend needs the copy
- Interface contract specifies exact format
- Both pass their respective quality gates before integration
