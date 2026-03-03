---
id: reflexion
name: "Reflexion"
aliases: ["Self-Reflection", "Verbal Reinforcement Learning"]
category: verification
family: verification
year: 2023
authors: ["Noah Shinn", "Federico Cassano", "Ashwin Gopinath", "Karthik Narasimhan", "Shunyu Yao"]
paper: "https://arxiv.org/abs/2303.11366"
paper_title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
venue: "NeurIPS 2023"
code: "https://github.com/noahshinn/reflexion"

complexity: high
token_cost: very_high
latency: very_high
num_calls: variable

requires_examples: false
requires_tools: true
requires_training: false
model_agnostic: true

best_for: ["sequential decision-making tasks", "code generation with test feedback", "multi-step agent tasks", "tasks with binary success/failure signals", "interactive environments with observable outcomes"]
avoid_when: ["single-turn question answering", "tasks without clear success criteria", "latency-sensitive applications", "tasks where previous attempts provide no useful signal"]
composes_with: ["chain-of-thought", "react-prompting", "self-refine", "few-shot-prompting"]

tags: ["agent", "episodic-memory", "self-reflection", "verbal-rl", "iterative", "learning-from-failure"]
---

# Reflexion

> **One-line summary:** Reflexion enables LLM agents to learn from failed attempts by generating verbal self-reflections that are stored in episodic memory and used to improve subsequent tries, functioning as a form of verbal reinforcement learning.

## Overview

Reflexion introduces a paradigm for LLM agents to learn from their mistakes across multiple episodes without updating model weights. When an agent fails at a task, rather than simply retrying, it generates a verbal reflection analyzing what went wrong, why the approach failed, and what should be done differently. These reflections are stored in an episodic memory buffer and included in the prompt for subsequent attempts, giving the agent an accumulated "experience log" that guides improved strategies.

The technique draws inspiration from reinforcement learning but replaces numerical reward signals and gradient updates with natural language feedback and in-context learning. This "verbal RL" approach is particularly powerful because the reflections can capture nuanced strategic insights that are difficult to express as scalar rewards. For example, a reflection might note "I failed because I assumed the API returns sorted results, but it does not -- I should add an explicit sort step," which is far more informative than a simple failure signal.

Reflexion was demonstrated to be highly effective on coding tasks (HumanEval, MBPP), question answering (HotpotQA), and sequential decision-making (ALFWorld). On HumanEval, Reflexion achieved 91% pass@1, substantially outperforming the base GPT-4 model. The approach requires an environment that provides feedback (e.g., test results, task completion signals) and benefits most from tasks where the agent can make multiple attempts.

## How It Works

1. **Action (Trial):** The LLM agent attempts to solve the task, generating a sequence of actions or outputs. This might be writing code, navigating an environment, or answering a question.

2. **Evaluation:** The agent's output is evaluated against the task's success criteria. This could be running unit tests (code), checking answer correctness (QA), or verifying task completion (decision-making). A binary or graded signal is produced.

3. **Self-Reflection (on failure):** If the attempt fails, the agent is prompted to analyze the failure. It examines its actions, the feedback received, and generates a verbal reflection describing what went wrong and what to do differently. This reflection is stored in the episodic memory.

4. **Memory-Augmented Retry:** The agent makes another attempt, but now its prompt includes the episodic memory of all previous reflections. These reflections guide the agent to avoid past mistakes and try new strategies.

5. **Iteration:** Steps 1-4 repeat until the task succeeds or a maximum number of trials is reached. Each reflection adds to the accumulated experience.

### Diagram

```
┌────────────────────────────────────────────────────────────┐
│                     Reflexion Loop                         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Episodic Memory                         │  │
│  │  [Reflection 1] [Reflection 2] ... [Reflection N]   │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │ (included in prompt)             │
│                         v                                  │
│  ┌───────────┐    ┌──────────┐    ┌──────────────┐        │
│  │   Task    │───>│  Agent   │───>│  Environment │        │
│  │           │    │  Action  │    │  (Execute)   │        │
│  └───────────┘    └──────────┘    └──────┬───────┘        │
│                                          │                 │
│                                          v                 │
│                                   ┌──────────────┐         │
│                          ┌────────│  Evaluate     │         │
│                          │        │  (pass/fail)  │         │
│                          │        └──────────────┘         │
│                          │                                 │
│                ┌─────────v──────────┐                      │
│                │  Success?          │                      │
│                │  Yes → Output      │                      │
│                │  No  → Reflect ──────> Add to Memory      │
│                └────────────────────┘                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Template

```
You are an agent attempting to solve a task. You have access to previous
reflections from failed attempts.

TASK: {task_description}

PREVIOUS REFLECTIONS (learn from these):
{reflection_1}
{reflection_2}
...

Based on the lessons from previous attempts, try to solve the task.
Avoid repeating past mistakes.

---

[If the attempt fails, generate a reflection:]

REFLECTION PROMPT:
You attempted the following task and failed.

Task: {task_description}
Your attempt: {agent_actions}
Feedback: {environment_feedback}

Reflect on what went wrong. Be specific:
1. What was the root cause of the failure?
2. What incorrect assumption did you make?
3. What should you do differently next time?

Store this reflection for your next attempt.
```

## Examples

### Example 1: Code Generation

**Trial 1 Attempt:**
```
Task: Write a function that returns the longest palindromic substring.

def longest_palindrome(s):
    if not s:
        return ""
    longest = s[0]
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > len(longest):
                longest = sub
    return longest
```

**Evaluation:** Fails on test case `longest_palindrome("")` — should return `""` but function returns `s[0]` which crashes on empty string. Also TLE on large inputs.

**Reflection 1:**
```
My solution had two issues: (1) The empty string check returns "" but
then I set longest = s[0] outside the check, which means for non-empty
strings I start correctly but the logic flow is confusing. The real
issue is the O(n^3) brute force approach — checking every substring and
reversing it is too slow for large inputs. Next time: use the expand-
around-center approach for O(n^2) time, and handle edge cases more
carefully at the start.
```

**Trial 2 Attempt (with reflection in context):**
```
# Learning from reflection: use expand-around-center, handle edge cases
def longest_palindrome(s):
    if not s:
        return ""

    start, max_len = 0, 1

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1

    for i in range(len(s)):
        # Odd-length palindromes
        l1, len1 = expand(i, i)
        if len1 > max_len:
            start, max_len = l1, len1

        # Even-length palindromes
        l2, len2 = expand(i, i + 1)
        if len2 > max_len:
            start, max_len = l2, len2

    return s[start:start + max_len]
```

**Evaluation:** All tests pass. Task completed.

### Example 2: Sequential Decision-Making (ALFWorld)

**Trial 1:**
```
Task: Put a clean apple in the fridge.

> go to countertop 1
You see a bread, a knife.
> go to countertop 2
You see an apple, a plate.
> take apple from countertop 2
You pick up the apple.
> go to fridge 1
> put apple in fridge 1
Task failed: The apple is not clean.
```

**Reflection 1:**
```
I failed because I put the apple directly in the fridge without cleaning
it first. The task says "clean apple" which means I need to wash it at
a sink before putting it in the fridge. Next time: after picking up the
apple, go to a sink, clean the apple, then go to the fridge.
```

**Trial 2 (with reflection):**
```
Task: Put a clean apple in the fridge.
Previous reflection: Need to clean at sink before putting in fridge.

> go to countertop 2
You see an apple, a plate.
> take apple from countertop 2
You pick up the apple.
> go to sinkbasin 1
> clean apple with sinkbasin 1
You clean the apple.
> go to fridge 1
> put apple in fridge 1
Task completed successfully.
```

## When to Use

- Coding tasks with automated test suites that provide clear pass/fail feedback
- Multi-step agent tasks in interactive environments (web navigation, game playing, household tasks)
- Tasks where the agent can make multiple attempts and the environment is resettable
- Problems where failure analysis provides actionable insights for improvement
- Scenarios with binary or clearly graded success criteria

## When to Avoid

- Single-turn question answering where there is no retry mechanism
- Tasks without observable success/failure signals
- Latency-critical applications where multiple trial-and-error loops are unacceptable
- Problems where failures are uninformative (random failures, environment noise)
- When the reflection mechanism consistently fails to produce useful insights

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | 3-10x base | Grows with number of trials and reflection length |
| Latency | Very high | Multiple trial-evaluate-reflect cycles |
| Quality gain | +15-30% | On HumanEval: 80% → 91% pass@1 |
| Typical trials | 2-4 | Most tasks solved within 3 attempts |
| Memory growth | Linear | Each reflection adds to the prompt context |

## Variants

- **Reflexion + External Feedback:** Use compiler errors, test outputs, or human feedback instead of self-evaluation for more reliable failure signals.
- **Bounded Reflexion:** Limit the number of reflections kept in memory (sliding window) to manage context length.
- **Reflexion with Heuristic Evaluation:** Use programmatic heuristics rather than binary success/failure for more granular feedback.
- **Collaborative Reflexion:** Multiple agents share their reflections, building a collective experience base.

## Composability

- **Reflexion + ReAct:** Use ReAct-style reasoning and acting within each trial, with Reflexion providing cross-trial learning.
- **Reflexion + Self-Refine:** Self-Refine handles within-trial iteration, while Reflexion handles across-trial learning.
- **Reflexion + Chain-of-Thought:** CoT reasoning within each trial, with reflections capturing strategic insights that CoT misses.
- **Reflexion + Few-Shot:** Include reflections as few-shot examples of failure analysis to bootstrap the reflection quality.

## Limitations

- Requires an environment or evaluation mechanism that provides actionable feedback
- Context window fills up quickly with accumulated reflections from many failed attempts
- The quality of reflections depends on the model's self-analysis capability
- May loop on tasks where the failure mode is beyond the model's ability to diagnose
- Not applicable to single-shot generation tasks without retry mechanisms
- The model may generate generic, unhelpful reflections that do not lead to improved strategies
- Resettable environments are required; irreversible actions in production settings preclude this approach

## Sources

- **Primary:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — Shinn et al., NeurIPS 2023
- **Code:** [github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion)
- **Related:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Madaan et al., 2023
- **Related:** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al., 2022
