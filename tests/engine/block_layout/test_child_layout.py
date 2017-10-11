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

    def test_collapsed_margins(self):
        child1 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=10),
        )
        child2 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=30),
        )
        child3 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=20),
        )

        root = TestNode(
            style=CSS(display=BLOCK),
            children=[child1, child2, child3]
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 10),
            'size': (640, 90),
            'children': [
                {'position': (10, 10), 'size': (620, 10)},
                {'position': (30, 50), 'size': (580, 10)},
                {'position': (20, 90), 'size': (600, 10)},
            ]
        })

    def test_collapse_outside_parent(self):
        grandchild1 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=50),
        )
        grandchild2 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=40),
        )

        child = TestNode(
            style=CSS(display=BLOCK, margin=10),
            children=[grandchild1, grandchild2]
        )

        root = TestNode(
            style=CSS(display=BLOCK),
            children=[child]
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 50),
            'size': (640, 70),
            'children': [
                {
                    'position': (10, 50),
                    'size': (620, 70),
                    'children': [
                        {'position': (60, 50), 'size': (520, 10)},
                        {'position': (50, 110), 'size': (540, 10)},
                    ]
                }
            ]
        })

    def test_overflow_outside_parent(self):
        grandchild1 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=50),
        )
        grandchild2 = TestNode(
            style=CSS(display=BLOCK, height=10, margin=40),
        )

        child = TestNode(
            style=CSS(display=BLOCK, height=10, margin=10),
            children=[grandchild1, grandchild2]
        )

        root = TestNode(
            style=CSS(display=BLOCK),
            children=[child]
        )

        layout(self.display, root)

        self.assertLayout(root, {
            'position': (0, 50),
            'size': (640, 10),
            'children': [
                {
                    'position': (10, 50),
                    'size': (620, 10),
                    'children': [
                        {'position': (60, 50), 'size': (520, 10)},
                        {'position': (50, 110), 'size': (540, 10)},
                    ]
                }
            ]
        })
