"""Run unchanged old control methods on the proved current-content replay view.

Only fixture placement differs: each original test gets a fresh ignored copy
of the exact reconstructed old layout. Guard and assertions remain unchanged.
No file is deleted or overwritten, and no financial calculation is executed.
"""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import unittest

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'notes/revision-v9'
receipt=json.loads((HERE/'wp7-supp-number-audit.json').read_text())
view=ROOT/receipt['unchanged_legacy_guard']['reconstruction_view']
path=ROOT/'notes/revision-v8/test_v8_supp_numbers.py'
spec=importlib.util.spec_from_file_location('unchanged_supp_controls',path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
runroot=ROOT/'.scratch/revision-v9/wp7-supp-legacy-negative-controls'
runroot.mkdir(exist_ok=False)


def setup(self):
    self.docs=runroot/self._testMethodName
    for name in ['submission-jof/supplement.tex',*module.checker.EXPECTED_INPUTS]:
        target=self.docs/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(view/name,target)


# Do not call TemporaryDirectory cleanup: all task-owned fixtures are preserved.
module.SupplementNumericControls.setUp=setup
module.SupplementNumericControls.tearDown=lambda self:None
suite=unittest.defaultTestLoader.loadTestsFromTestCase(module.SupplementNumericControls)
stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
console=stream.getvalue()
with (HERE/'wp7-supp-legacy-controls-console.txt').open('x') as f:f.write(console)
print(console,end='')
payload=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests_run=result.testsRun,
    errors=len(result.errors),failures=len(result.failures),skips=len(result.skipped),
    old_guard_path=str((ROOT/'notes/revision-v8/check_wp8_supp_numbers.py').relative_to(ROOT)),
    old_guard_sha256=hashlib.sha256((ROOT/'notes/revision-v8/check_wp8_supp_numbers.py').read_bytes()).hexdigest(),
    old_control_file=str(path.relative_to(ROOT)),old_control_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    fixture_source=str(view.relative_to(ROOT)),preserved_fixture_directory=str(runroot.relative_to(ROOT)),
    scope='Original unchanged test methods and original unchanged guard; fixture setup uses the exact inverse-mapped layout already proved from current compact/extended text. This is not PDF/current-layout validation.',
    control_mutations=['swapped complete MC rows','changed integer master entropy','unbound inline p-value','unbound result beside image layout command','omitted required table input','changed old numeric row'],
    additional_controls=['unmutated replay passes','native JSON types are not coerced'],
    source_files_overwritten=0,files_deleted=0,new_financial_calculations=0)
with (HERE/'wp7-supp-legacy-controls.json').open('x') as f:json.dump(payload,f,indent=2);f.write('\n')
print(json.dumps({k:payload[k] for k in ('status','tests_run','errors','failures','skips','files_deleted','new_financial_calculations')},indent=2))
raise SystemExit(0 if result.wasSuccessful() else 1)
