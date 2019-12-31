from . import parser
from . import units


def _numeric_validator(value, numeric_type, min_value, max_value):
    error_msg = ''
    try:
        value = numeric_type(value)
    except (ValueError, TypeError):
        error_msg = "Cannot coerce {value} to {numeric_type}".format(
            value=value, numeric_type=numeric_type.__name__)

    if not error_msg and min_value is not None and value < min_value:
        error_msg = 'Value {value} bellow minimum value {min_value}'.format(
            value, min_value)

    if not error_msg and max_value is not None and value > max_value:
        error_msg = 'Value {value} above maximum value {max_value}'.format(
            value, max_value)

    return error_msg, value


def is_number(value, min_value=None, max_value=None):
    """
    Validate that value is a valid float.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(value):
        return _numeric_validator(value, numeric_type=float, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_number.description = '<number>'


def is_integer(value, min_value=None, max_value=None):
    """
    Validate that value is a valid integer.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(value):
        return _numeric_validator(value, numeric_type=int, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_integer.description = '<integer>'


def is_length(value):
    error_msg = ''
    try:
        value = parser.units(value)
    except ValueError as error:
        error_msg = str(error)

    return error_msg, value


is_length.description = '<length>'


def is_percentage(value):
    error_msg = ''
    try:
        value = parser.units(value)
    except ValueError as error:
        error_msg = str(error)

    if not isinstance(value, units.Percent):
        error_msg = 'Value {value} is not a Percent unit'.format(value=value)

    return error_msg, value


is_percentage.description = '<percentage>'


def is_color(value):
    error_msg = ''
    try:
        value = parser.color(value)
    except ValueError as error:
        error_msg = str(error)

    return error_msg, value


is_color.description = '<color>'
