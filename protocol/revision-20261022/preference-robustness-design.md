# Fixed-report preference robustness: design and implementation plan

22 October 2026. The user reopened the previously closed working paper and
authorized improvements on GitHub. This is a new exploratory supplement.
The original paper, reports, selections, result archives and closure snapshot
remain available in history. No independent data, new quantile fits, unseen
holdout or financial policy evaluation is represented.

## Diagnosed gap and choice

The current paper already includes QR, local quantiles, residual replay,
empirical-rank controls and coverage diagnostics. Its stipulated 19:1
shortfall/excess tradeoff leaves the robustness of individual rankings
unquantified. We choose an analytic fixed-report preference frontier from
existing public aggregates. Additional model fits would expand the inspected
menu without solving the missing unseen/decision evidence; horizon sorting
has a mature existing derivation and needs private traces. These remain
separate possible projects. The present choice adds concrete interpretable
findings using no source observations and changes no primary comparison.

## Exact scope

For each source / H / W cell retain QR, KNN, SCALED_KNN, frozen F/S/K,
AR1_REPLAY and I. There are eight cells and 64 reports, all with matching
completed-label history length and update schedule within each cell. The
same eight reports are evaluated on the existing globally anchored H+1
sparse grid, yielding another 64 reports. The sparse grid does not create
independence. No rolling or one-state report enters these frontiers.
Four separately labeled headline comparisons retain the original FX H6,
matched FX H6, legacy FX H24 and Treasury H6 reference definitions.

Let U=mean(P-C)+ and V=mean(C-P)+. Compute J(alpha)=alpha U+(1-alpha)V
for the full continuum 0<=alpha<=1. At alpha=.95 it reconciles with the
archived pinball mean to relative 1e-12 / absolute 1e-9 tolerance. The
ratio r=alpha/(1-alpha) is hypothetical shortfall/excess preference, not
observed funding prices. The endpoint alpha=1 means the limiting r=infinity;
alpha=0 is a degenerate excess-only objective. Retain exact pair crossings,
all ties and endpoints, maximal open frontier regions, coefficientwise
Pareto domination and every .95 winner. Do not choose a future selector
from these inspected outcomes. Forecasts fitted for .95 are fixed actions
under alternative preferences, not estimates of other quantiles. This is
not a Murphy diagram or dominance under every consistent .95 score.

Arithmetic uses Fraction on the saved decimal mean tokens, not rounded
manuscript values. It is exact for those tokens; the archived means are
floating point summaries of original data, not infinite-precision sample
truth. Report approximate displayed thresholds alongside exact fractions.
Do not interpret tiny endpoint differences as economic significance.

## Mature practice and reading

Gneiting (2011), Making and Evaluating Point Forecasts, JASA 106, 746-762,
https://arxiv.org/abs/0912.0902 and the existing paper reference establish
the need to match a forecast directive with its evaluation loss. The official
publisher abstract of Gneiting (2011), Quantiles as optimal point forecasts,
https://doi.org/10.1016/j.ijforecast.2009.12.015 describes the cost-asymmetry
interpretation. The publisher summary of Ehm et al. (2016),
https://doi.org/10.1111/rssb.12154 describes varying consistent scores for
a fixed functional, a distinct exercise. Only these summaries and existing
manuscript material were consulted in this revision; no new full-body
reading, proof reproduction or priority claim is implied. Linear-envelope
and pairwise crossing arithmetic here are elementary, not a new estimator.

## Execution and verification plan

1. Test exact component parsing, dominance, ties, crossings and lower
   envelopes on synthetic rational examples before implementing the engine.
2. Test archive admission failures, implement a standalone aggregate-only
   runner and bind six input files, implementation and this design by hashes.
3. Commit the design/executable freeze before the recorded complete run.
   Preliminary diagnostic values were already inspected; this freeze fixes
   execution identity and does not imply statistical preregistration.
4. Generate all 16 groups, 128 report records, 448 unordered pair analyses,
   four named headline comparisons and every frontier without omission.
5. Independently reconstruct each method's optimal alpha interval by affine
   inequalities, verify source tokens and all output inventories, and test
   that deletion/corruption is detected.
6. Integrate the results and their interpretation into the English paper,
   add a complete table and a supplementary preference plot, rebuild TeX
   and PDF, inspect rendered pages and verify content and figure fidelity.
7. Run the complete test suite, original read-only archive verification,
   obtain a fresh review and publish the branch/PR with exact limitations.

The default system Python is 3.9 without required dependencies. The
existing bundled Python 3.12 environment passes the original 526 tests.
No packages are installed. The new analysis is standard-library-only,
single process, with no network, refits, raw-source acquisition or GPU.
Document generation uses the existing reportlab/pypdf environment.
