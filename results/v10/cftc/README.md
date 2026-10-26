# CFTC application receipt map

`eligibility.json`, `sources.json`, `splits.json` and the `sources/` vectors are the final prepared input from the fixed universe after two outcome-free schema clarifications. `preparation-status.json` is a snapshot taken before model execution. Once present, `summary.json`, `method-inventory.json` and `formal/` are the authoritative forecast results, including every failed slot.

The original design was committed before every data download. Two additional standalone commits clarified a literal midnight date decoration and exact integer values written with a zero decimal part. Both preceded every candidate validation, model fit, forecast and score. All numeric observations, sample filters, model/penalty grids and registered T1–T3 thresholds stayed fixed. The amendment timing is explicitly disclosed; ingestion is not described as wholly fixed before data access.

Earlier technical attempts remain intact:

- `preparation-failure.json` and root `source-audit.json`: first-record date-format stop, before screening.
- `preparation-after-clarification/`: date-normalized parsing, but the old count lexer incorrectly rejected integral decimal-zero text, yielding a zero-universe technical receipt. The root `unavailable.json` is the same historical attempt and does not describe the final prepared universe.
- `preparation-after-count-clarification/`: final successful archive audit. Prior current metadata was backed up as `.bak` before replacement and copied verbatim into the preceding attempt directory.

These technical stops are neither model negative findings nor evidence for external validity. No numerical forecasting cell has been retried. Source response ZIPs and every earlier receipt are preserved. Original download provenance and the unchanged raw bytes are at `data/cftc-tff/`.
