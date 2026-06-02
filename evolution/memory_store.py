#!/usr/bin/env python3
"""memory_store.py — persist technique success rates (EMA). STDLIB-ONLY.

Lights the technique-selector.md familiarity stub: `memory.success_rate(id)` now reads a real value
from data/metrics/technique_success.json instead of being undefined. L0 calls --bump after each
pipeline; Phase 3 (Score) reads --get. EMA (not win/uses ratio) so the signal ADAPTS to recent use.
  --bump <id> --success | --fail   EMA update
  --get <id>                        print success_rate (default 0.0 if unseen)
  --familiarity <id>                print success_rate, familiarity(=rate*100), contribution(=*0.05)
"""
import sys, os, json, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
STORE = os.path.join(SQUAD, "data", "metrics", "technique_success.json")
KERNEL_FIT = os.path.join(HERE, "kernel", "fitness.yaml")
SEAL = os.path.join(HERE, "kernel", "kernel.seal.json")
FAMILIARITY_WEIGHT = 0.05   # technique-selector.md Phase 3 Score 5 weight


def ema_alpha():
    if os.path.exists(KERNEL_FIT):
        for ln in open(KERNEL_FIT, encoding="utf-8"):
            s = ln.strip()
            if s.startswith("ema_alpha:"):
                try:
                    return float(s.split(":", 1)[1].strip().strip('"'))
                except ValueError:
                    pass
    return 0.2


def metric_hash():
    if os.path.exists(SEAL):
        return json.load(open(SEAL, encoding="utf-8")).get("components", {}).get("fitness_hash")
    return None


def load():
    # COLD-START SENTINEL: `_metric_hash: null` + `techniques: {}` means "never written". Any write
    # binds `_metric_hash` to the current kernel fitness_hash (see save), so a POPULATED store always
    # carries the kernel hash it was written under — a consumer can thus distinguish cold-start (null)
    # from a real store written under a known kernel.
    if os.path.exists(STORE):
        return json.load(open(STORE, encoding="utf-8"))
    return {"_schema_version": "1.0", "_metric_hash": metric_hash(), "techniques": {}}


def save(d):
    d["_metric_hash"] = metric_hash()
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    json.dump(d, open(STORE, "w", encoding="utf-8"), indent=2)


def success_rate(d, tid):
    return d["techniques"].get(tid, {}).get("success_rate", 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bump"); ap.add_argument("--success", action="store_true")
    ap.add_argument("--fail", action="store_true")
    ap.add_argument("--get"); ap.add_argument("--familiarity")
    a = ap.parse_args()
    d = load()

    if a.bump:
        a_ = ema_alpha()
        t = d["techniques"].setdefault(a.bump, {"success_rate": 0.0, "uses": 0, "wins": 0,
                                                "ema_alpha": a_, "last_used": None})
        verdict = 1.0 if a.success else 0.0
        t["success_rate"] = round((1 - a_) * t["success_rate"] + a_ * verdict, 6)
        t["uses"] += 1
        t["wins"] += int(a.success)
        t["last_used"] = int(time.time())
        save(d)
        print(json.dumps({"technique": a.bump, "success_rate": t["success_rate"], "uses": t["uses"],
                          "familiarity_contribution": round(t["success_rate"] * 100 * FAMILIARITY_WEIGHT, 4)}))
        return 0

    if a.get:
        print(round(success_rate(d, a.get), 6))
        return 0

    if a.familiarity:
        r = success_rate(d, a.familiarity)
        print(json.dumps({"technique": a.familiarity, "success_rate": round(r, 6),
                          "familiarity": round(r * 100, 4),
                          "contribution_to_total": round(r * 100 * FAMILIARITY_WEIGHT, 4)}))
        return 0

    print(json.dumps(d, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
