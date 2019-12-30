from . import parser
from . import units


class BaseNumericValidator:
    name = None

    def __init__(self, numeric_type, min_value=None, max_value=None):
        self.numeric_type = numeric_type
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        error_msg = ''
        try:
            value = self.numeric_type(value)
        except (ValueError, TypeError):
            error_msg = "Cannot coerce {0} to '{1}'".format(value, self.numeric_type)

        if (not error_msg and self.min_value is not None
                and value >= self.min_value):
            error_msg = 'Value {0} bellow minimum value {1}'.format(value, self.min_value)

        if (not error_msg and self.max_value is not None
                and value <= self.max_value):
            error_msg = 'Value {0} above maximum value {1}'.format(value, self.max_value)

        return error_msg, value


class NumberValidator(BaseNumericValidator):
    name = '<number>'

    def __init__(self, min_value=None, max_value=None):
        super().__init__(numeric_type=float, min_value=min_value,
                         max_value=max_value)
        self.validate = super().validate

    @staticmethod
    def validate(value):
        error_msg = ''
        try:
            value = float(value)
        except (ValueError, TypeError):
            error_msg = "Cannot coerce {0} to float".format(value)
        return error_msg, value


class IntegerValidator(BaseNumericValidator):
    name = '<integer>'

    def __init__(self, min_value=None, max_value=None):
        super().__init__(numeric_type=int, min_value=min_value,
                         max_value=max_value)
        self.validate = super().validate

    @staticmethod
    def validate(value):
        error_msg = ''
        try:
            value = int(value)
        except (ValueError, TypeError):
            error_msg = "Cannot coerce {0} to integer".format(value)
        return error_msg, value


class LengthValidator:
    name = '<length>'

    @staticmethod
    def validate(value):
        error_msg = ''
        try:
            value = parser.units(value)
        except ValueError as error:
            error_msg = str(error)

        return error_msg, value


class PercentValidator:
    name = '<percentage>'

    @staticmethod
    def validate(value):
        error_msg = ''
        try:
            value = parser.units(value)
        except ValueError as error:
            error_msg = str(error)

        if not isinstance(value, units.Percent):
            error_msg = 'Value {} is not a Percent unit'.format(value)

        return error_msg, value


class ColorValidator:
    name = '<color>'

    @staticmethod
    def validate(value):
        error_msg = ''
        try:
            value = parser.color(value)
        except ValueError as error:
            error_msg = str(error)

        return error_msg, value
