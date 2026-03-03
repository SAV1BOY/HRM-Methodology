---
id: thread-of-thought
name: "Thread of Thought"
aliases:
  - ThoT
  - Thread-of-Thought
  - Threaded Reasoning
category: reasoning
family: thought-generation
year: 2023
authors:
  - Yucheng Zhou
  - Xiubo Geng
  - Tao Shen
  - Chongyang Tao
  - Guodong Long
  - Jian-Guang Lou
  - Jianbing Shen
paper: "https://arxiv.org/abs/2311.08734"
paper_title: "Thread of Thought Unraveling Chaotic Contexts"
venue: "Preprint 2023"
code: null
complexity: low
token_cost: medium
latency: medium
num_calls: 1
requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - chaotic or unstructured input text
  - long documents with scattered information
  - retrieval-augmented generation with noisy context
  - conversation summarization
  - multi-document question answering
  - information extraction from messy data
avoid_when:
  - input is already well-structured and concise
  - simple factual questions with short context
  - mathematical reasoning (use CoT instead)
  - tasks not involving context comprehension
  - token budget is very tight
composes_with:
  - chain-of-thought
  - retrieval-augmented-generation
  - self-consistency
  - few-shot-prompting
tags:
  - context-comprehension
  - unstructured-text
  - information-extraction
  - summarization
  - long-context
  - retrieval
---

# Thread of Thought

> **One-line summary:** Systematically walks through chaotic or unstructured context in manageable segments before answering, improving comprehension of messy real-world text.

## Overview

Thread of Thought (ThoT), introduced by Zhou et al. (2023), addresses a specific challenge that standard chain-of-thought prompting does not handle well: reasoning over chaotic, unstructured, or noisy input contexts. While CoT excels at structured reasoning tasks (math, logic), it assumes that the relevant information is clearly presented in the prompt. In real-world applications -- retrieval-augmented generation, long document QA, conversation summarization -- the input context is often a disorganized jumble of relevant facts, irrelevant noise, contradictory statements, and implicit information scattered across paragraphs. ThoT introduces a systematic approach to *untangling* this chaos before reasoning over it.

The key mechanism is deceptively simple: instead of asking the model to answer directly from a messy context, ThoT instructs the model to "walk me through this context in manageable parts" before answering the question. This trigger phrase causes the model to segment the context, extract relevant information from each segment, organize it mentally, and then synthesize an answer from the organized understanding. The analogy is to how a human might handle a long, convoluted document: rather than trying to answer a question after one read-through, they would methodically go through it section by section, noting the relevant points, before formulating a response.

Empirically, ThoT shows significant improvements over both standard prompting and chain-of-thought on tasks involving noisy or long contexts, including retrieval-augmented QA, multi-turn conversation understanding, and information extraction from unstructured documents. The technique is particularly effective when combined with RAG systems, where retrieved passages often contain a mix of relevant and irrelevant information. By systematically processing the context before reasoning, ThoT reduces the impact of distracting or misleading information that would otherwise derail the model's answer.

## How It Works

1. **Context presentation**: The full (potentially chaotic) context is provided to the model along with the question.
2. **Thread trigger**: The prompt includes the instruction "Walk me through this context in manageable parts before answering" (or a similar threading directive).
3. **Segment processing**: The model systematically walks through the context, breaking it into logical segments and extracting the relevant information from each.
4. **Information synthesis**: After processing all segments, the model synthesizes the extracted relevant information into a coherent understanding.
5. **Answer generation**: Based on the synthesized understanding, the model generates the final answer.

### Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                   CHAOTIC INPUT CONTEXT                       │
│                                                               │
│  "...meeting notes from Tuesday... revenue was $2.3M...      │
│   side discussion about lunch plans... Q3 target revised     │
│   to $3.1M... John mentioned the client delay... weather     │
│   disrupted shipping... Sarah's promotion approved...        │
│   budget increase of 15%... parking lot construction..."     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  THREAD OF THOUGHT: "Walk through in manageable parts"       │
│                                                               │
│  Segment 1: Meeting context                                   │
│    → Tuesday meeting, relevant: revenue and targets           │
│                                                               │
│  Segment 2: Financial data                                    │
│    → Revenue: $2.3M, Q3 target: $3.1M, budget +15%          │
│                                                               │
│  Segment 3: Operational issues                                │
│    → Client delay (John), shipping disrupted by weather       │
│                                                               │
│  Segment 4: HR/administrative (not relevant to question)      │
│    → Sarah's promotion, parking construction (skip)           │
│                                                               │
│  Synthesis: Relevant financials extracted, noise filtered      │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  ANSWER: Based on the organized context, Q3 revenue target   │
│  is $3.1M with a 15% budget increase. Current revenue is     │
│  $2.3M with risks from client delays and shipping issues.    │
└──────────────────────────────────────────────────────────────┘
```

## Template

### Zero-Shot ThoT

```
Context:
{chaotic_context}

Question: {question}

Walk me through this context in manageable parts, then answer the question.
Segment the information, identify what's relevant, and synthesize your answer.
```

### ThoT with Explicit Structure

```
Context:
{chaotic_context}

Question: {question}

Before answering, systematically process the context:
1. Break the context into logical segments.
2. For each segment, note what information is relevant to the question.
3. Discard irrelevant information.
4. Synthesize the relevant pieces into a coherent understanding.
5. Answer the question based on your synthesis.
```

## Examples

### Example 1: Noisy Retrieval-Augmented QA

**Input:**
```
Context:
[Retrieved passage 1]: The Eiffel Tower was completed in 1889 for the World's
Fair. It stands 330 meters tall including antennas. The tower was designed by
Gustave Eiffel's engineering company.

[Retrieved passage 2]: Paris is the capital of France with a population of
about 2.1 million in the city proper. The city is known for its cafe culture
and the Louvre museum which houses the Mona Lisa.

[Retrieved passage 3]: The Burj Khalifa in Dubai is the world's tallest
building at 828 meters. It was completed in 2010. The Eiffel Tower was the
world's tallest structure for 41 years until the Chrysler Building in 1930.

[Retrieved passage 4]: French cuisine is renowned worldwide. Popular dishes
include coq au vin, bouillabaisse, and croissants. The Michelin Guide
originated in France in 1900.

Question: How long was the Eiffel Tower the world's tallest structure?

Walk me through this context in manageable parts, then answer.
```

**Output:**
```
Let me walk through each passage:

Segment 1 (Eiffel Tower basics): Completed 1889, 330m tall, designed by
Eiffel's company. Relevant: completion year 1889.

Segment 2 (Paris facts): General info about Paris, population, Louvre.
Not directly relevant to the height record question.

Segment 3 (Height comparisons): Burj Khalifa is current tallest at 828m.
Key fact: "Eiffel Tower was world's tallest structure for 41 years until
the Chrysler Building in 1930." Directly answers the question.

Segment 4 (French cuisine): Entirely irrelevant to the question.

Synthesis: Passage 3 directly states the Eiffel Tower held the record for
41 years (1889-1930), until surpassed by the Chrysler Building.

Answer: The Eiffel Tower was the world's tallest structure for 41 years,
from its completion in 1889 until the Chrysler Building surpassed it in 1930.
```

### Example 2: Conversation Summarization

**Input:**
```
Context:
[Chat transcript - Project Alpha standup, scattered messages]
9:01 AM - Bob: good morning everyone
9:02 AM - Alice: morning! quick update - the API integration is done
9:02 AM - Charlie: nice! btw has anyone seen my coffee mug?
9:03 AM - Alice: it also passed all unit tests
9:03 AM - Bob: @Charlie check the kitchen
9:04 AM - Diana: I'm blocked on the database migration, need DevOps help
9:04 AM - Charlie: thanks Bob
9:05 AM - Alice: I'll start on the frontend components today
9:05 AM - Bob: Diana, I'll ping the DevOps team after standup
9:06 AM - Charlie: my PR for the auth module is ready for review
9:06 AM - Bob: also reminder: team lunch Friday at noon
9:07 AM - Diana: thanks Bob. ETA for unblock is hopefully today
9:07 AM - Alice: I can review Charlie's PR this afternoon
9:08 AM - Bob: great, let's wrap up. any other blockers?
9:08 AM - Charlie: none from me
9:08 AM - Diana: just the DB migration thing

Question: What are the key project updates and action items from this standup?

Walk me through this context in manageable parts, then answer.
```

**Output:**
```
Walking through the conversation:

Segment 1 (Alice's updates, messages at 9:02-9:05):
  - API integration complete, unit tests passing
  - Starting frontend components today
  - Will review Charlie's PR this afternoon

Segment 2 (Diana's status, 9:04-9:08):
  - Blocked on database migration, needs DevOps support
  - Hoping for unblock today

Segment 3 (Charlie's status, 9:06-9:08):
  - Auth module PR ready for review
  - No other blockers

Segment 4 (Bob's actions, 9:05-9:08):
  - Will contact DevOps team for Diana's blocker
  - Team lunch Friday reminder

Segment 5 (Noise - not project-relevant):
  - Coffee mug discussion (irrelevant)

Synthesis:

Key project updates:
- API integration completed and tested (Alice)
- Auth module PR ready for review (Charlie)
- Database migration blocked pending DevOps help (Diana)

Action items:
- Bob: ping DevOps team to unblock Diana's database migration
- Alice: start frontend components; review Charlie's auth PR this afternoon
- Team lunch scheduled for Friday at noon
```

## When to Use

- Retrieval-augmented generation where retrieved passages contain a mix of relevant and irrelevant information.
- Long, unstructured documents (meeting transcripts, email threads, chat logs) where information is scattered and interleaved with noise.
- Multi-document QA where information must be gathered from multiple sources with varying relevance.
- Conversation summarization where key points are buried among casual chatter and off-topic discussion.
- Any task where the input context is messy, verbose, or poorly organized and the model needs to extract specific information.
- Information extraction from real-world documents that were not written for machine consumption.

## When to Avoid

- Input context is already well-structured, concise, and directly relevant to the question.
- Simple factual questions where the answer is explicit in a short context and segmentation adds no value.
- Mathematical reasoning tasks where the challenge is computation, not context comprehension.
- Token budget is very tight and the segmentation step adds significant overhead.
- Tasks that do not involve processing external context (e.g., creative writing, code generation from specifications).
- Very short contexts (1-2 sentences) where there is nothing to segment.

## Cost & Performance

| Metric              | Value                     | Notes                                             |
|---------------------|---------------------------|----------------------------------------------------|
| Token overhead       | ~1.5-2.5x                | Segmentation + synthesis before answering            |
| Latency              | Medium                    | Single call, longer generation                       |
| Quality gain (RAG)   | +5-12% on noisy contexts  | Larger gains with noisier retrieved passages         |
| Quality gain (conv.) | +8-15% on summarization   | Significant improvement for scattered conversations  |
| Implementation cost  | Very low                  | Single trigger phrase or brief instruction            |
| Model requirements   | 7B+ effective             | Benefits scale with model capability                  |

## Variants

- **Explicit Segmentation ThoT:** Provide numbered segment boundaries in the prompt to guide the model on how to break up the context, rather than letting it choose.
- **Relevance-Scored ThoT:** Ask the model to assign a relevance score (1-5) to each segment before synthesizing, making the filtering step more explicit.
- **Hierarchical ThoT:** For very long documents, first segment into major sections, then segment each section into sub-parts, processing in a top-down manner.
- **ThoT + Highlighting:** Instead of processing the full context, ask the model to first highlight (quote) the relevant passages, then reason over only the highlighted portions.
- **Streaming ThoT:** In a streaming context, process the input context incrementally as it arrives, building up understanding progressively rather than processing all at once.

## Composability

- **ThoT + Chain-of-Thought:** After organizing the context with ThoT, apply CoT reasoning to the extracted relevant information. ThoT handles comprehension; CoT handles reasoning.
- **ThoT + RAG:** ThoT is a natural companion to retrieval-augmented generation. Use RAG to retrieve passages, then ThoT to systematically process and filter the retrieved content before generating an answer.
- **ThoT + Self-Consistency:** Generate multiple threaded analyses of the same context (each may segment differently) and vote on the final answer for increased robustness.
- **ThoT + Few-Shot Prompting:** Provide exemplars that demonstrate the threading process on similar contexts, establishing the expected segmentation granularity and relevance filtering behavior.
- **ThoT + Summarization:** Use ThoT as the first stage of a summarization pipeline, organizing chaotic input before condensing it.

## Limitations

- Adds token overhead from the segmentation and synthesis steps, which may be wasteful when the context is already well-organized.
- The model may over-segment or under-segment the context, leading to either excessive detail on irrelevant parts or insufficient attention to relevant scattered information.
- Does not help with reasoning difficulty; if the challenge is in the computation or logic rather than context comprehension, ThoT provides no benefit.
- The quality of segmentation depends on the model's understanding of the question -- if the model misunderstands what is being asked, it may filter out relevant information.
- For very long contexts that exceed the model's context window, ThoT alone is insufficient; chunking or hierarchical approaches are needed.
- The technique has been primarily evaluated on English-language contexts; effectiveness on other languages and culturally different document structures is less studied.
- May produce verbose outputs that repeat information from the context unnecessarily during the threading phase.

## Sources

- **Primary:** Zhou, Y., Geng, X., Shen, T., Tao, C., Long, G., Lou, J.-G., & Shen, J. (2023). Thread of Thought Unraveling Chaotic Contexts. https://arxiv.org/abs/2311.08734
- **Related:** Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*. https://arxiv.org/abs/2005.11401
- **Related:** Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. https://arxiv.org/abs/2201.11903
