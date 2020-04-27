from unittest import TestCase

from colosseum.exceptions import ValidationError
from colosseum.shapes import Rect
from colosseum.units import px
from colosseum.validators import (is_border_spacing, is_font_family,
                                  is_integer, is_number, is_quote, is_rect)
from colosseum.wrappers import Quotes


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

    def test_border_spacing_valid_str_1_item(self):
        self.assertEqual(is_border_spacing('1').horizontal, 1 * px)
        self.assertEqual(is_border_spacing('1').vertical, 1 * px)

    def test_border_spacing_valid_str_1_item_with_spaces(self):
        self.assertEqual(is_border_spacing('  1  ').horizontal, 1 * px)
        self.assertEqual(is_border_spacing('  1  ').vertical, 1 * px)

    def test_border_spacing_valid_str_2_items(self):
        self.assertEqual(is_border_spacing('1 2').horizontal, 1 * px)
        self.assertEqual(is_border_spacing('1 2').vertical, 2 * px)

    def test_border_spacing_valid_str_2_items_with_spaces(self):
        self.assertEqual(is_border_spacing('  1  2  ').horizontal, 1 * px)
        self.assertEqual(is_border_spacing('  1  2  ').vertical, 2 * px)

    def test_border_spacing_valid_int_1_item(self):
        self.assertEqual(is_border_spacing(1).horizontal, 1 * px, )
        self.assertEqual(is_border_spacing(1).vertical, 1 * px, )

    def test_border_spacing_valid_int_2_items_sequence(self):
        # List
        self.assertEqual(is_border_spacing([1, 2]).horizontal, 1 * px)
        self.assertEqual(is_border_spacing([1, 2]).vertical, 2 * px)

        # Tuple
        self.assertEqual(is_border_spacing((1, 2)).horizontal, 1 * px)
        self.assertEqual(is_border_spacing((1, 2)).vertical, 2 * px)

    def test_border_spacing_valid_float_1_item(self):
        self.assertEqual(is_border_spacing(1.0).horizontal, 1 * px)
        self.assertEqual(is_border_spacing(1.0).vertical, 1 * px)

    def test_border_spacing_valid_float_2_items_sequence(self):
        # List
        self.assertEqual(is_border_spacing([1.0, 2.0]).horizontal, 1 * px)
        self.assertEqual(is_border_spacing([1.0, 2.0]).vertical, 2 * px)

        # Tuple
        self.assertEqual(is_border_spacing((1.0, 2.0)).horizontal, 1 * px)
        self.assertEqual(is_border_spacing((1.0, 2.0)).vertical, 2 * px)

    def test_border_spacing_invalid_units_str_2_item_commas(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('1, 2')

    def test_border_spacing_invalid_units_str_1_item(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('a a')

    def test_border_spacing_invalid_units_str_2_items(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('b')

    def test_border_spacing_invalid_units_sequence_2_items(self):
        # List
        with self.assertRaises(ValidationError):
            is_border_spacing(['a', 'b'])

        # Tuple
        with self.assertRaises(ValidationError):
            is_border_spacing(('a', 'b'))

    def test_border_spacing_invalid_length_str_0_items(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('')

    def test_border_spacing_invalid_length_str_3_items(self):
        with self.assertRaises(ValidationError):
            is_border_spacing('1 2 3')

    def test_border_spacing_invalid_length_sequence_0_items(self):
        # List
        with self.assertRaises(ValidationError):
            is_border_spacing([])

        # Tuple
        with self.assertRaises(ValidationError):
            is_border_spacing(())

    def test_border_spacing_invalid_length_sequence_3_items(self):
        # List
        with self.assertRaises(ValidationError):
            is_border_spacing([1, 2, 3])

        # tuple
        with self.assertRaises(ValidationError):
            is_border_spacing((1, 2, 3))


class RectTests(TestCase):
    """
    Comprehensive rect tests are found in the parser tests.

    This test checks basic cases work as expected.
    """

    def test_rect_valid(self):
        self.assertEqual(is_rect('rect(1px, 3px, 2px, 4px)'), Rect(1, 3, 2, 4))

    def test_rect_invalid(self):
        with self.assertRaises(ValidationError):
            is_rect('1px, 3px 2px, 4px')


class FontTests(TestCase):

    def test_font_family_name_valid(self):
        self.assertEqual(is_font_family(['Ahem', 'serif']), ['Ahem', 'serif'])
        self.assertEqual(is_font_family(["  Ahem  ", "  fantasy  "]), ["Ahem", 'fantasy'])
        self.assertEqual(is_font_family(["Ahem", "'White Space'"]), ["Ahem", 'White Space'])
        self.assertEqual(is_font_family(["Ahem", '"White Space"']), ["Ahem", 'White Space'])
        self.assertEqual(is_font_family(["  Ahem   ", "    ' White Space '  "]), ["Ahem", 'White Space'])
        self.assertEqual(is_font_family(["  Ahem   ", '    \" White Space \"  ']), ["Ahem", 'White Space'])

    def test_font_family_name_invalid(self):
        invalid_cases = [
            'Red/Black, sans-serif',
            '"Lucida" Grande, sans-serif',
            'Ahem!, sans-serif',
            'test@foo, sans-serif',
            '#POUND, sans-serif',
            'Hawaii 5-0, sans-serif',
            '123',
            'ThisIsDefintelyNotAFontFamily'
        ]
        for case in invalid_cases:
            with self.assertRaises(ValidationError):
                is_font_family([case])


class QuotesTests(TestCase):
    """
    Comprehensive quotes tests are found in the parser tests.

    This test checks basic cases work as expected.
    """

    def test_quote_valid(self):
        self.assertEqual(is_quote("'<' '>' '{' '}'"), Quotes([('<', '>'), ('{', '}')]))

    def test_quote_invalid(self):
        with self.assertRaises(ValidationError):
            is_quote("'<' '>' '{'")
