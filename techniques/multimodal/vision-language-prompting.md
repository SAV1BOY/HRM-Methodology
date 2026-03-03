---
id: vision-language-prompting
name: "Vision-Language Prompting"
aliases:
  - visual prompting
  - image-text prompting
  - VLM prompting
  - multimodal prompting
category: multimodal
family: multimodal-interaction
year: 2023
authors:
  - Haotian Liu
  - Chunyuan Li
  - Qingyang Wu
  - Yong Jae Lee
paper: "https://arxiv.org/abs/2304.08485"
paper_title: "Visual Instruction Tuning"
venue: "NeurIPS 2023"
code: null

complexity: medium
token_cost: variable
latency: medium
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: false

best_for:
  - image understanding and description
  - visual question answering
  - OCR and document understanding
  - visual grounding and localization
  - image-based data extraction
  - UI/UX screenshot analysis
avoid_when:
  - text-only inputs
  - models without vision capability
  - tasks requiring pixel-level precision
  - real-time video analysis
composes_with:
  - multimodal-cot
  - few-shot
  - chain-of-thought
  - output-format
  - role-prompting

tags:
  - multimodal
  - vision
  - image-understanding
  - VLM
  - visual-grounding
  - OCR
---

# Vision-Language Prompting

> **One-line summary:** Vision-Language Prompting encompasses the strategies and best practices for effectively communicating with vision-language models (VLMs) to extract, analyze, and reason about visual information from images alongside textual instructions.

## Overview

Vision-Language Prompting is the practice of crafting effective prompts for vision-language models (VLMs) — models that can process both images and text simultaneously. As VLMs have become increasingly capable (GPT-4V/4o, Claude 3/3.5/4, Gemini 1.5/2.0, LLaVA), the art of prompting them effectively has emerged as a distinct discipline. Unlike text-only prompting, VL prompting must account for the interaction between two modalities: how textual instructions direct the model's attention to specific visual elements, how visual context complements or overrides textual information, and how to elicit structured outputs from inherently unstructured visual inputs.

The foundational work in this area came from Visual Instruction Tuning (LLaVA, Liu et al. 2023), which demonstrated that language-only GPT-4 could generate high-quality visual instruction-following data to train multimodal models. This established the pattern of treating image understanding as an instruction-following task: rather than asking a model to simply "describe the image," effective VL prompting provides specific, structured instructions about what to look for, how to analyze it, and in what format to return results. The key insight is that the same image can yield dramatically different and more useful outputs depending on how the textual prompt directs the model's visual attention and analysis.

Modern VL prompting techniques include: specifying the visual task explicitly (description, analysis, comparison, extraction), providing spatial references (top-left, center, bounding coordinates), using visual markers or annotations overlaid on images (Set-of-Mark prompting), controlling output granularity (brief caption vs. exhaustive description), and combining visual analysis with downstream reasoning. These techniques are critical for production applications such as document processing, medical image analysis, autonomous driving, accessibility (image descriptions for blind users), and UI testing.

## How It Works

1. **Prepare the visual input:** Select and optionally preprocess the image — crop to relevant region, add visual markers, or overlay annotations if needed.
2. **Craft the textual prompt:** Write a clear instruction that specifies: (a) what to look at in the image, (b) what kind of analysis to perform, (c) what format the output should take.
3. **Combine image and text:** Present both the image and the textual prompt to the VLM via the appropriate API (image as base64, URL, or file attachment).
4. **Process the output:** Parse the model's response, which integrates visual understanding with the textual instruction.

### Diagram

```
┌──────────────────────────────────────────────────────────┐
│               Vision-Language Prompting                    │
│                                                           │
│  ┌─────────────────┐    ┌─────────────────────────────┐   │
│  │                  │    │  Textual Prompt:             │   │
│  │    [IMAGE]       │    │  "Analyze this dashboard     │   │
│  │   Screenshot,    │    │   screenshot. For each       │   │
│  │   Document,      │ +  │   metric, extract the        │   │
│  │   Photo, etc.    │    │   label, value, and trend    │   │
│  │                  │    │   direction. Return as JSON." │   │
│  └─────────────────┘    └─────────────────────────────┘   │
│           │                          │                     │
│           └──────────┬───────────────┘                     │
│                      v                                     │
│            ┌──────────────────┐                             │
│            │  Vision-Language  │                             │
│            │  Model (VLM)     │                             │
│            └────────┬─────────┘                             │
│                     v                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Structured Output:                                   │  │
│  │  {"metrics": [                                        │  │
│  │    {"label": "Revenue", "value": "$2.4M", "trend": ↑},│  │
│  │    {"label": "Users", "value": "12.3K", "trend": ↑},  │  │
│  │    ...                                                │  │
│  │  ]}                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Template

### General Visual Analysis
```
Analyze the provided image and answer the following question.

{specific_instruction}

Be specific about what you observe. Reference locations in the image
(top, bottom, left, right, center) when relevant.

{output_format_instruction}
```

### Visual Data Extraction
```
Extract the following information from the provided image:

{fields_to_extract}

Return the results in the following format:
{output_schema}

If a field is not visible or unclear in the image, indicate "not visible"
rather than guessing.
```

### Image Comparison
```
Compare the two provided images and describe:
1. Key similarities
2. Key differences
3. {specific_comparison_criteria}

Be precise and reference specific visual elements in each image.
```

## Examples

### Example 1: Document Data Extraction

**Input:**
```
[Image: A scanned invoice]

Extract the following fields from this invoice image:
- Invoice number
- Date
- Vendor name
- Line items (description, quantity, unit price, total)
- Subtotal, tax, and grand total

Return as JSON.
```

**Model Output:**
```json
{
  "invoice_number": "INV-2024-00847",
  "date": "2024-11-15",
  "vendor": "TechSupply Corp.",
  "line_items": [
    {
      "description": "USB-C Cable 2m",
      "quantity": 50,
      "unit_price": 8.99,
      "total": 449.50
    },
    {
      "description": "Wireless Mouse",
      "quantity": 25,
      "unit_price": 24.99,
      "total": 624.75
    }
  ],
  "subtotal": 1074.25,
  "tax": 96.68,
  "grand_total": 1170.93
}
```

### Example 2: UI Screenshot Analysis

**Input:**
```
[Image: A mobile app login screen]

You are a QA engineer. Analyze this login screen screenshot and identify:
1. All interactive elements (buttons, fields, links)
2. Any potential UI/UX issues
3. Accessibility concerns

Format as a bulleted report.
```

**Model Output:**
```
## Interactive Elements
- Email text field (center, with placeholder "Enter your email")
- Password text field (below email, with eye icon for show/hide)
- "Log In" button (blue, full-width, below password field)
- "Forgot Password?" link (below Log In button, small gray text)
- "Sign Up" link (bottom of screen)
- Social login buttons: Google, Apple (bottom section)

## Potential UI/UX Issues
- The "Forgot Password?" link is very small and low contrast (gray on
  white) — may be hard to tap on mobile
- No visible password requirements hint near the password field
- The Log In button appears disabled-style (muted blue) even when fields
  are empty — unclear affordance

## Accessibility Concerns
- The contrast ratio of the placeholder text appears below WCAG AA
  (4.5:1) standards
- Social login buttons lack visible text labels — icon-only may not
  be accessible to screen readers
- No visible focus indicators for keyboard navigation
```

### Example 3: Chart Analysis with Specific Questions

**Input:**
```
[Image: A multi-line time series chart showing CPU, Memory, and Disk
 usage over 24 hours]

Analyze this system monitoring chart and answer:
1. At what time did CPU usage peak?
2. Is there a correlation between CPU and Memory usage patterns?
3. Were there any anomalous periods?
```

**Model Output:**
```
1. **CPU Peak:** CPU usage peaked at approximately 14:30 (2:30 PM),
   reaching ~92%. There was a secondary peak around 10:00 at ~78%.

2. **CPU-Memory Correlation:** Yes, there is a positive correlation.
   Memory usage follows CPU with a slight lag (~15 minutes). When CPU
   spikes at 14:30, Memory rises from 60% to 75% by 14:45. This
   pattern is consistent throughout the day, suggesting the workload
   is both compute- and memory-intensive.

3. **Anomalous Periods:**
   - 03:00-03:30: Disk usage spikes to 95% while CPU and Memory remain
     low — likely a scheduled backup or log rotation job.
   - 14:00-15:00: All three metrics are elevated simultaneously, which
     is unusual compared to the rest of the day — suggests an
     unexpected high-load event (deployment, traffic spike, or batch job).
```

## When to Use

- Image understanding tasks: captioning, description, visual QA
- Document and form processing: invoices, receipts, contracts, IDs
- UI/UX analysis: screenshot review, accessibility auditing, design comparison
- Data extraction from visual sources: charts, tables in images, dashboards
- Scientific image analysis: medical scans, satellite imagery, microscopy
- Visual grounding: locating specific elements within images
- OCR-augmented workflows where text extraction needs contextual understanding

## When to Avoid

- Text-only inputs where no image is involved
- Models without vision capability (text-only LLMs)
- Tasks requiring sub-pixel precision or exact coordinate extraction
- Real-time video processing (current VLMs process individual frames)
- When structured data is already available in machine-readable format (no need to "read" it from an image)
- Privacy-sensitive images that should not be sent to external APIs

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token cost | Variable | Image tokens: ~85-1600 tokens depending on resolution |
| Latency | Medium-High | Vision encoding adds 1-5s depending on image size |
| Accuracy (OCR) | 90-98% | Modern VLMs rival dedicated OCR on clear documents |
| Accuracy (VQA) | 75-90% | On standard visual QA benchmarks |
| Model requirements | VLM | GPT-4V/4o, Claude 3+, Gemini, LLaVA, etc. |
| Image size limits | Varies | Typically 20MB max; high-res mode available |

## Variants

- **Direct Questioning:** Simple question about the image ("What color is the car?"). Best for straightforward visual queries.
- **Structured Extraction:** Request specific fields in a defined schema (JSON, table). Best for document processing.
- **Set-of-Mark (SoM):** Overlay numbered markers on the image and reference them in the prompt for precise visual grounding.
- **Visual Few-Shot:** Provide example image-response pairs to calibrate the model's output format and detail level.
- **Region-of-Interest:** Crop or highlight specific image regions to focus the model's attention.
- **Multi-Image Prompting:** Provide multiple images for comparison, temporal analysis, or multi-view understanding.

## Composability

- **VL Prompting + CoT:** Combine visual input with chain-of-thought instructions for visual reasoning tasks. See `multimodal-cot.md`.
- **VL Prompting + Output Format:** Request structured outputs (JSON, markdown tables) from visual analysis for downstream processing.
- **VL Prompting + Role Prompting:** Assign the model a domain-expert role ("You are a radiologist...") to guide the depth and vocabulary of visual analysis.
- **VL Prompting + Few-Shot:** Provide annotated example images to calibrate the model's analysis approach for domain-specific tasks.
- **VL Prompting + Self-Refine:** Generate initial visual analysis, then ask the model to review the image again and correct any errors.

## Limitations

- VLMs may hallucinate visual details — confidently describing elements that are not in the image or misreading text/numbers.
- Performance degrades on small, low-resolution, or blurry images where visual details are ambiguous.
- Complex images with dense information (crowded UIs, detailed technical drawings) can overwhelm the model's visual attention.
- Spatial reasoning remains imperfect — models may confuse left/right, miscount objects, or misjudge relative positions.
- Image tokenization varies by model; costs are not always predictable based on image content.
- Models may struggle with unusual visual formats (3D renders, specialized scientific visualizations, non-standard chart types).
- Cultural and contextual visual understanding may be biased toward Western/English visual conventions.
- Privacy concerns when sending images to cloud APIs — images may contain PII, proprietary content, or sensitive information.

## Sources

- **Primary:** [Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485) — Liu, H., Li, C., Wu, Q., & Lee, Y.J., NeurIPS 2023
- **GPT-4V:** [GPT-4V(ision) System Card](https://openai.com/index/gpt-4v-system-card/) — OpenAI, 2023
- **Claude:** [Anthropic Vision Documentation](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Anthropic, 2024
- **Set-of-Mark:** [Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V](https://arxiv.org/abs/2310.11441) — Yang et al., 2023
- **Survey:** [A Survey on Multimodal Large Language Models](https://arxiv.org/abs/2306.13549) — Yin et al., 2023
