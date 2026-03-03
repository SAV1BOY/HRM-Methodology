---
id: multimodal-cot
name: "Multimodal Chain-of-Thought"
aliases:
  - multimodal CoT
  - vision CoT
  - visual chain-of-thought
  - MM-CoT
category: multimodal
family: thought-generation
year: 2023
authors:
  - Zhuosheng Zhang
  - Aston Zhang
  - Mu Li
  - Hai Zhao
  - George Karypis
  - Alex Smola
paper: "https://arxiv.org/abs/2302.00923"
paper_title: "Multimodal Chain-of-Thought Reasoning in Language Models"
venue: "TMLR 2024"
code: "https://github.com/amazon-science/mm-cot"

complexity: medium
token_cost: medium
latency: medium
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for:
  - image-based reasoning tasks
  - visual question answering with multi-step logic
  - diagram and chart analysis
  - scientific figure interpretation
  - tasks requiring joint visual and textual reasoning
avoid_when:
  - text-only models without vision capability
  - simple image classification (no reasoning needed)
  - tasks where visual content is not relevant
  - models with no multimodal support
composes_with:
  - chain-of-thought
  - self-consistency
  - few-shot
  - self-refine

tags:
  - multimodal
  - reasoning
  - vision-language
  - chain-of-thought
  - visual-reasoning
---

# Multimodal Chain-of-Thought (MM-CoT)

> **One-line summary:** Multimodal CoT extends chain-of-thought prompting to vision-language models by having the model generate intermediate reasoning steps that integrate information from both images and text before arriving at a final answer.

## Overview

Multimodal Chain-of-Thought (MM-CoT), introduced by Zhang et al. (2023), extends the powerful chain-of-thought reasoning paradigm from text-only to multimodal settings. While standard CoT operates exclusively on textual inputs, many real-world reasoning tasks involve visual information — diagrams, charts, photographs, scientific figures — that must be jointly processed with text. MM-CoT prompts vision-language models to generate explicit reasoning steps that reference and integrate both visual and textual information before producing a final answer.

The key challenge in multimodal reasoning is that models often fail when they need to extract specific information from an image and use it in a multi-step reasoning chain. For example, reading a bar chart value, understanding a geometric figure's properties, or interpreting a scientific diagram's labels are all steps that must be correctly executed before any reasoning can begin. MM-CoT addresses this by explicitly requiring the model to describe its visual observations as part of the reasoning chain, creating an "observation → reasoning → conclusion" pattern that bridges the visual and linguistic modalities.

The original MM-CoT paper proposed a two-stage framework for smaller models: first generate a rationale (reasoning chain incorporating visual features) and then produce the answer conditioned on the rationale. For large vision-language models (GPT-4V, Claude 3+, Gemini), this can be accomplished in a single prompt by instructing the model to "describe what you see, then reason step by step." On the ScienceQA benchmark, MM-CoT achieved state-of-the-art results, demonstrating the effectiveness of structured multimodal reasoning. The approach has since become a standard practice for visual reasoning with modern VLMs.

## How It Works

1. **Present the visual and textual input:** Provide the image(s) along with the question to the vision-language model.
2. **Instruct multimodal reasoning:** Prompt the model to first describe relevant visual information from the image, then reason step by step using both the visual observations and the textual question.
3. **Model generates visual-textual reasoning chain:** The model produces a chain of reasoning that explicitly references visual elements (colors, labels, positions, quantities read from the image) and combines them with textual reasoning.
4. **Extract the final answer:** The answer follows from the multimodal reasoning chain.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   PROMPT                                  │
│                                                           │
│  ┌──────────────┐   ┌──────────────────────────────────┐  │
│  │              │   │ Question: "According to the bar  │  │
│  │   [IMAGE]    │   │ chart, which category had the    │  │
│  │  Bar Chart   │   │ highest growth rate between      │  │
│  │              │   │ 2020 and 2023?"                   │  │
│  └──────────────┘   └──────────────────────────────────┘  │
│                                                           │
│  Instruction: "First describe the relevant data from     │
│  the image, then reason step by step to answer."          │
│                                                           │
├──────────────────────────────────────────────────────────┤
│               MODEL GENERATES                             │
│                                                           │
│  Visual Observations:                                     │
│  - Category A: 2020=$40M, 2023=$52M                       │
│  - Category B: 2020=$25M, 2023=$45M                       │
│  - Category C: 2020=$60M, 2023=$72M                       │
│                                                           │
│  Reasoning:                                               │
│  - Growth A: (52-40)/40 = 30%                             │
│  - Growth B: (45-25)/25 = 80%                             │
│  - Growth C: (72-60)/60 = 20%                             │
│                                                           │
│  Answer: Category B had the highest growth rate (80%).    │
└──────────────────────────────────────────────────────────┘
```

## Template

### For Large Vision-Language Models (Single-Pass)
```
Look at the provided image and answer the following question.

Question: {question}

First, describe the relevant information you observe in the image.
Then, reason step by step using both the visual information and the
question to arrive at your answer.

Visual observations:
Step-by-step reasoning:
Final answer:
```

### For Structured Two-Stage Approach
```
Stage 1 — Generate Rationale:
Given the image and question below, generate a detailed reasoning chain
that explains how to arrive at the answer. Reference specific visual
elements from the image.

Question: {question}
Reasoning:

Stage 2 — Generate Answer:
Given the question, image, and the following reasoning, provide the
final answer.

Question: {question}
Reasoning: {generated_rationale}
Answer:
```

## Examples

### Example 1: Scientific Diagram

**Input:**
```
[Image: A food web diagram showing: Sun → Grass → Rabbit → Fox,
 Grass → Grasshopper → Frog → Snake → Hawk, Rabbit → Hawk]

Question: If the grasshopper population decreases significantly,
which organisms would be MOST directly affected?
```

**Model Output:**
```
Visual Observations:
- The food web shows: Sun provides energy to Grass
- Grass is eaten by both Rabbit and Grasshopper
- Grasshopper is eaten by Frog
- Frog is eaten by Snake
- Snake is eaten by Hawk
- Rabbit is eaten by both Fox and Hawk

Step-by-step reasoning:
1. Grasshopper is consumed by Frog (direct predator-prey relationship)
2. If grasshoppers decrease, Frogs lose a primary food source → Frog
   population likely decreases
3. Grass would experience less herbivory from grasshoppers → Grass may
   increase
4. Snake depends on Frog → indirectly affected (secondary effect)
5. The MOST directly affected organisms are Frog (loses food) and Grass
   (reduced predation)

Final answer: Frogs would be most directly affected as they lose their
primary prey, and Grass would be directly affected by reduced herbivory.
```

### Example 2: Chart Reading with Calculation

**Input:**
```
[Image: A pie chart showing market share - Company A: 35%, Company B: 28%,
 Company C: 22%, Others: 15%]

Question: If the total market is worth $4.2 billion, how much more revenue
does Company A generate than Company C?
```

**Model Output:**
```
Visual Observations:
- Company A holds 35% of the market
- Company C holds 22% of the market
- Total market value given: $4.2 billion

Step-by-step reasoning:
1. Company A revenue: 35% × $4.2B = 0.35 × $4.2B = $1.47B
2. Company C revenue: 22% × $4.2B = 0.22 × $4.2B = $0.924B
3. Difference: $1.47B − $0.924B = $0.546B

Final answer: Company A generates $546 million more in revenue than
Company C.
```

## When to Use

- Questions about images that require multi-step reasoning (not just description)
- Scientific figure interpretation where conclusions must be drawn from visual data
- Chart and graph analysis involving calculations on visually presented data
- Diagram-based reasoning (flowcharts, circuit diagrams, food webs, architecture diagrams)
- Medical image analysis where observations must be linked to diagnostic reasoning
- Document understanding where tables, figures, and text must be jointly processed

## When to Avoid

- Text-only models that lack vision capability
- Simple image classification or object detection (no reasoning chain needed)
- Tasks where the image is purely decorative or not relevant to the question
- When visual information is already transcribed/described in the text
- Models with weak vision encoders that cannot accurately extract visual details

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 1.5-3x base | Reasoning chain + visual descriptions |
| Latency | Medium | Single call; vision encoding adds processing time |
| Accuracy gain | +10-20% | Over direct answering on visual reasoning benchmarks |
| ScienceQA accuracy | 91.68% | State-of-the-art at time of publication |
| Model requirements | VLM required | GPT-4V, Claude 3+, Gemini, LLaVA, etc. |

## Variants

- **Two-Stage MM-CoT:** Separate rationale generation and answer generation stages (original paper approach for smaller models).
- **Single-Pass MM-CoT:** Modern VLMs handle both stages in one generation pass with appropriate prompting.
- **MM-CoT with Set-of-Mark:** Overlay numbered markers on the image to give the model precise visual references for its reasoning.
- **Interleaved MM-CoT:** Alternate between image patches and text reasoning for complex multi-image scenarios.
- **Region-Grounded MM-CoT:** Ground each reasoning step to specific bounding boxes or regions in the image.

## Composability

- **MM-CoT + Self-Consistency:** Generate multiple multimodal reasoning paths and majority-vote the answer. Reduces errors from visual misinterpretation.
- **MM-CoT + Self-Refine:** Generate initial visual reasoning, then ask the model to verify its visual observations against the image before finalizing.
- **MM-CoT + Few-Shot:** Provide image-text exemplars that demonstrate the desired level of visual detail and reasoning depth.
- **MM-CoT + Retrieval:** Retrieve similar image-question pairs from a database to provide as in-context examples.

## Limitations

- Accuracy depends heavily on the vision encoder's ability to extract fine-grained visual details (small text, precise values, subtle color differences).
- Models may hallucinate visual details that are not present in the image or misread specific values from charts and graphs.
- Complex images with dense information (detailed technical diagrams, crowded charts) remain challenging.
- The reasoning chain quality depends on the initial visual observations — errors in observation propagate through all subsequent reasoning steps.
- Two-stage approaches increase latency and cost; single-pass approaches depend on model capability.
- Performance varies significantly across VLM architectures; not all multimodal models benefit equally from CoT prompting.
- No standardized way to verify that the model's visual observations are correct before reasoning begins.

## Sources

- **Primary:** [Multimodal Chain-of-Thought Reasoning in Language Models](https://arxiv.org/abs/2302.00923) — Zhang, Z., Zhang, A., Li, M., Zhao, H., Karypis, G., & Smola, A., TMLR 2024
- **Code:** [GitHub: amazon-science/mm-cot](https://github.com/amazon-science/mm-cot)
- **Related:** [Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485) — Liu et al., NeurIPS 2023
- **Related:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) — Wei et al., NeurIPS 2022
- **Related:** [Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V](https://arxiv.org/abs/2310.11441) — Yang et al., 2023
