import psutil
from descriptors.memory import MemoryThreshold
from iterators import MemLimitedFibonacciIterator


class MockIterator(MemLimitedFibonacciIterator):
    __slots__ = ["__memory_threshold"]

    def __init__(self, *args, memory_threshold=90, **kwargs):
        self.__memory_threshold = memory_threshold
        super().__init__(*args, **kwargs)

    def _check_limit(self):
        print(self.__memory_threshold)
        if psutil.virtual_memory().percent >= self.__memory_threshold:
            raise MemoryError
        return psutil.virtual_memory().percent >= self.__memory_threshold


class DescriptorMock:
    m = MemoryThreshold()

    def __init__(self, thresh):
        self.m = thresh
