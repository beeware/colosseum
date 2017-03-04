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
        self.assertEqual(node.style.render(), "")

    def test_simple_style(self):
        node = TestNode(style=CSS(width=100))
        self.assertEqual(node.style.render(), "width: 100px")

    def test_style_with_dash(self):
        node = TestNode(style=CSS(margin_left=100))
        self.assertEqual(node.style.render(), "margin-left: 100px")

    def test_multi_value_style(self):
        node = TestNode(style=CSS(margin=100))
        self.assertEqual(node.style.render(), "margin: 100px 100px 100px 100px")

    def test_multiple_styles(self):
        node = TestNode(style=CSS(width=100, height=200))
        self.assertEqual(node.style.render(), "height: 200px; width: 100px")
