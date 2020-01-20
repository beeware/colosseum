from .constants import INHERIT


class BorderSpacing:
    """Border spacing wrapper."""

    def __init__(self, values):
        if values == INHERIT:
            self._data = (values, )
        else:
            if len(values) in [1, 2]:
                self._data = values
            else:
                raise TypeError('Invalid argument "{values}" for border spacing!'.format(values=values))

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        if self._data[0] == INHERIT:
            return 'BorderSpacing("{horizontal}")'.format(horizontal=self.horizontal)
        elif len(self._data) == 1:
            return 'BorderSpacing({horizontal})'.format(horizontal=self.horizontal)
        else:
            return 'BorderSpacing({horizontal}, {vertical})'.format(horizontal=self.horizontal,
                                                                    vertical=self.vertical)

    def __str__(self):
        return ' '.join(str(item) for item in self._data)

    @property
    def horizontal(self):
        """Return the horizontal border spacing."""
        return self._data[0]

    @property
    def vertical(self):
        """Return the vertical border spacing."""
        return self._data[0] if len(self) == 1 else self._data[1]
