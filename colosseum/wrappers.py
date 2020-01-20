from collections.abc import Sequence


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
