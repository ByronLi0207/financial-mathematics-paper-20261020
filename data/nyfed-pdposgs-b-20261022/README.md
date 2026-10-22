# Primary Dealer Statistics: accepted PDPOSGS-B snapshot

This folder preserves the **unchanged response used in this study**, rather than a new dataset or a fresh validation sample. The source is the Federal Reserve Bank of New York's Treasury-bill dealer long-minus-short aggregate. Units are millions of U.S. dollars. The CSV has706 observations, 3 April 2013–7 October 2026, and the exact original three-column header.

The original response completed 22 October 2026 at 07:26:01.658694 UTC. Its 23,315 bytes have SHA-256:

```text
9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb
```

The [CSV](PDPOSGS-B.csv) is byte-for-byte identical to that accepted input; no columns, records, line endings or values were changed. The [provenance record](provenance.json) supplies the actual original acquisition times and archive identity. The original response contains its header and data records; attribution is supplied here without modifying the CSV.

## Source and applicable conditions

[Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) · [Original API route](https://markets.newyorkfed.org/api/pd/get/PDPOSGS-B.csv) · [NYFed Terms of Use](https://www.newyorkfed.org/privacy/termsofuse), last updated 9 June 2023, checked 22 October 2026.

© 2026 Federal Reserve Bank of New York. Content from the New York Fed subject to the Terms of Use at newyorkfed.org.

The observations remain subject to the source's permissions, conditions and restrictions, including attribution and no implied endorsement. They are **excluded from any study-code license**; this archive imposes no additional restriction on the source content. The study's analysis and interpretations are its own, not findings or endorsements of the New York Fed. No source logo is reproduced.

## Reproduction and scientific scope

Use this exact file wherever a documented command requests the accepted NYFed CSV, for example by passing its absolute path as the NYFed source argument. Retain the command's existing strict SHA/schema checks. The full paired-source study still requires the separately obtained FX input; archiving this file does not settle that input's redistribution rights or turn the entire experiment into a data-independent download.

This is one **downloaded vintage**, not an archive of original publication releases or all revisions. Economic dates do not establish contemporaneous public availability. Later online responses can grow or be revised; a mismatching response should not be truncated or spliced to imitate this file. No new forecast, diagnostic, parameter choice or financial comparison was run to create the archive. See the [source measurement record](../../notes/revision-20261022/nyfed-data-source-draft.md), [issue-clock analysis](../../notes/revision-20261022/issue-clock-target-and-known-floor.md) and [main replication guide](../../README.md).
