"""Synthetic private/public NPZ fixtures only; no financial input is opened."""
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np


def api():
    assert importlib.util.find_spec('v10_loss_inputs') is not None, 'MCS input registry module is missing'
    return importlib.import_module('v10_loss_inputs')


def design(n=3):
    return dict(core_scope='requested_core_saved_method',
        grid={'fx_hourly': {'n_by_period': {'original_evaluation': n, 'early_2015': n}},
              'weekly': {'n': n}, 'fx_daily': {'n': n}, 'cftc': {'n': n}},
        matched_F_aliases=['original::frozen_F', 'panel_legacy::frozen_F', 'R6::R6_F', 'CFTC::F'],
        matched_I_aliases=['panel_E5::I', 'CFTC::I'],
        other_historical_F_aliases=['original::rolling_F'],
        other_benchmark_aliases=['original::frozen_S', 'Levy::Levy_L'],
        combinations={})


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='artificial-mcs-input-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.inventory = dict(methods=[], unavailable_method_slots=[],
            reported_deterministic_combinations_not_derived=[], minimum_core_private_copy_manifest=[],
            source_aliases={'PDPOSGS-B': 'nyfed_weekly'})
        self.design = design()
        self.serial = 0

    def method(self, family='original', method='QR', capacity=(1.,5.,2.), loss=(.1,.2,.3),
               target=(2.,4.,1.), floor=(0.,0.,0.), origins=(10,11,12), source='fx_hourly',
               period='original_evaluation', normalized_source=None):
        self.serial += 1
        rel = f'.scratch/inputs/artificial-{self.serial}.npz'
        path = self.root/rel; path.parent.mkdir(parents=True, exist_ok=True)
        arrays = dict(o=np.array(origins), c=np.array(capacity), y=np.array(target))
        if loss is not None: arrays['l'] = np.array(loss)
        if floor is not None: arrays['b'] = np.array(floor)
        np.savez(path, **arrays)
        raw = path.read_bytes(); old = f'/old/never-read/artificial-{self.serial}.npz'
        self.inventory['minimum_core_private_copy_manifest'].append(dict(path=old,
            proposed_scratch_relative=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
        row = dict(family=family, method=method, source=source,
            normalized_source=normalized_source or source, period=period, horizon=2, window=19,
            trace_path=old, origin_key='o', capacity_key='c', target_key='y',
            floor_key='b' if floor is not None else None, loss_key='l' if loss is not None else None,
            origin_count=3, first_origin=10, last_origin=12, status='COMPLETE_SAVED_VECTOR',
            scope_classification='requested_core_saved_method')
        self.inventory['methods'].append(row)
        return row

    def build(self, cftc=None):
        return api().build_registry(self.inventory, cftc or [], self.design, self.root)

    def combo_file(self, rows):
        p = self.root/'published-combos.json'
        p.write_text(json.dumps({'method_rows': rows}))
        self.design['combinations'] = dict(source='published-combos.json',
            source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            complete=sum(r['status']=='COMPLETE' for r in rows),
            unavailable=sum(r['status']!='COMPLETE' for r in rows))
        self.inventory['reported_deterministic_combinations_not_derived'] = [
            {k:v for k,v in r.items() if k!='scores'} for r in rows]

    def test_new_copy_only_and_stored_loss_preserved_with_missing_floor_unrecovered(self):
        row = self.method(family='QR4', method='QR4', floor=None)
        row['floor_recovery'] = {'trace_path': '/old/forbidden.npz', 'key': 'floor'}
        got = self.build(); group = got['groups'][0]; m = group['methods'][0]
        self.assertEqual(group['status'], 'READY')
        self.assertEqual(m['method_id'], 'QR4::QR4')
        self.assertEqual(m['method_class'], 'conditional')
        np.testing.assert_array_equal(m['loss'], [.1,.2,.3])
        self.assertIsNone(m['floor'])
        self.assertIn('/old/never-read/', json.dumps(m['provenance']))
        self.assertEqual(got['counts']['core_alias_rows'], 1)

    def test_missing_loss_is_derived_by_unchanged_pinball_without_new_forecast(self):
        self.method(loss=None)
        m = self.build()['groups'][0]['methods'][0]
        np.testing.assert_array_equal(m['loss'], [.95,.05,.05])
        self.assertEqual(m['provenance']['loss_origin'], 'derived_from_saved_capacity_target')

    def test_claimed_complete_hash_or_size_failure_fails_whole_group(self):
        self.method(method='frozen_F'); self.method()
        self.inventory['minimum_core_private_copy_manifest'][-1]['bytes'] += 1
        got = self.build()['groups'][0]
        self.assertEqual(got['status'], 'FAILED_INPUT')
        self.assertTrue(got['errors'])
        self.assertEqual(got['claimed_complete_method_count'], 2)

    def test_full_declared_axis_is_not_inferred_from_truncated_or_shifted_npz(self):
        for ids in [(11,12,13), (10,12,13), (10,11), (10.,11.,12.)]:
            with self.subTest(ids=ids):
                self.inventory['methods'].clear(); self.inventory['minimum_core_private_copy_manifest'].clear()
                self.method(origins=ids, capacity=(1.,)*len(ids), target=(2.,)*len(ids),
                            floor=(0.,)*len(ids), loss=(.1,)*len(ids))
                self.assertEqual(self.build()['groups'][0]['status'], 'FAILED_INPUT')

    def test_target_disagreement_fails_group_without_intersection_or_dropped_method(self):
        self.method(method='frozen_F'); self.method(target=(2.,4.,9.))
        group = self.build()['groups'][0]
        self.assertEqual(group['status'], 'FAILED_INPUT')
        self.assertTrue(any('COMMON_TARGET' in str(e) for e in group['errors']))

    def test_known_na_slot_is_visible_without_opening_its_partial_trace(self):
        self.method()
        self.inventory['unavailable_method_slots'] = [dict(family='mature_baselines', method='FHS',
            period='original_evaluation', normalized_source='fx_hourly', source='fx_hourly',
            horizon=2, window=19, status='NA', reason='known failure', partial_trace='/old/never-read.npz')]
        group = self.build()['groups'][0]
        self.assertEqual(group['status'], 'READY')
        self.assertEqual(len(group['unavailable_methods']), 1)
        self.assertEqual(group['unavailable_methods'][0]['method_id'], 'mature_baselines::FHS')

    def test_only_explicit_f_aliases_merge_and_query_nearest_keeps_conditional_class(self):
        self.method(method='frozen_F'); self.method(family='R6', method='R6_F')
        self.method(method='one_state_F'); self.method(method='rolling_F')
        self.method(family='Levy', method='Levy_L', floor=None)
        group = self.build()['groups'][0]
        methods = {m['method_id']:m for m in group['methods']}
        self.assertEqual(methods['F']['aliases'], ['R6::R6_F', 'original::frozen_F'])
        self.assertEqual(methods['F']['method_class'], 'matched_historical')
        self.assertEqual(methods['original::one_state_F']['method_class'], 'conditional')
        self.assertEqual(methods['original::rolling_F']['method_class'], 'other_historical')
        self.assertEqual(methods['Levy::Levy_L']['method_class'], 'other_benchmark')
        self.assertEqual(len(methods), 4)

    def test_alias_forecast_or_loss_difference_keeps_both_qualified_ids_and_discrepancy(self):
        self.method(method='frozen_F'); self.method(family='R6', method='R6_F', capacity=(1.,5.,3.))
        group = self.build()['groups'][0]
        self.assertEqual(group['status'], 'READY')
        self.assertEqual([m['method_id'] for m in group['methods']], ['R6::R6_F', 'original::frozen_F'])
        self.assertTrue(group['alias_discrepancies'])

    def test_conditional_identical_forecast_does_not_become_historical_and_i_is_distinct(self):
        self.method(method='frozen_F'); self.method(method='QR'); self.method(family='panel_E5', method='I')
        methods = {m['method_id']:m for m in self.build()['groups'][0]['methods']}
        self.assertEqual(sorted(methods), ['F', 'I', 'original::QR'])
        self.assertEqual(methods['original::QR']['method_class'], 'conditional')

    def test_copy_mapping_cannot_read_outside_new_private_scratch(self):
        self.method()
        self.inventory['minimum_core_private_copy_manifest'][0]['proposed_scratch_relative'] = '../outside.npz'
        self.assertEqual(self.build()['groups'][0]['status'], 'FAILED_INPUT')

    def test_source_alias_and_distinct_periods_are_preserved(self):
        self.method(source='PDPOSGS-B', normalized_source='nyfed_weekly')
        self.method(period='early_2015')
        got = self.build()
        self.assertEqual(len(got['groups']), 2)
        labels = {g['group_label'] for g in got['groups']}
        self.assertEqual(labels, {'Treasury bills', 'FX early2015'})
        method = next(g for g in got['groups'] if g['identity']['normalized_source']=='nyfed_weekly')['methods'][0]
        self.assertIn('PDPOSGS-B', json.dumps(method['provenance']))

    def test_cftc_uses_new_public_trace_exact_bytes_hash_and_declared_axis(self):
        path = self.root/'public.npz'
        np.savez(path, origins=np.arange(10,13), capacities=np.ones(3), peak=np.ones(3)*2,
                 floor=np.zeros(3), pinball=np.ones(3)*.95)
        raw = path.read_bytes()
        row = dict(code='001234', family='CFTC', period='economic_date_replay_2021_2026',
            normalized_source='cftc:001234', horizon=2, window=19, method='F', status='COMPLETE',
            trace_path='public.npz', trace_bytes=len(raw), trace_sha256=hashlib.sha256(raw).hexdigest(),
            origin_count=3, first_origin=10, last_origin=12)
        group = self.build([row])['groups'][0]
        self.assertEqual(group['status'], 'READY')
        self.assertEqual(group['group_label'], 'CFTC')
        self.assertEqual(group['methods'][0]['method_id'], 'F')
        row['trace_sha256'] = '0'*64
        self.assertEqual(self.build([row])['groups'][0]['status'], 'FAILED_INPUT')

    def test_published_combos_use_original_qr_and_knn_and_reconcile_saved_mean(self):
        self.method(method='frozen_F', capacity=(2.,2.,2.), target=(3.,3.,3.))
        self.method(method='QR', capacity=(4.,4.,4.), target=(3.,3.,3.))
        self.method(method='KNN', capacity=(5.,5.,5.), target=(3.,3.,3.))
        self.method(family='E3_extended_menu', method='QR33_plus', capacity=(20.,20.,20.), target=(3.,3.,3.))
        common = dict(source='fx_hourly', horizon=2, window=19, original=True, status='COMPLETE')
        self.combo_file([dict(common, method='MEAN_F_QR', scores={'mean_loss': 0.}),
                         dict(common, method='MEDIAN_F_QR_KNN', scores={'mean_loss': .05})])
        group = self.build()['groups'][0]; self.assertEqual(group['status'], 'READY')
        methods = {m['method_id']:m for m in group['methods']}
        mean = methods['published_combination::MEAN_F_QR']
        median = methods['published_combination::MEDIAN_F_QR_KNN']
        np.testing.assert_array_equal(mean['capacity'], [3.,3.,3.])
        np.testing.assert_array_equal(median['capacity'], [4.,4.,4.])
        self.assertEqual(mean['method_class'], 'conditional')
        self.assertIn('original::QR', json.dumps(mean['provenance']))

    def test_published_mean_mismatch_fails_whole_group_and_panel_na_remains_visible(self):
        self.method(family='panel_legacy', method='frozen_F', source='PANEL', capacity=(2.,)*3, target=(3.,)*3)
        self.method(family='panel_legacy', method='QR33', source='PANEL', capacity=(4.,)*3, target=(3.,)*3)
        common = dict(source='PANEL', horizon=2, window=19, original=False)
        self.combo_file([dict(common, method='MEAN_F_QR', status='COMPLETE', scores={'mean_loss': 99.}),
                         dict(common, method='MEDIAN_F_QR_KNN', status='NA', reason='no plain KNN')])
        group = self.build()['groups'][0]
        self.assertEqual(group['status'], 'FAILED_INPUT')
        self.assertTrue(any('PUBLISHED_MEAN' in str(e) for e in group['errors']))
        self.assertEqual(len(group['unavailable_methods']), 1)

    def test_published_source_must_reconcile_entire_inventory_including_known_na(self):
        self.method(family='panel_legacy', method='frozen_F', source='PANEL', capacity=(2.,)*3, target=(3.,)*3)
        self.method(family='panel_legacy', method='QR33', source='PANEL', capacity=(4.,)*3, target=(3.,)*3)
        common = dict(source='PANEL', horizon=2, window=19, original=False)
        complete = dict(common, method='MEAN_F_QR', status='COMPLETE', scores={'mean_loss': 0.})
        self.combo_file([complete, dict(common, method='MEDIAN_F_QR_KNN', status='NA')])
        # A bound source that lacks an inventoried NA row is not the declared
        # complete 112-slot published inventory, even though its mean is valid.
        path = self.root/'published-combos.json'
        path.write_text(json.dumps({'method_rows': [complete]}))
        self.design['combinations']['source_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.build()['groups'][0]['status'], 'FAILED_INPUT')

    def test_nonfinite_or_negative_stored_loss_fails_whole_comparison(self):
        for bad in [-.1, float('nan')]:
            with self.subTest(bad=bad):
                self.inventory['methods'].clear(); self.inventory['minimum_core_private_copy_manifest'].clear()
                self.method(method='frozen_F'); self.method(loss=(.1,bad,.3))
                group = self.build()['groups'][0]
                self.assertEqual(group['status'], 'FAILED_INPUT')
                self.assertEqual(len(group['planned_methods']), 2)

    def test_provided_floor_disagreement_prevents_semantic_alias_merge(self):
        self.method(method='frozen_F')
        self.method(family='R6', method='R6_F', floor=(.5,.5,.5))
        group = self.build()['groups'][0]
        self.assertEqual(group['status'], 'READY')
        self.assertEqual([m['method_id'] for m in group['methods']], ['R6::R6_F', 'original::frozen_F'])
        self.assertTrue(group['alias_discrepancies'])

    def test_complete_input_must_belong_to_the_declared_period_horizon_window_grid(self):
        self.method()
        self.design['grid']['fx_hourly'].update(horizons=[6], windows=[52])
        self.assertEqual(self.build()['groups'][0]['status'], 'FAILED_INPUT')

    def test_expected_inventory_counts_do_not_silently_accept_a_successful_subset(self):
        self.method()
        self.design.update(include_all_core_saved_alias_rows=2, total_expected_comparisons=2)
        got = self.build()
        self.assertTrue(got['counts']['errors'])
        self.assertTrue(all(g['status']=='FAILED_INPUT' for g in got['groups']))


if __name__=='__main__': unittest.main()
