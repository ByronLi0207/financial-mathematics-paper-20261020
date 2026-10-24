import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import v6_worker as w
from conditional_study import StudyConfig, historical_forecasts

class WorkerTests(unittest.TestCase):
    def test_frozen_f_is_original_component(self):
        x=np.array([((i*7)%19)-8. for i in range(110)])
        c=StudyConfig(3,20,7,2,4,3600);ids=np.arange(60,100)
        np.testing.assert_array_equal(w.frozen_f(x,ids,c),historical_forecasts(x,ids,c)['frozen_F'])
    def test_new_write_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'one.json';w.write_json_new(p,{'a':1})
            with self.assertRaises(FileExistsError):w.write_json_new(p,{'a':2})
            self.assertIn('1',p.read_text())
    def test_public_aci_is_scalar_aggregate(self):
        d=dict(alpha=np.array([.05,.06]),calibration_counts=np.array([19,20]),ranks=np.array([19,20]),feedback_counts=np.array([0,1]),clip_counts=np.array([1,0]),initial_calibration_count=19,feedback_consumed=1,gamma=.01,state_fractions=('1/20','3/50'),feedback_records=({'secret':10},))
        z=w.aci_diagnostics(d)
        self.assertEqual(z['alpha_max'],.06);self.assertEqual(z['clip_count'],1)
        self.assertNotIn('feedback_records',z);self.assertNotIn('state_fractions',z)
    def test_failed_sav_start_serializes_to_na_receipt(self):
        start=w.sav.SAVStart(0,(1.,.2,.01),False,False,'NONCONVERGED',2.,2.,3000,10,1,'limit',(1.,.2,.01),())
        z=w.sav_failure_public({'starts':(start,), 'scale':2.})
        self.assertEqual(z['starts'][0]['success'],False)
        with tempfile.TemporaryDirectory() as d:w.write_json_new(Path(d)/'fail.json',z)

    def test_worker_gamma_row_contract_selects_without_key_translation(self):
        rows=[w.gamma_row(g,{'n':20,'full_hits':1,'mean_loss':2.}, {}) for g in w.aci.GAMMAS]
        self.assertEqual(w.aci.select_gamma(rows,expected_count=20)['gamma'],.001)

    def test_initial_and_final_resource_probe_failures_are_recorded_na(self):
        for fail_call in (1,2):
            class FakeGuard:
                def __init__(self):self.calls=0
                def __call__(self,*a,**kw):
                    self.calls+=1
                    if self.calls==fail_call:raise RuntimeError('RESOURCE_RSS')
                def summary(self):return {'calls':self.calls}
            with tempfile.TemporaryDirectory() as d, patch.object(w,'PUBLIC',Path(d)), patch.object(w,'Guard',FakeGuard), patch.object(w,'check_execution_freeze',return_value='synthetic'), patch.object(w,'run_aci_validation',return_value=({'status':'COMPLETE'},{})):
                result=w.run_cell('validation','synthetic',2,20,'ACI_F')
                self.assertEqual(result['status'],'NA');self.assertEqual(result['reason'],'RESOURCE_RSS')
                self.assertTrue((Path(d)/'wp2/validation-synthetic-h2-w20-ACI_F.json').is_file())

    def test_all_json_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): w.write_json_new(Path(d)/'bad.json',{'x':float('nan')})
    def test_aggregate_aci_requires_all_indices(self):
        d=dict(alpha=np.array([.05,.06]),calibration_counts=np.array([19]),ranks=np.array([19,20]),feedback_counts=np.array([0,1]),clip_counts=np.array([1,0]),initial_calibration_count=19,feedback_consumed=1,gamma=.01)
        with self.assertRaises(ValueError): w.aci_diagnostics(d)

if __name__=='__main__': unittest.main()
