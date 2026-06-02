#!/usr/bin/env python3
"""harness_lock.py — Kernel root-of-trust verifier for the HRM Evolution Layer (Section 19).

Tier-(a) DETERMINISTIC utility. STDLIB-ONLY (no PyYAML). Python 3.12+.
Enforces the IMMUTABLE kernel: kernel/fitness.yaml, kernel/gates.lock.yaml, kernel/meta.yaml,
the pinned gate-definitions thresholds, and the security scripts themselves (self-hashing, C1).

"Immutable" here = TAMPER-EVIDENT, not tamper-proof (the in-session agent can edit any file).
Real enforcement = an EXTERNAL verifier (.git/hooks/pre-commit) running this from a pinned
checkout, plus a human reseal via a git SIGNED tag (`git tag -s kernel-seal-<hash>`). NO env var and
no hand-edited 'armed' flag can arm — guard re-verifies the signed tag LIVE. See README.md.

Commands:
  write    (re)compute all hashes, fill *_hash fields + kernel.seal.json (status PENDING_HUMAN_SEAL)
  verify   recompute and compare. exit 0 = INTACT, exit 3 = KERNEL TAMPER DETECTED
  guard    verify + require a valid human git SIGNED tag over combined_hash (IGNORES the stored
           'armed' flag and any env var). exit 0 ok / 3 tamper / 4 disarmed. Use before L1/L2
  status   print seal + armed flag
  reseal   HUMAN-ONLY. requires a verifiable `git tag -s kernel-seal-<hash>`; the agent cannot do this
           (no signing key). --token/--by are DEPRECATED and IGNORED. arms only if the tag verifies
  restore  git checkout -- kernel files (revert tamper)
"""
import sys, os, json, hashlib, subprocess, argparse, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
KDIR = os.path.join(HERE, "kernel")
SEAL = os.path.join(KDIR, "kernel.seal.json")
GATE_DEFS = os.path.join(REPO, "quality-gates", "gate-definitions.yaml")

# kernel file -> field name storing THIS file's own canonical hash (excluded when hashing it)
KERNEL_FILES = {"fitness.yaml": "metric_hash",
                "gates.lock.yaml": "gates_hash",
                "meta.yaml": "meta_metric_hash"}
# security/load-bearing scripts whose bytes are part of the seal (self-hashing, C1). skip-missing.
# Entries WITHOUT a slash resolve under evolution/; entries WITH a slash resolve under the squad root
# (so a leaf's scripts/reporting/fitness.py folds into the tamper-evident envelope too).
SCRIPT_MANIFEST = ["harness_lock.py", "fitness.py", "lineage_audit.py", "canary_suite.py",
                   "budget_guard.py", "scripts/reporting/fitness.py"]
# DATA files whose integrity underpins the promotion gates (canary baseline + suite). Folded into the
# seal so baseline drift is TAMPER-EVIDENT — re-baselining is a human event that requires a re-seal,
# closing the "edit baseline.json to bypass the 0.95 floor" hole. skip-missing (leaves have no canary).
DATA_MANIFEST = ["canary/baseline.json", "canary/canary_suite.yaml"]
# LOOP-mechanics DET scripts (selection/archive/evolution logic). Folded into the seal so an in-session
# edit to their ARITHMETIC is tamper-evident BEFORE arming (global-audit defense-in-depth). skip-missing
# (leaves carry only their subset). These are not the verifier itself (that's SCRIPT_MANIFEST).
LOOP_MANIFEST = ["selection.py", "archive.py", "memory_store.py", "reflexion.py", "stagnation.py",
                 "algo_evolve.py", "gepa_meta.py", "federation.py", "skill_promotion.py", "rollback.py",
                 "status.py", "sync_check.py"]


def _norm_lines(text):
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    return [ln.rstrip() for ln in t.split("\n")]


def sha256_hex(b):
    return "sha256:" + hashlib.sha256(b).hexdigest()


def canonical_hash(path, self_key=None):
    """Hash a config file ignoring comments, blank lines, trailing ws, and the self-hash field."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    out = []
    for ln in _norm_lines(text):
        s = ln.strip()
        if s == "" or s.startswith("#"):
            continue
        key = s.split(":", 1)[0].strip() if ":" in s else None
        # exclude the self-hash field ONLY at top level (no indent) to avoid a same-named nested key
        if self_key and key == self_key and ln[:1] not in (" ", "\t"):
            continue
        out.append(ln)
    return sha256_hex(("\n".join(out) + "\n").encode("utf-8"))


def raw_hash(path):
    """Newline-normalized hash of full file (for code/scripts: comments matter)."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return sha256_hex(("\n".join(_norm_lines(text)) + "\n").encode("utf-8"))


def set_field(path, key, value):
    """Replace 'key: ...' value in a flat YAML kernel file. Fails if key missing."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
    for i, ln in enumerate(lines):
        st = ln.strip()
        if (not st.startswith("#")) and ":" in st and st.split(":", 1)[0].strip() == key:
            indent = ln[:len(ln) - len(ln.lstrip())]
            lines[i] = f'{indent}{key}: "{value}"'
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return
    raise SystemExit(f"set_field: key '{key}' not found in {path}")


def _scripts_hash():
    parts, manifest = [], []
    for name in SCRIPT_MANIFEST:
        p = os.path.join(REPO, name) if "/" in name else os.path.join(HERE, name)
        if os.path.exists(p):
            parts.append(raw_hash(p))
            manifest.append(name if "/" in name else "evolution/" + name)
    return sha256_hex("|".join(parts).encode("utf-8")), manifest


def _data_hash():
    parts, manifest = [], []
    for name in DATA_MANIFEST:
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            parts.append(raw_hash(p))
            manifest.append("evolution/" + name)
    return sha256_hex("|".join(parts).encode("utf-8")), manifest


def _loop_hash():
    parts, manifest = [], []
    for name in LOOP_MANIFEST:
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            parts.append(raw_hash(p))
            manifest.append("evolution/" + name)
    return sha256_hex("|".join(parts).encode("utf-8")), manifest


def compute_all():
    gd = canonical_hash(GATE_DEFS) if os.path.exists(GATE_DEFS) else "sha256:NA"
    fit = canonical_hash(os.path.join(KDIR, "fitness.yaml"), "metric_hash")
    gat = canonical_hash(os.path.join(KDIR, "gates.lock.yaml"), "gates_hash")
    met = canonical_hash(os.path.join(KDIR, "meta.yaml"), "meta_metric_hash")
    sh, manifest = _scripts_hash()
    dh, dmanifest = _data_hash()
    lh, lmanifest = _loop_hash()
    combined = sha256_hex("|".join([fit, gat, met, sh, gd, dh, lh]).encode("utf-8"))
    return {"fitness_hash": fit, "gates_hash": gat, "meta_hash": met, "scripts_hash": sh,
            "gate_definitions_hash": gd, "data_hash": dh, "loop_scripts_hash": lh,
            "combined_hash": combined, "scripts_manifest": manifest, "data_manifest": dmanifest,
            "loop_manifest": lmanifest}


def _git_commit():
    try:
        return subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"],
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None


def _load_seal():
    if not os.path.exists(SEAL):
        raise SystemExit("No kernel.seal.json. Run: python harness_lock.py write")
    with open(SEAL, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_write():
    # pin gate-definitions hash first — HRM only; leaves have no external gate-definitions.yaml
    if os.path.exists(GATE_DEFS):
        set_field(os.path.join(KDIR, "gates.lock.yaml"), "pinned_gate_definitions_hash",
                  canonical_hash(GATE_DEFS))
    h = compute_all()
    set_field(os.path.join(KDIR, "fitness.yaml"), "metric_hash", h["fitness_hash"])
    set_field(os.path.join(KDIR, "gates.lock.yaml"), "gates_hash", h["gates_hash"])
    set_field(os.path.join(KDIR, "meta.yaml"), "meta_metric_hash", h["meta_hash"])
    h = compute_all()
    seal = {"_doc": "Bootstrap kernel seal. NOT human-approved. See evolution/README.md root-of-trust.",
            "combined_hash": h["combined_hash"],
            "components": {k: h[k] for k in ("fitness_hash", "gates_hash", "meta_hash", "scripts_hash",
                                             "gate_definitions_hash", "data_hash", "loop_scripts_hash")},
            "scripts_manifest": h["scripts_manifest"],
            "data_manifest": h["data_manifest"],
            "loop_manifest": h["loop_manifest"],
            "status": "PENDING_HUMAN_SEAL", "armed": False, "approved_sig": None,
            "approved_by": None, "approved_ts": None, "git_commit": _git_commit()}
    with open(SEAL, "w", encoding="utf-8") as f:
        json.dump(seal, f, indent=2)
        f.write("\n")
    print("KERNEL WRITTEN (status=PENDING_HUMAN_SEAL, armed=false)")
    print("  combined:", h["combined_hash"])
    return 0


def cmd_verify(quiet=False):
    seal = _load_seal()
    h = compute_all()
    problems = []
    for k in ("fitness_hash", "gates_hash", "meta_hash", "scripts_hash",
              "gate_definitions_hash", "data_hash", "loop_scripts_hash", "combined_hash"):
        exp = seal["combined_hash"] if k == "combined_hash" else seal["components"].get(k)
        if exp != h[k]:
            problems.append(f"  {k}: expected {exp} got {h[k]}")
    if problems:
        print("KERNEL TAMPER DETECTED")
        for p in problems:
            print(p)
        return 3
    if not quiet:
        print("KERNEL INTACT", h["combined_hash"])
    return 0


def _seal_tag(combined_hash):
    return "kernel-seal-" + combined_hash.split(":")[-1][:12]


def _authorized_keys():
    """Real (non-PENDING) signer fingerprints pinned in kernel/meta.yaml authorized_seal_keys."""
    import re as _re
    p = os.path.join(KDIR, "meta.yaml")
    if not os.path.exists(p):
        return []
    for ln in open(p, encoding="utf-8"):
        s = ln.strip()
        if s.startswith("authorized_seal_keys:"):
            return [v for v in _re.findall(r'"([^"]+)"', s) if "PENDING" not in v]
    return []


def _verify_signed_tag(combined_hash):
    """Arming requires a HUMAN-created git SIGNED tag over the current combined_hash.
    `git tag -v` exits 0 ONLY if the signature verifies against a trusted key. The in-session agent
    has no private key and cannot forge this, and CANNOT bypass it via an env var (unlike the old
    token). Returns (ok, signer). No key configured -> fail-closed (disarmed), which is correct."""
    tag = _seal_tag(combined_hash)
    try:
        r = subprocess.run(["git", "-C", REPO, "tag", "-v", tag], capture_output=True, text=True)
        if r.returncode != 0:
            return False, None
        out = r.stderr + "\n" + r.stdout
        keys = _authorized_keys()              # load-bearing once a real fingerprint is pinned (else no-op)
        if keys and not any(k in out for k in keys):
            return False, "signer not in authorized_seal_keys"
        signer = "verified"
        for line in out.splitlines():
            if "Good signature" in line or "Good \"git\"" in line:
                signer = line.strip()
                break
        return True, signer
    except Exception:
        return False, None


def cmd_guard():
    # Step 1: kernel content integrity.
    if cmd_verify(quiet=True) != 0:
        print("GUARD FAIL: kernel tamper")
        return 3
    seal = _load_seal()
    # Step 2: arming is NOT a stored boolean (agent can edit it) and NOT an env token (agent sets env).
    # The ONLY honest arm signal is a HUMAN git SIGNED tag over the current combined_hash, re-verified
    # LIVE here. guard ignores seal['armed'] entirely. Fail-closed otherwise. (ULTRAPLAN R1/R2/R8.)
    ok, signer = _verify_signed_tag(seal["combined_hash"])
    if not ok:
        print(f"GUARD DISARMED: no valid human-signed tag '{_seal_tag(seal['combined_hash'])}' for the "
              "current kernel. Arming requires `git tag -s` with a key the agent does NOT hold; neither "
              "an env var nor a hand-edited 'armed' flag can arm. Mutation loops MUST NOT run.")
        return 4
    print(f"GUARD PASS (kernel intact + human-signed tag verified: {signer})")
    return 0


def cmd_status():
    seal = _load_seal()
    print(json.dumps({"status": seal.get("status"), "armed": seal.get("armed"),
                      "combined_hash": seal.get("combined_hash"),
                      "approved_by": seal.get("approved_by"),
                      "scripts_manifest": seal.get("scripts_manifest")}, indent=2))
    return 0


def cmd_reseal(token, by):
    # Arming is a HUMAN action. The agent cannot reseal: it cannot create a valid signed tag.
    if cmd_verify(quiet=True) != 0:
        print("RESEAL REFUSED: kernel tamper present; resolve before sealing.")
        return 3
    seal = _load_seal()
    ch = seal["combined_hash"]
    ok, signer = _verify_signed_tag(ch)
    if not ok:
        tag = _seal_tag(ch)
        print("RESEAL REQUIRES A HUMAN-SIGNED TAG (the agent cannot do this — it holds no signing key):")
        print(f"  git tag -s {tag} -m \"approve kernel {ch}\"")
        print(f"  git tag -v {tag}        # must show a Good signature")
        print("Then re-run reseal. Without a verifiable signed tag the kernel stays DISARMED.")
        return 2
    seal["status"] = "HUMAN_SEALED"
    seal["armed"] = True                 # informational only; guard re-derives from the live signed tag
    seal["seal_tag"] = _seal_tag(ch)
    seal["approved_by"] = signer
    seal["approved_ts"] = int(time.time())
    seal["git_commit"] = _git_commit()
    with open(SEAL, "w", encoding="utf-8") as f:
        json.dump(seal, f, indent=2)
        f.write("\n")
    print("KERNEL RESEALED (human-signed tag verified):", signer)
    return 0


def cmd_restore():
    for fn in ["evolution/kernel/fitness.yaml", "evolution/kernel/gates.lock.yaml",
               "evolution/kernel/meta.yaml", "quality-gates/gate-definitions.yaml"]:
        subprocess.call(["git", "-C", REPO, "checkout", "--", fn])
    print("RESTORED kernel files from git HEAD")
    return 0


def main():
    ap = argparse.ArgumentParser(description="HRM Evolution Layer kernel root-of-trust")
    ap.add_argument("cmd", choices=["write", "verify", "guard", "status", "reseal", "restore"])
    ap.add_argument("--token", default=None, help="(DEPRECATED, IGNORED — arming requires a git signed tag)")
    ap.add_argument("--by", default=None, help="(DEPRECATED, IGNORED — signer is read from the verified tag)")
    a = ap.parse_args()
    sys.exit({"write": cmd_write, "verify": cmd_verify, "guard": cmd_guard,
              "status": cmd_status, "restore": cmd_restore,
              "reseal": lambda: cmd_reseal(a.token, a.by)}[a.cmd]())


if __name__ == "__main__":
    main()
