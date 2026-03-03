---
id: self-refine
name: "Self-Refine"
aliases: ["Iterative Self-Refinement", "Generate-Critique-Refine"]
category: verification
family: verification
year: 2023
authors: ["Aman Madaan", "Niket Tandon", "Prakhar Gupta", "Skyler Hallinan", "Luyu Gao", "Sarah Wiegreffe", "Uri Alon", "Nouha Dziri", "Shrimai Prabhumoye", "Yiming Yang", "Shashank Gupta", "Bodhisattwa Prasad Majumder", "Katherine Hermann", "Sean Welleck", "Amir Yazdanbakhsh", "Peter Clark"]
paper: "https://arxiv.org/abs/2303.17651"
paper_title: "Self-Refine: Iterative Refinement with Self-Feedback"
venue: "NeurIPS 2023"
code: "https://github.com/madaan/self-refine"

complexity: medium
token_cost: high
latency: high
num_calls: variable

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["code generation", "mathematical reasoning", "dialogue response quality", "review and critique tasks", "any task with objectively evaluable output quality"]
avoid_when: ["simple factual lookups", "tasks where initial output is consistently sufficient", "extreme latency constraints", "when model cannot meaningfully critique its own output"]
composes_with: ["chain-of-thought", "few-shot-prompting", "chain-of-verification", "retrieval-augmented-generation"]

tags: ["iterative", "self-feedback", "refinement", "critique", "loop"]
---

# Self-Refine

> **One-line summary:** Self-Refine iteratively improves LLM outputs through a generate-critique-refine loop where the same model produces an initial draft, provides structured feedback on it, and then generates an improved version, repeating until quality criteria are met.

## Overview

Self-Refine operationalizes the natural human process of drafting, reviewing, and revising. Rather than relying on a single-shot generation, the technique introduces an iterative loop with three distinct phases: initial generation, self-critique (feedback), and refinement. The same LLM performs all three roles, but with different prompts that frame each phase distinctly. This separation of concerns helps the model identify weaknesses in its own output that it might not have caught during generation.

The approach was developed by Madaan et al. and demonstrated across a wide range of tasks including code optimization, mathematical reasoning, dialogue generation, and constrained text generation. A key finding is that even strong models like GPT-4 consistently improve through Self-Refine iterations, with most gains occurring in the first 2-3 iterations before plateauing. This suggests that the feedback mechanism surfaces genuine quality improvements rather than just random variation.

What makes Self-Refine particularly practical is its simplicity: it requires no additional training, no external feedback signals, and no multiple models. The entire process runs with a single LLM and well-crafted prompts for each phase. The main trade-off is latency and token cost, which scale linearly with the number of refinement iterations. For tasks where output quality is paramount and some additional latency is acceptable, Self-Refine offers a reliable and generalizable improvement strategy.

## How It Works

1. **Initial Generation:** The LLM generates a first-draft response to the task. This draft is treated as a starting point, not a final answer.

2. **Self-Critique (Feedback):** The draft is presented back to the LLM with a feedback prompt that asks it to identify specific weaknesses, errors, or areas for improvement. The critique should be actionable and specific, not vague.

3. **Refinement:** The original draft and the critique are presented to the LLM with a refinement prompt that asks it to produce an improved version addressing the identified issues.

4. **Iteration Check:** If the refined output meets a stopping criterion (e.g., quality threshold, maximum iterations, or the critique says "no further improvements needed"), the loop terminates. Otherwise, return to step 2 with the refined output as the new draft.

### Diagram

```
┌──────────────────────────────────────────────────────┐
│                 Self-Refine Loop                     │
│                                                      │
│  ┌──────────┐                                        │
│  │  Task     │                                        │
│  └─────┬────┘                                        │
│        v                                             │
│  ┌──────────────┐                                    │
│  │ GENERATE     │                                    │
│  │ (Initial     │<──────────────────────┐            │
│  │  Draft)      │                      │            │
│  └─────┬────────┘                      │            │
│        │                               │            │
│        v                               │            │
│  ┌──────────────┐     ┌──────────────┐ │            │
│  │ CRITIQUE     │────>│ Feedback:    │ │            │
│  │ (Self-       │     │ - Issue 1    │ │            │
│  │  Feedback)   │     │ - Issue 2    │ │            │
│  └──────────────┘     │ - Issue 3    │ │            │
│                       └──────┬───────┘ │            │
│                              │         │            │
│                              v         │            │
│                       ┌──────────────┐ │            │
│                       │ REFINE       │ │            │
│                       │ (Improved    │─┘            │
│                       │  Version)    │ (if not done)│
│                       └──────┬───────┘              │
│                              │                      │
│                              v (if done)            │
│                       ┌──────────────┐              │
│                       │ Final Output │              │
│                       └──────────────┘              │
└──────────────────────────────────────────────────────┘
```

## Template

```
--- STEP 1: GENERATE ---
{task_description}

Provide your initial response.

--- STEP 2: CRITIQUE ---
Review the following response to the task: "{task_description}"

Response to review:
{current_draft}

Provide specific, actionable feedback. For each issue:
- What is the problem?
- Why is it a problem?
- How should it be fixed?

If the response is already excellent with no meaningful improvements
possible, respond with "NO FURTHER IMPROVEMENTS NEEDED."

--- STEP 3: REFINE ---
Original task: {task_description}

Previous response:
{current_draft}

Feedback received:
{feedback}

Produce an improved version that addresses all feedback points.
Preserve what was already good and only change what needs improvement.
```

## Examples

### Example 1: Code Optimization

**Input (Generate):**
```
Write a Python function to find all prime numbers up to n.
```

**Output (Initial Draft):**
```python
def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
```

**Critique:**
```
Issues identified:
1. PERFORMANCE: The inner loop checks divisibility up to num-1, but only
   needs to check up to sqrt(num). This makes the function O(n^2) instead
   of O(n * sqrt(n)).
2. ALGORITHM: The Sieve of Eratosthenes would be significantly more
   efficient for finding all primes up to n, achieving O(n log log n).
3. EDGE CASES: No handling for n < 2 (should return empty list).
4. DOCUMENTATION: Missing docstring and type hints.
```

**Refined Output:**
```python
def find_primes(n: int) -> list[int]:
    """Find all prime numbers up to n using the Sieve of Eratosthenes.

    Args:
        n: Upper bound (inclusive) for prime search.

    Returns:
        List of all prime numbers from 2 to n.
    """
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]
```

### Example 2: Email Writing

**Input (Generate):**
```
Write a professional email declining a meeting invitation due to a
schedule conflict, but expressing interest in the topic.
```

**Output (Initial Draft):**
```
Subject: Re: Meeting Invitation

Hi,

I can't make the meeting. I have something else at that time. But the
topic sounds interesting. Can you send me the notes after?

Thanks
```

**Critique:**
```
Issues identified:
1. TONE: Too informal for a professional email. "I can't make" and
   "something else" are vague and casual.
2. STRUCTURE: Missing proper greeting with the recipient's name.
3. SPECIFICITY: Does not mention the specific meeting or date, nor
   suggest an alternative.
4. CLOSING: Missing proper sign-off and full name.
5. ENGAGEMENT: Asking for notes is passive; could offer to contribute
   asynchronously or suggest a follow-up.
```

**Refined Output:**
```
Subject: Re: Q2 Planning Meeting — Schedule Conflict

Dear Sarah,

Thank you for the invitation to the Q2 Planning Meeting on March 15th.
Unfortunately, I have a prior commitment at that time and will not be
able to attend.

I am genuinely interested in the topics on the agenda, particularly
the discussion around resource allocation. I would appreciate it if you
could share the meeting notes or recording afterward. I am also happy
to provide any input asynchronously before the meeting if that would
be helpful.

If there is a follow-up session or if you would like to discuss any of
the outcomes, I would welcome the opportunity to connect the following
week.

Best regards,
James Chen
```

## When to Use

- Code generation and optimization where correctness and quality can be incrementally improved
- Writing tasks where tone, clarity, and completeness benefit from revision
- Mathematical problem solving where the model can catch computational errors
- Any task with clear quality criteria that the model can evaluate against
- Situations where a first draft is "good but not great" and systematic improvement is valuable

## When to Avoid

- Simple factual lookups where the answer is either right or wrong with no room for refinement
- When initial model output is already consistently high quality for the task type
- Extreme latency constraints where multiple LLM calls are unacceptable
- Tasks where the model cannot meaningfully evaluate its own output (e.g., highly specialized domains)
- When the cost of multiple iterations outweighs the quality improvement

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 2-4x per iteration | Each iteration adds critique + refined output |
| Latency | 2-4x baseline | Typically 2-3 iterations before convergence |
| Quality gain | +5-25% | Varies by task; code and math see largest gains |
| Optimal iterations | 2-3 | Diminishing returns after 3 iterations |
| Convergence | Usually 2-3 rounds | Model says "no further improvements" |

## Variants

- **Self-Refine with Rubric:** Provide explicit evaluation criteria in the critique prompt to guide more targeted feedback.
- **Self-Refine with Examples:** Include few-shot examples of good feedback-refinement pairs to improve critique quality.
- **Multi-Aspect Self-Refine:** Separate critiques for different quality dimensions (correctness, style, completeness) to prevent tunnel vision.
- **Bounded Self-Refine:** Hard cap on iterations (e.g., max 3) to prevent infinite loops and control cost.

## Composability

- **Self-Refine + Chain-of-Thought:** Use CoT during the critique phase to reason through why specific aspects are problematic.
- **Self-Refine + RAG:** Retrieve relevant reference material during the critique phase to ground the feedback in authoritative sources.
- **Self-Refine + Chain-of-Verification:** Use CoVe to verify factual claims in each refined draft before accepting it.
- **Self-Refine + Few-Shot:** Provide examples of high-quality outputs to calibrate the critique's quality expectations.

## Limitations

- The model's ability to critique is bounded by its own capabilities: it cannot identify errors it does not understand
- Risk of "refinement loops" where the model alternates between two versions without converging
- Later iterations may degrade output quality by over-optimizing on superficial feedback
- Token cost scales linearly with iterations, which can be expensive for complex tasks
- The model may be too lenient in self-critique, failing to identify genuine issues
- On some tasks, the first-draft output is already near-optimal and refinement adds cost without benefit

## Sources

- **Primary:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Madaan et al., NeurIPS 2023
- **Code:** [github.com/madaan/self-refine](https://github.com/madaan/self-refine)
- **Related:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — Shinn et al., 2023
- **Related:** [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) — Bai et al., 2022
