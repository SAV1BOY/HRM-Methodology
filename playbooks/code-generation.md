# Playbook: Code Generation

> **Pipeline:** Plan-and-Solve → Program of Thoughts → Self-Refine → Checklist Prompting
>
> **Best for:** Feature implementation, API development, algorithm coding, utility scripts, middleware, data pipelines.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │   Coding Task       │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. Plan-and-Solve   │  Decompose into plan
                    │     (PS+)           │  with numbered steps
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Program of       │  Generate code using
                    │     Thoughts (PoT)  │  code-based reasoning
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Self-Refine      │  Review code, find
                    │                     │  bugs, optimize
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Checklist        │  Verify against quality
                    │     Prompting       │  checklist before shipping
                    └─────────┴───────────┘
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | Plan-and-Solve | Coding tasks benefit from upfront decomposition — identifying data structures, interfaces, edge cases, and execution order before writing code |
| 2 | Program of Thoughts | Instead of natural-language reasoning, PoT produces executable code that serves as both the solution and the reasoning trace |
| 3 | Self-Refine | Code always benefits from review — catching bugs, improving naming, optimizing performance, adding error handling |
| 4 | Checklist Prompting | A systematic final pass against coding standards ensures nothing is missed: types, tests, docs, security, error handling |

## Step-by-Step Templates

### Step 1: Plan-and-Solve

**Purpose:** Decompose the coding task into a structured implementation plan before writing any code.

```
You are a senior software engineer. Before writing any code, create a detailed
implementation plan for the following task.

TASK:
{coding_task}

CONSTRAINTS:
- Language: {language}
- Framework: {framework}
- Must integrate with: {existing_codebase_context}

Create your plan:

1. REQUIREMENTS ANALYSIS
   - What are the inputs and outputs?
   - What are the edge cases?
   - What are the performance requirements?

2. DESIGN DECISIONS
   - What data structures will you use and why?
   - What design patterns apply?
   - What is the public API / interface?

3. IMPLEMENTATION STEPS (ordered)
   - Step 1: ...
   - Step 2: ...
   - Step N: ...

4. TESTING STRATEGY
   - What unit tests are needed?
   - What integration tests?
   - What edge cases to test?

5. ERROR HANDLING
   - What can go wrong?
   - How should each failure mode be handled?
```

### Step 2: Program of Thoughts

**Purpose:** Implement the code following the plan, using code as the reasoning medium.

```
Following the implementation plan below, write the complete code.
Use code comments to explain your reasoning at each step.

IMPLEMENTATION PLAN:
{plan_output}

REQUIREMENTS:
- Write production-quality code, not pseudocode
- Include type hints / type annotations
- Include docstrings for public functions and classes
- Handle errors explicitly — no bare except clauses
- Follow {language} conventions and idioms

Generate the implementation file by file:

### File: {filename}
```{language}
# Implementation here
```

For each file, explain:
- What this file is responsible for
- Key design choices made in the implementation
```

### Step 3: Self-Refine

**Purpose:** Review the generated code like a senior engineer conducting a code review.

```
You are a senior engineer conducting a thorough code review.
Review the following code and then produce an improved version.

CODE TO REVIEW:
{pot_output}

Review for:

1. **Correctness** — Does it handle all specified edge cases? Are there
   off-by-one errors, race conditions, or logic bugs?

2. **Performance** — Are there unnecessary allocations, O(n^2) loops that could
   be O(n), or missing caching opportunities?

3. **Security** — Input validation, SQL injection, path traversal, secret
   handling, authentication checks?

4. **Readability** — Clear naming, appropriate abstraction level, no magic
   numbers, logical grouping?

5. **Error handling** — All failure modes covered? Appropriate error types?
   Helpful error messages?

6. **Testability** — Can this be unit tested? Are dependencies injectable?

REVIEW OUTPUT FORMAT:
## Issues Found
- [SEVERITY] Description → Suggested fix

## Improved Code
(Complete revised implementation)
```

### Step 4: Checklist Prompting

**Purpose:** Final quality gate before the code is considered complete.

```
Verify the following code against this production readiness checklist.
For each item, mark PASS or FAIL with a brief note.

CODE:
{refined_code}

## Checklist

### Functionality
- [ ] All requirements from the original task are implemented
- [ ] Edge cases are handled (empty input, null, overflow, unicode)
- [ ] Return types are consistent and documented

### Code Quality
- [ ] Functions are under 50 lines (or have clear justification)
- [ ] No code duplication (DRY principle)
- [ ] Variable/function names are descriptive
- [ ] Comments explain "why" not "what"

### Type Safety
- [ ] All function signatures have type annotations
- [ ] Complex types use appropriate generics/unions
- [ ] No use of `Any` type without justification

### Error Handling
- [ ] All external calls are wrapped in try/except (or equivalent)
- [ ] Custom exception types for domain errors
- [ ] Error messages include context for debugging

### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] File paths are validated against traversal

### Testing
- [ ] Unit tests cover happy path
- [ ] Unit tests cover edge cases
- [ ] Unit tests cover error paths
- [ ] Test assertions are specific (not just "no error")

### Documentation
- [ ] Public API has docstrings
- [ ] Complex logic has inline comments
- [ ] Usage example is provided

If any items FAIL, produce a final corrected version of the code.
```

## Walk-Through Example

**Task:** "Build rate-limiting middleware for a FastAPI application that supports per-user and per-endpoint limits with a sliding window algorithm backed by Redis."

---

### Step 1 Output: Plan

> **1. Requirements Analysis**
> - Input: HTTP request with user identifier and endpoint path
> - Output: Either allow request (pass to next middleware) or return 429
> - Edge cases: Missing user ID (use IP), Redis unavailable (fail-open vs fail-closed), clock skew
> - Performance: Must add < 5ms latency per request
>
> **2. Design Decisions**
> - Sliding window using sorted sets in Redis (ZADD + ZRANGEBYSCORE)
> - Configuration via dataclass with per-endpoint overrides
> - Dependency injection for Redis client (testability)
> - Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
>
> **3. Implementation Steps**
> - Step 1: Define RateLimitConfig dataclass
> - Step 2: Implement SlidingWindowLimiter class
> - Step 3: Create FastAPI middleware
> - Step 4: Add configuration loading
> - Step 5: Write tests
>
> **4. Testing Strategy**
> - Unit test SlidingWindowLimiter with mock Redis
> - Integration test middleware with TestClient
> - Test: burst at limit, exceed limit, window sliding, Redis failure

### Step 2 Output: Program of Thoughts

> ```python
> # rate_limiter/config.py
> from dataclasses import dataclass, field
>
> @dataclass
> class RateLimitRule:
>     """Defines a rate limit rule for an endpoint pattern."""
>     requests: int          # max requests in window
>     window_seconds: int    # sliding window size
>     burst_multiplier: float = 1.0  # allow burst up to requests * multiplier
>
> @dataclass
> class RateLimitConfig:
>     """Global rate limit configuration."""
>     default_rule: RateLimitRule = field(
>         default_factory=lambda: RateLimitRule(requests=100, window_seconds=60)
>     )
>     endpoint_rules: dict[str, RateLimitRule] = field(default_factory=dict)
>     fail_open: bool = True  # allow requests if Redis is unavailable
>     user_id_header: str = "X-User-ID"
> ```
>
> [Full implementation continues with SlidingWindowLimiter, middleware, tests...]

### Step 3 Output: Self-Refine

> **Issues Found:**
> - [HIGH] Race condition in check-then-increment — should use Redis MULTI/EXEC pipeline
> - [MEDIUM] Missing EXPIRE on the sorted set key — could leak memory
> - [LOW] `window_seconds` should validate > 0 in `__post_init__`
>
> **Improved Code:** [Revised implementation with pipeline, TTL, validation]

### Step 4 Output: Checklist Verification

> - [PASS] All requirements implemented (per-user, per-endpoint, sliding window, Redis)
> - [PASS] Edge cases handled (missing user ID falls back to IP, Redis failure uses fail_open)
> - [PASS] Type annotations on all functions
> - [PASS] Custom RateLimitExceeded exception
> - [FAIL] Missing docstring on _get_user_identifier method → FIXED
> - [PASS] No hardcoded secrets
> - [PASS] Unit tests cover happy path, limit exceeded, Redis failure

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **Quick prototype** | Skip Checklist (step 4); use single Self-Refine pass |
| **High-stakes production** | Add Self-Consistency at step 2 (generate 3 implementations, pick best) |
| **Unfamiliar codebase** | Add Context-Stuffing before step 1 (inject existing code patterns) |
| **Complex algorithms** | Add Tree-of-Thoughts at step 2 for algorithm design exploration |
| **Team standards** | Customize the Checklist to match your organization's code review guidelines |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| Plan-and-Solve | 1 | ~800 output | Low |
| Program of Thoughts | 1 | ~2000 output | Medium |
| Self-Refine | 2-3 | ~2500 output | Medium |
| Checklist | 1 | ~1000 output | Low |
| **Total** | **5-6** | **~6300 tokens** | **~20-45s** |
