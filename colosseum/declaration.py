from . import engine as css_engine
from .constants import (
    AUTO, INLINE, STATIC, LTR, NORMAL,
    DISPLAY_CHOICES, POSITION_CHOICES, FLOAT_CHOICES,
    CLEAR_CHOICES, DIRECTION_CHOICES, UNICODE_BIDI_CHOICES,
)
from .units import PixelUnit


_CSS_PROPERTIES = set()


def dirty_property(name, choices=None, default=None):
    "Define a simple CSS property attribute."
    def getter(self):
        return getattr(self, '_%s' % name, default)

    def setter(self, value):
        if choices and value not in choices:
            raise ValueError("Invalid value '%s' for CSS property '%s'; Valid values are: %s" % (
                value,
                name,
                ', '.join(sorted(str(s).replace('_', '-') for s in choices)))
            )

        if isinstance(value, int):
            value = PixelUnit(value)

        if value != getattr(self, '_%s' % name, default):
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


def directional_property(name, default=0):
    "Define a property attribute that proxies for top/right/bottom/left alternatives."
    def getter(self):
        return (
            getattr(self, name % '_top', default),
            getattr(self, name % '_right', default),
            getattr(self, name % '_bottom', default),
            getattr(self, name % '_left', default),
        )

    def setter(self, value):
        try:
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
        except TypeError:
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
    margin_top = dirty_property('margin_top', default=0)
    margin_right = dirty_property('margin_right', default=0)
    margin_bottom = dirty_property('margin_bottom', default=0)
    margin_left = dirty_property('margin_left', default=0)
    margin = directional_property('margin%s', default=0)

    # 8.4 Padding properties
    padding_top = dirty_property('padding_top', default=0)
    padding_right = dirty_property('padding_right', default=0)
    padding_bottom = dirty_property('padding_bottom', default=0)
    padding_left = dirty_property('padding_left', default=0)
    padding = directional_property('padding%s', default=0)

    # 8.5 Border properties
    # 8.5.1 Border width
    border_top_width = dirty_property('border_top_width', default=0)
    border_right_width = dirty_property('border_right_width', default=0)
    border_bottom_width = dirty_property('border_bottom_width', default=0)
    border_left_width = dirty_property('border_left_width', default=0)
    border_width = directional_property('border%s_width', default=0)

    # 8.5.2 Border color
    # border_top_color
    # border_right_color
    # border_bottom_color
    # border_left_color
    # border_color

    # 8.5.3 Border style
    # border_top_style
    # border_right_style
    # border_bottom_style
    # border_left_style
    # border_style

    # 8.5.4 Border shorthand properties
    # border_top
    # border_right
    # border_bottom
    # border_left
    # border

    # 9. Visual formatting model #########################################
    # 9.2.4 The display property
    display = dirty_property('display', choices=DISPLAY_CHOICES, default=INLINE)
    # 9.3 Positioning schemes
    position = dirty_property('position', choices=POSITION_CHOICES, default=STATIC)

    # 9.3.2 Box offsets
    top = dirty_property('top', default=AUTO)
    bottom = dirty_property('bottom', default=AUTO)
    left = dirty_property('left', default=AUTO)
    right = dirty_property('right', default=AUTO)

    # 9.5.1 Positioning the float
    # float_ = dirty_property('float', choices=FLOAT_CHOICES, default=None)
    # 9.5.2 Controlling flow next to floats
    clear = dirty_property('clear', choices=CLEAR_CHOICES, default=None)

    # 9.10 Text Direction
    direction = dirty_property('direction', choices=DIRECTION_CHOICES, default=LTR)
    unicode_bidi = dirty_property('unicode_bidi', choices=UNICODE_BIDI_CHOICES, default=NORMAL)

    # 10. Visual formatting model details ################################
    # 10.2 Content width
    width = dirty_property('width', default=AUTO)

    # 10.4 Minimum and maximum width
    min_width = dirty_property('min_width', default=0)
    max_width = dirty_property('max_width')

    # 10.5 Content height
    height = dirty_property('height', default=AUTO)

    # 10.7 Minimum and maximum heights
    min_height = dirty_property('min_height', default=0)
    max_height = dirty_property('max_height')

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
    # outline-width
    # outline-style
    # outline-color
    # outline

    ######################################################################
    # Proxy the dirtiness state of layout calculations
    ######################################################################
    @property
    def dirty(self):
        return self._node.layout.dirty

    @dirty.setter
    def dirty(self, value):
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
