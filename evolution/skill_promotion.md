# skill_promotion.md — Voyager cross-squad skill promotion (PROT + DET, Section 19 §8.4)

> A skill crystallized in one squad (`<squad>/lib/skill_library/learned/`) is promoted to the shared
> cross-squad library (`Squad HRM/lib/learned-shared/`) when it is GENERIC. DET engine:
> `evolution/skill_promotion.py`; registry: `registry/learned-skills.yaml`.

## Promotion criteria (ALL of the immutable gate + ANY generality signal)
- `quality_gate_pass == true`, AND
- `used_in_squads >= 2` OR `generality_score >= 0.7` OR a manual `--manual` flag.
- `generality_score` is calibrated against a small labeled set (same κ discipline as proxy KPIs) before
  the 0.7 threshold is trusted.

## Dedup (anti-DGM: never silent-delete)
`skill_promotion.py` keys on a sha256 fingerprint over (purpose + interface + key steps):
- exact match → increment `used_in_squads` (no duplicate entry);
- near match → route a `merge_candidate` to the meta-agent (human/LLM reviews), never auto-delete;
- else → copy to `lib/learned-shared/<id>.md` + register in `registry/learned-skills.yaml`.

## Consult-before-solving
At task start a squad checks `lib/skill_library/index.yaml` then the shared `learned-skills.yaml` before
solving from scratch — competence compounds across the fleet with use.
