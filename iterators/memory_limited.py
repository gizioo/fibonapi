import psutil
from descriptors import MemoryThreshold
from .optimized import FibonacciIterator


class MemLimitedFibonacciIterator(FibonacciIterator):
    """
    A Fibonacci Iterator, based on the FibonacciIterator class, implements memory limit check.
    Resets the iterator if a given threshold has been reached.

    Attributes
    ----------

    memory_threshold (numeric): Numeric value representing the system memory usage percent at which the iterator should reset.
    """

    __memory_threshold = MemoryThreshold()

    def __init__(self, *args, memory_threshold=90, **kwargs):

        current_memory_usage = psutil.virtual_memory().percent
        if current_memory_usage > memory_threshold:
            raise MemoryError("Memory usage over given threshold")

        super().__init__(*args, **kwargs)

        self.__memory_threshold = memory_threshold

    def __next__(self):
        if self._check_limit():
            self._reset()
        return super().__next__()

    def _check_limit(self):
        return psutil.virtual_memory().percent >= self.__memory_threshold
