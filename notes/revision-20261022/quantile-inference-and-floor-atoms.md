# Conditional quantile inference and the known-floor atom

22 October 2026. This is a direction-first return to an existing original source, prompted by the missing inferential contribution in the current comparison. It changes no forecast, parameter, primary, evaluation sample or experiment. No confidence interval, encompassing test, forecast combination or strategy selector was run.

## Actual primary-source reading

Raffaella Giacomini and Ivana Komunjer (2005), **Evaluation and Combination of Conditional Quantile Forecasts**, *Journal of Business & Economic Statistics* 23(4), 416–431, October. [DOI:10.1198/073500105000000018](https://doi.org/10.1198/073500105000000018); [CaltechAUTHORS journal-layout body](https://authors.library.caltech.edu/records/cx897-csm79/files/RAFjbes05.pdf).

Root revisited the cached 16-page journal-layout body: physical pages 1–7, 10–12 in extracted text, and pages 5 and 12 in full-page rendered views. The selected passages include the finite-memory forecast environment, tick-loss encompassing definition, conditional moment construction, Propositions 1–2, Theorem 1, smoothing/variance implementation and the start of supplied proofs. This is selected reading, not a new acquisition, full-paper audit, proof certification or replication. The cached PDF has 632,821 bytes and SHA-256 `bf6234787c5befe3b2c2b971877baff7e0eed0726da7968ee4109441e4f920d2`; the third-party PDF remains outside public delivery. Earlier reading records remain in source-register-09 and the 21 October combination notes; this revisit does not count an additional distinct paper.

The theorem does more than compare two mean loss numbers. It defines conditional encompassing through the best combination and estimates weights with moment conditions, using issue-known instruments. It permits finite-memory forecasting methods and retains their estimation uncertainty as the evaluation period grows. Its stated assumptions include a continuous, strictly positive conditional density, stationary mixing variables with sufficient moments, nondegenerate instruments and forecast noncollinearity; the asymptotic-normality result adds further conditions. Its variance discussion distinguishes full-information martingale moments from more general HAC estimation when the chosen instruments omit relevant information. Its own smoothing calculation and size/power experiment do not supply a universal bandwidth or finite-sample guarantee for another application.

## An elementary response-specific obstruction

The following is our own conditional-loss calculation, not a new theorem or an allegation about the original article. For a response Y with finite first absolute moment, conditional distribution F and a fixed issue information set, let

`R(c)=tau*E[(Y-c)+ | issue] +(1-tau)*E[(c-Y)+ | issue]`.

The left and right derivatives are respectively `F(c-)-tau` and `F(c)-tau`. Thus a quantile minimizer satisfies `F(c-)<=tau<=F(c)`. This permits atoms and nonunique quantile sets. It does not generally require the strict exceedance probability to equal `1-tau`.

Here the response is `P=max(|N_t|,|N_(t+1)|,...,|N_(t+H)|)` and B=|N_t| is issue known. Whenever the future recorded path stays within [-B,B], P equals B exactly. Even continuous future signed observations can induce an atom in the conditional peak distribution at B. For a logical H1 example, fix N_t=1 and let the next signed observation be uniform on [-2,2]. Then P has mass 1/2 at B=1. This example is not a fitted financial process. More generally, if conditional floor mass reaches tau, B itself can minimize expected pinball loss with a strict exceedance probability at most 1-tau (strictly below when that mass exceeds tau).

The response transformation therefore does not automatically satisfy the cited smooth-density setup. Whether the actual relevant quantile is above a floor atom, whether a compatible local density exists there, and which alternative inference framework is valid require separate analysis. The archive's observed zero-headroom counts are descriptive and do not estimate every issue's conditional floor probability. Likewise, short-window KNN with k=W equals its historical F control exactly, so attempting an encompassing test of that pair would also conflict with the source's noncollinearity premise.

## Direction decision for this manuscript

Keep the current score and breach summaries descriptive. A lower sample pinball mean is not conditional encompassing, successful calibration or a forecast-combination recommendation. Removing overlapping target records on one sparse grid does not establish stationarity, mixing, a moment condition, valid variance estimation or a sufficient number of independent observations. Repeated fitting and an already inspected sample also remain part of the method/evidence history.

A future inferential extension would first define its estimand and null: unconditional average loss, selected conditional moments, absolute quantile calibration and encompassing are different questions. It would then justify assumptions for this known-floor response, label maturity, refit schedule, selection and dependence, before choosing a variance or resampling procedure and inspecting a new outcome. Adding a familiar Wald statistic or p-value during polishing would not close those gaps. The current omission limits inferential strength; it is not repaired by arithmetic reproducibility, another mature model or a larger reference list.
