# G1: high-quantile solver repair, designed after failure

This design is retrospective numerical repair, not a new statistical model or a replacement of v12 results. No real-data re-fitting occurred before this standalone design commit. The consistency gate is binding, including a possible decision that this repair cannot be used.

Root cause evidence: CFTC 33874A and original FX passed residual tests at iteration 10,000 but missed the unchanged Fenchel-gap test (1.835e-6 > 1.049e-6 and 2.457e-6 > 1.073e-6). Early FX has failures in both 0.001 and 0.1 validation candidates; the first also missed dual residual. These are saved diagnostics, not reruns.

Mature implementation references verified from primary sources: Boyd et al. (2011), Sections 3.3–3.4, [ADMM author page](https://stanford.edu/~boyd/papers/admm_distr_stats.html), DOI10.1561/2200000016; [CVXPY solver interface](https://www.cvxpy.org/tutorial/solvers/); [Clarabel settings](https://clarabel.org/stable/api_settings/). Residual balancing is an optimization device; no coverage or forecast-improvement guarantee follows. Internal solver stopping status alone never substitutes for the original external acceptance certificate.

The first ten complete finite validation candidate rows in the saved v12 candidate order fix ten first-refit tests (first CFTC contract, both histories, all five finite penalties). The saved first-refit-block capacities provide independent reference values; no examples are selected using repaired values. The native-capacity pointwise relative-error denominator is fixed below. This explicitly tests the actual repaired adaptive path.

```json
{
  "experiment": "G1",
  "base_commit": "80608070e4a6f4207483dc95770e6e5926172b19",
  "tau": 0.99,
  "menu": [
    0.001,
    0.01,
    0.1,
    1.0,
    10.0,
    "inf"
  ],
  "cells": [
    {
      "cell_id": "F3-cftc-33874A-original-H6-W260-V52-tau0.99",
      "family": "cftc",
      "source_key": "33874A",
      "source_index": 12,
      "period": "original",
      "horizon": 6,
      "window": 260,
      "refit_step": 13,
      "validation_first": 553,
      "validation_last": 604,
      "evaluation_first": 611,
      "evaluation_last": 870,
      "validation_n": 52,
      "evaluation_n": 260,
      "short_scale": 6,
      "long_scale": 26,
      "nominal_gap_seconds": 604800,
      "tau": 0.99,
      "source_sha256": "ce7484a6fa2167788e3ee1cf978e2a3b6059465ef49134b2887799c77859d2a1"
    },
    {
      "cell_id": "F3-fx-fx_hourly-original-H6-W2880-V1440-tau0.99",
      "family": "fx",
      "source_key": "fx_hourly",
      "source_index": null,
      "period": "original",
      "horizon": 6,
      "window": 2880,
      "refit_step": 24,
      "validation_first": 10463,
      "validation_last": 11902,
      "evaluation_first": 11927,
      "evaluation_last": 18551,
      "validation_n": 1440,
      "evaluation_n": 6625,
      "short_scale": 24,
      "long_scale": 168,
      "nominal_gap_seconds": 3600,
      "tau": 0.99,
      "source_sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa"
    },
    {
      "cell_id": "F3-fx-fx_hourly-early2015-H6-W2880-V1440-tau0.99",
      "family": "fx",
      "source_key": "fx_hourly",
      "source_index": null,
      "period": "early2015",
      "horizon": 6,
      "window": 2880,
      "refit_step": 24,
      "validation_first": 7535,
      "validation_last": 8974,
      "evaluation_first": 8999,
      "evaluation_last": 10438,
      "validation_n": 1440,
      "evaluation_n": 1440,
      "short_scale": 24,
      "long_scale": 168,
      "nominal_gap_seconds": 3600,
      "tau": 0.99,
      "source_sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa"
    }
  ],
  "consistency_examples": [
    {
      "cell_id": "F3-cftc-044601-original-H6-W52-V52-tau0.99",
      "penalty": 0.001,
      "cache_key": "b864d340c89a9396ae5702ad347b7038e5d54d762669373de20b28ef965921da",
      "source_key": "044601",
      "window": 52,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W52-V52-tau0.99",
      "penalty": 0.01,
      "cache_key": "5d83cccfd60b9f88a6b7e26c0b7d03f01b0bcf796248adf44ed56e8eb0a75966",
      "source_key": "044601",
      "window": 52,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W52-V52-tau0.99",
      "penalty": 0.1,
      "cache_key": "6cb2161b4f165a9af3d3fdf4bf45cbdb1574e8dc0d8f7f8b72b40947651caf66",
      "source_key": "044601",
      "window": 52,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W52-V52-tau0.99",
      "penalty": 1.0,
      "cache_key": "578713f0f643b394ea203981ed17d384d3892c4eb2561bf6893c85596b1c554d",
      "source_key": "044601",
      "window": 52,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W52-V52-tau0.99",
      "penalty": 10.0,
      "cache_key": "8af13d86044160042aadf7f85f7eb407bd4d8edef1a82dc6a4959ca9bf394057",
      "source_key": "044601",
      "window": 52,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W260-V52-tau0.99",
      "penalty": 0.001,
      "cache_key": "9b344bd22009f3ff088ebb13582719a361c7db6f3df48678c8447aa716f8a59b",
      "source_key": "044601",
      "window": 260,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W260-V52-tau0.99",
      "penalty": 0.01,
      "cache_key": "7598f2bdd20ea1cfdcbd8646dded9bad6db3b0ee3851b7f3b123e11f3e963895",
      "source_key": "044601",
      "window": 260,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W260-V52-tau0.99",
      "penalty": 0.1,
      "cache_key": "8d5fbc1ff37d2e9fc841e7828d4dd6d881defd2c5c3844f2a9675ce85f181ca8",
      "source_key": "044601",
      "window": 260,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W260-V52-tau0.99",
      "penalty": 1.0,
      "cache_key": "1ea524a928b757aefe99daed98ea23b5983ab2ebb1984fc5b23e93125a8b8a73",
      "source_key": "044601",
      "window": 260,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    },
    {
      "cell_id": "F3-cftc-044601-original-H6-W260-V52-tau0.99",
      "penalty": 10.0,
      "cache_key": "e58b7ca11e60ae65e28aff4c23b73fa9c0c6758d2d8bf6e5fe08db178eb77176",
      "source_key": "044601",
      "window": 260,
      "refit_index": 553,
      "query_origins": [
        553,
        565
      ]
    }
  ],
  "consistency_max_pointwise_relative_error": 1e-06,
  "consistency_denominator": "max(1,abs(original floor-projected capacity in native units)) pointwise for all 13 queries in each first original validation refit block; the maximum across every point of each of 10 fits must pass. Same causal training sample/transform/scale. Reference is saved trace capacity, not a fresh baseline fit.",
  "consistency_policy": "Run the fixed 10 examples exactly once, no replacement/cherry-picking. Any failure/error invalidates repair for this revision; do not run the three failed cells or change settings. Report NOT_RUN_CONSISTENCY_GATE for those cells, retaining original UNDETERMINED Q1/Q2.",
  "objective": "mean pinball_tau(y-Xbeta)+lambda*sum(beta[1:]**2)/2; intercept unpenalized, unchanged feature/response scaling and floor projection. Infinity is original lower empirical I.",
  "admm": {
    "max_iter": 100000,
    "rho_initial": "1/n",
    "rho_check_every": 50,
    "rho_balance_mu": 10.0,
    "rho_increase_factor": 2.0,
    "rho_decrease_factor": 2.0,
    "rho_min_multiplier": 0.0009765625,
    "rho_max_multiplier": 1024,
    "scaled_dual_rescaling": "u <- rho_old/rho_new*u; recompute ridge linear solve after each rho change",
    "initialization": "same cold initialization as original; no warm start",
    "certificate_dual_conversion": "Original _certificate uses weights=-u at rho=1/n. For variable rho supply n*rho*u to unchanged _certificate, giving weights=-n*rho*u."
  },
  "clarabel": {
    "invocation": "Only after the adaptive ADMM does not converge; one cold CVXPY/CLARABEL solve of same objective, no second setting attempt.",
    "max_iter": 500,
    "tol_gap_abs": 1e-10,
    "tol_gap_rel": 1e-10,
    "tol_feas": 1e-10,
    "time_limit_seconds_per_call": 30,
    "status": "Only OPTIMAL; OPTIMAL_INACCURATE is not accepted",
    "external_certificate": "u_plus,u_minus>=0 and Xbeta+u_plus-u_minus=y. Raw weights=-n*equality_dual. Use unchanged exact dyadic dual projection and Fenchel certificate; primal norm is equality residual, dual norm is ridge stationarity using projected feasible dual weights. Both are in the original objective scaling.",
    "postsolve_thresholds": "Original atol=1e-6,rtol=1e-5,gap_rtol=1e-6; no relaxed residual/gap acceptance. Primal tolerance sqrt(n)*atol+rtol*max(||Xbeta||,||u_plus-u_minus||,||y||); dual tolerance sqrt(p)*atol+rtol*||X_nonintercept^T weights/n|| plus intercept moment in the norm when checking stationarity."
  },
  "acceptance": {
    "atol": 1e-06,
    "rtol": 1e-05,
    "gap_rtol": 1e-06,
    "linear_system_residual": "<=1e-9*(1+||right||), unchanged",
    "dyadic_dual_grid": 1099511627776,
    "no_relaxation": true
  },
  "selection": "Recompute all six validation candidates in each of only the three failed cells. Exact minimum mean loss, exact ties prefer stronger lambda; all candidates must complete. Seal selection before evaluation. Refit selected candidate on full original evaluation origins only, no partial cell. Recompute matched F for that evaluation.",
  "failure_policy": "Any required finite fit that fails both declared stages fails the whole candidate and method-cell; preserve all other candidate outputs, but no successful-subset selection. No second repair, no retries, no original-file overwrites. A consistency-gate failure prevents adopting/running the repair.",
  "runtime": {
    "formal_cap_seconds": 1200,
    "includes": "Consistency gate plus three failed cells if gate passes; resource cancellation in fit checkpoints; no formal run before standalone design and committed-code seal",
    "workers": 1,
    "threads_per_worker": 1,
    "order": "10 fixed consistency fits; CFTC 33874A W260; FX original; FX early2015. Any wall cap leaves explicit resource statuses."
  },
  "public_private": "Aggregate rows, means, failure diagnostics, gate errors and scalar certificates public under results/v13/tau-repair; per-origin FX traces private .scratch/v13/tau-repair, SHA bound.",
  "reporting": "Original Q1/Q2 remain UNDETERMINED in original archive; repaired assessment appears separately as after a solver repair designed after the failure. Merge only a separate derived v13 assessment with original 71 completed rows, never overwrite old rows. Q1 fixed 34 denominator threshold29 strict F wins; Q2 both FX relative loss<0. Missing yields UNDETERMINED unless completed contradiction rules out criterion.",
  "inherited_code_sha256": {
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "v12_forecast.py": "d893d3cd6ba5542fbd5dfd2be95c1c8f9d4060eefa53b25e0490a2f938b2b3ef",
    "v12_inputs.py": "819087f0055fae722f9870378246d8e1dd7c45ecbe1484ef23d1fef21b7c8e0b",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "v6_inference.py": "1c7fc9a3fe8392c771dde0272966b9a0f0f3c4b969df481d0d6818385dcfd2e5",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf"
  }
}
```
