from unittest import TestCase

from colosseum import engine as css_engine
from colosseum.constants import AUTO, INLINE, BLOCK, TABLE
from colosseum.declaration import CSS
from colosseum.dimensions import Box
from colosseum.units import px


class TestNode:
    def __init__(self, style):
        self.children = []
        self.layout = Box(self)
        self.style = style.copy(self)


class CssDeclarationTests(TestCase):
    def test_engine(self):
        node = TestNode(CSS())
        self.assertEqual(node.style.engine(), css_engine)

    def test_auto_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is AUTO
        self.assertIs(node.style.width, AUTO)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.width = 10

        self.assertEqual(node.style.width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.width = 10
        self.assertEqual(node.style.width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.width = 20
        self.assertEqual(node.style.width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property again.
        # The underlying attribute won't exist, so this
        # should be a no-op.
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertFalse(node.style.dirty)

    def test_0_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.min_width, 0)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.min_width = 10

        self.assertEqual(node.style.min_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.min_width = 10
        self.assertEqual(node.style.min_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.min_width = 20
        self.assertEqual(node.style.min_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.min_width
        self.assertEqual(node.style.min_width, 0)
        self.assertTrue(node.style.dirty)

    def test_None_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is None
        self.assertIsNone(node.style.max_width)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.max_width = 10

        self.assertEqual(node.style.max_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.max_width = 10
        self.assertEqual(node.style.max_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.max_width = 20
        self.assertEqual(node.style.max_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.max_width
        self.assertIsNone(node.style.max_width)
        self.assertTrue(node.style.dirty)

    def test_property_with_choices(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is INLINE
        self.assertIs(node.style.display, INLINE)
        self.assertIsNone(node.style.dirty)

        # Try to provide a value that isn't on the choices list
        with self.assertRaises(ValueError):
            node.style.display = 10

        # Use a valid value
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.display = TABLE
        self.assertIs(node.style.display, TABLE)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.display
        self.assertIs(node.style.display, INLINE)
        self.assertTrue(node.style.dirty)

    def test_directional_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertIsNone(node.style.dirty)

        # Set a value in one axis
        node.style.margin_top = 10

        self.assertEqual(node.style.margin, (10, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = (10,)

        self.assertEqual(node.style.margin, (10, 10, 10, 10))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = 30

        self.assertEqual(node.style.margin, (30, 30, 30, 30))
        self.assertEqual(node.style.margin_top, 30)
        self.assertEqual(node.style.margin_right, 30)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 2 values
        node.style.margin = (10, 20)

        self.assertEqual(node.style.margin, (10, 20, 10, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 3 values
        node.style.margin = (10, 20, 30)

        self.assertEqual(node.style.margin, (10, 20, 30, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 4 values
        node.style.margin = (10, 20, 30, 40)

        self.assertEqual(node.style.margin, (10, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Set a value directly with an invalid number of values
        with self.assertRaises(ValueError):
            node.style.margin = ()

        with self.assertRaises(ValueError):
            node.style.margin = (10, 20, 30, 40, 50)

        # Clean the layout
        node.layout.dirty = False

        # Clear a value on one axis
        del node.style.margin_top

        self.assertEqual(node.style.margin, (0, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Restore the top margin
        node.style.margin_top = 10

        # Clean the layout
        node.layout.dirty = False

        # Clear a value directly
        del node.style.margin

        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

    def test_set_multiple_properties(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        node.style.set(width=10, height=20)

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 20)
        self.assertIs(node.style.top, AUTO)
        self.assertTrue(node.style.dirty)

        # Clear properties
        node.style.set(width=None, top=30)

        self.assertIs(node.style.width, AUTO)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.top, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Setting a non-property
        with self.assertRaises(NameError):
            node.style.set(not_a_property=10)

        self.assertFalse(node.style.dirty)

    def test_str(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        node.style.set(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK
        )
        print(node.style.height)
        self.assertEqual(
            str(node.style),
            "display: block; height: 20px; "
            "margin-bottom: 50px; margin-left: 60px; "
            "margin-right: 40px; margin-top: 30px; width: 10px"
        )
