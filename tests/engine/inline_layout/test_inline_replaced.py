from colosseum.constants import AUTO, INLINE
from colosseum.declaration import CSS
from colosseum.engine import layout

from ...utils import LayoutTestCase, TestNode


class WidthTests(LayoutTestCase):
    def test_auto_left_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_left=AUTO)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_auto_right_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_right=AUTO)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_intrinsic_height_and_ratio(self):
        node = TestNode(
            style=CSS(display=INLINE)
        )
        node.intrinsic.height = 10
        node.intrinsic.ratio = 3.0
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (30, 10)},
                'padding_box': {'position': (0, 0), 'size': (30, 10)},
                'content': {'position': (0, 0), 'size': (30, 10)},
            }
        )

    def test_intrinsic_ratio(self):
        node = TestNode(
            style=CSS(display=INLINE)
        )
        node.intrinsic.ratio = 1.5
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (640, 960)},
                'padding_box': {'position': (0, 0), 'size': (640, 960)},
                'content': {'position': (0, 0), 'size': (640, 960)},
            }
        )

    def test_intrinsic_width(self):
        node = TestNode(
            style=CSS(display=INLINE)
        )
        node.intrinsic.width = 50
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 25)},
                'padding_box': {'position': (0, 0), 'size': (50, 25)},
                'content': {'position': (0, 0), 'size': (50, 25)},
            }
        )

    def test_height_and_intrinsic_width(self):
        node = TestNode(
            style=CSS(display=INLINE, height=30)
        )
        node.intrinsic.width = 50
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 30)},
                'padding_box': {'position': (0, 0), 'size': (50, 30)},
                'content': {'position': (0, 0), 'size': (50, 30)},
            }
        )

    def test_no_intrinsic_size(self):
        node = TestNode(
            style=CSS(display=INLINE)
        )
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (300, 150)},
                'padding_box': {'position': (0, 0), 'size': (300, 150)},
                'content': {'position': (0, 0), 'size': (300, 150)},
            }
        )


class HeightTests(LayoutTestCase):
    def test_auto_top_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_top=AUTO)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_auto_bottom_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_bottom=AUTO)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_width_and_intrinsic_height(self):
        node = TestNode(
            style=CSS(display=INLINE, width=50)
        )
        node.intrinsic.height = 30
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 30)},
                'padding_box': {'position': (0, 0), 'size': (50, 30)},
                'content': {'position': (0, 0), 'size': (50, 30)},
            }
        )

    def test_width_and_height(self):
        node = TestNode(
            style=CSS(display=INLINE, width=50, height=30)
        )
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (50, 30)},
                'padding_box': {'position': (0, 0), 'size': (50, 30)},
                'content': {'position': (0, 0), 'size': (50, 30)},
            }
        )

    def test_no_intrinsic_size_auto_top_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_top=AUTO)
        )
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (300, 150)},
                'padding_box': {'position': (0, 0), 'size': (300, 150)},
                'content': {'position': (0, 0), 'size': (300, 150)},
            }
        )

    def test_no_intrinsic_size_auto_bottom_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_bottom=AUTO)
        )
        node.intrinsic.is_replaced = True

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'border_box': {'position': (0, 0), 'size': (300, 150)},
                'padding_box': {'position': (0, 0), 'size': (300, 150)},
                'content': {'position': (0, 0), 'size': (300, 150)},
            }
        )
