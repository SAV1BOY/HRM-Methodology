# judge.md — calibrated proxy-KPI LLM-judge (PROT, Section 19 §6.4)

> Tier-(b). For squads whose KPI is not directly auto-measurable (copy, brand, storytelling, movement,
> advisory), a CALIBRATED LLM-judge produces the proxy KPI score. Calibration + decorrelation are
> mandatory before the score is trusted — an uncalibrated judge is reward-hackable.

## Hard rules
1. **Calibrate first (κ ≥ 0.6):** before the judge drives anything, score a labeled gold set (≥20
   examples/squad, built by a human owner — ULTRAPLAN open Q6) and compute Cohen's κ vs the labels.
   If κ < 0.6 the KPI stays `kpi_measurability: proxy` and DOES NOT drive fitness (logged only).
2. **Pin the instrument:** `judge_model_id + prompt_hash + temperature(0) + seed` go in `kernel/meta.yaml`
   `judge_lock` (hashed into the seal). Changing any of them is tamper-evident and requires a re-seal.
3. **Decorrelate:** the proxy judge MUST be a DIFFERENT model/prompt from the gate judge (so a shared
   bias cannot make both rise together — closes H6 SCORE_DECOUPLE).
4. **Anchor:** pair the judge with ≥1 non-LLM oracle wherever a computable check exists; a fitness rise
   must be corroborated by the oracle + a mandatory human spot-check (H6).
5. **Confidence weighting:** a judge-scored contribution is multiplied by `min(1, (κ-0.6)/0.4)` so
   weakly-calibrated judges contribute less.
6. **Re-calibrate on a wall-clock cadence (14 days) AND on any judge/prompt version change** (not by
   task count — drift is time/version-driven). Rotate the gold set to resist Goodharting.

## Output
`{score: 0..1, kappa, judge_model_id, prompt_hash, oracle_corroborated: bool, label_set_version, label_date}`.
Until κ≥0.6 + a non-LLM oracle exist, the squad's KPI is shadow/log-only (drives_fitness:false).
