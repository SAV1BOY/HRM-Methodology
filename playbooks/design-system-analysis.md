# Playbook: Design System Analysis

> Pre-built technique pipeline for analyzing and designing component-based design systems. Triggered when DOMINIO in [DESIGN, WEB, REACT] and task involves design system work.

---

## Trigger Conditions

- DOMINIO in [DESIGN, WEB, REACT]
- Keywords: "design system", "component library", "design tokens", "UI architecture"
- TIPO in [REVIEW, BUILD, PLAN] with design system context

---

## Technique Pipeline

### Phase 1: Abstraction (step-back-prompting)

**Purpose**: Establish fundamental design principles before diving into details.

**Prompt pattern**:
```
Before analyzing the specific components, step back and consider:
1. What design principles should govern this system?
2. What consistency problems typically arise in systems of this scale?
3. What token architecture best supports the stated goals?
```

**Expected output**: List of governing principles and architectural decisions.

### Phase 2: Systematic Analysis (chain-of-thought)

**Purpose**: Walk through each layer of the design system methodically.

**Prompt pattern**:
```
Analyze the design system layer by layer:

Layer 1 — Tokens:
  - List all token categories (color, spacing, typography, etc.)
  - Check for consistency within each category
  - Identify gaps or redundancies

Layer 2 — Primitives:
  - List atomic components (Button, Input, Text, etc.)
  - Check API consistency across primitives
  - Verify accessibility built into each

Layer 3 — Compounds:
  - List compound components (Card, Modal, Form, etc.)
  - Check composition patterns
  - Verify they compose from primitives correctly

Layer 4 — Patterns:
  - List layout and interaction patterns
  - Check responsive behavior
  - Verify animation/motion patterns
```

**Expected output**: Structured analysis per layer with findings.

### Phase 3: Comparative Reference (analogical-prompting)

**Purpose**: Compare against best-practice design systems to identify gaps.

**Prompt pattern**:
```
Compare this system against reference systems:
- Token architecture vs Material Design 3
- Component API design vs Radix UI
- Accessibility vs Chakra UI
- Developer experience vs shadcn/ui

For each comparison, identify:
1. What this system does well
2. What it could adopt from the reference
3. Migration effort if adoption is recommended
```

**Expected output**: Gap analysis with actionable recommendations.

### Phase 4: Verification (checklist-prompting)

**Purpose**: Verify completeness against quality criteria.

**Checklist**:
```
Token Layer:
  [ ] All colors use tokens (no raw hex values)
  [ ] Color contrast meets WCAG AA
  [ ] Spacing uses consistent base unit
  [ ] Typography uses mathematical scale
  [ ] Semantic tokens exist for all use cases

Component Layer:
  [ ] Every component has documentation
  [ ] Props are consistent across similar components
  [ ] All interactive elements are keyboard accessible
  [ ] ARIA attributes are correct
  [ ] Components support theming via tokens

Pattern Layer:
  [ ] Responsive breakpoints are defined
  [ ] Layout patterns are documented
  [ ] Animation respects prefers-reduced-motion
  [ ] Error states are defined for all forms

System Level:
  [ ] No duplicate components serving same purpose
  [ ] Composition patterns are documented
  [ ] Version strategy exists
  [ ] Migration guides exist for breaking changes
```

**Expected output**: Checklist results with pass/fail per item.

### Phase 5: Multi-Perspective Review (optional, for complex systems)

**Purpose**: Evaluate from different stakeholder perspectives.

Uses **multi-agent-debate** or **simtom** technique:

```
Evaluate this design system from three perspectives:
1. DEVELOPER: Is it easy to use? Good DX? Clear API?
2. DESIGNER: Does it preserve design intent? Flexible enough?
3. USER: Is it accessible? Performant? Consistent?

For each perspective, rate 1-10 and list top 3 concerns.
```

**Expected output**: Multi-perspective evaluation with prioritized concerns.

---

## Pipeline Configuration

```yaml
pipeline:
  name: "design-system-analysis"
  techniques:
    - id: step-back-prompting
      phase: 1
      required: true
      cost: 2
    - id: chain-of-thought
      phase: 2
      required: true
      cost: 5
    - id: analogical-prompting
      phase: 3
      required: true
      cost: 3
    - id: checklist-prompting
      phase: 4
      required: true
      cost: 2
    - id: multi-agent-debate
      phase: 5
      required: false
      condition: "complexity_score >= 5"
      cost: 8
  total_cost:
    min: 12
    max: 20
  quality_threshold: 0.85
```

---

## Integration with HRM

- **Registry entry**: `registry/playbooks.yaml` -> `design-system-analysis`
- **Technique mapper**: L-Architect + DESIGN domain triggers this playbook
- **Quality gate**: Uses design domain threshold (0.85)
- **Reference**: See `references/design-systems-analysis.md` for detailed knowledge
