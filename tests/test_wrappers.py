from itertools import permutations
from unittest import TestCase

from colosseum.units import px
from colosseum.wrappers import BorderSpacing, Outline, Quotes


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


class TestShorthandOutline(TestCase):

    def test_shorthand_outline_valid_empty(self):
        outline = Outline()
        self.assertEqual(str(outline), '')
        self.assertEqual(repr(outline), 'Outline()')
        self.assertEqual(len(outline), 0)

    def test_shorthand_outline_valid_1_kwargs(self):
        for property_name in ['outline_color', 'outline_style', 'outline_width']:
            outline = Outline(**{property_name: 1})
            self.assertEqual(str(outline), '1')
            self.assertEqual(outline[property_name], 1)

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

    def test_shorthand_outline_valid_len(self):
        outline = Outline(outline_color=1)
        self.assertEqual(len(outline), 1)

        outline = Outline(outline_color=1, outline_style=2)
        self.assertEqual(len(outline), 2)

        outline = Outline(outline_color=1, outline_style=2, outline_width=3)
        self.assertEqual(len(outline), 3)

    def test_shorthand_outline_valid_get_values(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(outline[prop_1], kwargs[prop_1])
            self.assertEqual(outline[prop_2], kwargs[prop_2])
            self.assertEqual(outline[prop_3], kwargs[prop_3])

    def test_shorthand_outline_valid_set_values(self):
        perms = permutations(['outline_color', 'outline_style', 'outline_width'])
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}

            outline = Outline()
            outline[prop_1] = kwargs[prop_1]
            outline[prop_2] = kwargs[prop_2]
            outline[prop_3] = kwargs[prop_3]

            self.assertEqual(outline[prop_1], kwargs[prop_1])
            self.assertEqual(outline[prop_2], kwargs[prop_2])
            self.assertEqual(outline[prop_3], kwargs[prop_3])

    def test_shorthand_outline_valid_iter(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            items = []
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            for item in outline:
                items.append(item)

            self.assertEqual(items, expected_output)

    def test_shorthand_outline_valid_keys(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            keys = []
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            for key in outline.keys():
                keys.append(key)

            self.assertEqual(keys, expected_output)

    def test_shorthand_outline_valid_items(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(outline.items(), sorted(list(kwargs.items())))

    def test_shorthand_outline_valid_to_dict(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            self.assertEqual(outline.to_dict(), kwargs)

    def test_shorthand_outline_valid_copy(self):
        expected_output = ['outline_color', 'outline_style', 'outline_width']
        perms = permutations(expected_output)
        for (prop_1, prop_2, prop_3) in perms:
            kwargs = {prop_1: 1, prop_2: 2, prop_3: 3}
            outline = Outline(**kwargs)
            copy = outline.copy()
            self.assertEqual(outline, copy)
            self.assertNotEqual(id(outline), id(copy))

    # Invalid cases
    def test_shorthand_outline_invalid_kwargs(self):
        with self.assertRaises(ValueError):
            Outline(foobar='foobar')
