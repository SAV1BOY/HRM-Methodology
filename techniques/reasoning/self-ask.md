---
id: self-ask
name: "Self-Ask Prompting"
aliases:
  - self ask
  - follow-up question prompting
  - recursive question decomposition
category: reasoning
family: decomposition
year: 2022
authors:
  - Ofir Press
  - Muru Zhang
  - Sewon Min
  - Ludwig Schmidt
  - Noah A. Smith
  - Mike Lewis
paper: "https://arxiv.org/abs/2210.03350"
paper_title: "Measuring and Narrowing the Compositionality Gap in Language Models"
venue: "EMNLP 2023"
code: "https://github.com/ofirpress/self-ask"
complexity: medium
token_cost: medium
latency: medium
num_calls: 1-5
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - multi-hop question answering
  - compositional questions
  - knowledge-intensive reasoning
  - bridging entity questions
  - factual reasoning chains
  - questions requiring intermediate fact lookup
avoid_when:
  - single-hop factual questions
  - mathematical computation tasks
  - tasks without natural sub-question structure
  - open-ended generation
  - problems requiring procedural rather than factual reasoning
composes_with:
  - chain-of-thought
  - react
  - least-to-most
  - self-consistency
tags:
  - decomposition
  - reasoning
  - question-answering
  - multi-hop
  - compositionality
  - retrieval-compatible
---

# Self-Ask Prompting

> **One-line summary:** Enable multi-hop reasoning by teaching the model to explicitly generate and answer intermediate follow-up questions before addressing the original complex question.

## Overview

Self-Ask, introduced by Press et al. (2022), is a prompting technique designed to address the compositionality gap in language models -- the disparity between a model's ability to answer individual factual questions and its ability to compose those facts into multi-hop reasoning chains. The key insight is that models often know the individual facts needed to answer a complex question but fail to chain them together. Self-Ask solves this by training the model (via few-shot examples) to explicitly ask and answer intermediate follow-up questions.

The technique works by showing the model examples where a complex question is followed by a structured sequence: "Are follow-up questions needed here: Yes. Follow up: [sub-question]. Intermediate answer: [answer]." This pattern repeats until all necessary intermediate facts have been established, at which point the model provides the final answer. The explicit question-answer format makes the reasoning chain transparent and auditable, with each intermediate step clearly linked to a verifiable sub-question. The authors measured a compositionality gap of 40%+ in GPT-3 on multi-hop questions, which Self-Ask substantially narrowed.

Self-Ask is particularly powerful when combined with a search engine or retrieval system to answer the follow-up questions (the authors call this "Self-Ask + Search"). In this configuration, the model generates the follow-up questions but delegates answering them to an external search tool, grounding the reasoning in retrieved facts rather than the model's parametric memory. This hybrid approach significantly reduces hallucination and improves factual accuracy on knowledge-intensive multi-hop questions like those in Musique, 2WikiMultihopQA, and Bamboogle.

## How It Works

1. **Present few-shot exemplars**: Show the model 3-5 examples of multi-hop questions decomposed into follow-up questions with intermediate answers.
2. **Ask the target question**: Append the new question to the prompt.
3. **Model generates follow-up check**: The model outputs "Are follow-up questions needed here: Yes/No."
4. **Generate follow-up questions**: If yes, the model generates a follow-up question ("Follow up: ...") and answers it ("Intermediate answer: ...").
5. **Iterate**: The model continues generating follow-up questions and answers until it has enough information.
6. **Final answer**: The model outputs "So the final answer is: ..." once all sub-questions are resolved.

### Diagram

```
+-----------------------------------------+
|  Q: {complex multi-hop question}        |
|                                         |
|  Are follow-up questions needed here:   |
|  Yes.                                   |
|                                         |
|  Follow up: {sub-question 1}            |
|  Intermediate answer: {answer 1}   <----+-- (or: Search Engine)
|                                         |
|  Follow up: {sub-question 2}            |
|  Intermediate answer: {answer 2}   <----+-- (or: Search Engine)
|                                         |
|  Follow up: {sub-question 3}            |
|  Intermediate answer: {answer 3}   <----+-- (or: Search Engine)
|                                         |
|  So the final answer is: {answer}       |
+-----------------------------------------+
```

## Template

```
Question: {exemplar_question_1}
Are follow-up questions needed here: Yes.
Follow up: {follow_up_q1a}
Intermediate answer: {intermediate_a1a}
Follow up: {follow_up_q1b}
Intermediate answer: {intermediate_a1b}
So the final answer is: {final_answer_1}

Question: {exemplar_question_2}
Are follow-up questions needed here: Yes.
Follow up: {follow_up_q2a}
Intermediate answer: {intermediate_a2a}
Follow up: {follow_up_q2b}
Intermediate answer: {intermediate_a2b}
So the final answer is: {final_answer_2}

Question: {test_question}
Are follow-up questions needed here:
```

## Examples

### Example 1: Multi-Hop Knowledge Question

**Prompt:**
```
Question: Who lived longer, Muhammad Ali or Alan Turing?
Are follow-up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali lived longer.

Question: Who was the president of the US when the founder of SpaceX
was born?
Are follow-up questions needed here: Yes.
Follow up: Who is the founder of SpaceX?
Intermediate answer: Elon Musk founded SpaceX.
Follow up: When was Elon Musk born?
Intermediate answer: Elon Musk was born on June 28, 1971.
Follow up: Who was the president of the US in 1971?
Intermediate answer: Richard Nixon was the president of the US in 1971.
So the final answer is: Richard Nixon.

Question: Was the director of Inception born in the same country as the
author of Harry Potter?
Are follow-up questions needed here:
```

**Model Output:**
```
Yes.
Follow up: Who directed Inception?
Intermediate answer: Christopher Nolan directed Inception.
Follow up: Where was Christopher Nolan born?
Intermediate answer: Christopher Nolan was born in London, England.
Follow up: Who is the author of Harry Potter?
Intermediate answer: J.K. Rowling is the author of Harry Potter.
Follow up: Where was J.K. Rowling born?
Intermediate answer: J.K. Rowling was born in Yate, England.
So the final answer is: Yes, both were born in England.
```

### Example 2: Temporal Reasoning

**Prompt (with one exemplar for brevity):**
```
Question: Did the first iPhone release before or after the founding
of YouTube?
Are follow-up questions needed here: Yes.
Follow up: When was the first iPhone released?
Intermediate answer: The first iPhone was released on June 29, 2007.
Follow up: When was YouTube founded?
Intermediate answer: YouTube was founded on February 14, 2005.
So the final answer is: The first iPhone was released after the
founding of YouTube.

Question: Was Wikipedia launched before or after the Human Genome
Project was completed?
Are follow-up questions needed here:
```

**Model Output:**
```
Yes.
Follow up: When was Wikipedia launched?
Intermediate answer: Wikipedia was launched on January 15, 2001.
Follow up: When was the Human Genome Project completed?
Intermediate answer: The Human Genome Project was completed in April
2003.
So the final answer is: Wikipedia was launched before the Human
Genome Project was completed.
```

## When to Use

- The task involves multi-hop reasoning where facts must be chained together.
- The model knows individual facts but fails to compose them (compositionality gap).
- Questions require bridging entities (finding an intermediate entity to connect the question to the answer).
- You want transparent, auditable reasoning with clearly identified sub-questions.
- You can optionally augment with search for grounded, factual intermediate answers.
- The domain is knowledge-intensive (history, geography, science, current events).

## When to Avoid

- Single-hop factual questions that require no decomposition.
- Mathematical or computational tasks where sub-questions are not natural (use CoT or PS+ instead).
- Open-ended or creative tasks without clear factual sub-questions.
- The model lacks the factual knowledge to answer sub-questions and no search tool is available.
- Extremely time-sensitive applications where the iterative question-answer loop adds too much latency.
- Problems requiring procedural or computational reasoning rather than factual composition.

## Cost & Performance

| Dimension          | Rating   | Notes                                           |
|--------------------|----------|-------------------------------------------------|
| Token overhead     | Medium   | Sub-questions add tokens but are concise          |
| Latency            | Medium   | 1 call self-contained; more if using search       |
| Accuracy gain      | High     | +10-20% on multi-hop QA benchmarks                |
| Implementation     | Low      | Structured few-shot prompt; simple parsing         |
| Model requirements | Large    | Best at 100B+; works reasonably at smaller scales  |

## Variants

- **Self-Ask + Search**: The model generates follow-up questions, but a search engine (e.g., Google, Bing) provides the intermediate answers. This grounds reasoning in retrieved facts and dramatically reduces hallucination.
- **Self-Ask + Retrieval**: Similar to search but uses a vector database or knowledge base to answer follow-up questions with domain-specific knowledge.
- **Adaptive Self-Ask**: The model decides dynamically whether follow-up questions are needed, allowing simple questions to be answered directly without decomposition overhead.
- **Recursive Self-Ask**: If a follow-up question is itself multi-hop, the model recursively decomposes it further before answering.

## Composability

Self-Ask integrates well with retrieval and reasoning techniques:

- **Self-Ask + ReAct**: Self-Ask can be viewed as a structured form of the "Thought" component in ReAct, where thoughts are explicitly framed as follow-up questions. The two techniques can be merged so that follow-up questions trigger search actions. See `react.md`.
- **Self-Ask + Self-Consistency**: Sample multiple Self-Ask chains and vote on the final answer. Different chains may identify different bridging entities or decomposition strategies. See `self-consistency.md`.
- **Self-Ask + CoT**: Use Chain-of-Thought reasoning within each intermediate answer to handle sub-questions that themselves require multi-step reasoning. See `chain-of-thought.md`.
- **Self-Ask + Least-to-Most**: Both are decomposition techniques; Self-Ask decomposes into questions while L2M decomposes into problems. They can be combined when sub-problems are best phrased as questions. See `least-to-most.md`.

## Limitations

- **Factual dependence**: Self-Ask relies on the model's (or search engine's) ability to answer individual sub-questions correctly. If intermediate answers are wrong, the final answer will be wrong.
- **Over-decomposition**: The model may generate unnecessary follow-up questions, wasting tokens and potentially introducing confusion or factual errors.
- **Limited to question-answerable decompositions**: Not all reasoning steps naturally take the form of questions. Mathematical computations, spatial reasoning, and procedural tasks may not fit the question-answer format.
- **Exemplar design**: The few-shot examples must carefully demonstrate the decomposition pattern; poor exemplars lead to shallow or incorrect decompositions.
- **Search integration complexity**: While Self-Ask + Search is powerful, it requires engineering a reliable search pipeline with answer extraction, adding system complexity.
- **Compositionality gap persistence**: Even with Self-Ask, models can still fail when the number of required hops exceeds what the exemplars demonstrate.

## Sources

- Press, O., Zhang, M., Min, S., Schmidt, L., Smith, N. A., & Lewis, M. (2022). Measuring and Narrowing the Compositionality Gap in Language Models. *EMNLP 2023*. https://arxiv.org/abs/2210.03350
- Trivedi, H., Balasubramanian, N., Khot, T., & Sabharwal, A. (2022). Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions. https://arxiv.org/abs/2212.10509
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. https://arxiv.org/abs/2210.03629
