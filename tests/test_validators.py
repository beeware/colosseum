from unittest import TestCase

from colosseum.shapes import Rect
from colosseum.validators import is_integer, is_number, is_shape, ValidationError


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


class ShapeTests(TestCase):

    def test_shape_valid(self):
        # Comma separated
        self.assertEqual(is_shape('rect(1px, 3px, 2px, 4px)'), Rect(1, 3, 2, 4))

        # Comma separated with extra spaces
        self.assertEqual(is_shape(' rect( 1px,  3px,  2px,  4px ) '), Rect(1, 3, 2, 4))

        # Space separated
        self.assertEqual(is_shape('rect(1px 3px 2px 4px)'), Rect(1, 3, 2, 4))

        # Space separated with extra spaces
        self.assertEqual(is_shape(' rect( 1px  3px  2px  4px ) '), Rect(1, 3, 2, 4))

    def test_shape_invalid(self):
        # Mix of commas and spaces
        with self.assertRaises(ValidationError):
            is_shape('rect(1px, 3px, 2px 4px)')

        # Incorrect number of elements
        with self.assertRaises(ValidationError):
            is_shape('rect(1px, 3px, 2px)')

        with self.assertRaises(ValidationError):
            is_shape('rect(1px, 3px)')

        with self.assertRaises(ValidationError):
            is_shape('rect(1px)')

        with self.assertRaises(ValidationError):
            is_shape('rect()')

        # Other values
        with self.assertRaises(ValidationError):
            is_shape('(1px, 3px, 2px, 4px)')

        with self.assertRaises(ValidationError):
            is_shape('rect(a, b, c, d)')
