"""Synthetic-only tests for diagnostics after an audited frozen replication."""
import copy
import csv
import importlib.util
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import types
import unittest
import zipfile

import reproduce_conditional as rep
import reconcile_conditional_replication as adapter

for _name in rep.THREAD_NAMES:
    __import__('os').environ[_name] = '1'
import numpy as np
from conditional_study import score_predictions, summarize_scores


MODULE_AVAILABLE = importlib.util.find_spec('reproduce_conditional_diagnostics') is not None
if MODULE_AVAILABLE:
    import reproduce_conditional_diagnostics as diagnostics


class EntryPointContract(unittest.TestCase):
    def test_explicit_diagnostic_replication_module_exists(self):
        self.assertTrue(MODULE_AVAILABLE, 'diagnostic reproduction entry point is absent')

    def test_help_needs_no_numeric_import_or_source_access(self):
        if not MODULE_AVAILABLE:
            self.skipTest('initial RED: module absent')
        script = Path(__file__).resolve().parent / 'reproduce_conditional_diagnostics.py'
        code = ("import runpy,sys; sys.argv=[sys.argv[1],'--help']\n"
                "try: runpy.run_path(sys.argv[0],run_name='__main__')\n"
                "except SystemExit as e: assert e.code==0\n"
                "assert 'numpy' not in sys.modules and 'run_study' not in sys.modules\n")
        completed = subprocess.run([sys.executable, '-B', '-c', code, str(script)],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)


ROOT = Path(__file__).resolve().parent
RESULTS = rep.RESULTS
TABLE_COUNTS = dict(zip(('evaluation-summary.csv', 'evaluation-annual.csv',
    'evaluation-nonoverlap.csv', 'paired-comparisons.csv', 'paired-annual.csv',
    'paired-nonoverlap.csv'), (90, 372, 90, 98, 388, 98)))


def identity(raw):
    return dict(bytes=len(raw), sha256=rep.sha(raw))


def json_raw(value):
    return rep.json_bytes(value)


def parse_csv(raw):
    return list(csv.DictReader(io.StringIO(raw.decode(), newline='')))


def resources():
    return dict(elapsed_seconds=.25, peak_rss_bytes=100000,
        maximum_observed_os_threads=1, thread_snapshot_count=2, thread_probe_status='PASS')


def loaded_original_helpers():
    path = ROOT / RESULTS / 'post-result-builder-v01.py'
    module = types.ModuleType('_synthetic_real_diagnostic_helpers')
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


class SyntheticFixture:
    """Actual 24/32/90/45 inventory, four invented issues, no raw source files."""
    def __init__(self, root, *, shift=0., trace_mutator=None, reconcile_metrics=False):
        self.root = root
        self.attempt = root / '.scratch/revision-20261022/replication-synthetic-01'
        self.attempt.mkdir(parents=True)
        self.spec = dict(horizons=[6, 24], families=['QR', 'KNN', 'SCALED_KNN'],
            qr_penalties=[.001, .01, .1], sources={})
        for source, windows, first, states in (
            ('fx_hourly', [720, 2880], 10000, {'720': 360, '2880': None}),
            ('nyfed_weekly', [52, 260], 1000, {'52': 40, '260': 80})):
            self.spec['sources'][source] = dict(input_relative_path='.scratch/NEVER_READ-'+source,
                sha256=rep.sha(source.encode()), bytes=17, record_count=first+100,
                native_unit='USD' if source=='fx_hourly' else 'USD millions',
                windows=windows, evaluation_origin_first=first, evaluation_origin_last=first+3,
                validation_origin_first=first-100, validation_origin_last=first-99,
                refit_step=2, one_state_reference_neighbors=states,
                knn_candidates={str(w): [20, 40, w] for w in windows})
        self.write('synthetic-model.py', b'# generated contract fixture, never financial data\n')
        self.write(rep.SPEC_PATH, json_raw(self.spec))
        code_files = ('synthetic-model.py', rep.SPEC_PATH)
        freeze = dict(version=1, status='FROZEN', created_utc='2026-01-01T00:00:00Z',
            files={p: rep.sha((root/p).read_bytes()) for p in code_files},
            sources={s:{k:c[k] for k in ('sha256','bytes')} for s,c in self.spec['sources'].items()})
        self.freeze = rep.sha(json_raw(freeze)); self.write(rep.FREEZE_PATH, json_raw(freeze))
        self.archived_files = {}; archived_cells=[]; new_cells=[]; validation=[]
        for key in rep.inventory(self.spec):
            s,h,w,f = key; cfg=self.spec['sources'][s]
            candidates=self.spec['qr_penalties'] if f=='QR' else cfg['knn_candidates'][str(w)]
            receipt=dict(version=1,phase='validation',source=s,horizon=h,window=w,family=f,
                status='COMPLETE',stop_code=None,executable_freeze_sha256=self.freeze,
                selection_freeze_sha256=None,source_identity={k:cfg[k] for k in ('sha256','bytes','record_count','native_unit')},
                resources=resources(),result=dict(origin_identity=rep.origin_identity(cfg['validation_origin_first'],cfg['validation_origin_last']),
                    candidate_rows=[dict(parameter=p,status='COMPLETE',origin_count=2,mean_pinball=1.,failure=None) for p in candidates]))
            raw=json_raw(receipt); public=rep.public_validation_name(key); self.archive(public,raw)
            path=rep.worker_directory(self.attempt,('validation',*key))/'public/manifest.json'
            self.write(path,raw)
            base=dict(source=s,horizon=h,window=w,family=f,status='SELECTED',parameter=candidates[-1])
            archived_cells.append(base|dict(validation_receipts=[dict(path=rep.historical_validation_name(key),sha256=rep.sha(raw))]))
            new_cells.append(base|dict(validation_receipts=[dict(path=str(path.relative_to(root)),sha256=rep.sha(raw))]))
            validation.append(dict(phase='validation',source=s,horizon=h,window=w,family=f,
                exit_code=0,timed_out=False,status='COMPLETE',stop_code=None,
                receipt_path=str(path.relative_to(root)),receipt_sha256=rep.sha(raw)))
        common=dict(version=1,status='FROZEN',created_utc='2026-01-01T00:01:00Z',executable_freeze_sha256=self.freeze)
        old_selection=common|dict(cells=archived_cells); raw=json_raw(old_selection)
        self.selection_old=rep.sha(raw); self.write(rep.SELECTION_PATH,raw)
        self.selection=common|dict(cells=new_cells); raw=json_raw(self.selection)
        self.selection_hash=rep.sha(raw); self.write(self.attempt/'selection-freeze.json',raw)
        self.write(self.attempt/'validation-queue.json',json_raw(dict(version=1,cells=validation)))
        old=self.generated(0.,None); current=self.generated(shift,trace_mutator,reconcile_metrics=reconcile_metrics)
        summary_old, old_floor, old_horizon=old['summary'],old['floor'],old['horizon']
        audit_output=self.attempt/'numerical-audit/public'
        self.queue=current['queue']; self.write(self.attempt/'evaluation-queue.json',json_raw(dict(version=1,cells=self.queue)))
        new_tables={}; old_tables={}
        for name,count in TABLE_COUNTS.items():
            old_tables[name]=adapter.csv_bytes(summary_old if name=='evaluation-summary.csv' else [dict(synthetic=i) for i in range(count)])
            new_tables[name]=adapter.csv_bytes(current['summary']) if name=='evaluation-summary.csv' else old_tables[name]
            self.archive(RESULTS+'/'+name,old_tables[name]);self.write(audit_output/name,new_tables[name])
        receipts=[]; exports=[dict(path=n,**identity(raw)) for n,raw in new_tables.items()]
        for name,raw in current['receipts'].items():
            self.archive(RESULTS+'/'+name,b'{}\n')
            self.write(audit_output/name,raw)
            receipts.append(dict(public_file=name,**identity(raw)))
            exports.append(dict(path=name,**identity(raw)))
        # The production archive contains 69 entries; this fixture has the same
        # count and actual validation selection evidence, not a mocked verifier.
        for i in range(6):self.archive(RESULTS+'/synthetic-archive-'+str(i)+'.txt',b'synthetic\n')
        helper_path=RESULTS+'/audit-builder-v01.py'
        self.archive(helper_path,(ROOT/helper_path).read_bytes())
        self.archive_contract=rep.ArchiveContract(self.freeze,self.selection_old,code_files,self.archived_files)
        self.comparison=dict(version=1,status='NUMERICAL_AUDIT_VERIFIED',created_utc='2026-01-01T00:02:00Z',
            archived_selection_sha256=self.selection_old,new_selection_sha256=self.selection_hash,
            selection_status_parameter_matrix_identical=True,
            queue_sha256=rep.sha((self.attempt/'evaluation-queue.json').read_bytes()),
            tables={n:adapter.compare_csv(new_tables[n],old_tables[n]) for n in TABLE_COUNTS},
            exports=exports,receipts=receipts,audit_resources=resources(),runtime=dict(platform_system='Darwin'),
            source_identities={s:{k:c[k] for k in ('sha256','bytes','record_count','native_unit')} for s,c in self.spec['sources'].items()},
            summary_rows=90,annual_rows=372,paired_rows=98,paired_annual_rows=388)
        self.comparison['exact_csv_byte_agreement']=all(t['byte_identical'] for t in self.comparison['tables'].values())
        self.comparison['exact_csv_scalar_agreement']=all(t['exact_scalar_agreement'] for t in self.comparison['tables'].values())
        self.comparison_path=audit_output/'reproduction-comparison.json';self.write(self.comparison_path,json_raw(self.comparison))
        self.controller=dict(version=1,status='REPLICATION_AUDITED',stop_code=None,
            executable_freeze_sha256=self.freeze,archived_selection_sha256=self.selection_old,
            attempt_path=str(self.attempt.relative_to(root)),accuracy_recomputed=True,selection_agrees_with_archive=True,
            completed_validation_cells=24,completed_evaluation_reference_cells=32,
            validation_jobs_retained=24,evaluation_reference_jobs_retained=32,
            queue_path=str((self.attempt/'evaluation-queue.json').relative_to(root)),
            selection_path=str((self.attempt/'selection-freeze.json').relative_to(root)),selection_sha256=self.selection_hash,
            audit=dict(status='NUMERICAL_AUDIT_VERIFIED',comparison_path=str(self.comparison_path.relative_to(root)),
                exact_csv_byte_agreement=self.comparison['exact_csv_byte_agreement'],
                exact_csv_scalar_agreement=self.comparison['exact_csv_scalar_agreement']))
        self.write_controller()
        self.diagnostic_files={}
        for name in ('post-result-builder-v01.py',):
            path=RESULTS+'/'+name;self.diagnostic_files[path]=(ROOT/path).read_bytes()
        plan='protocol/revision-20261022/post-result-diagnostics.md'
        self.diagnostic_files[plan]=b'# Synthetic fixture diagnostic plan\n'
        for name,rows in (('post-result-floor.csv',old_floor),('post-result-horizon.csv',old_horizon)):
            self.diagnostic_files[RESULTS+'/'+name]=adapter.csv_bytes(rows)
        audit=dict(version=1,status='VERIFIED',floor_rows=90,horizon_rows=45,
            builder_sha256=rep.sha(self.diagnostic_files[RESULTS+'/post-result-builder-v01.py']),
            plan=dict(path=plan,sha256=rep.sha(self.diagnostic_files[plan])),
            exports=[dict(path=n,**identity(self.diagnostic_files[RESULTS+'/'+n])) for n in ('post-result-floor.csv','post-result-horizon.csv')])
        self.diagnostic_files[RESULTS+'/post-result-diagnostics-audit.json']=json_raw(audit)
        for path,raw in self.diagnostic_files.items():self.write(path,raw)
        self.diagnostic_contract=diagnostics.DiagnosticContract({p:(len(r),rep.sha(r)) for p,r in self.diagnostic_files.items()})

    def write(self,path,raw):
        p=Path(path);p=p if p.is_absolute() else self.root/p
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)

    def archive(self,path,raw):
        self.write(path,raw);self.archived_files[path]=(len(raw),rep.sha(raw))

    def write_controller(self):self.write(self.attempt/'controller-final.json',json_raw(self.controller))

    def generated(self,shift,mutator,*,reconcile_metrics=False):
        helper=loaded_original_helpers();summary=[];floor_rows=[];stored={};queue=[];receipts={}
        selected={(c['source'],c['horizon'],c['window'],c['family']):c['parameter'] for c in self.selection['cells']}
        for cell in rep.phase_jobs(self.spec,'evaluation')+rep.phase_jobs(self.spec,'references'):
            phase,s,h,w,f=cell;cfg=self.spec['sources'][s];parameter=selected[s,h,w,f] if f else None
            methods=[f] if f else [p+'_'+r for p in (('rolling','frozen','one_state') if cfg['one_state_reference_neighbors'][str(w)] else ('rolling','frozen')) for r in ('F','S','K')]
            first=cfg['evaluation_origin_first'];ids=np.arange(first,first+4,dtype=np.int64)
            arrays={};reported=[]
            for index,method in enumerate(methods):
                b=np.array([1.,2.,1.,2.]);p=np.array([2.,2.,4.,4.])+(0. if h==6 else 2.)
                c=b.copy() if method=='QR' else b+10. if method=='KNN' else b+1.+index*.125
                if method=='KNN' and parameter==w:c=b+1.375 # frozen_F index3
                if s=='fx_hourly' and h==6 and method=='QR':c=c+shift
                refits=first+(ids-first)//cfg['refit_step']*cfg['refit_step'] if f or method.startswith('frozen_') else ids.copy()
                metrics=summarize_scores(score_predictions(p,c,b,ids))
                row=dict(method=method,parameter=parameter)|metrics;reported.append(row)
                shown_parameter=cfg['one_state_reference_neighbors'][str(w)] if method.startswith('one_state_') else parameter
                meta=dict(source=s,native_unit=cfg['native_unit'],horizon=h,window=w,method=method,parameter=shown_parameter)
                summary.append(meta|dict(refit_step=cfg['refit_step'] if f or method.startswith('frozen_') else 1,
                    plain_knn_full_pool_fallback=method=='KNN' and parameter==w)|metrics)
                floor_rows.append(meta|helper.floor_diagnostics(p,c,b))
                stored[s,h,w,method]=dict(origins=ids.copy(),peak=p.copy(),capacity=c.copy(),floor=b.copy(),parameter='' if shown_parameter is None else str(shown_parameter))
                values=dict(origins=ids,peak=p,floor=b,capacity=c,refit_indices=refits,pinball=score_predictions(p,c,b,ids).pinball)
                if mutator is not None:mutator(cell,method,values)
                if reconcile_metrics:
                    scores=score_predictions(values['peak'],values['capacity'],values['floor'],values['origins'])
                    values['pinball']=scores.pinball
                    metrics=summarize_scores(scores)
                    reported[-1]=dict(method=method,parameter=parameter)|metrics
                    summary[-1]={k:v for k,v in summary[-1].items() if k not in metrics}|metrics
                arrays.update({method+'_'+k:v for k,v in values.items()})
            memory=io.BytesIO();np.savez_compressed(memory,**arrays);raw_npz=memory.getvalue()
            fits=[]
            if f:
                for r in range(first,first+4,cfg['refit_step']):
                    entry=dict(method=f,parameter=parameter,refit_index=r,training_first_origin=r-h-w+1,
                        training_last_origin=r-h,training_count=w,latest_label_end=r)
                    if f=='QR':
                        a,d=float(.95).as_integer_ratio();g=2**40
                        entry.update(primal_objective=0.,dual_objective=0.,duality_gap=0.,primal_residual=0.,dual_residual=0.,
                            primal_tolerance=1e-6,dual_tolerance=1e-6,gap_tolerance=1e-6,iterations=1,
                            dual_integer_lower=-((d-a)*g//d),dual_integer_upper=a*g//d,dual_integer_sum=0,dual_grid_denominator=g)
                    fits.append(entry)
            receipt=dict(version=1,phase=phase,source=s,horizon=h,window=w,family=f,status='COMPLETE',stop_code=None,
                executable_freeze_sha256=self.freeze,selection_freeze_sha256=self.selection_hash if f else None,
                source_identity={k:cfg[k] for k in ('sha256','bytes','record_count','native_unit')},resources=resources(),
                result=dict(status='COMPLETE',failure=None,candidate_rows=[],native_unit=cfg['native_unit'],
                    selection=dict(status='SELECTED',parameter=parameter) if f else None,
                    origin_identity=rep.origin_identity(first,first+3),summary_rows=reported,fit_diagnostics=fits),
                artifacts=[dict(area='private',name='numeric-traces.npz',**identity(raw_npz))])
            path=rep.worker_directory(self.attempt,cell)/'public/manifest.json'
            raw=json_raw(receipt);self.write(path,raw);self.write(path.parent.parent/'private/numeric-traces.npz',raw_npz)
            queue.append(dict(phase=phase,source=s,horizon=h,window=w,family=f,exit_code=0,timed_out=False,
                status='COMPLETE',stop_code=None,receipt_path=str(path.relative_to(self.root)),receipt_sha256=rep.sha(raw)))
            name=f'evaluation-{s}-h{h}-w{w}-{f}.json' if f else f'references-{s}-h{h}-w{w}.json'
            receipts[name]=raw
        horizons=[]
        for (s,h,w,m),short in stored.items():
            if h!=6:continue
            long=stored[s,24,w,m]
            horizons.append(dict(source=s,native_unit=self.spec['sources'][s]['native_unit'],window=w,method=m,
                parameter_h6=short['parameter'],parameter_h24=long['parameter'])|
                helper.horizon_diagnostics(short['capacity'],long['capacity'],short['peak'],long['peak']))
        return dict(summary=summary,floor=floor_rows,horizon=horizons,queue=queue,receipts=receipts)


class SyntheticGuard:
    def __init__(self,*args):self.resources=resources()
    def __call__(self,**kwargs):pass
    def arrays(self,*args):pass


@unittest.skipUnless(MODULE_AVAILABLE,'initial RED: module absent')
class AuditedDiagnosticTests(unittest.TestCase):
    def setUp(self):
        parent=ROOT/'.scratch/revision-20261022/diagnostic-synthetic-tests'
        parent.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=parent);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.fixture=SyntheticFixture(self.root)

    def prepare(self, fixture=None):
        f=fixture or self.fixture
        return diagnostics.prepare(f.root,f.attempt,archive_contract=f.archive_contract,
                                   diagnostic_contract=f.diagnostic_contract)

    def run_fixture(self,fixture=None):
        f=fixture or self.fixture
        return diagnostics.reproduce(f.root,f.attempt,archive_contract=f.archive_contract,
            diagnostic_contract=f.diagnostic_contract,guard_factory=SyntheticGuard)

    def test_real_pinned_helper_interfaces_and_known_arithmetic(self):
        helper=diagnostics.load_diagnostic_helpers(ROOT)
        row=helper.floor_diagnostics([2.,3.,4.],[2.,2.,5.],[2.,2.,1.])
        self.assertEqual((row['floor_binding_count'],row['floor_binding_breach_count']), (2,1))
        self.assertEqual(row['floor_binding_breach_rate'],.5)
        horizon=helper.horizon_diagnostics([5.,2.,7.],[4.,3.,5.],[3.,2.,4.],[4.,3.,5.])
        self.assertEqual(horizon['strict_crossing_count'],2)
        self.assertEqual(horizon['maximum_positive_crossing'],2.)
        self.assertEqual(horizon['mean_positive_crossing'],1.)
        real=adapter._load_helpers(ROOT)
        self.assertTrue(callable(real.verify_method));self.assertTrue(callable(real.summarize_scores))

    def test_real_published_aggregate_labels_match_frozen_inventory(self):
        # Read-only public metadata check, not a financial accuracy computation.
        archived=rep.verify_archive(ROOT)
        selected={(c['source'],c['horizon'],c['window'],c['family']):c for c in archived['selection']['cells']}
        cells,expected=diagnostics._inventory(archived['spec'],selected)
        self.assertEqual((len(cells),len(expected)),(32,90))
        for name,horizon in (('post-result-floor.csv',False),('post-result-horizon.csv',True)):
            diagnostics._check_labels(parse_csv((ROOT/RESULTS/name).read_bytes()),expected,horizon=horizon)

    def test_npy_header_shape_rejected_before_any_array_allocation(self):
        for descriptor in ('<f8','|O'):
            header=io.BytesIO()
            np.lib.format.write_array_header_1_0(header,dict(descr=descriptor,fortran_order=False,shape=(10**9,)))
            archive=io.BytesIO()
            with zipfile.ZipFile(archive,'w') as zipped:zipped.writestr('toy_capacity.npy',header.getvalue())
            with self.subTest(dtype=descriptor),self.assertRaises(rep.ReproductionError) as caught:
                diagnostics._check_trace_headers(archive.getvalue(),{'toy_capacity'},np,4)
            self.assertEqual(caught.exception.code,'NPZ_HEADER')

    def test_full_synthetic_inventory_matches_and_inputs_are_preserved(self):
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result=self.run_fixture()
        self.assertEqual(result['status'],'DIAGNOSTICS_REPRODUCED')
        self.assertEqual((result['floor_rows'],result['horizon_rows']),(90,45))
        self.assertTrue(result['exact_csv_scalar_agreement'])
        self.assertFalse(result['raw_sources_read']);self.assertFalse(result['models_refitted'])
        for relative,raw in before.items():self.assertEqual((self.root/relative).read_bytes(),raw)
        out=self.fixture.attempt/'post-result-diagnostics/public'
        self.assertEqual(len(parse_csv((out/'post-result-floor.csv').read_bytes())),90)
        self.assertEqual(len(parse_csv((out/'post-result-horizon.csv').read_bytes())),45)

    @unittest.skipUnless(platform.system()=='Darwin','Darwin resource contract only')
    def test_synthetic_execution_uses_real_resource_measurement(self):
        result=diagnostics.reproduce(self.root,self.fixture.attempt,
            archive_contract=self.fixture.archive_contract,diagnostic_contract=self.fixture.diagnostic_contract)
        measured=result['resources']
        self.assertEqual(measured['requested_numerical_threads'],1)
        self.assertTrue(0<measured['peak_rss_bytes']<1610612736)
        self.assertTrue(1<=measured['maximum_observed_os_threads']<=2)
        self.assertGreater(measured['thread_snapshot_count'],0)
        self.assertEqual(measured['current_stage'],'diagnostic_verified_before_receipt')

    def test_zero_denominators_remain_blank_with_explicit_reasons(self):
        self.run_fixture();out=self.fixture.attempt/'post-result-diagnostics/public/post-result-floor.csv'
        rows=parse_csv(out.read_bytes())
        all_bound=next(r for r in rows if r['method']=='QR')
        self.assertEqual(all_bound['other_issue_breach_denominator'],'0')
        self.assertEqual(all_bound['other_issue_breach_rate'],'')
        self.assertEqual(all_bound['other_issue_undefined_reason'],'NO_OTHER_ISSUES')
        no_bound=next(r for r in rows if r['method']=='KNN' and r['window']=='2880')
        self.assertEqual(no_bound['floor_binding_breach_denominator'],'0')
        self.assertEqual(no_bound['floor_binding_breach_rate'],'')
        self.assertEqual(no_bound['floor_binding_undefined_reason'],'NO_FLOOR_BINDING_ISSUES')

    def test_changed_audited_replication_retains_all_exact_cell_differences(self):
        other=self.root/'different';other.mkdir();fixture=SyntheticFixture(other,shift=.125)
        result=self.run_fixture(fixture)
        self.assertEqual(result['status'],'DIAGNOSTICS_REPRODUCED')
        self.assertFalse(result['numerical_replication_exact_scalar_agreement'])
        self.assertFalse(result['exact_csv_scalar_agreement'])
        changes=result['tables']['post-result-floor.csv']['differences']
        changed={d['column'] for d in changes}
        self.assertIn('floor_binding_count',changed)
        self.assertIn('other_issue_undefined_reason',changed)
        self.assertTrue(any(d['new']=='NO_FLOOR_BINDING_ISSUES' for d in changes))

    def test_existing_output_is_rejected_without_overwrite(self):
        self.run_fixture();output=self.fixture.attempt/'post-result-diagnostics'
        before={p.relative_to(output):p.read_bytes() for p in output.rglob('*') if p.is_file()}
        with self.assertRaises(rep.ReproductionError):self.run_fixture()
        after={p.relative_to(output):p.read_bytes() for p in output.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_late_output_mutation_refuses_verified_audit(self):
        class MutatingGuard(SyntheticGuard):
            def __init__(inner,started,utc,attempt,public,private):
                super().__init__();inner.public=public
            def __call__(inner,*,stage=None,**kwargs):
                if stage=='diagnostic_reproduction_final':
                    path=inner.public/'post-result-floor.csv';path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaises(rep.ReproductionError):
            diagnostics.reproduce(self.root,self.fixture.attempt,
                archive_contract=self.fixture.archive_contract,diagnostic_contract=self.fixture.diagnostic_contract,
                guard_factory=MutatingGuard)
        out=self.fixture.attempt/'post-result-diagnostics/public'
        self.assertFalse((out/'diagnostic-reproduction-audit.json').exists())
        self.assertEqual(rep.strict_json((out/'diagnostic-failure.json').read_bytes())['status'],'STOPPED')

    def test_production_rejects_injected_resource_guard(self):
        # This must stop before any production archive, trace or raw-source read.
        with self.assertRaises(rep.ReproductionError) as caught:
            diagnostics.reproduce(ROOT,'.scratch/revision-20261022/replication-ABSENT',guard_factory=SyntheticGuard)
        self.assertEqual(caught.exception.code,'TEST_ONLY_GUARD')

    def test_wrong_controller_state_accuracy_counts_or_hash_rejected(self):
        original=copy.deepcopy(self.fixture.controller)
        mutations=[lambda d:d.update(status='PHASES_COMPLETE_AUDIT_PENDING'),lambda d:d.update(accuracy_recomputed=False),
            lambda d:d.update(selection_sha256='0'*64),lambda d:d.update(completed_evaluation_reference_cells=31),
            lambda d:d.update(selection_agrees_with_archive=False),lambda d:d.update(stop_code='ANY_FAILURE')]
        for change in mutations:
            self.fixture.controller=copy.deepcopy(original);change(self.fixture.controller);self.fixture.write_controller()
            with self.subTest(change=change),self.assertRaises(rep.ReproductionError):self.prepare()

    def test_changed_selection_choice_rejected_even_when_controller_hash_is_rebound(self):
        selected=copy.deepcopy(self.fixture.selection);selected['cells'][0]['parameter']=.001
        raw=json_raw(selected);self.fixture.write(self.fixture.attempt/'selection-freeze.json',raw)
        self.fixture.controller['selection_sha256']=rep.sha(raw);self.fixture.write_controller()
        with self.assertRaises(rep.ReproductionError):self.prepare()

    def test_changed_archive_and_new_export_are_rejected(self):
        p=self.root/RESULTS/'evaluation-summary.csv';old=p.read_bytes();p.write_bytes(old+b'\n')
        with self.assertRaises(rep.ReproductionError):self.prepare()
        p.write_bytes(old)
        p=self.fixture.attempt/'numerical-audit/public/evaluation-summary.csv';p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(rep.ReproductionError):self.prepare()

    def test_forged_numerical_comparison_flags_or_receipt_inventory_rejected(self):
        original=copy.deepcopy(self.fixture.comparison)
        mutations=[lambda d:d.update(status='PENDING'),lambda d:d.update(new_selection_sha256='0'*64),
            lambda d:d.update(queue_sha256='0'*64),lambda d:d['receipts'].pop(),
            lambda d:d['exports'].append(copy.deepcopy(d['exports'][0])),
            lambda d:d['tables']['evaluation-summary.csv'].update(exact_scalar_agreement=False)]
        for change in mutations:
            current=copy.deepcopy(original);change(current);self.fixture.write(self.fixture.comparison_path,json_raw(current))
            with self.subTest(change=change),self.assertRaises(rep.ReproductionError):self.prepare()

    def test_receipt_or_npz_hash_mutation_rejected(self):
        inputs=self.prepare();path=self.root/self.fixture.queue[0]['receipt_path'];raw=path.read_bytes()
        path.write_bytes(raw+b' ')
        with self.assertRaises(rep.ReproductionError):diagnostics.derive(inputs,np,diagnostics.load_diagnostic_helpers(self.root,self.fixture.diagnostic_contract))
        path.write_bytes(raw);npz=path.parent.parent/'private/numeric-traces.npz';npz.write_bytes(npz.read_bytes()+b'x')
        with self.assertRaises(rep.ReproductionError):diagnostics.derive(inputs,np,diagnostics.load_diagnostic_helpers(self.root,self.fixture.diagnostic_contract))

    def test_dtype_issue_refit_floor_and_target_order_fail_closed(self):
        def wrong_dtype(cell,method,values):
            if cell[:2]==('evaluation','fx_hourly'):values['origins']=values['origins'].astype(np.float64)
        def wrong_issue(cell,method,values):values['origins']=values['origins']+1
        def wrong_refit(cell,method,values):values['refit_indices']=values['refit_indices']+1
        def wrong_floor(cell,method,values):values['capacity']=values['floor']-1.
        def wrong_order(cell,method,values):
            if cell[2]==6:values['peak']=values['peak']+100.
        for index,change in enumerate((wrong_dtype,wrong_issue,wrong_refit,wrong_floor,wrong_order)):
            other=self.root/('bad-'+str(index));other.mkdir();fixture=SyntheticFixture(other,trace_mutator=change)
            inputs=self.prepare(fixture)
            with self.subTest(index=index),self.assertRaises(rep.ReproductionError):
                diagnostics.derive(inputs,np,diagnostics.load_diagnostic_helpers(other,fixture.diagnostic_contract))

    def test_consistent_traces_reach_exact_cross_cell_and_horizon_checks(self):
        def target_order(cell,method,values):
            if cell[2]==6:values['peak']=values['peak']+100.
        def horizon_floor(cell,method,values):
            if cell[2]==24:values['floor']=np.zeros_like(values['floor'])
        def inconsistent_same_horizon_target(cell,method,values):
            if cell[4]=='QR':values['peak']=values['peak']+.125
        for i,(change,code) in enumerate(((target_order,'HORIZON_TARGET_ORDER'),
                (horizon_floor,'HORIZON_ISSUE_FLOOR'),
                (inconsistent_same_horizon_target,'CROSS_CELL_TARGET_FLOOR'))):
            other=self.root/('consistent-bad-'+str(i));other.mkdir()
            fixture=SyntheticFixture(other,trace_mutator=change,reconcile_metrics=True)
            with self.subTest(code=code),self.assertRaises(rep.ReproductionError) as caught:
                diagnostics.derive(self.prepare(fixture),np,diagnostics.load_diagnostic_helpers(other,fixture.diagnostic_contract))
            self.assertEqual(caught.exception.code,code)

    def test_failed_trace_retains_failure_and_no_verified_receipt(self):
        other=self.root/'failed-trace';other.mkdir()
        def broken(cell,method,values):values['capacity']=values['floor']-1.
        fixture=SyntheticFixture(other,trace_mutator=broken)
        with self.assertRaises(rep.ReproductionError):self.run_fixture(fixture)
        output=fixture.attempt/'post-result-diagnostics/public'
        receipt=rep.strict_json((output/'diagnostic-failure.json').read_bytes())
        self.assertEqual((receipt['status'],receipt['verified_diagnostics']),('STOPPED',False))
        self.assertFalse((output/'diagnostic-reproduction-audit.json').exists())

    def test_changed_consumed_snapshot_is_rejected_before_verified_export(self):
        inputs=self.prepare();self.fixture.write(self.fixture.attempt/'controller-final.json',b'{}')
        with self.assertRaises(rep.ReproductionError):diagnostics.verify_snapshots(inputs)

    def test_unsafe_attempt_and_symlink_rejected(self):
        for value in ('../bad','.scratch/revision-20261022/other','/tmp/replication-elsewhere'):
            with self.subTest(value=value),self.assertRaises(rep.ReproductionError):
                diagnostics.prepare(self.root,value,archive_contract=self.fixture.archive_contract,
                                    diagnostic_contract=self.fixture.diagnostic_contract)
        linked=self.root/'.scratch/revision-20261022/replication-linked';linked.symlink_to(self.fixture.attempt,target_is_directory=True)
        with self.assertRaises(rep.ReproductionError):
            diagnostics.prepare(self.root,linked,archive_contract=self.fixture.archive_contract,
                                diagnostic_contract=self.fixture.diagnostic_contract)


if __name__ == '__main__':
    unittest.main()
