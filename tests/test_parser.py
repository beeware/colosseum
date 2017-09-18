from unittest import TestCase

from colosseum import parser
from colosseum.color import rgb, hsl
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
        self.assertEqualUnits(10, 10 * pt)
        self.assertEqualUnits(10.0, 10 * pt)

    def test_no_units(self):
        self.assertEqualUnits('10', 10 * pt)
        self.assertEqualUnits('10.0', 10 * pt)

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

    def test_rgb(self):
        self.assertEqualColor('rgb(1,2,3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb(1, 2, 3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb( 1 , 2 , 3)', rgb(1, 2, 3))

        self.assertEqualColor('#123', rgb(0x11, 0x22, 0x33))
        self.assertEqualColor('#112233', rgb(0x11, 0x22, 0x33))

    def test_rgba(self):
        self.assertEqualColor('rgba(1,2,3,0.5)', rgb(1, 2, 3, 0.5))
        self.assertEqualColor('rgba(1, 2, 3, 0.5)', rgb(1, 2, 3, 0.5))
        self.assertEqualColor('rgba( 1 , 2 , 3 , 0.5)', rgb(1, 2, 3, 0.5))

        self.assertEqualColor('#1234', rgb(0x11, 0x22, 0x33, 0.2666))
        self.assertEqualColor('#11223344', rgb(0x11, 0x22, 0x33, 0.2666))

    def test_hsl(self):
        self.assertEqualHSL('hsl(1,20%,30%)', hsl(1, 20, 30))
        self.assertEqualHSL('hsl(1, 20%, 30%)', hsl(1, 20, 30))
        self.assertEqualHSL('hsl( 1, 20% , 30%)', hsl(1, 20, 30))

    def test_hsla(self):
        self.assertEqualHSL('hsla(1,20%,30%,0.5)', hsl(1, 20, 30, 0.5))
        self.assertEqualHSL('hsla(1, 20%, 30%, 0.5)', hsl(1, 20, 30, 0.5))
        self.assertEqualHSL('hsla( 1, 20% , 30% , 0.5)', hsl(1, 20, 30, 0.5))

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
