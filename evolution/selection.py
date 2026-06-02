#!/usr/bin/env python3
"""selection.py — score_child_prop parent selection over the evolution archive. STDLIB-ONLY.

P(i) proportional to  sigmoid(score_i) * 1/(children_i + 1) * (1 + novelty_weight * novelty_i),
normalized over the whole archive. The 1/(children+1) term damps over-explored genomes; the novelty
term rewards diversity — together they keep open-ended search from collapsing onto the current best.
Reusable by HRM L1 (Phase 4). novelty_weight defaults from evolution/kernel/meta.yaml.

Usage:
  python evolution/selection.py --sample 1000 --seed 1337     # histogram: sampled vs expected
  python evolution/selection.py --emit parent --seed 1337     # emit one parent_id + trace
"""
import sys, os, json, math, random, argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))           # evolution/
SQUAD = os.path.dirname(HERE)
ARCHIVE = os.path.join(SQUAD, "data", "registries", "evolution", "archive.json")
META = os.path.join(HERE, "kernel", "meta.yaml")
FIT = os.path.join(HERE, "kernel", "fitness.yaml")


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def default_novelty_weight():
    if os.path.exists(META):
        for ln in open(META, encoding="utf-8"):
            s = ln.strip()
            if s.startswith("novelty_weight:"):
                try:
                    return float(s.split(":", 1)[1].strip().strip('"'))
                except ValueError:
                    pass
    return 0.30


def kernel_drives_fitness():
    """False => the kernel's fitness metric is conformance/LOG-ONLY (drives_fitness:false); selection
    must REFUSE to optimize it (ULTRAPLAN §6.4 / Phase-1 audit). Default True if the field is absent."""
    if not os.path.exists(FIT):
        return True
    val = True
    for ln in open(FIT, encoding="utf-8"):
        s = ln.strip()
        if s.startswith("#") or ":" not in s:
            continue
        if s.split(":", 1)[0].strip() == "drives_fitness":
            val = s.split(":", 1)[1].strip().strip('"').lower() in ("true", "1", "yes")
    return val


def load_archive():
    if not os.path.exists(ARCHIVE):
        return []
    return json.load(open(ARCHIVE, encoding="utf-8")).get("variants", [])


def weights(arch, nw):
    return [sigmoid(v["score"]) * (1.0 / (v.get("children", 0) + 1)) * (1 + nw * v.get("novelty", 0.0))
            for v in arch]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--emit", choices=["parent"], default=None)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--novelty-weight", type=float, default=None)
    ap.add_argument("--exploration-only", action="store_true",
                    help="required when the kernel metric is drives_fitness:false (log-only)")
    a = ap.parse_args()
    arch = load_archive()
    if not arch:
        print(json.dumps({"error": "empty archive — run archive.py --seed-demo or --add first"}))
        return 1
    if not kernel_drives_fitness() and not a.exploration_only:
        print(json.dumps({"refused": True, "selection_note": "LOG ONLY",
                          "reason": "kernel fitness_metric has drives_fitness:false (conformance / pending "
                                    "external-outcome pair). Selection MUST NOT optimize this metric. Re-run "
                                    "with --exploration-only for archive exploration; promotion stays barred "
                                    "until an external KPI is instrumented and the kernel is re-sealed."}, indent=2))
        return 2
    nw = a.novelty_weight if a.novelty_weight is not None else default_novelty_weight()
    ws = weights(arch, nw)
    total = sum(ws)
    probs = {v["variant_id"]: w / total for v, w in zip(arch, ws)}
    cum, c = [], 0.0
    for w in ws:
        c += w / total
        cum.append(c)

    if a.sample > 0:
        random.seed(a.seed)
        counts = Counter()
        for _ in range(a.sample):
            r = random.random()
            for v, cc in zip(arch, cum):
                if r <= cc or v is arch[-1]:   # force final bucket (float cum may end < 1.0)
                    counts[v["variant_id"]] += 1
                    break
        hist = {v["variant_id"]: {"score": v["score"], "children": v.get("children", 0),
                                  "novelty": v.get("novelty", 0.0),
                                  "expected_prob": round(probs[v["variant_id"]], 4),
                                  "sampled_frac": round(counts[v["variant_id"]] / a.sample, 4),
                                  "sampled": counts[v["variant_id"]]} for v in arch}
        print(json.dumps({"n": a.sample, "seed": a.seed, "novelty_weight": nw, "histogram": hist}, indent=2))
        return 0

    if a.emit == "parent":
        random.seed(a.seed)
        r = random.random()
        for v, cc in zip(arch, cum):
            if r <= cc or v is arch[-1]:   # force final bucket (float cum may end < 1.0)
                print(json.dumps({"parent_id": v["variant_id"], "seed": a.seed,
                                  "novelty_weight": nw, "prob": round(probs[v["variant_id"]], 4)}))
                return 0

    print(json.dumps({"novelty_weight": nw, "probs": {k: round(v, 4) for k, v in probs.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
