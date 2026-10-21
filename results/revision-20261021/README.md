# Exploratory historical-selection extension

This directory contains the accepted aggregates from one execution of the [fixed extension protocol](../../protocol/revision-20261021-exploratory-protocol.md). The original evaluation interval had already been inspected when the extension was designed. These are exploratory results on the same source, not a new holdout or independent validation. The protocol and machine specification were publicly recorded before the added forecasts were calculated, at commit `69d5bb67c6ca1e3c1509e29c14400462ce2a1130`.

The comparison uses H=6 and 24 subsequent records, tau=19/20, 720 fully completed candidate episodes, and all 6,625 original issue origins. At each issue it evaluates full720, recent360, nearest360, recent180 and nearest180 using F (native headroom), S (raw reanchored increment envelope) and K (floored native peak). K is the original method L, relabeled. Nearest membership uses absolute signed-position distance with most-recent ties; selected paired rows retain chronological order. No model, count, horizon, score or reporting group was chosen after these results.

| File | Data rows | Scope |
|---|---:|---|
| [summary.csv](summary.csv) | 30 | Every horizon, historical set and representation; loss, capacity, allowance, strict breaches, overrun, conditional denominator and unused allowance |
| [geometry.csv](geometry.csv) | 10 | Both anchor radii, exact F/S equality, mean absolute gap, selected age and arithmetic diagnostics |
| [comparisons.csv](comparisons.csv) | 22 | All 12 nearest-minus-recent and 10 same-set F-minus-S paired means |
| [monthly.csv](monthly.csv) | 26 | All 13 months at both horizons for the primary nearest360K-minus-recent360K comparison |
| [manifest.json](manifest.json) | — | Accepted source/code/specification/output identities, checks and measured resources |

The fixed primary H6 nearest360K-minus-recent360K mean is **−USD277,704.4657473585**, a **31.8280%** reduction relative to recent360K loss. All 12 matched retrieval score contrasts are negative. The reference matters: no added configuration beats the better original full720 F/S rule at either horizon. S has more strict breaches and greater mean positive overrun in all four matched retrieval comparisons. Primary K reduces breaches and unconditional overrun but has a larger conditional mean overrun on a different event set. January 2016 is adverse for the primary monthly contrast at both horizons. The complete tables preserve these tradeoffs.

All 11 recorded checks pass. The six shared full720 rows match original F/S/L metrics exactly; they are repeated references rather than new discoveries. The original 35 method rows and other original evidence remain unchanged in the parent results directory. New contrasts have no attached confidence interval, bootstrap or population-superiority test. Construction bounds and nominal breach frequencies are not conditional-coverage certificates.

The run began at `2026-10-21T20:43:44Z`. Its final pre-manifest checkpoint recorded **10.3072380419 seconds**, process high-water RSS **64,602,112 bytes (61.609375 MiB)**, and maximum observed process threads **1 across 675 snapshots**. Five numerical thread requests were set to one. A separate operating-system measurement of the completed process displayed **10.35 real seconds** and peak RSS **64,634,880 bytes**; the displayed wall time has two-decimal precision. Snapshot counts do not prove a continuous thread maximum, and the internal checkpoint precedes the final metadata write. The manifest records local source reuse and no download.

Reproduction requires the documented existing macOS Python/NumPy environment, all original modules, the four new code/test files and the [sanitized public-freeze receipt](../../state/revision-20261021-protocol-publication.json). This single receipt contains public repository metadata and is a replication dependency; private operational state is excluded. The extension expects the exact authorized source snapshot at `.scratch/data/1hourNetPositionsKaggle.csv`, with the source identity in the manifest. It does not fetch or accept an alternate input. Follow the root data-provenance instructions to obtain the matching snapshot; the original `run_study.py --fetch` route also executes the original study. A manual original `--input` file elsewhere does not populate the extension cache: place the independently obtained matching snapshot at the fixed path first, verify the documented byte count/hash, and preserve any existing mismatched cache for investigation.

From the repository root, use a new output path each time:

```
python3 -B -m unittest -v test_revision_selection test_revision_runner
python3 -B run_revision_selection.py --output .scratch/my-revision-attempt
```

The illustrated command writes its four CSVs and `manifest.json` directly to `.scratch/my-revision-attempt/public/`; it does not replace the accepted files in this directory. Inspect that attempt’s manifest and all checks. The runner refuses an existing output path, a symlink, a changed protocol/source or unverified resources. Inspect every check and actual output identity before accepting a reproduction. Numerical thread requests, strict internal resource stops, source restrictions, null reasons and stored float64 arithmetic are part of the implementation. No raw source CSV/ZIP, origin-level forecast traces, private selection evidence or third-party paper PDFs are distributed here; raw redistribution permission remains unverified.
