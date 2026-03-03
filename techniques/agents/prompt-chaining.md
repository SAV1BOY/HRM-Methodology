---
id: prompt-chaining
name: "Prompt Chaining"
aliases: ["Sequential Prompting", "Pipeline Prompting", "Multi-Stage Prompting", "Chained Prompts"]
category: agents
family: orchestration
year: 2022
authors: []
paper: null
paper_title: null
venue: null
code: null

complexity: medium
token_cost: variable
latency: high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["complex multi-step tasks", "document processing pipelines", "content transformation workflows", "quality-critical generation", "tasks exceeding single-prompt capability"]
avoid_when: ["simple single-step tasks", "low-latency requirements", "tight token budgets", "tasks with no natural decomposition"]
composes_with: ["chain-of-thought", "tool-augmented-prompting", "few-shot", "self-consistency", "verification"]

tags: ["agents", "orchestration", "pipeline", "sequential", "decomposition", "workflow", "multi-step"]
---

# Prompt Chaining

> **One-line summary:** Decompose a complex task into a sequential pipeline of simpler prompts, where each stage transforms the output of the previous stage into the input for the next.

## Overview

Prompt chaining is the practice of breaking a complex task into a series of smaller, focused sub-tasks, each handled by a dedicated prompt. The output of one prompt becomes the input (or part of the input) to the next prompt in the sequence. This mirrors the software engineering principle of composing simple functions into complex pipelines, and it produces more reliable results than attempting to handle everything in a single monolithic prompt.

The technique emerged organically from the prompt engineering community rather than from a single paper. Practitioners discovered that LLMs perform significantly better when asked to do one thing well rather than many things at once. A single prompt that says "analyze this document, extract key entities, classify sentiment, generate a summary, and produce a formatted report" will almost always underperform compared to five sequential prompts, each handling one of those steps. Each stage can have its own optimized instructions, examples, and output format.

Prompt chaining also enables important engineering benefits: each stage can be independently tested, debugged, and improved. Intermediate outputs can be inspected, cached, or validated. Different stages can use different models (e.g., a fast model for classification, a powerful model for generation). The pipeline can include non-LLM steps like retrieval, code execution, or human review. This makes prompt chaining the backbone of most production LLM applications.

## How It Works

1. **Task Decomposition:** Analyze the overall task and identify natural sub-tasks that can be performed sequentially. Each sub-task should have clear input/output boundaries.
2. **Prompt Design:** Create a dedicated prompt for each stage. Each prompt should focus on a single, well-defined transformation or generation task.
3. **Interface Definition:** Define the output format of each stage to ensure it can be cleanly consumed by the next stage (e.g., JSON, structured text, specific sections).
4. **Pipeline Assembly:** Connect the stages so that each stage's output is parsed, optionally transformed, and fed as input to the next stage.
5. **Execution:** Run the pipeline sequentially, passing outputs through the chain. Optionally include validation or branching logic between stages.

### Diagram

```
┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│  Stage 1  │    │  Stage 2  │    │  Stage 3  │    │  Stage N  │
│  Extract  │───▶│ Transform │───▶│  Enrich   │───▶│  Format   │
│           │    │           │    │           │    │           │
└───────────┘    └───────────┘    └───────────┘    └───────────┘
     │                │                │                │
     ▼                ▼                ▼                ▼
 output_1         output_2         output_3         final_output

Optional: validation gates, branching, or retry logic between stages

     ┌──────────┐
     │ Gate:    │  ← Validation / quality check between stages
     │ Valid?   │
     ├────┬─────┤
     │YES │ NO  │
     └──┬─┘  └──┤
        │       │
        ▼       ▼
     next    retry or
     stage   fallback
```

## Template

**Stage 1 — Extraction:**
```
Extract the following information from the text below:
- Key entities (people, organizations, locations)
- Main claims or arguments
- Numerical data and statistics

Text:
{input_text}

Extracted information (as JSON):
```

**Stage 2 — Analysis:**
```
Given the following extracted information, analyze the relationships between
entities and assess the strength of each claim.

Extracted information:
{stage_1_output}

Analysis:
```

**Stage 3 — Generation:**
```
Using the analysis below, write a {output_format} that {output_requirements}.

Analysis:
{stage_2_output}

Original context:
{input_text}

Output:
```

## Examples

### Example 1: Research Paper to Blog Post Pipeline

**Stage 1 Input (Extract key points):**
```
Extract the 5 most important findings from the following research paper
abstract. For each finding, note: the claim, the evidence, and the
significance. Output as a numbered list.

Abstract:
We present a study of 10,000 software developers examining the impact of
AI coding assistants on productivity. Developers using AI assistants
completed tasks 55% faster on average (p<0.001). Code quality, measured
by bug density, improved by 12% for assisted developers. However, we
observed a 23% decline in developers' ability to explain their own code
when assistants were removed. Junior developers showed the largest
productivity gains (78%) while senior developers gained 34%. The study
controlled for task difficulty, programming language, and developer
experience.

Key findings:
```

**Stage 1 Output:**
```
1. Claim: AI assistants increase task completion speed by 55%.
   Evidence: Study of 10,000 developers, p<0.001.
   Significance: Substantial, statistically significant productivity gain.

2. Claim: Code quality improves by 12% with AI assistance.
   Evidence: Measured by bug density metric.
   Significance: AI doesn't just speed up work, it improves output quality.

3. Claim: Developer code comprehension declines 23% without assistants.
   Evidence: Measured when assistants were removed.
   Significance: Suggests dependency risk and skill atrophy.

4. Claim: Junior developers benefit most (78% gain vs 34% for seniors).
   Evidence: Controlled for task difficulty and experience.
   Significance: AI may be a great equalizer for skill gaps.

5. Claim: Study controlled for confounding variables.
   Evidence: Controls for task difficulty, language, experience.
   Significance: Results are methodologically robust.
```

**Stage 2 Input (Transform to blog narrative):**
```
Transform the following key findings into an engaging blog post outline with
a compelling hook, 3 main sections, and a conclusion. Target audience:
engineering managers.

Key findings:
{stage_1_output}

Blog outline:
```

**Stage 2 Output:**
```
Hook: "Your junior developers might be getting more from AI than your
seniors — and that's both an opportunity and a warning."

Section 1: The Productivity Promise (findings 1, 2)
- 55% faster, 12% fewer bugs — the headline numbers
- What this means for sprint planning and delivery estimates

Section 2: The Hidden Cost (finding 3)
- 23% decline in code comprehension — the dependency trap
- Implications for on-call rotations and code reviews

Section 3: The Great Equalizer (finding 4)
- Junior devs gain 78% — closing the experience gap
- How to leverage this for team composition and mentoring

Conclusion: Embrace AI assistants but invest in comprehension safeguards.
```

### Example 2: Customer Feedback Processing

**Stage 1 Input:**
```
Classify the sentiment and extract the main topic from each customer
feedback item. Output as JSON.

Feedback items:
1. "The new dashboard is incredibly slow. Takes 30 seconds to load."
2. "Love the new export feature! Saved me hours this week."
3. "Why did you remove the dark mode? That was the only reason I upgraded."

JSON output:
```

**Stage 1 Output:**
```json
[
  {"id": 1, "sentiment": "negative", "topic": "dashboard performance",
   "specific_issue": "slow load time (30s)"},
  {"id": 2, "sentiment": "positive", "topic": "export feature",
   "specific_issue": null},
  {"id": 3, "sentiment": "negative", "topic": "dark mode removal",
   "specific_issue": "feature regression"}
]
```

**Stage 2 Input:**
```
Given the classified feedback below, write a summary for the product team
with actionable recommendations prioritized by severity.

Classified feedback:
{stage_1_output}

Product team summary:
```

**Stage 2 Output:**
```
## Feedback Summary

**Critical (P1):** Dashboard performance regression — 30-second load times
reported. This is a usability blocker. Recommend immediate investigation
by the frontend team.

**High (P2):** Dark mode removal caused user dissatisfaction. This was a
valued feature that drove upgrades. Recommend reinstating or communicating
a timeline for return.

**Positive signal:** Export feature is well-received and delivering real
time savings. Consider highlighting in release notes and marketing.
```

## When to Use

- Tasks with natural sequential decomposition (extract -> analyze -> generate)
- When a single prompt produces unreliable or low-quality results
- Document processing pipelines (e.g., parse, classify, summarize, format)
- Quality-critical applications where intermediate validation is needed
- When different stages benefit from different prompt strategies or models
- Building production applications that need maintainability and debuggability

## When to Avoid

- Simple tasks that a single well-crafted prompt can handle
- Real-time applications where multi-call latency is unacceptable
- When the task has no natural decomposition into sequential stages
- Token budgets that cannot accommodate multiple full-context calls
- Exploratory or creative tasks where rigid pipelines constrain output

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 2-5x | Each stage requires full prompt + partial context |
| Latency | N x single-call | Sequential, so latency scales linearly with stages |
| Quality gain | +20-50% | Over single monolithic prompt for complex tasks |
| Reliability | Higher | Each stage is simpler and more predictable |
| API calls | N stages | Typically 2-5 stages for common workflows |
| Debuggability | High | Intermediate outputs can be inspected and tested |

## Variants

- **Branching Chains:** Include conditional logic between stages; different paths based on intermediate results (e.g., route positive vs. negative sentiment to different generation prompts).
- **Parallel Chains:** Run independent sub-tasks in parallel, then merge results in a final stage. Reduces latency for independent stages.
- **Iterative Chains:** Loop a stage until a quality criterion is met (e.g., generate, evaluate, refine, re-evaluate).
- **Human-in-the-Loop Chains:** Insert human review or approval at critical points between stages.
- **Mixed-Model Chains:** Use different models for different stages (e.g., fast model for classification, powerful model for generation).

## Composability

- **Chaining + CoT:** Each stage can use chain-of-thought internally for better reasoning within that step.
- **Chaining + Tool Use:** Individual stages can invoke tools (search, calculate, code execution) as needed.
- **Chaining + Few-Shot:** Each stage can include domain-specific examples tuned for that particular transformation.
- **Chaining + Self-Consistency:** Run multiple instances of a critical stage and take the majority or best output.
- **Chaining + Verification:** Add a dedicated verification stage that checks the output of the previous stage before proceeding.

## Limitations

- Latency scales linearly with the number of stages
- Errors in early stages propagate and compound through the pipeline
- Total token cost is higher than a single-prompt approach
- Defining clean interfaces between stages requires careful design
- Context can be lost between stages unless explicitly passed through
- Over-decomposition (too many stages) adds overhead without quality benefit
- Pipeline rigidity may not handle edge cases that require flexible reasoning

## Sources

- **Community:** Prompt chaining emerged from practitioner experience rather than a single paper
- **Related:** [AI Chains: Transparent and Controllable Human-AI Interaction by Chaining Large Language Model Prompts](https://arxiv.org/abs/2110.01691) — Wu et al., 2022
- **Related:** [Decomposed Prompting: A Modular Approach for Solving Complex Tasks](https://arxiv.org/abs/2210.02406) — Khot et al., 2022
- **Industry:** [LangChain Documentation](https://docs.langchain.com/) — Popular framework for building prompt chains
