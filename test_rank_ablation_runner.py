import importlib.util
import pathlib
import tempfile
import unittest
import json
import hashlib


class RunnerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = None
        spec = importlib.util.find_spec('run_rank_ablation')
        if spec is not None:
            import run_rank_ablation
            cls.module = run_rank_ablation

    def test_runner_exists(self):
        self.assertIsNotNone(self.module, 'rank runner must exist')

    def test_duplicate_reference_rejected(self):
        self.assertIsNotNone(self.module)
        row = dict(source='x', horizon='6', window='52', method='QR')
        with self.assertRaises(ValueError):
            self.module.reference_index([row, row])

    def test_exact_reference_check_catches_changed_breach_count(self):
        self.assertIsNotNone(self.module)
        self.module.compare_reference({'mean_pinball': 1.25, 'strict_breach_count': 2},
                                      {'mean_pinball': '1.25', 'strict_breach_count': '2'})
        with self.assertRaises(ValueError):
            self.module.compare_reference({'mean_pinball': 1.25, 'strict_breach_count': 3},
                                          {'mean_pinball': '1.25', 'strict_breach_count': '2'})

    def test_changed_or_traversing_freeze_rejected(self):
        self.assertIsNotNone(self.module)
        with tempfile.TemporaryDirectory() as t:
            r = pathlib.Path(t).resolve()
            (r/'x').write_bytes(b'good')
            entry = {'path': 'x', 'bytes': 4, 'sha256': hashlib.sha256(b'good').hexdigest()}
            self.module.check_frozen_files(r, [entry])
            (r/'x').write_bytes(b'bad!')
            with self.assertRaises(ValueError):
                self.module.check_frozen_files(r, [entry])
            entry['path'] = '../x'
            with self.assertRaises(ValueError):
                self.module.check_frozen_files(r, [entry])

    def test_output_path_cannot_escape_task_scratch(self):
        self.assertIsNotNone(self.module)
        with tempfile.TemporaryDirectory() as t:
            root = pathlib.Path(t).resolve()
            allowed = root/'.scratch'/'attempt'
            self.assertEqual(self.module.scratch_output(root, str(allowed)), allowed)
            with self.assertRaises(ValueError):
                self.module.scratch_output(root, str(root/'.scratch'/'..'/'escape'))
            with self.assertRaises(ValueError):
                self.module.scratch_output(root, str(root/'other'))

    def test_means_contrast_keeps_adverse_sign_and_zero_reason(self):
        self.assertIsNotNone(self.module)
        c = self.module.mean_contrast(2., 1.)
        self.assertEqual(c['relative_mean_loss_difference_percent'], 100.)
        self.assertEqual(c['difference_of_means'], 1.)
        z = self.module.mean_contrast(1., 0.)
        self.assertIsNone(z['relative_mean_loss_difference_percent'])
        self.assertEqual(z['undefined_reason'], 'ZERO_REFERENCE_MEAN_LOSS')

if __name__ == '__main__':
    unittest.main()
