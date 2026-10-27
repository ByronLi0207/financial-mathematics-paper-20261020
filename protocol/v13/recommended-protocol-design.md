# G3: benchmark-protected validation protocol

Status: proposed fixed protocol; root will seal this standalone commit only at G3, after G2 completes, and before any G3 evaluation. The rule is deliberately retrospective and supplies no formal protection guarantee.

All indices are zero-based and inclusive. Decisions use validation only, then remain fixed throughout each original evaluation segment.

```json
{
  "base_commit": "80608070e4a6f4207483dc95770e6e5926172b19",
  "tau": 0.95,
  "menu": [
    0.001,
    0.01,
    0.1,
    1.0,
    10.0,
    "inf"
  ],
  "input_inventory_contract": "protocol/v12/loss-decomposition-design.md",
  "input_inventory_contract_sha256": "cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1",
  "inherited_code_sha256": {
    "v12_inputs.py": "819087f0055fae722f9870378246d8e1dd7c45ecbe1484ef23d1fef21b7c8e0b",
    "v12_forecast.py": "d893d3cd6ba5542fbd5dfd2be95c1c8f9d4060eefa53b25e0490a2f938b2b3ef",
    "v12_runner.py": "714ab36d47cee56947b131661ab2f9afb9f23529cea9f5b59f0424f2ad293e3b",
    "v12_decomposition.py": "e9df96e98954e287cabf30ae003474d633b565f8e72be2a641c4680a8b3006bf",
    "v12_summaries.py": "78caf8e4ccbe27e98d04311a94a747500b1c6acab5ad73144c9e31323cd70893",
    "v10_menu.py": "e91c942d6a24cb833ceaed48c282360a578325c0ebf3c5b370b42c4b14ca5014",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "empirical_headroom.py": "db5d73facae28432bb0617d173e5b4c933d95e52b43f9363543e21194919412e",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "v6_inference.py": "1c7fc9a3fe8392c771dde0272966b9a0f0f3c4b969df481d0d6818385dcfd2e5",
    "inference_tests.py": "2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c"
  },
  "source_policy": "Only the 31 existing SHA-pinned sources in the v12 F1 inventory; no acquisition, old-v3 access, source edits, interpolation, splicing or data extension.",
  "training_rule": "At segment-anchored refit r, use completed origins r-H-W+1..r-H inclusive; label_end<=r; causal features valid from26 weekly or168 FX; training-only transforms and response scale; historical F has corrected ceil((W+1)*.95) order statistic, infinity is ordinary I and is not F.",
  "refit_rule": "r=a+d*floor((t-a)/d), separately anchored at each validation/evaluation segment start; d13 weekly, d24 FX.",
  "selection": "All six validation candidate means must be finite, complete and aligned; choose minimum mean loss, exact ties favor stronger penalty with infinity strongest. No tolerance ties or successful-subset selection.",
  "score": "v6_inference.pinball_losses at tau.95 and study_core.stable_mean; relative loss100*(QRmean-Fmean)/Fmean with positive reference; strict breach peak>capacity.",
  "cache": "Original v12 caches may be read only after full source/grid/code/H/W/tau/d/origin/refit identity and trace-SHA checks; all newly attempted reports are in private .scratch/v13. Exact prior FAILED identity propagates without retry. G2 results may be reused by G3 with these same checks. No cache required by G4 clean reproduction.",
  "publication": "Public aggregates and provenance under results/v13; restricted FX per-origin observations/forecasts/losses remain private with SHA receipts.",
  "code_gate": "Design must be its own standalone ancestor commit, working design bytes equal committed bytes, and implementation/input/code seal committed and recorded before any financial computation. No protocol/rule/threshold changes after start.",
  "resource": {
    "workers": 4,
    "numerical_threads_per_worker": 1,
    "max_worker_rss_bytes": 2147483648,
    "max_cell_wall_seconds": 300,
    "no_failed_candidate_retry": true
  },
  "retrospective": "Designed after inspecting all prior studies, including original evaluation periods and v12 F2. Not prospective, a new holdout, a causal validation-length effect, a formal protected-risk guarantee, or an independence test across related series.",
  "experiment": "G3",
  "methods": [
    "QR33"
  ],
  "rp_definition": [
    "Six-point menu .001,.01,.1,1,10,infinity; minimum mean validation loss and strongest exact tie.",
    "Weekly validation156 with horizon-completed boundary; FX validation5760 ending at its unchanged original validation boundary. Eligibility is before outcomes and rejects an entire geometry.",
    "Default corrected-rankF. Only if selectedQR validation mean loss is strictly lower thanF and the positive improvement strictly exceeds one paired HAC standard error, chooseQR for full evaluation; else useF. One decision per geometry, no evaluation-period switching or rescanning."
  ],
  "weekly_geometry": {
    "cftc": {
      "source_count": 17,
      "N": 877,
      "horizons": [
        6
      ],
      "windows": [
        52,
        260
      ],
      "validation": [
        449,
        604
      ],
      "evaluation": [
        611,
        870
      ],
      "evaluation_n": 260,
      "validation_dates": [
        "2018-08-14",
        "2021-08-03"
      ],
      "evaluation_dates": [
        "2021-09-21",
        "2026-09-08"
      ],
      "baseline_validation": [
        553,
        604
      ],
      "feature_valid_from": 26,
      "first_training_origin_by_W": {
        "52": 392,
        "260": 184
      }
    },
    "nyfed": {
      "source_count": 13,
      "N": 706,
      "horizons": [
        6,
        24
      ],
      "windows": [
        52
      ],
      "validation_H6": [
        243,
        398
      ],
      "validation_H24": [
        225,
        380
      ],
      "evaluation": [
        405,
        681
      ],
      "evaluation_n": 277,
      "baseline_validation": [
        329,
        380
      ],
      "feature_valid_from": 26,
      "first_training_origin_by_H": {
        "6": 186,
        "24": 150
      }
    }
  },
  "fx_geometry": {
    "source_count": 1,
    "N": 18576,
    "horizon": 6,
    "window": 2880,
    "validation_n": 5760,
    "feature_valid_from": 168,
    "original": {
      "validation": [
        6143,
        11902
      ],
      "baseline_validation": [
        10463,
        11902
      ],
      "evaluation": [
        11927,
        18551
      ],
      "evaluation_n": 6625,
      "validation_dates": [
        "2015-01-29T00:00:00",
        "2015-12-30T23:00:00"
      ],
      "first_training_origin": 3258
    },
    "early2015": {
      "validation": [
        3215,
        8974
      ],
      "baseline_validation": [
        7535,
        8974
      ],
      "evaluation": [
        8999,
        10438
      ],
      "evaluation_n": 1440,
      "validation_dates": [
        "2014-08-12T00:00:00",
        "2015-07-13T23:00:00"
      ],
      "first_training_origin": 330
    },
    "boundary_rationale": "Keep original commonH24 validation endpoint even though H6 is evaluated, to isolate the4x length change and retain refit-grid phase: start differs4320=180*d24. Every validation label completes strictly before evaluation. Original/early latest label11908/8980; evaluation11927/8999."
  },
  "eligibility": "Before any outcomes, for every source/geometry and both baseline andlong validation use training_first=validation_first-H-W+1; require >=max(24,long_scale,short_scale), valid complete source grid and complete labels. If any fails, exclude entire geometry from RP,F,ordinaryQR comparison and record why; never shorten histories orvalidation. All planned60weekly+2FX are feasible using saved metadata.",
  "planned_weekly_cells": 60,
  "planned_fx_cells": 2,
  "planned_method_comparisons": 186,
  "comparators": [
    "RP",
    "corrected-rank F",
    "ordinary QR33 selected on original validation length with the same six-point menu"
  ],
  "gate": {
    "paired_difference": "d_t = loss(selectedQR,t)-loss(F,t) on exactly thelong-validation origins; F uses identical W,H,d and segment anchor.",
    "mean": "math.fsum(d)/n",
    "bandwidth": "K=min(n-1,max(H,floor(4*(n/100)**(2/9)))) exactly inference_tests.bandwidth(n,H)",
    "covariance": "demean d; gamma_k=sum((d_t-mean)*(d_(t-k)-mean))/n; Omega=gamma0+2*sum_(k=1)^K(1-k/(K+1))*gamma_k, using inference_tests.hac",
    "standard_error": "sqrt(Omega/n); no HLN adjustment for the1SE gate, no p-value threshold and no multiplicity interpretation.",
    "choose_QR_iff": "mean(d)<0 and -mean(d)>standard_error, both strict. Otherwise F.",
    "zero_lrv": "If finite Omega==0, SE=0 and the same strict inequalities apply; didentically0 therefore returnsF.",
    "invalid_lrv": "If nonfinite ornegative Omega, record gate UNAVAILABLE and conservatively useF with reason; not a successful evidence gate.",
    "selection_disclaimer": "The winner and evidence gate share validation data; this is a heuristic retrospective decision rule, not a nominal hypothesis test or formal risk guarantee.",
    "infinity": "Infinity is empirical I rather than corrected-rankF. It must meet the identical paired evidence gate to replaceF."
  },
  "selection_seal": "Complete all six long-validation means, choose lambda and write the signed gate decision before reading/scoring evaluation. Seal ordinaryQR choice independently on the original validation segment before its evaluation score.",
  "predictions": {
    "R1": {
      "universe": "all pre-outcome eligible60weekly cells, equalcell normalizedlosses",
      "support_median_rp_relative_excess_pct_lte": 1.0,
      "missing": "If any eligibleRP result missing, formal full-universe median is UNDETERMINED; descriptive complete-row median may be printed with denominator."
    },
    "R2": {
      "universe": "same60weekly eligible cells",
      "adverse_if_rp_relative_excess_pct_gt": 10.0,
      "support_fraction_lte": 0.05,
      "integer_threshold_if60": 3,
      "missing": "Known adverse count>3 immediately NOT_SUPPORTED; otherwise any eligiblemissing outcome makes UNDETERMINED; no failure-to-F substitution."
    },
    "R3": {
      "universe": "each pre-outcome eligible FX period separately, W2880H6",
      "if_ordinary_relative_excess_pct_lt": 0,
      "support_if_rp_excess_pct_lte": "0.5 * ordinaryQR_relative_excess_pct",
      "no_baseline_gain": "Mark NOT_APPLICABLE for an FX period with no ordinaryQR gain; do not claim retained benefit.",
      "overall": "SUPPORTED if every eligible positive-baseline-gain period meets halfgain and at least one such periodexists; any known failure NOT_SUPPORTED; any requiredmissing UNDETERMINED; all no-gain NOT_APPLICABLE."
    }
  },
  "failure_policy": "If any of six required candidate fits or alignment fails, record entire ordinaryQR orRP method-cell FAILED and do not switch it silently toF. ChoosingF is reserved for a completely calculated finite gate that lacks sufficient benefit (or explicitly predeclared unavailable HAC with a valid completed selection). PreserveF comparator and allfailed rows; no retry.",
  "runtime": {
    "total_cap_seconds": 2700,
    "order": "AllNYFed13 H6 thenH24; CFTC17 W52 thenW260; FXoriginal thenearly2015; fixed original source order. Each geometry long andbaseline choices beforeevaluation.",
    "prelaunch_reduction": "If a time-only workload estimate before formal run exceeds cap, omit whole FXearly2015, then FXoriginal secondary periods before dropping any weekly primarygroup; retain omitted planned rows andR3 UNDETERMINED if positivegain preservation cannot beassessed. Never choose scope by observed losses. Stop atcap."
  },
  "report": "All62geometry rows withRP outcome,F outcome,ordinaryQR outcome, long/baseline lambda, validationmeans,HAC K/Omega/SE, gateseal, actual usedmodel and failure/exclusionreasons. Report Ffallback count/fraction bysourcefamily/history/horizon and overall; failed rows have unknown route and are not creditedasfallback. Plot RP/ordinary normalized distributions byCFTC,NYFed,FX with complete/planned counts, no pooled independence test."
}
```
