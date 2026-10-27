# v9 research and manuscript implementation plan

> For agentic workers: execute this plan in order with the supplied C0–C7 authority. Independent source audits can be delegated; a stage's downstream work waits for its prerequisite commit. No Claude or cross-model review.

**Goal:** retain PR #5 evidence, adopt the clearer revision-v8 writing, and test the nonstationarity explanation under a design committed before computation.

**Architecture:** the public PR5 commit is the immutable scientific base. New diagnostics and synthetic experiments live under v9 paths; unchanged WP3 forecasting and WP4 aggregation functions are reused. Native TeX remains authoritative; all result claims carry located archive bindings.

**Tech stack:** Python 3.12 bundled runtime, uv temporary packages, existing NumPy/SciPy/arch/statsmodels/pytest, Tectonic and Poppler. No system-Python installation.

**Spec:** `/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/导师v9合并任务-20261024.md`.

## Global constraints

- Only `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024` and its new `revision-v9` are writable. Base `0f1f066843e0c49cf3e24bce7d72032dc189603d`; no merge.
- Do not alter existing branch refs, old local directories, PR3/4/5, main or archived study results. Publish only revision-v9; no PR creation/closure.
- C2 design must be a standalone commit before real-series diagnostics, parameter estimation or simulation. Read-only metadata, existing-output comparison, source inspection and software tests are preparation.
- No new real-data forecast evaluation, financial source download or forecast model family. Existing input observations stay private where their source rules require it.
- Each stage ends with its numbered commit and timing evidence. Stop an unfinished stage after150% of its budget; record remaining work and continue.
- Existing untracked output must be backed up before overwrite. Prefer exclusive paths. Do not delete old outputs or workspace artifacts.
- All author/ORCID/funding/conflict/AI placeholders remain unfilled. Decisions are recorded, not used to stall.

## Review focus

1. Original evaluation cutoffs, not backcast/retro cutoffs, bound diagnostics; no evaluated outcome enters calibration.
2. Shared record identity does not identify a frequency effect; daily and hourly clocks and minimum segments must be explicit.
3. Parameter instability diagnostics must account for serial dependence/conditional heteroskedasticity; a classical iid cutoff must not be represented as valid under fitted GARCH without qualification.
4. Median percentage loss and WP3's ratio of mean losses are different estimands; C2's aggregation and unavailable-cell handling are frozen first.
5. Seven old hourly failures, the WP3 failed candidate, the daily exception and overlapping backcast remain visible; historical tests cannot be skipped or guards weakened to obtain a green suite.

## C0 — preparation (30min; stop45min)

- [x] Clone remote revision-v8-goal, create revision-v9, record protected files/refs.
- [x] Compare writing/products and classify each as import, supplement or omit.
- [x] Compare all shared real-data archives/located core fields; Expected: zero unexplained numerical differences.
- [x] Map WP3/WP4 pure-function interfaces and exact settings; verify existing local input fingerprints without study computation.
- [x] Commit all C0 records, append actual timing. Whole-suite baseline can complete in the background, reading this same unmodified base.

## C1 — thesis (30min; stop45min)

- [x] Write `notes/v9/thesis.md`: common findings from hourly, weekly, daily, stationary simulations; explicitly reserve the instability sentence for C2.
- [x] Expected: no established causal instability explanation, no independent-third-period claim, at most three future contribution threads. Commit C1.

## C2 — registered instability study (240min; stop360min)

- [x] Verify primary literature and save `notes/v9/literature.md`; choose mature diagnostics and bootstrap/segmentation policy with its assumptions.
- [x] Write `protocol/v9/nonstationarity-design.md` with source cutoffs, alpha/multiplicity, max breaks/min segments, segment fitting/failure rules, regime placement, no-break matched control, estimands, N1–N4, exact WP3 settings and timing ladder. Commit this file alone before computation.
- [x] New code units: `v9_nonstationarity.py` (diagnostics/calibration), `v9_switching.py` (generation), `v9_exposure.py` (fixed descriptive geometry), `run_v9_nonstationarity.py` (bounded orchestration), and synthetic tests. Scientific contracts precede code; helper signatures are implementation choices.
- [x] Tests first: inserted break detection; stable-null/control behavior; complete labels and input cutoff; regime-boundary state transitions; whole-cell failures; median aggregation. Observed RED then GREEN, including independent driver-repair cases.
- [x] Reuse `v8_mechanism_mc.forecast_report/select_candidate`, original features/QR/F, and `v8_daily_fx.resample_closed_days`; do not run old financial drivers or modify their guards.
- [x] Two-repetition pilot selected R32/both QR under the fixed global5400s ceiling from first diagnosis; the run plan was committed alone before formal. No post-launch rule changes or research retries.
- [x] Archive every diagnostic/source row and simulation cell under `results/v9/nonstationarity/`; report N1–N4 and the required figure. Expected: complete inventory even if failures or unsupported predictions. Finalize thesis according to the registered branch, then commit C2.

## C3 — prose integration (120min; stop180min)

- [x] Rewrite abstract, introduction, Section2 ending, Section8, conclusion and limitations, retaining PR5 evidence and actual C2 outcome. First/Second/Third only; elementary target facts are supporting material.
- [x] Rename7.4 as specified and keep it<=1.5pages. Bind all numbers to unchanged PR5 archives or new v9 output.
- [x] Use one fixed writing counter before/after; report any discrepancy with quoted task snapshots. Expected:<=8% flagged,<=20words/mean,0sentences>40,primary<=3; preserve the eight limitations once.
- [x] Version historical v8 document tests against their frozen v8 fixtures and add v9 located-binding/negative checks; retain all cases rather than skip them. Commit C3.

## C4 — structure (60min; stop90min)

- [x] Main<=18pages including references; supplement<=30. One two-panel simulation figure in main; full WP3/C2 grids and the separate original D0/D2 section in supplement, with D1 failures.
- [x] Update Table6 with daily/C2; use readable figure labels and comma ticks without changing Figure1 data. Commit C4 after compile/layout check.

## C5 — referee reconciliation (30min; stop45min)

- [x] `notes/v9/referee-check.md`: each of15 V8 plus27 PR5 concerns has a disposition and exact v9 location/reason. Unresolved scientific gaps go to Limitations/AUTHOR-TODO. Commit C5.

## C6 — package (30min; stop45min)

- [x] One-page JoF cover letter,<=6keywords, running title<=40characters; all links/availability/crossrefs/aliases/content snapshots/ZIP current and v9-specific. Placeholders retained. Commit C6.

## C7 — final verification/publication (30min; stop45min)

- [x] Full suite, numeric/source/archive protection checks, native main/supp/title compilation; render and inspect every final page.
- [x] Publish only revision-v9 using existing authenticated transport; no credential/permission expansion or private-object export. Preserve original research history privately if browser transport is required; report file-tree and Git-history identity separately.
- [x] Verify remote/local files, modes and head; protected refs and local snapshots unchanged. Give fixed-base compare link and keep PR3/4/5 decisions for author. Commit C7 records.

## Rulings

- The user's detailed task and instruction to continue conservatively replace additional design-approval questions; methodological choices are recorded before computation.
- Five exact pre-existing historical Git objects are imported privately into NEW.git solely to preserve unchanged provenance guards. They are not v9 ancestors and must not be published in a bundle/ref or through --all/--mirror.
- WP3 uses controlled normal innovations and ratio-of-means summaries. C2 explicitly requests estimated AR-GARCH-t and medians; new paired processes share that required t/calibration choice, while cross-study comparisons retain the distinction.
- The old writing metrics have different scopes/snapshots; C3 must use the same fixed program for its own before/after comparison and document the scope instead of adopting quoted numbers unverified.
