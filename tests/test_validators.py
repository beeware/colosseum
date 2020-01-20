from unittest import TestCase

from colosseum.units import px
from colosseum.validators import (is_border_spacing, is_integer, is_number,
                                  ValidationError)


class NumericTests(TestCase):

    def test_integer(self):
        self.assertEqual(is_integer('1'), 1)

        validator = is_integer(min_value=0, max_value=12)
        self.assertEqual(validator('1'), 1)
        self.assertEqual(validator('0'), 0)
        self.assertEqual(validator('12'), 12)

        with self.assertRaises(ValidationError):
            validator(-2)

        with self.assertRaises(ValidationError):
            validator(15)

        with self.assertRaises(ValidationError):
            validator('spam')

    def test_number(self):
        self.assertEqual(is_number('1'), 1.0)

        validator = is_number(min_value=0, max_value=12)
        self.assertEqual(validator('1.0'), 1.0)
        self.assertEqual(validator('0.0'), 0.0)
        self.assertEqual(validator('12.0'), 12.0)

        with self.assertRaises(ValidationError):
            validator(-2)

        with self.assertRaises(ValidationError):
            validator(15)

        with self.assertRaises(ValidationError):
            validator('spam')


class BorderSpacingTests(TestCase):

    def test_border_spacing_valid_str(self):
        self.assertEqual(is_border_spacing('1 1'), (1 * px, 1 * px))
        self.assertEqual(is_border_spacing('1'), (1 * px, ))

    def test_border_spacing_valid_numbers(self):
        self.assertEqual(is_border_spacing(1), (1 * px, ))
        self.assertEqual(is_border_spacing(1.0), (1 * px, ))

    def test_border_spacing_valid_sequences(self):
        # List of strings
        self.assertEqual(is_border_spacing(['1', '2']), (1 * px, 2 * px))
        self.assertEqual(is_border_spacing(['1']), (1 * px, ))

        # List of ints
        self.assertEqual(is_border_spacing([1, 2]), (1 * px, 2 * px))
        self.assertEqual(is_border_spacing([1]), (1 * px, ))

        # List of floats
        self.assertEqual(is_border_spacing([1.0, 2.0]), (1 * px, 2 * px))
        self.assertEqual(is_border_spacing([1.0]), (1 * px, ))

        # Tuple of ints
        self.assertEqual(is_border_spacing((1, 2)), (1 * px, 2 * px))
        self.assertEqual(is_border_spacing((1, )), (1 * px, ))

    def test_border_spacing_valid_spaces(self):
        self.assertEqual(is_border_spacing('  1   1  '), (1 * px, 1 * px))
        self.assertEqual(is_border_spacing('  1  '), (1 * px, ))

    def test_border_spacing_invalid(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('a a')

        with self.assertRaises(ValidationError):
            is_border_spacing('b')

        with self.assertRaises(ValidationError):
            is_border_spacing([1, 2, 3])

        with self.assertRaises(ValidationError):
            is_border_spacing([])

        with self.assertRaises(ValidationError):
            is_border_spacing(['a', 'b'])
