"""Synthetic contracts for frozen R6 selection and real-index rolling folds."""
import importlib.util
import json
import math
import unittest

if importlib.util.find_spec('supervisor_r6_rules'):
    import supervisor_r6_rules as rules
else:
    rules = None


class R6RuleTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(rules, 'R6 pure rule implementation is missing')

    def test_minimum_uses_fsum_and_exact_strongest_tie(self):
        values = {'0.001':[1e16, 1., 1., 1.], 'I':[2500000000000000.5]*4}
        result = rules.select_minimum(values, ['0.001', 'I'])
        self.assertEqual(result['selected_id'], 'I')
        self.assertEqual(result['candidates'][0]['mean_loss'], 2500000000000001.)
        values = {'0.001':[1., 2.], '10':[2., 1.], 'I':[1.5, 1.5]}
        self.assertEqual(rules.select_minimum(values, ['0.001', '10', 'I'])['selected_id'], 'I')
        self.assertEqual(rules.select_minimum(values, ['0.001', '10'])['selected_id'], '10')

    def test_missing_or_failed_required_candidate_kills_only_dependent_selection(self):
        values = {'0.001':[1., 1., 1., 1.], 'I':None}
        self.assertEqual(rules.select_minimum(values, ['0.001'])['status'], 'SELECTED')
        for invalid in (None, [1., float('nan'), 1., 1.], [1., 1., 1.], []):
            values['I'] = invalid
            for result in (rules.select_minimum(values, ['0.001', 'I']),
                           rules.select_paired_one_se(values, [0, 1, 2, 3], 1, ['0.001', 'I'])):
                self.assertEqual(result['status'], 'FAILED')
                self.assertIsNone(result['selected_id'])
                self.assertEqual(len(result['candidates']), 2)
                json.dumps(result, allow_nan=False)
        del values['I']
        self.assertEqual(rules.select_minimum(values, ['0.001', 'I'])['status'], 'FAILED')

    def test_one_se_includes_exact_boundary_and_prefers_I(self):
        values = {'0.001':[1., 1., 1., 1.], 'I':[.25, 2.25, .25, 2.25]}
        result = rules.select_paired_one_se(values, [0, 1, 2, 3], 1, ['0.001', 'I'])
        self.assertEqual(result['status'], 'SELECTED')
        self.assertEqual(result['best_id'], '0.001')
        self.assertEqual(result['selected_id'], 'I')
        ordinary = result['candidates'][1]
        self.assertEqual(ordinary['paired_mean_gap'], .25)
        self.assertEqual(ordinary['standard_error'], .25)
        self.assertTrue(ordinary['eligible'])
        json.dumps(result, allow_nan=False)

    def test_one_se_criterion_has_no_added_tolerance(self):
        values = {'0.001':[1., 1., 1., 1.], 'I':[.25000001, 2.25000001, .25000001, 2.25000001]}
        result = rules.select_paired_one_se(values, [0, 1, 2, 3], 1, ['0.001', 'I'])
        self.assertEqual(result['selected_id'], '0.001')
        self.assertFalse(result['candidates'][1]['eligible'])

    def test_paired_SE_cancels_shared_loss_variation(self):
        values = {'0.001':[10., 20., 10., 20.], 'I':[10.1, 20.1, 10.1, 20.1]}
        result = rules.select_paired_one_se(values, [0, 1, 2, 3], 1, ['0.001', 'I'])
        self.assertEqual(result['selected_id'], '0.001')
        self.assertLess(result['candidates'][1]['standard_error'], 1e-12)

    def test_constant_positive_gap_is_not_rescued_by_zero_SE(self):
        result = rules.select_paired_one_se({'0.001':[1.]*4, 'I':[2.]*4},
                                           [0, 1, 2, 3], 1, ['0.001', 'I'])
        self.assertEqual(result['selected_id'], '0.001')
        self.assertEqual(result['candidates'][1]['standard_error'], 0.)
        tied = rules.select_paired_one_se({'0.001':[1.]*4, 'I':[1.]*4},
                                         [0, 1, 2, 3], 1, ['0.001', 'I'])
        self.assertEqual(tied['selected_id'], 'I')

    def test_known_NW_fixture_uses_n_denominator(self):
        result = rules.origin_aware_nw([1., 2., 3., 4.], [0, 1, 2, 3], 1)
        self.assertEqual(result['bandwidth'], 1)
        self.assertEqual(result['mean'], 2.5)
        self.assertEqual(result['raw_lrv'], 1.5625)
        self.assertEqual(result['standard_error'], .625)
        self.assertEqual(result['lag_pair_counts'], [4, 3])

    def test_real_index_HAC_does_not_create_adjacency_across_a_gap(self):
        difference = [-.75, 1.25, -.75, 1.25]
        contiguous = rules.origin_aware_nw(difference, [0, 1, 2, 3], 1)
        gapped = rules.origin_aware_nw(difference, [0, 1, 4, 5], 1)
        self.assertEqual(contiguous['raw_lrv'], .25)
        self.assertEqual(gapped['raw_lrv'], .5)
        self.assertEqual(gapped['lag_pair_counts'], [4, 2])

    def test_negative_LRV_is_clipped_with_visible_numerical_status(self):
        result = rules.lrv_standard_error(-1e-15, 4)
        self.assertEqual(result['raw_lrv'], -1e-15)
        self.assertEqual(result['lrv'], 0.)
        self.assertEqual(result['standard_error'], 0.)
        self.assertEqual(result['status'], 'NUMERICAL_LRV_CLIPPED_TO_ZERO')
        with self.assertRaises(ValueError):
            rules.lrv_standard_error(float('nan'), 4)

    def test_short_or_misaligned_origins_fail_without_bandwidth_capping(self):
        values = {'0.001':[1., 1.], 'I':[2., 2.]}
        for origins in ([1, 2], [1], [1, 1], [2, 1], [1., 2.]):
            result = rules.select_paired_one_se(values, origins, 2, ['0.001', 'I'])
            self.assertEqual(result['status'], 'FAILED')
            self.assertIsNone(result['selected_id'])

    def test_infinity_is_only_the_explicit_I_ID_and_order_is_frozen(self):
        for ids in (['0.001', float('inf')], ['0.001', 'Infinity'], ['I', '0.001'], ['I', 'I']):
            with self.assertRaises(ValueError):
                rules.select_minimum({'0.001':[1.]*4, 'I':[1.]*4}, ids)

    def test_weekly_retro_fold_boundaries_and_equal_origin_weighting(self):
        folds = rules.rolling_folds(177, 228, 52, 26, 13)
        self.assertEqual(folds, [(103, 115), (140, 152), (177, 228)])
        self.assertEqual(sum(last-first+1 for first,last in folds), 78)

    def test_inspected_weekly_W260_has_only_full_validation(self):
        self.assertEqual(rules.rolling_folds(329, 380, 260, 26, 13), [(329, 380)])
        self.assertEqual(rules.rolling_folds(329, 380, 52, 26, 13),
                         [(107, 119), (144, 156), (181, 193), (218, 230),
                          (255, 267), (292, 304), (329, 380)])

    def test_frozen_FX_fold_counts_use_metadata_only(self):
        for first,last,window,count,origins in [(7535,8974,720,139,4752),
                                               (7535,8974,2880,94,3672),
                                               (10463,11902,720,200,6216),
                                               (10463,11902,2880,155,5136)]:
            with self.subTest(first=first,window=window):
                folds = rules.rolling_folds(first,last,window,168,24)
                self.assertEqual(len(folds), count)
                self.assertEqual(sum(b-a+1 for a,b in folds), origins)
                self.assertEqual(folds[-1], (first,last))

    def test_fold_purge_maturity_and_outer_cutoff_for_both_horizons(self):
        folds = rules.rolling_folds(177, 228, 52, 26, 13)
        for horizon in (6,24):
            for first,last in folds:
                self.assertGreaterEqual(first-horizon-52+1, 26)
                self.assertLessEqual(last+horizon, 252)
                self.assertLess(first-horizon, first)
            for previous,current in zip(folds,folds[1:]):
                self.assertEqual(current[0]-previous[1]-1,24)
                self.assertLess(previous[1]+horizon,current[0])
        self.assertLess(folds[-1][1]+24,253)

    def test_earliest_fold_is_retained_on_equality_and_invalid_metadata_rejected(self):
        self.assertEqual(rules.rolling_folds(177,228,54,26,13)[0], (103,115))
        self.assertEqual(rules.rolling_folds(177,228,55,26,13)[0], (140,152))
        for args in [(50,100,52,26,13,24), (177,176,52,26,13,24),
                     (177,228,52,26,0,24), (177,228,52,26,13,6)]:
            with self.assertRaises(ValueError):
                rules.rolling_folds(*args)


if __name__ == '__main__':
    unittest.main(verbosity=2)
