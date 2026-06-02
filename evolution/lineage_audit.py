#!/usr/bin/env python3
"""lineage_audit.py — validate the append-only CHAINED lineage (ULTRAPLAN R12 / H1-H7 backbone).
STDLIB-ONLY. Re-walks data/registries/evolution/lineage.jsonl and asserts, for each line:
  (1) prev_line_hash == the prior line's line_hash (chain continuity), and
  (2) line_hash == sha256(prev_line_hash + json(event without line_hash))  (not silently rewritten).
A rewound/edited/forged lineage breaks the chain. Exit 0 = intact, 6 = broken.
Usage: python evolution/lineage_audit.py
"""
import sys, os, json, hashlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
LINEAGE = os.path.join(SQUAD, "data", "registries", "evolution", "lineage.jsonl")


def recompute(event, prev):
    e = {k: v for k, v in event.items() if k != "line_hash"}
    payload = json.dumps(e, sort_keys=True)
    return "sha256:" + hashlib.sha256((prev + payload).encode()).hexdigest()[:16]


def audit_chain():
    if not os.path.exists(LINEAGE):
        print("LINEAGE EMPTY (no file yet)")
        return 0
    prev = "GENESIS"
    n = 0
    with open(LINEAGE, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            n += 1
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                print(f"CHAIN BREAK at line {n}: invalid JSON")
                return 6
            if ev.get("prev_line_hash") != prev:
                print(f"CHAIN BREAK at line {n}: prev_line_hash {ev.get('prev_line_hash')} != expected {prev}")
                return 6
            expect = recompute(ev, prev)
            if ev.get("line_hash") != expect:
                print(f"HASH MISMATCH at line {n}: recorded {ev.get('line_hash')} != recomputed {expect} (rewritten?)")
                return 6
            prev = ev["line_hash"]
    print(f"LINEAGE INTACT: {n} entries, chain verified end-to-end")
    return 0


def check_rewrite(base, candidate, require):
    """H2 CHECK_DELETION (the DGM cautionary analog) + H4 surface guard for an L2 logic rewrite.
    A candidate must NOT remove any kernel-immutable token (a scoring dimension name, a phase header,
    a required gate/check/rubric line). exit 6 if any required token's count drops vs the base."""
    bt = open(base, encoding="utf-8").read()
    ct = open(candidate, encoding="utf-8").read()
    violations = [tok for tok in require if ct.count(tok) < bt.count(tok)]
    if violations:
        print("H2 CHECK_DELETION: candidate removed immutable token(s): " + ", ".join(violations))
        return 6
    print(f"REWRITE OK: all {len(require)} required immutable tokens preserved")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-rewrite", action="store_true")
    ap.add_argument("--base"); ap.add_argument("--candidate"); ap.add_argument("--require", default="")
    a = ap.parse_args()
    if a.check_rewrite:
        req = [t.strip() for t in a.require.split(",") if t.strip()]
        sys.exit(check_rewrite(a.base, a.candidate, req))
    sys.exit(audit_chain())


if __name__ == "__main__":
    main()

