# Verification loop 037 — preserved methods definition audit and corrected empirical numeric trace

This is same-model internal source/display verification, not external peer review, a new proof, a new financial analysis, independent replication, or completion of the six-hour revision goal. Only this note and `verification-loop-037-method-numbers-selection.json` are written.

## Scope correction and complete preservation

The initial assignment explicitly allowed “numerical/definition propositions” from all 35 blocks of current main Section 4, “Target and forecasting methods.” That produced a **47-proposition definition/setting frame**, frozen with seed `2026102337` at **2026-10-23T22:33:21.035405+00:00**, and draw indices **[29, 4, 39, 24, 35]**. The five entries concern training versus issued projection; peak/floor/headroom; full-pool KNN identity; past-increment RMS; and the Treasury W260 neighbor menu.

**Initial scope gap: this is a bounded definition audit and does not supply five actual empirical numeric result-to-output traces.** The root then explicitly corrected the scope: preserve the original frame, seed, draw, timestamps and every record, and separately freeze a current-Table3 empirical-cell fallback. This correction is about the kind of evidence required, not an unfavorable result or result-driven resampling.

The companion JSON nests the entire original record under `initial_definition_audit`. Its original file-byte SHA-256 was `065375250b3ceb2464b12e5b5623b4d179cc706922ef6a400bad56ead8e27ca0`. Reserializing that preserved nested record using its original JSON encoding reproduces **the same SHA-256**, observed at `2026-10-23 22:37:39 UTC`. No original frame entry, draw or timestamp was deleted, replaced or hidden. The JSON separately records the correction authority, fallback frozen frame and current trace readback. A frozen `output_lookup_started:false` field describes its historical freeze time, not the later completed lookup status.

## Timing and current source identity

- Checkout: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`; observed branch supplied/current task: `revision-v4-jof`.
- Initial and latest observed HEAD: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`.
- Initial clock observation: `2026-10-23 22:31:25 UTC`.
- Initial definition selection freeze: `2026-10-23T22:33:21.035405+00:00`.
- Corrected fallback selection freeze: **`2026-10-23T22:36:07.749009+00:00`**, before the new owning empirical result-field lookup.
- Fallback saved-field/display readback recorded: `2026-10-23T22:37:10.241698+00:00`.
- Latest pre-note source/HEAD/preservation readback: `2026-10-23 22:37:39 UTC`.
- Note written: `2026-10-23T22:38:35.832560+00:00`.
- Goal deadline supplied by root: `2026-10-24T00:31:50Z`; no goal-status, state or ledger action is taken.

The main JSON, article TeX and PDF hashes match the supplied fingerprints throughout. The article is `manuscript.tex`; the PDF was hashed only and this pass makes no rendered-PDF claim. The final companion JSON SHA-256 at this note's write is `c2446572e0d8028f2bce6051306afb4c1986d15461ce387d192d57030e72b5b8`.

## Initial bounded definition audit — not counted as five numeric traces

All 35 current Section 4 blocks were read directly. The ordered frame merges equivalent overview/prose/formula occurrences while retaining their pointers. Navigation/bibliographic identifiers and repeated proof steps were not extra lottery entries. The previously selected 33-coordinate/lag-span claims from loop021 and 640/6625 crossing claim from loop013 were excluded; prior selected-claim metadata was routing only. Seed `2026102337` selected the five entries listed above before current owning protocol/formula lookup.

Their bounded definition readback was consistent:

1. The QR training objective uses unconstrained affine normalized headroom, while report issuance/validation applies the nonnegative projection and validation uses source-native units. This matches the frozen design, working-paper paragraph, v3 objective/issued-report formulas and frozen v5 text.
2. `B=|N_t|`, `P=max_(0≤h≤H)|N_(t+h)|`, `G=P−B≥0` match the frozen design and original v3 formula. The start observation remains included; these are forecast amounts rather than cash allocations.
3. Plain `k=W` KNN is defined as frozen F **under the same mature pool, corrected rank and arithmetic**; scaled KNN retains response normalization and is not assumed to collapse. The frozen design states this identity explicitly. This is a definition/premise trace, not new pointwise report-vector verification or a new proof.
4. The past-increment RMS formula with range `j=t−L+1..t`, `L^−1` normalization, squared increments and outer square root matches the provenance-linked v3 formula and frozen v5 formula. It remains a position-increment quantity in source units, not price/yield volatility.
5. The Treasury W260 neighbor **menu** is `{40,80,160}` in the frozen protocol. The menu is distinct from the selected neighbor counts in Table S2 and from a probability level or order-statistic rank.

These observations do not discharge the corrected five-empirical-trace requirement; that requirement is handled separately below.

## Corrected fallback frame and prior exposure

Root authorized current main **Table 3 empirical result cells**, JSON `/sections/5/blocks/0`, as the fallback. The frozen frame uses row-major/column-major order. Each displayed numeric cell is one claim; a displayed L/R pair stays one cell. Of 24 result positions, the two “Outside family” statuses are nonnumeric, and ten cells are conservatively excluded as identifiable prior selected cells/propositions. These include the five loop001 cells, original FX/Treasury percentage results previously selected elsewhere, matched FX breach results, and compound Kupiec pairs containing the FX H6 POF value selected in loop009. The complete exclusions and their reasons are preserved in the JSON.

The resulting frame contains **12 eligible actual empirical cells**, so there is no fewer-than-five fallback problem. With the same fixed seed, `random.Random(2026102337).sample(range(12),5)` gives draw indices **[7, 1, 9, 6, 8]** and cell IDs **[table3:r3:c1, table3:r0:c5, table3:r3:c3, table3:r2:c6, table3:r3:c2]**. This is a separate frozen frame, not a revision of the original 47-definition draw.

The current table's displays had been seen earlier and were read again to frame this fallback. In loop033, the paired-comparison and DM CSVs were parsed for FX H6/H24 identities and bandwidth fields; static authoring context was also read. Earlier selected-cell metadata exposes some display/source-field identities. **No claim is made that these files or display values were unseen.** The new empirical result-field lookup in corrected loop037 begins after the fallback freeze; the initial definition phase did not open the paired, DM or coverage result fields. Prior verdicts are not used as evidence.

## Five frozen empirical-cell traces

1. **`table3:r3:c1` — FX H24 legacy loss change `-1.83`: MATCH.** `results/revision-20261022/paired-comparisons.csv`, selector `contrast_id=fx_hourly-h24-QR2880-minus-rolling_S720`, field `relative_mean_loss_difference_percent` is **`-1.8290714567022697`**. Static `v4_submission.py` line 43 formats this existing percentage with signed fixed two decimals, producing **`-1.83`**. It is not recomputed from the two mean losses. Identity fields retain H24, QR W2880, rolling S W720, source unit USD, `h24_legacy_contrast=True`, and `declared_source_primary=False`.

2. **`table3:r0:c5` — FX H6 original-primary breach percentages `5.675 / 5.011`: MATCH.** The same saved CSV, selector `fx_hourly-h6-QR2880-minus-rolling_F720`, stores **`strict_breach_count_left=376`**, **`strict_breach_count_right=332`**, **`origin_count=6625`**. Static table formatter line 44 converts the saved counts/denominator to percent and displays fixed three decimals, producing **`5.675 / 5.011`**. Only that existing display conversion was applied; no counts were re-estimated from forecasts. This is the all-origin H6 QR versus original rolling-F comparison, not the matched frozen-F comparison and not a sparse-grid POF sample.

3. **`table3:r3:c3` — FX H24 legacy HLN p `0.839`: MATCH.** `results/revision-20261023/inference/dm.csv`, selector `fx_hourly-h24-QR2880-minus-rolling_S720`, field **`hln_p=0.8390894089762104`**. The static `.3g` display at `v4_submission.py` lines 42–43 gives **`0.839`**. The saved row has H24, `n=6625`, category `h24_legacy_contrast` and status `OK`. The archived inference protocol identifies this as the Student-reference HLN p with approximate pinball use. It is not a Holm-adjusted or selection-adjusted value.

4. **`table3:r2:c6` — Treasury H6 Kupiec p pair `0.00413 / 0.199`: MATCH.** `results/revision-20261023/inference/coverage.csv`, left selector `(source=nyfed_weekly,horizon=6,window=260,method=QR)`, field **`pof_p=0.004126046248434382`**; right selector with `method=frozen_F`, field **`pof_p=0.1986410814587244`**. Static `.3g` p-value formatting and L/R joining at lines 40–44 yield **`0.00413 / 0.199`**. Both saved rows specify **`n=40`** and **`grid_stride=7`**; their saved sparse-grid hits are 7 and 4. These are the fixed H+1-grid POF p-values, not the 277-origin breach percentages, transition-independence/CC p-values, full-sample DQ p-values, or S16's different CC likelihood. No LR statistic or p-value was recomputed.

5. **`table3:r3:c2` — FX H24 legacy DM p `0.839`: MATCH.** The same named DM row stores **`dm_p=0.8385182122097816`**. Static `.3g` display gives **`0.839`**. This is the two-sided normal-reference DM field. It is a different saved field and reference from the HLN value in trace 3 even though both round to the same displayed string. Neither equality of the displays nor nonrejection establishes equal forecast performance.

All five displays match their sampled current cells. Machine-readable raw scalar fields, exact selectors, format descriptions, expected/reformatted displays and source hashes are appended in `fallback_trace_readback` in the companion JSON. The saved mean-loss percent, p-values and breach counts were not regenerated. Applying the already specified table percentage conversion and decimal/significant-digit formatting is the only result-number conversion performed.

## Source hashes and exact read boundary

| File | Observed SHA-256 |
| --- | --- |
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `protocol/revision-20261022/study-spec.json` | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |
| `protocol/revision-20261022/conditional-baseline-design.md` | `bdede74b2394a8dfb149c0671015bbb419609229779ca31b664f9b1756629725` |
| `notes/revision-v6/v5-manuscript-before.json` | `2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7` |
| `manuscript/revision-v3/paper-content.json` | `3a35590321c752186ab6dbfb46d115b725cdad3528b0dae73cf2c209f555dcb7` |
| `manuscript/working-paper/paper-content.json` | `6d06f8cb3fa429601967d7ab847da975f04d262b97e5091b4ec72d01faa2927f` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `v4_submission.py` | `11725bfe7c8922fb08ad8c6acb579bf53f890ab82967c52368c5f1f589022852` |
| `results/revision-20261022/paired-comparisons.csv` | `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9` |
| `results/revision-20261023/inference/dm.csv` | `0e8aa499fab31a5928be0ccb9198d5f6ee2833a01410a17fc965985bb65f5e41` |
| `results/revision-20261023/inference/coverage.csv` | `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419` |
| `results/revision-20261023/inference-design.md` | `31353e0470d744c9adccb7a5130935542cdce1ccc4f993fc09951a2a5e8d59cf` |

Initial substantive scope: current main Section 4 all 35 JSON blocks; current source metadata for blocks 3, 10, 13, 14, 15, 19; article TeX selected lines 113, 130, 137, 140, 143, 152 within the located Section 4 range 88–183; complete frozen study-spec and conditional-baseline design; frozen v5 methods blocks 3, 10, 13, 14, 15, 19; original v3 section 3 blocks 2, 9, 13, 14, 18; working-paper section 3 block 12. Current Supplement text read: S1 blocks 1, 13 and full Table S2 at block 5; S4 blocks 0, 1, 2, 9; S5 blocks 2, 3, 14, 16. S1 Table S10 caption/count were routed, not its rows. Prior selection metadata for loops013/021/033 was read for the initial duplicate exclusions. Existing proof prose was encountered in the required 35-block read but no proof was checked or generated.

Fallback scope: current Table 3 complete displayed rows/caption/headers; prior loops001/005/009 record identities/displayed fields and loop013 selected-claim routing; static `v4_submission.py` lines 1–48 and its targeted table-search context through line 76; complete archived inference-design Markdown; the two named paired-comparison scalar rows, the named FX H24 DM scalar row, and the two named Treasury H6 coverage scalar rows above. Current main/PDF/TeX and source hashes were read. No other result family was calculated or rescored.

No `.scratch`, raw-data file, private origin vector, coefficient vector or forecast trace was opened. No financial routine, mean/loss/inference estimator, model, test, proof check, network/UI action, installation, deletion, source/result edit, state/ledger update, commit or nested agent was performed. Directory/path routing and current HEAD were read. The only writes are the two authorized loop037 files; updating the JSON preserves the complete initial record and appends the transparent correction/fallback record.

## Verdict and limit

**Initial phase: bounded definition audit only, with the empirical-trace scope gap explicitly retained. Corrected fallback phase: all five frozen actual empirical cells match their saved source fields and existing display rules.** No necessary numerical correction or conclusion-level problem is identified by this corrected sample. No conclusion edit is applied; a later necessary conclusion change remains author-pending under the work-package restriction.

The result is a source/display trace with declared prior exposure. It is not fresh financial computation, an audit of every table cell, proof validation, confirmation of asymptotic reference assumptions, selection-adjusted inference, unseen-dealer replication, prospective validation or submission readiness. Rank versus target level, mature-pool/anchor conditions, source-native units, method/control identity and full-sample versus sparse-grid meaning are retained. The six-hour goal remains active for root to manage through its stated deadline.
