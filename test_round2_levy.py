import itertools,unittest
from statistics import NormalDist
import numpy as np
from round2_levy import predict,corrected_endpoint_rank,gaussian_endpoint_variance
class LevyBaseline(unittest.TestCase):
 def test_exact_independent_symmetric_maximal_inequality(self):
  for h in range(1,9):
   s=np.cumsum(np.array(list(itertools.product([-1.,1.],repeat=h))),axis=1)
   for c in np.arange(0,h+.5,.5):self.assertLessEqual(np.mean(np.max(np.abs(s),axis=1)>c),2*np.mean(np.abs(s[:,-1])>c))
  self.assertEqual(float(np.mean(np.max(np.abs(np.array([[1.,0.],[1.,2.],[-1.,0.],[-1.,-2.]])),axis=1)>.5)),1.)
 def test_discrete_population_quantile_triangle_corollary(self):
  h=8;s=np.cumsum(np.array(list(itertools.product([-1.,1.],repeat=h))),axis=1);a=np.sort(np.abs(s[:,-1]));q=a[int(np.ceil(.975*len(a)))-1]
  self.assertLessEqual(np.mean(np.abs(s[:,-1])>q),.025)
  for x in [-4.,0.,.5,4.]:self.assertLessEqual(np.mean(np.max(np.abs(x+s),axis=1)>abs(x)+q),.05)
 def test_rank_and_gaussian_variance(self):
  self.assertEqual([corrected_endpoint_rank(w) for w in [52,260,720,2880]],[52,255,703,2809])
  self.assertEqual(gaussian_endpoint_variance(6,0),6.)
  self.assertAlmostEqual(gaussian_endpoint_variance(6,.5),sum(.5**abs(i-j) for i in range(6) for j in range(6)))
  self.assertAlmostEqual(2*(1-NormalDist().cdf(NormalDist().inv_cdf(.9875))),.025)
 def test_future_perturbation_and_truncation(self):
  x=np.cumsum(np.random.default_rng(5).normal(size=300));o=np.arange(140,211);a=predict(x,o,6,52,13);xx=x.copy();xx[201:]+=1e6;b=predict(xx,o,6,52,13)
  np.testing.assert_array_equal(a['capacity'][o<=200],b['capacity'][o<=200]);c=predict(x[:201],o[o<=200],6,52,13);np.testing.assert_array_equal(a['capacity'][o<=200],c['capacity'])
 def test_exact_mature_endpoint_pool(self):
  x=np.arange(120.)**2;o=np.arange(80,83);r=predict(x,o,6,52,13);pool=np.arange(80-6-52+1,80-6+1);q=np.sort(np.abs(x[pool+6]-x[pool]))[-1]
  np.testing.assert_array_equal(r['capacity'],np.abs(x[o])+q);self.assertTrue(np.all(r['latest_label_end']<=o))

class IndependenceBoundary(unittest.TestCase):
 def test_symmetric_but_dependent_counterexample(self):
  increments=np.array([[1.,-1.],[-1.,1.]])
  partial=np.cumsum(increments,axis=1)
  self.assertEqual(float(np.mean(np.max(np.abs(partial),axis=1)>0)),1.)
  self.assertEqual(float(2*np.mean(np.abs(partial[:,-1])>0)),0.)
