# Verification loop 14 — three randomly selected reference metadata checks

Checked at 2026-10-23T21:40:01.340064+00:00. This is source-metadata verification only, not full-paper reading, a new financial analysis, or independent replication. Selection was frozen before the relevant source lookups in `verification-loop-014-references-selection.json`, seed 2026102314, excluding previously checked IDs. No manuscript, result, inference, source code or conclusion was changed.

Current main JSON SHA-256: `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2`.
Current main TeX SHA-256: `6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72`.

| Reference | Primary source actually inspected | Metadata assessment and reading limit |
| --- | --- | --- |
| holm1979 | [JSTOR volume 6 issue 2 table of contents](https://www.jstor.org/stable/i412579), volume/issue heading and Holm entry; article page itself exposes no usable body through the text reader | Sture Holm, 1979, *Scandinavian Journal of Statistics* 6(2), pp.65–70, and title agree. The official issue links the exact stable article 4615733. Metadata PASS; no new reading of its proof. |
| nyfeddata | [NYFed official statistics page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics), update paragraph; [official time-series metadata API](https://markets.newyorkfed.org/api/pd/list/timeseries.json), exact `keyid == PDPOSGS-B` object only | The key identifies dealer Treasury-bill long positions less short positions, excluding TIPS. The metadata object's seriesbreak is SBN2024. The statistics page describes a Thursday afternoon release of the prior week's data. These support source identity and publication lag; they do not prove that a downloaded economic-date row was public at that economic date. The manuscript's 22 October snapshot date is an archived local acquisition fact, not a live metadata field. No current observations downloaded. |
| hoogen2017 | [Indexed official TU Delft PDF title page](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1); current direct resolver and PDF requests timed out | The official indexed cover identifies Sofie van den Hoogen, August 2017, and the title *Intraday liquidity risk estimation using transaction data: an extreme value theory approach*. These agree with the current bibliography. Direct institutional-record UUID resolution and body reading were **not** completed in this round. Metadata match is limited to that indexed official cover, not a successful live full-record/full-text check. |

## Actual access outcomes

- JSTOR direct stable article returned only a tag-manager link in the text rendering. Its issue table of contents was successfully opened and read, including the year, volume, issue, author and page interval. Third-party search results were excluded from the verdict.
- NYFed HTML body was successfully read. A bounded Python urllib metadata-only request returned application/json, 335616 bytes; only the object with exact key PDPOSGS-B was inspected. No financial time-series CSV or new observations were retrieved. The official metadata API's exact series description is paraphrased above rather than reproduced in bulk.
- Delft resolver request: `URLError <urlopen error timed out>`. Text-reader requests to the resolver and official PDF also timed out. The direct official file's indexed title-page text was available through a domain-restricted search and contained the matching author/month/year/title. The unverified live UUID-to-file mapping remains an access limit, not a fabricated success.
- An initial navigation batch opened three other existing references before the random selection's exact URLs were followed; those responses were not used as evidence for the selected three. No new analysis or citation was added from that incidental navigation.

## Disposition

No conflicting metadata was found. Two entries have direct official page/API confirmation; the thesis check is explicitly narrower because direct access failed. Existing bibliography is retained. Access failure does not justify changing a correct citation, bypassing authentication, installing software, or claiming a new scientific reading. The snapshot-vs-release distinction remains explicit in the manuscript.
