"""Artificial scalar/metadata checks only; no financial file or fit is used."""
import copy
import contextlib
from fractions import Fraction
import io
import math
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import reproduce_conditional as rep
import verify_ar1_output as audit


def fixture():
    configs={s:dict(native_unit='USD' if s=='fx_hourly' else 'USD million',
        evaluation_origin_first=3000,evaluation_origin_last=3004,refit_step=2,
        sha256='a'*64,bytes=100,record_count=4000)
        for s in ('fx_hourly','nyfed_weekly')}
    cells=[dict(source=s,horizon=h,window=w) for s in configs for h in (6,24)
        for w in ((720,2880) if s=='fx_hourly' else (52,260))]
    selected={(c['source'],c['horizon'],c['window'],'QR'):dict(parameter=.01) for c in cells}
    years={s:['2000','2001'] for s in configs}
    tables={n:[] for n in ('ar1-summary.csv','ar1-annual.csv','ar1-nonoverlap.csv',
        'ar1-paired.csv','ar1-paired-annual.csv','ar1-paired-nonoverlap.csv')}
    for cell in cells:
        s,h,w=(cell[k] for k in ('source','horizon','window'))
        base=dict(source=s,native_unit=configs[s]['native_unit'],horizon=str(h),window=str(w),
            refit_step='2',status='COMPLETE',stop_code='')
        for name in tables:
            pair='paired' in name
            for method in (('frozen_S','frozen_F','QR') if pair else (None,)):
                for year in (years[s] if 'annual' in name else (None,)):
                    row=base.copy()
                    if pair:row.update(left_method='AR1_REPLAY',right_method=method,
                        right_parameter='0.01' if method=='QR' else '',
                        contrast_role='DIRECT_S' if method=='frozen_S' else 'CONTEXT')
                    else:row['method']='AR1_REPLAY'
                    if year is not None:row['calendar_year']=year
                    if 'nonoverlap' in name:row['stride_records']=str(h+1)
                    if name=='ar1-summary.csv':row.update(expected_origin_count='5',completed_origin_count='5')
                    tables[name].append(row)
    return tables,cells,configs,selected,years


def zero_row():
    return dict(origin_count='1',mean_pinball='0',mean_capacity='1',mean_extra_allowance='0',
        mean_positive_overrun='0',mean_unused_allowance='0',strict_breach_count='0',
        conditional_overrun_denominator='0',strict_breach_rate='0',conditional_mean_overrun='',
        conditional_overrun_undefined_reason='NO_STRICT_BREACHES')


class TableInventoryTests(unittest.TestCase):
    def test_legacy_checks_accept_a_mislabeled_numeric_row(self):
        # Direct demonstration of the previous checker, not a mock of it.
        row=zero_row()|dict(method='WRONG',native_unit='wrong',status='FAILED',refit_step='999')
        audit.check_summary(row,audit.scalar_scores([1.],[1.],[1.]),[0])

    def test_legacy_row_count_loop_cannot_detect_repeated_paired_method(self):
        args=fixture();rows=args[0]['ar1-paired.csv']
        rows[1]=rows[0].copy()  # Omit F and repeat S without changing 24 rows.
        self.assertEqual(len(rows),24)
        numeric=ArithmeticTests().pair(1.,1.);scores=ArithmeticTests().scores(1.)
        checked=0
        for cell in args[1]:
            for row in rows:
                if (row['source'],int(row['horizon']),int(row['window']))==(
                        cell['source'],cell['horizon'],cell['window']):
                    audit.check_pair(row|numeric,scores,scores,[0],[7]);checked+=1
        self.assertEqual(checked,24)  # Previous main's count and score logic pass.
        with self.assertRaises(rep.ReproductionError):audit.verify_table_inventory(*args)

    def test_exact_declared_inventory_is_accepted(self):
        args=fixture()
        audit.verify_table_inventory(*args)

    def test_duplicate_and_omission_preserving_total_count_are_rejected(self):
        for name in fixture()[0]:
            with self.subTest(name=name):
                args=fixture();tables=args[0]
                tables[name][1]=tables[name][0].copy()
                with self.assertRaises(rep.ReproductionError):audit.verify_table_inventory(*args)

    def test_labels_are_bound_to_current_cell_selection_and_units(self):
        for table,field,value in (('ar1-summary.csv','method','OTHER'),
                ('ar1-summary.csv','native_unit','wrong'),('ar1-annual.csv','status','FAILED'),
                ('ar1-annual.csv','stop_code','SILENT'),('ar1-summary.csv','refit_step','3'),
                ('ar1-summary.csv','expected_origin_count','4'),
                ('ar1-summary.csv','completed_origin_count','4'),
                ('ar1-nonoverlap.csv','stride_records','6'),
                ('ar1-paired.csv','left_method','OTHER'),
                ('ar1-paired.csv','contrast_role','CONTEXT'),
                ('ar1-paired-nonoverlap.csv','right_parameter','.1')):
            with self.subTest(table=table,field=field):
                args=fixture();args[0][table][0][field]=value
                with self.assertRaises(rep.ReproductionError):audit.verify_table_inventory(*args)

    def test_qr_parameter_and_calendar_year_are_checked(self):
        for field,value in (('right_parameter','.1'),('calendar_year','2099')):
            args=fixture();row=next(r for r in args[0]['ar1-paired-annual.csv'] if r['right_method']=='QR')
            row[field]=value
            with self.assertRaises(rep.ReproductionError):audit.verify_table_inventory(*args)


class ArithmeticTests(unittest.TestCase):
    def pair(self,left,right):
        difference=left-right
        return dict(origin_count='1',first_source_index='7',last_source_index='7',
            mean_pinball_left=str(left),mean_pinball_right=str(right),mean_pinball_difference=str(difference),
            relative_mean_loss_difference_percent=str(100*(difference/right)) if right else '',
            relative_difference_undefined_reason='' if right else 'ZERO_REFERENCE_MEAN_LOSS',
            mean_capacity_difference='0',mean_positive_overrun_difference='0',
            mean_unused_allowance_difference='0',strict_breach_count_left='0',strict_breach_count_right='0')

    def scores(self,loss):
        return dict(loss=[loss],capacity=[1.],over=[0.],unused=[0.],breach=[False])

    def test_relative_quotient_avoids_false_intermediate_overflow(self):
        audit.check_pair(self.pair(1e308,5e307),self.scores(1e308),self.scores(5e307),[0],[7])

    def test_undefined_reason_is_checked_for_finite_and_zero_reference(self):
        for left,right in ((2.,1.),(0.,0.)):
            row=self.pair(left,right);row['relative_difference_undefined_reason']='WRONG'
            with self.assertRaises(rep.ReproductionError):
                audit.check_pair(row,self.scores(left),self.scores(right),[0],[7])

    def test_true_nonfinite_relative_difference_has_fixed_reason(self):
        row=self.pair(1.,1.);row.update(mean_pinball_left='1e308',mean_pinball_right='1e-308',
            mean_pinball_difference='1e308',relative_mean_loss_difference_percent='',
            relative_difference_undefined_reason='RELATIVE_DIFFERENCE_NOT_FINITE')
        audit.check_pair(row,self.scores(1e308),self.scores(1e-308),[0],[7])

    def test_breach_reason_must_be_empty_for_defined_conditional_mean(self):
        row=zero_row()|dict(mean_pinball='.95',mean_positive_overrun='1',strict_breach_count='1',
            conditional_overrun_denominator='1',strict_breach_rate='1',conditional_mean_overrun='1',
            conditional_overrun_undefined_reason='WRONG')
        with self.assertRaises(rep.ReproductionError):
            audit.check_summary(row,audit.scalar_scores([2.],[1.],[1.]),[0])

    def test_fraction_oracle_preserves_represented_high_offset_inputs(self):
        for changes,expected in (([0,0,1,0,1,2],Fraction(1,3)),([0,1,0,1,1,0],Fraction(-2,3))):
            phi,c=audit.exact_ols([2.**52+x for x in changes])
            self.assertEqual(phi,float(expected));self.assertTrue(math.isfinite(c))

    def test_scalar_recursion_reads_no_values_after_refit(self):
        class Limited:
            def __getitem__(self,index):
                if index>21:raise AssertionError('future value used')
                return float(index%3)
        fit=dict(phi=.5,c=.25,first_origin=2)
        self.assertTrue(math.isfinite(audit.scalar_replay(Limited(),fit,1,19,2.)))


class ArtifactTests(unittest.TestCase):
    def test_exact_export_inventory_rejects_missing_duplicate_and_unknown_names(self):
        cells=fixture()[1]
        public=[dict(path=n,bytes=1,sha256='a'*64) for n in fixture()[0]]
        private=[]
        for c in cells:
            stem=f'{c["source"]}-h{c["horizon"]}-w{c["window"]}'
            public.append(dict(path=stem+'-receipt.json',bytes=1,sha256='a'*64))
            private.extend(dict(path=stem+s,bytes=1,sha256='a'*64) for s in ('-fits.json','-traces.npz'))
        audit.verify_export_inventory(public,private,cells)
        for entries,kind in ((public,'public'),(private,'private')):
            for mutation in ('omit','duplicate','unknown'):
                p,q=copy.deepcopy(public),copy.deepcopy(private);target=p if kind=='public' else q
                if mutation=='omit':target.pop()
                elif mutation=='duplicate':target[-1]=target[0].copy()
                else:target[0]['path']='unexpected'
                with self.assertRaises(rep.ReproductionError):audit.verify_export_inventory(p,q,cells)

    def test_csv_parser_uses_the_verified_byte_snapshot(self):
        raw=b'a,b\n1,2\n'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();dest=root/'attempt';(dest/'public').mkdir(parents=True)
            path=dest/'public/table.csv';path.write_bytes(raw)
            entry=dict(path='table.csv',bytes=len(raw),sha256=rep.sha(raw))
            real_read=rep.read_bytes
            def changed(*args,**kwargs):
                found=real_read(*args,**kwargs);path.write_text('a,b\n9,9\n');return found
            with patch.object(rep,'read_bytes',side_effect=changed):
                got=audit.load_verified_csv(root,dest,entry)
            self.assertEqual(got,[dict(a='1',b='2')])

    def test_main_rejects_missing_export_before_source_access(self):
        args=ProvenanceTests().context();manifest,execution,inputs,_,_=args
        manifest.update(exports=[],private_exports=[])
        with patch.object(audit.runner,'prepare_replica',return_value=inputs), \
                patch.object(audit.runner,'verify_execution',return_value=execution), \
                patch.object(audit.rep,'read_bytes',return_value=rep.json_bytes(manifest)), \
                patch.object(audit.runner,'load_sources',side_effect=AssertionError('source accessed')) as loader, \
                patch.object(audit.signal,'signal'),patch.object(audit.signal,'setitimer'):
            with self.assertRaises(rep.ReproductionError):
                audit.main(['--replication-dir','unused','--attempt-id','synthetic','--output','unused'])
        loader.assert_not_called()


def fit_fixture():
    cell=fixture()[1][0];cfg=fixture()[2][cell['source']];h,w=cell['horizon'],cell['window']
    rows=[]
    for r in (3000,3002,3004):
        rows.append(dict(refit_index=r,first_origin=r-h-w+1,last_origin=r-h,horizon=h,window=w,
            rank=(19*(w+1)+19)//20,phi=.5,c=1.,scale=2.,transition_count=w+h-1,
            scaled_mean_residual=0.,scaled_regressor_residual=0.,normal_tolerance=1e-10,
            scaled_x_mean=1.,scaled_y_mean=1.,scaled_x_variance=.25))
    return dict(version=1,cell=cell,status='COMPLETE',fit_records=rows,failure=None),cell,cfg,[3000,3002,3004]


class FitInventoryTests(unittest.TestCase):
    def test_all_fit_metadata_are_checked_without_new_fit(self):
        args=fit_fixture();self.assertEqual(list(audit.verify_fit_inventory(*args)),args[-1])

    def test_duplicate_fits_cannot_disappear_in_dict_conversion(self):
        args=fit_fixture();args[0]['fit_records'].insert(1,args[0]['fit_records'][0].copy())
        with self.assertRaises(rep.ReproductionError):audit.verify_fit_inventory(*args)

    def test_wrong_cell_maturity_rank_or_numerical_metadata_fail(self):
        for field,value in (('first_origin',3001),('last_origin',3001),('rank',1),('horizon',24),
                ('transition_count',1),('phi',math.inf),('scaled_x_variance',0.),
                ('scaled_mean_residual',1.),('normal_tolerance',-1.)):
            args=fit_fixture();args[0]['fit_records'][1][field]=value
            with self.subTest(field=field),self.assertRaises(rep.ReproductionError):
                audit.verify_fit_inventory(*args)

    def test_derived_phi_summary_is_bound_to_all_retained_fits(self):
        fits=fit_fixture()[0]['fit_records']
        row=dict(completed_refit_count='3',phi_min='.5',phi_max='.5',phi_mean='.5',
            phi_below_zero='0',phi_exactly_one='0',phi_above_one='0')
        audit.check_fit_summary(row,fits)
        for field,value in (('completed_refit_count','2'),('phi_mean','.6'),('phi_above_one','1')):
            with self.subTest(field=field),self.assertRaises(rep.ReproductionError):
                audit.check_fit_summary(row|{field:value},fits)


class ProvenanceTests(unittest.TestCase):
    def context(self):
        tables,cells,configs,selected,years=fixture()
        execution=dict(spec=dict(cells=cells),spec_sha256='b'*64,freeze_sha256='c'*64)
        inputs=dict(attempt=Path('/synthetic/replica'),root=Path('/synthetic'),
            archive=dict(executable_freeze_sha256='d'*64,selection_freeze_sha256='e'*64),
            selection_hash='f'*64,spec=dict(sources=configs))
        manifest=dict(version=1,status='AR1_REPLAY_COMPLETE',analysis_status='POST_RESULT_EXPLORATORY',
            method='AR1_REPLAY',original_primaries_changed=False,original_models_refitted=False,
            new_parameter_selection=False,all_cells_complete=True,complete_cells=8,failed_cells=0,
            summary_rows=8,paired_rows=24,annual_rows=16,paired_annual_rows=48,
            nonoverlap_rows=8,paired_nonoverlap_rows=24,audited_original_cells=32,source_snapshots_read=2,
            replication_dir='replica',attempt_id='synthetic',ar1_spec_sha256='b'*64,ar1_freeze_sha256='c'*64,
            original_executable_freeze_sha256='d'*64,archived_selection_sha256='e'*64,new_selection_sha256='f'*64)
        return manifest,execution,inputs,'synthetic',years

    def test_manifest_labels_and_selection_chain_are_verified(self):
        args=self.context();audit.verify_manifest_context(*args)
        for field,value in (('method','OTHER'),('new_selection_sha256','0'*64),('replication_dir','other'),
                ('attempt_id','other'),('all_cells_complete',False),('original_models_refitted',True),
                ('annual_rows',32),('complete_cells',True)):
            bad=copy.deepcopy(args);bad[0][field]=value
            with self.subTest(field=field),self.assertRaises(rep.ReproductionError):
                audit.verify_manifest_context(*bad)

    def test_cell_receipt_cannot_point_to_different_inputs_or_private_files(self):
        _,execution,inputs,_,_=self.context();cell=execution['spec']['cells'][0];s=cell['source']
        artifacts=[dict(path=a,bytes=10,sha256='a'*64) for a in ('fits.json','traces.npz')]
        row=dict(version=1,cell=cell,method='AR1_REPLAY',status='COMPLETE',stop_code=None,
            expected_origin_count=5,completed_origin_count=5,fit_count=3,
            source_identity={k:inputs['spec']['sources'][s][k] for k in ('sha256','bytes','record_count','native_unit')},
            new_selection_sha256='f'*64,ar1_spec_sha256='b'*64,ar1_freeze_sha256='c'*64,private_artifacts=artifacts)
        audit.verify_cell_receipt(row,cell,inputs,execution,artifacts,3)
        for field,value in (('method','OTHER'),('fit_count',2),('new_selection_sha256','0'*64),
                ('private_artifacts',[]),('source_identity',{})):
            with self.subTest(field=field),self.assertRaises(rep.ReproductionError):
                audit.verify_cell_receipt(row|{field:value},cell,inputs,execution,artifacts,3)


class MainWiringTests(unittest.TestCase):
    def test_complete_eight_cell_scalar_fixture_runs_main_without_any_model_fit(self):
        # The only injected boundary is preverified replica/source loading. All
        # new guards, exact OLS, recursion, artifact reads and CSV checks execute.
        for name in rep.THREAD_NAMES:__import__('os').environ[name]='1'
        import numpy as np
        from conditional_study import score_predictions,summarize_scores,paired_comparison
        from reconcile_conditional_replication import csv_bytes
        from run_study import RunGuard
        root=Path(__file__).resolve().parent
        scratch=root/'.scratch/revision-20261022/ar1-auditor-synthetic-tests'
        scratch.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            attempt=Path(tmp);destination=attempt/'ar1-replay-synthetic'
            public=destination/'public';private=destination/'private';public.mkdir(parents=True);private.mkdir()
            _,execution,inputs,_,_=ProvenanceTests().context()
            inputs.update(root=root,attempt=attempt,snapshots={})
            configs=inputs['spec']['sources']
            for cfg in configs.values():cfg.update(evaluation_origin_first=40,evaluation_origin_last=44)
            cells=[dict(source=s,horizon=h,window=w) for s in configs for h in (1,2) for w in (19,20)]
            execution['spec']['cells']=cells
            inputs['selected']={(c['source'],c['horizon'],c['window'],'QR'):dict(parameter=.01) for c in cells}
            origins=np.arange(40,45,dtype=np.int64)
            position=np.array([float(j%7)+.125*(j%3) for j in range(50)])
            dates=np.array(['1999-01-01']*50,dtype='datetime64[D]')
            dates[40:45]=np.array(['2000-01-01','2001-01-01','2002-01-01','2003-01-01','2003-01-02'],dtype='datetime64[D]')
            sources={s:types.SimpleNamespace(position=position,dates=dates) for s in configs}
            tables={name:[] for name in audit.TABLE_NAMES};exports=[];private_exports=[];receipts=[];references={}
            def write(area,name,raw):
                (destination/area/name).write_bytes(raw)
                entry=dict(path=name,bytes=len(raw),sha256=rep.sha(raw))
                (exports if area=='public' else private_exports).append(entry);return entry
            for cell in cells:
                s,h,w=(cell[k] for k in ('source','horizon','window'));stem=audit.cell_stem(cell)
                fit_rows=[]
                for r in (40,42,44):
                    phi,c=audit.exact_ols(position[r-h-w+1:r+1])
                    fit_rows.append(dict(refit_index=r,first_origin=r-h-w+1,last_origin=r-h,horizon=h,window=w,
                        rank=(19*(w+1)+19)//20,transition_count=w+h-1,phi=phi,c=c,scale=8.,
                        scaled_mean_residual=0.,scaled_regressor_residual=0.,normal_tolerance=1e-10,
                        scaled_x_mean=1.,scaled_y_mean=1.,scaled_x_variance=.25))
                by_refit={f['refit_index']:f for f in fit_rows};refits=np.array([40,40,42,42,44],dtype=np.int64)
                caps=np.array([audit.scalar_replay(position,by_refit[int(r)],h,w,float(position[t]))
                    for t,r in zip(origins,refits)])
                peak=np.array([max(abs(float(v)) for v in position[t:t+h+1]) for t in origins])
                floor=np.abs(position[origins]);left=score_predictions(peak,caps,floor,origins)
                buffer=io.BytesIO();np.savez_compressed(buffer,origins=origins,capacity=caps,refit_indices=refits,
                    peak=peak,floor=floor,pinball=left.pinball)
                fit_entry=write('private',stem+'-fits.json',rep.json_bytes(dict(version=1,cell=cell,status='COMPLETE',
                    fit_records=fit_rows,failure=None)))
                trace_entry=write('private',stem+'-traces.npz',buffer.getvalue())
                base=dict(source=s,native_unit=configs[s]['native_unit'],horizon=h,window=w,method='AR1_REPLAY',
                    refit_step=2,status='COMPLETE',stop_code=None)
                phis=[f['phi'] for f in fit_rows]
                tables['ar1-summary.csv'].append(base|dict(expected_origin_count=5,completed_origin_count=5)|
                    summarize_scores(left)|dict(completed_refit_count=3,phi_min=min(phis),phi_max=max(phis),
                    phi_mean=math.fsum(p/3 for p in phis),phi_below_zero=sum(p<0 for p in phis),
                    phi_exactly_one=sum(p==1 for p in phis),phi_above_one=sum(p>1 for p in phis)))
                years=dates[origins].astype('datetime64[Y]')
                for year in np.unique(years):
                    mask=years==year
                    tables['ar1-annual.csv'].append(base|dict(calendar_year=str(year))|
                        summarize_scores(score_predictions(peak[mask],caps[mask],floor[mask],origins[mask])))
                mask=np.arange(5)%(h+1)==0
                tables['ar1-nonoverlap.csv'].append(base|dict(stride_records=h+1)|
                    summarize_scores(score_predictions(peak[mask],caps[mask],floor[mask],origins[mask])))
                for k,method in enumerate(audit.runner.COMPARATORS):
                    right=score_predictions(peak,floor+(k+1)*.5,floor,origins)
                    references[s,h,w,method]=right
                    pmeta={k:v for k,v in base.items() if k!='method'}|dict(left_method='AR1_REPLAY',
                        right_method=method,right_parameter=.01 if method=='QR' else None,
                        contrast_role='DIRECT_S' if method=='frozen_S' else 'CONTEXT')
                    comparison=paired_comparison(left,right,dates[origins],horizon=h)
                    tables['ar1-paired.csv'].append(pmeta|comparison['all'])
                    tables['ar1-paired-annual.csv'].extend(pmeta|row for row in comparison['years'])
                    tables['ar1-paired-nonoverlap.csv'].append(pmeta|comparison['nonoverlap'])
                receipt=dict(version=1,cell=cell,method='AR1_REPLAY',status='COMPLETE',stop_code=None,
                    expected_origin_count=5,completed_origin_count=5,fit_count=3,
                    source_identity={k:configs[s][k] for k in ('sha256','bytes','record_count','native_unit')},
                    new_selection_sha256='f'*64,ar1_spec_sha256='b'*64,ar1_freeze_sha256='c'*64,
                    private_artifacts=[fit_entry,trace_entry])
                entry=write('public',stem+'-receipt.json',rep.json_bytes(receipt))
                receipts.append(dict(cell=cell,status='COMPLETE',receipt=entry))
            for name,rows in tables.items():write('public',name,csv_bytes(rows))
            manifest=ProvenanceTests().context()[0]
            resource=dict(elapsed_seconds=.1,peak_rss_bytes=1000000,maximum_observed_os_threads=1,
                thread_snapshot_count=1,thread_probe_status='PASS')
            manifest.update(replication_dir=str(attempt.relative_to(root)),annual_rows=32,paired_annual_rows=96,
                exports=exports,private_exports=private_exports,resources=resource,original_receipts=[],
                input_file_identities={},cell_receipts=receipts)
            (public/'ar1-replay-manifest.json').write_bytes(rep.json_bytes(manifest))
            class Guard:
                def __init__(self,*args):self.resources=resource.copy()
                def __call__(self,**kwargs):pass
                def arrays(self,*args):pass
            output='state/revision-20261022/test-auditor-never-written-'+attempt.name+'.json'
            with patch.object(audit.runner,'prepare_replica',return_value=inputs), \
                    patch.object(audit.runner,'verify_execution',return_value=execution), \
                    patch.object(audit.runner,'load_sources',return_value=sources), \
                    patch.object(audit.runner,'audit_references',return_value=(references,[])), \
                    patch.object(audit.runner,'verify_inputs'),patch.object(audit.adapter,'_load_helpers',return_value=None), \
                    patch('run_study.RunGuard',Guard),patch.object(audit.rep,'write_json') as writer, \
                    patch.object(audit.signal,'signal'),patch.object(audit.signal,'setitimer'), \
                    contextlib.redirect_stdout(io.StringIO()):
                audit.main(['--replication-dir','synthetic','--attempt-id','synthetic','--output',output])
            result=writer.call_args.args[1]
            self.assertEqual(result['aggregate_rows_independently_checked'],192)
            self.assertEqual(result['fit_records_metadata_checked'],24)
            self.assertEqual(result['exact_fraction_fits'],24)
            self.assertEqual(result['scalar_recursive_reports'],24)
            self.assertEqual(result['version'],2)
            self.assertFalse((root/output).exists())


if __name__=='__main__':unittest.main()
