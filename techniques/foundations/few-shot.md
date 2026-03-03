---
id: few-shot
name: "Few-Shot Prompting"
aliases:
  - few-shot
  - in-context-learning
  - ICL
  - k-shot
  - few-shot-examples
category: foundations
family: demonstration-based
year: 2020
authors:
  - Tom Brown
  - Benjamin Mann
  - Nick Ryder
  - Melanie Subbiah
  - Jared Kaplan
  - Prafulla Dhariwal
  - Arvind Neelakantan
  - Pranav Shyam
  - Girish Sastry
  - Amanda Askell
  - Sandhini Agarwal
  - Ariel Herbert-Voss
  - Gretchen Krueger
  - Tom Henighan
  - Rewon Child
  - Aditya Ramesh
  - Daniel M. Ziegler
  - Jeffrey Wu
  - Clemens Winter
  - Christopher Hesse
  - Mark Chen
  - Eric Sigler
  - Mateusz Litwin
  - Scott Gray
  - Benjamin Chess
  - Jack Clark
  - Christopher Berner
  - Sam McCandlish
  - Alec Radford
  - Ilya Sutskever
  - Dario Amodei
paper: "https://arxiv.org/abs/2005.14165"
paper_title: "Language Models are Few-Shot Learners"
venue: "NeurIPS 2020"
code: null
complexity: low
token_cost: medium
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - classification with specific label sets
  - consistent output formatting
  - domain-specific tasks
  - pattern replication
  - disambiguation of task intent
  - structured extraction
avoid_when:
  - context window is severely limited
  - examples are unavailable or hard to curate
  - task is simple enough for zero-shot
  - examples might introduce bias toward seen patterns
  - dynamic tasks where input structure varies widely
composes_with:
  - chain-of-thought
  - role-prompting
  - output-format
  - prompt-scaffolding
  - self-consistency
tags:
  - in-context-learning
  - demonstration-based
  - foundational
  - GPT-3
  - few-shot
---

# Few-Shot Prompting

> **One-line summary:** Provide k input-output demonstration examples before the actual task input, enabling the model to learn the task pattern in-context without any parameter updates.

## Overview

Few-shot prompting, formally introduced by Brown et al. (2020) in the landmark GPT-3 paper, demonstrated that large language models can perform new tasks by conditioning on a small number of input-output examples provided directly in the prompt. This discovery -- termed "in-context learning" (ICL) -- fundamentally changed the paradigm for using language models. Rather than fine-tuning model weights for each task, practitioners could simply demonstrate the desired behavior through examples, and the model would generalize to new inputs.

The mechanism behind few-shot prompting is still an active area of research. Theoretical work by Xie et al. (2022) frames ICL as implicit Bayesian inference, where examples help the model identify a latent concept. Empirical work by Min et al. (2022) controversially showed that even examples with random labels can improve performance, suggesting that the format and input distribution of examples matter more than label correctness for some tasks. However, subsequent studies have nuanced this finding, showing that correct labels become increasingly important for harder tasks and larger models.

In practice, few-shot prompting bridges the gap between zero-shot instruction following and fine-tuning. It offers substantially more control over output format and task semantics than zero-shot approaches, while requiring no training data, compute, or model access beyond the inference API. The number of examples (k) typically ranges from 2 to 10, with diminishing returns beyond 5-8 examples for most tasks. The technique remains one of the most widely used prompting strategies in production systems.

## How It Works

1. **Select representative examples.** Choose k input-output pairs that exemplify the desired task behavior. Prioritize diversity across edge cases, categories, and input styles.

2. **Format examples consistently.** Structure each example with a clear delimiter between input and output. Use the same format for every example to establish an unambiguous pattern.

3. **Order examples thoughtfully.** Research shows that example order affects performance. Place the most representative or highest-quality examples last (recency bias) and maintain label balance for classification tasks.

4. **Append the actual task input.** After the examples, provide the new input in the exact same format, leaving the output position empty for the model to complete.

5. **Generate the output.** The model pattern-matches against the demonstrations and produces an output consistent with the observed examples.

### Diagram

```
┌─────────────────────────────────────┐
│  EXAMPLE 1                          │
│  Input:  "I love this product!"     │
│  Output: "Positive"                 │
├─────────────────────────────────────┤
│  EXAMPLE 2                          │
│  Input:  "Terrible experience."     │
│  Output: "Negative"                 │
├─────────────────────────────────────┤
│  EXAMPLE 3                          │
│  Input:  "It's okay, nothing great."│
│  Output: "Neutral"                  │
├─────────────────────────────────────┤
│  ACTUAL TASK                        │
│  Input:  "Best purchase ever!"      │
│  Output:  ???                       │
├─────────────────────────────────────┤
│            ▼                        │
│    ┌──────────────┐                 │
│    │    MODEL      │                 │
│    │  (few-shot)   │                 │
│    └──────┬───────┘                 │
│            ▼                        │
│  Output: "Positive"                 │
└─────────────────────────────────────┘
```

## Template

```
{task_instruction}

{input_label}: {example_1_input}
{output_label}: {example_1_output}

{input_label}: {example_2_input}
{output_label}: {example_2_output}

{input_label}: {example_3_input}
{output_label}: {example_3_output}

{input_label}: {actual_input}
{output_label}:
```

## Examples

### Example 1: Named Entity Extraction (Biomedical)

**Input prompt:**
```
Extract all drug names from the clinical text. Return them as a comma-separated list.

Text: "Patient was prescribed metformin 500mg twice daily and lisinopril 10mg for hypertension management."
Drugs: metformin, lisinopril

Text: "Discontinue warfarin 48 hours before surgery. Start enoxaparin bridging therapy."
Drugs: warfarin, enoxaparin

Text: "Current medications include atorvastatin 20mg, amlodipine 5mg, and omeprazole 20mg daily."
Drugs: atorvastatin, amlodipine, omeprazole

Text: "The patient reports taking ibuprofen as needed and was recently started on sertraline 50mg for depression."
Drugs:
```

**Model output:**
```
ibuprofen, sertraline
```

### Example 2: Intent Classification (Customer Support)

**Input prompt:**
```
Classify the customer message into one of these intents: billing, technical_support, account_management, general_inquiry.

Message: "I was charged twice for my subscription this month."
Intent: billing

Message: "The app keeps crashing when I try to upload photos."
Intent: technical_support

Message: "How do I change the email address on my account?"
Intent: account_management

Message: "What are your business hours?"
Intent: general_inquiry

Message: "I need to update my credit card information and my last payment didn't go through."
Intent:
```

**Model output:**
```
billing
```

## When to Use

- **Classification tasks with specific label sets** where you need the model to output from a constrained vocabulary consistently.
- **Structured extraction** where examples demonstrate exactly what to extract and how to format the output.
- **Domain-specific conventions** that the model may not infer from instructions alone (e.g., citation formats, coding styles).
- **Disambiguation of task intent** when the instruction alone could be interpreted multiple ways, but examples make the intent unambiguous.
- **Output format enforcement** when examples anchor the model to produce a consistent structure across all inputs.
- **Improving accuracy on moderate-difficulty tasks** where zero-shot performance is adequate but not sufficient.

## When to Avoid

- **Context window pressure.** If the input itself is long (e.g., full documents), examples may consume too much of the available context window.
- **Trivial tasks.** When zero-shot achieves near-perfect performance, examples add cost without benefit.
- **High-variance inputs.** If the task inputs are structurally diverse, a fixed set of examples may not cover the relevant patterns.
- **Majority label bias.** In classification, imbalanced example sets can bias the model toward overrepresented classes.
- **Rapidly changing tasks.** When the desired behavior changes frequently, maintaining a curated example set becomes burdensome.

## Cost & Performance

| Metric            | Value       | Notes                                                |
|--------------------|-------------|------------------------------------------------------|
| Token cost         | Medium      | k examples add ~50-500 tokens depending on task      |
| Latency            | Low         | Single call; slight increase from longer prompt       |
| API calls          | 1           | Single call per task                                  |
| Accuracy (simple)  | High        | 85-98% on classification with well-chosen examples    |
| Accuracy (complex) | High        | 70-90%; significant uplift over zero-shot             |
| Setup effort       | Moderate    | Requires curating and validating example sets          |
| Consistency        | High        | Examples anchor output format and label vocabulary     |

## Variants

- **Dynamic few-shot:** Examples are selected at runtime based on similarity to the current input (e.g., using embedding-based retrieval). Significantly improves performance on heterogeneous tasks. Also called "retrieval-augmented few-shot."
- **Stratified few-shot:** For classification, ensures equal representation of each label class in the example set to avoid majority bias.
- **Chain-of-thought few-shot:** Each example includes not just input-output but also an intermediate reasoning trace. Combines ICL with explicit reasoning (Wei et al., 2022).
- **Negative few-shot:** Includes examples of incorrect outputs alongside correct ones, demonstrating what not to do. Useful for teaching edge case handling.
- **Minimal few-shot:** Uses the fewest examples possible (often 2-3) to balance performance gain against token cost. Optimal for high-volume production use.

## Composability

Few-shot prompting composes naturally with many techniques:

- **+ Chain-of-Thought:** Add reasoning traces to each example. The model learns not just the input-output mapping but the reasoning pattern (Few-Shot CoT, Wei et al. 2022).
- **+ Role Prompting:** Prefix examples with a persona definition to combine domain expertise framing with demonstrated behavior.
- **+ Output Format Control:** Use examples to demonstrate the desired format (JSON, table, etc.), reinforcing format specifications given in the instruction.
- **+ Prompt Scaffolding:** Wrap examples in XML tags or delimiters to clearly separate them from instructions and the actual input.
- **+ Self-Consistency:** Generate multiple outputs and vote on the most common answer, combining ICL stability with statistical robustness.
- **+ Context Stuffing:** Provide reference documents alongside examples, grounding the model in both demonstrated behavior and factual context.

## Limitations

- **Token overhead.** Each example consumes context window space that could otherwise be used for longer inputs or more detailed instructions. With k=5 and moderately sized examples, the overhead can reach 500-1000 tokens.
- **Example selection sensitivity.** Performance is highly sensitive to which examples are chosen. Poor or unrepresentative examples can degrade performance below zero-shot baselines.
- **Order sensitivity.** The sequence in which examples are presented affects results, with models showing recency bias (favoring patterns in later examples) and primacy effects.
- **Spurious correlation risk.** The model may learn surface-level patterns from examples (e.g., output length, first-word patterns) rather than the intended task semantics.
- **Maintenance burden.** Example sets must be updated as task requirements evolve, adding operational overhead compared to zero-shot approaches.
- **Label bias.** The distribution of labels in examples can override the model's prior, leading to systematic misclassification when the example distribution does not match the true data distribution.

## Sources

**Primary:**
- Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., et al. (2020). "Language Models are Few-Shot Learners." NeurIPS 2020. https://arxiv.org/abs/2005.14165

**Secondary:**
- Min, S., Lyu, X., Holtzman, A., Arber, M., Lewis, M., Hajishirzi, H., & Zettlemoyer, L. (2022). "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?" EMNLP 2022. https://arxiv.org/abs/2202.12837
- Xie, S.M., Raghunathan, A., Liang, P., & Ma, T. (2022). "An Explanation of In-context Learning as Implicit Bayesian Inference." ICLR 2022. https://arxiv.org/abs/2111.02080
- Liu, J., Shen, D., Zhang, Y., Dolan, B., Carin, L., & Chen, W. (2022). "What Makes Good In-Context Examples for GPT-3?" DeeLIO Workshop, ACL 2022. https://arxiv.org/abs/2101.06804
- Wei, J., Wang, X., Schuurmans, D., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. https://arxiv.org/abs/2201.11903
