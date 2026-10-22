# Separate AR floor and horizon diagnostics

22 October 2026. These explicitly post-result descriptive checks complete the diagnostic coverage of the later eight-cell AR addition. They change no forecast, model, selected parameter or original primary. The original sixty-nine-file conditional archive and its ninety-floor/forty-five-horizon tables remain unchanged.

The [plan](../../../protocol/revision-20261022/ar1-diagnostics-plan.json), [design](../../../notes/revision-20261022/ar1-diagnostic-design-agent.md) and [46-file executable freeze](../../../protocol/revision-20261022/ar1-diagnostics-executable-freeze.json) were publicly verified at commit `8c88f0832585599331f9dcc3abb6f8cf28623d52`, 13:30:21 UTC, before the new counts were computed at 13:30:40 UTC. The samples and earlier AR scores had already been inspected. This ordering does not make these diagnostics confirmatory or restore an unseen holdout.

All eight floor rows and four paired-horizon rows are retained. Pairing requires identical full origins, source, history, issue floor and refit indices; realized peaks must satisfy `P6<=P24`. No intersection, truncated segment, forecast sorting or reconciliation is used.

| Source | W | Short report exceeds long | Origins | Crossing % | Maximum positive gap in native units | Mean positive gap over all origins |
|---|---:|---:|---:|---:|---:|---:|
| FX | 720 | 0 | 6,625 | 0 | 0 USD | 0 USD |
| FX | 2,880 | 0 | 6,625 | 0 | 0 USD | 0 USD |
| Treasury | 52 | 59 | 277 | 21.299639 | 11,784.473495 USD millions | 655.684048 USD millions |
| Treasury | 260 | 26 | 277 | 9.386282 | 5,347.869636 USD millions | 139.737500 USD millions |

The short-history Treasury AR report equals its issue floor on seven H6 issues, with five strict breaches, and seven H24 issues, with seven breaches. The four FX cells and two long-history Treasury cells never bind the floor. Empty binding-group rates are undefined, with explicit reasons in the CSV; they are not zero breach-rate estimates. `P==B` describes a realized zero-headroom atom and differs from `C==B`.

Every realized paired target is ordered. Separately estimated horizon models and mature scenario sets need not yield ordered reports. Zero observed FX crossings do not establish general coherence, and the Treasury crossings do not isolate a cause of model error. These counts reinforce the score-versus-tail limitations of favorable AR cells without selecting a replacement forecast or claiming coverage.

The [production audit](ar1-diagnostics-audit.json) binds the accepted AR manifest, all eight receipt/trace identities, source fingerprints and exported bytes. The separate [scalar readback](independent-readback.json) independently checks all 236 fields and complete vectors without importing the diagnostic kernels; its `math.fsum` means equal the CSV values. Neither check repeats the source-label, OLS or recursive-report oracles from the earlier AR readback.

Actual production measurements were 0.345336 seconds internally, peak RSS 55,115,776 bytes and one observed OS thread across eleven snapshots. The external process measure was 0.42 seconds, RSS 55,164,928 bytes and no swaps. The independent scalar check took 0.055801 seconds with RSS 39,436,288 bytes; its OS thread count was not separately measured. These are computation observations, not active research hours or an operating-system memory sandbox.

The exact retained-attempt audit command is:

```text
python3 -B build_ar1_diagnostics.py \
  --replication-dir .scratch/revision-20261022/replication-root-check-20261022-01 \
  --ar1-attempt-id financial-20261022-01 \
  --readback results/revision-20261022/ar1-replay/inventory-readback.json \
  --diagnostic-id NEW_UNIQUE_ID \
  --freeze 505024752bb38194132ce7d06db0ee781f19846cd622037bc8ca8de5c0e8e9dd
```

This exact audit requires the retained private AR attempt; its per-origin vectors are not redistributed. A fresh AR replay produces new receipt/manifest identities even if numerical reports agree, so it cannot silently reuse this old manifest-bound plan. A newly bound plan/readback and separately versioned execution are required for that case. The public source retrieval and full financial replay commands remain in the main guide and [AR supplement](../ar1-replay/README.md). The current diagnostic command is not claimed to be a one-command fresh-checkout reproduction of private artifacts.
