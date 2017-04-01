from unittest import TestCase

from colosseum.constants import (
    ABSOLUTE, RELATIVE,
    ROW, COLUMN,
    FLEX_START, FLEX_END,
    AUTO, CENTER, STRETCH,
    WRAP, NOWRAP
)
from colosseum.declaration import CSS

from .utils import TestNode


class RenderTest(TestCase):
    def test_default_styles(self):
        node = TestNode()
        self.assertEqual(str(node.style), "")

    def test_simple_style(self):
        node = TestNode(style=CSS(width=100))
        self.assertEqual(str(node.style), "width: 100px")

    def test_style_with_dash(self):
        node = TestNode(style=CSS(margin_left=100))
        self.assertEqual(str(node.style), "margin-left: 100px")

    def test_multi_value_style(self):
        node = TestNode(style=CSS(margin=100))
        self.assertEqual(str(node.style), "margin-bottom: 100px; margin-left: 100px; margin-right: 100px; margin-top: 100px")

    def test_multiple_styles(self):
        node = TestNode(style=CSS(width=100, height=200))
        self.assertEqual(str(node.style), "height: 200px; width: 100px")
