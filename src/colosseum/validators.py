"""
Validate values of different css properties.
"""

import re

from . import parser, units
from .exceptions import ValidationError


def _numeric_validator(num_value, numeric_type, min_value, max_value):
    try:
        num_value = numeric_type(num_value)
    except (ValueError, TypeError):
        error_msg = "Cannot coerce {num_value} to {numeric_type}".format(
            num_value=num_value, numeric_type=numeric_type.__name__
        )
        raise ValidationError(error_msg)

    if min_value is not None and num_value < min_value:
        error_msg = "Value {num_value} below minimum value {min_value}".format(
            num_value=num_value, min_value=min_value
        )
        raise ValidationError(error_msg)

    if max_value is not None and num_value > max_value:
        error_msg = "Value {num_value} above maximum value {max_value}".format(
            num_value=num_value, max_value=max_value
        )
        raise ValidationError(error_msg)

    return num_value


def is_number(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid float.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(
            num_value=num_value,
            numeric_type=float,
            min_value=min_value,
            max_value=max_value,
        )

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_number.description = "<number>"


def is_integer(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid integer.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(
            num_value=num_value,
            numeric_type=int,
            min_value=min_value,
            max_value=max_value,
        )

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_integer.description = "<integer>"


def is_length(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_length.description = "<length>"


def is_percentage(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    if not isinstance(value, units.Percent):
        error_msg = f"Value {value} is not a Percent unit"
        raise ValidationError(error_msg)

    if value < units.Percent(0):
        error_msg = f"Value {value} can not negative"
        raise ValidationError(error_msg)

    return value


is_percentage.description = "<percentage>"


def is_color(value):
    try:
        value = parser.color(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_color.description = "<color>"


def is_border_spacing(value):
    """
    Check if value is corresponds to a border spacing.

    <length> <length>?
    """
    try:
        value = parser.border_spacing(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_border_spacing.description = "<length> <length>?"


def is_rect(value):
    """Check if given value is a rect shape and return it."""
    try:
        value = parser.rect(value)
    except ValueError:
        raise ValidationError(f"Value {value} is not a rect shape")

    return value


is_rect.description = "<rect>"


def is_quote(value):
    """Check if given value is of content quotes and return it."""
    try:
        value = parser.quotes(value)
    except ValueError:
        raise ValidationError(f"Value {value} is not a valid quote")

    return value


is_quote.description = "[<string> <string>]+"


URI_RE = re.compile(
    r"""(
    (?:url\(\s?'[A-Za-z0-9\./\:\?]*'\s?\))  # Single quotes and optional spaces
    |
    (?:url\(\s?"[A-Za-z0-9\./\:\?]*"\s?\))  # Double quotes and optional spaces
    |
    (?:url\(\s?[A-Za-z0-9\./\:\?]*\s?\))    # No quotes and optional spaces
)""",
    re.VERBOSE,
)


def is_uri(value):
    """Validate value is <uri>."""
    try:
        value = parser.uri(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_uri.description = "<uri>"


def is_cursor(value):
    """
    Validate if values are correct cursor values and in correct order and quantity.

    This validator returns a list.
    """
    try:
        value = parser.cursor(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_cursor.description = (
    "[ [<uri> ,]* [ auto | crosshair | default | pointer | move | e-resize "
    "| ne-resize | nw-resize | n-resize | se-resize | sw-resize | s-resize "
    "| w-resize | text | wait | help | progress ] ]"
)
