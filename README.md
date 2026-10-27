# Peak net-position limits: submission-final

This study asks whether conditional quantile models forecast the largest absolute net position reached within a review horizon better than matched historical rules. It compares hourly FX positions, weekly New York Fed dealer aggregates and CFTC dealer positions. Conditional gains depend on the reference, history and tuning evidence; negative, numerical-failure and indeterminate results remain visible. Limit-cost rankings also depend on stipulated preferences.

The only current submission entrance is [submission-package/MANIFEST.md](submission-package/MANIFEST.md), on **submission-final**. The primary package targets Applied Stochastic Models in Business and Industry; [Quantitative Finance](submission-package/QF/README.md) is an alternative format of the same study. The [MJL and publisher audit](notes/submission/journal-shortlist.md) verifies SCIE coverage and separates unverified quartiles and policy details. No manuscript has been submitted by this task.

The current ASMBI editorial revision has passed writing, numerical-provenance, source-archive compilation and page-review checks. The complete test suite also passed using a temporary dependency environment explicitly authorized by the author. Publication and local cleanup are checked separately after R8. See [the execution ledger](ASMBI_FINAL_CHANGELOG.md). Complete earlier supplementary results remain in [EXTENDED_RESULTS.md](EXTENDED_RESULTS.md).

## Reproduction and scope

Start with [REPRODUCING.md](REPRODUCING.md). Document compilation, inspection of saved aggregates, software tests and financial re-estimation are separate operations. This final round changes writing and packaging only; it performs no new experiment or financial fit. The [source-import audit](notes/submission/import-audit.md) and [prewritten-prediction register](notes/submission/prediction-register.md) preserve source identities, timing limits and adverse judgments.

A bounded [code and aggregate release](submission-package/RELEASE/README.md) omits raw observations and private pointwise vectors. It is not a full-data reproduction bundle. The repository has no selected software license or new Zenodo DOI; both require the author's decision. Existing third-party source and template conditions continue to apply.

## Data access

- **FX:** obtain the specified Net Position Time Series Dataset from [its Kaggle source](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset), subject to the original rights holders' terms. The exact input fingerprint is documented; raw FX and private forecasts are excluded.
- **New York Fed:** [Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) provides the public dealer aggregates. The accepted Treasury snapshot is preserved with attribution. The original panel CSV is not redistributed; a current download is not guaranteed to reproduce the original vintage. Respect the Bank's [Terms of Use](https://www.newyorkfed.org/privacy/termsofuse.html).
- **CFTC:** unchanged public TFF downloads and their official URLs, acquisition times and SHA-256 identities are already retained under `data/cftc-tff/`. See the [official historical service](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm). This final round downloads no new data.

## Repository map

| Location | Purpose |
|---|---|
| `submission-final/` | Common editable scientific manuscript and supplement |
| `submission-package/ASMBI/`, `QF/`, `SHARED/` | Journal formats, separate figures and author materials |
| `protocol/`, `results/` | Frozen designs, saved outputs, failures and judgments |
| `evidence/submission/final-jof/` | Audited saved history-extension evidence, with original bytes |
| `notes/submission/` | Import, journal, provenance, review, compilation and delivery receipts |
| root Python modules and tests | Existing research implementation and software checks |
| older submission directories and revision notes | Historical versions; not current upload entrances |

Author identities, affiliations, ORCID, corresponding contact, funding, interests, CRediT, permissions and exclusive-submission approval remain author-only fields. Follow the [Chinese submission checklist](notes/submission/投稿操作清单.md); reviewer candidates have not been contacted. Old branches and PRs are preserved, with recommendations only in [CANONICAL.md](CANONICAL.md). The historical root README is preserved verbatim in [historical-readme-v13.md](notes/submission/historical-readme-v13.md).
