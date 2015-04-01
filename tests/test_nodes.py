try:
    from unittest import TestCase
except ImportError:
    from unittest2 import TestCase

from colosseum.nodes import CSSNode, UnknownCSSStyleException


class CSSNodeTest(TestCase):
    def test_style_in_constructor(self):
        node = CSSNode(width=10, height=20)

        self.assertEqual(node.width, 10)
        self.assertEqual(node.height, 20)
        self.assertIsNone(node.top)

    def test_unknown_style_in_constructor(self):
        with self.assertRaises(TypeError):
            CSSNode(doesnt_exist=10)

    def test_bulk_style(self):
        node = CSSNode(width=10, height=20)

        node.style(width=30, height=40, top=50)

        self.assertEqual(node.width, 30)
        self.assertEqual(node.height, 40)
        self.assertEqual(node.top, 50)

    def test_unknown_style_in_bulk(self):
        node = CSSNode(width=10, height=20)

        with self.assertRaises(UnknownCSSStyleException):
            node.style(width=30, height=40, top=50, doesnt_exist=60)

