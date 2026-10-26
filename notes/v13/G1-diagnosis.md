# G1 diagnosis before repair

# G1: high-quantile solver repair, designed after failure

This design is retrospective numerical repair, not a new statistical model or a replacement of v12 results. No real-data re-fitting occurred before this standalone design commit. The consistency gate is binding, including a possible decision that this repair cannot be used.

Root cause evidence: CFTC 33874A and original FX passed residual tests at iteration 10,000 but missed the unchanged Fenchel-gap test (1.835e-6 > 1.049e-6 and 2.457e-6 > 1.073e-6). Early FX has failures in both 0.001 and 0.1 validation candidates; the first also missed dual residual. These are saved diagnostics, not reruns.

Mature implementation references verified from primary sources: Boyd et al. (2011), Sections 3.3–3.4, [ADMM author page](https://stanford.edu/~boyd/papers/admm_distr_stats.html), DOI10.1561/2200000016; [CVXPY solver interface](https://www.cvxpy.org/tutorial/solvers/); [Clarabel settings](https://clarabel.org/stable/api_settings/). Residual balancing is an optimization device; no coverage or forecast-improvement guarantee follows. Internal solver stopping status alone never substitutes for the original external acceptance certificate.

The first ten complete finite validation candidate rows in the saved v12 candidate order fix ten first-refit tests (first CFTC contract, both histories, all five finite penalties). The saved first-origin capacities provide independent reference values; no examples are selected using repaired values. The native-capacity pointwise relative-error denominator is fixed below. This explicitly tests the actual repaired adaptive path.


No fitted values have been recomputed. The unchanged original diagnostics show slow certificate convergence, not source/data corruption; the fallback retains the same convex objective and independent dyadic feasible-dual gap.
