# reflexion.md — HRM L0 verbal reflection (PROT)

> Tier-(b). After each HRM pipeline runs, reflect on the outcome and record it so the technique
> selector learns with use (lights the familiarity term that was a stub). Cheap, per-pipeline.

## When
After the pipeline's `pipeline_report` (post-execution analysis) is produced.

## Steps
1. Read the pipeline outcome: `status`, `gate_pass`, `gate_score`, canonical telemetry
   `{total_tokens, total_latency, api_calls}`, and (when available) the `downstream_kpi_delta`
   reported by the leaf squad's EVOLUTION SIGNAL.
2. Write a one-paragraph verbal reflection: which techniques/playbook helped, what was marginal, what
   to try differently. Emit `reflexion_verdict ∈ {good, bad, neutral}` for the pipeline as a whole.
3. Record (DET): call `python evolution/reflexion.py --pipeline-id ... --techniques <csv> --status ...
   --gate-pass ... --gate-score ... --tokens ... --latency ... --calls ... --verdict <v>`.
   This appends a 16-column row to `data/metrics/pipeline_outcomes.tsv` AND bumps each technique's
   EMA success rate via `memory_store.py` (good=success, bad=fail, neutral=skip).
4. Next pipeline's Phase-3 Score reads `memory.success_rate(id)` from `technique_success.json`, so the
   familiarity term (weight 0.05) reflects real history.

## Contract
- Append-only; never edit prior rows or the kernel. EMA (not win/uses) so the signal adapts.
- L0 is always safe/additive. L1/L2 (GEPA over weights) require `harness_lock.py guard` PASS — disarmed.
