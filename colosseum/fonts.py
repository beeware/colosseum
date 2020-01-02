import re

from .constants import (FONT_STYLE_CHOICES, FONT_VARIANT_CHOICES,
                        FONT_WEIGHT_CHOICES, INHERIT, INITIAL_FONT_VALUES,
                        NORMAL, SYSTEM_FONT_KEYWORDS)
from .validators import ValidationError

# Find spaces within single and double quotes
SQ_PATTERN = re.compile(r"\s+(?=(?:(?:[^']*'){2})*[^']*'[^']*$)")
DQ_PATTERN = re.compile(r'\s+(?=(?:(?:[^"]*"){2})*[^"]*"[^"]*$)')


def get_system_font(keyword):
    """Return a font object from given system font keyword."""
    if keyword in SYSTEM_FONT_KEYWORDS:
        # Get the system font
        font = INITIAL_FONT_VALUES.copy()
    return font


def construct_font_property(font):
    """Construct font property string from a dictionary of font properties."""
    return ('{font_style} {font_variant} {font_weight} '
            '{font_size}/{line_height} {font_family}').format(**font)


def replace_font_family_spaces(string, space_sep):
    """Replace spaces between quotes by character."""
    string = SQ_PATTERN.sub(space_sep, string)
    string = DQ_PATTERN.sub(space_sep, string)
    return string


def parse_font_property(string):
    """
    Parse font string into a dictionary of font properties.

    Reference:
    - https://www.w3.org/TR/CSS22/fonts.html#font-shorthand
    - https://developer.mozilla.org/en-US/docs/Web/CSS/font
    """
    font = INITIAL_FONT_VALUES.copy()
    comma, space = ', ', ' '
    comma_sep, space_sep = '~', '@'

    # Remove extra inner spaces
    string = space.join(string.strip().split())

    # Replace commas between font families with some character
    string = string.replace(comma, comma_sep)
    string = string.replace(comma[0], comma_sep)
    string = replace_font_family_spaces(string, space_sep)
    parts = string.split()

    if len(parts) == 1:
        value = parts[0]
        if value == INHERIT:
            # ??
            pass
        else:
            if value not in SYSTEM_FONT_KEYWORDS:
                error_msg = ('Font property value "{value}" '
                             'not a system font keyword!'.format(value=value))
                raise ValidationError(error_msg)
            font = get_system_font(value)
    elif len(parts) <= 5:
        font_properties, font_family = parts[:-1], parts[-1]

        # Restore original space characters
        font_family = font_family.replace(comma_sep, comma)
        font_family = font_family.replace(space_sep, space)
        font['font_family'] = font_family

        # font size is be the last item on the rest of font properties
        font['font_size'] = font_properties.pop(-1)

        for value in font_properties:
            if value != NORMAL:
                for property_name, choices in {'font_variant': FONT_VARIANT_CHOICES,
                                               'font_weight': FONT_WEIGHT_CHOICES,
                                               'font_style': FONT_STYLE_CHOICES}.items():
                    try:
                        value = choices.validate(value)
                        font[property_name] = value
                    except (ValidationError, ValueError):
                        pass

        if '/' in font['font_size']:
            font['font_size'], font['line_height'] = font['font_size'].split('/')
    else:
        error_msg = ('Font property shorthand contains too many parts!')
        raise ValidationError(error_msg)

    return font
