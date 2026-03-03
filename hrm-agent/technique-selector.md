# HRM Agent: Technique Selector

> The algorithm the HRM Agent uses to analyze a task, score candidate techniques, and select the optimal set for pipeline construction.

---

## Overview

The Technique Selector is the core intelligence of the HRM Agent. Given a user's task, it must answer: **which prompt engineering techniques should be applied, and in what order?**

The selection process has four phases:

```
User Task
    │
    ▼
┌──────────────────┐
│ Phase 1: Analyze  │  Classify the task and extract constraints
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 2: Filter   │  Remove techniques that violate constraints
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 3: Score    │  Rank remaining techniques by fit
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 4: Compose  │  Select a compatible set and order them
└──────────────────┘
```

---

## Phase 1: Task Analysis

The agent analyzes the user's task and produces a structured task profile.

### Task Profile Schema

```yaml
task_profile:
  raw_input: "The original user request"

  # Classification
  primary_type: reasoning | code | creative | extraction | summarization |
                classification | agent | rag | translation | other
  secondary_types: [list of additional applicable types]

  # Complexity assessment
  complexity: simple | moderate | complex
  num_subtasks: integer  # estimated number of sub-problems
  requires_external_info: boolean
  requires_tool_use: boolean

  # Quality requirements (inferred or specified)
  quality_level: casual | standard | high | critical
  accuracy_importance: low | medium | high  # is factual correctness crucial?
  creativity_importance: low | medium | high  # is creative quality crucial?

  # Constraints
  latency_budget: fast (<5s) | moderate (5-30s) | relaxed (30s+) | async
  token_budget: minimal | low | medium | high | unlimited
  num_calls_budget: 1 | few (2-5) | moderate (5-15) | unlimited

  # Context
  has_examples: boolean  # did the user provide examples?
  has_context: boolean   # is there retrieved/injected context?
  tools_available: [list of available tool types]
  output_format: free | structured | json | code | table
```

### Analysis Prompt

The agent uses this prompt to analyze the task:

```
Analyze the following task and produce a structured task profile.

TASK:
{user_task}

Classify the task along these dimensions:
1. PRIMARY TYPE: What kind of task is this? (reasoning, code, creative,
   extraction, summarization, classification, agent, rag)
2. COMPLEXITY: How many distinct reasoning steps or sub-problems are
   involved? (simple=1, moderate=2-4, complex=5+)
3. QUALITY LEVEL: Based on the user's intent, how important is output
   quality? (casual, standard, high, critical)
4. CONSTRAINTS: Infer any latency, cost, or format constraints from
   the request context.
5. REQUIREMENTS: Does this task need external information, tool use,
   specific expertise, or a particular output format?

Output the task profile as YAML.
```

---

## Phase 2: Constraint Filtering

Load all 75 techniques from `taxonomy.yaml` and eliminate those that violate hard constraints.

### Filter Rules

```
FOR each technique IN taxonomy.yaml:

  # Filter 1: Complexity ceiling
  IF task.complexity == "simple" AND technique.complexity == "high":
    ELIMINATE (overkill for simple tasks)

  # Filter 2: Latency budget
  IF task.latency_budget == "fast" AND technique.num_calls > 1:
    ELIMINATE (too many calls for fast response)

  # Filter 3: Token budget
  IF task.token_budget == "minimal" AND technique.token_cost IN ["high", "very_high"]:
    ELIMINATE (exceeds token budget)

  # Filter 4: Tool requirements
  IF technique.requires_tools == true AND task.tools_available == []:
    ELIMINATE (no tools available)

  # Filter 5: Training requirements
  IF technique.requires_training == true AND no_training_infrastructure:
    ELIMINATE (cannot train)

  # Filter 6: Example requirements
  IF technique.requires_examples == true AND task.has_examples == false:
    DEPRIORITIZE (not eliminate — agent may generate synthetic examples)

  # Filter 7: Avoid-when match
  IF task matches any item in technique.avoid_when:
    ELIMINATE (technique explicitly advises against this use case)
```

### Filter Output

A reduced candidate list, typically 20-40 techniques out of 75.

---

## Phase 3: Technique Scoring

Score each remaining technique on a 0-100 scale across multiple dimensions, then compute a weighted total.

### Scoring Dimensions

```
FOR each candidate technique:

  # Score 1: Task Fit (weight: 0.35)
  task_fit = 0
  FOR each item IN technique.best_for:
    IF item matches task.primary_type or task.secondary_types:
      task_fit += 25
    IF item matches task description keywords:
      task_fit += 10
  task_fit = min(task_fit, 100)

  # Score 2: Quality Impact (weight: 0.25)
  quality_impact = BASE_QUALITY_SCORE[technique.category]
  # Reasoning techniques: 70-90
  # Verification techniques: 60-80
  # Foundation techniques: 40-60
  # Agent techniques: 50-70
  IF task.quality_level == "critical":
    quality_impact *= 1.2  # bonus for verification/refinement techniques
  IF task.quality_level == "casual":
    quality_impact *= 0.8  # penalty for expensive techniques

  # Score 3: Efficiency (weight: 0.20)
  efficiency = 100
  IF technique.token_cost == "high": efficiency -= 30
  IF technique.token_cost == "very_high": efficiency -= 50
  IF technique.num_calls > 5: efficiency -= 20
  IF task.latency_budget == "fast" AND technique.latency != "low":
    efficiency -= 30

  # Score 4: Composability (weight: 0.15)
  composability = len(technique.composes_with) * 10
  composability = min(composability, 100)
  # Bonus if composes_with includes other high-scoring candidates

  # Score 5: Familiarity (weight: 0.05)
  # Techniques the agent has used successfully before get a bonus
  familiarity = memory.success_rate(technique.id) * 100

  # Total score
  total = (task_fit * 0.35) + (quality_impact * 0.25) +
          (efficiency * 0.20) + (composability * 0.15) +
          (familiarity * 0.05)
```

### Scoring Output

A ranked list of candidate techniques with scores, typically selecting the top 3-7.

---

## Phase 4: Pipeline Composition

Select a compatible subset of top-scoring techniques and arrange them into a pipeline.

### Composition Rules

```
1. PLAYBOOK CHECK: Before building a custom pipeline, check if a
   pre-built playbook matches:
   - Research → playbooks/research-and-analysis.md
   - Code → playbooks/code-generation.md
   - Creative → playbooks/creative-writing.md
   - Extraction → playbooks/data-extraction.md
   - Agent → playbooks/agent-orchestration.md
   - RAG → playbooks/rag-pipeline.md

   If a playbook matches with >80% technique overlap, use it directly.

2. ORDERING: Techniques must follow a logical flow:
   a. Context setup (Role, Context Stuffing, Step-Back)
   b. Reasoning (CoT, ToT, PoT, Plan-and-Solve)
   c. Generation (the main output production)
   d. Verification (CoVe, Self-Refine, Checklist)
   e. Formatting (Output Format Control)

3. COMPATIBILITY: Check composes_with metadata:
   FOR each pair (technique_i, technique_j) in selected set:
     IF technique_i.id NOT IN technique_j.composes_with:
       WARN (untested composition — proceed with caution)
     IF technique_i CONFLICTS with technique_j:
       REMOVE lower-scoring technique

4. BUDGET CHECK: Estimate total pipeline cost:
   total_calls = SUM(technique.num_calls for all selected)
   total_tokens = SUM(estimated_tokens for all selected)
   IF total_calls > task.num_calls_budget: TRIM lowest-value technique
   IF total_tokens > task.token_budget: TRIM lowest-value technique

5. DIMINISHING RETURNS: Do not add a 5th technique if the estimated
   quality gain is < 5% over 4 techniques.
```

### Composition Output

A finalized pipeline definition:

```yaml
pipeline:
  name: "Custom pipeline for: {task_summary}"
  based_on_playbook: null | "playbook_name"
  steps:
    - order: 1
      technique: "step-back-prompting"
      template: "templates/reasoning/step-back.yaml"
      input: "{user_task}"
      purpose: "Extract high-level principles"
    - order: 2
      technique: "chain-of-thought"
      template: "templates/reasoning/chain-of-thought.yaml"
      input: "{step_1_output}"
      purpose: "Systematic reasoning through the problem"
    - order: 3
      technique: "self-refine"
      template: "templates/verification/self-refine.yaml"
      input: "{step_2_output}"
      purpose: "Iterative quality improvement"
  estimated_cost:
    api_calls: 5
    tokens: 4500
    latency_seconds: 25
```

---

## Decision Trace

For transparency, the agent logs its selection reasoning:

```
SELECTION TRACE:
Task: "Research the impact of MoE architectures on LLM scaling"
Task Profile: type=reasoning, complexity=complex, quality=high

Phase 2 — Filtered: 75 → 34 candidates
  Eliminated: prompt-tuning (requires training), tree-of-thoughts
  (not a search problem), program-of-thoughts (not code)

Phase 3 — Top scores:
  1. step-back-prompting: 87 (task_fit=90, quality=80, efficiency=85)
  2. chain-of-thought: 85 (task_fit=85, quality=85, efficiency=90)
  3. chain-of-verification: 78 (task_fit=70, quality=90, efficiency=65)
  4. self-refine: 76 (task_fit=70, quality=85, efficiency=70)
  5. output-format: 72 (task_fit=60, quality=60, efficiency=100)

Phase 4 — Composition:
  Playbook match: research-and-analysis.md (100% overlap)
  Using playbook pipeline directly.
```
