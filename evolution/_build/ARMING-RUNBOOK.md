# Section 19 — Arming Runbook (HUMAN-ONLY, turnkey)

> The agent **cannot** run this: every arming path requires a human signing key it has no access to,
> and `guard` re-verifies a live `git tag -v` against a pinned fingerprint (fail-closed). This runbook
> reduces your work to copy-paste + the four irreducibly-human inputs. **Nothing here is armed yet.**
>
> ⚠️ **Hash-changes-on-edit invariant:** `kernel/meta.yaml` is part of `combined_hash`. The moment you
> pin your fingerprint / fill `judge_lock`, the hash changes — so the tag name **must be derived after
> `write`**, never from today's disarmed hash. The snippets below derive it for you.

## Today's DISARMED reference (will change after step 3)
| Repo | git root | harness_lock | disarmed combined_hash | disarmed tag (pre-edit) |
|---|---|---|---|---|
| HRM | `Squad HRM/` | `evolution/harness_lock.py` | `…c92fdee6b187…` | `kernel-seal-c92fdee6b187` |
| Pre-Programming | `Pre-Programming-Squad/` | `squads/pre-programming/evolution/harness_lock.py` | `…10aabbc2f5bf…` | `kernel-seal-10aabbc2f5bf` |
| Deep-Research | `Deep-Research-Squad/` | `evolution/harness_lock.py` | `…367fab50e00c…` | `kernel-seal-367fab50e00c` |

## The four irreducibly-human inputs
1. A signing key (GPG or SSH) the agent has **no** access to → its fingerprint `FPR`.
2. The pinned fingerprint in `kernel/meta.yaml: authorized_seal_keys` (replaces `PENDING_HUMAN_FINGERPRINT`).
3. `judge_lock_judge_model_id` + `judge_lock_prompt_hash` (replace `PENDING_HUMAN_SEAL`/`PENDING`).
4. The 5 proxy-KPI gold sets (copy/brand/storytelling/movement/advisory, κ≥0.6) — until these exist, keep
   `l1_l2_armed:false`; B0 stays shadow/archive-only even when sealed.

## Ordered ceremony (per repo — do HRM **last**, its blast radius is the whole fleet)

```bash
# ── one-time: configure your signing key ──────────────────────────────────────
git config user.signingkey <FPR>
git config commit.gpgsign true        # GPG; for SSH: git config gpg.format ssh

# ── per repo: set HL = path to that repo's harness_lock.py, ROOT = its git root ─
HL="<repo>/.../evolution/harness_lock.py"; ROOT="<repo git root>"

# 1) PIN fingerprint + fill judge_lock in kernel/meta.yaml (edit by hand):
#      authorized_seal_keys: ["<FPR>"]
#      judge_lock_judge_model_id: "<model id>"
#      judge_lock_prompt_hash: "sha256:<hash of the frozen judge prompt>"

# 2) FAIL-CLOSED preflight — abort if any placeholder remains:
META="$(dirname "$HL")/kernel/meta.yaml"
if grep -qE "PENDING_HUMAN_FINGERPRINT|PENDING_HUMAN_SEAL|PENDING\"" "$META"; then
  echo "ABORT: placeholders still present in $META — fill inputs 1-3 first."; exit 1; fi

# 3) Re-seal the hashes over your edits (recomputes combined_hash → NEW value):
python "$HL" write
python "$HL" verify        # expect: KERNEL INTACT sha256:<NEW>

# 4) Derive the CORRECT tag from the NEW hash and create the SIGNED tag with your key:
TAG="kernel-seal-$(python "$HL" status | sed -n 's/.*"combined_hash": "sha256:\(............\).*/\1/p')"
echo "tag to sign: $TAG"
git -C "$ROOT" tag -s "$TAG" -m "Section 19 kernel seal — human-approved arming"

# 5) Prove the signature verifies (must print a Good signature from <FPR>):
git -C "$ROOT" tag -v "$TAG"

# 6) Guard now ARMS (exit 0). Disarmed/forged stays exit 4:
python "$HL" guard; echo "guard exit: $?   # 0 = ARMED"
```

Then, fleet-wide, only after ≥1 leaf has emitted real downstream rows and you've re-verified:
- **L0** install the project-scoped Stop hook (`l0_close.py --status`) — per-task L0 closure.
- **L1/L2** flip `evolution.l1_l2_armed:true` **last**, staged shadow→pilot→fleet (canary regression
  ceiling 0.0; cybersecurity 0.95 hard). HRM is armed only after the leaves prove safe.

## Reversibility
`evolution.enabled:false` restores pre-evolution behavior anywhere. Delete the `kernel-seal-*` tag
(`git tag -d <TAG>`) and `guard` returns to DISARMED (exit 4) immediately — arming is not sticky beyond
the signed tag.
