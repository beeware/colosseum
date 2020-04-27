from collections import OrderedDict
from itertools import permutations
from unittest import TestCase

from colosseum.units import px
from colosseum.wrappers import (Border, BorderBottom, BorderLeft, BorderRight,
                                BorderSpacing, BorderTop, FontFamily,
                                FontShorthand, ImmutableList, Outline, Quotes,
                                Shorthand)


class BorderSpacingTests(TestCase):

    def test_valid_1_arg_string(self):
        border_spacing = BorderSpacing('1')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '1')
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1')")

    def test_valid_1_arg_int(self):
        border_spacing = BorderSpacing(1)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 1)
        self.assertEqual(str(border_spacing), '1')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1)")

    def test_valid_1_arg_px(self):
        border_spacing = BorderSpacing(1 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 1 * px)
        self.assertEqual(str(border_spacing), '1px')
        self.assertEqual(repr(border_spacing), "BorderSpacing(1px)")

    def test_valid_2_arg_str(self):
        border_spacing = BorderSpacing('1', '2')
        self.assertEqual(border_spacing.horizontal, '1')
        self.assertEqual(border_spacing.vertical, '2')
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), "BorderSpacing('1', '2')")

    def test_valid_2_arg_int(self):
        border_spacing = BorderSpacing(1, 2)
        self.assertEqual(border_spacing.horizontal, 1)
        self.assertEqual(border_spacing.vertical, 2)
        self.assertEqual(str(border_spacing), '1 2')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1, 2)')

    def test_valid_2_arg_px(self):
        border_spacing = BorderSpacing(1 * px, 2 * px)
        self.assertEqual(border_spacing.horizontal, 1 * px)
        self.assertEqual(border_spacing.vertical, 2 * px)
        self.assertEqual(str(border_spacing), '1px 2px')
        self.assertEqual(repr(border_spacing), 'BorderSpacing(1px, 2px)')

    def test_invalid_arg_number(self):
        with self.assertRaises(TypeError):
            BorderSpacing(1, 2, 3)


class ImmutableListTests(TestCase):

    def test_immutable_list_initial(self):
        # Check initial
        ilist = ImmutableList()
        self.assertEqual(str(ilist), 'ImmutableList()')
        self.assertEqual(repr(ilist), 'ImmutableList()')
        self.assertEqual(len(ilist), 0)

    def test_immutable_list_creation(self):
        # Check value
        ilist = ImmutableList([1])
        self.assertEqual(str(ilist), "ImmutableList([1])")
        self.assertEqual(repr(ilist), "ImmutableList([1])")
        self.assertEqual(len(ilist), 1)

        # Check values
        ilist = ImmutableList(['Ahem', 'White Space', 'serif'])
        self.assertEqual(str(ilist), "ImmutableList(['Ahem', 'White Space', 'serif'])")
        self.assertEqual(repr(ilist), "ImmutableList(['Ahem', 'White Space', 'serif'])")
        self.assertEqual(len(ilist), 3)

    def test_immutable_list_get_item(self):
        # Check get item
        ilist = ImmutableList(['Ahem', 'White Space', 'serif'])
        self.assertEqual(ilist[0], 'Ahem')
        self.assertEqual(ilist[-1], 'serif')

    def test_immutable_list_set_item(self):
        # Check immutable
        ilist = ImmutableList()
        with self.assertRaises(TypeError):
            ilist[0] = 'initial'

    def test_immutable_list_equality(self):
        # Check equality
        ilist1 = ImmutableList(['Ahem', 2])
        ilist2 = ImmutableList(['Ahem', 2])
        ilist3 = ImmutableList([2, 'Ahem'])
        self.assertEqual(ilist1, ilist2)
        self.assertNotEqual(ilist1, ilist3)

    def test_immutable_list_hash(self):
        # Check hash
        ilist1 = ImmutableList(['Ahem', 2])
        ilist2 = ImmutableList(['Ahem', 2])

        self.assertEqual(hash(ilist1), hash(ilist2))

    def test_immutable_list_id(self):
        # Check id
        ilist1 = ImmutableList(['Ahem', 2])
        ilist2 = ImmutableList(['Ahem', 2])
        self.assertNotEqual(id(ilist1), id(ilist2))
        self.assertNotEqual(id(ilist1), id(ilist1.copy()))
        self.assertNotEqual(id(ilist2), id(ilist1.copy()))

    def test_immutable_list_copy(self):
        # Check copy
        ilist1 = ImmutableList(['Ahem', 2])
        ilist2 = ImmutableList(['Ahem', 2])

        self.assertEqual(hash(ilist2), hash(ilist1.copy()))
        self.assertEqual(ilist1, ilist1.copy())


class FontFamilyTests(TestCase):

    def test_fontfamily_initial(self):
        # Check initial
        font = FontFamily()
        self.assertEqual(str(font), '')
        self.assertEqual(repr(font), 'FontFamily()')
        self.assertEqual(len(font), 0)

    def test_fontfamily_values(self):
        # Check value
        font = FontFamily(['Ahem'])
        self.assertEqual(str(font), 'Ahem')
        self.assertEqual(repr(font), "FontFamily(['Ahem'])")
        self.assertEqual(len(font), 1)

        # Check values
        font = FontFamily(['Ahem', 'White Space', 'serif'])
        self.assertEqual(str(font), 'Ahem, "White Space", serif')
        self.assertEqual(repr(font), "FontFamily(['Ahem', 'White Space', 'serif'])")
        self.assertEqual(len(font), 3)

    def test_fontfamily_get_item(self):
        # Check get item
        font = FontFamily(['Ahem', 'White Space', 'serif'])
        self.assertEqual(font[0], 'Ahem')
        self.assertEqual(font[-1], 'serif')

    def test_fontfamily_set_item(self):
        # Check immutable
        font = FontFamily(['Ahem', 'White Space', 'serif'])
        with self.assertRaises(TypeError):
            font[0] = 'initial'

    def test_fontfamily_equality(self):
        # Check equality
        font1 = FontFamily(['Ahem', 'serif'])
        font2 = FontFamily(['Ahem', 'serif'])
        font3 = FontFamily(['serif', 'Ahem'])
        self.assertEqual(font1, font2)
        self.assertNotEqual(font1, font3)

    def test_fontfamily_hash(self):
        # Check hash
        font1 = FontFamily(['Ahem', 'serif'])
        font2 = FontFamily(['Ahem', 'serif'])
        self.assertEqual(hash(font1), hash(font2))

    def test_fontfamily_copy(self):
        # Check copy
        font1 = FontFamily(['Ahem', 'serif'])
        font2 = FontFamily(['Ahem', 'serif'])
        self.assertNotEqual(id(font1), id(font2))
        self.assertNotEqual(id(font1), id(font1.copy()))
        self.assertNotEqual(id(font2), id(font2.copy()))
        self.assertEqual(font1, font1.copy())


class ShorthandTests(TestCase):

    def test_shorthand(self):
        shorthand = Shorthand()
        self.assertEqual(str(shorthand), 'Shorthand()')
        self.assertEqual(repr(shorthand), ("Shorthand()"))


class FontShorthandTests(TestCase):

    def test_font_shorthand_initial(self):
        # Check initial
        font = FontShorthand()
        self.assertEqual(str(font), 'normal normal normal medium/normal initial')
        self.assertEqual(
            repr(font),
            ("FontShorthand(font_style='normal', font_variant='normal', font_weight='normal', "
             "font_size='medium', line_height='normal', font_family=FontFamily(['initial']))")
        )

    def test_font_shorthand_set_weight(self):
        font = FontShorthand(font_weight='bold')
        self.assertEqual(str(font), 'normal normal bold medium/normal initial')
        self.assertEqual(
            repr(font),
            ("FontShorthand(font_style='normal', font_variant='normal', font_weight='bold', "
             "font_size='medium', line_height='normal', font_family=FontFamily(['initial']))")
        )

    def test_font_shorthand_set_variant(self):
        font = FontShorthand(font_variant='small-caps')
        self.assertEqual(str(font), 'normal small-caps normal medium/normal initial')
        self.assertEqual(
            repr(font),
            ("FontShorthand(font_style='normal', font_variant='small-caps', font_weight='normal', "
             "font_size='medium', line_height='normal', font_family=FontFamily(['initial']))")
        )

    def test_font_shorthand_set_style(self):
        font = FontShorthand(font_style='oblique')
        self.assertEqual(str(font), 'oblique normal normal medium/normal initial')
        self.assertEqual(
            repr(font),
            ("FontShorthand(font_style='oblique', font_variant='normal', font_weight='normal', "
             "font_size='medium', line_height='normal', font_family=FontFamily(['initial']))")
        )

    def test_font_shorthand_invalid_key(self):
        # Check invalid key
        font = FontShorthand()
        with self.assertRaises(KeyError):
            font['invalid-key'] = 2

    def test_font_shorthand_copy(self):
        # Copy
        font = FontShorthand()
        self.assertEqual(font, font.copy())
        self.assertNotEqual(id(font), id(font.copy()))

    def test_font_shorthand_iteration(self):
        font = FontShorthand()
        keys = []
        for prop in font:
            keys.append(prop)
        self.assertEqual(len(keys), 6)
class QuotesTests(TestCase):

    # Valid cases
    def test_quotes_valid_1_pair(self):
        quotes = Quotes([('<', '>')])

        self.assertEqual(quotes.opening(level=0), '<')
        self.assertEqual(quotes.closing(level=0), '>')
        self.assertEqual(len(quotes), 1)
        self.assertEqual(str(quotes), "'<' '>'")
        self.assertEqual(repr(quotes), "Quotes([('<', '>')])")

    def test_quotes_valid_2_pairs(self):
        quotes = Quotes([('<', '>'), ('{', '}')])

        self.assertEqual(quotes.opening(level=0), '<')
        self.assertEqual(quotes.closing(level=0), '>')
        self.assertEqual(quotes.opening(level=1), '{')
        self.assertEqual(quotes.closing(level=1), '}')
        self.assertEqual(len(quotes), 2)
        self.assertEqual(str(quotes), "'<' '>' '{' '}'")
        self.assertEqual(repr(quotes), "Quotes([('<', '>'), ('{', '}')])")

    # Invalid cases
    def test_quotes_invalid_1_pair_level(self):
        quotes = Quotes([('<', '>')])

        with self.assertRaises(IndexError):
            quotes.opening(level=1)

        with self.assertRaises(IndexError):
            quotes.closing(level=1)


class TestShorthand(TestCase):

    def test_shorthand_invalid_empty(self):
        with self.assertRaises(ValueError):
            Shorthand()


class TestShorthandOutline(TestCase):

    def test_shorthand_outline_valid_empty(self):
        outline = Outline()
        self.assertEqual(str(outline), '')
        self.assertEqual(repr(outline), 'Outline()')

    def test_shorthand_outline_valid_1_kwargs(self):
        for property_name in ['outline_color', 'outline_style', 'outline_width']:
            outline = Outline(**{property_name: 1})
            self.assertEqual(str(outline), '1')
            self.assertEqual(getattr(outline, property_name), 1)

    def test_shorthand_outline_valid_2_kwargs(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'], 2)
        for (prop_1, prop_2) in perms:
            kwargs = {prop_1: 1, prop_2: 2}
            outline = Outline(**kwargs)
            self.assertEqual(str(outline), ' '.join(str(v[1]) for v in sorted(kwargs.items())))

    def test_shorthand_outline_valid_3_kwargs(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(str(outline), ' '.join(str(v[1]) for v in sorted(kwargs.items())))

    def test_shorthand_outline_valid_get_values(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(getattr(outline, prop_1), kwargs[prop_1])
            self.assertEqual(getattr(outline, prop_2), kwargs[prop_2])
            self.assertEqual(getattr(outline, prop_3), kwargs[prop_3])

    def test_shorthand_outline_valid_set_values(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(getattr(outline, prop_1), kwargs[prop_1])
            self.assertEqual(getattr(outline, prop_2), kwargs[prop_2])
            self.assertEqual(getattr(outline, prop_3), kwargs[prop_3])

    def test_shorthand_outline_equality(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline1 = Outline(**kwargs)
            outline2 = Outline(**kwargs)
            self.assertEqual(outline1, outline2)

    def test_shorthand_outline_valid_to_dict(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(outline.to_dict(), kwargs)

    # Invalid cases
    def test_shorthand_outline_invalid_kwargs(self):
        with self.assertRaises(ValueError):
            Outline(foobar='foobar')


class TestShorthandBorder(TestCase):

    def test_shorthand_boder_valid_empty(self):
        for wrapper_class in [Border, BorderBottom, BorderLeft, BorderRight, BorderTop]:
            wrapper = wrapper_class()
            self.assertEqual(str(wrapper), '')
            self.assertEqual(repr(wrapper), wrapper_class.__name__ + '()')

    def test_shorthand_outline_valid_1_kwargs(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            for property_name in ['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)]:

                wrapper = wrapper_class(**{property_name: 1})
                self.assertEqual(str(wrapper), '1')
                self.assertEqual(getattr(wrapper, property_name), 1)

    def test_shorthand_outline_valid_2_kwargs(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)], 2)

            for (prop_1, prop_2) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for property_name in wrapper_class.VALID_KEYS:
                    if prop_1 == property_name:
                        kwargs[prop_1] = 1

                    elif prop_2 == property_name:
                        kwargs[prop_2] = 2

                wrapper = wrapper_class(**kwargs)
                self.assertEqual(str(wrapper), ' '.join(str(v[1]) for v in kwargs.items()))

    def test_shorthand_outline_valid_3_kwargs(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)])

            for (prop_1, prop_2, prop_3) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for idx, property_name in enumerate(wrapper_class.VALID_KEYS):
                    kwargs[property_name] = idx + 1

                wrapper = wrapper_class(**kwargs)
                self.assertEqual(str(wrapper), ' '.join(str(v[1]) for v in kwargs.items()))

    def test_shorthand_outline_valid_get_values(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)])

            for (prop_1, prop_2, prop_3) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for idx, property_name in enumerate(wrapper_class.VALID_KEYS):
                    kwargs[property_name] = idx + 1

                wrapper = wrapper_class(**kwargs)
                self.assertEqual(getattr(wrapper, prop_1), kwargs[prop_1])
                self.assertEqual(getattr(wrapper, prop_2), kwargs[prop_2])
                self.assertEqual(getattr(wrapper, prop_3), kwargs[prop_3])

    def test_shorthand_outline_valid_set_values(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)])

            for (prop_1, prop_2, prop_3) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for idx, property_name in enumerate(wrapper_class.VALID_KEYS):
                    kwargs[property_name] = idx + 1

                wrapper = wrapper_class(**kwargs)
                self.assertEqual(getattr(wrapper, prop_1), kwargs[prop_1])
                self.assertEqual(getattr(wrapper, prop_2), kwargs[prop_2])
                self.assertEqual(getattr(wrapper, prop_3), kwargs[prop_3])

    def test_shorthand_outline_equality(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)])

            for (prop_1, prop_2, prop_3) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for idx, property_name in enumerate(wrapper_class.VALID_KEYS):
                    kwargs[property_name] = idx + 1

                wrapper1 = wrapper_class(**kwargs)
                wrapper2 = wrapper_class(**kwargs)
                self.assertEqual(wrapper1, wrapper2)

    def test_shorthand_outline_valid_to_dict(self):
        for direction, wrapper_class in {'': Border,
                                         'bottom_': BorderBottom,
                                         'left_': BorderLeft,
                                         'right_': BorderRight,
                                         'top_': BorderTop}.items():

            perms = permutations(['border_{direction}color'.format(direction=direction),
                                  'border_{direction}style'.format(direction=direction),
                                  'border_{direction}width'.format(direction=direction)])

            for (prop_1, prop_2, prop_3) in perms:
                kwargs = OrderedDict()

                # This is to guarantee the proper order
                for idx, property_name in enumerate(wrapper_class.VALID_KEYS):
                    kwargs[property_name] = idx + 1

                wrapper = wrapper_class(**kwargs)
                self.assertEqual(wrapper.to_dict(), kwargs)

    # Invalid cases
    def test_shorthand_outline_invalid_kwargs(self):
        for wrapper_class in [Border, BorderBottom, BorderLeft, BorderRight, BorderTop]:
            with self.assertRaises(ValueError):
                wrapper_class(foobar='foobar')
