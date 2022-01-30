import unittest
from .mocks import DescriptorMock


class DescriptorTestCase(unittest.TestCase):
    def test_create(self):

        try:
            DescriptorMock(50)
            DescriptorMock(25.5)
        except:
            self.fail("myFunc() raised ExceptionType unexpectedly!")

    def test_threshold_less_then_zero(self):

        with self.assertRaises(ValueError):
            DescriptorMock(-10)

    def test_threshold_above_100(self):
        with self.assertRaises(ValueError):
            DescriptorMock(120)

    def test_threshold_not_a_number(self):
        with self.assertRaises(TypeError):
            DescriptorMock("one million")
