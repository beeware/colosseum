from .colors import NAMED_COLOR, hsl, rgb
from .exceptions import ValidationError
from .fonts import get_system_font
from .units import Unit, px


def units(value):
    """Parse a unit value

    Accepts:
    * An already converted instance of unit
    * An integer (interpreted as pixels)
    * A float (interpreted as pixels)
    * A string with a known unit suffix
    * A string containing an float (interpreted as pixels)
    """
    if isinstance(value, Unit):
        return value
    elif isinstance(value, (int, float)):
        return value * px
    elif isinstance(value, str):
        for suffix, unit in Unit.UNITS:
            if value.endswith(suffix):
                try:
                    return float(value[:-len(suffix)]) * unit
                except ValueError:
                    pass

        try:
            return float(value) * px
        except ValueError:
            pass

    raise ValueError('Unknown size %s' % value)


def color(value):
    """Parse a color from a value.

    Accepts:
    * rgb() instances
    * hsl() instances
    * '#RGB'
    * '#RGBA'
    * '#RRGGBB'
    * '#RRGGBBAA'
    * 'rgb(0, 0, 0)'
    * 'rgba(0, 0, 0, 0.0)'
    * 'hsl(0, 0%, 0%)'
    * 'hsla(0, 0%, 0%, 0.0)'
    * A named color
    """

    if isinstance(value, (rgb, hsl)):
        return value

    elif isinstance(value, str):
        if value[0] == '#':
            if len(value) == 4:
                return rgb(
                    r=int(value[1] + value[1], 16),
                    g=int(value[2] + value[2], 16),
                    b=int(value[3] + value[3], 16),
                )
            elif len(value) == 5:
                return rgb(
                    r=int(value[1] + value[1], 16),
                    g=int(value[2] + value[2], 16),
                    b=int(value[3] + value[3], 16),
                    a=int(value[4] + value[4], 16) / 0xff,
                )
            elif len(value) == 7:
                return rgb(
                    r=int(value[1:3], 16),
                    g=int(value[3:5], 16),
                    b=int(value[5:7], 16),
                )
            elif len(value) == 9:
                return rgb(
                    r=int(value[1:3], 16),
                    g=int(value[3:5], 16),
                    b=int(value[5:7], 16),
                    a=int(value[7:9], 16) / 0xff,
                )
        elif value.startswith('rgba'):
            try:
                values = value[5:-1].split(',')
                if len(values) == 4:
                    return rgb(int(values[0]), int(values[1]), int(values[2]), float(values[3]))
            except ValueError:
                pass
        elif value.startswith('rgb'):
            try:
                values = value[4:-1].split(',')
                if len(values) == 3:
                    return rgb(int(values[0]), int(values[1]), int(values[2]))
            except ValueError:
                pass

        elif value.startswith('hsla'):
            try:
                values = value[5:-1].split(',')
                if len(values) == 4:
                    return hsl(
                        int(values[0]),
                        int(values[1].strip().rstrip('%')) / 100.0,
                        int(values[2].strip().rstrip('%')) / 100.0,
                        float(values[3])
                    )
            except ValueError:
                pass

        elif value.startswith('hsl'):
            try:
                values = value[4:-1].split(',')
                if len(values) == 3:
                    return hsl(
                        int(values[0]),
                        int(values[1].strip().rstrip('%')) / 100.0,
                        int(values[2].strip().rstrip('%')) / 100.0,
                    )
            except ValueError:
                pass
        else:
            try:
                return NAMED_COLOR[value.lower()]
            except KeyError:
                pass

    raise ValueError('Unknown color %s' % value)


##############################################################################
# Font handling
##############################################################################
def _parse_font_property_part(value, font_dict):
    """Parse font shorthand property part for known properties."""
    from .constants import (FONT_SIZE_CHOICES, FONT_STYLE_CHOICES, FONT_VARIANT_CHOICES,
                            FONT_WEIGHT_CHOICES, LINE_HEIGHT_CHOICES, NORMAL)
    font_dict = font_dict.copy()
    if value != NORMAL:
        for property_name, choices in {'font_variant': FONT_VARIANT_CHOICES,
                                       'font_weight': FONT_WEIGHT_CHOICES,
                                       'font_style': FONT_STYLE_CHOICES}.items():
            try:
                value = choices.validate(value)
                font_dict[property_name] = value
                return font_dict
            except (ValidationError, ValueError):
                pass

        if '/' in value:
            # Maybe it is a font size with line height
            font_dict['font_size'], font_dict['line_height'] = value.split('/')
            FONT_SIZE_CHOICES.validate(font_dict['font_size'])
            LINE_HEIGHT_CHOICES.validate(font_dict['line_height'])
            return font_dict
        else:
            # Or just a font size
            try:
                FONT_SIZE_CHOICES.validate(value)
                font_dict['font_size'] = value
                return font_dict
            except ValueError:
                pass

        raise ValidationError('Font value "{value}" not valid!'.format(value=value))

    return font_dict


def parse_font(string):
    """
    Parse font string into a dictionary of font properties.

    The font CSS property is a shorthand for font-style, font-variant, font-weight,
    font-size, line-height, and font-family.

    Alternatively, it sets an element's font to a system font.

    Reference:
    - https://www.w3.org/TR/CSS21/fonts.html#font-shorthand
    - https://developer.mozilla.org/en-US/docs/Web/CSS/font
    """
    from .constants import INHERIT, INITIAL_FONT_VALUES, SYSTEM_FONT_KEYWORDS, FONT_FAMILY_CHOICES  # noqa
    font_dict = INITIAL_FONT_VALUES.copy()

    # Remove extra spaces
    string = ' '.join(str(string).strip().split())

    parts = string.split(' ', 1)
    if len(parts) == 1:
        # If font is specified as a system keyword, it must be one of:
        # caption, icon, menu, message-box, small-caption, status-bar
        value = parts[0]
        if value == INHERIT:
            # TODO: To be completed by future work
            pass
        else:
            if value not in SYSTEM_FONT_KEYWORDS:
                error_msg = ('Font property value "{value}" '
                             'not a system font keyword!'.format(value=value))
                raise ValueError(error_msg)
            font_dict = get_system_font(value)
    else:
        # If font is specified as a shorthand for several font-related properties, then:
        #  - It must include values for:
        #    <font-size> and <font-family>
        #  - It may optionally include values for:
        #    <font-style> <font-variant> <font-weight> and <line-height>
        #  - font-style, font-variant and font-weight must precede font-size
        #  - font-variant may only specify the values defined in CSS 2.1
        #  - line-height must immediately follow font-size, preceded by "/", like this: "16px/3"
        #  - font-family must be the last value specified.

        # We iteratively split by the first left hand space found and try to validate if that part
        # is a valid <font-style> or <font-variant> or <font-weight> (which can come in any order)
        # or <font-size>/<line-height> (which has to come after all the other properties)
        for _ in range(5):
            value = parts[0]
            try:
                font_dict = _parse_font_property_part(value, font_dict)
                parts = parts[-1].split(' ', 1)
            except ValidationError:
                break
        else:
            # Font family can have a maximum of 4 parts before the font_family part.
            # <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
            raise ValueError('Font property shorthand contains too many parts!')

        value = ' '.join(parts)
        font_dict['font_family'] = FONT_FAMILY_CHOICES.validate(value)

    return font_dict


def construct_font(font_dict):
    """Construct font property string from a dictionary of font properties."""
    font_dict_copy = font_dict.copy()
    font_dict_copy['font_family'] = construct_font_family(font_dict_copy['font_family'])

    return ('{font_style} {font_variant} {font_weight} '
            '{font_size}/{line_height} {font_family}').format(**font_dict_copy)


def construct_font_family(font_family):
    """Construct a font family property from a list of font families."""
    assert isinstance(font_family, list)
    checked_font_family = []
    for family in font_family:
        if ' ' in family:
            family = '"{value}"'.format(value=family)

        checked_font_family.append(family)

    return ', '.join(checked_font_family)
