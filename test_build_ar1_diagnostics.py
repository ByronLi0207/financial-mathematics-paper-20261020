"""Artificial AR diagnostic fixtures; never locate real traces or sources."""
import copy
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent
AVAILABLE=importlib.util.find_spec('build_ar1_diagnostics') is not None
if AVAILABLE:import build_ar1_diagnostics as builder

for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'


def raw_json(x):return (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
def identity(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


class Guard:
    def __init__(self,*args):
        self.resources=dict(elapsed_seconds=.1,peak_rss_bytes=1000000,maximum_observed_os_threads=1,
            requested_numerical_threads=1,thread_snapshot_count=1,thread_probe_status='PASS')
    def __call__(self,**kwargs):pass
    def arrays(self,*args):pass


class Fixture:
    def __init__(self,root):
        import numpy as np
        self.np=np;self.root=Path(root);self.plan=json.loads((ROOT/'protocol/revision-20261022/ar1-diagnostics-plan.json').read_bytes())
        self.attempt=self.root/'.scratch/revision-20261022/replication-synthetic';self.attempt.mkdir(parents=True)
        self.ar_id='retained';self.dest=self.attempt/('ar1-replay-'+self.ar_id)
        (self.dest/'public').mkdir(parents=True);(self.dest/'private').mkdir()
        skip={builder.PLAN_PATH,self.plan['accepted_v2_readback']['path'],*builder.PROTECTED_PATHS}
        for name in builder.required_freeze_paths(ROOT):
            if name not in skip:self.write(name,(ROOT/name).read_bytes())
        for name in builder.PROTECTED_PATHS:self.write(name,b'protected,unchanged\nfixture,only\n')
        self.spec=json.loads((self.root/'protocol/revision-20261022/study-spec.json').read_bytes())
        self.cells=[dict(source=s,horizon=h,window=w) for s,c in self.plan['sources'].items()
            for h in (6,24) for w in c['windows']]
        self.execution=dict(spec=dict(cells=self.cells),spec_sha256=self.plan['ar1_spec_sha256'],
            freeze_sha256=self.plan['ar1_freeze_sha256'])
        self.inputs=dict(root=self.root,attempt=self.attempt,spec=self.spec,snapshots={},selection_hash='f'*64,
            archive=dict(executable_freeze_sha256=self.plan['original_executable_freeze_sha256'],
                selection_freeze_sha256=self.plan['original_selection_sha256']))
        self.vectors={};self.summary=[];self.fit_entries={};self.trace_entries={};self.cell_entries={}
        for cell in self.cells:
            s,h,w=(cell[k] for k in ('source','horizon','window'));cfg=self.plan['sources'][s]
            ids=np.arange(cfg['evaluation_first'],cfg['evaluation_last']+1,dtype=np.int64);j=np.arange(len(ids))
            floor=np.ones(len(ids),dtype=np.float64);peak=1.+(j%2)+(1. if h==24 else 0.)
            capacity=(np.array([3.,1.,3.,2.] if h==6 else [1.,2.,3.,2.])[j%4]
                if w==cfg['windows'][0] else np.ones(len(ids)))
            refit=ids[0]+(ids-ids[0])//cfg['refit_step']*cfg['refit_step']
            self.vectors[s,h,w]=dict(origins=ids,capacity=capacity,peak=peak,floor=floor,refit_indices=refit,
                pinball=.95*np.maximum(peak-capacity,0.)+.05*np.maximum(capacity-peak,0.))
        self.reseal()

    def write(self,name,raw):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)

    def csv(self,rows):
        out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        return out.getvalue().encode()

    def reseal(self):
        np=self.np;public=[];private=[];receipts=[];self.summary=[]
        for cell in self.cells:
            s,h,w=(cell[k] for k in ('source','horizon','window'));stem=f'{s}-h{h}-w{w}'
            v=self.vectors[s,h,w];cfg=self.spec['sources'][s]
            fit_name=stem+'-fits.json';fit_raw=b'{"synthetic_opaque_prior_audit":true}\n'
            self.write(str((self.dest/'private'/fit_name).relative_to(self.root)),fit_raw)
            fit_entry=dict(path=fit_name,**identity(fit_raw));private.append(fit_entry);self.fit_entries[s,h,w]=fit_entry
            trace_name=stem+'-traces.npz';out=io.BytesIO();np.savez_compressed(out,**v);trace_raw=out.getvalue()
            self.write(str((self.dest/'private'/trace_name).relative_to(self.root)),trace_raw)
            trace_entry=dict(path=trace_name,**identity(trace_raw));private.append(trace_entry);self.trace_entries[s,h,w]=trace_entry
            fit_count=len(set(map(int,v['refit_indices'])))
            receipt=dict(version=1,cell=cell,method='AR1_REPLAY',status='COMPLETE',stop_code=None,
                expected_origin_count=len(v['origins']),completed_origin_count=len(v['origins']),fit_count=fit_count,
                source_identity={k:cfg[k] for k in ('sha256','bytes','record_count','native_unit')},
                new_selection_sha256='f'*64,ar1_spec_sha256=self.plan['ar1_spec_sha256'],
                ar1_freeze_sha256=self.plan['ar1_freeze_sha256'],private_artifacts=[fit_entry,trace_entry])
            name=stem+'-receipt.json';raw=raw_json(receipt);self.write(str((self.dest/'public'/name).relative_to(self.root)),raw)
            entry=dict(path=name,**identity(raw));public.append(entry);self.cell_entries[s,h,w]=entry
            receipts.append(dict(cell=cell,status='COMPLETE',receipt=entry))
            self.summary.append(dict(source=s,native_unit=cfg['native_unit'],horizon=h,window=w,method='AR1_REPLAY',
                status='COMPLETE',stop_code='',refit_step=cfg['refit_step'],expected_origin_count=len(v['origins']),
                completed_origin_count=len(v['origins']),origin_count=len(v['origins']),
                strict_breach_count=int(np.count_nonzero(v['peak']>v['capacity']))))
        for name in ('ar1-summary.csv','ar1-annual.csv','ar1-nonoverlap.csv','ar1-paired.csv','ar1-paired-annual.csv','ar1-paired-nonoverlap.csv'):
            raw=self.csv(self.summary) if name=='ar1-summary.csv' else b'opaque,previously_checked\nfixture,only\n'
            self.write(str((self.dest/'public'/name).relative_to(self.root)),raw);public.append(dict(path=name,**identity(raw)))
        self.manifest=dict(version=1,status='AR1_REPLAY_COMPLETE',analysis_status='POST_RESULT_EXPLORATORY',method='AR1_REPLAY',
            all_cells_complete=True,complete_cells=8,failed_cells=0,original_primaries_changed=False,
            original_models_refitted=False,new_parameter_selection=False,
            replication_dir=str(self.attempt.relative_to(self.root)),attempt_id=self.ar_id,
            ar1_spec_sha256=self.plan['ar1_spec_sha256'],ar1_freeze_sha256=self.plan['ar1_freeze_sha256'],
            original_executable_freeze_sha256=self.plan['original_executable_freeze_sha256'],
            archived_selection_sha256=self.plan['original_selection_sha256'],new_selection_sha256='f'*64,
            cell_receipts=receipts,exports=public,private_exports=private,resources=Guard().resources)
        raw=raw_json(self.manifest);self.write(str((self.dest/'public/ar1-replay-manifest.json').relative_to(self.root)),raw)
        self.plan['ar1_manifest_sha256']=hashlib.sha256(raw).hexdigest()
        self.readback=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',ar1_manifest_sha256=self.plan['ar1_manifest_sha256'],
            ar1_spec_sha256=self.plan['ar1_spec_sha256'],ar1_freeze_sha256=self.plan['ar1_freeze_sha256'],cells=8,
            aggregate_rows_independently_checked=192,exact_fraction_fits=24,scalar_recursive_reports=24,
            exact_unique_csv_keys_checked=True,all_consumed_exports_bound_to_manifest=True,new_model_selection=False,
            original_models_refitted=False,source_values_public=False,code_sha256=self.plan['accepted_v2_readback']['code_sha256'])
        raw=raw_json(self.readback);self.write(self.plan['accepted_v2_readback']['path'],raw)
        self.plan['accepted_v2_readback'].update(identity(raw))
        self.write(builder.PLAN_PATH,raw_json(self.plan));self.freeze()

    def freeze(self):
        files={name:hashlib.sha256((self.root/name).read_bytes()).hexdigest() for name in builder.required_freeze_paths(self.root)}
        freeze=dict(version=1,status='FROZEN',created_utc='2000-01-01T00:00:00Z',plan_path=builder.PLAN_PATH,
            plan_sha256=files[builder.PLAN_PATH],files=files)
        raw=raw_json(freeze);self.write(builder.FREEZE_PATH,raw);self.freeze_hash=hashlib.sha256(raw).hexdigest()

    def context(self,helpers,root,replication_dir):
        def forbidden(*args,**kwargs):raise AssertionError('forbidden fit/predict/source/main call')
        helpers.runner.load_sources=forbidden;helpers.runner.main=forbidden
        helpers.auditor.main=forbidden;helpers.kernels.main=forbidden
        helpers.results.load_source=forbidden
        # The original 69-file replica is this fixture's preverified external
        # context. New freeze/artifact snapshots and every diagnostic guard run.
        helpers.runner.verify_inputs=lambda inputs:None
        # This is the sole external preverified-context seam; no I/O guard is mocked.
        return self.inputs,self.execution

    def run(self,diagnostic_id='fresh',guard=Guard):
        return builder.execute(self.root,str(self.attempt.relative_to(self.root)),self.ar_id,
            self.plan['accepted_v2_readback']['path'],diagnostic_id,self.freeze_hash,
            context_provider=self.context,guard_factory=guard)


@unittest.skipUnless(AVAILABLE,'initial RED: module absent')
class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(builder,'execute',None)),'executable diagnostic behavior missing')
        scratch=ROOT/'.scratch/revision-20261022/ar1-diagnostic-tests';scratch.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.tmp.cleanup)
        self.fx=Fixture(Path(self.tmp.name).resolve())

    def test_full_eight_cell_pipeline_retains_all_twelve_rows_and_unchanged_inputs(self):
        f=self.fx;before={p:p.read_bytes() for p in f.root.rglob('*') if p.is_file()}
        result=f.run();dest=f.attempt/'ar1-diagnostics-fresh/public'
        self.assertEqual(result['status'],'AR1_DIAGNOSTICS_VERIFIED');self.assertEqual(result['floor_rows'],8)
        self.assertEqual(result['horizon_rows'],4)
        rows=list(csv.DictReader(io.StringIO((dest/'ar1-floor.csv').read_text())))
        for row in rows:
            key=(row['source'],int(row['horizon']),int(row['window']));v=f.vectors[key]
            binding=[float(c)==float(b) for c,b in zip(v['capacity'],v['floor'])]
            breaches=[float(p)>float(c) for p,c in zip(v['peak'],v['capacity'])]
            self.assertEqual(int(row['floor_binding_count']),sum(binding))
            self.assertEqual(int(row['floor_binding_breach_count']),sum(a and b for a,b in zip(binding,breaches)))
            self.assertEqual(int(row['other_issue_breach_count']),sum(not a and b for a,b in zip(binding,breaches)))
        pairs=list(csv.DictReader(io.StringIO((dest/'ar1-horizon.csv').read_text())))
        for row in pairs:
            s,w=row['source'],int(row['window']);x=f.vectors[s,6,w]['capacity'];y=f.vectors[s,24,w]['capacity']
            d=[max(float(a)-float(b),0.) for a,b in zip(x,y)]
            self.assertEqual(int(row['strict_crossing_count']),sum(a>0 for a in d))
            self.assertAlmostEqual(float(row['mean_positive_crossing']),sum(d)/len(d),delta=1e-13)
        self.assertTrue(all(p.read_bytes()==raw for p,raw in before.items()))
        self.assertFalse(result['source_loaded']);self.assertFalse(result['models_fitted']);self.assertFalse(result['forecasts_repaired'])

    def test_invalid_freeze_stops_before_helper_or_context_execution(self):
        f=self.fx;(f.root/'conditional_features.py').write_text('raise AssertionError("UNVERIFIED EXECUTED")\n')
        with self.assertRaises(builder.DiagnosticError):f.run()
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh').exists())

    def test_missing_closure_entry_cannot_be_accepted(self):
        f=self.fx;path=f.root/builder.FREEZE_PATH;x=json.loads(path.read_bytes());x['files'].pop('study_core.py')
        raw=raw_json(x);path.write_bytes(raw);f.freeze_hash=hashlib.sha256(raw).hexdigest()
        with self.assertRaises(builder.DiagnosticError):f.run()

    def test_resource_contract_cannot_be_redeclared_by_a_new_plan(self):
        f=self.fx;f.plan['resources']['requested_numerical_threads']=4
        f.write(builder.PLAN_PATH,raw_json(f.plan));f.freeze()
        with self.assertRaises(builder.DiagnosticError):f.run()

    def test_snapshot_code_is_executed_from_checked_bytes_and_later_change_stops_output(self):
        f=self.fx;actual=builder.safe_read;hits=[0]
        def change_after_checked_read(root,path,**kwargs):
            raw=actual(root,path,**kwargs)
            p=Path(path);p=p if p.is_absolute() else Path(root)/p
            if p==f.root/'build_conditional_diagnostics.py':
                hits[0]+=1
                if hits[0]==2:p.write_text('raise AssertionError("unverified replacement executed")\n')
            return raw
        with patch.object(builder,'safe_read',side_effect=change_after_checked_read):
            with self.assertRaises(builder.DiagnosticError) as context:f.run()
        self.assertEqual(context.exception.code,'DIAGNOSTIC_INPUT_CHANGED')
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').exists())

    def test_changed_trace_hash_is_failure_with_retained_receipt(self):
        f=self.fx;p=next((f.dest/'private').glob('*-traces.npz'));p.write_bytes(p.read_bytes()+b'altered')
        with self.assertRaises(builder.DiagnosticError):f.run()
        failure=json.loads((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-failure.json').read_bytes())
        self.assertEqual(failure['status'],'STOPPED');self.assertFalse(failure['shortened_segment_published'])
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-floor.csv').exists())

    def test_resealed_missing_origin_or_floor_mismatch_fails_semantic_checks(self):
        f=self.fx;key=next(k for k in f.vectors if k[1]==24)
        f.vectors[key]['floor'][0]=0.;f.reseal()
        with self.assertRaises(builder.DiagnosticError):f.run()
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').exists())

    def test_resealed_origin_permutation_is_rejected(self):
        f=self.fx;key=next(iter(f.vectors));f.vectors[key]['origins'][0]+=1;f.reseal()
        with self.assertRaises(builder.DiagnosticError):f.run()

    def test_nonfinite_or_below_floor_reports_are_rejected_even_with_valid_hashes(self):
        f=self.fx;key=next(iter(f.vectors));original=f.vectors[key]['capacity'].copy()
        for j,value in enumerate((.5,float('nan'),float('inf'))):
            f.vectors[key]['capacity']=original.copy();f.vectors[key]['capacity'][0]=value;f.reseal()
            with self.subTest(value=value),self.assertRaises(builder.DiagnosticError):f.run(diagnostic_id='bad'+str(j))

    def test_no_binding_group_is_null_instead_of_zero_risk(self):
        f=self.fx;s='nyfed_weekly';w=f.plan['sources'][s]['windows'][0]
        f.vectors[s,6,w]['capacity'][:]=2.;f.reseal();f.run()
        rows=list(csv.DictReader(io.StringIO((f.attempt/'ar1-diagnostics-fresh/public/ar1-floor.csv').read_text())))
        row=next(r for r in rows if r['source']==s and r['horizon']=='6' and r['window']==str(w))
        self.assertEqual(row['floor_binding_count'],'0');self.assertEqual(row['floor_binding_breach_rate'],'')
        self.assertEqual(row['floor_binding_undefined_reason'],'NO_FLOOR_BINDING_ISSUES')

    def test_mixed_floor_counts_near_equality_and_empty_other_group(self):
        f=self.fx;np=f.np;s='nyfed_weekly';w=f.plan['sources'][s]['windows'][0]
        v=f.vectors[s,6,w];v['capacity'][:4]=[1.,np.nextafter(1.,2.),1.,2.];v['peak'][:4]=[1.,2.,2.,2.]
        f.reseal();f.run();rows=list(csv.DictReader(io.StringIO((f.attempt/'ar1-diagnostics-fresh/public/ar1-floor.csv').read_text())))
        row=next(r for r in rows if r['source']==s and r['horizon']=='6' and r['window']==str(w))
        expected=sum(float(c)==float(b) for c,b in zip(v['capacity'],v['floor']))
        self.assertEqual(int(row['floor_binding_count']),expected)
        all_bound=next(r for r in rows if r['source']==s and r['window']==str(f.plan['sources'][s]['windows'][1]))
        self.assertEqual(all_bound['other_issue_breach_rate'],'')
        self.assertEqual(all_bound['other_issue_undefined_reason'],'NO_OTHER_ISSUES')

    def test_impossible_target_fails_but_forecast_crossings_are_retained(self):
        f=self.fx;s,_,w=next(iter(f.vectors));f.vectors[s,24,w]['peak'][0]=0.5;f.reseal()
        with self.assertRaises(builder.DiagnosticError):f.run()

    def test_summary_duplicate_replacing_an_omission_is_rejected(self):
        f=self.fx;rows=copy.deepcopy(f.summary);rows[1]=rows[0].copy();name='ar1-summary.csv';raw=f.csv(rows)
        (f.dest/'public'/name).write_bytes(raw)
        entry=next(e for e in f.manifest['exports'] if e['path']==name);entry.update(identity(raw))
        # Update the declared manifest/readback/plan together: hash agreement is not enough.
        manifest_raw=raw_json(f.manifest);(f.dest/'public/ar1-replay-manifest.json').write_bytes(manifest_raw)
        f.plan['ar1_manifest_sha256']=hashlib.sha256(manifest_raw).hexdigest()
        f.readback['ar1_manifest_sha256']=f.plan['ar1_manifest_sha256'];raw=raw_json(f.readback)
        f.write(f.plan['accepted_v2_readback']['path'],raw);f.plan['accepted_v2_readback'].update(identity(raw))
        f.write(builder.PLAN_PATH,raw_json(f.plan));f.freeze()
        with self.assertRaises(builder.DiagnosticError):f.run()

    def test_unique_output_refuses_overwrite(self):
        f=self.fx;f.run();old=(f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').read_bytes()
        with self.assertRaises(builder.DiagnosticError):f.run()
        self.assertEqual((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').read_bytes(),old)

    def test_resource_stop_preserves_failure_without_complete_csvs(self):
        class Cancel(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_cell_checked':
                    error=RuntimeError('private message must not be exported');error.code='RESOURCE_WALL';raise error
        f=self.fx
        with self.assertRaises(builder.DiagnosticError):f.run(guard=Cancel)
        raw=(f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-failure.json').read_bytes()
        self.assertNotIn(b'private message',raw);self.assertIn(b'RESOURCE_WALL',raw)
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-horizon.csv').exists())

    def test_failure_after_export_preserves_unverified_csvs_only_privately(self):
        class Cancel(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_final':
                    e=RuntimeError('cancel');e.code='RESOURCE_WALL';raise e
        f=self.fx
        with self.assertRaises(builder.DiagnosticError):f.run(guard=Cancel)
        out=f.attempt/'ar1-diagnostics-fresh'
        self.assertFalse((out/'public/ar1-floor.csv').exists())
        self.assertTrue((out/'private/unverified-ar1-floor.csv').is_file())
        self.assertTrue((out/'private/unverified-ar1-horizon.csv').is_file())

    def test_last_checkpoint_input_change_prevents_verified_audit(self):
        f=self.fx;trace=next((f.dest/'private').glob('*-traces.npz'))
        class Change(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_final':trace.write_bytes(trace.read_bytes()+b'changed')
        with self.assertRaises(builder.DiagnosticError):f.run(guard=Change)
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').exists())

    def test_last_checkpoint_export_change_prevents_verified_audit(self):
        f=self.fx
        class Change(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='ar1_diagnostic_final':
                    p=f.attempt/'ar1-diagnostics-fresh/public/ar1-floor.csv';p.write_bytes(p.read_bytes()+b'changed')
        with self.assertRaises(builder.DiagnosticError):f.run(guard=Change)
        self.assertFalse((f.attempt/'ar1-diagnostics-fresh/public/ar1-diagnostics-audit.json').exists())

    def assert_partial_write_quarantined(self,name):
        f=self.fx;original=Path.open
        target=f.attempt/'ar1-diagnostics-fresh/public'/name
        class PartialWriter:
            def __init__(self,stream):self.stream=stream
            def __enter__(self):self.stream.__enter__();return self
            def __exit__(self,*args):return self.stream.__exit__(*args)
            def write(self,raw):
                self.stream.write(raw[:17])
                raise OSError('synthetic partial write; no real disk failure')
        def open_with_failure(path,*args,**kwargs):
            stream=original(path,*args,**kwargs)
            return PartialWriter(stream) if path==target and args==('xb',) else stream
        with patch.object(Path,'open',new=open_with_failure):
            with self.assertRaises(builder.DiagnosticError):f.run()
        out=f.attempt/'ar1-diagnostics-fresh'
        self.assertFalse(target.exists(),'partially written output must not remain public')
        self.assertEqual(len((out/'private'/('unverified-'+name)).read_bytes()),17)
        failure=json.loads((out/'public/ar1-diagnostics-failure.json').read_bytes())
        self.assertEqual(failure['status'],'STOPPED');self.assertFalse(failure['shortened_segment_published'])

    def test_partial_csv_write_is_preserved_only_privately(self):
        self.assert_partial_write_quarantined('ar1-floor.csv')

    def test_partial_success_audit_write_is_preserved_only_privately(self):
        self.assert_partial_write_quarantined('ar1-diagnostics-audit.json')


class EntryTests(unittest.TestCase):
    def test_new_explicit_entry_exists(self):
        self.assertTrue(AVAILABLE,'AR diagnostic wrapper is missing')

    @unittest.skipUnless(AVAILABLE,'initial RED: module absent')
    def test_import_help_needs_no_numpy_or_cache_access(self):
        code=("import runpy,sys; sys.argv=[sys.argv[1],'--help']\n"
              "try: runpy.run_path(sys.argv[0],run_name='__main__')\n"
              "except SystemExit as e: assert e.code==0\n"
              "assert 'numpy' not in sys.modules and 'run_study' not in sys.modules\n")
        done=subprocess.run([sys.executable,'-B','-c',code,str(ROOT/'build_ar1_diagnostics.py')],
            capture_output=True,text=True)
        self.assertEqual(done.returncode,0,done.stderr)
        for flag in ('--freeze','--replication-dir','--ar1-attempt-id','--readback','--diagnostic-id'):
            self.assertIn(flag,done.stdout)


if __name__=='__main__':unittest.main()
