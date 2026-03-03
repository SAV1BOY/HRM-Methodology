---
id: directional-stimulus
name: "Directional Stimulus Prompting"
aliases: ["DSP", "Directional Stimulus", "Hint Prompting", "Keyword Steering"]
category: perception
family: stimulus-guidance
year: 2023
authors: ["Zekun Li", "Baolin Peng", "Pengcheng He", "Michel Galley", "Jianfeng Gao", "Xifeng Yan"]
paper: "https://arxiv.org/abs/2302.11520"
paper_title: "Guiding Large Language Models via Directional Stimulus Prompting"
venue: "arXiv 2023"
code: null

complexity: low
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["targeted summarization", "keyword-guided generation", "steering output focus", "dialogue response shaping", "constrained creative writing"]
avoid_when: ["open-ended exploration needed", "no clear directional intent", "keywords would over-constrain output", "task requires broad coverage"]
composes_with: ["chain-of-thought", "few-shot", "system-2-attention", "retrieval-augmented-generation"]

tags: ["perception", "stimulus", "keywords", "hints", "steering", "guidance", "focus"]
---

# Directional Stimulus Prompting

> **One-line summary:** Augment prompts with small hint keywords or phrases that steer the LLM's generation toward desired aspects of the output without fully specifying the answer.

## Overview

Directional Stimulus Prompting (DSP) addresses a fundamental challenge in prompt engineering: how to guide a language model toward specific aspects of a desired output without being so prescriptive that you might as well write the answer yourself. The technique works by including carefully chosen "stimulus" keywords or short phrases in the prompt that act as gentle nudges, directing the model's attention and generation toward particular topics, angles, or details.

The approach was introduced by Li et al. (2023), who demonstrated that small, targeted hints can significantly improve the quality and relevance of generated text across tasks like summarization, dialogue generation, and question answering. The key insight is that LLMs are highly sensitive to lexical cues in the prompt, and strategically placed keywords can activate relevant knowledge and framing without the rigidity of fully specified templates. In the paper, the authors explored both manually crafted and automatically generated (via a smaller tuned policy model) directional stimuli.

Unlike techniques that filter or rewrite the context (like S2A or SimToM), DSP operates additively: it enriches the prompt with signal rather than removing noise. This makes it lightweight --- requiring only a single LLM call --- and easy to integrate into existing workflows. The stimuli can be as simple as a few keywords or as structured as a short phrase describing the desired angle.

## How It Works

1. **Task Analysis:** Identify what specific aspect, angle, or focus the output should emphasize. Determine which keywords or phrases would best guide the model toward this focus.
2. **Stimulus Construction:** Craft a small set of hint keywords, key phrases, or directional cues. These should be specific enough to steer output but general enough to allow the model creative freedom.
3. **Prompt Assembly:** Integrate the directional stimuli into the prompt alongside the original input (context, question, or instruction). Place hints where they will have maximum influence --- typically near the instruction or immediately before the expected output.
4. **Generation:** The LLM processes the augmented prompt in a single call, producing output that is naturally guided by the embedded stimuli.

### Diagram

```
┌─────────────────────┐     ┌─────────────────────┐
│   Original Input    │     │  Directional Hints   │
│   (context, task)   │     │  (keywords/phrases)  │
└────────┬────────────┘     └────────┬────────────┘
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Augmented Prompt     │
         │  Input + Hints        │
         │  + Task Instruction   │
         └───────────┬───────────┘
                     │
                     ▼  (single LLM call)
         ┌───────────────────────┐
         │  Steered Output       │
         │  (focused on hints)   │
         └───────────────────────┘
```

## Template

```
{task_instruction}

{input_context}

Hints: Focus on the following aspects: {keyword_1}, {keyword_2}, {keyword_3}.

{output_instruction}
```

**Summarization variant:**
```
Summarize the following article. Your summary should particularly address
the aspects indicated by the hint keywords.

Article:
{article_text}

Hint keywords: {keyword_1}, {keyword_2}, {keyword_3}

Summary:
```

**Dialogue variant:**
```
Generate a response in the conversation below. The response should naturally
incorporate or address the following topics: {hint_phrases}.

Conversation:
{dialogue_history}

Response:
```

## Examples

### Example 1: Guided Summarization

**Input:**
```
Summarize the following article. Your summary should particularly address
the aspects indicated by the hint keywords.

Article:
Tesla reported Q3 2023 earnings that missed analyst expectations. Revenue
came in at $23.4 billion, a 9% increase year-over-year but below the
consensus estimate of $24.1 billion. The company's automotive gross margin
fell to 18.7%, down from 27.9% a year ago, largely due to aggressive price
cuts across its vehicle lineup. CEO Elon Musk emphasized the company's
progress in AI and its Dojo supercomputer initiative. The Cybertruck is
expected to begin deliveries later in the quarter. Tesla's energy generation
and storage segment saw record revenue of $1.56 billion. The stock fell 4%
in after-hours trading.

Hint keywords: margin pressure, price cuts, market reaction

Summary:
```

**Output:**
```
Tesla's Q3 2023 results highlighted growing margin pressure as the company's
aggressive price cuts drove automotive gross margin down sharply to 18.7%
from 27.9% a year earlier. While revenue grew 9% year-over-year to $23.4
billion, it fell short of analyst expectations, and the market reaction was
negative with shares dropping 4% in after-hours trading. The margin erosion
from price reductions across Tesla's vehicle lineup overshadowed positive
developments in the energy segment and upcoming Cybertruck deliveries.
```

### Example 2: Steered Dialogue Response

**Input:**
```
Generate a response in the conversation below. The response should naturally
incorporate or address the following topics: weekend plans, Italian food.

Conversation:
User: Hey, I've been so busy with work this week. I barely had time to eat
      properly.
Assistant: That sounds exhausting! It's important to take care of yourself
           even during busy periods.
User: Yeah, I know. At least Friday is almost here.

Response:
```

**Output:**
```
That's great — the weekend is almost within reach! Do you have any plans to
unwind? If you haven't been eating well, maybe this weekend would be a perfect
time to treat yourself to a nice meal. There's nothing like a good Italian
dinner — a hearty pasta or a fresh margherita pizza — to reset after a
grueling week. Do you have a favorite Italian place nearby?
```

## When to Use

- You want to steer the model toward specific topics or angles without over-constraining
- Summarization tasks where certain aspects need emphasis over others
- Dialogue systems that need to naturally introduce specific topics
- Creative writing with thematic guidance (e.g., "tone: melancholic, setting: coastal")
- When a small tuned model or retrieval system can provide hint keywords automatically
- Keyword-guided question answering where you want the model to focus on particular entities

## When to Avoid

- Fully open-ended brainstorming where any direction is valid
- Tasks where the keywords would bias the output in harmful ways
- When the hints are too vague to provide meaningful steering
- Highly constrained outputs where a strict template would be more appropriate
- When the input already contains strong enough signal about the desired focus

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | +5-20 tokens | Only the hint keywords/phrases added |
| Latency | ~1x | Single LLM call, negligible overhead |
| Quality gain | +10-20% | On targeted summarization and dialogue tasks (per paper) |
| Implementation effort | Very low | Just add keywords to existing prompts |
| API calls | 1 | No additional calls needed |

## Variants

- **Automated DSP:** Use a smaller fine-tuned model (policy model) to generate optimal hint keywords for each input, as proposed in the original paper.
- **Retrieval-Augmented DSP:** Extract keywords from retrieved documents to use as directional stimuli, ensuring the output aligns with the most relevant retrieved content.
- **Negative DSP:** Include keywords to explicitly avoid: "Do NOT focus on: X, Y, Z." Useful for steering away from common but undesired framings.
- **Graduated DSP:** Provide keywords with importance weights: "Primary focus: X (high), Y (medium). Secondary: Z (low)."
- **Chain DSP:** Use the output of one DSP call to generate better keywords for a refined second call.

## Composability

- **DSP + Chain-of-Thought:** Provide hint keywords that guide not just the final answer but the reasoning steps (e.g., "Consider: edge cases, boundary conditions, overflow").
- **DSP + RAG:** Use top retrieved document keywords as directional stimuli to keep the generation grounded in the retrieved content.
- **DSP + Few-Shot:** Combine worked examples with keyword hints to demonstrate both the desired format and the desired focus.
- **DSP + S2A:** Use S2A to clean the context first, then apply DSP to steer generation from the cleaned context toward specific aspects.

## Limitations

- Effectiveness depends heavily on choosing the right keywords; poor keywords can mislead the model
- The model may over-index on hint keywords, producing output that feels forced or unnatural
- No guarantee the model will address all provided keywords, especially with longer lists
- Automatically generating optimal keywords requires a separate model or retrieval system
- Keyword selection introduces a human bottleneck unless automated
- The technique provides soft guidance, not hard constraints --- the model may still drift off-topic

## Sources

- **Primary:** [Guiding Large Language Models via Directional Stimulus Prompting](https://arxiv.org/abs/2302.11520) — Li et al., 2023
- **Related:** [Keyword-based Summarization](https://arxiv.org/abs/2012.07436) — Background on keyword-guided summarization approaches
- **Context:** [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916) — Kojima et al., 2022 — Related work on prompt augmentation
