import cProfile
from iterators import FibonacciIterator

f = FibonacciIterator()

for _ in range(1000000):
    next(f)
