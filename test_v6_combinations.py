import importlib,importlib.util,unittest
import numpy as np

class CombinationTests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_combinations'),'fixed combination API not implemented')
        return importlib.import_module('v6_combinations')
    def test_arithmetic_and_median_have_independent_known_answers(self):
        r=self.api().combine_reports([10,11,12],[0,0,0],[2.,8.,4.],[4.,2.,9.],[3.,5.,6.])
        np.testing.assert_array_equal(r['MEAN_F_QR']['capacity'],[3.,5.,6.5])
        np.testing.assert_array_equal(r['MEDIAN_F_QR_KNN']['capacity'],[3.,5.,6.])
    def test_knn_equal_f_median_is_exactly_f_for_any_qr(self):
        a=self.api();f=np.array([1.,10.,3.]);r=a.combine_reports([10,11,12],[0,0,0],f,[30.,2.,.1],f)
        np.testing.assert_array_equal(r['MEDIAN_F_QR_KNN']['capacity'],f)
        self.assertEqual(r['MEDIAN_F_QR_KNN']['identity'],'EXACTLY_F')
    def test_missing_knn_is_na_without_substitution(self):
        r=self.api().combine_reports([10,11],[0,0],[2.,8.],[4.,2.],None)
        self.assertEqual(r['MEDIAN_F_QR_KNN']['status'],'NA');self.assertNotIn('capacity',r['MEDIAN_F_QR_KNN'])
        self.assertEqual(r['MEAN_F_QR']['status'],'COMPLETE')
    def test_misalignment_and_floor_breach_rejected(self):
        a=self.api()
        for ids,floor,f,q in [([10,12],[0,0],[2.,3.],[2.,3.]),([10,11],[0,4],[2.,3.],[2.,3.]),([10,11],[0,0],[2.],[2.,3.])]:
            with self.assertRaises(ValueError):a.combine_reports(ids,floor,f,q,None)
    def test_mean_does_not_claim_to_beat_best_constituent(self):
        a=self.api();r=a.combine_reports([1],[0],[0.],[10.],None)
        from v6_inference import pinball_losses
        loss=float(pinball_losses([0.],r['MEAN_F_QR']['capacity'],tau=.95)[0])
        self.assertEqual(loss,.25);self.assertGreater(loss,0.)
    def test_exact_murphy_matches_hand_threshold_scores(self):
        a=self.api();left=np.array([0.,3.,2.]);right=np.array([2.,1.,4.]);y=np.array([1.,2.,3.]);z=a.murphy_exact(left,right,y,tau=.95)
        for j,t in enumerate(z['theta']):
            def score(v):return np.mean([(int(yy<xx)-.95)*(int(t<xx)-int(t<yy)) for xx,yy in zip(v,y)])
            self.assertAlmostEqual(z['difference'][j],score(left)-score(right),places=14)
        self.assertEqual(z['comparison_grid'],'ALL_UNIQUE_BREAKPOINTS_INTEGER_EVENT_SIGNS')
    def test_murphy_known_dominance_equal_and_crossing(self):
        a=self.api()
        self.assertEqual(a.murphy_exact([1,1],[3,3],[1,1],tau=.95)['ranking'],'LEFT_DOMINATES_SAMPLE')
        self.assertEqual(a.murphy_exact([2,2],[2,2],[1,3],tau=.95)['ranking'],'EQUAL_SAMPLE')
        self.assertEqual(a.murphy_exact([0,3],[2,1],[1,2],tau=.95)['ranking'],'CROSSING')
    def test_curve_integral_equals_explicit_pinball_difference(self):
        a=self.api();z=a.murphy_exact([0,3,2],[2,1,4],[1,2,3],tau=.9)
        self.assertAlmostEqual(z['integral_difference'],z['pinball_difference'],places=14)

if __name__=='__main__':unittest.main()
