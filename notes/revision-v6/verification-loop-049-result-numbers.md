# Verification loop 049 — five remaining actual Table5 result cells

Only the plan §3 random five-actual-result-cell source/display trace is performed. Method definitions, formula constants, literal protocol settings and newly computed statistics are not sampling units. The only writes are this note and `verification-loop-049-result-numbers-selection.json`.

## Actual clock, hashes and preserved selection

- First real clock observation: **2026-10-23 22:49:23 UTC**, followed by initial target hashes and the prior-selection metadata read.
- Initial and latest observed HEAD: `abe017800a156a11a57dc8f103d1998b908b65e1`; latest branch observation: `revision-v4-jof`.
- Frame/seed/draw frozen: **`2026-10-23T22:49:46.861802+00:00`**, before loop049 owning coverage-field/formatter lookup.
- Saved-field/display readback: **`2026-10-23T22:50:39.954672+00:00`**.
- Latest pre-note clock/HEAD observation: **2026-10-23 22:50:40 UTC**.
- Note written: `2026-10-23T22:51:39.913897+00:00`.
- The six-hour goal remains active through the parent's `2026-10-24T00:31:50Z` deadline; this note makes no goal-status update.

The initial main JSON/article/PDF hashes were respectively `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`, `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` and `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`; they remain the same at note creation. `manuscript.tex` is the article; the PDF was hashed only.

## Complete frame and prior exposure

Current main Table5 is JSON `/sections/6/blocks/0`: all **35 actual empirical result cells** (seven observed `k/n` cells plus four diagnostic-p columns on seven reports). Row and column identities are retained even when strings coincide.

Before the draw, the loop045 selection file was read **only for its ten original excluded cells and its five selected cells**, along with their IDs/displays and the file hash. Their union contains **15 unique prior-selected cells**. All 15 were excluded against the current table; every prior display still matches the current corresponding cell. This produces exactly the expected **20 eligible cells**, fully enumerated in document row/column order in the companion JSON and printed before lookup. `frame_issues=[]`; there is no count discrepancy, missing prior ID, changed display, insufficient frame or fallback.

Fixed seed **2026102349**, algorithm `random.Random(2026102349).sample(range(20),5)`, produced draw indices **[17, 8, 7, 19, 15]**:

1. `Table5|Treasury QR H6|DQ p` — `0.00891`
2. `Table5|FX matched F H6|CC p` — `0.647`
3. `Table5|FX matched F H6|k/n` — `49/947`
4. `Table5|Treasury F H6|Ind p` — `0.338`
5. `Table5|Treasury QR H6|Ind p` — `0.775`

The frozen frame hash is `002f7219feef3ab59060f2f3f1a44f41edcef563e47a4527c3c09b02d7b2377b`. The original frozen selection file hash before appending trace records was `86a3d45d3464a787434b23e83b03085a44bfc70a3e12204aaf7b6bc9033ae2a4`. Its frame, seed, draw and freeze time are unchanged. The final JSON only appends the later direct-field readback and preserves `output_lookup_started:false` as the historical freeze-time state.

**Exposure is transparent:** table displays and the coverage file were known from earlier work. Loop045 read FX matched frozen-F H6 and Treasury frozen-F H6 rows, including some then-unselected fields; loop037 read Treasury H6 rows, including the QR DQ/independence fields. The current sample therefore contains previously exposed but not previously randomly selected cells. No unseen-value or blinded-validation claim is made. Prior loop045 verdicts/raw values are not used as present source evidence; its selected/excluded IDs determine only the exclusions. Current owning fields are read directly after this loop's freeze, without favorable replacement.

## Exact owning fields and actual formatter

All five cells belong to the saved script output **`results/revision-20261023/inference/coverage.csv`**, SHA-256 `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419`.

The actual static formatter is `v3_additions.py` **line12**: `NA` for `None`/empty, otherwise `format(float(x),'.3g')`. Lines23–26 bind report labels to exact source/horizon/window/method tuples. Line27 reads each p field directly and formats it; it displays the observed count cell by joining saved `hits` and `n` strings with `/`. The authoring module is not imported or executed. Only these scalar display conversions/string joining are applied.

1. **Treasury QR H6, DQ p: MATCH.** Selector `(source=nyfed_weekly,horizon=6,window=260,method=QR)`, field **`dq_p=0.008908086546044377`** → `.3g` **`0.00891`**. The saved DQ metadata is **`dq_status=OK`, `dq_n=267`, `dq_df=6`, `dq_bandwidth=6`**. This is the full-issue-axis HAC DQ adaptation after its unavailable lags, not the row's separate sparse-grid `n=40`, `hits=7`, stride7. The effective DQ n is read, not derived anew.

2. **FX matched F H6, CC p: MATCH.** Selector `(fx_hourly,6,2880,frozen_F)`, field **`cc_p=0.6470566587146238`** → **`0.647`**. Its legacy sparse-grid metadata is `n=947`, `hits=49`, `grid_stride=7`, `first_origin=11927`; `ind_status=OK`, `boundary=False`. It remains the matched frozen W2880 reference, distinct from original rolling F W720. The stored legacy CC field is not replaced by the S16 transition-conditional likelihood or a DQ p-value.

3. **FX matched F H6, k/n: MATCH.** Same exact frozen-W2880 selector, saved fields **`hits="49"`, `n="947"`** → direct string joining **`49/947`**. No hits are counted from a vector and no ratio/rate is calculated. Original rolling F W720 also displays `49/947`, but its different selector is retained in the frame; equal text is not an instruction to substitute that control or merge these propositions. This is a sparse-grid observed result, not a training-window setting or all-origin breach count.

4. **Treasury F H6, Ind p: MATCH with retained boundary warning.** Selector `(nyfed_weekly,6,260,frozen_F)`, field **`ind_p=0.3384519174717687`** → **`0.338`**. Grid metadata: `n=40`, `hits=4`, `grid_stride=7`, `first_origin=405`. The saved **`ind_status=BOUNDARY_REFERENCE`, `boundary=True`** are retained. Display agreement does not remove that warning or validate its chi-square reference. This is frozen F, not rolling F or the QR row.

5. **Treasury QR H6, Ind p: MATCH.** Selector `(nyfed_weekly,6,260,QR)`, field **`ind_p=0.7754414145076511`** → **`0.775`**. Saved grid metadata: `n=40`, `hits=7`, stride7, first405; `ind_status=OK`, `boundary=False`. This independence field is distinct from the same row's CC or full-sample DQ field; no inference value is recomputed.

All five source selectors have exactly one row, all sampled fields are present, and all five displayed results match. **Lookup failures, NA substitutions and display mismatches: zero.** The boundary warning in item4 remains an explicit source limitation. Complete field strings, selectors, formatter descriptions, grid/DQ metadata, source hashes, displayed/reformatted values and any failure list are preserved in `trace_readback` in the companion JSON. No frame or source problem was hidden or replaced.

## Interpretation and NA boundaries

The current table caption and the directly read B3 paragraph of `inference-design.md` distinguish fixed `first_origin+j(H+1)` sparse-grid POF/independence/CC from the full-sample HAC DQ adaptation. Legacy CC combines full-grid-n POF LR with transition-independence LR; it is not a full-all-origin POF calculation or the new S16 likelihood. Missing transition rows or singular references retain NA/status rather than an alternative p-value. The actual formatter returns NA for missing/empty values. The current selected fields are finite, while the Treasury-F boundary reference is expressly retained.

These are post-result/exploratory diagnostics. A large p-value does not establish equal performance, independence or conditional coverage; a small saved DQ p-value is not promoted here into a new selection-adjusted conclusion. No null/reference law or mathematical proof is checked in this numeric source/display trace.

## File fingerprints and bounded operations

| File | Observed SHA-256 |
| --- | --- |
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `results/revision-20261023/inference/coverage.csv` | `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419` |
| `v3_additions.py` | `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525` |
| `results/revision-20261023/inference-design.md` | `31353e0470d744c9adccb7a5130935542cdce1ccc4f993fc09951a2a5e8d59cf` |
| `notes/revision-v6/verification-loop-045-result-numbers-selection.json` | `4ffc521b120368b212bfd9aae05ac78ddd80bd836104cfee69fc9a4dd507036b` |

Read scope: initial target hashes and HEAD; current complete displayed Table5 payload; loop045 excluded/selected ID/display metadata; the three exact coverage rows named above, restricted to sampled fields and needed grid/DQ/status context; `v3_additions.py` lines1–28 as static formatter/label routing; archived `inference-design.md` B3 paragraph at line7; current branch/HEAD and final file hashes. Other output paths/imports shown in the authoring source were not opened or executed in loop049.

Only current saved-field lookup, identity hashing, deterministic sample bookkeeping, `.3g` formatting and hits/n string joining are performed. No coverage counts, statistic, p-value, loss, model, forecast, test or proof is computed or re-executed. No raw/private vector, `.scratch` source, network/UI, Claude, nested agent, source/result/manuscript/state/ledger edit, deletion, installation or commit is involved. Only the two authorized loop049 files are written.

## Result

**All five frozen actual Table5 result cells match their exact saved coverage-output fields and actual formatter.** The expected 20-cell frame, method identities, matched/original control distinction, grid versus DQ sample meaning, prior exposure, NA behavior and boundary warning remain explicit. No numerical correction is indicated by this sample. This does not complete the overall goal, establish prospective or independent financial validation, or certify the reported reference distributions.
