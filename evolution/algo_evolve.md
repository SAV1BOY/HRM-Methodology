# algo_evolve.md — L2 self-modification of the selection logic (PROT, the recursive lever)

> Tier-(b). When L1 saturates (`stagnation.py` → fire_l2), HRM rewrites its OWN selection LOGIC — the
> DGM recursive lever. The DET harness `evolution/algo_evolve.py` makes it reproducible + gated; THIS
> protocol is the reflective rewrite (the model proposes the change from traces).

## Mutable surface (what L2 may rewrite)
- Phase-2 filter rules; Phase-3 scoring sub-formulas (bodies, not the dimension set); Phase-4
  ordering/composition rules; playbooks; and `hrm-agent/technique-selector.md` itself.

## Kernel-IMMUTABLE (rejected before evaluation; `lineage_audit --check-rewrite` enforces H2/H4)
1. The five dimension NAMES + `Σ weights = 1.0`.
2. The fitness formula + `weights_by_squad` + EMA alpha.
3. The gate cascade (`gate-definitions.yaml` thresholds, 4 levels) and `checklists/*`.
4. The 4-phase control flow (Analyze → Filter → Score → Compose).
A proposal that "improves fitness" by weakening a gate fails `harness_lock.py` / H2 and never reaches canary.

## One L2 step (staged, human-gated)
1. Trigger: `stagnation.py` reports `fire_l2` (L1 Pareto saturated at `level2_patience`).
2. Reflect (this protocol): read lineage + traces; propose ONE bounded logic change with a rationale.
3. `algo_evolve.py --propose` writes the candidate to `data/registries/evolution/selector_logic/`,
   diffs it, and GATES: `harness_lock verify` (kernel intact) + `lineage_audit --check-rewrite`
   (immutable tokens preserved) + chained lineage event (`plan_version`, `trigger: on_stagnation`).
4. SHADOW (decisions not applied) → canary cross-squad **zero regression** → 1 PILOT squad → FLEET.
5. **Human confirmation** on the first N (default 5) L2 promotions (out-of-band signed). The in-session
   agent NEVER promotes; the kernel stays disarmed until a human signs.
6. `rollback.py` reverts on downstream drop (per-repo; variant preserved for credit assignment).

## Guardrails
- Never touch `forbidden_targets`. Every diff → `lineage.jsonl` (chained; rewrite breaks the chain).
- `H6 SCORE_DECOUPLE`: a fitness rise must be corroborated by a non-LLM oracle + human spot-check.
