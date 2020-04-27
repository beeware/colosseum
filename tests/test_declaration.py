from unittest import TestCase

from colosseum import engine as css_engine
from colosseum.colors import GOLDENROD, NAMED_COLOR, REBECCAPURPLE
from colosseum.constants import (AUTO, BLOCK, INHERIT, INITIAL,
                                 INITIAL_FONT_VALUES, INLINE, LEFT, REVERT,
                                 RIGHT, RTL, TABLE, UNSET, Choices,
                                 OtherProperty)
from colosseum.declaration import CSS, validated_property
from colosseum.units import percent, px
from colosseum.validators import (is_color, is_integer, is_length, is_number,
                                  is_percentage)
from colosseum.wrappers import BorderSpacing, FontFamily, FontShorthand, Quotes

from .utils import ColosseumTestCase, TestNode


class PropertyChoiceTests(TestCase):
    def test_none(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(None), initial=None)

        obj = MyObject()
        self.assertIsNone(obj.prop)

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: none"
            )

    def test_allow_length(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_length]), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0 * px)

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <length>"
            )

    def test_allow_percentage(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_percentage]), initial=99 * percent)

        obj = MyObject()
        self.assertEqual(obj.prop, 99 * percent)

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <percentage>"
            )

    def test_allow_integer(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_integer]), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0)

        obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <integer>"
            )

    def test_allow_color(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_color]), initial='goldenrod')

        obj = MyObject()
        self.assertEqual(obj.prop, NAMED_COLOR[GOLDENROD])

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        obj.prop = REBECCAPURPLE
        obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <color>"
            )

    def test_values(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices('a', 'b', None), initial='a')

        obj = MyObject()
        self.assertEqual(obj.prop, 'a')

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        obj.prop = 'a'
        obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: a, b, none"
            )

    def test_all_choices(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(
                'a', 'b', None,
                validators=[is_integer, is_number, is_length, is_percentage, is_color],
                explicit_defaulting_constants=[INITIAL, INHERIT, UNSET, REVERT]
            ), initial=None)

        obj = MyObject()

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        obj.prop = REBECCAPURPLE
        obj.prop = '#112233'
        obj.prop = 'a'
        obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'
        obj.prop = INITIAL
        obj.prop = INHERIT
        obj.prop = UNSET
        obj.prop = REVERT

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; "
                "Valid values are: <color>, <integer>, <length>, <number>, <percentage>, "
                "a, b, inherit, initial, none, revert, unset"
            )

    def test_string_symbol(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=None)

        obj = MyObject()

        # Set a symbolic value using the string value of the symbol
        # We can't just use the string directly, though - that would
        # get optimized by the compiler. So we create a string and
        # transform it into the value we want.
        val = 'AUTO'
        obj.prop = val.lower()

        # Both equality and instance checking should work.
        self.assertEqual(obj.prop, AUTO)
        self.assertIs(obj.prop, AUTO)


class CssDeclarationTests(ColosseumTestCase):
    def test_engine(self):
        node = TestNode(style=CSS())
        self.assertEqual(node.style.engine(), css_engine)

    def test_auto_default_property(self):
        node = TestNode(style=CSS())
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
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.border_top_width, 0)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.border_top_width = 10

        self.assertEqual(node.style.border_top_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.border_top_width = 10
        self.assertEqual(node.style.border_top_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.border_top_width = 20
        self.assertEqual(node.style.border_top_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.border_top_width
        self.assertEqual(node.style.border_top_width, 0)
        self.assertTrue(node.style.dirty)

    def test_None_default_property(self):
        node = TestNode(style=CSS())
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
        node = TestNode(style=CSS())
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

    def test_list_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Check initial value
        self.assertEqual(node.style.font_family, FontFamily(['initial']))

        # Check valid values
        node.style.font_family = ['serif']
        node.style.font_family = ["Ahem", 'serif']

        # This will coerce to a list, is this a valid behavior?
        node.style.font_family = 'Ahem'
        self.assertEqual(node.style.font_family, FontFamily(['Ahem']))
        node.style.font_family = '     Ahem       ,   serif '
        self.assertEqual(node.style.font_family, FontFamily(['Ahem', 'serif']))

        # Check valid value without extra quotes
        node.style.font_family = ['White Space']

        # Check extra quotes are removed
        node.style.font_family = ['"White Space"']
        self.assertEqual(node.style.font_family, FontFamily(['White Space']))

        # Check it raises
        try:
            node.style.font_family = ['123']
            self.fail('Should raise ValueError')
        except ValueError:
            pass

    def test_property_border_spacing_valid_str_1_item_inherit(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Text value
        node.style.border_spacing = 'inherit'
        self.assertEqual(node.style.border_spacing, 'inherit')
        self.assertEqual(node.style.border_spacing, 'inherit')
        self.assertNotIsInstance(node.style.border_spacing, BorderSpacing)

    def test_property_border_spacing_valid_str_1_item(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_spacing = '1'
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 1 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px)')
        self.assertEqual(str(node.style.border_spacing), '1px')

        node.style.border_spacing = '1px'
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 1 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px)')
        self.assertEqual(str(node.style.border_spacing), '1px')

    def test_property_border_spacing_valid_str_1_item_spaces(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_spacing = '  1  '
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 1 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px)')
        self.assertEqual(str(node.style.border_spacing), '1px')

        node.style.border_spacing = '  1px  '
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 1 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px)')
        self.assertEqual(str(node.style.border_spacing), '1px')

    def test_property_border_spacing_valid_str_2_items_numbers(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_spacing = '1 2'
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

        node.style.border_spacing = '1.0 2.0'
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

    def test_property_border_spacing_valid_str_2_items_px(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_spacing = '1px 2px'
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

    def test_property_border_spacing_valid_str_2_items_numbers_spaces(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_spacing = '  1  2  '
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

        node.style.border_spacing = '  1.0  2.0  '
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

    def test_property_border_spacing_valid_sequence_2_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # List of strings
        node.style.border_spacing = ['1', '2']
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

        # List
        node.style.border_spacing = [1, 2]
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

        # Tuple
        node.style.border_spacing = (1, 2)
        self.assertEqual(node.style.border_spacing.horizontal, 1 * px)
        self.assertEqual(node.style.border_spacing.vertical, 2 * px)
        self.assertEqual(repr(node.style.border_spacing), 'BorderSpacing(1px, 2px)')
        self.assertEqual(str(node.style.border_spacing), '1px 2px')

    def test_property_border_spacing_invalid_empty_item(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = ''

        with self.assertRaises(ValueError):
            node.style.border_spacing = ()

        with self.assertRaises(ValueError):
            node.style.border_spacing = []

    def test_property_border_spacing_invalid_value_1_item(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = 'foobar'

        with self.assertRaises(ValueError):
            node.style.border_spacing = ['foobar']

        with self.assertRaises(ValueError):
            node.style.border_spacing = ('foobar', )

    def test_property_border_spacing_invalid_value_2_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = 'foobar spam'

        with self.assertRaises(ValueError):
            node.style.border_spacing = ['foobar', 'spam']

        with self.assertRaises(ValueError):
            node.style.border_spacing = ('foobar', 'spam')

    def test_property_border_spacing_invalid_amount_of_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = '1 2 3'

        with self.assertRaises(ValueError):
            node.style.border_spacing = 1, 2, 3,

        with self.assertRaises(ValueError):
            node.style.border_spacing = [1, 2, 3]

    def test_property_border_spacing_invalid_separator_str_1_item(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = '1,'

        with self.assertRaises(ValueError):
            node.style.border_spacing = '1;'

    def test_property_border_spacing_invalid_separator_str_2_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.border_spacing = '1, 2'

        with self.assertRaises(ValueError):
            node.style.border_spacing = '1; 2'

    def test_directional_property(self):
        node = TestNode(style=CSS())
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
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(width=10, height=20)

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 20)
        self.assertIs(node.style.top, AUTO)
        self.assertTrue(node.style.dirty)

        # Clear properties
        node.style.update(width=None, top=30)

        self.assertIs(node.style.width, AUTO)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.top, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Setting a non-property
        with self.assertRaises(NameError):
            node.style.update(not_a_property=10)

        self.assertFalse(node.style.dirty)

    def test_other_property_valid(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=OtherProperty('other_prop'))
            other_prop = validated_property('other_prop', choices=Choices(0, AUTO), initial=AUTO)

        obj = MyObject()
        self.assertEqual(obj.prop, AUTO)
        self.assertEqual(obj.prop, obj.other_prop)

        obj.other_prop = 0
        self.assertEqual(obj.prop, 0)
        self.assertEqual(obj.prop, obj.other_prop)

        obj.prop = None
        self.assertEqual(obj.prop, None)
        self.assertNotEqual(obj.prop, obj.other_prop)

    def test_other_property_invalid_no_name_argument(self):
        with self.assertRaises(TypeError):
            OtherProperty()

    def test_other_property_invalid_incorrect_property_name(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=OtherProperty('foobar'))

        obj = MyObject()
        with self.assertRaises(ValueError):
            obj.prop

    def test_other_property_callable_valid(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Check initial value LTR
        self.assertEqual(node.style.text_align, LEFT)

        # Change direction to RTL
        node.style.update(direction=RTL)
        self.assertEqual(node.style.text_align, RIGHT)

    def test_other_property_invalid_no_value_attr(self):
        class SomeProperty:
            boo = None

        with self.assertRaises(ValueError):
            class MyObject:
                prop = validated_property('prop', choices=Choices(AUTO, None), initial=SomeProperty())

    def test_other_property_callable_invalid_value_not_a_method(self):
        class SomeProperty:
            value = None

        with self.assertRaises(ValueError):
            class MyObject:
                prop = validated_property('prop', choices=Choices(AUTO, None), initial=SomeProperty())

    ##############################################################################
    # Quotes
    ##############################################################################
    def test_quotes_valid_str_2_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = "'<' '>'"
        self.assertEqual(node.style.quotes, Quotes([('<', '>')]))

    def test_quotes_valid_str_4_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = "'<' '>' '{' '}'"
        self.assertEqual(node.style.quotes, Quotes([('<', '>'), ('{', '}')]))

    def test_quotes_valid_sequence_2_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = '<', '>'
        self.assertEqual(node.style.quotes, Quotes([('<', '>')]))

    def test_quotes_valid_sequence_4_items(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = '<', '>', '{', '}'
        self.assertEqual(node.style.quotes, Quotes([('<', '>'), ('{', '}')]))

    def test_quotes_valid_list_1_pair(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = [('<', '>')]
        self.assertEqual(node.style.quotes, Quotes([('<', '>')]))

    def test_quotes_valid_list_2_pairs(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = [('<', '>'), ('{', '}')]
        self.assertEqual(node.style.quotes, Quotes([('<', '>'), ('{', '}')]))

    def test_quotes_valid_str(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.quotes = [('<', '>'), ('{', '}')]
        self.assertEqual(str(node.style), "quotes: '<' '>' '{' '}'")

    def test_quotes_invalid_empty(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None
        with self.assertRaises(ValueError):
            node.style.quotes = ''

        with self.assertRaises(ValueError):
            node.style.quotes = []

        with self.assertRaises(ValueError):
            node.style.quotes = [()]

    def test_quotes_invalid_1_item(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.quotes = '">"'

        with self.assertRaises(ValueError):
            node.style.quotes = '>'

        with self.assertRaises(ValueError):
            node.style.quotes = '>',

        with self.assertRaises(ValueError):
            node.style.quotes = ['>']

        with self.assertRaises(ValueError):
            node.style.quotes = [('>')]

    ##############################################################################
    # Outline shorthand
    ##############################################################################
    def test_shorthand_valid_outline_property_initial_values(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        self.assertEqual(str(node.style.outline), '')

    def test_shorthand_valid_outline_subproperties_set_shorthand_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.outline_color = "black"
        node.style.outline_style = "solid"
        node.style.outline_width = "thick"

        self.assertEqual(str(node.style.outline), 'rgba(0, 0, 0, 1.0) solid thick')
        self.assertEqual(str(node.style),
                         "outline-color: rgba(0, 0, 0, 1.0); outline-style: solid; outline-width: thick")

    def test_shorthand_valid_outline_property_str_sets_shorthand_subproperties(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.outline = "black solid thick"

        self.assertEqual(str(node.style.outline_color), 'rgba(0, 0, 0, 1.0)')
        self.assertEqual(str(node.style.outline_style), 'solid')
        self.assertEqual(str(node.style.outline_width), 'thick')

    def test_shorthand_valid_outline_property_list_sets_shorthand_subproperties(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.outline = "black", "solid", "thick"

        self.assertEqual(str(node.style.outline_color), 'rgba(0, 0, 0, 1.0)')
        self.assertEqual(str(node.style.outline_style), 'solid')
        self.assertEqual(str(node.style.outline_width), 'thick')

    def test_shorthand_valid_outline_property_resets(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.outline_color = "black"
        node.style.outline_style = "solid"
        node.style.outline_width = "thick"

        self.assertEqual(str(node.style.outline), 'rgba(0, 0, 0, 1.0) solid thick')
        self.assertEqual(str(node.style),
                         "outline-color: rgba(0, 0, 0, 1.0); outline-style: solid; outline-width: thick")

        # This should reset all other properties to their initial values
        node.style.outline = "black"

        self.assertEqual(str(node.style.outline_color), "rgba(0, 0, 0, 1.0)")
        self.assertEqual(node.style.outline_style, None)
        self.assertEqual(node.style.outline_width, "medium")

        self.assertEqual(str(node.style.outline), 'rgba(0, 0, 0, 1.0)')
        self.assertEqual(str(node.style), "outline-color: rgba(0, 0, 0, 1.0)")

    def test_shorthand_valid_outline_property_delete(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # This should reset all other properties to their initial values
        node.style.outline = "black"

        self.assertEqual(str(node.style.outline_color), "rgba(0, 0, 0, 1.0)")
        self.assertEqual(node.style.outline_style, None)
        self.assertEqual(node.style.outline_width, "medium")

        # This should reset all properties to their initial values
        del node.style.outline
        self.assertEqual(node.style.outline, '')
        self.assertEqual(str(node.style.outline_color), 'invert')
        self.assertEqual(node.style.outline_style, None)
        self.assertEqual(node.style.outline_width, "medium")

    def test_shorthand_invalid_outline_property_values(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        with self.assertRaises(ValueError):
            node.style.outline = "foo bar spam"

        with self.assertRaises(ValueError):
            node.style.outline = "foo", "bar", "spam"

    ##############################################################################
    # Border shorthands
    ##############################################################################
    def test_border_shorthands_valid_initial_values(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        for property_name in ['border', 'border_bottom', 'border_left', 'border_right', 'border_top']:
            self.assertEqual(str(getattr(node.style, property_name)), '')

    def test_border_shorthands_valid_set_subproperties_get_shorthand_property(self):
        for direction in ['bottom', 'left', 'right', 'top']:
            node = TestNode(style=CSS())
            node.layout.dirty = None

            setattr(node.style, 'border_{direction}_width'.format(direction=direction), 'thick')
            setattr(node.style, 'border_{direction}_style'.format(direction=direction), 'solid')
            setattr(node.style, 'border_{direction}_color'.format(direction=direction), 'black')

            shorthand = 'border_{direction}'.format(direction=direction)
            self.assertEqual(str(getattr(node.style, shorthand)), 'thick solid rgba(0, 0, 0, 1.0)')
            self.assertEqual(str(node.style),
                             "border-{direction}-color: rgba(0, 0, 0, 1.0); "
                             "border-{direction}-style: solid; "
                             "border-{direction}-width: thick"
                             "".format(direction=direction))

    def test_border_shorthands_valid_property_str_sets_shorthand_subproperties(self):
        for direction in ['bottom', 'left', 'right', 'top']:
            node = TestNode(style=CSS())
            node.layout.dirty = None

            setattr(node.style, 'border_' + direction, 'solid thick black')

            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_color'.format(direction=direction))),
                'rgba(0, 0, 0, 1.0)'
            )
            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_style'.format(direction=direction))),
                'solid'
            )
            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_width'.format(direction=direction))),
                'thick'
            )

    def test_border_shorthands_valid_property_tuple_sets_shorthand_subproperties(self):
        for direction in ['bottom', 'left', 'right', 'top']:
            node = TestNode(style=CSS())
            node.layout.dirty = None

            setattr(node.style, 'border_' + direction, ('solid', 'thick', 'black'))

            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_color'.format(direction=direction))),
                'rgba(0, 0, 0, 1.0)'
            )
            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_style'.format(direction=direction))),
                'solid'
            )
            self.assertEqual(
                str(getattr(node.style, 'border_{direction}_width'.format(direction=direction))),
                'thick'
            )

    def test_border_shorthand_valid(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border = ('solid', 'thick', 'black')

        self.assertEqual(
            str(node.style),
            ('border-bottom-color: rgba(0, 0, 0, 1.0); '
             'border-bottom-style: solid; '
             'border-bottom-width: thick; '
             'border-left-color: rgba(0, 0, 0, 1.0); '
             'border-left-style: solid; '
             'border-left-width: thick; '
             'border-right-color: rgba(0, 0, 0, 1.0); '
             'border-right-style: solid; '
             'border-right-width: thick; '
             'border-top-color: rgba(0, 0, 0, 1.0); '
             'border-top-style: solid; '
             'border-top-width: thick')
        )

    def test_shorthand_valid_border_property_resets(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border_color = "black"
        node.style.border_style = "solid"
        node.style.border_width = "thick"

        self.assertEqual(str(node.style.border_color), '(rgba(0, 0, 0, 1.0), '
                                                       'rgba(0, 0, 0, 1.0), '
                                                       'rgba(0, 0, 0, 1.0), '
                                                       'rgba(0, 0, 0, 1.0))')
        self.assertEqual(node.style.border_style, ('solid', 'solid', 'solid', 'solid'))
        self.assertEqual(node.style.border_width, ('thick', 'thick', 'thick', 'thick'))

        # This should reset all other properties to their initial values
        node.style.border = "red"
        self.assertEqual(str(node.style.border_color), '(rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0))')
        self.assertEqual(node.style.border_style, (None, None, None, None))
        self.assertEqual(str(node.style.border_width), '(0px, 0px, 0px, 0px)')

    def test_shorthand_valid_border_property_delete(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.border = "red"
        self.assertEqual(str(node.style.border_color), '(rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0), '
                                                       'rgba(255, 0, 0, 1.0))')
        self.assertEqual(node.style.border_style, (None, None, None, None))
        self.assertEqual(str(node.style.border_width), '(0px, 0px, 0px, 0px)')

        # This should reset all properties to their initial values
        del node.style.border
        self.assertEqual(str(node.style), '')

    def test_border_shorthands_invalid_values(self):
        for direction in ['', '_bottom', '_left', '_right', '_top']:
            node = TestNode(style=CSS())
            node.layout.dirty = None

            with self.assertRaises(ValueError):
                setattr(node.style, 'border' + direction, 'foo bar spam')

            with self.assertRaises(ValueError):
                setattr(node.style, 'border' + direction, ("foo", "bar", "spam"))

    def test_str(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK,
        )

        self.assertEqual(
            str(node.style),
            "display: block; "
            "height: 20px; "
            "margin-bottom: 50px; "
            "margin-left: 60px; "
            "margin-right: 40px; "
            "margin-top: 30px; "
            "width: 10px"
        )

    def test_dict(self):
        "Style declarations expose a dict-like interface"
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK
        )

        self.assertEqual(
            node.style.keys(),
            {'display', 'height', 'margin_bottom', 'margin_left', 'margin_right', 'margin_top', 'width'}
        )
        self.assertEqual(
            sorted(node.style.items()),
            sorted([
                ('display', BLOCK),
                ('height', 20),
                ('margin_bottom', 50),
                ('margin_left', 60),
                ('margin_right', 40),
                ('margin_top', 30),
                ('width', 10),
            ])
        )

        # A property can be set, retrieved and cleared using the CSS attribute name
        node.style['margin-bottom'] = 10
        self.assertEqual(node.style['margin-bottom'], 10)
        del node.style['margin-bottom']
        self.assertEqual(node.style['margin-bottom'], 0)

        # A property can be set, retrieved and cleared using the Python attribute name
        node.style['margin_bottom'] = 10
        self.assertEqual(node.style['margin_bottom'], 10)
        del node.style['margin_bottom']
        self.assertEqual(node.style['margin_bottom'], 0)

        # Clearing a valid property isn't an error
        del node.style['margin_bottom']
        self.assertEqual(node.style['margin_bottom'], 0)

        # Non-existent properties raise KeyError
        with self.assertRaises(KeyError):
            node.style['no-such-property'] = 'no-such-value'

        with self.assertRaises(KeyError):
            node.style['no-such-property']

        with self.assertRaises(KeyError):
            del node.style['no-such-property']

    def test_font_shorthand_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Check initial value
        self.assertTrue(isinstance(node.style.font, FontShorthand))
        self.assertEqual(node.style.font.to_dict(), INITIAL_FONT_VALUES)

        # Check Initial values
        self.assertEqual(node.style.font_style, 'normal')
        self.assertEqual(node.style.font_weight, 'normal')
        self.assertEqual(node.style.font_variant, 'normal')
        self.assertEqual(node.style.font_size, 'medium')
        self.assertEqual(node.style.line_height, 'normal')
        self.assertEqual(node.style.font_family, FontFamily(['initial']))

        # Check individual properties update the unset shorthand
        node.style.font_style = 'italic'
        node.style.font_weight = 'bold'
        node.style.font_variant = 'small-caps'
        node.style.font_size = '10px'
        node.style.line_height = '1.5'
        node.style.font_family = ['Ahem', 'serif']
        expected_font = {
            'font_style': 'italic',
            'font_weight': 'bold',
            'font_variant': 'small-caps',
            'font_size': '10px',
            'line_height': '1.5',
            'font_family': FontFamily(['Ahem', 'serif']),
        }
        font = node.style.font.to_dict()
        font['font_size'] = str(font['font_size'])
        font['line_height'] = str(font['line_height'])
        self.assertEqual(font, expected_font)

        # Check setting the shorthand resets values
        node.style.font = '9px serif'
        self.assertEqual(node.style.font_style, 'normal')
        self.assertEqual(node.style.font_weight, 'normal')
        self.assertEqual(node.style.font_variant, 'normal')
        self.assertEqual(node.style.line_height, 'normal')
        self.assertEqual(str(node.style.font_size), '9px')
        self.assertEqual(node.style.font_family, FontFamily(['serif']))

        # Check individual properties do not update the set shorthand
        node.style.font = '9px "White Space", serif'
        node.style.font_style = 'italic'
        node.style.font_weight = 'bold'
        node.style.font_variant = 'small-caps'
        node.style.font_size = '10px'
        node.style.line_height = '1.5'
        expected_font = {
            'font_style': 'italic',
            'font_weight': 'bold',
            'font_variant': 'small-caps',
            'font_size': '10px',
            'line_height': '1.5',
            'font_family': FontFamily(['White Space', 'serif']),
        }
        font = node.style.font.to_dict()
        font['font_size'] = str(font['font_size'])
        font['line_height'] = str(font['line_height'])
        self.assertEqual(font, expected_font)

        # Check string
        self.assertEqual(str(node.style), (
            'font: italic small-caps bold 10px/1.5 "White Space", serif; '
            'font-family: "White Space", serif; '
            'font-size: 10px; '
            'font-style: italic; '
            'font-variant: small-caps; '
            'font-weight: bold; '
            'line-height: 1.5'
        ))
        node.style.font = '9px "White Space", serif'
        self.assertEqual(str(node.style), (
            'font: normal normal normal 9px/normal "White Space", serif; '
            'font-family: "White Space", serif; '
            'font-size: 9px; '
            'font-style: normal; '
            'font-variant: normal; '
            'font-weight: normal; '
            'line-height: normal'
        ))

        # Check invalid values
        with self.assertRaises(ValueError):
            node.style.font = 'ThisIsDefinitelyNotAFontName'

    def test_font_family_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Check type
        self.assertTrue(isinstance(node.style.font_family, FontFamily))

        # Check Initial values
        self.assertEqual(node.style.font_family, FontFamily([INITIAL]))

        # Check lists as input
        node.style.font_family = ['Ahem', 'White Space', 'serif']
        self.assertTrue(isinstance(node.style.font_family, FontFamily))
        self.assertEqual(node.style.font_family, FontFamily(['Ahem', 'White Space', 'serif']))

        # Check strings as input
        node.style.font_family = 'Ahem, "White Space", serif'
        self.assertTrue(isinstance(node.style.font_family, FontFamily))
        self.assertEqual(node.style.font_family, FontFamily(['Ahem', 'White Space', 'serif']))

        # Check string
        self.assertEqual(str(node.style.font_family), 'Ahem, "White Space", serif')
        self.assertEqual(str(node.style), 'font-family: Ahem, "White Space", serif')

        # # Check resets value
        del node.style.font_family
        self.assertEqual(node.style.font_family, FontFamily([INITIAL]))

        # Check invalid values
        with self.assertRaises(ValueError):
            node.style.font_family = 1

        with self.assertRaises(ValueError):
            node.style.font_family = {1}
