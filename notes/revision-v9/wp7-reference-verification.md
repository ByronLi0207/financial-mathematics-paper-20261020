# WP7 reference metadata and citation/cross-reference verification

## Scope and result

**PASS for the four requested bibliographic records and the static citation/cross-reference checks on the inspected source bytes.** The metadata comparison found **0 paper metadata mismatches**. Two differences between external primary records themselves are explicitly recorded below as **MISMATCH** and resolved by the publisher's record; neither calls for changing the current bibliography. Source SHA-256 values and actual UTC timestamps are in `wp7-reference-check.json` and `wp7-crossref-check.json`.

This is metadata/abstract verification, not a new full-paper reading claim. It runs no forecasting code, statistical analysis, model, pytest suite or TeX compiler. Compiler diagnostics and rendered-PDF checks remain separate owning gates. Only four bibliographic records are checked against external primary sources here; the static citation census is broader and must not be described as external metadata revalidation of every reference.

## Verified records and actual reading scope

| Key | Bibliographic record retained in both current source surfaces | Primary source and actual access scope |
|---|---|---|
| `merton1976` | Robert C. Merton (1976), “Option pricing when underlying stock returns are discontinuous,” *Journal of Financial Economics* **3**(1–2), 125–144. DOI **10.1016/0304-405X(76)90022-2**. Publisher issue date: January–March 1976. | [Owning publisher article record](https://www.sciencedirect.com/science/article/pii/0304405X76900222). Read its publisher-indexed metadata and abstract/article preview through the web tool. Direct DOI/publisher opens returned 403. No original body read in this check. |
| `turner1989` | Christopher M. Turner, Richard Startz and Charles R. Nelson (1989), “A Markov model of heteroskedasticity, risk, and learning in the stock market,” *Journal of Financial Economics* **25**(1), 3–22. DOI **10.1016/0304-405X(89)90094-9**. Publisher issue date: November 1989. | [Publisher article record](https://www.sciencedirect.com/science/article/pii/0304405X89900949), [publisher's Startz author listing](https://www.sciencedirect.com/author/6602724008/richard-startz), and [Nelson's university-hosted CV](https://faculty.washington.edu/cnelson/CV.htm). Read publisher-indexed metadata/abstract and the corresponding author-CV entry. Direct publisher opens returned 403; no original article body read. |
| `viering2023` | Tom Viering and Marco Loog (2023), “The Shape of Learning Curves: A Review,” *IEEE Transactions on Pattern Analysis and Machine Intelligence* **45**(6), 7799–7819. DOI **10.1109/TPAMI.2022.3220744**. June 2023 issue; online publication 9 November 2022. | [IEEE article record](https://ieeexplore.ieee.org/document/9944190/), [author institutional publication record](https://research.tudelft.nl/en/publications/the-shape-of-learning-curves-a-review/), and [version-specific arXiv record](https://arxiv.org/abs/2103.10948v2). Read metadata, abstract, and arXiv submission history. The direct IEEE open showed robot verification. No full original-body reading in this check. |
| `bollerslev1986` | Tim Bollerslev (1986), “Generalized autoregressive conditional heteroskedasticity,” *Journal of Econometrics* **31**(3), 307–327. DOI **10.1016/0304-4076(86)90063-1**. Publisher issue date: April 1986. | [Publisher article record](https://www.sciencedirect.com/science/article/pii/0304407686900631), [author's Duke institutional record](https://scholars.duke.edu/publication/651658), and [author's research list](https://public.econ.duke.edu/~boller/research.html). Read publisher-indexed metadata/abstract, direct institutional metadata/abstract, and the 1986 author-list entry. Direct publisher open returned 403; no original article body read. |

The current manuscript's explicit `thebibliography` entries occur at lines 408, 458, 460 and 462. The corresponding `references.bib` entries begin at lines 297, 309, 320 and 331. Both surfaces match the verified author/title/year/journal/volume/issue/pages/DOI fields, allowing ordinary title capitalization and author-initial formatting differences.

### Version and primary-record discrepancies

- **MISMATCH — Turner pagination in one author record:** Nelson's university-hosted CV gives 3–25, while the owning publisher's issue record gives 3–22. The current manuscript and BibTeX already use the publisher's **3–22**. The discrepancy is retained in the JSON receipt; no manuscript change is warranted.
- **MISMATCH — Bollerslev repository date:** Duke's institutional publication record shows “January 1, 1986”; the publisher identifies the issue as **April 1986**. The paper currently gives only the correct year **1986**. Do not promote the repository's generic date to a verified issue-publication day.
- **Different version events, no contradiction — Viering/Loog:** arXiv `2103.10948v2` was revised **2022-11-05** (v1 submitted 2021-03-19), the journal article was published online in November 2022, and its journal issue is 2023. `references.bib` correctly retains journal year 2023 plus the separately labelled v2 preprint note. This check does not claim the preprint and published PDF are byte-identical or that all body changes between them were reviewed.

## Citation-use check

The learning-curve citation in main §2 is used for diversity and possible nonmonotonicity in learning curves; its abstract supports that background. The same paragraph explicitly distinguishes the manuscript's fixed-period relative-loss comparison from an independent-sample expected-risk curve.

Main §7 cites Bollerslev for the inherited conditional-variance model family, and cites Turner et al. and Merton for financial precedents for switching and jumps. The text also calls its own experiments discrete mean-reverting level processes with independently specified equations. The sources are not presented as an exact calibration of those processes, proof of the study's results, or empirical confirmation of the rejected narrow-regime account. The metadata/abstract scope supports this limited attribution; it does not independently audit those sources' complete assumptions, proofs or numerical applications.

## Static citation and cross-reference check

Executed command:

```sh
python3 -B notes/revision-v9/wp7-crossref-check.py --output notes/revision-v9/wp7-crossref-check.json > notes/revision-v9/wp7-crossref-console.txt 2>&1
```

Full actual stdout: `notes/revision-v9/wp7-crossref-console.txt`. The result is `PASS`, with `error_count: 0`:

| Entry document | Labels | Reference commands | Citation occurrences | Undefined / duplicate-within-document / missing-file findings |
|---|---:|---:|---:|---:|
| `submission-jof/manuscript.tex` | 23 | 23 | 35 | 0 |
| `submission-jof/supplement.tex`, including recursive generated inputs | 43 | 1 | 0 | 0 |
| `submission-jof/extended-v9-technical.tex` | 3 | 0 | 0 | 0 |

The companion BibTeX contains 32 distinct keys. Every explicit main `bibitem` has a corresponding BibTeX key, and every main citation resolves against its active explicit bibliography. The `.bib` file is a consistency surface rather than the compiler's active bibliography source in the current manuscript.

The three labels `sup:frontier-0`, `sup:frontier-8`, and `sup:implementation` occur once in each of two **separate standalone documents**. In the compact Supplement they label retained relocation/index sections; in the technical appendix they label the full sections. The compact text explicitly links the technical PDF and extended-results index. There is no `externaldocument` directive and no unresolved cross-document `ref` reliance. Reusing those names across standalone PDFs is intentional and is not a duplicate label inside one compilation unit. All actual `ref` commands must resolve locally, which this check verifies.

The checker recursively visits `input`/`include`, verifies referenced graphics exist, inventories hashes, removes ordinary TeX comments, and checks the supported standard citation/reference commands. It is a static source check, not a substitute for the separately required actual compilation and rendered hyperlink/number inspection.

## Metadata comparison command and raw output

Executed command:

```sh
python3 -B notes/revision-v9/wp7-reference-check.py > notes/revision-v9/wp7-reference-console.txt 2>&1
```

Full actual stdout: `notes/revision-v9/wp7-reference-console.txt`. Actual result: `PASS`, `paper_metadata_mismatch_count: 0`, all four requested keys `PASS`, each with `reading_scope: metadata_and_abstract_only`. The two external-record discrepancies remain explicitly marked `MISMATCH` in that output and in the JSON receipt.

No manuscript, Supplement, technical source, bibliography, frozen scientific archive, protected reference or other working directory was modified by this verification.


Final source follow-through: the subsequent author-year entry ordering leaves all32 complete bibliography entry contents byte-identical. Initial line positions above refer to the pre-order snapshot; current source hashes are revalidated by `wp7-reference-final.json` and all citation/label keys by `wp7-crossref-final.json`. No new original-body reading is implied.
