"""Synthetic-only integration checks for the separate AR replay runner."""
import copy
import csv
from datetime import datetime, timedelta
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import reproduce_conditional as rep
for _name in rep.THREAD_NAMES:__import__('os').environ[_name]='1'
import numpy as np
import reconcile_conditional_replication as adapter
from conditional_study import score_predictions, summarize_scores, nonoverlap_origins

from test_reproduce_conditional_diagnostics import SyntheticFixture

ROOT = Path(__file__).resolve().parent
AVAILABLE = importlib.util.find_spec('run_ar1_replay') is not None
if AVAILABLE:
    import run_ar1_replay as runner


def temporary_fixture():
    parent=ROOT/'.scratch/revision-20261022/ar1-runner-synthetic-tests'
    parent.mkdir(parents=True,exist_ok=True)
    return tempfile.TemporaryDirectory(dir=parent)


class SourceFixture(SyntheticFixture):
    """Generate raw bytes and source-consistent 32-cell receipts; no real values."""
    def values(self,source,count):
        return np.array([2.+(j%17)*.125+(j%3)*.03125 for j in range(count)])

    def write(self,path,raw):
        if str(path)==rep.SPEC_PATH:
            self.positions={};self.dates={}
            for s,cfg in self.spec['sources'].items():
                count=cfg['record_count'];values=self.values(s,count)
                start=datetime(2000,1,1);step=timedelta(hours=1) if s=='fx_hourly' else timedelta(days=7)
                dates=[start+j*step for j in range(count)]
                out=io.StringIO(newline='');writer=csv.writer(out,lineterminator='\n')
                writer.writerow(['datetime','NetPosUsd','NetUsdPnL','AbsVolume','Mid'] if s=='fx_hourly'
                    else ['As Of Date','Time Series','Value (millions)'])
                for d,v in zip(dates,values):
                    writer.writerow([d.strftime('%Y.%m.%dT%H:%M:%S.%f'),repr(float(v)),'0','0','1'] if s=='fx_hourly'
                        else [d.strftime('%Y-%m-%d'),'PDPOSGS-B',repr(float(v))])
                source_raw=out.getvalue().encode();cfg['input_relative_path']='.scratch/data/'+s+'.csv'
                cfg.update(bytes=len(source_raw),sha256=rep.sha(source_raw))
                super().write(cfg['input_relative_path'],source_raw)
                self.positions[s]=values;self.dates[s]=np.array(dates,dtype='datetime64[us]')
            raw=rep.json_bytes(self.spec)
        super().write(path,raw)

    def generated(self,shift,mutator,*,reconcile_metrics=False):
        def actual(cell,method,values):
            _,s,h,_,_=cell;ids=values['origins'];pos=self.positions[s]
            values['floor']=np.abs(pos[ids])
            values['peak']=np.array([max(abs(float(v)) for v in pos[t:t+h+1]) for t in ids])
            values['capacity']=values['floor']+(0.25 if method=='QR' else 0.5)
            if mutator:mutator(cell,method,values)
        generated=super().generated(shift,actual,reconcile_metrics=True)
        for queued in generated['queue']:
            receipt_path=self.root/queued['receipt_path'];receipt=rep.strict_json(receipt_path.read_bytes())
            s=queued['source'];h=queued['horizon'];year_rows=[];grid_rows=[]
            with np.load(receipt_path.parent.parent/'private/numeric-traces.npz',allow_pickle=False) as traces:
                for row in receipt['result']['summary_rows']:
                    m=row['method'];ids=traces[m+'_origins'];p=traces[m+'_peak'];b=traces[m+'_floor'];c=traces[m+'_capacity']
                    years=self.dates[s][ids].astype('datetime64[Y]').astype(int)+1970
                    for y in np.unique(years):
                        mask=years==y
                        year_rows.append(dict(method=m,parameter=row['parameter'],year=int(y))|
                            summarize_scores(score_predictions(p[mask],c[mask],b[mask],ids[mask])))
                    mask=np.isin(ids,nonoverlap_origins(int(ids[0]),int(ids[-1]),h))
                    grid_rows.append(dict(method=m,parameter=row['parameter'])|
                        summarize_scores(score_predictions(p[mask],c[mask],b[mask],ids[mask])))
            receipt['result'].update(year_rows=year_rows,nonoverlap_rows=grid_rows)
            raw=rep.json_bytes(receipt);self.write(receipt_path,raw);queued['receipt_sha256']=rep.sha(raw)
            name=(f'evaluation-{s}-h{h}-w{queued["window"]}-{queued["family"]}.json' if queued['family']
                else f'references-{s}-h{h}-w{queued["window"]}.json')
            generated['receipts'][name]=raw
        return generated


class EntryTests(unittest.TestCase):
    def test_explicit_entry_point_exists(self):
        self.assertTrue(AVAILABLE, 'separate AR replay runner is absent')

    @unittest.skipUnless(AVAILABLE, 'initial RED: entry point absent')
    def test_help_is_stdlib_only_and_requires_explicit_paths(self):
        script = ROOT/'run_ar1_replay.py'
        code = ("import runpy,sys; sys.argv=[sys.argv[1],'--help']\n"
                "try: runpy.run_path(sys.argv[0],run_name='__main__')\n"
                "except SystemExit as e: assert e.code==0\n"
                "assert 'numpy' not in sys.modules and 'conditional_sources' not in sys.modules\n"
                "assert 'ar1_replay' not in sys.modules\n")
        p = subprocess.run([sys.executable,'-B','-c',code,str(script)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('--replication-dir',p.stdout)
        self.assertIn('--attempt-id',p.stdout)
        missing = subprocess.run([sys.executable,'-B',str(script)],capture_output=True,text=True)
        self.assertEqual(missing.returncode,2)


@unittest.skipUnless(AVAILABLE, 'initial RED: entry point absent')
class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temp=temporary_fixture();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.f=SyntheticFixture(self.root)

    def prepare(self):
        return runner.prepare_replica(self.root,self.f.attempt,archive_contract=self.f.archive_contract)

    def test_actual_context_accepts_existing_diagnostics_without_touching_them(self):
        output=self.f.attempt/'post-result-diagnostics';output.mkdir()
        sentinel=output/'keep';sentinel.write_bytes(b'keep old diagnostics\n')
        inputs=self.prepare()
        self.assertEqual((len(inputs['queue']),len(inputs['selected'])),(32,24))
        self.assertEqual(inputs['selection_hash'],self.f.selection_hash)
        self.assertEqual(sentinel.read_bytes(),b'keep old diagnostics\n')
        self.assertFalse((self.f.attempt/'ar1-replay-new').exists())

    def test_controller_and_receipt_mutations_fail_in_real_validator(self):
        self.f.controller['accuracy_recomputed']=False;self.f.write_controller()
        with self.assertRaises(rep.ReproductionError):self.prepare()
        self.f.controller['accuracy_recomputed']=True;self.f.write_controller()
        path=self.root/self.f.queue[0]['receipt_path']
        path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(rep.ReproductionError):self.prepare()

    def test_selection_or_export_hash_change_rejected(self):
        path=self.f.attempt/'selection-freeze.json';raw=path.read_bytes()
        path.write_bytes(raw+b' ')
        with self.assertRaises(rep.ReproductionError):self.prepare()
        path.write_bytes(raw)
        export=self.f.attempt/'numerical-audit/public/evaluation-summary.csv'
        export.write_bytes(export.read_bytes()+b'\n')
        with self.assertRaises(rep.ReproductionError):self.prepare()

    def test_snapshot_readback_rejects_late_change(self):
        inputs=self.prepare()
        path=self.f.attempt/'controller-final.json';path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(rep.ReproductionError):runner.verify_inputs(inputs)


@unittest.skipUnless(AVAILABLE, 'initial RED: entry point absent')
class SourceAndTraceTests(unittest.TestCase):
    def setUp(self):
        self.temp=temporary_fixture();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.f=SourceFixture(self.root)
        self.inputs=runner.prepare_replica(self.root,self.f.attempt,archive_contract=self.f.archive_contract)

    def test_actual_local_loader_and_all_32_npz_audits_keep_exact_24_references(self):
        sources=runner.load_sources(self.inputs)
        self.assertEqual(set(sources),{'fx_hourly','nyfed_weekly'})
        self.assertFalse(sources['fx_hourly'].position.flags.writeable)
        helper=adapter._load_helpers(ROOT)
        refs,receipts=runner.audit_references(self.inputs,sources,np,helper)
        self.assertEqual(len(receipts),32);self.assertEqual(len(refs),24)
        self.assertEqual({key[-1] for key in refs},{'frozen_S','frozen_F','QR'})
        for (s,h,w,m),score in refs.items():
            np.testing.assert_array_equal(score.floors,np.abs(self.f.positions[s][score.origins]))
        runner.verify_inputs(self.inputs)

    def test_same_source_hash_symlink_and_private_npz_change_refused(self):
        cfg=self.f.spec['sources']['fx_hourly'];path=self.root/cfg['input_relative_path']
        original=path.read_bytes();path.write_bytes(original+b' ')
        with self.assertRaises(Exception):runner.load_sources(self.inputs)
        path.write_bytes(original);target=path.with_suffix('.other');path.rename(target);path.symlink_to(target)
        with self.assertRaises(rep.ReproductionError):runner.load_sources(self.inputs)
        path.unlink();target.rename(path)
        sources=runner.load_sources(self.inputs)
        q=self.f.queue[0];npz=(self.root/q['receipt_path']).parent.parent/'private/numeric-traces.npz'
        npz.write_bytes(npz.read_bytes()+b' ')
        with self.assertRaises(rep.ReproductionError):
            runner.audit_references(self.inputs,sources,np,adapter._load_helpers(ROOT))

    def test_actual_native_model_keeps_refit_and_query_separate(self):
        sources=runner.load_sources(self.inputs);source=sources['fx_hourly']
        cfg=self.f.spec['sources']['fx_hourly']
        rows,trace,fit_rows,failure=runner.run_cell(source,cfg,6,720)
        self.assertIsNone(failure);self.assertEqual(len(trace['capacity']),4)
        self.assertEqual([r['refit_index'] for r in fit_rows],[10000,10002])
        self.assertEqual([r['transition_count'] for r in fit_rows],[725,725])
        np.testing.assert_array_equal(trace['refit_indices'],[10000,10000,10002,10002])
        self.assertEqual(rows['origin_count'],4)
        import ar1_replay as ar
        expected=[]
        for t in range(10000,10004):
            r=10000+(t-10000)//2*2
            history=ar.prepare_ar1_history(source.position,r,6,720)
            expected.append(ar.predict(history,float(source.position[t])))
        np.testing.assert_array_equal(trace['capacity'],expected)


def freeze_fixture(f):
    for name in runner.DEPENDENCIES+runner.TEST_FILES:
        f.write(name,(ROOT/name).read_bytes())
    design='protocol/revision-20261022/ar1-replay-design.md';f.write(design,b'# Synthetic-only AR design\n')
    spec=dict(version=1,experiment='AR1_REPLAY_EXPLORATORY_V1',design=dict(path=design,bytes=26,
        sha256=rep.sha((f.root/design).read_bytes())),
        original_executable_freeze_sha256=f.freeze,original_selection_sha256=f.selection_old,
        method='AR1_REPLAY',comparators=['frozen_S','frozen_F','QR'],
        cells=[dict(source=s,horizon=h,window=w) for s,cfg in f.spec['sources'].items()
            for h in f.spec['horizons'] for w in cfg['windows']],
        resources=dict(wall_seconds=540,hard_seconds=600,rss_bytes=1610612736,
            requested_threads=1,maximum_observed_os_threads=2),
        numerical_contract=copy.deepcopy(runner.NUMERICAL_CONTRACT),
        dependencies={name:dict(bytes=len((f.root/name).read_bytes()),sha256=rep.sha((f.root/name).read_bytes()))
            for name in runner.DEPENDENCIES})
    spec['design']['bytes']=len((f.root/design).read_bytes())
    f.write(runner.SPEC_PATH,rep.json_bytes(spec))
    files=list(runner.DEPENDENCIES)+list(runner.TEST_FILES)+[design,runner.SPEC_PATH]
    frozen=dict(version=1,status='FROZEN',created_utc='2026-01-01T00:00:00Z',spec_path=runner.SPEC_PATH,
        spec_sha256=rep.sha((f.root/runner.SPEC_PATH).read_bytes()),
        files={n:rep.sha((f.root/n).read_bytes()) for n in files})
    f.write(runner.FREEZE_PATH,rep.json_bytes(frozen))
    return spec,frozen


class Guard:
    def __init__(self,*args):
        self.resources=dict(elapsed_seconds=.1,peak_rss_bytes=100000,maximum_observed_os_threads=1,
            thread_snapshot_count=1,thread_probe_status='PASS',requested_numerical_threads=1)
    def __call__(self,**kwargs):self.resources.update(current_stage=kwargs.get('stage'))
    def arrays(self,*args):pass


@unittest.skipUnless(AVAILABLE, 'initial RED: entry point absent')
class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp=temporary_fixture();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.f=SourceFixture(self.root)

    def execute(self,**kwargs):
        return runner.execute(self.root,self.f.attempt,'synthetic-new',archive_contract=self.f.archive_contract,
            guard_factory=Guard,**kwargs)

    def test_full_actual_synthetic_entry_keeps_8_24_and_refuses_overwrite(self):
        freeze_fixture(self.f)
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result=self.execute()
        self.assertEqual(result['status'],'AR1_REPLAY_COMPLETE')
        self.assertEqual((result['summary_rows'],result['paired_rows'],result['audited_original_cells']),(8,24,32))
        self.assertEqual(result['complete_cells'],8);self.assertEqual(result['failed_cells'],0)
        self.assertEqual(len(result['cell_receipts']),8)
        self.assertEqual(result['source_snapshots_read'],2)
        for relative,raw in before.items():self.assertEqual((self.root/relative).read_bytes(),raw)
        out=self.f.attempt/'ar1-replay-synthetic-new/public'
        rows=list(csv.DictReader(io.StringIO((out/'ar1-paired.csv').read_text())))
        self.assertEqual(len(rows),24);self.assertEqual({r['status'] for r in rows},{'COMPLETE'})
        self.assertEqual({r['right_method'] for r in rows},{'frozen_S','frozen_F','QR'})
        with self.assertRaises(rep.ReproductionError):self.execute()

    def test_wrong_new_freeze_dependency_or_cell_inventory_cannot_execute(self):
        spec,frozen=freeze_fixture(self.f)
        self.f.write('ar1_replay.py',(self.root/'ar1_replay.py').read_bytes()+b'\n')
        with self.assertRaises(rep.ReproductionError):self.execute()
        self.assertFalse((self.f.attempt/'ar1-replay-synthetic-new').exists())
        freeze_fixture(self.f)
        spec=rep.strict_json((self.root/runner.SPEC_PATH).read_bytes());spec['cells'].reverse()
        self.f.write(runner.SPEC_PATH,rep.json_bytes(spec))
        frozen=rep.strict_json((self.root/runner.FREEZE_PATH).read_bytes())
        digest=rep.sha((self.root/runner.SPEC_PATH).read_bytes());frozen['spec_sha256']=digest
        frozen['files'][runner.SPEC_PATH]=digest;self.f.write(runner.FREEZE_PATH,rep.json_bytes(frozen))
        with self.assertRaises(rep.ReproductionError) as caught:self.execute()
        self.assertEqual(caught.exception.code,'AR1_SPEC_CONTRACT')

    def test_production_rejects_test_guard_before_source_access(self):
        with self.assertRaises(rep.ReproductionError) as caught:
            runner.execute(ROOT,'.scratch/revision-20261022/replication-ABSENT','new',guard_factory=Guard)
        self.assertEqual(caught.exception.code,'TEST_ONLY_GUARD')

    def test_spec_snapshot_cannot_change_between_parse_and_freeze_file_check(self):
        spec,frozen=freeze_fixture(self.f)
        path=self.root/runner.SPEC_PATH;initial=path.read_bytes();changed=initial+b' '
        # A deliberately inconsistent synthetic freeze cannot authorize parsing
        # one specification snapshot and hashing another in the same attempt.
        frozen['files'][runner.SPEC_PATH]=rep.sha(changed)
        self.f.write(runner.FREEZE_PATH,rep.json_bytes(frozen))
        read=rep.read_bytes;seen=0
        def changing(root,relative,**kwargs):
            nonlocal seen
            raw=read(root,relative,**kwargs)
            if Path(relative)==Path(runner.SPEC_PATH):
                seen+=1
                if seen==1:path.write_bytes(changed)
            return raw
        inputs=runner.prepare_replica(self.root,self.f.attempt,archive_contract=self.f.archive_contract)
        with patch.object(rep,'read_bytes',side_effect=changing):
            with self.assertRaises(rep.ReproductionError) as caught:runner.verify_execution(inputs)
        self.assertEqual(caught.exception.code,'INPUT_SNAPSHOT_CHANGED')

    def test_native_failure_retains_prefix_without_shortened_metric(self):
        values=np.arange(150,dtype=float);values[102]=1e308
        cfg=dict(evaluation_origin_first=100,evaluation_origin_last=103,refit_step=2)
        summary,trace,fits,failure=runner.run_cell(types.SimpleNamespace(position=values),cfg,6,52)
        self.assertIsNone(summary);self.assertEqual(len(trace['capacity']),2)
        self.assertEqual(failure['completed_origins'],2);self.assertEqual(failure['expected_origins'],4)
        self.assertNotIn('pinball',trace);self.assertEqual(len(fits),1)

    def test_resource_cadence_covers_each_refit_and_maximum128_issue_gap(self):
        import ar1_replay as ar
        source=types.SimpleNamespace(position=np.array([2.+(j%17)*.125 for j in range(900)]))
        cfg=dict(evaluation_origin_first=400,evaluation_origin_last=700,refit_step=170)
        checks=[];array_checks=[]
        summary,trace,fits,failure=runner.run_cell(source,cfg,6,52,
            checkpoint=lambda **kw:checks.append(kw),arrays=lambda *values:array_checks.append(values))
        self.assertIsNone(failure);self.assertEqual(summary['origin_count'],301)
        positions=[r['completed_origins'] for r in checks]
        self.assertEqual(positions,[0,128,170,256,301])
        self.assertTrue(all(b-a<=128 for a,b in zip(positions,positions[1:])))
        self.assertEqual([r['refit_index']-400 for r in fits],[0,170])
        self.assertEqual(len(array_checks),5)
        self.assertTrue(all(len(args)==2 for args in array_checks[:-1]))
        histories={r:ar.prepare_ar1_history(source.position,r,6,52) for r in (400,570)}
        expected=[ar.predict(histories[400+(t-400)//170*170],float(source.position[t])) for t in range(400,701)]
        np.testing.assert_array_equal(trace['capacity'],expected)

    def test_known_paired_arithmetic_zero_denominator_and_global_grid(self):
        origins=np.arange(8,dtype=np.int64);floor=np.zeros(8);peak=np.ones(8)
        left=score_predictions(peak,np.array([1.,2.,1.,2.,1.,2.,1.,2.]),floor,origins)
        right=score_predictions(peak,np.ones(8),floor,origins)
        dates=np.array(['2020-12-28','2020-12-29','2020-12-30','2020-12-31',
            '2021-01-01','2021-01-02','2021-01-03','2021-01-04'],dtype='datetime64[D]')
        found=runner.describe_pair(left,right,dates,horizon=2)
        self.assertAlmostEqual(found['all']['mean_pinball_difference'],.025)
        self.assertIsNone(found['all']['relative_mean_loss_difference_percent'])
        self.assertEqual(found['all']['relative_difference_undefined_reason'],'ZERO_REFERENCE_MEAN_LOSS')
        self.assertEqual(found['nonoverlap']['origin_count'],3)
        self.assertEqual(found['nonoverlap']['last_source_index'],6)

    def test_all_failed_cells_keep_full_inventory_with_blank_accuracy(self):
        class Constants(SourceFixture):
            def values(self,source,count):
                return np.ones(count) if source=='nyfed_weekly' else super().values(source,count)
        other=self.root/'constant';other.mkdir();fixture=Constants(other);freeze_fixture(fixture)
        result=runner.execute(other,fixture.attempt,'all-failures',archive_contract=fixture.archive_contract,guard_factory=Guard)
        self.assertEqual(result['status'],'AR1_REPLAY_WITH_FAILURES')
        self.assertEqual((result['complete_cells'],result['failed_cells']),(4,4))
        out=fixture.attempt/'ar1-replay-all-failures/public'
        summaries=list(csv.DictReader(io.StringIO((out/'ar1-summary.csv').read_text())))
        pairs=list(csv.DictReader(io.StringIO((out/'ar1-paired.csv').read_text())))
        self.assertEqual((len(summaries),len(pairs)),(8,24))
        for row in summaries:
            if row['source']=='nyfed_weekly':
                self.assertEqual(row['status'],'FAILED');self.assertEqual(row['mean_pinball'],'')
                self.assertEqual(row['completed_origin_count'],'0');self.assertEqual(row['origin_count'],'')
        failed=[r for r in pairs if r['source']=='nyfed_weekly']
        self.assertEqual(len(failed),12)
        for row in failed:
            self.assertEqual(row['mean_pinball_difference'],'')
            self.assertEqual(row['relative_difference_undefined_reason'],'AR1_CELL_FAILED')

    def test_late_input_and_private_or_public_output_mutation_refused(self):
        for target in ('input','public','private'):
            with self.subTest(target=target):
                base=self.root/target;base.mkdir();fixture=SourceFixture(base);freeze_fixture(fixture)
                class Mutating(Guard):
                    def __init__(inner,start,utc,attempt,public,private):
                        super().__init__();inner.public=public;inner.private=private
                    def __call__(inner,*,stage=None,**kwargs):
                        super().__call__(stage=stage,**kwargs)
                        if stage=='ar1_final_readback':
                            path=(fixture.attempt/'controller-final.json' if target=='input' else
                                inner.public/'ar1-summary.csv' if target=='public' else
                                next(inner.private.glob('*-traces.npz')))
                            path.write_bytes(path.read_bytes()+b' ')
                with self.assertRaises(rep.ReproductionError):
                    runner.execute(base,fixture.attempt,'mutation',archive_contract=fixture.archive_contract,guard_factory=Mutating)
                output=fixture.attempt/'ar1-replay-mutation/public'
                self.assertFalse((output/'ar1-replay-manifest.json').exists())
                self.assertEqual(rep.strict_json((output/'ar1-failure.json').read_bytes())['status'],'STOPPED')

    def test_resource_stop_keeps_completed_cell_without_acceptance(self):
        freeze_fixture(self.f)
        class Stopping(Guard):
            def __call__(self,*,stage=None,**kwargs):
                super().__call__(stage=stage,**kwargs)
                if stage=='ar1_cell_retained':raise rep.ReproductionError('RESOURCE_WALL')
        with self.assertRaises(rep.ReproductionError):
            runner.execute(self.root,self.f.attempt,'stopped',archive_contract=self.f.archive_contract,guard_factory=Stopping)
        out=self.f.attempt/'ar1-replay-stopped/public'
        self.assertFalse((out/'ar1-replay-manifest.json').exists())
        failure=rep.strict_json((out/'ar1-failure.json').read_bytes())
        self.assertEqual(failure['stop_code'],'RESOURCE_WALL');self.assertEqual(len(failure['retained_cell_receipts']),1)
        self.assertEqual(len(failure['unretained_cells']),7)

    @unittest.skipUnless(__import__('platform').system()=='Darwin','measured resource contract is Darwin-only')
    def test_synthetic_execution_with_real_resource_guard(self):
        freeze_fixture(self.f)
        result=runner.execute(self.root,self.f.attempt,'real-resource',archive_contract=self.f.archive_contract)
        measured=result['resources']
        self.assertTrue(0<measured['peak_rss_bytes']<1610612736)
        self.assertTrue(1<=measured['maximum_observed_os_threads']<=2)
        self.assertGreater(measured['thread_snapshot_count'],0)
        self.assertEqual(measured['current_stage'],'ar1_verified_before_manifest')


if __name__=='__main__':unittest.main()
