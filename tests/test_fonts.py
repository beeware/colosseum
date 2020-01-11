from colosseum.fonts import FontDatabase, get_system_font
from colosseum.constants import INITIAL_FONT_VALUES

from .utils import ColosseumTestCase


class ParseFontTests(ColosseumTestCase):

    def test_font_database(self):
        # Check empty cache
        FontDatabase.clear_cache()
        self.assertEqual(FontDatabase._FONTS_CACHE, {})  # noqa

        # Check populated cache
        FontDatabase.validate_font_family('Ahem')
        FontDatabase.validate_font_family('White Space')
        self.assertEqual(FontDatabase._FONTS_CACHE, {'Ahem': None, 'White Space': None})  # noqa

        # Check clear cache
        FontDatabase.clear_cache()
        self.assertEqual(FontDatabase._FONTS_CACHE, {})  # noq

        # Check returns a string
        self.assertTrue(bool(FontDatabase.fonts_path(system=True)))
        self.assertTrue(bool(FontDatabase.fonts_path(system=False)))

    def test_get_system_font(self):
        self.assertEqual(get_system_font('status-bar'), INITIAL_FONT_VALUES)
