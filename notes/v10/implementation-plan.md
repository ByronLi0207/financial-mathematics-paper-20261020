# v10 forecasting-paper implementation plan

> For agentic workers: execute E0–E7 in order with root as committer and focused, nonoverlapping helpers. Use the supplied user brief as authority, synthetic-test-first scientific adapters, independent artifact/source verification and an end-of-branch review. No Claude/Cloud or cross-model review.

**Goal:** add a paired menu experiment, independently reported CFTC positions, standard multi-method forecast comparison and a fixed illustrative limit-cost analysis, then deliver the bounded v10 article.

**Architecture:** public v9 `0d2526cc69092c5158437a0509613bac5e86d47f` is the immutable base. Inherited forecast/solver/old-study modules stay byte-identical. New v10 adapters live in new modules; source/results bind all printed numbers. Each of four research designs is committed alone before its own computation (and before any CFTC download for E2).

**Tech Stack:** existing Python3.12 runtime with temporary uv packages (arch8.0.0/NumPy2.3.5/scikit-learn1.9.1/pytest9.1.1/matplotlib3.11.2), unchanged mature forecasting code, arch.MCS, native Tectonic and Poppler. No system package installation.

**Spec:** `notes/v10/task.md`, byte copy of the user's named supervisor task. The original absolute source and SHA are in `e0-baseline.json`.

## Global constraints

- Only `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024` and new `revision-v10` are writable paper targets. No existing branch/PR/directory writes, no PR create/merge/close, no delete/cleanup.
- Stage budgets E0/E1/E2/E3/E4/E5/E6/E7:30/90/210/60/60/90/30/30min; hard-stop150%:45/135/315/90/90/135/45/45min. Goal10h; early finish allowed. Stage receipts record actual wall time, incomplete work and transitions.
- E1 formal<=1800s; two-repetition pilot selectsR32 orR16 before launch. E2 formal<=3600s. No retry of failed research cells, tolerance changes, shortened success medians or favourable replacements.
- New financial data only official CFTC TFF files after E2 standalone design commit. No other source refresh; existing private files are read/copied by fingerprint, never redistributed.
- Do not modify old data/results, forecast engines, solvers or inherited provenance guards. Private historical objects imported into NEW.git are not ancestors/exported. Final publication transports only revision-v10 content; preserve history limitations explicitly.
- All new scientific numbers come from results/v10; old real-data numbers bind to unchanged v9 archives. All author/ORCID/funding/conflict/AI placeholders remain unfilled.
- Missing decisions go to PENDING.md with conservative rulings; user explicitly delegated these choices and opted out of waiting for design/approach approval. User-specified clone overrides worktree defaults. No skill approval loop or deletion instruction applies.
- Existing untracked output is backed up to.bak before overwrite; prefer new/exclusive outputs. No output dir reuse for a numerical run.

## Review focus

1. Menu pairing must keep the original stage seed/tag and switching-phase denominator, including anR16 subset; merely retaining RNG seeds is insufficient. Verify geometry/uniforms and Fpoint receipts against v9.
2. New CFTC contracts are related category aggregates. Continuity uses report weeks, not fixed Tuesday/gap7; source/market units, code changes, vintage/release lags and fewer-than20 eligibility must remain explicit.
3. MCS uses all complete declared procedures per common source/period/H/W grid. Do not silently intersect grids, score partial files, merge overlapping periods or treat duplicate loss columns as distinct stochastic evidence.
4. Fixed costs require genuine saved capacity/target/floor arrays and an identified F report; zero meanFheadroom makes that cell unavailable. Costs/coefficients are illustrative, not measured operating benefits.
5. A positive finding cannot repair original negative/failed evidence, infer a pure frequency effect or establish prospective/individual-dealer validation. Official journal quartiles not accessible are “unverified,” never recalled from memory.

## E0 — preparation (30min; stop45)

- [x] Clone remotev9 into exact new path, verify0d2526c and create revision-v10. Inspect applicable instructions.
- [x] Snapshot all14 existing remote refs and five old paper directories; identify outside v8-goal/PR5 drift without writing/rolling it back.
- [x] Inventory saved private loss/report schemas and copy only core complete vectors by exact hashes. Investigate official CFTC metadata/URLs without any dataset request.
- [x] Preserve required old private Git objects only in NEW.git and run unchanged full-suite baseline. Expected: all inherited tests pass with original guards, no study run or private-source refresh.
- [x] Commit E0 plan, metadata/provenance and availability receipts; startE1 only after this commit.

## E1 — menu isolation (90min; stop135)

**Files:** standalone `protocol/v10/menu-isolation-design.md`; new `v10_menu.py`, `run_v10_menu.py`, `test_v10_menu.py`, `test_v10_menu_driver.py`; `results/v10/menu/`.

**Consumes:** unchanged v9 diagnostics/calibration, generator, stage seeds, Fpoint archive, finite `v8_mechanism_mc.forecast_report`, exact empirical I. **Produces:** exhaustive source/arm/W/method cells, paired old/new summaries, M1–M3, bindings and Figure4 inputs.

- [x] Freeze six-candidate menu/I, required-all QR33 vs eligible-completed QR4, directed stronger-lambda exact ties (disclose original QR4 difference), samepath evidence, R32-phase/R16subset, pilot/failure/deadline/aggregation/M1–3 rules. Commit DESIGN ONLY.
- [x] Write and observe failing artificial tests: infinity equals ordinary I with mature pool; finite forecasts unchanged; ties/failures/selected-eval no fallback; phase-preserving subset and whole-cell incompleteness. Implement minimal adapters, run focused/full required checks, seal code before actual outputs.
- [x] PilotR2 on old pilot paths; freeze timing-derived formal plan. Run exactly one formal experiment; compare v9 uniform/RNG/geometry and Fpoints, retain all failures. Format complete grids/figure and actual protocol/run clocks; commit E1.

## E2 — CFTC external application (210min; stop315)

**Files:** standalone `protocol/v10/cftc-design.md`; `v10_cftc_data.py`, `v10_cftc_forecast.py`, `run_v10_cftc.py` and their synthetic tests; `data/cftc-tff/provenance.json`; `results/v10/cftc/`.

**Consumes:** verified official HTML metadata/URLs, existing weekly features and forecasting core plus E1 menu adapter; optional generic delayed ACI engine. **Produces:** raw-file provenance, fixed eligibility/ranking/splits, complete method vectors and T1–3 per-contract results usable by E3/E4.

- [x] Freeze futures-only/2010start/full-history handling, exact official acquisition list/transport/failure-stop, weekly coverage/code/stable identity/OI tie ranking/top20-or-fewer, economic-date replay/release caveats, formula-based52val/260eval/H6/W52,260/refit13 split, methods and optional paired finite delayed ACI inputs/parameters, T1–3/unknown handling. Commit DESIGN ONLY before any dataset download.
- [x] Tests first on invented ZIP/rows: schema/code preservation/report-week continuity, gaps/duplicates/ranking/splits; labels completed before selection, full training windows, six-menu/I, no scoring incomplete methods. Implement using frozen forecast core.
- [x] Acquire only official CFTC files, recording URL/UTC/bytes/SHA/status; any download failure stops data acquisition and proceedsE3 with E2 explicitly unavailable. Never substitute another source or fabricate20eligible contracts.
- [x] If data usable, run once<=3600s; no retries, all contracts/cells and failed slots reported; preserve public vectors. Save T1–3, complete tables/plot and clocks; commit E2.

## E3 — model confidence sets (60min; stop90)

**Files:** standalone `protocol/v10/mcs-design.md`; `v10_loss_inputs.py`, `v10_mcs.py`, `run_v10_mcs.py` and focused synthetic tests; `results/v10/mcs/`.

**Consumes:** core source inventory with exact saved report/loss vectors and E2 complete vectors; origin identities fixed before matrix construction. **Produces:**90%arch.MCS per complete comparison grid plus source-level membership/exclusion counts and full pvalues/statuses.

- [x] Freeze scope (two hourly periods, original weekly/Treasury/panel,daily,CFTC), variant labels/aliases, complete-grid/no-partial policy, deterministic existing combinations if included, loss derivation only where missing, duplicate equivalence handling, arch statistic/bootstrap/reps/block/seed, report denominators/failure rules. Commit DESIGN ONLY before loss derivation/bootstrap.
- [x] Tests first: origin/target mismatches rejected rather than shortened; known duplicate identities unfolded honestly; seeded mature MCS on artificial loss matrix; failed methods/cells remain inventoried. Implement adapters+arch wrapper.
- [x] Run saved-loss analysis once; no new forecasts or adaptive settings. Save all memberships/pvalues, method availability, counts and source-generated main table; commit E3.

## E4 — illustrative limit costs (60min; stop90)

**Files:** standalone `protocol/v10/cost-design.md`; `v10_cost.py`, `run_v10_cost.py`, tests; `results/v10/cost/`.

**Consumes:** saved C/Y/B/origins from E3 registry and matching correctedF. **Produces:** fixed-grid normalized costs/differences and source-level parameter-region figure.

- [x] Freeze units of kappa/b/c, positive-scale F headroom denominator and zero-scale unavailable rule, full parameter grid/primary plot c, reference/candidate inventory and method-specific comparison (no outcome-picked best model). Commit DESIGN ONLY before cost means/regions.
- [x] Tests first: hand-worked reserve/breach/exceedance costs, strict breach vs amount distinction, F normalization invariance, zero-Fscale unavailable. Implement and run on frozen vectors, full grid/status outputs; commit E4.

## E5 — positioning and writing (90min; stop135)

- [x] Verify official JCR/CAS pages and three candidates includingJoF, scopes and format; record query dates/URL/access limitations, choose first target with unverified classification explicitly unverified. Check primary DM/GW/MCS and inventory-risk references before adding.
- [x] Rewrite around RQ1 matched accuracy/RQ2 frequencies+independent report system/RQ3 fixed cost; <=3finding contributions synchronized across abstract/intro/conclusion/letter. Preserve all adverse/NA/survivorship/measurement/selection/coverage boundaries, one Limits statement for illustrative costs.
- [x] Put new E1/E2/MCS/cost evidence in main, retain detailed/archive-linked complete results. Main<=20inclrefs/Supp<=35; same fixed writing counter<=8%/<=20words/0over40. Canonical sources/snapshots/ZIP/metadata coherent; author placeholders retained. Commit E5.

## E6 — simulated reviewer reconciliation (30min; stop45)

- [x] Two same-model internal roles (method/domain),five principal concerns each. Combine with prior42 into52unique dispositions with exact current source locations; actual fixes or reasons, unresolved science inLimits/TODO. No Claude/cross-model/outreach. Commit E6.

## E7 — final checks and publication (30min; stop45)

- [x] Full suite and all source/archive numeric/identity/old-target protection checks. Compile four native PDFs from saved sources/fresh sourceZIP, render/open every final page and verify caps.
- [x] Publish onlyrevision-v10, no PR/merge/closure; original private Git identity history not exported. Compare against fixedv9base; retrieve complete remote tree and verify every path/mode/byte, then align only new localbranch after preserving local research history.
- [x] Recheck protected refs/directories; report outside drift separately. Final Chinese7deliverables, complete prose, clocks/timings/unknowns and pending decisions; commit final records and close goal only after actual required gates.

## Pre-flight dependency rulings

E1 output is required before interpreting menu mechanism in E5. E2 eligibility/results feed E3/E4; official download failure is an authorized branch to unavailable-E2, not permission for another data source. E3/E4 independently registered designs do not authorize one another's calculations. Their common input adapter does metadata assembly before the respective gated computation. E5 waits for all four result states, including failures. E6 fixes feed E7 final source, which is always recompiled/reviewed after changes.

Ruling: the user's detailed execution order, conservative decision delegation and instruction not to wait supersede skill design-approval questions, worktree selection and cleanup defaults. No file deletion. Scientific test-first work is limited to new behavior; reversible document packaging uses actual hash/compile/render checks rather than mirror tests.
