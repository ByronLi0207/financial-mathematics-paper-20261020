# WP4 source inventory: metadata and plotted-point provenance

All values below come from existing public result tables. No financial model, statistical test or new fit was run.

## Census and evidence mismatch

| Source | Saved rows | Conditional plot records | Treatment |
|---|---:|---:|---|
| WP1 v8 simulation |144|144|QR33/QR4 each72|
| WP2 v9 summary |144|96|Exclude48 F self-reference rows; QR33/QR4 each48|
| WP1 empirical overlay |120|120|Hourly FX8, daily FX8, original Treasury8, panel96|
| WP3 learning curve |20|20|Same inspected hourly FX period; QR33/QR4 each10|
| Total |428|380|190 records per method; no same-x pooling|

**MISMATCH:** interpreting the144-row v9 summary as144 conditional-model points would count48 F self-comparisons. The conditional figure census is380, not428.

## Sources and stable locators

- `results/revision-v9/wp1/simulation-cells.json`: 296855 B; SHA256 `1186c50c4033332a58718f680ad00a5d7a47fb67c4c5c3e1bb9210be8a4de5a3`.
- `results/revision-v9/wp1/empirical-overlay.json`: 66901 B; SHA256 `c3c94df846cd8888c4d6fe8c0863dd1e5787894901d9aa3bc1b87064b6edf647`.
- `results/revision-v9/wp2/summary.json`: 137693 B; SHA256 `ab77dade64a67751f8e93b1bb18bc9a491c22a6efb2b5292840748e8a6b636bc`.
- `results/revision-v9/wp3/contrasts.json`: 12569 B; SHA256 `576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4`.
- `notes/revision-v9/wp1-breakeven.json`: 8014 B; SHA256 `84d983fffcc79b19d9a1618cf44a7d3c11a2b40f8d51eb23cb0068c13b069184`.
- `protocol/revision-v9/wp3-learning-curve.json`: 51316 B; SHA256 `0490302463c17096b612fa7241cae97fed082052cefd29f176f0eba3926aedae`.

Every point is enumerated in the companion JSON with a semantic point_id, zero-based JSON list index, source file/hash, method/W/H/source metadata, exact rational c, saved ordinate field, and marker recommendation. Old empirical points also retain the original one-based CSV line (including header).

## Known repeated same-period observations

Eight pairs repeat the original FX task at W720/W2880 × H6/H24 × QR33/QR4. All eight pairs have exactly equal model/reference mean losses, issue counts and rational x. Their stored y values differ by at most 9.547918011776346e-15 percentage points because the already frozen source arithmetic differs: old100*(model/F-1), new100*(model-F)/F. Preserve both original values, identify both records and their shared period, and use distinct old/new markers. They are not eight extra independent validation observations.

## Marker adaptation

- `simulation_v8`: marker `o`, light; v8 Gaussian/GARCH simulation.
- `simulation_v9`: marker `x`, light-distinct; v9 new-DGP simulation.
- `fx_hourly_old`: marker `o`, dark; FX hourly: original inspected period.
- `fx_daily_old`: marker `s`, dark; FX daily: same dealer.
- `nyfed_weekly_old`: marker `^`, dark; Treasury original series.
- `panel_old`: marker `D`, dark; 12 Treasury panel series.
- `fx_hourly_learning_curve`: marker `P`, dark-distinct; FX hourly learning curve: same inspected period.

These are source-adaptation recommendations, not a requirement to use a particular color. The plotted provenance must identify the actual adopted marker/color; the two simulation generations must remain visibly distinct, and learning-curve points must remain distinguishable from the original same-period FX points.

## Full required finite-point extent

- QR33: c in [2.08, 822.8571428571429], relative loss in [-26.42400809091828, 544.3372584055676] percent; 190 finite points.
- QR4: c in [2.08, 822.8571428571429], relative loss in [-19.40674890580287, 299.1157073741312] percent; 190 finite points.

All coincident-x records and outliers are retained in JSON. Do not trim, average or jitter true coordinates. A detail inset cannot replace full-range evidence.

## Independent validator checklist

1. All380 point IDs unique; JSON source_sha256/path/index must resolve to frozen source records.
2. Exclude only the48 F self-reference rows from WP2; preserve every QR33/QR4 row, failure/NA included.
3. Check exact rational x=W/(H+1), then plot log(c) via axis transformation only; never substitute W/p or an effective-sample interpretation.
4. Use v8 relative_loss_percent, v9 full_procedure_relative_loss_percent, empirical saved relative_loss_percent; do not recompute/round source y for plotting.
5. Verify each row method/H/W/DGP/phi/volatility/source and complete counts; retain source statuses even if unplottable.
6. Retain120 old empirical rows and20 new learning-curve rows; eight duplicates are one same-period FX task with repeated evidence, not independent validation.
7. Keep every coincident-x record; no averaging, outcome-based deduplication, jittering true x or dropped zero/negative point.
8. Use the original WP1 all-draw envelope by method; identify it as post-hoc/fixed-grid uncertainty and preserve a nonmonotone/first-cutpoint caveat.
9. Axis limits must contain every finite point and band; no outlier crop/percentile clip. If a detail inset is used, retain a full-range panel.
10. Verify plotted offsets against manifest, expected collections/markers/panels, output PNG/PDF existence and rendered visibility, and route every point to a specificsource row.
