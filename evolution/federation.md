# federation.md — federated evolution across the fleet (PROT + DET, Section 19 §8.3)

> Hub-and-spoke (no peer channel exists). The meta-orchestrator reallocates a shared evolution budget to
> the squads with the best EXPECTED improvement, so effort flows where it pays off — without starving a
> critical squad. DET engine: `evolution/federation.py`; policy: `registry/evolution-federation.yaml`.

## Each epoch (every N fleet attempts) — IMPLEMENTED in `federation.py` (§8.3)
1. For each participant, discover its `data/metrics/evolution_log.tsv` and build a `gate_score` series.
2. `progress_velocity` = **std-error-weighted shrunk** slope over the last K: each slope is shrunk toward
   the fleet mean with precision `1/se²` (an extreme slope is trusted only if precise; a confidence bonus
   applies when the slope CI excludes zero). Raw slope amplifies noise.
3. `score = max(0, shrunk_slope) × P(improvable)` (UCB expected improvement; `P(improvable)` = headroom
   to target), so converged squads at the ceiling stop being funded.
4. Allocate proportionally to `score^(1/temperature)` → **dwell hysteresis** (blend 50/50 toward the prior
   epoch's ledger so a one-epoch swing does not yank budget) → clamp [min,max] → `criticality_floor`
   (cybersecurity ≥ 0.10, data ≥ 0.08 — never starved) → renormalize to 1.0.
5. Write `data/registries/evolution/federation_ledger.yaml` (with per-squad `slope_se`).

## Cost hierarchy
per-attempt budget < per-epoch federation budget < global monthly ceiling (`data/metrics/evolution/cost-ledger.tsv`).
A/B attribution is opt-in + budgeted (default DiD) so it does not double fleet cost.
