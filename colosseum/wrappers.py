from collections import OrderedDict


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
