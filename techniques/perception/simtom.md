---
id: simtom
name: "SimToM (Simulated Theory of Mind)"
aliases: ["SimToM", "Simulated Theory of Mind", "Perspective-Taking Prompting"]
category: perception
family: perspective-filtering
year: 2023
authors: ["Wilka Carvalho Wilf", "Tobias Gerstenberg", "Hyowon Gweon", "Simon DeDeo"]
paper: "https://arxiv.org/abs/2311.10227"
paper_title: "Think Twice: Perspective-Taking Improves Large Language Models' Theory-of-Mind Capabilities"
venue: "arXiv 2023"
code: null

complexity: medium
token_cost: medium
latency: medium
num_calls: 2

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["theory of mind tasks", "perspective-taking questions", "social reasoning", "false-belief scenarios", "character knowledge tracking"]
avoid_when: ["omniscient narrator perspective needed", "no distinct character perspectives", "single-agent factual QA", "low-latency requirements"]
composes_with: ["chain-of-thought", "system-2-attention", "few-shot"]

tags: ["perception", "theory-of-mind", "perspective-taking", "context-filtering", "social-cognition", "two-pass"]
---

# SimToM (Simulated Theory of Mind)

> **One-line summary:** A two-step prompting method that first filters a narrative to only what a specific character knows, then answers perspective-dependent questions using that filtered view.

## Overview

Theory of Mind (ToM) is the ability to attribute mental states --- beliefs, intents, desires, knowledge --- to others and to understand that others may hold beliefs different from one's own. Large language models notoriously struggle with ToM tasks, particularly false-belief scenarios where a character holds an outdated or incorrect belief because they lack information the narrator (and reader) possesses. SimToM addresses this by explicitly simulating the information state of a specific character before answering questions about that character's beliefs.

The key insight from Wilf et al. (2023) is that LLMs fail ToM tasks not because they lack reasoning ability but because they fail to properly scope their attention to the right subset of information. When the full story is in context, the model "knows too much" and cannot help but use privileged information when reasoning about what a character believes. SimToM solves this by creating an information barrier: the first call extracts only what the target character has seen, heard, or been told, and the second call answers based solely on that restricted view.

This approach is closely related to System 2 Attention (S2A) in its two-pass architecture, but where S2A filters for relevance, SimToM filters for perspective. The technique proved highly effective on standard ToM benchmarks, significantly improving performance on classic false-belief tasks like the Sally-Anne test and its variants.

## How It Works

1. **Perspective Identification:** Given a narrative and a target character, identify which character's perspective we need to simulate.
2. **Information Filtering (Call 1):** Ask the LLM to list only the facts, events, and statements that the target character has directly witnessed, been told about, or could reasonably infer. Exclude any information the character would not have access to.
3. **Perspective-Grounded Answering (Call 2):** Present only the filtered information alongside the question. The LLM answers based solely on what the character knows, naturally producing correct false-belief responses.

### Diagram

```
┌──────────────────────────┐
│   Full Narrative          │
│   + Target Character      │
│   + Question              │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│  CALL 1: Perspective     │
│  Filter                  │
│  "What does {character}  │
│   know/see/hear?"        │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│  Character's Knowledge   │
│  State (filtered view)   │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│  CALL 2: Answer from     │
│  Character's Perspective │
│  "Based only on this,    │
│   what does {character}  │
│   believe?"              │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│  Perspective-Correct     │
│  Answer                  │
└──────────────────────────┘
```

## Template

**Call 1 — Perspective Filtering:**
```
Read the following story carefully. Then list only the facts and events that
{character} has directly witnessed, been told about, or could reasonably know.
Do NOT include anything that {character} has no way of knowing.

Story:
{narrative}

What {character} knows:
```

**Call 2 — Perspective-Grounded Answer:**
```
Based ONLY on the following information (which represents everything {character}
knows), answer the question. Do not use any outside knowledge.

What {character} knows:
{filtered_knowledge}

Question:
{question}

Answer:
```

## Examples

### Example 1: Classic False-Belief (Sally-Anne)

**Input (Call 1):**
```
Read the following story carefully. Then list only the facts and events that
Sally has directly witnessed, been told about, or could reasonably know.
Do NOT include anything that Sally has no way of knowing.

Story:
Sally places her marble in the red basket and leaves the room. While Sally is
away, Anne moves the marble from the red basket to the blue box. Sally returns
to the room.

What Sally knows:
```

**Output (Call 1):**
```
- Sally placed her marble in the red basket.
- Sally left the room and then returned.
- Sally does NOT know that anyone moved the marble while she was away.
- From Sally's perspective, the marble is still in the red basket.
```

**Input (Call 2):**
```
Based ONLY on the following information (which represents everything Sally
knows), answer the question. Do not use any outside knowledge.

What Sally knows:
- Sally placed her marble in the red basket.
- Sally left the room and then returned.
- Sally does NOT know that anyone moved the marble while she was away.
- From Sally's perspective, the marble is still in the red basket.

Question:
Where will Sally look for her marble?

Answer:
```

**Output (Call 2):**
```
Sally will look for her marble in the red basket, because that is where she
left it and she has no knowledge that it was moved.
```

### Example 2: Information Asymmetry in a Meeting

**Input (Call 1):**
```
Read the following story carefully. Then list only the facts and events that
Bob has directly witnessed, been told about, or could reasonably know.
Do NOT include anything that Bob has no way of knowing.

Story:
Alice, Bob, and Carol are planning a surprise birthday party for Dave. In a
group email that includes Bob, Alice proposes Saturday at 7pm at her house.
Bob replies agreeing. Later, Carol privately texts Alice suggesting they change
it to Sunday at 6pm because the caterer is unavailable Saturday. Alice agrees
and texts the caterer to confirm Sunday. Alice has not yet told Bob about the
change. Dave has no idea about any party.

What Bob knows:
```

**Output (Call 1):**
```
- A surprise birthday party is being planned for Dave.
- Alice proposed Saturday at 7pm at her house (from the group email).
- Bob agreed to Saturday at 7pm.
- Bob does NOT know about Carol's suggestion to change to Sunday.
- Bob does NOT know Alice agreed to change the date.
- Bob believes the party is on Saturday at 7pm at Alice's house.
```

**Input (Call 2):**
```
Based ONLY on the following information (which represents everything Bob
knows), answer the question. Do not use any outside knowledge.

What Bob knows:
- A surprise birthday party is being planned for Dave.
- Alice proposed Saturday at 7pm at her house (from the group email).
- Bob agreed to Saturday at 7pm.
- Bob does NOT know about Carol's suggestion to change to Sunday.
- Bob does NOT know Alice agreed to change the date.
- Bob believes the party is on Saturday at 7pm at Alice's house.

Question:
When does Bob think the party is?

Answer:
```

**Output (Call 2):**
```
Bob thinks the party is on Saturday at 7pm at Alice's house. He is unaware
of the schedule change to Sunday at 6pm.
```

## When to Use

- Tasks requiring reasoning about what specific characters know or believe
- False-belief scenarios where characters have incomplete information
- Multi-character narratives with information asymmetry
- Social reasoning tasks (e.g., predicting behavior based on beliefs)
- Game theory scenarios where agents have private information
- Evaluating misunderstandings or miscommunications in dialogues

## When to Avoid

- Questions that require omniscient or narrator perspective
- Single-agent factual question-answering with no perspective component
- Tasks where all characters share the same information
- Real-time applications that cannot tolerate two sequential LLM calls
- When the narrative is extremely short and the perspective is obvious

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | ~1.5-2x | Filtered perspective is typically shorter than full narrative |
| Latency | ~2x | Two sequential LLM calls |
| Quality gain | +20-50% | On ToM benchmarks, especially false-belief tasks (per paper) |
| False-belief accuracy | High | Dramatic improvement on Sally-Anne style tasks |
| API calls | 2 | One for filtering, one for answering |

## Variants

- **Multi-Character SimToM:** Run Call 1 for each character independently, then compare their knowledge states to answer questions about interactions and misunderstandings.
- **Incremental SimToM:** Track a character's knowledge state as events unfold, updating the filtered view after each new event rather than processing the full narrative each time.
- **Self-SimToM:** Combine both steps into a single prompt: "First list what the character knows, then answer." Faster but less reliable for complex scenarios.
- **SimToM with Confidence:** Add a confidence estimate to the answer, flagging cases where the character's knowledge state is ambiguous.

## Composability

- **SimToM + Chain-of-Thought:** After filtering to the character's perspective, use CoT to reason through what the character would conclude from their limited information.
- **SimToM + S2A:** Apply S2A first to remove noise and irrelevant details, then apply SimToM to filter to a character's perspective. Useful for long, noisy narratives.
- **SimToM + Few-Shot:** Provide examples of correct perspective-filtering in Call 1 to improve extraction quality for complex scenarios.
- **SimToM + Self-Consistency:** Generate multiple perspective-filtered views and answers, then vote on the most common response.

## Limitations

- Doubles the number of LLM calls and associated latency
- The model may struggle to correctly identify what a character would "reasonably infer" versus what they directly observed
- Implicit knowledge (e.g., common sense a character would have) is hard to specify in the filtering step
- Performance degrades with very long narratives containing many characters and events
- The technique assumes the narrative provides clear information about who witnessed what
- Does not handle second-order beliefs well (what A thinks B thinks C knows)

## Sources

- **Primary:** [Think Twice: Perspective-Taking Improves Large Language Models' Theory-of-Mind Capabilities](https://arxiv.org/abs/2311.10227) — Wilf et al., 2023
- **Background:** [Theory of Mind May Have Spontaneously Emerged in Large Language Models](https://arxiv.org/abs/2302.02083) — Kosinski, 2023
- **Related:** [System 2 Attention (is something you might need too)](https://arxiv.org/abs/2311.11829) — Weston & Sukhbaatar, 2023
