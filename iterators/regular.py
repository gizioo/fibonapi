class RegularFibonacciIterator(object):
    """
    A regular Fibonacci iterator class, using the cache + iteration approach

    """

    # slots to limit attributes
    __slots__ = ["__iteration", "__nums"]

    def __init__(self):

        self.__iteration = 0
        self.__nums = [0, 1]

    def __iter__(self):
        return self

    def __next__(self):

        return_value = None
        if self.__iteration < 2:  # check if first in series
            return_value = self.__iteration, self.__nums
        else:

            self.__nums.append(
                self.__nums[self.__iteration - 2] + self.__nums[self.__iteration - 1]
            )
            return_value = self.__nums[-1]

        self.__iteration += 1
        return return_value
