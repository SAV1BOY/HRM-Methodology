---
id: planner-worker-solver
name: "Planner-Worker-Solver"
aliases: ["Plan-Execute-Solve", "PWS", "Multi-Agent Decomposition", "Planner-Executor Pattern"]
category: agents
family: orchestration
year: 2023
authors: []
paper: null
paper_title: null
venue: null
code: null

complexity: high
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for:
  - "complex multi-step research tasks"
  - "tasks requiring diverse expertise"
  - "long-horizon planning problems"
  - "workflows with heterogeneous sub-tasks"
  - "enterprise automation pipelines"
avoid_when:
  - "simple tasks solvable in 1-2 steps"
  - "tight latency constraints"
  - "insufficient budget for many LLM calls"
  - "sub-tasks are not clearly separable"
composes_with:
  - "chain-of-thought"
  - "tool-augmented-prompting"
  - "prompt-chaining"
  - "memory-prompting"
  - "self-consistency"

tags: ["agents", "orchestration", "multi-agent", "planning", "decomposition", "coordination"]
---

# Planner-Worker-Solver

> **One-line summary:** A three-role multi-agent orchestration pattern where a Planner decomposes a complex task into sub-tasks, specialized Workers execute each sub-task independently, and a Solver integrates the results into a coherent final output.

## Overview

The Planner-Worker-Solver (PWS) pattern is a multi-agent orchestration strategy inspired by classic divide-and-conquer algorithms and modern software engineering practices like the manager-worker pattern. It addresses the fundamental challenge that complex, open-ended tasks often exceed the reliable capability of a single LLM call --- or even a simple linear chain of calls. By introducing three distinct roles with clear responsibilities, PWS creates a structured framework for tackling tasks that require planning, diverse execution, and synthesis.

The pattern's power comes from the separation of concerns across three roles. The Planner operates at a strategic level, analyzing the overall task and producing a structured decomposition into well-defined sub-tasks with clear inputs, outputs, and dependencies. Workers are tactical executors --- each handles one specific sub-task and can be specialized with different system prompts, tools, models, or temperature settings. The Solver operates at an integrative level, combining all Worker outputs while resolving conflicts, filling gaps, and ensuring coherence. This separation allows each role to be independently optimized and debugged.

PWS is widely used in production systems for tasks like comprehensive research reports, complex document analysis, multi-step data processing, and enterprise workflow automation. Frameworks such as LangGraph, CrewAI, and AutoGen provide direct support for this pattern. The approach scales naturally: simple tasks might use one planner call, two worker calls, and one solver call, while complex tasks can involve dozens of workers operating in parallel with multiple planning and solving rounds.

## How It Works

1. **Planning Phase (Planner):** The Planner receives the original task and produces a structured execution plan. This plan lists each sub-task with its description, required inputs, expected output format, dependencies on other sub-tasks, and execution order.
2. **Dispatch:** The orchestration layer parses the Planner's output and dispatches each sub-task to an appropriate Worker. Independent sub-tasks can run in parallel.
3. **Execution Phase (Workers):** Each Worker receives its sub-task description, any relevant context, and the outputs of upstream sub-tasks it depends on. Workers execute independently, potentially using tools or specialized prompts.
4. **Collection:** The orchestration layer collects all Worker outputs and packages them for the Solver.
5. **Integration Phase (Solver):** The Solver receives the original task, the plan, and all Worker outputs. It synthesizes them into a coherent final deliverable, resolving any contradictions or redundancies.
6. **Validation (Optional):** The final output can be validated against the original requirements, potentially triggering a re-plan if quality criteria are not met.

### Diagram

```
                    ┌──────────────────┐
                    │   ORIGINAL TASK  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     PLANNER      │
                    │  Decompose into  │
                    │  sub-tasks with  │
                    │  dependencies    │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    │   TASK PLAN     │
                    │  1. Sub-task A  │
                    │  2. Sub-task B  │
                    │  3. Sub-task C  │
                    └───┬────┬────┬───┘
                        │    │    │
             ┌──────────┘    │    └──────────┐
             ▼               ▼               ▼
      ┌────────────┐  ┌────────────┐  ┌────────────┐
      │  WORKER A  │  │  WORKER B  │  │  WORKER C  │
      │ (research) │  │ (analyze)  │  │ (generate) │
      └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
            │               │               │
            └───────┬───────┴───────┬───────┘
                    │               │
                    ▼               │
           ┌────────────────┐      │
           │    SOLVER      │◄─────┘
           │  Integrate all │
           │  worker outputs│
           │  into final    │
           │  deliverable   │
           └───────┬────────┘
                   │
                   ▼
           ┌────────────────┐
           │  FINAL OUTPUT  │
           └────────────────┘
```

## Template

**Planner Prompt:**
```
You are a task planner. Given a complex task, decompose it into a list of
concrete, actionable sub-tasks. For each sub-task, specify:
- A short ID (e.g., "task_1")
- A clear description of what needs to be done
- Required inputs (from the original task or from other sub-tasks)
- Expected output format
- Dependencies (which other sub-tasks must complete first)

Task:
{original_task}

Output the plan as a numbered list of sub-tasks.
```

**Worker Prompt:**
```
You are a specialist executing a specific sub-task. Complete the following
task using only the information provided. Be thorough and precise.

Sub-task:
{subtask_description}

Context from prior steps:
{dependency_outputs}

Additional context:
{relevant_context}

Your output:
```

**Solver Prompt:**
```
You are an integrator. Given the original task and the outputs from
multiple specialist workers, synthesize a coherent final deliverable.
Resolve any contradictions, fill gaps, and ensure the output fully
addresses the original task.

Original task:
{original_task}

Plan:
{execution_plan}

Worker outputs:
{all_worker_outputs}

Final integrated output:
```

## Examples

### Example 1: Competitive Analysis Report

**Planner Input:**
```
You are a task planner. Decompose the following task into sub-tasks.

Task: Write a competitive analysis comparing Slack, Microsoft Teams,
and Discord for enterprise use. Cover features, pricing, integrations,
and security. Provide a recommendation for a 500-person company.
```

**Planner Output:**
```
1. task_1: Research Slack's enterprise features, pricing tiers,
   integration ecosystem, and security certifications.
   Inputs: none. Output: structured feature summary.

2. task_2: Research Microsoft Teams' enterprise features, pricing
   tiers, integration ecosystem, and security certifications.
   Inputs: none. Output: structured feature summary.

3. task_3: Research Discord's enterprise features, pricing tiers,
   integration ecosystem, and security certifications.
   Inputs: none. Output: structured feature summary.

4. task_4: Create a comparison matrix across all three platforms
   on features, pricing, integrations, and security.
   Inputs: task_1, task_2, task_3. Output: comparison table.
   Dependencies: task_1, task_2, task_3.

5. task_5: Write a recommendation for a 500-person company based
   on the comparison analysis.
   Inputs: task_4. Output: recommendation paragraph.
   Dependencies: task_4.
```

**Worker 1 (Slack Research) Output:**
```
Slack Enterprise Grid:
- Features: Channels, threads, huddles, canvas, workflow builder,
  unlimited message history
- Pricing: $12.50/user/month (Business+), custom (Enterprise Grid)
- Integrations: 2,600+ apps in marketplace, open API
- Security: SOC 2, ISO 27001, HIPAA eligible, Enterprise Key Management
```

**Solver Input (after all workers):**
```
Original task: Write a competitive analysis comparing Slack, Teams,
and Discord for enterprise use...

Worker outputs:
[Worker 1: Slack summary]
[Worker 2: Teams summary]
[Worker 3: Discord summary]
[Worker 4: Comparison matrix]
[Worker 5: Draft recommendation]

Synthesize into a final report.
```

### Example 2: Codebase Migration Planning

**Planner Output for "Migrate a React class-component codebase to hooks":**
```
1. task_1: Inventory all class components and categorize by complexity
   (simple state, lifecycle methods, HOC wrappers).
2. task_2: For each complexity category, provide migration patterns
   with before/after code examples.
3. task_3: Identify shared state patterns and recommend Context API
   or state management library approach.
4. task_4: Create a migration priority order based on dependency graph
   and risk assessment.
5. task_5: Write a testing strategy to validate each migrated component.
```

**Solver Output (integrated):**
```
# React Class-to-Hooks Migration Plan

## 1. Component Inventory
[Integrated from Worker 1: categorized list of components]

## 2. Migration Patterns
[Integrated from Worker 2: patterns with code examples]

## 3. State Management Strategy
[Integrated from Worker 3: Context API recommendations]

## 4. Migration Priority
[Integrated from Worker 4: ordered migration schedule]

## 5. Testing Strategy
[Integrated from Worker 5: testing approach per component type]

## Estimated Timeline
Based on the inventory of 47 class components (12 simple, 25 medium,
10 complex), estimated migration effort is 3-4 weeks for a team of
two developers.
```

## When to Use

- The task involves multiple distinct types of work (research, analysis, writing, coding)
- Sub-tasks can benefit from different specializations, tools, or model configurations
- The task is too complex for a single prompt to handle reliably
- Parallel execution of independent sub-tasks would significantly reduce wall-clock time
- You need a clear audit trail showing how the final output was constructed
- The decomposition itself is valuable (e.g., project planning, resource allocation)

## When to Avoid

- The task is straightforward enough for a linear chain of 2-3 prompts
- Latency budget does not allow for planning + execution + integration overhead
- The sub-tasks are so tightly coupled that they cannot be executed independently
- Budget constraints prevent the multiple LLM calls required
- The task does not naturally decompose into distinct sub-tasks

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 3-10x | Plan + multiple worker contexts + solver synthesis |
| Latency | 3-10x | Sequential: plan + execute + solve. Parallel workers help |
| Quality gain | +25-50% | On complex tasks vs. single prompt or simple chaining |
| API calls | 5-20+ | 1 planner + N workers + 1 solver (+ optional validation) |
| Parallelism | High | Independent workers can execute simultaneously |
| Debuggability | Very high | Each role's output can be inspected independently |

## Variants

- **Iterative PWS:** The Solver identifies gaps and triggers a re-plan, creating a loop: Plan -> Work -> Solve -> Re-Plan -> Work -> Solve until quality criteria are met.
- **Hierarchical PWS:** The Planner creates high-level sub-tasks, each of which is further decomposed by sub-planners, creating a tree of workers.
- **Adaptive PWS:** The orchestration layer dynamically adjusts the plan based on Worker outputs --- if a Worker discovers the sub-task is more complex than expected, it can request decomposition.
- **Specialized Solver:** Instead of a general-purpose Solver, use a domain-specific integration prompt tailored to the output type (e.g., report assembly, code merging, data reconciliation).
- **Human-in-the-Loop PWS:** Insert human review gates after the Planner and/or Solver steps for high-stakes applications.

## Composability

- **PWS + Tool Use:** Workers can each have access to different tool sets --- a research worker uses search, a data worker uses SQL, a code worker uses a sandbox.
- **PWS + Chain-of-Thought:** Workers use CoT for complex reasoning within their sub-tasks while the overall structure remains managed by the PWS pattern.
- **PWS + Memory:** Store sub-task results in persistent memory so that subsequent runs can skip completed sub-tasks (checkpointing).
- **PWS + Self-Consistency:** Run critical workers multiple times with self-consistency voting to improve reliability of individual sub-task outputs.
- **PWS + Prompt Chaining:** Individual workers may internally use prompt chaining for their sub-tasks, nesting patterns within patterns.

## Limitations

- High token and latency cost due to the overhead of planning, multiple worker calls, and integration
- The Planner may produce poor decompositions --- garbage-in at the plan level cascades through the entire pipeline
- Worker outputs may be inconsistent in format or quality, making the Solver's job harder
- Coordination overhead: managing dependencies, passing context, and handling failures adds engineering complexity
- The pattern can be over-engineered for tasks that do not truly require this level of decomposition
- Information loss between roles: the Solver only sees Worker outputs, not the full context each Worker processed

## Sources

- **Related:** [HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face](https://arxiv.org/abs/2303.17580) --- Shen et al., 2023
- **Related:** [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) --- Wu et al., 2023
- **Framework:** [LangGraph: Multi-Actor Applications with LLMs](https://github.com/langchain-ai/langgraph) --- LangChain, 2024
- **Framework:** [CrewAI: Framework for Orchestrating Role-Playing AI Agents](https://github.com/crewAIInc/crewAI) --- Moura, 2024
- **Related:** [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091) --- Wang et al., 2023
