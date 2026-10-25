# E2 CFTC pure summary: artificial RED to GREEN

依据 root 已单文件提交的 `protocol/v10/cftc-design.md`（`acd567c`），本轮实现 `v10_cftc_summary.py`、`test_v10_cftc_summary.py` 与本说明。输入均为人工构造的 scalar records；没有读取真实 CFTC observations/结果、筛选合约、运行 study、重拟合、预测或新增检验。未提交。后续报告脚本可单独准备但不运行。

## API and inventory

`summarize(records, contract_codes, design)` returns:

- `cells`: exactly one slot per selected literal `code` × both windows × all six methods. Missing/duplicate/non-COMPLETE/incomplete records produce `FAILED`, with no partial mean, breach count or breach rate. The saved failure reason and record count remain visible.
- `contracts`: one row per selected code in supplied order. `windows[str(W)].methods[method]` contains all six method slots at each window; complete/required/failed method inventories remain explicit.
- `across_contracts`: one row per window/method, with the median and descriptive IQR of within-contract relative losses against that contract's own F. Any required method/F missing, or nonpositive F, makes the whole comparison `UNASSESSABLE`; no successful-contract subset median is produced. Raw contract-count losses are never aggregated across markets.
- `predictions`: registered T1/T2/T3, each independently `SUPPORTED`, `NOT_SUPPORTED` or `UNASSESSABLE`. A zero-contract selected universe produces `UNAVAILABLE` without fabricated contracts.

Complete scalar method receipts require n=260, finite nonnegative mean loss and valid strict-breach count. QR4/QR33 selections must belong to the frozen six-point menu; ACI methods require a frozen gamma. Literal code strings preserve leading zeros and plus signs. Unknown inventory identities and duplicate selected codes are rejected rather than silently removed.

T1 retains the full2K denominator and requires every F/I/QR33 operand. Its strict `min(F,I)<QR33` comparison can use a complete F with zero mean; T2/T3 relative ratios cannot. T2 requires both complete all-K QR33/F medians inside the closed registered interval. T3 requires the complete all-K QR4/F median atW260 to be strictly lower than atW52. Missing required operands remain unknown even when a known subset already meets a numerical threshold. Ancillary failures do not erase complete primary operands.

## Arithmetic and boundary checks

Relative change is exactly `100. * (float(loss)/float(F)-1.)`, preserving the frozen arithmetic. No subtraction-before-division replacement, epsilon, clipping or rounding is used for decisions. The artificial110/100 case is exactly `10.000000000000009` under this arithmetic and therefore fails the positive closed10 threshold. The theoretical closed endpoints are separately tested by supplying artificial across-contract operands to the real predicate.

Medians use `statistics.median`; quartiles use the inherited `(n-1)*p` linear interpolation with `a+(b-a)*fraction`. Generated output values are native Python scalars and serialize with `allow_nan=False`.

## Observed test evidence

RED was observed before implementation using:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest test_v10_cftc_summary -q
Ran17 tests
FAILED (failures=21, skipped=1)
```

All failures/subtest failures were the explicit missing-summary-implementation assertion; the skip was the NumPy-only test in the system stdlib runtime.

After the minimal implementation, the same artificial file passed locally (`OK`, one NumPy skip). The pinned offline environment then ran only this test file, including the real NumPy-scalar case:

```text
uv run --offline --no-project --no-env-file
  --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
  --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1
  --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow
  python -B -m pytest -q -p no:cacheprovider test_v10_cftc_summary.py

17 passed, 6 subtests passed in0.12s
exit0; no skip
```

The only stderr line was uv's informational `--no-project` warning. No post-change whole-repository suite was run by this subtask; root retains that unified gate.

The17 methods cover full12K inventory; one row per contract; literal code ordering; exact60% T1 support; strict ties and either-reference wins; required-operand missingness; per-contract normalization before across-contract medians; closed T2 operands; frozen IEEE arithmetic; strict/missing T3; zero-F semantics; duplicate and invalid method slots; ACI gamma failure; absent entire contract; empty selected universe; immutable input; JSON-native outputs; and actual NumPy scalars. These are artificial behavior checks and establish no CFTC empirical result.
