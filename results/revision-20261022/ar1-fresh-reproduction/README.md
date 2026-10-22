# New-attempt AR and diagnostic reproduction

22 October 2026. This is a genuine new execution of the unchanged eight-cell exploratory AR contract and its diagnostics, using the already audited conditional-replication directory and the same hash-matching financial inputs. It is a computation reproduction, not a new financial sample, an unseen holdout, a new selection or another independent dealer. The original conditional archive and original AR/diagnostic attempts are preserved.

The [separate 54-file adapter freeze](../../../protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json) has SHA-256 `5396b96307c49a8f578244c8fdc50ba813eae3ce54f8b0d66aefa83fc7a8b633`. Its code, design, retained reference identities and implementation note were publicly byte-verified at commit `9e34cc9d771802fee8568e8c34a305fa289d6532`, 14:03:16 UTC, before the new AR execution began at 14:03:39 UTC. This adapter fixes a reproduction limitation: the earlier diagnostic command deliberately accepts only its original manifest and readback. New execution timestamps change those identities even when the numerical forecasts agree.

The adapter requires a genuinely generated version-2 AR readback and checks its actual hash, manifest, frozen model/selection contracts and complete retained vectors. It does not generate or copy an upstream PASS, replace the old plan in memory, refit a model, read raw observations, sort forecasts or change the diagnostic definitions. It records a new input binding and compares every table cell with the frozen reference, preserving any disagreement. Verification and numerical agreement are separate statuses.

## Observed reproduction

All eight new AR cells completed, with no failed cell. All six AR CSVs are byte-identical to the original AR archive: 192 aggregate rows across summary, annual, fixed sparse and paired tables. The new manifest and eight cell receipts have genuine new identities and resources. The [new inventory readback](inventory-readback.json) checks all 192 aggregate rows and 1,196 fit metadata records, with the same explicitly limited 24 exact represented-input Fraction OLS and 24 scalar-recursion report oracles. It does not independently recompute every fit or forecast.

The [new diagnostic audit](ar1-diagnostics-reproduction-audit.json) and [complete comparison](ar1-diagnostics-comparison.json) retain all eight floor and four paired-horizon rows. Both diagnostic CSVs are byte-identical, with exact scalar agreement and no suppressed difference. The adverse Treasury crossings remain 59/277 and 26/277; all seven short-history H24 floor-binding reports still breach. Reproducing these counts does not establish coverage, model adequacy or a financial benefit.

A [distinct scalar readback](diagnostic-independent-readback-threadrefined.json) independently checks all236 public fields,27,608 single-cell vector rows and13,804 paired origins without importing the builder, adapter or diagnostic statistical kernels. NumPy only decodes typed NPZ arrays; Python scalar comparisons and `math.fsum` reconstruct the counts/rates/means. All complete origins, floors and refit alignments pass; the independently summed means differ by zero. This check took0.105083seconds and42,401,792bytes peak RSS, with14 valid identity-checked OS-thread snapshots and maximum1. It does not repeat the upstream source/OLS/replay oracles. The [earlier readback](diagnostic-independent-readback.json) remains unchanged: its numerical checks passed but its14 thread probes had a format error and supplied no accepted OS-thread observations. The refined receipt preserves that history and the initial checking-script column-name error, which stopped before writing a PASS. No result was changed to resolve either checking-script problem.

| Process | Internal checkpoint seconds | Internal peak RSS bytes | External elapsed seconds | External peak RSS bytes | Maximum observed OS threads |
|---|---:|---:|---:|---:|---:|
| New eight-cell AR execution | 8.788284 | 102,596,608 | 8.85 | 102,629,376 | 1 |
| Genuine new version-2 readback | 1.243548 | 93,306,880 | 1.30 | 93,306,880 | 1 |
| New-attempt diagnostic adapter | 0.487801 | 52,674,560 | 0.56 | 54,804,480 | 1 |

The probes recorded 1,465, 106 and 10 OS-thread snapshots respectively; all three external process measures recorded zero swaps. Numerical libraries requested one thread. These measurements describe the recorded processes, not a memory sandbox or active research hours. No software installation, new download, parameter search or repeat of the original 56 conditional phases was needed for these steps.

## Reproduce from a successful local conditional attempt

First obtain the two exact private input versions and run the original conditional reproduction as described in the [root guide](../../../README.md). The [AR guide](../ar1-replay/README.md) gives the model contract. In the documented macOS/NumPy environment, substitute a successful `REPLAY_ID`, a new `AR_ID`, a new readback filename and a new diagnostic ID:

```text
python3 -B run_ar1_replay.py \
  --replication-dir .scratch/revision-20261022/replication-REPLAY_ID \
  --attempt-id AR_ID

python3 -B verify_ar1_output.py \
  --replication-dir .scratch/revision-20261022/replication-REPLAY_ID \
  --attempt-id AR_ID \
  --output state/revision-20261022/my-new-ar-readback.json

shasum -a 256 state/revision-20261022/my-new-ar-readback.json

python3 -B reproduce_ar1_diagnostics.py \
  --replication-dir .scratch/revision-20261022/replication-REPLAY_ID \
  --ar1-attempt-id AR_ID \
  --readback state/revision-20261022/my-new-ar-readback.json \
  --readback-sha256 HASH_FROM_THE_NEW_READBACK \
  --diagnostic-id NEW_DIAGNOSTIC_ID \
  --freeze 5396b96307c49a8f578244c8fdc50ba813eae3ce54f8b0d66aefa83fc7a8b633
```

The receipt hash must be computed from that genuinely new successful readback, not copied from this archive. The final output is a new sibling `ar1-diagnostics-reproduction-NEW_DIAGNOSTIC_ID`, with separate public tables/comparison/audit and a private input binding. Existing attempt IDs and output files are refused. The original manifest-bound diagnostic command remains available for its exact retained attempt; this adapter supplies the separate fresh-attempt route.

Only public aggregate exports and audit metadata are retained here. Raw observations, per-origin vectors and per-refit coefficients remain private. The new manifest binds those private artifacts by hash without redistributing them. The duplicated public CSVs make the new manifest's public file inventory inspectable; they do not count as additional experimental evidence.
