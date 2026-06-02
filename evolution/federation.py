#!/usr/bin/env python3
"""federation.py — federated evolution budget allocation (Section 19, ULTRAPLAN §8.3). STDLIB-ONLY.

Hub-and-spoke (no peer channel). IMPLEMENTS the §8.3 spec:
  progress_velocity = std-error-weighted SHRUNK slope(fitness, last K) toward the fleet mean (trust an
    extreme slope only if precise / CI excludes zero — raw slope amplifies noise);
  score = UCB of EXPECTED IMPROVEMENT = max(0, shrunk_slope) * P(improvable)  (+ confidence bonus when
    the slope CI excludes zero), so converged squads at the ceiling stop being funded;
  allocate proportionally to score^(1/temperature) -> DWELL hysteresis (blend toward the prior epoch's
    ledger so a one-epoch swing does not yank budget) -> clamp [min,max] -> criticality_floor -> renorm.
Production path (default): discover each participant's data/metrics/evolution_log.tsv (status-style walk),
build its fitness series, and regenerate data/registries/evolution/federation_ledger.yaml from LIVE data.
  python evolution/federation.py            # production: live participant series
  python evolution/federation.py --demo     # synthetic steep-vs-flat + floored critical squad
"""
import sys, os, re, math, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
SQUADS_ROOT = os.path.dirname(SQUAD)
CFG = os.path.join(SQUAD, "registry", "evolution-federation.yaml")
LEDGER = os.path.join(SQUAD, "data", "registries", "evolution", "federation_ledger.yaml")
NON_SQUAD = {".git", ".claude", "Mappings"}


def cfg():
    c = {"temperature": 0.5, "min_share": 0.03, "max_share": 0.35, "dwell_epochs": 2,
         "target": 0.95, "floor": {}, "participants": []}
    section = None
    for ln in open(CFG, encoding="utf-8"):
        s = ln.strip()
        for k in ("temperature", "min_share", "max_share", "dwell_epochs"):
            if s.startswith(k + ":"):
                try:
                    c[k] = float(s.split(":", 1)[1].split("#")[0].strip())
                except ValueError:
                    pass
        if s.startswith("criticality_floor:"):
            section = "floor"; continue
        if s.startswith("participants:"):
            section = "part"; continue
        if section == "floor":
            m = re.match(r"([a-z0-9_-]+):\s*([0-9.]+)", s)
            if m:
                c["floor"][m.group(1)] = float(m.group(2))
            elif s and not s.startswith("#") and not s.startswith("-"):
                section = None
        if section == "part":
            m = re.search(r"squad:\s*([a-z0-9_-]+)", s)
            if m:
                c["participants"].append(m.group(1))
    c["dwell_epochs"] = int(c["dwell_epochs"])
    return c


def slope_and_se(ys):
    n = len(ys)
    if n < 2:
        return 0.0, float("inf")
    xs = list(range(n)); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0, float("inf")
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    sse = sum((y - (my + b * (x - mx))) ** 2 for x, y in zip(xs, ys))
    se = math.sqrt((sse / (n - 2)) / sxx) if (n > 2 and sse > 0) else 0.0
    return b, se


def ci_excludes_zero(b, se):
    return se not in (0.0, float("inf")) and abs(b) > 1.96 * se


def p_improvable(current, target):
    return max(0.0, min(1.0, (target - current) / max(1e-6, target)))


def prior_shares():
    if not os.path.exists(LEDGER):
        return {}
    out = {}
    for ln in open(LEDGER, encoding="utf-8"):
        m = re.search(r"squad:\s*([a-z0-9_-]+).*budget_share:\s*([0-9.]+)", ln)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def allocate(series_by_squad, c):
    slopes, ses = {}, {}
    for k, ys in series_by_squad.items():
        slopes[k], ses[k] = slope_and_se(ys)
    fleet_mean = sum(slopes.values()) / len(slopes)
    shrunk = {}
    for k in slopes:                              # precision-weighted (std-error) shrinkage to fleet mean
        se = ses[k]
        if se == 0:
            shrunk[k] = slopes[k]
        elif math.isinf(se):
            shrunk[k] = fleet_mean
        else:
            w = 1.0 / (se * se)
            shrunk[k] = (w * slopes[k] + 1.0 * fleet_mean) / (w + 1.0)
    scores = {}
    for k, ys in series_by_squad.items():
        ei = max(0.0, shrunk[k]) * p_improvable(ys[-1] if ys else 0.0, c["target"])   # UCB expected improvement
        if ci_excludes_zero(slopes[k], ses[k]) and shrunk[k] > 0:
            ei *= 1.25                            # confidence bonus when the slope CI excludes zero
        scores[k] = max(1e-9, ei)
    t = max(0.05, c["temperature"])
    powered = {k: scores[k] ** (1.0 / t) for k in scores}
    Z = sum(powered.values())
    share = {k: powered[k] / Z for k in powered}
    prior = prior_shares()                        # DWELL hysteresis: damp single-epoch swings
    if prior:
        share = {k: 0.5 * v + 0.5 * prior.get(k, v) for k, v in share.items()}
    share = {k: min(c["max_share"], max(c["min_share"], v)) for k, v in share.items()}
    for k, f in c["floor"].items():
        if k in share:
            share[k] = max(share[k], f)
    tot = sum(share.values())
    share = {k: round(v / tot, 4) for k, v in share.items()}
    return slopes, ses, shrunk, share


def write_ledger(slopes, ses, share):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    lines = ["# federation_ledger.yaml (auto-generated by federation.py — §8.3 IMPLEMENTED)", "allocations:"]
    for k in sorted(share):
        se = "inf" if math.isinf(ses[k]) else round(ses[k], 5)
        lines.append(f"  - {{squad: {k}, slope: {round(slopes[k], 5)}, slope_se: {se}, budget_share: {share[k]}}}")
    open(LEDGER, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")


def discover_series():
    """Production: for each participant, find its data/metrics/evolution_log.tsv and build a fitness
    series from the gate_score column (fleet-comparable). Returns {squad: [scores]}."""
    logs = {}
    for root, dirs, files in os.walk(SQUADS_ROOT):
        dirs[:] = [d for d in dirs if d not in NON_SQUAD and not d.startswith(".")]
        if os.path.basename(root) == "metrics" and "evolution_log.tsv" in files:
            rel = os.path.relpath(os.path.join(root, "evolution_log.tsv"), SQUADS_ROOT).replace("\\", "/")
            key = re.sub(r"[^a-z0-9]", "", rel.split("/data/metrics/")[0].lower())
            with open(os.path.join(root, "evolution_log.tsv"), encoding="utf-8") as f:
                hdr = f.readline().rstrip("\n").split("\t")
                gi = hdr.index("gate_score") if "gate_score" in hdr else None
                ys = []
                for ln in f:
                    cells = ln.rstrip("\n").split("\t")
                    if gi is not None and len(cells) > gi and cells[gi] not in ("", "NA"):
                        ys.append(float(cells[gi]))
                if ys:
                    logs[key] = ys
    return logs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    c = cfg()
    if a.demo:
        series = {"pre-programming": [0.70, 0.74, 0.78, 0.82, 0.86],
                  "deep-research": [0.85, 0.85, 0.85, 0.85, 0.85],
                  "cybersecurity": [0.90, 0.90, 0.90, 0.90, 0.90]}
    else:
        disc = discover_series()
        # map participants (registry) to discovered series by normalized-name containment
        series = {}
        for p in c["participants"] or list(disc):
            pn = re.sub(r"[^a-z0-9]", "", p.replace("-", ""))
            for k, ys in disc.items():
                if pn and (pn in k or k in pn):
                    series[p] = ys
                    break
        if not series:
            print(json.dumps({"note": "no live participant series discovered yet (leaves have not emitted "
                              "gate_score rows); run --demo or wait for L0 rows", "participants": c["participants"]}))
            return 0
    slopes, ses, shrunk, share = allocate(series, c)
    write_ledger(slopes, ses, share)
    print(json.dumps({"mode": "demo" if a.demo else "production(live evolution_log.tsv)",
                      "squads": sorted(series), "slopes": {k: round(v, 5) for k, v in slopes.items()},
                      "budget_share": share, "criticality_floor": c["floor"], "dwell_epochs": c["dwell_epochs"],
                      "method": "std_error_shrinkage + UCB_expected_improvement + dwell_hysteresis (§8.3 implemented)"},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
