"""Synthetic tests for the fixed ordinary/corrected headroom-rank ablation.

No test reads a financial file or calls the financial runner. Fraction losses
and scalar window maxima supply oracles distinct from the vector issuer.
"""
from fractions import Fraction
import importlib.util
import math
import unittest

import numpy as np


SPEC = importlib.util.find_spec('empirical_headroom')
if SPEC is not None:
    import empirical_headroom as empirical
else:
    empirical = None


def exact_loss(labels, report):
    """Exact rational .95 pinball sum, independent of production rank helpers."""
    return sum((Fraction(19, 20) * max(Fraction(y) - report, 0)
                + Fraction(1, 20) * max(report - Fraction(y), 0)
                for y in labels), Fraction(0))


class EmpiricalHeadroomTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(empirical, 'source-independent rank issuer is missing')

    def test_exact_ranks_preserve_both_integral_minimizer_endpoints(self):
        # Changing to a single ordinary rank would lose the corrected endpoint.
        for window, want in ((20, (19, 20)), (52, (50, 51)),
                             (260, (247, 248)), (720, (684, 685)),
                             (2880, (2736, 2737))):
            with self.subTest(window=window):
                self.assertEqual(empirical.ranks(window), want)
        labels = list(range(20))
        lo, hi = (Fraction(18), Fraction(19))
        best = exact_loss(labels, lo)
        self.assertEqual(exact_loss(labels, hi), best)
        self.assertEqual(exact_loss(labels, (lo + hi) / 2), best)
        self.assertGreater(exact_loss(labels, lo - Fraction(1, 2)), best)
        self.assertGreater(exact_loss(labels, hi + Fraction(1, 2)), best)

    def test_nonintegral_w52_has_unique_distinct_response_minimizer(self):
        # Applying the add-one rank as an ordinary ERM fails for distinct W52.
        labels = list(range(52))
        ordinary, corrected = empirical.ranks(52)
        best = exact_loss(labels, Fraction(labels[ordinary - 1]))
        self.assertGreater(exact_loss(labels, Fraction(labels[corrected - 1])), best)
        self.assertGreater(exact_loss(labels, Fraction(97, 2)), best)
        self.assertGreater(exact_loss(labels, Fraction(99, 2)), best)

    def test_issue_floor_and_duplicate_labels_are_preserved(self):
        # Dropping duplicates or excluding current B changes this constant case.
        result = empirical.predict([-7.] * 28, [23, 24, 25, 26, 27], 3, 20, 4)
        np.testing.assert_array_equal(result['I'], [7.] * 5)
        np.testing.assert_array_equal(result['F'], [7.] * 5)
        np.testing.assert_array_equal(result['floors'], [7.] * 5)
        self.assertEqual(exact_loss([0] * 52, Fraction(0)), 0)
        self.assertGreater(exact_loss([0] * 52, Fraction(1)), 0)

    def test_frozen_pool_matures_at_refit_and_query_floor_updates(self):
        # Rolling at each issue, delaying H by one, or forgetting current B fails.
        positions = np.arange(35, dtype=float)
        result = empirical.predict(positions, [25, 26, 27, 28, 29], 3, 20, 4)
        np.testing.assert_array_equal(result['refit_indices'], [25, 25, 25, 25, 29])
        np.testing.assert_array_equal(result['training_first_origins'], [3, 3, 3, 3, 7])
        np.testing.assert_array_equal(result['training_last_origins'], [22, 22, 22, 22, 26])
        np.testing.assert_array_equal(result['latest_label_ends'], [25, 25, 25, 25, 29])
        np.testing.assert_array_equal(result['I'], [28., 29., 30., 31., 32.])
        np.testing.assert_array_equal(result['F'], [28., 29., 30., 31., 32.])

    def test_direct_scalar_oracle_distinguishes_rank_reports(self):
        # Swapping ranks, using peaks as headrooms or a wrong H window fails.
        positions = np.asarray([(-1 if j % 2 else 1) * j * j
                                for j in range(110)], float)
        origins = list(range(59, 79))
        result = empirical.predict(positions, origins, 4, 52, 7)
        want_i, want_f = [], []
        for t in origins:
            r = 59 + ((t - 59) // 7) * 7
            labels = []
            for i in range(r - 4 - 52 + 1, r - 4 + 1):
                peak = max(abs(float(positions[j])) for j in range(i, i + 5))
                labels.append(peak - abs(float(positions[i])))
            ordered = sorted(labels)
            want_i.append(abs(float(positions[t])) + ordered[49])
            want_f.append(abs(float(positions[t])) + ordered[50])
        np.testing.assert_array_equal(result['I'], want_i)
        np.testing.assert_array_equal(result['F'], want_f)
        self.assertTrue(np.any(result['I'] != result['F']))

    def test_future_perturbation_and_unresolved_outcomes_do_not_change_issue(self):
        # Reading future labels, future scaling or requiring future P fails.
        positions = np.asarray([((j * 11) % 47) - 23 for j in range(92)], float)
        base = empirical.predict(positions, [66], 6, 52, 13)
        changed = positions.copy()
        changed[67:] = 1.e100
        altered = empirical.predict(changed, [66], 6, 52, 13)
        prefix = empirical.predict(positions[:67], [66], 6, 52, 13)
        for key in base:
            np.testing.assert_array_equal(base[key], altered[key])
            np.testing.assert_array_equal(base[key], prefix[key])

    def test_outputs_do_not_alias_inputs_and_are_readonly(self):
        # Returning writable buffers can silently alter a retained forecast.
        origins = np.arange(25, 30)
        positions = np.arange(31, dtype=float)
        result = empirical.predict(positions, origins, 3, 20, 4)
        origins[:] = 0
        positions[:] = 0
        np.testing.assert_array_equal(result['origins'], [25, 26, 27, 28, 29])
        np.testing.assert_array_equal(result['I'], [28., 29., 30., 31., 32.])
        for values in result.values():
            self.assertFalse(values.flags.writeable)

    def test_rejects_invalid_configuration_and_indices(self):
        # Coercing booleans/floats, gaps or unsigned overflow can hide bad clocks.
        for window in (0, -1, True, 20., '20'):
            with self.subTest(window=window), self.assertRaises(ValueError):
                empirical.ranks(window)
        cases = [([], 3, 20, 4), ([24, 26], 3, 20, 4), ([25, 25], 3, 20, 4),
                 ([25.], 3, 20, 4), ([True], 3, 20, 4), ([40], 3, 20, 4),
                 ([-1], 3, 20, 4), ([18], 3, 20, 4), ([25], 0, 20, 4),
                 ([25], 3, 18, 4), ([25], 3, 20, 0), ([25], True, 20, 4),
                 ([25], 3, 20, 1.5), ([2**63], 3, 20, 4)]
        for ids, horizon, window, step in cases:
            with self.subTest(case=(ids, horizon, window, step)), self.assertRaises(ValueError):
                empirical.predict(np.arange(40.), ids, horizon, window, step)

    def test_rejects_nonfinite_bad_shape_and_capacity_overflow(self):
        # Silent nonfinite propagation must stop the whole segment.
        for bad in (math.nan, math.inf, -math.inf):
            positions = np.arange(30.)
            positions[10] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                empirical.predict(positions, [25], 3, 20, 4)
        for positions in ([], [[1.] * 30], np.arange(30.) + 1.j):
            with self.subTest(shape=str(type(positions))), self.assertRaises(ValueError):
                empirical.predict(positions, [25], 3, 20, 4)
        huge = np.asarray([0., 1.e308] * 14)
        with self.assertRaises(ValueError):
            empirical.predict(huge, [25], 1, 20, 4)


if __name__ == '__main__':
    unittest.main()
