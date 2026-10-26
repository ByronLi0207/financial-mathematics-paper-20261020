# Reproduction of the local v3 revision

This branch starts at cbce3986276e994add53b0f5c6bdeec5191f4412. Original440 files, main and FINAL.md remain untouched. No push is performed.

## Existing dependencies and raw inputs

Use Python3 with NumPy, ReportLab and pypdf already available. No installation was performed. test files are unittest-compatible; pytest can run them in an environment where it is already installed. On this host pytest is unavailable.

For a fresh clone, first follow the original README source-acquisition section to obtain the exact Kaggle Version2 one-hour member and put its accepted bytes at .scratch/data/1hourNetPositionsKaggle.csv (SHA-256 b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa). Copy the already published data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv bytes to .scratch/revision-20261022/nyfed-PDPOSGS-B.csv. Do not substitute another vintage or frequency. The recovery/ directory retains the actual bounded successful official acquisition receipt; recover_v3_traces.py records this one-off recovery and refuses to overwrite a retained attempt. Raw FX inputs and private traces are not committed.

## Ordered execution on a fresh checkout

Use a fresh checkout/private attempt tree, because existing retained attempts are deliberately not overwritten.

```sh
python3 -B reproduce_conditional.py verify
python3 -B reproduce_conditional.py replicate --attempt-id revision-v3-b5-full
python3 -B -m unittest test_inference_tests test_parsimonious_v3 -v
python3 -B run_v3_inference.py --stage B1
python3 -B run_v3_inference.py --stage B3
python3 -B run_v3_inference.py --stage B2
python3 -B run_v3_inference.py --stage B4
```

Run parsimonious_v3.py for every combination source=nyfed_weekly,H=6/24,W=52/260 and source=fx_hourly,H=6/24,W=720/2880, one process at a time, using --source --horizon --window. Then run --aggregate. Each cell retains all5 candidate receipts, accepted fit diagnostics and its resource measurements.

```sh
python3 -B parsimonious_v3.py --aggregate
python3 -B v3_revision.py
python3 -B build_revision_v3.py
```

The B1 receipt's started_utc was originally recorded as a phase label rather than a timestamp; no exact start time is inferred from it. Its measured elapsed/RSS/thread fields and checkpoint UTC are retained. Other inference and C2 receipts record actual UTC starts.

## Deliverable and acceptance

The canonical new content is manuscript/revision-v3/paper-content.json; formal source main.tex and rendered paper.pdf are adjacent. The PDF is ReportLab-rendered, with vector plots and actual mathematical scripts. The native desktop compiler accepted the TeX source without a new software installation; its separate preview/export layout is not claimed identical to the delivered ReportLab PDF.

The original six-table numerical archive is immutable. New complete inference CSVs and C2 outputs are under results/revision-20261023/. Negative-sentence counts follow the literal full-stop split and named regex on abstract/prose, with main/appendix scopes and a decimal-safe sensitivity separately reported. All revised scientific analyses are exploratory and reuse inspected outcomes.
