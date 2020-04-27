from collections import OrderedDict
from collections.abc import Sequence


class BorderSpacing:
    """
    Border spacing wrapper.

    Examples:
        BorderSpacing(1px)
        BorderSpacing(1px, 2px)
    """

    def __init__(self, horizontal, vertical=None):
        self._horizontal = horizontal
        self._vertical = vertical

    def __repr__(self):
        if self._vertical is None:
            string = 'BorderSpacing({horizontal})'.format(horizontal=repr(self._horizontal))
        else:
            string = 'BorderSpacing({horizontal}, {vertical})'.format(horizontal=repr(self._horizontal),
                                                                      vertical=repr(self._vertical))
        return string

    def __str__(self):
        if self._vertical is not None:
            string = '{horizontal} {vertical}'.format(horizontal=self._horizontal,
                                                      vertical=self._vertical)
        else:
            string = '{horizontal}'.format(horizontal=self._horizontal)

        return string

    @property
    def horizontal(self):
        """Return the horizontal border spacing."""
        return self._horizontal

    @property
    def vertical(self):
        """Return the vertical border spacing."""
        return self._horizontal if self._vertical is None else self._vertical


class ImmutableList(Sequence):
    """
    Immutable list to store list properties like outline and font family.
    """

    def __init__(self, iterable=()):
        self._data = tuple(iterable)

    def _get_error_message(self, err):
        return str(err).replace('tuple', self.__class__.__name__, 1)

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self._data == other._data

    def __getitem__(self, index):
        try:
            return self._data[index]
        except Exception as err:
            error_msg = self._get_error_message(err)
            raise err.__class__(error_msg)

    def __len__(self):
        return len(self._data)

    def __hash__(self):
        return hash((self.__class__.__name__, self._data))

    def __repr__(self):
        class_name = self.__class__.__name__
        if len(self._data) > 1:
            text = '{class_name}([{data}])'.format(data=str(self._data)[1:-1], class_name=class_name)
        elif len(self._data) == 1:
            text = '{class_name}([{data}])'.format(data=str(self._data)[1:-2], class_name=class_name)
        else:
            text = '{class_name}()'.format(class_name=class_name)
        return text

    def __str__(self):
        return repr(self)

    def copy(self):
        return self.__class__(self._data)


class FontFamily(ImmutableList):
    """Immutable list like wrapper to store font families."""

    def __init__(self, iterable=()):
        try:
            super().__init__(iterable)
        except Exception as err:
            error_msg = self._get_error_message(err)
            raise err.__class__(error_msg)
        self._check_values(list(iterable))

    def _check_values(self, values):
        if not isinstance(values, list):
            values = [values]

        for value in values:
            if not isinstance(value, str):
                raise TypeError('Invalid argument for font family')

    def __str__(self):
        items = []
        for item in self._data:
            if ' ' in item:
                item = '"{item}"'.format(item=item)
            items.append(item)
        return ', '.join(items)


class Shorthand:
    """
    Dictionary-like wrapper to hold shorthand data.

    This class is not iterable and should be subclassed
    """
    VALID_KEYS = []

    def __init__(self, **kwargs):
        self._map = kwargs

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self._map == other._map

    def __setitem__(self, key, value):
        if self.VALID_KEYS:
            if key in self.VALID_KEYS:
                self._map[key] = value
            else:
                raise KeyError('Valid keys are: {keys}'.format(keys=self.VALID_KEYS))
        else:
            self._map[key] = value

    def __getitem__(self, key):
        if self.VALID_KEYS:
            if key in self.VALID_KEYS:
                return self._map[key]
        else:
            return self._map[key]

        raise KeyError('Valid keys are: {keys}'.format(keys=self.VALID_KEYS))

    def __repr__(self):
        map_copy = self._map.copy()
        items = []
        for key in self.VALID_KEYS:
            items.append("{key}={value}".format(key=key, value=repr(map_copy[key])))

        class_name = self.__class__.__name__
        string = "{class_name}({items})".format(class_name=class_name, items=', '.join(items))
        return string.format(**map_copy)

    def __len__(self):
        return len(self._map)

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.VALID_KEYS) if self.VALID_KEYS else iter(self._map)

    def keys(self):
        return self._map.keys()

    def items(self):
        return self._map.items()

    def copy(self):
        return self.__class__(**self._map)

    def to_dict(self):
        return self._map.copy()


class FontShorthand(Shorthand):
    """Dictionary-like wrapper to hold font shorthand property."""
    VALID_KEYS = ['font_style', 'font_variant', 'font_weight', 'font_size', 'line_height', 'font_family']

    def __init__(self, font_style='normal', font_variant='normal', font_weight='normal',
                 font_size='medium', line_height='normal', font_family=FontFamily(['initial'])):
        super().__init__(
            font_style=font_style, font_variant=font_variant, font_weight=font_weight,
            font_size=font_size, line_height=line_height, font_family=font_family,
        )

    def __str__(self):
        string = '{font_style} {font_variant} {font_weight} {font_size}/{line_height} {font_family}'
        return string.format(**self._map)
class Quotes:
    """
    Content opening and closing quotes wrapper.

    Examples:
        Quotes([('<', '>')])
        Quotes([('<', '>'), ('{', '}')])
        Quotes([('<', '>'), ('{', '}'), ('[', ']')])
    """
    def __init__(self, values):
        self._quotes = values

    def __repr__(self):
        return 'Quotes({values})'.format(values=self._quotes)

    def __str__(self):
        quotes = []
        for start, end in self._quotes:
            quotes.append(repr(start))
            quotes.append(repr(end))

        return ' '.join(val for val in quotes)

    def __len__(self):
        return len(self._quotes)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._quotes == other._quotes

    def opening(self, level):
        """Return the opening quote for the given level."""
        try:
            return self._quotes[level][0]
        except IndexError:
            raise IndexError('Quotes level out of range')

    def closing(self, level):
        """Return the opening quote for the given level."""
        try:
            return self._quotes[level][-1]
        except IndexError:
            raise IndexError('Quotes level out of range')


class Shorthand:
    VALID_KEYS = []

    def __init__(self, **kwargs):
        if self.VALID_KEYS:
            for key in kwargs:
                if key not in self.VALID_KEYS:
                    raise ValueError('Invalid key "{key}". Valid keys are {keys}'.format(key=key,
                                                                                         keys=self.VALID_KEYS))
                setattr(self, key, kwargs[key])
        else:
            raise ValueError('Shorthand must define `VALID_KEYS`')

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.to_dict() == other.to_dict()

    def __repr__(self):
        items = []
        properties = self.to_dict()
        for key, value in properties.items():
            items.append("{key}={value}".format(key=key, value=repr(value)))

        class_name = self.__class__.__name__
        string = "{class_name}({items})".format(class_name=class_name, items=', '.join(items))
        return string.format(**properties)

    def __str__(self):
        parts = []
        for key, value in self.to_dict().items():
            parts.append(str(value))

        return ' '.join(parts)

    def to_dict(self):
        """Return dictionary of the defined properties."""
        properties = OrderedDict()
        for key in self.VALID_KEYS:
            if key in self.__dict__:
                properties[key] = self.__dict__[key]

        return properties


class Outline(Shorthand):
    VALID_KEYS = ['outline_color', 'outline_style', 'outline_width']


class BorderTop(Shorthand):
    VALID_KEYS = ['border_top_width', 'border_top_style', 'border_top_color']


class BorderRight(Shorthand):
    VALID_KEYS = ['border_right_width', 'border_right_style', 'border_right_color']


class BorderBottom(Shorthand):
    VALID_KEYS = ['border_bottom_width', 'border_bottom_style', 'border_bottom_color']


class BorderLeft(Shorthand):
    VALID_KEYS = ['border_left_width', 'border_left_style', 'border_left_color']


class Border(Shorthand):
    VALID_KEYS = ['border_width', 'border_style', 'border_color']
