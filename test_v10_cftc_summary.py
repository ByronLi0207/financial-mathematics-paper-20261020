"""E2 summary tests use invented scalar records, never downloaded data."""
import copy
import importlib
import json
from pathlib import Path
import unittest


METHODS = ['F', 'I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33']


def design():
    return dict(windows=[52, 260], methods=list(METHODS), top_contracts=20,
                split_formulas=dict(evaluation_n=260),
                menus={m: [.001, .01, .1, 1., 10., 'inf'] for m in ['QR4', 'QR33']},
                ancillary=dict(gammas=[.001, .005, .01, .05]),
                T1=dict(minimum_inclusive_fraction=.6),
                T2=dict(lower_inclusive_pct=-10., upper_inclusive_pct=10.), T3=dict(strict=True))


def fixture(codes=('005', '100+')):
    rows = []
    for code in codes:
        for window in [52, 260]:
            for method in METHODS:
                loss = {'F': 100., 'I': 90., 'QR33': 100., 'ACI_F': 98., 'ACI_QR33': 102.}.get(method)
                if method == 'QR4':loss = 110. if window == 52 else 105.
                rows.append(dict(code=code, window=window, method=method, status='COMPLETE',
                    mean_loss=loss, strict_breach_count=13, n=260,
                    selected_penalty='inf' if method in ['QR4', 'QR33', 'ACI_QR33'] else None,
                    selected_gamma=.005 if method.startswith('ACI_') else None, reason=None))
    return rows


def pick(rows, code='005', window=52, method='QR33'):
    return next(r for r in rows if r.get('code', code) == code and r['window'] == window and r['method'] == method)


class CftcSummaryTests(unittest.TestCase):
    def api(self):
        self.assertTrue(Path(__file__).with_name('v10_cftc_summary.py').is_file(),
                        'the pure E2 summary implementation is absent')
        return importlib.import_module('v10_cftc_summary')

    def summary(self, rows=None, codes=('005', '100+')):
        return self.api().summarize(fixture(codes) if rows is None else rows, list(codes), design())

    def test_complete_inventory_one_contract_row_and_all_methods_both_windows(self):
        result = self.summary()
        self.assertEqual(len(result['cells']), 24)
        self.assertEqual(len(result['contracts']), 2)
        self.assertEqual(len(result['across_contracts']), 12)
        contract = result['contracts'][0]
        self.assertEqual(contract['code'], '005')
        self.assertEqual(contract['status'], 'COMPLETE')
        self.assertEqual(set(contract['windows']), {'52', '260'})
        self.assertEqual(set(contract['windows']['52']['methods']), set(METHODS))
        self.assertEqual(pick(result['cells'])['mean_loss'], 100.)
        self.assertEqual(pick(result['cells'])['strict_breach_rate'], .05)
        self.assertEqual(pick(result['cells'])['selected_penalty'], 'inf')
        self.assertEqual([result['predictions'][x]['status'] for x in ['T1', 'T2', 'T3']],
                         ['SUPPORTED', 'SUPPORTED', 'SUPPORTED'])

    def test_t1_denominator_includes_every_contract_window_and_sixty_percent_is_closed(self):
        codes = tuple('c'+str(i) for i in range(5)); rows = fixture(codes)
        for code, window in [(codes[0], 52), (codes[0], 260), (codes[1], 52), (codes[1], 260)]:
            pick(rows, code, window)['mean_loss'] = 80.
        result = self.summary(rows, codes)['predictions']['T1']
        self.assertEqual(result['required_cells'], 10)
        self.assertEqual(result['simple_better_cells'], 6)
        self.assertEqual(result['fraction'], .6)
        self.assertEqual(result['status'], 'SUPPORTED')

    def test_t1_strict_min_uses_either_reference_and_ties_are_not_wins(self):
        rows = fixture()
        pick(rows, method='I')['mean_loss'] = 150.
        pick(rows)['mean_loss'] = 120.  # F alone is better.
        pick(rows, window=260, method='I')['mean_loss'] = 80.
        pick(rows, window=260)['mean_loss'] = 90.  # I alone is better.
        pick(rows, code='100+')['mean_loss'] = 90.  # min(F,I) == QR33.
        pick(rows, code='100+', window=260)['mean_loss'] = 90.
        result = self.summary(rows)['predictions']['T1']
        self.assertEqual(result['simple_better_cells'], 2)
        self.assertEqual(result['fraction'], .5)
        self.assertEqual(result['status'], 'NOT_SUPPORTED')

    def test_missing_t1_operand_remains_unknown_even_when_known_wins_already_suffice(self):
        rows = fixture(); pick(rows)['status'] = 'FAILED'; pick(rows)['reason'] = 'ARTIFICIAL_FAILURE'
        result = self.summary(rows)['predictions']['T1']
        self.assertEqual(result['required_cells'], 4)
        self.assertEqual(result['complete_operand_cells'], 3)
        self.assertIsNone(result['fraction'])
        self.assertEqual(result['status'], 'UNASSESSABLE')

    def test_relative_loss_is_normalized_within_contract_before_across_median(self):
        rows = fixture()
        pick(rows, method='F')['mean_loss'] = 10.
        pick(rows)['mean_loss'] = 9.
        pick(rows, code='100+', method='F')['mean_loss'] = 1000.
        pick(rows, code='100+')['mean_loss'] = 1200.
        group = pick(self.summary(rows)['across_contracts'])
        self.assertEqual(group['status'], 'COMPLETE')
        self.assertAlmostEqual(group['median_pct'], 5.)
        self.assertAlmostEqual(group['q25_pct'], -2.5)
        self.assertAlmostEqual(group['q75_pct'], 12.5)
        self.assertNotIn('raw_mean_loss_median', group)

    def test_t2_closed_bounds_require_both_complete_window_operands(self):
        result = self.summary()
        pick(result['across_contracts'])['median_pct'] = -10.
        pick(result['across_contracts'], window=260)['median_pct'] = 10.
        outcome = self.api()._predictions(result['cells'], result['across_contracts'], ['005', '100+'], design())['T2']
        self.assertEqual(outcome['status'], 'SUPPORTED')
        pick(result['across_contracts'], window=260)['median_pct'] = 10.0001
        outcome = self.api()._predictions(result['cells'], result['across_contracts'], ['005', '100+'], design())['T2']
        self.assertEqual(outcome['status'], 'NOT_SUPPORTED')

    def test_frozen_ieee_ratio_is_not_rearranged_or_epsilon_clipped(self):
        rows = fixture()
        for row in rows:
            if row['method'] == 'QR33':row['mean_loss'] = 110.
        result = self.summary(rows)
        self.assertEqual(pick(result['cells'])['relative_loss_pct'], 10.000000000000009)
        self.assertEqual(result['predictions']['T2']['status'], 'NOT_SUPPORTED')

    def test_t3_is_strict_and_uses_both_all_contract_qr4_medians(self):
        rows = fixture()
        for row in rows:
            if row['method'] == 'QR4':row['mean_loss'] = 100.
        result = self.summary(rows)['predictions']['T3']
        self.assertEqual(result['status'], 'NOT_SUPPORTED')
        self.assertEqual(result['W260_minus_W52_pct_points'], 0.)
        rows.remove(pick(rows, window=260, method='QR4'))
        result = self.summary(rows)['predictions']['T3']
        self.assertEqual(result['status'], 'UNASSESSABLE')
        self.assertIsNone(result['W260_minus_W52_pct_points'])

    def test_zero_f_does_not_invalidate_t1_mean_comparison_but_blocks_ratios(self):
        rows = fixture(); pick(rows, method='F')['mean_loss'] = 0.
        result = self.summary(rows)
        self.assertEqual(result['predictions']['T1']['status'], 'SUPPORTED')
        self.assertEqual(result['predictions']['T2']['status'], 'UNASSESSABLE')
        self.assertEqual(result['predictions']['T3']['status'], 'UNASSESSABLE')
        self.assertIsNone(pick(result['across_contracts'])['median_pct'])
        self.assertIsNone(pick(result['cells'])['relative_loss_pct'])

    def test_duplicate_method_slot_fails_without_choosing_one_and_retains_inventory(self):
        rows = fixture(); rows.append(copy.deepcopy(pick(rows, method='ACI_F')))
        result = self.summary(rows)
        cell = pick(result['cells'], method='ACI_F')
        self.assertEqual(cell['status'], 'FAILED')
        self.assertEqual(cell['record_count'], 2)
        self.assertIsNone(cell['mean_loss'])
        self.assertIn('DUPLICATE', cell['reason'])
        self.assertEqual(len(result['cells']), 24)
        self.assertEqual(result['contracts'][0]['status'], 'FAILED')
        self.assertEqual(result['predictions']['T1']['status'], 'SUPPORTED')
        self.assertIsNone(pick(result['across_contracts'], method='ACI_F')['median_pct'])

    def test_invalid_full_method_never_reports_partial_mean_or_breach_score(self):
        for field, value in [('n', 259), ('mean_loss', float('nan')), ('mean_loss', -1.),
                             ('strict_breach_count', 261), ('selected_penalty', None), ('status', 'NA')]:
            with self.subTest(field=field, value=value):
                rows = fixture(); row = pick(rows); row[field] = value; row['reason'] = 'ARTIFICIAL_ONLY'
                result = self.summary(rows); cell = pick(result['cells'])
                self.assertEqual(cell['status'], 'FAILED')
                self.assertIsNone(cell['mean_loss'])
                self.assertIsNone(cell['strict_breach_count'])
                self.assertIn('ARTIFICIAL_ONLY', cell['reason'])
                json.dumps(result, allow_nan=False)

    def test_ancillary_gamma_failure_is_retained_without_destroying_other_method_claims(self):
        rows = fixture(); pick(rows, method='ACI_QR33')['selected_gamma'] = None
        result = self.summary(rows)
        self.assertEqual(pick(result['cells'], method='ACI_QR33')['status'], 'FAILED')
        self.assertEqual(result['predictions']['T2']['status'], 'SUPPORTED')
        self.assertEqual(result['predictions']['T3']['status'], 'SUPPORTED')

    def test_absent_contract_gets_all_twelve_failed_slots_and_no_partial_contract_median(self):
        rows = [r for r in fixture() if r['code'] == '005']
        result = self.summary(rows)
        self.assertEqual([c['code'] for c in result['contracts']], ['005', '100+'])
        self.assertEqual(result['contracts'][1]['complete_method_slots'], 0)
        self.assertEqual(result['contracts'][1]['required_method_slots'], 12)
        self.assertTrue(all(r['status'] == 'UNASSESSABLE' and r['median_pct'] is None for r in result['across_contracts']))
        self.assertTrue(all(r['status'] == 'UNASSESSABLE' for r in result['predictions'].values()))

    def test_empty_selected_universe_is_unavailable_without_fabricating_contracts(self):
        result = self.summary([], ())
        self.assertEqual(result['cells'], [])
        self.assertEqual(result['contracts'], [])
        self.assertEqual(len(result['across_contracts']), 12)
        self.assertTrue(all(r['status'] == 'UNAVAILABLE' for r in result['predictions'].values()))

    def test_codes_are_literal_ordered_strings_and_unplanned_records_are_rejected(self):
        result = self.summary(codes=('100+', '005'))
        self.assertEqual([c['code'] for c in result['contracts']], ['100+', '005'])
        rows = fixture(); rows[0]['code'] = '5'
        with self.assertRaises(ValueError):self.summary(rows)
        with self.assertRaises(ValueError):self.summary([], ('005', '005'))
        with self.assertRaises(ValueError):self.summary([], (5,))

    def test_input_unchanged_and_output_is_native_json_safe(self):
        class FloatScalar(float):
            pass
        rows = fixture(); before = copy.deepcopy(rows)
        for row in rows:row['mean_loss'] = FloatScalar(row['mean_loss'])
        result = self.summary(rows)
        self.assertEqual(rows, before)
        json.dumps(result, allow_nan=False)
        def native(value):
            if isinstance(value, dict):
                for k, v in value.items():self.assertIs(type(k), str);native(v)
            elif isinstance(value, list):
                for v in value:native(v)
            else:self.assertIn(type(value), [str, int, float, bool, type(None)])
        native(result)

    def test_numpy_scalars_are_native_when_numpy_is_available(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy is absent in this stdlib-only runtime')
        rows = fixture()
        for row in rows:
            row['window'] = np.int64(row['window']); row['n'] = np.int64(row['n'])
            row['mean_loss'] = np.float64(row['mean_loss'])
            row['strict_breach_count'] = np.int64(row['strict_breach_count'])
            if row['selected_gamma'] is not None:row['selected_gamma'] = np.float64(row['selected_gamma'])
        result = self.summary(rows)
        self.assertEqual(pick(result['cells'])['status'], 'COMPLETE')
        self.assertIs(type(pick(result['cells'])['mean_loss']), float)
        json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
