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
