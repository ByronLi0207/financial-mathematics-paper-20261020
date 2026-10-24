# Supervisor round-two revision implementation plan

> **For agentic workers:** Execute the user's ordered task list in this session. The user has authorized execution and explicitly asked that unresolved choices be logged rather than awaited.

**Goal:** Complete E6, E5, W1–W5 and C1 on PR #3, within a ten-hour maximum, preserving all original evidence.

**Architecture:** Reuse the frozen numerical archives and unchanged forecasting core. Add versioned E6/E5 and inference outputs; generate manuscript tables and numerical statements from those outputs. Keep the actual TeX compiler as the sole manuscript-PDF author.

**Tech stack:** Existing Python/NumPy forecasting code, aggregate ReportLab figures, Tectonic and Poppler. Use the bundled runtime; no system package installation.

**Spec:** User-supplied `导师第二轮修改意见-20261023.md`, read from the named review workspace on 23 October 2026.

## Global constraints

- Order: E6 → E5 → W1 → W2 → W3 → W4 → W5 → C1; item-prefixed commits.
- Maximum budgets in hours: 1.5, 3.5, 1.5, .5, .5, .5, 1, 1. Stop an unfinished item after 150% of its budget; E5 computation stops at three hours.
- E5 prediction file gets a standalone commit before any new E5 model run. All 48 cells remain in all denominators; no retries or menu changes after outcomes.
- No main changes, new PR, deletion, raw-data publication or overwriting untracked files without `.bak`.
- Numerical statements must trace to archived files or actual run output. No new external sample, causal feature claim or evaluation guarantee.
- No Claude/Cloud or cross-model review. Routine tests and same-model numerical checking remain authorized.
- Final main text including references ≤14 pages; appendices ≤5. Compile, render and inspect every page, run the full tests, push and verify remote equality.

## Review focus

- Intercept-only minimizers can be intervals; ordinary I and corrected-rank F are not identical at every window.
- Validation candidate nesting does not guarantee holdout noninferiority.
- Panel membership is the archived exact 12, with shared reporting provenance; it is not independent replication.
- The revised 71-member Holm family is a later reporting choice; retain the original 72-member archive.
- Retained numerical results, primary definitions and adverse outcomes must survive prose and layout edits.

## Ordered deliverables

- [ ] **E6:** Reconcile I and QR33+ breaches, produce Table 6, qualify the λ limit, optionally archive/plot the two original primary λ paths. Check saved arrays and original archives; commit.
- [ ] **E5 prediction:** Freeze sources, split, menu, tie/eligibility rules, P1–P3, failure denominator and hard stop in one-file standalone commit.
- [ ] **E5:** Port the two existing panel entry points without changing the forecasting core; run the expanded QR33 menu, retain all 48 statuses, recompute I, verify saved arrays, archive the 48-row comparison and P1–P3. Add compact figure and manuscript account; commit.
- [ ] **W1:** Rewrite abstract, contribution paragraph, related-literature synthesis and 150–200-word conclusion around the numerical finding; generate empirical numbers from evidence and preserve limitations; commit.
- [ ] **W2:** Add three practical implications before Discussion, with exact candidate-nesting and evaluation qualifications; commit.
- [ ] **W3:** Generate raw/Bonferroni primary evidence and remaining-71 Holm adjustment from the archived DM outputs; preserve old outputs; synchronize tables and prose; commit.
- [ ] **W4:** Calculate AR comparisons against F/S and expanded QR33 from saved summaries; synchronize robustness and coverage interpretation and adverse FX case; commit.
- [ ] **W5:** Remove audit-style repetitions, move/number notation, check source-faithful literature cells and plot labels/captions; commit.
- [ ] **C1:** Rebuild sources and actual PDF, enforce page counts, inspect all rendered pages, run all tests and source/archive checks, update the Chinese change inventory and timings, push the same PR and verify equality; commit.

## Timing and decisions

The goal began at 2026-10-23 18:15:24 UTC (11:15:24 America/Vancouver). Record item boundaries in `results/supervisor-20261023/round2/timing.json`; report actual elapsed time, never credit the maximum budget as worked time. Any unresolved user choice goes at the end of the change inventory under `待用户决定`.
