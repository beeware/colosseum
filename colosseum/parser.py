from .colors import Color, NAMED_COLOR, hsl, rgb
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
