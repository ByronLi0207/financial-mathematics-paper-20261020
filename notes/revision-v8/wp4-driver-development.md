# WP4 driver development evidence

Only constructed arrays/reports and temporary IO are tested. No accepted raw FX file is read, aggregated, or fit during development.

## RED before implementation

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp4_driver.py`

Exit code: 1

```text
FFFFFFFFFFF                                                              [100%]
=================================== FAILURES ===================================
_____________ test_parent_import_keeps_numerical_modules_unloaded ______________
test_v8_wp4_driver.py:21: in test_parent_import_keeps_numerical_modules_unloaded
    assert r.returncode==0,r.stderr
E   AssertionError: Traceback (most recent call last):
E       File "<string>", line 1, in <module>
E         import run_v8_wp4,sys; assert not any(x in sys.modules for x in ('numpy','study_data','v8_daily_fx','v8_mechanism_mc'))
E         ^^^^^^^^^^^^^^^^^^^^^
E     ModuleNotFoundError: No module named 'run_v8_wp4'
E     
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['/Users/bingyouli/.cache/uv/builds-v0/.tmpCdFadw/bin/python', '-c', "import run_v8_wp4,sys; ass...v8_daily_fx\',\'v8_mechanism_mc\'))\n    ^^^^^^^^^^^^^^^^^^^^^\nModuleNotFoundError: No module named \'run_v8_wp4\'\n').returncode
______ test_four_cells_have_twelve_methods_and_thirty_two_candidate_slots ______
test_v8_wp4_driver.py:25: in test_four_cells_have_twelve_methods_and_thirty_two_candidate_slots
    d=driver();dd=design()
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
___________ test_sample_na_keeps_all_methods_and_declared_candidates ___________
test_v8_wp4_driver.py:36: in test_sample_na_keeps_all_methods_and_declared_candidates
    d=driver();dd=design();cell=list(d.planned_cells(dd))[0]
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
_________ test_source_and_daily_fingerprints_must_match_across_workers _________
test_v8_wp4_driver.py:50: in test_source_and_daily_fingerprints_must_match_across_workers
    d=driver()
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
___ test_private_trace_is_exclusive_and_public_receipt_has_only_fingerprint ____
test_v8_wp4_driver.py:61: in test_private_trace_is_exclusive_and_public_receipt_has_only_fingerprint
    d=driver();private=tmp_path/'private';private.mkdir();public=tmp_path/'public';public.mkdir()
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
_________ test_parent_deadline_interrupts_only_owned_inflight_process __________
test_v8_wp4_driver.py:74: in test_parent_deadline_interrupts_only_owned_inflight_process
    d=driver();child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],start_new_session=True)
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
________ test_trace_fingerprint_is_reconciled_into_candidate_inventory _________
test_v8_wp4_driver.py:82: in test_trace_fingerprint_is_reconciled_into_candidate_inventory
    d=driver();dd=design();public=tmp_path/'cells'/'W52_H6';public.mkdir(parents=True)
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
___ test_eight_contrasts_keep_full_precision_matched_counts_and_na_reference ___
test_v8_wp4_driver.py:106: in test_eight_contrasts_keep_full_precision_matched_counts_and_na_reference
    d=driver();rows=_reports()
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
__ test_zero_reference_loss_is_undefined_without_inventing_a_relative_change ___
test_v8_wp4_driver.py:119: in test_zero_reference_loss_is_undefined_without_inventing_a_relative_change
    d=driver();rows=_reports();rows[0]['evaluation']['mean_loss']=0.
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
_______ test_summary_refuses_before_termination_without_creating_output ________
test_v8_wp4_driver.py:126: in test_summary_refuses_before_termination_without_creating_output
    d=driver();d.exclusive_json(tmp_path/'manifest.json',{'formal_directory':str(tmp_path)})
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
___ test_existing_output_is_not_reused_and_source_code_mutation_is_detected ____
test_v8_wp4_driver.py:132: in test_existing_output_is_not_reused_and_source_code_mutation_is_detected
    d=driver();formal=tmp_path/'formal';formal.mkdir()
      ^^^^^^^^
test_v8_wp4_driver.py:12: in driver
    def driver():return importlib.import_module('run_v8_wp4')
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
E   ModuleNotFoundError: No module named 'run_v8_wp4'
=========================== short test summary info ============================
FAILED test_v8_wp4_driver.py::test_parent_import_keeps_numerical_modules_unloaded
FAILED test_v8_wp4_driver.py::test_four_cells_have_twelve_methods_and_thirty_two_candidate_slots
FAILED test_v8_wp4_driver.py::test_sample_na_keeps_all_methods_and_declared_candidates
FAILED test_v8_wp4_driver.py::test_source_and_daily_fingerprints_must_match_across_workers
FAILED test_v8_wp4_driver.py::test_private_trace_is_exclusive_and_public_receipt_has_only_fingerprint
FAILED test_v8_wp4_driver.py::test_parent_deadline_interrupts_only_owned_inflight_process
FAILED test_v8_wp4_driver.py::test_trace_fingerprint_is_reconciled_into_candidate_inventory
FAILED test_v8_wp4_driver.py::test_eight_contrasts_keep_full_precision_matched_counts_and_na_reference
FAILED test_v8_wp4_driver.py::test_zero_reference_loss_is_undefined_without_inventing_a_relative_change
FAILED test_v8_wp4_driver.py::test_summary_refuses_before_termination_without_creating_output
FAILED test_v8_wp4_driver.py::test_existing_output_is_not_reused_and_source_code_mutation_is_detected
11 failed in 0.22s
```

## RED: transient final resource failure and lifecycle fixtures

The worker fixture injects one constructed observation through the source-loader boundary; the accepted raw file is never opened. It takes NA geometry and cannot fit any model. Parent dispatch is replaced by a deterministic failed child.

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp4_driver.py`

Exit code: 1

```text
...........F..                                                           [100%]
=================================== FAILURES ===================================
___ test_transient_cell_end_resource_failure_cannot_leave_na_worker_success ____
test_v8_wp4_driver.py:166: in test_transient_cell_end_resource_failure_cannot_leave_na_worker_success
    assert d.run_worker(args)==1
E   AssertionError: assert 0 == 1
E    +  where 0 = <function run_worker at 0x10b47fba0>(namespace(manifest=PosixPath('/private/var/folders/4g/4pc4x_0x10dcd_t1wwhqss980000gn/T/pytest-of-bingyouli/pytest-49/test_transient_cell_end_resour0/manifest.json'), window=52, horizon=6, global_deadline=2009297.180777333))
E    +    where <function run_worker at 0x10b47fba0> = <module 'run_v8_wp4' from '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/run_v8_wp4.py'>.run_worker
=========================== short test summary info ============================
FAILED test_v8_wp4_driver.py::test_transient_cell_end_resource_failure_cannot_leave_na_worker_success
1 failed, 13 passed in 0.27s
```

## GREEN: final driver tests

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp4_driver.py`

Exit code: 0

```text
..............                                                           [100%]
14 passed in 0.26s
```

## Static source/code verification

`run_v8_wp4.py --help` exited 0 without creating formal output. `verify_design()` verified both current WP4 protocol bytes against commit `1427dc0`, the nine frozen source modules, and `protocol/study-spec.json` against `run_study.SPEC_SHA256`, including matching source SHA/bytes/row count in the two contracts. These checks read only protocol/source code, not the accepted raw FX file. `results/revision-v8/wp4/` remained absent.

The parent imports only stdlib and the sealed stdlib-only WP3 runner. Four sequential cells use actual RunGuard RSS/ps checks, the sealed global-deadline wrapper and owned-process cancellation. Every private daily mapping and complete per-issue trace is NPZ under task scratch; only hashes and aggregate metadata appear publicly. Candidate trace hashes are reconciled into the twelve-slot inventory. No formal aggregation, forecast, or study run was executed. Root owns the final full test suite and the unique formal run.

## RED: interrupted ineligible validation selection

A sealed INELIGIBLE selection with penalty None is a valid interrupted state, while SELECTED must carry a declared nonempty penalty. Only constructed receipts are read.

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp4_driver.py`

Exit code: 1

```text
.......F..F.......                                                       [100%]
=================================== FAILURES ===================================
___ test_ineligible_selection_survives_hard_kill_before_final_method_receipt ___
test_v8_wp4_driver.py:101: in test_ineligible_selection_survives_hard_kill_before_final_method_receipt
    rows=d.build_inventory(dd,tmp_path);row=rows[1]
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
run_v8_wp4.py:144: in build_inventory
    if penalty not in design['menus'].get(method,[]):raise DriverStop('INVALID_SELECTION_RECEIPT')
                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   run_v8_wp3.DriverStop: INVALID_SELECTION_RECEIPT
_____ test_invalid_selected_or_ineligible_penalty_is_rejected[selection2] ______
test_v8_wp4_driver.py:118: in test_invalid_selected_or_ineligible_penalty_is_rejected
    with pytest.raises(d.DriverStop,match='INVALID_SELECTION_RECEIPT'):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   Failed: DID NOT RAISE DriverStop
=========================== short test summary info ============================
FAILED test_v8_wp4_driver.py::test_ineligible_selection_survives_hard_kill_before_final_method_receipt
FAILED test_v8_wp4_driver.py::test_invalid_selected_or_ineligible_penalty_is_rejected[selection2]
2 failed, 16 passed in 0.28s
```

## GREEN: interrupted ineligible validation selection

Command: `uv run --offline --with numpy==2.3.5 --with pytest pytest -q --tb=short test_v8_wp4_driver.py`

Exit code: 0

```text
..................                                                       [100%]
18 passed in 0.24s
```

The interrupted row now preserves FAILED / VALIDATION_INELIGIBLE, selected_penalty None, validation_selection, and all failed candidates. SELECTED still requires a menu penalty; an INELIGIBLE record carrying a penalty is rejected. No protocol or sealed WP3 file changed. No raw data or formal run was used.
