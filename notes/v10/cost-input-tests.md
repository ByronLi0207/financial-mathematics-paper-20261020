# E4 frozen input adapter: artificial RED to GREEN

依据 root 已独立提交的 `protocol/v10/cost-design.md`（`a112e45`），本轮仅新增 `v10_cost_inputs.py`、`test_v10_cost_inputs.py` 和本说明，未提交。没有读取真实数组、计算 reserve/headroom 均值、破线/超额、成本或区域，也没有改 E3/E2 冻结代码。前一轮规划建议已由 root 纳入正式设计，本轮不另写其他规划文件。

## Interface

`load_cost_group(group, inventory, root)` accepts one public E3 group descriptor, the frozen E0 inventory JSON object, and the NEW v10 root. It returns exactly:

```text
origins: read-only integer array
target: read-only finite array
floor: read-only finite nonnegative common current-floor array
capacities: {full_method_id: read-only finite capacity array}
recovery_receipts: list of native JSON metadata records
```

Any invalid or incomplete input raises `CostInputError` for the whole comparison. There is no smaller grid, deleted method, fallback F, clipping, source reconstruction or retry. This adapter does not calculate the normalization scale; that belongs to the separately frozen cost core.

## Identity and floor guarantees

1. Require a READY E3 group and a regular file beneath the NEW root. Verify group bytes/SHA before parsing, exact array-name inventory, each shape/dtype/payload SHA pin and finite numeric data, then verify the file remained unchanged during reading.
2. Require the complete declared contiguous origin range, target shape and both method-matrix shapes. The existing loss matrix is only verified, never recalculated. Method IDs must be unique and bound to their exact recorded column indices.
3. Require exactly one literal canonical `F`, explicitly `matched_historical`, with a provided floor key. There is no qualified/rolling reference fallback. All provided floors must exactly equal that canonical F floor over the entire grid. Require all capacities and targets to be at least that floor.
4. Only `QR4::QR4` and `Levy::Levy_L` may recover a missing floor, and only when the authoritative E0 method row matches period/normalized_source/H/W plus full method ID, declares `floor_key=None`, and carries its registered `floor_recovery`. The method's original-trace provenance must match that E0 row.
5. Resolve `floor_recovery.trace_path` by exact original-path match in `minimum_core_private_copy_manifest`; use only that entry's NEW `proposed_scratch_relative` copy and pinned bytes/SHA. Old absolute paths remain identity strings and are never opened.
6. The frozen reference key prefix (for example `frozen_F_floor`) identifies its `frozen_F_origins` and `frozen_F_peak`. Require the entire origins and target arrays to equal the E3 group's arrays, and the saved source floor to equal canonical F's provided floor exactly. No raw position series or estimate is constructed.
7. Record method/reference IDs, comparison identity, candidate/source original paths, copied-source path/pin, source keys, canonical F floor key/payload SHA and explicit full-array equality results. Existing E3 NPZs/index are never changed. Returned arrays are copied and marked read-only.

The copy location is the E0 proposed destination already used by the minimal private-copy manifest; no additional directory search, alias inference or alternative file is selected.

## Artificial test evidence

The22 parameterized tests were written before implementation. The pinned offline run first observed22 failures, all from the explicit missing-adapter assertion. After the minimal implementation, the same command returned:

```text
22 passed in0.12s
exit0; no skip
```

Invocation selected only the new test file:

```text
uv run --offline --no-project --no-env-file
  --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
  --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1
  --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow
  python -B -m pytest -q -p no:cacheprovider test_v10_cost_inputs.py
```

The only stderr was uv's informational `--no-project` warning. Root retains the combined/full-suite check; this subtask did not run it.

All NPZs were manufactured under pytest temporary directories. The tests cover both allowlisted recoveries; complete provided floors with no recovery-file access; file/payload pins and array-name changes; noncontiguous origins; target/matrix/column mismatches; missing canonical F; missing F floor; unequal provided floors; C or Y below B; unknown missing floors; wrong E0 source identity; absent recovery declaration; bad copied-source fingerprint; entire copied origins/target/floor differences; path escape rejection; input immutability; and read-only returned arrays. These are structural artificial checks, not financial computations or empirical cost results.
