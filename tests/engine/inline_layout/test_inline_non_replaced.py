from colosseum.constants import AUTO, INLINE
from colosseum.declaration import CSS
from colosseum.engine import layout

from ...utils import LayoutTestCase, TestNode


class WidthTests(LayoutTestCase):
    def test_no_horizontal_properties(self):
        root = TestNode(
            style=CSS(display=INLINE)
        )
        root.intrinsic.width = 50
        root.intrinsic.height = 10

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (50, 10)})

    def test_auto_left_margin(self):
        root = TestNode(
            style=CSS(display=INLINE, margin_left=AUTO)
        )
        root.intrinsic.width = 50
        root.intrinsic.height = 10

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (50, 10)})

    def test_auto_right_margin(self):
        root = TestNode(
            style=CSS(display=INLINE, margin_right=AUTO)
        )
        root.intrinsic.width = 50
        root.intrinsic.height = 10

        layout(self.display, root)

        self.assertLayout(root, {'position': (0, 0), 'size': (50, 10)})
