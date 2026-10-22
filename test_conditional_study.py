"""Array-only scientific integration oracles; no financial source files."""
import importlib.util
from fractions import Fraction
import math
import unittest
from unittest.mock import patch
import numpy as np
import study_core as old
from revision_selection import issue_selected

if importlib.util.find_spec('conditional_study') is None:
    cs=None
else:
    import conditional_study as cs


class ConditionalStudyTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(cs,'conditional study implementation is missing')

    @staticmethod
    def source(n=190):
        i=np.arange(n)
        return 20*np.sin(i*.23)+i*.1, np.datetime64('2019-01-02')+i*np.timedelta64(7,'D')

    def config(self,**overrides):
        args=dict(horizon=6,window=40,refit_step=7,short_scale=3,long_scale=26,nominal_gap_seconds=604800)
        args.update(overrides);return cs.StudyConfig(**args)

    def test_zero_and_constant_sources_are_valid_for_all_three_families(self):
        _,times=self.source()
        for constant in (0.,-12.5):
            x=np.full(len(times),constant)
            for family,p in (('QR',.01),('KNN',20),('SCALED_KNN',20)):
                fit=cs.conditional_forecast(x,times,np.arange(100,110),self.config(),family,p)
                np.testing.assert_allclose(fit.capacities,abs(constant),atol=1e-9)
                self.assertFalse(fit.capacities.flags.writeable)
                self.assertEqual(len(fit.fit_diagnostics),2)

    def test_known_linear_path_has_exact_fixed_future_headroom(self):
        _,times=self.source();x=np.arange(len(times),dtype=float)
        for family,p in (('QR',.01),('KNN',20),('SCALED_KNN',20)):
            fit=cs.conditional_forecast(x,times,np.arange(100,112),self.config(),family,p)
            np.testing.assert_allclose(fit.capacities,x[100:112]+6,atol=2e-4,rtol=0)

    def test_mutating_future_observations_cannot_change_issued_forecasts(self):
        x,t=self.source();changed=x.copy();changed[111:]=1e5+np.arange(len(x)-111)
        t2=t.copy();t2[111:]+=np.timedelta64(9,'D')
        for family,p in (('QR',.1),('KNN',20),('SCALED_KNN',20)):
            a=cs.conditional_forecast(x,t,np.arange(100,111),self.config(),family,p)
            b=cs.conditional_forecast(changed,t2,np.arange(100,111),self.config(),family,p)
            np.testing.assert_array_equal(a.capacities,b.capacities)
            np.testing.assert_array_equal(a.refit_indices,[100]*7+[107]*4)
            for d in a.fit_diagnostics:
                self.assertEqual(d['training_last_origin']+6,d['refit_index'])
                self.assertLessEqual(d['latest_label_end'],d['refit_index'])

    def test_frozen_historical_pool_reanchors_at_actual_query(self):
        x,t=self.source();config=self.config();cache=old.build_label_cache(x,6)
        got=cs.issue_historical(x,cache,issue=105,refit=100,window=40,step=7)
        pool=range(55,95);cur=x[105];B=abs(cur)
        G=[];S=[];P=[]
        for i in pool:
            path=x[i:i+7];peak=max(abs(float(v)) for v in path)
            increments=[float(v-x[i]) for v in path]
            G.append(peak-abs(float(x[i])));P.append(peak)
            S.append(max(cur+max(increments),-cur-min(increments))-B)
        rank=39
        np.testing.assert_array_equal(got,[B+sorted(G)[rank-1],B+sorted(S)[rank-1],max(B,sorted(P)[rank-1])])
        with self.assertRaises(ValueError):cs.issue_historical(x,cache,issue=107,refit=100,window=40,step=7)
        with self.assertRaises(ValueError):cs.issue_historical(x,cache,issue=99,refit=100,window=40,step=7)

    def test_rolling_and_one_state_references_match_accepted_legacy_arithmetic(self):
        x,t=self.source();config=self.config();ids=np.arange(100,111)
        got=cs.historical_forecasts(x,ids,config,neighbor_count=20)
        cell=old.CellSpec('synthetic',6,40,19,20,39);cache=old.build_label_cache(x,6)
        for j,issue in enumerate(ids):
            labels=old.mature_window(cache,int(issue),cell)
            for selection,prefix,k in (('full','rolling',40),('nearest','one_state',20)):
                expected=issue_selected(int(issue),x[issue],labels,x[labels.origins],cell,selection,k)
                for col,name in enumerate(('F','S','K')):
                    self.assertEqual(got[prefix+'_'+name][j],expected.capacities[col])

    def test_unit_scaling_of_raw_local_quantiles_and_historical_references(self):
        x,t=self.source();ids=np.arange(100,111);config=self.config()
        a=cs.conditional_forecast(x,t,ids,config,'KNN',20)
        b=cs.conditional_forecast(x*1000,t,ids,config,'KNN',20)
        np.testing.assert_allclose(b.capacities,a.capacities*1000,rtol=1e-12,atol=1e-8)
        for key,value in cs.historical_forecasts(x,ids,config).items():
            np.testing.assert_allclose(cs.historical_forecasts(x*1000,ids,config)[key],value*1000,rtol=1e-12,atol=1e-8)

    def test_full_pool_plain_knn_is_exactly_the_frozen_headroom_reference(self):
        # This is a scientific identity of an existing boundary configuration,
        # not evidence that the rich distance features improved forecasting.
        x,t=self.source(1100)
        for window,first in ((52,200),(720,1000)):
            for horizon in (6,24):
                config=self.config(window=window,horizon=horizon,refit_step=13)
                ids=np.arange(first,first+16)
                fit=cs.conditional_forecast(x,t,ids,config,'KNN',window)
                reference=cs.historical_forecasts(x,ids,config)['frozen_F']
                np.testing.assert_array_equal(fit.capacities,reference)

    def test_native_score_uses_stored_peak_minus_final_capacity_and_own_denominator(self):
        s=cs.score_predictions(np.array([10.,20.,3.]),np.array([8.,25.,3.]),np.array([1.,1.,1.]),np.arange(3))
        np.testing.assert_array_equal(s.pinball,[float(Fraction(19,20))*2,float(Fraction(1,20))*5,0.])
        metrics=cs.summarize_scores(s)
        self.assertEqual(metrics['strict_breach_count'],1)
        self.assertEqual(metrics['conditional_overrun_denominator'],1)
        self.assertEqual(metrics['conditional_mean_overrun'],2.)
        self.assertEqual(metrics['mean_pinball'],math.fsum([1.9,.25,0.])/3)
        with self.assertRaises(ValueError):cs.score_predictions(np.array([1.]),np.array([0.]),np.array([1.]),np.array([0]))

    def test_no_breach_conditional_mean_is_null_not_zero(self):
        m=cs.summarize_scores(cs.score_predictions(np.array([1.,2.]),np.array([1.,3.]),np.zeros(2),np.arange(2)))
        self.assertIsNone(m['conditional_mean_overrun']);self.assertEqual(m['conditional_overrun_undefined_reason'],'NO_STRICT_BREACHES')

    def test_selection_exact_tie_prefers_larger_parameter_and_a_failed_candidate_blocks_cell(self):
        rows=[{'parameter':p,'status':'COMPLETE','origin_count':10,'mean_pinball':2.} for p in (.001,.01,.1)]
        self.assertEqual(cs.select_parameter(rows,[.001,.01,.1],expected_count=10)['parameter'],.1)
        rows[0]={'parameter':.001,'status':'FAILED','failure_code':'NONCONVERGENCE'}
        self.assertIsNone(cs.select_parameter(rows,[.001,.01,.1],expected_count=10)['parameter'])
        with self.assertRaises(ValueError):cs.select_parameter(rows[1:],[.001,.01,.1],expected_count=10)

    def test_candidate_selection_uses_loss_not_breach_or_parameter_order(self):
        rows=[dict(parameter=.1,status='COMPLETE',origin_count=10,mean_pinball=3.),dict(parameter=.001,status='COMPLETE',origin_count=10,mean_pinball=1.)]
        self.assertEqual(cs.select_parameter(rows,[.001,.1],expected_count=10)['parameter'],.001)

    def test_resource_incomplete_candidate_blocks_selection_without_fake_loss(self):
        rows=[dict(parameter=.001,status='COMPLETE',origin_count=10,mean_pinball=1.),
              dict(parameter=.01,status='INCOMPLETE',stop_code='RESOURCE_WALL'),
              dict(parameter=.1,status='INCOMPLETE',stop_code='NOT_STARTED_AFTER_RESOURCE_STOP')]
        selected=cs.select_parameter(rows,[.001,.01,.1],expected_count=10)
        self.assertEqual(selected['status'],'INELIGIBLE');self.assertIsNone(selected['parameter'])
        self.assertEqual(selected['incomplete_candidates'],[.01,.1])

    def test_nonoverlap_grid_uses_H_plus_one_without_year_reset(self):
        np.testing.assert_array_equal(cs.nonoverlap_origins(405,681,24),np.arange(405,682,25))
        grid=cs.nonoverlap_origins(100,120,6)
        self.assertTrue(all(b>a+6 for a,b in zip(grid,grid[1:])))

    def test_paired_contrasts_use_aligned_direct_differences_and_global_year_grid(self):
        ids=np.arange(100,116);dates=np.datetime64('2020-12-25')+np.arange(16)*np.timedelta64(1,'D')
        peak=np.full(16,10.);floor=np.zeros(16)
        left=cs.score_predictions(peak,np.full(16,8.),floor,ids)
        right=cs.score_predictions(peak,np.full(16,12.),floor,ids)
        got=cs.paired_comparison(left,right,dates,horizon=6)
        self.assertAlmostEqual(got['all']['mean_pinball_difference'],1.8)
        self.assertEqual([(r['calendar_year'],r['origin_count']) for r in got['years']], [('2020',7),('2021',9)])
        self.assertEqual(got['nonoverlap']['origin_count'],3)
        self.assertEqual(got['nonoverlap']['first_source_index'],100)
        self.assertEqual(got['nonoverlap']['last_source_index'],114)
        self.assertAlmostEqual(got['nonoverlap']['mean_pinball_difference'],1.8)
        # A comparison cannot silently shift one forecast series by one issue.
        shifted=cs.score_predictions(peak,np.full(16,12.),floor,ids+1)
        with self.assertRaises(ValueError):cs.paired_comparison(left,shifted,dates,horizon=6)

    def test_relative_percent_avoids_unnecessary_intermediate_overflow(self):
        peak=np.array([1e307]);floor=np.zeros(1);ids=np.array([1]);dates=np.array(['2020-01-01'],dtype='datetime64[D]')
        left=cs.score_predictions(peak,np.array([0.]),floor,ids)
        right=cs.score_predictions(peak,np.array([5e306]),floor,ids)
        got=cs.paired_comparison(left,right,dates,horizon=6)
        self.assertEqual(got['all']['relative_mean_loss_difference_percent'],100.)

    def test_noncontiguous_origins_and_unavailable_features_fail(self):
        x,t=self.source()
        with self.assertRaises(ValueError):cs.conditional_forecast(x,t,np.array([100,102]),self.config(),'KNN',20)
        with self.assertRaises(ValueError):cs.conditional_forecast(x,t,np.arange(40,50),self.config(),'KNN',20)
        with self.assertRaises(ValueError):cs.conditional_forecast(x,t,np.arange(100,110),self.config(),'KNN',1)

    def test_caller_cancellation_propagates_instead_of_becoming_forecasts(self):
        class Cancel(Exception):pass
        def stop(**kwargs):raise Cancel()
        x,t=self.source()
        with self.assertRaises(Cancel):cs.conditional_forecast(x,t,np.arange(100,110),self.config(),'KNN',20,checkpoint=stop)

    def test_failed_refit_retains_context_and_partial_issues_without_complete_score(self):
        from conditional_quantile import QuantileFitError
        real=cs.fit_quantile_ridge;calls=[]
        def fail_second(*args,**kwargs):
            calls.append(1)
            if len(calls)==2:raise QuantileFitError('NONCONVERGENCE',{'iterations':10000})
            return real(*args,**kwargs)
        x,t=self.source()
        with patch.object(cs,'fit_quantile_ridge',side_effect=fail_second):
            with self.assertRaises(QuantileFitError) as caught:
                cs.conditional_forecast(x,t,np.arange(100,111),self.config(),'QR',.1)
        exc=caught.exception
        self.assertEqual(exc.failure_context['refit_index'],107)
        self.assertEqual(exc.failure_context['training_first_origin'],62)
        self.assertEqual(exc.failure_context['training_last_origin'],101)
        self.assertEqual(exc.failure_context['issued_origin_count'],7)
        np.testing.assert_array_equal(exc.partial_forecast.origins,np.arange(100,107))
        self.assertEqual(len(exc.partial_forecast.fit_diagnostics),1)
        self.assertFalse(exc.partial_forecast.capacities.flags.writeable)
        self.assertEqual(dict(exc.diagnostics),{'iterations':10000})


if __name__=='__main__':unittest.main()
