"""Synthetic contract/controller tests. No accepted raw financial data is read."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

MODULE_AVAILABLE = importlib.util.find_spec('reproduce_conditional') is not None
if MODULE_AVAILABLE:
    import reproduce_conditional as rep
ADAPTER_AVAILABLE = importlib.util.find_spec('reconcile_conditional_replication') is not None
if ADAPTER_AVAILABLE:
    import reconcile_conditional_replication as adapter


def raw_json(value):
    return (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def temporary_directory():
    base=Path(__file__).resolve().parent/'.scratch/revision-20261022-data-scout/replication-synthetic-tests'
    base.mkdir(parents=True,exist_ok=True)
    return tempfile.TemporaryDirectory(dir=base)


def make_spec():
    return dict(horizons=[2], families=['QR', 'KNN'], qr_penalties=[.001, .01, .1],
        sources={'fx_hourly': dict(input_relative_path='.scratch/input.csv', sha256=digest(b'synthetic source'),
        bytes=16, record_count=30, native_unit='USD', windows=[20], validation_origin_first=22,
        validation_origin_last=23, evaluation_origin_first=26, evaluation_origin_last=27,
        knn_candidates={'20': [19, 20]}, refit_step=1, short_scale=1, long_scale=2,
        nominal_gap_seconds=3600, one_state_reference_neighbors={'20': None})})


def keys(spec):
    return [(s, h, w, f) for s, c in spec['sources'].items()
            for h in spec['horizons'] for w in c['windows'] for f in spec['families']]


def origin_identity(first=22, last=23):
    return dict(count=last-first+1, first=first, last=last,
        sha256=digest(b''.join(x.to_bytes(8, 'little', signed=True) for x in range(first,last+1))))


def receipt(spec, key, freeze_hash, *, phase='validation'):
    s, h, w, f = key; c = spec['sources'][s]
    rows = [dict(parameter=p, status='COMPLETE', origin_count=2, mean_pinball=1., failure=None)
            for p in (spec['qr_penalties'] if f == 'QR' else c['knn_candidates'][str(w)])]
    return dict(version=1, phase=phase, source=s, horizon=h, window=w, family=f,
        status='COMPLETE', stop_code=None, executable_freeze_sha256=freeze_hash,
        selection_freeze_sha256=None,
        source_identity={n:c[n] for n in ('sha256','bytes','record_count','native_unit')},
        resources=dict(elapsed_seconds=.1, peak_rss_bytes=10000, maximum_observed_os_threads=1,
            thread_snapshot_count=1, thread_probe_status='PASS'),
        result=dict(candidate_rows=rows, origin_identity=origin_identity()))


class Fixture:
    def __init__(self, root):
        self.root=root; self.spec=make_spec()
        self.freeze_path='protocol/revision-20261022/executable-freeze.json'
        self.selection_path='protocol/revision-20261022/selection-freeze.json'
        self.spec_path='protocol/revision-20261022/study-spec.json'
        self.write('model.py',b'# synthetic immutable model\n')
        self.write(self.spec_path,raw_json(self.spec))
        freeze=dict(version=1,status='FROZEN',created_utc='2026-01-01T00:00:00Z',
            files={p:digest((root/p).read_bytes()) for p in ('model.py',self.spec_path)},
            sources={s:{n:c[n] for n in ('sha256','bytes')} for s,c in self.spec['sources'].items()})
        self.freeze_raw=raw_json(freeze); self.freeze_hash=digest(self.freeze_raw)
        self.write(self.freeze_path,self.freeze_raw)
        self.cells=[]; self.archive={}
        for key in keys(self.spec):
            s,h,w,f=key; raw=raw_json(receipt(self.spec,key,self.freeze_hash))
            public=f'results/revision-20261022/validation-{s}-h{h}-w{w}-{f}.json'
            historical=f'.scratch/revision-20261022/val-{s}-h{h}-w{w}-{f}-01/public/manifest.json'
            self.write(public,raw);self.archive[public]=(len(raw),digest(raw))
            self.cells.append(dict(source=s,horizon=h,window=w,family=f,status='SELECTED',
                parameter=.1 if f=='QR' else 20,validation_receipts=[dict(path=historical,sha256=digest(raw))]))
        self.selection=dict(version=1,status='FROZEN',created_utc='2026-01-01T00:01:00Z',
            executable_freeze_sha256=self.freeze_hash,cells=self.cells)
        selection_raw=raw_json(self.selection);self.write(self.selection_path,selection_raw)
        self.selection_hash=digest(selection_raw)

    def write(self,path,raw):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)

    def contract(self):
        return rep.ArchiveContract(self.freeze_hash,self.selection_hash,
            ('model.py',self.spec_path),dict(self.archive),self.freeze_path,self.selection_path,self.spec_path)

    def refresh_selection(self):
        raw=raw_json(self.selection);self.write(self.selection_path,raw);self.selection_hash=digest(raw)


class ModuleContract(unittest.TestCase):
    def test_module_exists(self):
        self.assertTrue(MODULE_AVAILABLE, 'new reproduction entry point is not implemented')

    def test_adapter_exists(self):
        self.assertTrue(ADAPTER_AVAILABLE, 'new-attempt numerical reconciliation is not implemented')

    def test_cli_module_identity_is_shared_with_deferred_adapter_import(self):
        # --help reads no archive or source and must work without numeric imports.
        script=Path(__file__).resolve().parent/'reproduce_conditional.py'
        code=("import runpy,sys; sys.argv=[sys.argv[1],'--help']\n"
              "try: runpy.run_path(sys.argv[0],run_name='__main__')\n"
              "except SystemExit as e: assert e.code==0\n"
              "m=sys.modules.get('reproduce_conditional')\n"
              "assert m is not None and hasattr(m,'ReproductionError')\n"
              "assert 'numpy' not in sys.modules and 'run_study' not in sys.modules\n")
        completed=subprocess.run([sys.executable,'-B','-c',code,str(script)],capture_output=True,text=True)
        self.assertEqual(completed.returncode,0,completed.stderr)


@unittest.skipUnless(MODULE_AVAILABLE,'initial RED: module absent')
class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=temporary_directory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.fx=Fixture(self.root)

    def verify(self):
        return rep.verify_archive(self.root,contract=self.fx.contract())

    def test_read_only_archive_without_raw_or_historical_scratch(self):
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with mock.patch.dict('sys.modules', {'numpy': None, 'run_conditional_study': None}):
            report=self.verify()
        after={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after);self.assertFalse((self.root/'.scratch').exists())
        self.assertEqual(report['status'],'ARCHIVE_VERIFIED');self.assertFalse(report['accuracy_recomputed'])
        self.assertEqual(len(report['selection']['cells']),2)

    def test_modified_code_rejected(self):
        self.fx.write('model.py',b'# altered\n')
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_changed_public_receipt_rejected(self):
        p=next(iter(self.fx.archive));self.fx.write(p,b'{}')
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_selection_receipt_hash_cannot_be_rebound(self):
        self.fx.cells[0]['validation_receipts'][0]['sha256']='a'*64;self.fx.refresh_selection()
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_changed_choice_rejected_even_with_new_selection_hash(self):
        self.fx.cells[0]['parameter']=.001;self.fx.refresh_selection()
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_missing_cell_or_duplicate_cell_rejected(self):
        self.fx.selection['cells']=[self.fx.cells[0],self.fx.cells[0]];self.fx.refresh_selection()
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_symlink_rejected(self):
        original=self.root/'model.py';saved=self.root/'other.py';original.rename(saved);original.symlink_to(saved)
        with self.assertRaises(rep.ReproductionError):self.verify()

    def test_traversal_rejected(self):
        with self.assertRaises(rep.ReproductionError):rep.project_file(self.root,'../elsewhere')

    def test_duplicate_and_nonfinite_json_rejected(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'[]'):
            with self.subTest(raw=raw),self.assertRaises(rep.ReproductionError):rep.strict_json(raw)

    def test_selection_failed_candidate_is_ineligible_no_fallback(self):
        data=receipt(self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash)
        data['result']['candidate_rows'][0].update(status='FAILED',mean_pinball=None)
        data['status']='INELIGIBLE'
        self.assertEqual(rep.validation_choice(data,self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash),
            dict(status='INELIGIBLE',parameter=None))

    def test_validation_origin_resource_and_candidate_integrity(self):
        mutations=[lambda d:d['result']['origin_identity'].update(count=1),
            lambda d:d['resources'].update(maximum_observed_os_threads=3),
            lambda d:d['result']['candidate_rows'].reverse(),
            lambda d:d['result']['candidate_rows'][0].update(mean_pinball=float('nan')),
            lambda d:d['result']['candidate_rows'][0].update(origin_count=1)]
        for change in mutations:
            data=receipt(self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash);change(data)
            with self.subTest(change=change),self.assertRaises(rep.ReproductionError):
                rep.validation_choice(data,self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash)

    def test_exact_tie_prefers_larger_parameter(self):
        data=receipt(self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash)
        self.assertEqual(rep.validation_choice(data,self.fx.spec,keys(self.fx.spec)[0],self.fx.freeze_hash)['parameter'],.1)


@unittest.skipUnless(MODULE_AVAILABLE,'initial RED: module absent')
class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp=temporary_directory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.fx=Fixture(self.root);self.calls=[]
        self.archive=rep.verify_archive(self.root,contract=self.fx.contract())

    def fake_worker(self,job,attempt,selection,remaining):
        self.calls.append((job,remaining));attempt.mkdir()
        (attempt/'public').mkdir();(attempt/'private').mkdir()
        phase,s,h,w,f=job
        data=receipt(self.fx.spec,(s,h,w,f),self.fx.freeze_hash,phase=phase)
        if phase=='evaluation':data['selection_freeze_sha256']=selection[1]
        (attempt/'public/manifest.json').write_bytes(raw_json(data))
        return dict(exit_code=0,timed_out=False)

    def run_plan(self,**kwargs):
        return rep.run_plan(self.root,'synthetic-01',self.archive,worker=self.fake_worker,**kwargs)

    def test_all_validation_before_selection_before_eval_and_refs(self):
        result=self.run_plan()
        self.assertEqual([c[0][0] for c in self.calls],['validation','validation','evaluation','evaluation','references'])
        self.assertEqual(result['status'],'PHASES_COMPLETE_AUDIT_PENDING')
        p=self.root/result['selection_path'];new=rep.strict_json(p.read_bytes())
        self.assertEqual([c['parameter'] for c in new['cells']],[.1,20])
        self.assertNotEqual(digest(p.read_bytes()),self.fx.selection_hash)
        self.assertTrue(all('replication-synthetic-01/' in c['validation_receipts'][0]['path'] for c in new['cells']))
        self.assertEqual(len(rep.strict_json((self.root/result['queue_path']).read_bytes())['cells']),3)

    def test_existing_attempt_is_never_overwritten(self):
        self.run_plan();first=list(self.calls)
        with self.assertRaises(rep.ReproductionError):self.run_plan()
        self.assertEqual(first,self.calls)

    def test_safe_id_rejects_traversal_and_path_separators(self):
        for tag in ('../bad','a/b','/tmp/a','a\\b','','a'*65):
            with self.subTest(tag=tag),self.assertRaises(rep.ReproductionError):
                rep.run_plan(self.root,tag,self.archive,worker=self.fake_worker)
        self.assertFalse((self.root/'.scratch').exists())

    def test_mismatched_new_selection_stops_before_evaluation(self):
        normal=self.fake_worker
        def changed(job,attempt,selection,remaining):
            result=normal(job,attempt,selection,remaining)
            p=attempt/'public/manifest.json';d=rep.strict_json(p.read_bytes())
            if job[-1]=='QR':d['result']['candidate_rows'][0]['mean_pinball']=0.
            p.write_bytes(raw_json(d));return result
        result=rep.run_plan(self.root,'different-choice',self.archive,worker=changed)
        self.assertEqual(result['status'],'STOPPED');self.assertEqual(result['stop_code'],'SELECTION_CHANGED')
        self.assertTrue(all(c[0][0]=='validation' for c in self.calls))
        self.assertTrue((self.root/result['selection_path']).is_file())

    def test_missing_receipt_retained_and_no_fabricated_manifest(self):
        def missing(job,attempt,selection,remaining):
            self.calls.append((job,remaining));attempt.mkdir();return dict(exit_code=1,timed_out=False)
        result=rep.run_plan(self.root,'missing',self.archive,worker=missing)
        self.assertEqual(result['status'],'STOPPED');self.assertEqual(result['stop_code'],'VALIDATION_INCOMPLETE')
        self.assertEqual(len(self.calls),2)
        self.assertFalse(any((self.root/result['attempt_path']).rglob('manifest.json')))

    def test_budget_covers_all_workers_and_stops_after_timeout(self):
        clock=mock.Mock(side_effect=[1.,541.,541.])
        result=rep.run_plan(self.root,'budget',self.archive,worker=self.fake_worker,clock=clock,started=0.)
        self.assertEqual(result['stop_code'],'GLOBAL_DEADLINE');self.assertEqual(len(self.calls),1)
        self.assertLessEqual(self.calls[0][1],539.)

    def test_worker_timeout_does_not_run_next_job(self):
        def timeout(job,attempt,selection,remaining):
            attempt.mkdir();self.calls.append((job,remaining));return dict(exit_code=-9,timed_out=True)
        result=rep.run_plan(self.root,'timeout',self.archive,worker=timeout)
        self.assertEqual(result['stop_code'],'GLOBAL_DEADLINE');self.assertEqual(len(self.calls),1)

    def test_worker_deadline_exception_retains_active_job_controller_record(self):
        def interrupted(job,attempt,selection,remaining):
            attempt.mkdir();raise rep.ReproductionError('GLOBAL_DEADLINE')
        result=rep.run_plan(self.root,'interrupted',self.archive,worker=interrupted)
        self.assertEqual(result['validation_jobs_retained'],1)
        path=self.root/result['attempt_path']/'validation-queue.json'
        self.assertEqual(rep.strict_json(path.read_bytes())['cells'][0]['status'],'NO_TERMINAL_RECEIPT')
        self.assertFalse(any((self.root/result['attempt_path']).rglob('manifest.json')))

    def test_platform_preflight_fails_before_source_access(self):
        with mock.patch.object(rep.platform,'system',return_value='Linux'),mock.patch.object(rep,'project_file') as read:
            with self.assertRaisesRegex(rep.ReproductionError,'DARWIN_REQUIRED'):
                rep.replication_preflight(self.root,self.archive)
            read.assert_not_called()

    def test_source_preflight_requires_exact_hash_and_does_not_create_attempt(self):
        self.fx.write('.scratch/input.csv',b'changed contents')
        with mock.patch.object(rep.platform,'system',return_value='Darwin'),mock.patch.object(rep.importlib.util,'find_spec',return_value=object()):
            with self.assertRaises(rep.ReproductionError):rep.replication_preflight(self.root,self.archive)
        self.assertFalse((self.root/'.scratch/revision-20261022').exists())

    def test_controller_interrupt_kills_active_worker_process_group(self):
        attempt=self.root/'new-attempt';attempt.mkdir();(attempt/'controller-private').mkdir()
        child=mock.Mock();child.wait.side_effect=[rep.ReproductionError('GLOBAL_DEADLINE'),-9]
        child.poll.return_value=None;child.pid=1234
        worker=rep.subprocess_worker(self.root)
        with mock.patch.object(rep.subprocess,'Popen',return_value=child),mock.patch.object(rep.os,'killpg') as kill:
            with self.assertRaisesRegex(rep.ReproductionError,'GLOBAL_DEADLINE'):
                worker(('validation','fx_hourly',2,20,'QR'),attempt/'child',None,1.)
            kill.assert_called_once_with(1234,rep.signal.SIGKILL)
            self.assertEqual(child.wait.call_count,2)

    def test_global_alarm_uses_remaining_budget_and_restores_prior_handler(self):
        with (mock.patch.object(rep.signal,'getsignal',return_value='prior'),
                mock.patch.object(rep.signal,'signal') as handler,
                mock.patch.object(rep.signal,'setitimer') as timer):
            with rep.controller_deadline(10.,clock=lambda:20.):
                self.assertEqual(timer.call_args_list[0],mock.call(rep.signal.ITIMER_REAL,530.))
            self.assertEqual(timer.call_args_list[-1],mock.call(rep.signal.ITIMER_REAL,0))
            self.assertEqual(handler.call_args_list[-1],mock.call(rep.signal.SIGALRM,'prior'))


@unittest.skipUnless(ADAPTER_AVAILABLE,'adapter RED: module absent')
class AdapterTests(unittest.TestCase):
    def setUp(self):
        import numpy as np
        helpers=adapter._load_helpers(Path(__file__).resolve().parent)
        from conditional_study import score_predictions,summarize_scores
        self.np=np;self.helpers=helpers
        self.temp=temporary_directory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.attempt=self.root/'.scratch/revision-20261022/replication-synthetic'
        self.directory=self.attempt/'evaluation-fx_hourly-h2-w20-KNN'
        (self.directory/'public').mkdir(parents=True);(self.directory/'private').mkdir()
        self.spec=make_spec();cfg=self.spec['sources']['fx_hourly']
        position=np.arange(-15.,15.,dtype=np.float64)
        dates=(np.datetime64('2020-01-01','us')+np.arange(30)*np.timedelta64(1,'h'))
        self.source=SimpleNamespace(source_id='fx_hourly',position=position,dates=dates,
            sha256=cfg['sha256'],bytes=cfg['bytes'],metadata={'units':'USD','observation_count':30})
        self.origins=np.arange(26,28,dtype=np.int64)
        self.peak=helpers.independent_peak(position,self.origins,2);self.floor=np.abs(position[self.origins])
        self.capacity=self.peak+1.;self.refits=self.origins.copy()
        scores=score_predictions(self.peak,self.capacity,self.floor,self.origins)
        metrics=summarize_scores(scores)
        part=score_predictions(self.peak[:1],self.capacity[:1],self.floor[:1],self.origins[:1])
        self.traces={f'KNN_{k}':v for k,v in dict(origins=self.origins,peak=self.peak,floor=self.floor,
            capacity=self.capacity,refit_indices=self.refits,pinball=scores.pinball).items()}
        data=receipt(self.spec,('fx_hourly',2,20,'KNN'),'f'*64,phase='evaluation')
        data['selection_freeze_sha256']='e'*64
        data['result']=dict(status='COMPLETE',failure=None,candidate_rows=[],native_unit='USD',
            origin_identity=origin_identity(26,27),selection=dict(status='SELECTED',parameter=20),
            summary_rows=[dict(method='KNN',parameter=20,**metrics)],
            year_rows=[dict(method='KNN',parameter=20,year=2020,**metrics)],
            nonoverlap_rows=[dict(method='KNN',parameter=20,**summarize_scores(part))],
            fit_diagnostics=[dict(method='KNN',parameter=20,refit_index=r,training_first_origin=r-2-20+1,
                training_last_origin=r-2,training_count=20,latest_label_end=r) for r in (26,27)])
        self.data=data;self.write_trace()
        self.selected={('fx_hourly',2,20,'KNN'):dict(status='SELECTED',parameter=20)}
        self.row=dict(phase='evaluation',source='fx_hourly',horizon=2,window=20,family='KNN',
            status='COMPLETE',stop_code=None,exit_code=0,receipt_path=str((self.directory/'public/manifest.json').relative_to(self.root)))
        self.write_receipt()

    def write_trace(self):
        path=self.directory/'private/numeric-traces.npz'
        self.np.savez(path,**self.traces);raw=path.read_bytes()
        self.data['artifacts']=[dict(area='private',name='numeric-traces.npz',bytes=len(raw),sha256=digest(raw))]

    def write_receipt(self):
        raw=raw_json(self.data);(self.directory/'public/manifest.json').write_bytes(raw)
        self.row['receipt_sha256']=digest(raw)

    def audit(self):
        return adapter.audit_cell(self.root,self.attempt,self.row,self.spec,self.selected,
            'f'*64,'e'*64,self.source,self.np,self.helpers,lambda:100.)

    def test_synthetic_trace_has_independently_verified_peak_scores_and_exports(self):
        found=self.audit()
        self.assertEqual(len(found['summary']),1);self.assertEqual(found['summary'][0]['origin_count'],2)
        self.assertEqual(found['annual'][0]['calendar_year'],2020)
        self.assertEqual(found['nonoverlap'][0]['origin_count'],1)

    def test_unmocked_published_helper_loader_contract_audits_synthetic_cell(self):
        helpers=adapter._load_helpers(Path(__file__).resolve().parent)
        self.assertEqual(Path(helpers.__file__).name,'audit-builder-v01.py')
        self.helpers=helpers
        self.assertEqual(self.audit()['summary'][0]['origin_count'],2)

    def test_helper_execution_uses_verified_snapshot_after_path_changes(self):
        root=self.root/'helper-mutation';relative=rep.RESULTS+'/audit-builder-v01.py'
        path=root/relative;path.parent.mkdir(parents=True)
        accepted=b'marker = "accepted snapshot"\n';replacement=b'raise RuntimeError("unverified second read executed")\n'
        path.write_bytes(accepted);original=rep.project_file;calls=[]
        def mutate_after_verified_read(*args,**kwargs):
            found=original(*args,**kwargs);calls.append(found)
            # The second path lookup follows the first read/hash check.
            if len(calls)==2:path.write_bytes(replacement)
            return found
        with (mock.patch.dict(rep.ARCHIVED_RESULTS,{relative:(len(accepted),digest(accepted))}),
                mock.patch.object(rep,'project_file',side_effect=mutate_after_verified_read)):
            loaded=adapter._load_helpers(root)
        self.assertEqual(loaded.marker,'accepted snapshot')
        self.assertEqual(path.read_bytes(),replacement)

    def test_changed_manifest_or_npz_hash_rejected(self):
        p=self.directory/'public/manifest.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(rep.ReproductionError):self.audit()
        self.write_receipt()
        p=self.directory/'private/numeric-traces.npz';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(rep.ReproductionError):self.audit()

    def test_forged_peak_loss_or_refit_rejected_despite_rehashed_artifact(self):
        for key in ('peak','pinball','refit_indices'):
            original=self.traces['KNN_'+key].copy();self.traces['KNN_'+key]=original.copy()
            self.traces['KNN_'+key][0]+=1
            self.write_trace();self.write_receipt()
            with self.subTest(key=key),self.assertRaises(rep.ReproductionError):self.audit()
            self.traces['KNN_'+key]=original

    def test_object_trace_and_unexpected_array_rejected(self):
        self.traces['KNN_capacity']=self.np.array([object(),object()],dtype=object)
        self.write_trace();self.write_receipt()
        with self.assertRaises(rep.ReproductionError):self.audit()

    def test_float_origins_rejected_even_when_numerically_equal(self):
        self.traces['KNN_origins']=self.origins.astype(float)
        self.write_trace();self.write_receipt()
        with self.assertRaises(rep.ReproductionError):self.audit()

    def test_csv_comparison_records_all_numeric_changes_without_tolerance(self):
        old=b'id,metric,undefined\na,1.0,\nb,0.0,\n';new=b'id,metric,undefined\na,1.0000000000000002,\nb,2.0,\n'
        report=adapter.compare_csv(new,old)
        self.assertFalse(report['byte_identical']);self.assertEqual(len(report['differences']),2)
        self.assertEqual(report['differences'][0]['column'],'metric')
        self.assertGreater(report['differences'][0]['absolute_numeric_difference'],0.)
        self.assertIsNone(report['differences'][1]['relative_numeric_difference'])

    def test_csv_shape_change_is_reported_not_silently_paired(self):
        report=adapter.compare_csv(b'id,x\na,1\nb,2\n',b'id,x\na,1\n')
        self.assertFalse(report['row_count_equal']);self.assertFalse(report['exact_scalar_agreement'])

    def test_complete_32_cell_synthetic_reconciliation_preserves90_and98_inventory(self):
        self.full_reconciliation_fixture()

    def test_finish_selection_mutation_prevents_verified_comparison(self):
        self.full_reconciliation_fixture(tamper_selection_at_finish=True)

    def full_reconciliation_fixture(self,*,tamper_selection_at_finish=False):
        """Exercise the whole adapter with synthetic paths, no model and no raw file."""
        np=self.np;helpers=self.helpers
        root=self.root/'full-synthetic';root.mkdir()
        attempt=root/'.scratch/revision-20261022/replication-full-synthetic';attempt.mkdir(parents=True)
        spec=rep.strict_json((Path(__file__).resolve().parent/rep.SPEC_PATH).read_bytes())
        source_map={};selected={};cells=[]
        for s,cfg in spec['sources'].items():
            count=cfg['record_count'];position=np.arange(count,dtype=np.float64)*.01-10.
            source_path=root/cfg['input_relative_path'];source_path.parent.mkdir(parents=True,exist_ok=True)
            synthetic_raw=('synthetic placeholder '+s).encode();source_path.write_bytes(synthetic_raw)
            cfg['sha256']=digest(synthetic_raw);cfg['bytes']=len(synthetic_raw)
            if s=='fx_hourly':
                zero=cfg['evaluation_origin_first']+6262
                dates=np.datetime64('2017-01-01','us')+(np.arange(count)-zero)*np.timedelta64(1,'h')
            else:dates=np.datetime64('2013-04-03','us')+np.arange(count)*np.timedelta64(7,'D')
            source_map[s]=SimpleNamespace(source_id=s,position=position,dates=dates,sha256=cfg['sha256'],
                bytes=cfg['bytes'],metadata={'units':cfg['native_unit'],'observation_count':count})
        for s,h,w,f in rep.inventory(spec):
            parameter=spec['qr_penalties'][-1] if f=='QR' else spec['sources'][s]['knn_candidates'][str(w)][-1]
            selected[s,h,w,f]=dict(status='SELECTED',parameter=parameter)
            cells.append(dict(source=s,horizon=h,window=w,family=f,status='SELECTED',parameter=parameter,validation_receipts=[]))
        new_selection=dict(version=1,status='FROZEN',created_utc='2026-01-01T00:00:00Z',
            executable_freeze_sha256='f'*64,cells=cells)
        selection_path=attempt/'selection-freeze.json';selection_path.write_bytes(raw_json(new_selection))
        selection_hash=digest(selection_path.read_bytes());queue=[]
        for job in helpers.expected_cells(spec):
            phase,s,h,w,f=job;cfg=spec['sources'][s];source=source_map[s]
            directory=rep.worker_directory(attempt,job);(directory/'public').mkdir(parents=True);(directory/'private').mkdir()
            origins=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
            peak=helpers.independent_peak(source.position,origins,h);floor=np.abs(source.position[origins]);capacity=peak+1.
            methods=([f] if f else [p+'_'+r for p in (('rolling','frozen','one_state')
                if cfg['one_state_reference_neighbors'][str(w)] else ('rolling','frozen')) for r in ('F','S','K')])
            parameter=selected[s,h,w,f]['parameter'] if f else None
            traces={};summary=[];annual=[];grid_rows=[];diagnostics=[]
            years=source.dates[origins].astype('datetime64[Y]').astype(int)+1970
            for method in methods:
                refits=(origins[0]+((origins-origins[0])//cfg['refit_step'])*cfg['refit_step']
                    if f or method.startswith('frozen_') else origins)
                scores=helpers.score_predictions(peak,capacity,floor,origins)
                summary.append(dict(method=method,parameter=parameter,**helpers.summarize_scores(scores)))
                for year in np.unique(years):
                    mask=years==year;part=helpers.score_predictions(peak[mask],capacity[mask],floor[mask],origins[mask])
                    annual.append(dict(method=method,parameter=parameter,year=int(year),**helpers.summarize_scores(part)))
                mask=np.isin(origins,helpers.nonoverlap_origins(int(origins[0]),int(origins[-1]),h))
                part=helpers.score_predictions(peak[mask],capacity[mask],floor[mask],origins[mask])
                grid_rows.append(dict(method=method,parameter=parameter,**helpers.summarize_scores(part)))
                traces.update({method+'_'+n:a for n,a in dict(origins=origins,peak=peak,floor=floor,
                    capacity=capacity,refit_indices=refits,pinball=scores.pinball).items()})
            if f:
                for r in range(int(origins[0]),int(origins[-1])+1,cfg['refit_step']):
                    row=dict(method=f,parameter=parameter,refit_index=r,training_first_origin=r-h-w+1,
                        training_last_origin=r-h,training_count=w,latest_label_end=r)
                    if f=='QR':
                        numerator,denominator=float(.95).as_integer_ratio();grid=2**40
                        row.update(primal_objective=0.,dual_objective=0.,duality_gap=0.,primal_residual=0.,
                            dual_residual=0.,primal_tolerance=0.,dual_tolerance=0.,gap_tolerance=0.,iterations=1,
                            dual_integer_lower=-((denominator-numerator)*grid//denominator),
                            dual_integer_upper=numerator*grid//denominator,dual_integer_sum=0,dual_grid_denominator=grid)
                    diagnostics.append(row)
            path=directory/'private/numeric-traces.npz';np.savez(path,**traces);trace_raw=path.read_bytes()
            data=dict(version=1,status='COMPLETE',stop_code=None,phase=phase,source=s,horizon=h,window=w,family=f,
                executable_freeze_sha256='f'*64,selection_freeze_sha256=selection_hash if f else None,
                source_identity={n:cfg[n] for n in ('sha256','bytes','record_count','native_unit')},
                resources=dict(elapsed_seconds=.1,peak_rss_bytes=10000,maximum_observed_os_threads=1,
                    thread_snapshot_count=1,thread_probe_status='PASS'),
                result=dict(status='COMPLETE',failure=None,candidate_rows=[],native_unit=cfg['native_unit'],
                    origin_identity=rep.origin_identity(int(origins[0]),int(origins[-1])),
                    selection=dict(status='SELECTED',parameter=parameter) if f else None,
                    summary_rows=summary,year_rows=annual,nonoverlap_rows=grid_rows,fit_diagnostics=diagnostics),
                artifacts=[dict(area='private',name='numeric-traces.npz',bytes=len(trace_raw),sha256=digest(trace_raw))])
            raw=raw_json(data);path=directory/'public/manifest.json';path.write_bytes(raw)
            queue.append(dict(phase=phase,source=s,horizon=h,window=w,family=f,status='COMPLETE',stop_code=None,
                exit_code=0,receipt_path=str(path.relative_to(root)),receipt_sha256=digest(raw)))
        queue_path=attempt/'evaluation-queue.json';queue_path.write_bytes(raw_json(dict(version=1,cells=queue)))
        archive=dict(spec=spec,selection=new_selection,executable_freeze_sha256='f'*64,selection_freeze_sha256='a'*64)
        helper_relative=rep.RESULTS+'/audit-builder-v01.py'
        helper_path=root/helper_relative;helper_path.parent.mkdir(parents=True,exist_ok=True)
        helper_path.write_bytes((Path(__file__).resolve().parent/helper_relative).read_bytes())
        fake_registry={}
        for name in ('evaluation-summary.csv','evaluation-annual.csv','evaluation-nonoverlap.csv',
                'paired-comparisons.csv','paired-annual.csv','paired-nonoverlap.csv'):
            name=rep.RESULTS+'/'+name;path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
            raw=b'id,metric\nold,0\n';path.write_bytes(raw);fake_registry[name]=(len(raw),digest(raw))
        class SyntheticGuard:
            def __init__(self,*args):self.resources={'synthetic_only':True}
            def __call__(self,**kwargs):pass
            def arrays(self,*args):pass
        archive_checks=[]
        def archive_checked(*args,**kwargs):
            archive_checks.append(1)
            if tamper_selection_at_finish and len(archive_checks)==2:
                changed=copy.deepcopy(new_selection);changed['created_utc']='2026-01-02T00:00:00Z'
                selection_path.write_bytes(raw_json(changed))
            return archive
        with (mock.patch.object(rep,'verify_archive',side_effect=archive_checked),
                mock.patch.object(rep,'replication_preflight'),
                mock.patch.object(helpers.runner,'verify_executable_freeze'),
                mock.patch.object(helpers.runner,'verify_selection_freeze',return_value=selected),
                mock.patch('conditional_sources.load_source',side_effect=lambda path,s,**kw:source_map[s]),
                mock.patch('run_study.RunGuard',SyntheticGuard),mock.patch.dict(rep.ARCHIVED_RESULTS,fake_registry)):
            if tamper_selection_at_finish:
                with self.assertRaisesRegex(rep.ReproductionError,'SELECTION_SNAPSHOT_HASH'):
                    adapter.reconcile(root,attempt,queue_path,(selection_path,selection_hash),archive,lambda:100.)
                self.assertFalse((attempt/'numerical-audit/public/reproduction-comparison.json').exists())
                return
            outcome=adapter.reconcile(root,attempt,queue_path,(selection_path,selection_hash),archive,lambda:100.)
        self.assertEqual(outcome['status'],'NUMERICAL_AUDIT_VERIFIED')
        self.assertFalse(outcome['exact_csv_scalar_agreement'])
        output=attempt/'numerical-audit/public'
        for name,count in (('evaluation-summary.csv',90),('evaluation-annual.csv',372),
                ('paired-comparisons.csv',98),('paired-annual.csv',388)):
            import csv
            with (output/name).open() as stream:self.assertEqual(len(list(csv.DictReader(stream))),count)
        comparison=rep.strict_json((output/'reproduction-comparison.json').read_bytes())
        self.assertFalse(comparison['exact_csv_byte_agreement'])
        self.assertEqual(len(comparison['receipts']),32)


@unittest.skipUnless(ADAPTER_AVAILABLE,'adapter RED: module absent')
class TightenedAuditAcceptanceTests(unittest.TestCase):
    def qr_record(self):
        numerator,denominator=float(.95).as_integer_ratio();grid=2**40
        return dict(refit_index=100,training_first_origin=79,training_last_origin=98,training_count=20,
            latest_label_end=100,primal_objective=0.,dual_objective=0.,duality_gap=0.,
            primal_residual=0.,dual_residual=0.,primal_tolerance=0.,dual_tolerance=0.,gap_tolerance=0.,
            iterations=1,dual_integer_lower=-((denominator-numerator)*grid//denominator),
            dual_integer_upper=numerator*grid//denominator,dual_integer_sum=0,dual_grid_denominator=grid)

    def test_valid_tightened_fit_record(self):
        adapter.verify_fit_records([self.qr_record()],{'refit_step':1},2,20,'QR',100,100)

    def test_invalid_qr_acceptance_diagnostics_rejected_by_adapter_itself(self):
        changes=[dict(iterations=0),dict(iterations=10001),dict(iterations=True),
            dict(primal_objective=float('nan')),dict(dual_objective=float('inf')),dict(primal_residual=-1.),
            dict(primal_objective=0.,dual_objective=-1.,duality_gap=0.),
            dict(dual_integer_lower=0),dict(dual_integer_upper=0),dict(dual_integer_sum=1),
            dict(dual_grid_denominator=2**41),dict(primal_residual=1.),dict(dual_residual=1.),
            dict(primal_objective=1.,duality_gap=1.),dict(latest_label_end=101),dict(training_count=19)]
        for change in changes:
            row=self.qr_record();row.update(change)
            with self.subTest(change=change),self.assertRaises(rep.ReproductionError):
                adapter.verify_fit_records([row],{'refit_step':1},2,20,'QR',100,100)

    def test_invalid_resource_types_limits_and_nonfinite_rejected(self):
        valid=dict(elapsed_seconds=.1,peak_rss_bytes=10000,maximum_observed_os_threads=1,
            thread_snapshot_count=1,thread_probe_status='PASS')
        adapter.verify_resource(valid)
        for change in (dict(elapsed_seconds=float('nan')),dict(elapsed_seconds=540.),dict(peak_rss_bytes=True),
                dict(peak_rss_bytes=1610612736),dict(maximum_observed_os_threads=3),
                dict(thread_snapshot_count=False),dict(thread_probe_status='UNVERIFIED')):
            value=valid|change
            with self.subTest(change=change),self.assertRaises(rep.ReproductionError):adapter.verify_resource(value)


@unittest.skipUnless(ADAPTER_AVAILABLE,'adapter RED: module absent')
class SelectionSnapshotTests(unittest.TestCase):
    def test_changed_timestamp_or_receipt_reference_rejected_with_original_expected_hash(self):
        temp=temporary_directory();self.addCleanup(temp.cleanup);root=Path(temp.name).resolve()
        attempt=root/'.scratch/revision-20261022/replication-selection';attempt.mkdir(parents=True)
        path=attempt/'selection-freeze.json'
        original=dict(created_utc='2026-01-01T00:00:00Z',cells=[dict(validation_receipts=[dict(path='one',sha256='a'*64)])])
        raw=raw_json(original);expected=digest(raw)
        for mutation in ('timestamp','reference'):
            changed=copy.deepcopy(original)
            if mutation=='timestamp':changed['created_utc']='2026-01-02T00:00:00Z'
            else:changed['cells'][0]['validation_receipts'][0]['sha256']='b'*64
            path.write_bytes(raw_json(changed))
            with self.subTest(mutation=mutation),self.assertRaisesRegex(rep.ReproductionError,'SELECTION_SNAPSHOT_HASH'):
                adapter.selection_snapshot(root,path,expected,attempt)


if __name__=='__main__':unittest.main()
