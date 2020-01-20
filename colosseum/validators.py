"""
Validate values of different css properties.
"""

from . import parser
from . import shapes
from . import units
from .exceptions import ValidationError


def _numeric_validator(num_value, numeric_type, min_value, max_value):
    try:
        num_value = numeric_type(num_value)
    except (ValueError, TypeError):
        error_msg = "Cannot coerce {num_value} to {numeric_type}".format(
            num_value=num_value, numeric_type=numeric_type.__name__)
        raise ValidationError(error_msg)

    if min_value is not None and num_value < min_value:
        error_msg = 'Value {num_value} below minimum value {min_value}'.format(
            num_value=num_value, min_value=min_value)
        raise ValidationError(error_msg)

    if max_value is not None and num_value > max_value:
        error_msg = 'Value {num_value} above maximum value {max_value}'.format(
            num_value=num_value, max_value=max_value)
        raise ValidationError(error_msg)

    return num_value


def is_number(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid float.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(num_value=num_value, numeric_type=float, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_number.description = '<number>'


def is_integer(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid integer.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(num_value=num_value, numeric_type=int, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_integer.description = '<integer>'


def is_length(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_length.description = '<length>'


def is_percentage(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    if not isinstance(value, units.Percent):
        error_msg = 'Value {value} is not a Percent unit'.format(value=value)
        raise ValidationError(error_msg)

    return value


is_percentage.description = '<percentage>'


def is_color(value):
    try:
        value = parser.color(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_color.description = '<color>'


def is_shape(value):
    """Check if given value is a shape."""
    try:
        # Remove extra outer  spaces
        value = value.strip()

        if value.startswith('rect'):
            value = value.replace('rect(', '').replace(')', '')

            # Remove extra inner spaces
            value = ' '.join(value.split()).strip()

            if ',' in value and value.count(',') == 3:
                values = value.split(',')
                return shapes.Rect(*values)

            if ',' not in value and value.count(' ') == 3:
                values = value.split(' ')
                return shapes.Rect(*values)

        raise ValidationError('Unknown shape %s' % value)
    except ValueError:
        raise ValidationError('Unknown shape %s' % value)


is_shape.description = '<shape>'
