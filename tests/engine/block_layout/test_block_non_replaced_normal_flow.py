from colosseum.constants import AUTO, BLOCK, RTL, SOLID
from colosseum.declaration import CSS
from colosseum.engine import layout

from ...utils import Display, LayoutTestCase, TestNode, layout_summary


class WidthTests(LayoutTestCase):
    def test_no_horizontal_properties(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (640, 10)})

    def test_left_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_left=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (640, 10)})

    def test_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (640, 10)})

    def test_left_and_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (640, 10)})

    def test_width(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (50, 10)})

    def test_width_auto_left_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (590, 0), 'size': (50, 10)})

    def test_width_auto_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (50, 10)})

    def test_width_auto_left_and_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (295, 0), 'size': (50, 10)})

    def test_width_fixed_left_and_right_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=50, height=10, margin_left=30, margin_right=40)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (30, 0), 'size': (50, 10)})

    def test_width_fixed_left_and_right_margin_rtl(self):
        root = TestNode(
            style=CSS(
                display=BLOCK, width=50, height=10,
                margin_left=30, margin_right=40, direction=RTL
            )
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (550, 0), 'size': (50, 10)})

    def test_width_exceeds_parent(self):
        root = TestNode(
            style=CSS(
                display=BLOCK, width=500, height=20,
                padding=50, border_width=60, border_style=SOLID,
                margin=70
            )
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (180, 180), 'size': (500, 20)})

    def test_width_exceeds_parent_auto_left_and_right_margins(self):
        root = TestNode(
            style=CSS(
                display=BLOCK, width=500, height=20,
                padding=50, border_width=60, border_style=SOLID,
                margin_left=AUTO, margin_right=AUTO
            )
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (110, 110), 'size': (500, 20)})


class HeightTests(LayoutTestCase):
    def test_no_vertical_properties(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=10)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (10, 0)})

    def test_height(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=10, height=50)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (10, 50)})

    def test_height_auto_top_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=10, height=50, margin_top=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (10, 50)})

    def test_height_auto_bottom_margin(self):
        root = TestNode(
            style=CSS(display=BLOCK, width=10, height=50, margin_bottom=AUTO)
        )

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (10, 50)})
