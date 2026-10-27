# G2: NY Fed validation-length replication

Status: fixed before any new G2 fit or evaluation; the standalone design commit is required before execution.

All indices are zero-based and inclusive. The H6 long arm intentionally follows the task’s most recent fully completed label, so its boundary also shifts18weeks relative to the original short arm. Results cannot isolate a causal length effect. V3/V4 are fixed-denominator retrospective descriptive screens.

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
  "experiment": "G2",
  "methods": [
    "QR33",
    "QR4"
  ],
  "weekly_sources": 13,
  "families": [
    "bill",
    "panel"
  ],
  "horizons": [
    6,
    24
  ],
  "windows": [
    52
  ],
  "validation_lengths": [
    52,
    156
  ],
  "evaluation": [
    405,
    681
  ],
  "evaluation_n": 277,
  "evaluation_dates": [
    "2021-01-06",
    "2026-04-22"
  ],
  "validation_geometry": {
    "52": {
      "all_horizons": [
        329,
        380
      ],
      "dates": [
        "2019-07-24",
        "2020-07-15"
      ]
    },
    "156": {
      "rule": "validation_last=evaluation_first-H-1; validation_first=validation_last-155",
      "H6": [
        243,
        398
      ],
      "H6_dates": [
        "2017-11-29",
        "2020-11-18"
      ],
      "H24": [
        225,
        380
      ],
      "H24_dates": [
        "2017-07-26",
        "2020-07-15"
      ],
      "latest_label_end": 404,
      "latest_label_end_date": "2020-12-30"
    }
  },
  "eligibility": {
    "feature_valid_from": 26,
    "first_training_origin_by_H": {
      "6": 186,
      "24": 150
    },
    "W260_first_training_origin_by_H": {
      "6": -22,
      "24": -58
    },
    "rule": "Before any fit reject the entire source/horizon if raw identity/date alignment fails or earliest V156 mature training origin<26. W260 deliberately not included because its -22/-58 earliest origins fail. Every source has common706-record grid so all13 per horizon are eligible."
  },
  "planned_geometry_cells": 52,
  "planned_method_cells": 104,
  "predictions": {
    "V3": {
      "method": "QR33",
      "per_horizon_denominator": 13,
      "statistic": "median across fixed13 of relative excess atV156 minus median atV52 (difference of arm medians, not median paired change)",
      "support_if_each_horizon_difference_pct_points_lte": -5.0,
      "overall": "SUPPORTED only if H6 and H24 both supported; a complete failing horizon makes NOT_SUPPORTED; missing required eligible pair makes that horizon UNDETERMINED, never replace by successful-subset median."
    },
    "V4": {
      "method": "QR33",
      "per_horizon_denominator": 13,
      "statistic": "count selecting infinity atV156 strictly greater than atV52, separately H6 andH24",
      "overall": "SUPPORTED only if bothH; complete failure of a horizon makes NOT_SUPPORTED; incomplete pairs UNDETERMINED. QR4 is separate sensitivity, never substitutes for QR33."
    }
  },
  "interpretation": {
    "supported": "The pre-specified validation extension improves forecasts in both reporting systems. H6 also shifts the validation endpoint18weeks and refit phase, so this is not a causal length-only claim.",
    "not_supported": "The CFTC improvement did not replicate in the pre-specified NYFed comparison. Report each horizon and any partial improvement without weakening the5pp/two-horizon rule.",
    "unknown": "Insufficient numerical completion to assess the full pre-specified NYFed comparison."
  },
  "failure_policy": "Any required candidate, selected evaluation or F reference failure makes its entire method-cell FAILED; keep all planned rows, reason and missingness; never retry, drop unfavorable outcomes or promote complete subsets.",
  "runtime": {
    "total_cap_seconds": 1800,
    "order": "QR33 for all13 sources H6 thenH24, V52 beforeV156, then QR4 same sequence; fixed bill first then original panel selection order. Evaluation dates never change.",
    "prelaunch_reduction": "Only if a time-only workload estimate before formal launch exceeds cap, omit the entire secondary QR4 method and record omitted planned rows as NOT_RUN_RESOURCE_LIMIT; never reduce source membership of a retained primary horizon. Stop remaining work atcap and retain NOT_RUN rows."
  },
  "comparison_plot": "Paired point groups by NYFed source/horizon, validation52 and156; beside unchanged archived CFTC17×2W results from results/v12/validation-length/rows.json, with provenance. No native-scale pooling or cross-series independence test."
}
```
