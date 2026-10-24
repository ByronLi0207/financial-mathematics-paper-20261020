"""Calibration contracts using synthetic prefixes only; no real data is opened."""
from __future__ import annotations

import importlib
import json
import unittest
from unittest.mock import patch

import numpy as np

from conditional_sources import SourceSeries

try:
    CAL = importlib.import_module("v8_mc_calibrate")
except ModuleNotFoundError as exc:
    if exc.name != "v8_mc_calibrate":
        raise
    CAL = None


def fixture(position, hourly=False):
    values = np.asarray(position, dtype=float)
    unit = np.timedelta64(1, "h") if hourly else np.timedelta64(7, "D")
    dates = np.datetime64("2000-01-03T00", "us") + np.arange(len(values)) * unit
    return SourceSeries("fx_hourly" if hourly else "nyfed_weekly", dates,
                        values, "0" * 64, 100, {"units": "invented"})


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(CAL, "v8 calibration implementation is missing")

    def test_ar_constraint_reestimates_intercept_instead_of_retaining_ols_intercept(self):
        fit = CAL.fit_ar1(np.array([1., 2., 4., 8., 16.]))
        self.assertAlmostEqual(fit["unconstrained_phi"], 2.)
        self.assertAlmostEqual(fit["phi"], .995)
        self.assertAlmostEqual(fit["c"], 3.76875)
        self.assertTrue(fit["constraint_binds"])
        self.assertAlmostEqual(float(np.mean(fit["residuals"])), 0.)

    def test_future_values_do_not_change_d0_scale_or_parameters(self):
        rng = np.random.default_rng(np.random.SeedSequence([20261024, 9, 0, 0, 0]))
        prefix = 6. + rng.normal(size=80)
        one = fixture(np.r_[prefix, np.arange(10.)])
        two = fixture(np.r_[prefix, np.full(10, 1e90)])
        first = CAL.calibrate_source(one, dgp="D0", prefix_stop=80)
        second = CAL.calibrate_source(two, dgp="D0", prefix_stop=80)
        self.assertEqual(first["status"], "COMPLETE")
        self.assertEqual(first["parameters"], second["parameters"])
        self.assertEqual(first["source_scale"], second["source_scale"])
        self.assertAlmostEqual(first["source_scale"], float(np.std(prefix, ddof=0)))
        self.assertGreater(first["parameters"]["c"], 1.)
        self.assertEqual(first["prefix_count"], 80)
        self.assertEqual(first["last_prefix_date"], str(one.dates[79]))
        self.assertEqual(first["parameters"]["burnin"], 10000)

    def test_hour_shape_recovers_known_rms_and_observation_weighting(self):
        hours = np.tile(np.arange(24), 4)
        residuals = np.tile(np.arange(1., 25.), 4) * np.repeat([1., -1., 1., -1.], 24)
        shape, counts = CAL.diurnal_shape(residuals, hours)
        self.assertAlmostEqual(shape[0], 1. / np.sqrt(4900. / 24.))
        self.assertAlmostEqual(shape[23] / shape[0], 24.)
        self.assertAlmostEqual(float(np.average(shape**2, weights=counts)), 1.)
        # Extra observations at hour zero change its normalization weight.
        shape2, counts2 = CAL.diurnal_shape(np.r_[residuals, 1., -1.], np.r_[hours, 0, 0])
        self.assertAlmostEqual(float(np.average(shape2**2, weights=counts2)), 1.)
        self.assertNotEqual(float(shape[0]), float(shape2[0]))

    def test_missing_or_zero_hour_rms_fails_without_shape_repair(self):
        for residuals, hours in [(np.ones(23), np.arange(23)),
                                 (np.r_[0., np.ones(23)], np.arange(24))]:
            with self.subTest(hours=len(hours)):
                with self.assertRaises(CAL.CalibrationError):
                    CAL.diurnal_shape(residuals, hours)

    def test_d0_degenerate_prefix_fails_instead_of_inventing_scale(self):
        result = CAL.calibrate_source(fixture(np.ones(80)), dgp="D0", prefix_stop=80)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["reason"], "NONPOSITIVE_SOURCE_SCALE")
        self.assertNotIn("parameters", result)

    def test_garch_failure_is_terminal_and_not_retried(self):
        source = fixture(np.random.default_rng(51).normal(size=100))
        with patch.object(CAL, "fit_garch", side_effect=CAL.CalibrationError("GARCH_NONCONVERGENCE")) as fit:
            result = CAL.calibrate_source(source, dgp="D2", prefix_stop=80)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["reason"], "GARCH_NONCONVERGENCE")
        self.assertEqual(fit.call_count, 1)
        self.assertNotIn("parameters", result)

    def test_nonfinite_fit_failure_still_has_strict_json_archive(self):
        source = fixture(np.random.default_rng(81).normal(size=100))
        failure = CAL.CalibrationError("GARCH_NONFINITE", {"omega": float("nan"), "fit_attempts": 1})
        with patch.object(CAL, "fit_garch", side_effect=failure):
            result = CAL.calibrate_source(source, dgp="D2", prefix_stop=80)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["reason"], "GARCH_NONFINITE")
        try:
            json.dumps(result, allow_nan=False)
        except ValueError:
            self.fail("terminal nonfinite calibration cannot be archived as strict JSON")

    def test_invalid_garch_parameters_and_excessive_burnin_fail(self):
        good = {"omega": .1, "alpha": .1, "beta": .8, "nu": 8.}
        for overrides in [{"omega": 0.}, {"alpha": -.1}, {"beta": -.1},
                          {"alpha": .2, "beta": .8}, {"nu": 2.},
                          {"nu": float("nan")}, {"beta": .89999999}]:
            with self.subTest(overrides=overrides):
                with self.assertRaises(CAL.CalibrationError):
                    CAL.garch_burnin(.5, good | overrides)

    def test_real_arch_fit_of_fixed_synthetic_garch_is_finite_stationary(self):
        rng = np.random.default_rng(np.random.SeedSequence([20261024, 9, 2, 0, 0]))
        z = rng.standard_t(8., size=6000) * np.sqrt(6. / 8.)
        u = np.empty(6000)
        variance = 1.
        previous = 0.
        for i in range(len(u)):
            variance = .08 + .1 * previous**2 + .82 * variance
            u[i] = np.sqrt(variance) * z[i]
            previous = u[i]
        fit = CAL.fit_garch(u[1000:])
        self.assertEqual(fit["convergence_flag"], 0)
        self.assertGreater(fit["omega"], 0.)
        self.assertGreater(fit["nu"], 2.)
        self.assertLess(fit["alpha"] + fit["beta"], 1.)
        self.assertGreaterEqual(CAL.garch_burnin(.5, fit), 10000)

    def test_prefix_boundaries_are_checked_and_results_are_json_safe(self):
        source = fixture(np.random.default_rng(71).normal(size=80))
        for stop in [0, 2, 81]:
            self.assertEqual(CAL.calibrate_source(source, dgp="D0", prefix_stop=stop)["status"], "FAILED")
        result = CAL.calibrate_source(source, dgp="D0", prefix_stop=60)
        json.dumps(result, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
