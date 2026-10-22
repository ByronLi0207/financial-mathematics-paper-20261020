# Metadata-only feasibility of a closed coverage-diagnostic input family

22 October 2026. This review identifies inputs for a possible later diagnostic; it does not execute that diagnostic. No hit/breach vector, score value, score ranking, e-value, p-value or model fit was read or computed. NPZ containers were hashed and their NPY headers inspected, without loading NPY payload arrays. No raw source observations, UI, network or package installation was used. Frozen scientific files and results were not modified.

## Actual eligible inventory

The proposed **56 report cells are correct**, if the family is defined as all eight source/H/window configurations crossed with exactly these seven method labels:

`QR, KNN, SCALED_KNN, frozen_F, frozen_S, frozen_K, AR1_REPLAY`.

There are 24 selected conditional cells, 24 matched frozen historical cells and eight cells from the fresh AR execution. This is a deliberately closed subset of the 98 total archived procedure reports (90 original plus eight AR); it excludes 24 rolling historical and 18 one-state reports. It must not be described as all archived procedures. Some reports can coincide: plain KNN at the short Treasury window uses k=W and is structurally the same as frozen F. Thus 56 labels do not establish 56 independent procedures or tests.

| Source | H | W | Full evaluation issue indices | Records | Global H+1 sparse count |
| --- | --- | --- | --- | --- | --- |
| FX hourly | 6 | 720, 2880 | 11927 through 18551 | 6625 | 947 |
| FX hourly | 24 | 720, 2880 | 11927 through 18551 | 6625 | 265 |
| Treasury weekly | 6 | 52, 260 | 405 through 681 | 277 | 40 |
| Treasury weekly | 24 | 52, 260 | 405 through 681 | 277 | 12 |

Each row represents two windows and seven methods. FX units are USD; Treasury units are USD millions. These distinct financial quantities must not be pooled. The frozen nominal tail/coverage convention is tau=19/20. A report with that nominal preference is not thereby an established conditional quantile or a distribution-free coverage guarantee.

## Identities and metadata actually checked

The original successful replica controller reports `REPLICATION_AUDITED`, 32 completed evaluation/reference jobs and the original executable freeze SHA-256 `e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb`. Its selected-parameter artifact is SHA-256 `05b9714aa689875e3b946210075bb8bbf5f23e795e28f9410b6b259b5230b1eb`; this is the fresh replica selection receipt, not the original archived selection hash `531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7`.

The fresh AR manifest is SHA-256 `709b5418f37f0abca7e4d9834aa2f3a865b6e37bb79969209aaf577a74139876`, with `AR1_REPLAY_COMPLETE`, eight complete cells and no failed cell. It binds AR specification `e9f40722e4b012b57a0eb0158d101b5bf6cd327586ced6e270d822adf4f8a9a2`, AR freeze `57a880384d1a978f4f37b18eeaed1716b21db1f48b88c1375a7b5348c5421261`, the original freeze/selection and the fresh selected-parameter receipt. The genuine version-2 independent readback is `results/revision-20261022/ar1-fresh-reproduction/inventory-readback.json`, SHA-256 `9cfe4a471d27378d973dc83cef4e27b816a09825a13aa8c93b076ee87256b9ae`; its complete-export binding and manifest identity were checked. This metadata review does not rerun that numerical readback or reinterpret its score results.

Across all 24 conditional, eight reference and eight AR trace containers, **40 NPZ hashes and 588 NPY headers** were checked. The header count includes unused rolling/one-state members of reference containers, because each container's complete header inventory was checked rather than ignoring unexpected members. Conditional/reference array names are `<method>_origins`, `<method>_peak`, `<method>_floor`, `<method>_refit_indices`, `<method>_capacity`, and `<method>_pinball`. AR has the same six unsuffixed field names. Every header is one-dimensional with the source's declared full-origin count, C order, int64 for origins/refit indices and float64 otherwise; ZIP entry/header/data byte counts and unencrypted unique member names matched. The `.npy` payloads were not loaded, and no comparison of peak with capacity was made.

Original queue/worker manifests were bound by exact receipt SHA, source/H/W/family, terminal COMPLETE/no-stop status, source identity and selected parameter. Each conditional parameter matches the fresh selection artifact. Reference family is null and its chosen labels are exactly frozen F/S/K, not similarly named rolling or one-state reports. Fresh AR cell receipts bind source/H/W, method, exact expected/completed origin counts, source identity, both new specification/freeze hashes and each consumed private trace's bytes/hash.

## Fail-closed contract for a later authorized auditor

1. Fix the exact 56 semantic keys before computing the new diagnostic. Check unique keys and full label/parameter/unit binding; row counts alone do not rule out a duplicate or omitted method. Do not silently substitute an older first AR attempt for the named fresh attempt.
2. Reverify both original frozen contracts, the explicit successful replica controller/selection/queues, the new AR specification/freeze/manifest, the genuine version-2 readback and all consumed receipt/trace hashes. Use nonsymlink bounded project paths and reject changes between initial consumption and final readback. The original and fresh selection hashes intentionally differ as receipts; require the documented parameter/status agreement rather than equating their bytes.
3. Reuse the read-only context boundaries in `run_ar1_replay.prepare_replica` and `verify_execution` where appropriate; neither refits a model. Do not call the older `reproduce_conditional_diagnostics.prepare` merely to obtain context on a replica with an already completed diagnostic output, because its existing-output lock intentionally refuses that reuse. Do not remove an output directory, construct a fake replica or weaken the lock.
4. The header checks in `reproduce_conditional_diagnostics._check_trace_headers` and the AR checker must precede any future `np.load(...,allow_pickle=False)`. Actual payload checks would still be required later: exact chronological origin arrays, finite reports/targets/floors, matching refit indices, source/H-specific target binding and current floors. Header shape is not proof of those values. Hash-bound earlier readbacks are provenance, not a fresh recomputation in this metadata-only review.
5. A coverage diagnostic needs only the declared report, target and origin alignment. Pinball arrays or CSV summary scores must not become an undeclared selection or repair channel. Any late diagnostic code/specification requires its own dated before-computation freeze; none of this changes original forecasts, parameter choices or primary comparisons.

All later statistics would be **post-result diagnostics on inspected archives**, not a restored unseen holdout or prospective registration. Nonsharing H+1 response windows do not establish independent hits: histories, refits and the financial series remain dependent. Whole-family multiplicity and dependence assumptions need a separate mathematical design, including the effect of choosing this subset after earlier results were visible. A newly dated freeze alone does not remove that selection history. The Treasury economic-date/current-position convention also remains hypothetical relative to the public-release filtration; metadata completeness does not turn it into a live released-vintage backtest. This note establishes input feasibility only.
