---
id: protegi
name: "ProTeGi: Prompt Optimization with Textual Gradients"
aliases: ["ProTeGi", "Prompt-Optimization-Textual-Gradients", "gradient-inspired-prompt-optimization"]
category: optimization
family: gradient-inspired-optimization
year: 2023
authors: ["Reid Pryzant", "Dan Iter", "Jerry Li", "Yin Tat Lee", "Chenguang Zhu", "Michael Zeng"]
paper: "https://arxiv.org/abs/2305.03495"
paper_title: "Automatic Prompt Optimization with 'Gradient Descent' and Beam Search"
venue: "EMNLP 2023"
code: "https://github.com/microsoft/LMOps/tree/main/prompt_optimization"
complexity: medium
token_cost: high
latency: high
num_calls: variable
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for: ["iterative prompt refinement", "error-driven optimization", "tasks with clear failure modes", "systematic prompt improvement"]
avoid_when: ["no labeled examples available", "extremely simple tasks", "need for real-time optimization", "very limited compute budget"]
composes_with: ["chain-of-thought", "few-shot-prompting", "self-consistency"]
tags: ["optimization", "gradient-inspired", "error-analysis", "beam-search", "iterative-refinement"]
---

# ProTeGi: Prompt Optimization with Textual Gradients

> **One-line summary:** An iterative prompt optimization method that mimics gradient descent by analyzing errors on a training batch, generating natural language "gradients" (edit suggestions), applying them to produce candidate prompts, and selecting the best via beam search.

## Overview

ProTeGi (Prompt Optimization with Textual Gradients) draws an analogy between numerical gradient descent in deep learning and iterative text-based prompt refinement. Just as gradient descent computes the direction of steepest improvement and takes a step, ProTeGi analyzes *why* the current prompt fails on specific examples, generates textual descriptions of what should change (the "textual gradient"), and produces edited prompts that address these failures. A beam search over candidate prompts ensures the optimization explores multiple promising directions simultaneously.

The method operates in a loop: (1) evaluate the current prompt on a mini-batch of training examples, (2) collect failure cases and use an LLM to summarize what went wrong, (3) use another LLM call to propose prompt edits based on the error summary, (4) generate multiple candidate prompts by applying different edits, and (5) evaluate all candidates and keep the top-k (beam search). This process mirrors the train-evaluate-update loop of standard machine learning, but operates entirely in natural language without any numerical gradients.

ProTeGi was developed at Microsoft Research and demonstrated consistent improvements over manual prompting, APE, and other baselines across diverse tasks including mathematical reasoning, instruction following, and text classification. The gradient-inspired framework provides an intuitive understanding of the optimization process -- practitioners can inspect the "gradients" to understand *why* certain prompt changes were made, offering a level of interpretability that purely evolutionary methods lack.

## How It Works

1. **Initialize**: Start with a seed prompt (hand-crafted or generated) and a labeled training set.

2. **Evaluate on Mini-batch**: Run the current prompt on a random mini-batch of training examples. Collect the outputs and identify failures (incorrect predictions).

3. **Compute Textual Gradient**: Feed the failures to an LLM with the meta-prompt: "Here is a prompt and examples where it failed. What is wrong with the prompt? How should it be changed?" The LLM produces a natural language critique and suggested direction for improvement.

4. **Generate Candidate Edits**: Use the textual gradient to generate multiple edited versions of the prompt. Each edit applies the gradient's suggestions in a slightly different way, creating diversity.

5. **Evaluate Candidates**: Score each candidate prompt on a validation mini-batch.

6. **Beam Search Selection**: Keep the top-k scoring candidates as the current beam. If a candidate outperforms all current beam members, it replaces the worst.

7. **Iterate**: Repeat steps 2-6 for a fixed number of steps or until the prompt's score plateaus.

8. **Return Best**: Output the highest-scoring prompt from the final beam.

### Diagram

```
Step 1: Evaluate              Step 2: Textual Gradient
+------------------+          +---------------------------+
| Current Prompt   |          | LLM Error Analyzer        |
| + Mini-batch     |--------->| "The prompt fails because  |
| = Successes +    |          |  it doesn't specify output |
|   Failures       |          |  format clearly..."        |
+------------------+          +-------------+-------------+
                                            |
Step 3: Generate Edits                      v
+------------------------------------------+
| LLM Edit Generator                        |
| Candidate 1: "... specify JSON output..." |
| Candidate 2: "... add format example..."  |
| Candidate 3: "... constrain to list..."   |
+------------------------------------------+
         |            |            |
         v            v            v
  [Evaluate]   [Evaluate]   [Evaluate]
         |            |            |
         v            v            v
  +----------------------------------+
  | Beam Search: Keep Top-k          |
  | -> Best becomes new current      |
  +----------------------------------+
         |
         v
  [Repeat for T steps]
```

## Template

```
--- Step 1: Error Analysis Meta-Prompt ---
I am trying to write a prompt for an AI assistant. My current prompt is:

"{current_prompt}"

But this prompt fails on the following examples:

{failure_examples_with_expected_and_actual_outputs}

What is wrong with the current prompt? Provide a concise summary of
the key issues and suggest specific improvements.

--- Step 2: Edit Generation Meta-Prompt ---
Based on the following analysis of prompt failures:

"{textual_gradient}"

Here is the current prompt:
"{current_prompt}"

Generate an improved version of the prompt that addresses the
identified issues. The improved prompt should be self-contained
and complete.

Improved Prompt:

--- Step 3: Task Evaluation ---
{candidate_prompt}

{task_input}
```

## Examples

### Example 1: Math Word Problem Formatting

**Task**: Optimize a prompt for math word problem solving with structured output.

**Initial Prompt**: "Solve the following math problem."

**Iteration 1**:
- *Failures*: Model outputs prose instead of numerical answers; sometimes skips steps.
- *Textual Gradient*: "The prompt doesn't specify that the answer should be a number, nor does it ask for step-by-step work. The model often provides narrative answers without clear final values."
- *Candidate Edits*:
  1. "Solve the following math problem step by step. Provide your final numerical answer after 'Answer:'."
  2. "Work through this math problem showing each step. End with 'The answer is [number]'."
  3. "Solve this math problem. Show your reasoning, then give the final answer as a number."
- *Best Candidate (score 72%)*: Edit 1

**Iteration 3**:
- *Failures*: Model makes arithmetic errors in multi-step problems.
- *Textual Gradient*: "The prompt doesn't encourage verification. Many errors occur in the final computation step where the model rushes to an answer."
- *Best Candidate (score 81%)*: "Solve the following math problem step by step. After each arithmetic operation, verify the result. Provide your final numerical answer after 'Answer:'. Double-check your final answer before responding."

**Final Result**: Accuracy improved from 58% to 81% over 5 iterations.

### Example 2: Instruction Following

**Task**: Optimize a prompt for an assistant that should follow formatting constraints.

**Initial Prompt**: "You are a helpful assistant. Answer the user's question."

**Iteration 1**:
- *Failures*: Model ignores length constraints, doesn't follow specified formats.
- *Textual Gradient*: "The prompt provides no guidance about respecting constraints in the user's question. The model treats all questions as open-ended."
- *Best Candidate*: "You are a helpful assistant. Carefully read the user's question and follow ALL formatting instructions exactly, including length limits, output format, and style requirements."

**Iteration 4**:
- *Failures*: Model follows most constraints but occasionally adds preambles ("Sure! Here's...") that violate format requirements.
- *Textual Gradient*: "The model adds unnecessary preambles and filler phrases. The prompt should explicitly instruct against conversational filler."
- *Best Candidate*: "You are a precise assistant. Follow ALL formatting instructions in the user's request exactly. Do not add preambles, filler phrases, or conversational niceties. Begin your response directly with the requested content. Respect all specified constraints including length, format, and style."

**Final Result**: Instruction-following score improved from 62% to 88% over 6 iterations.

## When to Use

- You want interpretable optimization (you can inspect the "gradients" to understand changes)
- You have clear failure modes that can be analyzed and described
- You want systematic, iterative improvement rather than random search
- You have a moderate evaluation dataset (50+ labeled examples)
- You want to optimize a single prompt (not a multi-step pipeline)

## When to Avoid

- No labeled data is available for evaluation
- The failures are hard to describe in natural language (e.g., subtle distributional shifts)
- You need to optimize a complex multi-module pipeline (use DSPy instead)
- Compute budget is very limited (beam search multiplies costs)
- The task has noisy or subjective metrics that make error analysis unreliable

## Cost & Performance

| Dimension          | Value                  | Notes                                          |
|---------------------|------------------------|-------------------------------------------------|
| Iterations          | 5-15                   | Each iteration = error analysis + edit + eval   |
| Beam width          | 2-5                    | More beams = better exploration, higher cost    |
| Candidates/step     | 3-5                    | Number of edits generated per gradient          |
| Total LLM calls     | 100-500                | Analysis + generation + evaluation              |
| Accuracy gain       | +5-20% over baseline   | Depends on initial prompt quality               |
| Wall-clock time     | 1-4 hours              | Moderate compared to evolutionary methods       |

## Variants

- **ProTeGi-Basic**: Single candidate per iteration (no beam search). Faster but less robust.
- **ProTeGi-Beam**: Full beam search with multiple candidates. More thorough exploration.
- **ProTeGi + Expansion**: Add a step that generates semantically diverse paraphrases of each candidate before evaluation.
- **Bandit-ProTeGi**: Replace beam search with multi-armed bandit selection for more adaptive exploration.

## Composability

- **With few-shot selection**: Optimize the instruction prefix while separately selecting few-shot demonstrations.
- **With Chain-of-Thought**: Include CoT triggers in the prompt being optimized.
- **As a DSPy optimizer**: The ProTeGi loop can be implemented as a custom DSPy teleprompter.
- **Cascaded with APE**: Use APE to generate initial candidates, then refine with ProTeGi.

## Limitations

- Error analysis quality depends on the LLM's ability to introspect on failures
- Beam search can collapse to similar candidates if the edit generator lacks diversity
- The method assumes failures are due to prompt deficiencies, not inherent model limitations
- Optimization can overfit to the training mini-batches if they are not representative
- Each iteration requires multiple LLM calls for analysis, generation, and evaluation
- Does not optimize few-shot example selection or prompt structure (only instruction text)

## Sources

- Pryzant, R. et al. (2023). "Automatic Prompt Optimization with 'Gradient Descent' and Beam Search." *EMNLP 2023*. *arXiv:2305.03495*. https://arxiv.org/abs/2305.03495
- Microsoft LMOps Repository: https://github.com/microsoft/LMOps/tree/main/prompt_optimization
- Yang, C. et al. (2023). "Large Language Models as Optimizers." *arXiv:2309.03409*.
- Zhou, Y. et al. (2022). "Large Language Models Are Human-Level Prompt Engineers." *arXiv:2211.01910*.
