# Endpoint marginals, path peaks and comparable scores

22 October2026. Directed closest-work rereading and elementary target arithmetic. No new forecast family, financial observation, score selection, fitted model, coverage claim or priority claim. Artificial finite laws below do not describe either source dataset.

## Consulted source and actual reading

Wisniewski, Lindsay and Lindsay, *Application of conformal prediction interval estimations to market makers' net positions*, [PMLR128:285–301,2020](https://proceedings.mlr.press/v128/wisniewski20a.html), official17-page proceedings PDF. The retained file has2,431,326bytes and SHA256b42f3abca77f5913499e59e2efdfc62b2b57e07faaca03fdc3fdd5d59a6d0bf2; the PDF internally numbers1–17. Root reread extracted text across all17pages, particularly Sections2,3.2–3.5and4.3; figures were not all visually audited or empirical tables/code reproduced. This is additional directed reading of an existing reference, not another distinct article. The official publisher metadata was reopened.

Its target is a signed next-hour position interval. Lagged positions, calendar/session inputs, rolling refitting, quantile/conformal/normalized-conformal variants and several regression engines already appear. Its interval evaluation averages lower/upper endpoint pinball losses. Those familiar operations predate this project; neither the new response nor a smaller implementation menu makes them new methods. The present input-byte identity and full-suite reproduction remain unestablished.

## Even complete issue-time marginals do not identify the peak law

Fix one issue, known current position0, two future records and tau19/20. Consider these two artificial predictive laws, conditional on the same fixed issue-time information:

| Future pair(N1,N2) | LawA probability | LawB probability |
|---|---:|---:|
| (0,0) |24/25|23/25|
| (10,10) |1/25|0|
| (10,0) |0|1/25|
| (0,10) |0|1/25|

In both laws each future coordinate separately equals0with probability24/25and10with probability1/25. Thus all one-dimensional future marginal distributions, not merely their .95quantiles, agree at this issue. Yet for P=max(0,abs(N1),abs(N2)), LawA has Pr(P=0)=24/25and LawB has23/25. Their ordinary .95peak quantiles are respectively0and10.

This proves a narrow information distinction: the vector's dependence matters. It does not say that identical full sequential conditional laws, including the information revealed at intermediate future records, can produce different joint laws. Nor does it rule out a distributional/scenario model that explicitly supplies that dependence.

For the fixed ordinary pinball score, expected losses at reports0and10are respectively19/50and12/25under LawA, versus19/25and23/50under LawB. Exact finite sums verify the change in optimal report without any MonteCarlo, calibration or financial computation. The example illustrates the response issue; it is not an empirical argument that direct peak regression must outperform a joint path model.

## Marginal information can still give a conservative peak bound

Suppose an issue-time procedure independently justifies

    Pr(abs(N_(t+h)) > c_h | F_t) <= alpha_h,

where every c_h is F_t-measurable. Set C=max(abs(N_t),c_1,...,c_H). Then

    {P_(t,H)>C} subset union_h {abs(N_(t+h))>c_h},

so the conditional union bound gives a peak exceedance probability at most sum_h alpha_h, without independence. Setting the sum at most alpha is sufficient. Merely assigning alpha to every horizon generally gives H*alpha, not alpha. In the artificial H2example, the common marginal .95report0has peak exceedance .04or.08; the .08case is compatible with the union bound and violates a claimed .05peak bound.

A separately justified simultaneous trajectory interval also maps to a peak bound by taking the largest absolute endpoint, as recorded in the [trajectory-envelope note](trajectory-envelope-and-peak-scope.md). These constructions give valid implications when their premises hold. They need not recover the least conservative peak quantile or minimize the present raw pinball score. No such marginal or trajectory guarantee is established for the current fitted financial reports.

## A central interval score is not a one-sided peak score

For L<=U and central miscoverage alpha, define

    IS_alpha(L,U;y) = U-L + (2/alpha)*(L-y)_+ + (2/alpha)*(y-U)_+.

The sum of ordinary pinball losses at probabilities alpha/2and1-alpha/2is(alpha/2)*IS_alpha; their average is(alpha/4)*IS_alpha. This follows by checking y<L, L<=y<=U and y>U; boundaries agree. At95percent central coverage, the probabilities are .025and.975, not one .95peak quantile. The identity is familiar score algebra, not a new result, and it applies to ordered endpoint reports on the same scalar outcome.

Consequently, published averaged endpoint pinball values cannot be ranked numerically against this study's single peak loss merely because both are called pinball and use USD. Outcome, tail functional, horizon, origins and scaling must agree before a method comparison is meaningful. Reproducing a source engine on our fixed peak labels is one way to obtain comparable reports; borrowing its endpoint table is not. The current matched QR/local comparisons do the former only for their bounded declared engines, not the full closest-paper model suite.

## Implication for the contribution

The changed response is mathematically meaningful but its peak/quantile operations are established. The supported empirical contribution is the same-target challenge and its complete adverse evidence, with known-floor, completed-label and update controls. It is not first financial path-risk forecasting, the invention of conditional quantiles, proof of a general direct-versus-path superiority or measured intervention value. This note changes no declared primary, current financial table, reference inventory or accepted manuscript result.
