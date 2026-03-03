---
id: one-shot
name: "One-Shot Prompting"
aliases:
  - one-shot
  - single-example
  - 1-shot
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
token_cost: low
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - format demonstration with minimal token overhead
  - tasks where one example suffices to disambiguate
  - rapid prompt development with tight token budgets
  - style or tone matching
  - structured output anchoring
avoid_when:
  - task has multiple distinct categories to demonstrate
  - complex reasoning patterns need to be shown
  - single example may introduce unwanted bias
  - task requires coverage of diverse edge cases
  - classification with more than two classes
composes_with:
  - role-prompting
  - output-format
  - prompt-scaffolding
  - chain-of-thought
  - context-stuffing
tags:
  - demonstration-based
  - foundational
  - low-cost
  - single-example
  - format-anchoring
---

# One-Shot Prompting

> **One-line summary:** Provide exactly one input-output demonstration example before the task input, establishing the expected pattern with minimal token cost.

## Overview

One-shot prompting is the minimal form of demonstration-based prompting, using exactly one example to establish the input-output pattern before presenting the actual task. While Brown et al. (2020) primarily focused on few-shot (k > 1) settings in the GPT-3 paper, they also evaluated one-shot performance and found it to be a surprisingly effective middle ground between zero-shot and few-shot approaches. A single well-chosen example can anchor the model's understanding of task format, output structure, and expected level of detail.

The practical value of one-shot prompting lies in its efficiency. A single example adds only a modest number of tokens to the prompt -- typically 50-200 tokens -- while providing a concrete reference pattern that eliminates the ambiguity inherent in instruction-only prompts. This makes it the preferred approach when token budgets are constrained (e.g., real-time applications with strict latency requirements, or workflows that process long documents consuming most of the context window).

Research on in-context learning has shown that the marginal value of each additional example follows a roughly logarithmic curve: the first example provides the largest boost, with diminishing returns for subsequent examples. Min et al. (2022) further demonstrated that the format and input distribution of examples carry significant explanatory power, suggesting that even a single example's primary function is to establish structural expectations rather than to teach the task itself. This makes one-shot prompting particularly effective when the model already understands the task semantics but needs guidance on output format.

## How It Works

1. **Select one high-quality example.** Choose an input-output pair that is representative of the most common case for the task. Avoid edge cases or atypical inputs for the single demonstration.

2. **Format the example clearly.** Use consistent labeling (e.g., "Input:" / "Output:") to delineate the example's components so the model can parse the pattern unambiguously.

3. **Match the example format to the task.** Ensure the example output exhibits exactly the structure, length, style, and level of detail you want the model to produce.

4. **Append the actual task input.** Present the new input in the identical format used in the example, leaving the output position for the model to complete.

5. **Generate and validate.** The model produces output consistent with the demonstrated pattern. If the output deviates, consider whether the example was sufficiently clear or if additional examples (few-shot) are needed.

### Diagram

```
┌──────────────────────────────────┐
│  DEMONSTRATION (1 example)       │
│  ┌────────────────────────────┐  │
│  │ Input:  "Example input"    │  │
│  │ Output: "Example output"   │  │
│  └────────────────────────────┘  │
│                                  │
│  ACTUAL TASK                     │
│  ┌────────────────────────────┐  │
│  │ Input:  "Real input"       │  │
│  │ Output: ???                │  │
│  └────────────────────────────┘  │
│              ▼                   │
│     ┌──────────────┐            │
│     │    MODEL      │            │
│     │  (one-shot)   │            │
│     └──────┬───────┘            │
│              ▼                   │
│  Output: "Generated output"     │
└──────────────────────────────────┘
```

## Template

```
{task_instruction}

{input_label}: {example_input}
{output_label}: {example_output}

{input_label}: {actual_input}
{output_label}:
```

**Alternative template with explicit section markers:**

```
{task_instruction}

### Example ###
{input_label}: {example_input}
{output_label}: {example_output}

### Task ###
{input_label}: {actual_input}
{output_label}:
```

## Examples

### Example 1: Code Documentation (Python)

**Input prompt:**
```
Generate a Google-style docstring for the given Python function.

Function:
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

Docstring:
"""Calculate Body Mass Index (BMI) from weight and height.

Args:
    weight_kg (float): Body weight in kilograms.
    height_m (float): Height in meters.

Returns:
    float: BMI value calculated as weight divided by height squared.
"""

Function:
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

Docstring:
```

**Model output:**
```
"""Calculate the great-circle distance between two points on Earth using the Haversine formula.

Args:
    lat1 (float): Latitude of the first point in degrees.
    lon1 (float): Longitude of the first point in degrees.
    lat2 (float): Latitude of the second point in degrees.
    lon2 (float): Longitude of the second point in degrees.

Returns:
    float: Distance between the two points in kilometers.
"""
```

### Example 2: Data Transformation (Structured to Prose)

**Input prompt:**
```
Convert the structured event data into a natural-language calendar notification.

Event Data:
- Title: Team Standup
- Date: Monday, March 10, 2025
- Time: 9:00 AM - 9:15 AM
- Location: Zoom (link: https://zoom.us/j/123)
- Attendees: Engineering team

Notification:
"Reminder: Team Standup is scheduled for Monday, March 10, 2025 from 9:00 AM to 9:15 AM via Zoom. The engineering team should join at https://zoom.us/j/123."

Event Data:
- Title: Q1 Budget Review
- Date: Wednesday, March 12, 2025
- Time: 2:00 PM - 3:30 PM
- Location: Conference Room B
- Attendees: Finance, Department Heads

Notification:
```

**Model output:**
```
"Reminder: Q1 Budget Review is scheduled for Wednesday, March 12, 2025 from 2:00 PM to 3:30 PM in Conference Room B. Finance and Department Heads should attend."
```

## When to Use

- **Format anchoring** when the primary goal is to show the model the exact output structure you want (JSON schema, table layout, specific prose style).
- **Token-constrained environments** where context window space is at a premium but zero-shot performance is insufficient.
- **Simple transformation tasks** (e.g., reformatting, translation, conversion) where one example fully captures the mapping pattern.
- **Style or tone matching** where a single example establishes the voice, register, and stylistic conventions for the output.
- **Binary classification** where one example of the positive class (or one of each class, making it technically two-shot) sufficiently anchors the label vocabulary.
- **Rapid iteration** during prompt development, when you want to quickly test whether an example-based approach will improve over zero-shot.

## When to Avoid

- **Multi-class classification** where a single example cannot demonstrate all possible output categories, leading to bias toward the shown class.
- **Complex reasoning tasks** where the reasoning pattern has multiple valid approaches that a single example cannot capture.
- **High-stakes applications** where the single example might anchor the model too strongly to a specific pattern, causing it to miss important variations.
- **Tasks with diverse output structures** where different inputs legitimately require different output formats.
- **When the example introduces unintended bias** -- a single example is more likely to anchor on surface features (length, word choice, structure) that may not generalize.

## Cost & Performance

| Metric            | Value       | Notes                                                    |
|--------------------|-------------|----------------------------------------------------------|
| Token cost         | Low         | ~50-200 tokens for one example; minimal overhead          |
| Latency            | Low         | Negligible increase over zero-shot                        |
| API calls          | 1           | Single call per task                                      |
| Accuracy (simple)  | High        | 85-95%; major uplift over zero-shot for format tasks      |
| Accuracy (complex) | Moderate    | 60-80%; less robust than few-shot for nuanced tasks       |
| Setup effort       | Low         | Only one example to curate and validate                   |
| Consistency        | Moderate-High | Format consistency improves significantly vs. zero-shot  |

## Variants

- **Contrastive one-shot:** Provide one correct and one incorrect example, demonstrating both what to do and what to avoid. Uses two examples but serves as a single-contrast teaching pattern.
- **Template one-shot:** The example is a template with placeholders rather than a concrete instance, showing the model the structural pattern abstractly.
- **Annotated one-shot:** The single example includes inline annotations or comments explaining why the output is structured a certain way, combining demonstration with instruction.
- **Dynamic one-shot:** The single example is selected at runtime from a pool based on similarity to the current input, ensuring maximum relevance.

## Composability

One-shot prompting integrates smoothly with other techniques while maintaining its low token footprint:

- **+ Role Prompting:** Set a persona, then demonstrate the desired behavior with one example. The role provides domain context while the example anchors format.
- **+ Output Format Control:** Use the example to demonstrate the target format (e.g., JSON, CSV) while the instruction specifies the schema. The example serves as a concrete instantiation of the format specification.
- **+ Chain-of-Thought:** Include a reasoning trace in the single example, teaching the model both the reasoning pattern and the output format simultaneously (one-shot CoT).
- **+ Prompt Scaffolding:** Wrap the example in XML tags (e.g., `<example>...</example>`) to clearly delineate it from the instruction and task input.
- **+ Context Stuffing:** Provide reference documents alongside a single example, combining grounding with pattern demonstration. Particularly effective when context windows are limited.

## Limitations

- **Anchoring to the single example.** The model may over-index on surface features of the one example (length, vocabulary, structure) rather than learning the general task pattern.
- **No coverage of diversity.** A single example cannot represent the full range of valid inputs and outputs, potentially causing the model to handle unusual inputs poorly.
- **Class imbalance by design.** For classification tasks, showing one class inherently biases the model toward that class, since the prompt's empirical distribution is 100% one label.
- **Fragile to example quality.** With only one demonstration, a poorly chosen example has outsized negative impact compared to few-shot, where other examples can compensate.
- **Difficult to teach exceptions.** Complex tasks with rules and exceptions cannot be fully demonstrated with a single example, requiring either additional instructions or more examples.

## Sources

**Primary:**
- Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., et al. (2020). "Language Models are Few-Shot Learners." NeurIPS 2020. https://arxiv.org/abs/2005.14165

**Secondary:**
- Min, S., Lyu, X., Holtzman, A., Arber, M., Lewis, M., Hajishirzi, H., & Zettlemoyer, L. (2022). "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?" EMNLP 2022. https://arxiv.org/abs/2202.12837
- Liu, J., Shen, D., Zhang, Y., Dolan, B., Carin, L., & Chen, W. (2022). "What Makes Good In-Context Examples for GPT-3?" DeeLIO Workshop, ACL 2022. https://arxiv.org/abs/2101.06804
- Zhao, Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021). "Calibrate Before Use: Improving Few-Shot Performance of Language Models." ICML 2021. https://arxiv.org/abs/2102.09690
