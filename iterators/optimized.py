class FibonacciIterator(object):
    """
    An optimized Fibonacci iterator class

    """

    # slots to limit attributes
    __slots__ = ["__first", "__second"]

    def __init__(self):

        # name mangling to prevent accidental access
        self.__first = -1
        self.__second = -1

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
            return self.__second

    def _reset(self):
        self.__first = -1
        self.__second = -1
