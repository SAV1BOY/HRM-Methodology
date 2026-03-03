---
id: react
name: ReAct
aliases:
  - ReAct prompting
  - reason-and-act
  - reason + act
  - thought-action-observation
category: reasoning
family: tool-use
year: 2022
authors:
  - Shunyu Yao
  - Jeffrey Zhao
  - Dian Yu
  - Nan Du
  - Izhak Shafran
  - Karthik Narasimhan
  - Yuan Cao
paper: https://arxiv.org/abs/2210.03629
paper_title: "ReAct: Synergizing Reasoning and Acting in Language Models"
venue: ICLR 2023
code: https://github.com/ysymyth/ReAct
complexity: medium
token_cost: variable
latency: high
num_calls: variable
requires_examples: true
requires_tools: true
requires_training: false
model_agnostic: true
best_for:
  - knowledge-intensive question answering
  - multi-step information retrieval
  - interactive task completion
  - grounded reasoning with external data
  - tasks requiring real-time information
avoid_when:
  - pure reasoning tasks with no external data needs
  - tasks where all information is in the prompt
  - latency-critical single-turn applications
  - environments without available tools or APIs
composes_with:
  - chain-of-thought
  - self-ask
  - self-consistency
  - tree-of-thoughts
  - rewoo
tags:
  - tool-use
  - reasoning
  - acting
  - grounding
  - agent
  - interactive
---

# ReAct

> Interleave reasoning traces (Thought) with task-specific actions (Action) and environmental feedback (Observation) in a loop to solve tasks requiring both reasoning and external interaction.

## Overview

ReAct, introduced by Yao et al. (2022), is a paradigm that synergizes reasoning and acting in large language models. The name is a portmanteau of "Reason" and "Act." While Chain-of-Thought prompting enables models to reason through problems step by step, and action-based approaches (like WebGPT or tool-use agents) enable models to interact with external environments, ReAct combines both capabilities in a single interleaved framework. At each step, the model generates a Thought (reasoning trace), takes an Action (interacting with a tool or environment), and receives an Observation (the result of that action).

The key insight behind ReAct is that reasoning and acting are synergistic: reasoning helps the model plan actions, interpret observations, and handle exceptions, while actions ground the reasoning in real information and prevent hallucination. A pure reasoning approach (CoT) may hallucinate facts it does not know. A pure action approach may take inefficient or incorrect actions without thinking ahead. ReAct combines the best of both: the Thought step plans and interprets, the Action step gathers information, and the Observation step provides grounded feedback.

ReAct was evaluated on diverse benchmarks including knowledge-intensive QA (HotpotQA, FEVER) and interactive decision-making tasks (ALFWorld, WebShop). On HotpotQA, ReAct outperformed both CoT-only and Act-only baselines, with the combined approach achieving higher accuracy while producing more interpretable and grounded reasoning traces. The framework has become the foundation for modern LLM agent architectures, influencing tools like LangChain, AutoGPT, and numerous production agent systems. Its Thought-Action-Observation loop is now the de facto standard for building tool-augmented LLM agents.

## How It Works

1. **Present the task and available tools**: Define the task, available actions (e.g., Search, Lookup, Calculate), and provide few-shot examples of the Thought-Action-Observation pattern.
2. **Generate a Thought**: The model reasons about the current state, what information is needed, and what action to take next.
3. **Produce an Action**: Based on the thought, the model outputs a specific action with arguments (e.g., `Search[population of France]`).
4. **Execute the Action**: The system executes the action against the external environment (API call, search engine, database query) and returns the result.
5. **Receive an Observation**: The action's result is fed back to the model as an Observation.
6. **Iterate**: Steps 2-5 repeat until the model decides it has enough information and outputs a Finish action with the final answer.

### Diagram

```
┌──────────────────────────────────────────────────┐
│                    ReAct Loop                    │
│                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐ │
│  │ Thought  │────>│  Action  │────>│Observation│ │
│  │(Reason)  │     │  (Act)   │     │(Feedback) │ │
│  └──────────┘     └────┬─────┘     └─────┬─────┘ │
│       ^                |                  |       │
│       |                v                  |       │
│       |         ┌────────────┐            |       │
│       |         │  External  │            |       │
│       |         │Environment │            |       │
│       |         │(Search,API)│            |       │
│       |         └────────────┘            |       │
│       |                                   |       │
│       └───────────────────────────────────┘       │
│                                                   │
│  Repeat until: Finish[answer]                     │
└───────────────────────────────────────────────────┘
```

## Template

```
Solve the following task by interleaving Thought, Action, and Observation steps.

Available actions:
- Search[query]: Search for information about the query.
- Lookup[term]: Look up a specific term on the current page.
- Finish[answer]: Return the final answer.

{exemplar_1_with_thought_action_observation_trace}

{exemplar_2_with_thought_action_observation_trace}

Question: {test_question}
Thought 1:
```

## Examples

### Example 1: Multi-Hop Question Answering

**Prompt (abbreviated exemplar + test question):**
```
Question: What is the elevation range for the area that the eastern
sector of the Colorado orogeny extends into?

Thought 1: I need to search for Colorado orogeny to find information
about its eastern sector.
Action 1: Search[Colorado orogeny]
Observation 1: The Colorado orogeny was an episode of mountain building
(an orogeny) in Colorado and surrounding areas. The eastern sector
extends into the High Plains.
Thought 2: The eastern sector extends into the High Plains. I need to
find the elevation range of the High Plains.
Action 2: Search[High Plains elevation]
Observation 2: The High Plains are a subregion of the Great Plains,
mainly in Western Kansas and Eastern Colorado. The elevation ranges
from around 1,800 to 7,000 feet.
Thought 3: The High Plains elevation ranges from 1,800 to 7,000 feet.
That is the elevation range for the area the eastern sector of the
Colorado orogeny extends into.
Action 3: Finish[approximately 1,800 to 7,000 feet]

Question: Were the directors of Jaws and Casino Royale (2006) from
the same country?

Thought 1:
```

**Model Output:**
```
Thought 1: I need to find the directors of both movies and their
nationalities. Let me start with Jaws.
Action 1: Search[director of Jaws film]
Observation 1: Jaws is a 1975 American thriller film directed by
Steven Spielberg.
Thought 2: Steven Spielberg directed Jaws. Now I need to find the
director of Casino Royale (2006).
Action 2: Search[director of Casino Royale 2006]
Observation 2: Casino Royale is a 2006 spy film directed by Martin
Campbell.
Thought 3: Martin Campbell directed Casino Royale (2006). Now I need
to check if Spielberg and Campbell are from the same country.
Steven Spielberg is American. Let me verify Martin Campbell's
nationality.
Action 3: Search[Martin Campbell nationality]
Observation 3: Martin Campbell is a New Zealand film director.
Thought 4: Steven Spielberg is American and Martin Campbell is from
New Zealand. They are not from the same country.
Action 4: Finish[No, Steven Spielberg (American) and Martin Campbell
(New Zealander) are from different countries.]
```

### Example 2: Fact Verification

**Test question:**
```
Question: Claim: "The Eiffel Tower is the tallest structure in France."
Verify whether this claim is true or false.

Thought 1:
```

**Model Output:**
```
Thought 1: I need to check the height of the Eiffel Tower and whether
there are taller structures in France.
Action 1: Search[height of Eiffel Tower]
Observation 1: The Eiffel Tower is 330 meters tall (including antennas).
It was the tallest man-made structure in the world until 1930.
Thought 2: The Eiffel Tower is 330 meters. I should check if there are
taller structures in France now, such as TV masts or transmission towers.
Action 2: Search[tallest structure in France]
Observation 2: The Longwave transmitter Allouis is a guyed mast near
Allouis, France, standing at 350 meters, making it the tallest structure
in France.
Thought 3: The Longwave transmitter Allouis at 350 meters is taller
than the Eiffel Tower at 330 meters. Therefore the claim is false.
Action 3: Finish[False. The Eiffel Tower (330m) is not the tallest
structure in France. The Longwave transmitter Allouis (350m) is taller.]
```

## When to Use

- The task requires external information that may not be in the model's parametric memory.
- Multi-hop reasoning is needed where each hop requires fetching new information.
- You want to reduce hallucination by grounding reasoning in retrieved facts.
- The task involves interaction with an environment (browsing, tool use, API calls).
- Interpretability is important -- the Thought-Action-Observation trace is highly auditable.

## When to Avoid

- All necessary information is already in the prompt or context window.
- The task is purely computational or logical with no need for external data.
- Latency requirements are strict and the multi-turn loop is too slow.
- No tools or APIs are available to execute actions against.
- The overhead of tool calls outweighs the benefit (simple factual questions the model knows).

## Cost & Performance

| Dimension          | Rating    | Notes                                            |
|---------------------|-----------|-------------------------------------------------|
| Token overhead      | High      | Each loop iteration adds thought + obs tokens    |
| Latency             | High      | Sequential: thought -> action -> observation      |
| Accuracy gain       | High      | Reduces hallucination; +6% on HotpotQA over CoT  |
| Implementation      | Medium    | Need tool integration and loop orchestration      |
| Model requirements  | Large     | Needs strong instruction-following and tool use    |

## Variants

- **ReAct + Self-Consistency**: Run multiple ReAct traces and vote on the final answer, combining grounding with robustness.
- **Reflexion**: Extends ReAct with a self-reflection step where the model critiques its own reasoning after a failed attempt and retries (Shinn et al., 2023).
- **FireAct**: Fine-tune a smaller model on successful ReAct traces from a larger model, distilling the reasoning-acting capability.
- **ReWOO**: Plan all actions upfront before executing any, reducing the sequential dependency between reasoning and acting. See `rewoo.md`.
- **ReAct with memory**: Add a long-term memory component to store and retrieve information across multiple ReAct episodes.

## Composability

ReAct is the foundational agent loop that composes naturally with most other techniques:

- **ReAct + CoT**: The "Thought" step in ReAct is essentially a CoT reasoning step. Enriching it with more detailed CoT improves planning quality.
- **ReAct + Self-Ask**: Self-Ask's follow-up question structure can replace or complement the Thought step, with actions used to answer the follow-up questions via search.
- **ReAct + Tree-of-Thoughts**: Explore multiple action sequences as a tree, evaluating different tool-use strategies before committing.
- **ReAct + Self-Consistency**: Run multiple ReAct traces in parallel with temperature sampling and majority vote on the final answer.
- **ReAct + ReWOO**: Use ReWOO-style upfront planning for the action sequence, then fall back to ReAct-style interleaving when the plan encounters unexpected observations.

## Limitations

- **Sequential bottleneck**: Each Thought-Action-Observation cycle is sequential. The model cannot plan multiple actions in parallel within the standard ReAct framework (see ReWOO for a solution).
- **Action space design**: The effectiveness of ReAct depends heavily on the quality and design of available actions. Poorly designed tools or limited action spaces constrain the model.
- **Error compounding**: If an early action returns incorrect information, subsequent reasoning is built on a faulty foundation. The model may not recognize and recover from bad observations.
- **Loop termination**: The model may get stuck in loops, repeatedly searching for the same information or failing to converge on an answer. A maximum iteration limit is essential.
- **Cost of tool calls**: Each action incurs both the LLM generation cost and the external tool execution cost (API latency, rate limits, monetary cost).

## Sources

- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. https://arxiv.org/abs/2210.03629
- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. *NeurIPS 2023*. https://arxiv.org/abs/2303.11366
- Schick, T., Dwivedi-Yu, J., Dessi, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. https://arxiv.org/abs/2302.04761
