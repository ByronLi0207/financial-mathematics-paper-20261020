# V5 author–date citation routing preflight for V6

Read-only review on 23 October 2026. Scope: the V5 manuscript and supplement JSON, visible author–date citations, and their own reference lists. No manuscript, bibliography, prior reference audit, financial file, model, or result was changed. No web or UI retrieval was performed. Bibliographic metadata dispositions below come from the existing V4/V5 notes; this is not a fresh verification of external sources or a new substantive reading of the cited works.

The current `submission-jof` JSON files were byte-identical to the V5 snapshots when checked. The snapshots provide stable locators while the V6 authoring work proceeds. JSON pointers below are zero-based and refer to those snapshots. A table-cell citation counts as a citation; a name in `_bindings`, `_source`, reference entries, or another metadata field does not.

## Outcome

- Main manuscript: 36 distinct listed IDs; 35 have an actual visible author–date/data-source citation. The sole truly uncited entry is **`sussman2023`**.
- Supplement: 17 distinct listed IDs; all 17 have an actual visible author–date citation.
- The union has 40 distinct IDs. The 13 IDs common to the two lists have exactly identical reference HTML. Neither list contains a duplicate ID.
- No existing explicit author–date citation in either visible document lacks a corresponding entry in that document's own list.
- No further uncited-entry deletion is supported. In particular, **Giacomini and White (2006) is already cited**, not merely listed.

This result concerns the captured V5 documents. The planned V6 Gibbs/SAV/GW additions need the ordinary final readback after their concrete text has been generated; this note does not claim to audit text that has not yet been written.

## Required fix already assigned to the main author

**Sussman (2023): listed, presently uncited.** Main reference `/references/29`, ID `sussman2023`; the classical inequality attribution is at `/sections/3/blocks/25/html` in Section 4, Proposition 2, and the proof invocation at `/sections/3/blocks/27/html`. Neither contains Sussman's name or a year. Searching visible body/table/caption text for `Sussman` found no occurrence in either V5 document.

Recommended exact local wording at the end of the Proposition 2 assumptions paragraph, replacing its last sentence:

> This is a direct scalar application of the classical Lévy maximal inequality (see Sussman, 2023, Proposition 3.4), not a new inequality.

This routes the already listed, already audited source to the existing classical attribution. Parent has explicitly scheduled this fix. Supplement S11 begins as a proof of Proposition 2 and need not acquire a redundant reference solely to cure the main-list orphan. If the supplement is intended to give a standalone external attribution, a Sussman citation and a copied entry could additionally be placed in S11; that is an optional standalone-reading choice, not an existing unmatched citation.

## Additional local routing improvement

**QRF in Supplement S13: attribution is only in the main article.** At supplement `/sections/12/blocks/12/html`, the paragraph describes the leaf-distribution quantile and ends by declining to transfer “the original consistency theorem” to dependent fixed-window data. It does not name the original source; `meinshausen2006` is absent from the supplement's 17-entry list. The main article already contains and cites the correct entry at `/sections/1/blocks/3/html` and `/sections/7/blocks/3/html`.

This is **not** an unmatched existing author–date citation. It is a concrete opportunity to route an existing methodological claim for a reader consulting the supplement independently. Recommended minimal fix:

1. Change the beginning of S13's QRF paragraph to: “Following the leaf-distribution quantile construction of Meinshausen (2006), the forest uses the same 33 causal predictors, training-only transforms and response scaling as QR.” Retain all subsequent implementation and theorem-scope qualifications.
2. Copy the existing main `meinshausen2006` reference entry into the supplement, unchanged. No new metadata lookup is needed.

The main entry is: Meinshausen, N. (2006). Quantile Regression Forests. *Journal of Machine Learning Research* 7, 983–999; the existing link is the official JMLR article.

Other supplement shorthand such as `HLN`, `Holm`, `DM`, and the unnamed out-of-sample CAViaR theorem in S9 is intelligible through the main methods/inference section. It is not evidence of author–date citations missing from the supplement bibliography. If expanded into author–date citations during V6 editing, add the corresponding main entries at that time rather than leaving new dangling citations.

## Planned V6 routes and existing routes that must be retained

- Parent is adding Gibbs and Candès (2021), with the already verified official NeurIPS bibliographic identity, and explicit Gibbs/Engle/GW citations in new S16. This note did not independently browse or re-verify that new source.
- `engle2004` already exists and is cited in both V5 lists. Main: `/sections/1/blocks/0/rows/4/0`, `/sections/1/blocks/3/html`, `/sections/4/blocks/10/html`. Supplement: `/sections/14/blocks/20/html`. S16 can reuse its existing supplement entry.
- `gw2006` already exists in the main list and is actually cited in `/sections/4/blocks/8/html`: “Fixed finite estimation windows motivate the unconditional predictive-ability interpretation of Giacomini and White (2006) ...”. It is absent from the V5 supplement list, so the new S16 author–date citation should be accompanied by a copied supplement entry.
- Main corporate citation “Board of Governors, March 2013 and July 2024 instructions” in `/sections/2/blocks/1/html` resolves to `fr2004`. Here FR 2004 is the reporting-form identifier, not a conflicting publication year. Separate 2013/2024 bibliography entries are not needed merely to make a numeric-year matcher pass.
- Main data-source paragraph `/sections/2/blocks/5/html` explicitly cites Lindsay (2020) and Federal Reserve Bank of New York (2026), backed by `dataset` and `nyfeddata`. These entries are not uncited.

## Citation inventory and concrete routes

The inventory gives one actual route per listed ID. Main pointers are relative to `/sections`; S pointers are relative to the supplement's `/sections`. When an author appears under more than one year, the actual author–date phrase was checked; a surname-only occurrence was not used to credit the wrong year.

| Listed ID | Main actual route | Supplement actual route |
|---|---|---|
| arjani2020 | `1/blocks/2/html` | `14/blocks/19/html` |
| avellaneda2008 | `9/blocks/4/html` | — |
| barone1999 | `1/blocks/3/html` | `6/blocks/11/html` |
| biau2011 | `1/blocks/3/html` | — |
| fr2004 | `2/blocks/1/html` (versioned corporate attribution) | — |
| boudoukh2004 | `1/blocks/2/html` | `14/blocks/17/html` |
| boyd2011 | — | `3/blocks/3/html` |
| casgrain2023 | — | `4/blocks/7/html` |
| christ1998 | `4/blocks/10/html` | `8/blocks/1/html` |
| dataset | `2/blocks/5/html` | — |
| dm1995 | `4/blocks/8/html` | — |
| duffie2023 | `0/blocks/0/html` | `14/blocks/22/html` |
| ehm2016 | `6/blocks/2/html` | `14/blocks/21/html` |
| engle2004 | `1/blocks/3/html` | `14/blocks/20/html` |
| nyfeddata | `2/blocks/5/html` | — |
| gw2006 | `4/blocks/8/html` | — |
| gneiting2011 | `1/blocks/3/html` | `5/blocks/3/html` |
| gneiting2007 | `6/blocks/2/html` | — |
| hansch1998 | `0/blocks/0/html` | — |
| hln1997 | `4/blocks/8/html` | — |
| henzi2022 | — | `4/blocks/7/html` |
| ho1981 | `0/blocks/0/html` | — |
| holm1979 | `4/blocks/10/html` | — |
| hull1998 | `1/blocks/3/html` | `6/blocks/11/html` |
| koenker1978 | `1/blocks/3/html` | — |
| kupiec1995 | `4/blocks/10/html` | — |
| liao2005 | `1/blocks/2/html` | — |
| lyons1995 | `0/blocks/0/html` | — |
| mcneilfrey2000 | `7/blocks/3/html` | `12/blocks/10/html` |
| meinshausen2006 | `1/blocks/3/html` | — (proposed S13 attribution above) |
| nw1987 | `4/blocks/8/html` | — |
| petrunia2019 | `1/blocks/2/html` | `14/blocks/18/html` |
| politis1994 | — | `2/blocks/5/html` |
| sussman2023 | **uncited** | — |
| sozen2026 | `1/blocks/3/html` | — |
| hoogen2017 | `1/blocks/2/html` | — |
| wisniewski2020 | `1/blocks/1/html` | `14/blocks/16/html` |
| wisniewski2024 | `1/blocks/1/html` | `14/blocks/16/html` |
| xu2023 | `1/blocks/3/html` | — |
| zhou2024 | `1/blocks/3/html` | — |

## Metadata notes used and their limits

Existing `notes/revision-v4-jof/reference-audit.{json,md}` audited all 40 original identities, explicitly retaining incomplete/unverified metadata rather than certifying every field. Existing `notes/revision-v5-novelty/reference-amendments.{json,md}` covered the nine positioning sources and supplied the later MaxVaR final-layout pagination resolution.

Their relevant existing distinctions are correctly retained in the captured V5 references:

- MaxVaR uses the subsequently authenticated author-hosted final-layout `2(3), 1–6`, rather than silently treating the V4 unresolved pages as settled at the earlier audit.
- Ehm remains the formal 2016 journal identity; the supplement S15 explicitly labels its substantive page locators as the 2015 author-v2 revision. That version date is not a separate dangling in-text citation.
- Wisniewski (2024) is the institutional thesis identity even though prior evidence separately records a 2023 cover; this is not evidence of a missing “Wisniewski (2023)” entry.
- The prior van den Hoogen body-access limitation is not cured by this routing check. No current full-text-reading credit is added here.

The 2004 New York Fed announcement mentioned in main Section 3 `/sections/2/blocks/4/html` is a historical-source claim, not an author–date citation. This preflight does not re-verify that announcement or infer a new publication entry from its year. The existing general New York Fed data/definitions route should not be described as fresh verification of that announcement.

## Input fingerprints and literal inventory output

Observed input SHA-256 values:

```text
submission-jof/manuscript-content.json 2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7
submission-jof/supplement-content.json 6cef270b0958f6895ab091589289e9aed17fca46c1cdc30d5c0118d5fe206e8a
notes/revision-v6/v5-manuscript-before.json 2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7
notes/revision-v6/v5-supplement-before.json 6cef270b0958f6895ab091589289e9aed17fca46c1cdc30d5c0118d5fe206e8a
notes/revision-v4-jof/reference-audit.json 51c5ef6583df60e197ed0e5b9185a99c94353b8cf27673543f3c68b4a7b3437a
notes/revision-v5-novelty/reference-amendments.json 0cae6fb99b4cec46037fff53557bed7d6cda082ec8ca484c7f7a208396d41db2
```

The executed inventory loaded only these public document/metadata JSONs, recursively inspected visible fields while excluding underscored provenance and the reference list, printed strings with four-digit years for manual author–date adjudication, and separately compared reference IDs/HTML. Literal reference-list summary output:

```text
submission-jof/manuscript-content.json 2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7 references 36 sections 12
submission-jof/supplement-content.json 6cef270b0958f6895ab091589289e9aed17fca46c1cdc30d5c0118d5fe206e8a references 17 sections 15
notes/revision-v6/v5-manuscript-before.json 2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7 references 36 sections 12
notes/revision-v6/v5-supplement-before.json 6cef270b0958f6895ab091589289e9aed17fca46c1cdc30d5c0118d5fe206e8a references 17 sections 15
COMMON_DIFFERENT []
DUPLICATEIDS False False
UNION 40
```

No automated surname hit was treated as sufficient by itself: for example, `Ho` occurs inside ordinary words, `Gneiting` has two listed years, and `Lindsay` is both the dataset author and a coauthor of the endpoint paper. The final inventory above uses the concrete visible author–date/data-source phrases instead.
