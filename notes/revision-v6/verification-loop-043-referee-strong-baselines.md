# Verification loop 043 — S13 stronger-baseline definitions and scope

- Reviewer: same-model internal textual/static referee check, not external peer review or independent empirical validation.
- Assignment: read all non-table method/failure/scope material in current Supplement S13 and compare bounded existing protocol/implementation definitions for FHS, QRF and peak-headroom POT as needed. No new financial computation is authorized.
- First current-version/hash readback: **2026-10-23T22:37:12Z**.
- Last readback/note timestamp: **2026-10-23T22:39:57Z**.
- Branch: `revision-v4-jof`.
- Initial HEAD: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`; HEAD at note write: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`.
- Root goal remains active until 2026-10-24T00:31:50Z. This note does not close that goal.

## Verdict

No new scientific or conclusion-changing method/scope issue was found in this bounded current-text-to-static-definition reading. S13 distinguishes its same-target finite FHS, all-original-row leaf-distribution QRF and GARCH-scaled peak-headroom POT adaptations; retains exact mature-label and update conventions; and separates numerical admissibility, structural tail-size failure and financial performance. It expressly preserves original primaries, exploratory status, NA cells, finite-configuration limits and the distinction from canonical return-innovation EVT.

This verdict is not a fresh validation of any cell count, issued-prefix count, stored optimizer flag, saved residual hash, financial mean, table value, covariance or p-value. The observed numerical statements in prose and encountered table metadata were not recomputed. No claim is made that the original external methods' assumptions or the current empirical source vectors have been independently authenticated in this loop.

## Exact current reading scope

Current `submission-jof/supplement-content.json`, **section index 12**, title **`S13. Mature baselines: methods and complete outputs`**, has 27 blocks (indices 0–26). Read **all 24 non-table blocks**:

- Paragraphs: 0, 2, 4, 5, 8, 10, 12, 17–23 and 26 (15 paragraphs), including all method, retained-failure and interpretation text.
- Equations: 3, 6, 9, 13 and 24 (five equations), including displayed HTML/inline-math metadata.
- Subheadings: 1, 7, 11 and 16.
- Table blocks 14, 15 and 25 (S33–S35): captions/identity metadata were encountered; numerical table cells were not reviewed or newly validated.

Read the corresponding non-table Supplement TeX at **lines 955–983, 1077–1094 and 1111**, stopping before S14. JSON and TeX carry the same audited method/failure/scope meanings. Main JSON/article TeX/PDF and Supplement PDF were fingerprinted only; no fresh PDF rendering, visual audit or compilation is claimed.

Static sources consulted, without importing/executing their numerical code:

- `protocol/revision-20261023/round2-D1-mature-baselines.md`, full lines 1–38. Its historical implementation/test checklist was read as documentation, not as an instruction to run work in this verification-only loop.
- `round2_filtered.py`, lines 1–359, full source-independent FHS/POT implementation.
- `round2_qrf.py`, lines 1–204, full source-independent QRF implementation.
- `round2_baselines_run.py`, relevant caller/guard/no-fallback/aggregation definitions at lines 1–3, 17–37, 43–83 and 94–106; adjacent static context was also returned. Its financial routines were not run.
- `run_round2_baseline_queue.py`, lines 1–21, serial queue/no automatic retry definitions; no queue/state file was opened or changed.
- `run_study.py`, resource thresholds at lines 67–78 and RunGuard context at lines 169–264.
- `conditional_features.py`, lines 35–117, common feature/transform, mature-pool, refit-clock and response-scale helpers.
- `protocol/revision-20261022/study-spec.json`, current scalar H/window/refit/feature-clock fields only. No source data path was opened.
- Targeted locator snippets from `round2_baselines_verify.py` were encountered while locating failure/readback definitions; no historical verification status or prior review verdict was used as proof, and no saved-output readback was invoked.

## Definition and limitation checks

| Topic | Current static/protocol anchor | Finding and retained limit |
|---|---|---|
| Same measured response | D1 protocol 5, 20–24; filtered core 244–248, 286–319; QRF 145–152, 184–188 | Training labels are completed H-record peak headrooms G=P-|N|, with the current absolute-position floor restored at issue. FHS paths include h=0. QRF's target is G/a, and POT fits scaled G. None of these is silently scored as an endpoint interval or one-step return quantile. No actual source/forecast vector was reopened here. |
| Completed pool and refit clocks | Common helpers 94–105; filtered core 282–297; QRF 139–156; D1 protocol 14, 20 | At refit r the W origins run from r-H-W+1 through r-H, and latest label end is checked against r. Refit anchoring uses the original segment start and fixed steps 24 FX / 13 Treasury. Current common scalar protocol retains H=6/24, FX W720/2880 and Treasury W52/260. Static calls match these conventions; this is not a fresh receipt-by-receipt maturity validation. |
| GARCH envelope and fit | Filtered core 189–241, 286–308; D1 protocol 20–21 | The same source-position envelope a..r contains W+H-1 increments. Training RMS conditions the constant-mean Gaussian-QMLE GARCH(1,1) fit; zero/nonfinite scale fails. One fit is called, with maxiter 300 and ftol 1e-8; warnings/fit diagnostics are retained. Finite parameters, positive omega/variance and the declared persistence ceiling are eligibility checks, not statistical adequacy or coverage proofs. |
| Persistence and convergence distinction | Filtered core 215–238; current S13 17–24 | The shared error message covers either convergence or admissibility. The gate includes convergence flag 0 and alpha+beta <=1+1e-10. S13's later paragraph explicitly classifies its retained FX examples as successful optimizer flags rejected for persistence tolerance, rather than optimizer nonconvergence or worse financial predictions. The existing historical flag/count/hash assertions were read but not revalidated from saved fit arrays or new optimization. No tolerance was relaxed. |
| Frozen fit, moving issue variance | Filtered core 299–308, 328–342; current S13 block 2 | Parameters and standardized residual pool are frozen between refits; newly observed increments update the variance state only through the actual issue. Historical sigma estimates are in-sample at the later refit, not originally issued forecasts at each historical starting origin. S13 states that distinction explicitly and imports no independence/stationarity/coverage premise from numerical termination. |
| FHS path/rank construction | Filtered core 48–89, 309–316, 334–342; D1 protocol 22 | Fixed source/H/W/refit-bound seed and 2048 iid-with-replacement residual paths are drawn once per refit block and reused inside it. Simulation starts from the actual signed anchor and current one-step variance, recursively updates variance and native increments, retains maximum absolute position including the anchor, and uses the corrected empirical 19/20 rank for headroom. No endpoint/square-root-of-H shortcut appears. No simulation was run in this loop. |
| FHS residual and source-method limits | Filtered core 203–220, 312–313; current S13 block 5; D1 protocol 35 | Resampling uses stored standardized residuals directly; there is no further empirical recentering/unit-variance rescaling. A constant fitted mean does not claim the finite resampling pool has exactly zero mean/unit variance. The paper labels this same-target peak adaptation rather than exact derivative-portfolio reproduction. Original assumptions and financial adequacy are not established by this check. |
| POT threshold/tie rules | Filtered core 92–110, 276–278; D1 protocol 23 | The fixed ascending threshold leaves floor(.1W) potential upper observations; actual excesses use strict R>u, so ties can reduce m. Minimum 20 and tail fraction above .05 are enforced. W52 is structurally rejected before a tail optimizer/forecast is attempted. No alternate threshold or count rescue is present. This static rule check does not recount executed NA cells. |
| POT fit, support and zero-shape limit | Filtered core 113–182; D1 protocol 23 | One zero-location Nelder–Mead run in (xi, log beta), fixed initial value and stopping options is used. Positive finite scale, valid support and xi>-.5 are required. The implementation uses the declared exponential limit near zero shape (absolute xi <1e-7), and validates the extrapolated quantile/support. No alternate start, threshold, fit retry or fallback is implemented. No tail likelihood or quantile was evaluated here. |
| POT historical normalization and native report | Filtered core 317–325, 334–342; current S13 blocks 8–9 | Mature G at origin i is normalized by the refit's in-sample one-step sigma at i+1. The fixed fitted tail quantile is multiplied by current one-step sigma and added to the current floor. Historical in-sample normalization is not represented as an original historical issue-time forecast. The native-unit floor and nonnegative headroom are retained. |
| Canonical innovation EVT distinction | Current S13 block 10; D1 protocol 23, 36 | The text credits McNeil–Frey's filtered one-step return-innovation tail and multi-period sum construction, then explicitly says the current headroom-tail scaling is a different procedure. Signed-anchor/volatility ratio, drift, future variance-path effects and overlapping-label dependence remain after one-scale normalization. Successful GPD optimization does not remove those approximation limits or confer a theorem. No external original body was fetched/read anew. |
| QRF fixed feature/partition configuration | QRF 22–35, 131–162; common features 35–91; D1 protocol 24 | Same common 33 causal feature construction, training-only transform with nearest=False, mature headrooms and response scale are used. Fixed 100 trees, 11 candidate features, leaf 5/split 10/depth 10, bootstrap and one worker match the prose. The bounded configuration is not called an optimized QRF class or a proof of the original consistency theorem under dependent fixed windows. |
| Genuine leaf-distribution QRF | QRF 38–83, 160–188; current S13 12–13 | Tree partitions are learned with bootstrap, but leaves are applied to every original mature training row. Query weights average equal within-matching-leaf original-row masses over trees, without bootstrap multiplicity. Zero-mass responses are excluded before the noninterpolated left CDF inverse. Output is a positive-mass retained response, restored to native units with a and the floor; it is not a quantile of tree means and has no F rank correction. No forest was fitted or queried in this audit. |
| Complete-cell failure and no fallback | Filtered core 351–359; QRF 197–204; worker 43–83 | Cores preserve partial prefixes only as explicit failure material and rethrow. The worker requires full finite capacity shape for COMPLETE; failures clear evaluation and comparison scores, including resource failures caught at the final guard. No shortened mean, replacement report or automatic rerun is substituted. Current section's prefix counts are historical observations, not new results of this loop. |
| Resources and stopping | D1 protocol 16–17, 21–24; worker 1–3, 33–50, 80–83; RunGuard 67–78, 169–264; serial queue 1–21 | The protocol has one serial worker, one requested numeric thread and outer 2GiB/600s ceilings. The reused internal guard is stricter at >=1.5GiB and >=540s, rejects unverified resources or >2 observed OS threads; the worker sets a 590s signal and queue has a 620s outer call timeout. These are layered limits, not assertions of measured current-run RSS/time. A late resource failure makes the whole cell NA. No worker, resource probe, queue or optimizer was launched. |
| Original comparisons and separate family | Current S13 0, 26 and captions; worker 58–71, 94–106; D1 protocol 15, 30 | Original primaries and their 72-slot family are not replaced by these additions. New within-cell comparisons name frozen F and original QR and retain a separate 48-slot Holm family. Failed/degenerate component values remain displayed NA; 1 is only adjustment bookkeeping, not an observed valid p-value. No family, table, component test or aggregate was recomputed in this loop. |

## Necessary issues / optional language

- Necessary scientific or conclusion issue: **none found in this bounded static reading**; no scientific author-pending correction is created.
- Optional phrase only: “All original training rows receive within-leaf mass” could say “All original training rows in each matching query leaf receive within-leaf mass”. The displayed indicator/denominator equation and current code already make this condition explicit; this would avoid a standalone reading that every training row has positive mass for every query. No edit was made.
- All retained empirical counts, failure-prefix counts, optimizer-flag classifications, historical fixed-coefficient hash readbacks and financial outcomes remain **not freshly numerically validated by loop043**. In particular, the 18/6/24 prose counts and table cells were encountered, not recomputed.

## Current constraints and access limits

Only static sources and current document text/metadata were read. No raw observations, private vector/array file or retained forecast artifact was opened. No models, forecasts, residual draws, tail fits, forest fits, tests, covariance/likelihood/statistical calculations, proofs, new analyses, table/aggregate recomputation, network/external literature lookup, UI, Claude/Cloud/cross-model validation, nested delegation, source/manuscript/result/protocol/state/ledger changes, commit, push, deletion or installation occurred. Reading scripts that contain those actions did not execute them. Only this authorized note file was written.

## Current fingerprints

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |
| `submission-jof/supplement-preview.pdf` | `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991` |
| `protocol/revision-20261023/round2-D1-mature-baselines.md` | `cec3a4df77c2d7f749361bdcb1a1e5e87be1f4aec460696959831a968ab873db` |
| `protocol/revision-20261022/study-spec.json` | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |
| `round2_filtered.py` | `c01b675d5a284ffc92890b78d043362edcc329f5d1ef824e81db43cef3f0aad7` |
| `round2_qrf.py` | `52a3cffc2367fec54613d8a2eb47cd7dc0f335f48958565ea300dd5165d96db4` |
| `round2_baselines_run.py` | `35e184aa3fc861024413dad1b454695e11d56a112180a9110626eb10d053fa54` |
| `run_round2_baseline_queue.py` | `2ecc217f43ff0c2fcecf022a913e187e6de781909489f1a14f266fc8583765f3` |
| `run_study.py` | `8d8c305357e888f7665beed67dcc8f8a3619070a33a30d935c9582512db18f1f` |
| `conditional_features.py` | `4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5` |
