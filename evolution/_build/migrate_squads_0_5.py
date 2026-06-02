#!/usr/bin/env python3
"""Phase 0.5 migration: reconcile registry/squads.yaml to on-disk reality (idempotent).
- fix 10 wrong leaf paths to real disk folder names
- total 12 -> 15 (leaf squads, excludes hrm-squad orchestrator)
- version 1.1 -> 1.2
- append 4 missing leaves (Pre-Programming, Deep-Research, Human-Mapping, Sales-Call-Intelligence)
Run: python evolution/_build/migrate_squads_0_5.py  (re-runnable; only applies what's missing)
"""
import os, re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML = os.path.join(REPO, "registry", "squads.yaml")

PATH_FIX = {
    "SQUADS/Squad de Copy/": "SQUADS/Squad de Copy - Em Desenvolvimento/",
    "SQUADS/Squad Brand/": "SQUADS/Brand-Squad/",
    "SQUADS/Squad Design/": "SQUADS/Design-Squad/",
    "SQUADS/Squad Data/": "SQUADS/Data-Squad/",
    "SQUADS/Squad Cybersecurity/": "SQUADS/Cybersecurity-Squad/",
    "SQUADS/Squad C-Level/": "SQUADS/C-Level-Squad/",
    "SQUADS/Squad Storytelling/": "SQUADS/Storytelling-Squad/",
    "SQUADS/Squad Traffic Masters/": "SQUADS/Traffic-Masters-Squad/",
    "SQUADS/Squad Movement/": "SQUADS/Movement-Squad/",
    "SQUADS/Squad Advisory Board/": "SQUADS/Advisory-Board-Squad/",
}

NEW_ENTRIES = '''
  - id: pre-programming-squad
    name: "Pre-Programming Squad"
    chief: "pre-programming-chief"
    domain: "software-architecture-and-planning"
    path: "SQUADS/Pre-Programming-Squad/"
    status: "active"
    capabilities:
      - "Requirements engineering and spec authoring"
      - "Architecture decision records"
      - "Definition-of-Done gating and rework reduction"
      - "Test strategy before implementation"
    delegation_protocol: "squad-brief"
    deliverables:
      - "Specs, ADRs, DoD checklists, test plans"
    quality_integration:
      gate_owner: "pre-programming-chief"
      verification_levels: [local, global, semantic]
      acceptance_threshold: 0.88
      feedback_loop: "HRM -> pre-programming-chief -> internal review -> delivery"
    evolution:
      enabled: false
      primary_kpi: "gate_pass_rate"
      secondary_kpi: "rework_rate"
      fitness_direction: "maximize"
      kpi_measurability: "auto"
      conformance_note: "internal-checklist; pair with >=1 external-outcome KPI before driving fitness"

  - id: deep-research-squad
    name: "Deep Research Squad"
    chief: "deep-research-chief"
    domain: "research-and-synthesis"
    path: "SQUADS/Deep-Research-Squad/"
    status: "active"
    capabilities:
      - "Multi-source research and fact verification"
      - "Citation tracing and evidence density scoring"
      - "Adversarial claim verification"
      - "Cited report synthesis"
    delegation_protocol: "squad-brief"
    deliverables:
      - "Cited research reports with evidence map"
    quality_integration:
      gate_owner: "deep-research-chief"
      verification_levels: [local, semantic]
      acceptance_threshold: 0.85
      feedback_loop: "HRM -> deep-research-chief -> internal review -> delivery"
    evolution:
      enabled: false
      primary_kpi: "citation_accuracy"
      secondary_kpi: "evidence_density"
      fitness_direction: "maximize"
      kpi_measurability: "auto"
      ground_truth: "external (citations resolve)"

  - id: human-mapping-squad
    name: "Human Mapping Squad"
    chief: "human-mapping-chief"
    domain: "psychographic-profiling"
    path: "SQUADS/Human-Mapping-Squad/"
    status: "active"
    capabilities:
      - "Multi-framework personality and audience profiling"
      - "Test-retest profile consistency"
      - "Persona synthesis"
    delegation_protocol: "squad-brief"
    deliverables:
      - "Profiles and audience maps with consistency scores"
    quality_integration:
      gate_owner: "human-mapping-chief"
      verification_levels: [local, semantic]
      acceptance_threshold: 0.85
      feedback_loop: "HRM -> human-mapping-chief -> internal review -> delivery"
    evolution:
      enabled: false
      primary_kpi: "profile_consistency"
      fitness_direction: "maximize"
      kpi_measurability: "auto"
      ground_truth: "external (test-retest stability)"

  - id: sales-call-intelligence-squad
    name: "Sales Call Intelligence Squad"
    chief: "sales-call-chief"
    domain: "sales-conversation-analysis"
    path: "SQUADS/Sales-Call-Intelligence-Squad/"
    status: "active"
    capabilities:
      - "Call transcription analysis"
      - "Methodology adherence scoring"
      - "Extraction of objections, commitments, next steps"
      - "Close-rate attribution by closer"
    delegation_protocol: "squad-brief"
    deliverables:
      - "Call analyses, extraction sheets, close-rate reports"
    quality_integration:
      gate_owner: "sales-call-chief"
      verification_levels: [local, global, semantic]
      acceptance_threshold: 0.88
      feedback_loop: "HRM -> sales-call-chief -> internal review -> delivery"
    evolution:
      enabled: false
      primary_kpi: "extraction_accuracy"
      secondary_kpi: "close_rate"
      fitness_direction: "maximize"
      kpi_measurability: "auto"
      ground_truth: "labeled-set/external"
'''


def main():
    s = open(YAML, encoding="utf-8").read()
    changed = []
    for old, new in PATH_FIX.items():
        if old in s:
            s = s.replace(old, new); changed.append(f"path {old} -> {new}")
    if 'total: 12' in s:
        s = s.replace('total: 12', 'total: 15  # leaf squads on disk (excludes hrm-squad orchestrator)'); changed.append("total 12->15")
    if 'version: "1.1"' in s:
        s = s.replace('version: "1.1"', 'version: "1.2"', 1); changed.append("version 1.1->1.2")
    if 'id: pre-programming-squad' not in s:
        s = s.rstrip() + "\n" + NEW_ENTRIES; changed.append("appended 4 leaf entries")
    open(YAML, "w", encoding="utf-8", newline="").write(s)
    print("MIGRATION APPLIED:" if changed else "NO-OP (already migrated)")
    for c in changed:
        print("  +", c)


if __name__ == "__main__":
    main()
