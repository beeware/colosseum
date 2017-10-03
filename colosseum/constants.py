from . import color


class Choices:
    "A class to define allowable data types for a property"
    def __init__(self, *constants, length=False, percentage=False, integer=False, color=False):
        self.constants = set(constants)
        self.length = length
        self.percentage = percentage
        self.integer = integer
        self.color = color

    def is_valid(self, value):
        if hasattr(value, 'px'):
            if self.length:
                return True
            if self.percentage and value.suffix == '%':
                return True
            return False
        if isinstance(value, int) and (self.length or self.integer):
            return True
        if self.color and (hasattr(value, 'rgb') or value in color.NAMED_COLOR):
            return True
        if value in self.constants:
            return True
        return False

    def __str__(self):
        choices = [str(c).lower().replace('_', '-') for c in self.constants]
        if self.length:
            choices.append("<length>")
        if self.percentage:
            choices.append("<percentage>")
        if self.integer:
            choices.append("<integer>")
        if self.color:
            choices.append("<color>")
        return ", ".join(sorted(choices))


######################################################################
# Common constants
######################################################################

AUTO = 'auto'

TRANSPARENT = 'transparent'

######################################################################
# Margins
######################################################################

MARGIN_CHOICES = Choices(AUTO, length=True, percentage=True)

######################################################################
# Padding
######################################################################

PADDING_CHOICES = Choices(length=True, percentage=True)

######################################################################
# Borders
######################################################################

THIN = 'thin'
MEDIUM = 'medium'
THICK = 'thick'

BORDER_WIDTH_CHOICES = Choices(THIN, MEDIUM, THICK, length=True)

HIDDEN = 'hidden'
DOTTED = 'dotted'
DASHED = 'dashed'
SOLID = 'solid'
DOUBLE = 'double'
GROOVE = 'groove'
RIDGE = 'ridge'
INSET = 'inset'
OUTSET = 'outset'

BORDER_STYLE_CHOICES = Choices(
    None,
    HIDDEN,
    DOTTED,
    DASHED,
    SOLID,
    DOUBLE,
    GROOVE,
    RIDGE,
    INSET,
    OUTSET,
)

BORDER_COLOR_CHOICES = Choices(TRANSPARENT, color=True)

######################################################################
# Display
######################################################################

INLINE = 'inline'
BLOCK = 'block'
LIST_ITEM = 'list-item'
INLINE_BLOCK = 'inline-block'
TABLE = 'table'
INLINE_TABLE = 'inline-table'
TABLE_ROW_GROUP = 'table-row-group'
TABLE_HEADER_GROUP = 'table-header-group'
TABLE_FOOTER_GROUP = 'table-footer-group'
TABLE_ROW = 'table-row'
TABLE_COLUMN_GROUP = 'table-column-group'
TABLE_COLUMN = 'table-column'
TABLE_CELL = 'table-cell'
TABLE_CAPTION = 'table-caption'

DISPLAY_CHOICES = Choices(
    None,
    INLINE,
    BLOCK,
    LIST_ITEM,
    INLINE_BLOCK,
    TABLE,
    INLINE_TABLE,
    TABLE_ROW_GROUP,
    TABLE_HEADER_GROUP,
    TABLE_FOOTER_GROUP,
    TABLE_ROW,
    TABLE_COLUMN_GROUP,
    TABLE_COLUMN,
    TABLE_CELL,
    TABLE_CAPTION,
)

######################################################################
# Position
######################################################################

STATIC = 'static'
RELATIVE = 'relative'
ABSOLUTE = 'absolute'
FIXED = 'fixed'

POSITION_CHOICES = Choices(STATIC, RELATIVE, ABSOLUTE, FIXED)

BOX_OFFSET_CHOICES = Choices(AUTO, length=True, percentage=True)

######################################################################
# Float
######################################################################

LEFT = 'left'
RIGHT = 'right'
BOTH = 'both'

FLOAT_CHOICES = Choices(LEFT, RIGHT, None)
CLEAR_CHOICES = Choices(None, LEFT, RIGHT, BOTH)

######################################################################
# Layers
######################################################################

Z_INDEX_CHOICES = Choices(AUTO, integer=True)

######################################################################
# Direction
######################################################################

RTL = 'rtl'
LTR = 'ltr'

DIRECTION_CHOICES = Choices(RTL, LTR)

NORMAL = 'normal'
EMBED = 'embed'
BIDI_OVERRIDE = 'bidi-override'

UNICODE_BIDI_CHOICES = Choices(NORMAL, EMBED, BIDI_OVERRIDE)

######################################################################
# Sizes
######################################################################

SIZE_CHOICES = Choices(AUTO, length=True, percentage=True)
MIN_SIZE_CHOICES = Choices(length=True, percentage=True)
MAX_SIZE_CHOICES = Choices(None, length=True, percentage=True)
