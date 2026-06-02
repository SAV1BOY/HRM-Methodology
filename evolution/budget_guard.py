#!/usr/bin/env python3
"""budget_guard.py — per-attempt evolution budget enforcement (Section 19, ULTRAPLAN §7.7). STDLIB-ONLY.

Aborts an evolution attempt that would exceed budget_per_attempt (read from config.yaml
evolution.kernel.budget_per_attempt). FAIL-CLOSED self-test: if a canonical telemetry field
{total_tokens, total_latency, api_calls} is ABSENT from the supplied usage, it ABORTS — so a missing
field can never silently read 0 and let an over-budget attempt slip through (the exact hazard ULTRAPLAN
R/§7.7 calls out). The optimizer may lower its own caps but the kernel ceiling is the hard bound.
  python evolution/budget_guard.py --total-tokens 150000 --total-latency 800 --api-calls 40
  python evolution/budget_guard.py --selftest      # proves fail-closed on a missing field
exit 0 = within budget, 8 = OVER BUDGET / fail-closed abort.
"""
import sys, os, re, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SQUAD = os.path.dirname(HERE)
CONFIG = os.path.join(SQUAD, "config.yaml")
CANON = ["total_tokens", "total_latency", "api_calls"]


def caps():
    c = {"max_tokens": 200000, "max_seconds": 900, "max_cost_usd": 5.0}
    txt = open(CONFIG, encoding="utf-8").read() if os.path.exists(CONFIG) else ""
    m = re.search(r"budget_per_attempt:\s*\{([^}]*)\}", txt)
    if m:
        body = m.group(1)
        for k in c:
            mm = re.search(k + r":\s*([0-9.]+)", body)
            if mm:
                c[k] = float(mm.group(1))
    return c


def check(usage):
    # FAIL-CLOSED: every canonical field MUST be present
    missing = [f for f in CANON if f not in usage or usage[f] is None]
    if missing:
        return False, {"abort": "fail-closed: missing canonical telemetry field(s) " + ",".join(missing)}
    c = caps()
    breaches = []
    if usage["total_tokens"] > c["max_tokens"]:
        breaches.append(f"tokens {usage['total_tokens']}>{c['max_tokens']}")
    if usage["total_latency"] > c["max_seconds"]:
        breaches.append(f"seconds {usage['total_latency']}>{c['max_seconds']}")
    if usage.get("cost_usd", 0) > c["max_cost_usd"]:
        breaches.append(f"cost {usage.get('cost_usd', 0)}>{c['max_cost_usd']}")
    return (not breaches), {"within_budget": not breaches, "breaches": breaches, "caps": c}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--total-tokens", type=int)
    ap.add_argument("--total-latency", type=float)
    ap.add_argument("--api-calls", type=int)
    ap.add_argument("--cost-usd", type=float, default=0.0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        ok, info = check({"total_tokens": 1})           # deliberately missing total_latency/api_calls
        print(json.dumps({"selftest_fail_closed": (not ok), "info": info}))
        return 0 if (not ok) else 8                      # selftest PASSES when guard ABORTS (ok False)
    if a.total_tokens is None or a.total_latency is None or a.api_calls is None:
        print(json.dumps({"abort": "fail-closed: provide --total-tokens --total-latency --api-calls"}))
        return 8
    usage = {"total_tokens": a.total_tokens, "total_latency": a.total_latency,
             "api_calls": a.api_calls, "cost_usd": a.cost_usd}
    ok, info = check(usage)
    print(json.dumps(info))
    return 0 if ok else 8


if __name__ == "__main__":
    sys.exit(main())
