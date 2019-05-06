from . import units
from . import colors
from . import parser


class Choices:
    "A class to define allowable data types for a property"
    def __init__(
            self, *constants, length=False, percentage=False,
            integer=False, number=False, color=False,
            explicit_defaulting_constants=None):
        self.constants = set(constants)
        self.explicit_defaulting_constants = explicit_defaulting_constants or []
        self.length = length
        self.percentage = percentage
        self.integer = integer
        self.number = number
        self.color = color

    def validate(self, value):
        if self.length or self.percentage:
            try:
                val = parser.units(value)
                if self.length:
                    return val
                elif self.percentage and isinstance(val, units.Percent):
                    return val
            except ValueError:
                pass
        if self.integer:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        if self.number:
            try:
                return float(value)
            except (ValueError, TypeError):
                pass
        if self.color:
            try:
                return parser.color(value)
            except ValueError:
                pass
        if value == 'none':
            value = None
        for const in self.constants:
            if value == const:
                return const
        for const in self.explicit_defaulting_constants:
            if value == const:
                return const

        raise ValueError()

    def __str__(self):
        choices = [str(c).lower().replace('_', '-') for c in self.constants]
        if self.length:
            choices.append("<length>")
        if self.percentage:
            choices.append("<percentage>")
        if self.integer:
            choices.append("<integer>")
        if self.number:
            choices.append("<number>")
        if self.color:
            choices.append("<color>")
        if self.explicit_defaulting_constants:
            for item in self.explicit_defaulting_constants:
                choices.append(item)
        return ", ".join(sorted(choices))

######################################################################
# Standard versions
######################################################################
HTML4 = 'html4'
HTML5 = 'html5'

######################################################################
# Common constants
######################################################################

AUTO = 'auto'
COLUMN = 'column'
ROW = 'row'
TRANSPARENT = 'transparent'

######################################################################
# Explicit defaulting constants
######################################################################

INITIAL = 'initial'
INHERIT = 'inherit'
UNSET = 'unset'
REVERT = 'revert'

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

BORDER_COLOR_CHOICES = Choices(TRANSPARENT, color=True,
                               explicit_defaulting_constants=[INITIAL, INHERIT, UNSET, REVERT])

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

# CSS Flexbox
FLEX = 'flex'
INLINE_FLEX = 'inline-flex'

# CSS Grid
GRID = 'grid'
INLINE_GRID = 'inline-grid'

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

    FLEX,
    INLINE_FLEX,

    GRID,
    INLINE_GRID,
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
MIN_SIZE_CHOICES = Choices(AUTO, length=True, percentage=True)
MAX_SIZE_CHOICES = Choices(None, length=True, percentage=True)

######################################################################
# Flex flow (CSS-flexbox-1, Section 5)
######################################################################

ROW_REVERSE = 'row-reverse'
COLUMN_REVERSE = 'column-reverse'

FLEX_DIRECTION_CHOICES = Choices(ROW, ROW_REVERSE, COLUMN, COLUMN_REVERSE)

NOWRAP = 'no-wrap'
WRAP = 'wrap'
WRAP_REVERSE = 'wrap-reverse'

FLEX_WRAP_CHOICES = Choices(NOWRAP, WRAP, WRAP_REVERSE)

ORDER_CHOICES = Choices(integer=True)

######################################################################
# Flexibility (CSS-flexbox-1, Section 7)
######################################################################

FLEX_GROW_CHOICES = Choices(number=True)
FLEX_SHRINK_CHOICES = Choices(number=True)

CONTENT = 'content'

FLEX_BASIS_CHOICES = Choices(CONTENT, AUTO, length=True, percentage=True)

######################################################################
# Flex Alignment (CSS-flexbox-1, Section 8)
######################################################################

FLEX_START = 'flex-start'
FLEX_END = 'flex-end'
CENTER = 'center'
SPACE_BETWEEN = 'space-between'
SPACE_AROUND = 'space-around'

JUSTIFY_CONTENT_CHOICES = Choices(FLEX_START, FLEX_END, CENTER, SPACE_BETWEEN, SPACE_AROUND)

BASELINE = 'baseline'
STRETCH = 'stretch'

ALIGN_SELF_CHOICES = Choices(AUTO, FLEX_START, FLEX_END, CENTER, BASELINE, STRETCH)
ALIGN_ITEMS_CHOICES = Choices(AUTO, FLEX_START, FLEX_END, CENTER, BASELINE, STRETCH)

ALIGN_CONTENT_CHOICES = Choices(FLEX_START, FLEX_END, CENTER, SPACE_BETWEEN, SPACE_AROUND, STRETCH)


######################################################################
# Grid template (CSS-grid-1, Section 7)
######################################################################

GRID_TEMPLATE_CHOICES = Choices(None) #, track_list=True, auto_track_list=True)

GRID_TEMPLATE_AREA_CHOICES = Choices(None) #, strings=True), initial=None

GRID_AUTO_CHOICES = Choices(AUTO) #, track_sizes=True)

DENSE = 'dense'

GRID_AUTO_FLOW_CHOICES = Choices(ROW, COLUMN, DENSE)

######################################################################
# Grid placement (CSS-grid-1, Section 8)
######################################################################

GRID_PLACEMENT_CHOICES = Choices(AUTO) #, grid_line=True)

######################################################################
# Grid alignment (CSS-grid-1, Section 10)
######################################################################

GRID_GAP_CHOICES = Choices(percentage=True)
