"""Exact, synthetic checks independent of the paper's financial inputs."""

from fractions import Fraction as F
import itertools
import unittest

import preference_frontier as pf


class PreferenceFrontierTests(unittest.TestCase):
    def components(self, u, v):
        return pf.LossComponents.from_tokens(u, v)

    def test_decimal_tokens_are_exact(self):
        for token, expected in [("0.1", F(1, 10)), (" 1.25e-2 ", F(1, 80)),
                                ("+.5", F(1, 2)), ("-0", F(0)), (2, F(2)),
                                (F(2, 7), F(2, 7))]:
            with self.subTest(token=token):
                self.assertEqual(pf.parse_nonnegative_decimal(token), expected)

    def test_bad_tokens_rejected(self):
        for token in [True, False, None, 0.1, float("nan"), float("inf"),
                      "NaN", "Infinity", "-0.1", "1/2", "", "1_000", "one"]:
            with self.subTest(token=token):
                with self.assertRaises((TypeError, ValueError)):
                    pf.parse_nonnegative_decimal(token)

    def test_records_validate_components(self):
        with self.assertRaises(ValueError):
            self.components("-1", "0")
        with self.assertRaises(TypeError):
            pf.LossComponents(True, F(0))

    def test_fixed_alpha_and_endpoints(self):
        record = self.components("1.2", "0.3")
        self.assertEqual(pf.mean_loss(record, F(19, 20)), F(231, 200))
        self.assertEqual(pf.mean_loss(record, 0), F(3, 10))
        self.assertEqual(pf.mean_loss(record, 1), F(6, 5))

    def test_alpha_outside_unit_interval_or_inexact_rejected(self):
        for alpha in [F(-1, 10), F(11, 10), .95, True, "0.95"]:
            with self.subTest(alpha=alpha):
                with self.assertRaises((TypeError, ValueError)):
                    pf.mean_loss(self.components(0, 1), alpha)

    def test_global_dominance(self):
        result = pf.compare_records(self.components(1, 2), self.components(2, 3))
        self.assertEqual(result.relation, "left_dominates")
        self.assertIsNone(result.equality_alpha)
        reverse = pf.compare_records(self.components(2, 3), self.components(1, 2))
        self.assertEqual(reverse.relation, "right_dominates")

    def test_identical_lines_tie_for_every_alpha(self):
        result = pf.compare_records(self.components(1, 2), self.components(1, 2))
        self.assertEqual(result.relation, "identical")
        self.assertIsNone(result.equality_alpha)
        frontier = pf.lower_envelope({"B": self.components(1, 2),
                                      "A": self.components(1, 2)})
        self.assertEqual(frontier.regions, (pf.Region(F(0), F(1), ("A", "B")),))
        self.assertEqual(frontier.points, (pf.Point(F(0), ("A", "B")),
                                           pf.Point(F(1), ("A", "B"))))

    def test_positive_crossing_is_exact(self):
        result = pf.compare_records(self.components(1, 4), self.components(3, 1))
        self.assertEqual(result.relation, "crosses")
        self.assertEqual(result.equality_alpha, F(3, 5))
        self.assertEqual(pf.mean_loss(self.components(1, 4), F(3, 5)), F(11, 5))

    def test_dominance_can_have_an_endpoint_tie(self):
        for left, right, alpha in [((1, 2), (3, 2), F(0)),
                                   ((1, 2), (1, 4), F(1))]:
            result = pf.compare_records(self.components(*left), self.components(*right))
            self.assertEqual(result.relation, "left_dominates")
            self.assertEqual(result.equality_alpha, alpha)

    def test_parallel_unequal_lines_have_no_equality(self):
        result = pf.compare_records(self.components(2, 1), self.components(3, 2))
        self.assertEqual(result.relation, "left_dominates")
        self.assertIsNone(result.equality_alpha)

    def test_three_line_envelope_has_middle_segment(self):
        frontier = pf.lower_envelope({"A": self.components(4, 0),
                                      "B": self.components(1, 1),
                                      "C": self.components(0, 4)})
        self.assertEqual(frontier.regions,
                         (pf.Region(F(0), F(1, 4), ("A",)),
                          pf.Region(F(1, 4), F(3, 4), ("B",)),
                          pf.Region(F(3, 4), F(1), ("C",))))
        self.assertEqual(frontier.points,
                         (pf.Point(F(0), ("A",)), pf.Point(F(1, 4), ("A", "B")),
                          pf.Point(F(3, 4), ("B", "C")), pf.Point(F(1), ("C",))))

    def test_pareto_undominated_method_can_never_be_optimal(self):
        frontier = pf.lower_envelope({"A": self.components(4, 0),
                                      "B": self.components(3, 3),
                                      "C": self.components(0, 4)})
        self.assertEqual(frontier.regions,
                         (pf.Region(F(0), F(1, 2), ("A",)),
                          pf.Region(F(1, 2), F(1), ("C",))))
        self.assertEqual(frontier.points[1], pf.Point(F(1, 2), ("A", "C")))
        self.assertTrue(all("B" not in point.methods for point in frontier.points))

    def test_tie_only_method_retained_at_interior_frontier_point(self):
        frontier = pf.lower_envelope({"A": self.components(4, 0),
                                      "B": self.components(2, 2),
                                      "C": self.components(0, 4)})
        self.assertEqual(frontier.points[1], pf.Point(F(1, 2), ("A", "B", "C")))
        self.assertTrue(all("B" not in region.methods for region in frontier.regions))

    def test_endpoint_tie_only_methods_retained(self):
        frontier = pf.lower_envelope({"best": self.components(0, 0),
                                      "left": self.components(1, 0),
                                      "right": self.components(0, 1)})
        self.assertEqual(frontier.regions, (pf.Region(F(0), F(1), ("best",)),))
        self.assertEqual(frontier.points, (pf.Point(F(0), ("best", "left")),
                                           pf.Point(F(1), ("best", "right"))))

    def test_nonfrontier_crossings_are_merged_away(self):
        frontier = pf.lower_envelope({"best": self.components(0, 0),
                                      "B": self.components(1, 3),
                                      "C": self.components(3, 1)})
        self.assertEqual(frontier.regions, (pf.Region(F(0), F(1), ("best",)),))
        self.assertEqual(len(frontier.points), 2)

    def test_single_method_spans_whole_interval(self):
        frontier = pf.lower_envelope({"only": self.components(0, 3)})
        self.assertEqual(frontier.regions, (pf.Region(F(0), F(1), ("only",)),))

    def test_input_order_does_not_change_frontier(self):
        entries = [("A", self.components(4, 0)), ("B", self.components(1, 1)),
                   ("C", self.components(0, 4)), ("D", self.components(1, 1))]
        expected = pf.lower_envelope(dict(entries))
        for permutation in itertools.permutations(entries):
            self.assertEqual(pf.lower_envelope(dict(permutation)), expected)

    def test_frontier_matches_independent_exact_grid_enumeration(self):
        # Direct integer-weighted sums are independent of mean_loss and crossings.
        coordinates = [(0, 5), (1, 2), (2, 1), (5, 0), (2, 2), (3, 3)]
        for selected in itertools.combinations(coordinates, 4):
            raw = {str(i): pair for i, pair in enumerate(selected)}
            frontier = pf.lower_envelope({key: self.components(*pair)
                                          for key, pair in raw.items()})
            for numerator in range(21):
                alpha = F(numerator, 20)
                costs = {key: numerator * u + (20 - numerator) * v
                         for key, (u, v) in raw.items()}
                expected = tuple(sorted(key for key in raw if costs[key] == min(costs.values())))
                points = [point.methods for point in frontier.points if point.alpha == alpha]
                intervals = [region.methods for region in frontier.regions
                             if region.left < alpha < region.right]
                self.assertEqual((points or intervals), [expected], (selected, alpha))

    def test_invalid_frontier_inputs_rejected(self):
        for records in [{}, {"": self.components(0, 1)}, {1: self.components(0, 1)},
                        {"A": (0, 1)}]:
            with self.subTest(records=records):
                with self.assertRaises((TypeError, ValueError)):
                    pf.lower_envelope(records)


if __name__ == "__main__":
    unittest.main()
