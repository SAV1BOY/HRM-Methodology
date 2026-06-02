#!/usr/bin/env python3
"""status.py — fleet Evolution-Layer health dashboard. STDLIB-ONLY.

Anti "silent cron death" (ULTRAPLAN R18). DISCOVERS instrumented squads by walking SQUADS/ for any
data/metrics/evolution_log.tsv (drift-proof: reads reality, not the possibly-stale registry path),
then reports per-squad: rows (loops), fitness slope over last K, last-run age, and bootstrap stage;
plus a cron-heartbeat age that WARNs at >7 days. Writes data/metrics/evolution/dashboard.md.
Usage: python evolution/status.py [--now <epoch>]
"""
import sys, os, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)                       # Squad HRM
SQUADS_ROOT = os.path.dirname(REPO)                # SQUADS/
OUTDIR = os.path.join(REPO, "data", "metrics", "evolution")
OUT = os.path.join(OUTDIR, "dashboard.md")
HEARTBEAT = os.path.join(OUTDIR, "heartbeat")      # file containing an epoch-seconds int
WARN_AGE = 7 * 86400


def find_logs():
    out = []
    for root, dirs, files in os.walk(SQUADS_ROOT):
        dirs[:] = [d for d in dirs if d != ".git" and not d.startswith(".")]
        if os.path.basename(root) == "metrics" and "evolution_log.tsv" in files:
            out.append(os.path.join(root, "evolution_log.tsv"))
    return sorted(out)


def slope(ys):
    n = len(ys)
    if n < 2:
        return None
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return 0.0
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den, 5)


def read_scores(path):
    with open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        gi = header.index("gate_score") if "gate_score" in header else None
        ys = []
        for ln in f:
            cells = ln.rstrip("\n").split("\t")
            if gi is not None and len(cells) > gi and cells[gi] not in ("", "NA"):
                ys.append(float(cells[gi]))
        return ys


def squad_name(log_path):
    rel = os.path.relpath(log_path, SQUADS_ROOT).replace("\\", "/")
    return rel.split("/data/metrics/")[0]


def age_str(sec):
    if sec is None:
        return "n/a"
    d = sec / 86400
    return f"{d:.1f}d" if d >= 1 else f"{sec/3600:.1f}h"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", type=int, default=None)
    a = ap.parse_args()
    now = a.now if a.now is not None else int(time.time())
    os.makedirs(OUTDIR, exist_ok=True)
    rows = []
    for log in find_logs():
        ys = read_scores(log)
        rows.append({"squad": squad_name(log), "loops": len(ys),
                     "slope_k10": slope(ys[-10:]), "mean": round(sum(ys) / len(ys), 4) if ys else None,
                     "last_run_age": age_str(now - int(os.path.getmtime(log))),
                     "stage": "B0_shadow" if len(ys) < 40 else "B1_blend"})
    hb = None
    if os.path.exists(HEARTBEAT):
        try:
            hb = now - int(open(HEARTBEAT, encoding="utf-8").read().strip())
        except ValueError:
            hb = None
    hb_warn = (hb is not None and hb > WARN_AGE)
    lines = ["# Evolution Layer — Fleet Dashboard", "",
             f"_generated at epoch {now} · {len(rows)} instrumented squad(s)_", "",
             f"**Cron heartbeat:** {age_str(hb)} " + ("⚠️ STALE (>7d — cadencer may be dead)" if hb_warn else "(ok)" if hb is not None else "(no heartbeat file yet)"),
             "", "| squad | loops | slope(k10) | mean | last run | stage |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['squad']} | {r['loops']} | {r['slope_k10']} | {r['mean']} | {r['last_run_age']} | {r['stage']} |")
    if not rows:
        lines.append("| _(none discovered)_ | | | | | |")
    open(OUT, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
    print(f"dashboard -> {os.path.relpath(OUT, REPO)} | squads={len(rows)} | heartbeat={age_str(hb)} | warn={hb_warn}")
    for r in rows:
        print(f"  {r['squad']}: loops={r['loops']} slope={r['slope_k10']} stage={r['stage']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
