from ast import literal_eval
from collections import Sequence

from .colors import NAMED_COLOR, hsl, rgb
from .exceptions import ValidationError
from .shapes import Rect
from .units import Unit, px
from .wrappers import BorderSpacing, Cursor, Quotes, Uri


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


##############################################################################
# Uri
##############################################################################
def uri(value):
    """Parse a url from a value.

    Accepts:
    * url("<url>")
    * url( "<url>" )
    * url('<url>')
    * url( '<url>' )
    * url(<url>)
    * url( <url> )
    """
    if isinstance(value, str):
        value = value.strip()
    else:
        raise ValueError('Value {value} must be a string')

    if value.startswith('url(') and value.endswith(')'):
        # Remove the url word
        value = value[3:]

        # Single quotes and optional spaces
        if value.startswith("('") and value.endswith("')"):
            # "('some.url')"
            return Uri(value[2:-2])
        elif value.startswith("( '") and value.endswith("')"):
            # "( 'some.url')"
            return Uri(value[3:-2])
        elif value.startswith("('") and value.endswith("' )"):
            # "('some.url' )"
            return Uri(value[2:-3])
        elif value.startswith("( '") and value.endswith("' )"):
            # "( 'some.url' )"
            return Uri(value[3:-3])
        # Double quotes and optional spaces
        elif value.startswith('("') and value.endswith('")'):
            # '("some.url")'
            return Uri(value[2:-2])
        elif value.startswith('( "') and value.endswith('")'):
            # '( "some.url")'
            return Uri(value[3:-2])
        elif value.startswith('("') and value.endswith('" )'):
            # '("some.url" )'
            return Uri(value[2:-3])
        elif value.startswith('( "') and value.endswith('" )'):
            # '( "some.url" )'
            return Uri(value[3:-3].strip())
        # No quotes and optional spaces
        elif value.startswith('( ') and value.endswith(' )'):
            # '( some.url )'
            value = value[2:-2]
            if value != value.strip():
                raise ValueError('Invalid url %s' % value)

            return Uri(value)
        elif value.startswith('( ') and value.endswith(')'):
            # '( some.url)'
            value = value[2:-1]
            if value != value.strip() or value[-1] in ['"', "'"] or value[0] in ['"', "'"]:
                raise ValueError('Invalid url %s' % value)

            return Uri(value)
        elif value.startswith('(') and value.endswith(' )'):
            # '(some.url )'
            value = value[1:-2]
            if value != value.strip() or value[-1] in ['"', "'"] or value[0] in ['"', "'"]:
                raise ValueError('Invalid url %s' % value)

            return Uri(value)
        elif value[1:-1] == value[1:-1].strip():
            # '(some.url)'
            value = value[1:-1]

            # Some characters appearing in an unquoted URI, such as parentheses, white space characters,
            # single quotes (') and double quotes ("), must be escaped with a backslash so that the
            # resulting URI value is a URI token: '\(', '\)'
            escape_chars = ['(', ')', ' ', "'", '"']
            for char in escape_chars:
                if char in value and '\{char}'.format(char=char) not in value:
                    raise ValueError('Invalid url %s' % value)

            return Uri(value)

    raise ValueError('Invalid url %s' % value)



##############################################################################
# Cursor
##############################################################################
def cursor(values):
    """Parse a cursor from a value."""
    from .constants import CURSOR_OPTIONS

    if isinstance(values, str):
        values = [val.strip() for val in values.split(',')]

    validated_values = []
    has_cursor_option = False
    option_count = 0
    for value in values:
        if value in CURSOR_OPTIONS:
            has_cursor_option = True
            validated_values.append(value)
            option_count += 1

            if option_count > 1:
                raise ValueError('There can only be one cursor option in {values}!'.format(values=values))

            continue
        else:
            if has_cursor_option:
                raise ValueError('Values {values} are in incorrect order. '
                                 'Cursor option must come last!'.format(values=values))
            try:
                value = uri(value)
                validated_values.append(value)
                continue
            except ValueError:
                raise ValueError('Value {value} is not a valid url value'.format(value=value))

        raise ValueError('Value {value} is not a valid cursor value'.format(value=value))

    return Cursor(validated_values)
