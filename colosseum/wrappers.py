from abc import ABC


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


class Shorthand(ABC):
    """Dictionary-like wrapper to hold shorthand data."""
    VALID_KEYS = []

    def __init__(self, **kwargs):
        if self.VALID_KEYS:
            for key in kwargs:
                if key not in self.VALID_KEYS:
                    raise ValueError('Invalid key "{key}". Valid keys are {keys}'.format(key=key,
                                                                                         keys=self.VALID_KEYS))
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
            if key in map_copy:
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
        return sorted(self._map.keys())

    def items(self):
        return sorted(self._map.items())

    def copy(self):
        return self.__class__(**self._map)

    def to_dict(self):
        return self._map.copy()


class Outline(Shorthand):
    """Dictionary-like wrapper to hold outline shorthand property."""
    VALID_KEYS = ['outline_color', 'outline_style', 'outline_width']

    def __str__(self):
        parts = []
        for key in self.VALID_KEYS:
            if key in self._map:
                parts.append(str(self._map[key]))

        return ' '.join(parts)