# Source register 36: approximation layers and financial comparison targets

20 October 2026. This extends the adaptive-control reading in [register 35](source-register-35.md), follows its directly cited computational predecessor, and preserves favorable and adverse reported results. Literature review continues; no project empirical result or final specification is selected.

## Original editions and actual scope

**Tao Chen and Michael Ludkovski, _A Machine Learning Approach to Adaptive Robust Utility Maximization and Hedging_, arXiv 1912.00244v3**, DOI 10.48550/arXiv.1912.00244. First deposit 30 November 2019; selected revision deposited 4 May 2020. The PDF bears the same arXiv date and uses Mike Ludkovski on its title page. [Official version record](https://arxiv.org/abs/1912.00244v3), [original preprint](https://arxiv.org/pdf/1912.00244v3).

The [publisher record](https://epubs.siam.org/doi/10.1137/20M1336023) verifies the later SIAM Journal on Financial Mathematics 12(3), 1226–1256 (2021), DOI **10.1137/20M1336023**, submitted 5 May 2020, accepted 15 March 2021, online 16 September 2021. The journal body remains unread; equivalence with the preprint is not asserted. A public NSF PDF route returned an error and was closed.

| Original physical pages | Selected reading completed |
|---|---|
| 1–8 before Section 2 | Positioning, joint learning/control state, Bellman formulation and Gaussian investment setup |
| 9–17 before Section 3 | Numerical approximation, training-site design, separate fitted maps, forward evaluation and algorithm variability |
| 17–22 before Section 4 | One-period and dynamic investment comparisons and simulated terminal wealth |
| 22–28 before Section 5 | Hedging objective, computational choices, comparator distributions and Table 3 |
| 28–31 before References | Enhancements, integration comparison, related formulations and conclusion; Figure 11 also inspected |

Original formula, algorithm and result pages were inspected visually. The retained preprint has **33 pages, 1771626 bytes**, SHA256 **2ed89410334eeaea480d6142afc06e4e3eeee7579693f594bf7cc1784b0059bf**. References and external foundations are not fully audited, and every literal formula, guarantee and implementation detail is not independently certified. This is one source, not five papers.

**Bayraktar–Chen, arXiv 2202.10391v3**, is the same source and edition documented in register 35. The new selected reading covers physical 16–19 for the financial regularity argument, transport-duality reduction and compressed-state algorithm, and 20–23 before References for forward evaluation and reported utility comparisons. Its Proposition 2.3 proof remains uncompleted. Neither article's code was executed.

## What the computational predecessor already covers

Chen–Ludkovski already studies robust allocation and asymmetric-loss hedging with parameter learning and separate fitted value/control maps. Wealth and parameter estimates share an innovation, so their dependence is part of the model. The investment example uses Gaussian innovations and CRRA utility; wealth homogeneity supports its dimension reduction. The hedging action is a number of shares, whereas the allocation action is a wealth fraction. Identical numerical action bounds do not have identical financial units.

The paper separates integration, optimization and fitted-function errors, and distinguishes a directly optimized approximate policy from its fitted predictor. It examines training-region extrapolation and variation across complete algorithm runs. Its hedging implementation also says the worst parameter need not lie on the boundary; the utility example's boundary search is therefore not automatically transferable. These are existing practices and objective-dependent restrictions, not new contributions of this project.

## Keep the adverse comparator result

For hedging error defined as liability minus wealth, the source penalizes shortfall plus a weighted surplus penalty. Its Table 3 reports these **mean losses** at initial stock 100 and wealth 20:

| Surplus weight | Adaptive robust | Static robust | Myopic adaptive |
|---|---:|---:|---:|
| 0 | 3.52 | **0.08** | 6.50 |
| 0.5 | **4.07** | 8.44 | 13.83 |
| 0.75 | **5.70** | 13.59 | 14.31 |

These are author-reported simulation results, not a replication. Static robust wins the displayed one-sided-loss case. Adaptive robust has the smaller reported loss for the two displayed positive weights. A general claim that it always beats the baselines would omit a material result. The article's adaptive Delta comparator also targets a different objective from the asymmetric loss.

## Nonparametric continuation: approximation and evaluation

Bayraktar–Chen approximates the empirical-law state with a small moment vector **for regression purposes**. It does not thereby establish that those moments determine the full law. A finite empirical expectation, a fitted continuation value and numerical optimization introduce different approximation issues. Its distributional dual still contains optimization over possible innovations, not merely a choice among historical observations.

The reported study evaluates fresh simulated paths under a specified Gaussian mixture. This is not a historical-market holdout. Its true-law oracle has the larger reported mean utility; adaptive robust improves some lower-tail summaries relative to that oracle, while the nearly bank-only static robust policy has still stronger lower-tail protection. A smaller illustrated starting-radius functional modestly improves the adaptive mean while worsening variance and lower-tail summaries. The rare starting case is explicitly identified as such by the authors. These tradeoffs do not establish universal dominance.

## Requirements carried into later design

| Issue | Evidence still needed for a transfer |
|---|---|
| Financial target | State the liability or allocation objective, control units, constraints and information actually available. |
| Evaluation law | Distinguish the dynamically adverse robust objective, a fixed simulated test law and historical predictive performance. |
| Numerical approximation | Check state compression, integration, action/model search and fitted-policy errors separately. |
| Statistical uncertainty | Emulator uncertainty, algorithm-run variation and confidence about the financial law have different meanings. |
| Contribution | Identify a distinct financial question and closest applications; changing an asset, kernel or scalar solver is insufficient. |

Warm starts, fitted-parameter reuse and integration alternatives are already discussed in the predecessor; proposed enhancements are not universal validated speedups. Its observation that Monte Carlo needed more nodes than quadrature in a particular comparison is not a general runtime guarantee. The cited 2017 recursive-confidence-region foundation remains a targeted unread dependency. Fournier–Guillin was already covered by earlier selected original reading and is not counted as newly unread here.

No financial observations, author program, software installation, fitted model, simulation or empirical experiment was produced for this register. Runtime and memory compliance remain unmeasured. Source PDFs and fingerprints stay local; source-code/data availability and reuse rights were not established by these passages. No third-party PDF, raw data or figure is redistributed.
