# B4 technical guard for the prose rewrite

Source inspected: frozen `.scratch/v8/manuscript-before-b4.tex`. Scope is mathematical meaning, evidence scope and the eight mandatory limitations, not stylistic scoring. No experiment, source rewrite or Git operation was performed in this audit.

The current v8 instruction governs placement: concentrate the eight empirical limitations once in the Limitations section. It supersedes the older writing guide's instructions to repeat some in the abstract/evaluation/conclusion. The current limits are mean sentence length at most20 words and body at most18 pages; the older guide's25-word/15-page targets do not control this task.

## Mathematical and methodological invariants

|Frozen source lines|Meaning that must survive compression|
|---|---|
|85-96|The target is the **sampled absolute-position peak**, `Y_(t,H)=max_(0<=h<=H)|N_(t+h)|`. It includes the issue position, contains H+1 records, has known floor `B_t=|N_t|`, and headroom `Z=Y-B>=0`. H counts source records: six hourly records and six weekly records have different time spans.|
|95-103|Score peak minus capacity using pinball loss `rho_tau(u)=tau*u_+ +(1-tau)*(-u)_+`. The study uses tau19/20. A breach is strictly `Y>C`, not `Y>=C`. Error amounts and breach counts answer different questions.|
|99-103|Floor projection assumes `Y>=B` and B belongs to issue information. Its pathwise gain is exactly `tau*(B-c)_+`. The probability inequality applies to the **true conditional lower inverse quantile**, not an estimated QR forecast. Atoms can make strict exceedance smaller than alpha.|
|106-113|The classical Levy bound assumes independent future increments, each symmetric about zero, and the population `(1-alpha/2)` quantile of **absolute endpoint displacement** `|S_H|`. Preserve the factor2 and strict inequalities. Identical distributions and finite moments are unnecessary. Conditional application needs these premises under the conditional law. An empirical endpoint plug-in is a separately scored procedure.|
|116|Horizon nesting concerns peaks with a common origin and information set. Separately estimated reports can cross. The640-origin crossing result remains evidence of forecast incoherence, not incorrectly nested targets.|
|136-165|Retain the method identities: F is current floor plus corrected empirical headroom rank, S translates completed signed paths, K projects a historical peak quantile to the floor, L uses absolute endpoint displacement. QR has ridge slopes and an **unpenalized intercept**,33 predictors before intercept, training-based feature/response scaling, and the declared lambda menu. QR4 has signed/magnitude level and short/long past RMS.|
|165,172-175|History counts **completed labels**. At refit r the training pool is `[r-H-W+1,...,r-H]`, so every label ends at or before r. Current floor/query use actual issue t; transforms and estimates remain fixed within the refit block. Refit intervals are24 FX/13 weekly. Validation precedes evaluation; selected tuning remains fixed while mature pools update.|
|175,203-214|The original FX rolling reference uses the shorter history; matched FX uses the same history/refit schedule. Do not merge their losses or breach counts. Unwrapped matched comparison is376/360, whereas the shorter rolling-reference comparison uses376/332. Wrapped comparison is329/328.|
|178,258-280|HAC loss-difference tests, equality-based hit tests, transition likelihood and state diagnostics have different nulls. Spacing reduces overlap but does not make the observations independent. Keep the conditional-transition initialization, bandwidth/multiple-comparison family definitions and atom distinction in the relevant method/table/Supplement location.|
|294-324|Calibrated simulation has H6 only,100 repetitions and500 origins per complete cell;2000 oracle paths are a finite approximation. D0 is a constant-variance AR control with state information. All seven failed hourly cells remain unavailable, not statistically losing cells. P1/P3 are unsupported, P2/P4 unassessable. Frequency and validation length are bundled by DGP.|

The exact solver objective, ranks and detailed inference formulas may remain in the Supplement, but the body must continue to describe their executed meanings correctly. I uses the ordinary empirical rank `ceil(19W/20)` and F uses `ceil(19(W+1)/20)`; infinity in the Monte Carlo QR menu selects I. Do not call a selected infinity fit evidence of fitted predictor slopes.

Display percentages to one decimal without changing the underlying archived values. This does not authorize rounding p-values, tau, lambda, H/W, counts, or frozen prediction thresholds. Named comparisons must retain their original denominators. Figure/table references and author placeholders remain intact.

## Canonical location for the eight empirical limitations

Use the existing `sec:limitations` location, frozen lines330-338, as the single canonical home. Three short paragraphs can accommodate all eight facts, plus genuinely distinct measurement/inference boundaries.

|Required limitation|Current evidence/duplication|Canonical placement and content|
|---|---|---|
|1. Single FX market maker|Data123/129; literature-table source description; Limitations332|First limitations paragraph: evidence concerns one market maker's client-flow record. Data-source identity may remain a neutral description elsewhere; remove repeated external-validity warnings.|
|2. Original FX evaluation was already viewed|Transparency183 and Limitations332|First paragraph: original FX outcomes were viewed before conditional methods were specified. Keep this explicit rather than replacing it by the vague word retrospective.|
|3. Earlier2015 comparison is retrospective|Transparency183 and Limitations332 only imply part of it|First paragraph: explicitly name the earlier2015 comparison and state that its rules followed the original results. It is not a prospective test. Familiar source history alone does not fully state this limitation.|
|4. Weekly categories share reporting system|Data126/129; table235; Limitations335|Second paragraph: related weekly series share the reporting system and economic components, so they are related tasks rather than independent institutions.|
|5. Treasury is a downloaded-vintage replay|Data129 and Limitations335|Second paragraph: Treasury uses the downloaded-vintage economic-date series; historical publication-time vintages were not reconstructed. Do not label it a live historical-information test.|
|6. No causal explanation|Table316 only rules out a causal **frequency** effect; global statement is absent|Third paragraph: model, feature and source comparisons do not identify causal mechanisms or individual-predictor effects. Add an explicit global statement.|
|7. No coverage guarantee|Theorem/empirical distinctions are implicit across113/198/338|Third paragraph: the executed financial forecasts and finite delayed wrappers carry no established coverage guarantee. Do not replace this with the stronger false claim that all quantile/bound theory lacks guarantees.|
|8. No measured trading/funding gains|Limitations335/338 discuss decision costs indirectly|Third paragraph: the study does not measure trading or funding gains. Keep both terms explicit; a lower quantile loss is not an observed economic payoff.|

The frozen text does not yet explicitly satisfy6-8, and3 needs its chronological reason stated more directly. The rewrite should supply these once rather than merely deduplicate existing wording.

## Theorem premises are not duplicate empirical caveats

Keep the mathematical assumptions next to the propositions and the label-admission rules next to the method. Independence/symmetry conditional on issue information, the population endpoint quantile, measurable floor, strict exceedance and atoms define when statements are true. Removing them to reduce a caveat-word count would change the mathematics. Short active formulations can state them directly.

By contrast, repeated statements about single-source scope, already seen outcomes, retrospective design, shared reporting, vintage reconstruction, causal identification and economic value can move to the canonical limitations paragraphs. Later result paragraphs can lead with findings and point to their named tables without repeating these research-history warnings.

The score's19:1 evaluation weights, offsetting net exposures, between-record excursions, calibration-parameter uncertainty and unadjusted/working-reference inference are additional distinct boundaries. They can remain briefly in their natural method/Supplement location or the same Limitations section; do not imply that the eight-item list exhausts all assumptions. A result describes what happened under the executed procedures; the scope paragraph states what those comparisons can establish.
