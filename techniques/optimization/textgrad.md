---
id: textgrad
name: "TextGrad"
aliases: ["Text-Based Gradient Descent", "Textual Backpropagation"]
category: optimization
family: gradient-optimization
year: 2024
authors: ["Mert Yuksekgonul", "Federico Bianchi", "Joseph Boen", "Sheng Liu", "Zhi Huang", "Carlos Guestrin", "James Zou"]
paper: "https://arxiv.org/abs/2406.07496"
paper_title: "TextGrad: Automatic 'Differentiation' via Text"
venue: "arXiv 2024"
code: "https://github.com/zou-group/textgrad"

complexity: high
token_cost: high
latency: high
num_calls: variable

requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["compound AI system optimization", "multi-component pipeline tuning", "code generation improvement", "prompt + response co-optimization"]
avoid_when: ["simple single-prompt tasks", "no clear loss function", "budget-constrained settings", "tasks without iterative refinement potential"]
composes_with: ["chain-of-thought", "react", "dspy", "self-refine"]

tags: ["optimization", "gradient", "backpropagation", "compound-ai", "iterative", "textual-feedback"]
---

# TextGrad

> **One-line summary:** TextGrad performs automatic differentiation over compound AI systems using natural language feedback as textual gradients, enabling backpropagation-style optimization of prompts, responses, and code.

## Overview

TextGrad is an optimization framework that draws a direct analogy to backpropagation in neural networks, but operates entirely in the space of natural language. In a compound AI system with multiple LLM calls (or a mix of LLM calls and code), TextGrad treats each component as a differentiable function and propagates textual "gradients" -- natural language critiques -- backward through the computation graph. Each variable (prompt, intermediate response, code) is updated based on this textual feedback.

The key insight is that LLMs can serve as both the computation engine and the gradient engine. Just as numerical gradients indicate how to adjust weights to reduce loss, textual gradients describe how to modify text to improve performance. An LLM acting as the "backward engine" reads the loss/critique and each intermediate output, then generates specific, actionable feedback for improvement. This feedback is then used to update the text variables in a gradient descent-like loop.

TextGrad has demonstrated strong results across diverse applications: optimizing prompts for question answering, improving LLM-generated code solutions, refining molecular designs, and enhancing radiotherapy treatment plans. The framework provides a PyTorch-like API (`Variable`, `Loss`, `backward()`, `step()`) that makes it intuitive for ML practitioners to adopt.

## How It Works

1. **Define Computation Graph:** Model the system as a directed acyclic graph where nodes are text variables (prompts, responses, code) and edges represent LLM calls or function transformations.
2. **Forward Pass:** Execute the pipeline, recording each input-output relationship. The final output is evaluated against a loss function (which can itself be an LLM judge).
3. **Backward Pass:** Starting from the loss, the backward engine (an LLM) generates textual gradients -- natural language critiques explaining what went wrong and how each variable contributed to the error.
4. **Propagate Gradients:** Textual gradients are propagated backward through each node. At each step, the LLM considers the upstream gradient, the local computation, and generates a gradient for the next variable upstream.
5. **Update Variables:** Each text variable is updated by an optimizer (e.g., TextualGradientDescent) that reads the variable's current value and its accumulated textual gradient, then generates an improved version.
6. **Iterate:** Repeat forward-backward-update for multiple steps until convergence or budget exhaustion.

### Diagram

```
Forward Pass:
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │  System   │ ──→ │  LLM     │ ──→ │  LLM     │ ──→ Output
  │  Prompt   │     │  Call 1   │     │  Call 2   │
  └──────────┘     └──────────┘     └──────────┘
                                                      │
                                                      ▼
                                               ┌──────────┐
                                               │   Loss   │
                                               │  (Judge) │
                                               └────┬─────┘
Backward Pass:                                      │
  ┌──────────┐     ┌──────────┐     ┌──────────┐   │
  │ ∇ Prompt │ ←── │ ∇ Call 1 │ ←── │ ∇ Call 2 │ ←─┘
  │ "Make    │     │ "The     │     │ "Output  │
  │  prompt  │     │  first   │     │  missed  │
  │  more    │     │  step    │     │  edge    │
  │  specific│     │  should  │     │  case X" │
  │  about Y"│     │  clarify │     │          │
  └──────────┘     │  Z"      │     └──────────┘
                   └──────────┘

Update Step:
  Prompt_new = Optimizer(Prompt_old, ∇ Prompt)
```

## Template

```python
import textgrad as tg

# 1. Set up engines
tg.set_backward_engine("gpt-4o")

# 2. Define variables
system_prompt = tg.Variable(
    "{initial_system_prompt}",
    role_description="system prompt for {task_description}",
    requires_grad=True
)

# 3. Define forward pass
model = tg.BlackboxLLM("gpt-4o-mini")

def forward(input_text):
    query = tg.Variable(input_text, role_description="user query")
    response = model(system_prompt, query)
    return response

# 4. Define loss function
loss_fn = tg.TextLoss(
    "Evaluate whether the response {evaluation_criteria}. "
    "Provide specific, actionable feedback for improvement."
)

# 5. Optimizer
optimizer = tg.TGD(parameters=[system_prompt], lr="{learning_rate_description}")

# 6. Training loop
for step in range({num_steps}):
    response = forward("{sample_input}")
    loss = loss_fn(response)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

## Examples

### Example 1: Optimizing a QA System Prompt

**Input:**
```python
import textgrad as tg

tg.set_backward_engine("gpt-4o")

system_prompt = tg.Variable(
    "Answer the question.",
    role_description="system prompt for a QA system",
    requires_grad=True
)

model = tg.BlackboxLLM("gpt-4o-mini")

loss_fn = tg.TextLoss(
    "Evaluate if the response is accurate, complete, and well-structured. "
    "Provide specific feedback on what could be improved."
)

optimizer = tg.TGD(parameters=[system_prompt])

for step in range(5):
    question = tg.Variable(train_questions[step], role_description="user question")
    response = model(system_prompt, question)
    loss = loss_fn(response)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

**Output:**
```
Step 0 prompt: "Answer the question."
Step 0 gradient: "The prompt is too vague. It should instruct the model
to provide structured, evidence-based answers with clear reasoning."

Step 5 prompt: "You are a knowledgeable assistant. Answer the question
accurately and completely. Structure your response with: (1) a direct
answer, (2) supporting explanation, (3) any important caveats. If
uncertain, state your confidence level."

Accuracy: 64% → 79% after 5 optimization steps.
```

### Example 2: Improving Code Solutions

**Input:**
```python
code_solution = tg.Variable(
    initial_code,
    role_description="Python solution to a LeetCode problem",
    requires_grad=True
)

test_engine = tg.BlackboxLLM("gpt-4o")

loss_fn = tg.TextLoss(
    "Run the code mentally against these test cases and identify any bugs, "
    "edge cases, or inefficiencies. Be specific about what to change."
)

optimizer = tg.TGD(parameters=[code_solution])

for step in range(3):
    loss = loss_fn(code_solution)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

**Output:**
```
Step 0 code: [initial solution with off-by-one error]
Step 0 gradient: "The loop boundary should be range(len(arr)-1) instead
of range(len(arr)) to avoid index out of bounds. Also, the base case
for empty input is missing."

Step 3 code: [corrected solution passing all test cases]
LeetCode pass rate: 45% → 82% after 3 optimization steps.
```

## When to Use

- You have a compound AI system with multiple LLM calls that need joint optimization
- You want to iteratively refine prompts, responses, or generated code with natural language feedback
- The system has a clear evaluation criterion that can be expressed as an LLM judge
- You need to trace errors in multi-step pipelines back to their root cause
- You are comfortable with a PyTorch-like optimization workflow

## When to Avoid

- The task involves a single, simple prompt with no multi-step computation
- No clear evaluation criterion or loss function can be defined
- Token budget is limited, as each optimization step requires multiple LLM calls
- The system does not benefit from iterative refinement (e.g., one-shot retrieval)
- You need deterministic, reproducible optimization (TextGrad is stochastic)

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead per step | High | Forward pass + backward engine + optimizer calls |
| Typical optimization steps | 3-10 | Often converges quickly |
| Backward engine cost | ~2x forward | Gradient generation is verbose |
| Quality gain | +10-35% | Largest gains on code and multi-step tasks |
| Total optimization cost | 10-50x single run | Amortized over improved performance |

## Variants

- **TextGrad with Beam Search:** Maintain multiple candidate updates per variable and select the best, reducing variance in optimization.
- **TextGrad with Constraints:** Add constraints to the optimizer (e.g., "keep the prompt under 100 words") to control the optimization trajectory.
- **Momentum TextGrad:** Accumulate textual gradients over multiple steps to identify persistent issues, analogous to momentum in SGD.
- **Multi-Objective TextGrad:** Use multiple loss functions (accuracy, safety, conciseness) and combine their textual gradients.

## Composability

- **TextGrad + DSPy:** Use TextGrad as an optimizer within DSPy modules to refine individual component prompts.
- **TextGrad + ReAct:** Optimize the system prompt and tool descriptions in a ReAct agent through textual gradient feedback.
- **TextGrad + Chain-of-Thought:** Refine CoT prompts by propagating gradients from answer quality back through reasoning steps.
- **TextGrad + Self-Refine:** TextGrad generalizes self-refine to multi-component systems with backpropagation through the full computation graph.

## Limitations

- High computational cost: each optimization step requires multiple LLM calls for forward, backward, and update
- Textual gradients can be noisy or contradictory, especially for complex systems
- No convergence guarantees; optimization may oscillate or degrade
- Requires a strong backward engine (typically GPT-4-class) for high-quality gradient generation
- The analogy to numerical gradients is approximate; textual "gradients" do not have the mathematical properties of true gradients
- Currently best suited for offline optimization, not real-time adaptation

## Sources

- **Primary:** [TextGrad: Automatic "Differentiation" via Text](https://arxiv.org/abs/2406.07496) — Yuksekgonul et al., 2024
- **Code:** [zou-group/textgrad](https://github.com/zou-group/textgrad) — Official repository
- **Related:** [ProTeGi: Automatic Prompt Optimization](https://arxiv.org/abs/2305.03495) — Pryzant et al., 2023
- **Related:** [DSPy](https://arxiv.org/abs/2310.03714) — Khattab et al., 2023
