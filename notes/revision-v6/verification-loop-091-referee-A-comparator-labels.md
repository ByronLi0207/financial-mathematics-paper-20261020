# Loop 091 — internal referee A: proposed comparator-label clarifications

Audit: 2026-10-23T23:36:38Z to 2026-10-23T23:37:43Z UTC. Branch `revision-v4-jof`; observed HEAD `61d60e8fac7c2ec25e67268b7da4ef4ba233c018`. Same-model internal review only. Parent goal remains active to 2026-10-24T00:31:50Z; any later language edit is for the parent to decide.

## Actual current scope

Directly reread current main JSON index 6, **7. Scoring and calibration (RQ2)**, all six prose blocks (1–5, 8), both figure placements (6–7) and Table 5 caption (0): nine blocks total, no standalone equations/subheadings. Read corresponding article TeX 264–303 with table body excluded, including Figure 3/4 captions. Also read only main index 5 blocks **5–7** around the proposed year/grid label, and corresponding TeX 241–245. No table cells or figure images were inspected.

Permitted frozen-output check: `wp2-findings.json` top-level schema/status, method inventory and input-binding names, plus the single `wrapped_pairs` record with `source=fx_hourly`, `horizon=6`, `window=2880`. No other pair's metrics, linked result file, private/vector data or previous referee verdict was evidence. No arithmetic, model, statistic, proof or test was executed.

Fresh SHA-256 fingerprints:

- `submission-jof/manuscript-content.json`: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`
- `submission-jof/manuscript.tex`: `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`
- `submission-jof/manuscript-preview.pdf`: `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`
- `results/revision-20261023/v6/wp2-findings.json`: `8841a9258bae71c4c162afc6c5efd91ff4fa2a323621db637b7f012cf1623972`

The PDF hash identifies the unchanged candidate; no rendered-PDF audit occurred.

## Decision 1 — original-primary versus legacy label

**Faithful label clarification; no substantive objection.** In main 6 block 6, replace only `H6/H24 legacy-reference` with `H6 original-primary and H24 legacy-reference`. Keep the ordered displayed pair **−16.388%/−8.027%** unchanged.

The bounded context separately calls the H6 comparison the primary, distinguishes its original and matched-history reductions, and calls H24 the legacy-reference comparison. Main 7 blocks 1/3 likewise distinguish original H6, matched H6 and H24 legacy. The proposed expansion removes the compressed wording that could apply “legacy” to both horizons. It does not relabel the matched H6 result as the original primary, change a denominator, create a new primary or make the sparse grids independent holdouts.

This is a textual comparator-label check. The two sparse-grid numbers were not independently traced to output records or recomputed here; they are required to remain exactly as currently printed, in the same horizon order. The final same-inspected-record / no-independent-validation / no-retrospective-switching sentence must remain intact.

## Decision 2 — wrapped versus unwrapped QR/F

**Faithful and useful label clarification; no substantive objection.** In main 7 block 8, replace only `leave QR with` by `leave wrapped QR (ACI-QR) with`, and `than the wrapped historical rule` by `than wrapped F (ACI-F)`. Retain **15.00%** and all other numbers and surrounding qualifications.

The selected frozen record is explicitly under `wrapped_pairs`, has status COMPLETE, and identifies the FX H6/W2880 matched context. Its stored fields are `qr_minus_f_loss_percent=-14.99691078803782`, `qr_mean_loss=393795.05776986334`, `f_mean_loss=463271.4662733057`, with `qr_hits=329`, `f_hits=328`, `n=6625`; rates are stored as 0.04966037735849057 and 0.04950943396226415. These fields were read verbatim, not derived or recomputed. The method inventory names the wrapper methods `ACI_QR` and `ACI_F`; display aliases ACI-QR/ACI-F preserve that distinction. This is the wrapped-to-wrapped comparison, not unwrapped QR versus wrapped F or original rolling F W720.

The unchanged remainder must continue to call this a post-result empirical joint score–frequency result, deny conditional-coverage/canonical ACI guarantees, retain adverse SAV and FX-combination findings, retain the Treasury median's excess breach frequency, and preserve state and unavailable-upper-level limits. Explicit wrapper labels do not imply causal coverage correction or prospective validation.

## Full-section consistency and verdict

The rest of current main 7 separates paired-loss from coverage nulls; Murphy crossing from universal dominance; the finite eight-report envelope from global action optima; and original primaries from matched comparisons. Working-reference p values are not selection-adjusted confirmation. Neither proposed replacement changes those scopes or any numerical/scientific conclusion.

Both proposals are optional editorial clarifications justified by current text and the permitted stored pair; neither is a newly discovered conclusion defect. No necessary scientific issue or author-pending scientific correction found. This note authorizes no source action by itself; the parent retains the stated decision step.

Only this note was written. No source/result/state/ledger edit, commit, new search/network/UI/Claude/Cloud or nesting occurred. Final full readback, SHA-256 and UTC time are reported on delivery; no note edit follows.
