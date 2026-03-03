---
id: step-back-prompting
name: "Step-Back Prompting"
aliases: ["Step Back", "Abstraction-First Prompting"]
category: advanced-reasoning
family: decomposition
year: 2023
authors: ["Huaixiu Steven Zheng", "Swaroop Mishra", "Xinyun Chen", "Heng-Tze Cheng", "Ed H. Chi", "Quoc V. Le", "Denny Zhou"]
paper: "https://arxiv.org/abs/2310.06117"
paper_title: "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models"
venue: "ICLR 2024"
code: null

complexity: low
token_cost: medium
latency: medium
num_calls: 2

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["knowledge-intensive questions", "scientific reasoning", "multi-step reasoning with domain knowledge", "questions requiring first-principles thinking", "STEM problem solving"]
avoid_when: ["simple factual lookups", "creative writing", "tasks with no underlying principles", "extremely time-sensitive queries"]
composes_with: ["chain-of-thought", "retrieval-augmented-generation", "few-shot-prompting", "self-consistency"]

tags: ["abstraction", "decomposition", "first-principles", "two-step", "reasoning"]
---

# Step-Back Prompting

> **One-line summary:** Step-Back Prompting first asks the LLM a higher-level abstraction question to retrieve relevant principles or concepts, then uses that context to answer the original specific question.

## Overview

Step-Back Prompting is based on the observation that LLMs often fail on specific, detailed questions not because they lack the relevant knowledge, but because they struggle to connect the specific question to the broader principles needed to answer it. By explicitly prompting the model to "step back" and consider the general principle or concept before tackling the specific question, accuracy improves significantly.

The technique was developed by researchers at Google DeepMind who observed that humans naturally employ abstraction when solving difficult problems: a physics student facing a complex kinematics problem first recalls the relevant equations of motion, then applies them. Step-Back Prompting replicates this cognitive strategy in LLMs by introducing a two-step process where the first step deliberately elevates the reasoning to a more abstract level.

The approach is remarkably simple yet effective. It requires only two LLM calls: one to generate the step-back question and its answer (the abstract principle), and one to answer the original question using that principle as context. This simplicity makes it easy to implement and compose with other techniques while delivering substantial accuracy improvements, particularly on STEM and knowledge-intensive benchmarks.

## How It Works

1. **Step-Back Question Generation:** Given the original question, the LLM generates a more abstract, higher-level question. For example, if asked about a specific chemical reaction's properties, the step-back question might ask about the general class of reactions and their properties.

2. **Abstract Principle Retrieval:** The LLM answers the step-back question, producing a summary of the relevant principles, concepts, or background knowledge. This creates a rich context of foundational information.

3. **Grounded Answer Generation:** The original question is presented again, this time alongside the abstract principles retrieved in step 2. The LLM uses this combined context to produce a well-grounded, specific answer.

### Diagram

```
┌─────────────────────────────────────────────────┐
│            Step-Back Prompting Flow              │
│                                                 │
│  ┌──────────────────┐                           │
│  │ Original Question │                           │
│  │ (specific)        │──────────┐                │
│  └────────┬─────────┘          │                │
│           │                    │                │
│           v                    │                │
│  ┌──────────────────┐          │                │
│  │ Generate Step-Back│          │                │
│  │ Question          │          │                │
│  │ (abstraction)     │          │                │
│  └────────┬─────────┘          │                │
│           │                    │                │
│           v                    │                │
│  ┌──────────────────┐          │                │
│  │ Answer Step-Back  │          │                │
│  │ Question          │  Call 1  │                │
│  │ (principles)      │          │                │
│  └────────┬─────────┘          │                │
│           │                    │                │
│           v                    v                │
│  ┌──────────────────────────────────────────┐   │
│  │ Answer Original Question Using           │   │
│  │ Abstract Principles as Context   Call 2  │   │
│  └────────────────────┬─────────────────────┘   │
│                       v                         │
│              ┌─────────────────┐                │
│              │  Final Answer   │                │
│              └─────────────────┘                │
└─────────────────────────────────────────────────┘
```

## Template

```
STEP 1 — Step-Back Question:
Given the following question, first generate a more abstract, higher-level
question that captures the underlying principle or concept needed to answer it.

Original question: {original_question}

Step-back question: What is the general principle/concept behind
{abstracted_topic}?

Answer the step-back question with relevant principles and background
knowledge.

---

STEP 2 — Answer with Context:
Using the principles and context below, answer the original question.

Principles and background:
{step_back_answer}

Original question: {original_question}

Provide a detailed, accurate answer grounded in the principles above.
```

## Examples

### Example 1: Physics (STEM Reasoning)

**Input (Step 1):**
```
Given the following question, first generate a more abstract step-back
question, then answer it.

Original question: "If the temperature of an ideal gas is doubled while
the volume is halved, what happens to the pressure?"

Step-back question:
```

**Output (Step 1):**
```
Step-back question: "What is the ideal gas law and how do its variables
relate to each other?"

Answer: The ideal gas law is PV = nRT, where P is pressure, V is volume,
n is the number of moles, R is the gas constant, and T is absolute
temperature. For a fixed amount of gas (constant n), pressure is directly
proportional to temperature and inversely proportional to volume. This
can be expressed as P = nRT/V, meaning any change in T or V will affect P
proportionally.
```

**Input (Step 2):**
```
Using these principles, answer the original question.

Principles: The ideal gas law is PV = nRT. For fixed n, P = nRT/V.
Pressure is directly proportional to T and inversely proportional to V.

Original question: "If the temperature of an ideal gas is doubled while
the volume is halved, what happens to the pressure?"
```

**Output (Step 2):**
```
Using P = nRT/V:
- Temperature doubled: T → 2T → pressure doubles
- Volume halved: V → V/2 → pressure doubles

Combined effect: P_new = nR(2T)/(V/2) = 4nRT/V = 4P

The pressure increases by a factor of 4 (quadruples).
```

### Example 2: History (Knowledge-Intensive)

**Input (Step 1):**
```
Original question: "Why did the Weimar Republic experience hyperinflation
in 1923?"

Generate a step-back question and answer it.
```

**Output (Step 1):**
```
Step-back question: "What are the general economic causes and mechanisms
of hyperinflation?"

Answer: Hyperinflation occurs when a government dramatically increases
the money supply, typically to finance debts or deficits, faster than the
economy can grow. Key mechanisms include: (1) excessive money printing to
cover government spending, (2) loss of confidence in the currency causing
velocity of money to increase, (3) wage-price spirals as workers demand
higher wages, (4) external factors like trade imbalances or foreign debt
denominated in other currencies that create pressure to print more
domestic currency. A triggering event often combines with structural
fiscal weakness.
```

**Input (Step 2):**
```
Principles: Hyperinflation is caused by excessive money supply growth
relative to economic output, driven by government deficit financing, loss
of confidence, wage-price spirals, and external debt pressures.

Original question: "Why did the Weimar Republic experience hyperinflation
in 1923?"
```

**Output (Step 2):**
```
Applying these principles to the Weimar Republic:

1. **Excessive money printing:** Germany printed massive amounts of marks
   to pay war reparations imposed by the Treaty of Versailles and to fund
   the passive resistance in the Ruhr when France occupied it in Jan 1923.

2. **Foreign debt pressure:** Reparations were denominated in gold marks
   and foreign currencies, forcing Germany to buy foreign currency with
   newly printed marks, devaluing the mark on international exchanges.

3. **Loss of confidence:** As the mark depreciated, Germans rushed to
   spend money before it lost value, dramatically increasing the velocity
   of money and accelerating inflation.

4. **Wage-price spiral:** Workers demanded daily or even hourly pay
   adjustments, and prices were updated multiple times per day.

5. **Structural weakness:** The government had been running deficits since
   WWI and had already inflated the currency moderately from 1919-1922.

The hyperinflation peaked in November 1923, when the exchange rate
reached 4.2 trillion marks to 1 US dollar, before stabilization via the
introduction of the Rentenmark.
```

## When to Use

- Knowledge-intensive questions where the LLM needs to recall and apply domain principles
- STEM problems (physics, chemistry, biology) where first-principles reasoning improves accuracy
- Multi-step reasoning tasks where grounding in abstract concepts prevents errors
- Questions that are specific instances of general patterns or laws
- When the model is getting details wrong on domain-specific questions despite having relevant knowledge

## When to Avoid

- Simple factual questions that do not require principled reasoning (e.g., "What is the capital of France?")
- Creative or subjective tasks where abstraction adds no value
- When latency is critical and the two-call overhead is unacceptable
- Tasks where no meaningful abstraction exists (e.g., "Summarize this text")
- Highly novel problems where no general principle applies

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | ~1.5-2x | One additional call for the step-back question |
| Latency | ~2x baseline | Two sequential LLM calls |
| Quality gain | +7-11% | On MMLU physics, chemistry; +15%+ on TimeQA |
| Num calls | 2 | Fixed: step-back + final answer |
| Implementation | Very easy | No special tooling required |

## Variants

- **Multi-Step-Back:** Chain multiple levels of abstraction (specific → intermediate → general) for particularly complex questions.
- **Few-Shot Step-Back:** Provide examples of good step-back questions to improve the quality of the generated abstractions.
- **RAG + Step-Back:** Use the step-back question to query a retrieval system, then use retrieved documents alongside the original question for the final answer.

## Composability

- **Step-Back + RAG:** The step-back question makes an excellent retrieval query, often retrieving more relevant documents than the original specific question.
- **Step-Back + Chain-of-Thought:** After retrieving principles via step-back, use CoT for the detailed reasoning in the final answer step.
- **Step-Back + Self-Consistency:** Generate multiple step-back questions and final answers, then use majority voting for robustness.
- **Step-Back + Few-Shot:** Provide examples of step-back questions to guide the model toward better abstractions.

## Limitations

- The quality of the step-back question is crucial; poor abstractions can mislead the final answer
- Adds latency from the two-step process, which may not be acceptable in all applications
- Not all questions benefit from abstraction; some are inherently specific
- The model may generate step-back questions that are too broad or too narrow
- On some benchmarks, the improvement over well-crafted CoT prompts is modest
- Requires the model to have the abstract knowledge in its parameters; cannot create knowledge that is not there

## Sources

- **Primary:** [Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models](https://arxiv.org/abs/2310.06117) — Zheng et al., ICLR 2024
- **Related:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) — Wei et al., 2022
- **Related:** [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) — Zhou et al., 2022
