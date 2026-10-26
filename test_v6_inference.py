"""Synthetic, independently derived fixtures for the frozen v6 diagnostics.

No financial source/forecast arrays are read. Each fixture states the mutation
it catches; expected transition counts and likelihoods are not legacy outputs.
"""
import json
import math
import unittest

import numpy as np
from conditional_study import score_predictions

try:
    import v6_inference as inference
except ModuleNotFoundError as exc:
    if exc.name != "v6_inference":
        raise
    inference = None


class V6InferenceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(inference, "v6 inference features are not implemented")

    def test_explicit_tau_controls_pinball_weight_and_strict_hits(self):
        # Catches a hidden .95 scoring weight or >= rather than > hits.
        for tau, expected, mean in [(.9, [.1, 1.8, 0.], 1.9 / 3),
                                    (.99, [.01, 1.98, 0.], 1.99 / 3)]:
            with self.subTest(tau=tau):
                np.testing.assert_allclose(
                    inference.pinball_losses([1, 4, 2], [2, 2, 2], tau=tau),
                    expected, rtol=0, atol=1e-15)
                result = inference.summarize_scores(
                    [1, 4, 2], [2, 2, 2], tau=tau,
                    origins=[10, 11, 12], horizon=1)
                self.assertAlmostEqual(result["mean_loss"], mean)
                self.assertEqual((result["n"], result["full_hits"]), (3, 1))
                self.assertAlmostEqual(result["full_rate"], 1 / 3)
                self.assertAlmostEqual(result["coverage_distance"], abs(1 / 3 - (1 - tau)))
                json.dumps(result, allow_nan=False)

    def test_point_ninety_five_losses_are_exactly_source_native(self):
        # Catches 1-.95 rounding away from the frozen float(Fraction(1,20)).
        peak = np.array([.1, .3, 1.7, 10. / 3, 1000.123456789, 9.8765432101])
        capacity = np.array([.2, .2, 2.9, 17. / 7, 1001.987654321, 11.2345678901])
        original = score_predictions(peak, capacity, np.zeros(6), np.arange(6))
        np.testing.assert_array_equal(
            inference.pinball_losses(peak, capacity, tau=.95), original.pinball)
        summary = inference.summarize_scores(peak, capacity, tau=.95,
                                             origins=np.arange(6), horizon=1)
        self.assertEqual(summary["mean_loss"], math.fsum(map(float, original.pinball)) / 6)

    def test_decimal_tau_nulls_and_coverage_distances_are_nominal_exact(self):
        # Catches subtracting binary tau rather than interpreting its decimal level.
        for tau, alpha in [(.9, .1), (.95, .05), (.99, .01)]:
            with self.subTest(tau=tau):
                summary = inference.summarize_scores([1.] * 6, [1.] * 6,
                                                     tau=tau, origins=np.arange(6), horizon=1)
                self.assertEqual(summary["coverage"]["null_probability"], alpha)
                self.assertEqual(summary["coverage_distance"], alpha)

    def test_tau_point_nine_and_point_ninety_nine_set_hit_nulls(self):
        # Catches coverage nulls fixed at .05 while score tau changes.
        for tau, want_lr in [(.9, -12 * math.log(.9)),
                             (.99, -12 * math.log(.99))]:
            with self.subTest(tau=tau):
                result = inference.coverage_diagnostics(
                    [0] * 6, tau=tau, origins=list(range(6)), horizon=1)
                self.assertAlmostEqual(result["null_probability"], 1 - tau)
                self.assertAlmostEqual(result["full"]["uc_lr"], want_lr)
                self.assertAlmostEqual(result["full"]["uc_p"], math.erfc(math.sqrt(want_lr / 2)))

    def test_unrepresentable_interior_hit_null_is_rejected(self):
        # Catches alpha rounding to 1 and leaking Infinity into public JSON.
        with self.assertRaises(ValueError):
            inference.coverage_diagnostics([0, 1, 0, 1, 0, 1], tau=1e-20,
                                           origins=list(range(6)), horizon=1)

    def test_transition_cc_uses_literal_same_pair_likelihood_and_fixed_origin_grid(self):
        # Catches old full-sample UC + transition independence, or offset selection.
        result = inference.coverage_diagnostics(
            [0, 1, 0, 0, 1, 1, 0, 1, 1, 0], tau=.9,
            origins=list(range(100, 110)), horizon=1)
        self.assertEqual((result["full"]["n"], result["full"]["hits"]), (10, 5))
        grid = result["fixed_grid"]
        self.assertEqual((grid["n"], grid["hits"]), (5, 2))
        self.assertEqual(grid["origins"], {"start": 100, "step": 2, "expected_count": 5, "observed_count": 5})
        cc = grid["transition_cc"]
        self.assertEqual([cc[k] for k in ("n00", "n01", "n10", "n11")], [1, 2, 1, 0])
        self.assertEqual(cc["transition_n"], 4)
        self.assertEqual(cc["status"], "BOUNDARY_REFERENCE")
        self.assertEqual(cc["boundary_cell_count"], 1)
        # Saturated: row 0 has two successes in 3; row 1 has zero in 1.
        saturated_ll = 2 * math.log(2 / 3) + math.log(1 / 3)
        fixed_ll = 2 * math.log(.1) + 2 * math.log(.9)
        cc_lr = 2 * (saturated_ll - fixed_ll)
        self.assertAlmostEqual(cc["lr"], cc_lr)
        self.assertAlmostEqual(cc["p"], math.exp(-cc_lr / 2))
        grid_uc = 2 * (2 * math.log(.4) + 3 * math.log(.6)
                       - 2 * math.log(.1) - 3 * math.log(.9))
        self.assertAlmostEqual(grid["uc_lr"], grid_uc)
        # The legacy mixed-sample construction is intentionally a different number.
        transition_ind = 2 * (saturated_ll - 4 * math.log(.5))
        self.assertNotAlmostEqual(cc["lr"], grid_uc + transition_ind)
        self.assertEqual(result["na_count"], 0)
        json.dumps(result, allow_nan=False)

    def test_missing_transition_row_keeps_uc_but_marks_cc_na(self):
        # Catches reporting calibration success from an unidentified transition row.
        result = inference.coverage_diagnostics([0] * 8, tau=.9, origins=list(range(8)), horizon=1)
        self.assertEqual((result["full"]["n"], result["full"]["hits"]), (8, 0))
        self.assertIsNotNone(result["full"]["uc_p"])
        self.assertIsNotNone(result["fixed_grid"]["uc_p"])
        cc = result["fixed_grid"]["transition_cc"]
        self.assertEqual(cc["status"], "UNIDENTIFIED_TRANSITION_ROW")
        self.assertEqual(cc["absent_row_count"], 1)
        self.assertEqual([cc[k] for k in ("n00", "n01", "n10", "n11")], [3, 0, 0, 0])
        self.assertIsNone(cc["lr"])
        self.assertIsNone(cc["p"])
        self.assertEqual(result["na_count"], 1)
        self.assertGreaterEqual(result["boundary_count"], 1)

    def test_too_short_grid_preserves_its_full_sample_uc(self):
        # Catches disappearing denominators when the transition sample is empty.
        result = inference.coverage_diagnostics([1, 0], tau=.99, origins=[4, 5], horizon=6)
        grid = result["fixed_grid"]
        self.assertEqual((grid["n"], grid["hits"]), (1, 1))
        self.assertIsNotNone(grid["uc_p"])
        self.assertEqual(grid["transition_cc"]["status"], "TOO_SHORT")
        self.assertEqual(grid["transition_cc"]["transition_n"], 0)
        self.assertIsNone(grid["transition_cc"]["p"])

    def test_grid_gaps_are_not_silently_compressed_or_dropped(self):
        # Catches selecting every H+1-th row rather than actual origin arithmetic.
        result = inference.coverage_diagnostics(
            [0, 1, 1, 0, 1], tau=.9, origins=[10, 11, 13, 14, 16], horizon=1)
        grid = result["fixed_grid"]
        self.assertEqual((grid["n"], grid["hits"]), (3, 1))
        self.assertEqual(grid["origins"], {"start": 10, "step": 2, "expected_count": 4, "observed_count": 3})
        self.assertEqual(grid["missing_origin_count"], 1)
        self.assertEqual(grid["uc_status"], "MISSING_GRID_ORIGINS")
        self.assertIsNone(grid["uc_p"])
        self.assertEqual(grid["transition_cc"]["status"], "MISSING_GRID_ORIGINS")
        self.assertIsNone(grid["transition_cc"]["p"])
        self.assertIsNotNone(result["full"]["uc_p"])

    def test_nonfinite_scores_fail_whole_summary_without_row_deletion(self):
        # Catches scoring only the favorable finite rows.
        result = inference.summarize_scores(
            [1., float("nan"), 3.], [1., 2., 2.], tau=.9,
            origins=[10, 11, 12], horizon=1)
        self.assertEqual(result["status"], "NONFINITE_SCORES")
        self.assertEqual((result["n"], result["nonfinite_count"]), (3, 1))
        self.assertIsNone(result["mean_loss"])
        self.assertIsNone(result["full_hits"])
        self.assertIsNone(result["coverage"])
        json.dumps(result, allow_nan=False)

    def test_identical_scores_are_valid_but_dm_p_is_raw_na(self):
        # Catches turning identical-loss non-identification into p=1.
        summary = inference.summarize_scores([1.] * 6, [1.] * 6, tau=.9,
                                             origins=list(range(6)), horizon=1)
        self.assertEqual(summary["mean_loss"], 0.)
        self.assertEqual(summary["full_hits"], 0)
        comparison = inference.compare_losses([0.] * 6, [0.] * 6, horizon=1)
        self.assertEqual(comparison["status"], "IDENTICAL_LOSSES")
        self.assertIsNone(comparison["dm_p"])
        self.assertIsNone(comparison["hln_p"])
        adjusted = inference.fixed_slot_holm(["identity", "valid_one"], {"identity": comparison["dm_p"], "valid_one": 1.})
        self.assertIsNone(adjusted["slots"][0]["raw_p"])
        self.assertEqual(adjusted["slots"][0]["bookkeeping_p"], 1.)
        self.assertEqual(adjusted["slots"][1]["raw_p"], 1.)
        self.assertEqual(adjusted["slots"][1]["status"], "OK")

    def test_dm_hln_preserves_original_bandwidth_known_answer_and_direction(self):
        # n=4,H=2 gives original bandwidth 2, LRV=17/12, mean=2.5.
        result = inference.compare_losses([11., 12., 13., 14.], [10.] * 4, horizon=2)
        self.assertEqual((result["n"], result["horizon"], result["bandwidth"]), (4, 2, 2))
        self.assertEqual(result["direction"], "new_minus_control")
        self.assertAlmostEqual(result["mean_difference"], 2.5)
        self.assertAlmostEqual(result["lrv"], 17 / 12)
        self.assertAlmostEqual(result["dm_t"], 4.20084025208403)
        self.assertAlmostEqual(result["hln_p"], .08231560255047188)
        reverse = inference.compare_losses([10.] * 4, [11., 12., 13., 14.], horizon=2)
        self.assertAlmostEqual(reverse["dm_t"], -result["dm_t"])
        self.assertAlmostEqual(reverse["hln_p"], result["hln_p"])

    def test_dm_nonfinite_short_and_zero_variance_keep_na_status(self):
        # Catches deleting missing pairs or manufacturing a p for degenerate loss.
        for left, right, horizon, status in [
                ([1., float("nan"), 3.], [1., 2., 3.], 1, "NONFINITE_LOSSES"),
                ([1., 2.], [0., 0.], 2, "TOO_SHORT"),
                ([2.] * 4, [1.] * 4, 1, "ZERO_LONG_RUN_VARIANCE"),
                ([], [], 1, "EMPTY_SAMPLE")]:
            with self.subTest(status=status):
                result = inference.compare_losses(left, right, horizon=horizon)
                self.assertEqual(result["n"], len(left))
                self.assertEqual(result["status"], status)
                self.assertIsNone(result["dm_p"])
                self.assertIsNone(result["hln_p"])
                json.dumps(result, allow_nan=False)

    def test_fixed_inventory_holm_retains_every_frozen_family_slot(self):
        # Catches shrinking the divisor to successful comparisons after failure.
        for family_n in [56, 224, 4, 6]:
            slots = [f"slot_{i}" for i in range(family_n)]
            result = inference.fixed_slot_holm(slots, {"slot_0": .0001, "slot_1": None})
            self.assertEqual(result["family_n"], family_n)
            self.assertEqual([row["slot_id"] for row in result["slots"]], slots)
            self.assertAlmostEqual(result["slots"][0]["holm_p"], family_n * .0001)
            self.assertIsNone(result["slots"][1]["raw_p"])
            self.assertEqual(result["slots"][1]["status"], "RAW_P_NA")
            self.assertEqual(result["slots"][2]["status"], "MISSING_RAW_P")
            self.assertEqual(result["slots"][2]["bookkeeping_p"], 1.)
            self.assertEqual(result["raw_na_count"], family_n - 1)
            json.dumps(result, allow_nan=False)

    def test_holm_known_order_and_nonfinite_na_are_distinct_from_raw_one(self):
        # Catches unstable reconstruction of input slot order and NaN serialization.
        slots = ["a", "b", "c", "d", "nan", "one"]
        result = inference.fixed_slot_holm(slots, dict(a=.01, b=.04, c=.03, d=.002, nan=float("nan"), one=1.))
        np.testing.assert_allclose([row["holm_p"] for row in result["slots"]], [.05, .12, .12, .012, 1., 1.], rtol=0, atol=1e-15)
        self.assertIsNone(result["slots"][4]["raw_p"])
        self.assertEqual(result["slots"][4]["status"], "RAW_P_NONFINITE")
        self.assertEqual(result["slots"][5]["raw_p"], 1.)
        self.assertEqual(result["slots"][5]["status"], "OK")
        json.dumps(result, allow_nan=False)

    def test_invalid_contract_inputs_fail_explicitly(self):
        # Catches silent alignment repair, duplicate slots and invalid nulls.
        calls = [
            lambda: inference.pinball_losses([1], [1], tau=.0),
            lambda: inference.pinball_losses([1], [1], tau=1.),
            lambda: inference.pinball_losses([1], [1, 2], tau=.9),
            lambda: inference.coverage_diagnostics([0, 2], tau=.9, origins=[1, 2], horizon=1),
            lambda: inference.coverage_diagnostics([0, 1], tau=.9, origins=[2, 1], horizon=1),
            lambda: inference.coverage_diagnostics([0, 1], tau=.9, origins=[1, 1], horizon=1),
            lambda: inference.coverage_diagnostics([0, 1], tau=.9, origins=[1., 2.5], horizon=1),
            lambda: inference.coverage_diagnostics([0, 1], tau=.9, origins=[1, 2], horizon=0),
            lambda: inference.compare_losses([1], [1, 2], horizon=1),
            lambda: inference.fixed_slot_holm([], {}),
            lambda: inference.fixed_slot_holm(["a", "a"], {}),
            lambda: inference.fixed_slot_holm(["a"], {"b": .1}),
            lambda: inference.fixed_slot_holm(["a"], {"a": -.1}),
            lambda: inference.fixed_slot_holm(["a"], {"a": 1.1}),
        ]
        for call in calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main(verbosity=2)
