# Second supervisor revision: source and verification

Author: **Byron**. Other author details are omitted at the author's request.

The delivered `main.pdf` is actual Tectonic/XeTeX/xdvipdfmx output: **14 main/reference pages plus five appendix pages, nineteen total**. The abstract has **158 whitespace-delimited words** and the conclusion **185** after expanding the numerical macros; hyphenated compounds count once. The earlier progress counts used a punctuation-token rule; these final counts use the archived verifier's stated whitespace rule.

## Read and edit

- `main.tex` controls compilation, layout and author metadata. `abstract.tex`, `sections.tex`, `appendices.tex` and `references.tex` contain the editable paper.
- `generated/round2-facts.tex` resolves empirical prose numbers from 36 source-bound fields; `results/supervisor-20261023/round2/numerical-facts.json` gives the source fingerprints and displayed values. Design constants come from the frozen study specification; illustrative numbers are explicitly synthetic.
- `generated/` and six vector figures are produced from archived aggregates by `build_supervisor_document.py`. ReportLab draws figure assets only; Tectonic compiles the paper.
- `round2-rewritten-passages.md` contains the complete final abstract, contribution paragraph and conclusion in copyable English.
- Final proof is in `results/supervisor-20261023/round2/`: `document-verification.json`, `test-verification.json` and `visual-review.json`. All nineteen physical pages were individually rendered and inspected.

## Build and checks

Use the existing compatible project environment. The actual numerical environment is Python 3.12.14 with NumPy 2.3.5; no system package installation was performed. From the repository root:

```sh
python3 -B build_supervisor_document.py
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic --only-cached --keep-logs --keep-intermediates manuscript/supervisor-revision/main.tex
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -m unittest discover -v
python3 -B reproduce_conditional.py
```

The final full suite passed 574 tests in 91.582 seconds. The original archive check returned `ARCHIVE_VERIFIED` for 69 files, with `accuracy_recomputed=false` and `raw_sources_read=false`. The document verifier was run on the original local execution chain after real tests and visual review; it confirmed 516 protected baseline files unchanged and no tracked deletions. It creates a new exclusive receipt and refuses to overwrite the archived one. Its only observed text-comparison repair removes TeX line-wrap hyphenation in the extracted conclusion; the PDF and paper were unchanged by that repair.

The full numbered local execution chain and pre-fit E5 commit are preserved separately from the website's directory-upload commits. Publication and local/remote equality are documented in the Chinese change inventory and final delivery receipt. The old `verify_supervisor_document.py` and its first-round receipts remain historical records.

## Display map

| Display | Current inputs and scope |
|---|---|
| Table 1 | Primary-source comparison; current source check in `notes/supervisor-20261023/round2-literature-recheck.md` |
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
| Table 10 | Original historical construction table retained in Appendix B |
| Appendix C.1 | Notation moved from the main text without changing table numbering |

## Statistical and reuse limits

Both original primaries and every adverse result remain. The new 71-member reporting family is explicitly post-result, and the old 72-member analysis remains byte-preserved. E5's two failed predictions are retained with fixed denominators. Stronger shrinkage mitigates deterioration; neither benchmark equivalence nor evaluation noninferiority is established. I and exact F are different candidates at some ranks.

The twelve panel series share a reporting system and overlapping dealer positions. No extra data were downloaded, no missing dates filled and no eligible series changed. This extension supplies no independent dealer sample. Private raw observations and per-origin traces stay in ignored directories; public outputs contain source fingerprints, selections, aggregates and numerical diagnostics. A public checkout can rebuild the document from these aggregate files, while full added-model reproduction also needs the pinned private inputs and retained trace context. The original clean-attempt reproduction route remains unchanged.
