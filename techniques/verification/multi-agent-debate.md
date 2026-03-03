---
id: multi-agent-debate
name: "Multi-Agent Debate"
aliases: ["MAD", "LLM Debate", "Society of LLMs"]
category: verification
family: verification
year: 2023
authors: ["Yilun Du", "Shuang Li", "Antonio Torralba", "Joshua B. Tenenbaum", "Igor Mordatch"]
paper: "https://arxiv.org/abs/2305.14325"
paper_title: "Improving Factuality and Reasoning in Language Models through Multiagent Debate"
venue: "arXiv 2023"
code: null

complexity: high
token_cost: very_high
latency: very_high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["factual accuracy improvement", "mathematical reasoning", "questions with objectively verifiable answers", "tasks benefiting from adversarial scrutiny", "reducing hallucination through cross-verification"]
avoid_when: ["simple questions with obvious answers", "creative or subjective tasks", "extreme token budget constraints", "low-latency requirements", "when models are likely to converge on the same wrong answer"]
composes_with: ["chain-of-thought", "few-shot-prompting", "self-consistency", "retrieval-augmented-generation"]

tags: ["multi-agent", "debate", "consensus", "factuality", "adversarial", "ensemble"]
---

# Multi-Agent Debate

> **One-line summary:** Multi-Agent Debate improves LLM factuality and reasoning by having multiple LLM instances independently answer a question, then engage in multiple rounds of debate where they critique each other's answers, converging toward a more accurate consensus.

## Overview

Multi-Agent Debate (MAD) leverages the principle that diverse perspectives and adversarial scrutiny lead to more accurate conclusions. Instead of relying on a single model's output, MAD instantiates multiple LLM agents (which can be the same model or different models) that each independently generate an initial response. These agents then engage in structured rounds of debate, where each agent sees the others' responses and must either defend its position with additional reasoning or update its answer based on compelling arguments from the other agents.

The key insight from Du et al. is that individual LLM instances, even when using the same underlying model, can arrive at different answers due to sampling variability, and the debate process acts as a natural error-correction mechanism. When one agent makes an error, other agents are likely to catch it and present counter-arguments. Conversely, correct answers tend to be reinforced across rounds as agents converge. This dynamic is particularly effective for mathematical reasoning and factual questions where there is an objectively correct answer that can be identified through logical argument.

The approach differs from Self-Consistency (which merely votes across independent samples) in that agents actively engage with each other's reasoning. The debate structure forces models to articulate why specific answers are correct and identify flaws in alternatives, leading to deeper reasoning than independent parallel sampling. However, this comes at significant token cost, as each debate round multiplies the number of LLM calls.

## How It Works

1. **Independent Generation:** Each of N agents (typically 3-5) independently generates an initial answer to the question. These agents may be the same model with different sampling seeds or different models entirely.

2. **Debate Round:** Each agent receives the other agents' responses and is prompted to evaluate them. The agent must either defend its own answer with additional evidence/reasoning or concede and update its answer if another agent's argument is more compelling.

3. **Iteration:** The debate continues for multiple rounds (typically 2-4) until agents converge on a single answer or a maximum number of rounds is reached.

4. **Consensus Extraction:** After the final round, the majority answer is selected as the final output. In most cases, agents converge to the same answer through the debate process.

### Diagram

```
┌────────────────────────────────────────────────────────────┐
│                   Multi-Agent Debate                       │
│                                                            │
│  Round 0 (Independent):                                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ Agent A  │  │ Agent B  │  │ Agent C  │                    │
│  │ Answer:X │  │ Answer:Y │  │ Answer:X │                    │
│  └────┬────┘  └────┬────┘  └────┬────┘                    │
│       │            │            │                          │
│       └────────────┼────────────┘                          │
│                    v                                       │
│  Round 1 (Debate):                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Each agent sees all other answers and responds:     │   │
│  │ Agent A: "I maintain X because..."                  │   │
│  │ Agent B: "Upon reviewing, I agree X is correct..."  │   │
│  │ Agent C: "X is confirmed by reasoning..."           │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       v                                    │
│  Round 2 (if needed):                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Agents converge or continue debating...             │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       v                                    │
│              ┌─────────────────┐                           │
│              │ Majority Vote / │                           │
│              │ Consensus: X    │                           │
│              └─────────────────┘                           │
└────────────────────────────────────────────────────────────┘
```

## Template

```
--- ROUND 0: Independent Generation ---

[Agent {agent_id}]
Question: {question}

Provide your answer with detailed reasoning. Think step by step.

Answer:

--- ROUND N: Debate ---

[Agent {agent_id}]
Question: {question}

Your previous answer: {own_previous_answer}

Other agents' responses:
{other_agents_responses}

Review the other agents' answers and reasoning carefully.
If you find flaws in their reasoning, explain them.
If their arguments are more compelling than yours, update your answer.
Provide your revised (or maintained) answer with reasoning.

Updated answer:
```

## Examples

### Example 1: Mathematical Reasoning

**Round 0:**
```
Question: A train leaves Station A at 60 mph. Another train leaves
Station B (300 miles away) at 40 mph heading toward Station A.
When do they meet?

Agent A: Distance = 300 miles. Combined speed = 60 + 40 = 100 mph.
Time = 300/100 = 3 hours. They meet 3 hours after departure.

Agent B: Train 1 covers 60t miles. Train 2 covers 40t miles.
60t + 40t = 300. 100t = 300. t = 3 hours. 180 miles from A.

Agent C: 300 / 60 = 5 hours. They meet after 5 hours.
```

**Round 1:**
```
Agent A: I maintain 3 hours. Agent B confirms with algebra. Agent C
incorrectly divided by only one train's speed — both trains are moving
toward each other, so speeds must be combined.

Agent B: Agent A and I agree on 3 hours. Agent C's error is ignoring
the second train's contribution. Total closure rate is 100 mph, not
60 mph.

Agent C: Reviewing Agents A and B, I see my error. I only considered
one train's speed. The trains approach each other at a combined
100 mph, giving 300/100 = 3 hours. I update my answer to 3 hours.
```

**Consensus:** 3 hours (all agents agree after Round 1).

### Example 2: Factual Question

**Round 0:**
```
Question: Which planet in our solar system has the most moons?

Agent A: Jupiter has the most moons with approximately 95 known moons
as of 2023.

Agent B: Saturn has the most moons with 146 confirmed moons as of
2023, surpassing Jupiter.

Agent C: Jupiter has the most moons, around 79 known moons.
```

**Round 1:**
```
Agent A: Agent B raises a good point. In 2023, new Saturn moons were
indeed discovered. Let me reconsider. As of early 2023, Saturn was
confirmed to have 146 moons, surpassing Jupiter's count. I update
my answer to Saturn.

Agent B: I maintain Saturn. Agent C's count of 79 for Jupiter is
outdated (that was circa 2018). Even Jupiter's updated count (~95)
is less than Saturn's 146. The discoveries by Sheppard et al. gave
Saturn the lead.

Agent C: Agents A and B present more recent data. I was using an
outdated count. Saturn now holds the record with 146 known moons.
I update my answer to Saturn.
```

**Consensus:** Saturn (all agents converge after Round 1).

## When to Use

- Factual questions where different agents might catch each other's hallucinations
- Mathematical reasoning where computational errors can be identified through cross-checking
- Tasks with objectively correct answers that can be verified through argument
- High-stakes outputs where the cost of multiple LLM calls is justified by the accuracy improvement
- When you have access to multiple models and want to leverage their diverse strengths

## When to Avoid

- Simple questions where multiple agents will trivially agree from the start
- Creative or subjective tasks where "debate" is not meaningful (there is no correct answer)
- Extremely token-constrained settings (each debate round multiplies cost by the number of agents)
- Low-latency applications where multiple sequential rounds are unacceptable
- When all agents are likely to make the same error (e.g., shared training data bias)
- Tasks where the models lack sufficient knowledge to meaningfully evaluate each other

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | N * R * base | N agents, R rounds; typically 6-15x base |
| Latency | Very high | Multiple sequential debate rounds |
| Quality gain | +10-20% | On factual QA and math reasoning |
| Typical setup | 3 agents, 2-3 rounds | Good balance of cost vs. improvement |
| Best improvement | Factual QA | Where hallucinations are caught by other agents |

## Variants

- **Homogeneous Debate:** All agents are the same model with different random seeds. Simpler to implement but less diverse.
- **Heterogeneous Debate:** Agents are different models (e.g., GPT-4, Claude, Gemini). More diverse perspectives but harder to coordinate.
- **Judge-Based Debate:** A separate "judge" model evaluates the debate and selects the winning argument instead of relying on majority vote.
- **Timed Debate:** Each round has a token limit, forcing agents to prioritize their strongest arguments.
- **Adversarial Debate:** One agent is explicitly prompted to take a contrarian position, even if it initially agrees.

## Composability

- **MAD + Chain-of-Thought:** Each agent uses CoT reasoning, making the debate more substantive and arguments easier to evaluate.
- **MAD + RAG:** Agents can retrieve external evidence to support their arguments, grounding the debate in facts.
- **MAD + Self-Consistency:** Within each agent, use self-consistency before entering the debate to give each agent a stronger starting position.
- **MAD + Chain-of-Verification:** After debate consensus, verify the agreed-upon answer using CoVe for additional reliability.

## Limitations

- Very high token cost: N agents * R rounds makes this one of the most expensive techniques
- Agents with the same training data may share the same blind spots, reducing debate effectiveness
- "Confident but wrong" agents may persuade correct agents to switch to incorrect answers
- The debate can devolve into agents simply restating positions without substantive argumentation
- Diminishing returns after 2-3 rounds; extended debate rarely improves beyond this
- For subjective tasks, debate may produce artificial consensus rather than genuinely better answers
- Orchestrating multiple model calls adds significant engineering complexity

## Sources

- **Primary:** [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) — Du et al., 2023
- **Related:** [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) — Liang et al., 2023
- **Related:** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) — Wang et al., 2022
