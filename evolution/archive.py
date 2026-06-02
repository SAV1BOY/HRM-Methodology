#!/usr/bin/env python3
"""archive.py — evolutionary archive with chained lineage + Pareto front. STDLIB-ONLY.

- keep_stepping_stones: ancestors are NEVER removed (update_policy keep_all); they stay selectable.
- Adding a child bumps the parent's `children` count (feeds selection.py's 1/(children+1) damping).
- lineage.jsonl is append-only AND chained (prev_line_hash): a silent rewrite breaks the chain (R12).
- Pareto front over objectives {quality, -cost, -latency, diversity} (all treated as maximize).
Usage:
  python evolution/archive.py --seed-demo
  python evolution/archive.py --add --variant-id g_07 --parent g_03 --score 0.83 --novelty 0.4 \
        --quality 0.83 --cost 0.2 --latency 0.1 --diversity 0.4
"""
import sys, os, json, hashlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
EVDIR = os.path.join(SQUAD, "data", "registries", "evolution")
ARCHIVE = os.path.join(EVDIR, "archive.json")
ARCHIVE_YAML = os.path.join(EVDIR, "archive.yaml")
LINEAGE = os.path.join(EVDIR, "lineage.jsonl")


def load():
    if os.path.exists(ARCHIVE):
        return json.load(open(ARCHIVE, encoding="utf-8"))
    return {"variants": []}


def _dominates(a, b):
    # objectives stored already as maximize: quality, ncost(=-cost), nlatency(=-latency), diversity
    keys = ("quality", "ncost", "nlatency", "diversity")
    ge = all(a["obj"].get(k, 0) >= b["obj"].get(k, 0) for k in keys)
    gt = any(a["obj"].get(k, 0) > b["obj"].get(k, 0) for k in keys)
    return ge and gt


def recompute_pareto(arch):
    vs = arch["variants"]
    for v in vs:
        v["on_pareto_front"] = not any(_dominates(o, v) for o in vs if o is not v)


def _y(x):
    # emit YAML-native scalars so the human mirror round-trips to the same values as archive.json
    if x is None:
        return "null"
    if x is True:
        return "true"
    if x is False:
        return "false"
    return str(x)


def save(arch):
    recompute_pareto(arch)
    json.dump(arch, open(ARCHIVE, "w", encoding="utf-8"), indent=2)
    lines = ["# Evolution archive (Pareto, keep_stepping_stones). Canonical JSON: archive.json", "variants:"]
    for v in arch["variants"]:
        lines += [f"  - variant_id: {v['variant_id']}", f"    parent_id: {_y(v.get('parent_id'))}",
                  f"    score: {v['score']}", f"    children: {v.get('children', 0)}",
                  f"    novelty: {v.get('novelty', 0.0)}", f"    on_pareto_front: {_y(v.get('on_pareto_front'))}"]
    open(ARCHIVE_YAML, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")


def last_line_hash():
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
    prev = last_line_hash()
    event["prev_line_hash"] = prev
    payload = json.dumps(event, sort_keys=True)
    event["line_hash"] = "sha256:" + hashlib.sha256((prev + payload).encode()).hexdigest()[:16]
    with open(LINEAGE, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(event) + "\n")


def add(vid, parent, score, novelty, obj):
    arch = load()
    if any(v["variant_id"] == vid for v in arch["variants"]):
        print(f"NO-OP: {vid} already in archive (keep_all)")
        return
    arch["variants"].append({"variant_id": vid, "parent_id": parent, "score": score,
                             "novelty": novelty, "children": 0, "obj": obj})
    for v in arch["variants"]:               # keep_stepping_stones: bump parent, never remove
        if v["variant_id"] == parent:
            v["children"] = v.get("children", 0) + 1
    save(arch)
    append_lineage({"loop": "L1", "event": "add_variant", "variant_id": vid, "parent_id": parent,
                    "score": score, "novelty": novelty})
    print(f"ADDED {vid} (parent={parent}, score={score}); parent children bumped; lineage chained")


def seed_demo():
    for p in (ARCHIVE, ARCHIVE_YAML, LINEAGE):
        if os.path.exists(p):
            os.remove(p)
    os.makedirs(EVDIR, exist_ok=True)
    save({"variants": []})
    # g_a: 0.6 / 0 children ; g_b: 0.8 / 0 children ; g_c: 0.8 but already 5 children (over-explored)
    add("g_a", None, 0.6, 0.0, {"quality": 0.6, "ncost": -0.2, "nlatency": -0.1, "diversity": 0.5})
    add("g_b", "g_a", 0.8, 0.0, {"quality": 0.8, "ncost": -0.2, "nlatency": -0.1, "diversity": 0.3})
    add("g_c", "g_a", 0.8, 0.0, {"quality": 0.8, "ncost": -0.5, "nlatency": -0.3, "diversity": 0.2})
    arch = load()
    for v in arch["variants"]:               # force g_c to look over-explored (5 children)
        if v["variant_id"] == "g_c":
            v["children"] = 5
    save(arch)
    arch = load()
    desc = ", ".join(f"{v['variant_id']}({v['score']},ch{v.get('children', 0)})" for v in arch["variants"])
    print("SEEDED demo archive: " + desc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-demo", action="store_true")
    ap.add_argument("--add", action="store_true")
    ap.add_argument("--variant-id"); ap.add_argument("--parent", default=None)
    ap.add_argument("--score", type=float); ap.add_argument("--novelty", type=float, default=0.0)
    ap.add_argument("--quality", type=float, default=0.0); ap.add_argument("--cost", type=float, default=0.0)
    ap.add_argument("--latency", type=float, default=0.0); ap.add_argument("--diversity", type=float, default=0.0)
    a = ap.parse_args()
    if a.seed_demo:
        seed_demo(); return 0
    if a.add:
        obj = {"quality": a.quality, "ncost": -a.cost, "nlatency": -a.latency, "diversity": a.diversity}
        add(a.variant_id, a.parent, a.score, a.novelty, obj); return 0
    print(json.dumps(load(), indent=2)); return 0


if __name__ == "__main__":
    sys.exit(main())
