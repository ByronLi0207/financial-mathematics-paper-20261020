# Horizon rearrangement: pooled loss, individual tradeoffs and joint coverage

22 October 2026. This is an original explanatory derivation of a classical finite rearrangement implication. It is not a new estimator, a priority claim, an executed postprocessing experiment or a replacement for the current frozen comparisons. Every current forecast and adverse crossing remains unchanged.

## Mature precedent and consulted edition

Victor Chernozhukov, Ivan Fernandez-Val and Alfred Galichon, *Improving Point and Interval Estimates of Monotone Functions by Rearrangement*, [arXiv0806.4730v3](https://arxiv.org/abs/0806.4730v3), 7 November 2008. The actual retrieved [fixed-version PDF](https://arxiv.org/pdf/0806.4730v3) has 24 pages,3811885 bytes and SHA256 `667a1af606d9275d0a84ba4957fd7502ba9183d9e7256ebe9716aa36a352f8ca`. Its cover carries the v3 date. The PDF's internal regeneration metadata are not a new publication date, and the arXiv page's nominal historical size is not the identity of the actual downloaded response.

The formal publication is *Improving point and interval estimators of monotone functions by rearrangement*, Biometrika96(3):559–575, September2009 issue, [DOI10.1093/biomet/asp030](https://doi.org/10.1093/biomet/asp030). The owning metadata identify online publication on30June2009. Final-journal-body equivalence to the consulted preprint is unverified; a direct journal-body route was inaccessible. The title and edition are kept distinct rather than silently calling the preprint the final body.

Root read selected opening/Section2.1–2.4 passages, Proposition1 and the submodular discrepancy formulation, and AppendixA's Proposition1 proof in physical18–20. Physical4 and19 were rendered and read. This is not a full24-page, simulation, empirical-table, software or external-reference reproduction. The source establishes mature rearrangement precedents; the finite pinball arithmetic and scope checks below are written explicitly rather than borrowing a confidence-band or forecasting guarantee.

## What the current crossing example does and does not show

The main manuscript correctly shows that replacing a long-horizon report by a higher crossed short-horizon report can harm the long-horizon score. That example does not settle every possible joint objective. Sorting the two reports changes both coordinates and answers a different question. It need not be preferred by a user who cares about one particular horizon or different horizon costs.

Fix one source and issue, two ordered horizons, the same quantile probability tau and the same units. Write their realized sampled peaks as y1<=y2. Suppose the issued reports cross, c1>c2, and both obey the same known issue floor B. Swapping their assigned horizons gives the coherent pair (c2,c1), still above B. The operation uses only already issued reports, not the realized future peaks. It is causal if both original reports are measurable in the common issue information set.

## Exact equal-weight raw pinball implication

For real u, pinball loss satisfies

    rho_tau(u) = (tau - 1/2)u + |u|/2.

Define original loss minus swapped loss as

    Delta = rho_tau(y1-c1) + rho_tau(y2-c2)
            - rho_tau(y1-c2) - rho_tau(y2-c1).

The linear terms cancel because swapping preserves the sum of reports. Hence

    Delta = (|y1-c1| + |y2-c2| - |y1-c2| - |y2-c1|)/2
          = max(0, min(y2,c1) - max(y1,c2)) >= 0.

The last quantity is the length of the overlap of [y1,y2] and [c2,c1]. One can verify it by considering whether either report lies below, within or above [y1,y2]. If the targets coincide, the intervals are disjoint or their overlap is only an endpoint, improvement can be zero. Thus this is weak improvement, not a claim that every crossing produces a strict gain.

Repeated adjacent inversion swaps extend the weak inequality to a finite horizon vector with ordered realized targets. This establishes weak improvement of the equal-weight raw loss sum over permutations of the original report values. It does not establish optimality among all possible ordered reports, or dominance over a separately fitted coherent model. If the objective is the equal-weight average over two horizons, its improvement is Delta/2; the sum and the average must not be interchanged.

The identity assumes a common tau and equal horizon weights. It cannot simply be applied to separately normalized loss percentages or different operational costs. For example, take equal targets y1=y2=1 and crossed reports(10,1) at tau=.95. Original losses are(.45,0); swapped losses are(0,.45). Giving the long horizon twice the short horizon's weight makes the weighted sum increase from.45 to.90. The equal-weight raw sum is unchanged. These are artificial arithmetic examples, not fitted forecasts or measured financial costs.

This is a real-arithmetic identity. It is not a claim that storedfloat64 sums, or cancellation of nearly equal stored losses, must be bitwise identical to an interval-length calculation. No financial floating-point outputs have been transformed or rescored here.

## Better pooled loss can accompany more breach occasions

Take an artificial position path(0,5,10), with horizons1 and2. The common issue floor is0, the realized peaks are(5,10), and crossed reports are(6,0). At tau=19/20:

| Reports | Short loss | Long loss | Raw loss sum | Strict breach count across the two horizons |
|---|---:|---:|---:|---:|
| Original(6,0) | .05 | 9.50 | 9.55 | 1 |
| Sorted(0,6) | 4.75 | 3.80 | 8.55 | 2 |

The gain1 equals the overlap length of [5,10] and [0,6]. The short report becomes worse, the long report becomes better, and the number of strict breaches increases. This verifies why an aggregate score implication is not an individual-horizon or breach-frequency guarantee. It establishes no actual effect in the financial archive and supplies no reason to reinterpret its19:1preference as an observed financing price.

## A separate joint-coverage preservation implication

There is also a useful, narrower probability statement, conditional on an already justified premise. If all original reports cover their ordered targets, y_j<=c_j for every j, componentwise dominance gives the same ordering for their order statistics:

    y_j = y_(j) <= c_(j),

where parentheses denote sorting. Therefore

    {all original horizons cover} is a subset of {all sorted horizons cover}.

An independently established simultaneous across-horizon coverage lower bound would consequently be preserved by sorting. The same holds for a valid conditional joint lower bound under a common issue information set when all reports are measurable there. This follows from event inclusion, not from a fitted distribution or a new calibration theorem.

It does not guarantee an improvement in every horizon's marginal coverage relative to that horizon's original rate. A separately valid joint lower bound of1-alpha also lower-bounds each sorted horizon's marginal coverage; without that premise, this argument establishes no numerical marginal guarantee. The two-horizon breach example is consistent with event inclusion: both its original and sorted vectors fail joint coverage. On paths where the original reports all cover, sorting creates no breach; on already failing paths, the number of breaches can increase. The current paper has not established the joint probability premise, so sorting would not manufacture a coverage certificate, a valid same-sample post-selection test or a live-information guarantee.

These are simultaneous statements across the declared horizons of one issue. They are not a new guarantee over every future issue, arbitrary stopping or every possible source. Different anchors, units, target versions or missing reports require separate treatment before even the deterministic target-order premise can be invoked.

## Decision for this study

The calculation sharpens the scope of the existing no-repair example: a particular one-coordinate change can harm its own horizon, whereas a classical joint rearrangement has an equal-weight pooled-score implication and preserves any separately valid joint-coverage premise. Neither statement selects a universally best repair. Choosing an operational objective or choosing a repair after inspecting the archive is another design decision.

No isotonic/rearrangement competitor is added to the fixed financial results. No crossing, report, original primary, loss denominator or adverse breach count is overwritten. A later study could predeclare a causal coherent transform and evaluate individual horizon outcomes, pooled raw loss, joint event behavior and costs under its chosen information contract. That would remain a mature-method application unless a further substantive contribution were demonstrated. More such transformations on the inspected record would not replace compatible unseen validation, an admissible public issue clock or observed decision evidence.
