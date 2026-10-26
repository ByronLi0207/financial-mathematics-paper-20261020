"""Constructed input tests and saved-metadata grid checks; no financial labels."""
from pathlib import Path
import csv
import hashlib
import importlib
import importlib.util
import io
import tempfile
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parent


class InputTests(unittest.TestCase):
    def call(self, name, *args, **kwargs):
        self.assertIsNotNone(importlib.util.find_spec('v12_inputs'),
                             'new v12 input implementation is required')
        module = importlib.import_module('v12_inputs')
        self.assertTrue(callable(getattr(module, name, None)),
                        'missing input API: '+name)
        return getattr(module, name)(*args, **kwargs)

    def fixture(self, root, family, name, raw, **extra):
        path = Path(root)/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return dict(family=family, key=extra.pop('key', family), path=str(path),
                    sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                    short_scale=6, long_scale=26, nominal_gap_seconds=604800,
                    unit='USD millions', **extra)

    def test_saved_inventory_has_fixed_sources_and_current_bill(self):
        rows = self.call('source_inventory', ROOT)
        counts = {family:sum(r['family']==family for r in rows)
                  for family in ('cftc','panel','bill','fx')}
        self.assertEqual(counts, dict(cftc=17, panel=12, bill=1, fx=1))
        self.assertEqual(rows[0]['key'], '044601')
        panel = [r['key'] for r in rows if r['family']=='panel']
        self.assertEqual(panel[:3], ['PDPOSMBS-TOT','PDPOSCS-TOT','PDPOSFGS-TOT'])
        bill = next(r for r in rows if r['family']=='bill')
        self.assertEqual(Path(bill['path']), ROOT/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv')
        self.assertEqual(bill['N'], 706)
        for row in rows:
            self.assertNotIn('修订v3', row['path'])
            self.assertEqual(len(row['sha256']), 64)

    def test_f1_keeps_all_geometries_and_original_common_gap(self):
        rows = self.call('cells_for', 'F1', ROOT)
        self.assertEqual(len(rows), 90)
        self.assertEqual(len({r['cell_id'] for r in rows}), 90)
        self.assertEqual({r['period'] for r in rows}, {'original'})
        first = rows[0]
        self.assertEqual((first['source_key'],first['horizon'],first['window']),
                         ('044601',6,52))
        self.assertEqual((first['validation_first'],first['validation_last'],
                          first['evaluation_first'],first['evaluation_last']),
                         (553,604,611,870))
        for row in rows:
            gap = row['evaluation_first']-row['validation_last']-1
            self.assertEqual(gap, 6 if row['family']=='cftc' else 24)
            self.assertEqual(row['tau'], .95)
        self.assertEqual(sum(r['family']=='panel' for r in rows), 48)

    def test_f2_grid_keeps_eval_and_has_nested_matching_refit_starts(self):
        rows = self.call('cells_for', 'F2', ROOT)
        self.assertEqual(len(rows), 68)
        self.assertEqual(len({r['cell_id'] for r in rows}), 68)
        arm = [r for r in rows if r['source_key']=='044601' and r['window']==260]
        self.assertEqual([(r['validation_n'],r['validation_first'],r['validation_last'])
                          for r in arm], [(52,553,604),(156,449,604)])
        for row in rows:
            self.assertEqual((row['evaluation_first'],row['evaluation_last']), (611,870))
            self.assertEqual(row['evaluation_first']-row['validation_last']-1, 6)
            self.assertEqual(row['validation_first'] % 13, 7)

    def test_f3_priority_and_two_matched_fx_periods_are_preserved(self):
        rows = self.call('cells_for', 'F3', ROOT)
        self.assertEqual(len(rows), 74)
        self.assertEqual(len({r['cell_id'] for r in rows}), 74)
        self.assertEqual([r['tau'] for r in rows[:37]], [.99]*37)
        fx = [r for r in rows if r['family']=='fx' and r['tau']==.99]
        self.assertEqual([(r['period'],r['validation_first'],r['validation_last'],
                          r['evaluation_first'],r['evaluation_last']) for r in fx],
                         [('original',10463,11902,11927,18551),
                          ('early2015',7535,8974,8999,10438)])
        self.assertTrue(all((r['horizon'],r['window'],r['refit_step'])==(6,2880,24)
                            for r in fx))
        self.assertEqual(sum(r['family']=='bill' for r in rows), 2)

    def test_eligibility_rejects_whole_contract_at_718_and_accepts_719(self):
        no = self.call('eligibility', 718)
        yes = self.call('eligibility', 719)
        self.assertFalse(no['eligible'])
        self.assertEqual(no['earliest_training_origin'], 25)
        self.assertEqual(no['minimum_N'], 719)
        self.assertTrue(yes['eligible'])
        self.assertEqual(yes['earliest_training_origin'], 26)
        saved = self.call('f2_eligibility_inventory', ROOT)
        self.assertEqual(len(saved),17)
        self.assertTrue(all(r['eligible'] for r in saved))

    def test_hash_mismatch_is_rejected_before_malformed_csv_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.fixture(tmp,'fx','bad.csv',b'not,csv\n')
            source['sha256'] = '0'*64
            with self.assertRaisesRegex(ValueError,'SOURCE_HASH_MISMATCH'):
                self.call('load_series',source,tmp)

    def test_byte_mismatch_is_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.fixture(tmp,'bill','bad.csv',b'not,csv\n')
            source['bytes'] += 1
            with self.assertRaisesRegex(ValueError,'SOURCE_SIZE_MISMATCH'):
                self.call('load_series',source,tmp)

    def test_fx_preserves_naive_hourly_gaps_and_signed_positions(self):
        raw = (b'datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n'
               b'2015.01.01T01:00:00.000,-2,0,0,0\n'
               b'2015.01.03T05:00:00.000,3,0,0,0\n')
        with tempfile.TemporaryDirectory() as tmp:
            s = self.fixture(tmp,'fx','fx.csv',raw,key='fx_hourly',N=2,raw_rows=2)
            result = self.call('load_series',s,tmp)
            np.testing.assert_array_equal(result['position'],[-2.,3.])
            np.testing.assert_array_equal(result['times'],np.array(
                ['2015-01-01T01:00','2015-01-03T05:00'],dtype='datetime64[us]'))
            np.testing.assert_array_equal(result['times'],result['actual_dates'])
            self.assertFalse(result['position'].flags.writeable)

    def test_bill_uses_own_key_and_chronology(self):
        raw = (b'As Of Date,Time Series,Value (millions)\n'
               b'2020-01-01,PDPOSGS-B,-7\n2020-01-08,PDPOSGS-B,8\n')
        with tempfile.TemporaryDirectory() as tmp:
            s = self.fixture(tmp,'bill','bill.csv',raw,key='PDPOSGS-B',N=2,raw_rows=2)
            result = self.call('load_series',s,tmp)
            np.testing.assert_array_equal(result['position'],[-7.,8.])
            self.assertEqual(result['metadata']['N'],2)
            self.assertEqual(str(result['times'][-1]),'2020-01-08T00:00:00.000000')

    def test_panel_aligns_to_pinned_bill_grid_without_extending_sample(self):
        bill = (b'As Of Date,Time Series,Value (millions)\n'
                b'2020-01-01,PDPOSGS-B,0\n2020-01-08,PDPOSGS-B,0\n')
        panel = (b'As Of Date,Time Series,Value (millions)\n'
                 b'2020-01-01,PANEL,-5\n2020-01-08,PANEL,9\n2020-01-15,PANEL,100\n')
        with tempfile.TemporaryDirectory() as tmp:
            grid = self.fixture(tmp,'bill','bill.csv',bill,key='PDPOSGS-B',N=2,raw_rows=2)
            s = self.fixture(tmp,'panel','panel.csv',panel,key='PANEL',N=2,raw_rows=3,
                             grid_source=grid)
            result = self.call('load_series',s,tmp)
            np.testing.assert_array_equal(result['position'],[-5.,9.])
            self.assertEqual(result['metadata']['raw_rows'],3)
            self.assertEqual(result['metadata']['N'],2)
            self.assertFalse(result['metadata']['imputed'])

    def test_panel_missing_grid_date_is_terminal_not_filled(self):
        bill = (b'As Of Date,Time Series,Value (millions)\n'
                b'2020-01-01,PDPOSGS-B,0\n2020-01-08,PDPOSGS-B,0\n')
        panel = (b'As Of Date,Time Series,Value (millions)\n2020-01-08,PANEL,9\n')
        with tempfile.TemporaryDirectory() as tmp:
            grid = self.fixture(tmp,'bill','bill.csv',bill,key='PDPOSGS-B',N=2,raw_rows=2)
            s = self.fixture(tmp,'panel','panel.csv',panel,key='PANEL',N=2,raw_rows=1,
                             grid_source=grid)
            with self.assertRaisesRegex(ValueError,'MISSING_REQUIRED_DATES'):
                self.call('load_series',s,tmp)

    def test_cftc_keeps_actual_dates_separate_from_monday_model_clock(self):
        stream = io.BytesIO()
        np.savez_compressed(stream,position=np.array([-3.,4.]),
                            actual_dates=np.array(['2020-01-07','2020-01-14'],dtype='datetime64[D]'),
                            model_dates=np.array(['2020-01-06','2020-01-13'],dtype='datetime64[us]'))
        with tempfile.TemporaryDirectory() as tmp:
            s = self.fixture(tmp,'cftc','cftc.npz',stream.getvalue(),key='044601',N=2)
            result = self.call('load_series',s,tmp)
            self.assertEqual(str(result['times'][0]),'2020-01-06T00:00:00.000000')
            self.assertEqual(str(result['actual_dates'][0]),'2020-01-07')
            np.testing.assert_array_equal(result['position'],[-3.,4.])

    def test_invalid_chronology_and_nonfinite_positions_are_rejected(self):
        cases = [
            (b'2020-01-08,PDPOSGS-B,1\n2020-01-01,PDPOSGS-B,2\n','SOURCE_CHRONOLOGY'),
            (b'2020-01-01,PDPOSGS-B,nan\n2020-01-08,PDPOSGS-B,2\n','SOURCE_POSITION'),
            (b'2020-01-01,WRONG,1\n2020-01-08,WRONG,2\n','SOURCE_KEY')]
        for body, reason in cases:
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as tmp:
                s = self.fixture(tmp,'bill','bill.csv',
                    b'As Of Date,Time Series,Value (millions)\n'+body,
                    key='PDPOSGS-B',N=2,raw_rows=2)
                with self.assertRaisesRegex(ValueError,reason):
                    self.call('load_series',s,tmp)

    def test_snapshot_is_exclusive_private_copy_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = self.fixture(tmp,'fx','source.csv',b'original bytes\n')
            destination = Path(tmp)/'.scratch/v12/inputs/fx.csv'
            result = self.call('ensure_source_snapshot',s,destination,tmp)
            self.assertEqual(Path(result['path']),destination.resolve())
            self.assertEqual(destination.read_bytes(),b'original bytes\n')
            self.call('ensure_source_snapshot',s,destination,tmp)
            destination.write_bytes(b'altered bytes\n')
            with self.assertRaisesRegex(ValueError,'SOURCE_'):
                self.call('ensure_source_snapshot',s,destination,tmp)
            self.assertEqual(destination.read_bytes(),b'altered bytes\n')
            self.assertEqual(Path(s['path']).read_bytes(),b'original bytes\n')
            with self.assertRaisesRegex(ValueError,'PRIVATE_DESTINATION_REQUIRED'):
                self.call('ensure_source_snapshot',s,Path(tmp)/'public.csv',tmp)

    def test_symlink_source_and_snapshot_descendants_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = self.fixture(tmp,'fx','source.csv',b'original bytes\n')
            link = Path(tmp)/'linked.csv'
            link.symlink_to(Path(s['path']))
            linked = dict(s,path=str(link))
            with self.assertRaisesRegex(ValueError,'SOURCE_SYMLINK'):
                self.call('load_series',linked,tmp)
            private = Path(tmp)/'.scratch/v12'
            private.mkdir(parents=True)
            (private/'linked').symlink_to(Path(tmp),target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'SOURCE_SYMLINK'):
                self.call('ensure_source_snapshot',s,private/'linked/copied.csv',tmp)


if __name__ == '__main__':
    unittest.main()
