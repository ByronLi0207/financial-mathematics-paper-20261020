"""Synthetic, hand-valued oracles for the exploratory selected-row issuer."""

from dataclasses import FrozenInstanceError, replace
import unittest

import numpy as np

import study_core as core

try:
    import revision_selection as selection_core
except ModuleNotFoundError as exc:
    if exc.name != "revision_selection":
        raise
    selection_core = None


class SelectedForecastOracles(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(selection_core, "selected-row issuer is absent")

    def fixture(self, values=(0, 1, 4, 2, 3, 0, 9), *, t=5,
                horizon=1, window=4, numerator=1, denominator=2, rank=3):
        position = np.asarray(values, dtype=np.float64)
        cell = core.CellSpec("synthetic", horizon, window, numerator, denominator, rank)
        cache = core.build_label_cache(position, horizon)
        labels = core.mature_window(cache, t, cell)
        anchors = position[labels.origins].copy()
        return position, cell, labels, anchors

    def issue(self, selection, count, **kwargs):
        position, cell, labels, anchors = self.fixture(**kwargs)
        t = kwargs.get("t", 5)
        issued = selection_core.issue_selected(
            t, float(position[t]), labels, anchors, cell, selection, count
        )
        return issued

    def test_nearest2_uses_signed_anchors_and_paired_responses(self):
        # Rows 1,3: anchors 1,2; G=3,1; S-headrooms=3,1; peaks=4,3.
        issued = self.issue("nearest", 2)
        np.testing.assert_array_equal(issued.origins, [1, 3])
        np.testing.assert_array_equal(issued.capacities, [3., 3., 4.])
        self.assertEqual(issued.rank, 2)
        self.assertEqual(issued.absolute_radius, 2.)
        self.assertEqual(issued.signed_radius, 2.)
        self.assertEqual(issued.mean_age_records, 3.)
        self.assertEqual(issued.refined_bound, 2.)
        self.assertEqual(issued.arithmetic_tolerance, 256 * np.finfo(np.float64).eps)
        self.assertEqual(issued.geometry_excess, 0.)

    def test_recent2_keeps_chronological_paired_rows(self):
        # Rows 3,4: G=1,0; S-headrooms=1,3; peaks=3,3; k=2.
        issued = self.issue("recent", 2)
        np.testing.assert_array_equal(issued.origins, [3, 4])
        np.testing.assert_array_equal(issued.capacities, [1., 3., 3.])
        self.assertEqual(issued.mean_age_records, 1.5)
        self.assertEqual(issued.refined_bound, 3.)

    def test_full4_retains_duplicate_order_statistics(self):
        # G sorted=0,0,1,3; S sorted=1,2,3,3; P sorted=3,3,4,4; k=3.
        issued = self.issue("full", 4)
        np.testing.assert_array_equal(issued.origins, [1, 2, 3, 4])
        np.testing.assert_array_equal(issued.capacities, [1., 3., 4.])
        self.assertEqual(issued.rank, 3)
        self.assertEqual(issued.absolute_radius, 4.)
        self.assertEqual(issued.signed_radius, 4.)
        self.assertEqual(issued.mean_age_records, 2.5)

    def test_output_is_immutable_and_has_builtin_scalars(self):
        issued = self.issue("nearest", 2)
        self.assertIsInstance(issued, selection_core.SelectedForecast)
        self.assertEqual(issued.capacities.dtype, np.dtype(np.float64))
        self.assertEqual(issued.origins.dtype, np.dtype(np.int64))
        with self.assertRaises(FrozenInstanceError):
            issued.rank = 1
        with self.assertRaises(ValueError):
            issued.capacities[0] = 0.
        with self.assertRaises(ValueError):
            issued.origins[0] = 0
        self.assertIs(type(issued.rank), int)
        for name in ("absolute_radius", "signed_radius", "mean_age_records",
                     "refined_bound", "arithmetic_tolerance", "geometry_excess"):
            self.assertIs(type(getattr(issued, name)), float)

    def test_equal_distance_cutoff_prefers_most_recent_origins(self):
        # Distances at origins 2,3,4 all equal 1; take 3,4, then sort in time.
        issued = self.issue("nearest", 2, values=[0, 5, 1, -1, 1, 0, 9])
        np.testing.assert_array_equal(issued.origins, [3, 4])
        np.testing.assert_array_equal(issued.capacities, [0., 2., 1.])

    def test_unsigned_origin_zero_cannot_win_a_recency_tie(self):
        position, cell, labels, anchors = self.fixture(values=np.ones(5), t=4)
        labels = replace(labels, origins=labels.origins.astype(np.uint64))
        issued = selection_core.issue_selected(4, position[4], labels, anchors, cell, "nearest", 2)
        np.testing.assert_array_equal(issued.origins, [2, 3])

    def test_malformed_pool_or_cell_is_rejected_as_invalid_input(self):
        _, cell, labels, anchors = self.fixture()
        for bad_labels, bad_cell in ((None, cell), (labels, None)):
            with self.subTest(labels=bad_labels, cell=bad_cell), self.assertRaises(ValueError):
                selection_core.issue_selected(5, 0., bad_labels, anchors, bad_cell, "nearest", 2)

    def test_issuance_does_not_mutate_full_pool_or_anchor_inputs(self):
        position, cell, labels, anchors = self.fixture()
        names = ("origins", "peak", "headroom", "lower_increment", "upper_increment",
                 "radius", "label_end")
        snapshots = {name: getattr(labels, name).copy() for name in names}
        anchor_before = anchors.copy()
        for selection, count in (("nearest", 2), ("recent", 2), ("full", 4)):
            selection_core.issue_selected(5, position[5], labels, anchors, cell, selection, count)
        np.testing.assert_array_equal(anchors, anchor_before)
        for name, before in snapshots.items():
            np.testing.assert_array_equal(getattr(labels, name), before)
            self.assertFalse(getattr(labels, name).flags.writeable)

    def test_nearest_uses_signed_distance_rather_than_magnitude_distance(self):
        # At current 2, signed distances are 4,3,1,4; magnitude distances 0,3,1,4.
        issued = self.issue("nearest", 2, values=[0, -2, 5, 3, 6, 2, 9])
        np.testing.assert_array_equal(issued.origins, [2, 3])
        np.testing.assert_array_equal(issued.capacities, [5., 5., 6.])

    def test_selection_membership_does_not_use_candidate_responses(self):
        # Only record 5 differs. It is outside the anchor vector at H=2,t=6.
        common = dict(t=6, horizon=2)
        low = self.issue("nearest", 2, values=[0, 1, 4, 2, 3, 0, 0, 9], **common)
        high = self.issue("nearest", 2, values=[0, 1, 4, 2, 3, 20, 0, 9], **common)
        np.testing.assert_array_equal(low.origins, [1, 3])
        np.testing.assert_array_equal(high.origins, [1, 3])
        self.assertNotEqual(low.capacities.tolist(), high.capacities.tolist())

    def test_full_requires_the_entire_eligible_count(self):
        with self.assertRaises(ValueError):
            self.issue("full", 2)

    def test_bad_counts_are_rejected_before_array_slicing(self):
        for count in (-1, 0, 5, True, np.bool_(False), 2., np.array(2)):
            with self.subTest(count=count), self.assertRaises(ValueError):
                self.issue("recent", count)

    def test_unknown_selection_is_rejected(self):
        for selection in ("Nearest", "", None):
            with self.subTest(selection=selection), self.assertRaises(ValueError):
                self.issue(selection, 2)

    def test_exact_selected_rank_must_be_available(self):
        with self.assertRaises(ValueError):
            self.issue("recent", 2, values=np.zeros(22), t=20,
                       window=20, numerator=19, denominator=20, rank=20)

    def test_frozen_fractional_ranks_are_exact_for_every_configured_count(self):
        for horizon in (6, 24):
            for selection, count, want in (("full", 720, 685), ("recent", 360, 343),
                                            ("nearest", 360, 343), ("recent", 180, 172),
                                            ("nearest", 180, 172)):
                with self.subTest(horizon=horizon, selection=selection, count=count):
                    issued = self.issue(selection, count, values=np.zeros(720+horizon),
                                        t=719+horizon, horizon=horizon, window=720,
                                        numerator=19, denominator=20, rank=685)
                    self.assertEqual(issued.rank, want)
                    np.testing.assert_array_equal(issued.capacities, [0., 0., 0.])

    def test_nonfinite_and_malformed_anchor_vectors_are_rejected(self):
        position, cell, labels, anchors = self.fixture()
        bad = ([1., np.nan, 2., 3.], [1., np.inf, 2., 3.],
               [1., -np.inf, 2., 3.], [1., 4., 2.], [1., 4., 2., 3., 0.],
               [[1., 4., 2., 3.]], 0., ["bad"])
        for value in bad:
            with self.subTest(anchors=value), self.assertRaises(ValueError):
                selection_core.issue_selected(5, position[5], labels, value, cell, "recent", 2)

    def test_exact_anchor_headroom_alignment_is_checked_on_unselected_rows(self):
        position, cell, labels, anchors = self.fixture()
        for bad in (anchors[::-1], np.array([1., np.nextafter(4., 0.), 2., 3.])):
            with self.subTest(anchors=bad.tolist()), self.assertRaises(ValueError):
                selection_core.issue_selected(5, position[5], labels, bad, cell, "nearest", 2)

    def test_full_pool_maturity_is_validated_before_nearest_selection(self):
        position, cell, labels, anchors = self.fixture()
        for bad in (replace(labels, label_end=labels.label_end+1),
                    replace(labels, label_end=np.array([2, 4, 4, 5])),
                    replace(labels, origins=labels.origins+1),
                    replace(labels, horizon=2), replace(labels, window=3)):
            with self.subTest(labels=bad), self.assertRaises(ValueError):
                selection_core.issue_selected(5, position[5], bad, anchors, cell, "nearest", 2)

    def test_actual_issue_index_is_independent_of_the_label_end(self):
        position, cell, labels, anchors = self.fixture()
        for t in (4, 6, True, 5.):
            with self.subTest(t=t), self.assertRaises(ValueError):
                selection_core.issue_selected(t, position[5], labels, anchors, cell, "nearest", 2)

    def test_full_pool_label_fields_are_validated_even_when_not_selected(self):
        position, cell, labels, anchors = self.fixture()
        changed = labels.headroom.copy()
        changed[1] = np.nan  # Origin 2 is excluded from nearest2.
        for bad in (replace(labels, headroom=changed),
                    replace(labels, peak=labels.peak[:-1]),
                    replace(labels, headroom=np.array([3., -1., 1., 0.]))):
            with self.subTest(labels=bad), self.assertRaises(ValueError):
                selection_core.issue_selected(5, position[5], bad, anchors, cell, "nearest", 2)

    def test_current_state_is_a_finite_scalar(self):
        _, cell, labels, anchors = self.fixture()
        for current in (np.nan, np.inf, -np.inf, [0.], [0., 0.]):
            with self.subTest(current=current), self.assertRaises(ValueError):
                selection_core.issue_selected(5, current, labels, anchors, cell, "nearest", 2)

    def test_material_geometry_violation_is_rejected(self):
        _, cell, labels, anchors = self.fixture()
        upper = labels.upper_increment.copy()
        radius = labels.radius.copy()
        upper[0] = 100.
        radius[0] = 100.
        bad = replace(labels, upper_increment=upper, radius=radius)
        with self.assertRaises(ValueError):
            selection_core.issue_selected(5, 0., bad, anchors, cell, "nearest", 2)

    def test_arithmetic_tolerance_never_collapses_exact_capacity_difference(self):
        _, cell, labels, anchors = self.fixture(values=[0., 0., 0., 0.],
                                               t=3, window=3, rank=2)
        eps = np.finfo(np.float64).eps
        tiny = np.full(3, eps)
        labels = replace(labels, upper_increment=tiny, radius=tiny)
        issued = selection_core.issue_selected(3, 0., labels, anchors, cell, "full", 3)
        np.testing.assert_array_equal(issued.capacities, [0., eps, 0.])
        self.assertNotEqual(issued.capacities[0], issued.capacities[1])
        self.assertEqual(issued.geometry_excess, eps)
        self.assertEqual(issued.arithmetic_tolerance, 64*eps)
        outcome = np.nextafter(eps, np.inf)
        self.assertGreater(outcome-issued.capacities[1], 0.)

    def test_full_count_matches_original_f_s_l_for_all_selection_modes(self):
        fixtures = (
            {},
            dict(values=[0, 1, -1, 2, 0], t=4, horizon=2, window=3, rank=2),
            dict(values=[0, -1, -2, float(2**53)], t=3, window=3, rank=2),
        )
        for kwargs in fixtures:
            position, cell, labels, anchors = self.fixture(**kwargs)
            t = kwargs.get("t", 5)
            original = core.issue_capacities(t, position[t], labels, labels.origins, cell)
            for selection in ("full", "recent", "nearest"):
                with self.subTest(fixture=kwargs, selection=selection):
                    issued = selection_core.issue_selected(t, position[t], labels, anchors,
                                                            cell, selection, cell.window)
                    np.testing.assert_array_equal(issued.origins, labels.origins)
                    np.testing.assert_array_equal(issued.capacities, original.capacities[[0, 1, 3]])

    def test_large_floor_preserves_stored_rounding_in_original_s_order(self):
        B = float(2**53)
        for selection in ("full", "recent", "nearest"):
            issued = self.issue(selection, 3, values=[0., -1., -2., B], t=3,
                                window=3, rank=2)
            np.testing.assert_array_equal(issued.capacities, [B, B, B])

    def test_global_sign_and_positive_scale_transform_the_same_selected_rows(self):
        path = np.array([0., -2., 5., 3., 6., 2., 9.])
        for selection, count in (("full", 4), ("recent", 2), ("nearest", 2)):
            with self.subTest(selection=selection):
                base = self.issue(selection, count, values=path)
                signed = self.issue(selection, count, values=-path)
                scaled = self.issue(selection, count, values=path*8.)
                np.testing.assert_array_equal(signed.origins, base.origins)
                np.testing.assert_array_equal(scaled.origins, base.origins)
                np.testing.assert_array_equal(signed.capacities, base.capacities)
                np.testing.assert_array_equal(scaled.capacities, base.capacities*8.)
                for name in ("absolute_radius", "signed_radius", "refined_bound", "arithmetic_tolerance"):
                    self.assertEqual(getattr(signed, name), getattr(base, name))
                    self.assertEqual(getattr(scaled, name), getattr(base, name)*8.)
                self.assertEqual(scaled.mean_age_records, base.mean_age_records)

    def test_future_suffix_and_prefix_cannot_change_an_issue(self):
        prefix = [0., 1., 4., 2., 3., 0.]
        for selection, count, capacities in (("full", 4, [1., 3., 4.]),
                                             ("recent", 2, [1., 3., 3.]),
                                             ("nearest", 2, [3., 3., 4.])):
            baseline = self.issue(selection, count, values=prefix)
            for suffix in ([0.], [100., -100., 1.e6]):
                with self.subTest(selection=selection, suffix=suffix):
                    changed = self.issue(selection, count, values=prefix+suffix)
                    np.testing.assert_array_equal(changed.origins, baseline.origins)
                    np.testing.assert_array_equal(changed.capacities, capacities)
                    for name in ("rank", "absolute_radius", "signed_radius", "mean_age_records",
                                 "refined_bound", "arithmetic_tolerance", "geometry_excess"):
                        self.assertEqual(getattr(changed, name), getattr(baseline, name))


if __name__ == "__main__":
    unittest.main()
