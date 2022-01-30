from iterators import RegularFibonacciIterator

f = RegularFibonacciIterator()

for _ in range(1000000):
    next(f)
