# Section 19 kit — install steps (PT-BR/EN)

Drop-in to make a squad self-evolving. See `templates/squad-generator.md` for the full procedure and
`evolution/templates/section19.template.yaml` for the canonical `evolution:` block.

## Quick install (per squad)
1. Copy `evolution/templates/section19.template.yaml` → append to `<squad>/config.yaml`; fill `<...>`.
2. Copy shared DET scripts → `<squad>/evolution/`:
   `harness_lock.py selection.py archive.py stagnation.py lineage_audit.py` (byte-identical, no edits).
3. Create `<squad>/evolution/kernel/{fitness.yaml,gates.lock.yaml,meta.yaml}` (leaf variant: KPI=its
   primary metric; conformance KPIs set `drives_fitness:false`).
4. Add `<squad>/scripts/reporting/fitness.py` (KPI rollup), `data/metrics/evolution_log.tsv`,
   `data/registries/evolution/.gitkeep`, `lib/skill_library/`.
5. `python evolution/harness_lock.py write` (ships DISARMED) + `bash evolution/install_hooks.sh`.
6. Register in `registry/squads.yaml` (+`evolution:` block) and `registry/evolution-federation.yaml`;
   run `python evolution/sync_check.py` (must stay SYNC OK).

## Invariant
The shared DET scripts are squad-agnostic (paths relative to the script) — a correct drop-in needs ZERO
script edits, only config/kernel parameters. Kernel ships disarmed; arming = a human git signed tag.

## Kit model (intentional: single-source-of-truth, not vendored copies)
This kit is **reference-only by design** (vs ULTRAPLAN §9.2's vendored-copy directory): the canonical
`evolution:` block lives once at `evolution/templates/section19.template.yaml`, and the DET scripts are
pulled **byte-identical** from the HRM `evolution/` at drop-in time (proven: identical SHA-256 across all
3 repos). This avoids stale-copy drift — a copied kit would silently diverge from the shared kernel.
Drop-in = copy the 5 shared scripts + a leaf kernel + fill the template block (steps above).
