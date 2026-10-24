# Verification loop 045 — five actual reported coverage-result cells

This loop performs only the v6 plan §3 first-type random five-number source/display trace. It does not use method definitions, formulas or literal protocol settings to fill the sample. Only this note and `verification-loop-045-result-numbers-selection.json` are written. No financial statistic, forecast, model, test or proof is recalculated.

## Actual time and source identity

- First real clock observation: **2026-10-23 22:43:33 UTC**, before the target hashes and frame were read.
- Initial observed HEAD: `d2589d6a865ccb90484dcf716371798068fd896c` on the assigned `revision-v4-jof` checkout.
- Seed/frame/draw frozen: **`2026-10-23T22:44:32.129497+00:00`**, before owning result-field or actual formatter lookup in loop045.
- Five-field display readback recorded: **`2026-10-23T22:46:04.723318+00:00`**.
- Latest pre-note clock/source observation: **2026-10-23 22:46:20 UTC**; observed HEAD then `989ca3b0dcc9d81bef58129b98f83373bfcadeaf`. HEAD progressed during parallel work; the assigned main JSON/article TeX/PDF hashes remained identical. No cause of unrelated commit movement is inferred here.
- Note written: `2026-10-23T22:47:29.475308+00:00`.
- This is a bounded internal trace and does not mark the six-hour goal complete; the parent retains its deadline/status management.

The current main JSON is `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`, article `manuscript.tex` is `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`, and PDF is `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` at both target observations. The PDF was hashed only, not rendered.

## Complete eligible frame, prior selections and exposure

Permitted current Table 4 and Table 5 displays were first inspected. Table 4 has six empirical numeric cells, five already selected in loop005; only one remains there. **Table 5 was explicitly chosen as the sampling scope before the draw**, rather than enlarging a deficient frame after seeing results.

The Table 5 scope is current JSON `/sections/6/blocks/0`: seven reports, each with one observed `k/n` cell and four reported diagnostic-p cells, totaling **35 actual empirical result cells**. These observed count/denominator results are not count settings. All cells were enumerated in document row order and numeric-column order. Distinct report/test identities remain distinct even where displayed strings coincide.

Ten identifiable prior selected cells were removed before sampling: the five selected in loop009 and the five selected in loop041. The two Treasury POF cells were also identified as having appeared in loop037's corrected Table3 POF pair; they were already excluded through loop041 and are not counted twice. Exact prior cell IDs, displays, source-routing metadata and hashes are in the frozen JSON. Loop005's Table4 selections are separately recorded. No prior verdict is used as current source evidence.

This leaves the **complete 25-cell eligible frame**, fully listed in the companion JSON and printed before source lookup. The fixed seed is **2026102345**. `random.Random(2026102345).sample(range(25),5)` draws **[24, 15, 16, 9, 2]** in draw order:

1. `Table5|Treasury F H6|CC p` — `0.277`
2. `Table5|FX legacy S H24|POF p` — `0.339`
3. `Table5|FX legacy S H24|CC p` — `0.0855`
4. `Table5|FX matched F H6|POF p` — `0.807`
5. `Table5|FX QR H6|CC p` — `0.638`

The 25-cell frame is sufficient; no fallback, definition/formula substitution or post-result resampling is used. Its frame hash is `aea2e29528d003fd12a8f6e836eb9143b4a140bbdb752769875f72770605d138`. The initial frozen JSON file hash before trace append was `a0b7adf70f5253a7848b193255eaa1879f699774a5d5c02ef2e75856814422eb`; the frame, seed and selected cells remain unchanged in the final JSON.

**Prior exposure is explicit.** Table displays were known in earlier tasks and in this frame read. The coverage CSV was parsed in loop037, and its two Treasury H6 QR/frozen-F scalar rows were previously read; the current Treasury F CC value was therefore exposed earlier even though it was not a prior randomly selected cell. The fresh loop045 owning-field lookup occurs after the freeze. This is not a claim of previously unseen values or a blinded experiment.

## Owning output and actual display chain

The owning saved script output for all five selected cells is **`results/revision-20261023/inference/coverage.csv`**, SHA-256 `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419`.

The actual numerical formatter is **`v3_additions.py` line 12**:

`'NA' if x in (None,'') else format(float(x),'.3g')`

Its lines 23–26 bind each report label to an exact source/horizon/window/method selector. Line 27 takes `pof_p`, `ind_p`, `cc_p`, `dq_p` directly and applies that formatter; the count display is the saved `hits` and `n` joined by `/`. The module was read as static authoring text and was not imported or executed. Only the selected scalar `.3g` conversions were applied.

The publication chain was also read: frozen v5 Table 4 points to `manuscript/revision-v3/paper-content.json` `/sections/7/blocks/8`, whose selected rows match the present values. Current v6 re-labels that coverage table to Table 5 via `v6_submission.py`'s table-label remapping, without changing those numeric strings. Current article TeX lines 266–280 contains the displayed Table 5; selected report rows are lines 272, 274, 276 and 278. Generic current v6 binding paths were routed without opening every referenced file.

## Five source-field/display results

1. **Treasury F H6, CC p — MATCH.** Selector `(source=nyfed_weekly,horizon=6,window=260,method=frozen_F)`; direct saved field **`cc_p=0.2768409873964233`** formats as **`0.277`**. The row retains `n=40`, `hits=4`, `grid_stride=7`, `first_origin=405`. It also retains **`ind_status=BOUNDARY_REFERENCE`, `boundary=True`**. This warning is not removed or promoted into an ordinary validated reference distribution. The F identity is frozen W260, not rolling F.

2. **FX legacy S H24, POF p — MATCH.** Selector `(fx_hourly,24,720,rolling_S)`; field **`pof_p=0.33918013842732714`** formats as **`0.339`**. The row retains `n=265`, `hits=10`, `grid_stride=25`, `first_origin=11927`, `ind_status=OK`, `boundary=False`. It is the original rolling-S H24 legacy control; it is not H6, QR, or the matched frozen-F control.

3. **FX legacy S H24, CC p — MATCH.** Same exact selector, but the distinct saved field is **`cc_p=0.08554314109839081`**, formatting as **`0.0855`**. Its POF and CC values are kept as separate diagnostic fields. No LR statistic, p-value or combined reference was regenerated.

4. **FX matched F H6, POF p — MATCH.** Selector `(fx_hourly,6,2880,frozen_F)`; field **`pof_p=0.8067032386212847`** formats as **`0.807`**. The row retains `n=947`, `hits=49`, `grid_stride=7`, `first_origin=11927`, `ind_status=OK`, `boundary=False`. The same display `0.807` also appears for original rolling F W720, previously selected in loop041, but that is a different report selector. Here the matched frozen W2880 identity is retained; equal strings do not authorize substitution.

5. **FX QR H6, CC p — MATCH.** Selector `(fx_hourly,6,2880,QR)`; field **`cc_p=0.638050193956863`** formats as **`0.638`**. The row retains `n=947`, `hits=50`, `grid_stride=7`, `first_origin=11927`, `ind_status=OK`, `boundary=False`. This is the selected long-history QR report; the diagnostic is not itself an original-versus-matched paired equal-loss test.

All five saved fields are present and finite; all five exact existing formatter results match the frozen displayed cells. **There are zero lookup failures, missing/NA substitutions or display mismatches.** Machine-readable raw values, selectors, fields, grid metadata, retained boundary/status fields, source hash and expected/reformatted strings are appended to the companion JSON. Its `output_lookup_started:false` value is preserved as the initial freeze-time snapshot; the appended trace records the later lookup.

## Grid, test and NA meanings retained

The current caption and archived `inference-design.md` B3 define these POF/independence/CC results on the fixed `first_origin+j(H+1)` grid. The sparse-grid samples here are 40, 265 and 947. The legacy CC convention adds full-**grid-n** Kupiec POF LR to transition-independence LR; it is not full-all-origin POF and is not S16's separately stated transition-conditional CC likelihood. DQ is a different full-sample HAC adaptation; its `dq_n` values were read as context but are not used as the denominator or field for these five cells.

The formatter preserves a missing/empty field as `NA`; it does not replace it with a numeric p-value. An unidentified transition row or failed reference would remain a status/NA problem rather than be dropped or retried. None of the sampled fields is NA, while the Treasury F boundary warning remains explicit. These are post-result/exploratory reference p-values under their stated finite-sample/dependence qualifications, not conditional-coverage certification or selection-adjusted confirmation.

## File identity and bounded operations

| File | Observed SHA-256 |
| --- | --- |
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `results/revision-20261023/inference/coverage.csv` | `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419` |
| `v3_additions.py` | `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525` |
| `v6_submission.py` | `9f4984fc802f8a2e1375760d78cbe59ae04aa814bb83114d6707b70ac01b61c8` |
| `manuscript/revision-v3/paper-content.json` | `3a35590321c752186ab6dbfb46d115b725cdad3528b0dae73cf2c209f555dcb7` |
| `notes/revision-v6/v5-manuscript-before.json` | `2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7` |
| `results/revision-20261023/inference-design.md` | `31353e0470d744c9adccb7a5130935542cdce1ccc4f993fc09951a2a5e8d59cf` |

Read scope: current main Table4 and Table5 displayed payloads; selected-cell metadata from loops005/009/041 and known loop037 routing; current Table5 provenance; the four exact saved coverage rows needed by the five sampled fields; actual formatter/selector lines 1–28 of `v3_additions.py` and targeted surrounding search context; v6 label-remap lines 23–47; frozen v5 coverage-table metadata; original v3 coverage-table selected rows; current TeX Table5 and its returned immediate context; complete archived inference-design text. Initial narrow authoring-source searches returned no matching coverage literals before the actual `v3_additions.py` formatter was located; this was routing, not a failed numerical result. No code path named in those sources was run.

No `.scratch`, raw input, private origin vector, model coefficient vector or forecast trace was opened. No new mean, variance, statistic, p-value, coverage count, financial forecast, model, test, proof, network/UI request, Claude/Cloud call, package installation, deletion, source/result/manuscript edit, state/ledger change, commit or nested agent was performed. Hashing, deterministic sampling, direct saved-field lookup and the exact `.3g` scalar display conversion are the only computational work. Only the two authorized loop045 note files are written.

## Conclusion

**The five randomly selected actual empirical result cells match their saved script-output fields and actual display formatter.** Method identities, original versus matched controls, sparse versus full-sample meanings, post-result status and the observed boundary warning are retained. No numerical correction is indicated by this five-cell sample; it does not validate the reference assumptions, prove coverage or replication, audit every result, change conclusions, or complete the six-hour goal.
