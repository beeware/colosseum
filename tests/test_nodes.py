try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from colosseum.nodes import CSSNode, UnknownCSSStyleException, InvalidCSSStyleException
from colosseum.constants import *


class CSSNodeTest(TestCase):
    def test_default_styles(self):
        "A CSSNode has a known style when constructed"

        node = CSSNode()

        self.assertEqual(node.width, None)
        self.assertEqual(node.height, None)

        self.assertEqual(node.min_width, None)
        self.assertEqual(node.max_width, None)
        self.assertEqual(node.min_height, None)
        self.assertEqual(node.max_height, None)

        self.assertEqual(node.top, None)
        self.assertEqual(node.bottom, None)
        self.assertEqual(node.left, None)
        self.assertEqual(node.right, None)

        self.assertEqual(node.position, RELATIVE)

        self.assertEqual(node.flex_direction, COLUMN)
        self.assertEqual(node.flex_wrap, NOWRAP)
        self.assertEqual(node.flex, None)

        self.assertEqual(node.margin, (0, 0, 0, 0))
        self.assertEqual(node.margin_top, 0)
        self.assertEqual(node.margin_bottom, 0)
        self.assertEqual(node.margin_left, 0)
        self.assertEqual(node.margin_right, 0)

        self.assertEqual(node.padding, (0, 0, 0, 0))
        self.assertEqual(node.padding_top, 0)
        self.assertEqual(node.padding_bottom, 0)
        self.assertEqual(node.padding_left, 0)
        self.assertEqual(node.padding_right, 0)

        self.assertEqual(node.border_width, (0, 0, 0, 0))
        self.assertEqual(node.border_top_width, 0)
        self.assertEqual(node.border_bottom_width, 0)
        self.assertEqual(node.border_right_width, 0)
        self.assertEqual(node.border_left_width, 0)

        self.assertEqual(node.justify_content, FLEX_START)
        self.assertEqual(node.align_items, STRETCH)
        self.assertEqual(node.align_self, AUTO)

    def test_style_in_constructor(self):
        "A CSSNode can be constructed with a style"
        node = CSSNode(
            width=10, height=11,
            min_width=20, max_width=21, min_height=22, max_height=23,
            top=30, right=31, bottom=32, left=33,
            position=ABSOLUTE,
            flex_direction=ROW, flex_wrap=WRAP, flex=40,
            margin=(50, 51, 52, 53),
            padding=(60, 61, 62, 63),
            border_width=(70, 71, 72, 73),
            justify_content=FLEX_END, align_items=CENTER, align_self=FLEX_START
        )

        self.assertEqual(node.width, 10)
        self.assertEqual(node.height, 11)

        self.assertEqual(node.min_width, 20)
        self.assertEqual(node.max_width, 21)
        self.assertEqual(node.min_height, 22)
        self.assertEqual(node.max_height, 23)

        self.assertEqual(node.top, 30)
        self.assertEqual(node.right, 31)
        self.assertEqual(node.bottom, 32)
        self.assertEqual(node.left, 33)

        self.assertEqual(node.position, ABSOLUTE)

        self.assertEqual(node.flex_direction, ROW)
        self.assertEqual(node.flex_wrap, WRAP)
        self.assertEqual(node.flex, 40)

        self.assertEqual(node.margin, (50, 51, 52, 53))
        self.assertEqual(node.margin_top, 50)
        self.assertEqual(node.margin_right, 51)
        self.assertEqual(node.margin_bottom, 52)
        self.assertEqual(node.margin_left, 53)

        self.assertEqual(node.padding, (60, 61, 62, 63))
        self.assertEqual(node.padding_top, 60)
        self.assertEqual(node.padding_right, 61)
        self.assertEqual(node.padding_bottom, 62)
        self.assertEqual(node.padding_left, 63)

        self.assertEqual(node.border_width, (70, 71, 72, 73))
        self.assertEqual(node.border_top_width, 70)
        self.assertEqual(node.border_right_width, 71)
        self.assertEqual(node.border_bottom_width, 72)
        self.assertEqual(node.border_left_width, 73)

        self.assertEqual(node.justify_content, FLEX_END)
        self.assertEqual(node.align_items, CENTER)
        self.assertEqual(node.align_self, FLEX_START)

    def test_unknown_style_in_constructor(self):
        "Unknown style properties in a constructor raise an exception"
        with self.assertRaises(UnknownCSSStyleException):
            CSSNode(doesnt_exist=10)

    def test_set_style(self):
        "Individual style properties can be set"
        node = CSSNode(width=10, height=20)

        node.width = 30
        node.height = 40
        # A property that hasn't been set before
        node.top = 50

        self.assertEqual(node.width, 30)
        self.assertEqual(node.height, 40)
        self.assertEqual(node.top, 50)

    def test_delete_style(self):
        "Individual style properties can be removed"
        node = CSSNode(width=10, height=20, padding_left=30, margin_right=40)

        del(node.width)
        del(node.height)
        # A property that hasn't been set before
        del(node.top)
        # A property with a default value
        del(node.padding_left)
        # A meta-property
        del(node.margin)

        self.assertIsNone(node.width)
        self.assertIsNone(node.height)
        self.assertIsNone(node.top)
        self.assertEqual(node.padding_left, 0)
        self.assertEqual(node.padding, (0, 0, 0, 0))
        self.assertEqual(node.margin_right, 0)
        self.assertEqual(node.margin, (0, 0, 0, 0))

        # Try to delete them all again.
        del(node.width)
        del(node.height)
        del(node.top)
        del(node.padding_left)
        del(node.margin)

        self.assertIsNone(node.width)
        self.assertIsNone(node.height)
        self.assertIsNone(node.top)
        self.assertEqual(node.padding_left, 0)
        self.assertEqual(node.padding, (0, 0, 0, 0))
        self.assertEqual(node.margin_right, 0)
        self.assertEqual(node.margin, (0, 0, 0, 0))

    def test_bulk_style(self):
        "Style properties can be set in bulk"
        node = CSSNode(width=10, height=20)

        node.style(width=30, height=40, top=50, margin=60)

        self.assertEqual(node.width, 30)
        self.assertEqual(node.height, 40)
        self.assertEqual(node.top, 50)
        self.assertEqual(node.margin, (60, 60, 60, 60))
        self.assertEqual(node.margin_left, 60)

    def test_unknown_style_in_bulk(self):
        "Bulk style-set method raises exception on unknown style"
        node = CSSNode(width=10, height=20)

        with self.assertRaises(UnknownCSSStyleException):
            node.style(width=30, height=40, top=50, doesnt_exist=60)

    def test_directional_attribute_from_single_number(self):
        "Attributes that have directional underpinning can be set from a single number."

        node = CSSNode(margin=10)

        self.assertEqual(node.margin, (10, 10, 10, 10))
        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 10)
        self.assertEqual(node.margin_bottom, 10)
        self.assertEqual(node.margin_left, 10)

    def test_directional_attribute_len_1_list(self):
        "Attributes that have directional underpinning can be set by a len 1 list."

        node = CSSNode(margin=[10])

        self.assertEqual(node.margin, (10, 10, 10, 10))
        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 10)
        self.assertEqual(node.margin_bottom, 10)
        self.assertEqual(node.margin_left, 10)

    def test_directional_attribute_len_2_list(self):
        "Attributes that have directional underpinning can be set by a len 2 list."

        node = CSSNode(margin=[10, 20])

        self.assertEqual(node.margin, (10, 20, 10, 20))
        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 20)
        self.assertEqual(node.margin_bottom, 10)
        self.assertEqual(node.margin_left, 20)

    def test_directional_attribute_len_3_list(self):
        "Attributes that have directional underpinning can be set by a len 3 list."

        node = CSSNode(margin=[10, 20, 30])

        self.assertEqual(node.margin, (10, 20, 30, 20))
        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 20)
        self.assertEqual(node.margin_bottom, 30)
        self.assertEqual(node.margin_left, 20)

    def test_directional_attribute_len_4_list(self):
        "Attributes that have directional underpinning can be set by a len 4 list."

        node = CSSNode(margin=[10, 20, 30, 40])

        self.assertEqual(node.margin, (10, 20, 30, 40))
        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 20)
        self.assertEqual(node.margin_bottom, 30)
        self.assertEqual(node.margin_left, 40)

    def test_directional_attribute_other_lists(self):
        "Attributes that have directional underpinning can be set by other list sizes."

        with self.assertRaises(InvalidCSSStyleException):
            CSSNode(margin=[])

        with self.assertRaises(InvalidCSSStyleException):
            CSSNode(margin=[1, 2, 3, 4, 5])

    def test_content_validation(self):
        "Some attributes have validated choice values."

        node = CSSNode()

        node.align_self = 'center'
        self.assertEqual(node.align_self, 'center')

        with self.assertRaises(InvalidCSSStyleException):
            node.align_self = 'invalid value'

        self.assertEqual(node.align_self, 'center')

    def test_construct_with_children(self):
        "A node can be constructed with children"

        child1 = CSSNode()
        child2 = CSSNode()
        child3 = CSSNode()

        node = CSSNode(child1, child2, child3, margin=10)

        self.assertEqual(node.margin_top, 10)
        self.assertEqual(node.margin_right, 10)
        self.assertEqual(node.margin_bottom, 10)
        self.assertEqual(node.margin_left, 10)

        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0], child1)
        self.assertEqual(node.children[1], child2)
        self.assertEqual(node.children[2], child3)
