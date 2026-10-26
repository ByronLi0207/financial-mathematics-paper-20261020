"""Synthetic-only identities, causal clocks and exact WP5 tail-screen fixtures."""
from fractions import Fraction
import importlib
import importlib.util
import json
import unittest
from unittest.mock import patch

import numpy as np

import conditional_study as original
from conditional_quantile import QuantileFitError
import v6_inference as inference


class TauTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("v6_tau"), "generic tau engine is not implemented")
        self.api = importlib.import_module("v6_tau")

    @staticmethod
    def source(n=190):
        i = np.arange(n)
        return 20*np.sin(i*.23)+i*.1, np.datetime64("2019-01-02")+i*np.timedelta64(7,"D")

    @staticmethod
    def config(**overrides):
        options = dict(horizon=6, window=40, refit_step=7, short_scale=3,
                       long_scale=26, nominal_gap_seconds=604800)
        options.update(overrides)
        return original.StudyConfig(**options)

    def test_point_ninety_five_reproduces_all_original_qr_outputs_exactly(self):
        # Catches feature omission, changed pools/scales/refits, tolerances or tau drift.
        x, times = self.source()
        ids = np.arange(100, 111)
        expected = original.conditional_forecast(x, times, ids, self.config(), "QR", .1)
        got = self.api.forecast_qr_tau(x, times, ids, self.config(), .1, tau=.95)
        for field in ("origins", "capacities", "floors", "refit_indices"):
            np.testing.assert_array_equal(getattr(got, field), getattr(expected, field))
        self.assertEqual(got.fit_diagnostics, expected.fit_diagnostics)
        self.assertEqual((got.family, got.parameter), ("QR", .1))
        self.assertFalse(got.capacities.flags.writeable)
        self.assertEqual([row["training_first_origin"] for row in got.fit_diagnostics], [55, 62])
        self.assertEqual([row["latest_label_end"] for row in got.fit_diagnostics], [100, 107])

    def test_generic_solver_receives_all_thirty_three_features_and_new_tau(self):
        # Wrap the real solver to inspect this module's numerical boundary.
        x, times = self.source()
        calls = []
        real = self.api.fit_quantile_ridge
        def capture(design, response, **kwargs):
            calls.append((design.copy(), response.copy(), kwargs.copy()))
            return real(design, response, **kwargs)
        with patch.object(self.api, "fit_quantile_ridge", side_effect=capture):
            fit = self.api.forecast_qr_tau(x, times, np.arange(100, 104), self.config(), .1, tau=.9)
        self.assertEqual(calls[0][0].shape, (40, 34))
        np.testing.assert_array_equal(calls[0][0][:, 0], np.ones(40))
        self.assertEqual(calls[0][2]["tau"], .9)
        self.assertEqual((fit.fit_diagnostics[0]["training_first_origin"],
                          fit.fit_diagnostics[0]["training_last_origin"]), (55, 94))
        self.assertEqual(set(calls[0][2]), {"tau", "penalty", "checkpoint"})

    def test_new_tau_changes_fitted_reports_and_explicit_scores_and_hit_null(self):
        # Catches a generic wrapper that silently fits at .95 for every requested level.
        x, times = self.source()
        low = self.api.forecast_qr_tau(x, times, np.arange(100, 111), self.config(), .1, tau=.9)
        high = self.api.forecast_qr_tau(x, times, np.arange(100, 111), self.config(), .1, tau=.99)
        self.assertTrue(np.any(low.capacities != high.capacities))
        np.testing.assert_array_equal(inference.pinball_losses([3., 1.], [1., 3.], tau=.9), [1.8, .2])
        np.testing.assert_array_equal(inference.pinball_losses([3., 1.], [1., 3.], tau=.99), [1.98, .02])
        self.assertEqual(inference.coverage_diagnostics([0, 1], tau=.9, origins=[0, 1], horizon=1)["null_probability"], .1)
        self.assertEqual(inference.coverage_diagnostics([0, 1], tau=.99, origins=[0, 1], horizon=1)["null_probability"], .01)

    def test_future_positions_and_dates_cannot_change_earlier_issued_reports(self):
        # Catches unfinished labels or future feature normalization entering a fit.
        x, times = self.source()
        changed = x.copy(); changed[111:] = 1e5 + np.arange(len(x)-111)
        changed_times = times.copy(); changed_times[111:] += np.timedelta64(9, "D")
        ids = np.arange(100, 111)
        for tau in (.9, .99):
            with self.subTest(tau=tau):
                before = self.api.forecast_qr_tau(x, times, ids, self.config(), .1, tau=tau)
                after = self.api.forecast_qr_tau(changed, changed_times, ids, self.config(), .1, tau=tau)
                np.testing.assert_array_equal(before.capacities, after.capacities)
                self.assertEqual(before.fit_diagnostics, after.fit_diagnostics)
        for rolling in (False, True):
            np.testing.assert_array_equal(
                self.api.historical_f_tau(x, ids, self.config(), tau=.9, rolling=rolling),
                self.api.historical_f_tau(changed, ids, self.config(), tau=.9, rolling=rolling))

    def test_original_historical_f_is_exact_at_point_ninety_five(self):
        x, _ = self.source(); ids = np.arange(100, 111); cfg = self.config()
        old = original.historical_forecasts(x, ids, cfg)
        for rolling, name in [(False, "frozen_F"), (True, "rolling_F")]:
            got = self.api.historical_f_tau(x, ids, cfg, tau=.95, rolling=rolling)
            np.testing.assert_array_equal(got, old[name])
            self.assertFalse(got.flags.writeable)

    def test_historical_new_tau_ranks_pools_and_actual_issue_floor_match_literal_oracle(self):
        # Independent path maxima and literal ranks: W99 -> ranks90 and99.
        x = np.array([((i*7) % 19)-8. for i in range(220)])
        ids = np.arange(150, 160); cfg = self.config(horizon=3, window=99, refit_step=4)
        for tau, rank in [(.9, 90), (.99, 99)]:
            for rolling in (False, True):
                expected = []
                for t in ids:
                    r = int(t) if rolling else 150+4*((int(t)-150)//4)
                    responses = [max(abs(float(v)) for v in x[i:i+4])-abs(float(x[i]))
                                 for i in range(r-101, r-2)]
                    self.assertEqual(len(responses), 99)
                    expected.append(abs(float(x[t]))+sorted(responses)[rank-1])
                got = self.api.historical_f_tau(x, ids, cfg, tau=tau, rolling=rolling)
                np.testing.assert_array_equal(got, expected)

    def test_exact_tail_counts_and_corrected_ranks_for_original_windows(self):
        for tau, ranks, fractions in [(.9, [649, 2593, 235], ["72", "288", "26"]),
                                     (.99, [714, 2853, 259], ["36/5", "144/5", "13/5"])]:
            z = self.api.tail_admission([720, 2880, 260], 1440, tau=tau)
            self.assertEqual([r["rank"] for r in z["window_rows"]], ranks)
            self.assertEqual([r["nominal_tail_fraction"] for r in z["window_rows"]], fractions)
            self.assertEqual(z["tail_probability_fraction"], "1/10" if tau == .9 else "1/100")
            json.dumps(z, allow_nan=False)
        fx = self.api.tail_admission([2880, 720], 1440, tau=.99)
        treasury = self.api.tail_admission([260], 52, tau=.99)
        self.assertEqual(fx["status"], "ELIGIBLE")
        self.assertEqual(treasury["status"], "INELIGIBLE")
        self.assertEqual(treasury["validation_tail_fraction"], "13/25")
        self.assertEqual(treasury["reason"], "INSUFFICIENT_NOMINAL_TAIL")
        self.assertEqual(self.api.tail_admission([260], 52, tau=.9)["status"], "ELIGIBLE")

    def test_tail_information_threshold_is_inclusive_and_rank_must_exist(self):
        # Catches epsilon comparisons around the exact >=5 screen.
        for tau, boundary in [(.9, 50), (.99, 500)]:
            self.assertTrue(self.api.tail_admission([boundary], boundary, tau=tau)["eligible"])
            self.assertFalse(self.api.tail_admission([boundary-1], boundary, tau=tau)["eligible"])
            self.assertFalse(self.api.tail_admission([boundary], boundary-1, tau=tau)["eligible"])
        unavailable = self.api.tail_admission([98], 1000, tau=.99)
        self.assertEqual(unavailable["window_rows"][0]["rank"], 99)
        self.assertFalse(unavailable["window_rows"][0]["rank_available"])
        self.assertIn("UNAVAILABLE_HISTORICAL_RANK", unavailable["reasons"])
        x, _ = self.source()
        with self.assertRaises(ValueError):
            self.api.historical_f_tau(x, np.arange(150, 155), self.config(), tau=.99)

    def test_checkpoint_failure_propagates_without_forecast_fallback(self):
        class Cancel(RuntimeError): pass
        def stop(**_kwargs): raise Cancel("synthetic guard stop")
        x, times = self.source()
        with self.assertRaises(Cancel):
            self.api.forecast_qr_tau(x, times, np.arange(100, 111), self.config(), .1,
                                     tau=.9, checkpoint=stop)
        with self.assertRaises(Cancel):
            self.api.historical_f_tau(x, np.arange(100, 111), self.config(), tau=.9, checkpoint=stop)

    def test_later_qr_nonconvergence_is_terminal_with_original_private_failure_context(self):
        real = self.api.fit_quantile_ridge; count = 0
        def fail_second(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 2: raise QuantileFitError("NONCONVERGENCE", {"iterations": 10000})
            return real(*args, **kwargs)
        x, times = self.source()
        with patch.object(self.api, "fit_quantile_ridge", side_effect=fail_second):
            with self.assertRaises(QuantileFitError) as caught:
                self.api.forecast_qr_tau(x, times, np.arange(100, 111), self.config(), .1, tau=.9)
        error = caught.exception
        self.assertEqual((error.failure_context["refit_index"], error.failure_context["issued_origin_count"]), (107, 7))
        np.testing.assert_array_equal(error.partial_forecast.origins, np.arange(100, 107))
        self.assertEqual(len(error.partial_forecast.fit_diagnostics), 1)

    def test_invalid_tau_parameter_and_incomplete_origin_vectors_fail(self):
        x, times = self.source(); cfg = self.config()
        calls = [lambda: self.api.forecast_qr_tau(x, times, [100, 102], cfg, .1, tau=.9),
                 lambda: self.api.forecast_qr_tau(x, times, np.arange(100, 105), cfg, 0., tau=.9),
                 lambda: self.api.forecast_qr_tau(x, times, np.arange(100, 105), cfg, .1, tau=True),
                 lambda: self.api.historical_f_tau(x, [100, 102], cfg, tau=.9),
                 lambda: self.api.tail_admission([], 52, tau=.9),
                 lambda: self.api.tail_admission([260], 0, tau=.9),
                 lambda: self.api.tail_admission([260], 52, tau=1.),
                 lambda: self.api.tail_admission([260], 52, tau=.9, minimum_expected=0)]
        for call in calls:
            with self.assertRaises(ValueError): call()


if __name__ == "__main__": unittest.main(verbosity=2)
