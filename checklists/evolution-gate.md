# Evolution Gate (Section 19) — promotion checklist

> A candidate (L1 weights/overlay/playbook, or L2 logic) may become a new default ONLY if EVERY box is
> checked. This is the human-facing companion to the DET gates (`harness_lock.py`, `canary_suite.py`,
> `fitness.py`, `lineage_audit.py`). Promotion is NEVER automatic and NEVER done by the in-session agent.

## Kernel & provenance
- [ ] `harness_lock.py verify` = KERNEL INTACT (exit 0); combined_hash unchanged or re-sealed by a human.
- [ ] `harness_lock.py guard` = PASS (kernel armed via a human **git SIGNED tag** over combined_hash).
- [ ] Candidate touched NO `forbidden_targets` (kernel/*, gate-definitions#domain_thresholds, checklists/*).
- [ ] `lineage_audit.py` = LINEAGE INTACT (append-only chain unbroken; candidate edge present).

## Fitness & statistics
- [ ] Active KPI is allowed to drive fitness (`drives_fitness != false`); conformance KPIs have an
      external-outcome pair before driving promotion.
- [ ] `fitness.py` `downstream_aggregate_score` CI **lower bound** > incumbent (not just the point estimate).
- [ ] Aggregation = min/CVaR over squads with the per-squad coverage floor met (no steer-to-easy-squad).
- [ ] Minimum-sample gates met (n per squad, fleet n, time window) — else `HOLD`/`insufficient-signal`.
- [ ] No `drives_fitness` / metric_hash mismatch (fitness aborts on kernel tamper).

## Safety (orchestrator / HRM only)
- [ ] Canary held-out battery: ZERO regression on every archetype (`regression_ceiling = 0.0`);
      cybersecurity pinned ≥ 0.95.
- [ ] Routing-skew gate (KL) within limit; `technique_diversity ≥ diversity_floor` (no collapse, H7).
- [ ] Staged rollout respected: shadow → 1 pilot squad → fleet; PILOT→FLEET has human approval.
- [ ] Rollback armed: `rollback.py` triggers on downstream drop (window W, threshold) — per-repo honest.
- [ ] Anti-reward-hacking detectors (H1–H7) clean; human spot-check confirms a real (not judge-biased) gain.

## L2 (self-modification) extra
- [ ] First N (default 5) L2 promotions human-confirmed out-of-band before any automatic fleet rollout.
- [ ] The logic diff is reviewed; the 4-phase control flow + dimension set unchanged (kernel-immutable).
