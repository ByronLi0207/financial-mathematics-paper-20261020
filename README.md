# Historical and Conditional Forecasts of Sampled Net-Position Peaks

An English working paper comparing historical peak constructions with established conditional forecasts on a common response: the largest absolute source-reported position at issue and over the next H records. The 22 October revision adds ridge quantile regression (QR), multivariate local quantiles (KNN), a scale-adjusted local variant and a separately measured Treasury-bill position aggregate. It retains favorable and adverse results together.

**The current substantive refinement remains in progress.** The replacement manuscript and complete fixed conditional results are available; the requested approximately six hours of actual direction-first research, writing and issue-finding have not yet been audited as complete. Earlier completed research windows are separate historical records, not hours credited to this round. [Current revision record](REVISION_20261022.md).

Read the [22-page paper](manuscript/working-paper/paper.pdf), [compilable TeX source](manuscript/working-paper/main.tex), [shared structured content](manuscript/working-paper/paper-content.json), [26-reference companion](manuscript/working-paper/references.bib) and [document verification](manuscript/working-paper/rendering-verification.json). The [working-paper guide](manuscript/working-paper/README.md) explains the independent PDF-rendering route and actual document checks.

## What changed scientifically

The earlier historical-selection comparison omitted mature conditional competitors fitted directly to the peak response. That omission is now addressed by a small, frozen QR/KNN/scaled-KNN menu with training-only transforms, completed labels and source-specific chronological selection. The added procedures change the earlier FX ranking. A separate official aggregate application supplies adverse transfer evidence; it is not compatible individual-dealer replication.

| Fixed comparison | Mean pinball loss change | Strict breaches | Interpretation |
|---|---:|---:|---|
| FX H6 primary: QR W2880 minus original rolling F W720 | −12.660% | 376 vs 332, of 6625 | Lower score with more breach occasions; mean positive overrun falls. |
| FX H24 legacy sensitivity: QR W2880 minus original rolling S W720 | −1.829% | 531 vs 287, of 6625 | Modest lower score, with more than doubled mean positive overrun; most net improvement comes from the partial 2017 tail. |
| Treasury H6 primary: QR W260 minus matched frozen F W260 | +50.786% | 54 vs 28, of 277 | Adverse loss, breach and mean-overrun results. No favorable secondary model replaces this primary. |

Every selected Treasury QR cell loses to its own frozen F reference. Both short-window Treasury plain KNN fits select k=W and equal that historical reference exactly; their feature distances no longer change membership. A secondary long-horizon Treasury KNN gain reverses on the fixed sparse grid of only 12 origins. Calendar groups and sparse grids remain descriptive, not independent replications or confidence intervals.

The [complete QR validation-loss profiles](results/revision-20261022/SELECTION_DIAGNOSTICS.md) expose another limitation: five of eight selections occur at penalty-menu endpoints, including all four Treasury cells. The 52 Treasury validation origins also have overlapping responses. This post-result inspection does not expand the menu, change selections or establish that an untested penalty would help; it restricts conclusions to the tested specifications. The same supplement lists the fixed and source-adapted elements: FX coefficients and transforms were not moved directly to Treasury.

Here matching refers to the same W completed-response origins and refit schedule. Rich predictors also use older records to construct lag/RMS features: the oldest training origin i can read back to i−168 in FX and i−26 in Treasury. The controls do not equalize every raw observation or isolate the causal value of added information.

The score uses stipulated .95/.05 underprediction/overprediction weights. It is not an observed financing cost. Mean positive overrun averages max(P−C,0) over all origins; conditional severity instead uses each method's own event set. Unused allowance and extra allowance above the known issue floor are different quantities. Lower score or lower unused allowance does not by itself establish safer or cheaper operation.

The [financial measurement and decision-scope note](notes/revision-20261022/financial-measurement-and-decision-scope.md) uses selected primary-source reading and elementary counterexamples to distinguish a sampled absolute position peak from individual dealer exposures, between-record peaks and directional settlement deficits. It also states the finite-expected-loss condition for the simplified quantile decision problem. These are scope checks, not observed funding benefits or new financial validation. The [remaining-payment ratio and timing note](notes/revision-20261022/remaining-payment-ratio-and-path-timing.md) adds a verified prospective liquidity precedent and an explicitly constructed instruction-order example; it does not turn the position series into settlement cash.

## Later exploratory dynamic comparison

The separately frozen [AR residual-block addition](results/revision-20261022/ar1-replay/README.md) is now executed in all eight source/horizon/history cells, with all twenty-four comparisons retained. It estimates one intercept-bearing first-order mean filter and replays ordered historical residual blocks from the actual issue position. The original QR primaries and sixty-nine-file archive remain intact; both samples were already inspected.

AR has lower loss in five of eight cells against S, five against F and five against QR; these sets differ. It improves on QR in all four Treasury cells and loses in three of four FX cells. Against S, mean unused allowance falls in all eight, while breach occasions rise in all eight. Treasury H24 W260 loss is 24.118% lower, yet breaches rise from 12 to 59 of 277 and mean positive overrun rises from 306.848 to 892.437 USD millions. Two direct-S comparisons reverse on fixed sparse grids. These findings make the family/horizon and score/tail tradeoffs more explicit; no favorable AR result replaces a declared primary or establishes safer policy.

The public before-run freeze binds seventeen files. A separate scalar/Fraction readback reconciles all 192 new aggregate rows and 24 exact OLS / 24 scalar-recursion checks. The financial run took 10.75 seconds externally, with 104,284,160 bytes peak RSS and one observed OS thread; the separate readback took 1.332 seconds. Reproduction commands and all measurement limits are in the linked supplement. A subsequent [integrity addendum](notes/revision-20261022/ar1-auditor-integrity-addendum.md) closes duplicate/omission and same-byte parsing gaps in the checker. Its separate second readback passes all192 exact-key aggregate rows and1196 fit-record metadata entries; the independent coefficient/report oracles remain restricted to24 refits and24 issued reports. Both receipts are retained.

## Design, complete evidence and provenance

The [design](protocol/revision-20261022/conditional-baseline-design.md) and [machine specification](protocol/revision-20261022/study-spec.json) fixed sources, features, menus, completed-label timing, histories, update schedules, comparisons and resource/failure rules. The [16-file executable freeze](protocol/revision-20261022/executable-freeze.json) was publicly recorded at [1bd5b69](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/commit/1bd5b692fd9cb240763c032fb4e1c203871fad55) before new validation. All 24 source/H/W/family selections were then publicly fixed at [8ce6e39](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/commit/8ce6e398a17e4c12cb36a9a76785e78fd21a1da0) before evaluation. Public selection binds the exact validation receipt bytes; ties prefer the larger numeric candidate.

The immutable [core conditional result archive](results/revision-20261022/README.md) contains 72 validation candidates,90 procedure summaries,372 annual rows,98 declared paired comparisons,388 annual paired rows,98 sparse paired rows and 56 phase receipts. Its tightened [second audit](results/revision-20261022/evaluation-audit-02.json) reconciles source-window targets, trace identities, timing, scores, labels and aggregates. Failures would have been retained without shortened means or favorable replacement parameters; every declared original phase completed.

[Post-result diagnostics](results/revision-20261022/POST_RESULT_DIAGNOSTICS.md) separately retain all 90 floor-binding configurations and 45 paired-horizon reports, the original audit and a later snapshot-integrity addendum. They were designed after seeing results, outside the original 98 comparisons, and change no forecasts. Those original files cover the conditional study and historical controls. A [separate complete AR diagnostic addition](results/revision-20261022/ar1-diagnostics/README.md) now retains eight floor rows and four horizon pairs: FX has no observed crossings, while TreasuryW52/W260 cross59/26times out of277. The seven short-history Treasury H24 floor-binding reports all breach. All236fields were independently checked. Its exact retained-attempt audit is manifest-bound; a fresh run requires new input identities. Some estimated H6 reports exceed their H24 counterparts even though every realized target is ordered. A learned short-horizon report is not a known long-horizon lower bound; no retrospective monotone repair or regime switch was executed.

## Closest work and the actual contribution

[Wisniewski, Lindsay and Lindsay (2020)](https://proceedings.mlr.press/v128/wisniewski20a.html) and Chapter 6 of Wisniewski's thesis already apply richer features, neighbors, quantile and normalized/conformal forecasts to signed endpoints in this FX source family. Their two-endpoint interval scores are not benchmarks for the single absolute multi-record peak. Exact equality of their raw bytes to this accepted CSV is not established.

Financial path extrema, regression quantiles, nearest-neighbor prediction, volatility/residual scaling and constrained/calibrated horizon curves all have mature antecedents. The supported contribution is a bounded application/model-validation comparison: fit credible competitors to the same completed response, match histories/update schedules within sources, retain adverse results and record qualified source transfer. A changed target or dataset alone does not create a new estimator. The elementary finite construction bounds are supporting arguments, not new statistical guarantees.

The [26-reference evidence map](notes/revision-20261022/paper-evidence-map.md) records actual consulted versions and reading ranges. A [bounded priority follow-up](notes/revision-20261022/targeted-priority-followup-agent.md) distinguishes inspected original targets from metadata-only screening and unresolved access. These checks do not prove absence of an exact predecessor. QRF, CAViaR, SPCI and full volatility-filtered historical simulation remain distinct unexecuted competitors; the tested menu is not claimed to exhaust the strongest conditional methods.

The [whole-procedure selection note](notes/revision-20261022/whole-procedure-selection-and-unseen-evidence.md) separates causal refitting, tuning and research-family selection. The [finite-family inference review](notes/revision-20261022/finite-family-inference-applicability.md) reads the original Reality Check/SPA routes without appending a retrospective p-value or declaring all inference impossible. A [directed policy-evaluation reading](notes/revision-20261022/policy-generated-inventory-and-validation-boundary.md) distinguishes passive recorded peaks from policy-generated simulated inventory and a future decision study. These are background admission/interpretation notes, not extra main references, executed competitors or unseen samples.

The [known-floor inference note](notes/revision-20261022/quantile-inference-and-floor-atoms.md) revisits an original conditional-quantile encompassing test and distinguishes its density, dependence and noncollinearity requirements from this response. It explains why a familiar p-value cannot simply be appended to the current descriptive comparisons. That earlier note ran no new test or forecast combination; the later fixed-terminal diagnostic below addresses a different one-sided null.

The [horizon-sorting note](notes/revision-20261022/horizon-rearrangement-and-score-scope.md) derives an elementary consequence of mature rearrangement methods. With common ordered targets, units, origins and equal horizon weights, sorting crossed reports cannot increase their total pinball score, while an individual horizon and the number of breaches can worsen. Sorting inherits a valid pre-existing joint upper-coverage event; it creates no new 95% guarantee for these fits. A peak report can also define a constant symmetric sampled-path band, without recovering the original asymmetric intervals or unobserved paths. No sorted financial forecast or revised primary is executed.

## Sources, identities and limits

The FX input is version 2 of the [Net Position Time Series Dataset](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset), accepted member `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`. It has 18,576 records,1,286,391 bytes and SHA-256:

```
b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa
```

It is a signed client-flow aggregate from one market maker, not the complete hedged book, gross exposure, cash flow or funding requirement. Recorded gaps are retained; H counts records rather than uninterrupted calendar hours. The historical timezone/public-release vintage is unverified. Same-source files at another frequency are not independent dealers. Raw redistribution permission is unverified.

The post-result [stored-clock duration census](notes/revision-20261022/record-clock-duration-audit.md) quantifies this distinction on the fixed origins:336 of 6,625 FX H6 evaluation windows span 54 stored-clock hours, and 1,342 H24 windows span 72 hours. Treasury H6/H24 span 42/168 as-of calendar days. The census uses timestamps without forecast scores; source clocks and public-release vintages remain distinct. It does not create a fixed-clock target, a selected subsample or an accuracy claim.

To obtain the FX input manually, open the linked dataset record, select version2 and download only `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`. Do not request the complete collection, whose recorded metadata size is about274 MB. If the selected download is a ZIP, inspect its member list and extract only the requested CSV; the observed single-file wrapper used the basename `1hourNetPositionsKaggle.csv`. Require the byte count and SHA-256 above before placing it at `.scratch/data/1hourNetPositionsKaggle.csv`. Preserve an existing mismatching file for investigation; do not replace it or substitute a derived-feature member. Source access or account requirements can change, and the fingerprint is not a promise of permanent access.

The existing [bounded original runner](run_study.py) also supports explicit missing-source-only `--fetch`, using the source's single-member/version request and refusing a mismatching existing cache. **That option continues into the original historical analysis after acquisition; it is not a download-only command and is not required when the exact CSV is already available.** It uses the original study's separate owned attempt and recorded resource rules. No Kaggle Python package is required by that route. A manually supplied `--input` elsewhere does not populate the new replay's fixed cache path.

The separate [New York Fed Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) snapshot uses series `PDPOSGS-B`:706 weekly Treasury-bill long-minus-short market-value records in USD millions,3 April 2013–7 October 2026. The 23,315-byte CSV has SHA-256:

```
9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb
```

[Source definitions, acquisition routes, reporting/release dates, reuse terms and attribution](results/revision-20261022/EXTERNAL_DATA.md) are retained. An absolute signed sum permits cross-dealer cancellation and changes meaning with valuation, composition and weekly measurement. Original release times and historical unrevised vintages were not reconstructed: this is a downloaded-vintage economic-date replay, not a live public-information backtest. Sources are analyzed in native units and are not pooled. The [independent-source feasibility record](notes/revision-20261022/independent-source-feasibility.md) distinguishes acquired data, inaccessible/confidential alternatives, metadata-only candidates and the still unresolved compatible-dealer question.

The [unchanged accepted TreasuryCSV](data/nyfed-pdposgs-b-20261022/README.md) is archived with its source attribution and continuing NYFedTerms. FX raw observations, private per-origin traces, credentials and third-party paper PDFs remain excluded from public delivery. Free reading/downloading does not establish unrelated redistribution rights. A current source route may expand or revise its bytes; a mismatching snapshot is rejected rather than truncated, spliced or silently substituted.

## Reproduction and resource limits

In the existing Python environment, the default entry is read-only and requires only the standard library:

```bash
python3 -B reproduce_conditional.py
```

It checks the executable and selection freezes and all 69 core archived files. Historical temporary-path references in the selection are matched to their exact public validation receipt bytes in memory; a fresh checkout does not need the original temporary directory. Its successful status is `ARCHIVE_VERIFIED`, explicitly with `accuracy_recomputed=false` and `raw_sources_read=false`.

The explicit full replay requires macOS, an already available compatible NumPy environment, and the exact accepted snapshots at:

```
.scratch/data/1hourNetPositionsKaggle.csv
.scratch/revision-20261022/nyfed-PDPOSGS-B.csv
```

Use regular local files and regular parent directories. The replay rejects symlinked inputs or ancestor paths, including a shared cache linked into the repository, even when the target's bytes match.

```bash
python3 -B reproduce_conditional.py replicate --attempt-id NEW_UNIQUE_ID
```

This creates a new owned attempt and executes 24 validation,24 evaluation and 8 reference phases serially under one total 540-second deadline. A new selection binds new receipt paths/hashes; all statuses and chosen parameters must match the archived 24-cell matrix before evaluation proceeds. The adapter independently reconciles new source-window peaks, exact stored arrays/scores,90 summaries and 98 contrasts, exporting only inside the new attempt. It records every aggregate CSV scalar difference, including tiny floating differences, without a tolerance that conceals disagreement. New timestamps/resources need not match old receipt hashes. A numerical audit and agreement with old outputs are separate statuses. Existing attempts, old receipts, all original results and the scientific freeze are preserved.

The original accepted financial workers requested one numerical thread, observed at most one OS thread in their recorded snapshots and used less than 70 MB process RSS, with maximum phase duration 15.83 seconds. Internal phase stops are 540 seconds/1.5 GiB, with a 600-second alarm; the standing upper resource limits are 2 GiB RSS,2 observed threads,100 MiBraw sources and 25 MiBper download. These are process observations and budgets, not an OS memory sandbox or research hours. No installation, GPU, broad parameter search or persistent service is needed. A full replay completed in 129.50 seconds: all 56 phases passed, the 24 selected status/parameter cells matched and all six exported aggregate CSVs were byte-identical to the archive. Maximum worker RSS was 68,911,104 bytes and one thread was observed. The [compact replay verification](results/revision-20261022/reproduction-check-20261022.json) retains all six table comparisons and the 56 new phase identities/resources; all 72 validation candidate scalar rows also matched. This is a computation replay, not independent scientific replication.

The supplementary diagnostic replay then uses:

```bash
python3 -B reproduce_conditional_diagnostics.py --replication-dir .scratch/revision-20261022/replication-NEW_UNIQUE_ID
```

It writes inside that successful attempt, preserving all earlier files. The [actual diagnostic replay](results/revision-20261022/diagnostic-reproduction-check-20261022.json) reproduced both 90/45-row diagnostic tables byte-for-byte without reading raw sources or refitting models; peak RSS was 78.32 MB. These checks remain descriptive and change no forecasts.

Document rebuilding is separate:

```bash
mkdir -p .scratch
python3 -B build_conditional_figures.py --output .scratch/conditional-figure-rebuild-01
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
```

All outputs must be new. Figures use only pinned aggregates; document rendering uses the supplied content and approved assets. The scratch TeX command regenerates source for byte comparison; its relative figure paths are not a standalone scratch compilation package. Compile the supplied `main.tex` from `manuscript/working-paper/` with its adjacent `figures/`, or copy the entire document folder into a new build location. The [document guide](manuscript/working-paper/README.md) records dependencies, fonts, source compilation, the supplied PDF route and actual visual/text checks.

## Preserved earlier studies

[Original results](results/README.md) retain all 35 method/setting rows, seven paired comparisons, original diagnostics and four descriptive resampling profiles. The [earlier one-state retrieval extension](results/revision-20261021/README.md) retains 30 summary,10 geometry,22 comparison and 26 monthly rows. Their adverse horizon/preference/monthly evidence remains in Appendix B, existing files and repository history. The old statement that no added model beats the original leader applies only to that earlier one-state menu; it does not extend to the new QR/KNN results.

The [new-attempt AR and diagnostic reproduction](results/revision-20261022/ar1-fresh-reproduction/README.md) supplies a separately frozen route for genuinely new AR manifests and genuine version-2 readbacks. A new eight-cell execution reproduced all six AR tables and both 8/4-row diagnostic tables byte-for-byte; it reused the successful conditional attempt without repeating its 56 phases. Its actual AR process used about103 MB peak RSS and8.85 seconds externally. This computation replay preserves the adverse results and does not count as new data or independent scientific replication.

Further primary-paper reading checks the [finite-rank feasibility of a related ES-path calibration rule](notes/revision-20261022/finite-rank-feasibility-neighbor-note.md), including a small exact counterexample, the printed setting's feasible global ranks and the allocated rules' upper-end saturation. It neither reproduces that author's code nor overturns empirical tables. The project's own available ranks still supply no coverage guarantee without the separate statistical assumptions; a neighboring specification issue does not establish this project's novelty.

The [current scientific-direction audit](notes/revision-20261022/current-research-direction-audit.md) binds the exact 22-page manuscript and compares its actual contribution with the endpoint, path-risk, filtering and calibration literature. It distinguishes the strengthened same-target benchmark from the still-missing compatible unseen validation, financial mechanism and decision evidence.

The [late fixed-terminal coverage supplement](results/revision-20261022/coverage-evalues/README.md) retains all 56 matched reports and896 maturity phases after a publicly verified61-file freeze. A distinct exact-formula readback reconciles every hit, phase, value and input/output identity. Four specific QR cells cross the fixed 1120 reference threshold; the other 52 are not coverage PASSes. Treasury H24 W260 AR still has59/277 breaches with evidence 11.0284 below 1120. This is an inspected-sample exploratory diagnostic, without retrospective empirical5% familywise, arbitrary-stopping, new-data or financial-safety claims. The calculation used 1.19 seconds / 92,766,208 bytes peak RSS externally; its independent check used 1.18 seconds / 79,855,616 bytes. No forecast was refitted or repaired. That coverage addition preserved the earlier ten tables, seventeen equations, three figures and abstract. A later abstract/introduction correction explicitly labels the original and matched FX breach references and the Treasury AR contrast; it changes no financial result.

The [24-hour research-window audit](RESEARCH_WINDOW_AUDIT.md) and [prior six-hour revision audit](REVISION_20261021_AUDIT.md) are historical records. The current paper still lacks compatible unseen dealer data, a reconstructed public-release vintage, established population/conditional coverage and observed quote/hedge/funding decision costs. Better numerical reproducibility and presentation do not supply those scientific gaps or promise a journal tier. No journal submission is represented.

The later [official release-vintage audit](notes/revision-20261022/official-release-vintage-feasibility-agent.md), [issue-clock and known-floor analysis](notes/revision-20261022/issue-clock-target-and-known-floor.md), and [economic inventory-neighbor review](notes/revision-20261022/inventory-mechanism-neighbors-and-next-baseline.md) give concrete boundaries for future validation. They establish no new financial fit, compatible independent dealer record or live-vintage backtest, and preserve the then-current manuscript's25-reference scope.

For a fresh full replay, copy the archived `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv` to the exact `.scratch/revision-20261022/nyfed-PDPOSGS-B.csv` input path listed above, using regular files and parent directories. If the destination already exists, verify the accepted SHA and preserve it; do not overwrite a different snapshot. The frozen replay keeps its fixed input paths and still requires the separately obtained FX source.

The [conditional-baseline admission note](notes/revision-20261022/conditional-baseline-admission-and-delay.md) specifies what a later QRF/CAViaR comparison would need: completed-label feedback, a genuine weighted-response distribution, fixed initialization/optimization, chronological selection and explicit horizon-order conditions. These are unexecuted design boundaries, not additional favorable results or inherited coverage guarantees.

A separate [classical horizon-rearrangement derivation](notes/revision-20261022/horizon-rearrangement-pinball-and-coverage.md) clarifies pooled-score and joint-event properties without repairing or rescoring the financial reports. Better equal-weight pooled pinball can accompany more breach occasions; preserving an existing valid joint-coverage bound cannot create one. Individual horizons and unequal economic weights remain distinct.

The known [2017cash-peak quantile precursor](notes/revision-20261022/known-cash-peak-precursor-restoration.md) is now explicitly restored in the22-page/26-reference manuscript. It was present in earlier reading records, not a newly discovered paper or new data. The [endpoint/peak comparability note](notes/revision-20261022/endpoint-marginals-and-peak-score-comparability.md) gives elementary finite examples clarifying the changed target without claiming a new method or financial experiment.
