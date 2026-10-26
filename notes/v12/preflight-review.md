# v12 preflight scientific integration review

Review timestamp: 2026-10-25T11:12:48.590281+00:00. Scope: frozen F1/F2/F3 protocols and `v12_inputs.py`, `v12_forecast.py`, `v12_decomposition.py`. This review did not inspect the pending runner or launch a financial study. Only this note was written. No actual financial observations were read by the reviewer; the permitted existing toy tests use constructed observations and read saved protocol/selection metadata for grid checks.

The reviewed helpers have **no confirmed core scientific contradiction with the frozen protocols**. Their passing toy tests do not establish that the pending runner supplies complete declared operands, enforces once-only failures, or preserves resource decisions. Those are explicit integration obligations below, rather than defects inferred in code that has not yet been reviewed.

## Confirmed scientific checks

| Topic | Evidence and consequence |
|---|---|
| F1 original source grid | `v12_inputs.py:286-294` uses protocol geometries without shortening H6 to a horizon-specific buffer. CFTC remains validation 553..604 / evaluation 611..870. Panel and bill remain 329..380 / 405..681. FX original remains 10463..11902 / 11927..18551. Counts remain 90 source cells and 180 QR method cells. |
| H24 buffer and last labels | For panel/bill, 380+24=404<405 and 681+24=705=N706-1. For original FX, 11902+24=11926<11927 and 18551+24=18575=N18576-1. The same 24-record original buffer remains for their H6 rows; it is not compressed to six. Geometry is read from F1 at protocol lines 407-504 and materialized at `v12_inputs.py:255-265,286-294`. |
| Panel706 | Protocol panel CSV metadata has 707 raw rows while the original grid has N706. `v12_inputs.py:190-210` maps by exact date onto the verified Treasury grid, rejects missing required dates, and verifies final N. The extra raw observation cannot extend the experiment. No interpolation or forward fill occurs. |
| F2 histories and clocks | `v12_inputs.py:295-305` gives evaluation 611..870 for both V values; V52 is 553..604 and V156 is 449..604. The 104-record difference is exactly 8 times d13. Earliest V156/W260 training origin is 449-6-260+1=184, above feature prefix26. `eligibility` at lines 228-242 has the protocol threshold N>=719. |
| F3 fixed periods | `v12_inputs.py:307-326` prioritizes .99, then .90, and preserves 37 cells per tau: 34 CFTC, both original and early2015 FX H6/W2880/d24, and bill H6/W260. Early2015 validation7535..8974 / evaluation8999..10438 retains the original 24-record buffer. |
| Tau rank cap | `v12_forecast.py:90-104` computes one-based ranks by exact rational integer arithmetic: F=min(W,ceil((W+1)tau)); I=ceil(W tau). At W52/.99 both are rank52. This is exactly the F3 declared saturation convention, not a coverage claim. Other tau values are passed into the unchanged quantile solver at lines176-178. |
| Forecast/scoring equivalence | At .95, finite and infinity QR reports delegate unchanged at `v12_forecast.py:134-148`. The generic finite loop at lines150-201 preserves mature pool, QR33 transform, copied QR4 column/reduction arithmetic, response scale, solver defaults and nonnegative headroom projection, matching `v8_mechanism_mc.py:115-169`. `score_report` calls the frozen exact-decimal `pinball_losses` and `stable_mean` at lines217-225; strict breaches use error>0. It does not use binary 1-tau for the complementary loss weight. |
| Finite oracle, signed S | `v12_decomposition.py:55-78,113-138` requires all six complete candidate records; oracle index is selected from range(5), excluding infinity. Raw selected infinity may beat every finite candidate, so S remains negative. F<=0 or a nonfinite reference makes all relative components unavailable while retaining valid raw actual/oracle means. |
| Fixed prediction denominators | `v12_decomposition.py:151-162,196-213` makes 41 pinned source/H slots separately for QR33 and QR4. E<=0 is complete D2 nonsupport; G>0 and S>E/2 remain strict. Missing, failed and duplicate slots contribute uncertainty without shrinking41. D3 at lines165-183 requires both original FX W2880 H6/H24 negative, with a complete nonnegative G decisive against support and resource omissions explicitly NOT_EVALUATED. |
| Group summaries | Percentages remain grouped by family, period, H, W and method. Original planned180 remains visible even with missing rows. Component medians are computed independently; no pooled native-unit loss or independent-series combined test is introduced. |

## Real documentary contradictions to avoid propagating

The preliminary audit notes predate the frozen scientific decisions and must not override them:

1. `notes/v12/model-api-audit.md:93` and `notes/v12/split-design-audit.md:207-210` describe D3 as H6 primary with H24 separate. Frozen F1 explicitly replaces that with a conjunction over **both** horizons (`protocol/v12/loss-decomposition-design.md:7,521-522`). The current decomposition implementation follows the frozen conjunction correctly. A report/runner copied from the preliminary notes could restore the wrong criterion.
2. `notes/v12/model-api-audit.md:17` and `notes/v12/split-design-audit.md:120-121` describe inherited QR4 selection from completed candidates after other validation failures. Frozen F1/F2/F3 each require all six complete for **both** QR procedures (F1 line392 and candidate computation506; F2 line430; F3 selection section). The current v12 selector correctly enforces all six. The old `v10_menu.select_candidate` must not be used for v12 selection just because the forecasting adapter reuses `v10_menu.forecast_report`.

These are documentation conflicts, not newly observed failures of the reviewed helpers. No historical file was changed by this review.

## Runner integration obligations still open

1. **Freeze F2 eligible K after source verification and before any model.** `f2_eligibility_inventory` (`v12_inputs.py:245-252`) intentionally checks pinned metadata and the history formula only; it does not parse/hash/validate the financial source. Frozen F2 line429 additionally requires the full source fingerprint/complete-grid checks before whole-contract eligibility is final. `load_series` performs those checks when called. A late source failure must not silently become a solver failure after K was reported as fully eligible, nor may a later solver failure remove a contract from K.
2. **Bind the whole declared segment at the runner boundary.** `_origins` (`v12_forecast.py:38-47`) rejects empty, gapped, noninteger and out-of-range vectors but cannot recognize a uniformly truncated consecutive segment. `score_report` only knows the supplied vector. `select_candidate(expected_n=...)` can enforce the declared validation count; `decompose` verifies equal positive counts across the supplied six but has no declared evaluation count argument. Before marking COMPLETE, compare report origins with the exact protocol-derived segment, check score n against that segment for every candidate and F/I, and pass declared validation_n to the selector. A subset must never become a complete mean.
3. **Scope F1 criterion input to F1.** `evaluate_predictions` filters family/source/period/H/W/method, but its established row API does not require experiment/tau/V and therefore cannot distinguish F2/F3 rows with matching geometry. Pass only the 180 planned F1 method rows. Mixing experiments can either create unavailable duplicates or let a foreign row occupy a missing F1 slot. Call the grouped summaries with the matching experiment scope as well.
4. **Once-only full-method failure and exact cache identity remain driver responsibilities.** Forecast exceptions propagate and no fallback exists in the adapter; the selector/decomposition reject required incomplete records. The pending runner still must persist failed identical attempts as terminal, avoid retry through another phase/method alias, seal selection before evaluating it, validate source/code/tau/H/W/d/origin fingerprints on reuse, and retain unattempted resource omissions separately. F1 requires the complete five-finite-plus-infinity evaluation menu; F2/F3 require all six validation candidates but evaluate only the selected candidate. These are different workloads.
5. **Use protocol execution order/resource ladder, not raw grid iteration as a scheduler.** `cells_for` is a full scientific inventory. Its F1 inventory groups all panel W values before bill, while the frozen formal queue delays panelW260 until after bill and omits all FX before panelW260 when projections demand it. The pending scheduler must apply the frozen queue and recorded pre-launch reductions; preserve all planned slots and F4 reserve. F2 V1 is the difference of same-K cross-contract medians, rather than the median of paired differences, and a missing required eligible pair makes its W criterion undetermined. F3 Q1 retains denominator34 and Q2 is a both-period conjunction. None of those F2/F3 decision screens is implemented by the reviewed F1 decomposition helper.

## Existing toy verification

Command:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest==9.1.1 --with numpy==2.3.5 python -B -m pytest -q -p no:cacheprovider test_v12_inputs.py test_v12_forecast.py test_v12_decomposition.py
```

Observed exit0: **132 passed, 3 subtests passed in 6.71s**. These are existing constructed-data tests; no financial pilot, target evaluation or model fit was launched. The uv runner emitted only its known `--no-project` notice. A complete project test suite and runner integration review remain outside this bounded preflight task.

## Reviewed bytes

| Path | SHA-256 |
|---|---|
| `protocol/v12/loss-decomposition-design.md` | `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1` |
| `protocol/v12/validation-length-design.md` | `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819` |
| `protocol/v12/tau-design.md` | `366c56a57983cbe8c9569abf626f2d5947166b66fd0a2ca2fa23a444dcd8943c` |
| `v12_inputs.py` | `819087f0055fae722f9870378246d8e1dd7c45ecbe1484ef23d1fef21b7c8e0b` |
| `v12_forecast.py` | `d893d3cd6ba5542fbd5dfd2be95c1c8f9d4060eefa53b25e0490a2f938b2b3ef` |
| `v12_decomposition.py` | `e9df96e98954e287cabf30ae003474d633b565f8e72be2a641c4680a8b3006bf` |
