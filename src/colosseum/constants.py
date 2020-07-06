from .validators import (
    ValidationError,
    is_border_spacing,
    is_color,
    is_cursor,
    is_integer,
    is_length,
    is_number,
    is_percentage,
    is_quote,
    is_rect,
)


class Choices:
    "A class to define allowable data types for a property."

    def __init__(self, *constants, validators=None,
                 explicit_defaulting_constants=None):
        self.constants = set(constants)
        self.explicit_defaulting_constants = explicit_defaulting_constants or []
        self.validators = validators or []

    def validate(self, value):
        for validator in self.validators:
            try:
                value = validator(value)
                return value
            except ValidationError:
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
        choices = set([str(c).lower().replace('_', '-') for c in self.constants])
        for validator in self.validators:
            choices.add(validator.description)

        if self.explicit_defaulting_constants:
            for item in self.explicit_defaulting_constants:
                choices.add(item)

        return ", ".join(sorted(choices))


class OtherProperty:
    """A class to refer to another property."""

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '{class_name}("{name}")'.format(class_name=self.__class__.__name__, name=self._name)

    def value(self, context):
        try:
            return getattr(context, self._name)
        except AttributeError:
            raise ValueError('Property "%s" not found!' % self._name)


######################################################################
# Versions of the HTML standard
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
default = object()

######################################################################
# Explicit defaulting constants
######################################################################

INITIAL = 'initial'
INHERIT = 'inherit'
UNSET = 'unset'
REVERT = 'revert'

######################################################################
# Margins
# 8.3 Margin properties
######################################################################

MARGIN_CHOICES = Choices(AUTO, validators=[is_length, is_percentage])
MARGIN_CHOICES = Choices(AUTO, validators=[is_length, is_percentage])

######################################################################
# 8.4 Padding properties
######################################################################

PADDING_CHOICES = Choices(validators=[is_length, is_percentage])

######################################################################
# 8.5 Border properties
######################################################################

THIN = 'thin'
MEDIUM = 'medium'
THICK = 'thick'

BORDER_WIDTH_CHOICES = Choices(THIN, MEDIUM, THICK, validators=[is_length])

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

BORDER_COLOR_CHOICES = Choices(
    TRANSPARENT,
    validators=[is_color],
    explicit_defaulting_constants=[INITIAL, INHERIT, UNSET, REVERT],
)

######################################################################
# 9.2.4 The display property
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
# 9.3 Positioning schemes
# 9.3.2 Box offsets
######################################################################

STATIC = 'static'
RELATIVE = 'relative'
ABSOLUTE = 'absolute'
FIXED = 'fixed'

POSITION_CHOICES = Choices(STATIC, RELATIVE, ABSOLUTE, FIXED)

BOX_OFFSET_CHOICES = Choices(AUTO, validators=[is_length, is_percentage], explicit_defaulting_constants=[INHERIT])

######################################################################
# 9.5.1 Positioning the float
# 9.5.2 Controlling flow next to floats
######################################################################

LEFT = 'left'
RIGHT = 'right'
BOTH = 'both'

FLOAT_CHOICES = Choices(LEFT, RIGHT, None)
CLEAR_CHOICES = Choices(None, LEFT, RIGHT, BOTH)

######################################################################
# 9.9 Layered Presentation
######################################################################

Z_INDEX_CHOICES = Choices(AUTO, validators=[is_integer])

######################################################################
# 9.10 Text Direction
######################################################################

RTL = 'rtl'
LTR = 'ltr'

DIRECTION_CHOICES = Choices(RTL, LTR)

NORMAL = 'normal'
EMBED = 'embed'
BIDI_OVERRIDE = 'bidi-override'

UNICODE_BIDI_CHOICES = Choices(NORMAL, EMBED, BIDI_OVERRIDE)

######################################################################
# 10.4 Minimum and maximum width
# 10.5 Content height
# 10.7 Minimum and maximum heights
######################################################################

SIZE_CHOICES = Choices(AUTO, validators=[is_length, is_percentage])
MIN_SIZE_CHOICES = Choices(AUTO, validators=[is_length, is_percentage])
MAX_SIZE_CHOICES = Choices(None, validators=[is_length, is_percentage])

######################################################################
# 10.8 Leading and half-leading
######################################################################
# line_height
# vertical_align

######################################################################
# 11.1.1 Overflow
######################################################################
# overflow

SCROLL = 'scroll'
VISIBLE = 'visible'

OVERFLOW_CHOICES = Choices(VISIBLE, HIDDEN, SCROLL, AUTO, explicit_defaulting_constants=[INHERIT])

######################################################################
# 11.1.2 Clip
######################################################################
# clip

CLIP_CHOICES = Choices(AUTO, validators=[is_rect], explicit_defaulting_constants=[INHERIT])

######################################################################
# 11.2 Visibility
######################################################################

VISIBLE = 'visible'
HIDDEN = 'hidden'
COLLAPSE = 'collapse'

VISIBILITY_CHOICES = Choices(VISIBLE, HIDDEN, COLLAPSE)

######################################################################
# 12.2 The content property
######################################################################
# content

######################################################################
# 12.3 Quotation marks
######################################################################

# quotes
QUOTES_CHOICES = Choices(None, INITIAL, validators=[is_quote], explicit_defaulting_constants=[INHERIT])

######################################################################
# 12.4 Automatic counters and numbering
######################################################################
# counter-reset
# counter-increment

######################################################################
# 12.5 Lists
######################################################################
# list_style_type
# list_style_image
# list_style_position
# list_style

# 13. Paged media ####################################################
######################################################################
# 13.3.1 Page break properties
######################################################################

AUTO = 'auto'
ALWAYS = 'always'
AVOID = 'avoid'
LEFT = 'left'
RIGHT = 'right'

# page_break_before
PAGE_BREAK_BEFORE_CHOICES = Choices(AUTO, ALWAYS, AVOID, LEFT, RIGHT, explicit_defaulting_constants=[INHERIT])

# page_break_after
PAGE_BREAK_AFTER_CHOICES = Choices(AUTO, ALWAYS, AVOID, LEFT, RIGHT, explicit_defaulting_constants=[INHERIT])

# page_break_inside
PAGE_BREAK_INSIDE_CHOICES = Choices(AUTO, AVOID, explicit_defaulting_constants=[INHERIT])

######################################################################
# 13.3.2 Breaks inside elements
######################################################################

# orphans
ORPHANS_CHOICES = Choices(validators=[is_integer], explicit_defaulting_constants=[INHERIT])

# widows
WIDOWS_CHOICES = Choices(validators=[is_integer], explicit_defaulting_constants=[INHERIT])

######################################################################
# 14.1 Foreground color
######################################################################
COLOR_CHOICES = Choices(default, validators=[is_color])

######################################################################
# 14.2.1 Background properties
######################################################################
BACKGROUND_COLOR_CHOICES = Choices(default, TRANSPARENT, validators=[is_color])

# background_image
# background_repeat
# background_attachment
# background_position
# background

######################################################################
# 15. Fonts
# 15.3 Font family
######################################################################
# font_family

######################################################################
# 15.4 Font Styling
######################################################################
# font_style

######################################################################
# 15.5 Small-caps
######################################################################
# font_variant

######################################################################
# 15.6 Font boldness
######################################################################
# font_weight

######################################################################
# 15.7 Font size
######################################################################
# font_size

######################################################################
# 16. Text ###########################################################
######################################################################
# 16.1 Indentation
######################################################################

# text_indent
TEXT_INDENT_CHOICES = Choices(validators=[is_length, is_percentage], explicit_defaulting_constants=[INHERIT])

######################################################################
# 16.2 Alignment
######################################################################

# text_align
LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
JUSTIFY = 'justify'

TEXT_ALIGN_CHOICES = Choices(LEFT, RIGHT, CENTER, JUSTIFY, explicit_defaulting_constants=[INHERIT])


class TextAlignInitialValue:

    def value(self, context):
        """Return the initial alignment value based on direction."""
        direction = getattr(context, 'direction')
        if direction is LTR:
            return LEFT

        if direction is RTL:
            return RIGHT

        raise ValueError('Undefined value "{value}" for direction property!'.format(value=direction))


######################################################################
# 16.3 Decoration
######################################################################

# text_decoration
UNDERLINE = 'underline'
OVERLINE = 'overline'
LINE_THROUGH = 'line-through'
BLINK = 'blink'

TEXT_DECORATION_CHOICES = Choices(None, UNDERLINE, OVERLINE, LINE_THROUGH, BLINK,
                                  explicit_defaulting_constants=[INHERIT])

######################################################################
# 16.4 Letter and word spacing
######################################################################

# letter_spacing
LETTER_SPACING_CHOICES = Choices(NORMAL, validators=[is_length], explicit_defaulting_constants=[INHERIT])

# word_spacing
WORD_SPACING_CHOICES = Choices(NORMAL, validators=[is_length], explicit_defaulting_constants=[INHERIT])

######################################################################
# 16.5 Capitalization
######################################################################

# text_transform
CAPITALIZE = 'capitalize'
UPPERCASE = 'uppercase'
LOWERCASE = 'lowercase'

TEXT_TRANSFORM_CHOICES = Choices(CAPITALIZE, UPPERCASE, LOWERCASE, None, explicit_defaulting_constants=[INHERIT])

######################################################################
# 16.6 White space
######################################################################

# white_space
# NORMAL = 'normal'
PRE = 'pre'
NOWRAP = 'nowrap'
PRE_WRAP = 'pre-wrap'
PRE_LINE = 'pre-line'

WHITE_SPACE_CHOICES = Choices(NORMAL, PRE, NOWRAP, PRE_WRAP, PRE_LINE, explicit_defaulting_constants=[INHERIT])

######################################################################
# 17. Tables
######################################################################
# 17.4.1 Caption position and alignment
######################################################################

TOP = 'top'
BOTTOM = 'bottom'

# caption_side
CAPTION_SIDE_CHOICES = Choices(TOP, BOTTOM, explicit_defaulting_constants=[INHERIT])

######################################################################
# 17.5.2 Table width algorithms
######################################################################

# table_layout
TABLE_LAYOUT_CHOICES = Choices(AUTO, FIXED, explicit_defaulting_constants=[INHERIT])

######################################################################
# 17.6 Borders
######################################################################


# border_collapse
COLLAPSE = 'collapse'
SEPARATE = 'separate'

BORDER_COLLAPSE_CHOICES = Choices(COLLAPSE, SEPARATE, explicit_defaulting_constants=[INHERIT])

# border_spacing
BORDER_SPACING_CHOICES = Choices(validators=[is_border_spacing], explicit_defaulting_constants=[INHERIT])

# empty_cells
SHOW = 'show'
HIDE = 'hide'

EMPTY_CELLS_CHOICES = Choices(SHOW, HIDE, explicit_defaulting_constants=[INHERIT])

######################################################################
# 18. User interface #################################################
######################################################################
# 18.1 Cursors
# cursor

AUTO = 'auto'
CROSSHAIR = 'crosshair'
DEFAULT = 'default'
POINTER = 'pointer'
MOVE = 'move'
E_RESIZE = 'e-resize'
NE_RESIZE = 'ne-resize'
NW_RESIZE = 'nw-resize'
N_RESIZE = 'n-resize'
SE_RESIZE = 'se-resize'
SW_RESIZE = 'sw-resize'
S_RESIZE = 's-resize'
W_RESIZE = 'w-resize'
TEXT = 'text'
WAIT = 'wait'
PROGRESS = 'progress'
HELP = 'help'

CURSOR_OPTIONS = [AUTO, CROSSHAIR, DEFAULT, POINTER, MOVE, E_RESIZE, NE_RESIZE, NW_RESIZE, N_RESIZE, SE_RESIZE,
                  SW_RESIZE, S_RESIZE, W_RESIZE, TEXT, WAIT, PROGRESS, HELP]

# Since the order is important, the cursor options are used in the is_cursor validator
CURSOR_CHOICES = Choices(validators=[is_cursor], explicit_defaulting_constants=[INHERIT])

######################################################################
# 18.4 Dynamic outlines
######################################################################

# outline_width
OUTLINE_WIDTH_CHOICES = Choices(
    THIN,
    MEDIUM,
    THICK,
    validators=[is_length],
    explicit_defaulting_constants=[INHERIT],
)

# outline_style
OUTLINE_STYLE_CHOICES = Choices(
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
    explicit_defaulting_constants=[INHERIT],
)

# outline_color
INVERT = 'invert'

OUTLINE_COLOR_CHOICES = Choices(
    INVERT,
    validators=[is_color],
    explicit_defaulting_constants=[INHERIT],
)

# outline

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

ORDER_CHOICES = Choices(validators=[is_integer])

######################################################################
# Flexibility (CSS-flexbox-1, Section 7)
######################################################################

FLEX_GROW_CHOICES = Choices(validators=[is_number])
FLEX_SHRINK_CHOICES = Choices(validators=[is_number])

CONTENT = 'content'

FLEX_BASIS_CHOICES = Choices(CONTENT, AUTO, validators=[is_length, is_percentage])

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

GRID_TEMPLATE_CHOICES = Choices(None)  # track_list=True, auto_track_list=True)

GRID_TEMPLATE_AREA_CHOICES = Choices(None)  # strings=True), initial=None

GRID_AUTO_CHOICES = Choices(AUTO)  # track_sizes=True)

DENSE = 'dense'

GRID_AUTO_FLOW_CHOICES = Choices(ROW, COLUMN, DENSE)

######################################################################
# Grid placement (CSS-grid-1, Section 8)
######################################################################

GRID_PLACEMENT_CHOICES = Choices(AUTO)  # grid_line=True)

######################################################################
# Grid alignment (CSS-grid-1, Section 10)
######################################################################

GRID_GAP_CHOICES = Choices(validators=[is_percentage])
