# Validation-menu diagnostics and cross-source adaptation

This **post-result descriptive diagnostic** examines the already completed validation menu. It adds no model fit, parameter candidate, selection, evaluation or inferential test. All eight QR cells are shown, including unfavorable specifications; no favorable subset replaces a declared primary. Endpoint selection describes the boundary of this particular menu, not an incorrect model or evidence that a wider menu would improve forecasting.

## Inputs and independent reconciliation

The fixed [validation summary](validation-summary.csv) contains 72 candidate rows across 24 source/horizon/window/family cells. Standard-library CSV/decimal checks independently verified the complete cell inventory, three declared candidates per cell, COMPLETE status, source-native units, expected validation-origin counts and finite nonnegative mean losses. In every cell, the flagged selection equals the smallest loss, with the declared larger-parameter rule for an exact tie, and agrees with the SELECTED status/parameter in the [selection freeze](../../protocol/revision-20261022/selection-freeze.json). This scalar reconciliation does not repeat source/trace audits or establish predictive validity.

- Validation summary: 5,893 bytes; SHA-256 `7dc2c60085ceb31f701c6ba06b4a36cb6560c48aeeaad80be78eb460df9c9ae9`.
- Selection freeze: 10,040 bytes; SHA-256 `531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7`.
- [Study specification](../../protocol/revision-20261022/study-spec.json): SHA-256 `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0`.

## Every QR validation-loss profile

Entries reproduce the stored decimal strings for native mean pinball loss. **FX values are USD; Treasury values are USD millions.** They are not pooled or compared monetarily across sources. H and W count source records. “Interior” means the middle of the three declared lambdas, not an estimated optimum over a continuous parameter space.

| Source | H | W | lambda=0.001 | lambda=0.01 | lambda=0.1 | Selected lambda | Menu position |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FX | 6 | 720 | 492668.7218073945 | 474484.14003706095 | 483444.1584797041 | 0.01 | Interior |
| FX | 6 | 2880 | 452407.6922996637 | 449402.73877008253 | 452096.10824217787 | 0.01 | Interior |
| FX | 24 | 720 | 635015.0598105578 | 602921.2681086919 | 647029.9338587311 | 0.01 | Interior |
| FX | 24 | 2880 | 582035.5856921545 | 587654.5261525756 | 598006.0153988505 | 0.001 | Lower endpoint |
| Treasury | 6 | 52 | 12454.48723694224 | 10909.598525804087 | 9319.03031578235 | 0.1 | Upper endpoint |
| Treasury | 6 | 260 | 9632.855364451909 | 10298.513035148078 | 10254.267405374148 | 0.001 | Lower endpoint |
| Treasury | 24 | 52 | 30168.140839746957 | 31377.98659175543 | 31529.839868713407 | 0.001 | Lower endpoint |
| Treasury | 24 | 260 | 29590.357215542437 | 29785.540035811682 | 28534.89034727163 | 0.1 | Upper endpoint |

Five of eight QR selections lie at menu endpoints, including all four Treasury selections. This limits a claim that the fitted specifications exhaust ridge quantile regression. It does **not** show that the selected candidate is wrong, that the validation order is statistically stable, or that the next lambda outside the menu would help. The data provide no evaluated loss beyond the declared menu. Extending that menu after observing the evaluations would be another experiment, requiring separate versioning and an explicit design; no such extension or reselection occurs here.

## Overlap and the amount of validation information

Treasury validation uses 52 consecutive origins, indices 329–380, with H=6 or24. Each closed response window includes its issue observation and H subsequent observations. At H24, disjoint closed windows must have origins at least25 records apart. Within this 52-origin span, at most `floor(51/25)+1=3` such origins fit; the corresponding H6 count is8. These are geometric counts of nonsharing label windows, **not effective sample sizes of three or eight**. Shared training histories, time dependence and source behavior remain, and even disjoint label windows are not automatically independent.

The final H24 validation response ends at index404, before evaluation begins at405. Correct maturity prevents use of an unfinished label; it does not remove overlapping responses or create independent validation information. The loss profiles therefore identify the observed winner within each fixed menu, without confidence intervals for the selected lambda, a test of endpoint behavior or a causal explanation for later Treasury performance.

## What is fixed and what is adapted across sources

| Fixed procedural element | Predeclared source adaptation |
| --- | --- |
| Peak `P=max(|N_t|,...,|N_(t+H)|)`, known replay floor `B=|N_t|`, headroom `G=P-B`; H6/H24 | FX client-flow scalar versus aggregate Treasury-bill market-value positions; different units and calendar durations |
| Completed-label rule `i+H<=r`, chronological validation before evaluation | FX validation1440/evaluation6625 origins; Treasury validation52/evaluation277 origins; separate date ranges |
| Same 33 feature types, training-only centering/scaling and response-scale formula | Source-specific fitted transforms; RMS spans24/168 FX records versus6/26 Treasury records; nominal gaps3600/604800 seconds |
| QR objective, unpenalized intercept, lambda menu, floor projection, numerical acceptance and failure rules | W720/2880 and refit24 for FX; W52/260 and refit13 for Treasury |
| Same local-distance group weights, score preference and exact-tie rule | Source/window-specific neighborhood menus and separately validated parameters |
| Complete reporting and common-history/update controls | FX primary compares QR2880 with rolling F720; Treasury primary compares QR260 with frozen F260 |

The FX coefficients, scaler or selected model were **not directly moved to Treasury**. Each source was separately fitted and validated under its predeclared adaptations. The comparison concerns portability of a procedure family across two different measured prediction tasks. It is not transfer learning, one common replicated financial effect, compatible individual-dealer validation or an as-released public-information backtest. The downloaded-vintage issue convention and aggregation limits remain those in [EXTERNAL_DATA.md](EXTERNAL_DATA.md). This diagnostic leaves every accepted forecast, adverse result and scientific conclusion at its existing evidential scope.
