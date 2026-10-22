"""Known-event tests for post-result descriptive diagnostics, no financial data."""
import unittest
import hashlib
import numpy as np
import build_conditional_diagnostics as diagnostics
from build_conditional_diagnostics import floor_diagnostics, horizon_diagnostics


class DiagnosticTests(unittest.TestCase):
    def test_summary_labels_parse_the_exact_hashed_snapshot_once(self):
        class ChangingSource:
            def __init__(self):self.reads=0
            def read_bytes(self):
                self.reads+=1
                return b'source,parameter\nsynthetic,007\n' if self.reads==1 else b'source,parameter\nchanged,999\n'
            def open(self,*args,**kwargs):raise AssertionError('reopening a hashed source is forbidden')
        raw=b'source,parameter\nsynthetic,007\n'
        expected=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        source=ChangingSource()
        self.assertEqual(diagnostics.load_verified_summary(source,expected),[dict(source='synthetic',parameter='007')])
        self.assertEqual(source.reads,1)
        with self.assertRaises(ValueError):
            diagnostics.load_verified_summary(ChangingSource(),dict(bytes=len(raw),sha256='0'*64))
        with self.assertRaises(ValueError):
            diagnostics.load_verified_summary(ChangingSource(),dict(bytes=len(raw)+1,sha256=expected['sha256']))

    def test_binding_events_do_not_equal_outcome_atoms_or_all_breaches(self):
        p=np.array([3.,2.,4.]);c=np.array([3.,2.,0.]);b=np.array([1.,2.,0.])
        d=floor_diagnostics(p,c,b)
        self.assertEqual(d['origin_count'],3)
        self.assertEqual(d['zero_headroom_outcome_count'],1)
        self.assertEqual(d['floor_binding_count'],2)
        self.assertEqual(d['floor_binding_breach_count'],1)
        self.assertEqual(d['floor_binding_breach_rate'],.5)
        self.assertEqual(d['other_issue_breach_count'],0)

    def test_empty_event_sets_are_undefined_not_zero_risk(self):
        a=floor_diagnostics(np.array([3.]),np.array([2.]),np.array([1.]))
        self.assertIsNone(a['floor_binding_breach_rate'])
        self.assertEqual(a['floor_binding_undefined_reason'],'NO_FLOOR_BINDING_ISSUES')
        b=floor_diagnostics(np.array([3.]),np.array([1.]),np.array([1.]))
        self.assertIsNone(b['other_issue_breach_rate'])
        self.assertEqual(b['other_issue_undefined_reason'],'NO_OTHER_ISSUES')

    def test_horizon_crossing_has_a_distinct_target_order(self):
        d=horizon_diagnostics(np.array([3.,2.,0.]),np.array([2.,6.,5.]),
            np.array([3.,2.,4.]),np.array([4.,5.,4.]))
        self.assertEqual(d['strict_crossing_count'],1)
        self.assertEqual(d['maximum_positive_crossing'],1.)
        self.assertEqual(d['mean_positive_crossing'],1/3)
        self.assertEqual(d['target_order_violation_count'],0)

    def test_impossible_target_or_report_must_fail(self):
        with self.assertRaises(ValueError):horizon_diagnostics(np.array([2.]),np.array([3.]),np.array([4.]),np.array([3.]))
        with self.assertRaises(ValueError):floor_diagnostics(np.array([3.]),np.array([0.]),np.array([1.]))
        with self.assertRaises(ValueError):floor_diagnostics(np.array([3.]),np.array([float('nan')]),np.array([1.]))


if __name__=='__main__':unittest.main()
