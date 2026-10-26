# Verification loop 006: exactly three reference metadata checks

- Round: 6.
- Selection input: `notes/revision-v6/verification-loop-006-references-selection.json`.
- Selection seed recorded by the input: `2026102306`. The existing selection was used without resampling: `arjani2020`, `politis1994`, `gw2006`.
- Metadata check started: **2026-10-23 21:06:56 UTC** (2026-10-23 14:06:56 America/Vancouver).
- Source comparison ended: **2026-10-23 21:07:50 UTC** (2026-10-23 14:07:50 America/Vancouver).
- Scope: title, author list/order, year, publication/journal, volume, issue, pages and DOI **where those fields are present in the selected reference**. The three selected entries were the only references assessed. Official report/publisher front matter and metadata were used; search results for unrelated works were not assessed or used.
- Method: compare the selected citation with the issuing institution's report or the publisher's own metadata, distinguish journal issue year from later online posting dates, and record access limits rather than infer full-text access.

## Results

| Selected ID | Metadata result | Access/evidence boundary | Citation changes made |
| --- | --- | --- | --- |
| `arjani2020` | All fields actually supplied by the selected reference agree with official institutional evidence. | Official report title-page text confirms title and all three authors; the issuer's separate official page identifies the linked discussion paper as 2020. No full-paper reading is claimed. | None |
| `politis1994` | All supplied fields agree with the publisher's metadata returned through the web search index. | Direct Taylor & Francis page retrieval failed. This is **partial access: publisher metadata via search index**, not direct full-text or PDF verification. | None |
| `gw2006` | All supplied fields agree with the directly accessible Wiley article metadata. | Bibliographic/front-matter verification only; no full-text reading is claimed. | None |

No bibliographic mismatch was found in the fields checked. This does not validate how these works are interpreted or used in the manuscript.

## `arjani2020`

Official sources:

1. [Payments Canada official report](https://www.payments.ca/sites/default/files/discussion_paper_monitoring_intraday_liquidity_risks_in_a_real_time_gross_settlement_system.pdf), title-page text (PDF page index 1; the browser text extraction begins there).
2. [Payments Canada's response to OSFI's consultation](https://www.payments.ca/support-risk-mitigation-payments-canadas-response-osfis-consultation), dated 10 September 2024, footnote 9. This official institutional page explicitly labels the linked discussion paper with **(2020)**. It is used only to corroborate the same report's year and publication type.

| Field | Official value / evidence | Comparison |
| --- | --- | --- |
| Title | Monitoring Intraday Liquidity Risks in a Real Time Gross Settlement System | Matches |
| Authors, in order | Neville Arjani; Fuchun Li; Leonard Sabetti | Matches `N.`, `F.` and `L.` in the selected entry |
| Year | 2020, explicitly identified in the issuer's footnote 9 | Matches |
| Publication type / issuer | Payments Canada discussion paper, identified by the issuer's official page and the report's title-page acknowledgments | Matches |
| Journal, volume, issue, bibliographic page range, DOI | Not supplied in this selected report citation; not required to establish a match | Not assessed as missing or incorrect; no assertion that no DOI exists |

The online PDF was opened through the web reading tool; no third-party PDF was downloaded into the workspace or republished. Tool extraction made body text available, but only the report's metadata/front matter was used for this check. Screenshot requests for PDF page index 0 returned a source reference without viewable image pixels in the tool response; no visual inspection of that cover page is credited.

## `politis1994`

Official support:

- [Taylor & Francis / JASA article metadata](https://www.tandfonline.com/doi/abs/10.1080/01621459.1994.10476870).
- [DOI resolver](https://doi.org/10.1080/01621459.1994.10476870).

The publisher page's metadata was returned by official-domain web searches, including a search for the exact DOI, authors, volume and issue. Direct page retrieval failed, so this evidence is explicitly a publisher-page search-index representation.

| Field | Publisher metadata returned by the index | Comparison |
| --- | --- | --- |
| Title | The Stationary Bootstrap | Matches |
| Authors, in order | Dimitris N. Politis; Joseph P. Romano | Matches `D.N.` and `J.P.` |
| Issue year | 1994 | Matches |
| Journal | Journal of the American Statistical Association | Matches |
| Volume / issue | 89 / 428 | Matches |
| Pages | 1303-1313 | Matches |
| DOI | `10.1080/01621459.1994.10476870` | Matches |

The publisher metadata also gives an online publication date of 27 February 2012. This is distinct from the journal's 1994 issue year and is not evidence that the selected reference's year should change. No full text or article PDF was accessed or downloaded.

## `gw2006`

Official support: [Wiley / Econometrica article metadata](https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0262.2006.00718.x), including its author block, volume/issue and pages, first-publication date, DOI, and publisher-supplied citation.

| Field | Official publisher metadata | Comparison |
| --- | --- | --- |
| Title | Tests of Conditional Predictive Ability | Matches |
| Authors, in order | Raffaella Giacomini; Halbert White | Matches `R.` and `H.` |
| Year | 2006; first published 1 November 2006 | Matches |
| Journal | Econometrica | Matches |
| Volume / issue | 74 / 6 | Matches |
| Pages | 1545-1578 | Matches |
| DOI | `10.1111/j.1468-0262.2006.00718.x` | Matches |

The directly accessible page includes abstract and reference-list material, but neither abstract availability nor reference-list availability was treated as proof of reading the article's full text. No article PDF was downloaded.

## Access failures and limitations

- The direct Taylor & Francis abstract-page request returned **403 Forbidden**. The DOI request returned a tool error describing a redirect to the inaccessible publisher full-page route; a direct request to that full-page route was also inaccessible. Verification therefore remained at publisher metadata exposed by the search index.
- An attempted Payments Canada landing-page route was inaccessible. A generic official-site search result had an indexed snippet about the report, but opening that generic search page produced different current results; that snippet was not used as the decisive year evidence. The directly accessible issuer page's footnote 9 supplied the explicit 2020 corroboration instead.
- The report cover-page screenshot requests did not produce viewable pixels in the tool response. Title/author checking used the report's extracted title-page text; no successful cover-image inspection is claimed.
- The report citation supplies no journal/volume/issue/page-range/DOI fields. This round did not invent those fields, substitute the PDF file's page count for a bibliographic range, or conclude that a DOI does not exist.
- This round did not assess claims, methods, results, or manuscript citation context. It did not add literature, run analyses, create a model or experiment, run tests, change the manuscript/conclusion, or invoke Claude or another model for review.
- Only this new note was written by this metadata-check subtask. No state file, selection file, commit, external publication, or third-party PDF copy was created or modified.
