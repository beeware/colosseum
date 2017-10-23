from unittest import expectedFailure

from colosseum.constants import AUTO, BLOCK, RTL, SOLID
from colosseum.declaration import CSS
from colosseum.engine import layout

from ...utils import LayoutTestCase, TestNode


class ChildLayoutTests(LayoutTestCase):
    def test_simple_vertical(self):
        child1 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10),
        )
        child2 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10),
        )
        child3 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10),
        )

        root = TestNode(
            name='div',
            style=CSS(display=BLOCK),
            children=[child1, child2, child3]
        )

        layout(self.display, root)

        self.assertLayout(
            root,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (1024, 768)},
                'padding_box': {'position': (0, 0), 'size': (1024, 768)},
                'content': {'position': (0, 0), 'size': (1024, 768)},
                'children': [
                    {
                        'tag': 'div',
                        'border_box': {'position': (0, 0), 'size': (1024, 10)},
                        'padding_box': {'position': (0, 0), 'size': (1024, 10)},
                        'content': {'position': (0, 0), 'size': (1024, 10)},
                    },
                    {
                        'tag': 'div',
                        'border_box': {'position': (0, 10), 'size': (1024, 10)},
                        'padding_box': {'position': (0, 10), 'size': (1024, 10)},
                        'content': {'position': (0, 10), 'size': (1024, 10)},
                    },
                    {
                        'tag': 'div',
                        'border_box': {'position': (0, 20), 'size': (1024, 10)},
                        'padding_box': {'position': (0, 20), 'size': (1024, 10)},
                        'content': {'position': (0, 20), 'size': (1024, 10)},
                    }
                ],
            }
        )

    def test_collapsed_margins(self):
        child1 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=10),
        )
        child2 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=30),
        )
        child3 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=20),
        )

        root = TestNode(
            name='div',
            style=CSS(display=BLOCK),
            children=[child1, child2, child3]
        )

        layout(self.display, root)

        self.assertLayout(
            root,
            {
                'tag': 'div',
                'border_box': {'position': (0, 10), 'size': (1024, 738)},
                'padding_box': {'position': (0, 10), 'size': (1024, 738)},
                'content': {'position': (0, 10), 'size': (1024, 738)},
                'children': [
                    {
                        'tag': 'div',
                        'border_box': {'position': (10, 10), 'size': (1004, 10)},
                        'padding_box': {'position': (10, 10), 'size': (1004, 10)},
                        'content': {'position': (10, 10), 'size': (1004, 10)},
                    },
                    {
                        'tag': 'div',
                        'border_box': {'position': (30, 50), 'size': (964, 10)},
                        'padding_box': {'position': (30, 50), 'size': (964, 10)},
                        'content': {'position': (30, 50), 'size': (964, 10)},
                    },
                    {
                        'tag': 'div',
                        'border_box': {'position': (20, 90), 'size': (984, 10)},
                        'padding_box': {'position': (20, 90), 'size': (984, 10)},
                        'content': {'position': (20, 90), 'size': (984, 10)},
                    }
                ],
            }
        )

    def test_collapse_outside_parent(self):
        grandchild1 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=50),
        )
        grandchild2 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=40),
        )

        child = TestNode(
            name='div',
            style=CSS(display=BLOCK, margin=10),
            children=[grandchild1, grandchild2]
        )

        root = TestNode(
            name='div',
            style=CSS(display=BLOCK),
            children=[child]
        )

        layout(self.display, root)

        self.assertLayout(
            root,
            {
                'tag': 'div',
                'border_box': {'size': (1024, 678), 'position': (0, 50)},
                'padding_box': {'size': (1024, 678), 'position': (0, 50)},
                'content': {'size': (1024, 678), 'position': (0, 50)},
                'children': [
                    {
                        'tag': 'div',
                        'border_box': {'size': (1004, 70), 'position': (10, 50)},
                        'padding_box': {'size': (1004, 70), 'position': (10, 50)},
                        'content': {'size': (1004, 70), 'position': (10, 50)},
                        'children': [
                            {
                                'tag': 'div',
                                'border_box': {'size': (904, 10), 'position': (60, 50)},
                                'padding_box': {'size': (904, 10), 'position': (60, 50)},
                                'content': {'size': (904, 10), 'position': (60, 50)},
                            },
                            {
                                'tag': 'div',
                                'border_box': {'size': (924, 10), 'position': (50, 110)},
                                'padding_box': {'size': (924, 10), 'position': (50, 110)},
                                'content': {'size': (924, 10), 'position': (50, 110)},
                            }
                        ],
                    }
                ],
            }
        )

    def test_overflow_outside_parent(self):
        grandchild1 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=50),
        )
        grandchild2 = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=40),
        )

        child = TestNode(
            name='div',
            style=CSS(display=BLOCK, height=10, margin=10),
            children=[grandchild1, grandchild2]
        )

        root = TestNode(
            name='div',
            style=CSS(display=BLOCK),
            children=[child]
        )

        layout(self.display, root)

        self.assertLayout(
            root,
            {
                'tag': 'div',
                'border_box': {'size': (1024, 708), 'position': (0, 50)},
                'padding_box': {'size': (1024, 708), 'position': (0, 50)},
                'content': {'size': (1024, 708), 'position': (0, 50)},
                'children': [
                    {
                        'tag': 'div',
                        'border_box': {'size': (1004, 10), 'position': (10, 50)},
                        'padding_box': {'size': (1004, 10), 'position': (10, 50)},
                        'content': {'size': (1004, 10), 'position': (10, 50)},
                        'children': [
                            {
                                'tag': 'div',
                                'border_box': {'size': (904, 10), 'position': (60, 50)},
                                'padding_box': {'size': (904, 10), 'position': (60, 50)},
                                'content': {'size': (904, 10), 'position': (60, 50)},
                            },
                            {
                                'tag': 'div',
                                'border_box': {'size': (924, 10), 'position': (50, 110)},
                                'padding_box': {'size': (924, 10), 'position': (50, 110)},
                                'content': {'size': (924, 10), 'position': (50, 110)},
                            }
                        ],
                    }
                ],
            }
        )
