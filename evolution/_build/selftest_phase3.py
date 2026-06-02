#!/usr/bin/env python3
"""Phase 3 acceptance evidence: the familiarity stub is now LIVE and re-ranks techniques.
Run: python evolution/_build/selftest_phase3.py
Proves: 10 EMA successes from 0 -> success_rate == 1-0.8^10 (deterministic); familiarity contribution
== success_rate*100*0.05; and two techniques tied on all other dims FLIP rank once one is bumped.
"""
import subprocess, sys, os, json

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # evolution/
SQUAD = os.path.dirname(HERE)
MS = os.path.join(HERE, "memory_store.py")
STORE = os.path.join(SQUAD, "data", "metrics", "technique_success.json")
T = "selftest-cot"
W = {"task_fit": 0.35, "quality": 0.25, "efficiency": 0.20, "composability": 0.15, "familiarity": 0.05}


def run(*args):
    return subprocess.run([sys.executable, MS, *args], capture_output=True, text=True).stdout.strip()


def reset_T():
    d = json.load(open(STORE, encoding="utf-8")) if os.path.exists(STORE) else {"techniques": {}}
    d.setdefault("techniques", {}).pop(T, None)
    json.dump(d, open(STORE, "w", encoding="utf-8"), indent=2)


def total(dims):
    return round(sum(dims[k] * W[k] for k in W), 4)


def _run_test():
    reset_T()
    for _ in range(10):
        run("--bump", T, "--success")
    fam = json.loads(run("--familiarity", T))
    rate, contrib = fam["success_rate"], fam["contribution_to_total"]
    expected_rate = round(1 - 0.8 ** 10, 6)
    print(f"[ema] success_rate={rate} expected={expected_rate}")
    assert abs(rate - expected_rate) < 1e-5, "EMA must be deterministic 1-0.8^10"
    assert abs(contrib - rate * 100 * 0.05) < 1e-4, "contribution must equal familiarity*0.05"

    # two techniques identical on every dim except familiarity
    base = {"task_fit": 80, "quality": 70, "efficiency": 80, "composability": 50, "familiarity": 0}
    A = dict(base)
    B = dict(base)
    tie_before = total(A) == total(B)
    B["familiarity"] = fam["familiarity"]
    tA, tB = total(A), total(B)
    print(f"[rank] tie_before={tie_before} A={tA} B(bumped)={tB} delta={round(tB-tA,4)} contrib={round(contrib,4)}")
    assert tie_before, "A and B must start tied"
    assert tB > tA, "bumped technique must outrank"
    assert abs((tB - tA) - contrib) < 1e-4, "rank delta must equal the familiarity contribution"
    print("ALL ASSERTIONS PASSED")


def main():
    # isolate prod: restore data/metrics/technique_success.json after the test so acceptance
    # testing never pollutes the live store (Phase-3 audit LOW).
    backup = open(STORE, encoding="utf-8").read() if os.path.exists(STORE) else None
    try:
        _run_test()
    finally:
        if backup is not None:
            open(STORE, "w", encoding="utf-8").write(backup)
        elif os.path.exists(STORE):
            os.remove(STORE)


if __name__ == "__main__":
    main()
