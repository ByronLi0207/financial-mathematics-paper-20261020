"""Toy-only checks for the data-description generator; no financial parsing."""
import importlib
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest


class DescriptiveTests(unittest.TestCase):
    def call(self,name,*args,**kwargs):
        self.assertIsNotNone(importlib.util.find_spec('report_v12_descriptives'),
                             'new descriptive generator is required')
        module = importlib.import_module('report_v12_descriptives')
        self.assertTrue(callable(getattr(module,name,None)),name)
        return getattr(module,name)(*args,**kwargs)

    def test_h6_includes_anchor_and_uses_same_complete_origins(self):
        result = self.call('describe_series',[100.,1.,2.,3.,4.,5.,6.,7.])
        self.assertEqual(result['N'],8)
        self.assertEqual(result['origin_count'],2)
        self.assertEqual((result['first_origin'],result['last_origin']),(0,1))
        stats = result['statistics']
        self.assertEqual(stats['abs_N_mean'],50.5)
        self.assertAlmostEqual(stats['abs_N_sd'],math.sqrt(9801/2))
        self.assertEqual(stats['peak_Y_mean'],53.5)
        self.assertEqual(stats['headroom_Z_mean'],3.)
        self.assertAlmostEqual(stats['headroom_Z_sd'],math.sqrt(18))
        self.assertEqual(stats['headroom_Z_p95'],6.)

    def test_empirical_p95_is_lower_inverted_cdf_without_interpolation(self):
        result = self.call('describe_series',list(range(26)))
        self.assertEqual(result['origin_count'],20)
        self.assertEqual(result['statistics']['abs_N_p95'],18.)
        self.assertEqual(result['statistics']['peak_Y_p95'],24.)
        self.assertEqual(result['statistics']['headroom_Z_sd'],0.)

    def test_usd_scaling_applies_to_each_of_nine_statistics(self):
        positions = [100000000.,1000000.,2000000.,3000000.,4000000.,5000000.,6000000.,7000000.]
        result = self.call('describe_series',positions,display_divisor=1000000.)
        self.assertEqual(result['statistics']['abs_N_mean'],50.5)
        self.assertEqual(result['statistics']['peak_Y_mean'],53.5)
        self.assertEqual(result['statistics']['headroom_Z_p95'],6.)
        self.assertAlmostEqual(result['statistics']['headroom_Z_sd'],math.sqrt(18))

    def test_multi_series_summary_is_median_of_each_within_series_statistic(self):
        keys = ['abs_N_mean','abs_N_sd','abs_N_p95','peak_Y_mean','peak_Y_sd',
                'peak_Y_p95','headroom_Z_mean','headroom_Z_sd','headroom_Z_p95']
        rows = [dict(family='panel',source_key=str(i),display_statistics={k:value for k in keys},
                     N=100+i,origin_count=94+i,display_unit='USD millions')
                for i,value in enumerate([1.,100.,3.])]
        result = self.call('aggregate_statistics',rows)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['series_count'],3)
        self.assertEqual(result[0]['aggregation'],'median of within-series statistics')
        self.assertEqual(result[0]['statistics'],{k:3. for k in keys})

    def test_missing_f3_completion_gate_stops_before_source_access_or_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'F3_COMPLETION_GATE'):
                self.call('run',root=tmp)
            self.assertFalse((Path(tmp)/'results/v12/descriptives').exists())


if __name__=='__main__':
    unittest.main()
