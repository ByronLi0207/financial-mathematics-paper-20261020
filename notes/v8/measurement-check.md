# B5 measurement clarification

The existing v7 specification already calls the Treasury input an aggregate market-value replay (`protocol/revision-20261022/study-spec.json`, source interpretation). For the finance referee's wording question, the official FR2004 instructions were reopened on2026-10-24 during B5; no financial observations or new sample were obtained.

Source: [Federal Reserve FR2004 Reporting Guidelines, Section III.A, printed page13](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=f555fe11-e149-479b-8088-4ed4e9ae1206).

The accounting section specifies fair-value measurement and issue-level netting; reporting columns distinguish long and short positions. The accepted NYFed source identifies the public Treasury-bill input as long minus short, in USD millions. Section4 now makes its fair-value aggregate character explicit. This is a measurement definition, not an attribution of movements to trades, valuation or dealer actions.

Existing source identity: `data/nyfed-pdposgs-b-20261022/provenance.json`. The raw CSV, calculations and reported estimates remain unchanged. Valuation/gross-exposure decomposition is a future-data task in AUTHOR-TODO T4.
