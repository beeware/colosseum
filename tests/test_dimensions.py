from unittest import TestCase

from colosseum.dimensions import Size, Box


class TestNode:
    def __init__(self):
        self.children = []
        self.layout = Box(self)
        self.intrinsic = Size(self)


class SizeTests(TestCase):
    def setUp(self):
        self.node = TestNode()

        # Mark the layout as "in calculation"
        self.node.layout.dirty = None

    def test_initial_state(self):
        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has not been touched.
        self.assertIsNone(self.node.layout.dirty)

    def test_set_width(self):
        self.node.intrinsic.width = 10

        self.assertEqual(self.node.intrinsic.width, 10)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the width to the same value
        self.node.intrinsic.width = 10

        self.assertEqual(self.node.intrinsic.width, 10)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the width to something new
        self.node.intrinsic.width = 20

        self.assertEqual(self.node.intrinsic.width, 20)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_height(self):
        self.node.intrinsic.height = 10

        self.assertIsNone(self.node.intrinsic.width)
        self.assertEqual(self.node.intrinsic.height, 10)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the height to the same value
        self.node.intrinsic.height = 10

        self.assertIsNone(self.node.intrinsic.width)
        self.assertEqual(self.node.intrinsic.height, 10)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the height to something new
        self.node.intrinsic.height = 20

        self.assertIsNone(self.node.intrinsic.width)
        self.assertEqual(self.node.intrinsic.height, 20)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_width(self):
        self.node.intrinsic.exact_width = False

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertFalse(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact_width to the same value
        self.node.intrinsic.exact_width = False

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertFalse(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact_width to something new
        self.node.intrinsic.exact_width = True

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_height(self):
        self.node.intrinsic.exact_height = False

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertFalse(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact height to the same value
        self.node.intrinsic.exact_height = False

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertFalse(self.node.intrinsic.exact_height)

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact height to something else
        self.node.intrinsic.exact_height = True

        self.assertIsNone(self.node.intrinsic.width)
        self.assertIsNone(self.node.intrinsic.height)
        self.assertTrue(self.node.intrinsic.exact_width)
        self.assertTrue(self.node.intrinsic.exact_height)

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)


class BoxTests(TestCase):
    def setUp(self):
        self.node = TestNode()

        self.child1 = TestNode()
        self.child2 = TestNode()

        self.grandchild1_1 = TestNode()
        self.grandchild1_2 = TestNode()

        self.node.children = [self.child1, self.child2]
        self.child1.children = [self.grandchild1_1, self.grandchild1_2]

        # Mark the layout as "in calculation"
        self.node.layout.dirty = None

    def test_initial(self):
        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes are in calcuation
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

    def test_set_top(self):
        self.node.layout.top = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 5)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 21)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the top to the same value
        self.node.layout.top = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 5)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 21)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the top to a new value
        self.node.layout.top = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 7)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 7)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 23)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 23)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_set_left(self):
        self.node.layout.left = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 5)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 5)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 15)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 15)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the left to the same value
        self.node.layout.left = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 5)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 5)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 15)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 15)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the left to a new value
        self.node.layout.left = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 7)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 7)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 17)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 17)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_set_height(self):
        self.node.layout.height = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 5)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 5)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 5)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the height to the same value
        self.node.layout.height = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 5)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 5)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 5)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the height to a new value
        self.node.layout.height = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 7)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 7)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 7)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_set_width(self):
        self.node.layout.width = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 5)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 5)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 5)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the width to the same value
        self.node.layout.width = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 5)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 5)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 5)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the width to a new value
        self.node.layout.width = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 7)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 7)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 7)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_set_origin_top(self):
        self.node.layout.origin_top = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 5)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the origin_top to the same value
        self.node.layout.origin_top = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 5)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the origin_top to a new value
        self.node.layout.origin_top = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 7)
        self.assertEqual(self.node.layout.origin_left, 0)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 7)
        self.assertEqual(self.node.layout.absolute_left, 0)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 23)
        self.assertEqual(self.node.layout.absolute_right, 10)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_set_origin_left(self):
        self.node.layout.origin_left = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 5)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 5)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 15)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the origin_left to the same value
        self.node.layout.origin_left = 5

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 5)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 5)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 15)

        # Dirty state has not changed.
        self.assertIsNone(self.node.layout.dirty)
        self.assertIsNone(self.child1.layout.dirty)
        self.assertIsNone(self.child2.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)
        self.assertIsNone(self.grandchild1_1.layout.dirty)

        # Set the origin_left to a new value
        self.node.layout.origin_left = 7

        # Core attributes have been stored
        self.assertEqual(self.node.layout.top, 0)
        self.assertEqual(self.node.layout.left, 0)
        self.assertEqual(self.node.layout.height, 16)
        self.assertEqual(self.node.layout.width, 10)
        self.assertEqual(self.node.layout.origin_top, 0)
        self.assertEqual(self.node.layout.origin_left, 7)

        # Computed attributes have been stored
        self.assertEqual(self.node.layout.absolute_top, 0)
        self.assertEqual(self.node.layout.absolute_left, 7)

        self.assertEqual(self.node.layout.bottom, 16)
        self.assertEqual(self.node.layout.right, 10)
        self.assertEqual(self.node.layout.absolute_bottom, 16)
        self.assertEqual(self.node.layout.absolute_right, 17)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

    def test_descendent_offsets(self):
        self.node.layout.origin_top = 5
        self.node.layout.origin_left = 6

        self.child1.layout.top = 7
        self.child1.layout.left = 8

        self.grandchild1_1.layout.top = 9
        self.grandchild1_1.layout.left = 10

        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 6)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 16)

        self.assertEqual(self.child1.layout.absolute_top, 12)
        self.assertEqual(self.child1.layout.absolute_left, 14)
        self.assertEqual(self.child1.layout.absolute_bottom, 28)
        self.assertEqual(self.child1.layout.absolute_right, 24)

        self.assertEqual(self.grandchild1_1.layout.absolute_top, 21)
        self.assertEqual(self.grandchild1_1.layout.absolute_left, 24)
        self.assertEqual(self.grandchild1_1.layout.absolute_bottom, 37)
        self.assertEqual(self.grandchild1_1.layout.absolute_right, 34)

        # All the nodes have been marked dirty
        self.assertTrue(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertTrue(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Modify the grandchild position
        self.grandchild1_1.layout.top = 11
        self.grandchild1_1.layout.left = 12

        # Only the grandchild position has changed.
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 6)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 16)

        self.assertEqual(self.child1.layout.absolute_top, 12)
        self.assertEqual(self.child1.layout.absolute_left, 14)
        self.assertEqual(self.child1.layout.absolute_bottom, 28)
        self.assertEqual(self.child1.layout.absolute_right, 24)

        self.assertEqual(self.grandchild1_1.layout.absolute_top, 23)
        self.assertEqual(self.grandchild1_1.layout.absolute_left, 26)
        self.assertEqual(self.grandchild1_1.layout.absolute_bottom, 39)
        self.assertEqual(self.grandchild1_1.layout.absolute_right, 36)

        # Only the grandchild node is dirty
        self.assertFalse(self.node.layout.dirty)
        self.assertFalse(self.child1.layout.dirty)
        self.assertFalse(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertFalse(self.grandchild1_2.layout.dirty)

        # Modify the child position
        self.child1.layout.top = 13
        self.child1.layout.left = 14

        # Only the child and grandchild position has changed.
        self.assertEqual(self.node.layout.absolute_top, 5)
        self.assertEqual(self.node.layout.absolute_left, 6)
        self.assertEqual(self.node.layout.absolute_bottom, 21)
        self.assertEqual(self.node.layout.absolute_right, 16)

        self.assertEqual(self.child1.layout.absolute_top, 18)
        self.assertEqual(self.child1.layout.absolute_left, 20)
        self.assertEqual(self.child1.layout.absolute_bottom, 34)
        self.assertEqual(self.child1.layout.absolute_right, 30)

        self.assertEqual(self.grandchild1_1.layout.absolute_top, 29)
        self.assertEqual(self.grandchild1_1.layout.absolute_left, 32)
        self.assertEqual(self.grandchild1_1.layout.absolute_bottom, 45)
        self.assertEqual(self.grandchild1_1.layout.absolute_right, 42)

        # Only the affected child node, and grandchild nodes are dirty
        self.assertFalse(self.node.layout.dirty)
        self.assertTrue(self.child1.layout.dirty)
        self.assertFalse(self.child2.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
        self.assertTrue(self.grandchild1_1.layout.dirty)
