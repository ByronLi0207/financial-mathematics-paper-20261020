import unittest
import numpy as np
from round2_shrinkage import contributions,compare
class ShrinkageDiagnostics(unittest.TestCase):
 def test_projection_is_not_unprojected_contribution(self):
  z=np.array([[1.,2.],[-1.,-2.]])
  raw,actual=contributions(z,np.array([-.5,1.,0.]),2.)
  np.testing.assert_array_equal(raw,[2.,-2.]);np.testing.assert_array_equal(actual,[1.,0.])
 def test_zero_slope_and_constant_correlation(self):
  a,b=contributions(np.ones((3,2)),np.array([2.,0.,0.]),3.)
  np.testing.assert_array_equal(a,0.);np.testing.assert_array_equal(b,0.)
  r=compare(np.array([3.,3.]),np.array([3.,3.]),np.array([2.,2.]),np.array([1.,1.]))
  self.assertIsNone(r['capacity_correlation']);self.assertIsNone(r['breach_jaccard']);self.assertEqual(r['breach_union'],0)
 def test_overlap_counts_not_ordinary_accuracy(self):
  r=compare(np.array([1.,3.,3.]),np.array([3.,1.,3.]),np.array([2.,2.,4.]),np.zeros(3))
  self.assertEqual((r['left_breaches'],r['right_breaches'],r['breach_intersection'],r['breach_union'],r['breach_xor']),(2,2,1,3,2));self.assertEqual(r['breach_jaccard'],1/3)

class ManuscriptCells(unittest.TestCase):
 def test_round2_table_cells_are_formal_converter_strings(self):
  from unittest.mock import patch
  from round2_manuscript import augment_round2
  # A converter test must not depend on a private, ignored historical draft.
  c={'sections':[{'title':'Synthetic section','blocks':[]} for _ in range(9)],
     'references':[]}
  with patch('round2_levy_manuscript.augment_levy'), \
       patch('round2_panel_manuscript.augment_panel'), \
       patch('round2_baselines_manuscript.augment_baselines'):
   augment_round2(c)
  sections=[sec for sec in c['sections'] if sec['title'].startswith('Appendix I.')]
  self.assertEqual(len(sections),1)
  tables=[b for b in sections[0]['blocks'] if b['type']=='table']
  self.assertEqual(len(tables),2)
  for b in tables:
   self.assertTrue(b['rows'])
   self.assertTrue(all(isinstance(x,str) for row in b['rows'] for x in row))
