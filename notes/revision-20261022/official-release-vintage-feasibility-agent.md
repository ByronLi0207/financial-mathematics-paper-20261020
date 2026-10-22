# Official release-vintage feasibility for PDPOSGS-B

Checked 22 October 2026, approximately 15:56–15:58 UTC. This is a bounded official-documentation and metadata audit. No monetary observation file, forecast, new financial sample, API credential, registration or model run was requested. It does not change the frozen economic-date experiment.

The current manuscript's limitation remains appropriate: **a historical public-release/vintage backtest has not been established**. A documented publication lag and an API route containing `asof` do not establish a vintage archive. This search does not establish that no such archive exists elsewhere.

## Directly inspected official sources

1. [NYFed Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics), owning description and About the Data material. It describes Thursday updates at approximately 4:15 p.m. containing the previous week's statistics; warns that published data may include revisions; and divides the history into structural periods. These statements supply a normal publication convention, not a complete historical calendar of actual releases or unrevised snapshots.

2. [NYFed 15 January 2004 announcement](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html), entire short announcement. It establishes publication with a one-week lag from that date. It does not enumerate later holidays, interruptions, revision events or original observation values.

3. [Current Markets Data API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html) and its directly referenced [official OpenAPI YAML](https://markets.newyorkfed.org/static/docs/markets-api.yml). The HTML was 6,404 bytes, SHA-256 `c1ab76a0e006e7f16c5ba4660716f2ade0f8a76e58dbbe7124d73a9fbf98cd2c`; YAML was 143,746 bytes, SHA-256 `5dbb331d86b91bfc115be9b5fe9c46735833a4f7280d33e4327e8acf7ad30d2b`. Read all eight Primary Dealer route definitions and their referenced record schemas, plus directed global searches for vintage/realtime/revision/lastUpdated. The eight routes cover latest survey by break, all surveys, series definitions, as-of dates, structural breaks, survey by as-of date, survey by series and survey by series/break. The date in `/api/pd/get/asof/{date}.{format}` is explicitly the **time-series as-of date**. The PD value record schema has `asofdate`, `keyid` and `value`; it supplies no documented public-release/vintage selector or observation revision timestamp. Other API families contain `lastUpdated` or revision fields; their existence cannot be assigned to the PD schema. No undocumented query parameter was invented or tested. API software-production version support is a different concept from observation vintages.

4. Fresh, public **metadata-only** requests to [series definitions](https://markets.newyorkfed.org/api/pd/list/timeseries.json) and [structural breaks](https://markets.newyorkfed.org/api/pd/list/seriesbreaks.json) succeeded. The first was 335,616 bytes, SHA-256 `77a7805ffdf634d259bdc94c8eb4ff9f44acb7c5ea7c1246f05152a971d4c7c0`; the second was 716 bytes, SHA-256 `ef2ba93b10af9551181daf5a6f013dab9774ad0c84b9136d51fc17b79164ab78`. The current definition identifies `PDPOSGS-B` as Treasury-bill dealer long positions less short positions. Structural breaks are schema periods; they are not publication vintages. These responses contain definitions/dates rather than monetary observations. They do not validate the previously accepted snapshot against original releases.

5. [ALFRED Help](https://alfred.stlouisfed.org/help), selected opening questions through vintage verification. ALFRED explains that it preserves prior reported versions and normally adds new/revised observations soon after source release. Its release-date hierarchy uses the source's actual release date when available, otherwise a provider date, otherwise first FRED availability. Consequently even an ALFRED vintage date needs its own timing interpretation; generic service availability does not prove this exact NYFed series is covered or preserve intraday release time.

6. [FRED API Real-Time Periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html), complete short page, and [series vintage-date endpoint](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html), description/parameters and example structure. `realtime_start`/`realtime_end` identify the information period, distinct from economic observation dates. Vintage dates identify changes/new releases and omit release occasions when a series did not change. The examples use another series; they are not evidence for `PDPOSGS-B` membership. The [API-key documentation](https://fred.stlouisfed.org/docs/api/api_key.html) requires registered keys for these web-service requests. No key was located, requested, registered or submitted.

## What the directed FRED/ALFRED search did and did not resolve

Exact-key and narrowly targeted official-domain searches for `PDPOSGS-B`, `PDPOSGS`, and Treasury-bill dealer net positions did not identify a verified FRED/ALFRED counterpart. The ordinary web reader could not access the exact-key FRED and ALFRED website search URLs. That is an access/search limitation, **not proof of catalog absence**. Generic dealer-credit-facility and Federal Reserve balance-sheet matches concern different quantities and were not substituted.

A search surfaced an official old `dealpdf.pdf` release packet with an indexed January 2022 release header. Its complete file/body was not opened or acquired here, and no monetary contents were extracted. One indexed old release packet does not establish a complete, immutable, machine-readable archive spanning the study's 2013–2026 history. No release-packet crawler or archive reconstruction was started.

## Required distinctions

| Item | Meaning established here | What remains unverified |
|---|---|---|
| Economic/as-of date | Date attached to the reported position observation | Its availability to an outside forecaster at that date |
| Normal release schedule | Thursday afternoon, prior-week data, per current owning page | Actual historical timestamp, holiday changes and interruptions for every issue |
| Revision/vintage | Previously published values can be revised | Complete earlier values and their information intervals |
| API retrieval time or HTTP metadata | When the present response was fetched/served | Original release time or the full revision history of each value |
| `lastUpdated` elsewhere in the API | Field in another operation's schema | A PD observation-level revision/release clock |
| Structural series break | Data-definition period | Original-publication vintage or revision event |

## Implications for a future study, not a new experiment

The following are design deductions, rather than claims from the official pages. A genuine public-information replay needs a mapping from each economic observation to first availability, subsequent versions, and a stated evaluation-realization vintage. Predictor construction, the known current-position floor, completed-label eligibility and refit/selection timing must all use the same issue information set. Changing only a feature lag while retaining a not-yet-public contemporaneous floor would not solve the timing problem.

At a public release, a target defined as the next H economic records and a target defined as the next H releases can answer different questions. Some economic records after the last published observation may already have occurred before its public release. The issue clock, target start, known floor and label-maturity rule therefore require a new explicit contract; they cannot be recovered by relabeling the present record-index exercise.

For the present paper, retain the narrower downloaded-vintage, economic-date replay interpretation and the explicit unresolved historical-vintage limitation. A future extension should proceed only after an exact official counterpart or a sufficiently complete original-release archive is verified, together with date semantics and versions. No additional financial computation or stronger availability claim is justified by this audit alone.
