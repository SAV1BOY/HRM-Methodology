# Runtime Contract — How the Evolution Layer Loops Actually Execute

> Companion to `evolution/README.md`. This is the authoritative answer to "how does any of this
> run in a Claude-Code-driven markdown/YAML MMOS with no daemon?" — the question the ULTRAPLAN §3
> resolves. Every loop maps to **named triggers + durable state**, never an assumed background process.

## 1. The hard reality
- No daemon / scheduler / service loop. Gates are **agent-run protocols** (`gate-runner.md`), not executables.
- Only `SessionStart` hook exists today; no per-task hook is configured yet.
- Therefore loops are **re-entered** units of work, resuming from `data/`.

## 2. Loop → trigger → durable state

| Loop | Trigger kind | Entry point | Reads | Writes |
|---|---|---|---|---|
| L0 | event (per task) | `evolution-runner l0` from Step-11 cascade + Stop hook `l0_close.py` | trace, gate result | `technique_success.json`, `pipeline_outcomes.tsv`, `lineage.jsonl` |
| L1 | cadence (every N) | `stagnation.py` returns `fire_l1` → runner | `pipeline_outcomes.tsv`, archive | archive variant, `lineage.jsonl` |
| L2 | on_stagnation | `stagnation.py` returns `fire_l2` (L1 saturated) | saturation, lineage, traces | `selector_logic/` variant (gated) |

## 3. `never_stop`, honestly
`never_stop.semantics = "event_driven_L0 + cadence_driven_L1_L2"`. Not infinite. Guaranteed by:
1. **L0 fires on every task** (event-driven, inline, free) via the Step-11 cascade hook + a real Stop hook.
2. **Durable state** in `data/` → every new session resumes (`resume_from`).
3. **Re-armed cadencer** for L1/L2: Stop hook / manual `/loop` / durable cron (warns at 7-day expiry).

## 4. Is GEPA/DSPy runnable here?
- **GEPA = yes**, as a Tier-(b) PROT loop: reflective NL prompt evolution over recorded traces + a Pareto
  frontier. One "rollout" = one real pipeline pass the agent executes against the canary battery, logged to
  `pipeline_outcomes.tsv`. **Default engine.** ~35× more sample-efficient than PromptBreeder.
- **DSPy = no** natively: needs a Python optimizer + many in-process model rollouts, absent here. Deferred
  behind `requires_runner: true`. Never claim DSPy runs in-session.

## 5. Tier-(a) script viability
Python 3.12.10 confirmed. Scripts are **stdlib-only** (no PyYAML), pure (file/stdin in → file/stdout out),
no service loop, < ~150 LOC each, on-demand. Phase 0 verifies the runtime; if script execution is blocked,
lock/sampling degrade to (forgeable) hand-computation → **fail-closed** (do not proceed).

## 6. Cross-repo topology (B15)
Each squad is a **separate git repo** (own `.git`, gpgsign unset, single identity). Tooling uses absolute
paths; rollback reverts only the promoted repo's files; cross-repo reads are **untrusted input**
(hash-checked on ingestion); the single lineage ledger lives in the HRM repo.
