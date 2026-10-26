# Verification loop 035 — Referee A: finite adaptation method language

- Reviewer: same-model internal self-review; not external peer review or cross-model validation.
- Assignment: read the bounded first S16 adaptation subsection and its coverage-definition wording, ending before “Fixed report combinations”; compare the method/eligibility language with existing static implementations only as needed.
- First version/hash readback: **2026-10-23T22:26:27Z**.
- Last readback/note timestamp: **2026-10-23T22:28:33Z**.
- Initial HEAD: `2e7ff3bbfd631e69cdc188c47a1fa23aa590d3a3`; HEAD at note write: `2e7ff3bbfd631e69cdc188c47a1fa23aa590d3a3`.
- Root-supplied active goal deadline: 2026-10-24T00:31:50Z. Completion of this bounded review does not close that goal.

## Verdict

No new scientific or conclusion-changing method-language issue was found within this bounded static readback. The current prose describes a finite delayed projected ACI-style adaptation and a mature-headroom SAV adaptation without inheriting canonical ACI coverage, literal return-CAViaR replication, global optimizer guarantees or coverage certification from diagnostic nonrejection. The current supplement JSON and its TeX agree on the two audited paragraphs.

This finding is text-to-static-definition consistency. No model, state trajectory, financial output, likelihood value, p-value, test or proof was executed or reproduced. The audit does not establish fresh empirical correctness, conditional coverage, optimizer adequacy or source-data maturity from private vectors.

## Exact reading scope

Current `submission-jof/supplement-content.json`, `sections[15]`, titled `S16. Additional benchmarks and robustness`:

- Read **all non-table method/definition/eligibility prose** in the bounded interval `blocks[3:17]`: block 3, “Finite delayed ACI-style calibration and headroom SAV”, and block 6, “Coverage diagnostics”. These are the only two non-table paragraphs in the interval.
- Read both paragraphs in full, including inline-math mappings. Read their corresponding `submission-jof/supplement.tex` prose at lines **1228** and **1290** in full.
- Stop boundary: block 17 / TeX line 1656, “Fixed report combinations”; only its heading was used to locate the end. Its method content and later S16 subsections were not audited here.
- Table blocks 4, 5 and 7–16 (Tables S39–S50) were not numerically reviewed. Their captions and block/binding metadata were encountered to establish the coherent subsection's inventory. No bound result/validation file was opened merely because its path appeared in `_bindings`.

Static implementation read for the named issues:

- `v6_aci.py` lines 1–143 (including exact finite rank, mature-score and issued-hit cursors, projection, rank-zero floor, initialization and gamma selection).
- `v6_sav.py` lines 1–355 (including mature slices, scale, normalized recurrence, initialization, six numerical starts, analytic constant branch, cell failure and forecast scale restoration).
- `v6_worker.py` lines 154–226 and 241–253, read as static caller context specifically to check prevalidation eligibility, frozen gamma, selected validation-prefix replay across the unissued gap, and validation-ineligible/failed SAV whole-cell handling. Paths to private artifacts appearing in code were not opened.
- `v6_inference.py` lines 1–164, with reliance on the coverage definitions at lines 85–164.
- `inference_tests.py` lines 93–109 for the legacy UC-plus-independence definition. A separate bounded contextual read also returned lines 140–150; that unrelated elementary-score code was not used in this verdict.
- Main JSON/article TeX/PDF, supplement PDF, `v6_supplement.py` and the two bound protocol texts listed below were fingerprinted; no PDF page rendering, new compilation or fresh reading of those protocol bodies is claimed.

No previous review verdict was used as evidence.

## Method-language checks

| Topic | Static anchor | Finding / preserved boundary |
|---|---|---|
| Delayed score maturity | `v6_aci.py` 83–95 | The score deque has maximum length W. The score cursor admits only rows with origin + H <= current issue, in chronological order, using the completed peak minus that origin's base report. Warm-prefix scores and issued rows enter the same mature-score pool; future labels are not admitted by the stated loop. |
| Wrapped hits differ from base scores | `v6_aci.py` 97–105 | Feedback compares the actual earlier peak with the actual earlier **wrapped** capacity, rather than substituting the base report. The separate hit cursor consumes each eligible issued row once and only when origin + H <= current issue. Warmup base scores do not create fictitious wrapped hits. |
| Alpha update and current pool | `v6_aci.py` 91–108 | Alpha starts at exact 1/20. Each delayed update projects into [1/(m+1),1] using the pool size at the current issue; a separate projection is applied immediately before report issuance, including when no new hit was consumed. The prose describes both the update projection and issue-time state projection. |
| Fractional rank and rank zero | `v6_aci.py` 21–27, 106–114 | The corrected rank uses exact `Fraction` arithmetic for the ceiling. The finite domain enforces the feasible rank range. Rank zero issues the known floor directly; positive rank takes the score order statistic, adds the current base report and floors the result. The prose does not interpret a negative-infinite internal rank-zero sentinel as an issued nonfinite report. |
| Initial history / eligibility | `v6_aci.py` 58–71, 92–95; `v6_worker.py` 157–172 | The minimum initial mature-score count is explicitly enforced (19 in the caller/default); an inadequate prevalidation grid returns an ineligible cell before a fictitious gamma inventory is scored. The paragraph's statement that initial history can invalidate a cell is compatible with these checks. |
| Validation selection | `v6_aci.py` 125–143; `v6_worker.py` 182–201 | The fixed gamma menu is .001/.005/.01/.05. An eligible candidate must be COMPLETE with the exact validation count and finite valid metrics. Selection minimizes exact absolute hit-rate distance to .05, then mean .95 pinball loss, then gamma. Failed candidates remain explicit; if no candidate is eligible, the method is NA. Resource failure governs the whole cell. The prose calls this coverage-first retrospective selection and distinguishes original QR tuning. It does not equate a selected coverage distance with a guarantee. |
| Carry across unissued gap | `v6_aci.py` 60–65 and 85–108; `v6_worker.py` 203–223 | After gamma is frozen, the caller concatenates the original validation issues and evaluation issues, replays the chosen stream, and statically checks exact equality of its validation prefix before retaining evaluation outputs. Unissued gap rows are not manufactured. Mature validation hits still awaiting feedback are consumed at subsequent issued times, using the current pool and preserving once-only order. The prose's carry statement is consistent with this deterministic replay construction; it is not a claim of a new prospective evaluation. |
| SAV training and shock maturity | `v6_sav.py` 193–227, 280–290, 293–334 | At refit r, the W-response pool ends at r-H. Initialization uses earlier mature labels; training and issue shocks are G_(i-H). Between refits the recurrence consumes mature shocks while coefficients and scale remain fixed; a refit resets the fitted path. This agrees with the written H-delayed headroom recursion. |
| SAV scale and source-unit report | `v6_sav.py` 148–158, 222–227, 280–283, 330–343 | A positive training-response scale is set at refit using training-only quantities, with an explicit positive stabilizer. Responses, shocks and the initialization quantile use that same scale. The source-unit headroom is multiplied by the held scale and then added, after nonnegative projection, to the current absolute-position floor. The prose explicitly multiplies the normalized prediction back by the same a_kappa; it does not silently issue normalized values as native-unit capacities. |
| Finite optimizer and failed cells | `v6_sav.py` 19–20, 229–279; `v6_worker.py` 241–252 | Nonconstant training responses use the fixed 3-by-2 six-start bounded Powell menu and finite stopping budgets. A start is eligible only with solver success, legal finite coefficients and finite objectives; all start receipts are retained. No eligible start raises a terminal fit failure; the caller returns NA without partial scores, and failed validation blocks evaluation. Constant training responses have a separately labeled analytic fit. No global minimum or canonical CAViaR asymptotic conclusion is claimed. |
| Full-sample UC and fixed grid | `v6_inference.py` 127–164 | Full-origin UC uses every supplied evaluation hit. Grid selection is anchored at the first supplied authoritative evaluation origin with step H+1, without a searched offset. Grid UC uses all grid hits. Missing required interior grid origins suppress the grid tests, rather than reconnecting surviving rows as adjacent pairs. The static helper requires the caller's complete original origin vector; this review did not revalidate that vector from raw/private inputs. |
| Transition-conditional CC | `v6_inference.py` 98–124 | New CC compares the saturated two-row transition likelihood with fixed-alpha likelihood on the **same n-1 successor pairs**, conditioning on the first hit. The fixed likelihood's success count is n01+n11, not the all-n grid hit count. An absent row or no transition gives NA; boundary reference flags remain diagnostic. This matches the current paragraph. |
| Legacy distinction | `inference_tests.py` 93–108; `v6_inference.py` 3–7 | The legacy routine computes UC using its complete supplied n-hit sample and adds transition-independence LR based on n-1 pairs. New coverage code explicitly does not call that legacy routine and does not overwrite its archived values. The prose distinguishes the definitions; it does not import new CC values into the old tables. No numerical old/new likelihood was computed here. |
| No inherited canonical guarantees | Current two audited paragraphs; static module docstrings | “Finite-memory, delayed and projected”, “No original ACI guarantee”, “headroom adaptation rather than a literal CAViaR return-VaR replication”, no global optimum, NA/boundary references and the explicit non-certification statement are retained. Neither nonrejection, near-nominal breach frequency nor the Markov label is presented as conditional-coverage certification or as ruling out floor atoms. |

## Issues / author-pending record

- Necessary scientific/conclusion issue: **none found within this bounded reading**. No author-pending scientific correction is created by this loop.
- Optional language precision only: the Powell six-start sentence could say “For nonconstant training responses, ...” to state the analytic-constant exception locally. The existing S48 caption already distinguishes analytic constant fits; the static code does not pretend that branch underwent numerical convergence.
- Optional language precision only: “legacy mixed full-sample-UC-plus-transition-independence” could clarify “the full supplied grid sample” to distinguish that UC sample from the immediately preceding full-origin UC. The underlying definitions are explicitly separated and no value change is indicated.
- These suggestions were recorded only; no manuscript or source edit was made.

## Work and access limits

No model/test/statistical/proof execution, new analysis, private vector or raw financial data access, external literature/network search, Claude/Cloud/cross-model review, UI use, nested delegation, source/manuscript/result/protocol/state/ledger edit, commit, push, deletion or installation occurred. Static reading of code that contains scientific computations is not an execution of those computations. Only this authorized note path was written.

## Current fingerprints

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |
| `submission-jof/supplement-preview.pdf` | `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991` |
| `v6_aci.py` | `e81005a25ca7b94dec86540981b890c945c280478b861e7416f7fb852f67b15a` |
| `v6_sav.py` | `a476828ee8818572a4b57e4b170ec4ee4ccecbef43c4babdf37138329ee586c1` |
| `v6_inference.py` | `1c7fc9a3fe8392c771dde0272966b9a0f0f3c4b969df481d0d6818385dcfd2e5` |
| `v6_worker.py` | `c12878f4dd441b1d8bed05c8ada00fb370912ce8251a2c2b4e027217140efddc` |
| `inference_tests.py` | `2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c` |
| `v6_supplement.py` | `e8e85e8d0d3b03c21349a21b3a71af7fa209eb2ffb54ec82cd33acffbbcd237b` |
| `protocol/revision-v6/wp2-aci-sav.md` | `4d1115663011753ad85c41a9b5f6bf50b100e186d9a1c6d3c8b622fa996ac2e7` |
| `protocol/revision-v6/common-contract.md` | `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8` |
