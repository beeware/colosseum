from unittest import TestCase

from colosseum.constants import (
    ABSOLUTE, RELATIVE,
    ROW, COLUMN,
    FLEX_START, FLEX_END,
    AUTO, CENTER, STRETCH,
    WRAP, NOWRAP
)
from colosseum.declaration import CSS

from .utils import TestNode


class CSSNodeTest(TestCase):
    def test_default_styles(self):
        "A node has a known style when constructed"

        node = TestNode()

        self.assertEqual(node.style.width, None)
        self.assertEqual(node.style.height, None)

        self.assertEqual(node.style.min_width, None)
        self.assertEqual(node.style.max_width, None)
        self.assertEqual(node.style.min_height, None)
        self.assertEqual(node.style.max_height, None)

        self.assertEqual(node.style.top, None)
        self.assertEqual(node.style.bottom, None)
        self.assertEqual(node.style.left, None)
        self.assertEqual(node.style.right, None)

        self.assertEqual(node.style.position, RELATIVE)

        self.assertEqual(node.style.flex_direction, COLUMN)
        self.assertEqual(node.style.flex_wrap, NOWRAP)
        self.assertEqual(node.style.flex, None)

        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertEqual(node.style.margin_right, 0)

        self.assertEqual(node.style.padding, (0, 0, 0, 0))
        self.assertEqual(node.style.padding_top, 0)
        self.assertEqual(node.style.padding_bottom, 0)
        self.assertEqual(node.style.padding_left, 0)
        self.assertEqual(node.style.padding_right, 0)

        self.assertEqual(node.style.border_width, (0, 0, 0, 0))
        self.assertEqual(node.style.border_top_width, 0)
        self.assertEqual(node.style.border_bottom_width, 0)
        self.assertEqual(node.style.border_right_width, 0)
        self.assertEqual(node.style.border_left_width, 0)

        self.assertEqual(node.style.justify_content, FLEX_START)
        self.assertEqual(node.style.align_items, STRETCH)
        self.assertEqual(node.style.align_self, AUTO)

    def test_style_in_constructor(self):
        "A node can be constructed with a style"
        node = TestNode(style=CSS(
            width=10, height=11,
            min_width=20, max_width=21, min_height=22, max_height=23,
            top=30, right=31, bottom=32, left=33,
            position=ABSOLUTE,
            flex_direction=ROW, flex_wrap=WRAP, flex=40,
            margin=(50, 51, 52, 53),
            padding=(60, 61, 62, 63),
            border_width=(70, 71, 72, 73),
            justify_content=FLEX_END, align_items=CENTER, align_self=FLEX_START
        ))

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 11)

        self.assertEqual(node.style.min_width, 20)
        self.assertEqual(node.style.max_width, 21)
        self.assertEqual(node.style.min_height, 22)
        self.assertEqual(node.style.max_height, 23)

        self.assertEqual(node.style.top, 30)
        self.assertEqual(node.style.right, 31)
        self.assertEqual(node.style.bottom, 32)
        self.assertEqual(node.style.left, 33)

        self.assertEqual(node.style.position, ABSOLUTE)

        self.assertEqual(node.style.flex_direction, ROW)
        self.assertEqual(node.style.flex_wrap, WRAP)
        self.assertEqual(node.style.flex, 40)

        self.assertEqual(node.style.margin, (50, 51, 52, 53))
        self.assertEqual(node.style.margin_top, 50)
        self.assertEqual(node.style.margin_right, 51)
        self.assertEqual(node.style.margin_bottom, 52)
        self.assertEqual(node.style.margin_left, 53)

        self.assertEqual(node.style.padding, (60, 61, 62, 63))
        self.assertEqual(node.style.padding_top, 60)
        self.assertEqual(node.style.padding_right, 61)
        self.assertEqual(node.style.padding_bottom, 62)
        self.assertEqual(node.style.padding_left, 63)

        self.assertEqual(node.style.border_width, (70, 71, 72, 73))
        self.assertEqual(node.style.border_top_width, 70)
        self.assertEqual(node.style.border_right_width, 71)
        self.assertEqual(node.style.border_bottom_width, 72)
        self.assertEqual(node.style.border_left_width, 73)

        self.assertEqual(node.style.justify_content, FLEX_END)
        self.assertEqual(node.style.align_items, CENTER)
        self.assertEqual(node.style.align_self, FLEX_START)

    def test_unknown_style_in_constructor(self):
        "Unknown style properties in a constructor raise an exception"
        with self.assertRaises(NameError):
            TestNode(style=CSS(doesnt_exist=10))

    def test_set_style(self):
        "Individual style properties can be set"
        node = TestNode(style=CSS(width=10, height=20))

        node.style.width = 30
        node.style.height = 40
        # A property that hasn't been set before
        node.style.top = 50

        self.assertEqual(node.style.width, 30)
        self.assertEqual(node.style.height, 40)
        self.assertEqual(node.style.top, 50)

    def test_delete_style(self):
        "Individual style properties can be removed"
        node = TestNode(style=CSS(width=10, height=20, padding_left=30, margin_right=40))

        del(node.style.width)
        del(node.style.height)
        # A property that hasn't been set before
        del(node.style.top)
        # A property with a default value
        del(node.style.padding_left)
        # A meta-property
        del(node.style.margin)

        self.assertIsNone(node.style.width)
        self.assertIsNone(node.style.height)
        self.assertIsNone(node.style.top)
        self.assertEqual(node.style.padding_left, 0)
        self.assertEqual(node.style.padding, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin, (0, 0, 0, 0))

        # Try to delete them all again.
        del(node.style.width)
        del(node.style.height)
        del(node.style.top)
        del(node.style.padding_left)
        del(node.style.margin)

        self.assertIsNone(node.style.width)
        self.assertIsNone(node.style.height)
        self.assertIsNone(node.style.top)
        self.assertEqual(node.style.padding_left, 0)
        self.assertEqual(node.style.padding, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin, (0, 0, 0, 0))

    def test_bulk_style(self):
        "Style properties can be set in bulk"
        node = TestNode(style=CSS(width=10, height=20))

        node.style.set(width=30, height=40, top=50, margin=60)

        self.assertEqual(node.style.width, 30)
        self.assertEqual(node.style.height, 40)
        self.assertEqual(node.style.top, 50)
        self.assertEqual(node.style.margin, (60, 60, 60, 60))
        self.assertEqual(node.style.margin_left, 60)

    def test_unknown_style_in_bulk(self):
        "Bulk style-set method raises exception on unknown style"
        node = TestNode(style=CSS(width=10, height=20))

        with self.assertRaises(NameError):
            node.style.set(width=30, height=40, top=50, doesnt_exist=60)

    def test_directional_attribute_from_single_number(self):
        "Attributes that have directional underpinning can be set from a single number."

        node = TestNode(style=CSS(margin=10))

        self.assertEqual(node.style.margin, (10, 10, 10, 10))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)

    def test_directional_attribute_len_1_list(self):
        "Attributes that have directional underpinning can be set by a len 1 list."

        node = TestNode(style=CSS(margin=[10]))

        self.assertEqual(node.style.margin, (10, 10, 10, 10))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)

    def test_directional_attribute_len_2_list(self):
        "Attributes that have directional underpinning can be set by a len 2 list."

        node = TestNode(style=CSS(margin=[10, 20]))

        self.assertEqual(node.style.margin, (10, 20, 10, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 20)

    def test_directional_attribute_len_3_list(self):
        "Attributes that have directional underpinning can be set by a len 3 list."

        node = TestNode(style=CSS(margin=[10, 20, 30]))

        self.assertEqual(node.style.margin, (10, 20, 30, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 20)

    def test_directional_attribute_len_4_list(self):
        "Attributes that have directional underpinning can be set by a len 4 list."

        node = TestNode(style=CSS(margin=[10, 20, 30, 40]))

        self.assertEqual(node.style.margin, (10, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)

    def test_directional_attribute_other_lists(self):
        "Attributes that have directional underpinning can be set by other list sizes."

        with self.assertRaises(ValueError):
            TestNode(style=CSS(margin=[]))

        with self.assertRaises(ValueError):
            TestNode(style=CSS(margin=[1, 2, 3, 4, 5]))

    def test_content_validation(self):
        "Some attributes have validated choice values."

        node = TestNode()

        node.style.align_self = 'center'
        self.assertEqual(node.style.align_self, 'center')

        with self.assertRaises(ValueError):
            node.style.align_self = 'invalid value'

        self.assertEqual(node.style.align_self, 'center')

    def test_construct_with_children(self):
        "A node can be constructed with children"

        child1 = TestNode()
        child2 = TestNode()
        child3 = TestNode()

        node = TestNode(children=[child1, child2, child3], style=CSS(margin=10))

        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)

        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0], child1)
        self.assertEqual(node.children[1], child2)
        self.assertEqual(node.children[2], child3)

    def test_hint(self):
        node = TestNode(style=CSS(width=10, margin_left=40))
        # Evaluate the layout
        node.style.apply()
        self.assertFalse(node.layout.dirty)

        # Hint 2 manually set attributes:
        #   - an attribute that doesn't have a default, and
        #   - an attribute that *does* have a default
        node.style.hint(
            width=11,
            margin_left=41
        )

        self.assertEqual(node.style.width, 10)
        self.assertIsNone(node.style.height)
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_left, 40)

        # Layout is not dirty, because hinting these attributes
        # affects nothing.
        self.assertFalse(node.layout.dirty)

        # Hint 2 unset attributes:
        #   - one that doesn't have a default, and
        #   - one that *does* have a default
        node.style.hint(
            height=20,
            margin_top=30,
        )

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.margin_top, 30)
        self.assertEqual(node.style.margin_left, 40)

        # Layout is dirty
        self.assertTrue(node.layout.dirty)

        # Evaluate the layout
        node.style.apply()
        self.assertFalse(node.layout.dirty)

        # Delete the two attributes that were initially set
        node.style.set(
            width=None,
            margin_left=None
        )

        self.assertEqual(node.style.width, 11)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.margin_top, 30)
        self.assertEqual(node.style.margin_left, 41)

        # Layout is dirty
        self.assertTrue(node.layout.dirty)

        # Evaluate the layout
        node.style.apply()
        self.assertFalse(node.layout.dirty)
