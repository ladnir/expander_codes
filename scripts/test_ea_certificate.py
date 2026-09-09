#!/usr/bin/env python3

from __future__ import annotations

import itertools
import json
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path

from flint import arb, ctx

from ea_certificate import (
    entropy_count_bound_arb,
    exact_tail_bound_arb,
    q_arb,
    spectral_tail_bound_arb,
    verify_certificate,
)


def direct_accumulator_tail(n: int, q: Fraction, cutoff: int) -> Fraction:
    total = Fraction(0)
    for inputs in itertools.product((0, 1), repeat=n):
        probability = Fraction(1)
        state = 0
        weight = 0
        for bit in inputs:
            probability *= q if bit else 1 - q
            state ^= bit
            weight += state
        if weight <= cutoff:
            total += probability
    return total


class EACertificateTests(unittest.TestCase):
    def setUp(self) -> None:
        ctx.prec = 192

    def test_arb_chernoff_bounds_dominate_exact_small_tail(self) -> None:
        n, cutoff = 7, 2
        rational_q = Fraction(1, 4)
        q = arb(rational_q.numerator) / rational_q.denominator
        z = arb(2) / 5
        exact_probability = direct_accumulator_tail(n, rational_q, cutoff)
        exact_probability_arb = arb(exact_probability.numerator) / exact_probability.denominator

        matrix_bound = exact_tail_bound_arb(q, z, n, cutoff)
        spectral_bound = spectral_tail_bound_arb(q, z, n, cutoff)
        self.assertTrue(matrix_bound > exact_probability_arb)
        self.assertTrue(spectral_bound >= matrix_bound)

    def test_activation_probability_is_enclosed(self) -> None:
        # p=1/10 and r=3 give q=(1-(4/5)^3)/2=61/250 exactly.
        actual = q_arb(row_weight=1, n=10, r=3)
        expected = arb(61) / 250
        self.assertTrue(actual.contains(expected))

    def test_spectral_block_dominates_independently_enumerated_tails(self) -> None:
        k, n, row_weight, cutoff = 6, 8, 1, 2
        rho = Fraction(row_weight, n)
        for lo, hi in ((1, 1), (1, 3), (2, 3), (4, 6)):
            expected = Fraction(0)
            for r in range(lo, hi + 1):
                q = (1 - (1 - 2*rho)**r) / 2
                expected += comb(k, r) * direct_accumulator_tail(n, q, cutoff)
            count = (entropy_count_bound_arb(k, lo, hi)
                     if hi <= k // 2 else arb(2)**k)
            for z in (arb(1)/4, arb(2)/3, arb(1)):
                bound = count * spectral_tail_bound_arb(
                    q_arb(row_weight, n, lo), z, n, cutoff)
                self.assertTrue(bound > arb(expected.numerator)/expected.denominator)

    def test_symmetric_transfer_decreases_by_negative_square(self) -> None:
        # Put z=t^2 so the similarity transform has rational entries.
        # Check the quadratic-form identity without a numerical eigensolver.
        for t in (Fraction(1, 4), Fraction(2, 3), Fraction(1)):
            for a, b in ((Fraction(0), Fraction(1, 5)),
                         (Fraction(1, 5), Fraction(1, 2))):
                def matrix(q):
                    return ((1-q, q*t), (q*t, (1-q)*t*t))
                sa, sb = matrix(a), matrix(b)
                for vector in itertools.product(range(-2, 3), repeat=2):
                    value = sum(vector[i]*(sb[i][j]-sa[i][j])*vector[j]
                                for i in range(2) for j in range(2))
                    self.assertEqual(value, -(b-a)*(vector[0]-t*vector[1])**2)
                    self.assertLessEqual(value, 0)

    def test_checked_in_certificates_prove_twenty_bits(self) -> None:
        certificate_dir = Path(__file__).parent / "certificates"
        cases = (
            ("ea-k20-r5-d005-w50-s20.json", 2**20, 50),
            ("ea-k25-r5-d005-w56-s20.json", 2**25, 56),
            ("ea-k30-r5-d005-w62-s20.json", 2**30, 62),
        )
        for filename, expected_k, expected_row_weight in cases:
            with self.subTest(filename=filename):
                certificate = json.loads(
                    (certificate_dir / filename).read_text(encoding="utf-8")
                )
                result = verify_certificate(certificate)
                self.assertEqual(certificate["parameters"]["k"], expected_k)
                self.assertEqual(
                    certificate["parameters"]["row_weight"], expected_row_weight
                )
                self.assertTrue(result.success)
                self.assertTrue(result.security_bits > 20)
                self.assertEqual(result.largest_exact_r, 1)


if __name__ == "__main__":
    unittest.main()
