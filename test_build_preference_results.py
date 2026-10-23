"""Behavioral admission tests for fixed-report archive assembly."""
import csv
from pathlib import Path
import tempfile
import unittest

import build_preference_results as builder


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'summary.csv'
        self.fields = ['source','horizon','window','method','native_unit',
                       'origin_count','mean_positive_overrun','mean_unused_allowance',
                       'mean_pinball','strict_breach_count']
        self.row = dict(zip(self.fields, ['fx_hourly','6','720','QR','USD',
                                         '6625','2','10','2.4','5']))

    def write(self, rows):
        with self.path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=self.fields);w.writeheader();w.writerows(rows)

    def test_exact_archive_components_preserved_and_score_reconciled(self):
        self.write([self.row])
        rows=builder.read_rows(self.path, {'QR'})
        self.assertEqual(rows[0]['mean_positive_overrun'],'2')

    def test_wrong_pinball_identity_is_not_admitted(self):
        self.write([{**self.row,'mean_pinball':'9'}])
        with self.assertRaisesRegex(ValueError,'SCORE_IDENTITY'):
            builder.read_rows(self.path,{'QR'})

    def test_duplicate_method_cell_is_not_admitted(self):
        self.write([self.row,self.row])
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):
            builder.read_rows(self.path,{'QR'})

    def test_wrong_count_unit_and_nonfinite_components_are_not_admitted(self):
        for field,value in [('origin_count','6624'),('native_unit','USD millions'),
                            ('mean_positive_overrun','NaN'),('strict_breach_count','6626')]:
            with self.subTest(field=field):
                self.write([{**self.row,field:value}])
                with self.assertRaises(ValueError):builder.read_rows(self.path,{'QR'})

    def test_exported_boundaries_use_canonical_rationals_including_endpoints(self):
        rows=[{**self.row,'method':name} for name in sorted(builder.METHODS)]
        group=builder.group_result(('full','fx_hourly',6,720),rows)
        self.assertEqual([p['alpha'] for p in group['frontier']['points']],['0/1','1/1'])
        self.assertEqual(group['frontier']['regions'][0]['left'],'0/1')


if __name__=='__main__':unittest.main()
