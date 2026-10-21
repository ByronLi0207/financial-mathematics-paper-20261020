# Exploratory historical-selection extension

This directory contains the accepted aggregates from one execution of the [fixed extension protocol](../../protocol/revision-20261021-exploratory-protocol.md). The original evaluation interval had already been inspected when the extension was designed. These are exploratory results on the same source, not a new holdout or independent validation. The protocol and machine specification were publicly recorded before the added forecasts were calculated, at commit `69d5bb67c6ca1e3c1509e29c14400462ce2a1130`.

The comparison uses H=6 and 24 subsequent records, tau=19/20, 720 fully completed candidate episodes, and all 6,625 original issue origins. At each issue it evaluates full720, recent360, nearest360, recent180 and nearest180 using F (native headroom), S (raw reanchored increment envelope) and K (floored native peak). K is the original method L, relabeled. Nearest membership uses absolute signed-position distance with most-recent ties; selected paired rows retain chronological order. The listed extension configurations and reporting groups were fixed before the added forecasts were calculated.

| File | Data rows | Scope |
|---|---:|---|
| [summary.csv](summary.csv) | 30 | Every horizon, historical set and representation; loss, capacity, allowance, strict breaches, overrun, conditional denominator and unused allowance |
| [geometry.csv](geometry.csv) | 10 | Both anchor radii, exact F/S equality, mean absolute gap, selected age and arithmetic diagnostics |
| [comparisons.csv](comparisons.csv) | 22 | All 12 nearest-minus-recent and 10 same-set F-minus-S paired means |
| [monthly.csv](monthly.csv) | 26 | All 13 months at both horizons for the primary nearest360K-minus-recent360K comparison |
| [manifest.json](manifest.json) | — | Accepted source/code/specification/output identities, checks and measured resources |

## Units and column meanings

Monetary CSV fields use **unscaled source-reported USD**; the paper's tables often display USD millions. A pinball value is a forecast score with those units, rather than an observed funding cost or cash payment. In the definitions below, `P` is the realized sampled peak, `B=abs(N_t)` is the known issue-time floor, `C` is the issued forecast level, `O=max(P−C,0)` and `U=max(C−P,0)`. Unless explicitly conditional, each mean averages all issue origins in its row.

| Column | Meaning |
|---|---|
| `horizon` | Number of subsequent source records; not elapsed hours. |
| `eligible_count`, `selected_count`, `rank` | Candidate count, selected count and duplicate-preserving order-statistic rank at each issue; these are not independent tail-sample counts. |
| `origin_count` | Number of issue origins entering the reported row; 6,625 for each full-record summary/comparison. |
| `mean_pinball` | Mean of `0.95 O + 0.05 U`. |
| `mean_capacity` | Mean issued level `C`. The retained code/CSV name “capacity” denotes a passive forecast report. |
| `mean_extra_allowance` | Mean `C−B`; distinct from unused allowance. |
| `strict_breach_count`, `strict_breach_rate` | Count of `P>C` and that count divided by `origin_count`. Rates are fractions, not percentages; no tolerance changes event membership. |
| `mean_positive_overrun` | Mean `O` over all origins, including zeros when there is no breach. |
| `conditional_mean_overrun`, `conditional_overrun_denominator` | Sum of `O` divided by that rule's own strict-breach count, and the count itself. Different rules generally condition on different events. |
| `mean_unused_allowance` | Mean `U` over all origins. |
| `mean_pinball_difference` | Mean per-origin score on the named left side minus the named right side. Negative favors the left rule on the listed origins; it is calculated before display rounding. In `monthly.csv`, the sides are nearest360 K and recent360 K. |

In `geometry.csv`, `mean_absolute_f_minus_s` averages the absolute F/S report difference and `equal_capacity_count` counts exact stored F=S events. `mean_absolute_anchor_radius` and `mean_signed_anchor_radius` average the per-issue maximum absolute-anchor and signed-anchor distances, respectively; they are not average distances over all selected rows. `mean_selected_origin_age_records` averages each issue's mean selected age `t−i`, in records. `maximum_geometry_excess` and `maximum_arithmetic_tolerance` are separate maxima of per-issue arithmetic diagnostics; the issuer checks each origin before aggregation. Their tolerances never change breach flags or exact-equality counts.

An empty CSV field encodes null, not an observed zero. A defined conditional mean has an empty `conditional_overrun_undefined_reason`; with no breaches, the mean is empty and the reason is `NO_STRICT_BREACHES`. A monthly row with fewer than 30 origins retains its count and an `undefined_reason`, while its metrics are suppressed under `SUPPRESSED` status. Otherwise its status is `DISPLAYED`; the accepted monthly rows are all displayed. Calendar groups use naive issue timestamps and are not independent replications.

## Observed results and execution

The fixed primary H6 nearest360K-minus-recent360K mean is **−USD277,704.4657473585**, a **31.8280%** reduction relative to recent360K loss. All 12 matched retrieval score contrasts are negative. The reference matters: no added configuration beats the better original full720 F/S rule at either horizon. S has more strict breaches and greater mean positive overrun in all four matched retrieval comparisons. All four matched F comparisons reduce breach counts and mean positive overrun, while increasing conditional mean overrun on their own breach sets. Primary K reduces breaches and unconditional overrun but has a larger conditional mean overrun on a different event set. January 2016 is adverse for the primary monthly contrast at both horizons. The complete tables preserve these tradeoffs.

### Components of the two fixed primary score differences

At the existing weights, `Delta mean score = 0.95 Delta mean O + 0.05 Delta mean U`, where `Delta` is the named left side minus the right side. The components use all-origin means, not conditional overrun means. The following entries are **source-reported USD millions, rounded to six decimals**, over the same 6,625 H6 origins. This explains the existing primary contrasts; it does not calculate new forecasts or change their weights.

| Fixed primary contrast | `0.95 Delta mean O` | `0.05 Delta mean U` | Direct paired mean |
|---|---:|---:|---:|
| Original full720 F minus S | +0.047313 | −0.056688 | −0.009375 |
| nearest360 K minus recent360 K | −0.043915 | −0.233789 | −0.277704 |

The original F score advantage combines a greater overrun contribution with a larger reduction in unused allowance. In the primary K retrieval pair, both components fall, with unused allowance accounting for the larger reduction. These are stipulated forecast-score components, rather than observed financial payments or savings, and the interpretation is specific to these two contrasts.

Sources are the accepted [original summary](../summary.csv) and [paired comparison](../paired-comparison.csv), and the extension's [summary](summary.csv) and [comparisons](comparisons.csv). The last column preserves the stored direct per-origin paired mean. Components calculated from serialized aggregate means can differ at tiny floating-point precision; independently rounded displays need not sum exactly. No CSV or scientific manifest is changed.

All 11 recorded checks pass. The six shared full720 rows match original F/S/L metrics exactly; they are repeated references rather than new discoveries. The original 35 method rows and other original evidence remain unchanged in the parent results directory. New contrasts have no attached confidence interval, bootstrap or population-superiority test. Construction bounds and nominal breach frequencies are not conditional-coverage certificates.

The run began at `2026-10-21T20:43:44Z`. Its final pre-manifest checkpoint recorded **10.3072380419 seconds**, process high-water RSS **64,602,112 bytes (61.609375 MiB)**, and maximum observed process threads **1 across 675 snapshots**. Five numerical thread requests were set to one. A separate operating-system measurement of the completed process displayed **10.35 real seconds** and peak RSS **64,634,880 bytes**; the displayed wall time has two-decimal precision. Snapshot counts do not prove a continuous thread maximum, and the internal checkpoint precedes the final metadata write. The manifest records local source reuse and no download.

## Reproduce the extension

Reproduction requires the documented existing macOS Python/NumPy environment, all original modules, the four new code/test files and the [sanitized public-freeze receipt](../../state/revision-20261021-protocol-publication.json). This single receipt contains public repository metadata and is a replication dependency; private operational state is excluded. The extension expects the exact authorized source snapshot at `.scratch/data/1hourNetPositionsKaggle.csv`, with the source identity in the manifest. It does not fetch or accept an alternate input. Follow the root data-provenance instructions to obtain the matching snapshot; the original `run_study.py --fetch` route also executes the original study. A manual original `--input` file elsewhere does not populate the extension cache: place the independently obtained matching snapshot at the fixed path first, verify the documented byte count/hash, and preserve any existing mismatched cache for investigation.

From the repository root, use a new output path each time:

```
python3 -B -m unittest -v test_revision_selection test_revision_runner
python3 -B run_revision_selection.py --output .scratch/my-revision-attempt
```

The illustrated command writes its four CSVs and `manifest.json` directly to `.scratch/my-revision-attempt/public/`; it does not replace the accepted files in this directory. Inspect that attempt’s manifest and all checks. The runner refuses an existing output path, a symlink, a changed protocol/source or unverified resources. Inspect every check and actual output identity before accepting a reproduction. Numerical thread requests, strict internal resource stops, source restrictions, null reasons and stored float64 arithmetic are part of the implementation. No raw source CSV/ZIP, origin-level forecast traces, private selection evidence or third-party paper PDFs are distributed here; raw redistribution permission remains unverified.
