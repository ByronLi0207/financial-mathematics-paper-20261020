import unittest
import numpy as np
from parsimonious_v3 import features4,standardize
class CausalFourFeatures(unittest.TestCase):
    def test_current_and_rms_known(self):
        x=np.arange(120.)-50;t=np.arange(120).astype('datetime64[D]')
        v,valid=features4(x,t,6,26,86400)
        self.assertEqual(v.shape,(120,4));self.assertEqual(valid,26)
        np.testing.assert_allclose(v[60],[10.,10.,1.,1.],rtol=0,atol=2e-15)
    def test_future_changes_do_not_change_issued_features(self):
        x=np.sin(np.arange(120.));t=np.arange(120).astype('datetime64[D]')
        a,_=features4(x,t,6,26,86400);x[81:]+=1000;b,_=features4(x,t,6,26,86400)
        np.testing.assert_array_equal(a[26:81],b[26:81])
    def test_training_transform_constant_and_causal(self):
        a=np.array([[1.,2.,4.,0.],[1.,4.,8.,0.]])
        z,mu,scale=standardize(a)
        np.testing.assert_array_equal(z[:,[0,3]],0.)
        np.testing.assert_array_equal(mu,[1.,3.,6.,0.]);np.testing.assert_array_equal(scale,[1.,1.,2.,1.])
if __name__=='__main__':unittest.main(verbosity=2)
