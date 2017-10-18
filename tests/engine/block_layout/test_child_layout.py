from unittest import expectedFailure

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

        self.assertLayout(
            root,
            {
                'margin_box': {'position': (0, 0), 'size': (640, 480)},
                'border_box': {'position': (0, 0), 'size': (640, 480)},
                'padding_box': {'position': (0, 0), 'size': (640, 480)},
                'content': {'position': (0, 0), 'size': (640, 480)},
                'children': [
                    {
                        'margin_box': {'position': (0, 0), 'size': (640, 10)},
                        'border_box': {'position': (0, 0), 'size': (640, 10)},
                        'padding_box': {'position': (0, 0), 'size': (640, 10)},
                        'content': {'position': (0, 0), 'size': (640, 10)},
                    },
                    {
                        'margin_box': {'position': (0, 10), 'size': (640, 10)},
                        'border_box': {'position': (0, 10), 'size': (640, 10)},
                        'padding_box': {'position': (0, 10), 'size': (640, 10)},
                        'content': {'position': (0, 10), 'size': (640, 10)},
                    },
                    {
                        'margin_box': {'position': (0, 20), 'size': (640, 10)},
                        'border_box': {'position': (0, 20), 'size': (640, 10)},
                        'padding_box': {'position': (0, 20), 'size': (640, 10)},
                        'content': {'position': (0, 20), 'size': (640, 10)},
                    }
                ],
            }
        )

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

        self.assertLayout(
            root,
            {
                'margin_box': {'position': (0, 10), 'size': (640, 450)},
                'border_box': {'position': (0, 10), 'size': (640, 450)},
                'padding_box': {'position': (0, 10), 'size': (640, 450)},
                'content': {'position': (0, 10), 'size': (640, 450)},
                'children': [
                    {
                        'margin_box': {'position': (0, 0), 'size': (640, 30)},
                        'border_box': {'position': (10, 10), 'size': (620, 10)},
                        'padding_box': {'position': (10, 10), 'size': (620, 10)},
                        'content': {'position': (10, 10), 'size': (620, 10)},
                    },
                    {
                        'margin_box': {'position': (0, 20), 'size': (640, 70)},
                        'border_box': {'position': (30, 50), 'size': (580, 10)},
                        'padding_box': {'position': (30, 50), 'size': (580, 10)},
                        'content': {'position': (30, 50), 'size': (580, 10)},
                    },
                    {
                        'margin_box': {'position': (0, 70), 'size': (640, 50)},
                        'border_box': {'position': (20, 90), 'size': (600, 10)},
                        'padding_box': {'position': (20, 90), 'size': (600, 10)},
                        'content': {'position': (20, 90), 'size': (600, 10)},
                    }
                ],
            }
        )

    @expectedFailure
    def test_collapse_outside_parent(self):
        # This shouldn't pass... if it ever starts failing, the raw
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

        self.assertLayout(
            root,
            {
                'margin_box': {'size': (640, 390), 'position': (0, 50)},
                'border_box': {'size': (640, 390), 'position': (0, 50)},
                'padding_box': {'size': (640, 390), 'position': (0, 50)},
                'content': {'size': (640, 390), 'position': (0, 50)},
                'children': [
                    {
                        'margin_box': {'size': (640, 90), 'position': (0, 40)},
                        'border_box': {'size': (620, 70), 'position': (10, 50)},
                        'padding_box': {'size': (620, 70), 'position': (10, 50)},
                        'content': {'size': (620, 70), 'position': (10, 50)},
                        'children': [
                            {
                                'margin_box': {'size': (620, 110), 'position': (10, 0)},
                                'border_box': {'size': (520, 10), 'position': (60, 50)},
                                'padding_box': {'size': (520, 10), 'position': (60, 50)},
                                'content': {'size': (520, 10), 'position': (60, 50)},
                            },
                            {
                                'margin_box': {'size': (620, 90), 'position': (10, 70)},
                                'border_box': {'size': (540, 10), 'position': (50, 110)},
                                'padding_box': {'size': (540, 10), 'position': (50, 110)},
                                'content': {'size': (540, 10), 'position': (50, 110)},
                            }
                        ],
                    }
                ],
            }
        )

    @expectedFailure
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

        self.assertLayout(
            root,
            {
                'margin_box': {'size': (640, 420), 'position': (0, 50)},
                'border_box': {'size': (640, 420), 'position': (0, 50)},
                'padding_box': {'size': (640, 420), 'position': (0, 50)},
                'content': {'size': (640, 420), 'position': (0, 50)},
                'children': [
                    {
                        'margin_box': {'size': (640, 30), 'position': (0, 40)},
                        'border_box': {'size': (620, 10), 'position': (10, 50)},
                        'padding_box': {'size': (620, 10), 'position': (10, 50)},
                        'content': {'size': (620, 10), 'position': (10, 50)},
                        'children': [
                            {
                                'margin_box': {'size': (620, 110), 'position': (10, 0)},
                                'border_box': {'size': (520, 10), 'position': (60, 50)},
                                'padding_box': {'size': (520, 10), 'position': (60, 50)},
                                'content': {'size': (520, 10), 'position': (60, 50)},
                            },
                            {
                                'margin_box': {'size': (620, 90), 'position': (10, 70)},
                                'border_box': {'size': (540, 10), 'position': (50, 110)},
                                'padding_box': {'size': (540, 10), 'position': (50, 110)},
                                'content': {'size': (540, 10), 'position': (50, 110)},
                            }
                        ],
                    }
                ],
            }
        )
