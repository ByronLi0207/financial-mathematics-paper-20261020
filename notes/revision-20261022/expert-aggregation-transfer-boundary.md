# Expert aggregation: the loss and information must transfer too

22 October 2026. A directed return to the closest author/citation chain, after the current conditional and AR evaluations. This note adds no forecast, metric, selected model, confidence interval or financial experiment. Its elementary examples are artificial. Neither they nor a longer reading record establish a new method or priority for this paper.

## Sources actually consulted

- Wisniewski, Kalnishkan, Lindsay and Lindsay, *Temporal distribution of clusters of investors and their application in prediction with expert advice*, [arXiv:2406.19403v1](https://arxiv.org/abs/2406.19403v1), 4 June2024. Root read extracted text across all20 physical pages of the retained v1, including the clustering definitions, investment-loss construction, experiments and artificial duplicate-expert appendix; physical p14 was rendered and visually inspected. This extends earlier selected reading, rather than adding another distinct paper. Figures were not all visually audited and results/code were not reproduced. The 4,318,866-byte PDF has SHA-256 `58fdb9215f9291aa9d1412dd726c09874a4caa5b7f524de7f52253548e1223c5`. The consulted experiments concern clustered trader decisions and portfolio performance, not peak-quantile scores. Its discussion of large scaling factors and bankrupt/stopped experts must accompany its favorable cases. The formal2026 chapter body was not compared with v1.
- Al-Baghdadi, Lindsay, Kalnishkan and Lindsay, *Practical investment with the long-short game*, [PMLR128:209–228](https://proceedings.mlr.press/v128/al-baghdadi20a.html), 9–11September2020. The publisher record's author order differs from the PDF cover's Al-Baghdadi/Kalnishkan/Lindsay/Lindsay order; the retained20-page PDF internally numbers1–20. Root read selected physical pp1–8,9–15 and19–20, and visually inspected p4's substitution condition and Lemma2. It distinguishes mixable bounded investment games from a general game, discusses loss modifications, and evaluates portfolios. It does not supply a pinball-forecast guarantee. PDF:1,339,368bytes, SHA-256 `b13f7a2849ee680c69a89b2cb53f04ffc405ce83326f17b3245450f6599c263b`. Remaining experiment figures were not audited and no source computation was reproduced.
- Biau and Patra, *Sequential Quantile Prediction of Time Series*, consulted [arXiv:0908.2503v2](https://arxiv.org/abs/0908.2503v2),31May2010, rather than claiming final-journal-body equality. Root reread physical pp1–10 and14–23, including the full-history expert construction, Theorem3.1, Lemmas5.2–5.4 and displayed proof route. External ergodic/nearest-neighbor results used in that route were not independently certified. PDF:683,438bytes, SHA-256 `0eb17c666c19086339e51c5560249c4d5f767e0e1d8435d3e97ad37286bbb24c`. Its consistency result has stationarity/ergodicity, moment, regularity, truncation, learning-rate and growing-history premises. The practical finite grid is distinguished from the theoretical infinite family. The full strategy is not implemented here.
- Gneiting, *Making and Evaluating Point Forecasts*, [DOI10.1198/jasa.2011.r10138](https://doi.org/10.1198/jasa.2011.r10138). Root reread formal-body physical pp9–14, particularly §3.3, Theorem9, discussion and the displayed proof pointers. This revisits an already-read reference. PDF:227,162bytes, SHA-256 `70a05706f94d82ef1e59435a3c64e25a168815ba9a693c6f3ae2a95a4631c55b`. Consistent scoring identifies optimal quantiles under the stated integrability conditions; it does not give a metric-independent ordering of imperfect forecasts.

No original PDF, source figure, trader identifier or observation file is part of this note's public delivery.

## An elementary obstruction to borrowing the investment bound

Use pinball loss in report/outcome notation,

```math
S_\tau(c,y)=\tau(y-c)_+ +(1-\tau)(c-y)_+,\qquad0<\tau<1.
```

Ordinary unit-factor mixability would require, for any expert reports and weights, a report whose loss is bounded for every outcome by the negative log mixture of exponentiated expert losses. Consider equal weights on the two artificial expert reports0 and1, possible outcomes0 and1, and an issue-known floor0. These are feasible nonnegative peak/report values; no financial observations enter the example.

For any positive learning rate eta, the mixture bounds at the two outcomes are

```math
g(0)=-\eta^{-1}\log\{(1+e^{-\eta(1-\tau)})/2\}<(1-\tau)/2,
```
```math
g(1)=-\eta^{-1}\log\{(1+e^{-\eta\tau})/2\}<\tau/2.
```

Strict Jensen inequalities give the strict signs. For a candidate report in[0,1], the first requirement forces c<1/2 and the second forces c>1/2. A report above1 already fails at outcome0; even allowing a negative report would fail at outcome1. Thus no substitution satisfies both bounds. Pinball is not ordinarily eta-mixable with multiplicative constant1, already on these two outcomes.

This standard elementary check was independently reviewed; it is not a new theorem, an allegation about the cited investment results, or a claim that all quantile aggregation is impossible. It prevents transferring the corresponding unit-factor, fixed-eta logarithmic-expert-count guarantee merely because both applications use exponential expert weights. Convex averaging still satisfies

```math
S_\tau\!\left(\sum_jw_jc_j,y\right)\le\sum_jw_jS_\tau(c_j,y).
```

That weighted-mean inequality is different from the stronger log-mixture inequality. It does not promise superiority over the best expert or calibrated tails. Same-floor reports retain the floor under such averaging, but that deterministic feasibility is also distinct from predictive adequacy.

## A peak transformation does not itself prohibit asymptotic prediction

For fixed finite H, let `Z_s=max_(s-H<=j<=s)|N_j|`. If the primitive process N is strictly stationary and ergodic, the measurable shift-equivariant finite-window process Z has those properties. If `E[N_0^2]` is finite, then

```math
E[Z_s^2]\le(H+1)E[N_0^2].
```

These elementary implications were independently checked. They do not verify those assumptions for the present records. Nor do they supply conditional-CDF regularity, the source algorithm or its growing-history conditions. An atom is not by itself equivalent to failure of strict increase or uniqueness; the relevant quantile/distribution and theorem premises have to be examined.

At issue t the current target is `Z_(t+H)`, so writing a backward-window series does not convert the task into next-observation prediction. Intervening Z values generally contain future N observations. Past Z also need not retain the signed-position information in past N. A theorem for forecasting from one scalar series' past cannot silently become an optimality theorem for a different horizon and information set. This is why the source result is not inherited by the current finite QR/KNN menu; it is not a categorical ban on a properly designed delayed-feedback aggregation study.

## Same quantile does not mean the same finite forecast ranking

For two artificial records, take `(y,A,B)=(0,1,0)` and `(10,10,9)`, all with known floor0, and tau19/20. Ordinary pinball mean losses are1/40 for A and19/40 for B, a difference of−9/20.

Now use the strictly increasing function `q(c)=c+19min(c,1)` on nonnegative values and the generalized quantile score

```math
S_{\tau,q}(c,y)=(1\{c\ge y\}-\tau)\{q(c)-q(y)\}.
```

Here q(0),q(1),q(9),q(10) are0,20,28,29. The mean scores become1/2 for A and19/40 for B, reversing the difference to1/40. Both scores are consistent for the same quantile functional under their integrability conditions; an ideal quantile does not lose that property. The example only shows that two imperfect methods need not have the same ranking across all consistent scores. It uses no present forecast and selects no alternative evaluation loss.

The current study's native-unit linear pinball preference remains fixed. It is appropriate to state results under that preference while withholding claims of universal score dominance or measured financing benefits. Changing the scoring transformation after seeing financial rankings would be a new analysis decision.

## Disposition

Keep the current mature-method benchmark and its adverse cases. Neither a portfolio-aggregation method name, a consistency theorem for another information structure nor a different consistent score repairs the current missing compatible dealer validation or decision-cost evidence. A new aggregation experiment would first fix experts, loss, available feedback, learning-rate/scale rule, failures, comparators and evaluation; none was run here. The separately followed public-data citation is assessed in the [data-feasibility follow-up](longshort-data-feasibility.md).
