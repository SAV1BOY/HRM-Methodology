#!/usr/bin/env python3
"""test_hazards.py — H1-H7 anti-reward-hacking traceability + auto-test (Section 19 §7.6). STDLIB-ONLY.
Maps each hazard to its implementation and AUTO-TESTS the deterministic detectors. All mutations are
restored in finally blocks. Run from the HRM repo: python evolution/_build/test_hazards.py
"""
import subprocess, sys, os

EV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../evolution
SQUAD = os.path.dirname(EV)
HL = os.path.join(EV, "harness_lock.py")
LA = os.path.join(EV, "lineage_audit.py")
FIT = os.path.join(EV, "kernel", "fitness.yaml")
BASE = os.path.join(EV, "canary", "baseline.json")
SELECTOR = os.path.join(SQUAD, "hrm-agent", "technique-selector.md")
TMP_BAD = os.path.join(EV, "_build", "_bad_logic.md")

MAP = {
    "H1 KERNEL_DRIFT": "harness_lock.py verify — combined_hash over kernel+scripts+data+loop; exit 3 on any change [AUTO]",
    "H2 CHECK_DELETION": "lineage_audit.py --check-rewrite — immutable-token count drop; exit 6 [AUTO]",
    "H3 THRESHOLD_LOWER": "kernel/gates.lock.yaml floor_invariants + gate_definitions_hash in seal; lowering a domain threshold flips verify [covered by H1 mechanism]",
    "H4 GATES_TOUCHED": "kernel/meta.yaml forbidden_targets (kernel/gate-defs/checklists); L2 + canary verify kernel before acting [structural]",
    "H5 CANARY_TAMPER": "harness_lock DATA_MANIFEST (baseline.json + canary_suite.yaml in seal); editing baseline flips verify; exit 3 [AUTO]",
    "H6 SCORE_DECOUPLE": "judge.md — decorrelated judge + non-LLM oracle + MANDATORY human spot-check [process/PROT, not unit-testable]",
    "H7 DIVERSITY_COLLAPSE": "stagnation.py diversity_floor (kernel); diversity < floor flags level1 [AUTO]",
}


def run(*args):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def main():
    res = []
    run(HL, "write")  # clean baseline seal

    # H1 KERNEL_DRIFT
    o = read(FIT)
    try:
        write(FIT, o.replace("ema_alpha: 0.2", "ema_alpha: 0.25"))
        rc, _ = run(HL, "verify"); res.append(("H1 KERNEL_DRIFT", rc == 3))
    finally:
        write(FIT, o); run(HL, "write")

    # H2 CHECK_DELETION (remove a kernel-immutable dimension from a candidate)
    try:
        write(TMP_BAD, read(SELECTOR).replace("familiarity", ""))
        rc, _ = run(LA, "--check-rewrite", "--base", SELECTOR, "--candidate", TMP_BAD,
                    "--require", "task_fit,quality_impact,efficiency,composability,familiarity")
        res.append(("H2 CHECK_DELETION", rc == 6))
    finally:
        if os.path.exists(TMP_BAD):
            os.remove(TMP_BAD)

    # H5 CANARY_TAMPER (edit baseline without reseal -> DATA_MANIFEST trips verify)
    ob = read(BASE)
    try:
        write(BASE, ob.replace("0.96", "0.50"))
        rc, _ = run(HL, "verify"); res.append(("H5 CANARY_TAMPER", rc == 3))
    finally:
        write(BASE, ob); run(HL, "write")

    # H7 DIVERSITY_COLLAPSE (diversity below floor flags level1 even on a short series)
    rc, out = run(os.path.join(EV, "stagnation.py"), "--series", "0.80,0.81", "--diversity", "0.30")
    res.append(("H7 DIVERSITY_COLLAPSE", '"level1_breach": true' in out))

    print("=== H1-H7 DETECTOR MAP ===")
    for h, where in MAP.items():
        print(f"  {h}: {where}")
    print("\n=== AUTO-TESTS ===")
    ok = True
    for name, passed in res:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print("\nALL HAZARD AUTO-TESTS PASSED" if ok else "\nSOME HAZARD TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
