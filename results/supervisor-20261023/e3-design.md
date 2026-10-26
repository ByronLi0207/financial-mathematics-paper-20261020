# E3: common ridge menu, frozen before new computation

Declared 2026-10-23. This is a post-result exploratory comparison requested by the supervisor. It does not replace either archived primary comparison. Original source code, specifications, outputs and the actively edited prior checkout are read-only.

## Question and estimands

The previous four-predictor QR used the menu `{0.001, 0.01, 0.1, 1, 10}`; the original 33-predictor QR used `{0.001, 0.01, 0.1}`. Therefore their previous difference jointly changed the predictor specification and the tuning menu. E3 reruns the existing 33-predictor QR with the larger menu in all eight source/horizon/history cells. No new model or series is admitted.

Three comparisons will be retained for every cell: original 33-predictor versus expanded-menu 33-predictor (menu change); four-predictor versus expanded-menu 33-predictor (different predictor sets under the same tuning procedure); and historical frozen F versus each specification. The common-menu comparison allows each feature set its own validation-selected penalty. It is not a fixed-penalty or causal effect of individual features.

## Unchanged scientific and numerical choices

The owning sources are `protocol/revision-20261022/study-spec.json`, `conditional_study.py`, `conditional_features.py` and `conditional_quantile.py` at public main `65feeee`. Every validation and evaluation origin, completed-label fit pool, refit block, response scale, training-only feature transform, projected capacity, 0.95 pinball score and ADMM/Fenchel acceptance check is unchanged. `conditional_forecast` is called directly for all new 33-predictor forecasts. The solver defaults remain max_iter=10000, atol=1e-6, rtol=1e-5 and gap_rtol=1e-6.

The declared candidate order is increasing lambda: 0.001, 0.01, 0.1, 1, 10. Selection uses the original `select_parameter`: lowest complete validation mean, exact ties resolved toward the larger lambda. Any failed or incomplete declared candidate makes the whole cell ineligible. Evaluation uses only the frozen selected lambda. Failed evaluation is not scored as complete, and no row, failed fit or candidate is dropped. All cells continue after another cell's failure. There are no favorable retries or changed tolerances.

The eight cells are Treasury H6/W52, H6/W260, H24/W52, H24/W260; FX H6/W720, H6/W2880, H24/W720, H24/W2880. Treasury validation 329:380, evaluation 405:681, refit step13; FX validation10463:11902, evaluation11927:18551, refit step24. Endpoint indices are inclusive.

## Existing four-predictor comparison

The read-only prior `parsimonious_v3.py` and eight existing JSON/NPZ pairs are reused after strict origin, peak, capacity, score and summary reconciliation and hash capture. Its four predictors, in order, are abs(N_t), N_t, short RMS, long RMS. All40 saved validation candidates have status COMPLETE and all five means in each cell are distinct. Its less strict failure filtering and first-on-tie implementation therefore did not alter any actual recorded selection. Each saved selection must additionally agree with the original strict `select_parameter` applied to those five rows. Failed verification will block that comparison; it will not be patched or guessed. These prior results are archival reuse, not a new independent rerun of four-predictor QR.

## Paired inference and ordered decomposition

Every difference is new loss minus old loss on exactly equal origin/peak arrays. Report the Newey-West Bartlett HAC DM normal reference and Harvey-Leybourne-Newbold adjusted Student reference. Primary bandwidth is min(n-1,max(H,floor(4*(n/100)^(2/9)))); sensitivity is min(n-1,2L). No iid resampling or independence claim is made. Inference is exploratory and separate from the fixed72 original matched contrasts.

For each horizon the FX ordered chain is rolling F720 -> frozen F720 -> frozen F2880 -> four-predictor QR2880 -> expanded-menu 33-predictor QR2880. Treasury chains at each H/W are frozen F -> four-predictor QR -> expanded-menu 33-predictor QR. Additional paired rows provide frozen F -> four-predictor (8), four -> expanded33 (8), and original33 -> expanded33 (8), plus FX update and history steps (2 each):28 declared comparisons. Holm values, if reported, adjust within these28 E3 comparisons only. This order-dependent sequential accounting is not a Shapley decomposition. Loss ratios multiply across steps; percentage changes are not summed.

## Resource budget and execution policy

The previous four-predictor eight-cell recorded elapsed times range0.345-54.004s; the longest history uses4 slopes while the full specification uses33. The original generic guard has540s internal/600s hard limits. Before any new fit, E3 declares a generous 3600s internal and3660s hard budget per cell: more than60 times the longest prior four-predictor cell, allowing the wider design and full five-candidate validation/evaluation. This is an E3-only resource limit, not a changed estimator or convergence threshold. Internal RSS is1.5GiB, hard reported ceiling2GiB, requested numerical threads1 and observed maximum2. Cells run serially, no software is installed, source raw bytes are hash/length checked before parsing, and all attempts and failures remain recorded. A resource stop is an incomplete cell, never a reason to choose a different penalty. If a cell reaches its declared limit, retain its trace and report the missing result without a new, favorable budget.

## Files, privacy and audit

Only new E3 scripts/tests, this design, and `results/supervisor-20261023/e3/` are authored publicly. Task-owned numeric traces and exact local source copies live in ignored `.scratch/supervisor-20261023/e3/`; they are not redistributed. The original FX licensing boundary is unchanged. Public JSON/CSV contain aggregate scores, parameters, per-refit convergence diagnostics, source/code/spec hashes, measured timing/RSS/thread counts and explicit status/reasons. Per-origin positions, peaks, capacities, losses and fitted coefficients stay private. Public aggregate CSV/JSON and an interpretation note retain all adverse and numerical results.
