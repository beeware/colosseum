from unittest import TestCase
from colosseum import parser
from colosseum.colors import hsl, rgb
from colosseum.constants import SYSTEM_FONT_KEYWORDS
from colosseum.exceptions import ValidationError
from colosseum.parser import parse_font
from colosseum.units import (ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh,
                             vmax, vmin, vw)
from .utils import ColosseumTestCase


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


class ParseFontTests(ColosseumTestCase):
    TEST_CASES = {
        r'12px/14px sans-serif': {
            'font_style': 'normal',
            'font_variant': 'normal',
            'font_weight': 'normal',
            'font_size': '12px',
            'line_height': '14px',
            'font_family': ['sans-serif'],
            },
        r'80% sans-serif': {
            'font_style': 'normal',
            'font_variant': 'normal',
            'font_weight': 'normal',
            'font_size': '80%',
            'line_height': 'normal',
            'font_family': ['sans-serif'],
            },
        r'bold italic large Ahem, serif': {
            'font_style': 'italic',
            'font_variant': 'normal',
            'font_weight': 'bold',
            'font_size': 'large',
            'line_height': 'normal',
            'font_family': ['Ahem', 'serif'],
            },
        r'normal small-caps 120%/120% fantasy': {
            'font_style': 'normal',
            'font_variant': 'small-caps',
            'font_weight': 'normal',
            'font_size': '120%',
            'line_height': '120%',
            'font_family': ['fantasy'],
            },
        r'x-large/110% Ahem,serif': {
            'font_style': 'normal',
            'font_variant': 'normal',
            'font_weight': 'normal',
            'font_size': 'x-large',
            'line_height': '110%',
            'font_family': ['Ahem', 'serif'],
            },
    }

    def test_parse_font_shorthand(self):
        for case in sorted(self.TEST_CASES):
            expected_output = self.TEST_CASES[case]
            font = parse_font(case)
            self.assertEqual(font, expected_output)

        # Test extra spaces
        parse_font(r'  normal    normal    normal    12px/12px   serif  ')
        parse_font(r'  normal    normal    normal    12px/12px     Ahem  ,   serif  ')

        # Test valid single part
        for part in SYSTEM_FONT_KEYWORDS:
            parse_font(part)

    def test_parse_font_shorthand_invalid(self):
        # This font string has too many parts
        with self.assertRaises(ValidationError):
            parse_font(r'normal normal normal normal 12px/12px serif')

        # This invalid single part
        for part in ['normal', 'foobar']:
            with self.assertRaises(ValidationError):
                parse_font(part)

    def test_parse_font_part(self):
        pass
        #  - <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-style> <font-variant> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-weight> <font-style> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-style> <font-weight> <font-size>/<line-height> <font-family>

    def test_parse_font(self):
        pass
        # 5 parts with line height
        #  - <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        #  - <font-style> <font-weight> <font-variant> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-weight> <font-style> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-style> <font-weight> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-style> <font-variant> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-variant> <font-style> <font-size>/<line-height> <font-family>

        # 5 parts
        #  - <font-style> <font-variant> <font-weight> <font-size> <font-family>
        #  - <font-style> <font-weight> <font-variant> <font-size> <font-family>
        #  - <font-variant> <font-weight> <font-style> <font-size> <font-family>
        #  - <font-variant> <font-style> <font-weight> <font-size> <font-family>
        #  - <font-weight> <font-style> <font-variant> <font-size> <font-family>
        #  - <font-weight> <font-variant> <font-style> <font-size> <font-family>

        # 4 parts with height
        #  - <font-style> <font-variant> <font-size>/<line-height> <font-family>
        #  - <font-style> <font-weight> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-style> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-style> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-variant> <font-size>/<line-height> <font-family>

        # 4 parts
        #  - <font-style> <font-variant> <font-size> <font-family>
        #  - <font-style> <font-weight> <font-size> <font-family>
        #  - <font-variant> <font-weight> <font-size> <font-family>
        #  - <font-variant> <font-style> <font-size> <font-family>
        #  - <font-weight> <font-style> <font-size> <font-family>
        #  - <font-weight> <font-variant> <font-size> <font-family>

        # 3 parts with height
        #  - <font-style> <font-size>/<line-height> <font-family>
        #  - <font-variant> <font-size>/<line-height> <font-family>
        #  - <font-weight> <font-size>/<line-height> <font-family>

        # 3 parts with height
        #  - <font-style> <font-size> <font-family>
        #  - <font-variant> <font-size> <font-family>
        #  - <font-weight> <font-size> <font-family>

        # 2 parts with height
        #  - <font-size>/<line-height> <font-family>

        # 2 parts
        #  - <font-size> <font-family>

        # 1 part
