"""Artificial-path tests only; no financial file or accepted trace is read."""
import dataclasses
from fractions import Fraction
import importlib.util
import math
import unittest

import numpy as np

AVAILABLE = importlib.util.find_spec('ar1_replay') is not None
if AVAILABLE:
    import ar1_replay as ar


def pairwise_oracle(levels):
    """Exact represented-input oracle using pairwise, not centered, moments."""
    z = [Fraction.from_float(float(x)) for x in levels]
    x, y = z[:-1], z[1:]
    xx = sum((x[i]-x[j])**2 for i in range(len(x)) for j in range(i))
    xy = sum((x[i]-x[j])*(y[i]-y[j]) for i in range(len(x)) for j in range(i))
    slope = xy/xx
    return slope, sum(y)/len(y)-slope*sum(x)/len(x)


def recursive_report(history, query):
    """Independent residual extraction and scalar recursive path replay."""
    peaks = []
    phi, c = history.fit.phi, history.fit.c
    for row in history.paths:
        value = float(query)
        peak = abs(value)
        for before, after in zip(row[:-1], row[1:]):
            residual = float(after)-c-phi*float(before)
            value = c+phi*value+residual
            peak = max(peak, abs(value))
        peaks.append(peak)
    floor = abs(float(query))
    return floor+sorted(p-floor for p in peaks)[history.rank-1]


class ModuleContract(unittest.TestCase):
    def test_numerical_module_exists(self):
        self.assertTrue(AVAILABLE, 'AR1 numerical module is missing')


@unittest.skipUnless(AVAILABLE, 'AR1 implementation absent')
class FitTests(unittest.TestCase):
    def assert_error(self, code, values):
        with self.assertRaises(ar.AR1Error) as context:
            ar.fit_ar1(values)
        self.assertEqual(context.exception.code, code)
        self.assertEqual(str(context.exception), code)

    def test_intercept_slope_match_independent_pairwise_fraction_oracle(self):
        for levels in ([1., 2., 4., 3., 5.], [-3., 1., 0., 4., 2., -1.]):
            want_phi, want_c = pairwise_oracle(levels)
            fit = ar.fit_ar1(levels)
            self.assertAlmostEqual(fit.phi, float(want_phi), delta=2e-13)
            self.assertAlmostEqual(fit.c, float(want_c), delta=2e-13)
            self.assertEqual(fit.transition_count, len(levels)-1)
        fit = ar.fit_ar1([1., 2., 4., 3., 5.])
        self.assertAlmostEqual(fit.phi, .4, delta=1e-14)
        self.assertAlmostEqual(fit.c, 2.5, delta=1e-14)

    def test_high_offset_represented_spacing_does_not_disappear_in_centered_covariance(self):
        for changes, expected in (([0.,0.,1.,0.,1.,2.], Fraction(1,3)),
                                  ([0.,1.,0.,1.,1.,0.], Fraction(-2,3))):
            for offset in (0., 2.**52, -2.**52):
                for factor in (1., 2.**-400, 2.**400):
                    levels = [factor*(offset+x) for x in changes]
                    oracle_phi, oracle_c = pairwise_oracle(levels)
                    self.assertEqual(oracle_phi, expected)
                    fit = ar.fit_ar1(levels)
                    with self.subTest(changes=changes,offset=offset,factor=factor):
                        self.assertAlmostEqual(fit.phi,float(oracle_phi),delta=2e-15)
                        self.assertAlmostEqual(fit.c,float(oracle_c),
                            delta=max(8*math.ulp(float(oracle_c)),2e-13*factor))

    def test_binary_scale_is_finite_positive_at_smallest_subnormal(self):
        smallest = float(np.nextafter(0.,1.))
        fit = ar.fit_ar1([0.,smallest,2*smallest,3*smallest,4*smallest])
        self.assertEqual(fit.phi,1.)
        self.assertEqual(fit.c,smallest)
        self.assertGreater(fit.scale,0.)
        self.assertTrue(math.isfinite(fit.scale))

    def test_nonzero_intercept_phi_zero_and_exact_unit_are_not_degenerate(self):
        zero = ar.fit_ar1([10., 2., 2., 2., 2.])
        self.assertEqual((zero.phi, zero.c), (0., 2.))
        unit = ar.fit_ar1([0., 1., 2., 3., 4.])
        self.assertEqual((unit.phi, unit.c), (1., 1.))

    def test_negative_and_above_one_coefficients_are_not_clipped(self):
        for values, expected in (([1., -1., 1., -1., 1.], -1.),
                                 ([1., -.5, .25, -.125, .0625], -.5),
                                 ([1., 2., 4., 8., 16.], 2.),
                                 ([8., 4., 2., 1., .5], .5)):
            fit = ar.fit_ar1(values)
            self.assertAlmostEqual(fit.phi, expected, delta=2e-14)
            self.assertAlmostEqual(fit.c, 0., delta=2e-14)

    def test_common_scale_avoids_large_and_tiny_unscaled_variance_failures(self):
        maximum = float(np.finfo(np.float64).max)
        fit = ar.fit_ar1([-maximum, 0., maximum])
        self.assertEqual((fit.phi, fit.c, fit.scale), (1., maximum, 2.**1023))
        tiny = ar.fit_ar1(np.arange(5, dtype=float)*1e-200)
        self.assertAlmostEqual(tiny.phi, 1., delta=2e-14)
        self.assertAlmostEqual(tiny.c/1e-200, 1., delta=2e-14)

    def test_power_of_two_monetary_rescaling_preserves_slope_and_intercept_units(self):
        values = np.array([1., 2., 4., 3., 5.])
        base = ar.fit_ar1(values)
        for factor in (2.**-400, 2.**400):
            fit = ar.fit_ar1(factor*values)
            self.assertEqual(fit.phi, base.phi)
            self.assertAlmostEqual(fit.c/factor, base.c, delta=2e-14)

    def test_normal_equation_diagnostics_check_actual_fitted_coefficients(self):
        values = np.array([-3., 1., 0., 4., 2., -1.])
        fit = ar.fit_ar1(values)
        u, v = values[:-1]/fit.scale, values[1:]/fit.scale
        residual = v-fit.phi*u-fit.c/fit.scale
        self.assertAlmostEqual(fit.scaled_mean_residual,
            abs(math.fsum(map(float, residual))/len(u)), delta=1e-16)
        self.assertAlmostEqual(fit.scaled_regressor_residual,
            abs(math.fsum(float(a)*float(b) for a,b in zip(u,residual))/len(u)), delta=1e-16)
        bound = 1e-10*max(1., float(np.mean(np.abs(v))),
            float(np.mean(np.abs(fit.phi*u))), abs(fit.c/fit.scale))
        self.assertAlmostEqual(fit.normal_tolerance, bound, delta=1e-24)
        self.assertLessEqual(fit.scaled_mean_residual, fit.normal_tolerance)
        self.assertLessEqual(fit.scaled_regressor_residual, fit.normal_tolerance)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            fit.phi = 1.

    def test_constant_original_regressor_is_nonidentified_even_if_last_response_changes(self):
        for values in ([0., 0., 1.], [2., 2., 2., 2.]):
            self.assert_error('AR1_CONSTANT_REGRESSOR', values)

    def test_lost_scaled_dispersion_fails_without_different_scale(self):
        self.assert_error('AR1_DISPERSION_LOST', [1e-100, 2e-100, 3e-100, 1e100])
        self.assert_error('AR1_DISPERSION_LOST', [0., 0., 0., 3e-162, 1.])

    def test_unrepresentable_intercept_fails_without_coefficient_clipping(self):
        self.assert_error('AR1_NONFINITE_FIT', [1e308, np.nextafter(1e308, 0.), -1e308])

    def test_invalid_shape_type_length_and_nonfinite_are_fixed_code_errors(self):
        for values in ([], [1.], [1., 2.], [[1.,2.,3.]], ['1','2','3'], [True,False,True]):
            self.assert_error('AR1_INVALID_LEVELS', values)
        for value in (math.inf, -math.inf, math.nan):
            self.assert_error('AR1_NONFINITE_LEVELS', [1., value, 3., 4.])


@unittest.skipUnless(AVAILABLE, 'AR1 implementation absent')
class HistoryPredictionTests(unittest.TestCase):
    def ramp(self):
        return ar.prepare_ar1_history(np.arange(60, dtype=float),32,2,19)

    def test_preparation_uses_unique_mature_union_and_immutable_copies(self):
        source = np.arange(60, dtype=float)
        history = ar.prepare_ar1_history(source,32,2,19)
        self.assertEqual((history.first_origin,history.last_origin,history.refit), (12,30,32))
        self.assertEqual((len(history.levels),history.paths.shape,history.fit.transition_count), (21,(19,3),20))
        np.testing.assert_array_equal(history.paths[0], [12.,13.,14.])
        np.testing.assert_array_equal(history.paths[-1], [30.,31.,32.])
        before = ar.predict(history,.1)
        source[:33] = -1000.
        self.assertEqual(ar.predict(history,.1), before)
        for array in (history.levels,history.paths,history.lower_increment,history.upper_increment):
            with self.assertRaises(ValueError):
                array.flags.writeable = True

    def test_future_perturbations_do_not_enter_refit_and_query_does_not_reestimate(self):
        source = np.arange(60, dtype=float)
        first = ar.prepare_ar1_history(source,32,2,19)
        source[33:] = math.nan
        second = ar.prepare_ar1_history(source,32,2,19)
        self.assertEqual(first.fit, second.fit)
        np.testing.assert_array_equal(first.paths, second.paths)
        self.assertNotEqual(ar.predict(first, .1), ar.predict(first, 10.))
        self.assertEqual(first.fit, second.fit)

    def test_exact_unit_propagation_matches_real_frozen_s_arithmetic_bitwise(self):
        import study_core as core
        from conditional_study import issue_historical
        for query in (-1e16, -.3, 0., .1, np.nextafter(1.,2.), 1e16):
            source = np.arange(60,dtype=float);source[33] = query
            history = ar.prepare_ar1_history(source,32,2,19)
            self.assertEqual(history.fit.phi, 1.)
            cache = core.build_label_cache(source,2)
            want = issue_historical(source,cache,issue=33,refit=32,window=19,step=2)[1]
            self.assertEqual(np.float64(ar.predict(history,query)).tobytes(),np.float64(want).tobytes())

    def test_replay_matches_independent_scalar_residual_recursion(self):
        source = np.array([math.sin(i*.7)+i*.02 for i in range(80)])
        history = ar.prepare_ar1_history(source,60,6,40)
        self.assertNotEqual(history.fit.phi, 1.)
        for query in (-2., .125, 3.):
            self.assertAlmostEqual(ar.predict(history,query),recursive_report(history,query),delta=2e-12)

    def test_negative_and_above_one_replay_and_floor_are_valid(self):
        for source in (np.array([(-1.)**i for i in range(24)]),2.**np.arange(24)):
            history = ar.prepare_ar1_history(source,23,4,20)
            self.assertTrue(history.fit.phi<0 or history.fit.phi>1)
            for query in (-3., .5, 4.):
                got=ar.predict(history,query)
                self.assertGreaterEqual(got,abs(query))
                self.assertAlmostEqual(got,recursive_report(history,query),delta=2e-8)

    def test_near_one_is_not_rounded_to_unit_propagation(self):
        source = (1.-2.**-20)**np.arange(64)
        history = ar.prepare_ar1_history(source,50,24,20)
        self.assertNotEqual(history.fit.phi, 1.)
        raw = np.maximum(-1.+history.upper_increment,1.-history.lower_increment)
        legacy_s = 1.+sorted(raw-1.)[history.rank-1]
        self.assertLess(ar.predict(history,-1.),legacy_s)

    def test_phi_zero_replaces_old_anchor_and_is_not_native_k(self):
        source = np.array([10.]+[2.]*19)
        history = ar.prepare_ar1_history(source,19,1,19)
        self.assertEqual((history.fit.phi,history.fit.c), (0.,2.))
        self.assertEqual(ar.predict(history,1.), 2.)
        self.assertEqual(max(1., sorted(np.max(np.abs(history.paths),axis=1))[history.rank-1]),10.)

    def test_duplicate_scenarios_corrected_rank_and_issue_floor(self):
        history = ar.prepare_ar1_history(np.array([1.,-1.]*10),19,1,19)
        self.assertEqual(history.rank,19)
        self.assertEqual(ar.predict(history,0.),0.)
        self.assertEqual(ar.predict(history,3.),3.)

    def test_finite_power_underflow_is_allowed_but_overflow_is_failure(self):
        history = self.ramp()
        tiny = dataclasses.replace(history,fit=dataclasses.replace(history.fit,phi=1e-200))
        self.assertTrue(math.isfinite(ar.predict(tiny,1.)))
        huge = dataclasses.replace(history,fit=dataclasses.replace(history.fit,phi=1e200))
        with self.assertRaises(ar.AR1Error) as context:
            ar.predict(huge,1.)
        self.assertEqual(context.exception.code,'AR1_NONFINITE_REPLAY')

    def test_query_errors_and_replay_overflow_do_not_fallback(self):
        history = self.ramp()
        for query in (True, [], [1.], math.inf, math.nan, '1', 10**1000):
            with self.assertRaises(ar.AR1Error) as context:
                ar.predict(history,query)
            self.assertEqual(context.exception.code,'AR1_INVALID_QUERY')
        huge=dataclasses.replace(history,fit=dataclasses.replace(history.fit,phi=-2.))
        with self.assertRaises(ar.AR1Error) as context:
            ar.predict(huge,-float(np.finfo(float).max))
        self.assertEqual(context.exception.code,'AR1_NONFINITE_REPLAY')

    def test_invalid_indices_incomplete_history_and_unavailable_rank(self):
        source=np.arange(60,dtype=float)
        for r,h,w in ((True,2,19),(32,0,19),(32,25,19),(32,2,2881),(32.0,2,19)):
            with self.assertRaises(ar.AR1Error) as context:
                ar.prepare_ar1_history(source,r,h,w)
            self.assertEqual(context.exception.code,'AR1_INVALID_INDEX')
        for r,h,w in ((4,2,19),(60,2,19)):
            with self.assertRaises(ar.AR1Error) as context:
                ar.prepare_ar1_history(source,r,h,w)
            self.assertEqual(context.exception.code,'AR1_INCOMPLETE_HISTORY')
        with self.assertRaises(ar.AR1Error) as context:
            ar.prepare_ar1_history(source,32,2,18)
        self.assertEqual(context.exception.code,'AR1_UNAVAILABLE_RANK')

    def test_largest_declared_pool_is_bounded_and_one_query_at_a_time(self):
        source=np.sin(np.arange(3000)*.031)+.001*np.arange(3000)
        history=ar.prepare_ar1_history(source,2999,24,2880)
        self.assertEqual(history.paths.shape,(2880,25))
        self.assertEqual(history.paths.nbytes,576000)
        self.assertTrue(math.isfinite(ar.predict(history,.3)))


if __name__ == '__main__':
    unittest.main()
