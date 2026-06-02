#!/usr/bin/env python3
"""fitness.py (HRM) — indirect downstream_aggregate_score. STDLIB-ONLY.

DECOMPOSED (C4, anti zero-inflation): per squad s -> pass_rate = mean(gate_pass);
cond_kpi = mean(downstream_kpi_delta | gate_pass==1). Per-squad term = w_s * pass_rate * cond_kpi
(w_s from config.yaml evolution.weights_by_squad). AGGREGATE across squads with min (default) or CVaR
(C3, blocks steer-to-easy-squad). Bootstrap CI over rows (cluster by squad). Promotion needs the CI
LOWER bound to beat the incumbent — and this script NEVER promotes; it only scores + archives.
SAFETY: aborts if `harness_lock.py verify` fails (kernel tamper -> refuse to score), and refuses if the
kernel fitness has drives_fitness:false (log-only). Rows TSV needs: squad, gate_pass, downstream_kpi_delta.
Usage:
  python evolution/fitness.py --rows data/metrics/pipeline_outcomes.tsv
  python evolution/fitness.py --seed-demo    # writes a 2-squad demo rows file + scores it
"""
import sys, os, json, argparse, random, subprocess, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
HL = os.path.join(HERE, "harness_lock.py")
KERNEL_FIT = os.path.join(HERE, "kernel", "fitness.yaml")
SEAL = os.path.join(HERE, "kernel", "kernel.seal.json")
CONFIG = os.path.join(SQUAD, "config.yaml")
DEMO = os.path.join(SQUAD, "data", "metrics", "fitness_demo_rows.tsv")
TRUE = {"1", "true", "True", "yes"}


def kernel_ok():
    try:
        return subprocess.run([sys.executable, HL, "verify"], capture_output=True).returncode == 0
    except Exception:
        return False


def drives_fitness():
    if not os.path.exists(KERNEL_FIT):
        return True
    for ln in open(KERNEL_FIT, encoding="utf-8"):
        s = ln.strip()
        if not s.startswith("#") and s.split(":", 1)[0].strip() == "drives_fitness":
            return s.split(":", 1)[1].strip().strip('"').lower() in ("true", "1", "yes")
    return True


def weights_by_squad():
    w = {"default": 1.0}
    if not os.path.exists(CONFIG):
        return w
    inblock = False
    for ln in open(CONFIG, encoding="utf-8"):
        if ln.strip().startswith("weights_by_squad:"):
            inblock = True
            continue
        if inblock:
            stripped = ln.strip()
            indent = len(ln) - len(ln.lstrip(" "))
            if stripped and not stripped.startswith("#") and indent <= 2:
                break                       # a sibling/parent key (e.g. 'safety:') ends the block
            if indent >= 4 and ":" in stripped and not stripped.startswith("#"):
                k, v = stripped.split(":", 1)
                try:
                    w[k.strip()] = float(v.strip())
                except ValueError:
                    pass
    return w


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(header)}
        for ln in f:
            c = ln.rstrip("\n").split("\t")
            if len(c) < len(header):
                continue
            squad = c[idx["squad"]] if "squad" in idx else "fleet"
            gp = c[idx["gate_pass"]] in TRUE if "gate_pass" in idx else False
            kd = c[idx["downstream_kpi_delta"]] if "downstream_kpi_delta" in idx else "0"
            try:
                kd = float(kd)
            except ValueError:
                kd = 0.0
            rows.append((squad, gp, kd))
    return rows


def aggregate(rows, w, method="min"):
    by = {}
    for sq, gp, kd in rows:
        by.setdefault(sq, []).append((gp, kd))
    terms = []
    for sq, obs in by.items():
        n = len(obs)
        pass_rate = sum(1 for gp, _ in obs if gp) / n
        passed_kd = [kd for gp, kd in obs if gp]
        cond_kpi = (sum(passed_kd) / len(passed_kd)) if passed_kd else 0.0
        ws = w.get(sq, w.get("default", 1.0))
        terms.append(ws * pass_rate * cond_kpi)
    if not terms:
        return 0.0
    if method == "cvar":
        terms.sort()
        k = max(1, len(terms) // 5)          # worst 20%
        return sum(terms[:k]) / k
    return min(terms)


def bootstrap_ci(rows, w, method, n_boot, seed):
    random.seed(seed)
    by = {}
    for r in rows:
        by.setdefault(r[0], []).append(r)
    samples = []
    for _ in range(n_boot):
        resampled = []
        for sq, obs in by.items():                # cluster by squad
            resampled += [random.choice(obs) for _ in range(len(obs))]
        samples.append(aggregate(resampled, w, method))
    samples.sort()
    lo = samples[int(0.025 * len(samples))]
    hi = samples[int(0.975 * len(samples)) - 1]
    return round(lo, 4), round(hi, 4)


def seed_demo():
    os.makedirs(os.path.dirname(DEMO), exist_ok=True)
    rows = [("cybersecurity", 1, 0.10), ("cybersecurity", 1, 0.08), ("cybersecurity", 0, 0.0),
            ("cybersecurity", 1, 0.12), ("data", 1, 0.05), ("data", 1, 0.06), ("data", 0, 0.0),
            ("data", 1, 0.04), ("data", 1, 0.07)]
    with open(DEMO, "w", encoding="utf-8", newline="") as f:
        f.write("squad\tgate_pass\tdownstream_kpi_delta\n")
        for sq, gp, kd in rows:
            f.write(f"{sq}\t{gp}\t{kd}\n")
    print(f"seeded demo rows -> {os.path.relpath(DEMO, SQUAD)} (2 squads, 9 rows)", file=sys.stderr)
    return DEMO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default=os.path.join(SQUAD, "data", "metrics", "pipeline_outcomes.tsv"))
    ap.add_argument("--method", choices=["min", "cvar"], default="min")
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--seed-demo", action="store_true")
    ap.add_argument("--single-bucket", action="store_true",
                    help="allow rows WITHOUT a 'squad' column (collapses to one 'fleet' bucket; DISABLES "
                         "cross-squad min/CVaR steer-to-easy protection — not recommended for the HRM aggregate)")
    a = ap.parse_args()
    if not kernel_ok():
        print(json.dumps({"abort": "kernel verify failed (tamper) — refusing to score"}))
        return 3
    if not drives_fitness():
        print(json.dumps({"refused": "kernel fitness drives_fitness:false (log-only)"}))
        return 2
    rows_path = seed_demo() if a.seed_demo else a.rows
    if not os.path.exists(rows_path):
        print(json.dumps({"error": f"no rows at {rows_path}"}))
        return 1
    header = open(rows_path, encoding="utf-8").readline().rstrip("\n").split("\t")
    if "squad" not in header and not a.single_bucket:
        print(json.dumps({"abort": "rows have no 'squad' column — HRM fitness is INDIRECT and needs "
              "squad-tagged rows for cross-squad min/CVaR (anti steer-to-easy, C3). Pointing this at the "
              "16-col pipeline_outcomes.tsv would collapse all rows to one 'fleet' bucket. Re-run with "
              "--single-bucket only if you explicitly intend a single-bucket score."}))
        return 2
    rows = read_rows(rows_path)
    if not rows:
        print(json.dumps({"n": 0, "note": "no scorable rows yet (HRM fitness is indirect — needs leaf rows)"}))
        return 0
    w = weights_by_squad()
    agg = round(aggregate(rows, w, a.method), 4)
    lo, hi = bootstrap_ci(rows, w, a.method, a.bootstrap, a.seed)
    squads = sorted({r[0] for r in rows})
    print(json.dumps({"metric": "downstream_aggregate_score", "method": a.method, "n": len(rows),
                      "squads": squads, "weights_by_squad": w, "aggregate": agg,
                      "ci95": [lo, hi], "ci_lower": lo, "metric_hash": json.load(open(SEAL))["components"]["fitness_hash"],
                      "note": "scored only; promotion is canary-gated and never automatic here"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
