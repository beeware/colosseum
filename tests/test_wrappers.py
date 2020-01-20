from unittest import TestCase

from colosseum.wrappers import FontFamily, FontShorthand, ImmutableList, Shorthand


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
