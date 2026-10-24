"""Independent small fixtures for supervisor statistical audit conventions."""
import sys
sys.dont_write_bytecode = True
import math
import unittest
import numpy as np
from inference_tests import dm_test, coverage_tests, elementary, holm
from supervisor_inference_audit import independent_coverage, independent_dm, independent_murphy, independent_student_tail

class SupervisorInferenceFixtures(unittest.TestCase):
    def test_conditional_cc_direct_likelihood_oracle(self):
        # Transition counts are n00=6,n01=1,n10=1,n11=2; first zero is conditioned on.
        result=independent_coverage([0,0,0,0,0,0,0,1,1,1,0])
        alternative=(6/7)**6*(1/7)*(1/3)*(2/3)**2
        null=.95**7*.05**3
        common=.7**7*.3**3
        direct=2*math.log(alternative/null)
        conditional_uc=2*math.log(common/null)
        independence=2*math.log(alternative/common)
        self.assertAlmostEqual(result['cc_lr'],direct,places=12)
        self.assertAlmostEqual(result['conditional_uc_lr'],conditional_uc,places=12)
        self.assertAlmostEqual(result['ind_lr'],independence,places=12)
        self.assertAlmostEqual(result['cc_lr'],result['conditional_uc_lr']+result['ind_lr'],places=12)
        self.assertGreater(abs(result['cc_lr']-(result['pof_lr']+result['ind_lr'])),.1)
        self.assertAlmostEqual(result['cc_p'],math.exp(-direct/2),places=12)

    def test_first_one_is_omitted_for_conditional_uc(self):
        result=independent_coverage([1,0,0,1,0,1,1,0])
        conditional_uc=2*math.log(((4/7)**4*(3/7)**3)/(.95**4*.05**3))
        self.assertEqual(result['first_hit'],1)
        self.assertAlmostEqual(result['conditional_uc_lr'],conditional_uc,places=12)
        self.assertAlmostEqual(result['cc_lr'],result['conditional_uc_lr']+result['ind_lr'],places=12)

    def test_unidentified_markov_row_yields_missing_cc(self):
        for n in [12,40]:
            result=independent_coverage([0]*n)
            self.assertIsNone(result['ind_p'])
            self.assertIsNone(result['cc_p'])
            self.assertEqual(result['ind_status'],'UNIDENTIFIED_TRANSITION_ROW')
            self.assertAlmostEqual(result['pof_lr'],-2*n*math.log(.95))

    def test_scalar_hac_and_bandwidth(self):
        result=independent_dm([1.,2.,3.,4.],1,1)
        self.assertAlmostEqual(result[1],1.5625)
        self.assertAlmostEqual(result[2],4.)
        for n,h,want in [(6625,6,10),(6625,24,24),(277,6,6),(277,24,24)]:
            self.assertEqual(dm_test(np.arange(n,dtype=float),h)['bandwidth'],want)

    def test_exact_murphy_ties_and_exterior(self):
        left=np.array([0.,2.,1.,-1.,1.])
        right=np.array([2.,0.,1.,1.,2.])
        outcome=np.array([1.,1.,1.,0.,2.])
        theta,sl,sr,difference,integral,tolerance=independent_murphy(left,right,outcome)
        for index,threshold in enumerate(theta):
            self.assertAlmostEqual(sl[index],np.mean([elementary(x,y,threshold) for x,y in zip(left,outcome)]))
            self.assertAlmostEqual(sr[index],np.mean([elementary(x,y,threshold) for x,y in zip(right,outcome)]))
        for threshold in [theta[0]-1,theta[-1]+1]:
            self.assertEqual(sum(elementary(x,y,threshold) for x,y in zip(left,outcome)),0)
        loss=lambda x:.95*np.maximum(outcome-x,0)+.05*np.maximum(x-outcome,0)
        self.assertAlmostEqual(integral,np.mean(loss(left)-loss(right)))

    def test_student_independent_density_integral(self):
        for t in [0.,.2,1.,5.,20.]:
            self.assertAlmostEqual(independent_student_tail(t,1),1-2*math.atan(t)/math.pi,places=11)
            self.assertAlmostEqual(independent_student_tail(t,2),1-t/math.sqrt(t*t+2),places=11)

    def test_holm_preserves_ties_and_order(self):
        np.testing.assert_allclose(holm([.04,.002,.01,.03]),[.06,.008,.03,.06],atol=1e-15,rtol=0)
        np.testing.assert_allclose(holm([.01,.01,1.]),[.03,.03,1.],atol=1e-15,rtol=0)

if __name__=='__main__':
    unittest.main(verbosity=2)
