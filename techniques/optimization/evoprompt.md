---
id: evoprompt
name: "EvoPrompt: Evolutionary Prompt Optimization"
aliases: ["EvoPrompt", "EvoPrompting", "evolutionary-prompt-optimization"]
category: optimization
family: evolutionary-optimization
year: 2023
authors: ["Qingyan Guo", "Rui Wang", "Junliang Guo", "Bei Li", "Kaitao Song", "Xu Tan", "Guoqing Liu", "Jiang Bian", "Yujiu Yang"]
paper: "https://arxiv.org/abs/2309.08532"
paper_title: "Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers"
venue: "arXiv preprint"
code: null
complexity: medium
token_cost: high
latency: high
num_calls: variable
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for: ["discrete prompt optimization", "instruction tuning without gradients", "classification tasks", "simplification tasks", "benchmark optimization"]
avoid_when: ["no evaluation dataset", "very low compute budget", "tasks requiring precise control over prompt structure", "real-time optimization needs"]
composes_with: ["chain-of-thought", "few-shot-prompting", "self-consistency"]
tags: ["optimization", "evolutionary", "genetic-algorithm", "differential-evolution", "population-based"]
---

# EvoPrompt: Evolutionary Prompt Optimization

> **One-line summary:** Applies classical evolutionary algorithms (genetic algorithms and differential evolution) to evolve populations of prompts, using the LLM itself as the crossover and mutation operator.

## Overview

EvoPrompt bridges evolutionary computation and large language model prompting by adapting two classical optimization algorithms -- Genetic Algorithms (GA) and Differential Evolution (DE) -- to operate in the discrete space of natural language prompts. The key insight is that LLMs can serve as effective crossover and mutation operators for natural language, replacing the numerical operations used in traditional evolutionary algorithms with natural language generation guided by carefully designed meta-prompts.

The method maintains a population of candidate prompts and iteratively improves them through selection, crossover, and mutation. For the GA variant, two parent prompts are selected and the LLM generates an offspring by combining elements of both. For the DE variant, three prompts are sampled and the LLM generates a new prompt by applying the "difference" between two of them to the third -- a remarkably effective adaptation of differential evolution's core mechanism to text. Each offspring is evaluated on a development set and replaces its parent if it achieves higher fitness.

EvoPrompt was shown to outperform both human-designed prompts and prior automatic methods (including APE) across a range of NLP benchmarks. The DE variant proved particularly effective, consistently discovering high-quality prompts with smaller populations and fewer generations than the GA variant. The approach is notable for its simplicity and effectiveness, requiring no gradient access or model internals.

## How It Works

1. **Initialize Population**: Create an initial population of N prompts. These can be hand-written seed prompts, outputs from APE, or simple variations of a base instruction.

2. **Evaluate Population**: Score each prompt on a development set using the target task's metric (accuracy, F1, etc.).

3. **Generate Offspring (GA variant)**:
   - Select two parent prompts via tournament selection
   - Feed them to the LLM with a meta-prompt: "Given these two prompts, generate a new prompt that combines their strengths"
   - The LLM produces an offspring prompt

4. **Generate Offspring (DE variant)**:
   - Sample three prompts (a, b, c) from the population
   - Feed them to the LLM with a meta-prompt: "Generate a new prompt based on prompt_a, incorporating the difference between prompt_b and prompt_c"
   - The LLM produces a mutant prompt

5. **Evaluate Offspring**: Score the offspring on the same development set.

6. **Selection**: Replace the weakest member (GA) or the target individual (DE) with the offspring if it has higher fitness.

7. **Repeat**: Continue for a fixed number of generations or until convergence.

8. **Return Best**: Output the highest-scoring prompt from the final population.

### Diagram

```
GA Variant:                          DE Variant:
+-----------+  +-----------+        +-----------+ +-----------+ +-----------+
| Parent 1  |  | Parent 2  |        | Prompt a  | | Prompt b  | | Prompt c  |
| "Classify |  | "Determine|        | (base)    | | (donor 1) | | (donor 2) |
|  the ..."  |  |  whether."|        +-----------+ +-----------+ +-----------+
+-----+-----+  +-----+-----+              |              |             |
      |               |                   v              v             v
      +-------+-------+             +-----------------------------------+
              |                      | LLM: "Create new prompt based on |
              v                      | a, incorporating the difference  |
  +-----------------------+          | between b and c"                 |
  | LLM: "Combine these  |          +----------------+-----------------+
  | two prompts into a   |                           |
  | better one"          |                           v
  +-----------+-----------+                  +---------------+
              |                              | Mutant Prompt |
              v                              +-------+-------+
      +---------------+                             |
      | Child Prompt  |                     [Evaluate on dev set]
      +-------+-------+                             |
              |                              [Replace if better]
      [Evaluate on dev set]
              |
      [Replace if better]
```

## Template

```
--- GA Crossover Meta-Prompt ---
I have two prompts for a {task_description} task.

Prompt 1: "{parent_prompt_1}"
(Score: {score_1})

Prompt 2: "{parent_prompt_2}"
(Score: {score_2})

Generate a new prompt that combines the strengths of both prompts.
The new prompt should be clear, concise, and effective for the task.

New Prompt:

--- DE Mutation Meta-Prompt ---
I have three prompts for a {task_description} task.

Base Prompt: "{prompt_a}"
Reference Prompt 1: "{prompt_b}"
Reference Prompt 2: "{prompt_c}"

Generate a new prompt based on the Base Prompt, but incorporate the
conceptual difference between Reference Prompt 1 and Reference Prompt 2.

New Prompt:

--- Task Evaluation ---
{evolved_prompt}

Input: {test_input}
Output:
```

## Examples

### Example 1: Sentiment Classification (SST-2)

**Task**: Optimize prompts for binary sentiment classification.

**Initial Population (5 prompts)**:
1. "Classify the sentiment as positive or negative." (Acc: 89.2%)
2. "Is this review positive or negative?" (Acc: 87.5%)
3. "Determine the sentiment of the following text." (Acc: 88.1%)
4. "Read the text and decide if it is positive or negative." (Acc: 86.9%)
5. "What is the emotional tone of this text?" (Acc: 84.3%)

**DE Evolution (10 generations, population=5)**:

*Generation 3 offspring* (from prompts 1, 2, 3):
"Carefully analyze the emotional tone expressed in this review and classify it as either positive or negative based on the overall sentiment conveyed." (Acc: 91.4%)

*Generation 8 best*:
"Evaluate the following review. Consider the author's word choices, expressed emotions, and overall message. Classify the sentiment as strictly positive or negative." (Acc: 93.1%)

**Result**: DE variant improved accuracy from 89.2% (best initial) to 93.1% in 10 generations, using approximately 300 LLM calls total.

### Example 2: Topic Classification (AG News)

**Task**: Optimize prompts for 4-way news topic classification (World, Sports, Business, Sci/Tech).

**Initial Population (4 prompts)**:
1. "Classify this news article into one of: World, Sports, Business, Sci/Tech." (Acc: 78.5%)
2. "What category does this news belong to?" (Acc: 75.2%)
3. "Determine the topic of this article." (Acc: 76.8%)
4. "Read the article and assign it to the correct news category." (Acc: 77.1%)

**GA Evolution (15 generations)**:

*Generation 5 best offspring*:
"Read the following news article carefully. Based on the subject matter, classify it into exactly one category: World (international affairs/politics), Sports (athletic events/competitions), Business (finance/economy/markets), or Sci/Tech (science/technology/innovation). Output only the category name." (Acc: 84.7%)

*Generation 12 best*:
"Analyze this news article's primary subject. Classify into one of four categories -- World: global politics and international events; Sports: athletic competitions and sports news; Business: financial markets, companies, and economic policy; Sci/Tech: scientific discoveries and technology developments. Respond with only the category name." (Acc: 86.9%)

**Result**: GA variant improved from 78.5% to 86.9%, demonstrating that explicit category definitions emerged naturally through evolution.

## When to Use

- You want a simple, principled approach to prompt optimization
- You have a clear evaluation metric and a development set
- You want to explore a diverse range of prompt phrasings
- The DE variant is preferred when you want faster convergence with smaller populations
- You have moderate compute budget (hundreds of LLM calls, not thousands)

## When to Avoid

- The task lacks a quantitative evaluation metric
- You need real-time prompt adaptation (evolution is offline)
- The problem is well-solved by simple manual prompting
- Your compute budget cannot support population-based search (minimum ~200 calls)
- You need to optimize multi-step pipelines (use DSPy instead)

## Cost & Performance

| Dimension          | Value                  | Notes                                        |
|---------------------|------------------------|----------------------------------------------|
| Population size     | 5-20 prompts           | DE works well with smaller populations       |
| Generations         | 10-30                  | DE converges faster than GA typically        |
| LLM calls/gen      | 10-40                  | Mutation/crossover + evaluation              |
| Total LLM calls    | 200-800                | Much less than PromptBreeder                 |
| Accuracy gain       | +3-10% over baselines  | Compared to hand-crafted prompts             |
| Wall-clock time     | 1-6 hours              | Depends on model latency and population size |

## Variants

- **EvoPrompt-GA**: Uses genetic algorithm with crossover and mutation. Better for diverse exploration, larger populations.
- **EvoPrompt-DE**: Uses differential evolution. Generally more sample-efficient and achieves better results with smaller populations.
- **EvoPrompt + CoT**: Evolve chain-of-thought prompts specifically, where the evolved text includes reasoning instructions.
- **Multi-objective EvoPrompt**: Optimize for multiple objectives simultaneously (accuracy + conciseness).

## Composability

- **With few-shot examples**: Evolve the instruction prefix while keeping few-shot demonstrations fixed.
- **With Chain-of-Thought**: Evolve CoT trigger phrases and reasoning instructions.
- **Seeding from APE**: Use APE-generated prompts as the initial population for further evolution.
- **Pipeline integration**: Use EvoPrompt to optimize individual steps within a larger DSPy pipeline.

## Limitations

- Limited to single-prompt optimization; does not handle multi-step pipelines natively
- Fitness landscape can be noisy, especially with small evaluation sets
- LLM-based crossover/mutation is not guaranteed to preserve useful features from parents
- GA variant can be slow to converge and may require larger populations
- No mechanism for optimizing prompt structure beyond text (e.g., cannot optimize few-shot selection)
- Results depend heavily on the quality of the initial population -- poor seeds lead to poor evolution

## Sources

- Guo, Q. et al. (2023). "Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers." *arXiv:2309.08532*. https://arxiv.org/abs/2309.08532
- Fernando, C. et al. (2023). "PromptBreeder: Self-Referential Self-Improvement Via Prompt Evolution." *arXiv:2309.16797*.
- Zhou, Y. et al. (2022). "Large Language Models Are Human-Level Prompt Engineers." *arXiv:2211.01910*.
- Storn, R. & Price, K. (1997). "Differential Evolution -- A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces." *Journal of Global Optimization*, 11(4).
