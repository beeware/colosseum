from unittest import TestCase

from colosseum.units import px
from colosseum.wrappers import BorderSpacing, Quotes


class BorderSpacingTests(TestCase):

    def test_valid_1_arg_string(self):
        border_spacing = BorderSpacing('1')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '1')
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1')")

    def test_valid_1_arg_int(self):
        border_spacing = BorderSpacing(1)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 1)
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1)")

    def test_valid_1_arg_px(self):
        border_spacing = BorderSpacing(1 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 1 * px)
        self.assertEqual(str(border_spacing), '1px')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1px)")

    def test_valid_2_arg_str(self):
        border_spacing = BorderSpacing('1', '2')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '2')
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1', '2')")

    def test_valid_2_arg_int(self):
        border_spacing = BorderSpacing(1, 2)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 2)
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1, 2)')

    def test_valid_2_arg_px(self):
        border_spacing = BorderSpacing(1 * px, 2 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 2 * px)
        self.assertEqual(str(border_spacing), '1px 2px')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1px, 2px)')

    def test_invalid_arg_number(self):
        with self.assertRaises(TypeError):
            BorderSpacing(1, 2, 3)


class QuotesTests(TestCase):

    # Valid cases
    def test_quotes_valid_1_pair(self):
        quotes = Quotes([('<', '>')])

        self.assertEqual(quotes.opening(level=0), '<')
        self.assertEqual(quotes.closing(level=0), '>')
        self.assertEqual(len(quotes), 1)
        self.assertEqual(str(quotes), "'<' '>'")
        self.assertEqual(repr(quotes), "Quotes([('<', '>')])")

    def test_quotes_valid_2_pairs(self):
        quotes = Quotes([('<', '>'), ('{', '}')])

        self.assertEqual(quotes.opening(level=0), '<')
        self.assertEqual(quotes.closing(level=0), '>')
        self.assertEqual(quotes.opening(level=1), '{')
        self.assertEqual(quotes.closing(level=1), '}')
        self.assertEqual(len(quotes), 2)
        self.assertEqual(str(quotes), "'<' '>' '{' '}'")
        self.assertEqual(repr(quotes), "Quotes([('<', '>'), ('{', '}')])")

    # Invalid cases
    def test_quotes_invalid_1_pair_level(self):
        quotes = Quotes([('<', '>')])

        with self.assertRaises(IndexError):
            quotes.opening(level=1)

        with self.assertRaises(IndexError):
            quotes.closing(level=1)
