from unittest import TestCase

from colosseum.exceptions import ValidationError
from colosseum.validators import is_font_family, is_integer, is_number


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
        self.assertEqual(is_font_family('Ahem, serif'), ['Ahem', 'serif'])
        self.assertEqual(is_font_family("Ahem,fantasy"), ["Ahem", 'fantasy'])
        self.assertEqual(is_font_family("  Ahem   ,    fantasy  "), ["Ahem", 'fantasy'])

    def test_font_family_name_invalid(self):
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
                is_font_family(case)
