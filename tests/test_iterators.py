import unittest
import psutil
from iterators import FibonacciIterator, MemLimitedFibonacciIterator
from .mocks import MockIterator


class FibonacciTestCase(unittest.TestCase):
    def test_fibonacci_sequence(self):
        f = FibonacciIterator()
        test_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        for test_val in test_sequence:
            val = next(f)
            assert val == test_val

    def test_fibonacci_prevent_assign(self):
        f = FibonacciIterator()
        with self.assertRaises(AttributeError):
            f.__first = 6

        with self.assertRaises(AttributeError):
            f.__second = 6


class MemLimitedFibonacciTestCase(FibonacciTestCase):
    def test_assign_less_memory_than_available(self):
        starting_percent = psutil.virtual_memory().percent
        threshold = starting_percent * 0.5
        with self.assertRaises(MemoryError):
            f = MemLimitedFibonacciIterator(memory_threshold=threshold)

    def test_check_limit(self):
        starting_percent = psutil.virtual_memory().percent
        threshold = starting_percent * 0.99
        f = MockIterator(memory_threshold=threshold)

        with self.assertRaises(MemoryError):
            next(f)
