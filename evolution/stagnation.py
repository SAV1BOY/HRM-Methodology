#!/usr/bin/env python3
"""stagnation.py — L1/L2 stagnation detector. STDLIB-ONLY.

level1_breach: no NEW best fitness in the last `level1_patience` attempts (improvement <= epsilon),
               OR diversity below floor.
level2_breach: the no-improvement run reaches `level2_patience` attempts (escalate to L2 meta).
Patience/floor come from evolution/kernel/meta.yaml. Series from --series or the archive score history
(data/registries/evolution/archive.json) or data/metrics/evolution_log.tsv gate_score.
Usage:
  python evolution/stagnation.py --series 0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8
  python evolution/stagnation.py            # reads archive scores, else evolution_log gate_score
"""
import sys, os, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
META = os.path.join(HERE, "kernel", "meta.yaml")
ARCHIVE = os.path.join(SQUAD, "data", "registries", "evolution", "archive.json")
LOG = os.path.join(SQUAD, "data", "metrics", "evolution_log.tsv")
EPSILON = 0.005


def params():
    p = {"level1_patience": 10, "level2_patience": 50, "diversity_floor": 0.40}
    if os.path.exists(META):
        for ln in open(META, encoding="utf-8"):
            s = ln.strip()
            for k in p:
                if s.startswith(k + ":"):
                    try:
                        p[k] = float(s.split(":", 1)[1].strip().strip('"'))
                    except ValueError:
                        pass
    p["level1_patience"] = int(p["level1_patience"])
    p["level2_patience"] = int(p["level2_patience"])
    return p


def series_from_archive():
    if not os.path.exists(ARCHIVE):
        return []
    return [v["score"] for v in json.load(open(ARCHIVE, encoding="utf-8")).get("variants", [])]


def series_from_log():
    if not os.path.exists(LOG):
        return []
    out = []
    with open(LOG, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        gi = header.index("gate_score") if "gate_score" in header else None
        if gi is None:
            return []
        for ln in f:
            cells = ln.rstrip("\n").split("\t")
            if len(cells) > gi and cells[gi] not in ("", "NA"):
                out.append(float(cells[gi]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default=None, help="comma-separated fitness series")
    ap.add_argument("--diversity", type=float, default=None)
    a = ap.parse_args()
    p = params()
    if a.series:
        series = [float(x) for x in a.series.split(",") if x.strip() != ""]
    else:
        series = series_from_archive() or series_from_log()
    if not series:
        print(json.dumps({"verdict": "no_data"}))
        return 0
    n = len(series)
    best_so_far = series[0]
    last_meaningful = 0
    for i in range(1, n):
        if series[i] - best_so_far > EPSILON:     # only a > epsilon jump is a REAL improvement
            last_meaningful = i
            best_so_far = series[i]
        elif series[i] > best_so_far:             # track true max; sub-epsilon creep is NOT improvement
            best_so_far = series[i]
    attempts_since_best = (n - 1) - last_meaningful
    best = best_so_far
    level1 = attempts_since_best >= p["level1_patience"]
    level2 = attempts_since_best >= p["level2_patience"]
    if a.diversity is not None and a.diversity < p["diversity_floor"]:
        level1 = True
    verdict = "fire_l2" if level2 else "fire_l1" if level1 else "continue"
    print(json.dumps({"verdict": verdict, "level1_breach": level1, "level2_breach": level2,
                      "attempts_since_best": attempts_since_best, "n": n, "best": best,
                      "level1_patience": p["level1_patience"], "level2_patience": p["level2_patience"],
                      "epsilon": EPSILON}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
