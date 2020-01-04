from unittest import TestCase

from colosseum.constants import GENERIC_FAMILY_FONTS
from colosseum.validators import (ValidationError, is_font_family,
                                  is_integer, is_number)


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


class FontTests(TestCase):
    def test_font_family_name_valid(self):
        validator = is_font_family(generic_family=GENERIC_FAMILY_FONTS, font_families=['DejaVu Sans'])
        self.assertEqual(validator('"DejaVu Sans", serif'), ['"DejaVu Sans"', 'serif'])
        self.assertEqual(validator("'DejaVu Sans',fantasy"), ["'DejaVu Sans'", 'fantasy'])
        self.assertEqual(validator("  '   DejaVu   Sans   '   ,    fantasy  "), ["'DejaVu Sans'", 'fantasy'])

    def test_font_family_name_invalid(self):
        validator = is_font_family(generic_family=GENERIC_FAMILY_FONTS)
        invalid_cases = [
            'Red/Black, sans-serif',
            '"Lucida" Grande, sans-serif',
            'Ahem!, sans-serif',
            'test@foo, sans-serif',
            '#POUND, sans-serif',
            'Hawaii 5-0, sans-serif',
            '123',
        ]
        for case in invalid_cases:
            with self.assertRaises(ValidationError):
                validator(case)
