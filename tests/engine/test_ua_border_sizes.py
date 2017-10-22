from colosseum.constants import BLOCK, MEDIUM, SOLID, THICK, THIN
from colosseum.declaration import CSS

from ..utils import LayoutTestCase, TestNode


class UABorderSizes(LayoutTestCase):
    def test_thin_border(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, border_style=SOLID, border_width=THIN, width=50, height=30)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (52, 32)},
                'padding_box': {'position': (1, 1), 'size': (50, 30)},
                'content': {'position': (1, 1), 'size': (50, 30)},
            }
        )

    def test_medium_border(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, border_style=SOLID, border_width=MEDIUM, width=50, height=30)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (60, 40)},
                'padding_box': {'position': (5, 5), 'size': (50, 30)},
                'content': {'position': (5, 5), 'size': (50, 30)},
            }
        )

    def test_thick_border(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, border_style=SOLID, border_width=THICK, width=50, height=30)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (70, 50)},
                'padding_box': {'position': (10, 10), 'size': (50, 30)},
                'content': {'position': (10, 10), 'size': (50, 30)},
            }
        )
