---
id: prompt-frameworks
name: "Prompt Frameworks (Mnemonics)"
aliases:
  - prompt-frameworks
  - prompt-mnemonics
  - co-star
  - risen
  - crisp
  - clear-framework
  - rtf
  - tag-framework
  - bab-framework
  - aida-framework
  - pas-framework
  - race-framework
  - care-framework
  - roses-framework
category: foundations
family: instruction-based
year: 2023
authors:
  - Community-developed
paper: null
paper_title: null
venue: null
code: null
complexity: low
token_cost: medium
latency: low
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - structured prompt construction for beginners
  - ensuring completeness of prompt components
  - standardizing prompt engineering across teams
  - marketing and copywriting tasks
  - business communication generation
  - teaching prompt engineering concepts
avoid_when:
  - task is simple enough for a direct instruction
  - framework overhead exceeds the task complexity
  - the mnemonic does not map well to the task domain
  - rapid iteration is needed and framework slows experimentation
  - expert prompt engineers who work more fluidly
composes_with:
  - zero-shot
  - role-prompting
  - output-format
  - prompt-scaffolding
  - context-stuffing
  - few-shot
tags:
  - frameworks
  - mnemonics
  - structured-prompting
  - instruction-based
  - foundational
  - methodology
  - best-practices
---

# Prompt Frameworks (Mnemonics)

> **One-line summary:** Structured mnemonic frameworks (CO-STAR, RISEN, CRISP, CLEAR, RTF, TAG, BAB, AIDA, PAS, RACE, CARE, ROSES) that guide prompt construction by ensuring all critical components -- context, role, instructions, format, audience -- are systematically addressed.

## Overview

Prompt frameworks are structured templates, typically organized as acronym mnemonics, that guide users through constructing comprehensive prompts by ensuring essential components are not overlooked. These frameworks emerged from the prompt engineering community in 2023-2024 as practitioners recognized that prompt quality often suffers not from incorrect instructions but from missing context, undefined roles, or unspecified output requirements. By providing a checklist-style approach, frameworks help both beginners and teams produce consistently well-structured prompts.

The frameworks fall into two broad categories. General-purpose frameworks like CO-STAR, RISEN, CRISP, and CLEAR are designed for any task and emphasize completeness of prompt specification -- ensuring role, context, instructions, and format are all addressed. Domain-specific frameworks like AIDA, PAS, and BAB originated in marketing and copywriting, providing templates optimized for persuasive content generation. Both categories share a common principle: decomposing prompt construction into discrete, named components that can be individually optimized.

It is important to understand that these frameworks are organizational tools for humans, not techniques that fundamentally change how models process prompts. The model does not "understand" the CO-STAR acronym; it simply receives a well-structured prompt with all necessary information. The value lies in ensuring the prompt engineer does not forget critical elements and in standardizing prompt construction across teams. For experienced practitioners, these frameworks often become internalized heuristics rather than rigidly followed templates.

## How It Works

1. **Select the appropriate framework.** Choose a framework based on the task domain and complexity. General frameworks (CO-STAR, RISEN, CLEAR) work for most tasks. Marketing frameworks (AIDA, PAS, BAB) are optimized for persuasive content.

2. **Fill in each component.** Work through each letter/component of the mnemonic, drafting content for each element. Do not skip components -- the framework's value lies in completeness.

3. **Assemble the prompt.** Combine the components into a coherent prompt. The framework provides the structure; the final prompt should read naturally, not as a rigid form.

4. **Review for completeness.** Use the framework as a checklist to verify all elements are present and well-specified.

5. **Iterate and refine.** Test the prompt and adjust individual components based on output quality. The framework makes it easy to identify which component needs improvement.

### Diagram

```
┌─────────────────────────────────────────────┐
│  FRAMEWORK SELECTION                         │
│  (Choose based on task type)                 │
│                                              │
│  General: CO-STAR, RISEN, CRISP, CLEAR       │
│  Marketing: AIDA, PAS, BAB                   │
│  Task-focused: TAG, RTF, RACE, CARE, ROSES   │
├─────────────────────────────────────────────┤
│           ▼                                  │
│  COMPONENT SPECIFICATION                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │  Context  │ │   Role   │ │  Output  │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │   Task   │ │ Audience │ │  Style   │     │
│  └──────────┘ └──────────┘ └──────────┘     │
├─────────────────────────────────────────────┤
│           ▼                                  │
│  ASSEMBLED PROMPT                            │
│  (Components woven into natural instruction) │
├─────────────────────────────────────────────┤
│           ▼                                  │
│  ┌────────────┐                              │
│  │   MODEL    │                              │
│  └─────┬──────┘                              │
│           ▼                                  │
│  STRUCTURED OUTPUT                           │
└─────────────────────────────────────────────┘
```

## Framework Reference

### CO-STAR

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **C**  | Context      | Background information and situational details       |
| **O**  | Objective    | The specific task or goal                            |
| **S**  | Style        | Writing style, tone, or approach                     |
| **T**  | Tone         | Emotional register (formal, casual, empathetic)      |
| **A**  | Audience     | Who will consume the output                          |
| **R**  | Response     | Desired output format and structure                  |

### RISEN

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **R**  | Role         | Persona or expertise the model should adopt          |
| **I**  | Instructions | Clear task directives                                |
| **S**  | Steps        | Ordered procedure to follow                          |
| **E**  | End goal     | What success looks like                              |
| **N**  | Narrowing    | Constraints, boundaries, and exclusions              |

### CRISP

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **C**  | Capacity     | Role or expertise to adopt                           |
| **R**  | Request      | The specific task                                    |
| **I**  | Insight      | Context or background knowledge                     |
| **S**  | Statement    | Desired output format or style                       |
| **P**  | Personality  | Tone and communication approach                      |

### CLEAR

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **C**  | Concise      | Keep instructions brief and direct                   |
| **L**  | Logical      | Structure requests in logical order                  |
| **E**  | Explicit     | State requirements unambiguously                     |
| **A**  | Adaptive     | Allow for flexible responses where appropriate       |
| **R**  | Reflective   | Include verification or self-check instructions      |

### RTF

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **R**  | Role         | Who the model should be                              |
| **T**  | Task         | What needs to be done                                |
| **F**  | Format       | How the output should be structured                  |

### TAG

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **T**  | Task         | The action to perform                                |
| **A**  | Action       | Specific steps or approach                           |
| **G**  | Goal         | Desired outcome or success criteria                  |

### BAB (Before-After-Bridge)

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **B**  | Before       | Current state or problem                             |
| **A**  | After        | Desired future state                                 |
| **B**  | Bridge       | The solution or path from before to after            |

### AIDA (Marketing Classic)

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **A**  | Attention    | Hook that captures reader interest                   |
| **I**  | Interest     | Build engagement with relevant details               |
| **D**  | Desire       | Create emotional motivation                          |
| **A**  | Action       | Clear call-to-action                                 |

### PAS (Problem-Agitate-Solve)

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **P**  | Problem      | Identify the pain point                              |
| **A**  | Agitate      | Amplify the emotional impact of the problem          |
| **S**  | Solve        | Present the solution                                 |

### RACE

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **R**  | Role         | Persona to adopt                                     |
| **A**  | Action       | Task to perform                                      |
| **C**  | Context      | Background information                               |
| **E**  | Execute      | Expected output format and constraints               |

### CARE

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **C**  | Context      | Situational background                               |
| **A**  | Action       | What needs to be done                                |
| **R**  | Result       | Expected outcome or deliverable                      |
| **E**  | Example      | Sample input-output to demonstrate expectations      |

### ROSES

| Letter | Component    | Description                                         |
|--------|-------------|------------------------------------------------------|
| **R**  | Role         | Expertise or persona                                 |
| **O**  | Objective    | Task goal                                            |
| **S**  | Scenario     | Situational context                                  |
| **E**  | Expected     | Desired output format and content                    |
| **S**  | Steps        | Ordered procedure to follow                          |

## Template

**CO-STAR template:**

```
# Context
{background_information}

# Objective
{specific_task}

# Style
{writing_style_description}

# Tone
{emotional_register}

# Audience
{target_audience_description}

# Response Format
{desired_output_format}
```

**RISEN template:**

```
Role: {persona_description}

Instructions: {task_directives}

Steps:
1. {step_1}
2. {step_2}
3. {step_3}

End Goal: {success_criteria}

Narrowing:
- Do NOT {constraint_1}
- Limit to {constraint_2}
- Exclude {constraint_3}
```

**BAB template (marketing):**

```
Write {content_type} using the Before-After-Bridge framework:

Before (Current Problem):
{current_state_or_pain_point}

After (Desired Outcome):
{ideal_future_state}

Bridge (Solution):
{product_or_solution_description}
```

## Examples

### Example 1: CO-STAR for Blog Post Generation

**Input prompt:**
```
Context: Our SaaS company just launched a new AI-powered analytics dashboard that automatically detects anomalies in business metrics and provides natural language explanations of data trends.

Objective: Write a blog post announcing this feature to our existing customers and prospects.

Style: Informative yet engaging. Use concrete examples rather than abstract claims. Include a customer pain point, the solution, and a call-to-action.

Tone: Professional but approachable. Enthusiastic without being hyperbolic.

Audience: Mid-market business analysts and data team leads who currently use our platform for manual reporting.

Response: 800-word blog post with a compelling headline, 3-4 subheadings, one customer quote placeholder, and a CTA button text suggestion.
```

**Expected output:**
A structured 800-word blog post with the specified components, written in a professional-but-approachable tone for a data-savvy business audience, focusing on the anomaly detection feature.

### Example 2: PAS for Email Copy

**Input prompt:**
```
Use the Problem-Agitate-Solve framework to write a sales email for a project management tool targeting overwhelmed engineering managers.

Problem: Engineering managers spend 40% of their time in status meetings and chasing updates across Slack, email, and spreadsheets instead of actually supporting their team.

Agitate: This means delayed decisions, missed deadlines, burned-out engineers who feel micromanaged, and managers who go home exhausted having accomplished nothing strategic. Every week without a solution is another week of firefighting instead of leading.

Solve: ProjectSync automatically aggregates updates from your existing tools (GitHub, Jira, Slack) into a real-time dashboard. Your team updates their work once, and you see everything. Replace 5 weekly status meetings with a 5-minute dashboard review. Free trial, no credit card required.
```

**Expected output:**
A concise sales email that follows the PAS progression naturally, opening with the pain point, building emotional resonance in the middle, and presenting the solution with a clear CTA at the end.

## When to Use

- **Prompt engineering beginners** who benefit from structured guidance to ensure completeness.
- **Team standardization** when multiple people need to write prompts with consistent quality.
- **Complex multi-component tasks** where it is easy to forget critical elements like audience or format.
- **Marketing and copywriting** where frameworks like AIDA and PAS map directly to proven persuasion structures.
- **Prompt reviews and audits** where frameworks serve as checklists for evaluating prompt quality.
- **Training and education** when teaching others how to construct effective prompts.

## When to Avoid

- **Simple, direct tasks** where the framework overhead exceeds the benefit. "Translate this to French" does not need CO-STAR.
- **Expert prompt engineers** who have internalized these principles and work more fluidly without rigid structure.
- **Rapid iteration cycles** where the time to fill in a framework template slows down experimentation velocity.
- **Tasks where the framework is a poor fit** -- not every task maps cleanly to every framework's components.
- **Over-engineering risk** when the framework causes prompts to become unnecessarily verbose or redundant.

## Cost & Performance

| Metric            | Value     | Notes                                                    |
|--------------------|-----------|----------------------------------------------------------|
| Token cost         | Medium    | Framework-structured prompts tend to be 50-200 tokens longer |
| Latency            | Low       | Slightly longer prompts but negligible impact             |
| API calls          | 1         | Single call per task                                      |
| Completeness       | High      | Frameworks ensure no critical component is missing        |
| Consistency        | High      | Standardized structure produces more predictable outputs  |
| Setup effort       | Low       | Choose a framework and fill in components                 |
| Learning curve     | Low       | Mnemonics are designed to be memorable and accessible     |

## Variants

- **Hybrid frameworks:** Combining elements from multiple frameworks (e.g., CO-STAR's audience specification with RISEN's step-by-step approach). Common in practice when a single framework does not fully cover the task.
- **Domain-adapted frameworks:** Modifying framework components for specific domains (e.g., replacing "Audience" with "Patient Population" for healthcare prompt engineering).
- **Nested frameworks:** Using one framework for the overall prompt structure and another for a specific component (e.g., using RISEN for the overall prompt but AIDA within the instructions for a marketing task).
- **Minimal frameworks:** RTF and TAG represent minimal three-component frameworks for situations where full frameworks are overkill but some structure is helpful.

## Composability

- **+ Zero-Shot:** Most frameworks naturally produce zero-shot prompts -- they structure the instruction without requiring examples.
- **+ Role Prompting:** Most frameworks include a Role component (RISEN, RACE, ROSES, RTF). The framework simply formalizes what role prompting does informally.
- **+ Output Format Control:** The Response/Format/Expected components in frameworks like CO-STAR, RTF, and ROSES map directly to output format control.
- **+ Few-Shot:** The CARE framework explicitly includes an Example component. Other frameworks can be extended by adding examples after the assembled prompt.
- **+ Context Stuffing:** The Context component in CO-STAR, CARE, and RACE is where injected documents or retrieved chunks naturally fit.
- **+ Prompt Scaffolding:** Framework components can be wrapped in XML tags or delimiters, combining the organizational benefits of frameworks with the structural clarity of scaffolding.

## Limitations

- **False sense of completeness.** Filling in all framework fields does not guarantee prompt quality. The content within each field matters more than the structural completeness.
- **One-size-fits-all fallacy.** No single framework is optimal for all tasks. Marketing frameworks (AIDA, PAS) are poorly suited for technical tasks, and general frameworks may be too generic for specialized domains.
- **Verbosity overhead.** Framework-structured prompts tend to be longer than organically constructed prompts, consuming more tokens without necessarily improving output quality.
- **Rigidity.** Strict adherence to a framework can prevent creative or unconventional prompt constructions that might be more effective for unusual tasks.
- **No empirical validation.** Unlike techniques such as chain-of-thought or few-shot prompting, prompt frameworks have not been validated through rigorous academic research. Their effectiveness is based on practitioner experience rather than controlled experiments.
- **Framework proliferation.** The growing number of acronym frameworks (there are dozens beyond the 12 documented here) creates confusion about which to use, with significant overlap between frameworks.

## Sources

**Primary:**
- Sheila Teo. (2024). "How I Won Singapore's GPT-4 Prompt Engineering Competition." Towards Data Science. https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41

**Secondary:**
- Anthropic. (2023-2024). "Prompt Engineering Guide." https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- OpenAI. (2023-2024). "Prompt Engineering Best Practices." https://platform.openai.com/docs/guides/prompt-engineering
- Cialdini, R.B. (2006). "Influence: The Psychology of Persuasion." Harper Business. (Origin of AIDA, PAS frameworks in marketing context)
- Google DeepMind. (2024). "Prompting Guide for Gemini." https://ai.google.dev/gemini-api/docs/prompting-intro
