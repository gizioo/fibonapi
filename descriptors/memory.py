from .validator import Validator


class MemoryThreshold(Validator):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected {value!r} to be an int or float")
        if value < 0:
            raise ValueError(f"Expected {value!r} to be at least 0")
        if value > 100:
            raise ValueError(f"Expected {value!r} to be no more than 100!")
