# Independent position-data feasibility and measurement boundaries

This dated evidence record consolidates the source investigation conducted on 21–22 October 2026. It distinguishes inspected documentation, successful source acquisition and unresolved leads. It is not an exhaustive catalogue of public inventory data or a statement that the listed endpoints will remain unchanged. No new source retrieval or third-source experiment was performed when preparing this consolidated note.

The investigation sought another observed, signed financial position series on which the same sampled absolute-peak functional could be studied. A source's relevance depended on its measurement, chronology, availability and reuse conditions. Changing frequency or dataset title alone did not establish independent financial provenance.

## What the accepted external source adds

The Federal Reserve Bank of New York's [Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) supply an independently compiled aggregate-position application. The accepted series, `PDPOSGS-B`, is the long-position amount less the corresponding short-position amount for Treasury bills across reporting primary dealers. The [official time-series definitions](https://markets.newyorkfed.org/api/pd/list/timeseries.json) identify the key; the [FR 2004 register and original forms](https://www.federalreserve.gov/apps/reportingforms/Report/Index/FR_2004) establish weekly Wednesday-close measurement and market/fair-value accounting in millions of U.S. dollars.

The evidence consists of selected original form and instruction passages, official definitions and reporting-era metadata, API documentation, release information, and the subsequently acquired CSV. It does not rest on units inferred from the numerical scale. The form review covered the 1998 and 2001 first pages, the 2015 and 2024 position-form pages, and selected accounting, consolidation and confidentiality instructions. It did not audit every page or every historical reporting change.

| Accepted CSV identity | Recorded value |
| --- | --- |
| Official acquisition route | [Current Treasury-bills series CSV](https://markets.newyorkfed.org/api/pd/get/PDPOSGS-B.csv) |
| Acquisition date | 22 October 2026 |
| Size | 23,315 bytes |
| SHA-256 | `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb` |
| Records | 706, excluding the header |
| Economic dates in this snapshot | 2013-04-03 through 2026-10-07 |
| Exact header order | `As Of Date`, `Time Series`, `Value (millions)` |
| Native financial unit | USD millions |
| Earlier alias | Not spliced into the accepted sample |

The accepted source validation subsequently confirmed finite monetary tokens, the exact series key and header, unique increasing dates and seven-day adjacent intervals in these bytes. The earlier metadata-only checks are not represented as having established those facts before acquisition. The detailed [external-data record](../../results/revision-20261022/EXTERNAL_DATA.md) distinguishes acquisition, source validation, the frozen design and completed evaluation. A file hash identifies the retrieved snapshot; it does not identify an original public-release vintage or promise that later endpoint responses will match.

This compilation has a reporting and publication lineage distinct from the anonymous FX client-position record. That is the basis for calling it an independently sourced application. It does **not** establish probabilistic independence, a disjoint set of underlying institutions, an unchanged reporting panel or a second individual dealer's hourly client-flow history. Publisher differences cannot resolve unknown institutional overlap.

Treasury-bills net market value is also a different financial measurement. Changes can reflect trades, valuation, reporting composition and accounting events. Netting signed positions across dealers and instruments can conceal offsetting exposures. The absolute value of an aggregate is not the sum of individual absolute positions; its sampled peak is not gross dealer risk, cash funding need, capital need or an unobserved within-week maximum.

### Release timing and the information convention

The [current owning page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) describes Thursday updates at approximately 4:15 p.m. for the preceding week's statistics. The [15 January 2004 announcement](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html) establishes a one-week publication lag. Measurement at Wednesday close, submission by reporting institutions and public availability are separate events. About eight calendar days between Wednesday measurement and the following week's Thursday release is an ordinary-calendar implication of that schedule, rather than an independently reconstructed release calendar. Holiday adjustments and precise historical release times were not obtained.

The data can be revised. The inspected [API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html) and [OpenAPI schema](https://markets.newyorkfed.org/static/docs/markets-api.yml) supplied economic as-of dates but no verified historical release-vintage selector in the audited routes. This is an evidence limitation, not proof that an as-released archive exists nowhere.

The study therefore declares a retrospective downloaded-vintage replay indexed by economic as-of date. Its sampled peak includes the current record, whose absolute value is a lower bound under that stipulated replay convention. The public release schedule does not establish that a public observer knew the current physical position at Wednesday measurement time. This application does not supply a live public-information backtest or validate the original dealer's operational capacity decision.

The same mathematical functional can be applied to both paths while the economic task changes. Six or twenty-four Treasury records are weekly records; the original FX application uses nominally hourly records with its recorded gaps retained. Histories, neighbor menus and refit schedules are source-adapted. Raw monetary losses in USD and USD millions are not pooled. A second source can test the behavior of the declared procedure families on another measured process without becoming replication of one common operational effect.

## HKMA foreign-currency positions: documented candidate, incomplete acquisition

The Hong Kong Monetary Authority's [foreign-currency-position documentation](https://apidocs.hkma.gov.hk/documentation/market-data-and-statistics/monthly-statistical-bulletin/banking/fc-position-all/) describes monthly records identified by `end_of_month`, in HKD millions. The actual [official OpenAPI schema](https://apidocs.hkma.gov.hk/wp-content/uploads/swagger/T031001-swagger.json) was obtained: 6,361 bytes, SHA-256 `60274f8533948397c1e692875013d83b42d15f8944e3dc99257e7fd6681ad742`. Its financial fields are:

- `spot_assets` and `spot_liabilities`;
- `forward_purchases` and `forward_sales`;
- `net_spot_position`, `net_forward_position` and `open_position`.

The [September 2010 financial-stability report, Chart 5.17 notes](https://www.hkma.gov.hk/media/eng/publication-and-research/quarterly-bulletin/qb201009/E_halfyear.pdf) defines net spot as spot assets less spot liabilities, net forward as forward purchases less forward sales, and net open as their sum. Its selected narrative concerns authorized institutions' aggregate foreign-currency positions. The [March 2013 report, Chapter 4, footnote 19](https://www.hkma.gov.hk/media/eng/publication-and-research/quarterly-bulletin/qb201303/chapter4.pdf) cautions that net-spot changes include price and exchange-rate valuation effects. Only these definition and measurement passages and relevant chart notes were read; neither report was audited in full.

The documented July 1990 exclusion of certain structural assets and liabilities is an accounting break, not evidence of a stationary later process. A net spot position and a net open position define different exposure objects; selecting between them would require a new frozen measurement decision. These fields do not, by themselves, establish pure customer flows, gross currency exposure or a complete hedged book.

The [documented API endpoint](https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/banking/fc-position-all) was attempted with the date field alone. Two bounded, certificate-verified requests timed out after 20 seconds; one recorded zero response bytes. No successful date response or financial observation body was obtained. Actual coverage, record count, missingness, units as represented in observations and observation-file identity therefore remained unverified. The documentation's example month was not treated as a verified first observation.

The owning [Monthly Statistical Bulletin page](https://www.hkma.gov.hk/eng/data-publications-and-research/data-and-statistics/monthly-statistical-bulletin/) separately supplied the actual Section 3.10 link to [the all-foreign-currencies workbook](https://www.hkma.gov.hk/media/eng/doc/market-data-and-statistics/monthly-statistical-bulletin/T031001.xls). This was an observed official link, rather than an inferred filename. The page labeled it 109.5 KB. An HTTP HEAD check returned 200, `application/vnd.ms-excel`, `Content-Length: 116224` and `Last-Modified: Fri, 09 Oct 2026 07:56:39 GMT`. These are recorded response metadata. **The workbook body was not acquired or parsed**, and no observation hash or successful date-column inspection is claimed.

This audit did not verify a usable CSV alternative. The API timeout and unparsed workbook do not show that a CSV, another official export or compatible inventory data do not exist. They record the bounded access and format boundary reached here. HKMA remains a documented candidate, rather than an evaluated third source or a basis for choosing a favorable result.

## Other close leads and why they do not supply the missing dealer validation

| Lead | Actual inspection | Supported conclusion and remaining boundary |
| --- | --- | --- |
| Barbiero, Bräuning, Joaquim and Stein, *Dealer Risk Limits and Currency Returns* | Cover/introduction and selected Section 2 data passages of the [author-hosted 9 October 2026 version](https://obarbiero.github.io/files/FXdealerlimits.pdf), including physical page 15, footnote 24; not all 110 pages, proofs or empirical tables. | The paper identifies its underlying FRVV-1/FRY-14Q supervisory records as confidential. Public forms and published figures do not supply those reusable raw dealer histories. Its bank-quarter/currency risk-limit response also differs from the present sampled-peak response. This lead informs measurement and nearby research; no public record-level dataset was obtained. |
| CFTC Traders in Financial Futures | Entire four-page [explanatory notes](https://www.cftc.gov/sites/default/files/idc/groups/public/@commitmentsoftraders/documents/file/tfmexplanatorynotes.pdf), selected current [COT description](https://www.cftc.gov/MarketReports/CommitmentsofTraders/AbouttheCOTReports/index.htm), the TFF catalogue sections of [Historical Compressed](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm), and all 87 listed [schema field names](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalViewable/cotvariablestfm.html). No observation rows or annual archives were acquired. | This is a separately published weekly futures-position compilation grouped by trader category, including dealer/intermediary. It is not an individual OTC FX dealer's hourly client inventory. Category membership, spreading, contract units, publication lag, suppression and corrected/backcast files require a separately defined task. Actual sample continuity, size, missingness, vintage and redistribution rights were not certified. |
| Alternative frequencies, currencies or derived files in the original FX source family | Public dataset metadata and a partial file inventory, plus the source-lineage discussion in Wisniewski, Lindsay and Lindsay (2020), [*Application of conformal prediction interval estimations to market makers' net positions*](https://proceedings.mlr.press/v128/wisniewski20a.html), and selected chapters of Wisniewski's [Royal Holloway thesis](https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/). The dataset-wide inventory and every alternative file were not audited. | Resampling the same originating history, taking another currency column or using derived features does not establish another originating dealer. A similarly described alternative source-family record also requires primary provenance establishing a separate feed. No compatible second dealer was authenticated from these leads. |
| U.S. Treasury FC-1 weekly aggregate positions | Treasury Bulletin introduction screened and a bounded [FiscalData date-only route](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/tb/fcp1_weekly_report_major_market_participants?fields=record_date&sort=record_date&page%5Bsize%5D=1) attempted. | Certificate verification failed; no response body was accepted. No TLS verification bypass, usable observation sample, schema/date validation or source hash followed. This remains an undeveloped access lead, not a verified available dataset and not evidence that the series is unavailable. |

The CFTC materials ordinarily distinguish Tuesday measurement from Friday publication. Treating a Tuesday measured position as known that Tuesday would be a different and unsupported information convention. The explanatory notes contain launch-era and backcast descriptions; they were not treated as a newly verified 2026 operating procedure. No catalogue listing was promoted to a successful download of every annual archive.

Price returns, simulated inventories and inventories reconstructed from assumed trade signs can support other studies, but they are not observed independently sourced dealer positions. They were not substituted for the missing compatible dealer record in this revision.

## Access, attribution and raw redistribution

Free retrieval, public metadata and permission to run analysis are separate from permission to redistribute raw files under the repository's code license.

The inspected [New York Fed Terms of Use](https://www.newyorkfed.org/privacy/termsofuse.html), marked 9 June 2023, permit specified access, storage, copying and derivatives subject to conditions concerning source/copyright notices, identification of modifications, continuing permissions and restrictions, and no implied endorsement. The accepted data remain subject to those terms; they were not declared public domain or relicensed as code. The detailed source record supplies the attribution used by this study.

The inspected [HKMA general notes](https://www.hkma.gov.hk/eng/data-publications-and-research/data-and-statistics/monthly-statistical-bulletin/general-notes) allow reproduction with source acknowledgment and describe periodic revision. The [HKMA terms](https://www.hkma.gov.hk/eng/other-information/terms-and-conditions-of-use/), last revised 26 August 2019 when inspected, place conditions on reproduction and API use in paragraphs 12 and 17. These are conditional permissions, not a public-domain or MIT grant. Release and workbook modification dates do not constitute an original-release vintage archive.

The original FX dataset's visible label, **Data files © Original Authors**, did not establish a separate permissive raw-redistribution grant or complete rightsholder chain. The CFTC and undeveloped Treasury leads were not certified for raw republication in this audit. Unverified permission is an unresolved question, rather than a categorical assertion that reuse is prohibited.

The result package therefore provides acquisition instructions, source identities, original code and analytical aggregates rather than republishing raw observation files. Source rights and the study's original analysis remain distinguishable. Successful access to one route does not authorize redistribution of unrelated papers, datasets or supervisory records.

## What remains unresolved

This bounded investigation established one usable official external aggregate source and several documented alternatives with concrete limits. It did **not** locate and authenticate a compatible second individual-dealer hourly client-flow history, obtain historical public-release vintages, or eliminate aggregation and valuation differences. Nor did it establish that such data cannot be found elsewhere.

HKMA observation acquisition and parsing, CFTC observation-level continuity and permissions, and the Treasury FC-1 access lead remain incomplete. No unrun source receives a forecast-performance result. The accepted Treasury application is retained with its different measurement and information convention; incomplete alternatives do not justify replacing it after outcomes with a more favorable source. A new compatible dataset would require its own provenance, rights, version, information-set and design checks before becoming a further validation claim.

The later [long-short-game dataset follow-up](longshort-data-feasibility.md) follows a newly read primary-paper citation. Public metadata were acquired, but no raw CSV was downloaded: listed sizes fail a conservative budget screen while actual transfer/expanded bytes were not measured, the license label is Unknown, and compatible absolute positions and independent real-dealer provenance remain unauthenticated. This is an additional documented lead, not completed third-source validation.
