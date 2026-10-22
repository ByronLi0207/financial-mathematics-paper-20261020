# Exploratory AR(1) residual-block replay

This is a separately frozen, post-result addition to the original conditional study. Both financial samples had already been inspected. The original QR primary comparisons, sixteen-file freeze, parameter selections and sixty-nine-file core archive are unchanged. All eight source/H/W cells and twenty-four declared comparisons are retained.

The [design](../../../protocol/revision-20261022/ar1-replay-design.md), [executable specification](../../../protocol/revision-20261022/ar1-replay-spec.json) and [seventeen-file freeze](../../../protocol/revision-20261022/ar1-replay-executable-freeze.json) were published and all bound files freshly byte-verified at [a068dfe](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/commit/a068dfe6b4dcb2447d6d16f665fb39fe9defd329) before the financial attempt started at 22 October 2026, 11:50:31 UTC. Freeze SHA-256: `57a880384d1a978f4f37b18eeaed1716b21db1f48b88c1375a7b5348c5421261`.

## Fixed comparison and complete results

At each original refit r, estimate intercept-bearing AR(1) on the W+H−1 unique adjacent transitions in the mature scenario union N_(r−H−W+1)..N_r. Common binary scaling and anchor-centered moments preserve represented spacing. Replay each historical residual block in order from the actual current N_t using the same coefficients. The closed identity is `N_(i+h)+phi^h*(N_t−N_i)`; h0 is the current observation. Exact phi=1 preserves frozen S arithmetic. Use the same corrected rank, floor, histories and refit schedules. Finite phi is not clipped and a failed whole cell would have no shortened mean.

The direct comparison is AR minus matching frozen S; F and the originally selected QR are context comparisons. Negative percentage favors AR. Units are source-native; percentages are within-reference contrasts, not a pooled economic effect. H counts records: hourly archive records for FX and weekly transitions for Treasury.

| Source | H | W | AR−S loss | AR−F loss | AR−QR loss | Strict breaches AR / S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FX | 6 | 720 | -1.536% | +0.278% | +2.447% | 282 / 255 |
| FX | 6 | 2880 | -0.546% | -0.962% | +16.197% | 338 / 268 |
| FX | 24 | 720 | +2.386% | -1.790% | -25.318% | 401 / 289 |
| FX | 24 | 2880 | +5.147% | +4.595% | +8.679% | 444 / 292 |
| Treasury | 6 | 52 | -13.444% | -13.208% | -52.665% | 22 / 11 |
| Treasury | 6 | 260 | -18.887% | -20.399% | -47.209% | 31 / 28 |
| Treasury | 24 | 52 | +35.125% | +32.823% | -59.432% | 56 / 33 |
| Treasury | 24 | 260 | -24.118% | -24.162% | -63.860% | 59 / 12 |

AR lowers mean loss in five of eight cells against each of S, F and QR. It loses to QR in three of four FX cells and improves on QR in all four Treasury cells. The original adverse Treasury QR primary therefore does not establish failure of every conditional family. The addition supplies another bounded comparison, not a new estimator or a replacement primary.

Against S, mean report and mean unused allowance fall in all eight cells, but strict breach occasions rise in all eight and all-origin mean positive overrun rises in seven. In Treasury H24 W260, S loss 2478.871300 falls to AR 1881.016326 (−24.118%), while breaches increase 12→59 of 277. Mean positive overrun increases 306.848375→892.436616 USD millions; mean unused allowance falls 43747.306859→20664.030821. Under the stipulated score, `.05*23083.276039` of reduced unused-allowance loss exceeds `.95*585.588240` of added overrun loss. This arithmetic is not an observed funding saving, safer policy or conditional95% coverage.

All annual and fixed H+1-grid comparisons remain. Direct S signs reverse for FX H24 W720 (+2.386% overall,−1.884% on265 sparse origins) and Treasury H24 W52 (+35.125% overall,−14.100% on only12). Treasury H24 W260 remains favorable on the12-origin grid but is adverse against S in 2022 and 2023. No grid or year is used to select a strategy. These are dependent descriptive subdivisions, not new tests or replications. All fitted phi values in this run lie between 0 and 1; that is a description of the fitted histories, not identification of a mean-reverting data-generating process.

## Files and independent numerical readback

The six CSVs contain 8 summary, 32 annual, 8 sparse, 24 paired, 96 annual-paired and 24 sparse-paired rows. Eight cell receipts and `ar1-replay-manifest.json` identify the actual inputs, frozen files, retained private artifacts and resources. Raw observations, per-origin forecasts and per-refit coefficients remain private.

[independent-readback.json](independent-readback.json) records a distinct scalar/Fraction output check. It reconstructs all targets/floors/refit schedules and independently reconciles all 192 aggregate rows. First/midpoint/last issues in each cell give 24 exact represented-input Fraction OLS comparisons and 24 scalar residual-recursion report comparisons; maximum slope absolute error 1.11e−16 and report relative error 2.843e−16. The [check plan](../../../notes/revision-20261022/ar1-output-check-plan.md) was written after execution but before accuracy tables were read; it is not misrepresented as part of the earlier forecast freeze. The [check code](../../../verify_ar1_output.py) preserves the independent oracle and numerical tolerances. It tests arithmetic/output fidelity, not the financial adequacy of AR or innovation-block representativeness.

The new forecast attempt took 10.692 seconds at its final internal checkpoint (10.75 seconds externally), 104,251,392 bytes internal peak RSS (104,284,160 externally), one observed OS thread across 1465 snapshots and zero swaps. Its largest scenario matrix is 2880x25. The separate readback took 1.332 seconds with 94,126,080 bytes peak RSS and one observed thread. Its resource probe counts files in the existing read-only attempt directories; those byte counts are inputs, not new audit-generated files. No source download, installation, GPU, Monte Carlo randomness, new tuning menu or original-model refit was performed.

## Reproduce with exact local inputs

First follow the [root guide](../../../README.md) to obtain the two hash-matching private inputs and generate a successful fresh conditional replication with a new ID. This AR runner reuses its audited references and refuses existing output IDs. From the root, in the documented NumPy/macOS environment, replace `REPLAY_ID` and `AR_ID` with your fresh identifiers:

```bash
python3 -B run_ar1_replay.py --replication-dir .scratch/revision-20261022/replication-REPLAY_ID --attempt-id AR_ID
mkdir -p state/revision-20261022
python3 -B verify_ar1_output.py --replication-dir .scratch/revision-20261022/replication-REPLAY_ID --attempt-id AR_ID --output state/revision-20261022/my-ar1-readback-01.json
```

The output file and attempt ID must be new. Use ordinary directories without symlink ancestors. New timestamps/resources/paths change receipt hashes; numerical agreement is the relevant reproduction target. Full volatility-filtered historical simulation and autoregressive quantile models remain unexecuted alternatives. Compatible unseen dealer records, original-release vintages, valid inference and observed decision costs remain unresolved.
