"""Check field certificate bounds against independently enumerated traces."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import unittest

from flint import arb, ctx, fmpq

from prime_field_biregular_ec_certificate import (
    full_support_term_arb,
    singleton_exact_band_branch_term_arb,
    singleton_block_term_arb,
    singleton_region_polynomial_arb,
    validate_parameters,
)
from prime_field_biregular_ec_d22_m12_certificate import validate_coverage


def ball(value):
    return arb(fmpq(value.numerator, value.denominator))


def trace_data(occupancy, outputs, memory, start=None):
    """Return final trailing-zero state and mark count, or reject the trace."""
    state = memory if start is None else start
    marks = 0
    for multiplicity, nonzero in zip(occupancy, outputs):
        if state == memory:
            if multiplicity == 0 and nonzero:
                return None
            if multiplicity == 1 and not nonzero:
                return None
        if not nonzero and (state < memory or multiplicity):
            marks += 1
        state = 0 if nonzero else min(memory, state + 1)
    return state, marks


def regional_occupancies(k, group, r):
    for selected in combinations(range(k), r):
        occupancy = [0] * (k // group)
        for slot in selected:
            occupancy[slot // group] += 1
        yield tuple(occupancy)


class FieldTraceAuditTests(unittest.TestCase):
    def setUp(self):
        ctx.prec = 160

    def test_claimed_prime_field_gv_cutoffs_are_exact_integer_floors(self):
        root = Path(__file__).resolve().parent.parent / "results"
        names = (
            "prime_field_biregular_ea_p127_rate_half_d30_gv.json",
            "prime_field_biregular_ec_p127_rate_half_d28_m3_gv.json",
            "prime_field_biregular_ec_p127_rate_half_d26_m4_singleton_gv.json",
            "prime_field_biregular_ec_p127_rate_half_d24_m6_singleton_gv.json",
            "prime_field_biregular_ec_p127_rate_half_d22_m12_region_gv.json",
        )
        for name in names:
            with self.subTest(certificate=name):
                parameters = json.loads((root / name).read_text())["parameters"]
                p = int(parameters["prime"])
                k, n, cutoff = (int(parameters[key]) for key in ("k", "n", "cutoff"))
                target = (1-arb(k)/n)*arb(p).log()
                def entropy(weight):
                    x = arb(weight)/n
                    return -x*x.log()-(1-x)*(1-x).log()+x*arb(p-1).log()
                # h_p is strictly increasing below (p-1)/p. Bracketing
                # its target between adjacent integer cutoffs proves the floor,
                # independently of the floating-point root finder.
                self.assertLess(arb(cutoff+1)/n, arb(p-1)/p)
                self.assertLess(entropy(cutoff), target)
                self.assertGreater(entropy(cutoff+1), target)

    def test_regional_coefficients_against_slot_and_trace_enumeration(self):
        k, group, ell = 6, 2, 3
        z, v = F(3, 4), F(1, 4)
        for memory in (1, 2, 3):
            matrix = singleton_region_polynomial_arb(
                region_length=ell, group_size=group, max_weight=k,
                memory=memory, output_marker=ball(z), equation_marker=ball(v))
            for r in range(k + 1):
                for start in range(memory + 1):
                    expected = [F(0)] * (memory + 1)
                    for occupancy in regional_occupancies(k, group, r):
                        for outputs in product((0, 1), repeat=ell):
                            result = trace_data(occupancy, outputs, memory, start)
                            if result is not None:
                                end, a = result
                                expected[end] += z**sum(outputs) * v**a
                    for end, value in enumerate(expected):
                        self.assertTrue(matrix[start][end][r].contains(
                            fmpq(value.numerator, value.denominator)))

    def test_two_region_cap_branches_against_exact_rational_enumeration(self):
        k, group, regions, ell, memory = 4, 2, 2, 2, 2
        n, cutoff, q = 4, 1, 5
        z, v = F(3, 4), F(1, 4)
        for r in range(1, k + 1):
            counts = Counter()
            patterns = list(regional_occupancies(k, group, r))
            for first, second in product(patterns, repeat=regions):
                # Keep one state across the boundary: do not reset it.
                for outputs in product((0, 1), repeat=n):
                    result = trace_data(first + second, outputs, memory)
                    if result is not None:
                        counts[sum(outputs), result[1]] += 1
            normalizer = comb(k, r)**regions
            mgf = sum((F(count, normalizer)*z**h*v**a
                       for (h, a), count in counts.items()), F(0))
            for field in (False, True):
                actual = singleton_exact_band_branch_term_arb(
                    prime=q, k=k, n=n, cutoff=cutoff, region_count=regions,
                    memory=memory, lo=r, hi=r, values=["0.75", "0.25"], field=field)
                multiplier = v**(-r)/F(q-1) if field else v**(1-r)
                expected = comb(k, r)*mgf*z**(-cutoff)*multiplier
                self.assertTrue(actual.contains(fmpq(expected.numerator, expected.denominator)))
                restricted = sum((F(count, normalizer) *
                    (F(q-1)**(r-1-a) if field else 1)
                    for (h, a), count in counts.items()
                    if h <= cutoff and ((a >= r) if field else (a < r))), F(0))
                self.assertLessEqual(comb(k, r)*restricted, expected)

        # Also check that a multi-support coefficient block dominates the
        # sum of exact-regional bounds using the same z,v markers.
        markers = {name: ["0.75", "0.25", "0.5"] for name in ("structural", "field")}
        block = singleton_block_term_arb(
            prime=q, k=k, n=n, cutoff=cutoff, region_count=regions,
            memory=memory, lo=1, hi=3, markers=markers)
        exact = sum((singleton_exact_band_branch_term_arb(
            prime=q, k=k, n=n, cutoff=cutoff, region_count=regions,
            memory=memory, lo=r, hi=r, values=["0.75", "0.25"], field=field)
            for r in range(1, 4) for field in (False, True)), arb(0))
        self.assertTrue(block > exact)

    def test_rejects_missing_sparse_field_band(self):
        path = Path(__file__).resolve().parents[1] / "results/prime_field_biregular_ec_p127_rate_half_d22_m12_region_gv.json"
        original = json.loads(path.read_text())
        validate_coverage(original)
        for index in range(len(original["sparse_support"]["field_bands"])):
            altered = deepcopy(original)
            del altered["sparse_support"]["field_bands"][index]
            with self.assertRaisesRegex(ValueError, "sparse field coverage"):
                validate_coverage(altered)

    def test_rejects_invalid_full_support_markers(self):
        for markers in (["1.1", "0.5"], ["0.5", "1.1"], ["0", "0.5"]):
            with self.assertRaisesRegex(ValueError, "full-support markers"):
                full_support_term_arb(prime=5, n=4, cutoff=1, memory=2,
                    message_weight=2, markers={"structural": markers, "field": ["0.5", "0.25"]})

    def test_full_support_bound_has_closed_scalar_form(self):
        # Every row of P_1 sums to z+v, for every memory.
        q, n, r, cutoff = 5, 8, 4, 2
        z, v = F(3, 4), F(1, 4)
        expected = (z+v)**n*z**(-cutoff)*(v**(1-r)+v**(-r)/F(q-1))
        for memory in (1, 2, 5):
            actual = full_support_term_arb(prime=q, n=n, cutoff=cutoff,
                memory=memory, message_weight=r,
                markers={name: ["0.75", "0.25"] for name in ("structural", "field")})
            self.assertTrue(actual.contains(fmpq(expected.numerator, expected.denominator)))

    def test_field_order_and_regional_dimensions(self):
        certificate = {"parameters": {"field_order": 4, "k": 6, "n": 12,
            "cutoff": 3, "region_count": 4, "memory": 2, "target_bits": 20},
            "verification": {"precision_bits": 128}}
        for q in (2, 3, 4, 5, 9, 25, 729, 2**128, 2**127-1):
            certificate["parameters"]["field_order"] = q
            validate_parameters(certificate)
        for key, value in (("field_order", 6), ("field_order", 36), ("k", 5),
                           ("n", 13), ("cutoff", 13), ("memory", 0), ("k", 6.5)):
            altered = deepcopy(certificate)
            altered["parameters"][key] = value
            with self.assertRaises(ValueError):
                validate_parameters(altered)


if __name__ == "__main__":
    unittest.main()
