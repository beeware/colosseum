from unittest import TestCase

from colosseum.units import (
    ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh, vmax, vmin, vw,
)


class Display:
    def __init__(self, dpi, width, height):
        self.dpi = dpi
        self.width = width
        self.height = height


class Helvetica:
    def __init__(self, size):
        self.size = size

    @property
    def em(self):
        return self.size

    @property
    def ex(self):
        return 0.65 * self.size

    @property
    def ch(self):
        return 0.71 * self.size


class Courier:
    def __init__(self, size):
        self.size = size

    @property
    def em(self):
        return self.size

    @property
    def ex(self):
        return 0.75 * self.size

    @property
    def ch(self):
        return 0.75 * self.size


class BaseUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

        self.helvetica12 = Helvetica(12)
        self.helvetica16 = Helvetica(16)
        self.courier12 = Courier(12)

    def test_pixels(self):
        p = 1 * px
        self.assertAlmostEqual(p.pixels(display=self.simple), 1, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 1, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 1, places=3)

        self.assertAlmostEqual(p.pixels(font=self.helvetica12), 1, places=3)
        self.assertAlmostEqual(p.pixels(font=self.helvetica16), 1, places=3)
        self.assertAlmostEqual(p.pixels(font=self.courier12), 1, places=3)

        p = 5 * px
        self.assertAlmostEqual(p.pixels(display=self.simple), 5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 5, places=3)

        self.assertAlmostEqual(p.pixels(font=self.helvetica12), 5, places=3)
        self.assertAlmostEqual(p.pixels(font=self.helvetica16), 5, places=3)
        self.assertAlmostEqual(p.pixels(font=self.courier12), 5, places=3)

        self.assertAlmostEqual(p.pixels(size=100), 5, places=3)

        self.assertEqual(str(p), '5px')

    def test_multiply(self):
        p1 = 5 * px

        # A non-numerical unit can't be modified with units
        with self.assertRaises(TypeError):
            p1 * px

        # Numbers are multiplied by units, not vice versa.
        with self.assertRaises(TypeError):
            px * 5


class AbsoluteUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

    def test_pica(self):
        p = 1 * pc
        self.assertAlmostEqual(p.pixels(display=self.simple), 8, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 25, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 27.1666, places=3)

        p = 5 * pc
        self.assertAlmostEqual(p.pixels(display=self.simple), 40, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 125, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 135.8333, places=3)

        self.assertEqual(str(p), "5pc")

    def test_points(self):
        p = 1 * pt
        self.assertAlmostEqual(p.pixels(display=self.simple), 1.333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 4.1666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 4.5277, places=3)

        p = 5 * pt
        self.assertAlmostEqual(p.pixels(display=self.simple), 6.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 20.833, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 22.6385, places=3)

        self.assertEqual(str(p), "5pt")

    def test_inches(self):
        p = 1 * inch
        self.assertAlmostEqual(p.pixels(display=self.simple), 96, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 300, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 326, places=3)

        p = 5 * inch
        self.assertAlmostEqual(p.pixels(display=self.simple), 480, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 1500, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 1630, places=3)

        self.assertEqual(str(p), "5in")

    def test_centimeters(self):
        p = 1 * cm
        self.assertAlmostEqual(p.pixels(display=self.simple), 37.795, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 118.110, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 128.3466, places=3)

        p = 5 * cm
        self.assertAlmostEqual(p.pixels(display=self.simple), 188.9766, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 590.552, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 641.733, places=3)

        self.assertEqual(str(p), "5cm")

    def test_millimeters(self):
        p = 1 * mm
        self.assertAlmostEqual(p.pixels(display=self.simple), 3.7795, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 11.8110, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 12.8346, places=3)

        p = 5 * mm
        self.assertAlmostEqual(p.pixels(display=self.simple), 18.8976, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 59.0552, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 64.1733, places=3)

        self.assertEqual(str(p), "5mm")


class ViewportUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

    def test_viewwidth(self):
        p = 1 * vw
        self.assertAlmostEqual(p.pixels(display=self.simple), 6.4, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 24.81, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 6.4, places=3)

        p = 5 * vw
        self.assertAlmostEqual(p.pixels(display=self.simple), 32, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 124.05, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 32, places=3)

        self.assertEqual(str(p), "5vw")

    def test_viewheight(self):
        p = 1 * vh
        self.assertAlmostEqual(p.pixels(display=self.simple), 4.8, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 35.07, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 11.36, places=3)

        p = 5 * vh
        self.assertAlmostEqual(p.pixels(display=self.simple), 24, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 175.35, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 56.8, places=3)

        self.assertEqual(str(p), "5vh")

    def test_viewmin(self):
        p = 1 * vmin
        self.assertAlmostEqual(p.pixels(display=self.simple), 4.8, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 24.81, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 6.4, places=3)

        p = 5 * vmin
        self.assertAlmostEqual(p.pixels(display=self.simple), 24, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 124.05, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 32, places=3)

        self.assertEqual(str(p), "5vmin")

    def test_viewmax(self):
        p = 1 * vmax
        self.assertAlmostEqual(p.pixels(display=self.simple), 6.4, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 35.07, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 11.36, places=3)

        p = 5 * vmax
        self.assertAlmostEqual(p.pixels(display=self.simple), 32, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print), 175.35, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi), 56.8, places=3)

        self.assertEqual(str(p), "5vmax")


class FontUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

        self.helvetica12 = Helvetica(12)
        self.helvetica16 = Helvetica(16)
        self.courier12 = Courier(12)

    def test_em(self):
        p = 1 * em
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 16.0, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 21.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 16.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 50.0, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 66.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 50.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 54.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 72.4444, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 54.3333, places=3)

        p = 5 * em
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 80.0, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 106.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 80.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 250.0, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 333.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 250.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 271.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 362.2222, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 271.6666, places=3)

        self.assertEqual(str(p), "5em")

    def test_ex(self):
        p = 1 * ex
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 10.4, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 13.8666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 12.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 32.5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 43.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 37.5, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 35.3166, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 47.0888, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 40.75, places=3)

        p = 5 * ex
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 52.0, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 69.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 60.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 162.5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 216.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 187.5, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 176.5833, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 235.4444, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 203.75, places=3)

        self.assertEqual(str(p), "5ex")

    def test_ch(self):
        p = 1 * ch
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 11.36, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 15.1466, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 12.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 35.5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 47.3333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 37.5, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 38.5766, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 51.4355, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 40.75, places=3)

        p = 5 * ch
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica12), 56.8, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.helvetica16), 75.7333, places=3)
        self.assertAlmostEqual(p.pixels(display=self.simple, font=self.courier12), 60.0, places=3)

        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica12), 177.5, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.helvetica16), 236.6666, places=3)
        self.assertAlmostEqual(p.pixels(display=self.print, font=self.courier12), 187.5, places=3)

        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica12), 192.8833, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.helvetica16), 257.1777, places=3)
        self.assertAlmostEqual(p.pixels(display=self.hidpi, font=self.courier12), 203.75, places=3)

        self.assertEqual(str(p), "5ch")


class PercentUnitTests(TestCase):
    def test_percent(self):
        p = 1 * percent
        self.assertAlmostEqual(p.pixels(size=10), 0.1, places=3)
        self.assertAlmostEqual(p.pixels(size=100), 1, places=3)
        self.assertAlmostEqual(p.pixels(size=500), 5, places=3)

        p = 5 * percent
        self.assertAlmostEqual(p.pixels(size=10), 0.5, places=3)
        self.assertAlmostEqual(p.pixels(size=100), 5, places=3)
        self.assertAlmostEqual(p.pixels(size=500), 25, places=3)

        self.assertEqual(str(p), "5%")
