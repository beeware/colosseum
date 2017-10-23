from colosseum.constants import AUTO, BLOCK, RTL, SOLID
from colosseum.declaration import CSS

from ...utils import LayoutTestCase, TestNode


class WidthTests(LayoutTestCase):
    def test_no_horizontal_properties(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, height=10)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (1024, 10)},
                'padding_box': {'position': (0, 0), 'size': (1024, 10)},
                'content': {'position': (0, 0), 'size': (1024, 10)},
            }
        )

    def test_left_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, height=10, margin_left=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (1024, 10)},
                'padding_box': {'position': (0, 0), 'size': (1024, 10)},
                'content': {'position': (0, 0), 'size': (1024, 10)},
            }
        )

    def test_right_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, height=10, margin_right=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (1024, 10)},
                'padding_box': {'position': (0, 0), 'size': (1024, 10)},
                'content': {'position': (0, 0), 'size': (1024, 10)},
            }
        )

    def test_left_and_right_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (1024, 10)},
                'padding_box': {'position': (0, 0), 'size': (1024, 10)},
                'content': {'position': (0, 0), 'size': (1024, 10)},
            }
        )

    def test_width(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=50, height=10)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_width_auto_left_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (974, 0), 'size': (50, 10)},
                'padding_box': {'position': (974, 0), 'size': (50, 10)},
                'content': {'position': (974, 0), 'size': (50, 10)},
            }
        )

    def test_width_auto_right_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=50, height=10, margin_right=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (50, 10)},
                'padding_box': {'position': (0, 0), 'size': (50, 10)},
                'content': {'position': (0, 0), 'size': (50, 10)},
            }
        )

    def test_width_auto_left_and_right_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=50, height=10, margin_left=AUTO, margin_right=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (487, 0), 'size': (50, 10)},
                'padding_box': {'position': (487, 0), 'size': (50, 10)},
                'content': {'position': (487, 0), 'size': (50, 10)},
            }
        )

    def test_width_fixed_left_and_right_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=50, height=10, margin_left=30, margin_right=40)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (30, 0), 'size': (50, 10)},
                'padding_box': {'position': (30, 0), 'size': (50, 10)},
                'content': {'position': (30, 0), 'size': (50, 10)},
            }
        )

    def test_width_fixed_left_and_right_margin_rtl(self):
        node = TestNode(
            name='div', style=CSS(
                display=BLOCK, width=50, height=10,
                margin_left=30, margin_right=40, direction=RTL
            )
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (934, 0), 'size': (50, 10)},
                'padding_box': {'position': (934, 0), 'size': (50, 10)},
                'content': {'position': (934, 0), 'size': (50, 10)},
            }
        )

    def test_width_exceeds_parent(self):
        node = TestNode(
            name='div', style=CSS(
                display=BLOCK, width=500, height=20,
                padding=50, border_width=60, border_style=SOLID,
                margin=70
            )
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (70, 70), 'size': (720, 240)},
                'padding_box': {'position': (130, 130), 'size': (600, 120)},
                'content': {'position': (180, 180), 'size': (500, 20)},
            }
        )

    def test_width_exceeds_parent_auto_left_and_right_margins(self):
        node = TestNode(
            name='div', style=CSS(
                display=BLOCK, width=500, height=20,
                padding=50, border_width=60, border_style=SOLID,
                margin_left=AUTO, margin_right=AUTO
            )
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (152, 0), 'size': (720, 240)},
                'padding_box': {'position': (212, 60), 'size': (600, 120)},
                'content': {'position': (262, 110), 'size': (500, 20)},
            }
        )


class HeightTests(LayoutTestCase):
    def test_no_vertical_properties(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=10)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (10, 0)},
                'padding_box': {'position': (0, 0), 'size': (10, 0)},
                'content': {'position': (0, 0), 'size': (10, 0)},
            }
        )

    def test_height(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=10, height=50)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (10, 50)},
                'padding_box': {'position': (0, 0), 'size': (10, 50)},
                'content': {'position': (0, 0), 'size': (10, 50)},
            }
        )

    def test_height_auto_top_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=10, height=50, margin_top=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (10, 50)},
                'padding_box': {'position': (0, 0), 'size': (10, 50)},
                'content': {'position': (0, 0), 'size': (10, 50)},
            }
        )

    def test_height_auto_bottom_margin(self):
        node = TestNode(
            name='div', style=CSS(display=BLOCK, width=10, height=50, margin_bottom=AUTO)
        )

        self.layout_node(node)

        self.assertLayout(
            node,
            {
                'tag': 'div',
                'border_box': {'position': (0, 0), 'size': (10, 50)},
                'padding_box': {'position': (0, 0), 'size': (10, 50)},
                'content': {'position': (0, 0), 'size': (10, 50)},
            }
        )
