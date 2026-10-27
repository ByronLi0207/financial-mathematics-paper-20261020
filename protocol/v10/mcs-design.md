# E3 model confidence sets — design before loss derivation/bootstrap

Use the mature Hansen–Lunde–Nason MCS, not a new test. Publisher/author metadata verifies Econometrica79(2),453–497(2011),DOI10.3982/ECTA5771; official arch8.0.0 documentation/source verifies the R statistic, stationary bootstrap, explicit block size, seed and membership conventions. The older readthedocs latest page currently says7.2; execution is pinned to8.0.0 and its matching official GitHub Pages documentation. No MCS or new missing-loss derivation has yet run.

## Complete procedures and source clocks

Include every828 core saved alias row and all204 complete E2 method cells. The requested98 comparison grids are separate by source, period,H,W. Include the64 already published complete fixed combinations by their unchanged deterministic constituent recipe; preserve the48 unreported-panel-KNN median NA cases and all12 other inherited failed methods. The extra overlapping full-prefix, weekly-retro and fixed-lambda exploratory paths stay archived outside this selected-procedure scope. No source/period or model is selected by an MCS outcome.

Matched F/I storage aliases may be merged only by the explicit identity checks below. Rolling F controls remain distinct; query-nearest one-state F/S/K are conditional state baselines, not plain full-window F/I. All other distinct selection procedures retain their labels, including when they happen to choose I. Exact loss duplicates are grouped for stable library execution and unfolded after the calculation. Literal uniqueness and unique loss-class membership are reported separately.

Every complete input uses the entire declared origin grid and common target. Known prior NA is visible but does not enter a loss matrix. An unexplained changed/missing/misaligned claimed-complete vector fails the whole comparison; it does not trigger a shorter common sample or dropped inconvenient method. Missing stored losses are derived from already saved C/Y only, not new forecasts. Old private vectors remain private. Missing-floor recovery and cost summaries wait for E4.

## Fixed inference and reporting

Run arch8.0.0 MCS at size.10 using statisticR,1000stationary bootstrap replications and block=max(H,ceil(n^(1/3))). Source-specific seeds and method order are deterministic below. One unique loss class is an explicit exact-equality analytic case; other numerical/warning/resource failures remain failed without a different configuration or retry. The approximation presumes suitable loss dependence and is not a universal90% future guarantee under nonstationarity.

Main metrics use matchedF/I membership, literal sole-member frequency and conditional-procedure exclusion. Also disclose a sole surviving equivalence class containing F/I, broader rolling-F membership, every unavailable method, successful/planned denominators and planned-grid bounds for failed MCS comparisons. Related contracts/panels are not independent replications. Full methods/p-values/sets go to the Supplement and machine receipts.

## Frozen machine settings

```json
{
  "schema": "v10-mcs-design-v1",
  "created_utc": "2026-10-24T23:23:01.658276+00:00",
  "saved_inventory": "notes/v10/loss-input-inventory.json",
  "saved_inventory_sha256": "2f10465195e774540d9a49079de37d4e6a56d0e22be634241b1d2a315b08abb2",
  "copy_manifest": ".scratch/v10/copied-private-inputs.json",
  "core_scope": "requested_core_saved_method",
  "include_all_core_saved_alias_rows": 828,
  "core_financial_trace_files": 407,
  "old_expected_comparisons": 64,
  "new_cftc_inventory": "results/v10/cftc/method-inventory.json",
  "new_cftc_inventory_sha256": "722d3de06931a6ca6af80d01b1778dc71888b004bc4239df3c549ab4c3219824",
  "new_cftc_eligibility": "results/v10/cftc/eligibility.json",
  "new_cftc_eligibility_sha256": "0bacfb63a09a43f3f80832afafce403bdd824a6b48279bcf698d842d389943bf",
  "new_cftc_method_cells": 204,
  "total_expected_comparisons": 98,
  "comparison_identity": [
    "period",
    "normalized_source",
    "horizon",
    "window"
  ],
  "periods": {
    "fx_hourly": [
      "original_evaluation",
      "early_2015"
    ],
    "nyfed_weekly": [
      "original_evaluation"
    ],
    "panel": [
      "original_evaluation"
    ],
    "fx_daily": [
      "same_record_daily_evaluation"
    ],
    "cftc": [
      "economic_date_replay_2021_2026"
    ]
  },
  "grid": {
    "fx_hourly": {
      "periods": 2,
      "horizons": [
        6,
        24
      ],
      "windows": [
        720,
        2880
      ],
      "n_by_period": {
        "original_evaluation": 6625,
        "early_2015": 1440
      }
    },
    "weekly": {
      "sources": 13,
      "horizons": [
        6,
        24
      ],
      "windows": [
        52,
        260
      ],
      "n": 277
    },
    "fx_daily": {
      "horizons": [
        6,
        24
      ],
      "windows": [
        52,
        260
      ],
      "n": 501
    },
    "cftc": {
      "sources": 17,
      "horizons": [
        6
      ],
      "windows": [
        52,
        260
      ],
      "n": 260
    }
  },
  "excluded_scope_tags": [
    "supplemental_weekly_retro_2018_2019_period",
    "published_fixed_lambda_path_design_decision",
    "supplemental_overlapping_full_prefix_period"
  ],
  "excluded_reason": "The request specifies two hourly FX periods and original weekly/daily tasks. Overlapping full-prefix and extra weekly retrospective periods are not additional independent evaluations. E6 fixed-lambda paths are exploratory tuning candidates, not complete selected forecasting procedures in this comparison inventory. All remain in old archives; no outcome-based exclusion.",
  "core_method_id": "family::method, within declared comparison identity; preserve full source-qualified label unless the explicit F/I semantic alias rule below applies.",
  "matched_F_aliases": [
    "original::frozen_F",
    "panel_legacy::frozen_F",
    "E6_reference::E6_F",
    "R6::R6_F",
    "daily_FX::F",
    "CFTC::F"
  ],
  "matched_I_aliases": [
    "panel_E5::I",
    "E6_reference::E6_I",
    "R6::R6_I",
    "CFTC::I"
  ],
  "semantic_alias_rule": "Only the named matchedF aliases, and separately matchedI aliases, may be merged to canonicalF/I when complete origins, capacities, targets and loss vectors are exactly equal. Record every alias. If claimed aliases differ, retain every source-qualified procedure with an explicit discrepancy; never choose a favourable version or average them.",
  "other_historical_F_aliases": [
    "original::rolling_F",
    "R6_original_structure::retro_primary_F_reference"
  ],
  "one_state_class": "original::one_state_F/S/K condition on a query-nearest single-state subpool, so they are conditional state baselines, not the full-window matched F/I historical rule.",
  "other_benchmark_aliases": [
    "original::rolling_S",
    "original::rolling_K",
    "original::frozen_S",
    "original::frozen_K",
    "Levy::Levy_L",
    "panel_legacy::Levy_L",
    "mature_baselines::PEAK_POT"
  ],
  "conditional_class": "All remaining non-F/I procedures, including feature QR/KNN, query-nearest one-state baselines, QRF/FHS/SAV, selectedR0-R3, finite ACI wrappers and already published fixed combinations. A procedure selecting infinity or producing an identical forecast is not reclassified ex post as historical.",
  "unavailable_slots": "Retain all12 inherited NA/FAILED selected-method slots and48 previously reported unavailable panel-median combination slots. They have no complete loss vector, enter no bootstrap and are not counted as statistically excluded. Never score a partial vector or rerun a forecast.",
  "combinations": {
    "source": "results/revision-20261023/v6/wp3-combinations.json",
    "source_sha256": "1526d8aa656077445988271c76988c0a950cd95631946add3d8b8642629c7aaa",
    "complete": 64,
    "unavailable": 48,
    "methods": [
      "MEAN_F_QR",
      "MEDIAN_F_QR_KNN"
    ],
    "implementation": "Unchanged v6_combinations.combine_reports: meanF/2+originalQR/2; median np.median(np.stack((F,originalQR,plainKNN)),axis=0). Use original matched frozenF/QR constituents; panels originalQR33, not QR33plus or QR4. No missing KNN substitution.",
    "restriction": "Recover only previously COMPLETE published rows on the original56source/H/W contexts. Reconcile recovered aggregate loss with its unchanged published scores/mean_loss within existing1e-12absolute +2e-14relative arithmetic tolerance; failed reconciliation makes whole comparison FAILED_INPUT, not a new combination result. No new weights, models or periods."
  },
  "loss": "Use complete stored per-point pinball when available; derive only missing loss from saved complete peak/capacity by unchanged v6_inference.pinball_losses(tau=.95). Do not fit, select or issue a new financial report. Keep all private old input/derived vectors in .scratch; publish hashes/aggregate MCS only. CFTC vectors are already public.",
  "floor_boundary": "No missing QR4/Levy floor recovery in E3: their stored loss/target/capacity suffices. Preserve missing floor/reference metadata for the separately registered E4. Existing stored floors may be used for validation and published deterministic combinations; no cost/headroom/excess averages here.",
  "alignment": "Every claimed COMPLETE method must have its exact full declared origin axis, finite/nonnegative full loss, finite capacity/target, and exactly identical target/origins to every other method in that comparison. No intersection, truncation, imputation, rescaling, crossperiod merging or partial-prefix mean. File/hash/shape/target disagreement in a claimed complete input makes the whole comparison FAILED_INPUT. Known inherited NA slots remain explicit and do not prevent comparison of the complete methods.",
  "loss_equivalence": "After semantic aliases, collapse only exact np.array_equal full loss columns for the library call; representative is lexicographically first method ID. Preserve groups and unfold inclusion and p-values to every distinct procedure label. Distinct conditional selection rules/combinations remain distinct ex ante even when forecasts/losses coincide.",
  "all_equal_case": "One unique full loss column: analytic identical-loss set containing every procedure, p=1, with statusCOMPLETE_IDENTICAL_LOSSES; do not feed a one-column matrix into arch. Zero valid methods=>UNAVAILABLE. Single complete method=>analytic singleton with explicit count, no inferential discrimination claim.",
  "package": "arch==8.0.0",
  "implementation": "arch.bootstrap.MCS",
  "confidence": 0.9,
  "size": 0.1,
  "statistic": "R",
  "bootstrap": "stationary",
  "bootstrap_repetitions": 1000,
  "block_size": "max(H,ceil(n**(1/3)))",
  "block_rationale": "Fixed cube-root heuristic bounded below by label horizon; accommodates local overlap. Not selected using any MCS result and not claimed optimal.",
  "seed_prefix": "v10-MCS-20261024|",
  "seed_formula": "identity=json.dumps([period,normalized_source,H,W],separators=(',',':'),ensure_ascii=True); seed=int.from_bytes(sha256((seed_prefix+identity).encode('utf-8')).digest()[:4],'big')",
  "method_column_order": "lexicographic full method IDs after semantic alias handling; fixed independently of loss ranking",
  "membership": "Use arch included/excluded/pvalues properties literally; version8 usesPvalue>size for included and<=size for excluded. No manual boundary adjustment.",
  "failure": "One library attempt per complete comparison. RuntimeWarning, exception, nonfinite/out-of-range p-value, incomplete membership partition, timeout or resource failure =>MCS_FAILED for that whole comparison. Keep error/diagnostics and inventory, no retry, alternate statistic, block length, bootstrap or favourable subset.",
  "report": {
    "primary_historical": "Canonical/qualified matchedF/I only, from the explicit alias lists above; rolling primary controls remain in the model set but their broader historical membership is reported separately.",
    "historical_membership": "fraction of successful comparisons whose unfolded set contains any matchedF/I procedure",
    "historical_unique": "fraction whose unfolded set has exactly one distinct procedure and that procedure is matchedF/I; semantic duplicate storage aliases do not count as distinct procedures",
    "historical_unique_equivalence": "secondary fraction with exactly one surviving exact-loss class containing matchedF/I; this may still contain indistinguishable conditional labels and is not the primary literal uniqueness claim",
    "historical_only": "secondary fraction whose nonempty unfolded set is entirely matchedF/I",
    "conditional_exclusion": "excluded conditional distinct-procedure slots divided by conditional complete-procedure slots in successful MCS comparisons; inherited failed/NA procedures are inventoried separately, not counted as statistical exclusions",
    "failed_denominators": "Always show successful/planned comparisons and failed cells. In addition to successful-denominator fractions, publish all-planned lower/upper bounds obtained by treating failed comparisons (or their conditional slots) as unknown, never as favourable outcomes.",
    "groups": [
      "FX original",
      "FX early2015",
      "Treasury bills",
      "Other NYFed panels",
      "Same-record dailyFX",
      "CFTC",
      "All comparisons"
    ],
    "interpretation": "Descriptive fractions across related, overlapping tasks, no independent-source pooled test or family-wide across-cell coverage guarantee. Stationary-bootstrap approximation on inspected/replayed data does not establish future risk coverage, causal frequency effects or actual economic value."
  },
  "worker_count": 4,
  "worker_internal_seconds": 540,
  "worker_hard_seconds": 600,
  "global_mcs_max_seconds": 1800,
  "one_numerical_thread": true,
  "no_retry": true,
  "code_seal": "Commit artificial-tested adapter/wrapper/driver before source materialization/statistical run; seal numerical code, design commit, source inventory and private/public file hashes before the sole MCS launch. Report-only table derivations may follow without numerical rerun.",
  "method_sources": [
    {
      "url": "https://bashtage.github.io/arch/multiple-comparison/generated/arch.bootstrap.MCS.html",
      "version": "8.0.0",
      "checked_utc_date": "2026-10-24"
    },
    {
      "url": "https://bashtage.github.io/arch/_modules/arch/bootstrap/multiple_comparison.html",
      "version": "8.0.0",
      "checked_utc_date": "2026-10-24"
    },
    {
      "url": "https://pure.au.dk/portal/en/publications/the-model-confidence-set/",
      "reference": "Hansen PR,Lunde A,Nason JM2011. Econometrica79(2),453-497. DOI10.3982/ECTA5771",
      "checked_utc_date": "2026-10-24"
    }
  ],
  "unchanged_loss_and_combination_code_sha256": {
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "v6_inference.py": "1c7fc9a3fe8392c771dde0272966b9a0f0f3c4b969df481d0d6818385dcfd2e5",
    "v6_combinations.py": "24adcb0db6272139301dff65529d91c53a9264b451b1bfd9e238610fbe333513",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf"
  }
}
```
