"""Synthetic phase/receipt contracts; no financial file or network is used."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import numpy as np
from conditional_quantile import QuantileFitError

ROOT = Path(__file__).resolve().parent


def artificial():
    dates = np.datetime64('2019-06-01', 'us') + np.arange(280) * np.timedelta64(1, 'D')
    source = SimpleNamespace(source_id='fx_hourly', dates=dates,
        position=np.zeros(280), sha256='a' * 64, bytes=123,
        metadata={'units': 'USD', 'observation_count': 280,
                  'first_date': str(dates[0]), 'last_date': str(dates[-1]),
                  'irregular_gap_count': 0})
    config = dict(input_relative_path='.scratch/artificial.csv', bytes=123,
        sha256='a' * 64, record_count=280, native_unit='USD',
        validation_origin_first=190, validation_origin_last=195,
        evaluation_origin_first=212, evaluation_origin_last=223,
        windows=[40], primary_window=40, refit_step=4, short_scale=6,
        long_scale=26, nominal_gap_seconds=86400,
        knn_candidates={'40': [19, 20, 40]},
        one_state_reference_neighbors={'40': 20})
    spec = dict(horizons=[6], families=['QR', 'KNN', 'SCALED_KNN'],
        tau_numerator=19, tau_denominator=20, qr_penalties=[.001, .01, .1],
        sources={'fx_hourly': config})
    return source, spec


class PhaseRunnerTests(unittest.TestCase):
    def runner(self):
        try:
            return importlib.import_module('run_conditional_study')
        except ModuleNotFoundError as exc:
            if exc.name == 'run_conditional_study':
                self.fail('The bounded conditional phase runner is absent')
            raise

    def fake_project(self, runner, root, spec):
        for name in runner.CODE_FILES:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic executable fixture\n')
        (root / runner.SPEC_PATH).write_text(json.dumps(spec))
        (root / '.scratch').mkdir(exist_ok=True)
        for config in spec['sources'].values():
            input_path = root / config['input_relative_path']
            input_path.parent.mkdir(parents=True, exist_ok=True)
            input_path.write_bytes(b'synthetic loader-boundary fixture\n')
        freeze = dict(version=1, status='FROZEN', created_utc='2026-10-22T00:00:00Z',
            files={name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                   for name in runner.CODE_FILES},
            sources={name: dict(sha256=cfg['sha256'], bytes=cfg['bytes'])
                     for name, cfg in spec['sources'].items()})
        path = root / runner.FREEZE_PATH
        path.write_text(json.dumps(freeze))
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def args(self, attempt, freeze_hash, phase='validation', family='KNN'):
        args = ['--phase', phase, '--source', 'fx_hourly', '--horizon', '6',
                '--window', '40', '--attempt-dir', str(attempt),
                '--freeze-sha256', freeze_hash]
        if family is not None:
            args += ['--family', family]
        return args

    def validation_receipt(self, spec, family, executable_hash):
        params = spec['qr_penalties'] if family == 'QR' else [19, 20, 40]
        rows = [dict(parameter=param, status='COMPLETE', origin_count=6,
                     mean_pinball=loss) for param, loss in zip(params, [3., 1., 1.])]
        return dict(version=1, status='COMPLETE', phase='validation',
            source='fx_hourly', horizon=6, window=40, family=family,
            executable_freeze_sha256=executable_hash,
            selection_freeze_sha256=None,
            source_identity=dict(sha256='a' * 64, bytes=123, record_count=280,
                                 native_unit='USD'),
            resources=dict(elapsed_seconds=1., peak_rss_bytes=4096,
                maximum_observed_os_threads=1, thread_snapshot_count=1,
                thread_probe_status='PASS'),
            stop_code=None,
            result=dict(candidate_rows=rows, origin_identity=dict(
                count=6, first=190, last=195,
                sha256=hashlib.sha256(b''.join(i.to_bytes(8, 'little', signed=True)
                                             for i in range(190, 196))).hexdigest())))

    def selection_fixture(self, root, spec, executable_hash):
        cells = []
        for family in spec['families']:
            receipt = self.validation_receipt(spec, family, executable_hash)
            path = root / '.scratch' / (family + '-validation.json')
            path.write_text(json.dumps(receipt))
            params = spec['qr_penalties'] if family == 'QR' else [19, 20, 40]
            cells.append(dict(source='fx_hourly', horizon=6, window=40,
                family=family, status='SELECTED', parameter=params[-1],
                validation_receipts=[dict(path=str(path.relative_to(root)),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest())]))
        selection = dict(version=1, status='FROZEN', created_utc='2026-10-22T00:01:00Z',
                         executable_freeze_sha256=executable_hash, cells=cells)
        path = root / '.scratch/selection.json'
        path.write_text(json.dumps(selection))
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def test_import_and_help_do_not_import_numpy_or_sources(self):
        runner = self.runner()
        code = ('import sys,run_conditional_study;'
                'assert "numpy" not in sys.modules;'
                'assert "conditional_sources" not in sys.modules;'
                'run_conditional_study.main(["--help"])')
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--selection-freeze', result.stdout)
        self.assertIn('--freeze-sha256', result.stdout)

    def test_validation_runs_whole_menu_and_exact_ties_prefer_larger_parameter(self):
        runner = self.runner()
        source, spec = artificial()
        public, private = runner.execute_phase(source, spec, 'validation',
                                               'fx_hourly', 6, 40, 'KNN')
        self.assertEqual(public['status'], 'COMPLETE')
        self.assertEqual([r['parameter'] for r in public['candidate_rows']], [19, 20, 40])
        self.assertEqual(public['selection']['parameter'], 40)
        self.assertEqual([r['origin_count'] for r in public['candidate_rows']], [6, 6, 6])
        self.assertTrue(all(r['mean_pinball'] == 0 for r in public['candidate_rows']))
        self.assertIn('origin_identity', public)
        self.assertEqual(public['origin_identity'], dict(count=6, first=190, last=195,
            sha256=hashlib.sha256(b''.join(i.to_bytes(8, 'little', signed=True)
                                         for i in range(190, 196))).hexdigest()))
        self.assertEqual(private['candidate_0_origins'].tolist(), list(range(190, 196)))
        self.assertTrue(all(np.isfinite(value).all() for value in private.values()))
        runner.public_json_bytes(public)

    def test_failed_candidate_blocks_selection_but_remaining_candidates_run(self):
        runner = self.runner()
        source, spec = artificial()
        import conditional_study
        actual = conditional_study.conditional_forecast
        def fail_middle(*args, **kwargs):
            if args[5] == 20:
                raise QuantileFitError('NONCONVERGENCE', {'iterations': 10000})
            return actual(*args, **kwargs)
        with patch.object(conditional_study, 'conditional_forecast', side_effect=fail_middle):
            public, private = runner.execute_phase(source, spec, 'validation',
                                                   'fx_hourly', 6, 40, 'KNN')
        self.assertEqual([r['status'] for r in public['candidate_rows']],
                         ['COMPLETE', 'FAILED', 'COMPLETE'])
        self.assertEqual(public['status'], 'INELIGIBLE')
        self.assertIsNone(public['selection']['parameter'])
        self.assertNotIn('candidate_1_capacity', private)
        self.assertIn('candidate_2_capacity', private)
        self.assertIsNone(public['candidate_rows'][1]['mean_pinball'])

    def test_resource_cancellation_propagates_and_retains_incomplete_state(self):
        runner = self.runner()
        source, spec = artificial()
        class Cancel(Exception):
            pass
        error = Cancel()
        def stop(**_):
            raise error
        with self.assertRaises(Cancel) as caught:
            runner.execute_phase(source, spec, 'validation', 'fx_hourly',
                                 6, 40, 'KNN', checkpoint=stop)
        self.assertIs(caught.exception, error)
        public, private = error.partial_phase_state
        self.assertEqual([r['status'] for r in public['candidate_rows']],
                         ['INCOMPLETE'] * 3)
        self.assertTrue(all(r['mean_pinball'] is None for r in public['candidate_rows']))
        self.assertEqual(private, {})

    def test_evaluation_uses_selected_only_and_reports_year_and_global_grid(self):
        runner = self.runner()
        source, spec = artificial()
        selection = dict(status='SELECTED', parameter=20)
        public, private = runner.execute_phase(source, spec, 'evaluation',
            'fx_hourly', 6, 40, 'KNN', selection=selection)
        self.assertEqual(public['status'], 'COMPLETE')
        self.assertEqual(len(public['summary_rows']), 1)
        self.assertEqual(public['summary_rows'][0]['origin_count'], 12)
        self.assertEqual([(r['year'], r['origin_count']) for r in public['year_rows']],
                         [(2019, 2), (2020, 10)])
        self.assertEqual(public['nonoverlap_rows'][0]['origin_count'], 2)
        self.assertEqual(private['KNN_origins'].tolist(), list(range(212, 224)))
        self.assertEqual(private['KNN_refit_indices'].tolist(),
                         [212] * 4 + [216] * 4 + [220] * 4)

    def test_null_selection_never_calls_forecasting_and_has_no_scores(self):
        runner = self.runner()
        source, spec = artificial()
        import conditional_study
        with patch.object(conditional_study, 'conditional_forecast',
                          side_effect=AssertionError('must not forecast')):
            public, private = runner.execute_phase(source, spec, 'evaluation',
                'fx_hourly', 6, 40, 'KNN', selection=dict(status='INELIGIBLE', parameter=None))
        self.assertEqual(public['status'], 'INELIGIBLE')
        self.assertEqual(public['summary_rows'], [])
        self.assertEqual(private, {})

    def test_failed_evaluation_has_partial_trace_but_no_partial_accuracy_mean(self):
        runner = self.runner()
        source, spec = artificial()
        import conditional_study
        partial = conditional_study.ConditionalForecast(
            np.arange(212, 215), np.zeros(3), np.zeros(3),
            np.full(3, 212), (), 'QR', .01)
        error = QuantileFitError('NONCONVERGENCE', {'iterations': 10000})
        error.partial_forecast = partial
        error.failure_context = {'refit_index': 216, 'issued_origin_count': 3}
        with patch.object(conditional_study, 'conditional_forecast', side_effect=error):
            public, private = runner.execute_phase(source, spec, 'evaluation',
                'fx_hourly', 6, 40, 'QR', selection=dict(status='SELECTED', parameter=.01))
        self.assertEqual(public['status'], 'FAILED')
        self.assertEqual(public['summary_rows'], [])
        self.assertEqual(private['QR_partial_origins'].tolist(), [212, 213, 214])
        self.assertEqual(public['failure']['code'], 'NONCONVERGENCE')
        self.assertEqual(public['failure']['context']['refit_index'], 216)

    def test_references_keep_all_declared_update_families(self):
        runner = self.runner()
        source, spec = artificial()
        public, private = runner.execute_phase(source, spec, 'references',
                                               'fx_hourly', 6, 40, None)
        names = [r['method'] for r in public['summary_rows']]
        self.assertEqual(names, [p + '_' + m for p in ('rolling', 'frozen', 'one_state')
                                for m in ('F', 'S', 'K')])
        self.assertEqual(private['rolling_F_refit_indices'].tolist(), list(range(212, 224)))
        self.assertEqual(private['frozen_F_refit_indices'].tolist(),
                         [212] * 4 + [216] * 4 + [220] * 4)
        self.assertEqual(len(public['nonoverlap_rows']), 9)

    def test_sources_with_bad_count_date_identity_or_nonfinite_values_are_rejected(self):
        runner = self.runner()
        source, spec = artificial()
        for change in [dict(position=np.zeros(279)), dict(sha256='b' * 64),
                       dict(bytes=1), dict(position=np.full(280, np.nan))]:
            bad = SimpleNamespace(**(vars(source) | change))
            with self.subTest(change=list(change)), self.assertRaises(ValueError):
                runner.execute_phase(bad, spec, 'validation', 'fx_hourly', 6, 40, 'KNN')
        dated = deepcopy(spec)
        dated['sources']['fx_hourly']['evaluation_first_date'] = '1900-01-01'
        with self.assertRaises(ValueError):
            runner.execute_phase(source, dated, 'evaluation', 'fx_hourly', 6, 40,
                                 'KNN', selection=dict(status='SELECTED', parameter=20))

    def test_public_serialization_rejects_private_arrays_and_nonfinite_scalars(self):
        runner = self.runner()
        for value in [dict(prediction=np.zeros(3)), dict(loss=np.nan),
                      dict(loss=np.float64(1)), dict(private='/Users/secret/file'),
                      dict(raw=[1., 2., 3.])]:
            with self.subTest(value=type(value)), self.assertRaises(ValueError):
                runner.public_json_bytes(value)

    def test_freeze_exact_inventory_hashes_and_sources_are_required(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            path, digest = self.fake_project(runner, root, spec)
            loaded, manifest = runner.verify_executable_freeze(digest, root=root)
            self.assertEqual(loaded, spec)
            self.assertEqual(set(manifest['files']), set(runner.CODE_FILES))
            initial = json.loads(path.read_text())
            for mutate in ('missing', 'extra', 'source'):
                bad = deepcopy(initial)
                if mutate == 'missing':
                    del bad['files'][runner.CODE_FILES[0]]
                elif mutate == 'extra':
                    bad['files']['unknown.py'] = 'a' * 64
                else:
                    bad['sources']['fx_hourly']['sha256'] = 'b' * 64
                path.write_text(json.dumps(bad))
                changed = hashlib.sha256(path.read_bytes()).hexdigest()
                with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                    runner.verify_executable_freeze(changed, root=root)

    def test_invalid_freeze_stops_before_loader_and_preserves_failure_receipt(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            (root / runner.CODE_FILES[0]).write_text('changed executable')
            attempt = root / '.scratch/failed-attempt'
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source',
                    side_effect=AssertionError('source access forbidden')) as loader:
                code = runner.main(self.args(attempt, digest))
            self.assertEqual(code, 1)
            self.assertFalse(loader.called)
            receipt = json.loads((attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['status'], 'STOPPED')
            self.assertEqual(receipt['stop_code'], 'EXECUTABLE_FREEZE')
            self.assertIsNone(receipt['source_identity'])
            self.assertNotIn('/Users/', json.dumps(receipt))

    def test_selection_freeze_recomputes_menu_loss_tie_and_receipt_identity(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            path, selected_hash = self.selection_fixture(root, spec, digest)
            cells = runner.verify_selection_freeze(path, selected_hash, digest, spec, root=root)
            self.assertEqual(cells[('fx_hourly', 6, 40, 'QR')]['parameter'], .1)
            original = json.loads(path.read_text())
            for kind in ('wrong_parameter', 'missing_cell', 'wrong_receipt_cell', 'changed_menu'):
                bad = deepcopy(original)
                if kind == 'wrong_parameter':
                    bad['cells'][0]['parameter'] = .01
                elif kind == 'missing_cell':
                    bad['cells'].pop()
                else:
                    receipt_path = root / bad['cells'][0]['validation_receipts'][0]['path']
                    receipt = self.validation_receipt(spec, 'QR', digest)
                    if kind == 'wrong_receipt_cell':
                        receipt['horizon'] = 24
                    else:
                        receipt['result']['candidate_rows'][0]['parameter'] = .2
                    receipt_path.write_text(json.dumps(receipt))
                    bad['cells'][0]['validation_receipts'][0]['sha256'] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
                path.write_text(json.dumps(bad))
                changed_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                with self.subTest(kind=kind), self.assertRaises(ValueError):
                    runner.verify_selection_freeze(path, changed_hash, digest, spec, root=root)

    def test_selection_null_is_justified_by_failed_or_incomplete_menu(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            path, _ = self.selection_fixture(root, spec, digest)
            selection = json.loads(path.read_text())
            cell = selection['cells'][0]
            receipt_path = root / cell['validation_receipts'][0]['path']
            receipt = json.loads(receipt_path.read_text())
            receipt['status'] = 'STOPPED'
            receipt['stop_code'] = 'RESOURCE_WALL'
            receipt['result']['candidate_rows'][1].update(
                status='INCOMPLETE', origin_count=0, mean_pinball=None)
            receipt_path.write_text(json.dumps(receipt))
            cell.update(status='INELIGIBLE', parameter=None)
            cell['validation_receipts'][0]['sha256'] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            path.write_text(json.dumps(selection))
            digest_selection = hashlib.sha256(path.read_bytes()).hexdigest()
            cells = runner.verify_selection_freeze(path, digest_selection, digest, spec, root=root)
            self.assertIsNone(cells[('fx_hourly', 6, 40, 'QR')]['parameter'])

    def test_selection_rejects_a_complete_receipt_without_measured_resources(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            path, _ = self.selection_fixture(root, spec, digest)
            selection = json.loads(path.read_text())
            ref = selection['cells'][0]['validation_receipts'][0]
            receipt_path = root / ref['path']
            receipt = json.loads(receipt_path.read_text())
            receipt['resources']['peak_rss_bytes'] = None
            receipt_path.write_text(json.dumps(receipt))
            ref['sha256'] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            path.write_text(json.dumps(selection))
            digest_selection = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                runner.verify_selection_freeze(path, digest_selection, digest, spec, root=root)

    def test_actual_resource_stop_happens_before_source_loader(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            attempt = root / '.scratch/resource-stop'
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source',
                    side_effect=AssertionError('source access forbidden')) as loader, \
                    patch.object(runner.RunGuard, '__call__', side_effect=runner.StudyStop('RESOURCE_WALL')):
                code = runner.main(self.args(attempt, digest))
            self.assertEqual(code, 1)
            self.assertFalse(loader.called)
            receipt = json.loads((attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['stop_code'], 'RESOURCE_WALL')
            self.assertIsNone(receipt['resources']['peak_rss_bytes'])

    def test_hard_deadline_remains_armed_during_private_output(self):
        runner = self.runner()
        source, spec = artificial()
        import signal
        actual = runner._write_numeric
        observed = []
        def observed_write(*args):
            observed.append(signal.getitimer(signal.ITIMER_REAL)[0])
            return actual(*args)
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            attempt = root / '.scratch/deadline-test'
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source', return_value=source), \
                    patch.object(runner, '_write_numeric', side_effect=observed_write):
                code = runner.main(self.args(attempt, digest))
            self.assertEqual(code, 0)
            self.assertEqual(len(observed), 1)
            self.assertGreater(observed[0], 0)
            self.assertEqual(signal.getitimer(signal.ITIMER_REAL)[0], 0)

    def test_main_writes_private_numeric_trace_and_public_scalar_receipt_once(self):
        runner = self.runner()
        source, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            attempt = root / '.scratch/complete-attempt'
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source', return_value=source):
                code = runner.main(self.args(attempt, digest))
                before = (attempt / 'public/manifest.json').read_bytes()
                again = runner.main(self.args(attempt, digest))
            self.assertEqual(code, 0)
            self.assertEqual(again, 1)
            receipt = json.loads((attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['status'], 'COMPLETE')
            self.assertEqual(receipt['result']['selection']['parameter'], 40)
            self.assertEqual(receipt['source_identity']['record_count'], 280)
            self.assertGreater(receipt['resources']['peak_rss_bytes'], 0)
            self.assertGreater(receipt['resources']['thread_snapshot_count'], 0)
            self.assertEqual({p.name for p in (attempt / 'public').iterdir()},
                             {'attempt-start.json', 'manifest.json'})
            with np.load(attempt / 'private/numeric-traces.npz', allow_pickle=False) as traces:
                self.assertEqual(traces['candidate_0_origins'].tolist(), list(range(190, 196)))
            self.assertEqual(hashlib.sha256(before).hexdigest(),
                             hashlib.sha256((attempt / 'public/manifest.json').read_bytes()).hexdigest())

    def test_main_evaluation_verifies_selection_before_loading_and_issues_selected_only(self):
        runner = self.runner()
        source, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            selection, selection_hash = self.selection_fixture(root, spec, digest)
            attempt = root / '.scratch/evaluation'
            arguments = self.args(attempt, digest, phase='evaluation') + [
                '--selection-freeze', str(selection), '--selection-sha256', selection_hash]
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source', return_value=source):
                code = runner.main(arguments)
            self.assertEqual(code, 0)
            receipt = json.loads((attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['result']['selection']['parameter'], 40)
            self.assertEqual(len(receipt['result']['summary_rows']), 1)
            self.assertEqual(receipt['result']['summary_rows'][0]['origin_count'], 12)
            bad_attempt = root / '.scratch/rejected-selection'
            arguments = self.args(bad_attempt, digest, phase='evaluation') + [
                '--selection-freeze', str(selection), '--selection-sha256', '0' * 64]
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source',
                    side_effect=AssertionError('must not load')) as loader:
                code = runner.main(arguments)
            self.assertEqual(code, 1)
            self.assertFalse(loader.called)
            receipt = json.loads((bad_attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['stop_code'], 'SELECTION_FREEZE')

    def test_manifest_boolean_version_cannot_impersonate_version_one(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            path, _ = self.fake_project(runner, root, spec)
            freeze = json.loads(path.read_text())
            freeze['version'] = True
            path.write_text(json.dumps(freeze))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                runner.verify_executable_freeze(digest, root=root)

    def test_hard_kill_leaves_unverified_start_marker_without_invented_terminal_status(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            attempt = root / '.scratch/killed-attempt'
            arguments = self.args(attempt, digest)
            code = ("import pathlib,time,run_study,run_conditional_study as r;"
                    "r.ROOT=pathlib.Path(" + repr(str(root)) + ");"
                    "r.arm_hard_deadline=lambda:run_study.arm_hard_deadline(.08);"
                    "r.load_source=lambda *a,**k:time.sleep(2);"
                    "r.main(" + repr(arguments) + ")")
            completed = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                                       capture_output=True, text=True, timeout=5)
            import signal
            self.assertEqual(completed.returncode, -signal.SIGALRM)
            start = json.loads((attempt / 'public/attempt-start.json').read_text())
            self.assertEqual(start['status'], 'INCOMPLETE')
            self.assertEqual(start['terminal_receipt'], 'UNVERIFIED_UNTIL_MANIFEST')
            self.assertFalse((attempt / 'public/manifest.json').exists())

    def test_selection_receipt_must_bind_the_exact_declared_origin_vector(self):
        runner = self.runner()
        _, spec = artificial()
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            path, _ = self.selection_fixture(root, spec, digest)
            selection = json.loads(path.read_text())
            ref = selection['cells'][0]['validation_receipts'][0]
            receipt_path = root / ref['path']
            receipt = json.loads(receipt_path.read_text())
            receipt['result']['origin_identity']['sha256'] = '0' * 64
            receipt_path.write_text(json.dumps(receipt))
            ref['sha256'] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            path.write_text(json.dumps(selection))
            digest_selection = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                runner.verify_selection_freeze(path, digest_selection, digest, spec, root=root)

    def test_executable_change_during_phase_stops_the_complete_receipt(self):
        runner = self.runner()
        source, spec = artificial()
        actual = runner.execute_phase
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as folder:
            root = Path(folder)
            _, digest = self.fake_project(runner, root, spec)
            attempt = root / '.scratch/changed-during-phase'
            def changed_after_phase(*args, **kwargs):
                result = actual(*args, **kwargs)
                (root / runner.CODE_FILES[0]).write_text('concurrent change')
                return result
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'load_source', return_value=source), \
                    patch.object(runner, 'execute_phase', side_effect=changed_after_phase):
                code = runner.main(self.args(attempt, digest))
            self.assertEqual(code, 1)
            receipt = json.loads((attempt / 'public/manifest.json').read_text())
            self.assertEqual(receipt['status'], 'STOPPED')
            self.assertEqual(receipt['stop_code'], 'EXECUTABLE_FREEZE')
            self.assertTrue((attempt / 'private/numeric-traces.npz').exists())


if __name__ == '__main__':
    unittest.main()
