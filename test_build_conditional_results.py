"""Adversarial checks of the additive export auditor; no financial data."""
import copy
import hashlib
import io
import unittest
from unittest.mock import patch
import numpy as np
import build_conditional_results as builder
from build_conditional_results import independent_peak, verify_method, verify_resource, verify_fit_records


class ExportAuditTests(unittest.TestCase):
    def setUp(self):
        self.origins = np.array([0, 1, 2], dtype=np.int64)
        self.peak = np.array([8., 8., 4.])
        self.floor = np.array([8., 2., 4.])
        self.refits = np.array([0, 0, 2], dtype=np.int64)
        # Independently specified outcomes: no error, overrun2, unused6.
        self.traces = dict(m_origins=self.origins.copy(), m_peak=self.peak.copy(),
            m_floor=self.floor.copy(), m_refit_indices=self.refits.copy(),
            m_capacity=np.array([8., 6., 10.]), m_pinball=np.array([0., 1.9, .05 * 6.]))

    def check(self, traces):
        return verify_method(traces, 'm', self.origins, self.peak, self.floor, self.refits)

    def test_peak_includes_issue_last_endpoint_and_absolute_negative(self):
        p = np.array([-8., 2., -4., 9., -1.])
        np.testing.assert_array_equal(independent_peak(p, self.origins, 2), [8., 9., 9.])
        np.testing.assert_array_equal(p, [-8., 2., -4., 9., -1.])

    def test_known_native_loss_and_overrun_are_preserved(self):
        scores = self.check(self.traces)
        np.testing.assert_array_equal(scores.overrun, [0., 2., 0.])
        np.testing.assert_array_equal(scores.unused, [0., 0., 6.])
        self.assertEqual(scores.pinball[1], 1.9)

    def test_each_identity_or_score_tamper_is_rejected(self):
        for key in ('m_origins', 'm_peak', 'm_floor', 'm_refit_indices', 'm_pinball'):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.traces); changed[key][1] += 1
                with self.assertRaises(ValueError): self.check(changed)

    def test_capacity_below_known_floor_is_rejected_even_with_matching_loss(self):
        changed = copy.deepcopy(self.traces); changed['m_capacity'][0] = 7.
        changed['m_pinball'][0] = .95
        with self.assertRaises(ValueError): self.check(changed)

    def test_resource_overrun_and_unverified_probes_are_rejected(self):
        resource = dict(elapsed_seconds=1., peak_rss_bytes=1000,
            maximum_observed_os_threads=1, thread_snapshot_count=1, thread_probe_status='PASS')
        verify_resource(resource)
        for key, value in (('elapsed_seconds', 540.), ('elapsed_seconds', float('nan')),
                ('peak_rss_bytes', 1610612736), ('maximum_observed_os_threads', 3),
                ('thread_snapshot_count', 0), ('thread_probe_status', 'UNVERIFIED')):
            with self.subTest(key=key, value=value):
                with self.assertRaises(ValueError): verify_resource(resource | {key: value})

    def test_malformed_numerical_diagnostics_are_rejected(self):
        numerator, denominator = float(.95).as_integer_ratio(); grid = 2**40
        row = dict(method='QR', parameter=.01, refit_index=100,
            training_first_origin=75, training_last_origin=94, training_count=20, latest_label_end=100,
            iterations=50, primal_objective=.1, dual_objective=.1, duality_gap=0.,
            primal_residual=0., primal_tolerance=1e-6, dual_residual=0., dual_tolerance=1e-6,
            gap_tolerance=1.1e-6, dual_integer_sum=0, dual_grid_denominator=grid,
            dual_integer_lower=-((denominator-numerator)*grid//denominator),
            dual_integer_upper=numerator*grid//denominator)
        cfg=dict(refit_step=24)
        verify_fit_records([row], cfg, 6, 20, 'QR', 100, 100)
        for key, value in (('duality_gap', -1.), ('primal_residual', -1.), ('dual_residual', float('nan')),
                ('dual_tolerance', -1.), ('iterations', 10001), ('primal_objective', -.1),
                ('dual_objective', .2), ('dual_integer_lower', -1)):
            with self.subTest(key=key):
                with self.assertRaises(ValueError): verify_fit_records([row | {key:value}], cfg, 6, 20, 'QR', 100, 100)

    def test_phase_labels_and_terminal_fields_must_match_frozen_selection(self):
        receipt=dict(status='COMPLETE',stop_code=None,result=dict(status='COMPLETE',failure=None,candidate_rows=[],
            summary_rows=[dict(method='QR',parameter=.01)],fit_diagnostics=[dict(method='QR',parameter=.01)]))
        builder.verify_phase_labels(receipt,['QR'],.01)
        for location, key, value in (('summary_rows','parameter',.1),('fit_diagnostics','parameter',.1),
                ('fit_diagnostics','method','KNN')):
            changed=copy.deepcopy(receipt);changed['result'][location][0][key]=value
            with self.assertRaises(ValueError):builder.verify_phase_labels(changed,['QR'],.01)
        changed=copy.deepcopy(receipt);changed['stop_code']='NUMERICAL_FAILURE'
        with self.assertRaises(ValueError):builder.verify_phase_labels(changed,['QR'],.01)
        changed=copy.deepcopy(receipt);changed['result']['failure']={'code':'STOPPED'}
        with self.assertRaises(ValueError):builder.verify_phase_labels(changed,['QR'],.01)

    def test_parser_uses_only_the_verified_byte_snapshot(self):
        stream=io.BytesIO();np.savez(stream,x=np.array([7.]))
        accepted=stream.getvalue();metadata=dict(area='private',name='numeric-traces.npz',bytes=len(accepted),
            sha256=hashlib.sha256(accepted).hexdigest())
        with builder.verified_archive(accepted,metadata) as archive:
            np.testing.assert_array_equal(archive['x'],[7.])
        replacement=io.BytesIO();np.savez(replacement,x=np.array([8.]))
        with patch.object(builder.np,'load',side_effect=AssertionError('unverified bytes parsed')):
            with self.assertRaises(ValueError):builder.verified_archive(replacement.getvalue(),metadata)


if __name__ == '__main__': unittest.main()
