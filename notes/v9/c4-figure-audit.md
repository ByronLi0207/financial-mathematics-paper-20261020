# C4 saved-source figure audit

**PASS for both adopted new figures.** All four generatedPNGs were inspected. Both adoptedPDFs were independently Poppler-rendered at150dpi after the final layout revision and inspected with no clipping/overlap. EachPDF has one page. No financial forecast,model,diagnostic,simulation,target orscore calculation was run. Only archived-point rendering,equivalent unit display anddescriptive plot summaries were performed.

## Main include handoff

- Adopt `submission-jof/figures/v9-endpoint-peak-example.pdf` forFigure1;matchingPNG is beside it.
- Adopt `submission-jof/figures/v9-simulation-comparison.pdf` for the single main simulation figure;matchingPNG is beside it.
- Keep the existingv7Murphy paths inmain. Generatedv9MurphyPDF/PNG variants are retained **UNUSED**,per root instruction. The existing legends already sayQuantile regression/Historical headroom. No old file was overwritten or deleted.

## Figure1: same selected Treasury path, native units

The original `/selection` in`notes/v7/example-selection.json` has origin408,H6,dates2021-01-27..2021-03-10;absolute positions42513,43528,73875,65145,74397,50851,48144;report73139. Units are **USD millions**,not rawUSD. Endpoint48144<=report73139<peak74397. These seven points,dates andreport are unchanged.

The oldv8comma figure,builder,TeX source andbinding receipt were read only. Its receipt proves only five scientific tick strings became comma strings;all coordinates andBezier commands were unchanged. Its frozen seven values,report anddates exactly match the current public selectionJSON. PR5`notes/revision-v8/style_figures.py` instead displayed native values÷1000 withUSD billions. The new display undoes that representation: `v9_millions = PR5_display_billions *1000 = saved_native_value`. Ordinary y ticks48,000/56,000/64,000/72,000 show the original unit. The builder pins the public selection hash and can render without the oldv8directory;when present that directory supplies an additional read-only historical comparison. No privateGitobject is required or exported by this figure builder.

## Simulation panelA: controlled stationary grid

QR33,H6;all nine(phi,variance-persistence)settings atW52/260/720/2880. Every one of36curve points equals its exact`results/revision-v8/wp3/summary.json` `/cells/<index>/relative_loss_percent`,with identity fields checked. Every source cell has32/32 complete repetitions. Independent arithmetic verifies each saved percentage equals`100*(mean_model_loss/mean_reference_loss-1)` within1e-12;the saved percentage itself is plotted.

All nine thin curves are retained. Band=min/max across settings;dark line=descriptive median across nine settings. These plotting summaries are not confidence intervals,a pooled statistic ornew inference. X positions are categorical for the four planned windows;connecting segments guide the eye.

| History | Minimum% | Median% | Maximum% |
|---:|---:|---:|---:|
| 52 | 113.459742537191 | 120.531840150888 | 135.518859299387 |
| 260 | 21.307826749420 | 23.856176427308 | 36.270776649492 |
| 720 | 0.059039107093 | 5.223395919225 | 9.446283328541 |
| 2880 | -13.010271180464 | -3.952629995274 | 1.127275203226 |

## Simulation panelB: calibrated controls

Source is`results/v9/nonstationarity/postrun/analysis/report.json` `/across_source/0..3`. Medians andIQRs are across13source-level repetition medians,each requiring32complete paired repetitions. This is distinct fromPanelA’s ratio of mean losses across repetitions. Both definitions appear under the panels;the two designs are not pooled.

| Arm/history | Status | Complete | Median% | Q25% | Q75% |
|---|---|---:|---:|---:|---:|
| constant/52 | COMPLETE | 13/13 | 116.24327967680179 | 92.89995539118937 | 124.3385564851092 |
| constant/260 | UNASSESSABLE | 12/13 | None | None | None |
| switching/52 | COMPLETE | 13/13 | 121.40097999787356 | 101.91853468487092 | 131.2574640787476 |
| switching/260 | UNASSESSABLE | 12/13 | None | None | None |

The two right-panel markers are horizontally offset only for legibility; both have actual training history52. This is stated in the figure footnote and scalar receipt. No alternative history is implied. The footer uses the reader name “33-predictor regression.”

W260 full summaries are null inboth arms. No numeric point,whisker orconnecting line is drawn. The annotation states12/13complete sources ineach arm. Completed-only12-source medians andpartial repetitions do not replace missingPDPOSTIPS-G11. W52labels116.2%/121.4% are .1frounding ofthe exact archived medians. Higher y means higher loss. The visual comparison does not identify a causal mechanism.

## Unused Murphy variants

Each public`inherited-exact/murphy-*-display.csv` has201points. All402threshold/left/right triples in`scalars.json` equal the parsed owningCSV values exactly. No elementary score was recomputed. These initially rendered variants use native saved threshold unitsUSD millions,but remain explicitlyUNUSED. Main keeps the originalv7artifacts andunits. The full-breakpoint crossing result belongs to its original archive;the display grid alone is not claimed as its proof.

## Scalar ledger and input hashes

`results/v9/figures/scalars.json` retains all36controlled points withprecise JSONpointers;all4C2aggregate records;all402publicMurphy triples;source/outputhashes;the descriptive ranges/medians;units;adoption flags;and finalverification.

- `notes/v7/example-selection.json`: `c8166b3bb06fc2116db5f3e7143c7ff0cb38d72beb8893a20eb66f0c12e650b1`
- `notes/v7/build_figure_sources.py`: `a79a4731897e0c0c81a5395fe0b59542fe675c9e9019cd0e02337ff2720aa24d`
- `notes/revision-v8/style_figures.py`: `f66037aa6bc3260cfeb786cf40f2c06bbfd125fd40b4deba0aa9b75a6292b666`
- `notes/v7/figure-sources/v7-endpoint-peak-example.tex`: `ddae5f3b55c23b62ebedef90e8491f5ba1d90d29407944052530917522c976c4`
- `results/revision-v8/wp3/summary.json`: `3de27c0f50a5b1882d4c8aba80d3fc8d2487972f22674d7e6e1423e62da663d0`
- `results/v9/nonstationarity/postrun/analysis/report.json`: `60fe5055d0d67c45fb40d4ccbf022f297ae4a6fa53c4b25d7098e19389661a04`
- `results/supervisor-20261023/inference/inherited-exact/murphy-fx_hourly-display.csv`: `39135edee084bb0dc14ed503ab343678544fd92ee94d5ad8ef0005f42776d26a`
- `results/supervisor-20261023/inference/inherited-exact/murphy-nyfed_weekly-display.csv`: `27b481fec14dac803866d977a06beacd597324cca6a3c7c839ef3e023c721c57`

Protected oldv8sources read only:

- `notes/v8/format_figure1.py`: `02f246def676243c33763444988b3bc1788e4828a95396f76e72f4a6c0324736`
- `notes/v8/figure1-format-check.json`: `5e3ca83c2224c5fc7ce6058cd018cea98861a77137c1db7cc96edb5c8fe7314d`
- `notes/v8/figure-sources/endpoint-peak.tex`: `66b50f95179b4e30b6f45089fb69877fa060729297e7e81b51ab7890d2e01169`
- `submission-jof/figures/v8-endpoint-peak-example.pdf`: `e327077121aa55484dd3415c5b8b808e904d2cb2dcad3caea5cd9926d6e2a546`

## Output hashes

- Builder: `2bcd8eec74cd3010239c843e8b0ac2c4c6514889be9043307870d0a11269b7f7`
- Scalar ledger: `c67faab6648b2a65b21ec196202f4d911f84e47ae5c6c290eb62ddddacf637a1`
- `submission-jof/figures/v9-endpoint-peak-example.pdf`: `cc65cdbf1dcf0c200cfd0630bcba9cca78c2afe53b4cc4c46a536c36d8005610`; adopted=True; PNG SHA=`45a045d2764e8871ca64281e0baa65222e86ac21e432d1210071655d3357791d`
- `submission-jof/figures/v9-simulation-comparison.pdf`: `4772ac1240e0eda8e9dea9ffea43f227ea650c2ecb3950b0f1acf0f95ded872f`; adopted=True; PNG SHA=`dcf8e1fcf473b9bf9b09ba153fce6cb84b99726e9a8bf2019464b192ec3e2952`
- `submission-jof/figures/v9-murphy-fx_hourly.pdf`: `4546d49e3d71f4640e66f57bd4cfb739368167f3a98683d696ddf05f65eba5a2`; adopted=False; PNG SHA=`b477e887081fb96758c93f6ec47742d4d70ccb3a6a49891eca56a832f29701f6`
- `submission-jof/figures/v9-murphy-nyfed_weekly.pdf`: `a307843aa90d7443db24f3237e310f1fb54d6833f6856b8f7d7d3ebfbac79898`; adopted=False; PNG SHA=`6ba6a721b2c35be82e41c00e9e533f72a6f77936ac7dc7c67e9da2f27cf7e81b`

## Verification boundary

Builder asserts protected manuscripts,oldv7/v8figures andowning researchsources unchanged before/after each rendering run. All researchsources andoldfigures still match at final check. During later independent artifact verification,the parallel manuscript author updatedsupplement.tex;this document-only later change is recorded separately in`scalars.json`,not misreported as builder output. No manuscript orsupplement write is performed by this builder. Matplotlibfontcache is ignored within the ownedfigureoutput directory.

## Caption handoff

Suggested simulation caption: Relative pinball loss of the full regression against matched historical headroom for a six-step target. PanelA shows all nine controlled stationary persistence settings,their range anddescriptive median;each setting is a ratio of mean losses over32repetitions. PanelB shows the median andinterquartile range across13calibrated source medians,each requiring32paired repetitions. The longer-history full summaries are unavailable with12of13sources complete ineach arm. The panels summarize different estimands anddo not isolate a causal mechanism.

Final scope adjustment: reader-name footer and explicit marker-offset clarification only; no further aesthetic or categorical-axis change. Final simulationPDF was re-rendered and viewed after this adjustment.
