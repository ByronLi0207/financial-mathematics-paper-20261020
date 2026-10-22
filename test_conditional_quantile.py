"""Synthetic contracts for the direct ridge quantile solver; no financial data."""
import dataclasses
from fractions import Fraction
import importlib
import math
import unittest

import numpy as np


def objective(X, y, beta, tau, penalty):
    errors = y - X @ beta
    return float(np.mean(np.where(errors >= 0, tau * errors,
                                  (tau - 1) * errors))
                 + penalty * np.dot(beta[1:], beta[1:]) / 2)


def two_coordinate_oracle(X, y, tau, penalty):
    """Independent complete piecewise-quadratic search on active-residual lines.

    With an unpenalized intercept and n*tau nonintegral, at least one
    residual is zero at an optimum. Enumerate that observation, every
    slope breakpoint, and every quadratic stationary point between them.
    """
    x = X[:, 1]
    candidates = []
    for i in range(len(y)):
        dx, dy = x - x[i], y - y[i]
        breaks = sorted({float(dy[j] / dx[j]) for j in range(len(y))
                         if dx[j] != 0})
        slopes = list(breaks)
        boundaries = [-math.inf, *breaks, math.inf]
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            if math.isfinite(left) and math.isfinite(right):
                probe = (left + right) / 2
            elif math.isfinite(right):
                probe = right - 1
            else:
                probe = left + 1
            signs = np.where(dy - dx * probe >= 0, tau, tau - 1)
            stationary = float(np.mean(dx * signs) / penalty)
            if left <= stationary <= right:
                slopes.append(stationary)
        for slope in slopes:
            beta = np.array([y[i] - x[i] * slope, slope])
            candidates.append((objective(X, y, beta, tau, penalty), beta))
    return min(candidates, key=lambda item: item[0])


class ConditionalQuantileTests(unittest.TestCase):
    def solver(self):
        try:
            return importlib.import_module('conditional_quantile')
        except ModuleNotFoundError as exc:
            if exc.name == 'conditional_quantile':
                self.fail('The same-target quantile fitting feature is absent')
            raise

    def assert_certificate(self, fit, X, y, tau, penalty):
        self.assertLessEqual(fit.primal_residual, fit.primal_tolerance)
        self.assertLessEqual(fit.dual_residual, fit.dual_tolerance)
        self.assertGreaterEqual(fit.duality_gap, 0)
        self.assertLessEqual(fit.duality_gap, fit.gap_tolerance)
        nums = list(map(int, fit.dual_grid_numerators))
        denominator = fit.dual_grid_denominator
        self.assertEqual(sum(nums), 0)
        self.assertEqual(fit.dual_integer_sum, 0)
        exact_tau = Fraction.from_float(tau)
        for value in nums:
            rational = Fraction(value, denominator)
            self.assertGreaterEqual(rational, exact_tau - 1)
            self.assertLessEqual(rational, exact_tau)
        nu = fit.dual_weights
        np.testing.assert_array_equal(nu,
                                      fit.dual_grid_numerators / denominator)
        independently_computed = objective(X, y, fit.coefficients, tau, penalty)
        self.assertAlmostEqual(fit.primal_objective,
                               independently_computed, delta=1e-10)
        a = X[:, 1:].T @ nu / len(y)
        dual = float(np.mean(nu * y) - np.dot(a, a) / (2 * penalty))
        self.assertAlmostEqual(fit.dual_objective, dual, delta=1e-10)
        self.assertAlmostEqual(fit.primal_objective - dual,
                               fit.duality_gap, delta=1e-10)

    def test_intercept_only_targets_empirical_quantile_minimizer_set(self):
        cq = self.solver()
        y = np.arange(20, dtype=float)
        X = np.ones((20, 1))
        fit = cq.fit_quantile_ridge(X, y)
        self.assertGreaterEqual(fit.coefficients[0], 18 - 1e-4)
        self.assertLessEqual(fit.coefficients[0], 19 + 1e-4)
        self.assertAlmostEqual(fit.primal_objective, .475, delta=1e-6)
        self.assert_certificate(fit, X, y, .95, .01)

    def test_zero_headroom_and_constant_features_have_zero_solution(self):
        cq = self.solver()
        X = np.ones((24, 7))
        y = np.zeros(24)
        fit = cq.fit_quantile_ridge(X, y)
        np.testing.assert_allclose(fit.coefficients, 0, atol=1e-12)
        self.assertEqual(fit.primal_objective, 0)
        self.assertEqual(fit.duality_gap, 0)
        self.assert_certificate(fit, X, y, .95, .01)

    def test_unpenalized_intercept_is_not_shrunk_by_ridge(self):
        cq = self.solver()
        X = np.ones((12, 4))
        y = np.full(12, 7.0)
        fit = cq.fit_quantile_ridge(X, y, penalty=100)
        self.assertAlmostEqual(fit.coefficients[0], 7, delta=1e-8)
        np.testing.assert_allclose(fit.coefficients[1:], 0, atol=1e-8)

    def test_matches_independent_two_coordinate_piecewise_optimum(self):
        cq = self.solver()
        rng = np.random.default_rng(20261022)
        x = np.linspace(-2, 2, 11)
        X = np.column_stack([np.ones(len(x)), x])
        for tau, penalty in [(.95, .01), (.95, .1), (.37, .01), (.37, .1)]:
            with self.subTest(tau=tau, penalty=penalty):
                y = .8 + .7 * x + rng.normal(size=len(x))
                expected, _ = two_coordinate_oracle(X, y, tau, penalty)
                fit = cq.fit_quantile_ridge(X, y, tau=tau, penalty=penalty)
                self.assertGreaterEqual(fit.primal_objective, expected - 1e-10)
                self.assertLessEqual(fit.primal_objective - expected,
                                     3 * fit.gap_tolerance)
                self.assertLessEqual(fit.dual_objective, expected + 1e-10)
                self.assert_certificate(fit, X, y, tau, penalty)

    def test_duplicated_and_constant_predictors_remain_well_defined(self):
        cq = self.solver()
        x = np.linspace(-1, 1, 35)
        X = np.column_stack([np.ones(35), x, x, np.ones(35), np.zeros(35)])
        y = np.maximum(0, .5 + .2 * x + .1 * np.sin(4 * x))
        fit = cq.fit_quantile_ridge(X, y)
        self.assertTrue(np.isfinite(fit.coefficients).all())
        self.assertAlmostEqual(fit.coefficients[1], fit.coefficients[2], delta=1e-8)
        self.assertAlmostEqual(fit.coefficients[3], 0, delta=1e-7)
        self.assertEqual(fit.coefficients[4], 0)
        self.assert_certificate(fit, X, y, .95, .01)

    def test_response_rescaling_uses_corresponding_penalty_units(self):
        cq = self.solver()
        x = np.linspace(-2, 2, 13)
        X = np.column_stack([np.ones(13), x])
        y = 1 + .3 * x + .1 * np.cos(2 * x)
        first = cq.fit_quantile_ridge(X, y, tau=.63, penalty=.07)
        scaled = cq.fit_quantile_ridge(X, 7 * y, tau=.63, penalty=.07 / 7)
        np.testing.assert_allclose(scaled.coefficients,
                                   7 * first.coefficients, atol=2e-3, rtol=2e-3)
        self.assertAlmostEqual(scaled.primal_objective,
                               7 * first.primal_objective, delta=3e-5)

    def test_fits_are_frozen_and_backed_by_readonly_arrays(self):
        cq = self.solver()
        fit = cq.fit_quantile_ridge(np.ones((20, 1)), np.arange(20.))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            fit.iterations = 0
        for array in (fit.coefficients, fit.dual_weights,
                      fit.dual_grid_numerators):
            self.assertFalse(array.flags.writeable)
            with self.assertRaises(ValueError):
                array.flat[0] = 0
            with self.assertRaises(ValueError):
                array.setflags(write=True)

    def test_does_not_mutate_caller_training_arrays(self):
        cq = self.solver()
        X = np.column_stack([np.ones(17), np.arange(17.)])
        y = np.arange(17.) ** .5
        before_X, before_y = X.copy(), y.copy()
        cq.fit_quantile_ridge(X, y)
        np.testing.assert_array_equal(X, before_X)
        np.testing.assert_array_equal(y, before_y)

    def test_nonconvergence_raises_explicit_diagnostic_without_a_forecast(self):
        cq = self.solver()
        with self.assertRaises(cq.QuantileFitError) as context:
            cq.fit_quantile_ridge(np.ones((17, 1)), np.arange(17.),
                                  tau=.37, max_iter=1)
        self.assertEqual(context.exception.code, 'NONCONVERGENCE')
        self.assertEqual(context.exception.diagnostics['iterations'], 1)
        self.assertNotIn('coefficients', context.exception.diagnostics)

    def test_loose_residuals_do_not_bypass_the_objective_gap(self):
        cq = self.solver()
        x = np.linspace(-2, 2, 11)
        X = np.column_stack([np.ones(11), x])
        y = .7 + .4 * x + .3 * np.cos(3 * x)
        expected, _ = two_coordinate_oracle(X, y, .95, .01)
        fit = cq.fit_quantile_ridge(X, y, atol=100, rtol=100,
                                    gap_rtol=1e-8)
        self.assertGreater(fit.iterations, 1)
        self.assertLessEqual(fit.primal_objective - expected,
                             2 * fit.gap_tolerance)
        self.assert_certificate(fit, X, y, .95, .01)

    def test_nonfinite_arithmetic_fails_without_returning_coefficients(self):
        cq = self.solver()
        X = np.array([[1., 1e308], [1., -1e308]])
        with self.assertRaises(cq.QuantileFitError) as context:
            cq.fit_quantile_ridge(X, np.ones(2))
        self.assertNotIn('coefficients', context.exception.diagnostics)

    def test_shape_budget_rejects_oversized_fit(self):
        cq = self.solver()
        with self.assertRaises(cq.QuantileFitError):
            cq.fit_quantile_ridge(np.ones((10001, 1)), np.ones(10001))

    def test_rejects_invalid_data_shape_intercept_and_nonfinite_values(self):
        cq = self.solver()
        cases = [([], []), (np.ones(4), np.ones(4)),
                 (np.ones((0, 1)), np.ones(0)),
                 (np.ones((4, 0)), np.ones(4)),
                 (np.ones((4, 1)), np.ones(3)),
                 (np.ones((4, 1)), np.ones((4, 1))),
                 (np.zeros((4, 1)), np.ones(4)),
                 (np.array([[1., np.nan], [1., 0.]]), np.ones(2)),
                 (np.ones((2, 1)), np.array([1., np.inf])),
                 (np.ones((2, 1), dtype=complex), np.ones(2)),
                 (np.ones((2, 1)), np.array(['bad', 'data']))]
        for X, y in cases:
            with self.subTest(shape=np.shape(X), yshape=np.shape(y)):
                with self.assertRaises(cq.QuantileFitError):
                    cq.fit_quantile_ridge(X, y)

    def test_rejects_invalid_options(self):
        cq = self.solver()
        invalid = [dict(tau=0), dict(tau=1), dict(tau=np.nan),
                   dict(penalty=0), dict(penalty=-1), dict(penalty=np.inf),
                   dict(max_iter=0), dict(max_iter=1.5), dict(max_iter=True),
                   dict(atol=0), dict(rtol=-1), dict(gap_rtol=0),
                   dict(tau=np.array([.95])),
                   dict(checkpoint='not callable')]
        for kwargs in invalid:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(cq.QuantileFitError):
                    cq.fit_quantile_ridge(np.ones((4, 1)), np.arange(4.), **kwargs)

    def test_checkpoint_has_bounded_progress_and_can_abort(self):
        cq = self.solver()
        progress = []
        cq.fit_quantile_ridge(np.ones((17, 1)), np.arange(17.), tau=.37,
                              atol=1e-8, rtol=1e-8, checkpoint=progress.append)
        self.assertTrue(progress)
        for entry in progress:
            self.assertEqual(entry['iteration'] % 50, 0)
            self.assertEqual(entry['stage'], 'quantile_fit')
            self.assertTrue(all(not isinstance(v, (list, np.ndarray))
                                for v in entry.values()))
        class StopByCaller(Exception):
            pass
        def abort(_):
            raise StopByCaller()
        with self.assertRaises(StopByCaller):
            cq.fit_quantile_ridge(np.ones((17, 1)), np.arange(17.), tau=.37,
                                  atol=1e-8, rtol=1e-8, checkpoint=abort)

    def test_rich_feature_synthetic_case_has_an_accepted_certificate(self):
        cq = self.solver()
        rng = np.random.default_rng(20261022)
        z = rng.normal(size=(2880, 33))
        z = (z - z.mean(0)) / z.std(0)
        X = np.column_stack([np.ones(len(z)), z])
        y = np.maximum(0, .2 + .3 * z[:, 0]
                       + (.2 + .1 * np.abs(z[:, 1])) * rng.normal(size=len(z)))
        fit = cq.fit_quantile_ridge(X, y)
        self.assertEqual(fit.coefficients.shape, (34,))
        self.assert_certificate(fit, X, y, .95, .01)


if __name__ == '__main__':
    unittest.main()
