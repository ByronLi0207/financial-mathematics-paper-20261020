"""Synthetic-only checks of the frozen v8 DGP and peak oracle contract.

These fixtures never read or calibrate a financial source. Thresholds below
were chosen before the first implementation run and are not fitted to draws.
"""
import dataclasses
import importlib.util
import unittest

import numpy as np


if importlib.util.find_spec('v8_mc_dgp') is not None:
    import v8_mc_dgp as dgp
else:
    dgp = None


def fixture_seed(stream):
    return np.random.SeedSequence([20261024, 9, 0, 0, stream])


class DGPContractTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(dgp, 'v8_mc_dgp implementation is missing')

    def test_clock_extends_trading_week_into_burnin_and_skips_weekends(self):
        # Catches forgetting floor division for negative burn-in indices.
        times = dgp.clock('D1', np.array([-1, 0, 119, 120, 239, 240]))
        np.testing.assert_array_equal(times, np.array([
            '1999-12-31T23:00:00', '2000-01-03T00:00:00',
            '2000-01-07T23:00:00', '2000-01-10T00:00:00',
            '2000-01-14T23:00:00', '2000-01-17T00:00:00',
        ], dtype='datetime64[s]'))
        weekly = np.array(['1999-12-29', '2000-01-05', '2000-01-12'], dtype='datetime64[s]')
        for name in ('D0', 'D2'):
            np.testing.assert_array_equal(dgp.clock(name, np.array([-1, 0, 1])), weekly)

    def test_simulated_seed_stream_repeats_but_other_seed_changes_path(self):
        p = dgp.DGPParams('D0', c=.1, phi=.6, sigma=.8)
        a = dgp.simulate(p, 128, fixture_seed(1))
        b = dgp.simulate(p, 128, fixture_seed(1))
        c = dgp.simulate(p, 128, fixture_seed(2))
        for key in ('position', 'variance', 'residual', 'times'):
            np.testing.assert_array_equal(a[key], b[key])
        self.assertFalse(np.array_equal(a['position'], c['position']))
        np.testing.assert_array_equal(a['times'], dgp.clock('D0', np.arange(128)))

    def test_gaussian_calibration_omits_unused_garch_and_t_parameters(self):
        # The calibrator represents unused D0 GARCH parameters as zero/None.
        p = dgp.DGPParams('D0', c=0, phi=.5, omega=0, alpha=0, beta=0,
                          nu=None, sigma=.8)
        a = dgp.simulate(p, 20, fixture_seed(21))
        np.testing.assert_allclose(a['variance'], .64, rtol=0, atol=1e-15)
        self.assertTrue(np.isfinite(dgp.oracle_reports(p, a, [19], seed=fixture_seed(22))).all())

    def test_constant_variance_stationary_ar_moments(self):
        # Catches wrong innovation variance or dropping the AR intercept.
        p = dgp.DGPParams('D0', c=.2, phi=.65, sigma=.7)
        a = dgp.simulate(p, 120000, fixture_seed(3))
        self.assertAlmostEqual(a['position'].mean(), .2 / .35, delta=.06)
        self.assertAlmostEqual(a['position'].var(), .49 / (1 - .65**2), delta=.05)
        np.testing.assert_allclose(a['variance'], np.full(120000, .49), rtol=0, atol=1e-15)

    def test_student_t_innovations_are_standardized_to_unit_variance(self):
        # Raw t_5 has variance 5/3 and must fail this check.
        p = dgp.DGPParams('D2', c=0, phi=0, omega=1, alpha=0, beta=0, nu=5)
        a = dgp.simulate(p, 180000, fixture_seed(4))
        z = a['residual'] / np.sqrt(a['variance'])
        self.assertAlmostEqual(z.mean(), 0, delta=.02)
        self.assertAlmostEqual(z.var(), 1, delta=.045)

    def test_stationary_garch_unconditional_variance_and_ar_mean(self):
        # Catches wrong residual in the GARCH update or using sigma as variance.
        p = dgp.DGPParams('D2', c=.15, phi=.5, omega=.1, alpha=.1, beta=.8, nu=8)
        a = dgp.simulate(p, 180000, fixture_seed(5))
        self.assertAlmostEqual(a['variance'].mean(), 1, delta=.075)
        self.assertAlmostEqual(np.mean(a['residual']**2), 1, delta=.09)
        self.assertAlmostEqual(a['position'].mean(), .3, delta=.055)
        self.assertAlmostEqual(a['position'].var(), 1 / .75, delta=.13)

    def test_diurnal_rms_pattern_and_retained_clock_remain_aligned(self):
        # A burn-in phase shift of 16 hours swaps low/high-volatility hours.
        shape = tuple([1 / np.sqrt(2.5)] * 12 + [2 / np.sqrt(2.5)] * 12)
        p = dgp.DGPParams('D1', c=0, phi=0, omega=1, alpha=0, beta=0,
                          nu=10, shape=shape, burnin=10000)
        a = dgp.simulate(p, 120000, fixture_seed(6))
        hours = a['times'].astype('datetime64[h]').astype(np.int64) % 24
        rms = np.array([np.sqrt(np.mean(a['position'][hours == h]**2)) for h in range(24)])
        np.testing.assert_allclose(rms, shape, rtol=.07, atol=0)
        # residual means the latent unseasonalized u, not the multiplied shock.
        np.testing.assert_allclose(a['position'], a['residual'] * np.asarray(shape)[hours], rtol=0, atol=0)
        np.testing.assert_array_equal(a['times'], dgp.clock('D1', np.arange(120000)))

    def test_invalid_parameters_fail_without_stationarity_repair(self):
        for changes in ({'alpha': -.1}, {'alpha': .2, 'beta': .8}, {'omega': 0},
                        {'nu': 2}, {'phi': 1.1}, {'shape': (1.,) * 23},
                        {'shape': (0.,) * 24}, {'burnin': 1000001}, {'c': np.nan}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                dgp.DGPParams('D2', c=changes.get('c', 0), phi=changes.get('phi', .5),
                             **{k: v for k, v in changes.items() if k not in ('c', 'phi')})
        unit_root = dgp.DGPParams('D0', c=0, phi=1, sigma=1)
        with self.assertRaises(ValueError):
            dgp.simulate(unit_root, 20, fixture_seed(7))

    def test_clock_and_simulation_reject_invalid_shapes_and_counts(self):
        p = dgp.DGPParams('D0', c=0, phi=.5, sigma=1)
        for indices in ([1.5], [True]):
            with self.assertRaises(ValueError):
                dgp.clock('D1', indices)
        with self.assertRaises(ValueError):
            dgp.clock('other', [0])
        for n in (0, True, 2.5):
            with self.assertRaises(ValueError):
                dgp.simulate(p, n, fixture_seed(8))


class OracleContractTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(dgp, 'v8_mc_dgp implementation is missing')

    def state(self, name='D2', n=130, position=0., variance=1., residual=0.):
        return dict(position=np.full(n, position), variance=np.full(n, variance),
                    residual=np.full(n, residual), times=dgp.clock(name, np.arange(n)))

    def test_oracle_includes_current_floor_instead_of_only_endpoint(self):
        # Positive AR mean reversion puts every likely future level below 1000.
        p = dgp.DGPParams('D0', c=0, phi=0, sigma=.01)
        a = self.state('D0', position=1000.)
        out = dgp.oracle_reports(p, a, [0, 1], paths=2000, seed=fixture_seed(10))
        np.testing.assert_array_equal(out, [1000., 1000.])

    def test_oracle_uses_current_residual_and_variance_before_first_draw(self):
        p = dgp.DGPParams('D2', c=0, phi=0, omega=.1, alpha=.2, beta=.5, nu=8)
        low = self.state()
        shock = self.state(residual=20.)
        high = self.state(variance=200.)
        kwargs = dict(origins=[0], horizon=1, paths=2000, seed=fixture_seed(11))
        q0 = dgp.oracle_reports(p, low, **kwargs)[0]
        qshock = dgp.oracle_reports(p, shock, **kwargs)[0]
        qhigh = dgp.oracle_reports(p, high, **kwargs)[0]
        self.assertGreater(qshock, q0 * 5)
        self.assertGreater(qhigh, q0 * 5)
        # At H1, same draws imply exact scaling by known next variances.
        self.assertAlmostEqual(qshock / q0, np.sqrt(80.6 / .6), places=10)
        self.assertAlmostEqual(qhigh / q0, np.sqrt(100.1 / .6), places=10)

    def test_oracle_does_not_read_realized_future_and_accepts_prefix(self):
        p = dgp.DGPParams('D2', c=0, phi=.5, omega=.1, alpha=.1, beta=.8, nu=8)
        a = dgp.simulate(p, 130, fixture_seed(12))
        b = {k: v.copy() for k, v in a.items()}
        for name in ('position', 'variance', 'residual'):
            b[name][101:] = np.nan
        prefix = {k: v[:101] for k, v in a.items()}
        kwargs = dict(origins=[100], paths=2000, seed=fixture_seed(13))
        want = dgp.oracle_reports(p, a, **kwargs)
        np.testing.assert_array_equal(want, dgp.oracle_reports(p, b, **kwargs))
        np.testing.assert_array_equal(want, dgp.oracle_reports(p, prefix, **kwargs))

    def test_oracle_batch_size_preserves_draws_and_seed_identity(self):
        p = dgp.DGPParams('D2', c=0, phi=.4, omega=.1, alpha=.1, beta=.8, nu=8)
        a = dgp.simulate(p, 140, fixture_seed(14))
        kw = dict(origins=[100, 101, 119, 120], paths=2000, seed=fixture_seed(15))
        q1 = dgp.oracle_reports(p, a, batch_size=1, **kw)
        q4 = dgp.oracle_reports(p, a, batch_size=4, **kw)
        np.testing.assert_array_equal(q1, q4)
        other = dict(kw, seed=fixture_seed(16))
        self.assertFalse(np.array_equal(q1, dgp.oracle_reports(p, a, batch_size=4, **other)))

    def test_oracle_future_diurnal_hours_continue_across_weekend(self):
        # Friday 23 -> Monday 00: future multiplier is hour zero, not hour 23.
        shape = tuple([10.] + [1.] * 22 + [.1])
        p = dgp.DGPParams('D1', c=0, phi=0, omega=1, alpha=0, beta=0,
                          nu=8, shape=shape)
        base = dataclasses.replace(p, shape=(1.,) * 24)
        a = self.state('D1')
        kw = dict(origins=[119], horizon=1, paths=2000, seed=fixture_seed(17))
        actual = dgp.oracle_reports(p, a, **kw)[0]
        unshaped = dgp.oracle_reports(base, a, **kw)[0]
        self.assertAlmostEqual(actual / unshaped, 10, places=11)

    def test_nonstationary_positive_random_walk_oracle_agrees_with_long_F(self):
        # Explicit nonstationary boundary fixture, not the calibrated D0.
        from empirical_headroom import predict
        rng = np.random.default_rng(fixture_seed(18))
        x = 10000 + np.cumsum(rng.normal(size=60010))
        a = dict(position=x, variance=np.ones(len(x)), residual=np.zeros(len(x)),
                 times=dgp.clock('D0', np.arange(len(x))))
        p = dgp.DGPParams('D0', c=0, phi=1, sigma=1)
        origin = 60000
        empirical = predict(x, [origin], 6, 50000, 13)['F'][0] - x[origin]
        oracle = dgp.oracle_reports(p, a, [origin], horizon=6, paths=2000,
                                    seed=fixture_seed(19))[0] - x[origin]
        self.assertGreater(empirical, 0)
        self.assertLessEqual(abs(oracle / empirical - 1), .12)

    def test_oracle_rejects_bad_state_and_noninteger_controls(self):
        p = dgp.DGPParams('D2', c=0, phi=.5, omega=.1, alpha=.1, beta=.8, nu=8)
        a = self.state()
        for kwargs in ({'origins': []}, {'origins': [130]}, {'origins': [1.5]},
                       {'origins': [1], 'paths': 0}, {'origins': [1], 'horizon': True},
                       {'origins': [1], 'batch_size': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                dgp.oracle_reports(p, a, seed=fixture_seed(20), **kwargs)
        a['variance'][1] = -1
        with self.assertRaises(ValueError):
            dgp.oracle_reports(p, a, [1], seed=fixture_seed(20))


if __name__ == '__main__':
    unittest.main(verbosity=2)
