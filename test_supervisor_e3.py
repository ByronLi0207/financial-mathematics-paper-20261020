"""Behavioral checks for the E3 extension; no financial source is used."""
import importlib.util
import tempfile
import unittest
import json
from pathlib import Path
import numpy as np

if importlib.util.find_spec('supervisor_e3'):
    import supervisor_e3 as e3
else:
    e3 = None


class E3Tests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(e3, 'E3 implementation is missing')

    def test_failed_menu_candidate_blocks_selection_and_exact_tie_prefers_larger(self):
        # A faulty eligible-only minimum would incorrectly pick1 after failure.
        rows=[dict(parameter=p,status='COMPLETE',origin_count=4,mean_pinball=2.)
              for p in (.001,.01,.1,1.,10.)]
        self.assertEqual(e3.freeze_selection(rows,4)['parameter'],10.)
        rows[0]=dict(parameter=.001,status='FAILED',reason='NONCONVERGENCE')
        picked=e3.freeze_selection(rows,4)
        self.assertEqual(picked['status'],'INELIGIBLE')
        self.assertIsNone(picked['parameter'])

    def test_archive_trace_reconciliation_rejects_one_wrong_origin_or_loss(self):
        # Capacity5 and peaks4,6 give pinball .05,.95 and mean .5 at tau.95.
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'trace.npz'
            payload=dict(origins=np.array([10,11]),capacity=np.array([5.,5.]),
                         peak=np.array([4.,6.]),pinball=np.array([.05,.95]))
            np.savez(path,**payload)
            got=e3.checked_trace(path,np.array([10,11]),np.array([4.,6.]),.5)
            np.testing.assert_array_equal(got['capacity'],[5.,5.])
            with self.assertRaises(ValueError):
                e3.checked_trace(path,np.array([10,12]),np.array([4.,6.]),.5)
            payload['pinball'][1]=.9
            np.savez(path,**payload)
            with self.assertRaises(ValueError):
                e3.checked_trace(path,np.array([10,11]),np.array([4.,6.]),.5)

    def test_paired_difference_rejects_equal_length_but_misaligned_origins(self):
        old=dict(origins=np.array([10,11]),peak=np.array([4.,6.]),pinball=np.array([.05,.95]))
        new=dict(origins=np.array([10,11]),peak=np.array([4.,6.]),pinball=np.array([.1,.7]))
        np.testing.assert_allclose(e3.paired_loss_difference(old,new),[.05,-.25])
        new['origins']=np.array([9,10])
        with self.assertRaises(ValueError):e3.paired_loss_difference(old,new)

    def test_numerical_failure_diagnostics_survive_json_serialization(self):
        # The solver exposes an immutable mapping, which plain json cannot encode.
        # Losing it would erase the diagnostic on a genuine failed candidate.
        from conditional_quantile import QuantileFitError
        error=QuantileFitError('NONCONVERGENCE',dict(iterations=10000,duality_gap=.2))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'failure.json'
            e3.dump(path,dict(status='FAILED',reason=error.code,solver_diagnostics=error.diagnostics))
            self.assertEqual(json.loads(path.read_text()),dict(status='FAILED',reason='NONCONVERGENCE',
                             solver_diagnostics=dict(iterations=10000,duality_gap=.2)))


if __name__=='__main__':unittest.main()
