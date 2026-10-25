# F2 CFTC validation-length comparison

Status: frozen before the first v12 experiment pilot/evaluation.

The evaluation sample, target, training window and refit schedule do not change. V156 starts104records earlier thanV52, exactly8 refit steps, so the overlapping validation origins share their original refit grid. The change supplies more overlapping validation observations, not156 independent labels. This is a retrospective sensitivity comparison, not a new holdout or coverage result.

All indices are zero-based and inclusive. All times/run caps and results are recorded by the driver. A separate code/input seal must precede the run, and the following JSON is the executable scientific contract.

```json
{
  "base_commit": "452064866c2bdc4166b89d09d67b0cb2bc0ae415",
  "tau": 0.95,
  "menu": [
    0.001,
    0.01,
    0.1,
    1.0,
    10.0,
    "inf"
  ],
  "methods": [
    "QR33",
    "QR4"
  ],
  "inherited_code_sha256": {
    "v10_menu.py": "e91c942d6a24cb833ceaed48c282360a578325c0ebf3c5b370b42c4b14ca5014",
    "v8_mechanism_mc.py": "71134570e1b4d63f98dcd2bb4eb7c1bc596a516b3ca8243b77ad913670a7d7c4",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_sources.py": "a56cb374cff93b5d18889d2b69a993ad1a3b871ee20bb8349fad04b2fc839709",
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "empirical_headroom.py": "db5d73facae28432bb0617d173e5b4c933d95e52b43f9363543e21194919412e",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "round2_panel_sources.py": "e0b553d370a23f9dcc38caeb649e048bb880c6fcc9b93536d2e9a30402c4c17d",
    "v6_inference.py": "1c7fc9a3fe8392c771dde0272966b9a0f0f3c4b969df481d0d6818385dcfd2e5"
  },
  "input_provenance": {
    "raw_sources": [
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/1hourNetPositionsKaggle.csv",
        "fields": [
          "datetime",
          "NetPosUsd",
          "NetUsdPnL",
          "AbsVolume",
          "Mid"
        ],
        "rows": 18576,
        "date_key": "datetime",
        "first_date": "2014.02.05T01:00:00.000",
        "last_date": "2017.01.24T00:00:00.000",
        "bytes": 1286391,
        "sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice.",
        "index_date_metadata": {
          "3071": "2014.08.04T00:00:00.000",
          "7535": "2015.04.21T00:00:00.000",
          "8974": "2015.07.13T23:00:00.000",
          "8999": "2015.07.15T00:00:00.000",
          "10438": "2015.10.06T23:00:00.000",
          "10463": "2015.10.08T00:00:00.000",
          "11902": "2015.12.30T23:00:00.000",
          "11927": "2016.01.01T00:00:00.000",
          "18551": "2017.01.23T00:00:00.000"
        }
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 706,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-07",
        "bytes": 23315,
        "sha256": "9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSCS-TOT.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 24713,
        "sha256": "169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSFGS-TOT.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 25495,
        "sha256": "00f321abeebf1aaee1af68dc7ab41bb403eafe770c915f4229fc80e18e3586de",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSGSC-G2L3.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 25930,
        "sha256": "10c35a9516154011c0821d12eb86052f7d4df01a4c7b0cddee4878b72868678c",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSGSC-G3L6.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 26090,
        "sha256": "453f1a2458a2c9c7049d9128ccc9d1945b5a61e469ab1c8112577b3ad7539fa5",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSGSC-G6L7.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 25967,
        "sha256": "429d542e2cda305d8d5c458592b57b4042c9f479ce4135e3ab3610951ae6b35d",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSGSC-G7L11.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 26639,
        "sha256": "0b102760c5e4cc181d438d9c8618f8990d047ac8ecb9bd85bac63851742199d0",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSGSC-L2.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 24714,
        "sha256": "7ab08e2b39534ca67f43006949a7504334d90b63034b9ed3cd5248e59c9126bf",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSMBS-TOT.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 25680,
        "sha256": "2e493d17890870eff6eca247c62b9175fcf7564a70d87e63ee520561bb71efcb",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSTIPS-G11.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 25017,
        "sha256": "810355b1cf4c93282dcc76fa6fdc41bbccc1ec7d3675024a2400e2c27c695d5d",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSTIPS-G2.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 24761,
        "sha256": "8e54675071813501a240c1ea3a2ca4fda0f2e2aa88b1ea1bb2852fe6a9f6c894",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSTIPS-G6L11.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 26797,
        "sha256": "1e3ee3a336be321f47a3f7481591b15650607baa3fb46be7da99968ccbea7845",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      },
      {
        "path": "/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSTIPS-L2.csv",
        "fields": [
          "As Of Date",
          "Time Series",
          "Value (millions)"
        ],
        "rows": 707,
        "date_key": "As Of Date",
        "first_date": "2013-04-03",
        "last_date": "2026-10-14",
        "bytes": 24883,
        "sha256": "dc3dd1ef3f9a364c25789523a5b2f0d46860681808005620055db4a47c996995",
        "copy_requirement": "Optional date/provenance audit only; saved C/B/Y vectors suffice."
      }
    ],
    "cftc_sources": [
      {
        "source_index": 0,
        "code": "044601",
        "path": "results/v10/cftc/sources/s00.npz",
        "bytes": 9573,
        "sha256": "15301fe97329711d1a7bf93546c9252bd71a9787215a286a1e28297494b86e32"
      },
      {
        "source_index": 1,
        "code": "043602",
        "path": "results/v10/cftc/sources/s01.npz",
        "bytes": 9612,
        "sha256": "70e0354eaa93982a21890dec5ce81cdd4887cc7c56898390140e2471211e479e"
      },
      {
        "source_index": 2,
        "code": "042601",
        "path": "results/v10/cftc/sources/s02.npz",
        "bytes": 9520,
        "sha256": "aa865f0a0cbeb77d71c644d94ed49ea4549ec5f5f0d66dc3645f79f39559196b"
      },
      {
        "source_index": 3,
        "code": "045601",
        "path": "results/v10/cftc/sources/s03.npz",
        "bytes": 9599,
        "sha256": "eb7d6bb259637b65aca2cdb4b31e18c237d9c486c0fbce2f8916a49a6b19eb8f"
      },
      {
        "source_index": 4,
        "code": "020601",
        "path": "results/v10/cftc/sources/s04.npz",
        "bytes": 9365,
        "sha256": "f49b35626eda89da64ba05f6cad7e144b34b897b45b119c102d6a4f51bb2eb96"
      },
      {
        "source_index": 5,
        "code": "099741",
        "path": "results/v10/cftc/sources/s05.npz",
        "bytes": 9466,
        "sha256": "96a6ded494961a95225bb967f92f791998077de459e84dac8cee6129bd6d5014"
      },
      {
        "source_index": 6,
        "code": "1170E1",
        "path": "results/v10/cftc/sources/s06.npz",
        "bytes": 9375,
        "sha256": "e378513803e88b245daf7131ff01ed262b32a28cc5e40607a6275d6fd3c4577b"
      },
      {
        "source_index": 7,
        "code": "097741",
        "path": "results/v10/cftc/sources/s07.npz",
        "bytes": 9513,
        "sha256": "cd37daf92427cb6f17fe3c0207b830ecd575592c00f05f2247e2a9433572ed56"
      },
      {
        "source_index": 8,
        "code": "096742",
        "path": "results/v10/cftc/sources/s08.npz",
        "bytes": 9491,
        "sha256": "73ff25092f9270894000baea23b24343ec01d998306104c610f3ab97c9faaae9"
      },
      {
        "source_index": 9,
        "code": "095741",
        "path": "results/v10/cftc/sources/s09.npz",
        "bytes": 9387,
        "sha256": "c1cf66bb346bc38abe8554ce4e5fd09b6e41a53d4f826ef71869ed1ae5304f15"
      },
      {
        "source_index": 10,
        "code": "090741",
        "path": "results/v10/cftc/sources/s10.npz",
        "bytes": 9465,
        "sha256": "cf543927636b6d93e35e928cffe0ef7b254b4e8915a9071de073514bfad9d5f8"
      },
      {
        "source_index": 11,
        "code": "232741",
        "path": "results/v10/cftc/sources/s11.npz",
        "bytes": 9457,
        "sha256": "0eeaf81d454f2f7d8bb842ffc52f9548f111a5dd945b7770dbdebd5fee3d6fd5"
      },
      {
        "source_index": 12,
        "code": "33874A",
        "path": "results/v10/cftc/sources/s12.npz",
        "bytes": 9138,
        "sha256": "ce7484a6fa2167788e3ee1cf978e2a3b6059465ef49134b2887799c77859d2a1"
      },
      {
        "source_index": 13,
        "code": "240743",
        "path": "results/v10/cftc/sources/s13.npz",
        "bytes": 9113,
        "sha256": "e09931c22d291f48feeaffe30d8e34bd93ba63d1fa0a76bfb50e0541c6827ef7"
      },
      {
        "source_index": 14,
        "code": "092741",
        "path": "results/v10/cftc/sources/s14.npz",
        "bytes": 9242,
        "sha256": "791819f3b1605d62cf56337fbe316cdd1c47bc6eed4b54e3802fef8d56d7cea5"
      },
      {
        "source_index": 15,
        "code": "098662",
        "path": "results/v10/cftc/sources/s15.npz",
        "bytes": 8943,
        "sha256": "604483e315fe10a251cdb36eb1b58fa2217acbcdd00099765df5238e7f3feb41"
      },
      {
        "source_index": 16,
        "code": "112741",
        "path": "results/v10/cftc/sources/s16.npz",
        "bytes": 9199,
        "sha256": "7e497c720c7d7579410bc83404a44c978eb2c2e41f4ded8fbe9fe92e16fa2471"
      }
    ],
    "panel_selection_sha256": "c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858"
  },
  "source_policy": "Existing inventory-pinned v9 FX/panel copies, current billCSV and prepared CFTC NPZ only; no acquisition, v3 access or old-dir writes.",
  "refit_rule": "r=a+d*floor((t-a)/d) separately anchored in each validation/evaluation segment",
  "training_rule": "r-H-W+1..r-H inclusive; label_end<=r; issue-known predictors; original transforms/solver tolerances unchanged",
  "tie_rule": "Exact equal validation means favor stronger lambda; infinity strongest; finite oracle exact ties favor larger finite lambda; no tolerance ties.",
  "failure_policy": "Whole method-cell FAILED on any required candidate/operand numerical or structural failure; no successful-subset oracle, no retries. Already failed identical candidate cache propagates across phases; unattempted candidates are not failures. Resource omissions have distinct NOT_RUN_RESOURCE_LIMIT status.",
  "score": "v6_inference.pinball_losses with exact decimal tau weights and study_core.stable_mean; strict breach Y>C, full declared origins only.",
  "public_private": "Aggregate candidate means/selections/failures/criteria/figure mappings public; raw restricted FX and per-origin traces private .scratch/v12 with SHA manifests.",
  "code_gate": "Before first financial computation, protocol must be a standalone ancestor Git commit, working bytes equal committed bytes, and v12 code/input seal recorded from committed code. No threshold/setup alteration after run start.",
  "resource": {
    "workers": 4,
    "requested_numerical_threads_per_worker": 1,
    "max_worker_rss_bytes": 2147483648,
    "no_warm_start_or_solver_retuning": true
  },
  "experiment": "F2",
  "families": [
    "cftc"
  ],
  "validation_lengths": [
    52,
    156
  ],
  "windows": [
    52,
    260
  ],
  "H": 6,
  "evaluation": "N-H-260 .. N-H-1 inclusive (611..870 atN877)",
  "validation": "end=evaluation_first-H-1; start=end-V+1; V52 553..604, V156449..604",
  "dates": {
    "evaluation": [
      "2021-09-21",
      "2026-09-08"
    ],
    "validation52": [
      "2020-08-11",
      "2021-08-03"
    ],
    "validation156": [
      "2018-08-14",
      "2021-08-03"
    ]
  },
  "whole_contract_exclusion": "Before any model, reject entire contract for both histories/methods if either source fingerprint/complete grid fails, or earliest V156 training origin validation_first-H-maxW+1 <feature_valid_from26. Equivalent N>=719 for the declared geometry; no replacement, splicing or relaxed W.",
  "selection": "All six validation candidates required per method, same strongest exact-tie rule. Evaluate only its selected candidate on unchanged evaluation origins; valid completed F1 evaluation cache may be reused after source/code/tau/H/W/d/origin fingerprint checks; prior failed identical candidate is not retried.",
  "predictions": {
    "V1": "For QR33, each W separately: median across the same eligible contracts of relative excess atV156 minus itsV52 median <=-5 percentage points. Overall V1 requires bothW. QR4 separately sensitivity.",
    "V2": "ForQR33 eachW, fraction of eligible contracts selecting infinity atV156 strictly exceeds V52; overall requires bothW. QR4 separate.",
    "missing": "Report planned eligible denominator and completion for every arm. If any required eligible pair is missing, threshold status for thatW is UNDETERMINED; complete-pair medians explicitly descriptive. A complete failingW makes overall NOT_SUPPORTED; bothsupported required for overallSUPPORTED."
  },
  "runtime": {
    "total_cap_seconds": 2400,
    "order": "All17 W52 QR33, then all17 W260 QR33, then QR4W52, thenQR4W260. Contracts in fixed source order, V52then156; evaluationcache reuse no new retries.",
    "predeclared_reduction": "Only before formal launch, based on F1 timing and remaining F4reserve: trim QR4 first as entire secondary method, then W260 as entire secondary history if projected cap exceeds. Retained groups keep all17 contracts. Missing combined criteria remain unassessable; preserve full planned inventory.",
    "max_cell_wall_seconds": 300
  }
}
```
