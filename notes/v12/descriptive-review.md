# F4.1 descriptive table review and single execution

Reviewed and executed on 2026-10-25 after root authorization and the completed F3 attempt (root-reported commit `773b7ab`). No Git command was run in this subtask. No scientific core, main manuscript or supplement was edited; only the descriptive script, its permitted backups, new descriptive outputs, this note, and the exact generated-table copy were written.

## Scientific review

* H=6 uses `m=N-6` origins `0..N-7`, inclusive. The three quantities share exactly these origins. The peak is initialized to the issue magnitude and then maximized over six subsequent records, so the issue anchor is included and each headroom is nonnegative by construction.
* Stable means preserve constant values, otherwise use `math.fsum/m`. Sample SD uses denominator `m-1`. The empirical p95 is the one-based rank `ceil(95*m/100)` without interpolation. These definitions were unchanged during the display/provenance edit.
* FX display statistics are computed after dividing USD values by 1e6; bill/panel inputs are already USD millions. CFTC retains native contract counts.
* Panel and CFTC rows contain nine separate medians of their within-series statistics. They do not pool exposure vectors or supply independent-series inference. In particular, a median peak mean minus median anchor mean need not equal the median headroom mean; the identity is checked within each source instead.
* The saved 32 source rows have finite nonnegative displayed summaries, `origin_count=N-6`, `last_origin=N-7`, and within-source mean(Y)-mean(B)=mean(Z) within floating arithmetic. All five displayed summary rows exactly match the medians of the saved per-source statistic columns; no financial series was reloaded to repeat calculations.

## Dates and counts

| Source | Series | N per series | Matched H6 origins per series | Display unit | Aligned source span |
|---|---:|---:|---:|---|---|
| FX, hourly | 1 | 18576 | 18570 | USD millions | 2014-02-05 to 2017-01-24 |
| FX, daily | 1 | 930 | 924 | USD millions | 2014-02-05 to 2017-01-24 |
| Treasury bills | 1 | 706 | 700 | USD millions | 2013-04-03 to 2026-10-07 |
| NY Fed panel | 12 | 706 | 700 | USD millions | 2013-04-03 to 2026-10-07 |
| CFTC panel | 17 | 877 | 871 | contracts | 2010-01-05 to 2026-10-20 |

Daily FX exactly matches the existing last-per-nonempty-source-naive-day aggregation and all archived fingerprints. The old daily validation grid is 329–380, **2015-02-24T23:59:59.999999 to 2015-04-24T23:59:59.999999**; the old evaluation grid is 405–905, **2015-05-24T23:59:59.999999 to 2016-12-27T23:59:59.999999**, 501 issues. These are the preserved common H24 endpoints; the full-source H6 descriptive sample has 924 origins and is explicitly distinct. Both readout-binding dates and the old daily protocol/cell geometry were checked during the single execution.

Hourly FX retains both existing inspected periods: original validation 2015-10-08 to 2015-12-30 and evaluation 2016-01-01 to 2017-01-23; early-2015 validation 2015-04-21 to 2015-07-13 and evaluation 2015-07-15 to 2015-10-06. Treasury/panel validation is 2019-07-24 to 2020-07-15 and evaluation 2021-01-06 to 2026-04-22. The panel's 707 raw rows are aligned to the existing 706-date grid through 2026-10-07. CFTC displays actual economic dates (sample 2010-01-05 to 2026-10-20; validation 2020-08-11 to 2021-08-03; evaluation 2021-09-21 to 2026-09-08); metadata separately retains the Monday model clock, and both axes match the archived split receipt.

## Actual five-row summary

The following values are copied from saved `summary.json`; full precision and all numeric bindings remain in the output files. Means, SDs and p95 entries for multi-series groups are separate medians.

| Source | B mean | B SD | B p95 | Y mean | Y SD | Y p95 | Z mean | Z SD | Z p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FX, hourly | 8.917012394102093 | 10.182604636790247 | 27.623827640000002 | 11.065182699622499 | 11.654865223116602 | 30.179292359999998 | 2.148170305520405 | 5.923724122217754 | 7.960912700000001 |
| FX, daily | 9.001982545918398 | 10.48931924674969 | 27.53478021 | 17.907551967484846 | 16.551290122008037 | 41.02597926 | 8.905569421566451 | 14.792888652637604 | 24.949386805000003 |
| Treasury bills | 39462.77 | 27226.017326327077 | 92563.0 | 55296.69714285714 | 30359.668844564778 | 108323.0 | 15833.927142857143 | 15968.154340092628 | 50020.0 |
| NY Fed panel | 12372.707142857143 | 8337.376318425395 | 33344.5 | 16011.31357142857 | 9036.397274362535 | 37413.5 | 3745.430714285714 | 3556.179087801839 | 10538.0 |
| CFTC panel | 60204.7187141217 | 45975.618401874184 | 147849.0 | 81756.21469575202 | 45606.767280707456 | 168570.0 | 19873.51205510907 | 20858.604133519282 | 60555.0 |

## Display edit and backups

Before editing the previously untracked descriptive script, exact backups were created as `report_v12_descriptives.py.pre-descriptive-run.bak` and `test_v12_descriptives.py.pre-descriptive-run.bak`. Their SHA-256 values are respectively `1cd732784f666b78a53924ad1c16c3bd07a7ef400b01933cc8bd946c08bc09b6` and `c3610e42ae492a0584b330eaf52494cdb94dc83af6cd28d3ee85bf1756e5e526`. The test file itself was not changed.

The table note has exactly three sentences, preserving the requested definitions:

> All summaries use complete H=6 origins and include the issue anchor; SD uses m-1, and the empirical 95th percentile has rank ceil(95m/100). Daily FX uses the last record of each nonempty source-naive calendar day at day end; the reported FX comparison periods were already inspected. Dollar values are in millions; panel entries are nine separate medians of within-series summaries, without exposure pooling or independence inference, and CFTC retains heterogeneous native contract counts.

Only display text and execution/source-copy/hash provenance were added to the script; the descriptive arithmetic was not changed. The existing five toy tests were rerun before the real launch: **5 passed in 0.13 seconds**. Test coverage checks H6 anchor/common origins, sample SD, exact empirical rank, unit scaling, per-statistic panel medians and the pre-source-access completion gate. No forecast model or accuracy evaluation was run.

## Exact single-run command and timing

Working directory: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024`.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest==9.1.1 --with numpy==2.3.5 python -B report_v12_descriptives.py --run
```

Started UTC: `2026-10-25T12:15:20.697693+00:00`. Completed UTC: `2026-10-25T12:15:20.894740+00:00`. Recorded elapsed time: `0.1969181247986853` seconds. Exactly one real descriptive invocation was made. The script verified F3 completion at `2026-10-25T12:05:47.564774+00:00` with receipt SHA-256 `f83585a5d65b92b353e39ccc11e567be1f41839add50ad0396916a83ebc03e8c` before source access.

## Artifacts and independent readback

All generated analysis files are in `results/v12/descriptives/`:

* `rawstats.json` / `rawstats.csv`: all 32 source-summary rows.
* `summary.json` / `summary.csv`: the five displayed groups.
* `metadata.json`: definitions, all individual raw/aligned clock ranges, split dates, counts, code/input seals and 31 independently reread source-file byte hashes.
* `data-table.tex`: one table with metadata and nine-statistic panels.
* `number-bindings.json`: 1,324 numeric JSON bindings and 100 table/definition/date bindings.
* `source.py`: exact byte copy of the root reproduction script.
* `runtime.json`: actual timing and completion-gate identity.
* `manifest.json`: sizes/SHA-256 of all nine other output files, input byte proofs and the exact script-copy binding.

Independent readback verified every manifest member's bytes/hash, every numeric and table binding's source SHA and JSON pointer, all fixed counts and all source-group medians. The LaTeX has one table environment and exactly three note sentences. This subtask does not claim compiled/rendered layout QA; root compilation and visual inspection remain required.

Root reproduction script and `results/v12/descriptives/source.py` both have SHA-256 `097d621285bdd5daac6686ee4b9388212db000a4784834a720c376837dedf81a`. The generated `data-table.tex` was copied exactly, without editing main/supplement, to `submission-v10/generated/v12-data-table.tex`; both table files have SHA-256 `3e4b949cb0115720326171ff7adeac3c2fa43b13d0739ce0739b8588288d18c7`. No statistical regeneration followed this copy.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `data-table.tex` | 3469 | `3e4b949cb0115720326171ff7adeac3c2fa43b13d0739ce0739b8588288d18c7` |
| `manifest.json` | 13872 | `86a6c791126629e76e01519bcc79912a5338575f130867d410f7d6554d496c4d` |
| `metadata.json` | 96394 | `d50a39d9984961fc586db66cfb28ca07960ed7372e12390898a25e62352df02e` |
| `number-bindings.json` | 504436 | `d81d99c88f6caadf065b72bbb8abdb7014f8052784de551a6486765db4cc9358` |
| `rawstats.csv` | 10977 | `2d38be2b468859271853741e33b7db2adc81c3903984da029d0fdbdb8e967a7c` |
| `rawstats.json` | 31801 | `e33747bcadb60b1e6d33978b46c08629692958f7c3478d2b41701f9436da0657` |
| `runtime.json` | 924 | `539c23007a99e1649fc80aa6437d7950d2073ae8e06873ccd260a357b7845955` |
| `source.py` | 25917 | `097d621285bdd5daac6686ee4b9388212db000a4784834a720c376837dedf81a` |
| `summary.csv` | 1282 | `ccd38f7a886871119f859aab56764b9612d2c483d219bec4fecc482b360167ee` |
| `summary.json` | 3873 | `2c6de7c49842e045fdc315839950845053ef1e72db326b959d218ba935675c8c` |
