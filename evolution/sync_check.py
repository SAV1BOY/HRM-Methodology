#!/usr/bin/env python3
"""sync_check.py — Phase 0.5 DRIFT GUARD. STDLIB-ONLY (no PyYAML).

Re-derives the squad set + counts + anchors from DISK and FAILS (exit 1) on drift vs the
registry, so the plan can never silently desync from reality (ULTRAPLAN R20). Replaces brittle
line-number / hand-typed assumptions with a runnable check.

Checks: (1) on-disk leaf count == registry leaf count; (2) declared `total` == on-disk leaves;
(3) every on-disk leaf has a registry entry (by normalized name); (4) every registry path resolves
on disk; (5) presence of the section-19 anchor (warn-only until Phase 3).
exit 0 = in sync, exit 1 = drift.
"""
import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)                 # .../Squad HRM
SQUADS_ROOT = os.path.dirname(REPO)          # .../SQUADS
PARENT = os.path.dirname(SQUADS_ROOT)        # .../Obisidian (registry paths are 'SQUADS/...')
SQUADS_YAML = os.path.join(REPO, "registry", "squads.yaml")
CONFIG = os.path.join(REPO, "config.yaml")

NON_SQUAD = {".claude", ".git", "Mappings", "Squad HRM"}


def norm(name):
    base = os.path.basename(name.rstrip("/\\"))
    base = base.lower()
    base = re.sub(r"[-_ ]*squad[-_ ]*", "", base)   # drop the word 'squad'
    base = re.sub(r"\s*-\s*em\s*desenvolvimento", "", base)  # 'Squad de Copy - Em Desenvolvimento'
    tokens = [t for t in re.split(r"[^a-z0-9]+", base) if t and t not in {"de", "do", "da", "the", "of"}]
    return "".join(tokens)


def disk_leaves():
    out = {}
    for name in sorted(os.listdir(SQUADS_ROOT)):
        p = os.path.join(SQUADS_ROOT, name)
        if os.path.isdir(p) and name not in NON_SQUAD and not name.startswith("."):
            out[norm(name)] = name
    return out


def registry_squads():
    ids, paths, total = [], {}, None
    cur = None
    with open(SQUADS_YAML, encoding="utf-8") as f:
        for ln in f:
            s = ln.rstrip()
            m = re.match(r"\s*total:\s*(\d+)", s)
            if m and total is None:
                total = int(m.group(1)); continue
            m = re.match(r"\s*-\s*id:\s*(\S+)", s)
            if m:
                cur = m.group(1).strip().strip('"'); ids.append(cur); continue
            m = re.match(r'\s*path:\s*"?([^"]+)"?', s)
            if m and cur:
                paths[cur] = m.group(1).strip()
    return ids, paths, total


def main():
    problems = []
    disk = disk_leaves()
    ids, paths, total = registry_squads()
    leaf_ids = [i for i in ids if i != "hrm-squad"]
    disk_norms = set(disk.keys())
    reg_norms = {norm(i): i for i in leaf_ids}

    print(f"on-disk leaves ({len(disk)}): {sorted(disk.values())}")
    print(f"registry leaf entries ({len(leaf_ids)}): {sorted(leaf_ids)}")
    print(f"declared total: {total}")

    if len(disk) != len(leaf_ids):
        problems.append(f"LEAF COUNT DRIFT: disk={len(disk)} registry_leaves={len(leaf_ids)}")
    if total is not None and total != len(disk):
        problems.append(f"TOTAL DRIFT: declared total={total} != on-disk leaves={len(disk)}")

    def matched(a, pool):
        for b in pool:
            if a == b or (min(len(a), len(b)) >= 4 and (a in b or b in a)):
                return b
        return None
    missing = sorted(disk[n] for n in disk_norms if not matched(n, reg_norms.keys()))
    if missing:
        problems.append(f"MISSING FROM REGISTRY ({len(missing)}): {missing}")
    extra = sorted(reg_norms[n] for n in reg_norms if not matched(n, disk_norms))
    if extra:
        problems.append(f"REGISTRY ENTRY NOT ON DISK ({len(extra)}): {extra}")

    bad_paths = []
    for sid, pth in paths.items():
        if sid == "hrm-squad":
            continue
        cand = os.path.normpath(os.path.join(PARENT, pth))
        if not os.path.isdir(cand):
            bad_paths.append(f"{sid} -> {pth}")
    if bad_paths:
        problems.append(f"PATH UNRESOLVED ({len(bad_paths)}): {bad_paths}")

    if "EVOLUTION-ANCHOR: section-19" not in open(CONFIG, encoding="utf-8").read():
        print("WARN: config.yaml lacks 'EVOLUTION-ANCHOR: section-19' (added in Phase 3 — ok now).")

    if problems:
        print("\nDRIFT DETECTED:")
        for p in problems:
            print("  -", p)
        return 1
    print("\nSYNC OK: registry matches disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
