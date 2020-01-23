from unittest import TestCase

from colosseum.units import px
from colosseum.wrappers import BorderSpacing


class BorderSpacingTests(TestCase):

    def test_valid_1_arg(self):
        border_spacing = BorderSpacing('inherit')
        self.assertEqual(border_spacing.horizontal, 'inherit')
        self.assertEqual(border_spacing.vertical, 'inherit')
        self.assertEqual(str(border_spacing), 'inherit')
        self.assertEqual(repr(border_spacing), 'BorderSpacing("inherit")')

        border_spacing = BorderSpacing('1')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '1')
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1')")

        border_spacing = BorderSpacing(1)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 1)
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1)")

        border_spacing = BorderSpacing(1 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 1 * px)
        self.assertEqual(str(border_spacing), '1px')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1px)")

    def test_valid_2_arg(self):
        border_spacing = BorderSpacing('1', '2')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '2')
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1', '2')")

        border_spacing = BorderSpacing(1, 2)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 2)
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1, 2)')

        border_spacing = BorderSpacing(1 * px, 2 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 2 * px)
        self.assertEqual(str(border_spacing), '1px 2px')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1px, 2px)')

    def test_invalid_arg_number(self):
        with self.assertRaises(TypeError):
            BorderSpacing(1, 2, 3)

    def test_invalid_arg_type(self):
        with self.assertRaises(TypeError):
            BorderSpacing([1])

        with self.assertRaises(TypeError):
            BorderSpacing([1], [2])
