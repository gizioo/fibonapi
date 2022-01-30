import psutil
from descriptors import MemoryThreshold


class UnifiedMemLimitedFibonacciIterator(object):
    """
    A Fibonacci iterator with the same functionality as the MemLimitedFibonacciIterator but without using inheritance.
    For test purposes only.

    Attributes
    ----------

    memory_threshold (numeric): Numeric value representing the system memory usage percent at which the iterator should reset.
    """

    # slots to limit attributes
    __slots__ = ["__first", "__second"]

    __memory_threshold = MemoryThreshold()

    def __init__(self, memory_threshold=90):

        # name mangling to prevent accidental access
        self.__first = -1
        self.__second = -1
        self.__memory_threshold = memory_threshold

    def __iter__(self):
        return self

    def __next__(self):
        if self.__first == -1:  # check if first in series
            self.__first = 0
            return self.__first
        elif self.__second == -1:  # check if second
            self.__second = 1
            return self.__second
        else:  # calculate next in series
            self.__first, self.__second = (
                self.__second,
                self.__first + self.__second,
            )  # assign with a shift
            if self._check_limit():
                self._reset()
            return self.__second

    def _check_limit(self):
        return psutil.virtual_memory().percent >= self.__memory_threshold

    def _reset(self):
        self.__first = -1
        self.__second = -1
