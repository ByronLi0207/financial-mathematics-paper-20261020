# E2 exact-integer count notation clarification before model outcomes

The original rule requires nonnegative integer values. The confirmed official decimal-zero notation represents exactly those values. This correction changes no numeric observation, screening criterion or prediction rule. The first zero-eligibility receipt arose from a lexical parser defect and is preserved as a technical attempt, not reported as a scientific finding. No model has run.

```json
{
  "schema": "v10-cftc-count-notation-clarification-v1",
  "created_utc": "2026-10-24T23:03:41.438664+00:00",
  "original_design_commit": "acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf",
  "date_clarification_commit": "4d46550c23a54662112979acc891ba4f903dc39c",
  "observed_archive": "data/cftc-tff/raw/fin_fut_txt_2006_2016.zip",
  "observed_archive_sha256": "c3a8d01765133a24ce9c082de88933816497d06f1b03eec8c53750bdd818f14b",
  "observed_payload": "F_TFF_2006_2016.txt",
  "observed_line": 12198,
  "observed_code": "020601",
  "observed_position_date_compact": "161227",
  "observed_literal_values": {
    "Open_Interest_All": "594263.000000",
    "Dealer_Positions_Long_All": "6981.000000",
    "Dealer_Positions_Short_All": "36764.000000"
  },
  "cause": "The earlier lexical integer parser rejected mathematically integral official decimal-zero count notation. This incorrectly classified otherwise observed rows as INVALID_COUNTS. No model fitting, candidate validation, forecast score or T1-T3 outcome exists.",
  "prior_universe_receipt": "results/v10/cftc/eligibility.json",
  "prior_universe_sha256": "e3274cc66f417fbf23a49a81e302a078dab20893325125a812ee94bad94616a0",
  "prior_unavailable_receipt": "results/v10/cftc/unavailable.json",
  "prior_unavailable_sha256": "fde6a9336a4300c8aa51691a921b0d30246a1a7814f9cb608de86aaa8f23acb8",
  "correction": "When this separate clarification is verified, accept the existing unsigned integer/thousands-group text grammar followed optionally by a decimal point and one or more zero digits. Convert by exact integer arithmetic after proving the fractional part is allzero. No float rounding, scientific notation, nonzero fraction, sign, blank, NA, imputation or row replacement.",
  "accepted_zero_fraction": true,
  "next_preparation_attempt": "results/v10/cftc/preparation-after-count-clarification",
  "preservation": "Copy the prior zero-universe and unavailable receipts verbatim into their originating preparation-after-clarification directory and retain .bak copies before replacing untracked current metadata; commit the preserved attempt snapshots. Original raw ZIPs, failed-date receipt, original design and date clarification remain unchanged.",
  "unchanged": "Every observation value, ownership/year/date rule, literal code, gap/duplicate/unit/exchange/scope exclusion, OI ranking/top20 rule, methods, lambda/gamma grid, splits, T1-T3 threshold and denominator, resource and numerical no-retry policy. This restores the already specified nonnegative-integer value semantics; it does not relax any required count to a noninteger.",
  "timing_boundary": "The zero-universe metadata result and one concrete raw count-format example have been inspected. No forecast performance or model-selection outcome has been seen. Disclose both schema clarifications as post-acquisition and before all model outcomes; never call the entire ingestion workflow predata-blind."
}
```
