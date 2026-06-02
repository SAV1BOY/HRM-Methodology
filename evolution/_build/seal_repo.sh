#!/usr/bin/env bash
# seal_repo.sh — AGENT-SIDE steps to seal ONE repo's Section 19 kernel.
# The HUMAN still creates the signed tag (this script never signs and cannot arm).
#
# Usage:  bash seal_repo.sh <path/to/harness_lock.py> <git-root> <SHA256:fingerprint>
# Example (Pre-Programming):
#   bash seal_repo.sh \
#     "Pre-Programming-Squad/squads/pre-programming/evolution/harness_lock.py" \
#     "Pre-Programming-Squad" "SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#
# What it does (all non-secret):
#   1. pins YOUR fingerprint into kernel/meta.yaml authorized_seal_keys (idempotent)
#   2. re-seals the hashes (harness_lock.py write) — status stays PENDING_HUMAN_SEAL; NOT armed
#   3. verifies INTACT and derives the EXACT tag name from the new combined_hash
#   4. prints the 3 commands for YOU to run with your key (sign / verify / guard)
set -euo pipefail
HL="${1:?path to harness_lock.py}"; ROOT="${2:?git root}"; FPR="${3:?SHA256: fingerprint}"
case "$FPR" in SHA256:*) ;; *) echo "ABORT: fingerprint must start with 'SHA256:'"; exit 1;; esac
EVO="$(dirname "$HL")"; META="$EVO/kernel/meta.yaml"
[ -f "$META" ] || { echo "ABORT: no meta.yaml at $META"; exit 1; }

# 1) pin fingerprint (replaces PENDING_HUMAN_FINGERPRINT or any prior value)
python - "$META" "$FPR" <<'PY'
import sys, re
meta, fpr = sys.argv[1], sys.argv[2]
s = open(meta, encoding="utf-8").read()
new, n = re.subn(r'authorized_seal_keys:\s*\[[^\]]*\]',
                 'authorized_seal_keys: ["%s"]' % fpr, s)
if n != 1:
    sys.exit("ABORT: could not find a single authorized_seal_keys line to pin")
open(meta, "w", encoding="utf-8", newline="\n").write(new)
print("pinned authorized_seal_keys =", fpr)
PY

# 2) re-seal hashes over the edit (does NOT arm)
python "$HL" write   >/dev/null
python "$HL" verify

# 3) derive the exact tag from the NEW hash
TAG="kernel-seal-$(python "$HL" status | sed -n 's/.*"combined_hash": "sha256:\(............\).*/\1/p')"
[ -n "${TAG#kernel-seal-}" ] || { echo "ABORT: could not derive tag"; exit 1; }

cat <<EOF

================  NOW YOU (with your key + passphrase, your terminal)  ================
  git -C "$ROOT" tag -s $TAG -m "Section 19 kernel seal — human-approved"
  git -C "$ROOT" tag -v $TAG          # must print: Good "git" signature ... $FPR
  python "$HL" guard                  # must print GUARD PASS and exit 0 = SEALED
======================================================================================
(l1_l2_armed stays false until the 5 gold sets exist — sealing only locks the kernel.)
EOF
