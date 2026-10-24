# R6 writing-stage paired HAC readback

Post-result descriptive, nonconfirmatory paired unconditional HAC comparisons of two fixed references for the same retrospective conditional QR report. The original-three-menu validation selected lambda 0.01, also selected by R0 in this group. These are QR-versus-F comparisons, not R2 results. The R6 rules followed earlier inspected results; the bounded repository audit found no prior evaluation role for these earlier origins, but the raw history was familiar. These p-values are a later writing-stage readback and do not account for the whole selection and inspection process or supply confirmatory error control, prospective validation, or external replication.

Exactly two comparisons use the same saved QR W2880/d24, lambda 0.01 report on retrospective FX H6 origins 8999–10438 (n=1440). The references are matched frozen F/W2880/d24 and original-primary rolling F/W720/d1. The first comparison has a different reference from the original-primary comparison.

The manuscript Section 5 definition and unchanged inference_tests.dm_test supply Bartlett Newey–West covariance (denominator n) and a two-sided normal reference. L=max(H,floor(4*(n/100)^(2/9)))=7. Negative differences favour QR. No HLN, alternative bandwidth, adjustment family, or additional comparison is reported. If the helper reports nonpositive LRV, the statistic and p-value remain undefined.

The helper is reused unchanged. It also returns its legacy HLN fields internally; this readback discards those fields and reports only the two requested normal HAC p-values.

| Fixed comparison | QR − F mean loss | Change vs F | HAC statistic | Normal two-sided p |
|---|---:|---:|---:|---:|
| matched_frozen_F2880_d24 | -57134.7288313 | -16.6235653368% | -4.17827197816 | 2.93732277961e-05 |
| original_primary_rolling_F720_d1 | 8800.0645258 | +3.16819852932% | 0.562782095873 | 0.573583273454 |

results.json binds the private-archive manifest, retro seal, prior PASS verification, unchanged inference helper, exact three NPZ hashes and selection/primary identities. Per-origin arrays and source data remain private; no existing R6 file is changed.

Command: `PYTHONDONTWRITEBYTECODE=1 /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B supervisor_r6_hac_readback.py --execute`
