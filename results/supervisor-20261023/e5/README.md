# E5: frozen-prediction panel check

This post-result exploratory diagnostic reuses exactly the twelve eligible series in the original panel manifest. The series share a dealer reporting system and overlapping economic positions; they are not independent dealer replications. No new data were downloaded, no series were substituted, and no new model family was added.

## Frozen prediction and chronology

- Prediction: `protocol/supervisor-20261023/e5-panel-prediction.md`.
- Standalone prediction commit: `8baa2f5b44327b3ba295927bd3db954f3475d35d`, committed at **2026-10-23T18:27:50Z**.
- Prediction file SHA-256: `c9f82b37ee82dc000e6bf2590b1ef29195a0c442e7d3128536b6658d36f16d87`.
- Run started: **2026-10-23T18:30:55.671193Z**; first new fit: **2026-10-23T18:30:55.774398Z**.
- Run completed: **2026-10-23T18:31:33.256996Z**; elapsed **37.58584783296101 seconds**.
- All **48/48** planned cells completed on their first attempts. No failed fit was retried and no attempt was overwritten.

The executed command, from the current repository root, was:

```sh
'/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3' -B round2_panel_run.py --run
```

This is the historical execution command, not an instruction to rerun this frozen check. The runner uses exclusive output directories and refuses to overwrite the existing attempt.

## Results and fixed predictions

| Prediction | Observed success count | Frozen threshold | Decision |
|---|---:|---:|---|
| P1: expanded QR33+ improves original QR33 within the 45 original losing cells | 30/45 | at least 40 | Unsupported |
| P2: expanded QR33+ lies within the inclusive ±10% band around F | 24/48 | at least 36 | Unsupported |
| P3: selected penalty is at least 1 | 33/48 | at least 25 | Supported |

The median loss change relative to frozen F is +92.62799824594052% for original QR33, +9.90727239745182% for QR4+, +9.220703399904492% for QR33+, and +0.5006801691981209% for I. Expanded QR33+ still loses to F in 34 cells and wins in 14; 24 cells meet the frozen ±10% condition. Across all 48 cells it improves original QR33 in 31, equals it in 15, and worsens it in 2. These results support mitigation of the original deterioration, not its general elimination or a claim of equivalence. They do not prove that conditional predictors contain no usable information.

`summary.csv` contains all 48 rows with series, H, W, status, selected penalty, F/original QR33/QR4+/QR33+/I native-unit mean losses, strict breach counts, and relative loss changes. `prediction-assessment.json` preserves the fixed-denominator decisions. `descriptive-summary.json` provides the exact descriptive counts, medians and penalty distribution used for manuscript writing.

## Original-source aliases and private data

The read-only prior checkout is `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/`. `inputs/panel/` is a byte-exact copy of its `results/revision-20261023/round2/panel/`: the selection manifest, original aggregate CSV, 48 cell JSON records, all fourteen source provenance records, and descriptive counts. The two calendar-ineligible downloads remain skipped. `inputs/port-lineage/` preserves the two original panel entry points; `inputs/protocol/` preserves the earlier panel design. `input-inventory.json` records original paths, copied aliases, bytes and SHA-256 for all 130 copied files before the first new fit.

The ported root-level `round2_panel_sources.py` retains the original `align_source` function unchanged. The QR33 segment in `round2_panel_run.py` retains the original configuration and forecasting core. All six core dependency files match the prior checkout byte for byte. The first three validation-menu candidates also reproduce all 144 corresponding original validation losses exactly; only the menu was extended.

Raw observations and per-origin financial arrays remain under the ignored private root `.scratch/supervisor-round2-20261023/e5/`. Its `sources/` contains the twelve retained raw CSVs plus the immutable Treasury date-grid CSV; `old-traces/` contains the 48 copied archival arrays; `cells/` contains the new validation and evaluation traces. They are excluded from this public result bundle and from the study-code license. Original source provenance supplies the official URLs, publisher, acquisition dates, unit, fingerprints and historical redistribution convention. The analysis implies no New York Fed endorsement.

## Verification and limits

Before fitting, `contract-checks.json` verifies unchanged alignment/core code, full-menu failure rejection and exact-tie preference for the larger penalty. Every cell saves its complete menu in `selection-before-evaluation.json` before evaluation starts. `verification.json` independently rescored 240 evaluation arrays and 240 validation segments, checked 2,016 new fit diagnostics, and found zero absolute mean-loss discrepancy. Strict breach counts and completed-label timing agree. The archived F, original QR33 and QR4+ arrays were rescored without refitting.

`run-receipt.json` binds the prediction commit, file/code hashes, chronology and measured resources. The frozen limits were one worker, one numerical thread, 590 seconds per cell, 10,800 seconds overall and 2 GiB RSS. The observed maximum was one OS thread, 43,483,136 bytes RSS and 1.6224872081074864 seconds for a cell. No pooled significance calculation treats the twelve series as independent. No PDF or figure is created by the E5 runner.
