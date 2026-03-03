---
id: program-of-thoughts
name: "Program of Thoughts"
aliases:
  - PoT
  - Program-aided Language Model
  - PAL
category: reasoning
family: thought-generation
year: 2022
authors:
  - Wenhu Chen
  - Xueguang Ma
  - Xinyi Wang
  - William W. Cohen
paper: "https://arxiv.org/abs/2211.12588"
paper_title: "Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks"
venue: "TMLR 2023"
code: "https://github.com/wenhuchen/Program-of-Thoughts"
complexity: medium
token_cost: medium
latency: medium
num_calls: 1
requires_examples: true
requires_tools: true
requires_training: false
model_agnostic: true
best_for:
  - mathematical reasoning
  - numerical computation
  - financial calculations
  - data table reasoning
  - multi-step arithmetic
  - combinatorial problems
  - iterative algorithms
avoid_when:
  - no code interpreter available
  - purely qualitative reasoning
  - common-sense or social reasoning
  - simple factual recall
  - domains requiring natural language explanations
composes_with:
  - chain-of-thought
  - self-consistency
  - retrieval-augmented-generation
  - few-shot-prompting
tags:
  - code-generation
  - numerical-reasoning
  - tool-use
  - computation
  - math
  - interpreter
---

# Program of Thoughts

> **One-line summary:** Disentangles reasoning from computation by having the LLM generate executable code instead of natural-language arithmetic, then running that code in an interpreter for exact answers.

## Overview

Program of Thoughts (PoT) prompting, introduced by Chen et al. (2022), addresses a fundamental weakness of chain-of-thought reasoning: language models are strong at semantic understanding and translating word problems into formal logic, but weak at precise multi-step arithmetic. When an LLM reasons entirely in natural language, it must simultaneously decide the logical steps and execute calculations -- conflating two very different cognitive demands. PoT separates these concerns cleanly: the model reasons about *what* to compute and expresses that reasoning as executable Python code, while a deterministic interpreter handles the actual computation.

The technique emerged alongside the concurrent PAL (Program-Aided Language Models) work by Gao et al. (2022), and both share the core idea of delegating computation to code. Where PoT distinguishes itself is in its emphasis on disentangling the reasoning trace from the computational trace. The generated code is not merely a calculation script; it is a structured reasoning artifact with semantically meaningful variable names and explanatory comments that serve as an interpretable chain of logic. This makes PoT outputs simultaneously machine-executable and human-readable.

Empirically, PoT achieves state-of-the-art results across multiple math reasoning benchmarks including GSM8K, AQuA, SVAMP, TabMWP, and FinQA, outperforming standard chain-of-thought by significant margins. The gains are especially pronounced on problems involving iterative computation, complex arithmetic with large numbers, operations over structured data like tables, and financial calculations requiring compound formulas. The requirement for a code interpreter is the main deployment constraint, but the growing availability of sandboxed execution environments in production LLM systems has made this increasingly practical.

## How It Works

1. **Problem reception**: The LLM receives the problem statement along with few-shot exemplars demonstrating the expected format -- each exemplar shows a word problem followed by a Python program that solves it.
2. **Semantic parsing**: The model analyzes the problem to identify the quantities, relationships, and operations needed, translating the natural-language description into a computational plan.
3. **Code generation**: Rather than producing a textual reasoning chain, the model generates a Python program. Variables are given semantically meaningful names (e.g., `quarterly_rate` instead of `x`), and inline comments explain the reasoning behind each step.
4. **Code execution**: The generated program is sent to a sandboxed Python interpreter. The interpreter runs the code deterministically and returns the computed result.
5. **Answer extraction**: The final answer is extracted from the program output, typically the last printed value or a designated `ans` variable.

### Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      Input Problem                            │
│  "Sarah invests $10,000 at 6% compounded quarterly           │
│   for 5 years. How much does she have?"                      │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                 LLM  (Code Generation)                        │
│                                                               │
│  # Initial investment                                         │
│  principal = 10000                                            │
│  annual_rate = 0.06                                           │
│  n = 4  # quarterly compounding                               │
│  years = 5                                                    │
│  amount = principal * (1 + annual_rate / n) ** (n * years)    │
│  ans = round(amount, 2)                                       │
│  print(ans)                                                   │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  Python Interpreter                            │
│                  >>> 13468.55                                  │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                Final Answer: $13,468.55                        │
└──────────────────────────────────────────────────────────────┘
```

## Template

```
Solve the following problem by writing a Python program. Use meaningful variable
names and add comments explaining your reasoning. Store the final answer in a
variable called `ans` and print it.

{few_shot_examples}

Question: {question}

# Python program to solve this problem
```

## Examples

### Example 1: Financial Calculation

**Input:**
```
Solve the following problem by writing a Python program. Use meaningful variable
names and add comments explaining your reasoning. Store the final answer in a
variable called `ans` and print it.

Question: A company offers a 15% discount on bulk orders over 100 units. The
base price is $24.50 per unit. A customer orders 250 units and must pay 8.5%
sales tax on the discounted total. Additionally, there is a flat $45 shipping
fee. What is the total cost?

# Python program to solve this problem
```

**Output:**
```python
# Base price per unit
base_price = 24.50

# Number of units ordered
units = 250

# Bulk discount rate (15% for orders over 100)
discount_rate = 0.15

# Calculate discounted price per unit
discounted_price = base_price * (1 - discount_rate)

# Subtotal before tax
subtotal = discounted_price * units

# Sales tax rate
tax_rate = 0.085

# Tax amount
tax = subtotal * tax_rate

# Flat shipping fee
shipping = 45.00

# Total cost = subtotal + tax + shipping
total = subtotal + tax + shipping
ans = round(total, 2)
print(ans)  # 5714.19
```

### Example 2: Combinatorial Problem

**Input:**
```
Solve the following problem by writing a Python program. Use meaningful variable
names and add comments explaining your reasoning. Store the final answer in a
variable called `ans` and print it.

Question: A password must be exactly 4 characters long. The first character must
be an uppercase letter, the second and third must be digits (0-9), and the last
must be a special character from the set {!, @, #, $, %}. How many distinct
passwords are possible?

# Python program to solve this problem
```

**Output:**
```python
# Number of choices for each position
uppercase_letters = 26    # A-Z
digits = 10               # 0-9 for each digit position
special_chars = 5         # {!, @, #, $, %}

# Total passwords = choices_1 * choices_2 * choices_3 * choices_4
# Position 1: uppercase letter
# Position 2: digit
# Position 3: digit
# Position 4: special character
total_passwords = uppercase_letters * digits * digits * special_chars

ans = total_passwords
print(ans)  # 13000
```

## When to Use

- Problems requiring multi-step arithmetic where natural-language computation errors accumulate significantly.
- Financial calculations involving compound interest, amortization, depreciation, or tax logic with precise decimal handling.
- Combinatorics and probability requiring factorial, combination, or permutation calculations.
- Data table operations that benefit from programmatic iteration over rows and columns.
- Any task where a deterministic computation engine improves reliability over LLM mental math.
- Problems involving date arithmetic, unit conversions, or iterative/recursive algorithms.
- Situations where the reasoning trace must be both human-readable and machine-verifiable.

## When to Avoid

- No code execution environment is available in the deployment pipeline.
- The task is purely qualitative (ethical reasoning, creative writing, sentiment analysis).
- Common-sense reasoning where the "computation" is social or intuitive rather than mathematical.
- Simple single-step problems where chain-of-thought or direct answering is sufficient.
- Domains where generating and executing arbitrary code poses unacceptable security risks.
- Problems requiring deep domain knowledge not expressible in simple Python constructs.

## Cost & Performance

| Metric               | Value                    | Notes                                          |
|----------------------|--------------------------|-------------------------------------------------|
| Token overhead       | ~1.2-1.5x vs CoT        | Code is often more concise than natural language |
| Latency              | Medium                   | One LLM call + interpreter execution             |
| Quality gain         | +8-15% on math benchmarks| Largest gains on multi-step arithmetic            |
| GSM8K accuracy       | ~92% (GPT-4)             | vs ~87% with standard CoT                        |
| FinQA accuracy       | +12% over CoT            | Financial domain benefits most                    |
| Interpreter cost     | Negligible               | Python execution is near-instant                  |
| Implementation cost  | Medium                   | Requires sandboxed execution environment          |

## Variants

- **PAL (Program-Aided Language Models):** Gao et al. 2022 -- concurrent work with the same core idea. Uses Python functions rather than scripts and emphasizes few-shot exemplar design with function-based decomposition.
- **MathCoder:** Extends PoT with interleaved natural language and code, letting the model alternate between textual explanation and computational blocks within a single response.
- **CSV-PoT / Table-PoT:** Specialized variant for tabular data where the generated code manipulates pandas DataFrames, enabling complex aggregation and filtering operations.
- **PoT + Self-Consistency:** Run multiple PoT generations and take the majority-voted answer from the executed outputs for improved reliability.
- **PoT + Self-Debug:** After initial code generation and execution, the model reviews its own code for bugs and iteratively corrects errors before finalizing the answer.

## Composability

- **PoT + Self-Consistency:** Generate multiple programs, execute each, and take the majority answer. Reduces variance from different valid code paths while maintaining computational exactness.
- **PoT + Retrieval-Augmented Generation:** Retrieve relevant formulas, API documentation, library references, or data schemas before generating code, grounding the program in accurate domain knowledge.
- **PoT + Chain-of-Thought:** Use CoT for the high-level planning phase to outline the approach in natural language, then switch to PoT for the computation phase.
- **PoT + Tool Use:** Extend beyond a bare Python interpreter to include web APIs, databases, scientific computing libraries (NumPy, SciPy), or domain-specific packages.
- **PoT + Least-to-Most:** Decompose the problem into sub-problems, generate and execute a small program for each sub-problem, then compose the results.

## Limitations

- Requires a sandboxed code execution environment, adding infrastructure complexity and potential security concerns.
- Generated code may contain subtle bugs that produce incorrect but plausible-looking answers, and unlike natural language errors, code bugs can be harder to spot without execution.
- Models may generate overly complex code when a simpler solution exists, especially without strong few-shot guidance.
- Few-shot exemplars must be carefully designed to set the right code style, variable naming conventions, and output format.
- Not effective for non-computational reasoning tasks; attempting to force code generation for qualitative questions produces awkward and unreliable results.
- Python-specific syntax and library knowledge varies across models; some models may hallucinate non-existent library functions.
- The technique assumes the problem has a well-defined computational solution, which excludes open-ended or ambiguous questions.

## Sources

- **Primary:** Chen, W., Ma, X., Wang, X., & Cohen, W. W. (2022). Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks. *TMLR 2023*. https://arxiv.org/abs/2211.12588
- **Related:** Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y., Callan, J., & Neubig, G. (2022). PAL: Program-Aided Language Models. *ICML 2023*. https://arxiv.org/abs/2211.10435
- **Survey:** Qiao, S., Ou, Y., Zhang, N., Chen, X., Yao, Y., Deng, S., Tan, C., Huang, F., & Chen, H. (2023). Reasoning with Language Model Prompting: A Survey. https://arxiv.org/abs/2312.11562
