---
id: zero-shot
name: "Zero-Shot Instruction Prompting"
aliases:
  - zero-shot
  - direct-prompting
  - instruction-only
  - vanilla-prompting
category: foundations
family: instruction-based
year: 2021
authors:
  - Jason Wei
  - Maarten Bosma
  - Vincent Y. Zhao
  - Kelvin Guu
  - Adams Wei Yu
  - Brian Lester
  - Nan Du
  - Andrew M. Dai
  - Quoc V. Le
paper: "https://arxiv.org/abs/2109.01652"
paper_title: "Finetuned Language Models Are Zero-Shot Learners"
venue: "ICLR 2022"
code: null
complexity: low
token_cost: low
latency: low
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - simple classification tasks
  - straightforward Q&A
  - text generation with clear objectives
  - rapid prototyping of prompt ideas
  - tasks where examples are unavailable
  - baseline benchmarking of model capability
avoid_when:
  - task requires very specific output formatting
  - domain is highly specialized or ambiguous
  - consistent structured output is critical
  - task has nuanced edge cases that need demonstration
  - high accuracy on complex reasoning is required
composes_with:
  - role-prompting
  - output-format
  - prompt-scaffolding
  - emotion-prompting
  - prompt-repetition
  - chain-of-thought
tags:
  - baseline
  - instruction-following
  - zero-shot
  - foundational
  - low-cost
---

# Zero-Shot Instruction Prompting

> **One-line summary:** Provide a clear natural-language instruction to the model with no examples, relying entirely on the model's pre-trained and instruction-tuned knowledge to perform the task.

## Overview

Zero-shot instruction prompting is the most fundamental prompting technique and serves as the baseline against which all other methods are measured. The approach was formally studied by Wei et al. (2021) in the FLAN paper, which demonstrated that language models fine-tuned on a collection of tasks described via instructions can perform well on entirely unseen tasks without any task-specific examples. This finding established that instruction-tuned models possess emergent generalization capabilities that can be unlocked through well-crafted natural language directives alone.

The power of zero-shot prompting lies in its simplicity and efficiency. By providing only an instruction and the input, the technique minimizes token usage, latency, and prompt engineering overhead. Modern instruction-tuned models (GPT-4, Claude, Gemini, Llama-3-Instruct) have been specifically optimized for this interaction pattern, making zero-shot prompting surprisingly effective for a wide range of tasks. The quality of results depends heavily on the clarity, specificity, and completeness of the instruction itself.

Despite its simplicity, zero-shot prompting should not be dismissed as naive. Research has shown that careful instruction design -- including specifying the desired output format, providing constraints, and clarifying edge cases -- can dramatically improve zero-shot performance. The technique forms the foundation upon which more sophisticated methods like chain-of-thought, few-shot, and role prompting are built.

## How It Works

1. **Define the task clearly.** Formulate a precise natural-language instruction that describes what the model should do, including any constraints on format, length, or style.

2. **Provide the input.** Supply the data or content the model needs to process, clearly delineated from the instruction.

3. **Submit the prompt.** Send the combined instruction and input to the model in a single call.

4. **Receive the output.** The model generates a response based solely on its pre-trained knowledge and the instruction provided.

5. **Evaluate and iterate.** Assess whether the output meets requirements. If not, refine the instruction wording, add constraints, or consider escalating to a more advanced technique.

### Diagram

```
┌─────────────────────────────┐
│      INSTRUCTION            │
│  "Classify the following    │
│   review as positive or     │
│   negative."                │
├─────────────────────────────┤
│      INPUT                  │
│  "The battery life is       │
│   amazing but the screen    │
│   is too dim."              │
├─────────────────────────────┤
│          ▼                  │
│   ┌─────────────┐          │
│   │    MODEL     │          │
│   │  (zero-shot) │          │
│   └──────┬──────┘          │
│          ▼                  │
│      OUTPUT                 │
│  "Positive"                 │
└─────────────────────────────┘
```

## Template

```
{instruction}

{input_text}
```

**Expanded template with constraints:**

```
{instruction}

Constraints:
- {constraint_1}
- {constraint_2}

Input:
{input_text}
```

## Examples

### Example 1: Sentiment Classification (Product Reviews)

**Input prompt:**
```
Classify the sentiment of the following product review as "positive", "negative", or "mixed". Respond with only the sentiment label.

Review: "I've been using this keyboard for three months now. The mechanical switches feel great and the RGB lighting is customizable. However, the wrist rest started peeling after two weeks and customer support was unhelpful."
```

**Model output:**
```
mixed
```

### Example 2: Summarization (News Article)

**Input prompt:**
```
Summarize the following news article in exactly two sentences. Focus on the key facts and outcomes.

Article: "The European Central Bank announced on Thursday that it would raise interest rates by 25 basis points, bringing the main refinancing rate to 4.5%. The decision, which was widely anticipated by markets, marks the tenth consecutive rate hike since July 2022. ECB President Christine Lagarde stated that inflation remains 'too high for too long' and indicated that future decisions would be data-dependent. Bond yields across the eurozone rose modestly following the announcement, while the euro strengthened slightly against the dollar."
```

**Model output:**
```
The European Central Bank raised interest rates by 25 basis points to 4.5%, marking its tenth consecutive hike since July 2022. ECB President Lagarde cited persistent inflation concerns and signaled that future rate decisions would depend on incoming economic data.
```

## When to Use

- **Simple, well-defined tasks** where the instruction alone provides sufficient clarity (e.g., translation, classification, summarization).
- **Rapid prototyping** when exploring whether a model can handle a task before investing in example curation.
- **Token-constrained environments** where minimizing prompt length is critical for cost or context window reasons.
- **High-volume batch processing** where the overhead of curating examples for each task variant is impractical.
- **Baseline establishment** before evaluating whether few-shot or chain-of-thought techniques provide meaningful improvement.
- **General knowledge tasks** that align well with the model's training distribution.

## When to Avoid

- **Highly specialized domains** where the model's training data may lack sufficient coverage (e.g., rare medical conditions, niche legal precedents).
- **Tasks requiring precise output formatting** that the model consistently fails to follow without demonstrations.
- **Complex multi-step reasoning** where chain-of-thought or decomposition techniques significantly outperform direct instruction.
- **Ambiguous tasks** where the instruction alone cannot convey the full range of expected behaviors -- examples would disambiguate.
- **Safety-critical applications** where consistent, predictable behavior is essential and must be validated through structured prompting.

## Cost & Performance

| Metric            | Value     | Notes                                              |
|--------------------|-----------|----------------------------------------------------|
| Token cost         | Low       | Only instruction + input; no example overhead       |
| Latency            | Low       | Minimal prompt length means fast time-to-first-token|
| API calls          | 1         | Single call per task                                |
| Accuracy (simple)  | High      | 80-95% on well-defined tasks with modern models     |
| Accuracy (complex) | Moderate  | 50-75%; degrades on nuanced or multi-step tasks     |
| Setup effort       | Minimal   | No example curation or template engineering needed  |
| Consistency        | Moderate  | Output format may vary across runs without examples |

## Variants

- **Constrained zero-shot:** Adds explicit output constraints (format, length, vocabulary) to the instruction without providing examples. Bridges the gap toward output-format control techniques.
- **Guided zero-shot:** Includes hints or partial structure in the instruction (e.g., "Think about X before answering") without full chain-of-thought prompting. Lightweight reasoning scaffold.
- **Negative zero-shot:** Specifies what the model should *not* do (e.g., "Do not include explanations. Do not use bullet points."). Reduces unwanted output patterns.
- **Multi-task zero-shot:** Chains multiple instructions in a single prompt, asking the model to perform several tasks on the same input (e.g., "Classify, summarize, and extract entities from the following text.").

## Composability

Zero-shot instruction prompting is the most composable foundational technique:

- **+ Role Prompting:** Prefix the instruction with a persona to bias the model's tone, expertise level, or perspective. Example: "You are an expert botanist. Classify the following plant description..."
- **+ Output Format Control:** Append format specifications to the instruction. Example: "...respond in JSON with keys 'sentiment' and 'confidence'."
- **+ Prompt Scaffolding:** Wrap the instruction and input in XML tags or delimiters for clarity in complex prompts with multiple sections.
- **+ Chain-of-Thought:** Add "Think step by step" or "Explain your reasoning" to the instruction to elicit reasoning traces (zero-shot CoT, Kojima et al. 2022).
- **+ Emotion Prompting:** Append motivational or stakes-raising phrases to the instruction to improve engagement and accuracy on certain tasks.
- **+ Prompt Repetition:** Repeat critical constraints at the beginning and end of the prompt to reinforce adherence.

## Limitations

- **Format inconsistency.** Without examples to anchor the output format, models may produce varying structures across invocations, complicating downstream parsing.
- **Ambiguity sensitivity.** Instructions that are vague or underspecified lead to unpredictable outputs. The technique offers no mechanism to disambiguate beyond rewording.
- **Domain coverage gaps.** Performance degrades on tasks outside the model's training distribution, and zero-shot provides no mechanism for in-context learning of new patterns.
- **No error correction signal.** Unlike few-shot prompting, there is no implicit demonstration of correct behavior, so the model relies entirely on its prior.
- **Ceiling effects on complex tasks.** For tasks requiring multi-step reasoning, structured output, or domain-specific conventions, zero-shot consistently underperforms more sophisticated techniques.

## Sources

**Primary:**
- Wei, J., Bosma, M., Zhao, V.Y., Guu, K., Yu, A.W., Lester, B., Du, N., Dai, A.M., & Le, Q.V. (2021). "Finetuned Language Models Are Zero-Shot Learners." arXiv:2109.01652. https://arxiv.org/abs/2109.01652

**Secondary:**
- Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). "Large Language Models are Zero-Shot Reasoners." NeurIPS 2022. https://arxiv.org/abs/2205.11916
- Brown, T., Mann, B., Ryder, N., et al. (2020). "Language Models are Few-Shot Learners." NeurIPS 2020. https://arxiv.org/abs/2005.14165
- Ouyang, L., Wu, J., Jiang, X., et al. (2022). "Training language models to follow instructions with human feedback." NeurIPS 2022. https://arxiv.org/abs/2203.02155
- Sanh, V., Webson, A., Raffel, C., et al. (2021). "Multitask Prompted Training Enables Zero-Shot Task Generalization." ICLR 2022. https://arxiv.org/abs/2110.08207
