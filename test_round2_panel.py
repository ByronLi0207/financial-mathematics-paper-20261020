import unittest,csv,io
from round2_panel_sources import align_source
class PanelAlignment(unittest.TestCase):
 def make(self,rows):
  b=io.StringIO(newline='');w=csv.writer(b);w.writerow(['As Of Date','Time Series','Value (millions)']);w.writerows(rows);return b.getvalue().encode()
 def test_exact_grid_truncates_only_extra_dates(self):
  raw=self.make([['2020-01-01','KEY','2'],['2020-01-08','KEY','-3'],['2020-01-15','KEY','999']]);x,info=align_source(raw,'KEY',['2020-01-01','2020-01-08'])
  self.assertEqual(x.tolist(),[2.,-3.]);self.assertEqual(info['raw_observations'],3);self.assertEqual(info['aligned_observations'],2)
 def test_no_imputation_of_missing_date(self):
  raw=self.make([['2020-01-01','KEY','2']])
  with self.assertRaisesRegex(ValueError,'missing'):align_source(raw,'KEY',['2020-01-01','2020-01-08'])
 def test_duplicate_wrong_key_and_nonfinite_rejected(self):
  for rows in [[['2020-01-01','KEY','2'],['2020-01-01','KEY','3']],[['2020-01-01','OTHER','2']],[['2020-01-01','KEY','nan']]]:
   with self.assertRaises(ValueError):align_source(self.make(rows),'KEY',['2020-01-01'])

class PanelFitting(unittest.TestCase):
 def test_future_perturbation_preserves_both_issued_fits(self):
  import numpy as np
  from round2_panel_run import segment
  x=50+np.cumsum(np.random.default_rng(37).normal(size=300));dates=np.arange(300).astype('datetime64[W]');o=np.arange(200,221);changed=x.copy();changed[211:]+=500
  for method in ['QR33','C2_QR4']:
   a,_=segment(x,dates,o,6,52,method,.1,lambda **kw:None)
   b,_=segment(changed,dates,o,6,52,method,.1,lambda **kw:None)
   np.testing.assert_array_equal(a[o<=210],b[o<=210])
 def test_common_strict_menu_rejects_failure(self):
  from conditional_study import select_parameter
  rows=[dict(parameter=.01,status='COMPLETE',origin_count=2,mean_pinball=1.),dict(parameter=.1,status='FAILED')]
  r=select_parameter(rows,[.01,.1],expected_count=2);self.assertEqual(r['status'],'INELIGIBLE');self.assertIsNone(r['parameter'])
