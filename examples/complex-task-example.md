# Complex Task Example: HRM End-to-End Flow (FULL Mode)

> Demonstrates the complete FULL 12-Step flow for building a SaaS landing page with persuasive copy. Features hybrid execution (agent + squad delegation), all quality gate levels, and plan evolution from v1 to v2.

---

## User Input

> "Construa uma landing page com copy persuasivo para lancamento de produto SaaS"

---

## Step 0: HRM Triage

```
=== HRM TRIAGE ===
Input: "Construa uma landing page com copy persuasivo para lancamento de produto SaaS"
Timestamp: 2026-03-03T15:00:00Z

Classification:
  TIPO: BUILD
  DOMINIO: WEB
  COMPLEXIDADE: PARALELA
  ARTEFATO: CODIGO

Signals detected:
  TIPO=BUILD: "construa" -> BUILD
  DOMINIO=WEB: "landing page" -> WEB
  COMPLEXIDADE=PARALELA: 3 independent workstreams detected:
    1. Frontend implementation (landing page HTML/CSS/JS)
    2. Copy content (persuasive copywriting -- squad domain match!)
    3. SEO optimization (metadata, structured data, performance)
  ARTEFATO=CODIGO: primary output is a landing page (code + content)

Complexity Assessment (quick):
  estimated_files: 6-10 (HTML, CSS, JS, images, meta, copy content, SEO config)
  estimated_tool_calls: 35-50
  multi_domain: true (WEB + COPYWRITING + SEO)
  parallelizable: true (3 independent workstreams after initial planning)
  uncertainty: medium (scope of "persuasivo" depends on audience/product context)
  squad_delegation_detected: true (copy content -> Squad de Copy domain match)

complexity_score: 7.5 / 10
hrm_mode: FULL (score >= 5.0)

Decision: FULL mode. All 12 Steps execute.
HRM remains active as Supreme Squad Chief (supervisor).
Plan v1 will evolve continuously via feedback loops.
==================
```

---

## Step 0.5: Discovery (using-superpowers)

```yaml
discovery_result:
  status: complete
  skills_available: 44
  relevant_skills:
    phase_1:
      - brainstorming (TIPO=BUILD, DOMINIO=WEB)
      - planning-with-files (COMPLEXIDADE=PARALELA)
      - writing-plans (TIPO=BUILD, COMPLEXIDADE >= MODERADA)
    phase_2:
      - frontend-design (DOMINIO=WEB, TIPO=BUILD)
      - web-artifacts-builder (ARTEFATO=CODIGO, DOMINIO=WEB, multi-component)
      - ui-ux-pro-max (design system, landing page aesthetics)
      - test-driven-development (TIPO=BUILD, ARTEFATO=CODIGO)
      - agent-router (COMPLEXIDADE=PARALELA, multi-agent needed)
      - swarm-orchestrator (3+ workstreams with dependencies)
    phase_3:
      - requesting-code-review (TIPO=BUILD, ARTEFATO=CODIGO)
      - verification-before-completion (mandatory for code)
  agents_relevant:
    - id: "01-wshobson-frontend-developer"
      archetype: L-Builder-Frontend
      domain_affinity: [WEB, REACT]
      capabilities: ["frontend development", "responsive design", "performance optimization"]
      cost_tier: medium
    - id: "02-punkpeye-researcher"
      archetype: L-Researcher
      capabilities: ["research", "analysis", "competitive intelligence"]
      cost_tier: low
    - id: "01-wshobson-seo-specialist"
      archetype: L-Researcher
      capabilities: ["SEO optimization", "metadata", "structured data", "Core Web Vitals"]
      cost_tier: low
  squads_relevant:
    - id: copy-squad
      name: "Squad de Copy"
      domain: copywriting
      match_reason: "'copy persuasivo' -> direct domain match for copywriting squad"
      capabilities: ["Direct response copywriting", "Sales page creation", "Persuasion framework application"]
      delegation_protocol: squad-brief
```

---

## Step 0.7: Registry Lookup

```yaml
registry_matches:
  skills:
    - id: brainstorming
      phase: 1
      match_reason: "TIPO=BUILD, DOMINIO=WEB"
    - id: planning-with-files
      phase: 1
      match_reason: "COMPLEXIDADE=PARALELA"
    - id: frontend-design
      phase: 2
      match_reason: "DOMINIO=WEB, TIPO=BUILD"
    - id: web-artifacts-builder
      phase: 2
      match_reason: "ARTEFATO=CODIGO, DOMINIO=WEB, multi-component"
    - id: ui-ux-pro-max
      phase: 2
      match_reason: "Landing page design system"
    - id: test-driven-development
      phase: 2
      match_reason: "TIPO=BUILD, ARTEFATO=CODIGO"
    - id: agent-router
      phase: 2
      match_reason: "COMPLEXIDADE=PARALELA, multi-agent"
    - id: swarm-orchestrator
      phase: 2
      match_reason: "3+ workstreams with phased execution"
    - id: requesting-code-review
      phase: 3
      match_reason: "TIPO=BUILD, ARTEFATO=CODIGO"
    - id: verification-before-completion
      phase: 3
      match_reason: "mandatory for code"
  agents:
    - id: "01-wshobson-frontend-developer"
      archetype: L-Builder-Frontend
      assigned_to: [landing-page-frontend]
    - id: "01-wshobson-seo-specialist"
      archetype: L-Researcher
      assigned_to: [seo-optimization]
  squads:
    - id: copy-squad
      name: "Squad de Copy"
      assigned_to: [copy-content]
      delegation_protocol: squad-brief
      match_reason: "'copy persuasivo' is core squad domain"
  mcps:
    - id: dev-browser
      match_reason: "Landing page needs visual verification"
      usage: "Screenshot for visual quality gate"
```

---

## Steps 1-8: Full Analysis

### Step 1: Bloom Level Analysis

```yaml
bloom_analysis:
  bloom_level: 6
  bloom_name: "Criar (Create)"
  rationale: |
    The user asks to CREATE a novel artifact: a complete landing page with persuasive
    copy for a SaaS product launch. This requires synthesizing multiple domains (UI design,
    copywriting, SEO) into a coherent whole. It goes beyond applying known patterns (Bloom 3)
    because it requires original creative decisions about layout, messaging, and persuasion strategy.
  implications:
    - Scoring rubric: novelty_and_coherence
    - Threshold: 0.75 (Bloom 6 threshold)
    - Technique selection: favor creative + structured techniques
```

### Step 2: Complexity Assessment (5 dimensions)

```yaml
complexity_assessment:
  dimension_1_cognitive:
    score: 7
    max: 10
    rationale: "Multi-domain creative synthesis. Frontend + copywriting + SEO. Each requires specialized expertise."
  dimension_2_scope:
    score: 7
    max: 10
    rationale: "6-10 files. Multiple asset types (HTML, CSS, JS, copy content, metadata). Cross-domain integration."
  dimension_3_uncertainty:
    score: 6
    max: 10
    rationale: "Product details not specified. Audience unclear. Copy tone unspecified. These must be discovered or assumed."
  dimension_4_interdependence:
    score: 6
    max: 10
    rationale: "Copy content must integrate into frontend layout. SEO affects HTML structure. Frontend must accommodate variable copy lengths."
  dimension_5_quality_bar:
    score: 8
    max: 10
    rationale: "Landing page for product launch. Must be conversion-optimized, visually polished, SEO-friendly, and mobile-responsive."

  aggregate_score: 6.8 / 10
  adjusted_score: 7.5 / 10  # Elevated due to multi-domain + squad delegation complexity
  mode_confirmation: FULL
```

### Step 3: Decomposability Check

```yaml
decomposability:
  is_decomposable: true
  decomposition_strategy: "hybrid parallel + squad delegation"
  workstreams:
    - name: landing-page-frontend
      description: "Build the landing page structure, layout, styles, responsive design, animations"
      independence: "partially independent; needs copy content to fill sections"
      estimated_files: 4 (index.html, styles.css, main.js, assets/)
      estimated_effort: "15-20 tool calls"
      execution_mode: agent
      archetype: L-Builder-Frontend

    - name: copy-content
      description: "Write persuasive SaaS launch copy: hero headline, value propositions, social proof, CTA sections"
      independence: "independent of frontend (produces content that frontend consumes)"
      estimated_effort: "10-15 tool calls"
      execution_mode: squad_delegation
      squad: copy-squad
      note: "Delegated to Copy Squad -- domain match for persuasive copywriting"

    - name: seo-optimization
      description: "Optimize meta tags, Open Graph, structured data (JSON-LD), sitemap hints, Core Web Vitals"
      independence: "partially dependent on frontend structure and copy content"
      estimated_files: 2 (meta additions in HTML, robots.txt/sitemap hints)
      estimated_effort: "6-8 tool calls"
      execution_mode: agent
      archetype: L-Researcher

  dependency_graph: |
    copy-content (independent, start immediately)
        |
        v
    landing-page-frontend (can start layout in parallel, needs copy for content sections)
        |
        v
    seo-optimization (needs final HTML structure and copy for meta descriptions)

  execution_phases:
    phase_1: [copy-content, landing-page-frontend]  # Parallel start
    phase_2: [seo-optimization]  # After phase 1 completes
    integration: [frontend integrates copy + SEO meta]
```

### Step 4: Methodology Selection

```yaml
methodology:
  selected: "Planner-Worker-Solver com HRM como Planner"
  rationale: |
    For Bloom 6 (Create) with 3 workstreams across multiple domains including
    squad delegation, the HRM acts as the Planner, dispatching Workers (agents + squad)
    to execute workstreams, then Solving (verifying and integrating results).
  execution_approach:
    planner: HRM Architect (Supreme Squad Chief)
    workers:
      - landing-page-frontend: Agent (L-Builder-Frontend)
      - copy-content: Squad de Copy (via squad-brief delegation)
      - seo-optimization: Agent (L-Researcher)
    solver: HRM Architect (verification cascade + integration)
```

### Step 5: Resource Calculation

```yaml
resource_calculation:
  workstreams:
    - name: landing-page-frontend
      archetype: L-Builder-Frontend
      agent_id: "01-wshobson-frontend-developer"
      predicted_cost: 18 tool calls
      budget_allocated: 22 tool calls
      technique_pipeline: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]

    - name: copy-content
      execution_mode: squad_delegation
      squad: copy-squad
      predicted_cost: 12 tool calls (internal to squad)
      budget_allocated: 15 tool calls
      note: "Squad chief manages internal budget"

    - name: seo-optimization
      archetype: L-Researcher
      agent_id: "01-wshobson-seo-specialist"
      predicted_cost: 8 tool calls
      budget_allocated: 10 tool calls
      technique_pipeline: [step-back-prompting, self-ask, chain-of-thought, grounding-via-sources, checklist-prompting]

  overhead:
    hrm_full_analysis: 8 tool calls (Steps 0-9)
    planning_skills: 5 tool calls (brainstorming + planning-with-files)
    convergence_monitoring: 3 tool calls (Step 10)
    verification_cascade: 10 tool calls (Step 11, all 4 levels)
    backtracking_reserve: 8 tool calls (Step 12 budget)
    review_skills: 5 tool calls (code review + final verification)
  total_budget: 76 tool calls
  reserve: 10 tool calls (emergency)
  grand_total: 86 tool calls
```

### Step 6: Hierarchical Decomposition

```yaml
hierarchical_decomposition:
  level_0:
    objective: "Build a conversion-optimized landing page with persuasive copy for SaaS product launch"
    success_criteria:
      - "Landing page loads in < 3 seconds (Core Web Vitals)"
      - "Mobile-responsive (works on 320px to 2560px viewports)"
      - "Copy uses at least 2 persuasion frameworks (e.g., AIDA, PAS)"
      - "SEO score >= 90 (Lighthouse audit)"
      - "All sections: hero, value props, social proof, pricing, CTA, footer"
      - "Contrast ratio WCAG AA compliant"
    constraints:
      - "Vanilla HTML/CSS/JS (no React/framework dependency for a landing page)"
      - "Must be self-contained (single page, no server-side rendering needed)"
      - "Copy must be in Portuguese (matching user's language)"

  level_1:  # Workstream level
    workstreams:
      - landing-page-frontend
      - copy-content
      - seo-optimization

  level_2:  # Sub-task level within each workstream
    landing-page-frontend:
      - "HTML structure with semantic sections (header, hero, features, social-proof, pricing, cta, footer)"
      - "CSS: responsive grid, animations, typography scale, color system"
      - "JS: smooth scroll, lazy loading, intersection observer for animations"
      - "Integration slots for copy content (data-section attributes)"
    copy-content:
      - "Hero headline + subheadline (hook + value proposition)"
      - "3 value proposition blocks with headlines and descriptions"
      - "Social proof section (testimonials, metrics, logos)"
      - "Pricing section copy"
      - "Primary CTA copy (above fold + bottom)"
      - "Objection handling / FAQ"
    seo-optimization:
      - "Title tag, meta description, Open Graph tags"
      - "JSON-LD structured data (SoftwareApplication)"
      - "Image alt text recommendations"
      - "Performance: lazy loading, critical CSS, minification hints"
```

### Step 7: Domain Hyperparameter Tuning

```yaml
hyperparameters:
  domain: fullstack  # Landing page spans frontend + content + SEO
  verification_threshold: 0.88
  max_cycles: 3
  convergence_patience: 2
  stagnation_threshold: 0.02
  backtracking_budget_fraction: 0.15

  domain_specific:
    frontend:
      threshold: 0.88
      visual_quality_gate: true  # Use dev-browser for visual check
      performance_gate: true  # Lighthouse audit
    copywriting:
      threshold: 0.85
      persuasion_framework_required: true
      squad_acceptance_threshold: 0.85
    seo:
      threshold: 0.90
      lighthouse_target: 90
```

### Step 8: Execution Mode Mapping

```yaml
execution_mode:
  primary: swarm  # 3 workstreams with dependencies -> swarm orchestration
  hybrid: true    # One workstream delegated to squad
  breakdown:
    - workstream: landing-page-frontend
      mode: agent
      target: "01-wshobson-frontend-developer"
      protocol: agent-handoff
    - workstream: copy-content
      mode: squad_delegation
      target: copy-squad
      protocol: squad-brief
    - workstream: seo-optimization
      mode: agent
      target: "01-wshobson-seo-specialist"
      protocol: agent-handoff
  coordination: "HRM as Supreme Squad Chief orchestrates all three, collecting results and managing integration"
```

---

## Step 9: ExecutionPlan (Full)

```yaml
execution_plan:
  version: "v1"
  mode: FULL
  complexity_score: 7.5
  bloom_level: 6  # Criar
  supervisor_active: true  # HRM remains as Supreme Squad Chief
  hybrid_execution: true  # agent + squad delegation

  level_0:
    objective: "Build a conversion-optimized landing page with persuasive copy for SaaS product launch"
    success_criteria:
      - "Landing page loads in < 3 seconds (Core Web Vitals)"
      - "Mobile-responsive (320px to 2560px viewports)"
      - "Copy uses at least 2 persuasion frameworks"
      - "SEO score >= 90 (Lighthouse)"
      - "All sections present: hero, value props, social proof, pricing, CTA, footer"
      - "WCAG AA contrast compliance"
      - "Copy in Portuguese"
    constraints:
      - "Vanilla HTML/CSS/JS"
      - "Self-contained single page"
      - "Portuguese language"
    domain_config:
      domain: fullstack
      verification_threshold: 0.88
      max_cycles: 3

  level_1:
    workstreams:

      - name: landing-page-frontend
        objective: "Build the responsive landing page with all sections, animations, and performance optimization"
        archetype: L-Builder-Frontend
        agent_id: "01-wshobson-frontend-developer"
        execution_mode: agent
        phase: 1  # Starts in phase 1 (layout/structure can begin without copy)
        file_ownership:
          - "landing-page/index.html"
          - "landing-page/styles.css"
          - "landing-page/main.js"
          - "landing-page/assets/"
        deliverables:
          - "Semantic HTML structure with all landing page sections"
          - "Responsive CSS with mobile-first approach"
          - "Smooth scroll, lazy loading, scroll-triggered animations"
          - "Placeholder slots for copy content (data-copy attributes)"
          - "Integration of final copy content from squad delivery"
        estimated_effort: "18 tool calls"
        predicted_cost: 22
        verification: "Visual check (dev-browser), Lighthouse performance, responsive test"
        prompt_generation_spec:
          archetype_primary_type: "code, creative"
          technique_pipeline: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
          technique_source: "technique-mapper quick-path L-Builder-Frontend"
          quality_checks: [syntax_valid, files_exist, deliverables_complete, unit_tests_pass]
          bloom_rubric: "novelty_and_coherence (originality >= 0.75)"

      - name: copy-content
        objective: "Write persuasive SaaS launch copy for all landing page sections"
        execution_mode: squad_delegation
        squad_id: copy-squad
        squad_name: "Squad de Copy"
        phase: 1  # Starts in phase 1 (parallel with frontend layout)
        deliverables:
          - "Hero headline + subheadline (hook + value prop)"
          - "3 value proposition blocks (headline + 2-3 sentence description each)"
          - "Social proof section (3 testimonials + 3 key metrics)"
          - "Pricing section copy (3 tiers with feature lists)"
          - "Primary CTA copy (2 variants for A/B)"
          - "FAQ section (5 questions addressing common objections)"
        estimated_effort: "12 tool calls (internal to squad)"
        predicted_cost: 15
        verification: "Persuasion framework applied, audience fit, conversion optimization"
        squad_brief_spec:
          objective: "Write conversion-optimized copy for SaaS landing page launch"
          audience: "SaaS buyers, technical decision-makers, startup founders"
          tone: "Professional but approachable, confident, outcome-focused"
          format: "Markdown with clear section headers for frontend integration"
          constraints:
            - "Portuguese language"
            - "Each section must be self-contained"
            - "Hero headline max 10 words"
            - "Subheadline max 25 words"
          reference_materials:
            - "Use AIDA framework for overall page flow"
            - "Use PAS (Problem-Agitate-Solve) for value proposition blocks"
            - "Apply scarcity and social proof principles"
          conversion_goal: "Free trial signup"
          psychological_triggers: ["scarcity", "social-proof", "authority", "commitment-consistency"]

      - name: seo-optimization
        objective: "Optimize landing page for search engines and social sharing"
        archetype: L-Researcher
        agent_id: "01-wshobson-seo-specialist"
        execution_mode: agent
        phase: 2  # Runs after frontend structure and copy are available
        depends_on: [landing-page-frontend, copy-content]
        file_ownership:
          - "landing-page/index.html (meta section only)"
          - "landing-page/robots.txt"
          - "landing-page/sitemap.xml"
        deliverables:
          - "Title tag and meta description (from copy content)"
          - "Open Graph and Twitter Card tags"
          - "JSON-LD structured data (SoftwareApplication schema)"
          - "Image alt text recommendations"
          - "Performance optimization hints (lazy loading, critical CSS)"
        estimated_effort: "8 tool calls"
        predicted_cost: 10
        verification: "Lighthouse SEO score >= 90, structured data validates"
        prompt_generation_spec:
          archetype_primary_type: "research, extraction"
          technique_pipeline: [step-back-prompting, self-ask, chain-of-thought, grounding-via-sources, checklist-prompting]
          technique_source: "technique-mapper quick-path L-Researcher"
          quality_checks: [syntax_valid, deliverables_complete, format_correct]
          bloom_rubric: "novelty_and_coherence (completeness >= 0.75)"

    interface_contracts:
      - source: copy-content
        target: landing-page-frontend
        contract: "Copy delivered as Markdown with section headers matching HTML data-section attributes: hero, value-props, social-proof, pricing, cta, faq"
        format: "Markdown file with ## Section Name headers"
      - source: landing-page-frontend
        target: seo-optimization
        contract: "Final HTML structure with semantic elements for SEO agent to add meta tags"
        format: "HTML file with <head> section accessible for meta injection"
      - source: copy-content
        target: seo-optimization
        contract: "Final headline and value prop text for meta description generation"
        format: "From the Markdown copy file, hero section"

  squad_delegations:
    - workstream: copy-content
      squad_id: copy-squad
      brief_template: squad-brief
      delegation_protocol: "squad-delegation (from execution/squad-delegation.md)"
      internal_execution: "Squad chief handles internally: framework selection, psychology application, internal quality gates"
      quality_integration:
        gate_owner: copy-chief
        internal_verification: [local, semantic]
        hrm_acceptance_threshold: 0.85
        feedback_loop: "HRM -> copy-chief -> revision -> delivery"

  execution_phases:
    - phase: 1
      workstreams: [copy-content, landing-page-frontend]
      parallel: true
      note: "Frontend starts layout/structure; Copy squad works independently"
      gate_after: true
    - phase: 2
      workstreams: [seo-optimization]
      note: "SEO needs final HTML structure and copy for meta"
      gate_after: true
    - phase: 3  # Integration
      workstreams: [landing-page-frontend]  # Frontend integrates copy + SEO
      note: "Frontend agent integrates copy content into layout and SEO meta"
      gate_after: true  # Final gate

  mcp_integrations:
    - id: dev-browser
      purpose: "Visual verification of landing page in both desktop and mobile viewports"
      usage: "Screenshot after frontend completion and after copy integration"
      gate: "visual_quality_gate (level 4 semantic check)"

  quality_gates:
    max_level: 4  # Per auto_level_policy: complexity_score >= 6 -> max level 4
    levels: [syntax, local, global, semantic]
    domain_thresholds:
      level_2: 0.88  # fullstack
      level_3: 0.85
      level_4: 0.88

  loop_protocol:
    max_loops: 3
    backtracking_triggers:
      - "Copy content does not match frontend section structure (contract violation)"
      - "Lighthouse performance score < 90"
      - "Copy lacks persuasion framework application"
      - "Mobile layout broken at any standard breakpoint"
      - "SEO structured data fails validation"
      - "Visual quality below expected polish for product launch"
    escalation: "After 3 failed loops, escalate to user with diagnostic report"
    credit_assignment: "Identify which workstream caused the failure for targeted re-execution"
```

---

## Step 9.5: Universal Prompt Forge (FULL + QUICK Tiers)

### Instantiated Agent-Handoff: Workstream "landing-page-frontend"

```markdown
You are a L-Builder-Frontend specialist working on the "landing-page-frontend" workstream.
Your expertise: frontend development, responsive design, CSS animations, performance optimization, landing page architecture.

## Objective
Build a conversion-optimized, responsive landing page for a SaaS product launch.
The page must be visually polished, fast-loading, and structured to integrate
persuasive copy content provided by a separate team.

### Success Criteria
- Landing page loads in < 3 seconds (Core Web Vitals)
- Mobile-responsive (320px to 2560px viewports)
- All sections present: hero, value props, social proof, pricing, CTA, footer
- WCAG AA contrast compliance
- Smooth scroll navigation
- Scroll-triggered animations for engagement
- Placeholder slots for copy content integration

## Scope
### File Ownership (ONLY modify these files)
- landing-page/index.html
- landing-page/styles.css
- landing-page/main.js
- landing-page/assets/

### Deliverables
- Semantic HTML structure with all landing page sections
- Responsive CSS with mobile-first approach
- Smooth scroll, lazy loading, scroll-triggered animations
- Placeholder slots for copy content (data-copy attributes)
- Integration of final copy content from squad delivery

## Project Context
- Tech stack: Vanilla HTML5, CSS3, JavaScript (ES6+)
- Existing patterns: None (greenfield landing page)
- Constraints:
  - No framework dependencies (vanilla only)
  - Self-contained single page
  - Must accommodate variable-length copy content
  - Portuguese language for UI elements (navigation, buttons)

## Interface Contracts
### Inputs (from other workstreams)
- Copy content from Squad de Copy: Markdown file with ## Section Name headers
  matching data-section attributes (hero, value-props, social-proof, pricing, cta, faq)

### Outputs (to other workstreams)
- Final HTML structure with <head> section accessible for SEO meta injection
- Semantic elements for structured data attachment

### Contract Format
- Copy input: Markdown with ## headers
- HTML output: Semantic HTML5 with data-section attributes

## Approach
Follow this technique pipeline:
1. **Role Prompting**: Act as a senior frontend developer specializing in high-conversion landing pages
2. **Plan-and-Solve**: Plan the page architecture (sections, responsive grid, animation strategy)
3. **Few-Shot**: Reference modern SaaS landing page patterns (hero with gradient, card-based features)
4. **Output Format**: Produce clean HTML5/CSS3/JS with semantic markup and BEM-style classes
5. **Self-Refine**: Review for mobile responsiveness, performance (no layout shifts), and accessibility
6. **Checklist Prompting**: Verify against landing page quality checklist

## Quality Requirements
- Verification threshold: 0.88 (fullstack domain)
- Bloom level: 6 (Criar / Create)
- Key checks: syntax_valid, files_exist, deliverables_complete, visual quality (via dev-browser)

## Budget
- Allocated tool calls: 22
- Maximum cycles: 3

## When to Report Problems
Report immediately to the HRM if:
- Copy content format does not match expected Markdown structure
- Performance cannot meet < 3 second load time with current approach
- Mobile layout requires fundamental restructuring
- CSS animations cause layout shifts or jank
```

### Instantiated Squad Brief: Workstream "copy-content" (to Squad de Copy)

```markdown
# Squad Brief: Squad de Copy
From: HRM Architect (Supreme Squad Chief)
Priority: HIGH
Budget: 15 tool calls

## Objective
Write conversion-optimized, persuasive copy for a SaaS product launch landing page.
The copy must drive free trial signups through strategic use of persuasion frameworks
and psychological triggers.

### What Success Looks Like
- Hero headline that hooks in < 3 seconds of reading
- Value propositions that clearly articulate the transformation (before -> after)
- Social proof that builds credibility and reduces purchase anxiety
- CTAs that create urgency without being pushy
- FAQ that pre-emptively handles top 5 objections
- Minimum 2 persuasion frameworks applied (AIDA + PAS)

## Audience
- Target: SaaS buyers, technical decision-makers, startup founders (25-45 years old)
- Tone: Professional but approachable, confident, outcome-focused
- Format: Markdown with section headers for frontend integration

## Scope & Deliverables
- Hero headline + subheadline (hook + value prop) -- headline max 10 words
- 3 value proposition blocks (headline + 2-3 sentence description each)
- Social proof section (3 testimonials + 3 key metrics)
- Pricing section copy (3 tiers with feature lists)
- Primary CTA copy (2 variants for A/B testing)
- FAQ section (5 questions addressing common objections)

### Constraints
- Portuguese language
- Each section must be self-contained
- Hero headline max 10 words, subheadline max 25 words
- No jargon without explanation
- Must feel authentic (not generic "we're the best" copy)

## Reference Materials
- Use AIDA framework for overall page flow (Attention -> Interest -> Desire -> Action)
- Use PAS (Problem-Agitate-Solve) for value proposition blocks
- Apply scarcity principle for pricing section (limited launch pricing)
- Apply social proof principle (testimonials, user count, logos)
- Apply authority principle (certifications, press mentions if applicable)
- Apply commitment-consistency (free trial = low commitment entry)

## Internal Architecture Guidance
Use your internal squad architecture to:
- Select relevant swipe files for SaaS landing page copy
- Apply the Hormozi Offer Framework for value proposition clarity
- Use psychology principles library for trigger implementation
- Apply voice profile matching for professional-approachable tone

## Quality Gates
- Internal verification: [local, semantic]
- HRM acceptance threshold: 0.85
- Bloom level rubric: novelty_and_coherence (Bloom 6)
  - Originality: adapted (not generic templates) -> score >= 0.7
  - Coherence: consistent voice across all sections -> score >= 0.8
  - Completeness: all deliverables present -> score >= 1.0
  - Feasibility: copy is ready to integrate -> score >= 0.9

## Reporting Protocol
Report to HRM Architect:
- On completion of each major deliverable
- When encountering blockers or scope changes
- Final delivery with self-assessment score

Format:
```
=== SQUAD DELIVERY REPORT ===
Squad: Squad de Copy
Deliverables: [list with status]
Self-Assessment: X.XX/0.85
Issues: [any issues encountered]
==============================
```

## Timeline
- Expected completion: Phase 1 (parallel with frontend layout)
- Checkpoint: Hero + value props ready first (frontend needs these earliest)
```

### Forge Tier Distribution

In FULL mode with multiple dispatch points, the Forge applies different tiers based on dispatch type and granularity:

```yaml
forge_tier_map:
  # Top-level workstreams (task granularity) -> FULL tier
  landing-page-frontend:
    dispatch_type: workstream-agent
    granularity: task
    tier: FULL
    techniques: [role-prompting, plan-and-solve, few-shot, output-format, self-refine, checklist-prompting]
    source: "technique-selector 4-phase scoring + pipeline-builder"

  # Squad delegation (task granularity) -> QUICK tier with squad-chief overlay
  copy-content:
    dispatch_type: squad-chief
    granularity: task
    tier: QUICK
    techniques: [step-back-prompting, plan-and-solve, checklist-prompting]
    source: "technique-mapper + squad-chief dispatch profile overlay"

  # Sub-dispatches within the squad (subtask granularity) -> MICRO tier
  copy-content-subtasks:
    dispatch_type: feedback-target
    granularity: subtask
    tier: MICRO
    techniques: [self-refine, checklist-prompting]
    source: "technique-index.yaml micro_defaults"

  # Quality gate reviewers -> tier depends on level
  gate-reviewers:
    level-1-2:
      dispatch_type: gate-reviewer
      tier: MICRO
      techniques: [chain-of-verification, checklist-prompting]
    level-3-4:
      dispatch_type: gate-reviewer
      tier: QUICK
      techniques: [chain-of-verification, contrastive-cot, checklist-prompting, output-format]
```

### Forge Scaling Summary

| Dispatch Point | Type | Granularity | Tier | Technique Count |
|---------------|------|-------------|------|-----------------|
| Frontend agent | workstream-agent | task | FULL | 6 |
| SEO agent | workstream-agent | task | FULL | 5 |
| Copy squad chief | squad-chief | task | QUICK | 3 |
| Feedback revision | feedback-target | subtask | MICRO | 2 |
| Syntax gate | gate-reviewer | - | MICRO | 2 |
| Global gate | gate-reviewer | - | QUICK | 4 |

**Key insight**: The Forge applies techniques **proportionally** — the most complex dispatch point (frontend agent building the entire landing page) gets FULL 6-technique pipeline, while a feedback revision loop gets just 2 MICRO techniques. This is the core value of the Universal Prompt Forge: every dispatch point gets the RIGHT amount of technique guidance, not too much, not too little.

---

## SET (Skill Execution Timeline)

```
=== SKILL EXECUTION TIMELINE ===
Tarefa: Construir landing page com copy persuasivo para lancamento SaaS
Classificacao: TIPO=BUILD DOMINIO=WEB COMPLEXIDADE=PARALELA ARTEFATO=CODIGO
HRM Mode: FULL | Complexity Score: 7.50/10
Plano: v1 (prototipo, sera refinado com feedback via 12-Step loop)

FASE 0 (Startup -- OBRIGATORIO):
  [x] hrm-architect -- FULL 12-Step (PASSO 0: classificacao + analise completa + Plano v1)
  [x] using-superpowers -- (PASSO 0.5: discovery de skills/agents/squads)

FASE 1 (Planejamento):
  [ ] brainstorming -- TIPO=BUILD, DOMINIO=WEB (explorar conceitos de landing page)
  [ ] planning-with-files -- COMPLEXIDADE=PARALELA (estruturar workstreams e dependencias)

FASE 2 (Execucao - hibrida: agent + squad delegation):
  [ ] frontend-design -- landing-page-frontend (L-Builder-Frontend agent)
  [ ] ui-ux-pro-max -- design system para landing page (cores, tipografia, espacamento)
  [ ] web-artifacts-builder -- construcao multi-componente da landing page
  [ ] agent-router -- COMPLEXIDADE=PARALELA (roteamento para swarm + squad)
  [ ] swarm-orchestrator -- coordenacao das 3 workstreams em fases
  [ ] [SQUAD DELEGATION] Squad de Copy -- copy persuasivo via squad-brief
  [ ] test-driven-development -- testes de performance e responsividade
  HRM Loop: convergence monitoring -> quality gates -> refinamento do plano

FASE 3 (Revisao):
  [ ] requesting-code-review -- TIPO=BUILD, ARTEFATO=CODIGO
  [ ] verification-before-completion -- verificacao obrigatoria (cascade level 1-4)
================================
```

---

## Execution Flow

### FASE 1: Planning

**brainstorming output:**
```
Landing page concepts explored:
  1. "Gradient Hero" -- Bold gradient background hero with floating product mockup
  2. "Story-Driven" -- Narrative flow: problem -> pain -> solution -> proof -> action
  3. "Feature Grid" -- Clean grid layout with icons and micro-interactions

Selected: Option 2 "Story-Driven"
Rationale: Best alignment with AIDA persuasion framework;
narrative flow naturally guides the reader toward conversion
```

**planning-with-files output:**
```
Execution phases:
  Phase 1 (parallel):
    - Frontend: Build HTML structure with semantic sections and responsive CSS
    - Copy Squad: Write all copy sections via squad-brief delegation
  Phase 2:
    - SEO: Add meta tags, structured data, performance hints
  Phase 3 (integration):
    - Frontend: Integrate copy into layout, final visual polish
  Phase 4 (verification):
    - Full verification cascade (levels 1-4)
    - Dev-browser visual check (desktop + mobile)
```

### FASE 2: Execution

**Phase 1 (parallel):**

Frontend agent starts building layout structure while Copy Squad works on persuasive content.

**Copy Squad Internal Execution:**
```
=== SQUAD DELIVERY REPORT ===
Squad: Squad de Copy
Deliverables:
  - Hero headline + subheadline: COMPLETE
    "Transforme Sua Operacao em 30 Dias"
    "A plataforma SaaS que automatiza o que sua equipe faz em 40 horas por semana -- em menos de 4."
  - 3 Value proposition blocks: COMPLETE (PAS framework applied)
  - Social proof section: COMPLETE (3 testimonials + metrics)
  - Pricing section copy: COMPLETE (3 tiers, scarcity applied)
  - CTA variants (A/B): COMPLETE
    Variant A: "Comece Gratis -- Sem Cartao de Credito"
    Variant B: "Experimente por 14 Dias -- Vagas Limitadas"
  - FAQ (5 objection handlers): COMPLETE

Self-Assessment: 0.89/0.85
  - Objective alignment: 9/10
  - Audience fit: 8.5/10
  - Tone accuracy: 9/10
  - Constraint compliance: 9/10

Frameworks Applied:
  - AIDA (overall page flow)
  - PAS (value proposition blocks)
  - Hormozi Offer Framework (pricing section)

Psychology Principles Used:
  - Scarcity: "Vagas Limitadas" in CTA variant B, "Preco de Lancamento" in pricing
  - Social Proof: User count ("+2.400 empresas"), testimonials, logo bar
  - Authority: "Certificado ISO 27001", "Destaque no ProductHunt"
  - Commitment-Consistency: Free trial as low-commitment entry point

Issues: None
Notes: Copy delivered in Markdown with ## headers matching agreed contract format
==============================
```

**Phase 2:** SEO agent optimizes after receiving frontend structure and copy.

**Phase 3:** Frontend agent integrates copy content into layout sections.

### Step 10: Convergence Monitoring

```yaml
convergence_monitoring:
  check_1:
    timestamp: "after phase 1"
    landing-page-frontend: "IN_PROGRESS (layout complete, awaiting copy integration)"
    copy-content: "COMPLETE (delivered, self-assessment 0.89)"
    seo-optimization: "PENDING (waiting for phase 2)"
    convergence: "on track, no stagnation"
  check_2:
    timestamp: "after phase 2"
    landing-page-frontend: "IN_PROGRESS (integrating copy)"
    seo-optimization: "COMPLETE (meta tags added, JSON-LD validated)"
    convergence: "on track"
  check_3:
    timestamp: "after phase 3"
    all_workstreams: "COMPLETE"
    convergence: "ready for verification cascade"
```

---

## Quality Gates (Step 11: Verification Cascade)

### First Verification Attempt (triggers plan evolution)

```yaml
quality_gate_results_v1:

  level_1_syntax:
    status: PASS
    checks:
      syntax_valid: PASS (HTML validates, CSS parses, JS no errors)
      no_parse_errors: PASS
      format_correct: PASS (HTML5, CSS3, ES6+)
      files_exist: PASS (index.html, styles.css, main.js, robots.txt)
    cost: 3 tool calls

  level_2_local:
    status: PASS
    score: 0.90
    threshold: 0.88
    checks:
      unit_tests_pass: PASS (scroll behavior, lazy loading, theme toggle)
      deliverables_complete: PASS (all sections present)
      internal_consistency: PASS (CSS variables consistent)
      documentation_present: PASS (code comments present)
    cost: 5 tool calls

  level_3_global:
    status: FAIL  # <-- FAILURE TRIGGERS PLAN EVOLUTION
    score: 0.78
    threshold: 0.85
    checks:
      integration_tests_pass: FAIL
        issue: "Copy content section headers do not align with 2 frontend data-section attributes"
        details: "Frontend uses data-section='social-proof', copy uses '## Prova Social' (mismatch)"
      no_file_conflicts: PASS
      interface_contracts_met: FAIL
        issue: "Contract specified Markdown headers matching data-section attributes, but 2/6 sections have naming mismatches"
      dependency_graph_valid: PASS
    cost: 6 tool calls

  level_4_semantic: SKIPPED (level 3 failed, must fix before proceeding)

  aggregate:
    passed: false
    failure_level: 3 (Global)
    root_cause: "Interface contract violation between copy-content and landing-page-frontend"
    credit_assignment:
      - workstream: landing-page-frontend
        responsibility: 0.5 (used data-section='social-proof' but contract wasn't explicit about naming)
      - workstream: copy-content
        responsibility: 0.5 (used '## Prova Social' instead of matching attribute name)
    total_cost: 14 tool calls
```

---

## Plan Evolution: v1 -> v2

The Level 3 Global gate failure triggers backtracking (Step 12) and plan evolution.

```yaml
plan_evolution:
  - version: "v1"
    created_at: "Step 9"
    changes: "Initial plan with 3 workstreams (hybrid agent + squad)"
    status: "FAILED at Level 3 Global gate"

  - version: "v2"
    created_at: "Step 12 backtracking"
    trigger: "quality_gate_failed: interface_contract_violation (copy sections naming mismatch)"
    root_cause_analysis: |
      The interface contract between copy-content and landing-page-frontend specified
      that copy Markdown headers should match HTML data-section attributes, but did not
      provide an explicit mapping table. Result: 2 of 6 sections had naming mismatches
      ('social-proof' vs 'Prova Social', 'cta' vs 'Chamada para Acao').
    credit_assignment:
      - landing-page-frontend: 50% (ambiguous attribute naming)
      - copy-content: 50% (did not follow exact English attribute names)
    changes:
      - "ADDED: Explicit section name mapping table to interface contract"
      - "UPDATED: Frontend agent prompt to include exact section-to-header mapping"
      - "ACTION: Frontend agent re-maps 2 mismatched sections (targeted fix, not full re-execution)"
    cost_of_evolution: "4 tool calls (re-read contract, fix 2 sections, re-verify)"
    updated_interface_contract:
      source: copy-content
      target: landing-page-frontend
      contract: |
        Copy delivered as Markdown with EXACT section headers:
        ## Hero           -> data-section="hero"
        ## Proposta de Valor -> data-section="value-props"
        ## Prova Social      -> data-section="social-proof"
        ## Precos            -> data-section="pricing"
        ## CTA               -> data-section="cta"
        ## FAQ               -> data-section="faq"
      format: "Markdown with ## headers"
      mapping_table_added: true
```

### Post-Evolution Verification (v2 gate)

```yaml
quality_gate_results_v2:

  level_3_global:
    status: PASS  # Fixed!
    score: 0.92
    threshold: 0.85
    checks:
      integration_tests_pass: PASS (all sections correctly mapped)
      no_file_conflicts: PASS
      interface_contracts_met: PASS (explicit mapping table resolved mismatches)
      dependency_graph_valid: PASS
    cost: 4 tool calls

  level_4_semantic:
    status: PASS
    score: 0.91
    threshold: 0.88
    checks:
      success_criteria_met: PASS
        details:
          - "Landing page loads in 2.1s: PASS"
          - "Mobile responsive: PASS (tested 320px, 768px, 1024px, 1440px)"
          - "AIDA + PAS frameworks applied: PASS"
          - "SEO Lighthouse: 94/100: PASS"
          - "All sections present: PASS"
          - "WCAG AA contrast: PASS"
          - "Portuguese language: PASS"
      bloom_rubric_passed: PASS
        bloom_level: 6 (Create)
        rubric: novelty_and_coherence
        scores:
          originality: 0.80 (landing page has unique narrative-driven layout)
          coherence: 0.95 (consistent voice, visual style, persuasion flow)
          completeness: 1.0 (all deliverables present)
          feasibility: 1.0 (landing page is fully functional)
          novel_elements: PASS (scroll-triggered reveal animations, narrative structure)
        aggregate: 0.92
        threshold: 0.75
      user_intent_satisfied: PASS
        reasoning: "User asked for landing page with persuasive copy for SaaS launch. Delivered: functional landing page with AIDA/PAS-driven copy, responsive design, SEO optimization."
      quality_bar_met: PASS (0.91 > 0.88 threshold)
      no_scope_creep: PASS
    cost: 5 tool calls

  aggregate:
    passed: true
    total_cost_v2: 9 tool calls (targeted fix + re-verification)
    total_cost_all: 23 tool calls (v1 verification: 14 + v2 fix and verify: 9)
```

---

## Final Cost Summary

| Phase | Tool Calls | Notes |
|-------|-----------|-------|
| Step 0: Triage | 3 | Classification + full analysis start |
| Step 0.5: Discovery | 2 | Skill/agent/squad scan |
| Step 0.7: Registry | 2 | Full registry lookup (skills + agents + squads + MCPs) |
| Steps 1-8: Full Analysis | 6 | Bloom, complexity, decomposition, methodology, resources, hierarchy, hyperparams, mode |
| Step 9: ExecutionPlan | 2 | Full plan generation |
| Step 9.5: Prompt generation | 2 | Agent-handoff + squad-brief |
| Fase 1: Planning | 5 | brainstorming + planning-with-files |
| Fase 2: landing-page-frontend | 18 | Layout, styles, animations, integration |
| Fase 2: copy-content (squad) | 12 | Squad internal execution |
| Fase 2: seo-optimization | 8 | Meta, JSON-LD, performance |
| Step 10: Convergence monitoring | 3 | 3 checkpoint checks |
| Step 11: Verification v1 | 14 | Levels 1-3 (failed at 3) |
| Step 12: Backtracking | 4 | Root cause, credit assignment, targeted fix |
| Step 11: Verification v2 | 9 | Levels 3-4 (all pass) |
| Fase 3: Review | 3 | Code review + final sign-off |
| **Total** | **~93** | Slightly over budget (86 estimated), within emergency reserve |

---

## Key Takeaways for FULL Mode

1. **All 12 Steps execute**: Complete analysis from Bloom level to hyperparameter tuning provides the structure needed for multi-domain coordination.

2. **Hybrid execution mode**: The plan combines agent dispatch (frontend, SEO) with squad delegation (copy). The HRM coordinates across both modes using different protocols (agent-handoff vs squad-brief).

3. **Squad delegation**: Copy workstream is delegated to the Copy Squad, which uses its own internal knowledge base (swipe files, psychology principles, persuasion frameworks). The HRM does not micromanage the squad's process -- it sends a brief and verifies the output.

4. **Plan evolution**: The v1 plan failed at the Level 3 Global gate due to an interface contract ambiguity. The HRM performed root-cause analysis, credit assignment (50/50 between frontend and copy), and produced a targeted fix in v2 rather than re-executing entire workstreams.

5. **Verification cascade all 4 levels**: For `complexity_score >= 6`, all gate levels run including the Semantic level (Level 4), which checks whether the result actually fulfills the user's original intent.

6. **Bloom 6 rubric**: The Create-level rubric evaluates originality, coherence, completeness, and feasibility -- ensuring the landing page is not just technically correct but genuinely novel and polished.

7. **HRM as Supreme Squad Chief**: The HRM remains active throughout execution, monitoring convergence, running quality gates, managing backtracking, and evolving the plan. It is the persistent supervisor that ensures all three workstreams converge into a coherent result.

8. **Credit assignment on failure**: When the Global gate failed, the HRM did not blindly retry everything. It identified the exact cause (contract naming mismatch), assigned responsibility (50/50), and issued a targeted fix costing only 4 tool calls instead of re-executing full workstreams (~40 tool calls).

9. **Interface contracts are critical**: The v1 failure demonstrates why explicit interface contracts (with mapping tables when necessary) are essential for multi-workstream coordination. The v2 fix added an explicit mapping table that prevented further mismatches.

10. **Cost proportional to complexity**: The total ~93 tool calls for a `complexity_score=7.5` task is consistent with the resource calculation model. The 7-tool-call overage came from backtracking, which is normal for complex tasks and covered by the emergency reserve.
