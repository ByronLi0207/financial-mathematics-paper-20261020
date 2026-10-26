# E2 date-field ingestion clarification before any outcome calculation

The original E2 design stays byte-identical. The first preparation stopped on the first official data record, before netting/count processing, screening, ranking, model fitting or scoring. This narrow metadata correction recognizes the confirmed midnight decoration. It does not change an economic observation, sample rule, threshold or grid. Preserve the first failure and disclose the amendment timing.

```json
{
  "schema": "v10-cftc-ingestion-clarification-v1",
  "created_utc": "2026-10-24T22:58:31.222676+00:00",
  "original_design_commit": "acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf",
  "original_design_sha256": "a7aacd4180d27ab810284119b0e4d0cdef79e5d2b0d0c9e7ad2cef8037ab5d78",
  "initial_preparation_failure": "results/v10/cftc/preparation-failure.json",
  "initial_failure_sha256": "5176ab47a6f829f6ef16c3c231405ea128c35172833b92799b3ffb80a528a032",
  "observed_archive": "data/cftc-tff/raw/fin_fut_txt_2006_2016.zip",
  "observed_archive_sha256": "c3a8d01765133a24ce9c082de88933816497d06f1b03eec8c53750bdd818f14b",
  "observed_payload": "F_TFF_2006_2016.txt",
  "observed_line": 2,
  "observed_compact_date": "161227",
  "observed_full_date_literal": "12/27/2016 12:00:00 AM",
  "cause": "The additional official full-date field includes a literal midnight suffix, while the implementation accepted only the registered date-only spellings. Primary YYMMDD identifies the same economic date. No universe selection, net-position calculation or forecast/evaluation was reached.",
  "accepted_literal_suffix": " 12:00:00 AM",
  "normalization": "Only when this separately committed clarification is verified: remove exactly the literal terminal suffix above, then apply the original full-date formats and require exact equality to primary YYMMDD. Do not ignore the full-date field, infer ambiguous dates, accept arbitrary times/timezones or add a general date parser.",
  "unchanged": [
    "all eleven original ZIP bytes/URLs/ownership boundaries",
    "required fields and original date-only formats",
    "complete Monday calendar and every universe/code/unit/exchange/scope-change/ranking rule",
    "all model families, menus, candidate policies, lambda/gamma selection, horizon/history/refit/validation/evaluation/maturity geometry",
    "T1-T3 thresholds, complete-grid denominators, failure/no-retry rules, runtime budgets"
  ],
  "next_preparation_attempt": "results/v10/cftc/preparation-after-clarification",
  "preservation": "Keep every initial failure/audit byte and original source ZIP unchanged; write subsequent preparation audit in the exclusive path above. No numerical cell has run, so no failed numerical cell is rerun. Any further unsupported date spellings remain unavailable; no search over parser alternatives.",
  "interpretation": "Schema clarification after acquiring/seeing source formatting and before any screening/model/forecast outcomes. Disclose this timing rather than claiming all ingestion choices were fixed before data access."
}
```
