# squad-generator.md — make every NEW squad born self-evolving (Section 19 propagation, §9.4)

> There is no executable generator; squads are scaffolded from `registry/squads.yaml` + mapping docs.
> This is the enforced procedure so a new squad ships with the Evolution Layer from day one.

## Steps to add a squad (or retrofit one)
1. **Pick ONE auto-measurable primary KPI** (its `val_bpb`) — see ULTRAPLAN §6.5. If it is an internal
   checklist (conformance), set `conformance: true` + `drives_fitness: false` + name an external-outcome
   pair; it may be LOGGED but not drive L1 until the external pair exists (selection.py enforces this).
2. **Drop in the kit:** copy `evolution/templates/section19.template.yaml` into the squad's `config.yaml`
   (append at EOF, fill placeholders); copy the shared DET scripts into the squad's `evolution/`
   (`harness_lock.py, selection.py, archive.py, stagnation.py, lineage_audit.py`) + a leaf
   `evolution/kernel/{fitness,gates.lock,meta}.yaml`; add `scripts/reporting/fitness.py` (KPI rollup);
   create `data/metrics/evolution_log.tsv`, `data/registries/evolution/.gitkeep`, `lib/skill_library/`.
3. **Seal + install hooks:** `python evolution/harness_lock.py write` (ships disarmed); add the squad's
   own `.git/hooks/pre-commit` kernel-guard (signed-tag) via `evolution/install_hooks.sh`.
4. **Register:** add the squad to `registry/squads.yaml` with an `evolution:` block
   (`enabled, primary_kpi, fitness_direction, kpi_measurability`); add it to
   `registry/evolution-federation.yaml`. Run `python evolution/sync_check.py` (must stay SYNC OK).
5. **Verify drop-in:** `python scripts/reporting/fitness.py --last 5` must produce a KPI rollup with
   NO edits to the shared scripts (only config/kernel params differ).

## The 19th verification-checklist line
Add to `checklists/hrm-self-check.md` a `## Phase 9.5: Evolution Layer Verification`:
- [ ] Section 19 active: squad emits an EVOLUTION SIGNAL with an auto-measurable `primary_kpi` + locked
      `metric_hash`, KPI delta appended to `lineage.jsonl`, and the harness (quality_gates + meta_metric)
      hash-verified UNCHANGED by an EXTERNAL verifier (git signed-tag hook / human).
