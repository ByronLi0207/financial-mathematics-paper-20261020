"""Known-answer tests for reading already retained inference outputs."""
import unittest
from v3_inference_presentation import family_readback

class FamilyReadback(unittest.TestCase):
    def fixture(self):
        return [dict(contrast_id=str(i),status='OK',mean_difference=str([-1,1,-2][i]),dm_p=str(p),holm_p=str(a),double_dm_p=str(d)) for i,(p,a,d) in enumerate([(0.001,0.003,0.002),(0.02,0.04,0.03),(0.04,0.04,0.06)])]
    def test_existing_and_doubled_reference_counts(self):
        z=family_readback(self.fixture())
        self.assertEqual(z['family_size'],3)
        self.assertEqual(z['base_below_05'],3)
        self.assertEqual(z['double_below_05'],1)
        self.assertAlmostEqual(z['by_id']['1']['double_holm_p'],0.06)
    def test_rejection_counts_preserve_adverse_directions(self):
        report=family_readback(self.fixture())
        self.assertEqual(report['base_direction_counts'],dict(favorable=2,adverse=1,zero=0))
        self.assertEqual(report['double_direction_counts'],dict(favorable=1,adverse=0,zero=0))
        self.assertEqual(report['base_direction_ids']['adverse'],['1'])
    def test_mismatched_archived_adjustment_fails(self):
        rows=self.fixture();rows[1]['holm_p']='0.01'
        with self.assertRaisesRegex(ValueError,'stored Holm'):
            family_readback(rows)
    def test_identical_forecasts_are_conservative_bookkeeping(self):
        rows=[dict(contrast_id='same',status='IDENTICAL_LOSSES',mean_difference='0',dm_p='',holm_p='1',double_dm_p='')]
        z=family_readback(rows)
        self.assertEqual(z['base_below_05'],0)
        self.assertEqual(z['by_id']['same']['double_holm_p'],1)
if __name__=='__main__':unittest.main()
