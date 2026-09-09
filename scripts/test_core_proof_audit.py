"""Independent finite checks of the paper's probabilistic proof steps.

These tests enumerate sampled codes, not the certificate transfer routines.
They detect small counterexamples; the universal claims still need the proofs.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import ceil, comb
import unittest

from flint import fmpq_poly as Poly


def add(a, b, q):
    return a ^ b if q == 4 else (a + b) % q


def mul(a, b, q):
    if q != 4:
        return a * b % q
    # GF(4) = GF(2)[X]/(X^2 + X + 1), in the polynomial basis.
    value = 0
    while b:
        if b & 1:
            value ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return value


def dot(left, right, q):
    value = 0
    for a, b in zip(left, right):
        value = add(value, mul(a, b, q), q)
    return value


def mark_count(trace, occupancy, memory):
    trailing = memory
    marks = 0
    for nonzero, occupied in zip(trace, occupancy):
        if not nonzero and (trailing < memory or occupied):
            marks += 1
        trailing = 0 if nonzero else min(memory, trailing + 1)
    return marks


class CoreProofAuditTests(unittest.TestCase):
    def test_degree_five_variance_identities_as_exact_polynomials(self):
        x = Poly([0, 1])
        numerator = 10*x**2*(1-x)**2*(8*x**4-24*x**3+32*x**2-20*x+5)
        denominator = 16*x**4-40*x**3+40*x**2-20*x+5
        moments = []
        for parity in (0, 1):
            masses = [comb(5, 2*j+parity)*x**(2*j+parity)*(1-x)**(5-2*j-parity)
                      for j in range(3)]
            total = sum(masses, Poly([]))
            first = masses[1] + 2*masses[2]
            second = masses[1] + 4*masses[2]
            moments.append((second*total - first**2, total**2))
        odd_n, odd_d = moments[1]
        self.assertEqual(odd_n*denominator**2, numerator*odd_d)
        factor = x*(x-1)*(2*x-1)*(4*x**2-10*x+5)*(4*x**4-20*x**3+30*x**2-20*x+5)
        self.assertEqual(numerator.derivative()*denominator - 2*numerator*denominator.derivative(),
                         20*factor)
        # Check the variance difference after substituting t = 1-2*x,
        # by cross multiplication, without numerical sampling of theta.
        t = 1 - 2*x
        difference_n = 5*t**3*(1-t)**2*(1+t)**2*(t**2+1)*(2*t**4+t**2+2)
        difference_d = 4*(t**4-t**3+t**2-t+1)**2*(t**4+t**3+t**2+t+1)**2
        even_n, even_d = moments[0]
        self.assertEqual((even_n*odd_d-odd_n*even_d)*difference_d,
                         difference_n*even_d*odd_d)

    def test_full_field_feedback_is_uniform_including_extension_field(self):
        for q in (2, 3, 4, 5):
            for memory in (1, 2, 3):
                vectors = list(product(range(q), repeat=memory))
                for state in vectors[1:]:
                    counts = Counter(dot(taps, state, q) for taps in vectors)
                    self.assertEqual(counts, {x: q ** (memory - 1) for x in range(q)})

    def test_independent_nonzero_feedback_has_the_required_point_mass_bound(self):
        for q in (2, 3, 4, 5):
            for memory in (1, 2, 3):
                taps = list(product(range(1, q), repeat=memory))
                for state in list(product(range(q), repeat=memory))[1:]:
                    counts = Counter(dot(alpha, state, q) for alpha in taps)
                    self.assertLessEqual(max(counts.values()), (q - 1) ** (memory - 1))

    def test_capped_projective_union_for_shared_sampled_codes(self):
        # Both message symbols are nonzero. Each projective line is (1,c).
        # Importantly, all lines below share the SAME sampled labels and taps.
        patterns = (((0,), (1,), (0, 1)), ((0, 1), (), (0, 1)))
        for q, memory in ((3, 1), (4, 1), (3, 2)):
            for incidence in patterns:
                counts = Counter()
                samples = 0
                edges = sum(map(len, incidence))
                for labels in product(range(1, q), repeat=edges):
                    inputs = []
                    for c in range(1, q):
                        message = (1, c)
                        offset = 0
                        row = []
                        for neighbors in incidence:
                            row.append(dot(
                                [message[i] for i in neighbors],
                                labels[offset:offset + len(neighbors)], q))
                            offset += len(neighbors)
                        inputs.append(row)
                    for taps in product(range(q), repeat=3 * memory):
                        realized = set()
                        for row in inputs:
                            state = [0] * memory
                            trace = []
                            for t, symbol in enumerate(row):
                                out = add(symbol, dot(
                                    taps[t * memory:(t + 1) * memory], state, q), q)
                                trace.append(bool(out))
                                state = [out] + state[:-1]
                            realized.add(tuple(trace))
                        counts.update(realized)
                        samples += 1
                for trace, count in counts.items():
                    a = mark_count(trace, tuple(map(bool, incidence)), memory)
                    bound = min(F(1), F(q - 1) ** (1 - a))
                    self.assertLessEqual(F(count, samples), bound,
                                         (q, memory, incidence, trace, a))

    def test_singleton_region_event_containment(self):
        # Four regions, two right coordinates per region, two slots per
        # coordinate. Enumerate every possible regional multiplicity pattern.
        ell, regions, n = 2, 4, 8
        for r, region_options in ((1, ((1, 0), (0, 1))),
                                  (2, ((2, 0), (1, 1), (0, 2))),
                                  (3, ((2, 1), (1, 2)))):
            for memory in (1, 2, 3):
                intervals = 1 + (r - 1) // memory
                for pattern in product(region_options, repeat=regions):
                    occupancy = sum(pattern, ())
                    free = sum(1 not in region for region in pattern)
                    for trace in product((False, True), repeat=n):
                        trailing, valid = memory, True
                        for out, multiplicity in zip(trace, occupancy):
                            if trailing == memory:
                                if (multiplicity == 0 and out) or (multiplicity == 1 and not out):
                                    valid = False
                                    break
                            trailing = 0 if out else min(memory, trailing + 1)
                        if not valid or mark_count(trace, occupancy, memory) > r - 1:
                            continue
                        required = ceil((n - sum(trace) - (r - 1)) / ell) - 2 * intervals
                        self.assertGreaterEqual(free, required,
                                                (r, memory, pattern, trace))

    def test_compressed_wrapped_derivative_exactly(self):
        for memory in range(1, 13):
            c = F(1, 2 ** memory - 1)
            alpha = F(2 ** (memory - 1), 2 ** memory - 1)
            pi = [alpha / 2 ** j for j in range(memory)]
            self.assertEqual(sum(pi), 1)
            for theta in (F(0), F(1, 3), F(7)):
                derivative = [[F(0)] * (memory + 1) for _ in range(memory + 1)]
                for j in range(memory - 1):
                    derivative[j][0] = -theta / 2
                derivative[memory - 1][0] = -1 - theta
                derivative[memory - 1][memory] = 1
                derivative[memory][0] = 1
                derivative[memory][memory] = -1
                compressed = [
                    [sum(pi[j] * sum(derivative[j][:memory]) for j in range(memory)),
                     sum(pi[j] * derivative[j][memory] for j in range(memory))],
                    [sum(derivative[memory][:memory]), derivative[memory][memory]],
                ]
                self.assertEqual(compressed, [[-c - theta * alpha, c], [1, -1]])


if __name__ == "__main__":
    unittest.main()
