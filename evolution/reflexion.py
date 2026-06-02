#!/usr/bin/env python3
"""reflexion.py — L0 recorder (DET). STDLIB-ONLY.
Appends one canonical row to data/metrics/pipeline_outcomes.tsv AND updates per-technique memory
(memory_store.py) so the selector's familiarity term learns with use.
Usage:
  python evolution/reflexion.py --pipeline-id p1 --task-type reasoning --complexity complex \
    --quality high --playbook research-and-analysis --techniques chain-of-thought,self-refine \
    --selector-version v1 --status PASSED --gate-pass 1 --gate-score 0.91 \
    --tokens 4200 --latency 22.5 --calls 5 --downstream-kpi-delta 0.0 --verdict good
"""
import sys, os, time, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
OUT = os.path.join(SQUAD, "data", "metrics", "pipeline_outcomes.tsv")
MS = os.path.join(HERE, "memory_store.py")
COLS = ["pipeline_id", "timestamp", "task_type", "complexity", "quality_level", "playbook",
        "techniques", "selector_config_version", "status", "gate_pass", "gate_score",
        "total_tokens", "total_latency", "api_calls", "downstream_kpi_delta", "reflexion_verdicts"]


def append_row(vals):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    new = not os.path.exists(OUT)
    with open(OUT, "a", encoding="utf-8", newline="") as f:
        if new:
            f.write("\t".join(COLS) + "\n")
        f.write("\t".join(str(v) for v in vals) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pipeline-id", required=True); ap.add_argument("--task-type", default="")
    ap.add_argument("--complexity", default=""); ap.add_argument("--quality", default="")
    ap.add_argument("--playbook", default=""); ap.add_argument("--techniques", default="")
    ap.add_argument("--selector-version", default="v1"); ap.add_argument("--status", default="")
    ap.add_argument("--gate-pass", default="0"); ap.add_argument("--gate-score", default="")
    ap.add_argument("--tokens", default="0"); ap.add_argument("--latency", default="0")
    ap.add_argument("--calls", default="0"); ap.add_argument("--downstream-kpi-delta", default="0")
    ap.add_argument("--verdict", default="neutral", choices=["good", "bad", "neutral"])
    a = ap.parse_args()
    row = [a.pipeline_id, int(time.time()), a.task_type, a.complexity, a.quality, a.playbook,
           a.techniques, a.selector_version, a.status, a.gate_pass, a.gate_score,
           a.tokens, a.latency, a.calls, a.downstream_kpi_delta, a.verdict]
    append_row(row)
    # update technique memory (neutral = skip, per reflexion.md)
    if a.verdict in ("good", "bad") and a.techniques:
        flag = "--success" if a.verdict == "good" else "--fail"
        for t in [x for x in a.techniques.split(",") if x.strip()]:
            subprocess.call([sys.executable, MS, "--bump", t.strip(), flag])
    print(f"recorded {a.pipeline_id} -> {os.path.relpath(OUT, SQUAD)} (verdict={a.verdict}, techniques={a.techniques})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
