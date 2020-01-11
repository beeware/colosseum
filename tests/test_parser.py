from unittest import TestCase

from colosseum import parser
from colosseum.colors import hsl, rgb
from colosseum.parser import construct_font, construct_font_family, parse_font
from colosseum.units import (
    ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh, vmax, vmin, vw,
)

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
    CASE_5 = {
        # <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        'oblique small-caps bold 1.2em/3 Ahem': ('oblique', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal small-caps bold 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'oblique normal bold 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'oblique small-caps normal 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'normal small-caps normal 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'oblique normal normal 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'normal normal bold 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal normal normal 1.2em/3 Ahem': ('normal', 'normal', 'normal', '1.2em', '3', ['Ahem']),

        # <font-weight> <font-style> <font-variant> <font-size>/<line-height> <font-family>
        'bold oblique small-caps 1.2em/3 Ahem': ('oblique', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal oblique small-caps 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'bold normal small-caps 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'bold oblique normal 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal oblique normal 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'bold normal normal 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal normal small-caps 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),

        # <font-variant> <font-weight> <font-style> <font-size>/<line-height> <font-family>
        'small-caps bold oblique 1.2em/3 Ahem': ('oblique', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal bold oblique 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'small-caps normal oblique 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'small-caps bold normal 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal bold normal 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'small-caps normal normal 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'normal normal oblique 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),

        # <font-variant> <font-style> <font-weight> <font-size>/<line-height> <font-family>
        'small-caps oblique bold 1.2em/3 Ahem': ('oblique', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal oblique bold 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'small-caps normal bold 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'small-caps oblique normal 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
    }
    CASE_4 = {
        # <font-style> <font-variant> <font-size>/<line-height> <font-family>
        'oblique small-caps 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'oblique normal 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'normal small-caps 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'normal normal 1.2em/3 Ahem': ('normal', 'normal', 'normal', '1.2em', '3', ['Ahem']),

        #  <font-style> <font-weight> <font-size>/<line-height> <font-family>
        'oblique bold 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal bold 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),

        # <font-weight> <font-style> <font-size>/<line-height> <font-family>
        'bold oblique 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'bold normal 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal oblique 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),

        # <font-weight> <font-variant> <font-size>/<line-height> <font-family>
        'bold small-caps 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
    }
    CASE_3 = {
        # <font-style> <font-size>/<line-height> <font-family>
        'oblique 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'normal 1.2em/3 Ahem': ('normal', 'normal', 'normal', '1.2em', '3', ['Ahem']),

        # <font-variant> <font-size>/<line-height> <font-family>
        'small-caps 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),

        # <font-weight> <font-size>/<line-height> <font-family>
        'bold 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),

        # <font-style> <font-size> <font-family>
        'oblique 1.2em Ahem': ('oblique', 'normal', 'normal', '1.2em', 'normal', ['Ahem']),

        # <font-variant> <font-size> <font-family>
        'small-caps 1.2em Ahem': ('normal', 'small-caps', 'normal', '1.2em', 'normal', ['Ahem']),

        # <font-weight> <font-size> <font-family>
        'bold 1.2em Ahem': ('normal', 'normal', 'bold', '1.2em', 'normal', ['Ahem']),
    }
    CASE_2 = {
        #  <font-size>/<line-height> <font-family>
        '1.2em/3 Ahem': ('normal', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        '1.2em/3 Ahem, "White Space"': ('normal', 'normal', 'normal', '1.2em', '3',
                                        ['Ahem', 'White Space']),
        '1.2em/3 Ahem, "White Space", serif': ('normal', 'normal', 'normal', '1.2em', '3',
                                               ['Ahem', 'White Space', 'serif']),

        #  <font-size> <font-family>
        '1.2em Ahem': ('normal', 'normal', 'normal', '1.2em', 'normal', ['Ahem']),
        '1.2em Ahem, "White Space"': ('normal', 'normal', 'normal', '1.2em', 'normal',
                                      ['Ahem', 'White Space']),
        '1.2em Ahem, "White Space", serif': ('normal', 'normal', 'normal', '1.2em', 'normal',
                                             ['Ahem', 'White Space', 'serif']),
    }
    CASE_1 = {
        #  <system-font> | inherit
        'caption': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'icon': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'menu': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'message-box': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'small-caption': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'status-bar': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
        'inherit': ('normal', 'normal', 'normal', 'medium', 'normal', ['initial']),
    }
    CASE_EXTRAS = {
        # Spaces in family
        'normal normal normal 1.2em/3 Ahem, "White Space"': ('normal', 'normal', 'normal', '1.2em', '3',
                                                             ['Ahem', 'White Space']),
        "normal normal normal 1.2em/3 Ahem, 'White Space'": ('normal', 'normal', 'normal', '1.2em', '3',
                                                             ['Ahem', 'White Space']),
        # Extra spaces
        " normal  normal  normal  1.2em/3  Ahem,   '  White   Space ' ": ('normal', 'normal', 'normal', '1.2em', '3',
                                                                          ['Ahem', 'White Space']),
    }
    CASE_5_INVALID = set([
        # <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        '<NotValid> small-caps bold 1.2em/3 Ahem',
        '<NotValid> small-caps bold 1.2em/3 Ahem',
        '<NotValid> normal bold 1.2em/3 Ahem',
        '<NotValid> small-caps normal 1.2em/3 Ahem',
        '<NotValid> small-caps normal 1.2em/3 Ahem',
        '<NotValid> normal normal 1.2em/3 Ahem',
        '<NotValid> normal bold 1.2em/3 Ahem',

        'oblique <NotValid> bold 1.2em/3 Ahem',
        'normal <NotValid> bold 1.2em/3 Ahem',
        'oblique <NotValid> 1.2em/3 Ahem',
        'oblique <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> normal 1.2em/3 Ahem',
        'oblique <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> normal 1.2em/3 Ahem',

        'oblique small-caps <NotValid> 1.2em/3 Ahem',
        'normal small-caps <NotValid> 1.2em/3 Ahem',
        'oblique normal <NotValid> 1.2em/3 Ahem',
        'oblique small-caps <NotValid> 1.2em/3 Ahem',
        'normal small-caps <NotValid> 1.2em/3 Ahem',
        'oblique normal <NotValid> 1.2em/3 Ahem',
        'normal normal <NotValid> 1.2em/3 Ahem',

        'oblique small-caps bold <NotValid>/3 Ahem',
        'normal small-caps bold <NotValid>/3 Ahem',
        'oblique normal bold <NotValid>/3 Ahem',
        'oblique small-caps normal <NotValid>/3 Ahem',
        'normal small-caps normal <NotValid>/3 Ahem',
        'oblique normal normal <NotValid>/3 Ahem',
        'normal normal bold <NotValid>/3 Ahem',

        'oblique small-caps bold 1.2em/3 <NotValid>',
        'normal small-caps bold 1.2em/3 <NotValid>',
        'oblique normal bold 1.2em/3 <NotValid>',
        'oblique small-caps normal 1.2em/3 <NotValid>',
        'normal small-caps normal 1.2em/3 <NotValid>',
        'oblique normal normal 1.2em/3 <NotValid>',

        # <font-weight> <font-style> <font-variant> <font-size>/<line-height> <font-family>
        '<NotValid> oblique small-caps 1.2em/3 Ahem',
        '<NotValid> oblique small-caps 1.2em/3 Ahem',
        '<NotValid> normal small-caps 1.2em/3 Ahem',
        '<NotValid> oblique normal 1.2em/3 Ahem',
        '<NotValid> oblique normal 1.2em/3 Ahem',
        '<NotValid> normal normal 1.2em/3 Ahem',
        '<NotValid> normal small-caps 1.2em/3 Ahem',

        'bold <NotValid> small-caps 1.2em/3 Ahem',
        'normal <NotValid> small-caps 1.2em/3 Ahem',
        'bold <NotValid> small-caps 1.2em/3 Ahem',
        'bold <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> normal 1.2em/3 Ahem',
        'bold <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> small-caps 1.2em/3 Ahem',

        'bold oblique <NotValid> 1.2em/3 Ahem',
        'normal oblique <NotValid> 1.2em/3 Ahem',
        'bold normal <NotValid> 1.2em/3 Ahem',
        'bold oblique <NotValid> 1.2em/3 Ahem',
        'normal oblique <NotValid> 1.2em/3 Ahem',
        'bold normal <NotValid> 1.2em/3 Ahem',
        'normal normal <NotValid> 1.2em/3 Ahem',

        'bold oblique small-caps <NotValid>/3 Ahem',
        'normal oblique small-caps <NotValid>/3 Ahem',
        'bold normal small-caps <NotValid>/3 Ahem',
        'bold oblique normal <NotValid>/3 Ahem',
        'normal oblique normal <NotValid>/3 Ahem',
        'bold normal normal <NotValid>/3 Ahem',
        'normal normal small-caps <NotValid>/3 Ahem',

        'bold oblique small-caps 1.2em/<NotValid> Ahem',
        'normal oblique small-caps 1.2em/<NotValid> Ahem',
        'bold normal small-caps 1.2em/<NotValid> Ahem',
        'bold oblique normal 1.2em/<NotValid> Ahem',
        'normal oblique normal 1.2em/<NotValid> Ahem',
        'bold normal normal 1.2em/<NotValid> Ahem',
        'normal normal small-caps 1.2em/<NotValid> Ahem',

        'bold oblique small-caps 1.2em/3 <NotValid>',
        'normal oblique small-caps 1.2em/3 <NotValid>',
        'bold normal small-caps 1.2em/3 <NotValid>',
        'bold oblique normal 1.2em/3 <NotValid>',
        'normal oblique normal 1.2em/3 <NotValid>',
        'bold normal normal 1.2em/3 <NotValid>',
        'normal normal small-caps 1.2em/3 <NotValid>',

        # <font-variant> <font-weight> <font-style> <font-size>/<line-height> <font-family>
        '<NotValid> bold oblique 1.2em/3 Ahem',
        '<NotValid> bold oblique 1.2em/3 Ahem',
        '<NotValid> normal oblique 1.2em/3 Ahem',
        '<NotValid> bold normal 1.2em/3 Ahem',
        '<NotValid> bold normal 1.2em/3 Ahem',
        '<NotValid> normal normal 1.2em/3 Ahem',
        '<NotValid> normal oblique 1.2em/3 Ahem',

        'small-caps <NotValid> oblique 1.2em/3 Ahem',
        'normal <NotValid> oblique 1.2em/3 Ahem',
        'small-caps <NotValid> oblique 1.2em/3 Ahem',
        'small-caps <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> normal 1.2em/3 Ahem',
        'small-caps <NotValid> normal 1.2em/3 Ahem',
        'normal <NotValid> oblique 1.2em/3 Ahem',

        'small-caps bold <NotValid> 1.2em/3 Ahem',
        'normal bold <NotValid> 1.2em/3 Ahem',
        'small-caps normal <NotValid> 1.2em/3 Ahem',
        'small-caps bold <NotValid> 1.2em/3 Ahem',
        'normal bold <NotValid> 1.2em/3 Ahem',
        'small-caps normal <NotValid> 1.2em/3 Ahem',
        'normal normal <NotValid> 1.2em/3 Ahem',

        'small-caps bold oblique <NotValid>em/3 Ahem',
        'normal bold oblique <NotValid>/3 Ahem',
        'small-caps normal oblique <NotValid>/3 Ahem',
        'small-caps bold normal <NotValid>/3 Ahem',
        'normal bold normal <NotValid>/3 Ahem',
        'small-caps normal normal <NotValid>/3 Ahem',
        'normal normal oblique <NotValid>/3 Ahem',

        'small-caps bold oblique <NotValid>/3 Ahem',
        'normal bold oblique <NotValid>/3 Ahem',
        'small-caps normal oblique <NotValid>/3 Ahem',
        'small-caps bold normal <NotValid>/3 Ahem',
        'normal bold normal <NotValid>/3 Ahem',
        'small-caps normal normal <NotValid>/3 Ahem',
        'normal normal oblique <NotValid>/3 Ahem',

        'small-caps bold oblique 1.2em/<NotValid> Ahem',
        'normal bold oblique 1.2em/<NotValid> Ahem',
        'small-caps normal oblique 1.2em/<NotValid> Ahem',
        'small-caps bold normal 1.2em/<NotValid> Ahem',
        'normal bold normal 1.2em/<NotValid> Ahem',
        'small-caps normal normal 1.2em/<NotValid> Ahem',
        'normal normal oblique 1.2em/<NotValid> Ahem',

        'small-caps bold oblique 1.2em/3 <NotValid>',
        'normal bold oblique 1.2em/3 <NotValid>',
        'small-caps normal oblique 1.2em/3 <NotValid>',
        'small-caps bold normal 1.2em/3 <NotValid>',
        'normal bold normal 1.2em/3 <NotValid>',
        'small-caps normal normal 1.2em/3 <NotValid>',
        'normal normal oblique 1.2em/3 <NotValid>',

        # <font-variant> <font-style> <font-weight> <font-size>/<line-height> <font-family>
        '<NotValid> oblique bold 1.2em/3 Ahem',
        '<NotValid> oblique bold 1.2em/3 Ahem',
        '<NotValid> normal bold 1.2em/3 Ahem',
        '<NotValid> oblique normal 1.2em/3 Ahem',

        'small-caps <NotValid> bold 1.2em/3 Ahem',
        'normal <NotValid> bold 1.2em/3 Ahem',
        'small-caps <NotValid> bold 1.2em/3 Ahem',
        'small-caps <NotValid> normal 1.2em/3 Ahem',

        'small-caps oblique <NotValid> 1.2em/3 Ahem',
        'normal oblique <NotValid> 1.2em/3 Ahem',
        'small-caps normal <NotValid> 1.2em/3 Ahem',
        'small-caps oblique <NotValid> 1.2em/3 Ahem',

        'small-caps oblique bold <NotValid>/3 Ahem',
        'normal oblique bold <NotValid>/3 Ahem',
        'small-caps normal bold <NotValid>/3 Ahem',
        'small-caps oblique normal <NotValid>/3 Ahem',

        'small-caps oblique bold <NotValid>/3 Ahem',
        'normal oblique bold <NotValid>/3 Ahem',
        'small-caps normal bold <NotValid>/3 Ahem',
        'small-caps oblique normal <NotValid>/3 Ahem',

        'small-caps oblique bold 1.2em/<NotValid> Ahem',
        'normal oblique bold 1.2em/<NotValid> Ahem',
        'small-caps normal bold 1.2em/<NotValid> Ahem',
        'small-caps oblique normal 1.2em/<NotValid> Ahem',

        'small-caps oblique bold 1.2em/3 <NotValid>',
        'normal oblique bold 1.2em/3 <NotValid>',
        'small-caps normal bold 1.2em/3 <NotValid>',
        'small-caps oblique normal 1.2em/3 <NotValid>',
    ])
    CASE_4_INVALID = set([
        # <font-style> <font-variant> <font-size>/<line-height> <font-family>
        '<NotValid> small-caps 1.2em/3 Ahem',
        '<NotValid> normal 1.2em/3 Ahem',
        '<NotValid> small-caps 1.2em/3 Ahem',
        '<NotValid> normal 1.2em/3 Ahem',

        'oblique <NotValid> 1.2em/3 Ahem',
        'oblique <NotValid> 1.2em/3 Ahem',
        'normal <NotValid> 1.2em/3 Ahem',
        'normal <NotValid> 1.2em/3 Ahem',

        'oblique small-caps <NotValid>/3 Ahem',
        'oblique normal <NotValid>/3 Ahem',
        'normal small-caps <NotValid>/3 Ahem',
        'normal normal <NotValid>/3 Ahem',

        'oblique small-caps 1.2em/<NotValid> Ahem',
        'oblique normal 1.2em/<NotValid> Ahem',
        'normal small-caps 1.2em/<NotValid> Ahem',
        'normal normal 1.2em/<NotValid> Ahem',

        'oblique small-caps 1.2em/3 <NotValid>',
        'oblique normal 1.2em/3 <NotValid>',
        'normal small-caps 1.2em/3 <NotValid>',
        'normal normal 1.2em/3 <NotValid>',

        #  <font-style> <font-weight> <font-size>/<line-height> <font-family>
        '<NotValid> bold 1.2em/3 Ahem',
        '<NotValid> bold 1.2em/3 Ahem',

        'oblique <NotValid> 1.2em/3 Ahem',
        'normal <NotValid> 1.2em/3 Ahem',

        'oblique bold <NotValid>/3 Ahem',
        'normal bold <NotValid>/3 Ahem',

        'oblique bold 1.2em/<NotValid> Ahem',
        'normal bold 1.2em/<NotValid> Ahem',

        'oblique bold 1.2em/3 <NotValid>',
        'normal bold 1.2em/3 <NotValid>',

        # <font-weight> <font-style> <font-size>/<line-height> <font-family>
        '<NotValid> oblique 1.2em/3 Ahem',
        '<NotValid> normal 1.2em/3 Ahem',
        '<NotValid> oblique 1.2em/3 Ahem',

        'bold <NotValid> 1.2em/3 Ahem',
        'bold <NotValid> 1.2em/3 Ahem',
        'normal <NotValid> 1.2em/3 Ahem',

        'bold oblique <NotValid>/3 Ahem',
        'bold normal <NotValid>/3 Ahem',
        'normal oblique <NotValid>/3 Ahem',

        'bold oblique 1.2em/<NotValid> Ahem',
        'bold normal 1.2em/<NotValid> Ahem',
        'normal oblique 1.2em/<NotValid> Ahem',

        'bold oblique 1.2em/3 <NotValid>',
        'bold normal 1.2em/3 <NotValid>',
        'normal oblique 1.2em/3 <NotValid>',

        # <font-weight> <font-variant> <font-size>/<line-height> <font-family>
        '<NotValid> small-caps 1.2em/3 Ahem',

        'bold <NotValid> 1.2em/3 Ahem',

        'bold small-caps <NotValid>/3 Ahem',

        'bold small-caps 1.2em/<NotValid> Ahem',

        'bold small-caps 1.2em/3 <NotValid>',
    ])
    CASE_3_INVALID = set([
        # <font-style> <font-size>/<line-height> <font-family>
        '<NotValid> 1.2em/3 Ahem',

        'oblique <NotValid>/3 Ahem',

        'oblique 1.2em/<NotValid> Ahem',

        'oblique 1.2em/3 <NotValid>',

        # <font-variant> <font-size>/<line-height> <font-family>
        '<NotValid> 1.2em/3 Ahem',

        'small-caps <NotValid>/3 Ahem',

        'small-caps 1.2em/<NotValid> Ahem',

        'small-caps 1.2em/3 <NotValid>',

        # <font-weight> <font-size>/<line-height> <font-family>
        '<NotValid> 1.2em/3 Ahem',

        'bold <NotValid>/3 Ahem',

        'bold 1.2em/<NotValid> Ahem',

        'bold 1.2em/3 <NotValid>',

        # <font-style> <font-size> <font-family>
        '<NotValid> 1.2em Ahem',

        'oblique <NotValid> Ahem',

        'oblique 1.2em <NotValid>',

        # <font-variant> <font-size> <font-family>
        '<NotValid> 1.2em Ahem',

        'small-caps <NotValid> Ahem',

        'small-caps 1.2em <NotValid>',

        # <font-weight> <font-size> <font-family>
        '<NotValid> 1.2em Ahem',

        'bold <NotValid> Ahem',

        'bold 1.2em <NotValid>',
    ])
    CASE_2_INVALID = set([
        #  <font-size>/<line-height> <font-family>
        '<NotValid>/3 Ahem',
        '1.2em/<NotValid> Ahem, "White Space"',
        '1.2em/3 <NotValid>, "White Space", serif',
        '1.2em/3 Ahem, "<NotValid>", serif',
        '1.2em/3 Ahem, <NotValid>, serif',
        '1.2em/3 Ahem, "White Space", <NotValid>',

        #  <font-size> <font-family>
        '<NotValid> Ahem',
        '1.2em <NotValid>, "White Space"',
        '1.2em Ahem, "<NotValid>", serif',
        '1.2em Ahem, <NotValid>, serif',
        '1.2em Ahem, "White Space", <NotValid>',
    ])
    CASE_1_INVALID = set([
        # <system-font> | inherit
        'Ahem'
        '"White Space"'
        '<NotValid>',
        '20',
        20,
    ])
    CASE_EXTRAS_INVALID = set([
        # Space between font-size and line-height
        'small-caps oblique normal 1.2em /3 Ahem'
        'small-caps oblique normal 1.2em/ 3 Ahem'
        'small-caps oblique normal 1.2em / 3 Ahem'

        # Too many parts
        'normal normal normal normal 12px/12px serif'
        'normal normal normal normal normal 12px/12px serif'

        # No quotes with spaces
        'small-caps oblique normal 1.2em/3 Ahem, White Space'

        # No commas
        'small-caps oblique normal 1.2em/3 Ahem "White Space"'
    ])

    # Font construction test cases
    CASE_CONSTRUCT = {
        # <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
        'oblique small-caps bold 1.2em/3 Ahem': ('oblique', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'normal small-caps bold 1.2em/3 Ahem': ('normal', 'small-caps', 'bold', '1.2em', '3', ['Ahem']),
        'oblique normal bold 1.2em/3 Ahem': ('oblique', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'oblique small-caps normal 1.2em/3 Ahem': ('oblique', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'normal small-caps normal 1.2em/3 Ahem': ('normal', 'small-caps', 'normal', '1.2em', '3', ['Ahem']),
        'oblique normal normal 1.2em/3 Ahem': ('oblique', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'normal normal bold 1.2em/3 Ahem': ('normal', 'normal', 'bold', '1.2em', '3', ['Ahem']),
        'normal normal normal 1.2em/3 Ahem': ('normal', 'normal', 'normal', '1.2em', '3', ['Ahem']),
        'normal normal 900 1.2em/3 Ahem': ('normal', 'normal', '900', '1.2em', '3', ['Ahem']),
    }
    CASE_CONSTRUCT_FAMILY = {
        'Ahem': ['Ahem'],
        'Ahem, "White Space"': ['Ahem', 'White Space'],
        'Ahem, "White Space", serif': ['Ahem', 'White Space', 'serif'],
    }

    @staticmethod
    def tuple_to_font_dict(tup):
        """Helper to convert a tuple to a font dict to check for valid outputs."""
        font_dict = {}
        for idx, key in enumerate(['font_style', 'font_variant', 'font_weight',
                                   'font_size', 'line_height', 'font_family']):
            font_dict[key] = tup[idx]

        return font_dict

    def test_parse_font_shorthand(self):
        for cases in [self.CASE_5, self.CASE_4, self.CASE_3, self.CASE_2, self.CASE_1, self.CASE_EXTRAS]:
            for case in sorted(cases):
                expected_output = self.tuple_to_font_dict(cases[case])
                font = parse_font(case)
                self.assertEqual(font, expected_output)

    def test_parse_font_shorthand_invalid(self):
        for cases in [self.CASE_5_INVALID, self.CASE_4_INVALID, self.CASE_3_INVALID, self.CASE_2_INVALID,
                      self.CASE_1_INVALID, self.CASE_EXTRAS_INVALID]:
            for case in cases:
                with self.assertRaises(ValueError):
                    parse_font(case)

    def test_construct_font_shorthand(self):
        for expected_output, tup in sorted(self.CASE_CONSTRUCT.items()):
            case = self.tuple_to_font_dict(tup)
            font = construct_font(case)
            self.assertEqual(font, expected_output)

    def test_construct_font_family(self):
        for expected_output, case in sorted(self.CASE_CONSTRUCT_FAMILY.items()):
            font_family = construct_font_family(case)
            self.assertEqual(font_family, expected_output)
