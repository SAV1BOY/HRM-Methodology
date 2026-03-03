---
id: opro
name: "Optimization by PROmpting (OPRO)"
aliases: ["OPRO", "LLM Self-Optimization", "Meta-Prompt Optimization"]
category: optimization
family: meta-prompting
year: 2023
authors: ["Chengrun Yang", "Xuezhi Wang", "Yifeng Lu", "Hanxiao Liu", "Quoc V. Le", "Denny Zhou", "Xinyun Chen"]
paper: "https://arxiv.org/abs/2309.03409"
paper_title: "Large Language Models as Optimizers"
venue: "arXiv 2023"
code: null

complexity: medium
token_cost: high
latency: high
num_calls: variable

requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["instruction optimization", "finding better task descriptions", "improving zero-shot performance", "iterative prompt refinement"]
avoid_when: ["no evaluation data available", "extremely tight budgets", "tasks where instructions matter less than examples", "real-time optimization needed"]
composes_with: ["chain-of-thought", "few-shot", "self-consistency", "dspy"]

tags: ["optimization", "meta-prompting", "self-improving", "iterative", "automatic"]
---

# Optimization by PROmpting (OPRO)

> **One-line summary:** OPRO uses an LLM as its own optimizer, iteratively generating and scoring prompt instructions to maximize task performance via a meta-prompt containing past attempts and their scores.

## Overview

Optimization by PROmpting (OPRO) is a method that leverages the natural language understanding of large language models to perform optimization. Instead of using gradient-based methods or brute-force search, OPRO frames the optimization problem in natural language: a meta-prompt describes the task, shows previous candidate solutions with their scores, and asks the LLM to propose better solutions. This creates an iterative loop where each new candidate is evaluated and fed back into the meta-prompt.

The key insight is that LLMs can effectively serve as black-box optimizers when the optimization landscape is described textually. By presenting a trajectory of past attempts (instruction text paired with accuracy scores), the LLM learns to identify patterns in what makes instructions effective and proposes improved candidates. The approach discovered the famous "Let's think step by step" instruction and found even better variants like "Take a deep breath and work on this problem step by step."

OPRO is particularly powerful for instruction optimization -- finding the best natural language description of a task to prepend to prompts. The method consistently outperforms human-written instructions and prior automatic methods on benchmarks like GSM8K and BBH, demonstrating that LLMs have a latent ability to understand and improve their own prompting.

## How It Works

1. **Initialize Meta-Prompt:** Construct a meta-prompt containing the task description, a scoring function description, and an initially empty optimization trajectory.
2. **Generate Candidates:** The optimizer LLM reads the meta-prompt and generates one or more new candidate instructions.
3. **Evaluate Candidates:** Each candidate instruction is tested on a held-out evaluation set by the scorer LLM. Accuracy or another metric is computed.
4. **Update Trajectory:** Append (instruction, score) pairs to the meta-prompt's trajectory section, maintaining a sorted window of the best-performing candidates.
5. **Iterate:** Repeat steps 2-4 for a fixed number of rounds or until convergence. The trajectory grows, providing richer context for the optimizer.
6. **Select Best:** Return the instruction with the highest evaluation score across all iterations.

### Diagram

```
┌──────────────────────────────────────────────────┐
│                  Meta-Prompt                     │
│                                                  │
│  "Below are instructions with their scores..."  │
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │ Trajectory:                             │     │
│  │   "Solve carefully"         → 62.1%     │     │
│  │   "Think step by step"      → 71.8%     │     │
│  │   "Break into sub-problems" → 74.3%     │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
│  "Generate a new instruction that scores higher" │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Optimizer LLM │
              └───────┬────────┘
                      │ new instruction
                      ▼
              ┌────────────────┐      ┌──────────┐
              │  Scorer LLM   │ ───→ │  Score    │
              │  (eval set)   │      │  = 76.5%  │
              └────────────────┘      └──────┬───┘
                                             │
                                    add to trajectory
                                             │
                                     ┌───────▼──────┐
                                     │   Iterate    │
                                     └──────────────┘
```

## Template

```
I have some instructions along with their corresponding scores.
The instructions are applied to {task_description}.
The score indicates {metric_description} on a scale of 0 to 100.

{trajectory_of_instruction_score_pairs}

Below are some example cases for the task:

{few_shot_examples_from_eval_set}

Generate an instruction that is different from all the instructions above,
and has a higher score than all the instructions above. The instruction
should be concise, clear, and general enough to apply to all cases.

New instruction:
```

## Examples

### Example 1: Math Reasoning Optimization

**Input:**
```
I have some instructions along with their corresponding scores.
The instructions are applied to grade school math word problems.
The score indicates accuracy (percentage correct) on a held-out set.

Instruction: "Solve the following math problem."
Score: 58.2

Instruction: "Let's think step by step."
Score: 71.8

Instruction: "Break the problem into smaller parts and solve each one."
Score: 73.5

Generate an instruction that is different from all the instructions above,
and has a higher score. Be concise and clear.

New instruction:
```

**Output:**
```
"Take a deep breath and work through this problem step by step,
showing your reasoning for each calculation before giving the final answer."

[Evaluated score: 76.3%]
```

### Example 2: Classification Task Optimization

**Input:**
```
I have some instructions along with their corresponding scores.
The instructions are applied to sentiment classification of movie reviews.
The score indicates classification accuracy.

Instruction: "Classify the sentiment as positive or negative."
Score: 82.1

Instruction: "Read the review carefully and determine if the overall
sentiment is positive or negative. Consider the tone and word choice."
Score: 86.4

Instruction: "You are an expert film critic. Analyze the emotional
valence of this review."
Score: 84.7

Generate a new, different instruction with a higher score.

New instruction:
```

**Output:**
```
"Determine whether this movie review expresses a positive or negative opinion.
Focus on the reviewer's overall conclusion rather than individual complaints
or praises. Respond with exactly one word: positive or negative."

[Evaluated score: 88.9%]
```

## When to Use

- You want to automatically discover the best instruction/system prompt for a task
- You have an evaluation dataset with at least 50-100 examples
- Manual prompt engineering has plateaued and you want to explore further
- You need to optimize zero-shot performance before adding few-shot examples
- You want to compare LLM-discovered instructions against human-crafted ones

## When to Avoid

- No evaluation data or metric is available
- The task is highly subjective with no clear scoring function
- Budget constraints prevent running hundreds of LLM calls for optimization
- The prompt already performs at near-ceiling accuracy
- You need to optimize multi-step pipelines (DSPy is better suited)

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | High | Each iteration requires eval set scoring + generation |
| Optimization iterations | 20-100 | Typically converges within 50 iterations |
| Eval calls per iteration | N examples | Full eval set scored for each candidate |
| Quality gain | +3-15% | Varies by task; largest gains on reasoning tasks |
| Time to optimize | 30 min - 4 hrs | Depends on eval set size and iteration count |

## Variants

- **OPRO with Temperature Sampling:** Generate multiple candidates per iteration at higher temperature to increase diversity.
- **OPRO with Paraphrasing:** Use a separate LLM call to paraphrase top candidates, expanding the search space.
- **Scorer-Optimizer Split:** Use a cheaper model as scorer and a more capable model as optimizer to reduce costs.
- **Constrained OPRO:** Add constraints to the meta-prompt (e.g., "instruction must be under 20 words") for specific deployment requirements.

## Composability

- **OPRO + Chain-of-Thought:** Optimize the instruction prefix that precedes a CoT prompt for maximum reasoning quality.
- **OPRO + Few-Shot:** First optimize instructions with OPRO, then add few-shot examples for compounded gains.
- **OPRO + Self-Consistency:** Use OPRO-optimized instructions as the base prompt for self-consistency majority voting.
- **OPRO + DSPy:** OPRO's approach to instruction optimization is conceptually similar to DSPy's COPRO optimizer.

## Limitations

- Optimization cost scales linearly with evaluation set size and number of iterations
- May converge to local optima; results depend on initialization and trajectory
- Optimizer LLM must be capable enough to reason about instruction quality from score patterns
- Scores can be noisy on small evaluation sets, leading to unreliable optimization signal
- Does not optimize few-shot examples, prompt structure, or multi-step workflows -- only the instruction text
- Found instructions may be model-specific and not transfer to other LLMs

## Sources

- **Primary:** [Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409) — Yang et al., 2023
- **Related:** [Automatic Prompt Engineer (APE)](https://arxiv.org/abs/2211.01910) — Zhou et al., 2022
- **Related:** [PromptBreeder](https://arxiv.org/abs/2309.16797) — Fernando et al., 2023
- **Blog:** [Google DeepMind Blog on OPRO](https://deepmind.google/discover/blog/) — Overview and results
