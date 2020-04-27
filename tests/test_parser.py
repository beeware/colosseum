from itertools import permutations
from unittest import TestCase

import pytest

from colosseum import parser
from colosseum.colors import hsl, rgb
from colosseum.constants import INITIAL_FONT_VALUES
from colosseum.parser import (border, border_bottom, border_left, border_right,
                              border_top, color, outline, parse_font)
from colosseum.shapes import Rect
from colosseum.units import (ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh,
                             vmax, vmin, vw)
from colosseum.wrappers import FontFamily


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


##############################################################################
# Font tests with pytest parametrization
##############################################################################

# Constants
EMPTY = '<EMPTY>'
INVALID = '<INVALID>'


def tuple_to_font_dict(tup, font_dict, remove_empty=False):
    """Helper to convert a tuple to a font dict to check for valid outputs."""
    for idx, key in enumerate(('font_style', 'font_variant', 'font_weight',
                               'font_size', 'line_height', 'font_family')):
        value = tup[idx]

        if remove_empty:
            if value is not EMPTY:
                font_dict[key] = value
        else:
            font_dict[key] = value

        if key == 'font_family':
            font_dict[key] = FontFamily(value)

    return font_dict


# Test helpers
def construct_font(font_dict, order=0):
    """Construct font property string from a dictionary of font properties."""
    font_dict_copy = font_dict.copy()
    for key in font_dict:
        val = font_dict[key]
        if val == EMPTY:
            val = ''

        if key == 'line_height' and val != '':
            val = '/' + val

        font_dict_copy[key] = val

    font_dict_copy['font_family'] = FontFamily(font_dict_copy['font_family'])

    strings = {
        # Valid default order
        0: '{font_style} {font_variant} {font_weight} {font_size}{line_height} {font_family}',

        # Valid non default order
        1: '{font_style} {font_weight} {font_variant} {font_size}{line_height} {font_family}',
        2: '{font_weight} {font_variant} {font_style} {font_size}{line_height} {font_family}',
        3: '{font_weight} {font_style} {font_variant} {font_size}{line_height} {font_family}',
        4: '{font_variant} {font_weight} {font_style} {font_size}{line_height} {font_family}',
        5: '{font_variant} {font_style} {font_weight} {font_size}{line_height} {font_family}',

        # Invalid order
        10: '{font_size}{line_height} {font_style} {font_weight} {font_variant} {font_family}',
        11: '{font_weight} {font_size}{line_height} {font_variant} {font_style} {font_family}',
        12: '{font_weight} {font_style} {font_size}{line_height} {font_variant} {font_family}',
        13: '{font_style} {font_weight} {font_size}{line_height} {font_variant} {font_family}',
        14: '{font_weight} {font_variant} {font_size}{line_height} {font_style} {font_family}',
        15: '{font_variant} {font_weight} {font_size}{line_height} {font_style} {font_family}',
        16: '{font_style} {font_variant} {font_size}{line_height} {font_weight} {font_family}',
        17: '{font_variant} {font_style} {font_size}{line_height} {font_weight} {font_family}',
        18: '{font_variant} {font_style} {font_family} {font_size}{line_height} {font_weight}',
        19: '{font_family} {font_variant} {font_style} {font_size}{line_height} {font_weight}',
    }
    string = ' '.join(str(strings[order].format(**font_dict_copy)).strip().split())
    return string


def helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family):
    font_with_empty_values = tuple_to_font_dict(
        (font_style, font_variant, font_weight, font_size, line_height, font_family),
        INITIAL_FONT_VALUES.copy(),
        remove_empty=False)

    font_properties = set()
    for order in range(6):
        font_property = construct_font(font_with_empty_values, order)
        if font_property not in font_properties:
            font_properties.add(font_property)
            with pytest.raises(Exception):
                print(font_with_empty_values)
                print('Font: ' + font_property)
                parse_font(font_property)


# Tests
@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_2_to_5_parts(font_style, font_variant, font_weight, font_size, line_height,
                                           font_family):
    font_with_empty_values = tuple_to_font_dict(
        (font_style, font_variant, font_weight, font_size, line_height, font_family),
        INITIAL_FONT_VALUES.copy(),
        remove_empty=False)

    expected_output = tuple_to_font_dict(
        (font_style, font_variant, font_weight, font_size, line_height, font_family),
        INITIAL_FONT_VALUES.copy(),
        remove_empty=True)

    # Valid
    font_properties = set()
    for order in range(6):
        font_property = construct_font(font_with_empty_values, order)
        if font_property not in font_properties:
            font_properties.add(font_property)
            font = parse_font(font_property)
            print('\nfont:     ', font_property)
            print('parsed:   ', sorted(font.items()))
            print('expected: ', sorted(expected_output.items()))
            assert font == expected_output

    # Invalid
    font_properties_invalid = set()
    for order in range(10, 20):
        font_property = construct_font(font_with_empty_values, order)
        if font_property not in font_properties:
            font_properties_invalid.add(font_property)
            print('\nfont:     ', font_property)
            with pytest.raises(Exception):
                font = parse_font(font_property)


@pytest.mark.parametrize('font_style', [INVALID])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_invalid_1(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [INVALID])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_invalid_2(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [INVALID])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_invalid_3(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', [INVALID])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_invalid_4(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [INVALID])
@pytest.mark.parametrize('font_family', [['Ahem'], ['Ahem', 'White Space']])
def test_parse_font_shorthand_invalid_5(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_style', [EMPTY, 'normal', 'oblique'])
@pytest.mark.parametrize('font_variant', [EMPTY, 'normal', 'small-caps'])
@pytest.mark.parametrize('font_weight', [EMPTY, 'normal', 'bold', '500'])
@pytest.mark.parametrize('font_size', ['medium', '9px'])
@pytest.mark.parametrize('line_height', [EMPTY, 'normal', '2'])
@pytest.mark.parametrize('font_family', [[INVALID], ['Ahem', INVALID]])
def test_parse_font_shorthand_invalid_6(font_style, font_variant, font_weight, font_size, line_height, font_family):
    helper_test_font_invalid(font_style, font_variant, font_weight, font_size, line_height, font_family)


@pytest.mark.parametrize('font_property_string', [
    INVALID,
    # Space between font-size and line-height
    'small-caps oblique normal 1.2em /3 Ahem',
    'small-caps oblique normal 1.2em/ 3 Ahem',
    'small-caps oblique normal 1.2em / 3 Ahem',

    # Too many parts
    'normal normal normal normal 12px/12px serif',
    'normal normal normal normal normal 12px/12px serif',

    # No quotes with spaces
    'small-caps oblique normal 1.2em/3 Ahem, White Space',

    # No commas
    'small-caps oblique normal 1.2em/3 Ahem "White Space"',

    # Repeated options
    'bold 500 oblique 9px/2 Ahem',
    'bigger smaller Ahem',

    # <system-font> | inherit
    'Ahem',
    '<NotValid>',
    '20',
    20,
])
def test_parse_font_shorthand_invalid_extras(font_property_string):
    with pytest.raises(Exception):
        print('Font: ' + font_property_string)
        parse_font(font_property_string)


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
            'outline_color': color('black'),
            'outline_width': 'thick',
        }
        perms = permutations(['black', 'solid', 'thick'], 3)
        for perm in perms:
            value = ' '.join(perm)
            output = outline(value)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_str_2_parts(self):
        black = color('black')
        expected_outputs = {
            ('black', 'solid'): {'outline_color': black, 'outline_style': 'solid'},
            ('black', 'thick'): {'outline_color': black, 'outline_width': 'thick'},
            ('solid', 'thick'): {'outline_style': 'solid', 'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 2)
        for perm in perms:
            expected_output = expected_outputs[tuple(sorted(perm))]
            value = ' '.join(perm)
            output = outline(value)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_str_1_part(self):
        expected_outputs = {
            'black': {'outline_color': color('black')},
            'solid': {'outline_style': 'solid'},
            'thick': {'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 1)
        for perm in perms:
            value = ' '.join(perm)
            expected_output = expected_outputs[value]
            output = outline(value)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_3_parts(self):
        expected_output = {
            'outline_style': 'solid',
            'outline_color': color('black'),
            'outline_width': 'thick',
        }
        perms = permutations(['black', 'solid', 'thick'], 3)
        for perm in perms:
            value = perm
            output = outline(value)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_2_parts(self):
        black = color('black')
        expected_outputs = {
            ('black', 'solid'): {'outline_color': black, 'outline_style': 'solid'},
            ('black', 'thick'): {'outline_color': black, 'outline_width': 'thick'},
            ('solid', 'thick'): {'outline_style': 'solid', 'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 2)
        for perm in perms:
            expected_output = expected_outputs[tuple(sorted(perm))]
            value = perm
            output = outline(value)
            self.assertEqual(output, expected_output)

    def test_parse_outline_shorthand_valid_list_1_part(self):
        expected_outputs = {
            'black': {'outline_color': color('black')},
            'solid': {'outline_style': 'solid'},
            'thick': {'outline_width': 'thick'},
        }
        perms = permutations(['black', 'solid', 'thick'], 1)
        for perm in perms:
            value = perm
            expected_output = expected_outputs[value[0]]
            output = outline(value)
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


class ParseBorderTests(TestCase):

    # Valid cases
    def test_parse_border_shorthand_valid_str_3_parts(self):
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_output = {
                'border_{direction}width'.format(direction=direction): 'thick',
                'border_{direction}style'.format(direction=direction): 'solid',
                'border_{direction}color'.format(direction=direction): color('black'),
            }
            perms = permutations(['black', 'solid', 'thick'], 3)
            for perm in perms:
                value = ' '.join(perm)
                output = func(value)
                self.assertEqual(output, expected_output)

    def test_parse_border_shorthand_valid_str_2_parts(self):
        black = color('black')
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_outputs = {
                ('black', 'solid'): {'border_{direction}color'.format(direction=direction): black,
                                     'border_{direction}style'.format(direction=direction): 'solid'},
                ('black', 'thick'): {'border_{direction}color'.format(direction=direction): black,
                                     'border_{direction}width'.format(direction=direction): 'thick'},
                ('solid', 'thick'): {'border_{direction}style'.format(direction=direction): 'solid',
                                     'border_{direction}width'.format(direction=direction): 'thick'},
            }
            perms = permutations(['black', 'solid', 'thick'], 2)
            for perm in perms:
                expected_output = expected_outputs[tuple(sorted(perm))]
                value = ' '.join(perm)
                output = func(value)
                self.assertEqual(output, expected_output)

    def test_parse_border_shorthand_valid_str_1_part(self):
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_outputs = {
                'black': {'border_{direction}color'.format(direction=direction): color('black')},
                'solid': {'border_{direction}style'.format(direction=direction): 'solid'},
                'thick': {'border_{direction}width'.format(direction=direction): 'thick'},
            }
            perms = permutations(['black', 'solid', 'thick'], 1)
            for perm in perms:
                value = ' '.join(perm)
                expected_output = expected_outputs[value]
                output = func(value)
                self.assertEqual(output, expected_output)

    def test_parse_border_shorthand_valid_list_3_parts(self):
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_output = {
                'border_{direction}style'.format(direction=direction): 'solid',
                'border_{direction}color'.format(direction=direction): color('black'),
                'border_{direction}width'.format(direction=direction): 'thick',
            }
            perms = permutations(['black', 'solid', 'thick'], 3)
            for perm in perms:
                value = perm
                output = func(value)
                self.assertEqual(output, expected_output)

    def test_parse_border_shorthand_valid_list_2_parts(self):
        black = color('black')
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_outputs = {
                ('black', 'solid'): {'border_{direction}color'.format(direction=direction): black,
                                     'border_{direction}style'.format(direction=direction): 'solid'},
                ('black', 'thick'): {'border_{direction}color'.format(direction=direction): black,
                                     'border_{direction}width'.format(direction=direction): 'thick'},
                ('solid', 'thick'): {'border_{direction}style'.format(direction=direction): 'solid',
                                     'border_{direction}width'.format(direction=direction): 'thick'},
            }
            perms = permutations(['black', 'solid', 'thick'], 2)
            for perm in perms:
                expected_output = expected_outputs[tuple(sorted(perm))]
                value = perm
                output = func(value)
                self.assertEqual(output, expected_output)

    def test_parse_border_shorthand_valid_list_1_part(self):
        for direction, func in {'bottom_': border_bottom,
                                'left_': border_left,
                                'right_': border_right,
                                'top_': border_top,
                                '': border}.items():
            expected_outputs = {
                'black': {'border_{direction}color'.format(direction=direction): color('black')},
                'solid': {'border_{direction}style'.format(direction=direction): 'solid'},
                'thick': {'border_{direction}width'.format(direction=direction): 'thick'},
            }
            perms = permutations(['black', 'solid', 'thick'], 1)
            for perm in perms:
                value = perm
                expected_output = expected_outputs[value[0]]
                output = func(value)
                self.assertEqual(output, expected_output)

    # Invalid cases
    def test_parse_border_shorthand_invalid_empty(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                border('')

            with self.assertRaises(ValueError):
                border([])

    def test_parse_border_shorthand_invalid_value(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                border('foobar')

            with self.assertRaises(ValueError):
                border(2)

            with self.assertRaises(ValueError):
                border("#f")

    def test_parse_border_shorthand_invalid_duplicates_color(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                func('black black')

            with self.assertRaises(ValueError):
                func('black black black')

            with self.assertRaises(ValueError):
                func('black red blue')

    def test_parse_border_shorthand_invalid_duplicates_style(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                func('solid solid')

            with self.assertRaises(ValueError):
                func('solid solid solid')

    def test_parse_border_shorthand_invalid_duplicates_width(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                func('thick thick')

            with self.assertRaises(ValueError):
                func('thick thick thick')

    def test_parse_border_shorthand_invalid_too_many_items(self):
        for func in [border, border_bottom, border_left, border_right, border_top]:
            with self.assertRaises(ValueError):
                func('black solid thick black')

            with self.assertRaises(ValueError):
                func('black solid thick black thick')
