"""Synthetic contract and orchestration tests; never opens financial inputs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

if importlib.util.find_spec('supervisor_r6'):
    import supervisor_r6 as r6
else:
    r6 = None


class SyntheticReports:
    """Deterministic numerical boundary; failures must never be retried."""
    instances = []
    fail_id = None

    def __init__(self, position, dates, group, source_config, guard, folder):
        self.position = position
        self.calls = []
        self.group = group
        self.folder = Path(folder)
        self.cache = {}
        self.__class__.instances.append(self)

    def segment(self, candidate_id, origins, *, window=None, refit_step=None):
        key = (candidate_id, int(origins[0]), int(origins[-1]), window, refit_step)
        if key in self.cache:
            return self.cache[key]
        self.calls.append(key)
        if candidate_id == self.fail_id:
            raise ValueError('SYNTHETIC_CANDIDATE_FAILURE')
        # Constant positions are one; capacities one give exact zero loss.
        self.cache[key] = dict(origins=np.array(origins), capacity=np.ones(len(origins)),
            floor=np.ones(len(origins)), refit_indices=np.array(origins),
            fit_diagnostics=[], trace_sha256='synthetic', trace_path='synthetic')
        return self.cache[key]


class LimitedReports(SyntheticReports):
    def segment(self,candidate_id,origins,**kwargs):
        if candidate_id=='10' and int(origins[0])==253:
            raise r6.LimitStop('GROUP_TIME_LIMIT')
        return super().segment(candidate_id,origins,**kwargs)


class R6RunnerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(r6, 'R6 runner is missing')
        SyntheticReports.instances = []
        SyntheticReports.fail_id = None

    def test_frozen_inventory_keeps_all_thirty_and_fifty_six_groups(self):
        spec = r6.read_contract()
        groups = r6.group_inventory(spec)
        self.assertEqual(sum(g['phase'] == 'retro' for g in groups), 30)
        self.assertEqual(sum(g['phase'] == 'inspected' for g in groups), 56)
        self.assertEqual(sum(g['source'] == 'fx_hourly' and g['phase'] == 'retro' for g in groups), 4)
        self.assertEqual(sum(g['source'] == 'nyfed_weekly' and g['phase'] == 'inspected' for g in groups), 52)

    def test_retro_truncation_hides_old_validation_suffix_from_every_backend(self):
        spec = r6.read_contract()
        group = dict(phase='retro', source='nyfed_weekly', series_key='PDPOSGS-B', horizon=6, window=52)
        x = np.ones(706); x[329:] = np.nan
        with tempfile.TemporaryDirectory() as folder:
            result = r6.run_group(group, spec, x, np.arange(706), Path(folder),
                lambda **kw: None, backend_factory=SyntheticReports)
            self.assertEqual(len(SyntheticReports.instances[0].position), 329)
            self.assertEqual([q['status'] for q in result['rows']], ['COMPLETE'] * 6)
            selection = json.loads((Path(folder)/'selection-before-evaluation.json').read_text())
            self.assertEqual(selection['rules']['R2']['selected_id'], 'I')
            self.assertLessEqual(selection['selection_frozen_utc'], result['evaluation_started_utc'])

    def test_shared_selection_reuses_one_evaluation_and_full_outer_validation(self):
        spec = r6.read_contract()
        group = dict(phase='retro', source='nyfed_weekly', series_key='PDPOSGS-B', horizon=6, window=52)
        with tempfile.TemporaryDirectory() as folder:
            result = r6.run_group(group, spec, np.ones(706), np.arange(706), Path(folder),
                lambda **kw: None, backend_factory=SyntheticReports)
            calls = SyntheticReports.instances[0].calls
            self.assertEqual(sum(k[:3] == ('I', 253, 304) for k in calls), 1)
            self.assertEqual(sum(k[:3] == ('10', 253, 304) for k in calls), 1)
            self.assertEqual(sum(k[:3] == ('I', 177, 228) for k in calls), 1)
            self.assertEqual(len(result['rows']), 6)

    def test_failed_I_blocks_dependent_rules_but_R0_and_F_survive(self):
        spec = r6.read_contract(); SyntheticReports.fail_id = 'I'
        group = dict(phase='retro', source='nyfed_weekly', series_key='PDPOSGS-B', horizon=6, window=52)
        with tempfile.TemporaryDirectory() as folder:
            result = r6.run_group(group, spec, np.ones(706), np.arange(706), Path(folder),
                lambda **kw: None, backend_factory=SyntheticReports)
            status = {q['report']: q['status'] for q in result['rows']}
            self.assertEqual(status, {'F':'COMPLETE','I':'FAILED','R0':'COMPLETE',
                                     'R1':'FAILED','R2':'FAILED','R3':'FAILED'})
            self.assertTrue(all(q.get('mean_pinball') is None for q in result['rows'] if q['status']=='FAILED'))
            calls = SyntheticReports.instances[0].calls
            self.assertEqual(sum(k[:3] == ('I',177,228) for k in calls), 1)

    def test_w260_has_no_extra_folds_and_R3_equals_R2_by_construction(self):
        spec=r6.read_contract()
        group=dict(phase='inspected',source='nyfed_weekly',series_key='PDPOSGS-B',horizon=24,window=260)
        with tempfile.TemporaryDirectory() as folder:
            result=r6.run_group(group,spec,np.ones(706),np.arange(706),Path(folder),
                lambda **kw:None,backend_factory=SyntheticReports)
            self.assertEqual(result['r3_fold_bounds'], [[329,380]])
            self.assertEqual(result['r3_design_status'],'NO_EXTRA_FOLDS')
            self.assertEqual(result['selections']['R3'],result['selections']['R2'])

    def test_evaluation_timeout_retains_independent_completed_rows_without_fits(self):
        spec=r6.read_contract()
        group=dict(phase='retro',source='nyfed_weekly',series_key='PDPOSGS-B',horizon=6,window=52)
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(r6.LimitStop) as caught:
                r6.run_group(group,spec,np.ones(706),np.arange(706),Path(folder),
                    lambda **kw:None,backend_factory=LimitedReports)
            self.assertTrue(hasattr(caught.exception,'partial_group'))
            result=caught.exception.partial_group
            status={q['report']:q['status'] for q in result['rows']}
            self.assertEqual(status,{'F':'COMPLETE','I':'COMPLETE','R0':'TIME_LIMIT',
                                     'R1':'COMPLETE','R2':'COMPLETE','R3':'COMPLETE'})
            self.assertEqual(len(result['selections']),4)
            self.assertEqual(result['primary_replication']['status'],'NOT_RUN')

    def test_inspected_handler_cannot_start_until_retro_seal_returns(self):
        events=[]
        groups=[dict(phase='retro',id='a'),dict(phase='inspected',id='b')]
        def handler(group):
            events.append(group['phase']);return group
        def seal(results):
            self.assertEqual(events,['retro']);events.append('SEALED')
        result=r6.run_phases(groups,handler,seal)
        self.assertEqual(events,['retro','SEALED','inspected'])
        self.assertEqual(len(result['inspected']),1)

    def test_assessment_retains_failed_cells_and_zero_eligible_is_not_assessable(self):
        rows=[]
        for j in range(26):
            for report,delta in [('R0',7.),('R2',4.)]:
                rows.append(dict(phase='retro',source='nyfed_weekly',series_key=str(j),horizon=6,
                                 window=52,report=report,status='COMPLETE',percent_vs_F=delta))
        for w in (720,2880):
            for report in ('R0','R2'):
                rows.append(dict(phase='retro',source='fx_hourly',series_key='fx_hourly',horizon=6,
                                 window=w,report=report,status='COMPLETE',percent_vs_F=1.))
        got=r6.assess(rows,r6.read_contract())
        self.assertEqual([got[k]['status'] for k in ('S1','S2','S3')],['PASS','NOT_ASSESSABLE','PASS'])
        rows[1].update(status='FAILED',percent_vs_F=None)
        self.assertEqual(r6.assess(rows,r6.read_contract())['S1']['status'],'NOT_MET')

    def test_S2_requires_R2_only_in_windows_where_complete_R0_has_a_gain(self):
        rows=[]
        for w in (720,2880):
            rows.extend([dict(phase='retro',source='fx_hourly',series_key='fx_hourly',horizon=6,
                window=w,report='R0',status='COMPLETE',percent_vs_F=1.),
                dict(phase='retro',source='fx_hourly',series_key='fx_hourly',horizon=6,
                window=w,report='R2',status='FAILED',percent_vs_F=None)])
        got=r6.assess(rows,r6.read_contract())['S2']
        self.assertEqual(got['status'],'NOT_ASSESSABLE')
        self.assertEqual(got['eligible_count'],0)
        rows[0]['percent_vs_F']=-4.
        got=r6.assess(rows,r6.read_contract())['S2']
        self.assertEqual(got['status'],'NOT_MET')
        self.assertEqual(got['eligible_count'],1)

    def test_core_I_F_dispatch_uses_empirical_ranks_and_mature_history(self):
        group=dict(phase='retro',source='nyfed_weekly',series_key='synthetic',horizon=6,window=52)
        cfg=r6.read_contract()['sources']['nyfed_weekly']
        x=np.sin(np.arange(329)/9.)+2
        with tempfile.TemporaryDirectory() as folder:
            backend=r6.CoreReports(x,np.arange(329),group,cfg,lambda **kw:None,Path(folder))
            ids=np.arange(253,266)
            ordinary=backend.segment('I',ids);corrected=backend.segment('F',ids)
            self.assertTrue(np.all(corrected['capacity']>=ordinary['capacity']))
            np.testing.assert_array_equal(ordinary['refit_indices'],np.repeat(253,13))
            self.assertEqual(ordinary['fit_diagnostics'][0]['latest_label_end'],253)
            self.assertIs(backend.segment('I',ids),ordinary)

    def test_shared_empirical_failure_is_cached_for_both_reference_ids(self):
        # Retrying F after the shared I/F numerical attempt would violate no-retry.
        group=dict(phase='retro',source='nyfed_weekly',series_key='synthetic',horizon=6,window=52)
        cfg=r6.read_contract()['sources']['nyfed_weekly']; attempts=[]
        def fail(*args,**kwargs):
            attempts.append(1);raise ValueError('SYNTHETIC_EMPIRICAL_FAILURE')
        with tempfile.TemporaryDirectory() as folder:
            backend=r6.CoreReports(np.ones(329),np.arange(329),group,cfg,lambda **kw:None,Path(folder))
            with patch.object(r6,'empirical_predict',fail):
                for candidate in ('I','F'):
                    with self.assertRaises(ValueError):backend.segment(candidate,np.arange(253,266))
            self.assertEqual(len(attempts),1)

    def test_unrun_primary_keeps_a_failed_diagnostic_row(self):
        group=dict(phase='retro',source='fx_hourly',series_key='fx_hourly',horizon=6,window=2880)
        result=r6.terminal_group(group,'NOT_RUN','RUN_TIME_LIMIT')
        self.assertIn('primary_replication',result)
        self.assertEqual(result['primary_replication']['id'],'FX-original-structure')
        self.assertEqual(result['primary_replication']['status'],'NOT_RUN')
        self.assertEqual(len(result['rows']),6)

    def test_retro_seal_includes_all_failed_rows_and_both_primary_diagnostics(self):
        spec=r6.read_contract()
        results=[r6.terminal_group(g,'NOT_RUN','SYNTHETIC_STOP')
                 for g in r6.group_inventory(spec) if g['phase']=='retro']
        with tempfile.TemporaryDirectory() as folder:
            public=Path(folder)/'public';private=Path(folder)/'private'
            public.mkdir();(private/'retro').mkdir(parents=True)
            inventory=r6.seal_retro(results,public,private)
            sealed=json.loads((public/'retro-seal.json').read_text())
            self.assertEqual(sealed['report_row_count'],180)
            import csv
            with (public/'primary-replication.csv').open() as f: primary=list(csv.DictReader(f))
            self.assertEqual(len(primary),2)
            self.assertEqual({p['status'] for p in primary},{'NOT_RUN'})
            self.assertTrue(all(r6.sha(p['path'])==p['sha256'] for p in inventory))

    def test_core_QR_branch_calls_original_solver_on_only_synthetic_positions(self):
        group=dict(phase='retro',source='nyfed_weekly',series_key='synthetic',horizon=6,window=52)
        cfg=r6.read_contract()['sources']['nyfed_weekly']
        times=np.arange('2000-01-01','2006-04-22',7,dtype='datetime64[D]')[:329]
        x=2+np.sin(np.arange(329)/9.)
        with tempfile.TemporaryDirectory() as folder:
            backend=r6.CoreReports(x,times,group,cfg,lambda **kw:None,Path(folder))
            item=backend.segment('10',np.arange(253,266))
            self.assertEqual(item['summary']['origin_count'],13)
            self.assertTrue(np.all(item['capacity']>=item['floor']))
            self.assertEqual(item['fit_diagnostics'][0]['training_count'],52)


if __name__=='__main__': unittest.main()
