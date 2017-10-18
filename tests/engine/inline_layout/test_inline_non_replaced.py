from colosseum.constants import AUTO, INLINE
from colosseum.declaration import CSS

from ...utils import LayoutTestCase, TestNode


class WidthTests(LayoutTestCase):
    def test_no_horizontal_properties(self):
        node = TestNode(
            style=CSS(display=INLINE)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'margin_box': {'position': (0, 0), 'size': (50, 10)},
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_auto_left_margin(self):
        node = TestNode(
            style=CSS(display=INLINE, margin_left=AUTO)
        )
        node.intrinsic.width = 50
        node.intrinsic.height = 10

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'margin_box': {'position': (0, 0), 'size': (50, 10)},
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

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'margin_box': {'position': (0, 0), 'size': (50, 10)},
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )
