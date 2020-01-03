from .constants import (FONT_FAMILY_CHOICES, FONT_SIZE_CHOICES,
                        FONT_STYLE_CHOICES, FONT_VARIANT_CHOICES,
                        FONT_WEIGHT_CHOICES, INHERIT, INITIAL_FONT_VALUES,
                        NORMAL, SYSTEM_FONT_KEYWORDS)
from .validators import ValidationError


def get_system_font(keyword):
    """Return a font object from given system font keyword."""
    if keyword in SYSTEM_FONT_KEYWORDS:
        return '"Arial Black"'
        # Get the system font
    return None


def construct_font_property(font):
    """Construct font property string from a dictionary of font properties."""
    if isinstance(font['font_family'], list):
        font['font_family'] = ', '.join(font['font_family'])

    return ('{font_style} {font_variant} {font_weight} '
            '{font_size}/{line_height} {font_family}').format(**font)


def parse_font_property_part(value, font):
    """Parse font shorthand property part for known properties."""
    if value != NORMAL:
        for property_name, choices in {'font_variant': FONT_VARIANT_CHOICES,
                                       'font_weight': FONT_WEIGHT_CHOICES,
                                       'font_style': FONT_STYLE_CHOICES}.items():
            try:
                value = choices.validate(value)
                font[property_name] = value
                return font
            except (ValidationError, ValueError):
                pass

        # Maybe it is a font size
        if '/' in value:
            font['font_size'], font['line_height'] = value.split('/')
            return font
        else:
            try:
                FONT_SIZE_CHOICES.validate(value)
                font['font_size'] = value
                return font
            except ValueError:
                pass

        raise ValidationError

    return font


def parse_font_property(string):
    """
    Parse font string into a dictionary of font properties.

    Reference:
    - https://www.w3.org/TR/CSS21/fonts.html#font-shorthand
    - https://developer.mozilla.org/en-US/docs/Web/CSS/font
    """
    font = INITIAL_FONT_VALUES.copy()

    # Remove extra spaces
    string = ' '.join(string.strip().split())

    parts = string.split(' ', 1)
    if len(parts) == 1:
        value = parts[0]
        if value == INHERIT:
            # TODO: ??
            pass
        else:
            if value not in SYSTEM_FONT_KEYWORDS:
                error_msg = ('Font property value "{value}" '
                             'not a system font keyword!'.format(value=value))
                raise ValidationError(error_msg)
            font = get_system_font(value)
    else:
        for _ in range(5):
            value = parts[0]
            try:
                font = parse_font_property_part(value, font)
                parts = parts[-1].split(' ', 1)
            except ValidationError:
                break
        else:
            # Font family can have a maximum of 4 parts before the font_family part
            raise ValidationError('Font property shorthand contains too many parts!')

        value = ' '.join(parts)
        font['font_family'] = FONT_FAMILY_CHOICES.validate(value)

    return font
