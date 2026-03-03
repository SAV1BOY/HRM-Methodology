---
id: checklist-prompting
name: "Checklist Prompting"
aliases: ["Verification Checklist", "Criteria-Based Verification"]
category: verification
family: verification
year: null
authors: []
paper: null
paper_title: null
venue: null
code: null

complexity: low
token_cost: low
latency: low
num_calls: 1

requires_examples: false
requires_tools: false
requires_training: false
model_agnostic: true

best_for: ["structured output validation", "compliance checking", "quality assurance for generated content", "ensuring completeness of responses", "systematic code review"]
avoid_when: ["open-ended creative tasks", "exploratory brainstorming", "tasks where criteria are unknown or emergent", "simple factual queries"]
composes_with: ["chain-of-thought", "self-refine", "few-shot-prompting", "chain-of-verification"]

tags: ["verification", "checklist", "quality-assurance", "structured", "low-complexity", "practical"]
---

# Checklist Prompting

> **One-line summary:** Checklist Prompting provides the LLM with an explicit list of verification criteria to check against its own output, ensuring completeness, correctness, and adherence to requirements before finalizing a response.

## Overview

Checklist Prompting is a straightforward verification technique that leverages the well-established practice of checklist-based quality assurance. Just as pilots use pre-flight checklists and surgeons use surgical safety checklists to prevent errors, Checklist Prompting provides LLMs with explicit criteria to verify their outputs against. The checklist can be domain-specific (e.g., "Does the SQL query handle NULL values?") or general (e.g., "Is the response complete? Is it factually supported?").

The technique is valuable precisely because of its simplicity. Unlike more sophisticated verification methods such as Chain-of-Verification or Self-Refine, Checklist Prompting requires no additional LLM calls, no iterative loops, and no complex orchestration. The checklist is simply included in the prompt, and the model is instructed to verify its response against each criterion before outputting it. This makes it the lowest-overhead verification technique available, suitable even for latency-sensitive and token-constrained applications.

Despite its simplicity, Checklist Prompting is surprisingly effective at catching common errors and omissions. Models are generally good at verifying specific criteria when explicitly prompted to do so, even if they would not have spontaneously checked those criteria during generation. The technique is particularly powerful when the checklist is crafted by domain experts who know the common failure modes for a given task type, effectively encoding human expertise into the prompt.

## How It Works

1. **Task Execution:** The LLM generates its response to the task as it normally would.

2. **Checklist Application:** Before finalizing, the model evaluates its response against each item in the provided checklist, marking each as satisfied or not.

3. **Remediation:** If any checklist items are not satisfied, the model revises its response to address the gaps, then re-evaluates.

4. **Final Output:** The model produces its final response, optionally including the completed checklist as evidence of verification.

### Diagram

```
┌───────────────────────────────────────────────────┐
│              Checklist Prompting                   │
│                                                   │
│  ┌──────────┐    ┌────────────────────────┐       │
│  │  Task     │    │  Verification          │       │
│  │  Input    │    │  Checklist             │       │
│  └─────┬────┘    │  [ ] Criterion 1       │       │
│        │         │  [ ] Criterion 2       │       │
│        │         │  [ ] Criterion 3       │       │
│        v         │  [ ] Criterion N       │       │
│  ┌──────────┐    └──────────┬─────────────┘       │
│  │ Generate  │              │                     │
│  │ Response  │              │                     │
│  └─────┬────┘              │                     │
│        │                   │                     │
│        v                   v                     │
│  ┌───────────────────────────────────────┐       │
│  │  Verify Response Against Checklist    │       │
│  │  [✓] Criterion 1 — satisfied          │       │
│  │  [✗] Criterion 2 — needs fix          │       │
│  │  [✓] Criterion 3 — satisfied          │       │
│  └──────────────────┬────────────────────┘       │
│                     │                            │
│            ┌────────v────────┐                   │
│            │ Revise if needed │                   │
│            └────────┬────────┘                   │
│                     v                            │
│            ┌─────────────────┐                   │
│            │  Final Output   │                   │
│            │  + Checklist    │                   │
│            └─────────────────┘                   │
└───────────────────────────────────────────────────┘
```

## Template

```
{task_description}

Before providing your final answer, verify it against the following
checklist. If any item is not satisfied, revise your response.

VERIFICATION CHECKLIST:
[ ] {criterion_1}
[ ] {criterion_2}
[ ] {criterion_3}
[ ] {criterion_4}
[ ] {criterion_5}

Provide your response, then show the completed checklist with each
item marked as [✓] satisfied or [✗] not satisfied (with explanation).
```

## Examples

### Example 1: Code Review Checklist

**Input:**
```
Write a Python function to process user registration data from a form
submission. The function should validate the input and store it.

Before providing your final answer, verify it against the following
checklist:
[ ] Input validation for all fields (email format, password strength)
[ ] SQL injection prevention (parameterized queries or ORM)
[ ] Password hashing (never store plaintext)
[ ] Error handling with specific error messages
[ ] Return value indicates success/failure with details
[ ] Type hints and docstring included
```

**Output:**
```python
import re
import hashlib
import secrets
from dataclasses import dataclass
from typing import Optional


@dataclass
class RegistrationResult:
    """Result of a user registration attempt."""
    success: bool
    message: str
    user_id: Optional[int] = None


def register_user(
    email: str,
    password: str,
    name: str,
    db_connection
) -> RegistrationResult:
    """Register a new user with validated and secured data.

    Args:
        email: User's email address.
        password: User's chosen password (plaintext, will be hashed).
        name: User's display name.
        db_connection: Database connection object.

    Returns:
        RegistrationResult indicating success or failure.
    """
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return RegistrationResult(False, "Invalid email format")

    # Validate password strength
    if len(password) < 8:
        return RegistrationResult(False, "Password must be at least 8 characters")
    if not re.search(r'[A-Z]', password):
        return RegistrationResult(False, "Password must contain an uppercase letter")
    if not re.search(r'[0-9]', password):
        return RegistrationResult(False, "Password must contain a digit")

    # Validate name
    if not name or len(name.strip()) < 1:
        return RegistrationResult(False, "Name is required")

    # Hash password with salt
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt.encode(), 100000
    ).hex()

    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash, salt, name) VALUES (?, ?, ?, ?)",
            (email, password_hash, salt, name.strip())
        )
        db_connection.commit()
        user_id = cursor.lastrowid
        return RegistrationResult(True, "Registration successful", user_id)
    except Exception as e:
        return RegistrationResult(False, f"Registration failed: {str(e)}")


VERIFICATION:
[✓] Input validation — email regex, password length/complexity, name presence
[✓] SQL injection prevention — parameterized queries with ? placeholders
[✓] Password hashing — PBKDF2 with random salt, 100k iterations
[✓] Error handling — try/except with specific error messages per failure
[✓] Return value — RegistrationResult dataclass with success, message, user_id
[✓] Type hints and docstring — fully annotated with comprehensive docstring
```

### Example 2: Writing Quality Checklist

**Input:**
```
Write a product description for a noise-canceling headphone aimed at
remote workers.

Verify against this checklist:
[ ] Mentions the target audience (remote workers)
[ ] Highlights at least 3 specific features
[ ] Includes a clear value proposition
[ ] Uses professional but approachable tone
[ ] Is between 100-150 words
[ ] Contains no unsubstantiated superlative claims
```

**Output:**
```
Designed for the demands of remote work, the QuietFocus Pro headphones
deliver the silence you need to stay productive. Advanced hybrid
active noise cancellation blocks out household noise, coffee shop
chatter, and construction sounds, creating your ideal workspace
anywhere. The 40mm custom drivers produce clear, balanced audio for
video calls and focus music alike.

With 30 hours of battery life, you can work through the week on a
single charge. The lightweight 250g design and memory foam ear cushions
keep you comfortable during back-to-back meetings. A built-in
dual-microphone array with AI noise suppression ensures your
colleagues hear you clearly, not your environment.

QuietFocus Pro: professional-grade focus, wherever you work.

VERIFICATION:
[✓] Target audience — "remote work" and "remote workers" referenced
[✓] 3+ features — ANC, 30hr battery, dual-mic array, lightweight design
[✓] Value proposition — "professional-grade focus, wherever you work"
[✓] Tone — professional but conversational, no jargon
[✓] Word count — 127 words (within 100-150 range)
[✓] No unsubstantiated superlatives — specific numbers used, no "best ever"
```

## When to Use

- Any task with known quality criteria that can be expressed as checkable items
- Code generation where common security, performance, or style issues should be caught
- Content creation with specific requirements (word count, tone, mandatory elements)
- Compliance-oriented tasks (regulatory, legal, brand guidelines)
- When you want lightweight verification without the cost of multi-step approaches
- As a "last mile" quality gate in more complex pipelines

## When to Avoid

- Open-ended creative tasks where predefined criteria would be overly constraining
- Exploratory or brainstorming tasks where the output space is intentionally unconstrained
- When the relevant criteria are unknown upfront and must be discovered during generation
- Tasks so simple that a checklist adds unnecessary overhead

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | +10-20% | Checklist text + verification output |
| Latency | Negligible | Single call, inline verification |
| Quality gain | +5-15% | Depends on checklist relevance to common failure modes |
| Num calls | 1 | All happens within a single generation |
| Implementation | Trivial | Append checklist to any existing prompt |

## Variants

- **Pre-Generation Checklist:** Present the checklist before the task so the model considers criteria during generation (proactive vs. reactive).
- **Graduated Checklist:** Organize criteria by priority (must-have, should-have, nice-to-have) to help the model prioritize when trade-offs are necessary.
- **Dynamic Checklist:** The model generates its own checklist based on the task before verifying against it. Combines well with domain expertise.
- **Scored Checklist:** Assign weights to checklist items and compute a quality score, enabling quantitative quality comparison.

## Composability

- **Checklist + Self-Refine:** Use the checklist as the evaluation criteria in Self-Refine's critique step for more targeted feedback.
- **Checklist + Chain-of-Verification:** Use the checklist to generate the verification questions in CoVe's planning step.
- **Checklist + Few-Shot:** Include examples of completed checklists (both passing and failing) to calibrate the model's verification.
- **Checklist + Meta-Prompting:** Each expert persona in Meta-Prompting can have its own domain-specific checklist.

## Limitations

- Only as good as the checklist: missing criteria will not be verified
- The model may superficially mark items as satisfied without genuinely verifying
- Checklists require domain expertise to create well; generic checklists are less effective
- Cannot catch issues that are not anticipated in the checklist (unknown unknowns)
- For complex verification (e.g., logical correctness of multi-step proofs), simple checklist items may be insufficient
- The model may trade off unchecked qualities to satisfy the explicit checklist items

## Sources

- **Primary:** Practical technique widely used in prompt engineering; no single originating paper
- **Related:** [The Checklist Manifesto](https://atulgawande.com/book/the-checklist-manifesto/) — Atul Gawande (inspiration from medical/aviation checklists)
- **Related:** [Chain-of-Verification Reduces Hallucination in Large Language Model Responses](https://arxiv.org/abs/2309.11495) — Dhuliawala et al., 2023
- **Related:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Madaan et al., 2023
