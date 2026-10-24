"""Synthetic contract tests; no financial evaluation or production simulation."""
import unittest
import math
import importlib
from pathlib import Path
import tempfile


class MonteCarloContractTests(unittest.TestCase):
    def setUp(self):
        self.mc=importlib.import_module('v8_mc')

    def test_complete_origins_and_maturity_for_all_frequency_settings(self):
        for dgp,l,v in [('D0',26,52),('D1',168,1440),('D2',26,52)]:
            g=self.mc.geometry(dgp,500)
            self.assertEqual(g['validation_first'],l+2880+5)
            self.assertEqual(g['evaluation_first'],g['validation_last']+7)
            self.assertEqual(g['validation_last']+6,g['evaluation_first']-1)
            self.assertEqual(g['evaluation_last']-g['evaluation_first']+1,500)
            self.assertEqual(g['validation_first']-6-2880+1,l)

    def test_infinity_is_selected_on_exact_tie_but_failed_menu_is_ineligible(self):
        rows=[dict(parameter=x,status='COMPLETE',origin_count=52,mean_pinball=1.) for x in self.mc.MENU]
        self.assertTrue(math.isinf(self.mc.choose_candidate(rows,52)))
        rows[0]['status']='FAILED'
        with self.assertRaises(ValueError):self.mc.choose_candidate(rows,52)

    def test_one_failure_invalidates_entire_cell_not_only_the_failed_rep(self):
        good=dict(dgp='D0',window=52,features=4,rep=0,status='COMPLETE',qr_change=-12.,i_change=0.,oracle_change=-14.,win=True,selected='inf',f_breach=.1,i_breach=.1,qr_breach=.1,oracle_breach=.05)
        bad=dict(good,rep=1,status='FAILED',reason='solver')
        result=self.mc.aggregate([good,bad],2,500)
        self.assertEqual(len(result),24)
        row=result[0]
        self.assertEqual(row['status'],'FAILED')
        self.assertIsNone(row['qr_median_pct'])
        self.assertEqual(row['completed_repetitions'],1)
        self.assertEqual(result[1]['status'],'INCOMPLETE')

    def test_aggregation_uses_all_required_repetitions_and_iqr(self):
        template=dict(dgp='D0',window=52,features=4,status='COMPLETE',i_change=0.,oracle_change=-10.,selected='inf',f_breach=.1,i_breach=.1,qr_breach=.06,oracle_breach=.05)
        rows=[dict(template,rep=i,qr_change=x,win=x<0) for i,x in enumerate([-8.,4.])]
        out=self.mc.aggregate(rows,2,500)[0]
        self.assertEqual(out['status'],'COMPLETE')
        self.assertEqual(out['qr_median_pct'],-2.)
        self.assertEqual(out['qr_q25_pct'],-5.)
        self.assertEqual(out['qr_q75_pct'],1.)
        self.assertEqual(out['win_rate'],.5)

    def test_budget_ladder_fixed_and_does_not_use_losses(self):
        # Three DGPs, two reps; each complete job has100validation+100evaluation+40oracle seconds.
        pilot=[dict(dgp=d,rep=r,validation_seconds=100.,evaluation_seconds=100.,oracle_seconds=40.,simulation_seconds=0.,status='COMPLETE') for d in self.mc.DGPS for r in range(2)]
        p=self.mc.select_run_plan(pilot)
        self.assertEqual((p['repetitions'],p['evaluation_origins']),(50,300))
        self.assertGreater(p['projected_seconds'],5400)
        fast=[dict(x,validation_seconds=1.,evaluation_seconds=1.,oracle_seconds=.4) for x in pilot]
        self.assertEqual(self.mc.select_run_plan(fast)['repetitions'],100)

    def test_missing_cells_make_predictions_unassessable(self):
        rows=self.mc.aggregate([],100,500)
        self.assertTrue(all(x['status']=='UNASSESSABLE' for x in self.mc.predictions(rows).values()))

    def test_deadline_truncation_preserves_completed_rows_and_rejects_internal_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'worker.jsonl'
            path.write_text('{"status":"COMPLETE"}\n{"status":')
            rows,truncated=self.mc.read_worker_log(path,allow_truncated_final=True)
            self.assertEqual(rows,[{'status':'COMPLETE'}]);self.assertTrue(truncated)
            with self.assertRaises(ValueError):self.mc.read_worker_log(path,allow_truncated_final=False)
            path.write_text('broken\n{"status":"COMPLETE"}\n')
            with self.assertRaises(ValueError):self.mc.read_worker_log(path,allow_truncated_final=True)

    def test_failed_pilot_cell_keeps_spent_time_and_each_missing_cell_is_imputed(self):
        good=dict(dgp='D0',status='COMPLETE',validation_seconds=10.,evaluation_seconds=3.)
        bad=dict(dgp='D0',status='FAILED',validation_seconds=100.,evaluation_seconds=0.)
        skipped=dict(dgp='D0',status='NOT_RUN_CELL_FAILED',validation_seconds=0.,evaluation_seconds=0.)
        job=dict(dgp='D0',rep=0,status='PARTIAL_FAILURE',simulation_seconds=2.,oracle_seconds=1.,rows=[good,bad]+[skipped]*6)
        timing=self.mc.pilot_job_times([job])[0]
        self.assertEqual(timing['validation_seconds'],170.)
        self.assertEqual(timing['evaluation_seconds'],24.)
        self.assertEqual(timing['imputed_cells'],7)


if __name__=='__main__':unittest.main()
