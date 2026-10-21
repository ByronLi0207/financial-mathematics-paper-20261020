# Historical headrooms and current-state scenarios for sampled inventory peaks

An English working-paper study of a recorded market-maker net-inventory series. It compares mature empirical quantile constructions for a distinct response: the maximum absolute inventory over the current and next H recorded observations. It is a small application and measurement study, without a new algorithm, first-application claim, or coverage theorem.

The six-hour active literature review and two-hour active design gates are complete. The scientific specification was frozen at **2026-10-21 05:46:37 UTC**, before this study's labels, forecasts or losses were computed, and published in commit `6dd404d6e700ff031793d68be209e8f783b22582`. The [12-page English working paper](manuscript/working-paper/paper.pdf), [successfully compiled TeX source](manuscript/working-paper/main.tex), [complete aggregate results](results/), and bounded replication code are available. The original 24-hour checkpoint at 2026-10-21 07:28:56 UTC has been audited after it actually elapsed; see the [research-window and delivery audit](RESEARCH_WINDOW_AUDIT.md). Reading/design records, publication evidence and their limits are distinguished there. Elapsed scheduling time is not counted as active reading or design.

## Question and observed result

Does pooling historical peak headrooms at their own starting inventories improve fixed quantile loss relative to revaluing historical increment envelopes at today's signed inventory? The latter transfers the established historical-scenario revaluation principle. It does not implement filtered historical simulation, a volatility filter, fitted innovations or derivative pricing.

The common evaluation sample contains **6,625 origins**, with seven prespecified cells and five methods in every cell. At the primary H=6, n=720, tau=0.95 setting, mean pinball loss is USD441,774.04 for historical headrooms (F) and USD451,148.90 for current-state scenarios (S): the paired mean difference is USD-9,374.86, or -2.08% of S loss. F nevertheless has more strict breaches (332 versus 254) and larger mean positive overruns. This finite-record score advantage reverses at H=24 and tau=0.90. All four descriptive resampling ranges cross zero; they are not confidence intervals or superiority probabilities. Results are retained in the original method/cell order, including adverse comparisons and simple references.

The response is a sampled, netted inventory peak. It does not measure continuous-time maxima, gross currency exposure, cash or margin requirements, executable trading profit, or the effect of changing a dealer's risk policy. The source's timezone and historical field-release convention are unverified. The exercise uses an explicit retrospective information convention.

## Files and status

- `protocol/study-spec.json`: exact frozen seven-cell/five-method specification.
- `protocol/output-schema.json`: exact aggregate table, figure and provenance schemas.
- `protocol/research-design.md` and `protocol/design-freeze.json`: question, alternatives, assumptions and pre-evaluation identities.
- `notes/`: primary-source reading records; they distinguish abstract screening, selected full-text reading and full-paper reading. Recent is not treated as evidence of popularity. The [paper evidence map](notes/paper-evidence-map.md) ties the nine final references to actual consulted passages and claim boundaries.
- `study_data.py`, `study_core.py`, `study_report.py`, `run_study.py`: bounded acquisition, issue-time calculation, aggregate reporting and the single execution entry point.
- `test_data.py`, `test_core.py`, `test_report.py`, `test_runner.py`: 74 artificial tests, including hand-valued examples, chronology, invalid sources, output boundaries and stopping behavior.
- `results/`: four verified aggregate tables, the primary run manifest and separate fresh-acquisition verification.
- `manuscript/working-paper/`: reviewed paper, shared manuscript content, successfully compiled source, three unchanged vector figures and rendering verification.
- `build_paper.py`, `build_tex.py`, `requirements-paper.txt`: document-only rebuilding from shared manuscript content; they do not recalculate scientific outcomes.

A COMPLETE run manifest concerns the scientific run. It is separate from manuscript compilation, PDF inspection, GitHub byte verification and the final research-window audit. Local scratch and operational state are excluded from publication.

## Data provenance and access

Use version 2 of [David Lindsay's Net Position Time Series Dataset](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset), member `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv` (the accepted one-file archive uses a flat CSV member). The exact CSV is 1,286,391 bytes with SHA-256:

```
b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa
```

It contains 18,576 rows; only `datetime` and `NetPosUsd` enter the analysis. The source dates run from 5 February 2014 to 24 January 2017, with one-hour and 49-hour gaps preserved. H counts recorded steps, rather than elapsed hours. The download endpoint and container were observed on 21 October 2026 at 02:42 UTC. A separate fresh-cache acquisition at 06:24 UTC exercised the published one-file route, accepted the identical CSV and reproduced all four tables and three figures byte for byte; see [acquisition verification](results/acquisition-verification.json). The primary manifest records local reuse and does not claim a new request.

The observed rights label is “Data files © Original Authors”; raw redistribution permission has not been verified. This repository distributes original code, aggregate results and acquisition instructions, not the source CSV/ZIP, third-party papers, origin-level forecasts or development thresholds. Access availability and legal reuse conditions may change.

## Reproduction

The recorded environment is CPython3.12.14, NumPy2.3.5, ReportLab4.4.9 on macOS arm64. `requirements.txt` pins the two numerical/reporting dependencies. Use an environment where these versions are already available. The production resource monitor is currently macOS-specific and deliberately stops on other operating systems rather than claiming unmeasured resources.

Run the artificial checks first:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -m unittest -v test_data test_core test_report test_runner
```

To use the anonymous one-file acquisition route, explicitly request it:

```
python3 -B run_study.py --fetch
```

This creates only the fixed task cache `.scratch/data/1hourNetPositionsKaggle.csv`. It performs a bounded anonymous one-file request only if that input is absent. An existing mismatched input is rejected, never replaced. No credentials, account registration, retry loop, mirror, or full-dataset download is used. A changed endpoint, rights condition or content identity stops the attempt. To reuse an independently obtained matching file instead:

```
python3 -B run_study.py --input /path/to/1hourNetPositionsKaggle.csv
```

The runner sets five numerical thread requests to one before importing NumPy and creates a new exclusive output directory under `.scratch/`. Its `public/` subtree contains four CSVs, three vector PDF figures and `results/run-manifest.json`. Inspect `run_status`, all checks, completed cells and resource observations before promoting output. Failed attempts remain distinct. The manifest's common-origin fingerprint is SHA-256 of the ordered indices, each encoded as an unsigned eight-byte little-endian integer.

Bounds are 540 seconds for orderly stopping, a 600-second OS alarm, a 1.5GiB early RSS stop, at most two observed OS threads, 25MiB per download and small explicit storage/array caps. RSS is the process high-water mark reported at checkpoints; thread counts are snapshots, not a continuously observed peak. These are measured observations with limits, not an operating-system hard memory sandbox.

## Interpretation and closest work

Wisniewski, Lindsay and Lindsay (2020), [PMLR128:285–301](https://proceedings.mlr.press/v128/wisniewski20a.html), already study conformal forecasts of market makers' net positions on this source. Their scalar next-epoch signed-position response differs from this multi-record absolute peak; their published scores are not directly comparable benchmark numbers. Historical scenario revaluation and financial peak-risk quantiles also have established precedents, detailed in the design and manuscript. A changed dataset or target does not establish a new method.

Evaluation is a retrospective specification holdout with completed-label feedback, not external preregistration or a prospective live trading test. Overlapping labels, rolling windows and changing financial laws preclude importing exchangeability or stationary-bootstrap inference guarantees without separate assumptions. Pinball preferences are declared scoring weights, not estimated dealer costs. Cross-cell losses at different tau values do not define an across-preference winner.

## Document rebuilding and measured execution

The current `main.tex` compiled successfully with the desktop editor's built-in compiler. That interface supplied diagnostics without a standalone PDF export. The supplied `paper.pdf` is independently typeset from `paper-content.json` using ReportLab4.4.9, with the three unchanged scientific vector pages appended by pypdf6.10.0. It is not represented as that compiler's export. All twelve PDF pages were rendered and inspected; font coverage, page bounds, equations, tables, references and figure labels were checked. The [manuscript README](manuscript/working-paper/README.md) and [rendering verification](manuscript/working-paper/rendering-verification.json) record this distinction.

Using the documented existing macOS environment, the document-only commands are:

```
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
```

Both refuse to overwrite an existing output. `build_tex.py` regenerated source byte-identical to the compiled source. `build_paper.py` uses the four existing Times New Roman fonts in `/System/Library/Fonts/Supplemental/`; missing fonts stop it, and whole font files are not distributed. `requirements-paper.txt` lists the existing document dependencies. No software was installed for this project.

The primary attempt `20261021T060715Z-de1704c9` recorded 8.02145 seconds, process high-water RSS 80,936,960 bytes (77.19MiB), and a maximum observed OS thread count of 1 across 565 snapshots. This final resource checkpoint precedes metadata-write completion. The separate fresh-acquisition replication recorded 8.91694 seconds, 82.64 MiB and 1 observed thread; the earlier complete run used 82.95 MiB. Scientific tables and figures agree byte for byte across these executions. Thread snapshots are not a continuously observed peak, and the stated resource bounds are not an operating-system hard memory sandbox.
