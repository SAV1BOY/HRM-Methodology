# The Prompt Report — Detailed Summary

> Summary of "The Prompt Report: A Systematic Survey of Prompting Techniques" by Schulhoff et al. (2024). arXiv: [2406.06608](https://arxiv.org/abs/2406.06608).

---

## Paper Overview

The Prompt Report is the most comprehensive systematic survey of prompting techniques for large language models to date. It catalogs 58+ distinct text-based prompting techniques, along with multilingual, multimodal, and agent-based methods, and organizes them into a structured taxonomy. The paper also covers prompt engineering best practices, evaluation methods, security considerations, and the role of prompting in the broader AI landscape.

---

## Taxonomy Structure

The paper organizes prompting techniques into the following major categories:

### Text-Based Techniques

#### 1. Zero-Shot Techniques
Techniques that require no examples in the prompt:
- **Role Prompting** — Assigning a persona to the model
- **Emotion Prompting** — Adding emotional stimuli ("This is very important to my career")
- **System 2 Attention (S2A)** — Regenerating context to remove bias
- **SimToM** — Simulating Theory of Mind for perspective tasks
- **Rephrase and Respond (RaR)** — Model rephrases the question before answering
- **Self-Ask** — Model generates follow-up questions and answers them
- **Directional Stimulus Prompting** — Providing hints to guide generation

#### 2. Few-Shot Techniques
Techniques using in-context examples:
- **Few-Shot Prompting (ICL)** — Standard example-based prompting
- **Demonstration selection** — Strategies for choosing effective examples (kNN, diversity, similarity)
- **Demonstration ordering** — Impact of example order on performance

#### 3. Thought Generation
Techniques that elicit step-by-step reasoning:
- **Chain-of-Thought (CoT)** — Reasoning traces in examples
- **Zero-Shot CoT** — "Let's think step by step"
- **Analogical Prompting** — Self-generating relevant examples
- **Contrastive CoT** — Including both correct and incorrect reasoning
- **Thread-of-Thought (ThoT)** — Reasoning through chaotic contexts
- **Tab-CoT** — Tabular format for multi-variable reasoning
- **Step-Back Prompting** — Abstracting to principles before answering

#### 4. Decomposition
Techniques that break complex problems into parts:
- **Least-to-Most** — Solve sub-problems in increasing complexity
- **Plan-and-Solve (PS+)** — Generate plan then execute
- **Tree of Thoughts (ToT)** — Tree-structured exploration with backtracking
- **Graph of Thoughts (GoT)** — Graph-structured reasoning with merge/refine
- **Program of Thoughts (PoT)** — Using code as the reasoning medium
- **Skeleton of Thought (SoT)** — Outline then expand in parallel
- **Algorithm of Thoughts (AoT)** — Algorithmic search patterns in a single call

#### 5. Ensembling
Techniques that aggregate multiple outputs:
- **Self-Consistency** — Sample multiple CoT paths, take majority vote
- **Universal Self-Consistency** — Self-Consistency without fixed answer format
- **Meta-CoT** — Consensus across multiple reasoning approaches
- **Multi-Agent Debate** — Multiple simulated agents debate and converge

#### 6. Self-Criticism
Techniques for self-improvement:
- **Self-Refine** — Iterative critique and revision
- **Chain-of-Verification (CoVe)** — Generate then verify with focused questions
- **Reflexion** — Reflect on failures to improve future attempts
- **Cumulative Reasoning** — Incrementally build solutions with verification

### Agent-Based Techniques

- **ReAct** — Interleaved reasoning and acting
- **Tool Use / Function Calling** — Invoking external tools
- **Prompt Chaining** — Sequential multi-prompt pipelines
- **Memory and Context Management** — Persistent information across turns

### Multilingual Techniques

- **Cross-lingual prompting** — Techniques for non-English and multilingual tasks
- **Chain-of-Thought in different languages** — Impact of reasoning language choice

### Multimodal Techniques

- **Image prompting** — Techniques specific to vision-language models
- **Multimodal CoT** — Reasoning across text and image modalities

---

## Key Findings

### 1. Technique Effectiveness Rankings

The paper synthesizes effectiveness data across benchmarks:

| Rank | Category | Typical Improvement | Best For |
|------|----------|-------------------|----------|
| 1 | Self-Consistency + CoT | +15-25% on math/logic | High-stakes reasoning |
| 2 | Chain-of-Thought | +10-20% on reasoning | Multi-step problems |
| 3 | Few-Shot | +5-15% on format/style | Format control, classification |
| 4 | Tree of Thoughts | +10-30% on search tasks | Creative puzzles, planning |
| 5 | Self-Refine | +5-15% on quality | Writing, code improvement |
| 6 | Role Prompting | +0-10% on domain tasks | Domain expertise, voice |
| 7 | Zero-Shot CoT | +5-10% on reasoning | Quick reasoning boost |

### 2. Composition Patterns

The paper identifies common and effective technique compositions:

- **CoT + Self-Consistency** — The most studied and effective combination
- **Few-Shot + CoT** — Examples with reasoning traces
- **Role + CoT** — Domain persona with structured reasoning
- **ToT + Self-Refine** — Explore then polish
- **ReAct + Tool Use** — The standard agent loop
- **RAG + CoVe** — Retrieve then verify

### 3. When Techniques Fail

Important negative findings:

- **CoT can hurt simple tasks** — Adding reasoning steps to trivial factual recall can reduce accuracy by introducing reasoning errors
- **Few-Shot can introduce bias** — Examples can anchor the model to patterns that don't generalize
- **Self-Consistency is expensive** — Requires 5-40 calls; diminishing returns after ~10
- **Role prompting is unreliable** — Can introduce persona-consistent biases that harm factual accuracy
- **ToT is overkill for most tasks** — Linear CoT suffices for the vast majority of reasoning tasks

### 4. Model-Specific Findings

- Larger models benefit more from CoT than smaller models
- Few-shot example selection matters more for smaller models
- Instruction-tuned models often don't need few-shot examples
- Some techniques (e.g., Self-Consistency) work with any model; others require instruction following

---

## Evaluation Framework

The paper proposes a multi-dimensional evaluation framework:

### Dimensions

1. **Accuracy** — Correctness of the output
2. **Robustness** — Consistency across input variations
3. **Efficiency** — Token and API call cost
4. **Latency** — Wall-clock time to completion
5. **Composability** — How well the technique chains with others

### Recommended Evaluation Approach

1. Define task-specific metrics (accuracy, F1, BLEU, human rating)
2. Test on diverse inputs (not just benchmarks)
3. Measure cost and latency alongside quality
4. Compare against the simplest baseline (zero-shot)
5. Test technique compositions, not just individual techniques

---

## Security Analysis

The paper covers prompt security as a distinct concern:

- **Prompt injection** — Adversarial input that hijacks model behavior
- **Jailbreaking** — Bypassing safety training
- **Data leakage** — Extracting training data or system prompts
- **Defense techniques** — Instruction hierarchy, sandwich defense, input filtering

---

## Implications for Practitioners

### Recommended Starting Points by Task

| Task | Start With | Level Up |
|------|-----------|----------|
| Classification | Zero-Shot + Output Format | Few-Shot + Self-Consistency |
| Math/Logic | Zero-Shot CoT | Few-Shot CoT + Self-Consistency |
| Writing | Role Prompting | Role + SoT + Self-Refine |
| Code | Plan-and-Solve + PoT | + Self-Refine + Checklist |
| Research | Step-Back + CoT | + CoVe + Self-Refine |
| Agent tasks | ReAct | + Memory + Reflexion |
| RAG QA | Context Stuffing | + CoN + CRAG + Self-RAG |

### The Principle of Minimum Effective Technique

The paper implicitly supports a key principle: **always start with the simplest technique that might work, and add complexity only when measurement shows it's needed.** This aligns with the HRM Methodology's approach of providing both simple starting points and full playbook pipelines.

---

## Relationship to HRM Methodology

The HRM Methodology extends the Prompt Report in several ways:

| Prompt Report | HRM Methodology |
|--------------|-----------------|
| Catalogs techniques | Adds machine-readable YAML metadata |
| Describes compositions | Provides executable playbook pipelines |
| Academic focus | Practitioner and agent focus |
| Static survey | Living repository with templates |
| Classification | Decision trees for technique selection |
| Individual techniques | End-to-end workflow integration |

The Prompt Report's taxonomy was the primary inspiration for the HRM Methodology's 75-technique catalog, extended with additional techniques from Sahoo et al. (2024), Liu et al. (2023), and practitioner experience.
