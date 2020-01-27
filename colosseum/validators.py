"""
Validate values of different css properties.
"""
from collections import Sequence
import ast
import re

from . import exceptions
from . import parser
from . import units
from . import fonts
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
        validator.description = '<number>'
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
        validator.description = '<integer>'
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


is_border_spacing.description = '<length> <length>?'


def is_rect(value):
    """Check if given value is a rect shape and return it."""
    try:
        value = parser.rect(value)
    except ValueError:
        raise ValidationError('Value {value} is not a rect shape'.format(value=value))

    return value


is_rect.description = '<rect>'


# https://www.w3.org/TR/2011/REC-CSS2-20110607/syndata.html#value-def-identifier
_CSS_IDENTIFIER_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-\_]+$')


def is_font_family(values):
    """Validate that values are a valid list of font families."""
    from .constants import GENERIC_FAMILY_FONTS, INITIAL
    FontDatabase = fonts.FontDatabase

    assert isinstance(values, Sequence) and not isinstance(values, str)

    # Remove extra outer spaces
    values = [value.strip() for value in values]

    checked_values = []
    for value in values:
        # Remove extra inner spaces
        value = value.replace('" ', '"')
        value = value.replace(' "', '"')
        value = value.replace("' ", "'")
        value = value.replace(" '", "'")
        if (value.startswith('"') and value.endswith('"')
                or value.startswith("'") and value.endswith("'")):
            try:
                no_quotes_val = ast.literal_eval(value)
            except ValueError:
                raise exceptions.ValidationError

            if not FontDatabase.validate_font_family(no_quotes_val):
                raise exceptions.ValidationError('Font family "{font_value}"'
                                                 ' not found on system!'.format(font_value=no_quotes_val))
            checked_values.append(no_quotes_val)
        elif value in GENERIC_FAMILY_FONTS:
            checked_values.append(value)
        elif value in INITIAL:
            checked_values.append(value)
        else:
            error_msg = 'Font family "{font_value}" not found on system!'.format(font_value=value)
            if _CSS_IDENTIFIER_RE.match(value):
                if not FontDatabase.validate_font_family(value):
                    raise exceptions.ValidationError(error_msg)
                checked_values.append(value)
            else:
                raise exceptions.ValidationError(error_msg)

    if len(checked_values) != len(values):
        invalid = set(values) - set(checked_values)
        error_msg = 'Invalid font string "{invalid}"'.format(invalid=invalid)
        raise exceptions.ValidationError(error_msg)

    return checked_values


is_font_family.description = '<family-name>, <generic-family>'
