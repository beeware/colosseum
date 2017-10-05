from unittest import TestCase

from colosseum.constants import MEDIUM, THICK, THIN
from colosseum.declaration import CSS
from colosseum.dimensions import Box, Size


class Display:
    def __init__(self, dpi, width, height):
        self.dpi = dpi
        self.content_width = width
        self.content_height = height

    def fixed_size(self, value):
        return {
            THIN: 1,
            MEDIUM: 5,
            THICK: 10,
        }[value]


class TestNode:
    def __init__(self, style=None, children=None):
        self.children = children if children is not None else []
        self.intrinsic = Size(self)
        self.layout = Box(self)
        self.style = style.copy(self) if style else CSS


def layout_summary(node):
    if node.layout:
        layout = {
            'position': (node.layout.absolute_content_left, node.layout.absolute_content_top),
            'size': (node.layout.content_width, node.layout.content_height),
        }
        if node.children:
            layout['children'] = [
                layout_summary(child)
                for child in node.children
            ]
    else:
        layout = 'NOT DISPLAYED'

    return layout


class LayoutTestCase(TestCase):
    def setUp(self):
        self.display = Display(dpi=96, width=640, height=480)

    def assertLayout(self, node, layout):
        self.assertEqual(layout_summary(node), layout)
