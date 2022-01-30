from iterators import UnifiedMemLimitedFibonacciIterator

f = UnifiedMemLimitedFibonacciIterator()

for _ in range(1000000):
    next(f)
