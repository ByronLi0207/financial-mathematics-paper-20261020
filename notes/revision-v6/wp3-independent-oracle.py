#!/usr/bin/env python3
"""Independent synthetic WP3 review oracle; no financial/source archive I/O.

Run from any working directory. The only production imports are the pure
combination and pinball helpers. Expectations below use the elementary-score
formula and exact Fraction(19,20), without production event/path helpers.
"""
from fractions import Fraction
from itertools import product
import hashlib
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
from v6_combinations import combine_reports, murphy_exact
from v6_inference import pinball_losses

TAU = Fraction(19, 20)
SEED = 20261023


def elementary(reports, actual, theta):
    """Direct indicator definition, independent of production integer events."""
    return sum((int(y < x) - TAU) * (int(theta < x) - int(theta < y))
               for x, y in zip(reports, actual)) / len(actual)


def exact_pinball(reports, actual):
    """Direct rational .95/.05 loss in the original synthetic integer units."""
    return sum(TAU * max(y - x, 0) + (1 - TAU) * max(x - y, 0)
               for x, y in zip(reports, actual)) / len(actual)


def murphy_oracle():
    checks = 0
    for flat in product(range(3), repeat=6):
        left, right, actual = [list(flat[k:k + 2]) for k in (0, 2, 4)]
        result = murphy_exact(left, right, actual, tau=.95)
        # All these fixtures have literal integer breakpoints 0, 1, or 2.
        theta = [Fraction(int(value), 1) for value in result['theta']]
        assert theta == sorted(set(left + right + actual))
        exact_difference = []
        expected_denominator = 20 * len(actual)
        assert result['elementary_weight_denominator'] == expected_denominator
        for index, threshold in enumerate(theta):
            left_score = elementary(left, actual, threshold)
            right_score = elementary(right, actual, threshold)
            difference = left_score - right_score
            exact_difference.append(difference)
            assert difference * expected_denominator == int(result['integer_difference'][index])
            assert math.isclose(float(result['left'][index]), float(left_score),
                                rel_tol=1e-14, abs_tol=1e-14)
            assert math.isclose(float(result['right'][index]), float(right_score),
                                rel_tol=1e-14, abs_tol=1e-14)
            if index + 1 < len(theta):
                midpoint = (threshold + theta[index + 1]) / 2
                assert elementary(left, actual, midpoint) - elementary(right, actual, midpoint) == difference
        assert exact_difference[-1] == 0
        exact_loss_difference = exact_pinball(left, actual) - exact_pinball(right, actual)
        exact_integral = sum((upper - lower) * difference for lower, upper, difference in
                             zip(theta[:-1], theta[1:], exact_difference[:-1]))
        assert exact_integral == exact_loss_difference
        assert math.isclose(result['integral_difference'], float(exact_loss_difference),
                            rel_tol=1e-14, abs_tol=1e-14)
        assert math.isclose(result['pinball_difference'], float(exact_loss_difference),
                            rel_tol=1e-14, abs_tol=1e-14)
        positive = any(value > 0 for value in exact_difference)
        negative = any(value < 0 for value in exact_difference)
        expected = ('CROSSING' if positive and negative else
                    'LEFT_DOMINATES_SAMPLE' if negative else
                    'RIGHT_DOMINATES_SAMPLE' if positive else 'EQUAL_SAMPLE')
        assert result['ranking'] == expected
        checks += 1
    assert checks == 729
    return checks


def combination_oracle():
    rng = np.random.default_rng(SEED)
    for _ in range(100):
        floor = rng.uniform(0, 10, 40)
        frozen_f = floor + rng.uniform(0, 100, 40)
        qr = floor + rng.uniform(0, 100, 40)
        actual = floor + rng.uniform(0, 100, 40)
        result = combine_reports(np.arange(40), floor, frozen_f, qr, frozen_f)
        assert np.array_equal(result['MEDIAN_F_QR_KNN']['capacity'], frozen_f)
        assert result['MEDIAN_F_QR_KNN']['identity'] == 'EXACTLY_F'
        mean_report = result['MEAN_F_QR']['capacity']
        assert np.all(mean_report >= floor)
        mean_losses = pinball_losses(actual, mean_report, tau=.95)
        average_constituent_loss = (pinball_losses(actual, frozen_f, tau=.95)
                                    + pinball_losses(actual, qr, tau=.95)) / 2
        assert np.all(mean_losses <= average_constituent_loss + 1e-13)
    # The Jensen bound tested above is against average constituent loss. It is
    # deliberately not described as a bound against the best constituent.
    return 100


def main():
    print('scope: synthetic fixtures only; no financial NPZ or source data reads')
    print('tau: exact Fraction(19,20); elementary interval convention: [lower,upper)')
    print('seed:', SEED)
    print('python:', sys.version.split()[0])
    print('numpy:', np.__version__)
    for name in ('v6_combinations.py', 'v6_inference.py'):
        fingerprint = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        print('tested_code_sha256:', name, fingerprint)
    print('independent_fraction_murphy_exhaustive_cases:', murphy_oracle())
    print('independent_convexity_floor_and_knn_identity_cases:', combination_oracle())
    print('status: PASS')


if __name__ == '__main__':
    main()
