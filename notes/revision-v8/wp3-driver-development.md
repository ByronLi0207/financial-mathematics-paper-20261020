# WP3 driver development evidence

No study DGP or model fit was run during driver development. Root is responsible for the complete test suite and the single formal run.

## RED before implementation

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 1

```text
FFFFFFFFFFFF                                                             [100%]
=================================== FAILURES ===================================
_____________ test_parent_import_does_not_load_numerical_libraries _____________
test_v8_wp3_driver.py:24: in test_parent_import_does_not_load_numerical_libraries
    assert result.returncode == 0, result.stderr
E   AssertionError: Traceback (most recent call last):
E       File "<string>", line 1, in <module>
E         import run_v8_wp3,sys; assert not any(n in sys.modules for n in ('numpy','scipy','v8_mechanism_mc','conditional_study'))
E         ^^^^^^^^^^^^^^^^^^^^^
E     ModuleNotFoundError: No module named 'run_v8_wp3'
E     
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['/Users/bingyouli/.cache/uv/builds-v0/.tmpJ0zYi3/bin/python', '-c', "import run_v8_wp3,sys; ass...hanism_mc\',\'conditional_study\'))\n    ^^^^^^^^^^^^^^^^^^^^^\nModuleNotFoundError: No module named \'run_v8_wp3\'\n').returncode
________ test_planned_order_keeps_every_rep_phi_p_and_all_method_slots _________
test_v8_wp3_driver.py:28: in test_planned_order_keeps_every_rep_phi_p_and_all_method_slots
    d = driver(); units = list(d.planned_units(design()))
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
____ test_exclusive_outputs_reject_duplicate_and_symlink_without_overwrite _____
test_v8_wp3_driver.py:40: in test_exclusive_outputs_reject_duplicate_and_symlink_without_overwrite
    d = driver(); path = tmp_path/'record.json'
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
______ test_existing_formal_directory_is_refused_before_private_creation _______
test_v8_wp3_driver.py:52: in test_existing_formal_directory_is_refused_before_private_creation
    d = driver(); formal = tmp_path/'formal'; formal.mkdir()
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
_______ test_sealed_hash_mismatch_is_detected_before_any_numerical_work ________
test_v8_wp3_driver.py:60: in test_sealed_hash_mismatch_is_detected_before_any_numerical_work
    d = driver(); (tmp_path/'module.py').write_text('original\n')
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
__ test_checkpoint_checks_absolute_global_deadline_even_when_ps_is_throttled ___
test_v8_wp3_driver.py:69: in test_checkpoint_checks_absolute_global_deadline_even_when_ps_is_throttled
    d = driver(); clock = [10.0]; stages = []
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
_____ test_checkpoint_forces_each_cell_end_and_final_resource_measurement ______
test_v8_wp3_driver.py:87: in test_checkpoint_forces_each_cell_end_and_final_resource_measurement
    d = driver(); stages = []
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
______ test_parent_timeout_kills_inflight_owned_worker_at_global_deadline ______
test_v8_wp3_driver.py:100: in test_parent_timeout_kills_inflight_owned_worker_at_global_deadline
    d = driver(); proc = subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'], start_new_session=True)
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
_ test_inventory_preserves_completed_method_and_marks_interrupted_started_method _
test_v8_wp3_driver.py:110: in test_inventory_preserves_completed_method_and_marks_interrupted_started_method
    d = driver(); dd = design(); dd['repetitions'] = 1
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
____ test_support_requires_target_gains_and_rejects_outside_counterexample _____
test_v8_wp3_driver.py:135: in test_support_requires_target_gains_and_rejects_outside_counterexample
    d = driver(); rows = _screen_rows()
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
_____ test_support_missing_is_inconclusive_and_two_mcse_boundary_is_strict _____
test_v8_wp3_driver.py:145: in test_support_missing_is_inconclusive_and_two_mcse_boundary_is_strict
    d = driver(); rows = _screen_rows()
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
______ test_summary_pairs_same_rep_reference_and_retains_missing_reasons _______
test_v8_wp3_driver.py:153: in test_summary_pairs_same_rep_reference_and_retains_missing_reasons
    d = driver(); dd = design(); dd['repetitions']=2
        ^^^^^^^^
test_v8_wp3_driver.py:13: in driver
    return importlib.import_module('run_v8_wp3')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1395: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1324: in _find_and_load_unlocked
    ???
E   ModuleNotFoundError: No module named 'run_v8_wp3'
=========================== short test summary info ============================
FAILED test_v8_wp3_driver.py::test_parent_import_does_not_load_numerical_libraries
FAILED test_v8_wp3_driver.py::test_planned_order_keeps_every_rep_phi_p_and_all_method_slots
FAILED test_v8_wp3_driver.py::test_exclusive_outputs_reject_duplicate_and_symlink_without_overwrite
FAILED test_v8_wp3_driver.py::test_existing_formal_directory_is_refused_before_private_creation
FAILED test_v8_wp3_driver.py::test_sealed_hash_mismatch_is_detected_before_any_numerical_work
FAILED test_v8_wp3_driver.py::test_checkpoint_checks_absolute_global_deadline_even_when_ps_is_throttled
FAILED test_v8_wp3_driver.py::test_checkpoint_forces_each_cell_end_and_final_resource_measurement
FAILED test_v8_wp3_driver.py::test_parent_timeout_kills_inflight_owned_worker_at_global_deadline
FAILED test_v8_wp3_driver.py::test_inventory_preserves_completed_method_and_marks_interrupted_started_method
FAILED test_v8_wp3_driver.py::test_support_requires_target_gains_and_rejects_outside_counterexample
FAILED test_v8_wp3_driver.py::test_support_missing_is_inconclusive_and_two_mcse_boundary_is_strict
FAILED test_v8_wp3_driver.py::test_summary_pairs_same_rep_reference_and_retains_missing_reasons
12 failed in 0.07s
```

## RED: interrupted candidates and final summary schema

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 1

```text
............FFFFF                                                        [100%]
=================================== FAILURES ===================================
___ test_solver_failure_metadata_remains_scalar_and_preserves_reason_strings ___
test_v8_wp3_driver.py:176: in test_solver_failure_metadata_remains_scalar_and_preserves_reason_strings
    result=d.scalar_diagnostics([{'iterations':10000,'option':'max_iter','passed':False,'gap':.2}])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
run_v8_wp3.py:339: in scalar_diagnostics
    if item is None: raise ValueError('nonscalar diagnostic')
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ValueError: nonscalar diagnostic
_______ test_summary_command_requires_termination_and_writes_flat_cells ________
test_v8_wp3_driver.py:192: in test_summary_command_requires_termination_and_writes_flat_cells
    assert len(result['cells'])==3
               ^^^^^^^^^^^^^^^
E   KeyError: 'cells'
----------------------------- Captured stdout call -----------------------------
{"event": "summary_written", "status": "COMPLETE", "cells": 3}
_____ test_inflight_candidate_failure_is_not_relabelled_as_technical_error _____
test_v8_wp3_driver.py:205: in test_inflight_candidate_failure_is_not_relabelled_as_technical_error
    row=d.evaluate_method(design(),tmp_path,52,6,'QR33',report,lambda **kw:None,
        ^^^^^^^^^^^^^^^^^
E   AttributeError: module 'run_v8_wp3' has no attribute 'evaluate_method'
_________ test_selected_evaluation_failure_never_tries_another_penalty _________
test_v8_wp3_driver.py:221: in test_selected_evaluation_failure_never_tries_another_penalty
    row=d.evaluate_method(design(),tmp_path,52,6,'QR4',report,lambda **kw:None,
        ^^^^^^^^^^^^^^^^^
E   AttributeError: module 'run_v8_wp3' has no attribute 'evaluate_method'
___ test_resource_and_unknown_candidate_errors_are_persisted_then_propagate ____
test_v8_wp3_driver.py:236: in test_resource_and_unknown_candidate_errors_are_persisted_then_propagate
    d.evaluate_method(design(),public,52,6,'QR4',report,lambda **kw:None,FitError,(d.DriverStop,))
    ^^^^^^^^^^^^^^^^^
E   AttributeError: module 'run_v8_wp3' has no attribute 'evaluate_method'
=========================== short test summary info ============================
FAILED test_v8_wp3_driver.py::test_solver_failure_metadata_remains_scalar_and_preserves_reason_strings
FAILED test_v8_wp3_driver.py::test_summary_command_requires_termination_and_writes_flat_cells
FAILED test_v8_wp3_driver.py::test_inflight_candidate_failure_is_not_relabelled_as_technical_error
FAILED test_v8_wp3_driver.py::test_selected_evaluation_failure_never_tries_another_penalty
FAILED test_v8_wp3_driver.py::test_resource_and_unknown_candidate_errors_are_persisted_then_propagate
5 failed, 12 passed in 0.45s
```

## RED: failure diagnostics and pre-evaluation selection receipt

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 1

```text
.................FF                                                      [100%]
=================================== FAILURES ===================================
_____ test_fit_failure_nonfinite_diagnostic_does_not_erase_solver_failure ______
test_v8_wp3_driver.py:249: in test_fit_failure_nonfinite_diagnostic_does_not_erase_solver_failure
    assert row['candidates'][0]['reason']=='NONFINITE_ITERATE'
           ^^^^^^^^^^^^^^^^^^^^
E   IndexError: list index out of range
____ test_selection_is_sealed_before_evaluation_so_hard_kill_keeps_penalty _____
test_v8_wp3_driver.py:263: in test_selection_is_sealed_before_evaluation_so_hard_kill_keeps_penalty
    d.evaluate_method(design(),tmp_path,52,6,'QR4',report,lambda **kw:None,FitError,(d.DriverStop,))
run_v8_wp3.py:405: in evaluate_method
    score,diagnostics=report('evaluation',horizon,window,method,row['selected_penalty'])
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
test_v8_wp3_driver.py:258: in report
    selection=json.loads((tmp_path/'W52_H6_QR4.selection.json').read_text())
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/pathlib/_local.py:546: in read_text
    return PathBase.read_text(self, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/pathlib/_abc.py:632: in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/lib/python3.13/pathlib/_local.py:537: in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/4g/4pc4x_0x10dcd_t1wwhqss980000gn/T/pytest-of-bingyouli/pytest-29/test_selection_is_sealed_befor0/W52_H6_QR4.selection.json'
=========================== short test summary info ============================
FAILED test_v8_wp3_driver.py::test_fit_failure_nonfinite_diagnostic_does_not_erase_solver_failure
FAILED test_v8_wp3_driver.py::test_selection_is_sealed_before_evaluation_so_hard_kill_keeps_penalty
2 failed, 17 passed in 0.47s
```

## GREEN: final independent driver tests

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 0

```text
...................                                                      [100%]
19 passed in 0.43s
```

## Static CLI and source verification

`uv run --offline --with numpy==2.3.5 --with pytest python run_v8_wp3.py --help` exited 0, showing --run / --worker / --summarize and worker arguments without creating the formal directory.

`verify_design()` matched the current protocol bytes to design commit `039f6f1` and all five original-module SHA-256 digests. `results/revision-v8/wp3/` remained absent. No formal study was started.

The driver tests use constructed scalar reports, temporary files, a sleeping subprocess for deadline cancellation, and no DGP draws or model fits. Full repository pytest and the single formal run remain with root.

## RED: support classification with incomplete target cells

The frozen screen requires complete outside cells, while unknown target cells only prevent classification when they can change whether six target gains are attainable. No design files changed.

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 1

```text
...........FF.....F........                                              [100%]
=================================== FAILURES ===================================
_ test_support_classifies_only_when_missing_cells_cannot_change_decision[enough-known-target-gains] _
test_v8_wp3_driver.py:174: in test_support_classifies_only_when_missing_cells_cannot_change_decision
    assert result['status']==expected
E   AssertionError: assert 'INCONCLUSIVE' == 'SUPPORTED'
E     
E     - SUPPORTED
E     + INCONCLUSIVE
_ test_support_classifies_only_when_missing_cells_cannot_change_decision[too-few-possible-target-gains] _
test_v8_wp3_driver.py:174: in test_support_classifies_only_when_missing_cells_cannot_change_decision
    assert result['status']==expected
E   AssertionError: assert 'INCONCLUSIVE' == 'NOT_SUPPORTED'
E     
E     - NOT_SUPPORTED
E     + INCONCLUSIVE
_______ test_support_duplicate_cell_cannot_replace_missing_grid_identity _______
test_v8_wp3_driver.py:189: in test_support_duplicate_cell_cannot_replace_missing_grid_identity
    assert d.support_for_method(rows,'QR33')['status']=='INCONCLUSIVE'
E   AssertionError: assert 'SUPPORTED' == 'INCONCLUSIVE'
E     
E     - INCONCLUSIVE
E     + SUPPORTED
=========================== short test summary info ============================
FAILED test_v8_wp3_driver.py::test_support_classifies_only_when_missing_cells_cannot_change_decision[enough-known-target-gains]
FAILED test_v8_wp3_driver.py::test_support_classifies_only_when_missing_cells_cannot_change_decision[too-few-possible-target-gains]
FAILED test_v8_wp3_driver.py::test_support_duplicate_cell_cannot_replace_missing_grid_identity
3 failed, 24 passed in 0.48s
```

## GREEN: support classification correction

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp3_driver.py`

Exit code: 0

```text
...........................                                              [100%]
27 passed in 0.44s
```

Classification precedence now matches the frozen rule. Missing/unevaluable cells stay listed, including missing grid identities; complete-grid validation also rejects duplicated identities. No simulation or formal run was performed.
