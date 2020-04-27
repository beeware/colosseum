from ast import literal_eval
from collections import Sequence

from .colors import NAMED_COLOR, hsl, rgb
from .exceptions import ValidationError
from .fonts import get_system_font
from .shapes import Rect
from .units import Unit, px
from .wrappers import BorderSpacing, FontFamily, Quotes


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


def border_spacing(value):
    """
    Parse a border spacing value.

    Accepts:
    * A sequence object different that a string.
    * An integer (interpreted as pixels).
    * A float (interpreted as pixels).
    * A string with of 1 or 2 length items separated by spaces.
    """
    if isinstance(value, Sequence) and not isinstance(value, str):
        values = value
    elif isinstance(value, (int, float)):
        values = (value, )
    else:
        values = [x.strip() for x in value.split()]

    if len(values) == 1:
        horizontal = units(values[0])
        return BorderSpacing(horizontal)
    elif len(values) == 2:
        horizontal = units(values[0])
        vertical = units(values[1])
        return BorderSpacing(horizontal, vertical)

    raise ValueError('Unknown border spacing %s' % str(value))


def rect(value):
    """Parse a given rect shape."""
    value = ' '.join(val.strip() for val in value.split())
    if (value.startswith('rect(') and value.endswith(')') and
            value.count('rect(') == 1 and value.count(')') == 1):
        value = value.replace('rect(', '')
        value = value.replace(')', '').strip()

        values = None
        if value.count(',') == 3:
            values = value.split(',')
        elif value.count(',') == 0 and value.count(' ') == 3:
            values = value.split(' ')

        if values is not None:
            values = [units(val.strip()) for val in values]
            return Rect(*values)

    raise ValueError('Unknown shape %s' % value)


##############################################################################
# Font handling
##############################################################################
def _parse_font_property_part(value, font_dict):
    """
    Parse font shorthand property part for known properties.

    `value` corresponds to a piece (or part) of a font shorthand property that can
    look like:
     - '<font-style> <font-variant> <font-weight> <font-size>/<line-height> ...
     - '<font-size>/<line-height> ...'
     - '<font-weight> <font-style> <font-size>/<line-height> ...'
     - ...

    Each part can then correspond to one of these values:
    <font-style>, <font-variant>, <font-weight>, <font-size>/<line-height>

    The `font_dict` keeps track fo parts that have been already parse so that we
    can check that a part is duplicated like:
     - '<font-style> <font-style> <font-size>/<line-height>'
    """
    from .constants import (FONT_SIZE_CHOICES, FONT_STYLE_CHOICES, FONT_VARIANT_CHOICES,
                            FONT_WEIGHT_CHOICES, LINE_HEIGHT_CHOICES, NORMAL)
    if value != NORMAL:
        for property_name, choices in {'font_variant': FONT_VARIANT_CHOICES,
                                       'font_weight': FONT_WEIGHT_CHOICES,
                                       'font_style': FONT_STYLE_CHOICES}.items():
            try:
                value = choices.validate(value)
            except (ValidationError, ValueError):
                continue

            # If a property has been already parsed, finding the same property is an error
            if property_name in font_dict:
                raise ValueError('Font value "{value}" includes several "{property_name}" values!'
                                 ''.format(value=value, property_name=property_name))

            font_dict[property_name] = value

            return font_dict, False

        if '/' in value:
            # Maybe it is a font size with line height
            font_dict['font_size'], font_dict['line_height'] = value.split('/')
            FONT_SIZE_CHOICES.validate(font_dict['font_size'])
            LINE_HEIGHT_CHOICES.validate(font_dict['line_height'])
            return font_dict, True
        else:
            # Or just a font size
            try:
                FONT_SIZE_CHOICES.validate(value)
                font_dict['font_size'] = value
                return font_dict, True
            except ValueError:
                pass

        raise ValidationError('Font value "{value}" not valid!'.format(value=value))

    return font_dict, False


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

        # Need to check that some properties come after font-size
        old_is_font_size = False
        font_dict = {}

        # We iteratively split by the first left hand space found and try to validate if that part
        # is a valid <font-style> or <font-variant> or <font-weight> (which can come in any order)
        # or <font-size>/<line-height> (which has to come after all the other properties)
        for _ in range(5):
            value = parts[0]
            try:
                font_dict, is_font_size = _parse_font_property_part(value, font_dict)
                if is_font_size is False and old_is_font_size:
                    raise ValueError('Font property shorthand does not follow the correct order!'
                                     '<font-style>, <font-variant> and <font-weight> must come before <font-size>')
                old_is_font_size = is_font_size
                parts = parts[-1].split(' ', 1)
            except ValidationError:
                break
        else:
            # Font family can have a maximum of 4 parts before the font_family part.
            # <font-style> <font-variant> <font-weight> <font-size>/<line-height> <font-family>
            raise ValueError('Font property shorthand contains too many parts!')

        values = ' '.join(parts).split(',')
        font_dict['font_family'] = FontFamily(FONT_FAMILY_CHOICES.validate(values))

    full_font_dict = INITIAL_FONT_VALUES.copy()
    full_font_dict.update(font_dict)

    return full_font_dict


def quotes(value):
    """Parse content quotes.

    Accepts:
    * A string: "'<' '>' '{' '}'"
    * A sequence: ('<', '>') or ['{', '}']
    * A list of 2 item tuples: [('<', '>'), ('{', '}')]
    """
    if isinstance(value, str):
        values = [val.strip() for val in value.split()]
    elif isinstance(value, Sequence):
        # Flatten list of tuples
        values = [repr(item) for sublist in value for item in sublist]
    else:
        raise ValueError('Unknown quote %s' % value)

    # Length must be a multiple of 2
    if len(values) > 0 and len(values) % 2 == 0:
        parsed_values = []
        for idx in range(len(values) // 2):
            start = idx * 2
            end = start + 2
            opening, closing = values[start:end]

            try:
                opening = literal_eval(opening)
                closing = literal_eval(closing)
                parsed_values.append((opening, closing))

                if len(opening) == 0 or len(closing) == 0:
                    raise ValueError('Invalid quotes %s' % value)

            except SyntaxError:
                raise ValueError('Invalid quotes %s' % value)

        return Quotes(parsed_values)

    raise ValueError('Length of quote items must be a multiple of 2!')


##############################################################################
# Outline shorthand
##############################################################################
def _parse_outline_property_part(value, outline_dict):
    """Parse outline shorthand property part for known properties."""
    from .constants import (  # noqa
        OUTLINE_COLOR_CHOICES, OUTLINE_STYLE_CHOICES, OUTLINE_WIDTH_CHOICES,
    )

    for property_name, choices in {'outline_color': OUTLINE_COLOR_CHOICES,
                                   'outline_style': OUTLINE_STYLE_CHOICES,
                                   'outline_width': OUTLINE_WIDTH_CHOICES}.items():
        try:
            value = choices.validate(value)
        except (ValueError, ValidationError):
            continue

        if property_name in outline_dict:
            raise ValueError('Invalid duplicated property!')

        outline_dict[property_name] = value
        return outline_dict

    raise ValueError('Outline value "{value}" not valid!'.format(value=value))


def outline(value):
    """
    Parse outline string into a dictionary of outline properties.

    The font CSS property is a shorthand for outline-style, outline-width, and outline-color.

    Reference:
    - https://www.w3.org/TR/2011/REC-CSS2-20110607/ui.html#dynamic-outlines
    - https://developer.mozilla.org/en-US/docs/Web/CSS/outline
    """
    if value:
        if isinstance(value, str):
            values = [val.strip() for val in value.split()]
        elif isinstance(value, Sequence):
            values = value
        else:
            raise ValueError('Unknown outline %s ' % value)
    else:
        raise ValueError('Unknown outline %s ' % value)

    # We iteratively split by the first left hand space found and try to validate if that part
    # is a valid <outline-style> or <outline-color> or <ourline-width> (which can come in any order)

    # We use this dictionary to store parsed values and check that values properties are not
    # duplicated
    outline_dict = {}
    for idx, part in enumerate(values):
        if idx > 2:
            # Outline can have a maximum of 3 parts
            raise ValueError('Outline property shorthand contains too many parts!')

        outline_dict = _parse_outline_property_part(part, outline_dict)

    return outline_dict


##############################################################################
# Border shorthands
##############################################################################
def _parse_border_property_part(value, border_dict, direction=None):
    """Parse border shorthand property part for known properties."""
    from .constants import (  # noqa
        BORDER_COLOR_CHOICES, BORDER_STYLE_CHOICES, BORDER_WIDTH_CHOICES
    )

    direction = '' if direction is None else direction + '_'
    property_validators = {
        'border_{direction}width'.format(direction=direction): BORDER_WIDTH_CHOICES,
        'border_{direction}style'.format(direction=direction): BORDER_STYLE_CHOICES,
        'border_{direction}color'.format(direction=direction): BORDER_COLOR_CHOICES,
    }

    for property_name, choices in property_validators.items():
        try:
            value = choices.validate(value)
        except (ValueError, ValidationError):
            continue

        if property_name in border_dict:
            raise ValueError('Invalid duplicated property!')

        border_dict[property_name] = value
        return border_dict

    raise ValueError('Border value "{value}" not valid!'.format(value=value))


def border(value, direction=None):
    """
    Parse border string into a dictionary of outline properties.

    The font CSS property is a shorthand for border-width, border-style, and border-color.

    Reference:
    - https://www.w3.org/TR/2011/REC-CSS2-20110607/box.html#border-properties
    """
    if value:
        if isinstance(value, str):
            values = [val.strip() for val in value.split()]
        elif isinstance(value, Sequence):
            values = value
        else:
            raise ValueError('Unknown border %s ' % value)
    else:
        raise ValueError('Unknown border %s ' % value)

    # We iteratively split by the first left hand space found and try to validate if that part
    # is a valid <border-width> or <border-style> or <border-color> (which can come in any order)

    # We use this dictionary to store parsed values and check that values properties are not
    # duplicated
    border_dict = {}
    for idx, part in enumerate(values):
        if idx > 2:
            # Border can have a maximum of 3 parts
            raise ValueError('Border property shorthand contains too many parts!')

        border_dict = _parse_border_property_part(part, border_dict, direction=direction)

    return border_dict


def border_right(value):
    """Parse border string into a dictionary of outline properties."""
    return border(value, direction='right')


def border_left(value):
    """Parse border string into a dictionary of outline properties."""
    return border(value, direction='left')


def border_bottom(value):
    """Parse border string into a dictionary of outline properties."""
    return border(value, direction='bottom')


def border_top(value):
    """Parse border string into a dictionary of outline properties."""
    return border(value, direction='top')
