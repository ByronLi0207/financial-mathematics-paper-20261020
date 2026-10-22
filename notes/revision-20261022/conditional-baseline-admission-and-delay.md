# Admitting further conditional baselines without leaking unfinished labels

22 October 2026. This is a directed reading and design-boundary note. QRF and CAViaR remain unexecuted alternatives. No new model, parameter menu, score, hypothesis test or financial result is added, and no inspected evaluation is restored to unseen status.

## Sources and actual scope

Nicolai Meinshausen, *Quantile Regression Forests*, JMLR 7:983–999 (June 2006), [official published article](https://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf). The retrieved 17-page file has 799811 bytes and SHA256 `781a07fea0fadeec515ac0034a338efa66b234073cf5877e13ec08e5ffb2b882`. Root revisited selected Sections 3–4, Theorem 1/Lemma 2 and Section 5's evaluation description; physical page 5 was rendered and read for the CDF/algorithm. The earlier evidence map records selected pages 1–7. This is not an independent verification of every proof step, empirical table, software implementation or later forest-theory literature.

Robert F. Engle and Simone Manganelli, *CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles*, JBES 22(4):367–381 (October 2004), [DOI10.1198/073500104000000370](https://doi.org/10.1198/073500104000000370), [author-hosted published body](https://www.simonemanganelli.org/Simone/Research_files/caviarPublished.pdf). The retrieved 15-page file has 322942 bytes and SHA256 `39b926b9c40869d4ecf763c867a1660d29ebf785828b1311d84e88ed06e43f86`. Root revisited Sections 3–6, Appendix A's consistency/normality and out-of-sample conditions, and selected Appendix B arguments. Physical pages 3 and 8 were rendered and read for the recursions and assumptions. Existing reading is recorded separately. No source estimates, DQ test, global optimum or source-code reproduction is claimed.

The forest source estimates a response distribution using retained-response leaf weights. Its theorem has independent-observation and tree/distribution conditions. CAViaR models quantile dynamics using issue-known inputs; its stated asymptotic/DQ results impose additional information, density and limit conditions. Neither source theorem automatically covers our delayed overlapping headrooms or possible floor atom. Those source descriptions motivate the checks below, rather than a claim that either method is invalid or necessarily outperforms the current menu.

## Label maturity and recursive inputs are different questions

In the current economic-date replay, an issue follows observation of N_t. Its response is

    G_i = max_(0<=h<=H) |N_(i+h)| - |N_i|.

Absent extra information, the general completed-label boundary at issue t is i+H<=t. A fixed refit at r instead uses i+H<=r. Thus the latest generally completed headroom at issue t is G_(t-H), including the just-observed N_t. This is not an H+1 requirement: H+1 separates closed label windows, whereas label availability asks a different question. Original publication/revision timing can require further restrictions; the current replay convention does not solve Treasury's public-information clock.

For H>1, replacing a one-step return in an adaptive feedback rule with G_(t-1), its residual or its final hit usually reads the future. A concrete H2 example has the same history in two paths through issue t:

    N_(t-2)=0, N_(t-1)=0, N_t=1.

Let the next value N_(t+1) be 1 in path A and 9 in path B. Then G_(t-1) is respectively 1 and 9. The two inputs cannot be distinguished from issue-t information alone, although the historical evaluation table eventually contains both labels. This is an artificial indexing example, not observed financial data or a measured frequency of leakage.

The previously issued report q_(t-1) is different: it is already known even though its future outcome is not. Raw position changes such as |N_t-N_(t-1)| are also known under this observation convention. Consequently, a small symmetric-absolute-value-style quantile recursion can use causal raw inputs and mature fitting labels. It would be wrong to exclude every autoregressive quantile model because one particular hit-feedback substitution is unavailable.

A future implementation must separately declare parameter refits, report-state updates between refits, and feedback when labels mature. Refitting only on mature outcomes does not cure a state recursion that has already consumed unfinished labels. Conversely, updating a report state with genuinely known inputs between refits need not be leakage if that update is explicitly part of the fixed procedure. The initialization history, scale, sign convention, upper .95 target, floor projection and reset policy all matter. They cannot be supplied by copying the source's lower-return-tail notation.

## A forest quantile is not a quantile of tree means

For the same nonnegative completed labels, let a future fitted forest supply weights w_i(x)>=0 summing to one. Define the weighted empirical distribution and its ordinary upper quantile by

    Fhat(g|x) = sum_i w_i(x) 1{G_i<=g},
    q_.95(x) = inf{g: Fhat(g|x)>=.95}.

This finite construction selects a nonnegative value on the positive-weight label support. Therefore C_t=|N_t|+q_.95(x_t) obeys the known replay floor. That deterministic feasibility statement is not conditional coverage or a consistency theorem.

For an artificial example, suppose every relevant tree leaf contains responses {0,10} with equal weights. All leaf means are 5, so the .95 quantile of those tree means is 5. The retained-response weighted CDF instead gives .95 quantile 10. The methods answer different questions; ordinary mean-forest output does not implement the latter distribution estimator.

General forest weights also do not define a single uniform neighbor count k. The current local baseline's ceil((k+1)*.95) rule cannot simply be pasted into a weighted CDF. Even with exactly uniform weights, the ordinary empirical CDF definition gives ceil(k*.95), subject to ties, rather than automatically applying the add-one rank. A separate weighted conformal construction would require its own calibration definition and assumptions; it is not supplied here.

Monotonicity in the quantile probability is also different from monotonicity in H. Separately fitted horizon forests need not issue ordered reports. An elementary sufficient construction would retain the same eligible historical origins, the same nonnegative weights and the same-unit headrooms at both horizons. Since G_(i,H2)>=G_(i,H1) when H2>=H1, the weighted CDFs then satisfy Fhat_H2(g)<=Fhat_H1(g), so their ordinary quantiles are ordered. Adding the common query floor preserves that order. This is a finite CDF implication, not a new method, an executed forest, a coverage theorem or evidence of better score. A common pool must be mature for the longest horizon and can change the information/comparison problem; it cannot be silently substituted for the existing horizon-specific pools. The current adverse crossings are retained without repair.

Chronological validation with matured responses must replace any casual reuse of random-fold or ordinary out-of-bag scores as a deployment evaluation. Trees, bagging weights, leaf sizes, feature subsampling, seeds and quantile conventions need a fixed specification. This note makes no claim about which permitted setting would win. It also makes no claim that the original forest paper's empirical evaluation was inappropriate for its own data.

## Numerical and evidential admission

The source's CAViaR implementation uses multistart nonlinear optimization. This would require a declared finite starting set, initialization, stopping and failure rules within this project's resources; the existing convex QR certificate cannot be relabeled a certificate for a different recursive objective. Reproducing a source's large starting-point search is not authorized by merely citing that method. No new optimizer is installed or run here.

The following conditions are required before a later baseline can become a meaningful new comparison:

| Admission question | What must be fixed before new results |
|---|---|
| Same response | The identical source, peak/headroom, issue floor, horizon and eligible origins |
| Causal inputs | Exact raw-input availability and completed-label feedback, including refit and state-update clocks |
| Fitted procedure | Transformations, initialization, finite tuning menu, random state, empirical quantile convention and numerical failure rule |
| Fair comparison | Declared historical/conditional references and score, breach severity, floor and horizon diagnostics |
| Selection history | Explicitly exploratory reuse of inspected records, or a genuinely unseen compatible evaluation of the whole procedure |
| Resources | Existing one-process limits, no installation, measured memory/threads/time, and complete failed as well as successful cases |

These checks do not require a population assumption to be empirically proved from one finite archive. They do require assumptions to be stated and their applicability defended before statistical guarantees are invoked. An engine can be evaluated descriptively without inheriting its original theorem. Nor does passing an implementation check establish financial value.

## Decision

Keep the current bounded model-validation paper and its complete adverse evidence. The tested QR/local/mean-AR menu is a substantive improvement over the original historical-only challenge, while remaining a limited menu. No family is added merely to rescue an inspected outcome, and neither proposed alternative is selected as a future winner. A stronger subsequent study should freeze the complete family-selection procedure and obtain compatible unseen information, an admissible release clock or a decision-linked outcome. More same-sample models alone cannot supply those missing axes.
