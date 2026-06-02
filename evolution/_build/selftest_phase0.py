#!/usr/bin/env python3
"""Phase 0 acceptance evidence (hardened, signed-tag arming). Run: python evolution/_build/selftest_phase0.py
Proves:
  - write -> verify(0) -> tamper -> verify(3) -> restore -> verify(0)   [crash-safe]
  - guard disarmed (4): no human signed tag / no signing key configured
  - SELF-ARM CLOSED: a hand-edited armed=true (+bogus sig/tag) still yields guard(4) (flag is ignored)
  - SELF-ARM CLOSED: the agent setting its OWN $HRM_KERNEL_SEAL_TOKEN cannot reseal (2) or arm guard (4)
Arming requires a human git SIGNED tag the agent cannot forge; everything stays disarmed here (no key).
All mutations restored in finally blocks.
"""
import subprocess, sys, os, json

EV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HL = os.path.join(EV, "harness_lock.py")
FIT = os.path.join(EV, "kernel", "fitness.yaml")
SEAL = os.path.join(EV, "kernel", "kernel.seal.json")


def run(*args, env_token=None):
    env = dict(os.environ)
    if env_token:
        env["HRM_KERNEL_SEAL_TOKEN"] = env_token
    else:
        env.pop("HRM_KERNEL_SEAL_TOKEN", None)
    r = subprocess.run([sys.executable, HL, *args], capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def main():
    res = []
    run("write")
    rc, o = run("verify"); res.append(("verify_clean", rc, o)); assert rc == 0

    orig_fit = read(FIT)
    try:
        write(FIT, orig_fit.replace("ema_alpha: 0.2", "ema_alpha: 0.25"))
        rc, o = run("verify"); res.append(("verify_tampered", rc, o)); assert rc == 3
    finally:
        write(FIT, orig_fit)
    rc, o = run("verify"); res.append(("verify_restored", rc, o)); assert rc == 0

    rc, o = run("guard"); res.append(("guard_disarmed", rc, o)); assert rc == 4, "no signed tag -> disarmed"

    orig_seal = read(SEAL)
    try:
        d = json.loads(orig_seal)
        d["armed"] = True; d["status"] = "HUMAN_SEALED"; d["approved_sig"] = "sha256:deadbeef"
        d["seal_tag"] = "kernel-seal-forged"
        write(SEAL, json.dumps(d, indent=2))
        rc, o = run("guard"); res.append(("guard_forged_flag", rc, o)); assert rc == 4, "hand-edited armed must NOT arm"
        rc, o = run("reseal", "--token", "agent-self-chosen", env_token="agent-self-chosen")
        res.append(("reseal_self_token", rc, o)); assert rc != 0, "agent env token must NOT reseal"
        rc, o = run("guard", env_token="agent-self-chosen")
        res.append(("guard_self_token", rc, o)); assert rc == 4, "agent env token must NOT arm guard"
    finally:
        write(SEAL, orig_seal)

    run("write")
    rc, o = run("guard"); res.append(("guard_final_disarmed", rc, o)); assert rc == 4

    print("=== PHASE 0 SELFTEST (signed-tag arming; self-arm closed) ===")
    for name, rc, o in res:
        print(f"[{name}] exit={rc} :: {(o.splitlines()[0] if o else '')}")
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
