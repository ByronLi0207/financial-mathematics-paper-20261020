# Verified fixed-design analysis

These aggregates belong to study `sampled-inventory-peaks-v1`, attempt `20261021T060715Z-de1704c9`. The frozen seven-cell specification and all five methods were retained. `run-manifest.json` records COMPLETE for the scientific run and PASS for all thirteen required checks; it does not certify manuscript completion or external validation.

| File | Data rows excluding header | Meaning |
| --- | ---: | --- |
| summary.csv | 35 | Seven cells, five methods, score and capacity/risk metrics |
| paired-comparison.csv | 7 | Within-cell F-minus-S means and computed equality mechanisms |
| stability.csv | 4 | All fixed geometric-block lengths, 999 replicate identities each |
| diagnostics.csv | 1647 | All primary predetermined groups, including null/status rows |

Monetary values in CSV are source-reported USD; paper figures use USD millions (factor 1e-6). Empty CSV values denote the recorded undefined reason, not numerical zero. All cells share 6,625 original issue indices, 11927 through 18551 inclusive. The common-origin SHA-256 is defined in the root README.

The primary paired mean is USD-9,374.860250076379, or -2.0779969% of S loss. F has more strict breaches and greater unconditional/conditional overrun than S. The H=24 and tau=0.90 sensitivities reverse the primary mean-loss direction. All four descriptive resampling ranges cross zero; none is a population confidence interval or a superiority probability.

The three original aggregate vector figures are at `manuscript/working-paper/figures/`, with their canonical paths, byte sizes and SHA-256 identities in the manifest. The four tables and three figures were byte-identical in two complete executions. Raw observations, per-origin forecasts, private development thresholds and complete replicate vectors are excluded.

The final pre-manifest resource checkpoint measured 8.02144754 seconds, peak process RSS 80,936,960 bytes, and a maximum of one observed OS thread across 565 snapshots. The thread count is a snapshot maximum, not continuous monitoring. Both source reuse and historical download access are explicitly distinguished.

Scientific code and tests were published in commit `50b63dac9bb7f2dafaffc1ded7ccf3264672e2b2`; their full content hashes are recorded in the manifest. The root README describes reproduction, data identity, access conditions, resource limits and interpretation.
