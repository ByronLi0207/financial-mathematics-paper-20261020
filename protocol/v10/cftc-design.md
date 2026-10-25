# E2 independent CFTC reporting-system application — design before acquisition

This file fixes the source, universe, methods and decisions before any TFF ZIP/CSV/API request. The source preflight inspected only official explanatory material and HTML hrefs. No downloaded observations, performance, eligibility counts or contract rankings have been seen in this v10 task.

## Source and identity decisions

Use Futures Only, dealer-category long minus short in raw contracts. The official2010 annual anchor startsJuly20; therefore complete2010 coverage must come from the official2006–2016 backcast, followed by2017–2026 annual files. Download exactly the ordered URLs below through the normal official browser, at most one attempt each. Any failed required download stops E2 acquisition and analysis; there is no mirror, API, alternate transport or partial-year substitute.

Coverage means one valid row in each generated Monday report-week from2010-01-04 to the global latest position week. Actual position dates are preserved, including holiday Mondays. Duplicate rows cannot be resolved by choosing the last/Tuesday/mean record. Archive ownership by position year is frozen to prevent overlap, and every ownership exclusion is counted. Codes stay literal strings. Exchange and units must remain stable under the limited text normalization below; names are audited and never used to join codes.

The official2023 consolidation warning means unchanged codes alone cannot establish unchanged inventory scope. Conservatively exclude all codes in the three affected prefixes13874/20974/12460 before ranking. This is broader than the three documented plus-suffixed consolidated codes, and its exclusions are reported. No rename whitelist or discretionary post-download exception is allowed. Fewer than20 eligible contracts means fewer are reported; zero means unavailable. Full-history OI ranking is a retrospective universe choice, not a contemporaneous portfolio rule or common-dollar ranking.

## Forecast clocks, maturity and scope

Model feature dates are Monday week labels, using inherited weekly RMS6/26,13-record refits and604800 nominal seconds. Economic position dates remain separate and govern the displayed source-date audit; Monday labels do not claim Monday public information. With N records, evaluation is N-H-260..N-H-1; validation is evaluation_first-H-52..evaluation_first-H-1. There are52 validation and260 evaluation origins and six unissued origins between them. Every validation label completes strictly before evaluation starts. Print the exact indices and both date axes from acquired records before forecasting.

F uses corrected rank and I ordinary rank at the same history/update grid. QR4/QR33 use the E1 six-candidate adapter, not another model family or solver. Existing finite delayed ACI-style calibration is available, so include both ACI_F and ACI_QR33 as a paired ancillary comparison. The code-specific initial pool, exact delayed feedback and coverage-first gamma convention are fixed below. Failed candidates/selected evaluations are never retried; a failed full method has no partial mean and no fallback evaluation.

T1 uses every contract/window cell, T2 requires the full-contract median to meet its interval at both windows, and T3 compares the two complete QR4 medians. Missing required operands remain unassessable. Cross-contract summaries describe related markets; they are not pooled independent-trader tests. Keep every eligible selected contract, every method and every failure.

This is a replay of downloaded economic-date observations. Historical role classification is partly backcast, the full first-release/vintage history is unavailable, and reported positions usually become publicFriday after theirTuesday measurement. Shutdown/holiday/ION delays are documented. The source is independent of NYFed as a reporting system; its futures categories are aggregates and contract counts are not dollar exposures.

## Machine-readable frozen settings

```json
{
  "schema": "v10-cftc-design-v1",
  "created_utc": "2026-10-24T22:43:45.635008+00:00",
  "base_v9_commit": "0d2526cc69092c5158437a0509613bac5e86d47f",
  "source_preflight": "notes/v10/cftc-source-verification.json",
  "source_preflight_sha256": "940f0bacae5f1bbd391b078ec0e2f5ec21e84cac3f195ccbdb777d7f962b5553",
  "report": "TFF Futures Only",
  "target": "Dealer_Positions_Long_All minus Dealer_Positions_Short_All; raw contract counts, no division by OI",
  "official_index": "https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm",
  "downloads_in_fixed_order": [
    {
      "file": "fin_fut_txt_2006_2016.zip",
      "url": "https://www.cftc.gov/files/dea/history/fin_fut_txt_2006_2016.zip",
      "first_position_year": 2010,
      "last_position_year": 2016
    },
    {
      "file": "fut_fin_txt_2017.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2017.zip",
      "first_position_year": 2017,
      "last_position_year": 2017
    },
    {
      "file": "fut_fin_txt_2018.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2018.zip",
      "first_position_year": 2018,
      "last_position_year": 2018
    },
    {
      "file": "fut_fin_txt_2019.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2019.zip",
      "first_position_year": 2019,
      "last_position_year": 2019
    },
    {
      "file": "fut_fin_txt_2020.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2020.zip",
      "first_position_year": 2020,
      "last_position_year": 2020
    },
    {
      "file": "fut_fin_txt_2021.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2021.zip",
      "first_position_year": 2021,
      "last_position_year": 2021
    },
    {
      "file": "fut_fin_txt_2022.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2022.zip",
      "first_position_year": 2022,
      "last_position_year": 2022
    },
    {
      "file": "fut_fin_txt_2023.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2023.zip",
      "first_position_year": 2023,
      "last_position_year": 2023
    },
    {
      "file": "fut_fin_txt_2024.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip",
      "first_position_year": 2024,
      "last_position_year": 2024
    },
    {
      "file": "fut_fin_txt_2025.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2025.zip",
      "first_position_year": 2025,
      "last_position_year": 2025
    },
    {
      "file": "fut_fin_txt_2026.zip",
      "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2026.zip",
      "first_position_year": 2026,
      "last_position_year": 2026
    }
  ],
  "download_transport": "Normal official browser download from the verified HTML anchor, one attempt per archive, in listed order; no prior CLI dataset probe, mirror, API substitute, challenge bypass, retry or transport fallback after failure",
  "download_failure": "Stop all remaining E2 acquisition/analysis on first failed, blocked, timeout, nonofficial or absent required file. Preserve response/download/error evidence with URL, attempt UTC, bytes, SHA256 and status. Continue E3 with CFTC UNAVAILABLE. Do not fabricate20 or a contract-performance figure.",
  "download_per_file_timeout_seconds": 180,
  "annual_ownership": "Filter each archive by its predeclared position-year bounds; retain/audit every excluded original row. No overlap deduplication. Within the owned period any duplicate code/report-week, even byte-identical or Monday+Tuesday, disqualifies that code.",
  "new_data_hosts": [
    "www.cftc.gov",
    "cftc.gov"
  ],
  "financial_classification": "The official TFF financial-futures report universe; no commodity/Disaggregated/Legacy reports or external taxonomy",
  "first_included_position_date": "2010-01-01",
  "first_expected_week": "2010-01-04",
  "week_anchor": "Monday00:00, map each actual economic position date to its containing Monday; require one row in every generated calendar week from2010-01-04 through the global latest owned valid FO position week",
  "global_calendar": "Generate every seven-day Monday, NOT union of observed weeks; any full-calendar gap makes each affected code ineligible. Global latest is fixed by all valid owned FO rows before contract filtering/ranking.",
  "position_date_rule": "Use As_of_Date_In_Form_YYMMDD parsed as2000+YY; cross-check full date column when present. Monday/Tuesday and other official within-week days map to the same week; never require date.diff==7 or Tuesday only. Actual dates retained separately.",
  "date_header_aliases": [
    "Report_Date_as_MM_DD_YYYY",
    "Report_Date_as_YYYY-MM-DD"
  ],
  "required_columns": [
    "Market_and_Exchange_Names",
    "As_of_Date_In_Form_YYMMDD",
    "CFTC_Contract_Market_Code",
    "CFTC_Market_Code",
    "Open_Interest_All",
    "Dealer_Positions_Long_All",
    "Dealer_Positions_Short_All",
    "Contract_Units"
  ],
  "optional_audit_columns": [
    "CFTC_Region_Code",
    "CFTC_Commodity_Code",
    "CFTC_Contract_Market_Code_Quotes",
    "FutOnly_or_Combined"
  ],
  "text_encoding": "utf-8-sig; if decoding fails only, use cp1252 and record it; no schema/content repair",
  "payload": "Exactly one .txt or .csv table payload per ZIP; inspect without filesystem extraction; missing/multiple tables or malformed required schema makes E2 data unavailable. No alternate file type.",
  "date_error": "Missing/unparseable/inconsistent/future position date or missing code prevents a valid global calendar: entire dataset unavailable. Otherwise a named code with invalid count/identity/week records is ineligible with an explicit reason.",
  "counts": "Parse nonnegative integers after trimming whitespace and removing thousands commas; no imputation. Dealer net may be signed. Require all owned in-period counts finite and nonnegative before netting.",
  "code_rule": "Keep CFTC_Contract_Market_Code as stripped string including leadingzeros and plus signs; never splice, coalesce, infer or rename codes. Full-period weekly coverage under one unchanged literal code is mandatory. No code/name similarity matching.",
  "stable_identity": {
    "exchange_field": "CFTC_Market_Code",
    "exchange_normalization": "strip and uppercase only; exactly one nonblank value",
    "units_field": "Contract_Units",
    "units_normalization": "uppercase, collapse whitespace, remove thousands commas; exactly one nonblank value",
    "market_names": "Audit every distinct label and its date span; pure labels never splice histories or override code/exchange/unit criteria. No rename whitelist.",
    "economic_scope_boundary": "Stable observed code/exchange/unit strings do not establish invariant economic coverage or participant membership."
  },
  "known_scope_change_excluded_code_prefixes": [
    "13874",
    "20974",
    "12460"
  ],
  "scope_change_exclusion_reason": "Conservatively exclude the entire three official code families containing the S&P500/Nasdaq100/DJIA consolidated2023 e-micro integration, not just the plus-suffixed series; fixed before seeing values or outcomes. Record every excluded code and label.",
  "eligibility_order": [
    "owned financial FO rows and valid global calendar",
    "unchanged literal code",
    "one valid row every expected week, no duplicates or gaps",
    "stable nonblank exchange and normalized units",
    "exclude all three known scope-change code prefixes",
    "enough complete history for declared validation/training/warmup",
    "rank mean Open_Interest_All on the common full calendar, descending; exact tie code lexicographic ascending",
    "first20 or all if fewer; zero means unavailable"
  ],
  "top_contracts": 20,
  "rank": "Full-calendar arithmetic mean total market Open_Interest_All, not absolute dealer net or dollar risk. Whole-sample selection is disclosed as retrospective universe selection; no contemporaneous investable-universe claim.",
  "model_clock": "Weekly Monday00:00 labels for build_features; retain actual economic position dates for provenance and displayed splits. Monday labels are feature/time indices, NOT public decision or availability times.",
  "horizon": 6,
  "windows": [
    52,
    260
  ],
  "refit_step": 13,
  "feature_rms_short": 6,
  "feature_rms_long": 26,
  "nominal_gap_seconds": 604800,
  "tau_numerator": 19,
  "tau_denominator": 20,
  "split_formulas": {
    "N": "number of complete common weekly observations, indexed0..N-1",
    "evaluation_first": "N-H-260",
    "evaluation_last": "N-H-1",
    "validation_last": "evaluation_first-H-1",
    "validation_first": "validation_last-51",
    "validation_n": 52,
    "evaluation_n": 260,
    "unissued_gap_n": 6,
    "completion": "All validation labels end strictly before evaluation_first; all evaluation labels end<=N-1.",
    "training": "At refit r use W completed origins r-H-W+1..r-H inclusive, latest label ends r; conditional valid_from26. Both segments start their own13-observation refit grid; all model transforms/response scaling use only that pool.",
    "date_reporting": "After acquisition write exact indices, Monday-clock dates and actual economic first/last/label-completion dates from downloaded files into results/v10/cftc/splits.json before formal forecasting."
  },
  "methods": [
    "F",
    "I",
    "QR4",
    "QR33",
    "ACI_F",
    "ACI_QR33"
  ],
  "menus": {
    "QR33": [
      0.001,
      0.01,
      0.1,
      1.0,
      10.0,
      "inf"
    ],
    "QR4": [
      0.001,
      0.01,
      0.1,
      1.0,
      10.0,
      "inf"
    ]
  },
  "finite_forecast": "Unchanged v8_mechanism_mc.forecast_report through sealed v10_menu adapter; fixed solver defaults, feature transform, response scale and floor. No new model family.",
  "historical": "Unchanged empirical_headroom.predict; F corrected ceil((W+1)*19/20), I ordinary ceil(W*19/20); both use matched W and13-record refits/current absolute-position floor.",
  "conditional_selection": "v10_menu.select_candidate: QR33 allsix required, QR4 eligible completed candidates; exact equal validation mean pinball selects strongest penalty incl inf. Retain each failed candidate, never retry; write selection before evaluation. Selected evaluation failure makes the full method cell FAILED, no fallback or partial score.",
  "ancillary": {
    "methods": [
      "ACI_F",
      "ACI_QR33"
    ],
    "algorithm": "Existing v6_aci.aci_stream and select_gamma; finite delayed ACI-style calibration, no canonical coverage guarantee",
    "gammas": [
      0.001,
      0.005,
      0.01,
      0.05
    ],
    "gamma_selection": "Attempt allfour exactlyonce; existing select_gamma chooses completed full-validation candidates by exact absolute coverage distance to1/20, then pinball, then smaller gamma; none eligible=>NA. All failures stay in inventory.",
    "warmup": "Existing initialization_grid(validation_first,H,W,13,min_feature_index) with min0forF,26forQR33; all earlier legal warm issue origins through validation_first-1, refit13, at least19mature conformity scores. No extra tau fits. Selected QR33 lambda is frozen before its separate warmup segment. Reuse its saved candidate validation and selected evaluation bases, never refit a segment twice.",
    "state": "Initial alpha1/20; exact Fraction updates/projection, finite corrected rank, latestW mature scores, H-record delayed feedback using actual earlier wrapped reports; concatenate validation and evaluation only after gamma freeze, verify validation prefix unchanged; no invented issues in the unissued gap.",
    "failure": "Base QR33 ineligible/fails=>ACI_QR33 unavailable. Insufficient warmup, no complete gamma or selected evaluation failure=>whole ancillary cell unavailable/failed. Never retry, retune or replace it."
  },
  "scoring": "Existing score_predictions at tau19/20, full260points only; save origins, capacities, peak, floor, per-point pinball, strict_breach, overrun, unused for every complete method. Incomplete outputs kept as failed diagnostic bytes but never scored as a full method.",
  "T1": {
    "requirement": "At least60% of all selected-contract x two-window cells have min(F,I) mean loss strictly below QR33.",
    "minimum_inclusive_fraction": 0.6,
    "denominator": "2K, all selected contracts and bothW; any required operand missing=>UNASSESSABLE, no successful-subset denominator."
  },
  "T2": {
    "requirement": "For each W, median across allK contracts of100*(QR33/F-1) falls in closed[-10,+10]percent; SUPPORT requires both windows.",
    "lower_inclusive_pct": -10.0,
    "upper_inclusive_pct": 10.0,
    "failure": "Missing required contract/method or nonpositiveF mean=>that window UNASSESSABLE; never replace with a partial median."
  },
  "T3": {
    "requirement": "Across allK contracts, QR4/F relative-loss median atW260 is strictly lower than atW52.",
    "strict": true,
    "failure": "Any required operand incomplete=>UNASSESSABLE."
  },
  "summary": "One row per selected contract with all methods and bothW; full detailed cells/candidates/failedslots retained. Across-contract medians/fractions descriptive only, no independent-series pooled significance or dollar aggregation.",
  "worker_count": 4,
  "worker_internal_seconds": 540,
  "worker_hard_seconds": 600,
  "formal_max_seconds": 3600,
  "one_numerical_thread_per_worker": true,
  "no_pilot_or_adaptive_grid": true,
  "code_seal": "After synthetic tests, commit all v10 CFTC executable code and seal hashes, protocol commit and acquired bytes before the sole formal launch. Check archive/input hashes and code before/after use.",
  "information_time": "Economic-position-date replay of downloaded vintage, same structural limitation as Treasury. Normally Tuesday positions publishedFriday15:30ET, with documented holiday/shutdown/ION delays; exact full historical first-release dates unavailable. Not a tradable first-release-vintage backtest.",
  "interpretation": "Independent reporting system, category-aggregated dealer/intermediary futures positions; not individual dealers, independent contracts, complete balance-sheet inventory or causal frequency identification.",
  "failure_outputs": "If official acquisition fails, provenance lists the attempt and every NOT_ATTEMPTED required URL, CFTC outcome/T1-T3 UNAVAILABLE, empty selected-contract inventory and explicit missing table/figure receipt. Do not run forecasts, do not synthesize contracts; E3/E4 retain CFTC unavailable scope.",
  "inherited_or_E1_code_sha256": {
    "v10_menu.py": "e91c942d6a24cb833ceaed48c282360a578325c0ebf3c5b370b42c4b14ca5014",
    "v8_mechanism_mc.py": "71134570e1b4d63f98dcd2bb4eb7c1bc596a516b3ca8243b77ad913670a7d7c4",
    "empirical_headroom.py": "db5d73facae28432bb0617d173e5b4c933d95e52b43f9363543e21194919412e",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "v6_aci.py": "e81005a25ca7b94dec86540981b890c945c280478b861e7416f7fb852f67b15a",
    "run_study.py": "8d8c305357e888f7665beed67dcc8f8a3619070a33a30d935c9582512db18f1f"
  },
  "full_date_formats": [
    "%Y-%m-%d",
    "%m/%d/%Y"
  ],
  "report_type_marker": "When FutOnly_or_Combined is present, normalize by removing nonalphanumerics and uppercasing; only FUTONLY or FUTURESONLY accepted. Missing optional marker is documented and file identity comes from the verified official FuturesOnly URL; any contradictory/unrecognized populated marker makes data unavailable.",
  "required_year_payload": "Each requested annual file must contain at least one row in its declared position-year ownership; an empty required year is unavailable, never replaced by a partial earlier-vintage universe.",
  "byte_provenance": "Archive response bytes retained unchanged; URL is the actual observed official href, attempt/start/end UTC from browser/writer, local byte count and SHA256. Record unobservable HTTP/redirect information as unobserved rather than inventing it. Any observed nonofficial destination is a stop."
}
```
