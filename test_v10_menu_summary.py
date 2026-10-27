"""Artificial scalar fixtures only; no financial/simulation archives are read."""
import copy
import importlib
import json
from pathlib import Path
import unittest


def design(required_joint=2):
    return dict(
        windows=[52, 260], arms=['constant', 'switching'],
        conditional_methods=['QR33', 'QR4'],
        menus={m: [.001, .01, .1, 1., 10., 'inf'] for m in ['QR33', 'QR4']},
        evaluation_first=3168, evaluation_last=3239,
        M1=dict(arm='constant', window=52, method='QR33',
                lower_inclusive_pct=-5., upper_inclusive_pct=5.),
        M2=dict(window=52, method='QR33', minimum_inclusive_percentage_points=5.),
        M3=dict(window=52, method='QR33', minimum_joint_improved_sources=required_joint))


def records(sources=('a', 'b'), repetitions=2):
    """New constant=0%, switching=10%; matched old values=20%."""
    return [dict(rep=rep, source_id=s, arm=arm, window=w, method=m,
                 status='COMPLETE', qr_mean_loss=100. if arm == 'constant' else 110.,
                 f_mean_loss=100., qr_breaches=4, f_breaches=3, n=72,
                 selected_penalty='inf' if rep == 0 else .01,
                 qr_reason=None, f_reason=None, original_status='COMPLETE',
                 original_qr_mean_loss=120., original_f_mean_loss=100.)
            for s in sources for arm in ['constant', 'switching']
            for w in [52, 260] for m in ['QR33', 'QR4']
            for rep in range(repetitions)]


def pick(rows, *, source='a', arm='constant', window=52, method='QR33'):
    return next(x for x in rows if x.get('source_id', source) == source
                and x['arm'] == arm and x['window'] == window and x['method'] == method)


def change_primary(data, source, arm, new_pct, old_pct=20.):
    for row in data:
        if (row['source_id'], row['arm'], row['window'], row['method']) == (source, arm, 52, 'QR33'):
            row['qr_mean_loss'] = 100. + new_pct
            row['original_qr_mean_loss'] = 100. + old_pct


class MenuSummaryTests(unittest.TestCase):
    def api(self):
        self.assertTrue(Path(__file__).with_name('v10_menu_summary.py').is_file(),
                        'the pure E1 summary implementation is absent')
        return importlib.import_module('v10_menu_summary')

    def run_summary(self, data=None, sources=('a', 'b'), repetitions=2, settings=None):
        return self.api().summarize(records(sources, repetitions) if data is None else data,
                                    repetitions, list(sources), design() if settings is None else settings)

    def test_complete_cell_has_hand_calculated_median_iqr_old_pair_and_inf_count(self):
        # Catches quantiles of pooled means, wrong interpolation, or omitted inf selections.
        data = records(repetitions=4)
        target = [x for x in data if (x['source_id'], x['arm'], x['window'], x['method'])
                  == ('a', 'constant', 52, 'QR33')]
        for row, value in zip(target, [90., 100., 110., 120.]):
            row['qr_mean_loss'] = value
            row['selected_penalty'] = 'inf' if row['rep'] in [0, 3] else .01
        result = self.run_summary(data, repetitions=4)
        cell = pick(result['cells'])
        self.assertEqual(cell['status'], 'COMPLETE')
        self.assertEqual(cell['completed_repetitions'], 4)
        self.assertAlmostEqual(cell['relative_median_pct'], 5.)
        # Literal result of the inherited a+(b-a)*fraction quartile arithmetic.
        self.assertEqual(cell['q25'], -2.5)
        self.assertAlmostEqual(cell['q75'], 12.5)
        self.assertAlmostEqual(cell['original_relative_median_pct'], 20.)
        self.assertEqual(cell['selected_inf_count'], 2)

    def test_across_sources_uses_equal_weight_source_medians_not_pooled_repetitions(self):
        # Source medians 0 and10 imply5; all six repetition values have pooled median10.
        data = records(repetitions=3)
        for source, values in [('a', [100., 100., 200.]), ('b', [110., 110., 110.])]:
            for row in data:
                if (row['source_id'], row['arm'], row['window'], row['method']) == (source, 'constant', 52, 'QR33'):
                    row['qr_mean_loss'] = values[row['rep']]
        group = pick(self.run_summary(data, repetitions=3)['across_sources'])
        self.assertEqual(group['status'], 'COMPLETE')
        self.assertEqual(group['complete_sources'], 2)
        self.assertAlmostEqual(group['median_pct'], 5.)
        self.assertAlmostEqual(group['q25'], 2.5)
        self.assertAlmostEqual(group['q75'], 7.5)

    def test_missing_repetition_has_no_partial_cell_or_successful_source_median(self):
        data = records()
        data.remove(next(x for x in data if (x['source_id'], x['arm'], x['window'], x['method'], x['rep'])
                         == ('a', 'constant', 52, 'QR33', 1)))
        result = self.run_summary(data)
        cell = pick(result['cells'])
        self.assertEqual(cell['status'], 'FAILED')
        self.assertEqual(cell['completed_repetitions'], 1)
        self.assertIsNone(cell['relative_median_pct'])
        self.assertIsNone(cell['q25'])
        group = pick(result['across_sources'])
        self.assertEqual(group['status'], 'UNASSESSABLE')
        self.assertIsNone(group['median_pct'])
        self.assertEqual(group['missing_sources'], ['a'])
        self.assertEqual(pick(result['cells'], method='QR4')['status'], 'COMPLETE')

    def test_duplicate_repetition_fails_cell_without_deduplicating(self):
        data = records()
        data.append(copy.deepcopy(pick(data)))
        cell = pick(self.run_summary(data)['cells'])
        self.assertEqual(cell['status'], 'FAILED')
        self.assertEqual(cell['duplicate_repetitions'], [0])
        self.assertIsNone(cell['relative_median_pct'])
        self.assertIsNone(cell['original_relative_median_pct'])

    def test_out_of_plan_repetition_is_not_silently_paired_with_a_different_old_subset(self):
        data = records()
        extra = copy.deepcopy(pick(data)); extra['rep'] = 2
        extra['original_qr_mean_loss'] = 900.
        data.append(extra)
        cell = pick(self.run_summary(data)['cells'])
        self.assertEqual(cell['status'], 'FAILED')
        self.assertEqual(cell['unexpected_repetitions'], [2])
        self.assertIsNone(cell['original_relative_median_pct'])

    def test_missing_entire_source_still_emits_planned_inventory_and_unknown_group(self):
        data = [x for x in records() if x['source_id'] == 'a']
        result = self.run_summary(data)
        self.assertEqual(len(result['cells']), 16)
        group = pick(result['across_sources'])
        self.assertEqual(group['complete_sources'], 1)
        self.assertEqual(group['status'], 'UNASSESSABLE')
        self.assertIsNone(group['median_pct'])
        self.assertEqual(result['predictions']['M1']['status'], 'UNASSESSABLE')

    def test_invalid_or_failed_new_record_does_not_leak_partial_results_or_nan(self):
        for field, value in [('status', 'FAILED'), ('n', 71), ('f_mean_loss', 0.),
                             ('qr_mean_loss', float('nan')), ('f_mean_loss', float('inf')),
                             ('qr_breaches', 73), ('selected_penalty', None)]:
            with self.subTest(field=field, value=value):
                data = records(); row = pick(data)
                row[field] = value; row['qr_reason'] = 'ARTIFICIAL_FAILURE'
                result = self.run_summary(data); cell = pick(result['cells'])
                self.assertEqual(cell['status'], 'FAILED')
                self.assertIsNone(cell['relative_median_pct'])
                self.assertIn('ARTIFICIAL_FAILURE', str(cell['failures']))
                json.dumps(result, allow_nan=False)

    def test_old_incomplete_keeps_new_summary_but_m3_is_unknown(self):
        data = records(); row = pick(data)
        row.update(original_status='FAILED', original_qr_mean_loss=None)
        result = self.run_summary(data); cell = pick(result['cells'])
        self.assertEqual(cell['status'], 'COMPLETE')
        self.assertEqual(cell['relative_median_pct'], 0.)
        self.assertEqual(cell['original_status'], 'FAILED')
        self.assertIsNone(cell['original_relative_median_pct'])
        self.assertIsNone(pick(result['across_sources'])['original_median_pct'])
        self.assertEqual(result['predictions']['M1']['status'], 'SUPPORTED')
        self.assertEqual(result['predictions']['M2']['status'], 'SUPPORTED')
        self.assertEqual(result['predictions']['M3']['status'], 'UNASSESSABLE')

    def test_old_operand_requires_finite_positive_f_and_complete_same_repetitions(self):
        for replacement in [None, 0., float('nan')]:
            with self.subTest(replacement=replacement):
                data = records(); pick(data)['original_f_mean_loss'] = replacement
                self.assertIsNone(pick(self.run_summary(data)['cells'])['original_relative_median_pct'])
        data = records()
        for row in data:
            if (row['source_id'], row['arm'], row['window'], row['method']) == ('a', 'constant', 52, 'QR33'):
                row['original_qr_mean_loss'] = 104. if row['rep'] == 0 else 106.
        self.assertAlmostEqual(pick(self.run_summary(data)['cells'])['original_relative_median_pct'], 5.)

    def test_m1_closed_boundaries_and_negative_improvement_outside_interval(self):
        # Supply artificial across operands directly: the predicate is closed,
        # without changing the frozen repetition-ratio IEEE arithmetic.
        for percent, status in [(-5., 'SUPPORTED'), (5., 'SUPPORTED'),
                                (-5.0001, 'NOT_SUPPORTED'), (5.0001, 'NOT_SUPPORTED')]:
            with self.subTest(percent=percent):
                result = self.run_summary()
                pick(result['across_sources'])['median_pct'] = percent
                prediction = self.api()._predictions(result['cells'], result['across_sources'],
                                                     ['a', 'b'], design())['M1']
                self.assertEqual(prediction['status'], status)
                if percent < -5.:self.assertLess(prediction['constant_median_pct'], 0.)

    def test_frozen_ratio_ieee_result_is_not_rearranged_or_tolerance_clipped(self):
        # The v9-frozen formula at105/100 gives the literal IEEE value below.
        # A subtraction-before-division rewrite or threshold epsilon fails this.
        data = records()
        for s in ['a', 'b']:change_primary(data, s, 'constant', 5.)
        result = self.run_summary(data)
        self.assertEqual(pick(result['cells'])['relative_median_pct'], 5.000000000000004)
        self.assertEqual(result['predictions']['M1']['status'], 'NOT_SUPPORTED')

    def test_m2_inclusive_five_percentage_point_increment(self):
        for percent, status in [(5., 'SUPPORTED'), (4.9999, 'NOT_SUPPORTED')]:
            with self.subTest(percent=percent):
                data = records()
                for s in ['a', 'b']:change_primary(data, s, 'switching', percent)
                result = self.run_summary(data)['predictions']['M2']
                self.assertEqual(result['status'], status)
                self.assertAlmostEqual(result['switching_minus_constant_pct_points'], percent)

    def test_m3_requires_strict_group_improvement_in_both_arms(self):
        data = records()
        for s in ['a', 'b']:change_primary(data, s, 'constant', 0., old_pct=0.)
        result = self.run_summary(data)['predictions']['M3']
        self.assertEqual(result['status'], 'NOT_SUPPORTED')
        self.assertFalse(result['group_both_arms_improved'])

    def test_m3_uses_intersection_not_favourable_union(self):
        data = records(('a', 'b', 'c'))
        for s, value in [('a', 0.), ('b', 0.), ('c', 30.)]:change_primary(data, s, 'constant', value)
        for s, value in [('a', 30.), ('b', 0.), ('c', 0.)]:change_primary(data, s, 'switching', value)
        result = self.run_summary(data, sources=('a', 'b', 'c'))['predictions']['M3']
        self.assertTrue(result['group_both_arms_improved'])
        self.assertEqual(result['joint_improved_sources'], 1)
        self.assertEqual(result['joint_improved_source_ids'], ['b'])
        self.assertEqual(result['status'], 'NOT_SUPPORTED')

    def test_m3_supports_required_joint_sources_and_rejects_unknown_even_if_known_count_suffices(self):
        data = records(('a', 'b', 'c'))
        for arm in ['constant', 'switching']:
            for s, value in [('a', 0.), ('b', 0.), ('c', 30.)]:change_primary(data, s, arm, value)
        good = self.run_summary(data, sources=('a', 'b', 'c'))['predictions']['M3']
        self.assertEqual(good['status'], 'SUPPORTED')
        self.assertEqual(good['joint_improved_source_ids'], ['a', 'b'])
        row = pick(data, source='c'); row['original_status'] = 'FAILED'
        unknown = self.run_summary(data, sources=('a', 'b', 'c'))['predictions']['M3']
        self.assertEqual(unknown['status'], 'UNASSESSABLE')
        self.assertEqual(unknown['unknown_source_ids'], ['c'])

    def test_source_order_input_immutability_and_json_native_scalars(self):
        class FloatScalar(float):
            pass
        data = records(('b', 'a')); before = copy.deepcopy(data)
        for row in data:row['qr_mean_loss'] = FloatScalar(row['qr_mean_loss'])
        result = self.run_summary(data, sources=('b', 'a'))
        self.assertEqual(result['cells'][0]['source_id'], 'b')
        self.assertEqual(data, before)
        json.dumps(result, allow_nan=False)
        def native(value):
            if isinstance(value, dict):
                self.assertIs(type(value), dict)
                for k, v in value.items():self.assertIs(type(k), str);native(v)
            elif isinstance(value, list):
                for v in value:native(v)
            else:self.assertIn(type(value), [str, int, float, bool, type(None)])
        native(result)

    def test_unknown_inventory_identity_is_rejected_instead_of_silently_removed(self):
        data = records(); row = copy.deepcopy(pick(data)); row['source_id'] = 'unexpected'; data.append(row)
        with self.assertRaises(ValueError):self.run_summary(data)

    def test_numpy_scalars_are_normalized_when_numpy_is_available_in_the_runtime(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy is not installed in this stdlib-only runtime')
        data = records()
        for row in data:
            row['rep'] = np.int64(row['rep'])
            row['n'] = np.int64(row['n'])
            row['qr_mean_loss'] = np.float64(row['qr_mean_loss'])
            row['f_mean_loss'] = np.float64(row['f_mean_loss'])
            row['qr_breaches'] = np.int64(row['qr_breaches'])
            row['f_breaches'] = np.int64(row['f_breaches'])
            row['original_qr_mean_loss'] = np.float64(row['original_qr_mean_loss'])
            row['original_f_mean_loss'] = np.float64(row['original_f_mean_loss'])
        result = self.run_summary(data)
        self.assertEqual(pick(result['cells'])['status'], 'COMPLETE')
        self.assertIs(type(pick(result['cells'])['relative_median_pct']), float)
        json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
