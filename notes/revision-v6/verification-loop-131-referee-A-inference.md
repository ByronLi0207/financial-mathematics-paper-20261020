# Loop 131 - internal referee A: bounded S9 inference review

Reading: 2026-10-24T00:21:30Z to 00:21:57Z; audit completed 2026-10-24T00:22:25Z UTC. Branch `revision-v4-jof`; observed HEAD `d985c48e009dc6f0f332e337bf98d4b3faf32e22`. Same-model internal textual review, not external peer review. Parent goal remains active until 2026-10-24T00:31:50Z.

## Actual current scope

Read Supplement JSON index 8, **S9. Complete inference and specification outputs**, all five blocks at the permitted level: three full prose blocks (0-2) and both table captions (3-4, S24/S25). No standalone equation, subheading or figure blocks occur; the inline DQ moment null was read. Read corresponding Supplement TeX 610-710, excluding both table bodies. No table cells, result files, vectors, scripts/tests, source papers, other sections or prior verdicts were evidence.

Source hashes before reading at 00:21:30Z and after reading at 00:21:57Z were identical (before=after):

- `submission-jof/supplement-content.json`: `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28`
- `submission-jof/supplement.tex`: `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8`
- `submission-jof/supplement-preview.pdf`: `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991`

The PDF was hashed, not viewed.

## Interpretation checks

1. **Full/sparse information and maturity.** S9 distinguishes sparse-grid coverage from full-sample DQ. Its instruments are an intercept, four mature hit lags and issued capacity; only a full-rank case has the stated reference degrees of freedom. Capacity centering/scaling across diagnostic rows is numerical conditioning, not a forecast input or a quantity asserted available at issue. The stated invariance requires an intercept and finite positive capacity scale. Rejection concerns those moments; nonrejection leaves other conditional departures untested.

2. **Dependence, bandwidth and HLN.** Centered moment products use denominator n. Sparse windows remove target overlap, not shared training; short Treasury grids weaken asymptotic calibration. Doubling bandwidth remains short versus training history and does not establish adequate long-run covariance. HLN is approximate for pinball, outside its original MSE setting. Fixed-window overlapping-target HAC does not inherit the growing-sample CAViaR theorem. No covariance/theorem was checked.

3. **Coverage, atoms, legacy CC and NA.** Equality tests require exact .05 moments; valid conservative quantiles with atoms can have fewer strict hits, so low-frequency rejection is distinguished from undercoverage. POF uses all grid hits, while independence conditions on the first hit's transitions. Retained CC sums the two conventions and is explicitly not the uniformly first-observation-conditioned finite-sample LR. Its chi-square p remains a dependence/boundary/small-sample working reference. Missing transition rows are unidentified, and covariance must be finite, full rank and positive definite. Failure/NA is not evidence of calibrated forecasts.

4. **Family and post-inspection selection.** S25 caption declares the fixed common-history 72-member family with frozen F/S/K at common W, nonsignificant and identical-loss rows and negative-t direction. Its threshold uses unrounded normal-reference DM p values/adjustment, conditional on valid component tests. Identical-loss NA t/status differs from bookkeeping p=1. Holm does not validate component working references or erase inspected-sample selection. S9 explicitly calls all analyses post-result and reuses inspected samples. No family size, threshold decision or status inventory was recounted.

5. **Trace/arithmetic checks retain limited meaning.** S24 integral agreement is an arithmetic check, not independent validation/coverage. Block 0 references outputs/statuses/scripts/tests/recovery; these are provenance claims, not new execution evidence. No linked artifacts or private traces were opened.

## Explicit remaining scope gaps

S9 does not restate the full HAC bandwidth formula, exact mature-hit lag offsets, all regularity conditions, or the newer S16 transition-conditional CC/family definitions. Those implementations/new families were not audited or inferred from the old 72-member caption. Numerical reference validity, completeness and primary-source theorem accuracy remain unverified here.

## Verdict and limits

No necessary scientific-conclusion issue or author-pending correction found within the complete permitted S9 prose/caption scope. The section makes its working-reference, maturity, dependence, boundary, NA and selection limits explicit; the listed scope gaps remain outside this verdict.

Only this note was written. No source/result/state/ledger edit, commit, statistical counts/recomputation, model/proof/test execution, raw/private-vector access, network/search/UI/Claude/Cloud or nesting. Final full readback, hashes and UTC time are reported on delivery; no note edit follows.
