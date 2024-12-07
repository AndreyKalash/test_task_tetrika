import unittest
from solution import sum_two


class TestStrictDecorator(unittest.TestCase):
    def test_valid_arguments(self):
        self.assertEqual(sum_two(1, 2), 3)

    def test_invalid_arguments_type(self):
        with self.assertRaises(TypeError):
            sum_two(1, 2.5)

    def test_string_argument(self):
        with self.assertRaises(TypeError):
            sum_two("1", 2)

    def test_boolean_argument(self):
        with self.assertRaises(TypeError):
            sum_two(True, 1)

    def test_float_arguments(self):
        with self.assertRaises(TypeError):
            sum_two(1.1, 2.2)


if __name__ == "__main__":
    unittest.main()
