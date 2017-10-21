from unittest import TestCase

from colosseum.dimensions import Box
from .utils import TestNode


class SizeTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.node = TestNode()
        self.node.layout = Box(self.node)
        # Mark the layout as "in calculation"
        self.node.layout.dirty = None

    def assertSize(self, size, values):
        self.assertEqual(values[0], size.width)
        self.assertEqual(values[1], size.height)
        self.assertEqual(values[2], size.exact_width)
        self.assertEqual(values[3], size.exact_height)
        self.assertEqual(values[4], size.ratio)
        self.assertEqual(values[5], size.is_replaced)

    def test_initial_state(self):
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has not been touched.
        self.assertIsNone(self.node.layout.dirty)

    def test_set_width(self):
        self.node.intrinsic.width = 10
        self.assertSize(self.node.intrinsic, (10, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the width to the same value
        self.node.intrinsic.width = 10
        self.assertSize(self.node.intrinsic, (10, None, True, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the width to something new
        self.node.intrinsic.width = 20
        self.assertSize(self.node.intrinsic, (20, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_height(self):
        self.node.intrinsic.height = 10
        self.assertSize(self.node.intrinsic, (None, 10, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the height to the same value
        self.node.intrinsic.height = 10
        self.assertSize(self.node.intrinsic, (None, 10, True, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the height to something new
        self.node.intrinsic.height = 20
        self.assertSize(self.node.intrinsic, (None, 20, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_width(self):
        self.node.intrinsic.exact_width = False
        self.assertSize(self.node.intrinsic, (None, None, False, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact_width to the same value
        self.node.intrinsic.exact_width = False
        self.assertSize(self.node.intrinsic, (None, None, False, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact_width to something new
        self.node.intrinsic.exact_width = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_height(self):
        self.node.intrinsic.exact_height = False
        self.assertSize(self.node.intrinsic, (None, None, True, False, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact height to the same value
        self.node.intrinsic.exact_height = False
        self.assertSize(self.node.intrinsic, (None, None, True, False, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact height to something else
        self.node.intrinsic.exact_height = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_ratio(self):
        self.node.intrinsic.ratio = 0.5
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.5, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the ratio to the same value
        self.node.intrinsic.ratio = 0.5
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.5, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the ratio to something else
        self.node.intrinsic.ratio = 0.75
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.75, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_is_replaced(self):
        self.node.intrinsic.is_replaced = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, True))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set is_replaced to the same value
        self.node.intrinsic.is_replaced = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, True))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set is_replaced to something else
        self.node.intrinsic.is_replaced = False
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)


class BoxTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.node = TestNode()
        self.node.layout = Box(self.node)
        self.node.layout.content_width = 10
        self.node.layout.content_height = 16

        self.child1 = TestNode()
        self.child1.layout.content_width = 10
        self.child1.layout.content_height = 16
        self.child2 = TestNode()

        self.grandchild1_1 = TestNode()
        self.grandchild1_1.layout.content_width = 10
        self.grandchild1_1.layout.content_height = 16
        self.grandchild1_2 = TestNode()

        self.node.children = [self.child1, self.child2]
        self.child1.children = [self.grandchild1_1, self.grandchild1_2]

    def assertLayout(self, box, expected):
        actual = {}
        if 'origin' in expected:
            actual['origin'] = (box._origin_left, box._origin_top)

        if 'size' in expected:
            actual['size'] = {}
            if 'border' in expected['size']:
                actual['size']['border'] = (box.border_box_width, box.border_box_height)

            if 'padding' in expected['size']:
                actual['size']['padding'] = (box.padding_box_width, box.padding_box_height)

            if 'content' in expected['size']:
                actual['size']['content'] = (box.content_width, box.content_height)

        if 'relative' in expected:
            actual['relative'] = {}
            if 'border' in expected['relative']:
                actual['relative']['border'] = (
                    box.border_box_top,
                    box.border_box_right,
                    box.border_box_bottom,
                    box.border_box_left,
                )

            if 'padding' in expected['relative']:
                actual['relative']['padding'] = (
                    box.padding_box_top,
                    box.padding_box_right,
                    box.padding_box_bottom,
                    box.padding_box_left,
                )

            if 'content' in expected['relative']:
                actual['relative']['content'] = (
                    box.content_top,
                    box.content_right,
                    box.content_bottom,
                    box.content_left,
                )

        if 'absolute' in expected:
            actual['absolute'] = {}
            if 'border' in expected['absolute']:
                actual['absolute']['border'] = (
                    box.absolute_border_box_top,
                    box.absolute_border_box_right,
                    box.absolute_border_box_bottom,
                    box.absolute_border_box_left,
                )

            if 'padding' in expected['absolute']:
                actual['absolute']['padding'] = (
                    box.absolute_padding_box_top,
                    box.absolute_padding_box_right,
                    box.absolute_padding_box_bottom,
                    box.absolute_padding_box_left,
                )

            if 'content' in expected['absolute']:
                actual['absolute']['content'] = (
                    box.absolute_content_top,
                    box.absolute_content_right,
                    box.absolute_content_bottom,
                    box.absolute_content_left,
                )

        self.assertEqual(actual, expected)

    def test_repr(self):
        self.node.layout._origin_top = 1
        self.node.layout._origin_left = 2
        self.assertEqual(repr(self.node.layout), "<Box (10x16 @ 2,1)>")

    def test_initial(self):
        # Core attributes have been stored
        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {
                    'content': (10, 16),
                    'padding': (10, 16),
                    'border': (10, 16),
                },
                'relative': {
                    'content': (0, 10, 16, 0),
                    'padding': (0, 10, 16, 0),
                    'border': (0, 10, 16, 0),
                },
                'absolute': {
                    'content': (0, 10, 16, 0),
                    'padding': (0, 10, 16, 0),
                    'border': (0, 10, 16, 0),
                }
            }
        )

    def test_set_top(self):
        self.node.layout.content_top = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (5, 10, 21, 0)},
                'absolute': {'content': (5, 10, 21, 0)},
            }
        )

        # Set the top to a new value
        self.node.layout.content_top = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 10, 23, 0)},
                'absolute': {'content': (7, 10, 23, 0)},
            }
        )

    def test_set_left(self):
        self.node.layout.content_left = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 15, 16, 5)},
                'absolute': {'content': (0, 15, 16, 5)},
            }
        )

        # Set the left to a new value
        self.node.layout.content_left = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 17, 16, 7)},
                'absolute': {'content': (0, 17, 16, 7)},
            }
        )

    def test_set_height(self):
        self.node.layout.content_height = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 5)},
                'relative': {'content': (0, 10, 5, 0)},
                'absolute': {'content': (0, 10, 5, 0)},
            }
        )

        # Set the height to a new value
        self.node.layout.content_height = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 7)},
                'relative': {'content': (0, 10, 7, 0)},
                'absolute': {'content': (0, 10, 7, 0)},
            }
        )

    def test_set_width(self):
        self.node.layout.content_width = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (5, 16)},
                'relative': {'content': (0, 5, 16, 0)},
                'absolute': {'content': (0, 5, 16, 0)},
            }
        )

        # Set the width to a new value
        self.node.layout.content_width = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (7, 16)},
                'relative': {'content': (0, 7, 16, 0)},
                'absolute': {'content': (0, 7, 16, 0)},
            }
        )

    def test_descendent_offsets(self):
        self.node.layout.content_top = 7
        self.node.layout.content_left = 8

        self.child1.layout.content_top = 9
        self.child1.layout.content_left = 10

        self.grandchild1_1.layout.content_top = 11
        self.grandchild1_1.layout.content_left = 12

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (7, 18, 23, 8)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (8, 7),
                'size': {'content': (10, 16)},
                'relative': {'content': (9, 20, 25, 10)},
                'absolute': {'content': (16, 28, 32, 18)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (18, 16),
                'size': {'content': (10, 16)},
                'relative': {'content': (11, 22, 27, 12)},
                'absolute': {'content': (27, 40, 43, 30)},
            }
        )

        # Modify the grandchild position
        self.grandchild1_1.layout.content_top = 13
        self.grandchild1_1.layout.content_left = 14

        # Only the grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (7, 18, 23, 8)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (8, 7),
                'size': {'content': (10, 16)},
                'relative': {'content': (9, 20, 25, 10)},
                'absolute': {'content': (16, 28, 32, 18)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (18, 16),
                'size': {'content': (10, 16)},
                'relative': {'content': (13, 24, 29, 14)},
                'absolute': {'content': (29, 42, 45, 32)},
            }
        )

        # Modify the child position
        self.child1.layout.content_top = 15
        self.child1.layout.content_left = 16

        # The child and grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (7, 18, 23, 8)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (8, 7),
                'size': {'content': (10, 16)},
                'relative': {'content': (15, 26, 31, 16)},
                'absolute': {'content': (22, 34, 38, 24)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (24, 22),
                'size': {'content': (10, 16)},
                'relative': {'content': (13, 24, 29, 14)},
                'absolute': {'content': (35, 48, 51, 38)},
            }
        )

    def test_dirty_handling(self):
        self.node.layout.dirty = None
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_2.layout.dirty)

        self.node.layout.dirty = True
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_2.layout.dirty)

        self.node.layout.dirty = None
        self.grandchild1_2.layout.dirty = False
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertFalse(self.grandchild1_2.layout.dirty)

        self.node.layout.dirty = None
        self.child1.layout.dirty = False
        self.assertIsNone(self.node.layout.dirty)
        self.assertFalse(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertFalse(self.grandchild1_1.layout.dirty)
        self.assertFalse(self.grandchild1_2.layout.dirty)

    def test_margins_and_borders(self):
        self.node.layout._origin_top = 100
        self.node.layout._origin_left = 200

        self.node.layout.content_top = 50
        self.node.layout.content_left = 75

        self.assertLayout(
            self.node.layout,
            {
                'origin': (200, 100),
                'size': {
                    'content': (10, 16),
                    'padding': (10, 16),
                    'border': (10, 16),
                },
                'relative': {
                    'content': (50, 85, 66, 75),
                    'padding': (50, 85, 66, 75),
                    'border': (50, 85, 66, 75),
                },
                'absolute': {
                    'content': (150, 285, 166, 275),
                    'padding': (150, 285, 166, 275),
                    'border': (150, 285, 166, 275),
                },
            }
        )

        # Add a margin.
        self.node.layout.margin_top = 1
        self.node.layout.margin_right = 2
        self.node.layout.margin_bottom = 3
        self.node.layout.margin_left = 4

        self.assertLayout(
            self.node.layout,
            {
                'origin': (200, 100),
                'size': {
                    'content': (10, 16),
                    'padding': (10, 16),
                    'border': (10, 16),
                },
                'relative': {
                    'content': (50, 85, 66, 75),
                    'padding': (50, 85, 66, 75),
                    'border': (50, 85, 66, 75),
                },
                'absolute': {
                    'content': (150, 285, 166, 275),
                    'padding': (150, 285, 166, 275),
                    'border': (150, 285, 166, 275),

                },
            }
        )

        # Add a border. This will push out the margin box.
        self.node.layout.border_top_width = 5
        self.node.layout.border_right_width = 6
        self.node.layout.border_bottom_width = 7
        self.node.layout.border_left_width = 8

        self.assertLayout(
            self.node.layout,
            {
                'origin': (200, 100),
                'size': {
                    'content': (10, 16),
                    'padding': (10, 16),
                    'border': (24, 28),
                },
                'relative': {
                    'content': (50, 85, 66, 75),
                    'padding': (50, 85, 66, 75),
                    'border': (45, 91, 73, 67),
                },
                'absolute': {
                    'content': (150, 285, 166, 275),
                    'padding': (150, 285, 166, 275),
                    'border': (145, 291, 173, 267),
                },
            }
        )

        # Add padding. This will push out the margin and border boxes.
        self.node.layout.padding_top = 9
        self.node.layout.padding_right = 10
        self.node.layout.padding_bottom = 11
        self.node.layout.padding_left = 12

        self.assertLayout(
            self.node.layout,
            {
                'origin': (200, 100),
                'size': {
                    'content': (10, 16),
                    'padding': (32, 36),
                    'border': (46, 48),
                },
                'relative': {
                    'content': (50, 85, 66, 75),
                    'padding': (41, 95, 77, 63),
                    'border': (36, 101, 84, 55),
                },
                'absolute': {
                    'content': (150, 285, 166, 275),
                    'padding': (141, 295, 177, 263),
                    'border': (136, 301, 184, 255),
                },
            }
        )

    def test_relative_equalities(self):
        # Move the box around and set some borders.
        self.node.layout.origin_top = 100
        self.node.layout.origin_left = 200

        self.node.layout.content_top = 50
        self.node.layout.content_left = 75

        self.node.layout.margin_top = 1
        self.node.layout.margin_right = 2
        self.node.layout.margin_bottom = 3
        self.node.layout.margin_left = 4

        self.node.layout.border_top_width = 5
        self.node.layout.border_right_width = 6
        self.node.layout.border_bottom_width = 7
        self.node.layout.border_left_width = 8

        self.node.layout.padding_top = 9
        self.node.layout.padding_right = 10
        self.node.layout.padding_bottom = 11
        self.node.layout.padding_left = 12

        self.assertEqual(
            self.node.layout.content_left + self.node.layout.content_width,
            self.node.layout.content_right
        )
        self.assertEqual(
            self.node.layout.content_top + self.node.layout.content_height,
            self.node.layout.content_bottom
        )

        self.assertEqual(
            self.node.layout.padding_box_left + self.node.layout.padding_box_width,
            self.node.layout.padding_box_right
        )
        self.assertEqual(
            self.node.layout.padding_box_top + self.node.layout.padding_box_height,
            self.node.layout.padding_box_bottom
        )

        self.assertEqual(
            self.node.layout.border_box_left + self.node.layout.border_box_width,
            self.node.layout.border_box_right
        )
        self.assertEqual(
            self.node.layout.border_box_top + self.node.layout.border_box_height,
            self.node.layout.border_box_bottom
        )

    def test_absolute_equalities(self):
        # Move the box around and set some borders.
        self.node.layout.origin_top = 100
        self.node.layout.origin_left = 200

        self.node.layout.content_top = 50
        self.node.layout.content_left = 75

        self.node.layout.margin_top = 1
        self.node.layout.margin_right = 2
        self.node.layout.margin_bottom = 3
        self.node.layout.margin_left = 4

        self.node.layout.border_top_width = 5
        self.node.layout.border_right_width = 6
        self.node.layout.border_bottom_width = 7
        self.node.layout.border_left_width = 8

        self.node.layout.padding_top = 9
        self.node.layout.padding_right = 10
        self.node.layout.padding_bottom = 11
        self.node.layout.padding_left = 12

        self.assertEqual(
            self.node.layout.absolute_content_left + self.node.layout.content_width,
            self.node.layout.absolute_content_right
        )
        self.assertEqual(
            self.node.layout.absolute_content_top + self.node.layout.content_height,
            self.node.layout.absolute_content_bottom
        )

        self.assertEqual(
            self.node.layout.absolute_padding_box_left + self.node.layout.padding_box_width,
            self.node.layout.absolute_padding_box_right
        )
        self.assertEqual(
            self.node.layout.absolute_padding_box_top + self.node.layout.padding_box_height,
            self.node.layout.absolute_padding_box_bottom
        )

        self.assertEqual(
            self.node.layout.absolute_border_box_left + self.node.layout.border_box_width,
            self.node.layout.absolute_border_box_right
        )
        self.assertEqual(
            self.node.layout.absolute_border_box_top + self.node.layout.border_box_height,
            self.node.layout.absolute_border_box_bottom
        )

    def test_collapse_top(self):
        self.node.layout.collapse_top = 5
        self.assertEqual(self.node.layout.collapse_top, 5)

        # Setting the margin sets the collapse as well
        self.node.layout.margin_top = 15
        self.assertEqual(self.node.layout.margin_top, 15)
        self.assertEqual(self.node.layout.collapse_top, 15)

        # The collapse can't be set to a smaller value
        self.node.layout.collapse_top = 10
        self.assertEqual(self.node.layout.collapse_top, 15)

        # The margin can be set to a smaller value,
        # but that doesn't change the collapse
        self.node.layout.margin_top = 10
        self.assertEqual(self.node.layout.margin_top, 10)
        self.assertEqual(self.node.layout.collapse_top, 15)

    def test_collapse_right(self):
        self.node.layout.collapse_right = 5
        self.assertEqual(self.node.layout.collapse_right, 5)

        # Setting the margin sets the collapse as well
        self.node.layout.margin_right = 15
        self.assertEqual(self.node.layout.margin_right, 15)
        self.assertEqual(self.node.layout.collapse_right, 15)

        # The collapse can't be set to a smaller value
        self.node.layout.collapse_right = 10
        self.assertEqual(self.node.layout.collapse_right, 15)

        # The margin can be set to a smaller value,
        # but that doesn't change the collapse
        self.node.layout.margin_right = 10
        self.assertEqual(self.node.layout.margin_right, 10)
        self.assertEqual(self.node.layout.collapse_right, 15)

    def test_collapse_bottom(self):
        self.node.layout.collapse_bottom = 5
        self.assertEqual(self.node.layout.collapse_bottom, 5)

        # Setting the margin sets the collapse as well
        self.node.layout.margin_bottom = 15
        self.assertEqual(self.node.layout.margin_bottom, 15)
        self.assertEqual(self.node.layout.collapse_bottom, 15)

        # The collapse can't be set to a smaller value
        self.node.layout.collapse_bottom = 10
        self.assertEqual(self.node.layout.collapse_bottom, 15)

        # The margin can be set to a smaller value,
        # but that doesn't change the collapse
        self.node.layout.margin_bottom = 10
        self.assertEqual(self.node.layout.margin_bottom, 10)
        self.assertEqual(self.node.layout.collapse_bottom, 15)

    def test_collapse_left(self):
        self.node.layout.collapse_left = 5
        self.assertEqual(self.node.layout.collapse_left, 5)

        # Setting the margin sets the collapse as well
        self.node.layout.margin_left = 15
        self.assertEqual(self.node.layout.margin_left, 15)
        self.assertEqual(self.node.layout.collapse_left, 15)

        # The collapse can't be set to a smaller value
        self.node.layout.collapse_left = 10
        self.assertEqual(self.node.layout.collapse_left, 15)

        # The margin can be set to a smaller value,
        # but that doesn't change the collapse
        self.node.layout.margin_left = 10
        self.assertEqual(self.node.layout.margin_left, 10)
        self.assertEqual(self.node.layout.collapse_left, 15)
