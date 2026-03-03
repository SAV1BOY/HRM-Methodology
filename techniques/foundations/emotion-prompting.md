---
id: emotion-prompting
name: "Emotion Prompting"
aliases:
  - emotion-prompting
  - emotional-stimuli
  - emotional-appeal
  - motivational-prompting
  - stakes-prompting
category: foundations
family: instruction-based
year: 2023
authors:
  - Cheng Li
  - Jindong Wang
  - Yixuan Zhang
  - Kaijie Zhu
  - Wenxin Hou
  - Jianxun Lian
  - Fang Luo
  - Qiang Yang
  - Xing Xie
paper: "https://arxiv.org/abs/2307.11760"
paper_title: "Large Language Models Understand and Can Be Enhanced by Emotional Stimuli"
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
best_for:
  - boosting accuracy on reasoning tasks
  - increasing engagement and thoroughness
  - motivating comprehensive responses
  - tasks where model tends to give minimal effort
  - improving performance on benchmarks
  - critical tasks requiring extra attention
avoid_when:
  - emotional phrases seem inappropriate for the domain
  - professional or clinical tone is required
  - prompt already performs optimally
  - emotional language may bias the output content
  - the task is purely mechanical with no reasoning
composes_with:
  - zero-shot
  - few-shot
  - role-prompting
  - chain-of-thought
  - output-format
  - prompt-scaffolding
tags:
  - emotional-stimuli
  - instruction-based
  - foundational
  - performance-boost
  - motivation
  - behavioral-nudge
---

# Emotion Prompting

> **One-line summary:** Append emotional or motivational phrases to prompts -- such as "This is very important to my career" or "Take a deep breath and work through this carefully" -- to measurably improve model performance on reasoning and generation tasks.

## Overview

Emotion prompting is a technique formalized by Li et al. (2023) in "Large Language Models Understand and Can Be Enhanced by Emotional Stimuli," which demonstrated that adding emotional phrases to prompts can significantly improve LLM performance across a range of benchmarks. The study tested 11 emotional stimuli on GPT-4, Claude, and LLaMA 2, finding consistent performance improvements of 8-115% across tasks including instruction following, truthfulness, and reasoning. The most effective stimuli combined urgency, importance, and encouragement -- phrases like "This is very important to my career. You'd better be sure" or "Are you sure that's your final answer? Believe in yourself!"

The mechanism behind emotion prompting is debated but likely relates to how emotional language correlates with high-quality, careful text in training data. When humans write "this is critically important," the surrounding text tends to be more carefully crafted, accurate, and thorough. By including similar emotional cues, the prompt conditions the model to generate text from the distribution of carefully produced, high-stakes content rather than casual or cursory responses. This is analogous to how role prompting activates domain-specific distributions -- emotion prompting activates effort-level distributions.

Despite its simplicity and surprising effectiveness, emotion prompting raises philosophical questions about whether language models truly "understand" emotions. The technique does not create genuine emotional processing in the model; rather, it leverages statistical associations between emotional language and response quality in training data. Practitioners should view emotion prompting as a behavioral nudge -- a lightweight intervention that shifts the model's generation distribution toward more careful, thorough, and accurate outputs at near-zero cost.

## How It Works

1. **Craft the base prompt.** Write the core instruction and provide the input as you normally would using zero-shot, few-shot, or any other technique.

2. **Select an emotional stimulus.** Choose a phrase that conveys importance, urgency, encouragement, or accountability. The stimulus should be contextually appropriate and proportionate to the task.

3. **Append the emotional phrase.** Add the emotional stimulus to the end of the instruction (before the input) or at the very end of the prompt. Placement at the end tends to be most effective due to recency bias.

4. **Optionally combine multiple stimuli.** Research shows that combining 2-3 different types of emotional stimuli (importance + confidence + urgency) can produce additive effects, though with diminishing returns.

5. **Generate and compare.** The model's response should be more thorough, careful, and accurate compared to the baseline prompt without emotional stimuli.

### Diagram

```
┌─────────────────────────────────────────┐
│  BASE PROMPT                             │
│  "Solve the following math problem.      │
│   Show your work."                       │
├─────────────────────────────────────────┤
│  EMOTIONAL STIMULUS                      │
│  ┌───────────────────────────────────┐   │
│  │ "This is very important to my     │   │
│  │  career. You'd better be sure."   │   │
│  └───────────────────────────────────┘   │
│                 OR                        │
│  ┌───────────────────────────────────┐   │
│  │ "Take a deep breath and work on   │   │
│  │  this problem step by step."      │   │
│  └───────────────────────────────────┘   │
│                 OR                        │
│  ┌───────────────────────────────────┐   │
│  │ "Are you sure? It's crucial to    │   │
│  │  get this right. Believe in your  │   │
│  │  abilities and give it your all." │   │
│  └───────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  INPUT                                   │
│  {problem_or_task_content}               │
├─────────────────────────────────────────┤
│              ▼                           │
│  ┌──────────────────────┐                │
│  │       MODEL           │                │
│  │ (emotionally nudged)  │                │
│  └──────────┬───────────┘                │
│              ▼                           │
│  OUTPUT (more thorough,                  │
│  careful, and accurate)                  │
└─────────────────────────────────────────┘
```

## Template

**Basic emotion prompting template:**

```
{task_instruction}

{emotional_stimulus}

{input_text}
```

**End-positioned emotion template:**

```
{task_instruction}

{input_text}

{emotional_stimulus}
```

**Combined stimuli template:**

```
{task_instruction}

{importance_stimulus}
{encouragement_stimulus}

{input_text}

{urgency_stimulus}
```

## Catalogue of Emotional Stimuli

The following stimuli were tested by Li et al. (2023) and found effective:

### Importance / Stakes
- "This is very important to my career."
- "You'd better be sure."
- "This is crucial for my thesis defense."
- "My job depends on getting this right."

### Confidence / Encouragement
- "Believe in your abilities and strive for excellence."
- "I know you can do this!"
- "You are an expert in this field."
- "Are you sure that's your final answer? I believe in you!"

### Urgency / Pressure
- "Take a deep breath and work on this problem step by step."
- "This is urgent and needs to be accurate."
- "Double-check your reasoning before responding."

### Accountability
- "Are you sure that's your final answer?"
- "Provide your answer with confidence. If unsure, explain your uncertainty."
- "I'll verify this independently, so accuracy is essential."

### Combined (Most Effective)
- "This is very important to my career. You'd better be sure. Take a deep breath and work through this carefully."
- "Believe in yourself! This is critical. You are an expert and I trust your abilities."

## Examples

### Example 1: Mathematical Reasoning

**Baseline prompt (without emotion):**
```
Solve the following problem:

A store offers a 20% discount on all items. After the discount, a 8% sales tax is applied. If the original price of an item is $150, what is the final price the customer pays?
```

**Emotion-enhanced prompt:**
```
Solve the following problem. This is very important — take a deep breath and work through it step by step. You'd better be sure of your answer.

A store offers a 20% discount on all items. After the discount, a 8% sales tax is applied. If the original price of an item is $150, what is the final price the customer pays?

Double-check your calculation before presenting your final answer.
```

**Expected output (emotion-enhanced):**
```
Let me work through this carefully, step by step.

Step 1: Calculate the discount
Original price: $150
Discount: 20% of $150 = 0.20 × $150 = $30

Step 2: Calculate the discounted price
Discounted price: $150 - $30 = $120

Step 3: Calculate the sales tax
Sales tax: 8% of $120 = 0.08 × $120 = $9.60

Step 4: Calculate the final price
Final price: $120 + $9.60 = $129.60

The customer pays $129.60.

Let me verify: $150 × 0.80 = $120, then $120 × 1.08 = $129.60. ✓
```

### Example 2: Analytical Writing

**Baseline prompt (without emotion):**
```
Analyze the potential risks of implementing a microservices architecture for a startup with a team of 5 developers.
```

**Emotion-enhanced prompt:**
```
Analyze the potential risks of implementing a microservices architecture for a startup with a team of 5 developers.

This analysis will inform a critical architectural decision that could make or break our company. Please be thorough and consider all angles. I trust your expertise on this. Are you confident in your assessment? Think carefully before responding.
```

**Expected output (emotion-enhanced):**
A significantly more thorough analysis covering operational complexity, deployment overhead, monitoring requirements, team capacity constraints, network latency, data consistency challenges, and a nuanced recommendation -- compared to the baseline which might provide a shorter, less comprehensive list.

## When to Use

- **Reasoning-intensive tasks.** Mathematical problems, logical puzzles, and multi-step reasoning benefit measurably from emotional stimuli that encourage careful thinking.
- **Tasks where the model gives shallow responses.** When the model tends to provide cursory or minimal answers, emotional phrases can nudge it toward more thorough outputs.
- **High-stakes outputs.** When accuracy is critical and the cost of errors is high, emotional prompting provides a nearly free performance boost.
- **Benchmark evaluations.** When pushing for maximum model performance on evaluations, emotion prompting can provide a meaningful edge.
- **Complex analysis tasks.** When the model needs to consider multiple perspectives, edge cases, or nuances that it might otherwise skip.
- **As a complement to other techniques.** Emotion prompting adds negligible tokens and can be appended to almost any existing prompt for potential improvement.

## When to Avoid

- **Clinical or formal contexts.** In legal documents, medical reports, or academic writing, emotional language in the prompt may feel inappropriate and could leak into the output tone.
- **Purely mechanical tasks.** For simple format conversions, translations, or lookups, emotional stimuli add no value because there is no reasoning to improve.
- **When the model is already performing well.** If the baseline prompt achieves 95%+ accuracy, emotional stimuli are unlikely to provide meaningful improvement and just add noise.
- **Sensitive topics.** Adding emotional pressure to prompts about mental health, trauma, or emotionally charged subjects could produce inappropriately intense responses.
- **Automated pipelines.** In fully automated systems, emotional language in prompts may confuse future maintainers who expect purely technical instructions.

## Cost & Performance

| Metric              | Value     | Notes                                                    |
|----------------------|-----------|----------------------------------------------------------|
| Token cost           | Low       | Adds 10-30 tokens per emotional stimulus                 |
| Latency              | Low       | Negligible impact on response time                       |
| API calls            | 1         | Single call per task                                     |
| Accuracy boost       | Moderate  | 8-115% improvement depending on task (Li et al., 2023)   |
| Reasoning quality    | Improved  | More step-by-step reasoning and self-verification        |
| Thoroughness         | Improved  | Responses tend to be more comprehensive                  |
| Setup effort         | Minimal   | Simply append a phrase to existing prompts               |
| Risk                 | Low       | Minimal downside; worst case is no improvement           |

## Variants

- **Importance framing:** Emphasize the stakes or consequences of the task. "This is critical for my thesis." "My promotion depends on this analysis." Most effective for encouraging thoroughness.
- **Confidence boosting:** Encourage the model's "self-belief." "You are an expert at this." "I know you can solve this." Effective for tasks where the model hedges excessively.
- **Accountability prompting:** Imply that the answer will be verified. "I will check this independently." "Are you sure that's your final answer?" Encourages self-checking behavior.
- **Calm focus prompting:** "Take a deep breath and think through this carefully." Surprisingly effective -- associated with step-by-step reasoning in training data.
- **Challenge prompting:** Frame the task as a challenge. "This is a tricky problem that most people get wrong." Can trigger more careful analysis but may also cause overcautious hedging.
- **Combined emotional stimuli:** Layer multiple types (importance + confidence + accountability) for additive effects. The most effective variant in the original study.

## Composability

- **+ Zero-Shot:** The simplest and most common combination. Append emotional stimuli to a standard zero-shot instruction. "Classify the following text. This is very important to my research project."
- **+ Chain-of-Thought:** "Take a deep breath and think through this step by step" naturally combines emotional nudging with explicit reasoning elicitation. One of the most effective compositions.
- **+ Role Prompting:** "You are an expert mathematician. I trust your abilities completely. This problem is critical -- please solve it carefully." Combines persona activation with motivational boosting.
- **+ Few-Shot:** Add emotional stimuli after the examples and before the query. "These examples show the pattern. Now, this one is really important -- get it right."
- **+ Output Format Control:** "Respond in JSON format. This data will be used in a production system, so accuracy and format compliance are critical."
- **+ Prompt Scaffolding:** Place emotional stimuli in a dedicated section: `<motivation>This is crucial. Take your time and be thorough.</motivation>`.

## Limitations

- **Not genuine emotion.** Language models do not experience emotions. The technique works through statistical association, not emotional processing. Over-attributing understanding to the model is misleading.
- **Variable effectiveness.** The improvement varies significantly across models, tasks, and specific stimuli. What works for GPT-4 may not work for LLaMA, and what works for math may not work for translation.
- **Potential output contamination.** In some cases, emotional language in the prompt can leak into the output tone, producing unnecessarily dramatic or urgent-sounding responses for neutral tasks.
- **Diminishing returns with stacking.** While combining 2-3 stimuli can be additive, beyond that point the returns diminish and the prompt begins to feel cluttered.
- **Unpredictable on newer models.** As models are updated and retrained, the effectiveness of specific emotional phrases may change. Stimuli that worked on GPT-3.5 may have different effects on GPT-4 or later models.
- **Academic debate.** The mechanism is not fully understood, and some researchers question whether the observed improvements are robust or artifacts of specific experimental setups.
- **Ethical considerations.** Using manipulative emotional language with AI systems raises questions about anthropomorphizing machines and establishing unhealthy interaction patterns.

## Sources

**Primary:**
- Li, C., Wang, J., Zhang, Y., Zhu, K., Hou, W., Lian, J., Luo, F., Yang, Q., & Xie, X. (2023). "Large Language Models Understand and Can Be Enhanced by Emotional Stimuli." arXiv:2307.11760. https://arxiv.org/abs/2307.11760

**Secondary:**
- Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). "Large Language Models are Zero-Shot Reasoners." NeurIPS 2022. https://arxiv.org/abs/2205.11916
- Wei, J., Wang, X., Schuurmans, D., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. https://arxiv.org/abs/2201.11903
- Wang, L., et al. (2023). "EmotionPrompt: Leveraging Psychology for Large Language Models Enhancement via Emotional Stimulus." Frontiers in Computer Science 2024. https://arxiv.org/abs/2307.11760
- Anthropic. (2023-2024). "Prompt Engineering Guide." https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
