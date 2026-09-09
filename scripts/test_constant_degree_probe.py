"""Exact small checks for notes/CONSTANT_DEGREE_PROBE.md.

These enumerate the underlying recurrences, not certificate transfer code.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import unittest


def wrapped_step(state, taps, memory, input_bit=0):
    recent = state & ((1 << (memory - 1)) - 1)
    output = input_bit ^ (state >> (memory - 1)) ^ ((recent & taps).bit_count() & 1)
    return ((state << 1) | output) & ((1 << memory) - 1)


def wrapped_distribution(mass, memory, required_output=None):
    result = defaultdict(F)
    tap_count = 1 << (memory - 1)
    for state, probability in mass.items():
        for taps in range(tap_count):
            new_state = wrapped_step(state, taps, memory)
            if required_output is None or new_state & 1 == required_output:
                result[new_state] += probability / tap_count
    return result


class ConstantDegreeProbeTests(unittest.TestCase):
    def test_placement_count_in_both_regular_ensembles(self):
        for length in range(4, 11):
            half = length // 2
            for width in range(1, length // 2 + 1):
                for minimum_gap in range(1, width + 1):
                    def accepted(u, v):
                        return u < half and minimum_gap <= v - u <= width

                    pair_count = sum(accepted(u, v)
                                     for u in range(length) for v in range(length))
                    self.assertEqual(pair_count, half * (width - minimum_gap + 1))
                    left_probability = F(pair_count, length**2)
                    for right_degree in (1, 2, 3):
                        slots = length * right_degree
                        count = sum(accepted(a // right_degree, b // right_degree)
                                    for a in range(slots) for b in range(slots) if a != b)
                        probability = F(count, slots * (slots - 1))
                        self.assertEqual(count, pair_count * right_degree**2)
                        self.assertGreaterEqual(probability, left_probability)

    def test_accumulator_opposite_labels_and_burst_weight(self):
        for prime in (2, 3, 5, 7):
            pairs = [(a, b) for a in range(1, prime) for b in range(1, prime)
                     if (a + b) % prime == 0]
            self.assertEqual(F(len(pairs), (prime - 1)**2), F(1, prime - 1))
            for a, b in pairs:
                for gap in range(1, 8):
                    # Two regions with possibly different gap lengths.
                    inputs = [0, a] + [0] * (gap - 1) + [b, 0, 0, a, 0, b, 0]
                    state = weight = 0
                    for value in inputs:
                        state = (state + value) % prime
                        weight += state != 0
                    self.assertEqual(state, 0)
                    self.assertEqual(weight, gap + 2)

    def test_wrapped_active_state_cannot_die_without_input(self):
        for memory in range(1, 6):
            for state in range(1, 1 << memory):
                for taps in range(1 << (memory - 1)):
                    self.assertNotEqual(wrapped_step(state, taps, memory), 0)

    def test_prescribed_last_memory_outputs_allow_cancellation(self):
        for memory in range(1, 6):
            critical = 1 << (memory - 1)
            for state in range(1, 1 << memory):
                mass = {state: F(1)}
                for output in [1] + [0] * (memory - 1):
                    mass = wrapped_distribution(mass, memory, output)
                self.assertEqual(set(mass), {critical})
                self.assertGreaterEqual(mass[critical], F(1, 1 << memory))
            for taps in range(1 << (memory - 1)):
                self.assertEqual(wrapped_step(critical, taps, memory, 1), 0)

    def test_cancellation_bound_at_every_checked_gap(self):
        for memory in range(1, 6):
            mass = {1: F(1)}  # State just after the first input one.
            for gap in range(1, 3 * memory + 3):
                # Before input at distance gap there are gap-1 zero-input steps.
                if gap >= memory + 1:
                    self.assertGreaterEqual(mass[1 << (memory - 1)], F(1, 1 << memory))
                mass = wrapped_distribution(mass, memory)

    def test_full_field_reset_in_one_memory_block(self):
        for prime in (2, 3):
            for memory in (1, 2, 3):
                vectors = list(product(range(prime), repeat=memory))
                zero = (0,) * memory
                for initial in vectors:
                    mass = {initial: F(1)}
                    for _ in range(memory):
                        next_mass = defaultdict(F)
                        for state, probability in mass.items():
                            for taps in vectors:
                                output = sum(a*b for a, b in zip(state, taps)) % prime
                                if output == 0:
                                    next_mass[(0,) + state[:-1]] += probability / len(vectors)
                        mass = next_mass
                    self.assertEqual(set(mass), {zero})
                    self.assertGreaterEqual(mass[zero], F(1, prime**memory))


if __name__ == "__main__":
    unittest.main()
