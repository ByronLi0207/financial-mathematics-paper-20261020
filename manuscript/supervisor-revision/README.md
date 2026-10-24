# Second supervisor revision: source and verification

Author: **Byron**. Other author details are omitted at the author's request.

The delivered `main.pdf` is actual Tectonic/XeTeX/xdvipdfmx output: **15 main/reference pages plus five appendix pages, twenty total**. R6 follows the pre-evaluation design commit `6c0eef44c46a0ff525264b13ae1dae9b821ad3c2`. Its fixed main rule misses S1, S2 and S3. The subsequent writing clarification places the earlier-period qualification in the abstract and conclusion at the author's explicit request; it makes no positive R6 method claim. The earlier writing pass delivered 14+5 pages; its receipt remains historical.

## Read and edit

- `main.tex` controls compilation, layout and author metadata. `abstract.tex`, `sections.tex`, `appendices.tex` and `references.tex` contain the editable paper.
- `generated/round2-facts.tex` resolves empirical prose numbers from 36 source-bound fields; `results/supervisor-20261023/round2/numerical-facts.json` gives the source fingerprints and displayed values. Design constants come from the frozen study specification; illustrative numbers are explicitly synthetic.
- `generated/` and six vector figures are produced from archived aggregates by `build_supervisor_document.py`. ReportLab draws figure assets only; Tectonic compiles the paper.
- `round2-rewritten-passages.md` preserves the preceding E6–C1 wording at `348179c`. The current three-claim explanation, bilingual summaries, reviewer answers and title options are in `notes/supervisor-20261023/CONTRIBUTIONS.md`; current wording is in `abstract.tex` and `sections.tex`.
- E6–C1 baseline proof remains unchanged in `results/supervisor-20261023/round2/`. The writing-only update is recorded separately in `notes/supervisor-20261023/CONTRIBUTIONS-verification.json`: compilation, all eight changed pages visually checked, source-bound prose values, and no result/protocol/figure changes.
- R6 aggregates are in `results/supervisor-20261023/r6/`; `build_supervisor_r6_document.py` reads those files without fitting and generates `r6-facts.tex` and `r6-primary-table.tex`. Exact fact pointers and input hashes are in `notes/supervisor-20261023/r6-document-provenance.json`. The Chinese research memo is `notes/supervisor-20261023/r6-memo.md`; literature and the frozen protocol are separate files.
- The later writing clarification reads exactly two fixed QR-versus-F loss comparisons in `results/supervisor-20261023/r6-writing-hac-20261023/`; these are descriptive HAC readbacks, not R2 comparisons or new experiments. `build_supervisor_r6_writing.py` runs after the original R6 document reader and updates Table 10 plus `r6-writing-facts.tex` from existing aggregates only. Input hashes and field pointers are in `notes/supervisor-20261023/r6-writing-provenance.json`.

## Build and checks

Use the existing compatible project environment. The actual numerical environment is Python 3.12.14 with NumPy 2.3.5; no system package installation was performed. From the repository root:

```sh
python3 -B build_supervisor_document.py
python3 -B build_supervisor_r6_document.py
python3 -B build_supervisor_r6_writing.py
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic --only-cached --keep-logs --keep-intermediates manuscript/supervisor-revision/main.tex
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -m unittest discover -v
python3 -B reproduce_conditional.py
```

At the E6–C1 baseline `348179c`, the full suite passed 574 tests in 91.582 seconds. The original archive check returned `ARCHIVE_VERIFIED` for 69 files, with `accuracy_recomputed=false` and `raw_sources_read=false`. The document verifier was run on the original local execution chain after real tests and visual review; it confirmed 516 protected baseline files unchanged and no tracked deletions. It creates a new exclusive receipt and refuses to overwrite the archived one. Its only observed text-comparison repair removes TeX line-wrap hyphenation in the extracted conclusion; the PDF and paper were unchanged by that repair.

The full numbered local execution chain and pre-fit E5 commit are preserved separately from the website's directory-upload commits. Publication and local/remote equality are documented in the Chinese change inventory and final delivery receipt. The old `verify_supervisor_document.py` and its first-round receipts remain historical records.

## Display map

| Display | Current inputs and scope |
|---|---|
| Table 1 | Primary-source comparison; all 25 cells checked in `notes/supervisor-20261023/contributions-table1-audit.md`; Delft confidentiality wording corrected from original body passages |
| Table 2 | `round2/source-date-budgets.json`, computed from pinned existing source dates and frozen split indices |
| Tables 3/4 | `w3/tables3-4-ready.csv`; all 48 original method rows; two original primaries separately reported, remaining 71 matched contrasts Holm-adjusted |
| Table 5 | Original checked `inference/coverage-verified.csv`; consistent first-hit conditional likelihood |
| Table 6 | `e6/table6.csv`; original 33, four+, 33+, ordinary I, selected penalty and 33+ breaches |
| Table 7 / Figure 2 | `e3/primary-decomposition.csv`; additive common-baseline increments, order-dependent procedure comparison |
| Figure 3 | All 48 E5 cells from `e5/summary.csv`, original versus expanded QR33 relative to matched F; logarithmic loss-ratio axis |
| Table 8 / Figure 4 | Original U/V/breach evidence from `results/revision-20261022/paired-comparisons.csv` and `evaluation-summary.csv` |
| Table 9 | AR row uses `w4/ar-comparison.csv`; original rank/horizon and fixed-report supplements preserved |
| Figure 5 | Original all-breakpoint Murphy evidence in `inference/`; crossings do not establish population dominance |
| Figure 6 | `e6/lambda-path.csv` and `lambda-path-I.csv`; descriptive validation/evaluation paths, no new selection |
| Table 10 | `r6/primary-replication.csv` and `r6-writing-hac-20261023/comparisons.csv`; the same earlier FX QR reports versus matched frozen F2880 and original rolling F720, explicit origin counts and descriptive HAC p-values, plus the limited Treasury W52 analogue |
| Table 11 | Original historical construction table retained in Appendix B |
| Appendix C.1 | Notation remains in the appendix |

## Statistical and reuse limits

Both original primaries and every adverse result remain. The new 71-member reporting family is explicitly post-result, and the old 72-member analysis remains byte-preserved. E5's two failed predictions are retained with fixed denominators. Stronger shrinkage mitigates deterioration; neither benchmark equivalence nor evaluation noninferiority is established. I and exact F are different candidates at some ranks.

R6 retains all 516 report rows: 512 complete and four failed, with no retries or replacement candidates. All four failures belong to R3 FX/W720 at H6/H24 in the retrospective and inspected phases. Its independent archived-array verification checks the published design chronology, selections, all rows, private trace hashes and 525 protected baseline paths. Earlier retrospective origins had no evaluation role found in the bounded repository audit; this is familiar historical data and supplies neither prospective nor external validation. The original FX gain direction does not recur against rolling F/W720/d1, while Treasury's adverse direction recurs only in the W52 structural analogue. Exact earlier replication of its original W260 primary is unavailable.

The twelve panel series share a reporting system and overlapping dealer positions. No extra data were downloaded, no missing dates filled and no eligible series changed. This extension supplies no independent dealer sample. Private raw observations and per-origin traces stay in ignored directories; public outputs contain source fingerprints, selections, aggregates and numerical diagnostics. A public checkout can rebuild the document from these aggregate files, while full added-model reproduction also needs the pinned private inputs and retained trace context. The original clean-attempt reproduction route remains unchanged.
