---
id: ape
name: "Automatic Prompt Engineer (APE)"
aliases: ["APE", "Automatic Instruction Generation", "Prompt Generation and Selection"]
category: optimization
family: prompt-generation
year: 2022
authors: ["Yongchao Zhou", "Andrei Ioan Muresanu", "Ziwen Han", "Keiran Paster", "Silviu Pitis", "Harris Chan", "Jimmy Ba"]
paper: "https://arxiv.org/abs/2211.01910"
paper_title: "Large Language Models Are Human-Level Prompt Engineers"
venue: "ICLR 2023"
code: null

complexity: medium
token_cost: high
latency: high
num_calls: variable

requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["automatic instruction discovery", "bootstrapping prompts from input-output pairs", "large-scale prompt search", "finding non-obvious phrasings"]
avoid_when: ["no input-output examples", "single-turn creative tasks", "budget-constrained scenarios", "tasks with ambiguous evaluation"]
composes_with: ["chain-of-thought", "few-shot", "self-consistency", "opro"]

tags: ["optimization", "automatic", "generation", "selection", "meta-prompting"]
---

# Automatic Prompt Engineer (APE)

> **One-line summary:** APE automatically generates candidate instructions from input-output demonstrations, then selects the best one by scoring each against a validation set.

## Overview

Automatic Prompt Engineer (APE) is a two-stage framework for automatic prompt engineering. Given a set of input-output demonstrations, APE first uses an LLM to generate a diverse pool of candidate instructions that could explain the demonstrated behavior. It then evaluates each candidate on a held-out validation set and selects the one with the highest score. This generate-then-select paradigm treats prompt engineering as a program synthesis problem.

The central insight of APE is that LLMs can reverse-engineer instructions from examples. By showing an LLM pairs of inputs and desired outputs and asking "What instruction could have produced these outputs?", the system generates a rich set of candidate prompts that capture different aspects of the task. This is fundamentally different from forward approaches that try to write instructions from scratch -- APE works backward from demonstrated behavior.

APE demonstrated that automatically generated prompts can match or exceed human-written ones across a wide range of tasks. On instruction induction benchmarks, APE achieved human-level or better performance on 24 out of 24 tasks. The method also discovered that chain-of-thought-style instructions (e.g., "Let's work this out in a step by step way to be sure we have the right answer") emerge naturally from the generation process on reasoning tasks.

## How It Works

1. **Collect Demonstrations:** Gather a set of input-output pairs that illustrate the target task behavior.
2. **Generate Candidate Instructions:** Prompt the LLM with a subset of demonstrations and ask it to infer the instruction. Repeat with different subsets and generation temperatures to produce a diverse pool of 20-50 candidates.
3. **Score Candidates:** For each candidate instruction, prepend it to inputs from a validation set and measure the output quality (e.g., exact match, execution accuracy).
4. **Select Best:** Choose the instruction with the highest validation score.
5. **(Optional) Resample and Refine:** Generate semantic variations of top-scoring candidates and re-evaluate to further improve quality.

### Diagram

```
┌───────────────────────────────────────────────┐
│  Input-Output Demonstrations                  │
│  ┌──────────┬──────────┐                      │
│  │  Input   │  Output  │                      │
│  ├──────────┼──────────┤                      │
│  │  "2+3"   │  "5"     │                      │
│  │  "7*4"   │  "28"    │                      │
│  │  "15-9"  │  "6"     │                      │
│  └──────────┴──────────┘                      │
└──────────────────┬────────────────────────────┘
                   │
          ┌────────▼─────────┐
          │  Stage 1: GENERATE │
          │  "What instruction │
          │   produced these?" │
          └────────┬─────────┘
                   │
    ┌──────────────▼──────────────┐
    │  Candidate Pool             │
    │  ├─ "Calculate the result"  │
    │  ├─ "Solve the math problem"│
    │  ├─ "Compute the answer"    │
    │  └─ "Evaluate expression"   │
    └──────────────┬──────────────┘
                   │
          ┌────────▼─────────┐
          │  Stage 2: SELECT  │
          │  Score each on    │
          │  validation set   │
          └────────┬─────────┘
                   │
          ┌────────▼─────────┐
          │  Best Instruction │
          │  Score: 94.2%     │
          └──────────────────┘
```

## Template

```
Stage 1 — Generation prompt:

I gave a friend an instruction and some inputs. The friend read the
instruction and wrote an output for every input. Here are the
input-output pairs:

{input_output_pairs}

The instruction was:

---

Stage 2 — Evaluation (for each candidate instruction):

{candidate_instruction}

Input: {test_input}
Output:
```

## Examples

### Example 1: Discovering a Task Instruction

**Input:**
```
I gave a friend an instruction and some inputs. The friend read the
instruction and wrote an output for every input. Here are the
input-output pairs:

Input: "The movie was absolutely fantastic and kept me on the edge of my seat"
Output: "positive"

Input: "I was bored out of my mind, terrible waste of time"
Output: "negative"

Input: "It was okay, nothing special but not bad either"
Output: "neutral"

Input: "A masterpiece of modern cinema, truly breathtaking"
Output: "positive"

The instruction was:
```

**Output:**
```
Candidate 1: "Classify the sentiment of the following text as positive,
negative, or neutral."

Candidate 2: "Read the movie review and determine the overall emotional
tone. Respond with positive, negative, or neutral."

Candidate 3: "Categorize the opinion expressed in the text into one of
three categories: positive, negative, or neutral."

[After evaluation: Candidate 2 scores highest at 91.3%]
```

### Example 2: Math Reasoning Instruction Discovery

**Input:**
```
I gave a friend an instruction and some inputs. The friend read the
instruction and wrote an output for every input:

Input: "A store has 45 apples. They sell 12 and receive 23 more. How many?"
Output: "56"

Input: "Sarah has 8 stickers. She gives 3 to Tom and 2 to Jane. How many left?"
Output: "3"

The instruction was:
```

**Output:**
```
Candidate 1: "Solve the word problem and give only the numerical answer."

Candidate 2: "Read the math word problem carefully. Identify the relevant
numbers and operations, then compute the final answer step by step."

Candidate 3: "Let's work this out in a step by step way to make sure we
have the right answer."

[After evaluation: Candidate 3 achieves highest accuracy at 82.7%]
```

## When to Use

- You have input-output demonstrations but no clear instruction to describe the task
- You want to bootstrap a prompt for a new task quickly
- Manual prompt writing has not yielded good results and you want to explore alternatives
- You need to discover non-obvious instruction phrasings that improve performance
- You are building an automated pipeline that must create prompts without human intervention

## When to Avoid

- You have no input-output examples to seed the generation
- The task requires complex multi-turn or multi-step prompting beyond a single instruction
- Evaluation metric is undefined or highly subjective
- You are optimizing for latency and cannot afford the generation + evaluation overhead
- The candidate pool would be too large to evaluate within budget

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Generation calls | 10-50 | Number of candidate instructions generated |
| Eval calls per candidate | N | One call per validation example per candidate |
| Total token cost | High | ~(candidates x eval_size) scoring calls |
| Quality gain | +5-25% | Largest on tasks where instruction wording matters |
| Time to complete | 15 min - 2 hrs | Depends on pool size and eval set |

## Variants

- **APE with Resampling:** After initial selection, generate paraphrases of the top-K instructions and re-evaluate, yielding an additional 1-5% improvement.
- **APE-Zero:** Skip the demonstration stage and generate diverse instructions from a task description only, useful when demonstrations are scarce.
- **Iterative APE:** Run multiple rounds of generate-and-select, using top candidates from round N as seeds for round N+1, similar to evolutionary approaches.
- **Monte Carlo APE:** Use Monte Carlo sampling to estimate instruction quality with fewer evaluation examples per candidate.

## Composability

- **APE + Chain-of-Thought:** APE naturally discovers CoT-style instructions on reasoning tasks without being explicitly told to.
- **APE + Few-Shot:** Use APE to find the best instruction, then pair it with manually selected or automatically chosen few-shot examples.
- **APE + OPRO:** Use APE for initial candidate generation and OPRO for iterative refinement of top candidates.
- **APE + Self-Consistency:** Apply self-consistency voting on top of APE-discovered instructions for further accuracy gains.

## Limitations

- Quality depends heavily on the diversity and representativeness of input-output demonstrations
- Large candidate pools require significant compute for evaluation
- The method optimizes only the instruction prefix; it does not optimize prompt structure, formatting, or few-shot examples
- Generated instructions may overfit to the specific demonstrations used for generation
- Does not handle tasks requiring complex prompt structures (e.g., multi-turn, tool use)
- May discover instructions that work well on average but fail on specific edge cases

## Sources

- **Primary:** [Large Language Models Are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910) — Zhou et al., ICLR 2023
- **Related:** [Large Language Models as Optimizers (OPRO)](https://arxiv.org/abs/2309.03409) — Yang et al., 2023
- **Related:** [PromptBreeder](https://arxiv.org/abs/2309.16797) — Fernando et al., 2023
- **Benchmark:** [Instruction Induction](https://arxiv.org/abs/2205.10782) — Honovich et al., 2022
