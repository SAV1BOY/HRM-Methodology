---
id: dspy
name: "DSPy: Declarative Self-improving Language Programs"
aliases: ["DSPy", "Demonstrate-Search-Predict", "dspy-framework"]
category: optimization
family: compiler-optimization
year: 2023
authors: ["Omar Khattab", "Arnav Singhvi", "Paridhi Maheshwari", "Zhiyuan Zhang", "Keshav Santhanam", "Sri Vardhamanan", "Saiful Haq", "Ashutosh Sharma", "Thomas T. Joshi", "Hanna Moazam", "Heather Miller", "Matei Zaharia", "Christopher Potts"]
paper: "https://arxiv.org/abs/2310.03714"
paper_title: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
venue: "ICLR 2024"
code: "https://github.com/stanfordnlp/dspy"
complexity: high
token_cost: high
latency: high
num_calls: variable
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for: ["multi-step pipelines", "prompt optimization at scale", "reproducible LLM systems", "RAG pipeline tuning", "complex reasoning chains"]
avoid_when: ["single-shot simple tasks", "no labeled data available", "rapid prototyping without evaluation", "extremely low budget"]
composes_with: ["chain-of-thought", "react", "retrieval-augmented-generation", "self-consistency"]
tags: ["optimization", "compiler", "declarative", "pipeline", "few-shot", "automatic-prompting"]
---

# DSPy: Declarative Self-improving Language Programs

> **One-line summary:** A programming framework that replaces hand-crafted prompts with declarative modules and compiles them into optimized pipelines using teleprompters (optimizers).

## Overview

DSPy fundamentally rethinks how developers interact with language models. Instead of writing brittle prompt strings, developers define **signatures** (input-output specifications) and compose them into **modules** (ChainOfThought, ReAct, ProgramOfThought, etc.). A **compiler** (optimizer/teleprompter) then automatically generates effective prompts, selects few-shot demonstrations, or fine-tunes weights to maximize a user-defined metric on a development set.

The key insight is separating the *what* (the task logic expressed as modules and signatures) from the *how* (the specific prompt text and demonstrations that make a particular LLM perform well). This mirrors the compiler paradigm in traditional software engineering: write high-level code, let the compiler handle low-level optimization. DSPy supports multiple optimization strategies including BootstrapFewShot, BootstrapFewShotWithRandomSearch, MIPRO (Multi-prompt Instruction Proposal Optimizer), and COPRO.

DSPy has rapidly become one of the most popular frameworks for building compound AI systems, with a growing ecosystem of integrations. It supports all major LLM providers and can optimize both prompts (for API-based models) and weights (for open-source models via fine-tuning). The framework encourages a systematic, metrics-driven approach to prompt engineering that scales far beyond manual iteration.

## How It Works

1. **Define Signatures**: Specify input and output fields for each step of your pipeline using `dspy.Signature` classes or shorthand string notation (e.g., `"question -> answer"`).

2. **Build Modules**: Compose signatures into modules like `dspy.ChainOfThought`, `dspy.ReAct`, `dspy.ProgramOfThought`, or custom modules that chain multiple calls together.

3. **Assemble Program**: Combine modules into a complete program (a Python class inheriting from `dspy.Module`) with a `forward()` method that defines the data flow.

4. **Define Metric**: Write a metric function that scores program outputs on a development set (e.g., accuracy, F1, human preference scores).

5. **Compile with Optimizer**: Select a teleprompter/optimizer (e.g., `BootstrapFewShot`, `MIPRO`) and compile the program. The optimizer searches over demonstrations, instructions, and module configurations.

6. **Evaluate and Iterate**: Run the compiled program on held-out test data. If needed, iterate on the program structure or metric definition and recompile.

### Diagram

```
 Developer Defines:                    DSPy Compiles:
 +-----------------+                  +------------------+
 | Signatures      |                  | Optimized Prompts|
 | (I/O specs)     |---+             | (instructions +  |
 +-----------------+   |             | few-shot demos)  |
                       v             +------------------+
 +-----------------+  +----------+          ^
 | Modules         |->| Program  |--[Optimizer]--+
 | (CoT, ReAct...) |  | (forward)|          |
 +-----------------+  +----------+          |
                       |                    |
 +-----------------+   |   +-----------+    |
 | Metric Function |---+-->| Dev Set   |----+
 | (scoring)       |       | (examples)|
 +-----------------+       +-----------+
```

## Template

```python
import dspy

# Step 1: Configure the language model
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

# Step 2: Define signatures
class GenerateAnswer(dspy.Signature):
    """Answer questions with detailed reasoning."""
    context = dspy.InputField(desc="relevant context passages")
    question = dspy.InputField(desc="the question to answer")
    answer = dspy.OutputField(desc="a detailed, accurate answer")

# Step 3: Build the program
class RAGPipeline(dspy.Module):
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        answer = self.generate(context=context, question=question)
        return answer

# Step 4: Define metric
def answer_accuracy(example, prediction, trace=None):
    return dspy.evaluate.answer_exact_match(example, prediction)

# Step 5: Compile
optimizer = dspy.BootstrapFewShot(metric=answer_accuracy, max_bootstrapped_demos=4)
compiled_rag = optimizer.compile(RAGPipeline(), trainset={trainset})

# Step 6: Use the compiled program
result = compiled_rag(question="{user_question}")
```

## Examples

### Example 1: Optimizing a QA Pipeline

**Task**: Build an optimized question-answering system over a knowledge base.

```python
import dspy
from dspy.datasets import HotPotQA

dataset = HotPotQA(train_seed=1, eval_seed=2023, test_size=500)
trainset = [x.with_inputs('question') for x in dataset.train[:200]]
devset = [x.with_inputs('question') for x in dataset.dev[:500]]

class MultiHopQA(dspy.Module):
    def __init__(self):
        self.generate_query = dspy.ChainOfThought("question -> search_query")
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        query = self.generate_query(question=question).search_query
        context = dspy.Retrieve(k=3)(query).passages
        return self.generate_answer(context=context, question=question)

optimizer = dspy.MIPROv2(metric=dspy.evaluate.answer_exact_match, num_candidates=10)
optimized_qa = optimizer.compile(MultiHopQA(), trainset=trainset)

# Result: MIPRO discovers optimized instructions and selects 4 bootstrapped
# demonstrations, improving accuracy from 34% to 51% on HotPotQA.
```

### Example 2: Optimizing a Classification Pipeline

**Task**: Sentiment classification with automatic prompt optimization.

```python
import dspy

class SentimentClassifier(dspy.Signature):
    """Classify the sentiment of a product review."""
    review = dspy.InputField(desc="a product review text")
    sentiment = dspy.OutputField(desc="positive, negative, or neutral")

classify = dspy.Predict(SentimentClassifier)

trainset = [
    dspy.Example(review="This product is amazing!", sentiment="positive").with_inputs("review"),
    dspy.Example(review="Terrible quality, broke immediately.", sentiment="negative").with_inputs("review"),
    # ... more training examples
]

optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=lambda ex, pred, trace=None: ex.sentiment == pred.sentiment,
    max_bootstrapped_demos=3,
    num_candidate_programs=10
)
optimized_classifier = optimizer.compile(classify, trainset=trainset)

# The optimizer selects the most informative demonstrations and can
# improve accuracy from ~82% to ~91% on the dev set.
```

## When to Use

- You have a multi-step LLM pipeline with clear evaluation metrics
- You want to systematically optimize prompts rather than guess
- Your pipeline needs to work across different LLM backends
- You have at least a small labeled development set (50+ examples)
- You want reproducible, version-controlled prompt optimization

## When to Avoid

- Quick one-off tasks where manual prompting suffices
- No evaluation data or metrics are available
- The task is simple enough that a single well-crafted prompt works
- You need the lowest possible latency (compilation overhead is high)
- Your team is unfamiliar with Python-based ML workflows

## Cost & Performance

| Dimension         | Value                    | Notes                                          |
|--------------------|--------------------------|-------------------------------------------------|
| Compilation cost   | High (hundreds of calls) | Depends on optimizer and search budget           |
| Inference cost     | Low-Medium               | Compiled prompts add few-shot demos (more tokens)|
| Accuracy gain      | +5-25% typical           | Varies by task, model, and baseline              |
| Setup time         | 2-8 hours                | Define signatures, metrics, gather dev data      |
| Maintenance        | Low after compilation    | Recompile when task or model changes             |

## Variants

- **BootstrapFewShot**: Simplest optimizer; bootstraps demonstrations by running the program and selecting successful traces.
- **BootstrapFewShotWithRandomSearch**: Adds random search over demo combinations for better coverage.
- **MIPRO (Multi-prompt Instruction Proposal Optimizer)**: Jointly optimizes instructions and demonstrations using Bayesian optimization.
- **COPRO**: Coordinate-wise prompt optimization that tunes each module's instruction independently.
- **Assertions**: Add `dspy.Assert` and `dspy.Suggest` constraints to guide program behavior during compilation.

## Composability

DSPy modules naturally compose with each other and with external tools:
- **ChainOfThought + Retrieve**: Standard RAG pattern
- **ReAct + Tools**: Agent-style reasoning with external tool use
- **Ensemble**: Combine multiple compiled programs for self-consistency
- **Fine-tuning**: Use compiled prompts as training data for model distillation

## Limitations

- Requires a labeled development set with a clear metric -- not always available
- Compilation can be expensive (hundreds to thousands of LLM calls)
- Debugging compiled prompts can be opaque -- the "why" behind selected demos is unclear
- Framework lock-in: programs are tied to the DSPy API
- Optimized prompts may not transfer well across model families
- Learning curve is steep for teams without ML engineering experience

## Sources

- Khattab, O. et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." *arXiv:2310.03714*. https://arxiv.org/abs/2310.03714
- Opsahl-Ong, K. et al. (2024). "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs." *arXiv:2406.11695*.
- DSPy GitHub Repository: https://github.com/stanfordnlp/dspy
- DSPy Documentation: https://dspy-docs.vercel.app/
