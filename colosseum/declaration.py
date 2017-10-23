from . import engine as css_engine
from .constants import (
    ALIGN_CONTENT_CHOICES, ALIGN_ITEMS_CHOICES, ALIGN_SELF_CHOICES, AUTO,
    BORDER_COLOR_CHOICES, BORDER_STYLE_CHOICES, BORDER_WIDTH_CHOICES,
    BOX_OFFSET_CHOICES, CLEAR_CHOICES, DIRECTION_CHOICES, DISPLAY_CHOICES,
    FLEX_BASIS_CHOICES, FLEX_DIRECTION_CHOICES, FLEX_GROW_CHOICES,
    FLEX_SHRINK_CHOICES, FLEX_START, FLEX_WRAP_CHOICES, FLOAT_CHOICES,
    GRID_AUTO_CHOICES, GRID_AUTO_FLOW_CHOICES, GRID_GAP_CHOICES,
    GRID_PLACEMENT_CHOICES, GRID_TEMPLATE_AREA_CHOICES, GRID_TEMPLATE_CHOICES,
    INLINE, JUSTIFY_CONTENT_CHOICES, LTR, MARGIN_CHOICES, MAX_SIZE_CHOICES,
    MIN_SIZE_CHOICES, NORMAL, NOWRAP, PADDING_CHOICES, POSITION_CHOICES, ROW,
    SIZE_CHOICES, STATIC, STRETCH, TRANSPARENT, UNICODE_BIDI_CHOICES,
    Z_INDEX_CHOICES, ORDER_CHOICES
)

_CSS_PROPERTIES = set()


def unvalidated_property(name, choices, initial):
    "Define a simple CSS property attribute."
    initial = choices.validate(initial)

    def getter(self):
        return getattr(self, '_%s' % name, initial)

    def setter(self, value):
        if value != getattr(self, '_%s' % name, initial):
            setattr(self, '_%s' % name, value)
            self.dirty = True

    def deleter(self):
        try:
            delattr(self, '_%s' % name)
            self.dirty = True
        except AttributeError:
            # Attribute doesn't exist
            pass

    _CSS_PROPERTIES.add(name)
    return property(getter, setter, deleter)


def validated_property(name, choices, initial):
    "Define a simple CSS property attribute."
    initial = choices.validate(initial)

    def getter(self):
        return getattr(self, '_%s' % name, initial)

    def setter(self, value):
        try:
            value = choices.validate(value)
        except ValueError:
            raise ValueError("Invalid value '%s' for CSS property '%s'; Valid values are: %s" % (
                value, name, choices
            ))

        if value != getattr(self, '_%s' % name, initial):
            setattr(self, '_%s' % name, value)
            self.dirty = True

    def deleter(self):
        try:
            delattr(self, '_%s' % name)
            self.dirty = True
        except AttributeError:
            # Attribute doesn't exist
            pass

    _CSS_PROPERTIES.add(name)
    return property(getter, setter, deleter)


def directional_property(name, initial):
    "Define a property attribute that proxies for top/right/bottom/left alternatives."
    def getter(self):
        return (
            getattr(self, name % '_top', initial),
            getattr(self, name % '_right', initial),
            getattr(self, name % '_bottom', initial),
            getattr(self, name % '_left', initial),
        )

    def setter(self, value):
        if isinstance(value, tuple):
            if len(value) == 4:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[2])
                setattr(self, name % '_left', value[3])
            elif len(value) == 3:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[2])
                setattr(self, name % '_left', value[1])
            elif len(value) == 2:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[0])
                setattr(self, name % '_left', value[1])
            elif len(value) == 1:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[0])
                setattr(self, name % '_bottom', value[0])
                setattr(self, name % '_left', value[0])
            else:
                raise ValueError("Invalid value for '%s'; value must be an number, or a 1-4 tuple." % (name % ''))
        else:
            setattr(self, name % '_top', value)
            setattr(self, name % '_right', value)
            setattr(self, name % '_bottom', value)
            setattr(self, name % '_left', value)

    def deleter(self):
        delattr(self, name % '_top')
        delattr(self, name % '_right')
        delattr(self, name % '_bottom')
        delattr(self, name % '_left')

    _CSS_PROPERTIES.add(name % '')
    _CSS_PROPERTIES.add(name % '_top')
    _CSS_PROPERTIES.add(name % '_right')
    _CSS_PROPERTIES.add(name % '_bottom')
    _CSS_PROPERTIES.add(name % '_left')
    return property(getter, setter, deleter)


class CSS:
    def __init__(self, **style):
        self._node = None
        self.set(**style)

    ######################################################################
    # Style properties
    ######################################################################

    # 8. Box model #######################################################
    # 8.3 Margin properties
    margin_top = validated_property('margin_top', choices=MARGIN_CHOICES, initial=0)
    margin_right = validated_property('margin_right', choices=MARGIN_CHOICES, initial=0)
    margin_bottom = validated_property('margin_bottom', choices=MARGIN_CHOICES, initial=0)
    margin_left = validated_property('margin_left', choices=MARGIN_CHOICES, initial=0)
    margin = directional_property('margin%s', initial=0)

    # 8.4 Padding properties
    padding_top = validated_property('padding_top', choices=PADDING_CHOICES, initial=0)
    padding_right = validated_property('padding_right', choices=PADDING_CHOICES, initial=0)
    padding_bottom = validated_property('padding_bottom', choices=PADDING_CHOICES, initial=0)
    padding_left = validated_property('padding_left', choices=PADDING_CHOICES, initial=0)
    padding = directional_property('padding%s', initial=0)

    # 8.5 Border properties
    # 8.5.1 Border width
    border_top_width = validated_property('border_top_width', choices=BORDER_WIDTH_CHOICES, initial=0)
    border_right_width = validated_property('border_right_width', choices=BORDER_WIDTH_CHOICES, initial=0)
    border_bottom_width = validated_property('border_bottom_width', choices=BORDER_WIDTH_CHOICES, initial=0)
    border_left_width = validated_property('border_left_width', choices=BORDER_WIDTH_CHOICES, initial=0)
    border_width = directional_property('border%s_width', initial=0)

    # 8.5.2 Border color
    border_top_color = validated_property('border_top_color', choices=BORDER_COLOR_CHOICES, initial=TRANSPARENT)
    border_right_color = validated_property('border_right_color', choices=BORDER_COLOR_CHOICES, initial=TRANSPARENT)
    border_bottom_color = validated_property('border_bottom_color', choices=BORDER_COLOR_CHOICES, initial=TRANSPARENT)
    border_left_color = validated_property('border_left_color', choices=BORDER_COLOR_CHOICES, initial=TRANSPARENT)
    border_color = directional_property('border%s_color', initial=0)

    # 8.5.3 Border style
    border_top_style = validated_property('border_top_style', choices=BORDER_STYLE_CHOICES, initial=None)
    border_right_style = validated_property('border_right_style', choices=BORDER_STYLE_CHOICES, initial=None)
    border_bottom_style = validated_property('border_bottom_style', choices=BORDER_STYLE_CHOICES, initial=None)
    border_left_style = validated_property('border_left_style', choices=BORDER_STYLE_CHOICES, initial=None)
    border_style = directional_property('border%s_style', initial=None)

    # 8.5.4 Border shorthand properties
    # border_top
    # border_right
    # border_bottom
    # border_left
    # border

    # 9. Visual formatting model #########################################
    # 9.2.4 The display property
    display = validated_property('display', choices=DISPLAY_CHOICES, initial=INLINE)
    # 9.3 Positioning schemes
    position = validated_property('position', choices=POSITION_CHOICES, initial=STATIC)

    # 9.3.2 Box offsets
    top = validated_property('top', choices=BOX_OFFSET_CHOICES, initial=AUTO)
    bottom = validated_property('bottom', choices=BOX_OFFSET_CHOICES, initial=AUTO)
    left = validated_property('left', choices=BOX_OFFSET_CHOICES, initial=AUTO)
    right = validated_property('right', choices=BOX_OFFSET_CHOICES, initial=AUTO)

    # 9.5.1 Positioning the float
    float = validated_property('float', choices=FLOAT_CHOICES, initial=None)
    # 9.5.2 Controlling flow next to floats
    clear = validated_property('clear', choices=CLEAR_CHOICES, initial=None)

    # 9.9 Layered Presentation
    z_index = validated_property('z_index', choices=Z_INDEX_CHOICES, initial=AUTO)

    # 9.10 Text Direction
    direction = validated_property('direction', choices=DIRECTION_CHOICES, initial=LTR)
    unicode_bidi = validated_property('unicode_bidi', choices=UNICODE_BIDI_CHOICES, initial=NORMAL)

    # 10. Visual formatting model details ################################
    # 10.2 Content width
    width = validated_property('width', choices=SIZE_CHOICES, initial=AUTO)

    # 10.4 Minimum and maximum width
    # Initial value updated by Flexbox 4.5
    min_width = validated_property('min_width', choices=MIN_SIZE_CHOICES, initial=AUTO)
    max_width = validated_property('max_width', choices=MAX_SIZE_CHOICES, initial=None)

    # 10.5 Content height
    height = validated_property('height', choices=SIZE_CHOICES, initial=AUTO)

    # 10.7 Minimum and maximum heights
    # Initial value updated by Flexbox 4.5
    min_height = validated_property('min_height', choices=MIN_SIZE_CHOICES, initial=AUTO)
    max_height = validated_property('max_height', choices=MAX_SIZE_CHOICES, initial=None)

    # 10.8 Leading and half-leading
    # line_height
    # vertical_align

    # 11. Visual effects #################################################
    # 11.1.1 Overflow
    # overflow

    # 11.1.2 Clip
    # clip

    # 11.2 Visibility
    # visibility

    # 12. Visual effects #################################################
    # 12.2 The content property
    # content

    # 12.3 Quotation marks
    # quotes

    # 12.4 Automatic counters and numbering
    # counter-reset
    # counter-increment

    # 12.5 Lists
    # list_style_type
    # list_style_image
    # list_style_position
    # list_style

    # 13. Paged media ####################################################
    # 13.3.1 Page break properties
    # page_break_before
    # page_break_after
    # page_break_inside

    # 13.3.2 Breaks inside elements
    # orphans
    # widows

    # 14. Colors and backgrounds #########################################
    # 14.1 Foreground color
    # color

    # 14.2.1 Background properties
    # background_color
    # background_image
    # background_repeat
    # background_attachment
    # background_position
    # background

    # 15. Fonts ##########################################################
    # 15.3 Font family
    # font_family

    # 15.4 Font Styling
    # font_style

    # 15.5 Small-caps
    # font_variant

    # 15.6 Font boldness
    # font_weight

    # 15.7 Font size
    # font_size

    # 15.8 Shorthand font property
    # font

    # 16. Text ###########################################################
    # 16.1 Indentation
    # text_indent

    # 16.2 Alignment
    # text_align

    # 16.3 Decoration
    # text_decoration

    # 16.4 Letter and word spacing
    # letter_spacing
    # word_spacing

    # 16.5 Capitalization
    # text_transform

    # 16.6 White space
    # white_space

    # 17. Tables #########################################################
    # 17.4.1 Caption position and alignment
    # caption_side

    # 17.5.2 Table width algorithms
    # table_layout

    # 17.6 Borders
    # border_collapse
    # border_spacing
    # empty_cells

    # 18. User interface #################################################
    # 18.1 Cursors
    # cursor

    # 18.4 Dynamic outlines
    # outline_width
    # outline_style
    # outline_color
    # outline

    ######################################################################
    # Flexbox properties
    ######################################################################

    # 5. Ordering and orientation ########################################
    # 5.1 Flex flow direction
    # flex_direction = validated_property('flex_direction', choices=FLEX_DIRECTION_CHOICES, initial=ROW)

    # 5.2 Flex line wrapping
    # flex_wrap = validated_property('flex_wrap', choices=FLEX_WRAP_CHOICES, initial=NOWRAP)

    # 5.3 Flex direction and wrap
    # flex_flow =

    # 5.4 Display order
    # order = validated_property('order', choices=ORDER_CHOICES, initial=0)

    # 7. Flexibility #####################################################
    # 7.2 Components of flexibility
    # flex_grow = validated_property('flex_grow', choices=FLEX_GROW_CHOICES, initial=0)
    # flex_shrink = validated_property('flex_shrink', choices=FLEX_SHRINK_CHOICES, initial=1)
    # flex_basis = validated_property('flex_basis', choices=FLEX_BASIS_CHOICES, initial=AUTO)

    # 7.1 The 'flex' shorthand
    # flex =

    # 8. Alignment #######################################################
    # 8.2 Axis alignment
    # justify_content = validated_property('justify_content', choices=JUSTIFY_CONTENT_CHOICES, initial=FLEX_START)

    # 8.3 Cros-axis alignment
    # align_items = validated_property('align_items', choices=ALIGN_ITEMS_CHOICES, initial=STRETCH)
    # align_self = validated_property('align_self', choices=ALIGN_SELF_CHOICES, initial=AUTO)

    # 8.4 Packing flex lines
    # align_content = validated_property('align_content', choices=ALIGN_CONTENT_CHOICES, initial=STRETCH)

    ######################################################################
    # Grid properties
    ######################################################################
    # 7. Defining the grid ###############################################
    # 7.2 Explicit track sizing
    # grid_template_columns = validated_property('grid_template_columns', choices=GRID_TEMPLATE_CHOICES, initial=None)
    # grid_template_rows = validated_property('grid_template_rows', choices=GRID_TEMPLATE_CHOICES, initial=None)

    # 7.3 Named Areas
    # grid_template_areas = validated_property('grid_template_areas', choices=GRID_TEMPLATE_AREA_CHOICES, initial=None)

    # 7.4 Explicit grid shorthand
    # grid_template =

    # 7.6 Implicit track sizing
    # grid_auto_columns = validated_property('grid_auto_columns', choices=GRID_AUTO_CHOICES, initial=AUTO)
    # grid_auto_rows = validated_property('grid_auto_rows', choices=GRID_AUTO_CHOICES, initial=AUTO)

    # 7.7 Automatic placement
    # grid_auto_flow = validated_property('grid_auto_flow', choices=GRID_AUTO_FLOW_CHOICES, initial=ROW)

    # 7.8 Grid definition shorthand
    # grid =

    # 8. Placing grid items ##############################################
    # 8.3 Line-based placement
    # grid_row_start = validated_property('grid_row_start', choices=GRID_PLACEMENT_CHOICES, initial=AUTO)
    # grid_column_start = validated_property('grid_column_start', choices=GRID_PLACEMENT_CHOICES, initial=AUTO)
    # grid_row_end = validated_property('grid_row_end', choices=GRID_PLACEMENT_CHOICES, initial=AUTO)
    # grid_column_end = validated_property('grid_column_end', choices=GRID_PLACEMENT_CHOICES, initial=AUTO)

    # 8.4 Placement shorthands
    # grid_row =
    # grid_column =
    # grid_area =

    # 10. Alignment and spacing ##########################################
    # 10.1 Gutters
    # grid_row_gap = validated_property('grid_row_gap', choices=GRID_GAP_CHOICES, initial=0)
    # grid_column_gap = validated_property('grid_column_gap', choices=GRID_GAP_CHOICES, initial=0)
    # grid_gap =

    ######################################################################
    # Proxy the dirtiness state of layout calculations
    ######################################################################
    @property
    def dirty(self):
        if self._node:
            return self._node.layout.dirty

    @dirty.setter
    def dirty(self, value):
        if self._node:
            self._node.layout.dirty = value

    ######################################################################
    # Obtain the layout module
    ######################################################################
    def engine(self):
        return css_engine

    ######################################################################
    # Style manipulation
    ######################################################################
    def set(self, **styles):
        "Set multiple styles on the CSS definition."
        for name, value in styles.items():
            if not hasattr(self, name):
                raise NameError("Unknown CSS style '%s'" % name)

            if value is None:
                delattr(self, name)
            else:
                setattr(self, name, value)

    def copy(self, node=None):
        "Create a duplicate of this style declaration."
        dup = CSS()
        dup._node = node
        for style in _CSS_PROPERTIES:
            try:
                setattr(dup, style, getattr(self, '_%s' % style))
            except AttributeError:
                pass
        return dup

    ######################################################################
    # Get the rendered form of the style declaration
    ######################################################################
    def __str__(self):
        non_default = []
        for name in _CSS_PROPERTIES:
            try:
                non_default.append((
                    name.replace('_', '-'),
                    getattr(self, '_%s' % name)
                ))
            except AttributeError:
                pass

        return "; ".join(
            "%s: %s" % (name, value)
            for name, value in sorted(non_default)
        )
