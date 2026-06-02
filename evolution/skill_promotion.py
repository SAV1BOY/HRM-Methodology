#!/usr/bin/env python3
"""skill_promotion.py — Voyager cross-squad skill promotion (Section 19, ULTRAPLAN §8.4). STDLIB-ONLY.

Promotes a crystallized skill from a squad's lib/skill_library/learned to the SHARED cross-squad library
(Squad HRM/lib/learned-shared) when it is GENERIC: quality_gate_pass AND (used_in_squads>=2 OR
generality_score>=0.7 OR --manual). Dedup by sha256 fingerprint: exact-match -> increment used_in_squads
(no duplicate); else register. Never silent-delete (anti-DGM). Registers in registry/learned-skills.yaml.
  python evolution/skill_promotion.py --id parse-burp-xml --origin cybersecurity-squad \
     --fingerprint sha256:9a2c --generality 0.78 --used-in cybersecurity-squad,data-squad
"""
import sys, os, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
SHARED = os.path.join(SQUAD, "lib", "learned-shared")
REG = os.path.join(SQUAD, "registry", "learned-skills.yaml")
SIDE = REG + ".json"


def load():
    if os.path.exists(SIDE):
        return json.load(open(SIDE, encoding="utf-8"))
    return {"learned_skills": []}


def _atomic_write(path, text):
    tmp = path + ".tmp"
    open(tmp, "w", encoding="utf-8", newline="").write(text)
    os.replace(tmp, path)                      # atomic on the same filesystem (no torn/half-written file)


def save(d):
    _atomic_write(SIDE, json.dumps(d, indent=2))
    lines = ["# registry/learned-skills.yaml — cross-squad Voyager library (auto; dedup by fingerprint).",
             "learned_skills:"]
    for e in d["learned_skills"]:
        lines += [f"  - id: {e['id']}", f"    fingerprint: {e['fingerprint']}",
                  f"    origin_squad: {e['origin_squad']}", f"    generality_score: {e['generality_score']}",
                  f"    used_in_squads: {e['used_in_squads']}", f"    file: {e['file']}",
                  f"    quality_gate_pass: {str(e['quality_gate_pass']).lower()}"]
    _atomic_write(REG, "\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True); ap.add_argument("--origin", required=True)
    ap.add_argument("--fingerprint", required=True); ap.add_argument("--generality", type=float, default=0.0)
    ap.add_argument("--used-in", default=""); ap.add_argument("--manual", action="store_true")
    ap.add_argument("--quality-gate-pass", default="true")
    a = ap.parse_args()
    used = [s for s in a.used_in.split(",") if s.strip()]
    qgp = a.quality_gate_pass.lower() in ("true", "1", "yes")
    d = load()
    # DEDUP FIRST (before the generic gate): a resubmission of an already-promoted fingerprint merges
    # usage — never re-rejected by the gate, never duplicated, never silent-deleted (anti-DGM).
    for e in d["learned_skills"]:
        if e["fingerprint"] == a.fingerprint:
            for s in used:
                if s not in e["used_in_squads"]:
                    e["used_in_squads"].append(s)
            save(d)
            print(json.dumps({"promoted": False, "dedup": True, "id": e["id"],
                              "used_in_squads": e["used_in_squads"], "note": "exact fingerprint exists; merged usage"}))
            return 0
    # NEW entry must clear the generic gate
    generic = qgp and (len(used) >= 2 or a.generality >= 0.7 or a.manual)
    if not generic:
        print(json.dumps({"promoted": False, "reason": "not generic (need quality_gate_pass AND "
                          "(used_in>=2 OR generality>=0.7 OR --manual))"}))
        return 2
    os.makedirs(SHARED, exist_ok=True)
    rel = f"lib/learned-shared/{a.id}.md"
    open(os.path.join(SHARED, a.id + ".md"), "w", encoding="utf-8", newline="").write(
        f"# {a.id} (cross-squad)\n\nPromoted from {a.origin}. generality_score={a.generality}. "
        f"fingerprint={a.fingerprint}.\nUsed in: {', '.join(used) or a.origin}\n")
    d["learned_skills"].append({"id": a.id, "fingerprint": a.fingerprint, "origin_squad": a.origin,
                                "generality_score": a.generality, "used_in_squads": used or [a.origin],
                                "file": rel, "quality_gate_pass": qgp})
    save(d)
    print(json.dumps({"promoted": True, "id": a.id, "file": rel, "shared_library": "lib/learned-shared/"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
