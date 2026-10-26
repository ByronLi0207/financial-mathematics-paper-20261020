# Loop 099 — internal referee A: inference definitions and limits

Audit: 2026-10-23T23:47:08Z to 2026-10-23T23:48:02Z UTC. Branch `revision-v4-jof`; observed HEAD `581674aeded6ad5fb912c4183463e1f18b1d9c96`. Same-model internal textual review, not external peer review. Parent goal remains active to 2026-10-24T00:31:50Z.

## Actual reading scope and candidate

Read current Supplement JSON index 8, **S9. Complete inference and specification outputs**, all five blocks: three full prose blocks (0–2), including inline DQ null, and both table captions (3–4; S24/S25). Read corresponding Supplement TeX 610–710, excluding both table bodies. No table cells were read, counted or validated.

Necessary bounded main context only: Research design and transparency, JSON index 4 blocks **0, 7, 8, 9** (three prose, one equation); corresponding article TeX line 185 and lines 200–205. No other section, financial output, private trace, source paper or previous verdict was evidence. No S16 table/family inventory was reaudited.

Fresh SHA-256 fingerprints:

- Supplement JSON: `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28`
- Supplement TeX: `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8`
- Supplement PDF: `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991`
- Main JSON: `b9197f80173b8dccbb74cb2086cea202a4f2d1c1659768f7f62835a1a9a1510b`
- Article TeX: `2eda351b4dcc707c48b95133d6745fbb13a0b7b3ac8af049a4b856e948f30f11`
- Main PDF: `dbcf2d2d6bd301e36cecfca912717d5cdff8e935c770e56472e7c5d4d35d0714`

Paths respectively: `submission-jof/{supplement-content.json,supplement.tex,supplement-preview.pdf,manuscript-content.json,manuscript.tex,manuscript-preview.pdf}`. PDFs were hashed, not viewed; root's publication gate was not rerun.

## Definition and interpretation checks

1. **Full versus sparse samples.** S9 separates sparse-grid coverage from full-sample DQ. Main fixes the grid at first origin+j(H+1), while full-sample DQ uses mature hit lags H+1 through H+4 and issued capacity. POF's all-grid-hit denominator differs from adjacent transition pairs. Sparse windows remove target overlap, not shared-training dependence; the stated short Treasury grids remain weak for asymptotic calibration. No denominator or grid count was newly verified.

2. **Legacy versus new CC.** S9 explicitly says retained CC sums POF over all grid hits and independence conditional on the initial hit, combining initialization conventions. It denies equivalence to the finite-sample LR conditioning both components on the initial observation. Main separately identifies new S16 transition-conditional CC and says it does not replace the archived convention. Missing transition rows remain unidentified/NA. This is a clearly bounded working reference, not an inherited finite-sample likelihood guarantee.

3. **DQ and boundary qualifications.** S9 states the six-instrument null, finite/full-rank/positive-definite covariance and diagnostic capacity standardization. Its sample constants are not forecast inputs; invertible-transform invariance requires the intercept and positive finite scale. Nonrejection leaves other departures untested. Fixed-window overlapping-target HAC is an adaptation, not a direct CAViaR theorem application. Exact .05 equality tests can reject valid conservative quantiles with atoms; low hits are not automatically undercoverage. No new theorem/Wald calculation.

4. **DM, HLN and bandwidth.** Main states Bartlett-HAC, the declared bandwidth and doubled sensitivity, under mixing, adequate moments and positive long-run variance. S9 specifies centered products/denominator n and warns that doubling still falls short of long training-history dependence. HLN's use for pinball is explicitly approximate rather than its original MSE setting. These checks are not claimed to establish calibrated long-run covariance or exact finite-sample p values.

5. **Family, status and selection scope.** S25 caption names the 72-member common-history family, nonsignificant/identical-loss rows, frozen F/S/K and negative-t direction. NA status differs from bookkeeping p=1. Main freezes new families separately. Holm requires valid component p values; it repairs neither working references nor inspected-sample selection. S9 labels all analyses post-result. S24 integral agreement is an identity check, not new dominance evidence. No family/decision count, crossing statistic or table completeness was recalculated.

## Verdict and limits

No necessary scientific-conclusion issue or author-pending correction found. This checks current S9 prose/captions and bounded main definitions, not numerical outputs or primary-source theorem accuracy afresh.

Only this note was written. No models/statistics/proofs/tests/recomputation, raw/private-vector access, new search/network/UI/Claude/Cloud, nesting, source/result/state/ledger edit or commit. Final full readback, SHA-256 and UTC time are reported on delivery; no note edit follows.
