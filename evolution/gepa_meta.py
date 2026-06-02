#!/usr/bin/env python3
"""gepa_meta.py — L1 GEPA generation harness (DET orchestration). STDLIB-ONLY.

The reflective MUTATION is a PROT step (gepa_meta.md, the LLM proposes a change from traces). This DET
harness makes the loop reproducible + verifiable: it applies a SEEDED weight perturbation as a stand-in
candidate, validates the kernel invariant Σweights==1.0, archives the candidate with chained lineage,
and attaches a shadow fitness (fitness.py). It NEVER promotes — promotion is canary-gated (Phase 5) and
the kernel is DISARMED (guard). While disarmed it runs in shadow/archive-only mode (ULTRAPLAN B0).
Usage: python evolution/gepa_meta.py --generations 3 --seed 1337
"""
import sys, os, json, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
SELCONF = os.path.join(HERE, "selector_config.yaml")
HL = os.path.join(HERE, "harness_lock.py")
ARCHIVE = os.path.join(HERE, "archive.py")
FITNESS = os.path.join(HERE, "fitness.py")
DIMS = ["task_fit", "quality_impact", "efficiency", "composability", "familiarity"]


def load_weights():
    w, inblock = {}, False
    for ln in open(SELCONF, encoding="utf-8"):
        s = ln.strip()
        if s.startswith("weights:"):
            inblock = True
            continue
        if inblock:
            if ":" in s and s.split(":", 1)[0].strip() in DIMS:
                w[s.split(":", 1)[0].strip()] = float(s.split(":", 1)[1].strip())
            elif s and not s.startswith("#") and ":" in s and s.split(":", 1)[0].strip() not in DIMS:
                break
    return w


def perturb(w, gen):
    # deterministic, seeded-by-generation: move delta from 'efficiency' to 'familiarity' (bounded)
    c = dict(w)
    delta = round(0.02 * ((gen % 3) + 1), 4)
    if c.get("efficiency", 0) - delta >= 0.05:
        c["efficiency"] = round(c["efficiency"] - delta, 4)
        c["familiarity"] = round(c["familiarity"] + delta, 4)
    # renormalize defensively to keep the kernel invariant Σ==1.0
    total = sum(c.values())
    for k in c:
        c[k] = round(c[k] / total, 6)
    # fix rounding drift onto the largest dim
    drift = round(1.0 - sum(c.values()), 6)
    big = max(c, key=c.get)
    c[big] = round(c[big] + drift, 6)
    return c


def disarmed():
    return subprocess.run([sys.executable, HL, "guard"], capture_output=True).returncode != 0


def shadow_fitness(seed):
    r = subprocess.run([sys.executable, FITNESS, "--seed-demo", "--seed", str(seed)],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"ci_lower": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generations", type=int, default=3)
    ap.add_argument("--seed", type=int, default=1337)
    a = ap.parse_args()
    base = load_weights()
    assert abs(sum(base.values()) - 1.0) < 1e-6, "incumbent weights must sum to 1.0"
    shadow = disarmed()
    # seed the archive with the incumbent genome (v1) if empty
    subprocess.run([sys.executable, ARCHIVE, "--add", "--variant-id", "sel_v1", "--score", "0.80",
                    "--quality", "0.80", "--diversity", "0.30"], capture_output=True, text=True)
    fit = shadow_fitness(a.seed)
    candidates = []
    for g in range(1, a.generations + 1):
        cand = perturb(base, g)
        s = round(sum(cand.values()), 6)
        if abs(s - 1.0) > 1e-6:
            print(json.dumps({"gen": g, "rejected": f"Σweights={s} != 1.0 (kernel invariant)"}))
            continue
        vid = f"sel_g{g}"
        subprocess.run([sys.executable, ARCHIVE, "--add", "--variant-id", vid, "--parent", "sel_v1",
                        "--score", "0.80", "--novelty", "0.3", "--quality", "0.80", "--diversity", "0.30"],
                       capture_output=True, text=True)
        candidates.append({"variant_id": vid, "weights": cand, "weights_sum": s,
                           "shadow_ci_lower": fit.get("ci_lower"), "promoted": False})
    print(json.dumps({"mode": "shadow/archive-only (kernel DISARMED)" if shadow else "armed",
                      "incumbent": base, "generations": a.generations,
                      "candidates": candidates,
                      "note": "candidates archived with lineage; NONE promoted (canary-gated, Phase 5). "
                              "Real genome->fitness coupling needs live pipeline rollouts (disarmed here)."},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
