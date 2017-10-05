from colosseum.constants import AUTO, BLOCK, RTL, SOLID
from colosseum.declaration import CSS
from colosseum.engine import layout

from ...utils import LayoutTestCase, TestNode


class ChildLayoutTests(LayoutTestCase):
    def test_simple_vertical(self):
        child1 = TestNode(
            style=CSS(display=BLOCK, height=10),
        )
        child2 = TestNode(
            style=CSS(display=BLOCK, height=10),
        )
        child3 = TestNode(
            style=CSS(display=BLOCK, height=10),
        )

        root = TestNode(
            style=CSS(display=BLOCK),
            children=[child1, child2, child3]
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 0),
            'size': (640, 30),
            'children': [
                {'position': (0, 0), 'size': (640, 10)},
                {'position': (0, 10), 'size': (640, 10)},
                {'position': (0, 20), 'size': (640, 10)},
            ]
        })
