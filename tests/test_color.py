from unittest import TestCase

from colosseum.colors import hsl, rgb


class ColorTests(TestCase):
    def assertEqualColor(self, a, b):
        self.assertEqual(a.rgb.r, b.rgb.r)
        self.assertEqual(a.rgb.g, b.rgb.g)
        self.assertEqual(a.rgb.b, b.rgb.b)
        self.assertEqual(a.rgb.a, b.rgb.a)

    def test_rgb_repr(self):
        self.assertEqual(repr(rgb(10, 20, 30, 0.5)), "rgba(10, 20, 30, 0.5)")

    def test_hsl_repr(self):
        self.assertEqual(repr(hsl(10, 0.2, 0.3, 0.5)), "hsla(10, 0.2, 0.3, 0.5)")

    def test_hsl_blacks(self):
        self.assertEqualColor(hsl(0, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(60, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(180, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(240, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(360, 0.0, 0.0), rgb(0x00, 0x00, 0x00))

    def test_hsl_whites(self):
        self.assertEqualColor(hsl(0, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(60, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(180, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(240, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(360, 0.0, 1.0), rgb(0xff, 0xff, 0xff))

    def test_hsl_grays(self):
        self.assertEqualColor(hsl(0, 0.0, 0.2), rgb(0x33, 0x33, 0x33))
        self.assertEqualColor(hsl(0, 0.0, 0.4), rgb(0x66, 0x66, 0x66))
        self.assertEqualColor(hsl(0, 0.0, 0.5), rgb(0x80, 0x80, 0x80))
        self.assertEqualColor(hsl(0, 0.0, 0.6), rgb(0x99, 0x99, 0x99))
        self.assertEqualColor(hsl(0, 0.0, 0.8), rgb(0xcc, 0xcc, 0xcc))

    def test_hsl_primaries(self):
        self.assertEqualColor(hsl(0, 1.0, 0.5), rgb(0xff, 0x00, 0x00))
        self.assertEqualColor(hsl(60, 1.0, 0.5), rgb(0xff, 0xff, 0x00))
        self.assertEqualColor(hsl(120, 1.0, 0.5), rgb(0x00, 0xff, 0x00))
        self.assertEqualColor(hsl(180, 1.0, 0.5), rgb(0x00, 0xff, 0xff))
        self.assertEqualColor(hsl(240, 1.0, 0.5), rgb(0x00, 0x00, 0xff))
        self.assertEqualColor(hsl(300, 1.0, 0.5), rgb(0xff, 0x00, 0xff))
        self.assertEqualColor(hsl(360, 1.0, 0.5), rgb(0xff, 0x00, 0x00))

    def test_hsl_muted(self):
        self.assertEqualColor(hsl(0, 0.25, 0.25), rgb(0x50, 0x30, 0x30))
        self.assertEqualColor(hsl(60, 0.25, 0.25), rgb(0x50, 0x50, 0x30))
        self.assertEqualColor(hsl(120, 0.25, 0.25), rgb(0x30, 0x50, 0x30))
        self.assertEqualColor(hsl(180, 0.25, 0.25), rgb(0x30, 0x50, 0x50))
        self.assertEqualColor(hsl(240, 0.25, 0.25), rgb(0x30, 0x30, 0x50))
        self.assertEqualColor(hsl(300, 0.25, 0.25), rgb(0x50, 0x30, 0x50))
        self.assertEqualColor(hsl(360, 0.25, 0.25), rgb(0x50, 0x30, 0x30))

        self.assertEqualColor(hsl(0, 0.25, 0.75), rgb(0xcf, 0xaf, 0xaf))
        self.assertEqualColor(hsl(60, 0.25, 0.75), rgb(0xcf, 0xcf, 0xaf))
        self.assertEqualColor(hsl(120, 0.25, 0.75), rgb(0xaf, 0xcf, 0xaf))
        self.assertEqualColor(hsl(180, 0.25, 0.75), rgb(0xaf, 0xcf, 0xcf))
        self.assertEqualColor(hsl(240, 0.25, 0.75), rgb(0xaf, 0xaf, 0xcf))
        self.assertEqualColor(hsl(300, 0.25, 0.75), rgb(0xcf, 0xaf, 0xcf))
        self.assertEqualColor(hsl(360, 0.25, 0.75), rgb(0xcf, 0xaf, 0xaf))

        self.assertEqualColor(hsl(0, 0.75, 0.75), rgb(0xef, 0x8f, 0x8f))
        self.assertEqualColor(hsl(60, 0.75, 0.75), rgb(0xef, 0xef, 0x8f))
        self.assertEqualColor(hsl(120, 0.75, 0.75), rgb(0x8f, 0xef, 0x8f))
        self.assertEqualColor(hsl(180, 0.75, 0.75), rgb(0x8f, 0xef, 0xef))
        self.assertEqualColor(hsl(240, 0.75, 0.75), rgb(0x8f, 0x8f, 0xef))
        self.assertEqualColor(hsl(300, 0.75, 0.75), rgb(0xef, 0x8f, 0xef))
        self.assertEqualColor(hsl(360, 0.75, 0.75), rgb(0xef, 0x8f, 0x8f))

        self.assertEqualColor(hsl(0, 0.75, 0.25), rgb(0x70, 0x10, 0x10))
        self.assertEqualColor(hsl(60, 0.75, 0.25), rgb(0x70, 0x70, 0x10))
        self.assertEqualColor(hsl(120, 0.75, 0.25), rgb(0x10, 0x70, 0x10))
        self.assertEqualColor(hsl(180, 0.75, 0.25), rgb(0x10, 0x70, 0x70))
        self.assertEqualColor(hsl(240, 0.75, 0.25), rgb(0x10, 0x10, 0x70))
        self.assertEqualColor(hsl(300, 0.75, 0.25), rgb(0x70, 0x10, 0x70))
        self.assertEqualColor(hsl(360, 0.75, 0.25), rgb(0x70, 0x10, 0x10))

    def test_hsl_alpha(self):
        self.assertEqualColor(hsl(60, 0.0, 0.0, 0.3), rgb(0x00, 0x00, 0x00, 0.3))
        self.assertEqualColor(hsl(60, 0.0, 1.0, 0.3), rgb(0xff, 0xff, 0xff, 0.3))
        self.assertEqualColor(hsl(60, 1.0, 0.5, 0.3), rgb(0xff, 0xff, 0x00, 0.3))
        self.assertEqualColor(hsl(60, 0.25, 0.25, 0.3), rgb(0x50, 0x50, 0x30, 0.3))
        self.assertEqualColor(hsl(60, 0.25, 0.75, 0.3), rgb(0xcf, 0xcf, 0xaf, 0.3))
        self.assertEqualColor(hsl(60, 0.75, 0.75, 0.3), rgb(0xef, 0xef, 0x8f, 0.3))
        self.assertEqualColor(hsl(60, 0.75, 0.25, 0.3), rgb(0x70, 0x70, 0x10, 0.3))
