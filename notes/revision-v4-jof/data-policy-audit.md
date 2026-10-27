# v4 data-policy and tracked-source audit

Checked **23 October 2026, 17:13 UTC**. Scope: current Git index and existing source/provenance records, plus public source-policy/metadata pages. No raw dataset was downloaded, no existing file was changed, and this audit is not a certification of every historical Git blob or of a rightsholder chain.

## NYFed: conditional redistribution basis

The official [Terms of Use](https://www.newyorkfed.org/privacy/termsofuse), displaying last update **9 June 2023**, were read under *Permissible Use*, *Conditions*, *Use Restrictions*, and *Third Party Content*. They permit copying, distribution and derivatives for personal/business use, conditional on preserving source/copyright identifiers and free-source URLs, marking modifications, avoiding distortion, retaining the same permissions/restrictions, and avoiding implied endorsement. Third-party material and identified special categories can have additional restrictions. No Primary Dealer Statistics-specific restriction was found in the accessed terms or [owning page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics). The [Markets API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html) expressly subjects API data to those terms.

**Conclusion for this package:** keep the existing accepted primary-dealer aggregate snapshot with its attribution/provenance. Do not call it public domain, put it under a code license, imply NYFed endorsement, or silently replace it with a later vintage. This is a conditional source-based reuse conclusion, not a new license grant by the study.

Existing exact files and current byte checks:

| Tracked file | Bytes | SHA256 |
|---|---:|---|
| `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv` | 23,315 | `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb` |
| `data/nyfed-pdposgs-b-20261022/README.md` | 3,388 | `bea93f1facf30f70daf5ec42ce089b7f5ff360b38acd99c4000a7ee7518369b8` |
| `data/nyfed-pdposgs-b-20261022/provenance.json` | 1,880 | `fc902b76a9f61213dd5be14c8e69fd431ba80caa7d34498b0fda883a9b8734d6` |

The README already contains source attribution, a direct terms link, an explicit exclusion from code licensing, and the study's independent interpretation/no-endorsement boundary. The CSV is the accepted unchanged header plus 706 records; the provenance matches the original accepted-source fingerprint. Preserve these files together. This matches the existing delivery-only exception in `notes/revision-20261022/nyfed-source-archive-delivery-addendum.md`, without rewriting the original frozen no-raw-delivery plan.

## Kaggle FX: current metadata does not establish open redistribution

Public metadata endpoint (no raw request, no credentials):

[Dataset metadata API](https://www.kaggle.com/api/v1/datasets/view/davidlindsay1979/net-position-time-series-dataset) · [Original dataset page](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset)

The web reader could not open the JSON endpoint; an ordinary unauthenticated metadata-only HTTPS request succeeded. No permission change or access restriction workaround was used.

Actual selected response fields:

```json
{
  "checked_utc": "2026-10-23T17:13:02.257684+00:00",
  "http_status": 200,
  "content_type": "application/json",
  "metadata_bytes": 4552,
  "metadata_sha256": "7327238e6653bfbb68a5a83fd52cfc679d9358bc0232e9fdc9f6acac1b91f956",
  "id": 648361,
  "ref": "davidlindsay1979/net-position-time-series-dataset",
  "title": "Net Position Time Series Dataset",
  "currentVersionNumber": 2,
  "lastUpdated": "2020-07-20T12:21:30.54Z",
  "licenseName": "Data files © Original Authors"
}
```

The returned version list identifies version 2, created `2020-07-20T12:21:30.54Z`, as the current version. The observed rights label is **not a verified permissive redistribution license**. It does not establish the complete underlying rightsholder chain or authorize an open raw-data mirror. This audit does not infer a categorical legal prohibition from silence; the operative package rule is to **withhold raw FX data until a suitable redistribution grant is verified**.

The existing source records `protocol/study-spec.json` and `results/run-manifest.json` already record version 2, the label, `raw_redistribution_verified: false`, and the accepted member `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`, 1,286,391 bytes, SHA256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`. Keep acquisition instructions/fingerprint and use the approved wording **“available from the original Kaggle source”**. Do not promise that the complete analysis can run from the public repository without separately obtaining this source.

## Current tracked-file inventory and privacy boundary

Read-only inventory used `git ls-files -z`, then inspected tracked CSV headers/counts and JSON array schemas. Actual compact output:

```text
tracked_total 1296
tracked_data_paths 3
tracked_csv_paths 53
tracked_binary_arrays []
tracked_known_raw_fx []
tracked_scratch []
```

The only tracked source-observation CSV found is the NYFed snapshot above. The other 52 tracked CSVs are aggregate results/diagnostics or plotted aggregate score curves. No tracked `.npz`, `.npy`, `.parquet`, `.feather`, or `.arrow` source/forecast container was found; no tracked `.scratch/` path or `1hourNetPositionsKaggle` path was found.

Long JSON arrays were inspected rather than treated as private forecast vectors merely because they are long. Existing FX `evaluation-*` / `validation-*` fit diagnostics and `parsimonious/*` diagnostics contain solver/refit summaries and coefficient hashes. `round2/baselines/*` refits contain GARCH parameter/optimizer diagnostics and hashes. These are fitted summaries, **not individual observed FX positions or per-origin issued forecast trajectories**. The inventory does not claim that a schema/name check proves all possible privacy or inference risks absent.

Panel source records are **metadata only** at:

```text
results/revision-20261023/round2/panel/selection-manifest.json
results/revision-20261023/round2/panel/sources/<SERIES_KEY>/provenance.json
```

All 14 source records explicitly say raw redistribution is not included and reference ignored `.scratch/round2/panel-data/<SERIES_KEY>.csv` paths. Eligible keys are `PDPOSCS-TOT`, `PDPOSFGS-TOT`, `PDPOSGSC-G2L3`, `PDPOSGSC-G3L6`, `PDPOSGSC-G6L7`, `PDPOSGSC-G7L11`, `PDPOSGSC-L2`, `PDPOSMBS-TOT`, `PDPOSTIPS-G11`, `PDPOSTIPS-G2`, `PDPOSTIPS-G6L11`, and `PDPOSTIPS-L2`; `PDPOSGSC-G11L21` and `PDPOSGSC-G21` remain skipped. These records do not embed the raw series and do not make the ignored raw paths public.

## Handling recommendation for v4

1. Preserve the exact existing NYFed CSV plus adjacent README/provenance; cite the source terms in Data Availability and retain the accepted vintage distinction.
2. Publish code, frozen aggregate results, source fingerprints and acquisition directions. Keep raw FX and per-origin source/forecast containers out of the new branch and submission ZIP.
3. Add no new panel raw data in v4: none is needed for manuscript restructuring, and the existing source fingerprints/aggregate results suffice for the requested package.
4. Re-run an index/new-artifact inventory after staging; this snapshot precedes the final v4 additions. Inspect ZIP members as well as Git paths. Avoid blanket add commands that could include task scratch or backups.
5. Do not remove or rewrite protected archives to tidy a policy field. Their historical scope is explicit; any future source-delivery change needs a separate dated note.

Only this new audit note was written in this follow-up; no source bytes, tracked results, permissions, or repository index were altered by the audit.
