# Finite-rank feasibility in a related conformal ES-path paper

Date: 2026-10-22.

## Source, version, and reading scope

Çağlar Sözen, *Monotone forward expected shortfall paths with joint conformal calibration*, **AIMS Mathematics** 11(9), 27665–27688 (2026), [doi:10.3934/math.20261106](https://doi.org/10.3934/math.20261106). The journal PDF states: received 6 November 2025; revised 25 February 2026; accepted 3 March 2026; published 1 September 2026.

The checked artifact is the 24-page journal PDF stored locally at `.scratch/revision-20261022-novelty-sources/sozen-es-paths-2026.pdf`: 839,211 bytes; SHA-256 `e06cb174182d64e5ce2c31369ef6f7adc2060368232ccf9cca8ccc6416c73a18`. These conclusions refer to that exact artifact, rather than an unspecified subsequent version.

Reading depth: selected full-text passages, not a complete reading of all 24 pages. Checked physical pages 1–2 (bibliographic identity and introductory target qualification), 5 (shape-constraint qualification), 8 (framework and validity summary), 11 (order-statistic rule and Theorem 4.1), 12 (Šidák/Bonferroni allocations and block calibration), 14 (main sample sizes and calibration settings), and 19 (interpretation and limitations). Physical page 11 corresponds to printed page 27675; physical page 12 to 27676; physical page 14 to 27678.

The root review additionally read the extracted text on physical pages 3–24, revisited the sample-size and appendix tables on pages 14 and 23, verified the title-page metadata, and rendered and visually checked page 11. This does not claim a full visual audit of every figure or any execution of the author's code. A separate mathematical reader checked the rank argument and the stated 174/17-unit settings independently.

The author's implementation has **not** been inspected or executed in this audit. No empirical table has been reproduced or recalculated. The calculations below concern the mathematical rule and settings stated in the checked PDF.

## The finite-rank issue

The paper defines its order-statistic calibration rule using

```math
k_0=\left\lceil(1-\alpha)(n+1)\right\rceil,
\qquad
Q_{1-\alpha}^{\mathrm{OS}}=u_{(k)},
\qquad
k=\min\{n,\max\{1,k_0\}\}.
```

Theorem 4.1 then states the nominal path-coverage guarantee under exchangeability of the calibration and future path scores, with the predictor and postprocessing fixed before calibration. The displayed theorem does not additionally restrict \(n\) and \(\alpha\) to make the required rank available.

For \(0<\alpha<1\), the required finite rank is available precisely when

```math
k_0\le n
\quad\Longleftrightarrow\quad
(1-\alpha)(n+1)\le n
\quad\Longleftrightarrow\quad
\alpha\ge\frac{1}{n+1}.
```

When this condition fails, \(k_0=n+1\). Replacing that rank by the largest available finite calibration score does not, in general, preserve coverage at least \(1-\alpha\). This is a missing feasibility condition for the stated combination of rule and general guarantee.

### Elementary exchangeable-rank argument

Suppose \(R_1,\ldots,R_n,R_{n+1}\) are exchangeable and almost surely distinct. The rank of \(R_{n+1}\) among all \(n+1\) scores is uniform on \(\{1,\ldots,n+1\}\). For a calibration order statistic \(R_{(k)}\) with \(1\le k\le n\),

```math
\Pr\{R_{n+1}\le R_{(k)}\}=\frac{k}{n+1}.
```

In particular, for an available rank \(k_0\), rounding upward gives \(k_0/(n+1)\ge1-\alpha\). With ties, an auxiliary random tie-breaking order yields the same uniform-rank argument, while the non-strict score comparison can only increase coverage relative to that randomized rank event.

If an unavailable rank \(n+1\) is clipped to \(n\), the continuous case instead gives exactly

```math
\Pr\{R_{n+1}\le R_{(n)}\}=\frac{n}{n+1}<1-\alpha.
```

This argument is a simple check of the finite-sample statement. It is not a new conformal method or a new methodological contribution of the present project.

### A counterexample within the stated score assumptions

Let \(n=2\), \(\alpha=0.1\), and let the calibration and future scores be independent \(U(0,1)\) variables. The predictor and scale can be fixed in advance. The required rank is

```math
k_0=\lceil0.9\times3\rceil=3,
```

but the clipping rule uses \(k=2\). Thus

```math
\Pr\{R_3\le\max(R_1,R_2)\}=\frac23<0.9.
```

This construction can also be embedded in the paper's nonnegative path-score representation: take a fixed zero predictor, unit scales, and the same nonnegative uniform label at every horizon. Such a path is monotone, so a monotonicity requirement does not exclude the example. This is a mathematical counterexample to the unqualified general guarantee with clipping; it is not an empirical claim about financial ES labels.

## Exact ranks in the paper's main settings

The main settings reported on physical page 14 are \(H=20\), \(\alpha_{\mathrm{conf}}=0.1\), and \(n_{\mathrm{cal}}=174\). The nonoverlapping block rule on physical page 12 drops an incomplete trailing block. At block length 10, 174 raw calibration records therefore supply 17 complete blocks, with four records omitted from that block construction.

For the horizon allocations,

```math
\alpha_B=\frac{0.1}{20}=\frac1{200},
\qquad
\alpha_S=1-0.9^{1/20}
\approx0.00525417406947.
```

| Calibration unit count \(n\) | Rule | Required rank \(k_0\) | Rank after clipping | Required rank available? |
|---:|---|---:|---:|---|
| 174 | Global, \(\alpha=0.1\) | 158 | 158 | Yes |
| 17 | Global, \(\alpha=0.1\) | 17 | 17 | Yes |
| 174 | Bonferroni, \(\alpha=1/200\) | 175 | 174 | No |
| 174 | Šidák, \(\alpha=1-0.9^{1/20}\) | 175 | 174 | No |
| 17 | Bonferroni, \(\alpha=1/200\) | 18 | 17 | No |
| 17 | Šidák, \(\alpha=1-0.9^{1/20}\) | 18 | 17 | No |

For example, the raw Bonferroni rank is \(\lceil175\times199/200\rceil=\lceil174.125\rceil=175\). The global ranks are \(\lceil175\times0.9\rceil=158\) and \(\lceil18\times0.9\rceil=17\).

Consequently, the specific rank-clipping defect does **not** activate for the main global rule at either of these calibration-unit counts. The counterexample above therefore does not overturn the reported global empirical results.

For the two allocated rules in these settings, both required ranks exceed the available finite rank and both are clipped to the sample maximum. Their equality is thus more specifically explained by common upper-end saturation. Finite-sample discretization is a broader description, but describing this case only as an incidental shared interior grid rank would omit the active truncation mechanism. This conclusion is conditional on applying the rule printed in the paper; it is not evidence that the author's actual code or tables used a different rule or contained a computational error.

## Minimum calibration-unit counts

For Bonferroni, rank feasibility requires

```math
\frac1{200}\ge\frac1{n+1},
```

so the smallest feasible count is **199**.

For Šidák, the equivalent exact condition is

```math
\frac{n}{n+1}\ge0.9^{1/20}
\quad\Longleftrightarrow\quad
\left(\frac{n}{n+1}\right)^{20}\ge\frac9{10}.
```

Exact rational arithmetic gives

```math
\left(\frac{189}{190}\right)^{20}<\frac9{10},
\qquad
\left(\frac{190}{191}\right)^{20}>\frac9{10}.
```

Since \(n/(n+1)\) increases with \(n\), the smallest feasible count is therefore **190**. These counts refer to the units entering the corresponding quantile. When calibrating block maxima, they are counts of complete calibration blocks, rather than counts of raw daily observations. They establish rank feasibility only; they do not establish exchangeability, appropriate future-score comparability, independence across horizons, or empirical performance.

All reported integer ranks and the 199/190 boundaries were checked with exact rational arithmetic. The decimal Šidák level is supplied only for readability. The [root arithmetic record](finite-rank-feasibility-check.json) additionally enumerates the six equiprobable rank orderings in the two-calibration-score counterexample and checks every declared history/neighbor count in the current frozen study specification. No simulation, financial values or neighboring-paper result tables enter that calculation.

## Repairs and limits of the conclusion

The rule and theorem can be reconciled by adding the condition \(\alpha\ge1/(n+1)\), or by treating the unavailable \((n+1)\)-st score as \(+\infty\) and returning an infinite upper threshold when necessary. An implementation may instead reject an infeasible finite-rank request and report insufficient calibration size. Clipping to the largest finite score should not retain an unconditional claim at the original nominal level. These are corrections to the mathematical specification; this audit does not determine which repair the author would choose.

The article already makes several relevant qualifications that must be retained fairly:

- It explicitly treats monotonicity as a design constraint on the reported target representation, rather than a universal property of every horizon-specific ES definition. It also discusses potential distortion under mean reversion or rapid volatility normalization. The finite-rank finding supplies no basis for accusing the article of omitting that distinction.
- It distinguishes the canonical exchangeability guarantee from chronological time-series evaluation, and describes block-maxima calibration as a practical mitigation rather than a general proof of validity under dependence. Feasible global ranks alone do not turn that heuristic into an exact time-series guarantee. In particular, a calibration block maximum and a future single-record score should not silently be treated as identically distributed units.
- Its discussion of Šidák includes the independence motivation and dependence limitations. Even after rank feasibility is repaired, those separate assumptions still matter for a joint-coverage argument.

This note establishes a limited mathematical specification issue and its exact activation in the printed horizon-allocation settings. It does **not** establish an error in any empirical table, observed financial harm, or the superiority of the present project's method. It adds no new financial data or experimental results. Nor should a weakness in this neighboring paper be used as a substitute for demonstrating the present project's own novelty against the broader literature.

## Implication for this project's scope

The present project's corrected rank is `ceil((W+1)*19/20)`, or the corresponding neighbor-count rank, with unavailable finite ranks rejected rather than clipped. Its smallest retained neighbor count is 20, so the finite-rank requirement is met at the stipulated 0.05 level. This is only an arithmetic feasibility check. The historical overlapping records and selected neighboring labels have not been shown to be exchangeable with a future target, so an available corrected rank still supplies no 95% coverage guarantee here. The paper remains a descriptive same-target comparison. The most direct empirical lineage remains signed endpoint forecasting on market-maker positions; the ES-path paper studies a different response, and this finite-rank issue does not create priority for the current application.
