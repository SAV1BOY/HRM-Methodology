---
id: self-consistency
name: "Self-Consistency"
aliases:
  - SC
  - self-consistency decoding
  - majority voting CoT
  - CoT-SC
category: reasoning
family: thought-generation
year: 2022
authors:
  - Xuezhi Wang
  - Jason Wei
  - Dale Schuurmans
  - Quoc V. Le
  - Ed Chi
  - Sharan Narang
  - Aakanksha Chowdhery
  - Denny Zhou
paper: "https://arxiv.org/abs/2203.11171"
paper_title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
venue: "ICLR 2023"
code: null
complexity: medium
token_cost: high
latency: high
num_calls: 5-40
requires_examples: true
requires_tools: false
requires_training: false
model_agnostic: true
best_for:
  - arithmetic reasoning requiring high accuracy
  - commonsense reasoning with ambiguous paths
  - symbolic reasoning tasks
  - any task where a single CoT chain is unreliable
  - competition-level math problems
  - reducing variance in model outputs
avoid_when:
  - token budget is severely constrained
  - latency requirements are strict and parallelism is unavailable
  - task has open-ended or free-form answers
  - the answer space is continuous rather than discrete
  - single CoT already achieves near-perfect accuracy
composes_with:
  - chain-of-thought
  - zero-shot-cot
  - least-to-most
  - plan-and-solve
  - tree-of-thoughts
tags:
  - foundational
  - reasoning
  - ensemble
  - sampling
  - majority-vote
  - robustness
---

# Self-Consistency

> **One-line summary:** Sample multiple chain-of-thought reasoning paths from the model, then select the most common final answer by majority vote to dramatically improve accuracy.

## Overview

Self-Consistency (SC), introduced by Wang et al. (2022), is a decoding strategy that exploits a fundamental intuition: complex reasoning problems often admit multiple valid reasoning paths that all converge on the correct answer, while incorrect answers arise from diverse, non-convergent errors. By sampling multiple chain-of-thought responses and taking a majority vote over the final answers, self-consistency filters out the noise of individual reasoning chains and surfaces the most robust answer.

The method builds directly on Chain-of-Thought prompting but replaces greedy decoding (which produces a single deterministic chain) with stochastic sampling at a nonzero temperature. Each sample generates a potentially different reasoning path and potentially different final answer. The key observation is that the correct answer tends to be over-represented among the samples because there are more valid reasoning paths leading to it, while incorrect answers scatter across different wrong conclusions. This makes majority voting a powerful error-correction mechanism that requires no additional training, verifiers, or reward models.

Self-Consistency delivered striking improvements across benchmarks: on GSM8K, it pushed PaLM 540B + CoT from 56.9% to 74.4% (with 40 samples), and on ARC-Challenge from 85.2% to 88.7%. The technique works with any chain-of-thought prompt (few-shot or zero-shot) and any language model that supports temperature-based sampling. Its primary cost is computational: generating N samples multiplies the inference cost proportionally. However, the samples are embarrassingly parallel and can be generated concurrently, meaning latency need not scale linearly with sample count in production settings. In practice, N=5 to N=20 captures most of the gains, with diminishing returns beyond N=40.

## How It Works

1. **Construct a CoT prompt**: Use either few-shot Chain-of-Thought or Zero-Shot CoT as the base prompt for the reasoning task.
2. **Sample multiple outputs**: Generate N reasoning chains by sampling from the model with temperature > 0 (typically T=0.5 to T=0.7). Each sample produces a complete reasoning chain and a final answer.
3. **Extract final answers**: Parse the final answer from each of the N generated reasoning chains using a consistent extraction pattern.
4. **Majority vote**: Count the frequency of each distinct answer across all N samples and select the answer that appears most often.
5. **Return the winner**: Output the most frequent answer as the final result. Optionally, report the vote distribution as a confidence signal.

### Diagram

```
                         CoT Prompt + Question
                                 |
              +------------------+------------------+
              |                  |                   |
              v                  v                   v
     +-------------+   +-------------+    +-------------+
     |  Sample 1   |   |  Sample 2   |    |  Sample N   |
     |             |   |             |    |             |
     | Chain: ...  |   | Chain: ...  |    | Chain: ...  |
     | Answer: 42  |   | Answer: 42  |    | Answer: 38  |
     +------+------+   +------+------+    +------+------+
            |                 |                   |
            +-----------+-----+-------------------+
                        |
                   +----v-----+
                   | MAJORITY |
                   |  VOTE    |
                   |          |
                   | 42: 7/10 |
                   | 38: 2/10 |
                   | 45: 1/10 |
                   +----+-----+
                        |
                   Answer: 42
```

## Template

```
# Base prompt (few-shot CoT or zero-shot CoT)
{cot_prompt_with_exemplars}

Q: {test_question}
A: Let's think step by step.
```

**Sampling Configuration:**
```
num_samples: {n}          # Typically 5-40
temperature: {temp}        # Typically 0.5-1.0
top_p: {top_p}            # Optional, e.g., 0.95
```

**Aggregation (Python pseudocode):**
```python
from collections import Counter

answers = [extract_answer(sample) for sample in samples]
majority_answer = Counter(answers).most_common(1)[0][0]
confidence = Counter(answers).most_common(1)[0][1] / len(answers)
```

## Examples

### Example 1: Arithmetic Reasoning (GSM8K-style)

**Prompt (sent N=5 times with temperature=0.7):**
```
Q: Beth bakes 4 batches of cookies with 12 cookies per batch. She eats
3 cookies and gives 2 to each of her 5 friends. How many cookies does
Beth have left?

A: Let's think step by step.
```

**Sample outputs:**
```
Sample 1: Beth bakes 4 * 12 = 48 cookies. She eats 3, leaving
          48 - 3 = 45. She gives 2 * 5 = 10 away. 45 - 10 = 35.
          The answer is 35.

Sample 2: Total cookies: 4 * 12 = 48. Beth eats 3: 48 - 3 = 45.
          She gives away 2 * 5 = 10 cookies. 45 - 10 = 35.
          The answer is 35.

Sample 3: 4 * 12 = 48 cookies total. She eats 3 and gives 10 away.
          Total removed: 3 + 10 = 13. 48 - 13 = 35.
          The answer is 35.

Sample 4: Beth bakes 48 cookies. She gives 2 to 5 friends = 10.
          She also eats 3. So she loses 10 + 3 = 13. 48 - 13 = 35.
          The answer is 35.

Sample 5: Beth makes 4 * 12 = 48. She eats 3 = 45 left. She gives
          2 to 5 friends = 10 given away. 45 - 10 = 35.
          The answer is 35.
```

**Majority Vote:** 35 (5/5 = 100% confidence)

### Example 2: Multi-Hop with Disagreement

**Prompt (sent N=7 times with temperature=0.8):**
```
Q: A farmer has 17 sheep. All but 9 die. How many sheep does the
farmer have left?

A: Let's think step by step.
```

**Sample outputs:**
```
Sample 1: "All but 9 die" means 9 survive.          Answer: 9
Sample 2: 17 - 9 = 8 die. 9 are left.               Answer: 9
Sample 3: "All but 9" = 17 - 9 = 8 died. 9 remain.  Answer: 9
Sample 4: All but 9 die means 17 - 9 = 8 sheep die.  Answer: 9
Sample 5: 17 sheep minus those that died. All but 9,
          so 17 - 9 = 8 died. Left: 9.               Answer: 9
Sample 6: "All but 9 die." 17 - 9 = 8 died, 9 left.  Answer: 9
Sample 7: All but 9 = 9 survived.                     Answer: 9
```

**Majority Vote:** 9 (7/7 = 100% confidence, unanimous agreement)

## When to Use

- The task has a discrete, verifiable answer (a number, a multiple-choice option, yes/no, a named entity).
- Reasoning accuracy is paramount and justifies higher compute costs.
- You observe high variance in model outputs for the same question across different runs.
- The base CoT approach gets the right answer some of the time but not reliably.
- You have access to parallel inference infrastructure to mitigate latency.
- You want a confidence signal: the degree of agreement among samples indicates answer reliability.

## When to Avoid

- The task requires open-ended, creative, or free-form text generation where majority voting is not meaningful.
- Budget constraints prohibit 5-40x cost multiplication.
- Latency requirements are strict and you lack parallel inference capability.
- The answer space is continuous (e.g., regression) rather than discrete.
- The base CoT consistently produces the same wrong answer due to systematic bias; voting over wrong answers does not help.
- You need the reasoning trace itself, not just the final answer.

## Cost & Performance

| Dimension          | Rating   | Notes                                             |
|--------------------|----------|---------------------------------------------------|
| Token overhead     | High     | N * (prompt + generation) tokens                   |
| Latency            | High     | N calls; parallelizable to ~1x with infra          |
| Accuracy gain      | High     | +5-18% over single CoT on reasoning benchmarks     |
| Implementation     | Low      | Sampling + parsing + counting; trivial engineering  |
| Model requirements | Large    | Same scale requirements as CoT (100B+)              |
| Diminishing returns| N>20     | Most gains captured by N=10-20                      |

## Variants

- **Weighted Self-Consistency**: Weight each sample's vote by the model's confidence (e.g., log-probability of the answer tokens) rather than equal voting.
- **Universal Self-Consistency (USC)**: For free-form answers where exact matching is insufficient, use an LLM to identify the majority answer among diverse phrasings.
- **Progressive Self-Consistency**: Start with few samples and add more only if the vote margin is narrow, reducing average cost while maintaining accuracy.
- **Self-Consistency with Diverse Prompts**: Use different prompt variants (not just different samples from the same prompt) to increase reasoning diversity.
- **Complexity-Weighted SC**: Give more weight to samples with longer, more complex reasoning chains, which tend to be more accurate on harder problems.

## Composability

Self-Consistency is fundamentally an aggregation layer and composes with any technique that produces discrete answers:

- **CoT + Self-Consistency**: The canonical combination. Few-shot CoT provides the reasoning format; SC provides robustness through voting. See `chain-of-thought.md`.
- **Zero-Shot CoT + Self-Consistency**: Achieves strong results without any exemplars by combining the simplicity of zero-shot CoT with the robustness of voting. See `zero-shot-cot.md`.
- **Least-to-Most + Self-Consistency**: Apply SC at each sub-problem level or at the final answer level to improve decomposition-based reasoning. See `least-to-most.md`.
- **Plan-and-Solve + Self-Consistency**: Sample multiple PS+ reasoning chains and vote. The structured planning reduces variance across samples. See `plan-and-solve.md`.
- **Tree-of-Thoughts + Self-Consistency**: SC can be viewed as a simplified flat version of ToT. Alternatively, SC can be used at the leaf evaluation step within ToT. See `tree-of-thoughts.md`.

## Limitations

- **Cost scaling**: The primary limitation is linear cost scaling with sample count N. For large prompts and many questions, this can be prohibitive.
- **Diminishing returns**: Accuracy improvements plateau beyond a certain N (typically 10-20 samples). Very high N values waste compute.
- **Answer extraction brittleness**: Majority voting requires reliable answer extraction. If the model's answer format is inconsistent, parsing failures can skew votes.
- **Not helpful for systematic errors**: If the model consistently makes the same mistake (e.g., a knowledge gap or consistent misapplication of a formula), SC will amplify that error through majority voting.
- **Inapplicable to generation tasks**: Creative writing, summarization, and other open-ended tasks do not have discrete answers amenable to voting.
- **No trace selection**: Standard SC returns only the majority answer, discarding all reasoning traces. The "best" reasoning chain is lost unless you add a trace-selection step.

## Sources

- Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models. *ICLR 2023*. https://arxiv.org/abs/2203.11171
- Chen, X., Aksitov, R., Alon, U., Ren, J., Xiao, K., Yin, P., Prakash, S., Sutton, C., Wang, X., & Zhou, D. (2023). Universal Self-Consistency for Large Language Model Generation. https://arxiv.org/abs/2311.17311
- Fu, Y., Peng, H., Sabharwal, A., Clark, P., & Khot, T. (2023). Complexity-Based Prompting for Multi-Step Reasoning. *ICLR 2023*. https://arxiv.org/abs/2210.00720
