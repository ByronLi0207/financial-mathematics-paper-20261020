# WP4: same-dealer daily aggregation

The frozen finite-record classifications are **TREASURY_LIKE**
for the original regression and **TREASURY_LIKE** for the
four-feature regression. Historical headroom wins 7 of 8
complete named comparisons. Original regression historical wins:
4 / 4;
four-feature historical wins: 3 /
4. The complete table retains the exception:

- Four-feature regression, W260/H6: loss change -2.973993%; strict breaches 37 versus 30 for matched F.

## Observation and interpretation boundaries

The exact accepted 18576-row file produces
**930 nonempty source-naive calendar days**, rather than the
instruction's rough780-day expectation (**MISMATCH-WP4-02**). Every nonempty
day, including partial boundary days, remains under the frozen last-record
rule. No weekday filter or deletion was introduced to reach an expected count.
The report clock is the completed day's23:59:59.999999; this is a last-record
proxy, not a reconstruction of an actual financial market close or intraday peak.
The original timestamp timezone and historical release vintage remain unknown.

Validation: 2015-02-24T23:59:59.999999 through 2015-04-24T23:59:59.999999.
Evaluation: 2015-05-24T23:59:59.999999 through 2016-12-27T23:59:59.999999,
501 common issues. The original Treasury absolute2021
dates cannot be shared with this record; the predeclared adaptation carries
over its observation-index geometry (**MISMATCH-WP4-01**).

The same recorded dealer now yields a largely historical-rule-favoring pattern,
so source identity alone cannot describe all the rankings. Physical horizons,
physical histories, update cadence, calendar predictors and sampled targets
change jointly. This does not identify a pure frequency effect or prove a
source-only explanation; it supplies no independent-dealer or prospective
validation. The daily parsimonious gain also contradicts a literal hourly-only
description of conditional gains (**MISMATCH-WP4-03**), while its higher breach
count prevents equating a lower score with a safer limit.

## Decision-map consequence

Add a same-dealer daily row: historical score wins predominate at the executed
histories/horizons, retain the named parsimonious exception and assess its
breaches jointly. Short-history historical F itself also has substantial
breach frequencies; historical score superiority is not a nominal-coverage
guarantee. Keep the hourly/weekly evidence and every adverse daily cell.

## Verification and full record

- Design commit: `1427dc0b943ee77a82ee03a67ec9281c20e2cdf5`.
- Unique actual run: 9.748697s;
  4 / 4 workers;
  12 method slots; 32 declared validation candidates.
- Candidate statuses: `{"COMPLETE": 32}`.
- Independent readback: PASS, 0 differences;
  44 complete score traces and
  596 mature-refit records checked.
- Actual maximum worker RSS: 58359808B;
  maximum observed OS threads: 1.

`summary.json/csv`, `contrasts.csv`, `classification.json`, all four cell
receipts and `readout-bindings.json` preserve the complete aggregation and
comparison record. `daily-results-table.tex` is generated from those source
fields for later manuscript integration. No model or inferential test is added
by this readout. Raw/daily observations and per-issue NPZ arrays stay in task
scratch; their hashes support local audit without redistribution.
