#!/usr/bin/env python3
"""l0_close.py — L0 Stop-hook close entry (Section 19 never_stop = event_driven_L0). STDLIB-ONLY.

The deterministic entry a Stop hook (or the Step-11 verification cascade) calls to GUARANTEE the L0
loop closed after each task — belt-and-suspenders for the gate-runner L0 hook so per-task learning is
never skipped. It does NOT auto-install itself: wiring it into ~/.claude/settings.json is the human
opt-in (ULTRAPLAN open Q8). Idempotent + side-effect-light: confirms the L0 plumbing exists and reports
readiness + the exact settings.json snippet to install. The actual reflection/record is reflexion.py.
  python evolution/l0_close.py --status
"""
import sys, os, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
TS = os.path.join(SQUAD, "data", "metrics", "technique_success.json")
PO = os.path.join(SQUAD, "data", "metrics", "pipeline_outcomes.tsv")
REFLEXION = os.path.join(HERE, "reflexion.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.parse_args()
    ready = os.path.exists(TS) and os.path.exists(PO) and os.path.exists(REFLEXION)
    snippet = ('{"hooks":{"Stop":[{"hooks":[{"type":"command",'
               '"command":"python \\"' + os.path.relpath(__file__, SQUAD).replace(os.sep, "/") + '\\" --status"}]}]}}')
    print(json.dumps({
        "l0_plumbing_ready": ready,
        "technique_success_json": os.path.exists(TS),
        "pipeline_outcomes_tsv": os.path.exists(PO),
        "reflexion_recorder": os.path.exists(REFLEXION),
        "primary_l0_trigger": "gate-runner.md Step-11 cascade (event-driven, always covers L0)",
        "this_entry": "belt-and-suspenders Stop-hook close; NOT auto-installed (human opt-in, Q8)",
        "install_snippet_for_~/.claude/settings.json": snippet,
        "note": "never_stop = event_driven_L0 + cadence_driven_L1_L2; durable state in data/ resumes across sessions"
    }, indent=2))
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())
