"""Artificial membership receipts only; no loss vectors or MCS runs."""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import unittest


LABELS = ['FX original', 'FX early2015', 'Treasury bills', 'Other NYFed panels', 'Same-record dailyFX', 'CFTC']


def design():
    return dict(size=.1, report=dict(groups=LABELS+['All comparisons']))


def registry(source='a', label='FX original', methods=None, unavailable=None):
    return dict(identity=dict(period='original', normalized_source=source, horizon=6, window=52),
        group_label=label, status='READY',
        methods=methods if methods is not None else [
            dict(method_id='F', method_class='matched_historical'),
            dict(method_id='I', method_class='matched_historical'),
            dict(method_id='q', method_class='conditional'),
            dict(method_id='r', method_class='other_historical'),
            dict(method_id='b', method_class='other_benchmark')],
        unavailable_methods=[] if unavailable is None else unavailable)


def receipt(group, included=('F',), equivalence=None, status='COMPLETE'):
    methods = sorted(x['method_id'] for x in group['methods'])
    if status not in ['COMPLETE', 'COMPLETE_IDENTICAL_LOSSES', 'COMPLETE_SINGLE_METHOD']:
        return dict(identity=deepcopy(group['identity']), status=status, reason='ARTIFICIAL_FAILURE')
    included = sorted(included)
    return dict(identity=deepcopy(group['identity']), status=status, n=5, method_ids=methods,
        included=included, excluded=[m for m in methods if m not in included],
        pvalues={m: 1. if m in included else .05 for m in methods},
        unique_loss_groups=equivalence if equivalence is not None else [dict(representative=m, members=[m]) for m in methods])


class McsSummaryTests(unittest.TestCase):
    def api(self):
        self.assertTrue(Path(__file__).with_name('v10_mcs_summary.py').is_file(),
                        'the pure E3 summary implementation is absent')
        return importlib.import_module('v10_mcs_summary')

    def summarize(self, groups, rows=None):
        return self.api().summarize([receipt(g) for g in groups] if rows is None else rows, groups, design())

    def test_six_labels_and_overall_retain_planned_and_successful_counts(self):
        g = registry(); result = self.summarize([g])
        self.assertEqual([r['group_label'] for r in result['groups_summary']], LABELS)
        self.assertEqual(result['overall']['planned_comparisons'], 1)
        self.assertEqual(result['overall']['successful_comparisons'], 1)
        metric = result['overall']['metrics']['matched_FI_membership']
        self.assertEqual(metric['count_successful'], 1)
        self.assertEqual(metric['fraction_successful'], 1.)
        self.assertEqual(result['cells'][0]['included'], ['F'])
        self.assertEqual(result['groups_summary'][1]['planned_comparisons'], 0)
        self.assertIsNone(result['groups_summary'][1]['metrics']['matched_FI_membership']['fraction_successful'])

    def test_literal_sole_member_and_sole_loss_class_are_distinct(self):
        g = registry()
        classes = [dict(representative='F', members=['F', 'q'])]
        classes += [dict(representative=m, members=[m]) for m in ['I', 'r', 'b']]
        row = receipt(g, included=['F', 'q'], equivalence=classes)
        result = self.summarize([g], [row]); metrics = result['overall']['metrics']
        self.assertEqual(metrics['matched_FI_membership']['count_successful'], 1)
        self.assertEqual(metrics['literal_sole_FI']['count_successful'], 0)
        self.assertEqual(metrics['sole_loss_class_FI']['count_successful'], 1)
        self.assertEqual(metrics['historical_only']['count_successful'], 0)
        self.assertEqual(result['cells'][0]['conditional_included'], ['q'])
        self.assertEqual(result['overall']['conditional_exclusion']['excluded_slots'], 0)

    def test_two_matched_procedures_are_historical_only_but_not_literal_sole(self):
        g = registry(); result = self.summarize([g], [receipt(g, ['F', 'I'])])
        metrics = result['overall']['metrics']
        self.assertEqual(metrics['historical_only']['count_successful'], 1)
        self.assertEqual(metrics['literal_sole_FI']['count_successful'], 0)
        self.assertEqual(metrics['sole_loss_class_FI']['count_successful'], 0)

    def test_rolling_f_membership_never_becomes_matched_fi_membership(self):
        g = registry(); result = self.summarize([g], [receipt(g, ['r'])])
        metrics = result['overall']['metrics']
        self.assertEqual(metrics['matched_FI_membership']['count_successful'], 0)
        self.assertEqual(metrics['literal_sole_FI']['count_successful'], 0)
        self.assertEqual(metrics['rolling_F_membership']['count_successful'], 1)
        self.assertEqual(metrics['broad_FI_or_rolling_F_membership']['count_successful'], 1)

    def test_success_denominators_and_failed_planned_bounds_are_hand_calculated(self):
        groups = [registry(s) for s in ['a', 'b', 'c']]
        rows = [receipt(groups[0], ['F']), receipt(groups[1], ['q']), receipt(groups[2], status='MCS_FAILED')]
        result = self.summarize(groups, rows)['overall']
        metric = result['metrics']['matched_FI_membership']
        self.assertEqual((result['successful_comparisons'], result['planned_comparisons'], result['failed_comparisons']), (2, 3, 1))
        self.assertEqual(metric['fraction_successful'], .5)
        self.assertAlmostEqual(metric['fraction_all_planned_lower'], 1/3)
        self.assertAlmostEqual(metric['fraction_all_planned_upper'], 2/3)
        cond = result['conditional_exclusion']
        self.assertEqual((cond['excluded_slots'], cond['successful_complete_slots'], cond['failed_complete_slots'], cond['planned_complete_slots']), (1, 2, 1, 3))
        self.assertEqual(cond['fraction_successful'], .5)
        self.assertAlmostEqual(cond['fraction_all_planned_lower'], 1/3)
        self.assertAlmostEqual(cond['fraction_all_planned_upper'], 2/3)

    def test_known_na_is_counted_but_not_a_statistical_exclusion_or_unknown_complete_slot(self):
        na = [dict(method_id='never', method_class='conditional', status='NA', reason='NO_SAVED_KNN')]
        g = registry(unavailable=na)
        result = self.summarize([g])
        cond = result['overall']['conditional_exclusion']
        self.assertEqual(cond['excluded_slots'], 1)
        self.assertEqual(cond['successful_complete_slots'], 1)
        self.assertEqual(cond['planned_complete_slots'], 1)
        self.assertEqual(cond['known_na_slots'], 1)
        self.assertEqual(result['overall']['unavailable_method_slots'], 1)
        self.assertNotIn('never', result['cells'][0]['excluded'])

    def test_conditional_bounds_use_procedure_slots_not_comparison_counts(self):
        def plan(source, count):
            return registry(source, methods=[dict(method_id='F', method_class='matched_historical')]
                            +[dict(method_id='q'+str(i), method_class='conditional') for i in range(count)])
        groups = [plan('a', 2), plan('b', 1), plan('c', 3)]
        rows = [receipt(groups[0], ['F']), receipt(groups[1], ['q0']), receipt(groups[2], status='FAILED_INPUT')]
        cond = self.summarize(groups, rows)['overall']['conditional_exclusion']
        self.assertEqual((cond['excluded_slots'], cond['successful_complete_slots'], cond['failed_complete_slots']), (2, 3, 3))
        self.assertAlmostEqual(cond['fraction_successful'], 2/3)
        self.assertAlmostEqual(cond['fraction_all_planned_lower'], 2/6)
        self.assertAlmostEqual(cond['fraction_all_planned_upper'], 5/6)

    def test_missing_and_duplicate_results_fail_the_whole_comparison_inventory(self):
        a, b = registry('a'), registry('b', 'CFTC')
        result = self.summarize([a, b], [receipt(a), receipt(a)])
        self.assertEqual(len(result['cells']), 2)
        self.assertEqual(result['overall']['successful_comparisons'], 0)
        self.assertIn('DUPLICATE', result['cells'][0]['status'])
        self.assertIn('MISSING', result['cells'][1]['status'])
        self.assertEqual(result['overall']['metrics']['matched_FI_membership']['fraction_all_planned_lower'], 0.)
        self.assertEqual(result['overall']['metrics']['matched_FI_membership']['fraction_all_planned_upper'], 1.)
        self.assertIsNone(result['overall']['conditional_exclusion']['fraction_successful'])

    def test_record_cannot_silently_drop_a_complete_registry_method(self):
        g = registry(); row = receipt(g)
        row['method_ids'].remove('q'); row['excluded'].remove('q'); del row['pvalues']['q']
        row['unique_loss_groups'] = [x for x in row['unique_loss_groups'] if x['representative'] != 'q']
        result = self.summarize([g], [row])
        self.assertEqual(result['overall']['successful_comparisons'], 0)
        self.assertEqual(result['cells'][0]['status'], 'FAILED_INPUT')
        self.assertEqual(result['overall']['conditional_exclusion']['failed_complete_slots'], 1)

    def test_invalid_partition_pvalues_or_partial_equivalence_membership_is_not_success(self):
        for error in ['partition', 'pvalue', 'equivalence']:
            with self.subTest(error=error):
                g = registry(); row = receipt(g)
                if error == 'partition':row['excluded'].append('F')
                elif error == 'pvalue':row['pvalues']['F'] = float('nan')
                else:
                    row['unique_loss_groups'] = [dict(representative='F', members=['F', 'q'])]+[dict(representative=m, members=[m]) for m in ['I', 'r', 'b']]
                result = self.summarize([g], [row])
                self.assertEqual(result['overall']['successful_comparisons'], 0)
                json.dumps(result, allow_nan=False)

    def test_literal_arch_pvalue_boundary_is_preserved(self):
        g = registry(); row = receipt(g)
        row['pvalues']['q'] = .1
        row['pvalues']['F'] = .10000000000000002
        result = self.summarize([g], [row])
        self.assertEqual(result['cells'][0]['included'], ['F'])
        self.assertIn('q', result['cells'][0]['excluded'])
        self.assertEqual(result['cells'][0]['pvalues']['q'], .1)

    def test_identical_loss_case_unfolds_every_label_without_reclassifying_conditional(self):
        g = registry(); methods = sorted(x['method_id'] for x in g['methods'])
        row = receipt(g, methods, [dict(representative=methods[0], members=methods)], 'COMPLETE_IDENTICAL_LOSSES')
        result = self.summarize([g], [row])
        metrics = result['overall']['metrics']
        self.assertEqual(result['overall']['successful_comparisons'], 1)
        self.assertEqual(metrics['sole_loss_class_FI']['count_successful'], 1)
        self.assertEqual(metrics['literal_sole_FI']['count_successful'], 0)
        self.assertEqual(metrics['historical_only']['count_successful'], 0)
        self.assertEqual(result['cells'][0]['conditional_included'], ['q'])

    def test_single_method_analytic_case_and_no_conditional_denominator_are_explicit(self):
        g = registry(methods=[dict(method_id='F', method_class='matched_historical')])
        result = self.summarize([g], [receipt(g, ['F'], status='COMPLETE_SINGLE_METHOD')])
        self.assertEqual(result['overall']['successful_comparisons'], 1)
        self.assertEqual(result['overall']['single_method_comparisons'], 1)
        self.assertEqual(result['overall']['metrics']['literal_sole_FI']['count_successful'], 1)
        self.assertIsNone(result['overall']['conditional_exclusion']['fraction_successful'])

    def test_explicit_registry_classes_override_suggestive_method_names(self):
        g = registry(methods=[dict(method_id='CFTC::F', method_class='conditional'),
                              dict(method_id='odd-name', method_class='matched_historical')])
        result = self.summarize([g], [receipt(g, ['CFTC::F'])])
        self.assertEqual(result['overall']['metrics']['matched_FI_membership']['count_successful'], 0)
        self.assertEqual(result['cells'][0]['conditional_included'], ['CFTC::F'])

    def test_empty_registry_has_no_invented_comparison_or_fraction(self):
        result = self.summarize([], [])
        self.assertEqual(result['cells'], [])
        self.assertEqual(result['overall']['planned_comparisons'], 0)
        self.assertIsNone(result['overall']['metrics']['matched_FI_membership']['fraction_all_planned_lower'])

    def test_outside_record_duplicate_registry_and_unknown_class_are_rejected(self):
        a, b = registry('a'), registry('b')
        with self.assertRaises(ValueError):self.summarize([a], [receipt(b)])
        with self.assertRaises(ValueError):self.summarize([a, a], [])
        a['methods'][0]['method_class'] = 'inferred-from-name'
        with self.assertRaises(ValueError):self.summarize([a], [])

    def test_inputs_are_unchanged_and_native_json_values_are_returned(self):
        g = registry(); row = receipt(g); original = deepcopy((g, row))
        result = self.summarize([g], [row])
        self.assertEqual((g, row), original)
        json.dumps(result, allow_nan=False)
        def native(value):
            if isinstance(value, dict):
                for key, child in value.items():self.assertIs(type(key), str);native(child)
            elif isinstance(value, list):
                for child in value:native(child)
            else:self.assertIn(type(value), [str, int, float, bool, type(None)])
        native(result)

    def test_numpy_pvalues_and_identity_scalars_are_normalized_when_available(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy is absent in this stdlib-only runtime')
        g = registry(); row = receipt(g)
        for item in [g, row]:
            item['identity']['horizon'] = np.int64(item['identity']['horizon'])
            item['identity']['window'] = np.int64(item['identity']['window'])
        row['n'] = np.int64(row['n'])
        row['pvalues'] = {m: np.float64(p) for m, p in row['pvalues'].items()}
        result = self.summarize([g], [row])
        self.assertEqual(result['overall']['successful_comparisons'], 1)
        self.assertIs(type(result['cells'][0]['pvalues']['F']), float)
        json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
