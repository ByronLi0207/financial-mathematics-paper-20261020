"""Synthetic closed-family coverage inputs; never load financial payloads."""
import copy
import csv
from fractions import Fraction
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

from test_reproduce_ar1_diagnostics import Fixture as BaseFixture
from test_build_ar1_diagnostics import Guard,raw_json,identity
import reproduce_conditional as rep

ROOT=Path(__file__).resolve().parent

AVAILABLE=importlib.util.find_spec('run_coverage_evalues') is not None
if AVAILABLE:import run_coverage_evalues as runner


class EntryTests(unittest.TestCase):
    def test_closed_coverage_entry_exists(self):
        self.assertTrue(AVAILABLE,'closed coverage runner is missing')

    @unittest.skipUnless(AVAILABLE,'initial RED: module absent')
    def test_help_and_unrequested_execution_never_import_numpy_or_read_inputs(self):
        for args in (['--help'],['--replication-dir','MISSING','--ar1-attempt-id','ar','--readback','MISSING',
            '--readback-sha256','0'*64,'--attempt-id','fresh','--freeze','0'*64]):
            code=("import runpy,sys;sys.argv=[sys.argv[1]]+sys.argv[2:]\n"
                  "try:runpy.run_path(sys.argv[0],run_name='__main__')\n"
                  "except SystemExit as e:assert e.code==0\n"
                  "assert 'numpy' not in sys.modules and 'coverage_evalues' not in sys.modules\n")
            done=subprocess.run([sys.executable,'-B','-c',code,str(ROOT/'run_coverage_evalues.py'),*args],capture_output=True,text=True)
            self.assertEqual(done.returncode,0,done.stderr)
            self.assertIn('--execute' if args==['--help'] else 'NOT_EXECUTED',done.stdout)


@unittest.skipUnless(AVAILABLE,'initial RED: missing entry')
class SerializationTests(unittest.TestCase):
    def test_adjusted_reference_threshold_uses_exact_greater_or_equal(self):
        import coverage_evalues as kernel
        phases=tuple(types.SimpleNamespace(phase=r,n=1,k=1,value=Fraction(1120)) for r in range(2))
        value=types.SimpleNamespace(horizon=1,n=2,k=2,first_origin=10,last_origin=11,phases=phases,value=Fraction(1120))
        row,parts=runner.serialize_report(dict(horizon=1),value,kernel)
        self.assertTrue(row['adjusted_reference_threshold_crossed'])
        self.assertTrue(all(r['cell_adjusted_reference_threshold_crossed'] for r in parts))
        self.assertNotIn('adjusted_reference_threshold_crossed',parts[0])

    def test_empty_phases_keep_fixed_weight_and_value_one(self):
        import coverage_evalues as kernel
        result=kernel.phase_mixture([100],[False],24)
        row,parts=runner.serialize_report(dict(horizon=24),result,kernel)
        self.assertEqual(len(parts),25);self.assertEqual([r['phase'] for r in parts],list(range(25)))
        self.assertEqual(Fraction(int(row['evalue_numerator_hex'],16),int(row['evalue_denominator_hex'],16)),Fraction(49,50))
        self.assertTrue(all(r['n']==0 and r['evalue_numerator_hex']=='0x1' and r['evalue_denominator_hex']=='0x1' for r in parts[1:]))

    def test_kernel_horizon_cannot_be_serialized_under_a_different_report_horizon(self):
        import coverage_evalues as kernel
        result=kernel.phase_mixture([100],[False],6)
        with self.assertRaises(runner.CoverageError):runner.serialize_report(dict(horizon=24),result,kernel)

    def test_declared_adaptive_phase_weights_are_rejected_before_calculation(self):
        spec=json.loads((ROOT/'protocol/revision-20261022/coverage-evalue-spec.json').read_bytes())
        sources=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_bytes())
        spec['phase_weights']='choose weights using future breaches'
        with self.assertRaises(runner.CoverageError):runner.validate_spec(spec,sources)


class Fixture:
    def __init__(self,root):
        self.root=Path(root);self.base=BaseFixture(root);f=self.base.base;np=f.np
        self.inputs=f.inputs;self.inputs.update(cells=[],queue=[],selected={},exported_receipts={})
        families=('QR','KNN','SCALED_KNN');fields=('origins','peak','floor','refit_indices','capacity','pinball')
        for phase in ('evaluation','references'):
            for source,cfg in f.spec['sources'].items():
                for h in (6,24):
                    for w in cfg['windows']:
                        for family in (families if phase=='evaluation' else (None,)):
                            cell=(phase,source,h,w,family);self.inputs['cells'].append(cell)
                            parameter=(.01 if family=='QR' else cfg['knn_candidates'][str(w)][0]) if family else None
                            if family:self.inputs['selected'][source,h,w,family]=dict(status='SELECTED',parameter=parameter)
                            prefixes=('rolling','frozen','one_state') if cfg['one_state_reference_neighbors'][str(w)] else ('rolling','frozen')
                            methods=[family] if family else [p+'_'+m for p in prefixes for m in ('F','S','K')]
                            vectors=f.vectors[source,h,w];arrays={};first=cfg['evaluation_origin_first'];last=cfg['evaluation_origin_last']
                            for method in methods:
                                data={k:v.copy() for k,v in vectors.items()}
                                data['capacity']=data['peak'].copy();data['pinball']=np.zeros(last-first+1)
                                if not family and not method.startswith('frozen_'):data['refit_indices']=data['origins'].copy()
                                arrays.update({method+'_'+k:v for k,v in data.items()})
                            out=io.BytesIO();np.savez_compressed(out,**arrays);raw=out.getvalue()
                            path=rep.worker_directory(f.attempt,cell)/'public/manifest.json'
                            f.write(str((path.parent.parent/'private/numeric-traces.npz').relative_to(self.root)),raw)
                            fits=[]
                            if family:
                                for r in range(first,last+1,cfg['refit_step']):
                                    d=dict(method=family,parameter=parameter,refit_index=r,training_first_origin=r-h-w+1,
                                        training_last_origin=r-h,training_count=w,latest_label_end=r)
                                    if family=='QR':
                                        a,b=float(.95).as_integer_ratio();g=2**40
                                        d.update(primal_objective=0.,dual_objective=0.,duality_gap=0.,primal_residual=0.,dual_residual=0.,
                                            primal_tolerance=1e-6,dual_tolerance=1e-6,gap_tolerance=1e-6,iterations=1,
                                            dual_integer_lower=-((b-a)*g//b),dual_integer_upper=a*g//b,dual_integer_sum=0,dual_grid_denominator=g)
                                    fits.append(d)
                            receipt=dict(version=1,phase=phase,source=source,horizon=h,window=w,family=family,status='COMPLETE',stop_code=None,
                                executable_freeze_sha256=f.plan['original_executable_freeze_sha256'],selection_freeze_sha256=f.inputs['selection_hash'] if family else None,
                                source_identity={k:cfg[k] for k in ('sha256','bytes','record_count','native_unit')},resources=Guard().resources,
                                result=dict(status='COMPLETE',failure=None,candidate_rows=[],native_unit=cfg['native_unit'],
                                    selection=dict(status='SELECTED',parameter=parameter) if family else None,
                                    origin_identity=rep.origin_identity(first,last),summary_rows=[dict(method=m,parameter=parameter) for m in methods],
                                    fit_diagnostics=fits),artifacts=[dict(area='private',name='numeric-traces.npz',**identity(raw))])
                            receipt_raw=raw_json(receipt);f.write(str(path.relative_to(self.root)),receipt_raw)
                            self.inputs['queue'].append(dict(zip(('phase','source','horizon','window','family'),cell))|
                                dict(exit_code=0,timed_out=False,status='COMPLETE',stop_code=None,
                                    receipt_path=str(path.relative_to(self.root)),receipt_sha256=rep.sha(receipt_raw)))
                            name=f'evaluation-{source}-h{h}-w{w}-{family}.json' if family else f'references-{source}-h{h}-w{w}.json'
                            self.inputs['exported_receipts'][name]=receipt_raw
        self.populate_ar_fits()
        for name in runner.NEW_FILES:f.write(name,(ROOT/name).read_bytes())
        self.freeze()

    def populate_ar_fits(self):
        base=self.base;f=base.base;total=0
        for cell in f.cells:
            s,h,w=(cell[k] for k in ('source','horizon','window'));cfg=f.spec['sources'][s];stem=f'{s}-h{h}-w{w}'
            fits=[dict(refit_index=r,first_origin=r-h-w+1,last_origin=r-h,horizon=h,window=w,
                rank=(19*(w+1)+19)//20,transition_count=w+h-1,phi=0.,c=0.,scale=1.,scaled_mean_residual=0.,
                scaled_regressor_residual=0.,normal_tolerance=1e-10,scaled_x_mean=0.,scaled_y_mean=0.,scaled_x_variance=1.)
                for r in range(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,cfg['refit_step'])]
            total+=len(fits);entry=next(e for e in base.manifest['private_exports'] if e['path']==stem+'-fits.json')
            raw=raw_json(dict(version=1,cell=cell,status='COMPLETE',failure=None,fit_records=fits))
            (base.dest/'private'/entry['path']).write_bytes(raw);entry.update(identity(raw))
            e=next(e for e in base.manifest['exports'] if e['path']==stem+'-receipt.json')
            path=base.dest/'public'/e['path'];receipt=json.loads(path.read_bytes())
            receipt['private_artifacts']=[x for x in base.manifest['private_exports'] if x['path'] in (stem+'-fits.json',stem+'-traces.npz')]
            raw=raw_json(receipt);path.write_bytes(raw);e.update(identity(raw))
            for record in base.manifest['cell_receipts']:
                if record['cell']==cell:record['receipt']=e
        base.readback['fit_records_metadata_checked']=total;base.reseal()

    def freeze(self):
        f=self.base.base;names=runner.required_freeze_paths(self.root)
        files={n:rep.sha((self.root/n).read_bytes()) for n in names}
        value=dict(version=1,status='FROZEN',created_utc='2000-01-01T00:00:00Z',base_freeze_path=runner.BASE_FREEZE,
            base_freeze_sha256=files[runner.BASE_FREEZE],spec_path=runner.SPEC_PATH,spec_sha256=files[runner.SPEC_PATH],files=files)
        raw=raw_json(value);f.write(runner.FREEZE_PATH,raw);self.freeze_hash=rep.sha(raw)

    def run(self,attempt_id='coverage',guard=Guard,context=None,execute=True):
        # Real prepare_replica creates a fresh per-execution snapshot ledger.
        self.inputs['snapshots']={}
        return runner.execute(self.root,str(self.base.base.attempt.relative_to(self.root)),self.base.ar_id,
            self.base.readback_path,self.base.readback_hash,attempt_id,self.freeze_hash,execute=execute,
            context_provider=self.base.base.context if context is None else context,guard_factory=guard)

    @property
    def output(self):return self.base.base.attempt/'coverage-evalues-coverage'

    def change_phase(self,index,mutator):
        queued=self.inputs['queue'][index];path=self.root/queued['receipt_path'];receipt=json.loads(path.read_bytes())
        trace=path.parent.parent/'private/numeric-traces.npz';np=self.base.base.np
        with np.load(io.BytesIO(trace.read_bytes()),allow_pickle=False) as archive:arrays={k:archive[k].copy() for k in archive.files}
        mutator(receipt,arrays);out=io.BytesIO();np.savez_compressed(out,**arrays);raw=out.getvalue();trace.write_bytes(raw)
        receipt['artifacts']=[dict(area='private',name='numeric-traces.npz',**identity(raw))]
        raw=raw_json(receipt);path.write_bytes(raw);queued['receipt_sha256']=rep.sha(raw)
        phase,s,h,w,f=self.inputs['cells'][index]
        name=f'evaluation-{s}-h{h}-w{w}-{f}.json' if f else f'references-{s}-h{h}-w{w}.json'
        self.inputs['exported_receipts'][name]=raw


@unittest.skipUnless(AVAILABLE,'initial RED: missing entry')
class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(runner,'execute',None)),'closed-family execution is missing')
        parent=ROOT/'.scratch/revision-20261022/coverage-runner-tests';parent.mkdir(parents=True,exist_ok=True)
        temp=tempfile.TemporaryDirectory(dir=parent);self.addCleanup(temp.cleanup);self.f=Fixture(Path(temp.name).resolve())

    def test_full_56_closed_reports_and_896_phases_use_exact_rationals_and_strict_hits(self):
        f=self.f;result=f.run();self.assertEqual(result['status'],'COVERAGE_EVALUE_COMPUTATION_VERIFIED')
        self.assertEqual((result['summary_rows'],result['phase_rows']),(56,896))
        p=f.output/'public';rows=list(csv.DictReader(io.StringIO((p/'coverage-evalue-summary.csv').read_text())))
        self.assertEqual(len({(r['source'],r['horizon'],r['window'],r['method']) for r in rows}),56)
        r=next(r for r in rows if (r['source'],r['horizon'],r['window'],r['method'])==('fx_hourly','6','720','QR'))
        self.assertEqual((r['n'],r['k']),('6625','0'))
        value=Fraction(int(r['evalue_numerator_hex'],16),int(r['evalue_denominator_hex'],16))
        self.assertEqual(value,(3*Fraction(1,948)+4*Fraction(1,947))/7)
        phase_rows=list(csv.DictReader(io.StringIO((p/'coverage-evalue-phases.csv').read_text())))
        self.assertEqual(len(phase_rows),896);self.assertTrue(result['post_result_exploratory'])
        self.assertFalse(result['coverage_guarantee_established']);self.assertFalse(result['full_filtration_anytime_claim'])

    def test_without_execute_never_bootstraps_or_loads_any_input(self):
        with patch.object(runner,'preflight',side_effect=AssertionError('unrequested load')):
            result=self.f.run(execute=False)
        self.assertEqual(result['status'],'NOT_EXECUTED');self.assertFalse(self.f.output.exists())

    def test_changed_frozen_code_is_rejected_before_context(self):
        f=self.f;(f.root/'coverage_evalues.py').write_text('raise AssertionError("unverified")\n')
        def forbidden(*args):raise AssertionError('context before code identity')
        with self.assertRaises(runner.CoverageError):f.run(context=forbidden)
        self.assertFalse(f.output.exists())

    def test_missing_semantic_cell_is_not_replaced_or_M_reduced(self):
        f=self.f;f.inputs['queue'].pop();f.inputs['cells'].pop()
        with self.assertRaises(runner.CoverageError):f.run()
        self.assertFalse((f.output/'public/coverage-evalue-manifest.json').exists())

    def test_resealed_origin_nonfinite_refit_and_target_mismatches_fail(self):
        f=self.f
        queued=f.inputs['queue'][0];path=f.root/queued['receipt_path'];trace=path.parent.parent/'private/numeric-traces.npz'
        saved_receipt=path.read_bytes();saved_trace=trace.read_bytes();saved_hash=queued['receipt_sha256']
        exported=dict(f.inputs['exported_receipts'])
        mutations=(lambda r,a:a['QR_origins'].__setitem__(0,a['QR_origins'][0]+1),
            lambda r,a:a['QR_capacity'].__setitem__(0,float('nan')),
            lambda r,a:a['QR_refit_indices'].__setitem__(0,a['QR_refit_indices'][0]+1),
            lambda r,a:a['QR_peak'].__setitem__(0,a['QR_peak'][0]+.25))
        for j,change in enumerate(mutations):
            path.write_bytes(saved_receipt);trace.write_bytes(saved_trace);queued['receipt_sha256']=saved_hash
            f.inputs['exported_receipts']=dict(exported)
            f.change_phase(0,change)
            with self.subTest(case=j),self.assertRaises(runner.CoverageError) as caught:f.run(attempt_id='bad'+str(j))
            self.assertEqual(caught.exception.code,('COVERAGE_TRACE_ALIGNMENT','COVERAGE_TRACE_FINITE_FLOOR',
                'COVERAGE_TRACE_ALIGNMENT','COVERAGE_SHARED_TARGET_FLOOR')[j])

    def test_future_label_in_fit_metadata_fails_without_new_forecast(self):
        f=self.f
        def change(receipt,arrays):receipt['result']['fit_diagnostics'][0]['latest_label_end']+=1
        f.change_phase(0,change)
        with self.assertRaises(runner.CoverageError):f.run()

    def test_wrong_queued_hash_and_wrong_selected_parameter_fail(self):
        f=self.f;f.inputs['queue'][0]['receipt_sha256']='0'*64
        with self.assertRaises(runner.CoverageError) as caught:f.run(attempt_id='wronghash')
        self.assertEqual(caught.exception.code,'COVERAGE_RECEIPT_HASH')
        path=f.root/f.inputs['queue'][0]['receipt_path'];f.inputs['queue'][0]['receipt_sha256']=rep.sha(path.read_bytes())
        def change(receipt,arrays):receipt['result']['selection']['parameter']=.1
        f.change_phase(0,change)
        with self.assertRaises(runner.CoverageError) as caught:f.run(attempt_id='wrongparameter')
        self.assertEqual(caught.exception.code,'COVERAGE_SELECTED_PARAMETER')

    def test_altered_raw_npz_hash_is_rejected_before_payload_decoding(self):
        f=self.f;path=f.root/f.inputs['queue'][0]['receipt_path'];trace=path.parent.parent/'private/numeric-traces.npz'
        trace.write_bytes(trace.read_bytes()+b'altered')
        with self.assertRaises(runner.CoverageError) as caught:f.run()
        self.assertEqual(caught.exception.code,'COVERAGE_TRACE_ARTIFACT')

    def test_v2_for_a_different_manifest_cannot_borrow_this_attempt(self):
        f=self.f;path=f.root/f.base.readback_path;v=json.loads(path.read_bytes());v['ar1_manifest_sha256']='0'*64
        raw=raw_json(v);path.write_bytes(raw);f.base.readback_hash=rep.sha(raw)
        with self.assertRaises(runner.CoverageError) as caught:f.run()
        self.assertEqual(caught.exception.code,'COVERAGE_FRESH_MANIFEST_HASH')

    def test_changed_input_at_final_checkpoint_stops_all_public_results(self):
        f=self.f;target=f.root/f.inputs['queue'][0]['receipt_path']
        class Change(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='coverage_evalue_final':target.write_bytes(target.read_bytes()+b'changed')
        with self.assertRaises(runner.CoverageError):f.run(guard=Change)
        self.assertFalse((f.output/'public/coverage-evalue-summary.csv').exists())
        self.assertTrue((f.output/'private/unverified-coverage-evalue-summary.csv').exists())

    def test_resource_stop_has_sanitized_whole_family_failure(self):
        class Cancel(Guard):
            def __call__(self,**kwargs):
                if kwargs.get('stage')=='coverage_evalue_cell':
                    e=RuntimeError('private path/message');e.code='RESOURCE_WALL';raise e
        f=self.f
        with self.assertRaises(runner.CoverageError):f.run(guard=Cancel)
        raw=(f.output/'public/coverage-evalue-failure.json').read_bytes()
        self.assertIn(b'RESOURCE_WALL',raw);self.assertNotIn(b'private path',raw)
        self.assertFalse((f.output/'public/coverage-evalue-manifest.json').exists())

    def test_output_attempt_never_overwrites_a_verified_family(self):
        f=self.f;f.run();p=f.output/'public/coverage-evalue-manifest.json';raw=p.read_bytes()
        with self.assertRaises(runner.CoverageError):f.run()
        self.assertEqual(p.read_bytes(),raw)

    def test_partial_table_or_final_manifest_writes_are_kept_only_privately(self):
        f=self.f;original=Path.open
        for j,name in enumerate(('coverage-evalue-summary.csv','coverage-evalue-manifest.json')):
            target=f.base.base.attempt/('coverage-evalues-write'+str(j))/'public'/name
            class Partial:
                def __init__(self,stream):self.stream=stream
                def __enter__(self):self.stream.__enter__();return self
                def __exit__(self,*args):return self.stream.__exit__(*args)
                def write(self,raw):self.stream.write(raw[:17]);raise OSError('synthetic partial write')
            def fail(path,*args,**kwargs):
                stream=original(path,*args,**kwargs)
                return Partial(stream) if path==target and args==('xb',) else stream
            with self.subTest(name=name),patch.object(Path,'open',new=fail):
                with self.assertRaises(runner.CoverageError):f.run(attempt_id='write'+str(j))
            self.assertFalse(target.exists())
            self.assertEqual(len((target.parent.parent/'private'/('unverified-'+name)).read_bytes()),17)


if __name__=='__main__':unittest.main()
