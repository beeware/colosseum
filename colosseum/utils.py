from __future__ import print_function, absolute_import, division, unicode_literals

from .constants import *


def leading(axis):
    "Return the dimension attribute for leading space corresponding to the given axis"
    return TOP if axis == COLUMN else LEFT


def trailing(axis):
    "Return the dimension attribute for trailing space corresponding to the given axis"
    return BOTTOM if axis == COLUMN else RIGHT


def position(axis):
    "Return the position attribute corresponding to the given axis"
    return TOP if axis == COLUMN else LEFT


def dimension(axis):
    "Return the size dimension attribute corresponding to the given axis"
    return HEIGHT if axis == COLUMN else WIDTH
