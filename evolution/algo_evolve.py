#!/usr/bin/env python3
"""algo_evolve.py — L2 self-modification harness (DET orchestration; the rewrite is PROT). STDLIB-ONLY.

DGM-style: HRM proposes a BOUNDED change to its OWN selection logic (hrm-agent/technique-selector.md).
The reflective rewrite is algo_evolve.md (the model); this DET harness produces a reproducible candidate
(a benign ADDITIVE mutation in a mutable region), diffs it, and GATES it:
  - kernel must verify INTACT (the candidate is a COPY in selector_logic/; the live file is untouched);
  - H2/H4 immutable tokens preserved (lineage_audit --check-rewrite: 5 dims + 4 phase headers);
  - (Phase 5) canary zero-regression + (this) human-confirm. NEVER promotes (kernel disarmed; first N
    L2 promotions human-gated). Candidate + chained lineage event recorded.
Usage:
  python evolution/algo_evolve.py --propose
  python evolution/algo_evolve.py --validate --candidate <file>
"""
import sys, os, json, subprocess, argparse, difflib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
SELECTOR = os.path.join(SQUAD, "hrm-agent", "technique-selector.md")
OUTDIR = os.path.join(SQUAD, "data", "registries", "evolution", "selector_logic")
LINEAGE = os.path.join(SQUAD, "data", "registries", "evolution", "lineage.jsonl")
HL = os.path.join(HERE, "harness_lock.py")
LA = os.path.join(HERE, "lineage_audit.py")
IMMUTABLE = ["task_fit", "quality_impact", "efficiency", "composability", "familiarity",
             "Phase 1:", "Phase 2:", "Phase 3:", "Phase 4:"]


def _last_hash():
    if not os.path.exists(LINEAGE):
        return "GENESIS"
    last = "GENESIS"
    for ln in open(LINEAGE, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                last = json.loads(ln).get("line_hash", last)
            except json.JSONDecodeError:
                pass
    return last


def append_lineage(event):
    prev = _last_hash()
    event["prev_line_hash"] = prev
    event["line_hash"] = "sha256:" + hashlib.sha256((prev + json.dumps(event, sort_keys=True)).encode()).hexdigest()[:16]
    with open(LINEAGE, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(event) + "\n")


def verify_kernel():
    return subprocess.run([sys.executable, HL, "verify"], capture_output=True).returncode == 0


def check_rewrite(candpath):
    return subprocess.run([sys.executable, LA, "--check-rewrite", "--base", SELECTOR,
                           "--candidate", candpath, "--require", ",".join(IMMUTABLE)],
                          capture_output=True, text=True).returncode == 0


def propose():
    os.makedirs(OUTDIR, exist_ok=True)
    base = open(SELECTOR, encoding="utf-8").read()
    # Bounded ADDITIVE mutation in a mutable region (Phase 2 Filter Rules). Preserves all immutable
    # tokens (the kernel-frozen dimension names + 4-phase flow). The live file is NOT modified.
    marker = "### Filter Rules"
    add = ("\n\n# [L2-candidate] heuristic: deprioritize techniques whose memory.success_rate < 0.2 over\n"
           "# the last 20 uses (frees budget for higher-yield techniques). Additive; bounded; reversible.")
    cand = base.replace(marker, marker + add, 1) if marker in base else base + add
    vid = "logic_" + hashlib.sha256(cand.encode()).hexdigest()[:8]
    candpath = os.path.join(OUTDIR, vid + ".md")
    open(candpath, "w", encoding="utf-8", newline="").write(cand)
    diff = list(difflib.unified_diff(base.splitlines(), cand.splitlines(),
                                     "technique-selector.md(base)", vid + "(candidate)", lineterm=""))
    kok = verify_kernel()
    chk = check_rewrite(candpath)
    already = False                              # dedup: identical content-addressed variant already logged?
    if os.path.exists(LINEAGE):
        for ln in open(LINEAGE, encoding="utf-8"):
            try:
                ev = json.loads(ln)
                if ev.get("event") == "logic_rewrite" and ev.get("variant") == vid:
                    already = True
            except json.JSONDecodeError:
                pass
    if not already:
        append_lineage({"loop": "L2", "event": "logic_rewrite", "target": "hrm-agent/technique-selector.md",
                        "variant": vid, "plan_version": "v1", "trigger": "on_stagnation",
                        "kernel_hash_ok": kok, "checks_passed": chk, "human_confirm_required": True,
                        "promoted": False})
    print(json.dumps({"variant": vid, "duplicate_of_prior_proposal": already, "diff_preview": diff[:10], "kernel_intact": kok,
                      "immutable_tokens_preserved": chk, "promoted": False, "human_confirm_required": True,
                      "decision": "SHADOW — archived; needs canary zero-regression + human confirm "
                                  "(first 5 L2 promotions human-gated); kernel disarmed"}, indent=2))
    return 0 if (kok and chk) else 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--candidate", default=None)
    a = ap.parse_args()
    if a.validate and a.candidate:
        ok = check_rewrite(a.candidate)
        print(json.dumps({"candidate": a.candidate, "immutable_tokens_preserved": ok,
                          "verdict": "OK" if ok else "BLOCKED (H2 CHECK_DELETION)"}))
        return 0 if ok else 6
    if a.propose:
        return propose()
    print("use --propose or --validate --candidate <file>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
