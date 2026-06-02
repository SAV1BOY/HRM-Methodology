#!/usr/bin/env python3
"""canary_suite.py — cross-squad held-out regression gate (Section 19, ULTRAPLAN §7.3/§7.4). STDLIB-ONLY.

A candidate becomes default ONLY if it regresses on NO archetype (regression_ceiling=0.0) AND meets each
archetype's ABSOLUTE threshold (cybersecurity 0.95 HARD). Verifies the kernel first; runs harness_lock
guard — while the kernel is DISARMED a clean candidate is SHADOW-only and is NEVER auto-promoted.
Compares a candidate score file to evolution/canary/baseline.json over evolution/canary/canary_suite.yaml.
Usage: python evolution/canary_suite.py --candidate evolution/canary/_demo_good.json
exit 0 = promotable-on-canary, 5 = PROMOTION BLOCKED, 3 = kernel tamper.
"""
import sys, os, json, re, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))          # evolution
SQUAD = os.path.dirname(HERE)
CANARY = os.path.join(HERE, "canary")
SUITE = os.path.join(CANARY, "canary_suite.yaml")
BASELINE = os.path.join(CANARY, "baseline.json")
HL = os.path.join(HERE, "harness_lock.py")


def load_archetypes():
    out = []
    for ln in open(SUITE, encoding="utf-8"):
        m = re.match(r"\s*-\s*\{id:\s*([^,]+),.*?threshold:\s*([0-9.]+)\}", ln)
        if m:
            out.append((m.group(1).strip(), float(m.group(2))))
    return out


def _rc(*args):
    return subprocess.run([sys.executable, HL, *args], capture_output=True).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    a = ap.parse_args()
    if _rc("verify") != 0:
        print(json.dumps({"abort": "kernel tamper — refusing to evaluate canary"}))
        return 3
    arche = load_archetypes()
    base = json.load(open(BASELINE, encoding="utf-8"))
    cand = json.load(open(a.candidate, encoding="utf-8"))
    per, regressions, floor_fails, missing, baseline_missing = [], [], [], [], []
    for aid, thr in arche:
        b = base.get(aid)
        c = cand.get(aid)
        if c is None:
            missing.append(aid)
            per.append({"archetype": aid, "candidate": None, "status": "MISSING"})
            continue
        if b is None:                                 # fail-closed if suite/baseline drift out of sync
            baseline_missing.append(aid)
            floor = c < thr                           # absolute floor still applies even w/o a baseline
            if floor:
                floor_fails.append({"archetype": aid, "score": c, "threshold": thr})
            per.append({"archetype": aid, "candidate": c, "below_floor": floor, "status": "BASELINE_MISSING"})
            continue
        delta = round(c - b, 4)
        reg = delta < -1e-9
        floor = c < thr
        if reg:
            regressions.append(aid)
        if floor:
            floor_fails.append({"archetype": aid, "score": c, "threshold": thr})
        per.append({"archetype": aid, "baseline": b, "candidate": c, "delta": delta,
                    "threshold": thr, "regressed": reg, "below_floor": floor})
    promotable = not regressions and not floor_fails and not missing and not baseline_missing
    armed = _rc("guard") == 0
    if not promotable:
        decision = "PROMOTION BLOCKED"
    elif not armed:
        decision = "PROMOTABLE on canary -> SHADOW only (kernel DISARMED; pilot/fleet need armed + human)"
    else:
        decision = "PROMOTABLE -> staged rollout (shadow -> 1 pilot -> fleet, human-gated)"
    print(json.dumps({"candidate": os.path.basename(a.candidate), "regression_ceiling": 0.0,
                      "promotable_on_canary": promotable, "armed": armed, "decision": decision,
                      "regressions": regressions, "floor_fails": floor_fails, "missing": missing,
                      "baseline_missing": baseline_missing, "per_archetype": per}, indent=2))
    return 0 if promotable else 5


if __name__ == "__main__":
    sys.exit(main())
