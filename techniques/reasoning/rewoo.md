---
id: rewoo
name: ReWOO
aliases:
  - Reasoning WithOut Observation
  - rewoo
  - plan-then-execute agent
category: reasoning
family: tool-use
year: 2023
authors:
  - Binfeng Xu
  - Zhiyuan Peng
  - Bowen Lei
  - Subhabrata Mukherjee
  - Yuchen Liu
  - Dongkuan Xu
paper: https://arxiv.org/abs/2305.18323
paper_title: "ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models"
venue: arXiv 2023
code: https://github.com/billxbf/ReWOO
complexity: medium
token_cost: medium
latency: medium
num_calls: variable
requires_examples: true
requires_tools: true
requires_training: false
model_agnostic: true
best_for:
  - multi-tool tasks where actions can be planned upfront
  - reducing token cost compared to ReAct
  - parallelizable tool calls
  - tasks with predictable tool-use patterns
  - production agent systems optimizing for efficiency
avoid_when:
  - tasks requiring adaptive tool use based on intermediate results
  - highly dynamic environments with unpredictable observations
  - tasks where the next action depends critically on previous observations
  - single-tool simple lookups
composes_with:
  - react
  - chain-of-thought
  - plan-and-solve
  - self-consistency
tags:
  - tool-use
  - reasoning
  - planning
  - efficiency
  - agent
  - parallel-execution
---

# ReWOO

> Decouple reasoning from observation by planning all tool calls upfront, then executing them in batch, and finally synthesizing results -- eliminating redundant token processing in each loop iteration.

## Overview

ReWOO (Reasoning WithOut Observation), introduced by Xu et al. (2023), addresses a fundamental inefficiency in the ReAct paradigm: the repeated processing of the entire prompt context at every reasoning step. In ReAct, each Thought-Action-Observation cycle requires a full LLM call that includes all previous thoughts, actions, and observations in the prompt, leading to rapidly growing token costs as the conversation lengthens. ReWOO solves this by decoupling the planning phase from the execution phase, creating a three-module architecture: Planner, Worker, and Solver.

The Planner module generates the complete reasoning plan upfront, including all tool calls that will be needed, with placeholder variables for the tool outputs. The Worker module then executes all tool calls, potentially in parallel, filling in the placeholder values. Finally, the Solver module takes the original question, the plan, and all collected evidence to synthesize the final answer in a single LLM call. This architecture dramatically reduces token consumption because the full context is only processed twice (once for planning, once for solving) rather than at every step of an iterative loop.

The efficiency gains of ReWOO are substantial. The authors demonstrated a 5x reduction in token usage compared to ReAct on HotpotQA while achieving comparable accuracy. Beyond token savings, the decoupled architecture enables parallel execution of tool calls since the plan specifies all calls upfront. This can significantly reduce wall-clock latency in production systems. ReWOO also gracefully degrades when the model makes planning mistakes -- the Solver can often compensate for imperfect plans by reasoning about the collected evidence at the synthesis stage. The approach represents a shift from reactive agent design (sense-plan-act at each step) to proactive agent design (plan everything, then act, then synthesize).

## How It Works

1. **Planner**: The LLM generates a complete plan consisting of interleaved reasoning steps and tool calls. Each tool call output is assigned a placeholder variable (e.g., #E1, #E2) that subsequent steps can reference.
2. **Worker**: The system executes all tool calls from the plan, substituting placeholder references with actual results from earlier tool calls. Tools can be executed in parallel when they have no dependencies.
3. **Solver**: The LLM receives the original question, the plan, and all tool results (evidence), and synthesizes the final answer in a single pass.

### Diagram

```
┌──────────────────────────────────────────────────────┐
│                     PLANNER                          │
│  (Single LLM call)                                   │
│                                                      │
│  Plan:                                               │
│  #P1: I need to find who directed Inception.         │
│  #E1 = Search["director of Inception"]               │
│  #P2: Now find where this director was born.         │
│  #E2 = Search["birthplace of #E1"]                   │
│  #P3: Find the population of that city.              │
│  #E3 = Search["population of #E2"]                   │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│                     WORKER                           │
│  (Tool execution -- potentially parallel)            │
│                                                      │
│  #E1 = Search["director of Inception"]               │
│       -> "Christopher Nolan"                         │
│  #E2 = Search["birthplace of Christopher Nolan"]     │
│       -> "London, England"                           │
│  #E3 = Search["population of London, England"]       │
│       -> "8.8 million (2023)"                        │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│                     SOLVER                           │
│  (Single LLM call)                                   │
│                                                      │
│  Question: What is the population of the birthplace  │
│  of the director of Inception?                       │
│                                                      │
│  Evidence:                                           │
│  #E1: Christopher Nolan                              │
│  #E2: London, England                                │
│  #E3: 8.8 million (2023)                             │
│                                                      │
│  Answer: The director of Inception is Christopher    │
│  Nolan, who was born in London, England. London has  │
│  a population of approximately 8.8 million.          │
└──────────────────────────────────────────────────────┘
```

## Template

### Planner Prompt

```
For the following task, make a plan that can solve the problem step by step. For each plan, indicate which external tool together with tool input to retrieve evidence. You can store the evidence into a variable #E that can be called by later tools.

Tools available:
{tool_descriptions}

{exemplar_1_with_plan}

{exemplar_2_with_plan}

Task: {test_question}
Plan:
```

### Solver Prompt

```
Solve the following task or problem. To assist you, we provide some plans and corresponding evidences that might be helpful. Notice that some of these evidences may contain irrelevant information. Use your best judgment to solve the task.

Task: {test_question}

{plan_with_evidence_filled_in}

Now solve the task. Response:
```

## Examples

### Example 1: Multi-Hop Question Answering

**Planner Input:**
```
Task: What is the capital of the country where the inventor of the telephone was born?
Plan:
```

**Planner Output:**
```
#P1: I need to find who invented the telephone.
#E1 = Search["inventor of the telephone"]
#P2: Now I need to find which country this person was born in.
#E2 = Search["birthplace country of #E1"]
#P3: Finally, I need to find the capital of that country.
#E3 = Search["capital of #E2"]
```

**Worker Execution:**
```
#E1 = Search["inventor of the telephone"]
     -> "Alexander Graham Bell is credited as the inventor of the
        first practical telephone."

#E2 = Search["birthplace country of Alexander Graham Bell"]
     -> "Alexander Graham Bell was born in Edinburgh, Scotland,
        which is part of the United Kingdom."

#E3 = Search["capital of United Kingdom"]
     -> "London is the capital of the United Kingdom."
```

**Solver Input:**
```
Task: What is the capital of the country where the inventor of the
telephone was born?

Plan and Evidence:
#P1: I need to find who invented the telephone.
#E1: Alexander Graham Bell is credited as the inventor of the first
     practical telephone.
#P2: Now I need to find which country this person was born in.
#E2: Alexander Graham Bell was born in Edinburgh, Scotland, which is
     part of the United Kingdom.
#P3: Finally, I need to find the capital of that country.
#E3: London is the capital of the United Kingdom.

Now solve the task. Response:
```

**Solver Output:**
```
The inventor of the telephone is Alexander Graham Bell, who was born
in Edinburgh, Scotland (United Kingdom). The capital of the United
Kingdom is London. Therefore, the answer is London.
```

### Example 2: Parallel Tool Calls

**Planner Output:**
```
Task: Which is older, Toyota or Volkswagen?
#P1: Find when Toyota was founded.
#E1 = Search["Toyota founding year"]
#P2: Find when Volkswagen was founded.
#E2 = Search["Volkswagen founding year"]
```

**Worker Execution (E1 and E2 run in parallel):**
```
#E1 -> "Toyota was founded on August 28, 1937."
#E2 -> "Volkswagen was founded on May 28, 1937."
```

**Solver Output:**
```
Volkswagen (founded May 1937) is slightly older than Toyota (founded
August 1937), both established in the same year.
```

## When to Use

- The task involves multiple tool calls that can be partially or fully predicted upfront.
- Token efficiency is a priority and you want to avoid the growing context of ReAct loops.
- Tool calls can be parallelized for lower wall-clock latency.
- The reasoning pattern is relatively predictable (e.g., multi-hop QA with a known number of hops).
- You want a simpler agent architecture with clearly separated planning and execution phases.

## When to Avoid

- The next action critically depends on the result of the previous action in ways that cannot be anticipated.
- The environment is highly dynamic or adversarial, requiring reactive adaptation.
- The task may require an unknown or variable number of tool calls that cannot be planned upfront.
- Error recovery requires re-planning based on unexpected tool outputs.
- The task is simple enough that a single tool call suffices (ReWOO's overhead is not justified).

## Cost & Performance

| Dimension          | Rating    | Notes                                               |
|---------------------|-----------|----------------------------------------------------|
| Token overhead      | Medium    | ~5x fewer tokens than ReAct; 2 LLM calls + tools   |
| Latency             | Medium    | Parallelizable tools; 2 sequential LLM calls        |
| Accuracy gain       | Moderate  | Comparable to ReAct; slightly lower on adaptive tasks|
| Implementation      | Medium    | Planner + Worker + Solver architecture               |
| Model requirements  | Large     | Needs strong planning and synthesis capabilities      |

## Variants

- **Adaptive ReWOO**: If the Solver determines that the collected evidence is insufficient, trigger a second planning round to fill gaps. This adds ReAct-style adaptivity while retaining most of ReWOO's efficiency.
- **ReWOO with verification**: Add a verification step between Worker and Solver that checks whether tool outputs are valid and re-executes failed calls.
- **ReWOO with fallback to ReAct**: Start with ReWOO's planning approach but fall back to ReAct-style interleaving if the plan fails or the Solver cannot synthesize an answer.
- **Streaming ReWOO**: Execute tool calls as soon as their dependencies are resolved rather than waiting for the full plan.

## Composability

ReWOO's modular architecture makes it naturally composable:

- **ReWOO + CoT**: Use Chain-of-Thought reasoning within the Planner to improve plan quality and within the Solver to improve synthesis.
- **ReWOO + Plan-and-Solve**: PS+ style planning instructions can enhance the Planner module's ability to generate comprehensive plans with explicit variable extraction.
- **ReWOO + Self-Consistency**: Run multiple Planner instances to generate diverse plans, execute all of them, and vote on the Solver outputs.
- **ReWOO + ReAct**: Use ReWOO as the default approach and fall back to ReAct when the plan encounters unexpected results that require adaptive re-planning.
## Limitations

- **Plan rigidity**: The plan is fixed before any tool execution. If a tool returns unexpected results, ReWOO cannot adapt mid-execution.
- **Placeholder resolution**: When #E2 depends on #E1, execution must be sequential, reducing parallelism.
- **Planning errors propagate**: An incorrect or incomplete plan has no opportunity for course correction during the Worker phase.
- **Solver burden**: The Solver must compensate for planning mistakes by reasoning about potentially noisy or irrelevant evidence.
- **Limited applicability for exploratory tasks**: Tasks requiring open-ended exploration do not fit the plan-upfront paradigm.

## Sources

- Xu, B., Peng, Z., Lei, B., Mukherjee, S., Liu, Y., & Xu, D. (2023). ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models. https://arxiv.org/abs/2305.18323
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. https://arxiv.org/abs/2210.03629
- Khot, T., Trivedi, H., Finlayson, M., Fu, Y., Richardson, K., Clark, P., & Sabharwal, A. (2022). Decomposed Prompting: A Modular Approach for Solving Complex Tasks. https://arxiv.org/abs/2210.02406
