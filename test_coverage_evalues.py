"""Artificial exact-arithmetic checks, never financial archive observations."""
from dataclasses import FrozenInstanceError
from decimal import Decimal
from fractions import Fraction
from itertools import product
from math import comb, isfinite
import unittest

from coverage_evalues import mixture_evalue, phase_mixture, fraction_fields


A = Fraction(1, 20)


def polynomial_integral(n, k, alpha):
    """Independent small-fixture expansion in powers of u, with signed terms."""
    integral = sum((Fraction((-1) ** j * comb(n-k, j), k+j+1)
                    * (1-alpha ** (k+j+1)) for j in range(n-k+1)), Fraction())
    return integral / (alpha ** k * (1-alpha) ** (n-k+1))


def integer_oracle(n, k):
    return Fraction(sum(comb(n+1, j) * 19 ** (k-j) for j in range(k+1)),
                    (n+1) * comb(n, k))


class ExactMixtureTests(unittest.TestCase):
    def test_empty_and_analytic_small_cases(self):
        for n, k, expected in [(0, 0, 1), (1, 0, Fraction(1, 2)),
                               (1, 1, Fraction(21, 2)), (2, 0, Fraction(1, 3)),
                               (2, 1, Fraction(11, 3)), (2, 2, Fraction(421, 3))]:
            with self.subTest(n=n, k=k):
                self.assertEqual(mixture_evalue(n, k), expected)

    def test_all_small_counts_against_signed_polynomial_integral(self):
        for alpha in (A, Fraction(1, 2), Fraction(3, 7)):
            for n in range(11):
                for k in range(n+1):
                    self.assertEqual(mixture_evalue(n, k, alpha),
                                     polynomial_integral(n, k, alpha))

    def test_distinct_integer_formula_at_large_and_extreme_counts(self):
        for n, k in [(12, 0), (12, 6), (40, 8), (265, 16),
                     (947, 80), (947, 947), (10000, 0)]:
            self.assertEqual(mixture_evalue(n, k), integer_oracle(n, k))

    def test_exact_boundary_expectation_is_one(self):
        for n in range(10):
            expectation = sum((comb(n, k) * A ** k * (1-A) ** (n-k)
                               * mixture_evalue(n, k) for k in range(n+1)), Fraction())
            self.assertEqual(expectation, 1)

    def test_lower_null_probability_has_expectation_at_most_one(self):
        for q in (Fraction(), A/2, A):
            for n in range(8):
                expectation = sum((comb(n, k) * q ** k * (1-q) ** (n-k)
                                   * mixture_evalue(n, k) for k in range(n+1)), Fraction())
                self.assertLessEqual(expectation, 1)

    def test_adaptive_dependent_boundary_tree(self):
        # Conditional success probability depends on resolved previous bits.
        # It always stays <=alpha; independence is deliberately absent.
        total = Fraction()
        for bits in product((0, 1), repeat=6):
            probability = Fraction(1)
            previous = 0
            for bit in bits:
                q = A if previous == 0 else A/2
                probability *= q if bit else 1-q
                previous = bit
            total += probability * mixture_evalue(6, sum(bits))
        self.assertLessEqual(total, 1)

    def test_invalid_count_or_alpha_contracts(self):
        for args in [(-1, 0), (2, -1), (2, 3), (10001, 0), (True, 0),
                     (2, False), (2.0, 1), (2, 1.0), (None, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                mixture_evalue(*args)
        for alpha in (0.05, 0, 1, Fraction(), Fraction(1), Fraction(-1, 3), None):
            with self.subTest(alpha=alpha), self.assertRaises(ValueError):
                mixture_evalue(2, 1, alpha)


class PhaseTests(unittest.TestCase):
    def test_global_record_anchor_and_complete_inventory(self):
        origins = list(range(100, 131))
        hits = [int(t % 11 == 0) for t in origins]
        r = phase_mixture(origins, hits, 6)
        self.assertEqual((r.horizon, r.first_origin, r.last_origin, r.n, r.k),
                         (6, 100, 130, 31, sum(hits)))
        self.assertEqual([p.phase for p in r.phases], list(range(7)))
        self.assertEqual([p.n for p in r.phases], [5, 5, 5, 4, 4, 4, 4])
        self.assertEqual(sum(p.n for p in r.phases), r.n)
        self.assertEqual(sum(p.k for p in r.phases), r.k)
        self.assertEqual(r.value, sum((p.value for p in r.phases), Fraction()) / 7)
        shifted = phase_mixture([t+217 for t in origins], hits, 6)
        self.assertEqual(r.value, shifted.value)
        self.assertEqual(origins, list(range(100, 131)))

    def test_membership_uses_actual_origin_not_row_number(self):
        r = phase_mixture([100, 107, 120], [0, 1, 1], 6)
        self.assertEqual([p.n for p in r.phases], [2, 0, 0, 0, 0, 0, 1])
        self.assertEqual([p.k for p in r.phases], [1, 0, 0, 0, 0, 0, 1])

    def test_dependent_phases_average_not_product(self):
        # Two overlapping issues share a future coin revealed at record2.
        # For H2 the third fixed phase is empty and keeps its value/weight.
        zero = phase_mixture([0, 1], [0, 0], 2)
        one = phase_mixture([0, 1], [1, 1], 2)
        self.assertEqual(zero.phases[2].value, 1)
        self.assertEqual(one.phases[2].value, 1)
        self.assertEqual((1-A)*zero.value + A*one.value, 1)
        invalid_product_expectation = ((1-A)*zero.phases[0].value**2
                                       + A*one.phases[0].value**2)
        self.assertEqual(invalid_product_expectation, Fraction(23, 4))
        self.assertGreater(invalid_product_expectation, 1)

    def test_outputs_are_frozen(self):
        r = phase_mixture([0], [True], 1)
        self.assertIsInstance(r.phases, tuple)
        with self.assertRaises(FrozenInstanceError):
            r.value = Fraction(99)
        with self.assertRaises(FrozenInstanceError):
            r.phases[0].n = 9

    def test_invalid_origins_hits_or_horizon(self):
        for origins, hits, horizon in [([], [], 1), ([0, 0], [0, 1], 1),
                ([1, 0], [0, 1], 1), ([-1], [0], 1), ([True], [0], 1),
                ([0.0], [0], 1), ([0, 1], [0], 1), ([0], [2], 1),
                ([0], [0.0], 1), ([0], [None], 1), ([0], [0], 0),
                ([0], [0], 1001), ([0], [0], True), ([0], [0], 1.0)]:
            with self.subTest(args=(origins, hits, horizon)), self.assertRaises(ValueError):
                phase_mixture(origins, hits, horizon)


class SerializationTests(unittest.TestCase):
    def test_exact_hex_roundtrip_and_finite_approximate_labels(self):
        for e in (Fraction(1), Fraction(1, 10001), mixture_evalue(947, 947),
                  Fraction(1120) + Fraction(1, 10**20)):
            fields = fraction_fields(e)
            self.assertEqual(Fraction(int(fields['numerator_hex'], 16),
                                      int(fields['denominator_hex'], 16)), e)
            self.assertTrue(isfinite(fields['log10_approx']))
            self.assertTrue(Decimal(fields['display']).is_finite())

    def test_display_rounding_must_not_decide_threshold(self):
        lower = Fraction(1120) - Fraction(1, 10**20)
        upper = Fraction(1120) + Fraction(1, 10**20)
        self.assertEqual(fraction_fields(lower)['display'], fraction_fields(upper)['display'])
        self.assertFalse(lower >= 1120)
        self.assertTrue(upper >= 1120)

    def test_nonpositive_or_nonfraction_display_rejected(self):
        for e in (Fraction(), Fraction(-1), 1, 1.0, None):
            with self.assertRaises(ValueError):
                fraction_fields(e)


if __name__ == '__main__':
    unittest.main()
