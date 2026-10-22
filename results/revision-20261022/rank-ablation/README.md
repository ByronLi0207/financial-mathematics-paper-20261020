# Post-inspection ordinary empirical headroom rank ablation

This eight-cell supplement tests a specific finite-sample comparator issue. It does not replace either original primary, retune QR, add independent financial observations or introduce a new estimator. The [design](../../../protocol/revision-20261022/rank-ablation-design.md), [specification](../../../protocol/revision-20261022/rank-ablation-spec.json) and [16-file executable freeze](../../../protocol/revision-20261022/rank-ablation-executable-freeze.json) were public at [a36c658](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/commit/a36c65873f9c530673c038bf297e2a1d2a14fdd5), and all 17 public file bytes were verified before the additional financial execution. Both source archives and earlier outcomes had already been inspected.

The added intercept-only report I uses the lower ordinary empirical .95 headroom quantile, rank ceil(19W/20). It has the same completed-label pool, update schedule and actual issue floor as reconstructed frozen F, whose rank is ceil(19(W+1)/20). At W720, W2880 and W260 these are endpoints of the same empirical pinball minimizer interval. At W52 they are ranks50/51, and the latter need not minimize the ordinary empirical objective. Both reports retain duplicates and rank headrooms before adding the current floor.

| Source | H | W | I/F ranks | QR-minus-I loss % | I-minus-F loss % | QR / I / F breaches |
|---|---:|---:|---:|---:|---:|---:|
| FX | 6 | 720 | 684 / 685 | −1.967174 | −0.152554 | 531 / 337 / 332 |
| FX | 6 | 2880 | 2736 / 2737 | −14.773188 | +0.007540 | 376 / 365 / 360 |
| FX | 24 | 720 | 684 / 685 | +31.507777 | −0.002900 | 924 / 432 / 427 |
| FX | 24 | 2880 | 2736 / 2737 | −3.783192 | +0.026422 | 531 / 359 / 357 |
| Treasury | 6 | 52 | 50 / 51 | +87.086106 | −1.994602 | 84 / 14 / 11 |
| Treasury | 6 | 260 | 247 / 248 | +46.057709 | +3.237079 | 54 / 32 / 28 |
| Treasury | 24 | 52 | 50 / 51 | +208.257864 | +6.213227 | 132 / 37 / 33 |
| Treasury | 24 | 260 | 247 / 248 | +105.019569 | +2.352874 | 84 / 15 / 12 |

Negative changes favor the left report, relative to the right mean loss. Every FX cell has6,625 origins and every Treasury cell277. H counts source records; native monetary amounts and source-specific horizons are not pooled. Original QR means and breach counts are imported unchanged from the accepted archive. QR-minus-I is a difference of stored/new unrounded means, not an independently recomputed originwise QR contrast. Direct I-minus-F paired differences are separately retained in the complete CSV.

The two headline signs persist under this particular control: matched long-history H6 QR improves on I in FX and loses in Treasury. All four Treasury QR cells remain adverse. I itself has higher evaluation loss than F in five of eight cells, including +6.213% at Treasury H24 W52. Its capacity is strictly lower at every retained issue; breaches and mean positive overrun rise in all eight cells, while unused allowance falls. Lower empirical rank is not a universal improvement or a safety guarantee. These findings do not rule out all rank-related confounding or identify a causal feature effect.

## Complete outputs and independent arithmetic

The [pre-execution public-byte receipt](pre-execution-public-verification.json) records the actual17file comparisons and time before the added calculation.

- [summary.csv](summary.csv): all16 I/F summaries, including loss, capacity, extra allowance, breaches, overrun and unused allowance.
- [annual.csv](annual.csv): all64 issue-year summaries, with partial years preserved.
- [nonoverlap.csv](nonoverlap.csv): all16 globally anchored H+1 grid summaries; disjoint windows do not imply independent observations.
- [contrasts.csv](contrasts.csv): all24 QR-minus-I, I-minus-F and unchanged-QR-minus-F scalar contrasts.
- [audit.json](audit.json): all eight cell identities, exact reconstructed-F agreement with every original summary metric, original QR rows, output/private-vector fingerprints and measured process observations.
- [independent-readback.json](independent-readback.json): independent scalar-window/Python-sorting reconstruction of all55,216 I/F issued reports over27,608 cell-issues, all targets/scores/aggregates and361,487 exact checks with zero mismatches.
- [external-resources.json](external-resources.json): actual external process timing/RSS, separate from internal checkpoints and research hours.

The production calculation took0.29 seconds externally, peak RSS49,856,512 bytes; the scalar verifier took1.61 seconds, peak RSS59,293,696 bytes. Both observed one OS thread at recorded snapshots. This is not a hard continuous thread/memory sandbox. The verifier does not import the production predictor or scorer, but shares the strict input parser and the same accepted financial bytes. It verifies arithmetic, not unseen dealer validation, live original-release timing, statistical coverage or financial decision value.

## Reproduction

Use the existing compatible Python/NumPy environment, exact original source paths/hashes and original source acquisition/rights instructions in the [root guide](../../../README.md). Both fixed inputs are required; the official Treasury snapshot is public under its existing terms, while FX redistribution permission remains unverified.

```bash
python3 -B run_rank_ablation.py --output .scratch/rank-ablation-NEW_UNIQUE_ID
python3 -B verify_rank_ablation.py --attempt .scratch/rank-ablation-NEW_UNIQUE_ID
```

The destination must be new. The runner verifies the complete bound implementation/design/aggregate inventory before source loading and after calculations. Failure retains a failed receipt without a shortened complete mean, fallback or changed specification. The readback receipt also cannot overwrite an earlier one. New process timestamps/resources can differ; numerical disagreement is retained explicitly. Private per-origin vectors stay in the local attempt and are not redistributed. The original accepted QR/F/S/K, AR and coverage result files remain unchanged.
