from unittest import TestCase

from colosseum.units import (
    ch, cm, em, ex, inch, mm, pc, percent, pt, px, vh, vmax, vmin, vw,
)

from .utils import Display


# A dummy font declaration. ex < ch
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


# Another dummy font declaration. ex == ch == 3/4 of em
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
        self.display = Display(dpi=96, width=640, height=480)

    def test_logical_to_pixels(self):
        p = 0 * px
        self.assertEqual(p.lu(display=self.display), 0)
        self.assertEqual(p.px(display=self.display), 0)

        p = 0.2 * px
        self.assertEqual(p.lu(display=self.display), 13)
        self.assertEqual(p.px(display=self.display), 0)

        p = 0.5 * px
        self.assertEqual(p.lu(display=self.display), 32)
        self.assertEqual(p.px(display=self.display), 0)

        p = 0.7 * px
        self.assertEqual(p.lu(display=self.display), 45)
        self.assertEqual(p.px(display=self.display), 0)

        p = 1 * px
        self.assertEqual(p.lu(display=self.display), 64)
        self.assertEqual(p.px(display=self.display), 1)

        p = 1.2 * px
        self.assertEqual(p.lu(display=self.display), 77)
        self.assertEqual(p.px(display=self.display), 1)

        p = 1.5 * px
        self.assertEqual(p.lu(display=self.display), 96)
        self.assertEqual(p.px(display=self.display), 1)

        p = 1.7 * px
        self.assertEqual(p.lu(display=self.display), 109)
        self.assertEqual(p.px(display=self.display), 1)

        p = 2 * px
        self.assertEqual(p.lu(display=self.display), 128)
        self.assertEqual(p.px(display=self.display), 2)

    def test_multiply(self):
        p1 = 5 * px

        # A non-numerical unit can't be modified with units
        with self.assertRaises(TypeError):
            p1 * px

        # Numbers are multiplied by units, not vice versa.
        with self.assertRaises(TypeError):
            px * 5


class PixelUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

        self.helvetica12 = Helvetica(12)
        self.helvetica16 = Helvetica(16)
        self.courier12 = Courier(12)

    def test_pixels(self):
        p = 1 * px
        self.assertEqual(p.lu(display=self.simple), 64)
        self.assertEqual(p.lu(display=self.print), 64)
        self.assertEqual(p.lu(display=self.hidpi), 64)

        self.assertEqual(p.lu(font=self.helvetica12), 64)
        self.assertEqual(p.lu(font=self.helvetica16), 64)
        self.assertEqual(p.lu(font=self.courier12), 64)

        p = 5 * px
        self.assertEqual(p.lu(display=self.simple), 320)
        self.assertEqual(p.lu(display=self.print), 320)
        self.assertEqual(p.lu(display=self.hidpi), 320)

        self.assertEqual(p.lu(font=self.helvetica12), 320)
        self.assertEqual(p.lu(font=self.helvetica16), 320)
        self.assertEqual(p.lu(font=self.courier12), 320)

        self.assertEqual(p.lu(size=100), 320)

        self.assertEqual(str(p), '5px')
        self.assertEqual(repr(p), '5px')
        self.assertEqual(p, 5)
        self.assertEqual(p, 5 * px)


class AbsoluteUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

    def test_pica(self):
        p = 1 * pc
        self.assertEqual(p.lu(display=self.simple), 512)
        self.assertEqual(p.lu(display=self.print), 1600)
        self.assertEqual(p.lu(display=self.hidpi), 1739)

        p = 5 * pc
        self.assertEqual(p.lu(display=self.simple), 2560)
        self.assertEqual(p.lu(display=self.print), 8000)
        self.assertEqual(p.lu(display=self.hidpi), 8693)

        self.assertEqual(str(p), "5pc")
        self.assertEqual(repr(p), "5pc")
        self.assertEqual(p, 5 * pc)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_points(self):
        p = 1 * pt
        self.assertEqual(p.lu(display=self.simple), 85)
        self.assertEqual(p.lu(display=self.print), 267)
        self.assertEqual(p.lu(display=self.hidpi), 290)

        p = 5 * pt
        self.assertEqual(p.lu(display=self.simple), 427)
        self.assertEqual(p.lu(display=self.print), 1333)
        self.assertEqual(p.lu(display=self.hidpi), 1449)

        self.assertEqual(str(p), "5pt")
        self.assertEqual(repr(p), "5pt")
        self.assertEqual(p, 5 * pt)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_inches(self):
        p = 1 * inch
        self.assertEqual(p.lu(display=self.simple), 6144)
        self.assertEqual(p.lu(display=self.print), 19200)
        self.assertEqual(p.lu(display=self.hidpi), 20864)

        p = 5 * inch
        self.assertEqual(p.lu(display=self.simple), 30720)
        self.assertEqual(p.lu(display=self.print), 96000)
        self.assertEqual(p.lu(display=self.hidpi), 104320)

        self.assertEqual(str(p), "5in")
        self.assertEqual(repr(p), "5in")
        self.assertEqual(p, 5 * inch)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_centimeters(self):
        p = 1 * cm
        self.assertEqual(p.lu(display=self.simple), 2419)
        self.assertEqual(p.lu(display=self.print), 7559)
        self.assertEqual(p.lu(display=self.hidpi), 8214)

        p = 5 * cm
        self.assertEqual(p.lu(display=self.simple), 12095)
        self.assertEqual(p.lu(display=self.print), 37795)
        self.assertEqual(p.lu(display=self.hidpi), 41071)

        self.assertEqual(str(p), "5cm")
        self.assertEqual(repr(p), "5cm")
        self.assertEqual(p, 5 * cm)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_millimeters(self):
        p = 1 * mm
        self.assertEqual(p.lu(display=self.simple), 242)
        self.assertEqual(p.lu(display=self.print), 756)
        self.assertEqual(p.lu(display=self.hidpi), 821)

        p = 5 * mm
        self.assertEqual(p.lu(display=self.simple), 1209)
        self.assertEqual(p.lu(display=self.print), 3780)
        self.assertEqual(p.lu(display=self.hidpi), 4107)

        self.assertEqual(str(p), "5mm")
        self.assertEqual(repr(p), "5mm")
        self.assertEqual(p, 5 * mm)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)


class ViewportUnitTests(TestCase):
    def setUp(self):
        self.simple = Display(dpi=96, width=640, height=480)
        self.print = Display(dpi=300, width=8.27*300, height=11.69*300)  # A4
        self.hidpi = Display(dpi=326, width=640, height=1136)  # iPhone 7

    def test_viewwidth(self):
        p = 1 * vw
        self.assertEqual(p.lu(display=self.simple), 410)
        self.assertEqual(p.lu(display=self.print), 1588)
        self.assertEqual(p.lu(display=self.hidpi), 410)

        p = 5 * vw
        self.assertEqual(p.lu(display=self.simple), 2048)
        self.assertEqual(p.lu(display=self.print), 7939)
        self.assertEqual(p.lu(display=self.hidpi), 2048)

        self.assertEqual(str(p), "5vw")
        self.assertEqual(repr(p), "5vw")
        self.assertEqual(p, 5 * vw)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_viewheight(self):
        p = 1 * vh
        self.assertEqual(p.lu(display=self.simple), 307)
        self.assertEqual(p.lu(display=self.print), 2244)
        self.assertEqual(p.lu(display=self.hidpi), 727)

        p = 5 * vh
        self.assertEqual(p.lu(display=self.simple), 1536)
        self.assertEqual(p.lu(display=self.print), 11222)
        self.assertEqual(p.lu(display=self.hidpi), 3635)

        self.assertEqual(str(p), "5vh")
        self.assertEqual(repr(p), "5vh")
        self.assertEqual(p, 5 * vh)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_viewmin(self):
        p = 1 * vmin
        self.assertEqual(p.lu(display=self.simple), 307)
        self.assertEqual(p.lu(display=self.print), 1588)
        self.assertEqual(p.lu(display=self.hidpi), 410)

        p = 5 * vmin
        self.assertEqual(p.lu(display=self.simple), 1536)
        self.assertEqual(p.lu(display=self.print), 7939)
        self.assertEqual(p.lu(display=self.hidpi), 2048)

        self.assertEqual(str(p), "5vmin")
        self.assertEqual(repr(p), "5vmin")
        self.assertEqual(p, 5 * vmin)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_viewmax(self):
        p = 1 * vmax
        self.assertEqual(p.lu(display=self.simple), 410)
        self.assertEqual(p.lu(display=self.print), 2244)
        self.assertEqual(p.lu(display=self.hidpi), 727)

        p = 5 * vmax
        self.assertEqual(p.lu(display=self.simple), 2048)
        self.assertEqual(p.lu(display=self.print), 11222)
        self.assertEqual(p.lu(display=self.hidpi), 3635)

        self.assertEqual(str(p), "5vmax")
        self.assertEqual(repr(p), "5vmax")
        self.assertEqual(p, 5 * vmax)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)


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
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 1024)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 1365)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 1024)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 3200)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 4267)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 3200)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 3477)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 4636)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 3477)

        p = 5 * em
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 5120)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 6827)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 5120)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 16000)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 21333)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 16000)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 17387)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 23182)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 17387)

        self.assertEqual(str(p), "5em")
        self.assertEqual(repr(p), "5em")
        self.assertEqual(p, 5 * em)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_ex(self):
        p = 1 * ex
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 666)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 887)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 768)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 2080)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 2773)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 2400)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 2260)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 3014)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 2608)

        p = 5 * ex
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 3328)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 4437)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 3840)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 10400)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 13867)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 12000)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 11301)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 15068)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 13040)

        self.assertEqual(str(p), "5ex")
        self.assertEqual(repr(p), "5ex")
        self.assertEqual(p, 5 * ex)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)

    def test_ch(self):
        p = 1 * ch
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 727)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 969)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 768)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 2272)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 3029)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 2400)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 2469)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 3292)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 2608)

        p = 5 * ch
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica12), 3635)
        self.assertEqual(p.lu(display=self.simple, font=self.helvetica16), 4847)
        self.assertEqual(p.lu(display=self.simple, font=self.courier12), 3840)

        self.assertEqual(p.lu(display=self.print, font=self.helvetica12), 11360)
        self.assertEqual(p.lu(display=self.print, font=self.helvetica16), 15147)
        self.assertEqual(p.lu(display=self.print, font=self.courier12), 12000)

        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica12), 12345)
        self.assertEqual(p.lu(display=self.hidpi, font=self.helvetica16), 16459)
        self.assertEqual(p.lu(display=self.hidpi, font=self.courier12), 13040)

        self.assertEqual(str(p), "5ch")
        self.assertEqual(repr(p), "5ch")
        self.assertEqual(p, 5 * ch)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)


class PercentUnitTests(TestCase):
    def test_percent(self):
        p = 1 * percent
        self.assertEqual(p.lu(size=10), 6)
        self.assertEqual(p.lu(size=100), 64)
        self.assertEqual(p.lu(size=500), 320)

        p = 5 * percent
        self.assertEqual(p.lu(size=10), 32)
        self.assertEqual(p.lu(size=100), 320)
        self.assertEqual(p.lu(size=500), 1600)

        self.assertEqual(str(p), "5%")
        self.assertEqual(repr(p), "5%")
        self.assertEqual(p, 5 * percent)
        self.assertNotEqual(p, 5 * px)
        self.assertNotEqual(p, 5)
