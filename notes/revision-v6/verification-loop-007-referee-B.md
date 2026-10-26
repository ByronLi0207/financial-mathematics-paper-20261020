# Verification loop 007 — internal financial referee B

- Review role: INTERNAL financial measurement and target-relevance referee B.
- Review began: 2026-10-23T21:09:35+00:00 (clock recorded immediately before current section extraction; read-only path/branch inventory preceded this content-review interval).
- Review ended: 2026-10-23T21:13:00+00:00.
- Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
- Observed branch: `revision-v4-jof`; observed HEAD: `fa52cc683a14695433d88015817123c0467056fc`.
- Authorized manuscript sample: exactly `submission-jof/manuscript-content.json` → `sections[2]`, all seven blocks (`blocks[0]`–`blocks[6]`). Actual heading verified: **3. Data**.
- Corresponding TeX: `submission-jof/main.tex:1–2` selects `manuscript.tex`; `submission-jof/manuscript.tex:73–87` contains the same heading and seven paragraphs. Other manuscript headings encountered while locating the boundary were not substantive review samples. Section 4, Section 10, the abstract, results, conclusions and supplement were not reread.
- Method: read existing prose, owning source/provenance/protocol metadata, and selected official source passages. No financial arrays, forecasts or models were consumed or recomputed.

## Verdict

**PASS_WITH_OPTIONAL_LANGUAGE_CLARIFICATIONS, limited to section 3.** No material contradiction between this section's financial measurement / temporal claims and the inspected owning records was found. The section preserves the distinction between a source-described client-flow sample and a verified complete dealer book, between an absolute signed aggregate and individual gross exposure, and between economic dates and historical public-information availability. It supplies a defensible description for the existing sampled-position forecasting task.

**Necessary scientific conclusion change / author pending: none identified within this sample.** No manuscript or conclusion change was made. This verdict does not resolve independent dealer validation, public-release reconstruction, causal decision value, unseen path extrema or the validity of the rest of the paper.

## Measurement and relevance checks

| Requested focus | Exact reviewed route | Assessment and boundary |
| --- | --- | --- |
| Source-described sample versus audited dealer book | JSON `sections[2].blocks[0]`; TeX line 74; W20 §3.1, physical p.4; evidence-map source entries 7 and 19 | W20 describes a sample of one market maker's client flow and five liquid pairs. Current prose attributes the description and expressly declines independent complete-book verification. It does not supply audited hedge transactions, cash movements, a raw currency reconstruction, or proof that the current accepted CSV is byte-identical to W20's input. |
| Absolute aggregate versus gross exposure | JSON block 1; TeX line 76; NYFed exact-key metadata and external-data guide | The official `PDPOSGS-B` definition is bill long positions minus short positions. The section correctly puts absolute value after signed aggregation and explicitly allows cross-dealer cancellation. It does not identify sum-of-absolute positions, individual peaks, gross exposure or pure customer order flow. No dealer-by-dealer values were read. |
| Securities accounting versus cash holdings | JSON block 1; FR 2004 register; March 2013 physical p.13 and current instructions physical p.13 / A-1 | The selected official instructions support fair-value, trade-date positions, specified settlement-date buyback treatment and reportable forward/when-issued positions. This is consistent with the section's rejection of settled cash holdings. Reading two instruction editions does not prove an invariant definition or reporting panel throughout every historical row. The current instruction compilation contains July 2024 updates while its A-1 page retains a January 2022 footer; that page's accounting text agrees with the cited historical passage. |
| Economic dates versus historical releases | JSON block 4; TeX line 82; NYFed owning-page HTML; 2004 notice; provenance and external-data guide | The live owning HTML states ordinary Thursday updates for prior-week statistics, and the dated notice establishes the lag. Current prose expressly uses a downloaded-vintage economic-date convention and disclaims live / as-released status. A current API definition or downloaded snapshot cannot recover historical first-publication observations or exact release timestamps. The earlier no-selector finding is correctly attributed to inspected routes rather than universal archive nonexistence; the API's full vintage feasibility audit was not rerun here. |
| Native units and clocks | JSON blocks 0, 1, 3 and 6; study-spec `sources`; record-clock receipt | Treasury is expressly USD millions; FX's scalar is `NetPosUsd`, with native USD confirmed in the frozen spec and W20. Horizons count subsequent records and include the issue record. Treasury's weekly economic-date clock is separate from FX's stored naive timestamps. This does not establish a verified UTC clock or equivalent elapsed durations across sources. No monetary results were pooled or recalculated. |
| Gaps and chronology | JSON blocks 0 and 3; TeX lines 74 and 80; existing record-clock receipt | The stated retained FX gaps and no-interpolation rule are coherent with the existing duration metadata: some six-record windows span 54 stored-clock hours and some 24-record windows span 72. Treasury's existing receipt gives 42 / 168 economic calendar days. These are readbacks of existing metadata, not a fresh timestamp audit; no raw FX rows were opened. |
| Peak versus endpoint | JSON block 3; TeX line 80; external-data guide target and measurement-scope memo | The response uses `H+1` observed positions including issue time, consistent with the existing sampled absolute-peak definition. W20's signed endpoint task supplies source context, not an implemented peak-score benchmark. Neither the section nor the consulted target metadata makes sampled maxima equal to transaction-time / between-record extrema. The formal methods section was outside this sample. |
| Source comparability and operational decisions | JSON blocks 0, 1, 3 and 6; study-spec source-specific windows/refits; external-data guide and measurement-scope memo | A single source-described FX sample and an aggregate market-value Treasury series have different aggregation, sampling, monetary units and histories. They support source-specific forecast exercises, not a common independently replicated dealer effect. The section does not claim that passive forecast scores identify financing amounts, liquidity usage, quoting/hedging interventions, capital or realized profit. Establishing those links would require additional measurements and a decision design; none was added. |
| Label maturity and segment boundaries | JSON blocks 2, 3 and 6; study-spec origin metadata; external-data guide boundary table; common-contract | The listed validation/evaluation origins, mature terminal labels and source-specific histories/refits agree with the owning metadata read. The current record is known only under the stipulated economic-date replay convention. This was a prose/metadata reconciliation, not numerical verification of timestamps, traces or training membership. |

## Optional language only — no edits performed

1. JSON block 0 / TeX line 74 could explicitly say **“the signed NetPosUsd scalar, in source-reported USD”**. Treasury units are explicit nearby; making FX units equally explicit would reduce reader effort without changing any value or conclusion.
2. The same paragraph could use **“positions accumulated from a sample of client flow”** when introducing W20's description. The existing complete-book disclaimer already supplies the substantive boundary; this would align the introductory wording more closely with the selected source passage.
3. If section 3 must stand alone, its clock sentence could explicitly identify stored FX timestamps as timezone-unverified. It already routes clock limits to Section 10; that cross-referenced section was not checked in this loop, so this is a local readability suggestion only.

These are optional clarifications, not authority to alter the target, source, split, model menu, reported result or scientific conclusion.

## Primary sources revisited and mature measurement practice

The comparison followed established source-first measurement practice: identify the reported financial object, aggregation and accounting basis before attaching a risk or operational interpretation; keep measurement time distinct from information availability; preserve source-native units and sampled clocks.

- [Wisniewski, Lindsay and Lindsay (2020), official PMLR PDF](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf): selected §3.1, physical pp.4–5, with the introduction's endpoint-task description as context. Supports client-flow sample / five-pair / USD wording. This was selected reading, not a fresh full-article review or model reproduction.
- [FR 2004 official register](https://www.federalreserve.gov/apps/reportingforms/Report/Index/FR_2004): report-family distinctions, reporting frequency and respondent-panel description. [March 2013 instructions](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=f555fe11-e149-479b-8088-4ed4e9ae1206), physical pp.12–13, and [current instruction compilation](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa), physical pp.12–13 / A-1: selected accounting and reportable-position passages. No full instruction-book or historical reporting-compliance audit was performed.
- [NYFed Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics): its live HTML's update paragraph was inspected after the text-browser rendering omitted that body text. [Exact series metadata](https://markets.newyorkfed.org/api/pd/list/timeseries.json): only the exact `keyid == PDPOSGS-B` entry was selected, with `seriesbreak=SBN2024`; this tag is not a row-level vintage identifier. [15 January 2004 publication-lag notice](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html): dated lag passage. No current financial-series observations were downloaded.

The search engine also returned off-topic / secondary results; none was used as evidence. Public source bytes were read into memory only for route identity and hashing, not saved into the repository.

## Exact local routes and source fingerprints

All paths below are relative to the repository. Hashes identify bytes inspected in this loop; they do not certify financial accuracy or independently reproduce the measurements.

| Local source | Reviewed route / purpose | SHA-256 |
| --- | --- | --- |
| `submission-jof/manuscript-content.json` | Only `sections[2]`, title and all seven blocks | `3a13df3d818218b095f4a6a4c548221c1ce233ed4317e7a5b1784ca24095b28d` |
| `submission-jof/manuscript.tex` | Lines 73–87, section 3; section-heading lookup only elsewhere | `875516d3f7840e80f3b07de6783c68bc9efff248afff48ec280387d17c2bfab1` |
| `submission-jof/main.tex` | Lines 1–2, main-target route | `f67dee42ce85e43ee99337e09a1550892006b57b52017f6044edcb85068e0407` |
| `protocol/revision-20261022/study-spec.json` | Source identities, units, record counts, origin bounds, windows/refits and interpretation; full metadata file read | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |
| `protocol/revision-v6/common-contract.md` | Lines 1–15, maturity / no-pooling / post-WP restrictions | `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8` |
| `data/nyfed-pdposgs-b-20261022/provenance.json` | Lines 1–41, accepted-source provenance only | `fc902b76a9f61213dd5be14c8e69fd431ba80caa7d34498b0fda883a9b8734d6` |
| `results/revision-20261022/EXTERNAL_DATA.md` | Lines 1–90, definitions / clock / target / boundary metadata | `6c38c769951a309575ff793726b53dce85fc8095ca1fc30db2ae3c24bb15dac7` |
| `results/revision-20261022/record-clock-duration-verification.json` | Lines 1–152, existing aggregate clock receipt only | `1c4fe8be4d8e8c63d793ab3aa6a3832fad15299d6f7f7fb1b5d4c352c4ac3ae4` |
| `notes/revision-20261022/financial-measurement-and-decision-scope.md` | Lines 1–52, existing target and decision-link boundaries | `d0f839f015593b2fc9074bc7531860dfb1157db3e25a4f8e4150b7adfd1779f9` |
| `notes/revision-20261022/paper-evidence-map.md` | Search-selected entries 4, 7, 10, 19 and 20, especially lines 13, 19, 25 and 43–45; some neighboring search context surfaced incidentally | `c400b8aaa2f5a0051c5b96f82efe765913d7e413bcc758b457e41d43c112a549` |
| `README.md` | Search-selected provenance lines and lines 53–103, source/acquisition/reproduction context | `0a2dcd7b1fc36c8d08f9315b382352566d7c386ca392e2c8cadde7e00a60e9ed` |
| `notes/revision-v6/input-availability.md` | Lines 1–74, previously recorded metadata-only admission scope | `765f641bd258720db1204f1fbbd7990a08b9b776f216ad95fb60caaa21cfa4f6` |
| `protocol/revision-v6/REPLAY.md` | Search-selected acquisition/privacy lines, including line 15 | `e87441c4dd1630c56d3c6e79df8faac2d1afa4260b2037e8684bce9df9a9053d` |
| `notes/revision-v6/wp7-final-source-audit.md` | Search-selected lines 26 and source-ID table entries only | `8e2e15d68630279f8fd4e62ac85eee5f129061e6056a04d0e72b1f0ef29f4370` |
| `submission-jof/references.bib` | Search-selected `fr2004`, `dataset`, `nyfeddata`, W20 metadata; neighboring matches were not source-body review | `deb7d9f3bd4f90d77bfb2fcb78a5c5bf7373ca6885ab7a59cc926929f430831e` |
| `notes/revision-20261022/root-batch-020-publication-and-thesis-measurement.md` | Search only, no matching passage returned / no substantive reliance | `9331bbffacc6a3a6e7fa8dfcbc8cb68b3d010f8c3cc8c3b10c4326e4c21900fa` |

Section-only identities: canonical JSON `sections[2]` (UTF-8, `ensure_ascii=False`, sorted keys, compact separators) SHA-256 `122a8367a52a567ab0f2fa1b2c300382a6fffbf1d90104d0928c095a3433256c`; exact UTF-8 TeX lines 73–87 with original line endings SHA-256 `88de8c2a1b215c55446bcae8675666d5a352ca0e4fe62c2c5c872b0d43c959cd`.

Accepted underlying source identities were read from metadata, **not recalculated from raw source files**: FX `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa` (1,286,391 bytes); Treasury `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb` (23,315 bytes).

| Revisited public route | Bytes observed in memory | SHA-256 |
| --- | ---: | --- |
| NYFed owning-page HTML | 103117 | `fa9b7de732701b3e606dcce5c817d7beb161f8f7b828cd75abef7bf3e16a1d73` |
| NYFed series-definitions JSON | 335616 | `77a7805ffdf634d259bdc94c8eb4ff9f44acb7c5ea7c1246f05152a971d4c7c0` |
| FR 2004 current instruction compilation | 353043 | `3184245a8da570b14d34cbe6a2bf4fafb76acfc487c70c7642e8e4c3da755aeb` |
| FR 2004 March 2013 instructions | 139774 | `7fc2d9f7f4f0cd5ffad94fc328acd6a2115f96fed16b9b0fd559344e0ff05ac3` |
| W20 official PDF | 2431326 | `b42f3abca77f5913499e59e2efdfc62b2b57e07faaca03fdc3fdd5d59a6d0bf2` |
| NYFed dated 2004 lag-notice HTML | 104553 | `8722e4a2924420992febd8e732eabb30f9a825d4e9671ea128b6798adec21e37` |

Public HTML hashes are identities of the responses observed here; dynamic website markup need not have permanent byte identity. The official register and PMLR landing page were read through the web tool without a separate byte-hash receipt.

## Scope and action receipt

No raw FX CSV, raw Treasury CSV, private NPZ, per-origin array or per-origin prediction was opened. No analysis, scoring, model fitting, tests, numerical validation, new experiment, data repair, compilation or rendered-paper audit was run. No manuscript, financial conclusion, protocol, state file, commit, push or publication was changed. No Claude/Cloud or other cross-model review was invoked. The only repository write by this reviewer is this new note, created without overwriting an existing file.

This is a narrow internal section sample. It is not external review, independent replication, a full-paper review, proof of data completeness or a substitute for an author's scientific decision.
