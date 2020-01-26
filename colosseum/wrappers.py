from collections import Sequence


class BorderSpacing:
    """
    Border spacing wrapper.

    Examples:
        BorderSpacing(1px)
        BorderSpacing(1px, 2px)
    """

    def __init__(self, horizontal, vertical=None):
        if isinstance(horizontal, Sequence) and not isinstance(horizontal, str):
            raise TypeError('Invalid argument type for "horizontal"')

        if isinstance(vertical, Sequence) and not isinstance(vertical, str):
            raise TypeError('Invalid argument type for "vertical"')

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
