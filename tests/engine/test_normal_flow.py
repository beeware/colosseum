from unittest import TestCase

from colosseum.constants import AUTO, BLOCK
from colosseum.declaration import CSS
from colosseum.engine import layout

from ..utils import Display, TestNode, layout_summary


class BlockElementNormalFlowTests(TestCase):
    def setUp(self):
        self.display = Display(dpi=96, width=640, height=480)

    def assertLayout(self, node, layout):
        self.assertEqual(layout_summary(node), layout)

    def test_single_element(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (640, 10)
        })

    def test_single_element_auto_left_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_left=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (640, 10)
        })

    def test_single_element_auto_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (640, 10)
        })

    def test_single_element_auto_left_and_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (640, 10)
        })

    def test_single_element_with_width(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (50, 10)
        })

    def test_single_element_with_width_auto_left_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (50, 10)
        })

    def test_single_element_with_width_auto_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (50, 10)
        })

    def test_single_element_with_width_auto_left_and_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (295, 0),
            'size': (50, 10)
        })
