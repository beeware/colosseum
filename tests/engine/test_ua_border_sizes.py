from colosseum.constants import BLOCK, MEDIUM, SOLID, THICK, THIN
from colosseum.declaration import CSS
from colosseum.engine import layout

from ..utils import LayoutTestCase, TestNode


class UABorderSizes(LayoutTestCase):
    def test_thin_border(self):
        root = TestNode(
            style=CSS(display=BLOCK, border_style=SOLID, border_width=THIN, width=50, height=30)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (1, 1), 'size': (50, 30)})

    def test_medium_border(self):
        root = TestNode(
            style=CSS(display=BLOCK, border_style=SOLID, border_width=MEDIUM, width=50, height=30)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (5, 5), 'size': (50, 30)})

    def test_thick_border(self):
        root = TestNode(
            style=CSS(display=BLOCK, border_style=SOLID, border_width=THICK, width=50, height=30)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (10, 10), 'size': (50, 30)})
