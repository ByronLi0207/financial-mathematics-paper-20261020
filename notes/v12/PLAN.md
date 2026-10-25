# v12 scientific diagnostics and submission revision implementation plan

> **For agentic workers:** Execute the supplied F0–F6 sequence with independent scoped implementation and verification. User explicitly authorizes execution without waiting; log conservative decisions instead of approval gates.

**Goal:** Diagnose finite-menu conditional losses and produce the sole v12 submission, preserving all archived results and adverse findings.
**Architecture:** New v12-only loaders, forecast shell and experiment drivers call the unchanged causal features, ridge solver, empirical reports and scorer. Scientific protocols are separate Git commits before any pilot or evaluation. New aggregate results live only in results/v12; restricted source/prediction arrays stay in .scratch/v12. The native editable submission remains submission-v10/, with version identified by revision-v12 and canonical documentation.
**Tech stack:** Python via temporary uv, NumPy, existing certified ADMM ridge quantiles, pytest, Matplotlib, Tectonic, Poppler, pypdf.
**Spec:** notes/v12/supervisor-task.md; final user override deletes the active AI declaration while preserving other author placeholders.

## Global constraints

- Base452064866c2bdc4166b89d09d67b0cb2bc0ae415; only revision-v12 may change. All other refs/PRs protected; no old-v3 writes or execution. No downloads of new financial data.
- F1/F2/F3 each protocol alone committed before its first computation; protocol bytes and thresholds then immutable. Resource truncation is predeclared and never based on favorable results. No retries of failed cells/candidates.
- Formal wall caps including pilots: F1 3600s, F2 2400s, F3 1500s. Phase budgets1800/9000/5400/3600/12600/1800/1800s; stop an unfinished experiment phase at150% and log. Preserve all11 F4 items; reduce F2/F3 first.
- All new empirical numbers derive from results/v12 actual outputs; preserve old science seal. Separate retrospective diagnostics, finite-menu oracle, and deployable selection; no absence-of-all-signal theorem.
- Existing untracked file must have .bak before overwrite; preserve existing backups. No system Python package installation. No Claude or cross-model review.

## Review focus

1. Mature labels, original common H24 buffer in FX/Treasury, distinct CFTC H6 buffer, and unchanged evaluation/refit origins. Test earliest pool and exact grids.
2. Infinity is ordinary empirical headroom, not corrected historical rank; finite oracle excludes infinity. Test negative selection component and exact sum identity.
3. No successful-subset oracle after failure; planned denominators with unknown bounds. Test failed/missing candidates, strict signs, ties, and D2 E<=0 nonsupport.
4. Tau must change solver, ranks and pinball weights together; explicit capped corrected rank at W52/tau.99. Test equivalence at.95 and maximum-rank behavior on toy data.
5. Frozen results/refs and private-input boundaries; all F4 relocations retain existing numbers, and language does not claim structural absence of conditional information. Verify seals and all final rendered pages.

## Tasks and file ownership

- [x] F0: verify base and create revision-v12; record all protected refs and science hashes; source/API/split/literature audits. Commit F0.
- [ ] F1 design: protocol/v12/loss-decomposition-design.md alone commit;90 sourcecells/180 methodcells, full fixed six-menu validation and evaluation, exact signed decomposition andD1-D3. No pilot before gate.
- [ ] F1 code: v12_inputs.py for fixed fingerprints/clocks; v12_forecast.py for existing fixed-lambda calls; v12_decomposition.py pure algebra/predictions; run_v12_decomposition.py protocol gate, single-attempt workers/pilot/caps/results. Tests test_v12_inputs.py, test_v12_forecast.py, test_v12_decomposition.py use toy fixtures; run red before minimal implementation where practicable. Seal code commit before pilot; every actual output/timing archived.
- [ ] F2 design alone commit protocol/v12/validation-length-design.md. Implement isolated run_v12_validation.py; reuse exact F1 evaluation reports with fingerprint/clock checks, never retry an earlier failed candidate. Save results/v12/validation-length, V1/V2 byW and conjunction; no native-unit pooling.
- [ ] F3 design alone commit protocol/v12/tau-design.md. Add v12-only general-tau shell using same solver, new ranks and generic pinball; run_v12_tau.py outputs results/v12/tau.37 cells/tau, methodsF/QR33; no new model family. Meaningful toy tau/rank/clock tests.
- [ ] F4 all items, each recorded in notes/v12/edit-log.md with before/after and final page:
  1. DataTable2; source-native descriptive script/output in results/v12/descriptives, explicit population/horizon/aggregation and dates.
  2. F corrected rank, scaled ridge objective with unpenalized intercept, andDM formula.
  3. New <=1.5page low-frequency section combines saved menu evidence withF1/F2; signed decomposition figure, tau sentence/small table, no obsolete7.5.
  4. Readable names, clean design paragraph and threshold wording; verified M2 wording; mean overprediction; remove main-body internal codes.
  5. Table1 fully source-verified columns/rows; drop unverifiable whole columns; remove partial/unverified footnote; table1-check evidence.
  6. Compact propositions; verified textbook citation or no inappropriate citation, proofs retained inSupplement.
  7. Move original short-history/long-H FX paragraph verbatim toRQ1.
  8. Limitations<=.6page,6–8single-sentence items; all required scope/cost/posthoc boundaries; technical details moved verbatim toSupplement.
  9. Code availability one sentence linked revision-v12; canonical current entry v12.
  10. Interpretive paragraphs inSections7–9; avg15–20words, no>40; preserve three findings and numerical precision.
  11. Main<=20pages inclrefs;Supplement<=38; AR/rank/horizon body one sentence each, original details retained.
- [ ] F5: abstract<=180words/8numbers, at most2sentences changed including switching wording; <=3 contributions, four places aligned, RQ1–3 conclusion order; frozen before/after writing metrics.
- [ ] F6: all tests pass in qualified original-history environment, four native PDFs compiled, each page rendered and viewed; protected numbers/results/refs/author placeholders checked, AI declaration absent in active package; publish onlyv12 and exact remote/local tree; final Chinese full requested deliverables and real timings. End early once complete; no scope expansion to fill10h.
