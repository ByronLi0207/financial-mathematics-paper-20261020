# WP3: frozen level-AR/GARCH mechanism study

**Scientific conclusion: MISMATCH.**
The predeclared restriction to short-horizon, long-history, strongly clustered
conditions is contradicted by clear gains outside that region. The historical
empirical pattern cannot be presented as a universal mechanism boundary.
The support rule was not changed after seeing this result.

| Procedure | Clear gains inside target | Clear gains outside target | Frozen classification |
|---|---:|---:|---|
| 33-feature quantile regression | 2 / 12 | 6 / 60 | **MISMATCH** |
| Four-feature quantile regression | 2 / 12 | 6 / 60 | **MISMATCH** |

A clear gain requires all planned paired repetitions, a relative mean-loss
change plus twice its Monte Carlo standard error below zero, and a strict-win
fraction at least the frozen threshold. These are descriptive screens, without
a family-wide significance guarantee. Outside gains include homoskedastic
processes and the longer horizon. Small-history regression losses and excess
breaches remain visible in the full grids. The two regression procedures retain
their different original penalty menus and validation-failure rules; their
comparison is not a pure feature-count intervention.

## Provenance and measured execution

- Design commit: `039f6f1b49d46610697bed5300cab687b37951df`; protocol bytes are checked
  against that commit before any study draw.
- Study: `2026-10-24T08:59:35.025727Z` to `2026-10-24T09:33:54.670745Z`;
  elapsed 2059.646685 seconds.
- Worker tasks: 288 / 288.
- Complete method tasks: 6912.
- Candidate statuses: `{"COMPLETE": 18431, "FAILED": 1}`.
  Candidate failures are retained in `readout-bindings.json` and the full archive.
  A failed eligible-menu candidate does not imply the original QR4 procedure
  failed; no selected evaluation was replaced by another penalty.
- Actual observed peak worker RSS: 63258624 bytes;
  maximum observed OS threads: 1.
- Independent scalar/provenance audit: `PASS`,
  0 differences. This is arithmetic verification,
  not independent study replication.

## Complete delivery

`summary.csv` / `summary.json` retain every cell and full-precision metric;
`COMPLETE_RESULTS.md` is the complete readable grid. `support.json` records
every target and outside counterexample. `figures/` holds all six saved-summary
heatmaps with Monte Carlo uncertainty, using fixed shading limits and uncapped
numeric annotations. The QR33 loss figure is designated for the main paper;
the other grids and results remain available for the Supplement.

`wp3-driver-output.tar.gz` preserves the original driver manifest, inventory,
status logs, termination, summaries, support screen and every public per-unit
receipt. `wp3-driver-output-members.csv` enumerates every archived byte count
and SHA-256; `wp3-package-receipt.json` records the full archive readback.
The loose unit directory and large inventory remain locally intact and are
excluded from Git only to avoid publishing tens of thousands of tiny files and
an oversized loose JSON. Nothing is dropped from the complete archive.

The archive excludes `.scratch` traces and raw FX observations. For independent
readback, extract its contents into a separate empty directory and point
`notes/revision-v8/audit_wp3.py --formal` there. Re-executing the study requires
a fresh output location and the frozen design commit; version-specific public
reproduction instructions are finalized with the release.
