import importlib,importlib.util,unittest
from pathlib import Path
import tempfile,json
from unittest.mock import patch

class TauWorkerTests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_tau_worker'),'tau orchestration API missing')
        return importlib.import_module('v6_tau_worker')
    def test_any_failed_declared_candidate_invalidates_whole_menu(self):
        a=self.api();rows=[dict(parameter=p,status='COMPLETE',origin_count=20,mean_pinball=2.) for p in (.001,.01,.1)]
        rows[0].update(status='FAILED',origin_count=0,mean_pinball=None)
        self.assertEqual(a.select_declared_menu(rows,[.001,.01,.1],20)['status'],'INELIGIBLE')
    def test_complete_exact_tie_chooses_larger_penalty(self):
        a=self.api();rows=[dict(parameter=p,status='COMPLETE',origin_count=20,mean_pinball=2.) for p in (.001,.01,.1)]
        self.assertEqual(a.select_declared_menu(rows,[.001,.01,.1],20)['parameter'],.1)
    def test_initial_resource_failure_keeps_validation_menu_and_evaluation_na(self):
        a=self.api()
        class G:
            def __call__(self,*x,**k):raise RuntimeError('RESOURCE_RSS')
            def summary(self):return {'peak_rss_bytes':123}
        with tempfile.TemporaryDirectory() as d,patch.object(a,'OUT',Path(d)),patch.object(a,'check_freeze',return_value='f'*64),patch.object(a,'require_controls',return_value={'verified':True}),patch.object(a.w,'Guard',G),patch.object(a.signal,'signal'),patch.object(a.signal,'alarm'):
            a.validation('fx_hourly','90')
            z=json.loads((Path(d)/'validation-fx_hourly-tau90.json').read_text())
            self.assertEqual(z['status'],'NA');self.assertEqual(len(z['candidates']),3)
            (Path(d)/'selection-freeze.json').write_text(json.dumps({'cells':{'fx_hourly-tau90':{'status':'NA','reason':'RESOURCE_RSS','receipt_sha256':'f'*64}}}))
            a.evaluation('fx_hourly','90')
            z=json.loads((Path(d)/'evaluation-fx_hourly-tau90.json').read_text())
            self.assertEqual(z['status'],'NA');self.assertEqual(z['reason'],'RESOURCE_RSS')

    def test_reference_failure_retains_descriptive_direction_without_fabricated_p(self):
        a=self.api()
        with patch.object(a.inf,'compare_losses',return_value=dict(status='REFERENCE_FAILURE',mean_difference=None,dm_p=None)):
            z=a.compare_tau_losses([1.,2.],[2.,4.])
        self.assertEqual(z['mean_difference'],-1.5);self.assertIsNone(z['diagnostic_mean_difference']);self.assertIsNone(z['dm_p'])
        self.assertIsNone(a.direction_reversal(None,-1))

    def test_direction_reversal_is_against_same_named_point95_contrast(self):
        a=self.api()
        self.assertTrue(a.direction_reversal(2.,-1.));self.assertFalse(a.direction_reversal(-2.,-1.));self.assertFalse(a.direction_reversal(0.,-1.))
if __name__=='__main__':unittest.main()
