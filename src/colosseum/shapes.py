class Rect:
    """Representation of a rectangular shape."""

    def __init__(self, top, right, left, bottom):
        self._top = top
        self._right = right
        self._left = left
        self._bottom = bottom

    def __eq__(self, other):
        return (
            other.__class__ == self.__class__
            and other._top == self._top
            and other._right == self._right
            and other._left == self._left
            and other._bottom == self._bottom
        )

    def __repr__(self):
        return f"rect({self._top}, {self._right}, {self._left}, {self._bottom})"

    def __str__(self):
        return repr(self)

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
