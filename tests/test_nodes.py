try:
    from unittest import TestCase
except ImportError:
    from unittest2 import TestCase

from colosseum.nodes import CSSNode, UnknownCSSStyleException


class CSSNodeTest(TestCase):
    def test_style_in_constructor(self):
        "A CSSNode can be constructed with a style"
        node = CSSNode(width=10, height=20)

        self.assertEqual(node.width, 10)
        self.assertEqual(node.height, 20)
        self.assertIsNone(node.top)

    def test_unknown_style_in_constructor(self):
        "Unknown style properties in a constructor raise an exception"
        with self.assertRaises(TypeError):
            CSSNode(doesnt_exist=10)

    def test_set_style(self):
        "Individual style properties can be set"
        node = CSSNode(width=10, height=20)

        node.width = 30
        node.height = 40
        node.top = 50

        self.assertEqual(node.width, 30)
        self.assertEqual(node.height, 40)
        self.assertEqual(node.top, 50)

    def test_delete_style(self):
        "Individual style properties can be removed"
        node = CSSNode(width=10, height=20)

        del(node.width)
        del(node.height)

        self.assertIsNone(node.width)
        self.assertIsNone(node.height)
        self.assertIsNone(node.top)

    def test_bulk_style(self):
        "Style properties can be set in bulk"
        node = CSSNode(width=10, height=20)

        node.style(width=30, height=40, top=50)

        self.assertEqual(node.width, 30)
        self.assertEqual(node.height, 40)
        self.assertEqual(node.top, 50)

    def test_unknown_style_in_bulk(self):
        "Bulk style-set method raises exception on unknown style"
        node = CSSNode(width=10, height=20)

        with self.assertRaises(UnknownCSSStyleException):
            node.style(width=30, height=40, top=50, doesnt_exist=60)
