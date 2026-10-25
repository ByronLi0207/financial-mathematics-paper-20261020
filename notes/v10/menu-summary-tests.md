# E1 pure summary: artificial RED to GREEN evidence

本轮只实现 `v10_menu_summary.py`、`test_v10_menu_summary.py` 和本说明。冻结依据为 `protocol/v10/menu-isolation-design.md`，由 root 先单独提交为 `3c5f167632a1a21ded29731a773a85ab307d3a96`。未读取真实实验 comparison/point outputs 来产生任何新汇总，未改旧 archive、原 forecast/solver、NPZ 适配器或协议，未运行 E3/E4，也未提交。Claude/Cloud 与跨模型复审未启动。

## Interface and completeness

`summarize(records, repetitions, source_ids, design)` is an in-memory function returning `cells`, `across_sources`, and `predictions`. It opens no source/archive/output files and imports only standard-library modules.

- All planned source/arm/window/method cells are emitted in supplied source order. Rep IDs are exactly `0..R-1`.
- Missing, duplicate, unexpected, invalid, failed or non-72-point repetitions fail the whole owning cell. Invalid/nonpositive F or missing/invalid selected penalty also prevents a complete cell. No partial-repetition median is supplied.
- Old-menu values come only from the original operands attached to the same source/arm/window/method/rep row. Old completeness is recorded separately. Missing old operands do not erase an otherwise complete new summary, but make M3 unavailable where required.
- Across-source summaries use all declared within-source medians with equal source weight. A missing required source yields `UNASSESSABLE`; no successful-source-only median/IQR is emitted.
- Infinity selections are counted using the literal JSON-safe `"inf"`. Cells expose `q25/q75` and compatible `q25_pct/q75_pct` fields. Breach medians are rates over the fixed72 evaluation points.
- M1 uses the closed registered interval; M2 uses the inclusive switching-minus-constant threshold; M3 requires both strictly improved across-source arm medians and the registered number of sources whose within-source medians improve in BOTH arms. The source count is the intersection. Any necessary missing old/new operand remains `UNASSESSABLE`, even when a known subset alone would meet the count.
- Outputs normalize arithmetic/count results to native Python scalars. Artificial native-scalar and actual NumPy-scalar tests verify `json.dumps(..., allow_nan=False)`.

## Frozen arithmetic

The production ratio remains exactly `100. * (float(QR) / float(F) - 1.)`, matching the frozen v9 formula. There is no subtraction-before-division rearrangement and no epsilon, clipping or threshold tolerance.

The artificial `QR=105,F=100` case deliberately produces `5.000000000000004`; M1 is therefore `NOT_SUPPORTED` for that IEEE operand. Closed theoretical endpoints `-5` and `+5` are tested by directly supplying artificial across-source operands to the real predicate. This distinguishes a closed predicate from changing the registered ratio arithmetic to force a theoretical boundary result.

Median uses `statistics.median`. Quartiles retain the existing v9 report interpolation and arithmetic: position `(n-1)*p`, followed by `a+(b-a)*fraction`.

## Observed RED to GREEN sequence

1. Tests were written before the summary module existed. `python3 -B -m unittest test_v10_menu_summary -q` reported16 test methods and29 failures/subtest failures, all from the explicit missing-implementation assertion.
2. The first minimal implementation passed16 artificial tests. Root then required preserving the literal frozen ratio arithmetic. A new literal IEEE regression test first failed as expected (`5.0 != 5.000000000000004`), and passed after restoring `100*(QR/F-1)`.
3. A literal inherited-quartile regression first failed as expected (`-2.4999999999999996 != -2.5`), and passed after restoring `a+(b-a)*fraction`.
4. Final local stdlib-only run of this test file reported18 tests, `OK (skipped=1)`. The sole skip was the actual NumPy-scalar test because system Python lacks NumPy; all other artificial tests passed.
5. Root then ran the three new E1 test files together in the pinned offline temporary environment. The saved receipt `.scratch/v10/e1-focused-test-1.json` reports exit0 and **72 passed, 16 subtests passed in0.53s**, with no test skip. This includes the actual NumPy-scalar test. The invocation selected only `test_v10_menu.py`, `test_v10_menu_driver.py`, and `test_v10_menu_summary.py`; it was not a post-change full repository suite. Root owns the later unified full-suite gate.

The focused receipt uses the pinned runtime/environment recorded in `notes/v10/baseline-tests.json`: `arch==8.0.0`, `numpy==2.3.5`, `scikit-learn==1.9.1`, `pytest==9.1.1`, `matplotlib==3.11.2`, plus the recorded PDF/image packages, with offline/no-project/no-env-file execution. Its stderr contains only the uv informational warning that `--no-project` was supplied while no project was found.

## Artificial cases covered

The18 test methods exercise hand-calculated median/IQR and infinity counts; source-median weighting instead of pooled repetitions; missing/duplicate/extra rep rejection; missing entire source inventory; failed/invalid counts/losses/selections; complete matched old subsets; invalid or missing old operands; M1 closed endpoints and negative changes outside its interval; frozen IEEE ratio arithmetic; M2 inclusive5-point threshold; strict two-arm M3 group improvement; M3 intersection rather than union; unknown M3 operands despite a sufficient known subset; source ordering and input immutability; native JSON values and actual NumPy scalars; and rejection of out-of-plan source identities.

These checks establish summary-contract behavior on invented scalar fixtures. They provide no new E1 scientific result and no E3/MCS or E4/cost result.
