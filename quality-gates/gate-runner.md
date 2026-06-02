# Quality Gate Runner

> Protocol for executing the 4-level verification cascade. Defines how to run gates, what tools to use, and how to format output.

---

## Overview

The Gate Runner executes the verification cascade defined in `gate-definitions.yaml` using the scoring rubrics from `scoring-rubrics.yaml`. It runs after each execution phase and produces a structured verification result.

---

## Execution Protocol

### 1. Determine Gate Depth

```
Input: complexity_score, domain
Output: max_level (1-4)

if domain == "security": max_level = 4
elif complexity_score >= 6: max_level = 4
elif complexity_score >= 3: max_level = 3
else: max_level = 2
```

### 2. Run Gates Sequentially

Gates run in order: Syntax -> Local -> Global -> Semantic. Each gate must PASS before the next runs. If a gate FAILS, the cascade STOPS immediately.

```
for level in 1..max_level:
  result = run_gate(level, deliverables, workstream_spec)
  if result.passed:
    continue to next level
  else:
    STOP cascade
    return failure_report(level, result)

return success_report(all_levels_passed)
```

### 3. Per-Gate Execution

For each gate level:

1. **Load checks** from `gate-definitions.yaml` for this level
2. **Execute each check** using appropriate tools:
   - Syntax checks: `Bash` (lint, build, type-check)
   - Local checks: `Bash` (test runner), `Read` (deliverable verification)
   - Global checks: `Grep` (cross-reference), `Bash` (integration tests)
   - Semantic checks: `Read` (compare against criteria), rubric evaluation
3. **Score each check** using the method from `scoring-rubrics.yaml`
4. **Aggregate** using weighted average
5. **Compare** against domain threshold from `gate-definitions.yaml`

### 4. Scoring a Check

```yaml
check_result:
  check_id: "unit_tests_pass"
  score: 0.95  # 0.0 - 1.0
  passed: true  # score >= 0.5 for individual check
  details: "47/50 tests passed, 3 skipped"
  evidence: "bash output from test run"
```

### 5. Aggregating Gate Score

```
gate_score = sum(check.weight * check.score) for all checks
gate_passed = gate_score >= domain_threshold[level]
```

---

## Tool Usage by Gate Level

| Level | Primary Tools | What to Run |
|-------|--------------|-------------|
| Syntax | `Bash` | `npm run lint`, `tsc --noEmit`, `python -m py_compile`, YAML/JSON validators |
| Local | `Bash`, `Read`, `Glob` | Unit tests, file existence checks, deliverable completeness |
| Global | `Bash`, `Grep`, `Read` | Integration tests, cross-reference validation, dependency checks |
| Semantic | `Read` | Compare deliverables against success criteria and Bloom rubric |

---

## Output Format

### Gate Pass

```yaml
verification_result:
  status: "PASSED"
  levels_checked: 3
  scores:
    syntax: {score: 1.0, passed: true}
    local: {score: 0.92, passed: true}
    global: {score: 0.87, passed: true}
  aggregate_score: 0.93
  domain: "code"
  threshold: 0.88
  details:
    failed_checks: []
    warnings: ["integration test coverage at 78%"]
```

### Gate Failure

```yaml
verification_result:
  status: "FAILED"
  failed_level: 2
  levels_checked: 2
  scores:
    syntax: {score: 1.0, passed: true}
    local: {score: 0.72, passed: false}
  aggregate_score: 0.72
  domain: "code"
  threshold: 0.88
  failure_details:
    failed_checks:
      - check_id: "unit_tests_pass"
        score: 0.60
        details: "30/50 tests passed"
        evidence: "FAIL: auth.test.ts (12 failures)"
    root_cause_hint: "Authentication module has failing tests"
  recommended_action: "Re-execute auth workstream with test fixes"
```

---

## Integration with HRM Steps

| HRM Step | Gate Runner Action |
|----------|-------------------|
| Step 11 (Verification Cascade) | Run full gate cascade, return verification_result |
| Step 12 (Backtracking) | Use failure_details for root-cause analysis |
| Step 10 (Convergence) | Run partial gates at checkpoints for early feedback |

---

## Evolution Layer Hook (L0 — per task) — Section 19

After producing `verification_result` (Step 11), if the active squad has an Evolution Layer
(`evolution/` present + `evolution.enabled: true` in its config), persist the outcome so the squad
learns with use. This is the **L0 trigger seam**: every execution_mode passes through Step 11, so
coverage is guaranteed (a real Stop hook is the belt-and-suspenders backup).

1. **Persist** one append-only row to the squad's `data/metrics/evolution_log.tsv`:
   `task_id, timestamp, task_type, gate_pass, first_pass, gate_score, reflexion_verdict, crystallized_skill_ref`
   - `gate_pass` = (status == PASSED); `first_pass` = passed with no prior failed attempt; `gate_score` = aggregate_score.
2. **Reflect**: follow `evolution/reflexion.md` to write the verbal reflection + emit `reflexion_verdict ∈ {good,bad,neutral}`.
3. **Crystallize** (on clean pass): follow `evolution/voyager_crystallize.md` → `lib/skill_library/crystallize.py` (sha256 dedup).
4. **Never** edit prior rows or the kernel. The KPI rollup is `scripts/reporting/fitness.py` (DET) → `gate_pass_rate`.

> Disarmed safety: L0 (logging / reflection / crystallization) is always safe and additive. L1/L2
> mutation loops require `evolution/harness_lock.py guard` to return PASS (kernel intact + human-sealed),
> which it will refuse until the kernel is armed out-of-band. Until then, only L0 runs.

---

## Adaptive Frequency

Gate frequency adapts based on history:

- **First phase**: Run after every workstream completes
- **After 2+ consecutive passes**: Run only at phase boundaries
- **After any failure**: Increase to per-workstream until 2 consecutive passes
- **Emergency mode**: Skip level 4 if partial score > 0.80 and budget < 20%

---

## Checklist Before Running Gates

1. All expected deliverable files exist
2. Workstream specification is available (for comparison)
3. Test suites are runnable (dependencies installed)
4. Interface contracts are defined (for level 3)
5. Success criteria are defined (for level 4)
6. Domain threshold is set (from config.yaml or gate-definitions.yaml)
