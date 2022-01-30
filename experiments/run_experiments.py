from iterators import (
    FibonacciIterator,
    RegularFibonacciIterator,
)

from get_size import get_size

RUNS = 1000000


def optimized_fib():
    f = FibonacciIterator()

    for _ in range(RUNS):
        next(f)
    print(
        get_size(getattr(f, f"_{f.__class__.__name__}__first"))
        + (get_size(getattr(f, f"_{f.__class__.__name__}__second")))
    )


def regular_fib():
    f = RegularFibonacciIterator()

    for _ in range(RUNS):
        next(f)
    print(
        get_size(getattr(f, f"_{f.__class__.__name__}__iteration"))
        + (get_size(getattr(f, f"_{f.__class__.__name__}__nums")))
    )


if __name__ == "__main__":
    optimized_fib()
    regular_fib()
