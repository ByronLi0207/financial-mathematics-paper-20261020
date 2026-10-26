# Verification loop 010 — three original-source reference metadata checks

- Selection: `notes/revision-v6/verification-loop-010-references-selection.json` (round 10, seed 2026102310).
- Selection timestamp, as recorded by the parent process: 2026-10-23T21:15:28.954061+00:00.
- This metadata verification started: 2026-10-23 21:15:44 UTC.
- Source checks ended: 2026-10-23 21:16:33 UTC.
- Scope: exactly `zhou2024`, `nw1987`, and `casgrain2023`; author names/order, titles, cited year, frozen arXiv version/date where applicable, and journal volume/issue/pages/stable identifier where applicable. Subsequent publication metadata is recorded only to distinguish it from the frozen arXiv citations.
- Evidence sources used: the selected arXiv records, official PMLR publisher record, JSTOR's official issue record, and an IMS publisher-hosted search result for the Casgrain journal publication. No substantive literature synthesis, new methods, analyses, models, tests, manuscript changes, commits, or workflow-state changes were performed. No third-party PDF files were saved. No Claude/Cloud or different-model review was invoked.

## Result

All three selected entries match their cited source/version metadata. No bibliography mismatch was found within this scope. The selected arXiv dates are revision dates for the expressly cited `v2` records, rather than first-submission dates or dates of later formal publication. The conclusion does not establish that these are the latest publication forms or that their substantive claims support the manuscript.

## `zhou2024`

Selected citation: Zhou, Y., L. Lindemann and M. Sesia (2024), *Conformalized Adaptive Forecasting of Heterogeneous Trajectories*, arXiv:2402.09623v2, 15 May 2024.

The [original frozen arXiv v2 record](https://arxiv.org/abs/2402.09623v2) lists Yanfei Zhou, Lars Lindemann and Matteo Sesia in that order, with the same title. Its submission history identifies v1 as 14 February 2024 and v2 as **15 May 2024, 04:38:46 UTC**. The selected author initials, title, year, version and date therefore match. The [unversioned arXiv record](https://arxiv.org/abs/2402.09623) also showed v2 as its most recent revision during this check.

For publication-form distinction only, the [official PMLR record](https://proceedings.mlr.press/v235/zhou24l.html) lists the same authors/title in *Proceedings of the 41st International Conference on Machine Learning*, PMLR **235:62002–62056 (2024)**, with its BibTeX month field identifying **21–27 July**. This is a conference proceedings publication. Its July proceedings metadata does not invalidate the selected May arXiv v2 revision date. No automatic citation replacement was made.

Access: the arXiv and PMLR metadata pages were readable. No PDF was required or saved.

## `nw1987`

Selected citation: Newey, W.K. and K.D. West (1987), *A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix*, *Econometrica* 55(3), 703–708, JSTOR 1913610.

The [official JSTOR issue record](https://www.jstor.org/stable/i332769) identifies *Econometrica*, **Vol. 55, No. 3, May 1987**, published by The Econometric Society. Its entry for the selected paper supplies the exact title, **Whitney K. Newey and Kenneth D. West**, pages **703–708**, the [stable item 1913610](https://www.jstor.org/stable/1913610), and DOI **[10.2307/1913610](https://doi.org/10.2307/1913610)**. The selected initials, title, year, journal, volume, issue, page range and stable identifier match.

Access limitation: the individual JSTOR item page returned its page title but only a Google Tag Manager link as extracted content. Verification instead used JSTOR's readable, publisher-attributed issue table of contents, which directly connects the paper metadata to stable item 1913610. A search restricted to the Econometric Society domain reported a robots.txt block; unrelated papers' reference lists were not used as evidence. The journal article's full text was not checked, and no PDF was saved.

## `casgrain2023`

Selected citation: Casgrain, P., M. Larsson and J. Ziegel (2023), *Anytime-valid sequential testing for elicitable functionals via supermartingales*, arXiv:2204.05680v2, 4 June.

The [original frozen arXiv v2 record](https://arxiv.org/abs/2204.05680v2) lists Philippe Casgrain, Martin Larsson and Johanna Ziegel in that order, with the same title. Its submission history identifies v1 as 12 April 2022 and v2 as **4 June 2023, 19:28:30 UTC**. The selected author initials, title, cited revision year, version and date therefore match. The [unversioned arXiv record](https://arxiv.org/abs/2204.05680) also showed v2 as its most recent revision during this check.

For publication-form distinction only, an indexed result from the [IMS publisher-hosted issue PDF](https://www.imstat.org/publications/bej/bej_30_2/bej_30_2.pdf) reported *Sequential testing for elicitable functionals via supermartingales*, **Bernoulli 30(2), 2024, 1347–1374**, DOI **[10.3150/23-BEJ1634](https://doi.org/10.3150/23-BEJ1634)**. This journal title omits the initial “Anytime-valid” in the frozen arXiv title. The 2024 journal publication year is a different publication form from the selected 2023 arXiv v2 revision; the selected entry does not claim to be a Bernoulli citation.

Access limitation: arXiv metadata was fully readable. The DOI resolved to the [official Project Euclid article location](https://projecteuclid.org/journals/bernoulli/volume-30/issue-2/Sequential-testing-for-elicitable-functionals-via-supermartingales/10.3150/23-BEJ1634.full), but its response was an access-protection shell, without readable article metadata. The direct IMS PDF open failed with HTTP 502. Consequently the journal-form metadata above is explicitly limited to the indexed original publisher result, rather than a claim that the full publisher article/PDF was successfully inspected. The selected arXiv v2 metadata conclusion does not depend on that journal-form corroboration. No PDF was saved.

## Scope boundary

This record is a three-entry bibliography metadata audit. It neither upgrades the manuscript's research validation status nor assesses theoretical applicability, empirical correctness, novelty, or readiness for submission. No other bibliography entries were selected or assessed in this round, and this record makes no exhaustive claim about the latest publication status.
