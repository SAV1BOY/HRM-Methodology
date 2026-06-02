#!/usr/bin/env python3
"""rollback.py — automatic rollback on downstream drop (Section 19, ULTRAPLAN §7.5). STDLIB-ONLY.

Honest about git topology (B15): reverts ONLY the HRM repo's promotion files; each leaf reverts its own
repo via its own harness. Uses `git revert` (NOT reset) so the variant is preserved for credit assignment
+ keep_stepping_stones. Appends a chained lineage event (same scheme as archive.py).
  --check --series s1,s2,...  : TRIGGER if rolling mean(last W) < baseline - drop_threshold.
  --execute --commit <sha>    : git revert --no-edit <sha> -- <HRM promotion files> + lineage event.
exit 0 = no rollback / done, 7 = ROLLBACK TRIGGERED (on --check).
"""
import sys, os, json, subprocess, argparse, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
CONFIG = os.path.join(SQUAD, "config.yaml")
LINEAGE = os.path.join(SQUAD, "data", "registries", "evolution", "lineage.jsonl")
HRM_PROMOTION_FILES = ["evolution/selector_config.yaml", "hrm-agent/technique-selector.md",
                       "evolution/canary/baseline.json"]


def safety_params():
    p = {"drop_threshold": 0.03, "rollback_window": 10}
    inblock = False
    for ln in open(CONFIG, encoding="utf-8"):
        s = ln.strip()
        if s.startswith("safety:"):
            inblock = True
            continue
        if inblock:
            for k in ("drop_threshold", "rollback_window"):
                if s.startswith(k + ":"):
                    try:
                        p[k] = float(s.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            if s.startswith("operation:"):
                break
    p["rollback_window"] = int(p["rollback_window"])
    return p


def _last_hash():
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
    os.makedirs(os.path.dirname(LINEAGE), exist_ok=True)
    prev = _last_hash()
    event["prev_line_hash"] = prev
    payload = json.dumps(event, sort_keys=True)
    event["line_hash"] = "sha256:" + hashlib.sha256((prev + payload).encode()).hexdigest()[:16]
    with open(LINEAGE, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(event) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--series", default="")
    ap.add_argument("--baseline", type=float, default=None)
    ap.add_argument("--commit", default=None)
    a = ap.parse_args()
    p = safety_params()

    if a.check:
        s = [float(x) for x in a.series.split(",") if x.strip() != ""]
        if not s:
            print(json.dumps({"verdict": "no_data"}))
            return 0
        base = a.baseline if a.baseline is not None else s[0]
        w = s[-p["rollback_window"]:] if len(s) >= p["rollback_window"] else s
        mean_w = round(sum(w) / len(w), 4)
        triggered = mean_w < base - p["drop_threshold"]
        out = {"verdict": "ROLLBACK TRIGGERED" if triggered else "ok", "baseline": base,
               "window_mean": mean_w, "drop_threshold": p["drop_threshold"],
               "rollback_window": p["rollback_window"], "n": len(s),
               "params_source": "config.yaml#evolution.safety (defaults 0.03/10 if absent)"}
        if triggered:
            append_lineage({"loop": "rollback", "event": "trigger", "baseline": base,
                            "window_mean": mean_w, "reason": "downstream drop > threshold"})
            out["lineage"] = "appended (chained)"
            out["action"] = "git revert --no-edit <promotion_commit> -- " + " ".join(HRM_PROMOTION_FILES)
        print(json.dumps(out, indent=2))
        return 7 if triggered else 0

    if a.execute:
        if not a.commit:
            print(json.dumps({"error": "--execute requires --commit <sha>"}))
            return 1
        rc = subprocess.call(["git", "-C", SQUAD, "revert", "--no-edit", a.commit, "--"] + HRM_PROMOTION_FILES)
        append_lineage({"loop": "rollback", "event": "execute", "commit": a.commit, "git_rc": rc,
                        "files": HRM_PROMOTION_FILES})
        print(json.dumps({"reverted_commit": a.commit, "git_rc": rc, "files": HRM_PROMOTION_FILES,
                          "note": "HRM files only; leaves revert their own repos; variant preserved (no reset)"}))
        return 0

    print("use --check --series ... or --execute --commit <sha>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
