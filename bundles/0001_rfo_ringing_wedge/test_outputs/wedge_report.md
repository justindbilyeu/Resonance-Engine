# Wedge Report — 0001_rfo_ringing_wedge

- Mode: quick
- Grid: gamma=3, K=3
- Replicates per point: 1

## Ringing thresholds (point-level)
- Δ_PSD_dB ≥ 6.0
- N_over ≥ 2
- r_mean ≥ 0.35

## Sweep summary
- Ringing points |S|: 0 / 9 (0.0000)
- Largest connected component size (4-neighbor): 0

## Null evaluation
- Rejected: **True**

- null1_no_ringing_anywhere: FAIL
  - details: `{"thresholds": {"Delta_PSD_dB": 6.0, "N_over": 2, "r_mean": 0.35}, "any_point_passed": false}`
- null2_region_minimums: FAIL
  - details: `{"area_frac": 0.0, "area_frac_min": 0.02, "largest_cc_size": 0, "largest_cc_min": 20}`
- null3_unbounded_or_empty_rows: FAIL
  - details: `{"span_frac_max": 0.6, "row_spans_ok": false}`
- null4_negative_control: SKIP — negative control not run (disabled or quick mode)

## Files written
- grid.csv
- null_evaluation.json
- parameters_used.json
- seed_manifest.json
- wedge_report.md

## Deviations (recorded)
- mode: quick
- steps_total: 200000 -> 1000
- steps_burnin: 50000 -> 200
- steps_measure: 150000 -> 800
- replicates_per_point: 3 -> 1
- grid: 81x61 -> 3x3
