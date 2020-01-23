from unittest import TestCase

from colosseum.units import px
from colosseum.shapes import Rect


class ShapeUnitTests(TestCase):

    def test_shape_properties(self):
        rect = Rect(1, 3, 2, 4)
        self.assertEqual(rect.top, 1)
        self.assertEqual(rect.right, 3)
        self.assertEqual(rect.left, 2)
        self.assertEqual(rect.bottom, 4)

    def test_shape_methods(self):
        rect = Rect(1, 3, 2, 4)
        self.assertEqual(rect.to_tuple(), (1, 3, 2, 4))

    def test_shape_equality(self):
        rect1 = Rect(1 * px, 3 * px, 2 * px, 4 * px)
        rect2 = Rect(1 * px, 3 * px, 2 * px, 4 * px)
        self.assertEqual(rect1, rect2)

    def test_shape_string(self):
        rect = Rect(1 * px, 3 * px, 2 * px, 4 * px)
        self.assertEqual(str(rect), 'rect(1px, 3px, 2px, 4px)')
        self.assertEqual(repr(rect), 'rect(1px, 3px, 2px, 4px)')
