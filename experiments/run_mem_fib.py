from iterators import MemLimitedFibonacciIterator

f = MemLimitedFibonacciIterator()

for _ in range(1000000):
    next(f)
