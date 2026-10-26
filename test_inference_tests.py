"""Known-answer artificial tests, independent of the financial data."""
import math, unittest
import numpy as np
from inference_tests import dm_test, student_two_sided, coverage_tests, holm, elementary, murphy, chi_tail, dq_hac

class KnownAnswers(unittest.TestCase):
    def test_dm_known_bartlett_and_hln(self):
        z=dm_test([1.,2.,3.,4.],1,1)
        self.assertAlmostEqual(z['lrv'],1.5625)
        self.assertAlmostEqual(z['dm_t'],4.)
        self.assertAlmostEqual(z['dm_p'],.00006334248366623992)
        self.assertAlmostEqual(z['hln_t'],math.sqrt(12))
        self.assertAlmostEqual(z['hln_p'],.04051932635383382)
    def test_dm_horizon_two_known(self):
        z=dm_test([1.,2.,3.,4.],2,2)
        self.assertAlmostEqual(z['lrv'],17/12)
        self.assertAlmostEqual(z['dm_t'],4.20084025208403)
        self.assertAlmostEqual(z['hln_p'],.08231560255047188)
    def test_dm_sign_and_degenerate(self):
        a=dm_test([1.,2.,3.,4.],1,1);b=dm_test([-1.,-2.,-3.,-4.],1,1)
        self.assertEqual(a['dm_t'],-b['dm_t']);self.assertEqual(a['dm_p'],b['dm_p'])
        self.assertEqual(dm_test([0.]*20,2)['status'],'IDENTICAL_LOSSES')
        self.assertEqual(dm_test([2.]*20,2)['status'],'ZERO_LONG_RUN_VARIANCE')
    def test_student_against_closed_forms(self):
        for t in [0.,.1,1.,4.,20.]:
            self.assertAlmostEqual(student_two_sided(t,1),1-2*math.atan(t)/math.pi,places=12)
            self.assertAlmostEqual(student_two_sided(t,2),1-t/math.sqrt(t*t+2),places=12)
            u=t/math.sqrt(3)
            self.assertAlmostEqual(student_two_sided(t,3),1-2/math.pi*(math.atan(u)+u/(1+u*u)),places=12)
    def test_kupiec_known(self):
        z=coverage_tests([1,1]+[0]*18)
        self.assertAlmostEqual(z['pof_lr'],.826168756509853)
        self.assertAlmostEqual(z['pof_p'],.3633827177060031)
        z=coverage_tests([0]*20)
        self.assertAlmostEqual(z['pof_lr'],-40*math.log(.95))
        self.assertIsNone(z['ind_p']);self.assertIsNone(z['cc_p'])
    def test_christoffersen_known(self):
        z=coverage_tests([0,0,0,0,0,0,0,1,1,1,0])
        self.assertEqual([z[k] for k in ['n00','n01','n10','n11']],[6,1,1,2])
        self.assertAlmostEqual(z['ind_lr'],2.656572575291266)
        self.assertAlmostEqual(z['ind_p'],.10312272670368894)
        self.assertAlmostEqual(z['cc_lr'],8.560701324137902)
        self.assertAlmostEqual(z['cc_p'],.013837808840926764)
    def test_holm_known_and_order(self):
        np.testing.assert_allclose(holm([.01,.04,.03,.002]),[.03,.06,.06,.008],rtol=0,atol=1e-15)
    def test_murphy_crossing_and_integral(self):
        self.assertEqual(elementary(0.,1.,0.),.95)
        self.assertAlmostEqual(elementary(2.,1.,1.),.05)
        z=murphy([0.],[2.],[1.])
        self.assertEqual(z['ranking'],'CROSSING')
        self.assertAlmostEqual(z['integral_difference'],.9)
        self.assertAlmostEqual(z['pinball_difference'],.9)
    def test_bad_inputs(self):
        with self.assertRaises(ValueError):coverage_tests([0,2])
        with self.assertRaises(ValueError):dm_test([1.,float('nan')],1)
        with self.assertRaises(ValueError):holm([-.1])
    def test_chi_square_six_known(self):
        for x in [0.,.1,1.,5.,12.,50.]:
            self.assertAlmostEqual(chi_tail(x,6),math.exp(-x/2)*(1+x/2+(x/2)**2/2),places=13)
    def test_dq_unidentified_hits(self):
        z=dq_hac([0]*100,list(range(100)),6)
        self.assertEqual(z['status'],'RANK_DEFICIENT');self.assertIsNone(z['p'])
if __name__=='__main__':unittest.main(verbosity=2)
