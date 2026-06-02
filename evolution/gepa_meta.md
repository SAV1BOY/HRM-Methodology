# gepa_meta.md — L1 reflective evolution of the selector (PROT)

> Tier-(b) protocol: GEPA (Genetic-Pareto) evolution of the selector genome via natural-language
> reflection over recorded traces + a Pareto frontier. The DET harness `evolution/gepa_meta.py`
> orchestrates one generation; THIS protocol is the reflective MUTATION operator (the model).
> One "rollout" = one real pipeline pass against the held-out battery (gated; disarmed today → SHADOW).

## What may be evolved (targets — config.yaml evolution.meta.targets)
- `evolution/selector_config.yaml` `genome.weights` (the five dimension VALUES)
- `genome.composes_with_overlay` (ADDITIVE edges; the `taxonomy.yaml#composes_with` base is immutable)
- `genome.playbook_bindings`
NEVER the kernel, base checklists, gate thresholds, harness_lock (forbidden_targets → harness_lock blocks).

## One generation (reflective)
1. **Select parent** genome from the Pareto archive (`selection.py --emit parent`).
2. **Reflect** (this step): read recent `pipeline_outcomes.tsv` rows + `SELECTION TRACE:` logs + failure
   reflexions. Diagnose *why* the parent under/over-weighted a dimension or mis-composed techniques.
   Propose ONE targeted edit (a weight nudge, an overlay edge, a playbook rebinding) with a rationale.
3. **Invariants (hard, kernel)**: the candidate MUST keep the five dimension NAMES and `Σ weights == 1.0`
   (gepa_meta.py / fitness.py reject otherwise). It MUST NOT touch forbidden_targets.
4. **Score** the candidate: run it as a real pipeline pass over the held-out canary battery →
   `fitness.py` computes `downstream_aggregate_score` (decomposed, min/CVaR, bootstrap CI). If the
   active KPI has `drives_fitness:false`, the candidate is exploration-only (cannot promote).
5. **Archive** with chained lineage (`archive.py --add`); recompute the Pareto front (keep_stepping_stones).
6. **Promotion** is NOT done here — it is canary-gated + staged (Phase 5) and requires the kernel armed
   (human signed tag). While disarmed, generations are SHADOW/archive-only (ULTRAPLAN B0).

## Pareto frontier
Maintain non-dominated genomes over {quality, -cost, -latency, diversity}. Select from any stepping
stone (even dominated) so the search stays open-ended. GEPA's NL reflection is ~35x more sample-efficient
than PromptBreeder — feasible at session cadence; DSPy is deferred (`requires_runner:true`).
