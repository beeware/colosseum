from itertools import permutations
from unittest import TestCase

from colosseum import parser
from colosseum.colors import hsl, rgb
from colosseum.parser import outline
from colosseum.shapes import Rect
from colosseum.units import (
    ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh, vmax, vmin, vw,
)


class ParseUnitTests(TestCase):
    def assertEqualUnits(self, value, expected):
        # Nothing fancy - a unit is equal if
        # it's the same unit type, with the same value.
        actual = parser.units(value)
        self.assertEqual(actual.suffix, expected.suffix)
        self.assertEqual(actual.val, expected.val)

    def test_unit_types(self):
        self.assertEqualUnits('10ch', 10 * ch)
        self.assertEqualUnits('10cm', 10 * cm)
        self.assertEqualUnits('10em', 10 * em)
        self.assertEqualUnits('10ex', 10 * ex)
        self.assertEqualUnits('10in', 10 * inch)
        self.assertEqualUnits('10mm', 10 * mm)
        self.assertEqualUnits('10pc', 10 * pc)
        self.assertEqualUnits('10%', 10 * percent)
        self.assertEqualUnits('10pt', 10 * pt)
        self.assertEqualUnits('10px', 10 * px)
        self.assertEqualUnits('10vh', 10 * vh)
        self.assertEqualUnits('10vmax', 10 * vmax)
        self.assertEqualUnits('10vmin', 10 * vmin)
        self.assertEqualUnits('10vw', 10 * vw)

    def test_unit(self):
        self.assertEqualUnits(10 * pt, 10 * pt)

    def test_float(self):
        self.assertEqualUnits('10.0pt', 10 * pt)
        self.assertEqualUnits('10.0 pt', 10 * pt)

    def test_int(self):
        self.assertEqualUnits('10pt', 10 * pt)
        self.assertEqualUnits('10 pt', 10 * pt)

    def test_raw(self):
        self.assertEqualUnits(10, 10 * px)
        self.assertEqualUnits(10.0, 10 * px)

    def test_no_units(self):
        self.assertEqualUnits('10', 10 * px)
        self.assertEqualUnits('10.0', 10 * px)

    def test_non_value(self):
        # A string that isn't a unit declaration
        with self.assertRaises(ValueError):
            parser.units('hello')

        # Check a value that ends with a valid unit
        with self.assertRaises(ValueError):
            parser.units('church')


class ParseColorTests(TestCase):
    def assertEqualHSL(self, value, expected):
        # Nothing fancy - a color is equal if
        actual = parser.color(value)
        self.assertEqual(actual.h, expected.h)
        self.assertEqual(actual.s, expected.s)
        self.assertEqual(actual.l, expected.l)
        self.assertAlmostEqual(actual.a, expected.a, places=3)

    def assertEqualColor(self, value, expected):
        # Nothing fancy - a color is equal if
        actual = parser.color(value)
        self.assertEqual(actual.r, expected.r)
        self.assertEqual(actual.g, expected.g)
        self.assertEqual(actual.b, expected.b)
        self.assertAlmostEqual(actual.a, expected.a, places=3)

    def test_noop(self):
        self.assertEqualColor(rgb(1, 2, 3, 0.5), rgb(1, 2, 3, 0.5))
        self.assertEqualHSL(hsl(1, 0.2, 0.3), hsl(1, 0.2, 0.3))

    def test_rgb(self):
        self.assertEqualColor('rgb(1,2,3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb(1, 2, 3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb( 1 , 2 , 3)', rgb(1, 2, 3))

        self.assertEqualColor('#123', rgb(0x11, 0x22, 0x33))
        self.assertEqualColor('#112233', rgb(0x11, 0x22, 0x33))

        with self.assertRaises(ValueError):
            parser.color('rgb(10, 20)')

        with self.assertRaises(ValueError):
            parser.color('rgb(a, 10, 20)')

        with self.assertRaises(ValueError):
            parser.color('rgb(10, b, 20)')

        with self.assertRaises(ValueError):
            parser.color('rgb(10, 20, c)')

        with self.assertRaises(ValueError):
            parser.color('rgb(10, 20, 30, 0.5)')

    def test_rgba(self):
        self.assertEqualColor('rgba(1,2,3,0.5)', rgb(1, 2, 3, 0.5))
        self.assertEqualColor('rgba(1, 2, 3, 0.5)', rgb(1, 2, 3, 0.5))
        self.assertEqualColor('rgba( 1 , 2 , 3 , 0.5)', rgb(1, 2, 3, 0.5))

        self.assertEqualColor('#1234', rgb(0x11, 0x22, 0x33, 0.2666))
        self.assertEqualColor('#11223344', rgb(0x11, 0x22, 0x33, 0.2666))

        with self.assertRaises(ValueError):
            parser.color('rgba(10, 20, 30)')

        with self.assertRaises(ValueError):
            parser.color('rgba(a, 10, 20, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('rgba(10, b, 20, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('rgba(10, 20, c, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('rgba(10, 20, 30, c)')

        with self.assertRaises(ValueError):
            parser.color('rgba(10, 20, 30, 0.5, 5)')

    def test_hsl(self):
        self.assertEqualHSL('hsl(1,20%,30%)', hsl(1, 0.2, 0.3))
        self.assertEqualHSL('hsl(1, 20%, 30%)', hsl(1, 0.2, 0.3))
        self.assertEqualHSL('hsl( 1, 20% , 30%)', hsl(1, 0.2, 0.3))

        with self.assertRaises(ValueError):
            parser.color('hsl(1, 20%)')

        with self.assertRaises(ValueError):
            parser.color('hsl(a, 20%, 30%)')

        with self.assertRaises(ValueError):
            parser.color('hsl(1, a, 30%)')

        with self.assertRaises(ValueError):
            parser.color('hsl(1, 20%, a)')

        with self.assertRaises(ValueError):
            parser.color('hsl(1, 20%, 30%, 0.5)')

    def test_hsla(self):
        self.assertEqualHSL('hsla(1,20%,30%,0.5)', hsl(1, 0.2, 0.3, 0.5))
        self.assertEqualHSL('hsla(1, 20%, 30%, 0.5)', hsl(1, 0.2, 0.3, 0.5))
        self.assertEqualHSL('hsla( 1, 20% , 30% , 0.5)', hsl(1, 0.2, 0.3, 0.5))

        with self.assertRaises(ValueError):
            parser.color('hsla(1, 20%, 30%)')

        with self.assertRaises(ValueError):
            parser.color('hsla(a, 20%, 30%, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('hsla(1, a, 30%, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('hsla(1, 20%, a, 0.5)')

        with self.assertRaises(ValueError):
            parser.color('hsla(1, 20%, 30%, a)')

        with self.assertRaises(ValueError):
            parser.color('hsla(1, 20%, 30%, 0.5, 5)')

    def test_named_color(self):
        self.assertEqualColor('Red', rgb(0xFF, 0, 0))
        self.assertEqualColor('RED', rgb(0xFF, 0, 0))
        self.assertEqualColor('red', rgb(0xFF, 0, 0))
        self.assertEqualColor('rEd', rgb(0xFF, 0, 0))

        self.assertEqualColor('CornflowerBlue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('cornflowerblue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('CORNFLOWERBLUE', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('Cornflowerblue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('CoRnFlOwErBlUe', rgb(0x64, 0x95, 0xED))

        with self.assertRaises(ValueError):
            parser.color('not a color')


class ParseRectTests(TestCase):

    def test_rect_valid_commas(self):
        expected_rect = Rect(1 * px, 3 * px, 2 * px, 4 * px)

        # Comma separated without units
        self.assertEqual(parser.rect('rect(1, 3, 2, 4)'), expected_rect)

        # Comma separated with units
        self.assertEqual(parser.rect('rect(1px, 3px, 2px, 4px)'), expected_rect)

        # Comma separated with units and extra spaces
        self.assertEqual(parser.rect('  rect(  1px  ,  3px  ,  2px,  4px  )  '), expected_rect)

    def test_rect_valid_spaces(self):
        expected_rect = Rect(1 * px, 3 * px, 2 * px, 4 * px)

        # Space separated without units
        self.assertEqual(parser.rect('rect(1 3 2 4)'), expected_rect)

        # Space separated wit units
        self.assertEqual(parser.rect('rect(1px 3px 2px 4px)'), expected_rect)

        # Space separated with units and extra spaces
        self.assertEqual(parser.rect('  rect(  1px  3px  2px  4px  )  '), expected_rect)

    def test_rect_invalid_mix_commas_spaces(self):
        # Mix of commas and spaces
        with self.assertRaises(ValueError):
            parser.rect('rect(1px, 3px, 2px 4px)')

        with self.assertRaises(ValueError):
            parser.rect('rect(a b, c d)')

    def test_rect_invalid_number_of_arguments_empty(self):
        with self.assertRaises(ValueError):
            parser.rect('rect()')

    def test_rect_invalid_number_of_arguments_1_arg(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(1px)')

    def test_rect_invalid_number_of_arguments_2_args(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(1px, 3px)')

    def test_rect_invalid_number_of_arguments_3_args(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(1px, 3px, 2px)')

    def test_rect_invalid_number_of_arguments_5_args(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(1px, 3px, 2px, 5px, 7px)')

    def test_rect_invalid_missing_parens(self):
        # Missing parens
        with self.assertRaises(ValueError):
            parser.rect('rect a b c d)')

        with self.assertRaises(ValueError):
            parser.rect('rect(a b c d')

        with self.assertRaises(ValueError):
            parser.rect('rect a b c d')

    def test_rect_invalid_extra_parens(self):
        # Missing parens
        with self.assertRaises(ValueError):
            parser.rect('rect((a b c d)')

        # Missing parens
        with self.assertRaises(ValueError):
            parser.rect('rect(a b c d))')

    def test_rect_invalid_missing_rect(self):
        # Other values
        with self.assertRaises(ValueError):
            parser.rect('(1px, 3px, 2px, 4px)')

        with self.assertRaises(ValueError):
            parser.rect('1px, 3px, 2px, 4px')

        with self.assertRaises(ValueError):
            parser.rect('1px 3px 2px 4px')

        with self.assertRaises(ValueError):
            parser.rect('(1px 3px 2px 4px)')

    def test_rect_invalid_units(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(a, b, c, d)')

    def test_rect_invalid_case(self):
        with self.assertRaises(ValueError):
            parser.rect('rect(1PX, 3px, 2px, 4px)')

        with self.assertRaises(ValueError):
            parser.rect('RECT(1px, 3px, 2px, 4px)')


class ParseQuotesTests(TestCase):

    # Valid cases
    def test_quotes_valid_string_2_items(self):
        value = "'«' '»'"
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), value)

    def test_quotes_valid_string_4_items(self):
        value = "'«' '»' '(' ')'"
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), value)

    def test_quotes_valid_sequence_2_items(self):
        expected_output = "'«' '»'"

        value = ['«', '»']
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

        value = ('«', '»')
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

    def test_quotes_valid_sequence_4_items(self):
        expected_output = "'«' '»' '(' ')'"

        value = ['«', '»', '(', ')']
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

        value = ('«', '»', '(', ')')
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

    def test_quotes_valid_list_1_pair(self):
        value = [('«', '»')]
        expected_output = "'«' '»'"
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

    def test_quotes_valid_list_2_pairs(self):
        value = [('«', '»'), ('(', ')')]
        expected_output = "'«' '»' '(' ')'"
        quotes = parser.quotes(value)
        self.assertEqual(str(quotes), expected_output)

    # Invalid cases
    def test_quotes_invalid_string_empty_item(self):
        with self.assertRaises(ValueError):
            parser.quotes('')

    def test_quotes_invalid_string_empty_pair(self):
        with self.assertRaises(ValueError):
            parser.quotes('"" ""')

    def test_quotes_invalid_list_empty_pair(self):
        with self.assertRaises(ValueError):
            parser.quotes([('', '')])

    def test_quotes_invalid_string_1_item(self):
        with self.assertRaises(ValueError):
            parser.quotes('"«"')

    def test_quotes_invalid_string_1_item_incomplete_quotes(self):
        with self.assertRaises(ValueError):
            parser.quotes('"«')

    def test_quotes_invalid_string_3_item(self):
        with self.assertRaises(ValueError):
            parser.quotes('"«" ">" "<"')

    def test_quotes_invalid_string_3_item_incomplete_quotes(self):
        with self.assertRaises(ValueError):
            parser.quotes('"«" ">" "<')

    def test_quotes_invalid_string_2_items_no_quotes(self):
        with self.assertRaises(ValueError):
            parser.quotes('< >')

    def test_quotes_invalid_string_4_items_no_quotes(self):
        with self.assertRaises(ValueError):
            parser.quotes('< > { }')


class ParseOutlineTests(TestCase):

    # Valid cases
    def test_parse_outline_shorthand_valid_str_3_parts(self):
        expected_output = {
            'outline_style': 'solid',
            'outline_color': 'rgba(0, 0, 0, 1.0)',
            'outline_width': 'thick',
        }
        perms = permutations(['black', 'solid', 'thick'], 3)
        for perm in perms:
            value = ' '.join(perm)
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_str_2_parts(self):
        expected_outputs = {
            ('black', 'solid'): {'outline_color': 'rgba(0, 0, 0, 1.0)', 'outline_style': 'solid'},
            ('black', 'thick'): {'outline_color': 'rgba(0, 0, 0, 1.0)', 'outline_width': 'thick'},
            ('solid', 'thick'): {'outline_style': 'solid', 'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 2)
        for perm in perms:
            expected_output = expected_outputs[tuple(sorted(perm))]
            value = ' '.join(perm)
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_str_1_part(self):
        expected_outputs = {
            'black': {'outline_color': 'rgba(0, 0, 0, 1.0)'},
            'solid': {'outline_style': 'solid'},
            'thick': {'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 1)
        for perm in perms:
            value = ' '.join(perm)
            expected_output = expected_outputs[value]
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_3_parts(self):
        expected_output = {
            'outline_style': 'solid',
            'outline_color': 'rgba(0, 0, 0, 1.0)',
            'outline_width': 'thick',
        }
        perms = permutations(['black', 'solid', 'thick'], 3)
        for perm in perms:
            value = perm
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_2_parts(self):
        expected_outputs = {
            ('black', 'solid'): {'outline_color': 'rgba(0, 0, 0, 1.0)', 'outline_style': 'solid'},
            ('black', 'thick'): {'outline_color': 'rgba(0, 0, 0, 1.0)', 'outline_width': 'thick'},
            ('solid', 'thick'): {'outline_style': 'solid', 'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 2)
        for perm in perms:
            expected_output = expected_outputs[tuple(sorted(perm))]
            value = perm
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_1_part(self):
        expected_outputs = {
            'black': {'outline_color': 'rgba(0, 0, 0, 1.0)'},
            'solid': {'outline_style': 'solid'},
            'thick': {'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 1)
        for perm in perms:
            value = perm
            expected_output = expected_outputs[value[0]]
            output = outline(value)
            print(value, output, expected_output)
            self.assertEqual(output, expected_output)

    # Invalid cases
    def test_parse_outline_shorthand_invalid_empty(self):
        with self.assertRaises(ValueError):
            outline('')

        with self.assertRaises(ValueError):
            outline([])

    def test_parse_outline_shorthand_invalid_value(self):
        with self.assertRaises(ValueError):
            outline('foobar')

        with self.assertRaises(ValueError):
            outline(2)

        with self.assertRaises(ValueError):
            outline("#f")

    def test_parse_outline_shorthand_invalid_duplicates_color(self):
        with self.assertRaises(ValueError):
            outline('black black')

        with self.assertRaises(ValueError):
            outline('black black black')

        with self.assertRaises(ValueError):
            outline('black red blue')

    def test_parse_outline_shorthand_invalid_duplicates_style(self):
        with self.assertRaises(ValueError):
            outline('solid solid')

        with self.assertRaises(ValueError):
            outline('solid solid solid')

    def test_parse_outline_shorthand_invalid_duplicates_width(self):
        with self.assertRaises(ValueError):
            outline('thick thick')

        with self.assertRaises(ValueError):
            outline('thick thick thick')

    def test_parse_outline_shorthand_invalid_too_many_items(self):
        with self.assertRaises(ValueError):
            outline('black solid thick black')

        with self.assertRaises(ValueError):
            outline('black solid thick black thick')
