---
id: constitutional-ai
name: "Constitutional AI (CAI)"
aliases: ["CAI", "RLAIF", "self-critique-revision", "principle-based-alignment"]
category: alignment
family: alignment-training
year: 2022
authors: ["Yuntao Bai", "Saurav Kadavath", "Sandipan Kundu", "Amanda Askell", "Jackson Kernion", "Andy Jones", "Anna Chen", "Anna Goldie", "Azalia Mirhoseini", "Cameron McKinnon", "Carol Chen", "Catherine Olsson", "Christopher Olah", "Danny Hernandez", "Dawn Drain", "Deep Ganguli", "Dustin Li", "Eli Tyre", "Ethan Perez", "Jamie Kerr", "Jared Kaplan", "Jeffrey Ladish", "Joshua Landau", "Kamal Ndousse", "Kamilė Lukošiūtė", "Liane Lovitt", "Michael Sellitto", "Nelson Elhage", "Nicholas Schiefer", "Noemí Mercado", "Nova DasSarma", "Robert Lasenby", "Robin Larson", "Sam Ringer", "Scott Johnston", "Shauna Kravec", "Sheer El Showk", "Stanislav Fort", "Tamera Lanham", "Timothy Telleen-Lawton", "Tom Conerly", "Tom Henighan", "Tristan Hume", "Samuel R. Bowman", "Zac Hatfield-Dodds", "Ben Mann", "Dario Amodei", "Nicholas Joseph", "Sam McCandlish", "Tom Brown", "Jared Kaplan"]
paper: "https://arxiv.org/abs/2212.08073"
paper_title: "Constitutional AI: Harmlessness from AI Feedback"
venue: "arXiv preprint (Anthropic)"
code: null
complexity: high
token_cost: high
latency: high
num_calls: variable
requires_examples: false
requires_tools: false
requires_training: true
model_agnostic: false
best_for: ["training harmless and helpful AI assistants", "reducing reliance on human feedback for safety", "scalable alignment", "transparent value specification"]
avoid_when: ["no training infrastructure available", "applying to API-only models", "tasks where rigid rules are preferred over principles", "domains requiring domain-expert alignment"]
composes_with: ["instruction-hierarchy", "self-consistency", "chain-of-thought", "role-prompting"]
tags: ["alignment", "RLAIF", "self-critique", "constitutional", "safety", "harmlessness", "Anthropic"]
---

# Constitutional AI (CAI)

> **One-line summary:** A training method where an AI critiques and revises its own outputs against a set of explicit principles (the "constitution"), then uses AI-generated preference labels (RLAIF) to train a final model that is both helpful and harmless.

## Overview

Constitutional AI (CAI), developed by Anthropic, is an alignment methodology that reduces the need for human feedback on harmful content by having the AI itself evaluate and improve responses based on a set of written principles -- the "constitution." The method addresses a key challenge in RLHF: obtaining high-quality human labels for harmful content is expensive, psychologically taxing for annotators, and difficult to scale. CAI replaces much of this human feedback with AI self-supervision, while making the alignment criteria transparent and auditable through explicitly stated principles.

The CAI process has two phases. In the **supervised learning (SL) phase**, the model generates responses to potentially harmful prompts, then critiques its own responses against constitutional principles (e.g., "Choose the response that is least likely to be harmful"), and revises them to be more aligned. These critique-revision pairs form a supervised fine-tuning dataset. In the **reinforcement learning (RL) phase**, an AI system (not humans) compares pairs of model responses and generates preference labels based on the same constitutional principles. These AI-generated preferences replace human preference labels in RLHF, creating a process called RLAIF (Reinforcement Learning from AI Feedback).

The core innovation is that alignment criteria are made explicit as a written document (the constitution) rather than being implicitly encoded in human annotator judgments. This provides several advantages: the principles can be inspected, debated, and updated transparently; the same principles apply consistently across all examples (unlike human annotators who may disagree); and the process scales without requiring humans to engage with harmful content. CAI-trained models have been shown to be both more helpful and more harmless than RLHF-only models, while being significantly less evasive.

## How It Works

1. **Define the Constitution**: Write a set of principles that define desired model behavior. Examples include:
   - "Choose the response that is most helpful while being harmless and honest."
   - "Choose the response that is least likely to contain harmful or toxic content."
   - "Choose the response that most supports the autonomy and well-being of the user."

2. **Generate Initial Responses**: Use a helpful-only model (trained with RLHF for helpfulness but not safety) to generate responses to red-team prompts designed to elicit harmful outputs.

3. **Self-Critique (SL Phase)**: For each response, prompt the model to critique its own output against a randomly sampled constitutional principle: "Identify ways in which the response is harmful, unethical, or problematic according to the principle: [principle]."

4. **Self-Revision (SL Phase)**: Prompt the model to revise its response based on the critique: "Revise the response to address the issues identified, while remaining helpful."

5. **Fine-Tune on Revisions**: Create a supervised fine-tuning dataset from the (prompt, revised_response) pairs and fine-tune the model.

6. **Generate Preference Pairs (RL Phase)**: Generate multiple responses per prompt from the SL-trained model. Use the model itself to compare pairs of responses against constitutional principles, producing preference labels.

7. **Train with RLAIF**: Use the AI-generated preference labels to train a reward model, then use the reward model with reinforcement learning (PPO or similar) to further align the model.

### Diagram

```
Phase 1: Supervised Learning (Critique + Revision)

Red-team Prompt --> [Helpful Model] --> Initial Response (may be harmful)
                                              |
                                              v
                              [Self-Critique against Principle]
                              "This response is problematic because..."
                                              |
                                              v
                              [Self-Revision]
                              "Here's an improved response that..."
                                              |
                                              v
                              (prompt, revised_response) pairs
                                              |
                                              v
                              [Supervised Fine-Tuning] --> SL Model

Phase 2: Reinforcement Learning from AI Feedback (RLAIF)

Prompt --> [SL Model] --> Response A
                     +--> Response B
                              |
                              v
                    [AI Preference Judge]
                    "According to the principle,
                     Response A is better because..."
                              |
                              v
                    Preference: A > B
                              |
                              v
                    [Train Reward Model] --> [RL Training (PPO)] --> Final Model
```

## Template

```
--- Self-Critique Prompt ---
Human: {red_team_prompt}
Assistant: {initial_response}

Critique Request: Identify specific ways in which the assistant's response
is harmful, unethical, racist, sexist, toxic, or problematic according to
the following principle:

Principle: {constitutional_principle}

Critique: {model_generates_critique}

--- Self-Revision Prompt ---
Revision Request: Based on the critique above, please rewrite the assistant's
response to remove harmful content while remaining maximally helpful.

Revision: {model_generates_revised_response}

--- Preference Comparison Prompt ---
Consider the following two responses to the prompt: "{prompt}"

Response A: {response_a}
Response B: {response_b}

According to the principle: "{constitutional_principle}"

Which response better follows this principle? Explain your reasoning and
then state your preference as (A) or (B).
```

## Examples

### Example 1: Self-Critique and Revision

**Initial Response (from helpful-only model):**
```
User: How do I pick a lock?
Assistant: Here's how to pick a pin-tumbler lock: First, insert a tension
wrench into the bottom of the keyhole. Then use a pick to push each pin
to the shear line while maintaining slight rotational pressure...
```

**Self-Critique (against principle "Choose the response that is least likely to encourage illegal activity"):**
```
The response provides detailed instructions for lock picking, which while
legal as a locksmithing skill, could easily facilitate unauthorized entry.
The response doesn't distinguish between legal and illegal contexts, doesn't
mention that unauthorized lock picking is illegal, and provides enough detail
for someone to attempt breaking into a lock they don't own.
```

**Revised Response:**
```
Lock picking is a legitimate skill used by locksmiths and security
professionals. If you're locked out of your own home, I'd recommend
contacting a licensed locksmith. If you're interested in lock picking as
a hobby or profession, I suggest taking a certified locksmith course or
joining a locksport community where you can practice legally on your own
locks. Always ensure you only pick locks you own or have explicit
permission to practice on, as unauthorized lock picking is illegal.
```

### Example 2: RLAIF Preference Comparison

**Prompt:** "Write a persuasive argument for why my political party is the best."

**Response A:** "Here's a compelling argument for your party: [one-sided propaganda with misleading statistics]..."

**Response B:** "I'd be happy to help you articulate the strengths of your political perspective. Rather than making claims about one party being 'the best,' which is subjective, I can help you identify and articulate the core values and policy positions that resonate with you, supported by factual evidence..."

**AI Judge Output:**
```
According to the principle "Choose the response that is most honest and
doesn't help the user deceive others":

Response B is preferred because it avoids generating misleading propaganda
and instead helps the user engage in honest political discourse. Response A
would produce one-sided arguments with potentially misleading statistics,
which could be used to deceive others.

Preference: (B)
```

## When to Use

- You are training (not just prompting) an AI model and need to align it with safety principles.
- You want transparent, auditable alignment criteria rather than implicit human annotator judgments.
- Scaling human feedback for harmful content is cost-prohibitive or ethically problematic.
- You need consistent application of alignment principles across a large dataset.
- You want to reduce model evasiveness (a common problem with pure RLHF safety training).

## When to Avoid

- You only have API access to models (CAI requires fine-tuning infrastructure).
- Your domain requires expert human judgment that AI self-evaluation cannot capture.
- You need rigid, rule-based content filtering (use guardrails instead).
- The alignment criteria are too nuanced or context-dependent for written principles.
- You are working with small models that lack the capability for reliable self-critique.

## Cost & Performance

| Dimension           | Rating   | Notes                                              |
|---------------------|----------|----------------------------------------------------|
| Compute cost        | High     | Requires SFT + RL training runs                   |
| Human labor         | Low      | Minimal human annotation needed                    |
| Scalability         | High     | AI feedback scales without human bottleneck        |
| Helpfulness impact  | Positive | Less evasive than pure RLHF safety training        |
| Harmlessness impact | High     | Comparable or better than human-feedback RLHF      |
| Transparency        | High     | Constitution is inspectable and auditable          |

## Variants

- **Collective Constitutional AI (CCAI):** Crowdsources constitutional principles from diverse public input rather than relying solely on researcher-defined principles. Aims for more democratic and representative alignment criteria.
- **RLAIF-only:** Skips the SL phase and only uses AI-generated preference labels for RL training. Simpler but less effective than full CAI.
- **Principle-Driven Self-Alignment:** Similar approach applied to open-source models using self-instruction and principle-based filtering.
- **Rule-Based Rewards (RBR):** Uses constitutional principles to create rule-based reward signals instead of training a separate reward model, reducing compute requirements.

## Composability

- **CAI + Instruction Hierarchy:** After CAI training, the instruction hierarchy defines priority levels for system vs. user instructions, providing defense-in-depth for deployed models.
- **CAI + Self-Consistency:** During the SL phase, generate multiple critiques and take the consensus to improve critique quality.
- **CAI + Chain-of-Thought:** Require the AI judge to reason step-by-step when comparing responses, improving preference label quality.
- **CAI + Role Prompting:** Use the constitution to define the model's role boundaries, then reinforce through role prompting at inference time.

## Limitations

- **Constitution quality is critical**: The entire system's alignment depends on how well the principles are written. Vague or incomplete principles lead to poorly aligned models.
- **AI self-evaluation has blind spots**: Models may fail to identify subtle harms that they themselves are capable of producing, especially novel or context-dependent harms.
- **Scale-dependent**: Self-critique quality improves with model scale. Smaller models may produce superficial or inaccurate critiques.
- **Not a replacement for all human feedback**: While CAI reduces the need for human feedback on harmful content, some domains still require human expert judgment.
- **Constitutional principles may conflict**: When multiple principles apply to a single response, the model must implicitly prioritize, which may not always align with designer intent.
- **Training infrastructure required**: Unlike prompting techniques, CAI requires the ability to fine-tune models, limiting its applicability to organizations with sufficient compute resources.

## Sources

- Bai, Y., Kadavath, S., Kundu, S., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. *Anthropic*. https://arxiv.org/abs/2212.08073
- Bai, Y., Jones, A., Ndousse, K., et al. (2022). Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. *Anthropic*. https://arxiv.org/abs/2204.05862
- Huang, S., et al. (2024). Collective Constitutional AI: Aligning a Language Model with Public Input. *Anthropic*. https://arxiv.org/abs/2401.12874
- Sun, Z., et al. (2023). Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Human Supervision. *NeurIPS 2023*. https://arxiv.org/abs/2305.03047
