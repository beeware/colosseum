
AUTO = 'auto'

######################################################################
# Borders
######################################################################

HIDDEN = 'hidden'
DOTTED = 'dotted'
DASHED = 'dashed'
SOLID = 'solid'
DOUBLE = 'double'
GROOVE = 'groove'
RIDGE = 'ridge'
INSET = 'inset'
OUTSET = 'outset'

BORDER_STYLES = {
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
}

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

DISPLAY_CHOICES = {
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
}

######################################################################
# Position
######################################################################

STATIC = 'static'
RELATIVE = 'relative'
ABSOLUTE = 'absolute'
FIXED = 'fixed'

POSITION_CHOICES = { STATIC, RELATIVE, ABSOLUTE, FIXED }

######################################################################
# Direction
######################################################################

RTL = 'rtl'
LTR = 'ltr'

DIRECTION_CHOICES = { RTL, LTR }

NORMAL = 'normal'
EMBED = 'embed'
BIDI_OVERRIDE = 'bidi-override'

UNICODE_BIDI_CHOICES = { NORMAL, EMBED, BIDI_OVERRIDE }

######################################################################
# Float
######################################################################

LEFT = 'left'
RIGHT = 'right'
BOTH = 'both'

FLOAT_CHOICES = { LEFT, RIGHT, None }
CLEAR_CHOICES = { None, LEFT, RIGHT, BOTH }
