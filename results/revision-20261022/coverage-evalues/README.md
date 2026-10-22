# Late fixed-terminal conditional-coverage diagnostics

22 October 2026. This supplement calculates a mature one-sided evidence construction on the **already inspected** matched forecast archive. It changes no forecast, selection, primary comparison or original result. It is an exploratory diagnostic, not a new estimator, prospective registration, unseen validation sample, live-vintage test or financial safety certificate.

The [before-computation design](../../../protocol/revision-20261022/coverage-evalue-design.md), [specification](../../../protocol/revision-20261022/coverage-evalue-spec.json) and [61-file executable freeze](../../../protocol/revision-20261022/coverage-evalue-executable-freeze.json) were publicly byte-verified at commit `ff770368549d5b3962b0e121134d681ef2b4f470`, 15:32:30 UTC, before production began at 15:33:02 UTC. Freeze SHA-256: `ae1d118bb57bc031d24e19a084ec54926442960b59af9c2a29700a82a66790f4`. The [sanitized actual verification record](before-execution-publication.json) binds eight new raw files and all 61closure paths, with all 337older public files unchanged. This before-calculation boundary does not erase earlier method, sample or diagnostic selection.

## Null and construction

Let `I_t = 1{stored P_(t,H) > stored C_(t,H)}`; exact equality is a nonbreach. The formal null is the **datewise full-issue-information conditional upper bound** `E[I_t|F_t] <= 1/20` at every declared issue. It is different from equality of unconditional mean losses, an overall empirical five-percent hit rate or exact quantile identification at an atom. It presumes an issue-measurable causal report. Treasury retains the downloaded-vintage economic-date convention; its current floor is not claimed to have been available on that historical public-release date.

For a fixed alternative `u` in `[alpha,1]`, `alpha=1/20`, the factor is `u/alpha` on a hit and `(1-u)/(1-alpha)` otherwise. Its conditional expectation is at most one under that null. Partition actual issue indices by `(t-first_origin) mod (H+1)`. Earlier same-phase labels have resolved before the next issue, so a phase product has expectation at most one. Mix its **whole product** over the fixed uniform prior on `[alpha,1]`, then average every H+1phase with equal weight; an empty phase has value one. No independence, stationarity or moment bound on financial magnitudes is used in this elementary fixed-terminal argument. Causality, conditional-null and maturity assumptions remain essential.

All 56 report cells are retained: eight source/horizon/window configurations crossed with QR, KNN, scaled KNN, frozen F/S/K and AR. This matched subset excludes 24 rolling and 18 one-state reports from the 98-report archive. Structural aliases remain in the56-label count. The complete [56-row summary](coverage-evalue-summary.csv) and [896-row phase table](coverage-evalue-phases.csv) contain exact hexadecimal Fraction identities, approximate display labels and flags. Production uses a positive beta-integral recurrence. The [independent checker](../../../verify_coverage_evalues.py) instead uses

```text
E(n,k) = sum(comb(n+1,j)*19**(k-j), j=0..k)
         / ((n+1)*comb(n,k)).
```

All averages and `>=1120` crossings use exact rationals. Display rounding never defines a crossing. We average dependent phases rather than multiplying them or selecting a favorable one. This is a **fixed-terminal** construction; there is no full-filtration supermartingale, arbitrary-stopping, running-maximum or anytime p-value claim.

For a genuinely fixed procedure family, Markov's inequality and a union bound give the formal reference threshold `56/(1/20)=1120` without cell independence. **These inspected-sample diagnostics do not obtain retrospective empirical5% familywise error control from that threshold.** Correcting over98current reports would not automatically cover the wider research search. The output label is `adjusted_reference_threshold_crossed`, not a significance or coverage-PASS verdict.

## Complete outcome and interpretation

Four of56cells cross the fixed reference threshold, all QR:

| Source | H | W | Strict hits / issues | Approximate evidence value |
|---|---:|---:|---:|---:|
| FX |24|720|924 / 6625|8.499113e7|
| Treasury |6|52|84 / 277|1.310959e8|
| Treasury |6|260|54 / 277|2.204376e3|
| Treasury |24|52|132 / 277|3.814064e4|

The other 52cells and all896 phase rows remain in the linked tables. None was dropped or retuned. A noncrossing is not successful conditional coverage: Treasury H24 W260 AR has59strict breaches in277issues, while its evidence value is about11.0284, below1120. Treasury QR with84breaches has about1.311e8 at H6 W52 and59.4235 at H24 W260; the same overall count does not determine evidence when phase structure differs. These are diagnostic observations, not a comparison of financial safety by evidence magnitude.

Longer horizons leave fewer observations within each phase. The uniform prior, fixed family threshold, dependence and inspected selection history constrain interpretation. No power or equivalence study was run, and the prior/phase/family was not expanded after these values. A rejection of the stipulated fixed-procedure null would not identify the failure's cause/date, mean-loss superiority or financial loss severity. Nonrejection cannot certify sharpness, tail safety, funding adequacy or a beneficial intervention. All original favorable and adverse loss comparisons remain unchanged.

## Actual execution and independent arithmetic

The [actual manifest](coverage-evalue-manifest.json) binds the named successful conditional replica, genuine fresh AR manifest, version-2 upstream readback and90 consumed input-file identities. All40 NPZ containers and588 NPY headers were checked before the eligible numerical payloads. Actual chronological origins/refits, finite floor/report/target relations, common targets across methods/windows and nested realized horizons passed. Pinball and unused rolling/one-state payloads did not select the family.

The newly generated [independent readback](independent-readback.json) recounts every strict saved hit and actual-origin phase, then checks every 56/896 row, exact value, flag, semantic key, input binding and complete export inventory. It does not import either coverage production module. Its own code was separately published before calculation; SHA-256 `fdc9025a988a3ef44989df98bc7a3088f58d74dd6b857c278211f5e0e09b7967`. It is not a borrowed upstream PASS, independent dataset or another model validation.

| Process | Internal final-checkpoint seconds | External elapsed seconds | External peak RSS bytes | Accepted OS-thread snapshots / maximum |
|---|---:|---:|---:|---:|
|56-cell calculation|1.096508|1.19|92,766,208|98 / 1|
|Independent complete readback|1.139226|1.18|79,855,616|154 / 1|

Both external measures recorded zero swaps. The [execution record](execution-check.json) distinguishes final internal checkpoints from later external process high-water measurements. One worker ran at a time and one numerical thread was requested. These are observations, not a continuous thread guarantee, memory sandbox or active research hours. No raw source CSV, new download, model fit, report repair, parameter search or package installation was used.

## Reproduce with genuine new identities

First follow the [root conditional guide](../../../README.md) and [fresh AR guide](../ar1-fresh-reproduction/README.md) to generate a successful local conditional attempt, a new AR attempt and its genuinely generated version-2 readback. Use new output IDs and the actual hash of that new readback. A fresh run must not substitute the archived receipt merely because its status says PASS.

```text
python3 -B run_coverage_evalues.py --execute \
  --replication-dir .scratch/revision-20261022/replication-REPLAY_ID \
  --ar1-attempt-id AR_ID \
  --readback state/revision-20261022/my-new-ar-readback.json \
  --readback-sha256 HASH_OF_THAT_GENUINE_NEW_READBACK \
  --attempt-id NEW_COVERAGE_ID \
  --freeze ae1d118bb57bc031d24e19a084ec54926442960b59af9c2a29700a82a66790f4

python3 -B verify_coverage_evalues.py --execute \
  --replication-dir .scratch/revision-20261022/replication-REPLAY_ID \
  --ar1-attempt-id AR_ID --coverage-attempt-id NEW_COVERAGE_ID \
  --readback state/revision-20261022/my-new-ar-readback.json \
  --readback-sha256 HASH_OF_THAT_GENUINE_NEW_READBACK \
  --freeze-sha256 ae1d118bb57bc031d24e19a084ec54926442960b59af9c2a29700a82a66790f4 \
  --self-sha256 fdc9025a988a3ef44989df98bc7a3088f58d74dd6b857c278211f5e0e09b7967 \
  --output state/revision-20261022/my-new-coverage-readback.json
```

The producer writes an exclusive `coverage-evalues-NEW_COVERAGE_ID` under that replica. A missing, altered, duplicate, nonfinite or incomplete cell stops the whole family; it does not shorten the window or reduce56. Ordinary partial writes are quarantined, and an incomplete/hard-killed attempt has no accepted complete manifest. All old attempts and forecasts are preserved. New vectors and readbacks receive their own actual identities; numerical equality to this archive is separate from a successful computation/readback.

The statistical foundations are mature: [Henzi and Ziegel, arXiv2103.08402v3](https://arxiv.org/abs/2103.08402v3) for binary evidence/delayed fixed-terminal combination and [Casgrain, Larsson and Ziegel, arXiv2204.05680v2](https://arxiv.org/abs/2204.05680v2) for bounded conditional-moment betting. The design records selected reading ranges and the direct one-sided proof, without borrowing their optional-stopping, power or continuity-qualified equality-identification results. Source PDFs, raw observations and per-origin vectors are not redistributed here.
