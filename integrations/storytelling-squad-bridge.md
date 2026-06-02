# Storytelling Squad Bridge

> Integration bridge between HRM Architect and Storytelling Squad. Defines when to delegate, how to map swarm workstreams to storytelling tasks, brief format, and quality gate integration.

---

## Overview

The Storytelling Squad Bridge enables the HRM to seamlessly delegate narrative and presentation workstreams to the Storytelling Squad instead of using generic agents. This produces higher quality narratives by leveraging the squad's 12-agent roster covering brand narrative, pitch design, case studies, public narrative, keynotes, and improvisational storytelling.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Storytelling Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO == WRITE AND domain is storytelling | "Write a brand origin story" |
| Keywords: "narrativa", "storytelling", "historia da marca" | "Create company narrative" |
| Keywords: "pitch", "pitch deck", "investor pitch" | "Build investor pitch narrative" |
| Keywords: "case study", "caso de sucesso", "case de cliente" | "Write customer case study" |
| Keywords: "apresentacao", "keynote", "brand story" | "Design keynote narrative" |
| Keywords: "manifesto", "origin story", "founding story" | "Write brand manifesto" |
| Workstream archetype includes narrative/story + persuasion | Build task with story workstream |

### Manual Override

User can explicitly request Storytelling Squad: "Use the Storytelling Squad for this" or "Delegate to storytelling team".

### When NOT to Delegate

- Short social media captions (use Copy Squad)
- Technical documentation without narrative arc (use doc-coauthoring)
- Data-driven reports without storytelling angle (use Data Squad)
- Simple blog posts without strategic narrative (use Copy Squad)

---

## Swarm-to-Storytelling Mapping

When a multi-workstream task includes a storytelling component:

```yaml
# Example: Product launch with narrative
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "brand-narrative"
    archetype: L-Storyteller  # detected as storytelling domain
    execution: squad_delegation  # -> Storytelling Squad
  - name: "sales-copy"
    archetype: L-Writer
    execution: squad_delegation  # -> Copy Squad

interface_contracts:
  - between: ["brand-narrative", "frontend"]
    contract: "Narrative delivered as structured story arc with sections: hook, conflict, resolution, CTA"
    owner: "brand-narrative"
    delivery_checkpoint: "Before frontend content integration"
  - between: ["brand-narrative", "sales-copy"]
    contract: "Brand narrative framework and key messages delivered before copy creation"
    owner: "brand-narrative"
    delivery_checkpoint: "Before copy drafting phase"
```

---

## Brief Format for Storytelling Squad

### Minimum Required Fields

```yaml
storytelling_brief:
  objective: "What the narrative needs to achieve (specific, measurable)"
  narrative_type:
    type: "brand_story|pitch|case_study|keynote|manifesto|origin_story|campaign_narrative"
    format: "presentation|document|video_script|speech|web_content"
    length: "word count or duration"
  audience:
    primary: "Target audience description"
    emotional_state: "current|desired emotional state"
    knowledge_level: "what they already know"
  story_context:
    protagonist: "Who is the hero of the story"
    conflict: "The core tension or challenge"
    stakes: "What's at risk"
    transformation: "The desired change"
  constraints:
    - "brand voice requirements"
    - "factual accuracy requirements"
    - "cultural sensitivity"
```

### Optional Enrichment (from HRM context)

```yaml
storytelling_enrichment:
  frameworks_to_use:
    - "heros-journey"          # from reference/books/
    - "story-brand-framework"  # from methodology
  narrative_techniques:
    - "in-medias-res"          # from techniques
    - "nested-loops"
  reference_stories: ["relevant story examples or swipe files"]
  emotional_arc: "specific emotional journey desired"
```

---

## Quality Gate Integration

### Storytelling Squad Internal Gates

The Storytelling Squad chief runs internal quality checks before delivering:

1. **Narrative structure**: Is the story arc complete and compelling?
2. **Audience resonance**: Does the story connect with the target audience?
3. **Emotional authenticity**: Are emotional beats genuine and earned?
4. **Message clarity**: Is the core message clear without being heavy-handed?
5. **Constraint compliance**: All brand/factual requirements respected?

### HRM External Gates (after delivery)

The HRM verifies Storytelling Squad output using these checks:

| Gate Level | Checks for Storytelling |
|-----------|------------------------|
| Level 2 (Local) | Deliverables exist, format matches, length within bounds |
| Level 4 (Semantic) | Objective addressed, audience connection, emotional impact, message clarity |

### Threshold

Storytelling quality threshold: **0.85** (design domain threshold, as narrative is creative work).

---

## Feedback Protocol

### HRM -> Storytelling Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: STORY REVISION ===
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

### Storytelling Squad Chief -> HRM

Revision delivery:

```
=== STORY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
================================
```
