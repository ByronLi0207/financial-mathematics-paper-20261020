# External data: New York Fed Treasury-bills net positions

This document records the external application's source, accepted snapshot, measurement, timing and reuse conditions. Source validation and the prespecified evaluation and historical-reference phases are complete. The strict loader accepted 706 finite monetary observations with the declared schema and chronology, and all twelve NYFed validation receipts record the same source identity. The [combined evaluation summaries](evaluation-summary.csv) contain 90 rows across the two applications. The [independent evaluation audit](evaluation-audit-02.json) reports `VERIFIED` after source-and-array reconciliation. Data acceptance and successful numerical reconciliation establish reproducibility checks; forecast comparisons retain the measurement and information limits below.

## Source and measured object

The Federal Reserve Bank of New York's [Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) provide the series `PDPOSGS-B`. The [official series definitions](https://markets.newyorkfed.org/api/pd/list/timeseries.json) identify it as the Treasury-bills dealer long-position amount less the corresponding short-position amount. The result is a **signed aggregate position across reporting primary dealers**, measured in **millions of U.S. dollars**. The [FR 2004 reporting register and forms](https://www.federalreserve.gov/apps/reportingforms/Report/Index/FR_2004) establish the weekly Wednesday-close basis and market/fair-value accounting.

This is a security-position measurement, rather than trading volume, pure customer order flow or a complete hedged book. Changes may reflect trades, valuation and reporting composition. Taking an absolute value after summing signed dealer positions permits cancellation between institutions; it does not recover the sum of their individual absolute exposures or peaks. The sampled aggregate peak therefore does not identify individual-dealer risk, gross exposure, capital, cash funding needs or unobserved within-week maxima.

The independently compiled official series supplies another financial measurement process for the mathematical peak application. Its publication lineage is separate from the original anonymous FX client-position dataset. This does not establish a disjoint set of underlying institutions, a fixed reporting panel or probabilistic independence, and it does not supply a second hourly individual-dealer record.

## Accepted snapshot

The exact acquisition route is:

```
https://markets.newyorkfed.org/api/pd/get/PDPOSGS-B.csv
```

| Field | Accepted identity |
| --- | --- |
| Acquisition date | 22 October 2026 |
| Format | CSV |
| Source key | `PDPOSGS-B`, on every record |
| File size | 23,315 bytes |
| SHA-256 | `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb` |
| Observations, excluding header | 706 |
| First economic date | 2013-04-03 |
| Last economic date in the snapshot | 2026-10-07 |
| Header, in source order | `As Of Date`, `Time Series`, `Value (millions)` |
| Native monetary unit | USD millions |
| Date order | Unique and strictly increasing |
| Adjacent intervals differing from the seven-day nominal interval | 0 |
| Earlier historical alias | Not spliced into this sample |

The validation receipts, including [H6/W260 KNN](validation-nyfed_weekly-h6-w260-KNN.json) and [H24/W52 QR](validation-nyfed_weekly-h24-w52-QR.json), retain the accepted byte count, hash, record count, native unit, boundary dates and irregular-gap count. All twelve receipts agree on those fields. Their shared executable-freeze identity is `e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb`.

The [strict source loader](../../conditional_sources.py) verifies a caller-pinned byte count and SHA-256 before parsing financial tokens. It requires the exact header and series key, unambiguous dates, strict chronology and finite numeric positions. Missing, suppressed, malformed or nonfinite values, duplicate or reversed dates, and source-identity discrepancies stop loading. It does not delete, sort, interpolate or replace observations, convert units, or splice an older series alias. The zero irregular-gap count is an observed property of this accepted snapshot, rather than an assumption used to manufacture a regular grid.

For definition provenance, the official time-series metadata retrieved on 22 October 2026 contain 335,616 bytes and have SHA-256 `77a7805ffdf634d259bdc94c8eb4ff9f44acb7c5ea7c1246f05152a971d4c7c0`. The target entry carries the reporting-era tag `SBN2024`. That tag is not an original-release vintage identifier for every historical row.

## Acquisition and exact-version reproduction

Retrieve the HTTPS route with a 2 MiB response cap, retain the returned bytes locally, and record the acquisition time, URL, byte count and SHA-256. Compare the byte count and digest above before parsing. The endpoint's last observation date is not a certification that no later report exists elsewhere, and its current response need not remain identical to this snapshot.

Do not automatically overwrite an accepted local snapshot when a later download differs. Retain both identities and document the discrepancy. If the accepted bytes cannot be recovered, a new download supports a separately versioned rerun; it does not establish exact reproduction of this version. The hash identifies the retrieved file, not a publisher-assigned permanent dataset version.

The repository supplies original analysis code, aggregates, acquisition instructions and source fingerprints. The raw CSV is not redistributed in this result package. Source data remain subject to the publisher's terms and are separate from the repository's code license.

## Public release and downloaded vintage

The [owning page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) describes Thursday updates at approximately 4:15 p.m. for the previous week's statistics. The [15 January 2004 announcement](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html) established a one-week publication lag. Economic measurement at Wednesday close and subsequent public release are distinct events. The ordinary-calendar implication is about eight days between measurement and the following week's Thursday publication; precise historical release times and holiday adjustments have not been reconstructed.

The source can be revised. The audited [API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html) and [OpenAPI schema](https://markets.newyorkfed.org/static/docs/markets-api.yml) provide economic as-of dates, but the inspected routes supplied no verified historical release-vintage selector. This does not establish that an as-released archive is unavailable everywhere.

The experiment consequently uses a **retrospective downloaded-vintage replay indexed by economic as-of date**. Its information convention treats the current and earlier recorded values as available at the index of issue. This is a stipulated replay convention, not evidence that a public observer knew the current physical position on its measurement date. “Final vintage,” where used in earlier materials, means the frozen downloaded snapshot; the publisher has not certified permanent finality. This application cannot support a live public-information or original-release backtest claim.

## Target, time boundaries and transfer interpretation

For signed sampled position N, the target includes the current record:

$$
P_{t,H}=\max_{0\le h\le H}|N_{t+h}|,
\qquad B_t=|N_t|,
\qquad G_{t,H}=P_{t,H}-B_t.
$$

For Treasury, H=6 and H=24 count subsequent **weekly records**. They do not represent the original FX application's six or twenty-four nominally hourly records; its long date gaps also remain records rather than fixed elapsed hours. Neither application observes every intervening path excursion. The current lower bound B is known under the declared retrospective issue convention.

| Segment | Zero-based origin indices | Economic dates | Origin count |
| --- | --- | --- | ---: |
| Validation | 329–380 inclusive | 2019-07-24 through 2020-07-15 | 52 |
| Evaluation | 405–681 inclusive | 2021-01-06 through 2026-04-22 | 277 |

The last validation label at H=24 ends at index 404, dated 2020-12-30, before evaluation starts. Both horizons share the final issue origin at index 681, dated **2026-04-22**. The last H=6 label ends at index 687, dated **2026-06-03**; the last H=24 label ends at index 705, dated **2026-10-07**, the last source record. Fitted models use only labels completed by their refit date; later completed evaluation labels enter subsequent refits according to the frozen schedule. These are design and data boundaries, not forecast-performance findings. The [frozen design](../../protocol/revision-20261022/conditional-baseline-design.md) specifies the model menu, tuning, resources and failure rules.

This is a **source-adapted procedure-family comparison**. Training windows, refit schedules and neighbor menus differ between the FX and Treasury applications. The source-specific primary references also differ. A matching sign in their primary comparisons would not identify one common replicated effect. Within-source matched-history comparisons must accompany any transfer interpretation; shared histories and overlapping labels remain dependent.

Treasury scores retain USD-million units, while the original FX scores retain USD units. Raw monetary losses are not pooled across sources. A second measurement process and successful numerical validation do not create a new estimator, prove conditional coverage, validate individual-dealer operations or establish funding, hedging, quoting or profit benefits. Forecast conclusions must follow the complete prespecified evaluation, including adverse outcomes and failures.

## Attribution and reuse

The [New York Fed Terms of Use](https://www.newyorkfed.org/privacy/termsofuse.html), marked 9 June 2023 when inspected, permit access, storage, copying and derivatives subject to their conditions. Preserve copyright/source notices and applicable permissions and restrictions, identify modifications, and avoid implied endorsement. Source data are not relicensed under the code license or represented as public domain. Reference-rate and staff-paper provisions are separate from this position series.

The default attribution, where no content-specific form supersedes it, is:

> © 2026 Federal Reserve Bank of New York. Content from the New York Fed subject to the Terms of Use at newyorkfed.org.

The underlying series is freely available through the [official data page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics). Derived tables and figures are this study's analysis of the identified snapshot; they are not New York Fed findings and carry no claimed endorsement.
