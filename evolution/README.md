# Evolution Layer (Section 19) — Substrate Contract

This repo is **markdown + YAML driven by a Claude Code agent**. There is **no daemon, scheduler, or
service loop**. The three self-improvement loops (L0/L1/L2) do not "run" — they are **re-entered by
triggers**, reading/writing durable state under `data/` so progress survives between sessions.

## The three tiers (load-bearing classification)

Every mechanism is exactly one of:

| Tier | What | Examples | Why |
|---|---|---|---|
| **(a) DET** | stdlib-only `.py`, invoked on demand via Bash | `harness_lock.py`, `selection.py`, `fitness.py`, `archive.py`, `stagnation.py`, `memory_store.py`, `canary_suite.py`, `rollback.py`, `lineage_audit.py`, `federation.py`, `status.py`, `sync_check.py`, `budget_guard.py` | math/hash/IO must be byte-reproducible and tamper-evident; the agent cannot forge a SHA-256 |
| **(b) PROT** | `.md` protocol the agent follows (same model as `gate-runner.md`) | `reflexion.md`, `judge.md`, `gepa_meta.md`, `meta_agent.md` / `algo_evolve.md` | these are judgments; the model **is** the mutation operator |
| **(c) DATA** | TSV/JSONL/JSON/YAML state files | `pipeline_outcomes.tsv`, `technique_success.json`, `lineage.jsonl`, archive variants | sessions are stateless; the filesystem is the only persistent memory |

**Fitness split:** *scoring* an output against a rubric is Tier-(b) (LLM-judge — gates are agent-run).
*Aggregating* scores into a number is Tier-(a) (`fitness.py`, pure arithmetic). This is the only way to
honor "fitness must be auto-measurable" without inventing an executable gate engine.

## Trigger model — the honest `never_stop` (no daemon)

| Loop | Canonical trigger | How it actually fires | Fallback |
|---|---|---|---|
| **L0** (per task) | event-driven inline | Step-11 verification cascade emits `verification_result` → `evolution-runner l0`; **+ a real Stop hook** running `l0_close.py` | `verification-before-completion` checklist item |
| **L1** (every N) | cadence-driven | counter in `evolution_log.tsv` crosses N → `stagnation.py` → runner chains L1; or manual `/loop` | durable cron (**expires in 7 days**, warned) |
| **L2** (on stagnation) | on_stagnation | `stagnation.py` returns `fire_l2` (L1 saturated) → `meta_agent.md`, gated by canary + staged rollout + **human confirm** | manual `evolution-runner l2`; never a blind timer |

`never_stop` = `event_driven_L0 + cadence_driven_L1_L2` + durable state (`resume_from: data/…`). NOT an
infinite process (impossible here).

## Canonical serialization (how `harness_lock.py` hashes)

Kernel files are hashed by a **stdlib-only canonicalizer** (no PyYAML): drop comments, blank lines, and
trailing whitespace; normalize newlines to `\n`; exclude only each file's own self-hash field
(`metric_hash` / `gates_hash` / `meta_metric_hash`). `combined_hash = sha256(fitness | gates | meta | scripts | gate_definitions | data | loop_scripts)` —
7 components: the 3 kernel YAMLs, the security-script self-hash (C1), the pinned gate-definitions, the
DATA_MANIFEST (canary baseline + suite), and the LOOP_MANIFEST (selection/archive/evolution scripts).
Result is invariant to comments/whitespace, sensitive to any value, and reproducible across clean runs.

## Root of trust = TAMPER-EVIDENT, not tamper-proof

The in-session agent can edit any file **and set any env var**, so arming must require something the
agent cannot synthesize: a **human git SIGNED tag** (`git tag -s kernel-seal-<hash>`) over the current
`combined_hash`, re-verified live by `guard` via `git tag -v`. `guard` **ignores the stored `armed`
flag and accepts no env token** — a hand-edited flag or a self-chosen `$HRM_KERNEL_SEAL_TOKEN` CANNOT
arm (the earlier token was NOT agent-isolated; that hole is closed). With no signing key configured the
kernel stays `armed=false` / disarmed (`guard` exit 4) — correct fail-closed. The
`.git/hooks/pre-commit` adds committer-side tamper-evidence. See `kernel/kernel.seal.json` and
`harness_lock.py`. (Configuring the signing key is the L1-arming gate, ULTRAPLAN open question #1.)

## Commands
```
python evolution/harness_lock.py write     # (re)compute hashes + seal (PENDING_HUMAN_SEAL)
python evolution/harness_lock.py verify    # exit 0 intact / 3 tamper
python evolution/harness_lock.py guard     # exit 0 ok / 3 tamper / 4 disarmed  (call before L1/L2)
python evolution/harness_lock.py status
python evolution/_build/selftest_phase0.py # acceptance evidence (tamper round-trip)
```
## Seal operational notes
- **Re-seal AFTER editing any sealed file.** The kernel YAMLs, the SCRIPT_MANIFEST scripts, and the
  DATA_MANIFEST files (`canary/baseline.json`, `canary/canary_suite.yaml`) are folded into the seal —
  edit one without `harness_lock.py write` and `verify` returns exit 3 (tamper). Order: edit → `write` → commit.
- **`seal.status` / `armed` are ADVISORY only.** `verify` does NOT cover them (they sit outside the hashed
  envelope by design); `guard` is the authority and re-derives arming from a LIVE git signed tag.
  External tooling must not trust `seal.status`.

See `evolution/DECISIONS.md` for adopted defaults and `evolution/_build/PROGRESS.md` for phase status.
