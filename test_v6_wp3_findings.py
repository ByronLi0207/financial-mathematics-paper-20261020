import unittest
from v6_wp3_findings import build

class FindingsTests(unittest.TestCase):
    def test_both_beats_requires_strict_improvement_and_na_never_vanishes(self):
        common=dict(original=False,horizon=6,source='synthetic',window=20,identity=None)
        mean=[dict(**common,method='MEAN_F_QR',status='COMPLETE',percent_vs_F=-2,percent_vs_QR=-1),dict(**common,method='MEAN_F_QR',status='COMPLETE',percent_vs_F=-2,percent_vs_QR=0)]
        median=[dict(**common,method='MEDIAN_F_QR_KNN',status='NA')]
        z=build(dict(method_rows=mean+median,murphy=[]))
        self.assertEqual(z['counts']['MEAN_F_QR']['lower_than_both'],1)
        self.assertEqual(z['counts']['MEDIAN_F_QR_KNN']['na'],1)
if __name__=='__main__':unittest.main()
