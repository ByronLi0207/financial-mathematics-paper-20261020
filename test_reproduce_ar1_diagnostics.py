"""Artificial fresh-attempt binding; no real sources, traces or counts."""
import copy
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_build_ar1_diagnostics import Fixture as RetainedFixture,Guard,raw_json,identity
import build_ar1_diagnostics as retained

ROOT=Path(__file__).resolve().parent
AVAILABLE=importlib.util.find_spec('reproduce_ar1_diagnostics') is not None
if AVAILABLE:import reproduce_ar1_diagnostics as fresh


class EntryTests(unittest.TestCase):
    def test_fresh_diagnostic_entry_exists(self):
        self.assertTrue(AVAILABLE,'fresh-attempt diagnostic entry is missing')

    @unittest.skipUnless(AVAILABLE,'initial RED: missing entry')
    def test_help_and_import_do_not_load_numeric_or_sources(self):
        code=("import runpy,sys; sys.argv=[sys.argv[1],'--help']\n"
              "try: runpy.run_path(sys.argv[0],run_name='__main__')\n"
              "except SystemExit as e: assert e.code==0\n"
              "assert 'numpy' not in sys.modules and 'run_ar1_replay' not in sys.modules\n")
        done=subprocess.run([sys.executable,'-B','-c',code,str(ROOT/'reproduce_ar1_diagnostics.py')],capture_output=True,text=True)
        self.assertEqual(done.returncode,0,done.stderr)
        for flag in ('--replication-dir','--ar1-attempt-id','--readback','--readback-sha256','--diagnostic-id','--freeze'):
            self.assertIn(flag,done.stdout)


class Fixture:
    """Only the old replica proof and actual measurement are external seams."""
    def __init__(self,root):
        self.root=Path(root);self.base=RetainedFixture(root);f=self.base
        f.run(diagnostic_id='reference')
        old_output=f.attempt/'ar1-diagnostics-reference/public'
        for name in ('ar1-floor.csv','ar1-horizon.csv','ar1-diagnostics-audit.json'):
            f.write(fresh.REFERENCE_DIR+'/'+name,(old_output/name).read_bytes())
        f.write(fresh.REFERENCE_DIR+'/independent-readback.json',b'{"artificial_prior_independent_check":true}\n')
        self.old_manifest=copy.deepcopy(f.manifest);self.old_readback=copy.deepcopy(f.readback)
        self.ar_id='fresh';self.dest=f.attempt/('ar1-replay-'+self.ar_id);shutil.copytree(f.dest,self.dest)
        self.manifest=copy.deepcopy(f.manifest)
        self.manifest.update(attempt_id=self.ar_id,created_utc='2000-01-02T00:00:00Z',new_selection_sha256='a'*64)
        f.inputs['selection_hash']='a'*64
        for entry in self.manifest['exports']:
            if entry['path'].endswith('-receipt.json'):
                p=self.dest/'public'/entry['path'];receipt=json.loads(p.read_bytes());receipt['new_selection_sha256']='a'*64
                raw=raw_json(receipt);p.write_bytes(raw);entry.update(identity(raw))
        by_name={e['path']:e for e in self.manifest['exports']}
        for record in self.manifest['cell_receipts']:
            record['receipt']=by_name[record['receipt']['path']]
        self.readback=copy.deepcopy(f.readback)
        self.readback.update(verified_utc='2000-01-02T00:01:00Z',resources=Guard().resources)
        self.readback_path='state/revision-20261022/synthetic-fresh-ar1-readback.json'
        for name in ('reproduce_ar1_diagnostics.py','test_reproduce_ar1_diagnostics.py',fresh.DESIGN_PATH):
            f.write(name,(ROOT/name).read_bytes())
        self.reseal()

    def reseal(self):
        raw=raw_json(self.manifest);(self.dest/'public/ar1-replay-manifest.json').write_bytes(raw)
        self.readback['ar1_manifest_sha256']=hashlib.sha256(raw).hexdigest()
        raw=raw_json(self.readback);self.base.write(self.readback_path,raw)
        self.readback_hash=hashlib.sha256(raw).hexdigest();self.freeze()

    def freeze(self):
        paths=fresh.required_freeze_paths(self.root)
        files={n:hashlib.sha256((self.root/n).read_bytes()).hexdigest() for n in paths}
        value=dict(version=1,status='FROZEN',created_utc='2000-01-01T00:00:00Z',retained_freeze_path=fresh.RETAINED_FREEZE,
            retained_freeze_sha256=files[fresh.RETAINED_FREEZE],design_path=fresh.DESIGN_PATH,
            design_sha256=files[fresh.DESIGN_PATH],files=files)
        raw=raw_json(value);self.base.write(fresh.FREEZE_PATH,raw);self.freeze_hash=hashlib.sha256(raw).hexdigest()

    def replace_trace(self,cell,vectors):
        stem=f"{cell['source']}-h{cell['horizon']}-w{cell['window']}";np=self.base.np
        entry=next(e for e in self.manifest['private_exports'] if e['path']==stem+'-traces.npz')
        out=io.BytesIO();np.savez_compressed(out,**vectors);raw=out.getvalue()
        (self.dest/'private'/entry['path']).write_bytes(raw);entry.update(identity(raw))
        public=next(e for e in self.manifest['exports'] if e['path']==stem+'-receipt.json')
        p=self.dest/'public'/public['path'];receipt=json.loads(p.read_bytes())
        receipt['private_artifacts']=[e for e in self.manifest['private_exports']
            if e['path'] in (stem+'-fits.json',stem+'-traces.npz')]
        raw=raw_json(receipt);p.write_bytes(raw);public.update(identity(raw))
        for row in self.manifest['cell_receipts']:
            if row['cell']==cell:row['receipt']=public
        self.reseal()

    def run(self,diagnostic_id='fresh-diagnostics',guard=Guard,readback_hash=None,context=None):
        return fresh.execute(self.root,str(self.base.attempt.relative_to(self.root)),self.ar_id,self.readback_path,
            self.readback_hash if readback_hash is None else readback_hash,diagnostic_id,self.freeze_hash,
            context_provider=self.base.context if context is None else context,guard_factory=guard)

    @property
    def output(self):return self.base.attempt/'ar1-diagnostics-reproduction-fresh-diagnostics'


@unittest.skipUnless(AVAILABLE,'initial RED: missing entry')
class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(fresh,'execute',None)),'fresh-attempt execution is missing')
        parent=ROOT/'.scratch/revision-20261022/ar1-diagnostic-reproduction-tests';parent.mkdir(parents=True,exist_ok=True)
        temp=tempfile.TemporaryDirectory(dir=parent);self.addCleanup(temp.cleanup)
        self.f=Fixture(Path(temp.name).resolve())

    def test_fresh_timestamp_attempt_and_selection_are_bound_without_altering_retained_plan(self):
        f=self.f;old_plan=(f.root/retained.PLAN_PATH).read_bytes();old_readback=(f.root/retained.READBACK_PATH).read_bytes()
        result=f.run();self.assertEqual(result['status'],'AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED')
        self.assertEqual((result['floor_rows'],result['horizon_rows']),(8,4))
        self.assertTrue(result['exact_csv_byte_agreement']);self.assertTrue(result['exact_csv_scalar_agreement'])
        self.assertEqual((f.root/retained.PLAN_PATH).read_bytes(),old_plan)
        self.assertEqual((f.root/retained.READBACK_PATH).read_bytes(),old_readback)
        binding=json.loads((f.output/'private/input-binding.json').read_bytes())
        self.assertEqual(binding['role'],'INPUT_BINDING_ONLY');self.assertFalse(binding['upstream_receipt_generated'])
        self.assertEqual(binding['new_selection_sha256'],'a'*64)
        self.assertEqual(binding['readback']['sha256'],f.readback_hash)
        self.assertNotEqual(binding['manifest']['sha256'],f.base.plan['ar1_manifest_sha256'])

    def test_retained_entry_still_rejects_fresh_manifest_and_readback_path(self):
        f=self.f;frozen=retained.preflight(f.root,f.base.freeze_hash)
        raw=(f.dest/'public/ar1-replay-manifest.json').read_bytes()
        with self.assertRaises(retained.DiagnosticError):retained.validate_readback(frozen,raw)
        with self.assertRaises(retained.DiagnosticError):retained.verify_context(frozen,f.base.inputs,f.base.execution,
            f.ar_id,f.readback_path)

    def test_bad_new_code_hash_stops_before_any_context_call(self):
        f=self.f;(f.root/'reproduce_ar1_diagnostics.py').write_bytes(b'raise AssertionError("unverified")\n')
        def forbidden(*args):raise AssertionError('context called before code verification')
        with self.assertRaises(fresh.ReproductionError):f.run(context=forbidden)
        self.assertFalse(f.output.exists())

    def test_explicit_readback_hash_mismatch_is_rejected_before_context(self):
        f=self.f
        def forbidden(*args):raise AssertionError('context called before receipt hash verification')
        with self.assertRaises(fresh.ReproductionError):f.run(readback_hash='0'*64,context=forbidden)
        self.assertFalse(f.output.exists())

    def test_readback_for_other_manifest_is_rejected_even_when_all_tables_equal(self):
        f=self.f;f.readback['ar1_manifest_sha256']=f.base.plan['ar1_manifest_sha256']
        raw=raw_json(f.readback);f.base.write(f.readback_path,raw);f.readback_hash=hashlib.sha256(raw).hexdigest()
        with self.assertRaises(fresh.ReproductionError):f.run()
        self.assertFalse((f.output/'public/ar1-diagnostics-reproduction-audit.json').exists())

    def test_pass_label_does_not_override_wrong_auditor_or_scientific_contract(self):
        f=self.f
        for j,key in enumerate(('code_sha256','ar1_spec_sha256','ar1_freeze_sha256')):
            saved=f.readback[key];f.readback[key]='0'*64
            raw=raw_json(f.readback);f.base.write(f.readback_path,raw);f.readback_hash=hashlib.sha256(raw).hexdigest()
            with self.subTest(key=key),self.assertRaises(fresh.ReproductionError):f.run(diagnostic_id='bad'+str(j))
            f.readback[key]=saved

    def test_manifest_wrong_context_or_selection_is_rejected_with_matching_readback(self):
        f=self.f
        for j,(key,value) in enumerate((('new_selection_sha256','b'*64),('attempt_id','different'),
            ('replication_dir','.scratch/revision-20261022/replication-other'))):
            saved=f.manifest[key];f.manifest[key]=value;f.reseal()
            with self.subTest(key=key),self.assertRaises(fresh.ReproductionError):f.run(diagnostic_id='bad'+str(j))
            f.manifest[key]=saved

    def test_changed_capacity_is_valid_recomputation_with_public_scalar_differences(self):
        f=self.f;cell=f.base.cells[0];v={k:a.copy() for k,a in f.base.vectors[
            cell['source'],cell['horizon'],cell['window']].items()}
        v['capacity'][0]=1.;v['pinball'][0]=0.;f.replace_trace(cell,v);result=f.run()
        self.assertEqual(result['status'],'AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED')
        self.assertFalse(result['exact_csv_scalar_agreement'])
        comparison=json.loads((f.output/'public/ar1-diagnostics-comparison.json').read_bytes())
        columns={d['column'] for d in comparison['tables']['ar1-floor.csv']['differences']}
        self.assertIn('floor_binding_count',columns)

    def test_resealed_trace_origin_refit_and_floor_alignment_fail_without_shortened_export(self):
        f=self.f;cell=f.base.cells[0]
        for j,field in enumerate(('origins','refit_indices','floor')):
            v={k:a.copy() for k,a in f.base.vectors[cell['source'],cell['horizon'],cell['window']].items()}
            v[field][0]+=1;f.replace_trace(cell,v)
            with self.subTest(field=field),self.assertRaises(fresh.ReproductionError):f.run(diagnostic_id='alignment'+str(j))
            p=f.base.attempt/('ar1-diagnostics-reproduction-alignment'+str(j))/'public'
            self.assertFalse((p/'ar1-floor.csv').exists())

    def test_reference_duplicate_key_is_not_accepted_as_a_comparison(self):
        f=self.f;p=f.root/fresh.REFERENCE_DIR/'ar1-floor.csv'
        rows=list(csv.DictReader(io.StringIO(p.read_text())));rows[-1]=rows[0].copy();raw=f.base.csv(rows);p.write_bytes(raw)
        a=f.root/fresh.REFERENCE_DIR/'ar1-diagnostics-audit.json';audit=json.loads(a.read_bytes())
        for e in audit['exports']:
            if e['path']=='ar1-floor.csv':e.update(identity(raw))
        a.write_bytes(raw_json(audit));f.freeze()
        with self.assertRaises(fresh.ReproductionError):f.run()

    def test_wrong_reference_horizon_label_is_rejected_even_with_resealed_hashes(self):
        f=self.f;p=f.root/fresh.REFERENCE_DIR/'ar1-horizon.csv'
        rows=list(csv.DictReader(io.StringIO(p.read_text())));rows[0]['short_horizon']='24'
        raw=f.base.csv(rows);p.write_bytes(raw)
        a=f.root/fresh.REFERENCE_DIR/'ar1-diagnostics-audit.json';audit=json.loads(a.read_bytes())
        for e in audit['exports']:
            if e['path']=='ar1-horizon.csv':e.update(identity(raw))
        a.write_bytes(raw_json(audit));f.freeze()
        with self.assertRaises(fresh.ReproductionError):f.run()

    def test_missing_reference_numeric_column_cannot_claim_a_complete_comparison(self):
        f=self.f;p=f.root/fresh.REFERENCE_DIR/'ar1-floor.csv'
        rows=list(csv.DictReader(io.StringIO(p.read_text())))
        for row in rows:row.pop('floor_binding_count')
        raw=f.base.csv(rows);p.write_bytes(raw)
        a=f.root/fresh.REFERENCE_DIR/'ar1-diagnostics-audit.json';audit=json.loads(a.read_bytes())
        for e in audit['exports']:
            if e['path']=='ar1-floor.csv':e.update(identity(raw))
        a.write_bytes(raw_json(audit));f.freeze()
        with self.assertRaises(fresh.ReproductionError):f.run()

    def test_one_ulp_public_scalar_difference_is_preserved_without_a_tolerance(self):
        f=self.f;p=f.root/fresh.REFERENCE_DIR/'ar1-floor.csv'
        rows=list(csv.DictReader(io.StringIO(p.read_text())))
        rows[0]['floor_binding_rate']=str(float(f.base.np.nextafter(float(rows[0]['floor_binding_rate']),1.)))
        raw=f.base.csv(rows);p.write_bytes(raw)
        a=f.root/fresh.REFERENCE_DIR/'ar1-diagnostics-audit.json';audit=json.loads(a.read_bytes())
        for e in audit['exports']:
            if e['path']=='ar1-floor.csv':e.update(identity(raw))
        a.write_bytes(raw_json(audit));f.freeze();result=f.run()
        self.assertEqual(result['status'],'AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED')
        self.assertFalse(result['exact_csv_scalar_agreement'])
        comp=json.loads((f.output/'public/ar1-diagnostics-comparison.json').read_bytes())
        found=[d for d in comp['tables']['ar1-floor.csv']['differences'] if d['column']=='floor_binding_rate']
        self.assertEqual(len(found),1);self.assertGreater(found[0]['absolute_numeric_difference'],0.)

    def test_private_trace_change_at_final_checkpoint_is_failure_not_a_verified_subset(self):
        f=self.f;trace=next((f.dest/'private').glob('*-traces.npz'))
        class Change(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_reproduction_final':trace.write_bytes(trace.read_bytes()+b'changed')
        with self.assertRaises(fresh.ReproductionError):f.run(guard=Change)
        self.assertFalse((f.output/'public/ar1-floor.csv').exists())
        self.assertTrue((f.output/'private/unverified-ar1-floor.csv').exists())

    def test_final_binding_and_readback_change_each_stop_success(self):
        f=self.f
        for j,kind in enumerate(('binding','readback')):
            class Change(Guard):
                def __call__(self,**kwargs):
                    if kwargs.get('stage')=='ar1_diagnostic_reproduction_final':
                        p=(f.base.attempt/('ar1-diagnostics-reproduction-case'+str(j))/'private/input-binding.json'
                            if kind=='binding' else f.root/f.readback_path)
                        p.write_bytes(p.read_bytes()+b'changed')
            with self.subTest(kind=kind),self.assertRaises(fresh.ReproductionError):f.run(diagnostic_id='case'+str(j),guard=Change)

    def test_output_collision_never_overwrites_success(self):
        f=self.f;f.run();p=f.output/'public/ar1-diagnostics-reproduction-audit.json';raw=p.read_bytes()
        with self.assertRaises(fresh.ReproductionError):f.run()
        self.assertEqual(p.read_bytes(),raw)

    def test_resource_cancellation_preserves_sanitized_failure(self):
        class Cancel(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_reproduction_cell':
                    e=RuntimeError('private message');e.code='RESOURCE_WALL';raise e
        f=self.f
        with self.assertRaises(fresh.ReproductionError):f.run(guard=Cancel)
        raw=(f.output/'public/ar1-diagnostics-reproduction-failure.json').read_bytes()
        self.assertNotIn(b'private message',raw);self.assertIn(b'RESOURCE_WALL',raw)
        self.assertFalse((f.output/'public/ar1-floor.csv').exists())

    def test_partial_csv_comparison_and_success_audit_writes_are_quarantined(self):
        f=self.f;original=Path.open
        for j,name in enumerate(('ar1-floor.csv','ar1-diagnostics-comparison.json','ar1-diagnostics-reproduction-audit.json')):
            target=f.base.attempt/('ar1-diagnostics-reproduction-write'+str(j))/'public'/name
            class Partial:
                def __init__(self,stream):self.stream=stream
                def __enter__(self):self.stream.__enter__();return self
                def __exit__(self,*args):return self.stream.__exit__(*args)
                def write(self,raw):self.stream.write(raw[:17]);raise OSError('artificial partial write')
            def fail(path,*args,**kwargs):
                stream=original(path,*args,**kwargs)
                return Partial(stream) if path==target and args==('xb',) else stream
            with self.subTest(name=name),patch.object(Path,'open',new=fail):
                with self.assertRaises(fresh.ReproductionError):f.run(diagnostic_id='write'+str(j))
            self.assertFalse(target.exists())
            self.assertEqual(len((target.parent.parent/'private'/('unverified-'+name)).read_bytes()),17)


if __name__=='__main__':unittest.main()
