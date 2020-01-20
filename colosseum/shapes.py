from .parser import units


class Rect:
    """Representation of a rectangular shape."""

    def __init__(self, top, right, left, bottom):
        self._top = units(top)
        self._right = units(right)
        self._left = units(left)
        self._bottom = units(bottom)

    def __eq__(self, other):
        return other.__class__ == self.__class__ and other.to_tuple() == self.to_tuple()

    def __repr__(self):
        return 'rect({top}, {right}, {left}, {bottom})'.format(
            top=self._top, right=self._right, left=self._left, bottom=self._bottom
        )

    def __str__(self):
        return repr(self)

    def to_tuple(self):
        return self._top, self._right, self._left, self._bottom

    @property
    def top(self):
        return self._top

    @property
    def right(self):
        return self._right

    @property
    def left(self):
        return self._left

    @property
    def bottom(self):
        return self._bottom
