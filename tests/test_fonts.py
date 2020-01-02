from unittest import TestCase

from colosseum.fonts import parse_font_property
from colosseum.validators import ValidationError


FONT_CASES = {
    r'12px/14px sans-serif': {
        'font_style': 'normal',
        'font_variant': 'normal',
        'font_weight': 'normal',
        'font_size': '12px',
        'line_height': '14px',
        'font_family': 'sans-serif',
        },
    r'80% sans-serif': {
        'font_style': 'normal',
        'font_variant': 'normal',
        'font_weight': 'normal',
        'font_size': '80%',
        'line_height': 'normal',
        'font_family': 'sans-serif',
        },
    r'bold italic large Palatino, serif': {
        'font_style': 'italic',
        'font_variant': 'normal',
        'font_weight': 'bold',
        'font_size': 'large',
        'line_height': 'normal',
        'font_family': 'Palatino, serif',
        },
    r'normal small-caps 120%/120% fantasy': {
        'font_style': 'normal',
        'font_variant': 'small-caps',
        'font_weight': 'normal',
        'font_size': '120%',
        'line_height': '120%',
        'font_family': 'fantasy',
        },
    r'x-large/110% "New  Century Schoolbook",serif': {
        'font_style': 'normal',
        'font_variant': 'normal',
        'font_weight': 'normal',
        'font_size': 'x-large',
        'line_height': '110%',
        'font_family': '"New Century Schoolbook", serif',
        },
}


class FontTests(TestCase):
    def test_parse_font_shorthand(self):
        for case in sorted(FONT_CASES):
            expected_output = FONT_CASES[case]
            font = parse_font_property(case)
            self.assertEqual(font, expected_output)

        # Test extra spaces
        parse_font_property(r'  normal    normal    normal    12px/12px   serif  ')

        with self.assertRaises(ValidationError):
            font = parse_font_property(r'normal normal normal normal 12px/12px serif')
