import copy
import unittest
from v6_wp2_findings import build

class PresentationTests(unittest.TestCase):
    def fixture(self):
        methods=[];controls=[]
        for s in ('a','b'):
            for h in (6,24):
                for w in (50,100):
                    for m,loss,hits in [('ACI_QR',80.,4),('ACI_F',100.,5),('SAV',110.,6),('QR',90.,7),('frozen_F',105.,8)]:
                        r=dict(source=s,horizon=h,window=w,method=m,status='COMPLETE',scores=dict(mean_loss=loss,full_hits=hits,n=100,full_rate=hits/100,coverage_distance=abs(hits/100-.05)))
                        (controls if m in ('QR','frozen_F') else methods).append(r)
        phases=[dict(status=z,resources=dict(peak_rss_bytes=1000,elapsed_seconds=2.,maximum_observed_os_threads=1)) for z in ('COMPLETE','NA')]
        return dict(method_rows=methods,control_rows=controls),dict(family_n=56,raw_na_count=5),phases
    def test_pair_percent_denominator_and_preserved_eight_cells(self):
        a,b,c=self.fixture();z=build(a,b,c)
        self.assertEqual(len(z['wrapped_pairs']),8)
        self.assertAlmostEqual(z['wrapped_pairs'][0]['qr_minus_f_loss_percent'],-20.)
        self.assertEqual(z['wrapped_pairs'][0]['qr_hits'],4)
        self.assertEqual(z['resources']['na_phase_count'],1)
    def test_failed_pair_does_not_disappear(self):
        a,b,c=self.fixture();a['method_rows'][0]['status']='NA';z=build(a,b,c)
        self.assertEqual(z['wrapped_pairs'][0]['status'],'NA');self.assertEqual(len(z['wrapped_pairs']),8)
        self.assertEqual(z['method_inventory']['ACI_QR']['na'],1)
if __name__=='__main__':unittest.main()
