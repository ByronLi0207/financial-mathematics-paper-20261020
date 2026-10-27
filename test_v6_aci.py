"""Independent clock/rank oracles for the frozen finite delayed adaptation."""
from fractions import Fraction
import importlib
import importlib.util
import unittest
import numpy as np


class FiniteDelayedACI(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_aci'),
                             'finite delayed ACI implementation is missing')
        return importlib.import_module('v6_aci')

    def stream(self, origins=(20,21,22), peak=(20.,20.,10.), gamma=.01, **changes):
        args=dict(origins=np.array(origins), base=np.full(len(origins),10.),
                  peak=np.array(peak), floor=np.zeros(len(origins)), horizon=2,
                  window=20, gamma=gamma, warm_origins=np.arange(20),
                  warm_base=np.full(20,10.), warm_peak=np.full(20,10.))
        args.update(changes)
        return self.api().aci_stream(**args)

    def test_corrected_rank_exactly_at_finite_lower_boundary(self):
        a=self.api()
        for m in (19,20,52,260,2880):
            self.assertEqual(a.finite_rank(Fraction(1,m+1),m),m)
        self.assertEqual(a.finite_rank(Fraction(1),19),0)
        self.assertEqual(a.finite_rank(Fraction(1,20),19),19)

    def test_feedback_waits_for_the_issued_outcome_and_uses_old_report(self):
        r=self.stream()
        np.testing.assert_array_equal(r['capacities'],[10.,10.,20.])
        np.testing.assert_array_equal(r['feedback_counts'],[0,0,1])
        self.assertEqual(r['state_fractions'][2],'1/21')

    def test_future_peak_perturbation_cannot_change_pre_maturity_reports(self):
        a=self.stream();b=self.stream(peak=(1e8,20.,10.))
        np.testing.assert_array_equal(a['capacities'][:2],b['capacities'][:2])
        self.assertGreater(b['capacities'][2],a['capacities'][2])

    def test_gap_consumes_each_matured_wrapped_hit_once(self):
        r=self.stream(origins=(20,21,24,25),peak=(20.,20.,20.,20.),gamma=.001,window=100)
        np.testing.assert_array_equal(r['feedback_counts'],[0,0,2,0])
        self.assertEqual(r['state_fractions'][2],'481/10000')
        self.assertEqual(r['state_fractions'][3],'481/10000')
        self.assertEqual([z['origin'] for z in r['feedback_records']],[20,21])

    def test_negative_corrections_reach_floor_then_use_new_matured_score(self):
        r=self.stream(base=np.full(3,20.),floor=np.full(3,5.),peak=np.full(3,6.),
                      warm_base=np.full(20,20.),warm_peak=np.ones(20))
        # First two thresholds are20-19=1, projected to5. At22 the newly
        # mature issue20 score is6-20=-14, so the finite upper rank gives6.
        np.testing.assert_array_equal(r['capacities'],[5.,5.,6.])

    def test_inadequate_initial_calibration_is_whole_stream_failure(self):
        a=self.api()
        with self.assertRaises(a.InsufficientCalibration):
            self.stream(warm_origins=np.array([18,19]),warm_base=np.ones(2),warm_peak=np.ones(2))

    def test_original_treasury_grid_admission_is_value_free(self):
        a=self.api()
        f=a.initialization_grid(329,24,260,13,0)
        q=a.initialization_grid(329,24,260,13,26)
        h6=a.initialization_grid(329,6,260,13,26)
        self.assertEqual((f['first_legal_refit'],f['mature_initial_count']),(290,16))
        self.assertEqual((q['first_legal_refit'],q['mature_initial_count']),(316,0))
        self.assertEqual((h6['first_legal_refit'],h6['mature_initial_count']),(303,21))

    def test_validation_selection_is_coverage_first_with_visible_failure(self):
        a=self.api()
        candidates=[dict(gamma=.001,status='COMPLETE',origin_count=20,hits=0,mean_loss=1.),
                    dict(gamma=.005,status='COMPLETE',origin_count=20,hits=1,mean_loss=100.),
                    dict(gamma=.01,status='FAILED',origin_count=0,hits=None,mean_loss=None),
                    dict(gamma=.05,status='COMPLETE',origin_count=20,hits=1,mean_loss=100.)]
        r=a.select_gamma(candidates,expected_count=20)
        self.assertEqual(r['gamma'],.005)
        self.assertEqual(r['status'],'SELECTED')
        self.assertEqual(r['failed_gamma'],[.01])

    def test_missing_validation_candidate_is_not_silently_omitted(self):
        a=self.api()
        with self.assertRaises(ValueError):
            a.select_gamma([],expected_count=20)

    def test_nonfinite_candidate_visible_but_other_gammas_remain_eligible(self):
        a=self.api()
        rows=[dict(gamma=g,status='COMPLETE',origin_count=20,hits=1,mean_loss=10.) for g in a.GAMMAS]
        rows[0]['mean_loss']=float('nan')
        r=a.select_gamma(rows,expected_count=20)
        self.assertEqual(r['gamma'],.005);self.assertEqual(r['failed_gamma'],[.001])

    def test_private_threshold_survives_floor_projection(self):
        r=self.stream(base=np.full(3,20.),floor=np.full(3,5.),peak=np.full(3,6.),
                      warm_base=np.full(20,20.),warm_peak=np.ones(20))
        np.testing.assert_array_equal(r['score_quantiles'],[-19.,-19.,-14.])
        np.testing.assert_array_equal(r['raw_thresholds'],[1.,1.,6.])
        np.testing.assert_array_equal(r['floor'],[5.,5.,5.])

    def test_unsigned_descending_clock_rejected_before_cast(self):
        with self.assertRaises(ValueError):self.stream(origins=np.array([20,19],dtype=np.uint64),peak=(10.,10.))
        with self.assertRaises(ValueError):self.stream(origins=np.array([2**63,2**63+1],dtype=np.uint64),peak=(10.,10.))

    def test_exact_warm_grid_boundary_uses_latest_sufficient_start(self):
        self.assertEqual(self.api().initialization_grid(100,2,19,20,0)['pre_first'],80)

    def test_checkpoint_failure_propagates_without_partial_scoring(self):
        self.api()
        def stop(**_):raise RuntimeError('resource stop')
        with self.assertRaisesRegex(RuntimeError,'resource stop'):
            self.stream(checkpoint=stop)


if __name__=='__main__':unittest.main()
