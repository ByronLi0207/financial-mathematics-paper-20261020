"""Independent readback contract, using only synthetic observations."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import numpy as np


class ReadbackFixture:

    @classmethod
    def setUpClass(cls):
        cls.module = None
        if importlib.util.find_spec('verify_rank_ablation') is not None:
            import verify_rank_ablation
            cls.module = verify_rank_ablation

    def verifier(self):
        self.assertIsNotNone(self.module, 'independent arithmetic verifier must exist')
        return self.module


class IndependentReadbackTests(ReadbackFixture, unittest.TestCase):
    def test_integer_ranks_and_minimizer_endpoint_contract(self):
        v = self.verifier()
        for w, expected in [(52, (50, 51)), (260, (247, 248)),
                            (720, (684, 685)), (2880, (2736, 2737))]:
            self.assertEqual(v.exact_ranks(w), expected)
        # The empirical derivative is zero between ranks 19 and 20 for W20.
        for q in (19, 19.25, 19.5, 20):
            loss = sum(19 * max(y-q, 0) + max(q-y, 0) for y in range(1, 21))
            self.assertEqual(loss, 190)
        self.assertGreater(sum(19*max(y-18, 0)+max(18-y, 0) for y in range(1, 21)), 190)
        self.assertGreater(sum(19*max(y-21, 0)+max(21-y, 0) for y in range(1, 21)), 190)
        with self.assertRaises(ValueError):
            v.exact_ranks(True)
        with self.assertRaises(ValueError):
            v.exact_ranks(1)

    def test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit(self):
        v = self.verifier()
        x = [float(i*i) for i in range(30)]
        rows = v.reconstruct_cell(x, [22, 23, 24], 1, 20, 2)
        self.assertEqual(rows['origins'], [22, 23, 24])
        self.assertEqual(rows['refit_indices'], [22, 22, 24])
        self.assertEqual(rows['latest_label_ends'], [22, 22, 24])
        self.assertEqual(rows['floor'], [484., 529., 576.])
        self.assertEqual(rows['I'], [525., 570., 621.])
        self.assertEqual(rows['F'], [527., 572., 623.])
        self.assertEqual(rows['peak'], [529., 576., 625.])
        self.assertEqual(rows['I_pinball'], [3.8, 5.699999999999999, 3.8])
        self.assertEqual(rows['F_pinball'], [1.9, 3.8, 1.9])
        self.assertEqual(rows['refit_count'], 2)
        self.assertEqual(rows['source_window_headroom_count'], 40)

    def test_future_values_cannot_change_pre_refit_reports_but_do_change_target(self):
        v = self.verifier()
        x = [float(i*i) for i in range(30)]
        base = v.reconstruct_cell(x, [22, 23], 1, 20, 2)
        x[23] = 10000.
        changed = v.reconstruct_cell(x, [22, 23], 1, 20, 2)
        self.assertEqual(changed['I'][0], base['I'][0])
        self.assertEqual(changed['F'][0], base['F'][0])
        self.assertEqual(changed['peak'][0], 10000.)
        self.assertEqual(changed['I'][1], 10041.)
        self.assertEqual(changed['F'][1], 10043.)

    def test_ties_strict_breach_and_zero_breach_reason(self):
        v = self.verifier()
        rows = v.reconstruct_cell([7.]*30, [22, 23, 24], 1, 20, 2)
        self.assertEqual(rows['I'], [7., 7., 7.])
        self.assertEqual(rows['F'], [7., 7., 7.])
        stats = v.summarize(rows, 'I', [0, 1, 2])
        self.assertEqual(stats['strict_breach_count'], 0)
        self.assertIsNone(stats['conditional_mean_overrun'])
        self.assertEqual(stats['conditional_overrun_undefined_reason'], 'NO_STRICT_BREACHES')
        self.assertEqual(stats['mean_extra_allowance'], 0.)
        self.assertEqual(stats['mean_pinball'], 0.)

    def test_constant_decimal_mean_is_preserved_exactly(self):
        v = self.verifier()
        rows = v.reconstruct_cell([.1]*30, [22, 23, 24], 1, 20, 2)
        self.assertEqual(v.summarize(rows, 'I', [0,1,2])['mean_capacity'], .1)

    def test_thread_snapshot_requires_every_pid_row(self):
        v = self.verifier()
        self.assertTrue(callable(getattr(v, '_parse_thread_snapshot', None)), 'strict independent PID parser required')
        self.assertEqual(v._parse_thread_snapshot(' 42\n42\n', 42), 2)
        native = 'USER PID TT %CPU STAT PRI STIME UTIME COMMAND\nu 42 ?? 0 S 31T 0:00 0:00 /python 42\n'
        self.assertEqual(v._parse_thread_snapshot(native, 42), 1)
        with self.assertRaises(ValueError):
            v._parse_thread_snapshot(native.replace('/python 42', '/python 43'), 42)
        for raw in ('', '42\n43\n', 'USER PID\n42\n', '42x\n'):
            with self.assertRaises(ValueError):
                v._parse_thread_snapshot(raw, 42)

    def test_attempt_dotdot_escape_does_not_create_outside_receipt(self):
        v = self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve(); (root/'.scratch').mkdir()
            (root/'elsewhere'/'public').mkdir(parents=True)
            with self.assertRaises(ValueError):
                v.verify_attempt(root/'.scratch'/'..'/'elsewhere', root=root)
            self.assertFalse((root/'elsewhere'/'public'/'independent-readback.json').exists())

    def test_oracle_rejects_missing_history_duplicate_origins_and_incomplete_targets(self):
        v = self.verifier()
        for ids in ([1], [22, 22], [22, 24], [29]):
            with self.assertRaises(ValueError):
                v.reconstruct_cell([float(i*i) for i in range(30)], ids, 1, 20, 2)

    def test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys(self):
        v = self.verifier()
        arrays = dict(origins=np.array([22]), peak=np.array([529.]), floor=np.array([484.]),
                      I=np.array([525.]), F=np.array([527.]), refit_indices=np.array([22]),
                      I_pinball=np.array([3.8]), F_pinball=np.array([1.9]))
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/'cell.npz'
            np.savez(p, **arrays)
            self.assertEqual(set(v.read_private_npz(p)), set(arrays))
            absent = dict(arrays); del absent['F_pinball']
            np.savez(p, **absent)
            with self.assertRaises(ValueError):
                v.read_private_npz(p)
            np.savez(p, **arrays, surprise=np.array([0]))
            with self.assertRaises(ValueError):
                v.read_private_npz(p)
            np.savez(p, **arrays)
            with zipfile.ZipFile(p, 'a') as archive:
                content = io.BytesIO(); np.save(content, np.array([0]))
                with self.assertWarns(UserWarning):
                    archive.writestr('origins.npy', content.getvalue())
            with self.assertRaises(ValueError):
                v.read_private_npz(p)

    def test_exact_table_matching_reports_all_changed_fields_and_duplicate_rows(self):
        v = self.verifier()
        wanted = [dict(source='s', horizon=1, window=20, method='I',
                       origin_count=3, mean_pinball=1.25, conditional_mean_overrun=None)]
        got = [dict(source='s', horizon='1', window='20', method='I',
                    origin_count='2', mean_pinball='1.2500000000000002', conditional_mean_overrun='')]
        checks = v.Checks()
        v.compare_table(got, wanted, ('source','horizon','window','method'), checks, 'summary')
        self.assertEqual(len(checks.errors), 2)
        checks = v.Checks()
        v.compare_table(got+got, wanted, ('source','horizon','window','method'), checks, 'summary')
        self.assertTrue(any('DUPLICATE' in e for e in checks.errors))
        self.assertGreater(checks.count, 0)

    def test_saved_arrays_compare_every_issue_and_count_exact_disagreements(self):
        v = self.verifier()
        rows = v.reconstruct_cell([float(i*i) for i in range(30)], [22, 23, 24], 1, 20, 2)
        saved = {key: np.asarray(rows[key]) for key in v.PRIVATE_KEYS}
        saved['I'][0] += 1
        saved['F_pinball'][2] = np.nextafter(saved['F_pinball'][2], np.inf)
        checks = v.Checks()
        v.compare_private(saved, rows, checks, 'synthetic')
        self.assertEqual(len(checks.errors), 2)
        self.assertEqual(checks.count, 24)

    def test_no_overwrite_and_scratch_boundary(self):
        v = self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            outside = root/'elsewhere'; outside.mkdir()
            with self.assertRaises(ValueError):
                v.verify_attempt(outside, root=root)
            attempt = root/'.scratch'/'attempt'; (attempt/'public').mkdir(parents=True)
            receipt = attempt/'public'/'independent-readback.json'
            receipt.write_text('preserved')
            with self.assertRaises(FileExistsError):
                v.verify_attempt(attempt, root=root)
            self.assertEqual(receipt.read_text(), 'preserved')


class CompleteSyntheticAttemptTests(ReadbackFixture, unittest.TestCase):
    """Closed-form constant-source fixture protects the complete artifact boundary."""
    def make_attempt(self, root):
        import csv
        import hashlib
        v = self.verifier()
        def digest(raw): return hashlib.sha256(raw).hexdigest()
        def dump(path, obj):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(obj))
        def table(path, rows):
            with path.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader(); writer.writerows(rows)
        sources = {}
        for name in ('fx_hourly', 'nyfed_weekly'):
            path = root/(name+'.csv')
            if name == 'fx_hourly':
                from datetime import datetime, timedelta
                path.write_text('datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n'+''.join(
                    f'{(datetime(2020,12,28)+timedelta(days=i)).strftime("%Y.%m.%dT%H:%M:%S.%f")},7,0,0,0\n' for i in range(90)))
            else:
                from datetime import datetime, timedelta
                path.write_text('As Of Date,Time Series,Value (millions)\n'+''.join(
                    f'{(datetime(2020,12,28)+timedelta(days=i)).strftime("%Y-%m-%d")},PDPOSGS-B,7\n' for i in range(90)))
            raw = path.read_bytes()
            sources[name] = dict(input_relative_path=path.name, bytes=len(raw), sha256=digest(raw),
                                 record_count=90, native_unit='synthetic', evaluation_origin_first=82,
                                 evaluation_origin_last=84, windows=[20,40], refit_step=2)
        original = dict(sources=sources, horizons=[1,2])
        original_name = 'protocol/revision-20261022/study-spec.json'
        dump(root/original_name, original)
        rank_name = 'protocol/revision-20261022/rank-ablation-spec.json'
        rank = dict(original_spec=original_name, original_spec_sha256=digest((root/original_name).read_bytes()),
                    original_summary='archive.csv', tau=[19,20])
        dump(root/rank_name, rank)
        attempt = root/'.scratch'/'synthetic'; (attempt/'private').mkdir(parents=True); (attempt/'public').mkdir()
        stats = dict(origin_count=3,mean_pinball=0.,mean_capacity=7.,mean_extra_allowance=0.,
                     strict_breach_count=0,strict_breach_rate=0.,mean_positive_overrun=0.,
                     conditional_mean_overrun=None,conditional_overrun_denominator=0,
                     conditional_overrun_undefined_reason='NO_STRICT_BREACHES',mean_unused_allowance=0.)
        summaries=[]; annual=[]; sparse=[]; contrasts=[]; cells=[]; archived=[]
        for source, cfg in sources.items():
            for h in (1,2):
                for w in (20,40):
                    meta=dict(source=source,native_unit='synthetic',horizon=h,window=w,refit_step=2)
                    for method in ('I','F'):
                        summaries.append(dict(**meta,method=method,**stats))
                        annual.append(dict(**meta,method=method,issue_year='2021',**stats))
                        small=dict(stats); small['origin_count']=2 if h==1 else 1
                        sparse.append(dict(**meta,method=method,**small))
                    frow=dict(**meta,method='frozen_F',**stats)
                    qr=dict(**meta,method='QR',**stats); qr['mean_pinball']=.5
                    archived.extend((frow,qr))
                    for name,left,right in [('QR-minus-I',.5,0.),('I-minus-frozen_F',0.,0.),('QR-minus-frozen_F',.5,0.)]:
                        contrasts.append(dict(**meta,contrast=name,origin_count=3,mean_loss_left=left,mean_loss_right=right,
                                              difference_of_means=left-right,relative_mean_loss_difference_percent=None,
                                              undefined_reason='ZERO_REFERENCE_MEAN_LOSS',
                                              direct_paired_difference=0. if name=='I-minus-frozen_F' else None))
                    p=attempt/'private'/f'{source}-h{h}-w{w}.npz'
                    np.savez(p,origins=np.array([82,83,84]),peak=np.array([7.,7.,7.]),floor=np.array([7.,7.,7.]),
                             I=np.array([7.,7.,7.]),F=np.array([7.,7.,7.]),refit_indices=np.array([82,82,84]),
                             I_pinball=np.array([0.,0.,0.]),F_pinball=np.array([0.,0.,0.]))
                    qr_strings={k: '' if val is None else str(val) for k,val in qr.items()}
                    cells.append(dict(**meta,origin_count=3,rank_I=(19*w+19)//20,rank_F=(19*(w+1)+19)//20,
                                      both_empirical_minimizer_endpoints=True,changed_capacity_count=0,
                                      imported_QR_summary=qr_strings,reference_F_metrics_exact=True,
                                      private_file='private/'+p.name,private_sha256=digest(p.read_bytes()),observed_os_threads=1))
        table(root/'archive.csv',archived)
        for name,rows in [('summary.csv',summaries),('annual.csv',annual),('nonoverlap.csv',sparse),('contrasts.csv',contrasts)]:
            table(attempt/'public'/name,rows)
        freeze_name='protocol/revision-20261022/rank-ablation-executable-freeze.json'
        bound=[]
        for name in [rank_name,original_name,'archive.csv']:
            raw=(root/name).read_bytes(); bound.append(dict(path=name,bytes=len(raw),sha256=digest(raw)))
        dump(root/freeze_name,dict(files=bound))
        audit=dict(status='COMPLETE',completed_cells=8,summary_rows=16,annual_rows=16,nonoverlap_rows=16,contrast_rows=24,
                   executable_freeze_sha256=digest((root/freeze_name).read_bytes()),cells=cells,
                   accuracy_recomputed=['I','frozen_F'],QR_refitted=False,independent_data_validation=False,
                   requested_numerical_threads=1,maximum_observed_os_threads=1,peak_rss_bytes=1000000,elapsed_seconds=1.,
                   thread_snapshot_count=9,resources_are_snapshot_observations=True)
        audit['exports']=[dict(path=p.name,bytes=p.stat().st_size,sha256=digest(p.read_bytes())) for p in sorted((attempt/'public').glob('*.csv'))]
        dump(attempt/'public'/'audit.json',audit)
        return attempt

    def test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources(self):
        v=self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); attempt=self.make_attempt(root)
            result=v.verify_attempt(attempt,root=root)
            self.assertEqual(result['status'],'VERIFIED',result.get('errors'))
            self.assertEqual(result['verified_cells'],8)
            self.assertEqual(result['verified_issues'],24)
            self.assertEqual(result['checked_issued_reports'],48)
            self.assertGreaterEqual(result['full_check_count'],192)
            self.assertFalse(result['independent_financial_validation'])
            self.assertGreater(result['peak_rss_bytes'],0)
            self.assertGreater(result['elapsed_seconds'],0)
            self.assertGreater(result['maximum_observed_os_threads'],0)
            readback=json.loads((attempt/'public'/'independent-readback.json').read_text())
            self.assertEqual(result,readback)
            self.assertNotIn('raw_vectors',readback)

    def test_changed_public_values_and_private_issue_are_all_reported(self):
        v=self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); attempt=self.make_attempt(root)
            p=attempt/'public'/'summary.csv'
            p.write_text(p.read_text().replace(',I,3,0.0,7.0,',',I,3,0.1,7.0,',1))
            p=attempt/'private'/'fx_hourly-h1-w20.npz'
            with np.load(p) as z: arrays={k:z[k].copy() for k in z.files}
            arrays['I'][0]=8.; np.savez(p,**arrays)
            result=v.verify_attempt(attempt,root=root)
            self.assertEqual(result['status'],'FAILED')
            self.assertGreaterEqual(result['mismatch_count'],4)
            self.assertTrue(any('summary' in e for e in result['errors']))
            self.assertTrue(any('I[0]' in e for e in result['errors']))
            self.assertEqual(result['verified_cells'],8)


if __name__ == '__main__':
    unittest.main()
