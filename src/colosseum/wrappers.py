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
            string = f"BorderSpacing({repr(self._horizontal)})"
        else:
            string = "BorderSpacing({horizontal}, {vertical})".format(
                horizontal=repr(self._horizontal), vertical=repr(self._vertical)
            )
        return string

    def __str__(self):
        if self._vertical is not None:
            string = f"{self._horizontal} {self._vertical}"
        else:
            string = f"{self._horizontal}"

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
        return f"Quotes({self._quotes})"

    def __str__(self):
        quotes = []
        for start, end in self._quotes:
            quotes.append(repr(start))
            quotes.append(repr(end))

        return " ".join(val for val in quotes)

    def __len__(self):
        return len(self._quotes)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._quotes == other._quotes

    def opening(self, level):
        """Return the opening quote for the given level."""
        try:
            return self._quotes[level][0]
        except IndexError:
            raise IndexError("Quotes level out of range")

    def closing(self, level):
        """Return the opening quote for the given level."""
        try:
            return self._quotes[level][-1]
        except IndexError:
            raise IndexError("Quotes level out of range")


class Shorthand:
    VALID_KEYS = []

    def __init__(self, **kwargs):
        if self.VALID_KEYS:
            for key in kwargs:
                if key not in self.VALID_KEYS:
                    raise ValueError(f'Invalid key "{key}". Valid keys are {self.VALID_KEYS}')
                setattr(self, key, kwargs[key])
        else:
            raise ValueError("Shorthand must define `VALID_KEYS`")

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.to_dict() == other.to_dict()

    def __repr__(self):
        items = []
        properties = self.to_dict()
        for key, value in properties.items():
            items.append(f"{key}={repr(value)}")

        class_name = self.__class__.__name__
        string = "{class_name}({items})".format(class_name=class_name, items=", ".join(items))
        return string.format(**properties)

    def __str__(self):
        parts = []
        for key, value in self.to_dict().items():
            parts.append(str(value))

        return " ".join(parts)

    def to_dict(self):
        """Return dictionary of the defined properties."""
        properties = OrderedDict()
        for key in self.VALID_KEYS:
            if key in self.__dict__:
                properties[key] = self.__dict__[key]

        return properties


class Outline(Shorthand):
    VALID_KEYS = ["outline_color", "outline_style", "outline_width"]


class BorderTop(Shorthand):
    VALID_KEYS = ["border_top_width", "border_top_style", "border_top_color"]


class BorderRight(Shorthand):
    VALID_KEYS = ["border_right_width", "border_right_style", "border_right_color"]


class BorderBottom(Shorthand):
    VALID_KEYS = ["border_bottom_width", "border_bottom_style", "border_bottom_color"]


class BorderLeft(Shorthand):
    VALID_KEYS = ["border_left_width", "border_left_style", "border_left_color"]


class Border(Shorthand):
    VALID_KEYS = ["border_width", "border_style", "border_color"]


class Uri:
    """Wrapper for a url."""

    def __init__(self, url):
        self._url = url

    def __repr__(self):
        return 'url("%s")' % self._url

    def __str__(self):
        return repr(self)

    @property
    def url(self):
        return self._url


class ImmutableList(list):
    """Immutable list to store list properties."""

    def __init__(self, iterable=()):
        super().__init__(iterable)

    def _get_error_message(self, err):
        return str(err).replace("list", self.__class__.__name__, 1)

    # def __eq__(self, other):
    #     return other.__class__ == self.__class__ and self == other

    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except Exception as err:
            error_msg = self._get_error_message(err)
            raise err.__class__(error_msg)

    def __setitem__(self, index, value):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def __hash__(self):
        return hash((self.__class__.__name__, tuple(self)))

    def __repr__(self):
        class_name = self.__class__.__name__
        if len(self) != 0:
            text = f"{class_name}([{repr(list(self))[1:-1]}])"
        else:
            text = f"{class_name}()"

        return text

    def __str__(self):
        return ", ".join(str(v) for v in self)

    def copy(self):
        return self.__class__(self)

    # Disable mutating methods
    def append(self, object):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def extend(self, iterable):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def insert(self, index, object):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def pop(self, index=None):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def remove(self, value):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def reverse(self):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")

    def sort(self, cmp=None, key=None, reverse=False):
        raise TypeError(f"{self.__class__.__name__} values cannot be changed!")


class Cursor(ImmutableList):
    """Immutable list to store cursor property."""
