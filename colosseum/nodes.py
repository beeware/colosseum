from __future__ import print_function, absolute_import, division, unicode_literals

from .constants import *


class UnknownCSSStyleException(Exception):
    pass


class InvalidCSSStyleException(Exception):
    pass


def leading(axis):
    "Return the dimension attribute for leading space corresponding to the given axis"
    return TOP if axis == COLUMN else LEFT


def trailing(axis):
    "Return the dimension attribute for trailing space corresponding to the given axis"
    return BOTTOM if axis == COLUMN else RIGHT


def position(axis):
    "Return the position attribute corresponding to the given axis"
    return TOP if axis == COLUMN else LEFT


def dimension(axis):
    "Return the size dimension attribute corresponding to the given axis"
    return HEIGHT if axis == COLUMN else WIDTH


class Layout(object):
    def __init__(self, width=None, height=None, top=0, left=0):
        self.width = width
        self.height = height
        self.top = top
        self.left = left

    def __repr__(self):
        return u'<Layout (%sx%s @ %s,%s)>' % (self.width, self.height, self.left, self.top)

    def __eq__(self, value):
        return all([
            self.width == value.width,
            self.height == value.height,
            self.top == value.top,
            self.left == value.left
        ])

    def reset(self):
        self.width = None
        self.height = None
        self.top = 0
        self.left = 0


class ChildList(list):
    def __init__(self, parent, elements):
        super(ChildList, self).__init__(elements)
        self.parent = parent

    def append(self, child):
        super(ChildList, self).append(child)
        child.parent = self.parent
        self.parent.dirty = True

    def extend(self, child_list):
        super(ChildList, self).extend(child_list)
        for child in child_list:
            child.parent = self.parent
        self.parent.dirty = True

    def insert(self, index, child):
        super(ChildList, self).insert(index, child)
        child.parent = self.parent
        self.parent.dirty = True


def css_property(name, choices=None, default=None):
    "Define a simple CSS property attribute."
    def getter(self):
        return getattr(self, '_%s' % name, default)

    def setter(self, value):
        if value != getattr(self, '_%s' % name, default):
            if choices and value not in choices:
                raise InvalidCSSStyleException("Invalid value for CSS property '%s'; Valid values are: %s" % (
                    name,
                    ', '.join(s.replace('-', '_').upper() for s in choices))
                )
            setattr(self, '_%s' % name, value)
            self.dirty = True

    def deleter(self):
        try:
            delattr(self, '_%s' % name)
            self.dirty = True
        except AttributeError:
            # Attribute doesn't exist
            pass

    return property(getter, setter, deleter)


def css_directional_property(name, default=0):
    "Define a CSS property attribute that defers to top/right/bottom/left alternatives."
    def getter(self):
        return (
            getattr(self, name % 'top', default),
            getattr(self, name % 'right', default),
            getattr(self, name % 'bottom', default),
            getattr(self, name % 'left', default),
        )

    def setter(self, value):
        try:
            if len(value) == 4:
                setattr(self, name % 'top', value[0])
                setattr(self, name % 'right', value[1])
                setattr(self, name % 'bottom', value[2])
                setattr(self, name % 'left', value[3])
            elif len(value) == 3:
                setattr(self, name % 'top', value[0])
                setattr(self, name % 'right', value[1])
                setattr(self, name % 'bottom', value[2])
                setattr(self, name % 'left', value[1])
            elif len(value) == 2:
                setattr(self, name % 'top', value[0])
                setattr(self, name % 'right', value[1])
                setattr(self, name % 'bottom', value[0])
                setattr(self, name % 'left', value[1])
            elif len(value) == 1:
                setattr(self, name % 'top', value[0])
                setattr(self, name % 'right', value[0])
                setattr(self, name % 'bottom', value[0])
                setattr(self, name % 'left', value[0])
            else:
                raise InvalidCSSStyleException("Invalid value for '%s'; value must be an number, or a 1-4 tuple." % (name % ''))
        except TypeError:
            setattr(self, name % 'top', value)
            setattr(self, name % 'right', value)
            setattr(self, name % 'bottom', value)
            setattr(self, name % 'left', value)

    def deleter(self):
        delattr(self, name % 'top')
        delattr(self, name % 'right')
        delattr(self, name % 'bottom')
        delattr(self, name % 'left')

    return property(getter, setter, deleter)


class CSSNode(object):

    def __init__(self, *children, **style):
        self._layout = Layout()
        self._parent = None
        self.children = ChildList(self, children)

        self.measure = style.pop('measure', None)

        self.style(**style)
        self.dirty = True

    ######################################################################
    # Style properties
    ######################################################################

    width = css_property('width')
    height = css_property('height')
    min_width = css_property('min_width')
    min_height = css_property('min_height')
    max_width = css_property('max_width')
    max_height = css_property('max_height')

    position = css_property('position', choices=set([RELATIVE, ABSOLUTE]), default=RELATIVE)
    top = css_property('top')
    bottom = css_property('bottom')
    left = css_property('left')
    right = css_property('right')

    flex_direction = css_property('flex_direction', choices=set([COLUMN, ROW]), default=COLUMN)
    flex_wrap = css_property('flex_wrap', choices=set([WRAP, NOWRAP]), default=NOWRAP)
    flex = css_property('flex')

    margin_top = css_property('margin_top', default=0)
    margin_right = css_property('margin_right', default=0)
    margin_bottom = css_property('margin_bottom', default=0)
    margin_left = css_property('margin_left', default=0)

    padding_top = css_property('padding_top', default=0)
    padding_right = css_property('padding_right', default=0)
    padding_bottom = css_property('padding_bottom', default=0)
    padding_left = css_property('padding_left', default=0)

    border_top_width = css_property('border_top_width', default=0)
    border_right_width = css_property('border_right_width', default=0)
    border_bottom_width = css_property('border_bottom_width', default=0)
    border_left_width = css_property('border_left_width', default=0)

    justify_content = css_property('justify_content', choices=set([FLEX_START, CENTER, FLEX_END, SPACE_BETWEEN, SPACE_AROUND]), default=FLEX_START)
    align_items = css_property('align_items', choices=set([FLEX_START, CENTER, FLEX_END, STRETCH]), default=STRETCH)
    align_self = css_property('align_self', choices=set([FLEX_START, CENTER, FLEX_END, STRETCH, AUTO]), default=AUTO)

    # Some special case meta-properties that defer to underlying top/bottom/left/right base properties
    margin = css_directional_property('margin_%s')
    padding = css_directional_property('padding_%s')
    border_width = css_directional_property('border_%s_width')

    ######################################################################
    # Style manipulation
    ######################################################################

    def style(self, **styles):
        "Set multiple styles on the CSS node."
        for style, value in styles.items():
            if not hasattr(self, style):
                raise UnknownCSSStyleException("Unknown CSS style '%s'" % style)
            setattr(self, style, value)

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for child in self.children:
            child.dirty = value

    ######################################################################
    # Internal helpers for computing layout
    ######################################################################

    def _dimension_is_defined(self, axis):
        value = getattr(self, dimension(axis))
        return value is not None and value > 0

    def _position_is_defined(self, position):
        return getattr(self, position) is not None

    def _padding_and_border(self, position):
        return getattr(self, 'padding_' + position) + getattr(self, 'border_' + position + '_width')

    def _margin_for_axis(self, axis):
        return getattr(self, 'margin_' + leading(axis)) + getattr(self, 'margin_' + trailing(axis))

    def _padding_and_border_for_axis(self, axis):
        return self._padding_and_border(leading(axis)) + self._padding_and_border(trailing(axis))

    def _relative_position(self, axis):
        lead = getattr(self, leading(axis))
        if lead is not None:
            return lead
        value = getattr(self, trailing(axis))
        return -value if value is not None else 0

    def _align_item(self, child):
        if child.align_self != AUTO:
            return child.align_self

        return self.align_items

    def _dimension_with_margin(self, axis):
        return getattr(self._layout, dimension(axis)) + getattr(self, 'margin_' + leading(axis)) + getattr(self, 'margin_' + trailing(axis))

    @property
    def _is_flex(self):
        return self.position == RELATIVE and self.flex is not None and self.flex > 0

    def _bound_axis(self, axis, value):
        minValue = {
            ROW: self.min_width,
            COLUMN: self.min_height,
        }[axis]

        maxValue = {
            ROW: self.max_width,
            COLUMN: self.max_height,
        }[axis]

        boundValue = value
        if maxValue is not None and maxValue >= 0 and boundValue > maxValue:
            boundValue = maxValue

        if minValue is not None and minValue >= 0 and boundValue < minValue:
            boundValue = minValue

        return boundValue

    def _set_dimension_from_style(self, axis):
        # The parent already computed us a width or height. We just skip it
        if getattr(self._layout, dimension(axis)) is not None:
            return

        # We only run if there's a width or height defined
        if not self._dimension_is_defined(axis):
            return

        # The dimensions can never be smaller than the padding and border
        maxLayoutDimension = max(
            self._bound_axis(axis, getattr(self, dimension(axis))),
            self._padding_and_border_for_axis(axis)
        )
        setattr(self._layout, dimension(axis), maxLayoutDimension)

    ######################################################################
    # Calculate layout
    ######################################################################

    @property
    def layout(self):
        if self.dirty:
            self._layout.reset()
            self._calculate_layout(None)
            self.dirty = False
        return self._layout

    def _calculate_layout(self, parent_max_width=None):
        for child in self.children:
            child._layout.reset()

        main_axis = self.flex_direction
        cross_axis = COLUMN if main_axis == ROW else ROW

        # Handle width and height style attributes
        self._set_dimension_from_style(main_axis)
        self._set_dimension_from_style(cross_axis)

        # The position is set by the parent, but we need to complete it with a
        # delta composed of the margin and left/top/right/bottom
        setattr(
            self._layout,
            leading(main_axis),
            getattr(self._layout, leading(main_axis)) + getattr(self, 'margin_' + leading(main_axis)) + self._relative_position(main_axis)
        )
        setattr(
            self._layout,
            leading(cross_axis),
            getattr(self._layout, leading(cross_axis)) + getattr(self, 'margin_' + leading(cross_axis)) + self._relative_position(cross_axis)
        )

        if self.measure:
            width = None
            if self._dimension_is_defined(ROW):
                width = self.width
            elif getattr(self._layout, dimension(ROW)) is not None:
                width = getattr(self._layout, dimension(ROW))
            else:
                try:
                    width = parent_max_width - self._margin_for_axis(ROW)
                except TypeError:
                    pass

            if width:
                width = width - self._padding_and_border_for_axis(ROW)

            # We only need to give a dimension for the text if we haven't got any
            # for it computed yet. It can either be from the style attribute or because
            # the element is flexible.
            row_undefined = not self._dimension_is_defined(ROW) and getattr(self._layout, dimension(ROW)) is None
            column_undefined = not self._dimension_is_defined(COLUMN) and getattr(self._layout, dimension(COLUMN)) is None

            # Let's not measure the text if we already know both dimensions
            if row_undefined or column_undefined:
                measureDim = self.measure(width)
                if row_undefined:
                    self._layout.width = measureDim['width'] + self._padding_and_border_for_axis(ROW)
                if column_undefined:
                    self._layout.height = measureDim['height'] + self._padding_and_border_for_axis(COLUMN)
            return

        # Pre-fill some dimensions straight from the parent
        for i, child in enumerate(self.children):
            # Pre-fill cross axis dimensions when the child is using stretch before
            # we call the recursive layout pass
            if (self._align_item(child) == STRETCH and
                    child.position == RELATIVE and
                    getattr(self._layout, dimension(cross_axis)) is not None and
                    not child._dimension_is_defined(cross_axis)):
                setattr(
                    child._layout,
                    dimension(cross_axis),
                    max(
                        child._bound_axis(cross_axis,
                            getattr(self._layout, dimension(cross_axis))
                            - self._padding_and_border_for_axis(cross_axis)
                            - child._margin_for_axis(cross_axis)
                        ),
                        # You never want to go smaller than padding
                        child._padding_and_border_for_axis(cross_axis)
                    )
                )

            elif child.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets for the axis are defined (either both
                # left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self._layout, dimension(axis)) is not None and
                            not child._dimension_is_defined(axis) and
                            child._position_is_defined(leading(axis)) and
                            child._position_is_defined(trailing(axis))):
                        setattr(
                            child._layout,
                            dimension(axis),
                            max(
                                child._bound_axis(axis,
                                    getattr(self._layout, dimension(axis))
                                    - self._padding_and_border_for_axis(axis)
                                    - child._margin_for_axis(axis)
                                    - getattr(child, leading(axis))
                                    - getattr(child, trailing(axis))
                                ),
                                # You never want to go smaller than padding
                                child._padding_and_border_for_axis(axis)
                            )
                        )

        defined_main_dim = None
        if getattr(self._layout, dimension(main_axis)) is not None:
            defined_main_dim = getattr(self._layout, dimension(main_axis)) - self._padding_and_border_for_axis(main_axis)

        # We want to execute the next two loops one per line with flex-wrap
        start_line = 0
        end_line = 0
        # int nextOffset = 0;
        already_computed_next_layout = False
        # We aggregate the total dimensions of the container in those two variables
        lines_cross_dim = 0.0
        lines_main_dim = 0.0

        while end_line < len(self.children):
            # <Loop A> Layout non flexible children and count children by type

            # main_content_dim is accumulation of the dimensions and margin of all the
            # non flexible children. This will be used in order to either set the
            # dimensions of the self if none already exist, or to compute the
            # remaining space left for the flexible children.
            main_content_dim = 0.0

            # There are three kind of children, non flexible, flexible and absolute.
            # We need to know how many there are in order to distribute the space.
            flexible_children_count = 0
            total_flexible = 0
            non_flexible_children_count = 0

            for i, child in enumerate(self.children[start_line:]):
                next_content_dim = 0

                # If it's a flexible child, accumulate the size that the child potentially
                # contributes to the row
                if child._is_flex:
                    flexible_children_count = flexible_children_count + 1
                    total_flexible = total_flexible + child.flex

                    # Even if we don't know its exact size yet, we already know the padding,
                    # border and margin. We'll use this partial information, which represents
                    # the smallest possible size for the child, to compute the remaining
                    # available space.
                    next_content_dim = child._padding_and_border_for_axis(main_axis) + child._margin_for_axis(main_axis)

                else:
                    max_width = None;
                    if main_axis != ROW:
                        try:
                            max_width = parent_max_width - self._margin_for_axis(ROW) - self._padding_and_border_for_axis(ROW)
                        except TypeError:
                            pass

                        if self._dimension_is_defined(ROW):
                            max_width = getattr(self._layout, dimension(ROW)) - self._padding_and_border_for_axis(ROW)

                    # This is the main recursive call. We layout non flexible children.
                    if not already_computed_next_layout:
                        child._calculate_layout(max_width)

                    # Absolute positioned elements do not take part of the layout, so we
                    # don't use them to compute main_content_dim
                    if child.position == RELATIVE:
                        non_flexible_children_count = non_flexible_children_count + 1
                        # At this point we know the final size and margin of the element.
                        next_content_dim = child._dimension_with_margin(main_axis)

                # The element we are about to add would make us go to the next line
                if (self.flex_wrap == WRAP and
                        getattr(self._layout, dimension(main_axis)) is not None and
                        main_content_dim + next_content_dim > defined_main_dim and
                        # If there's only one element, then it's bigger than the content
                        # and needs its own line
                        i != 0):
                    already_computed_next_layout = True
                    break

                already_computed_next_layout = False
                main_content_dim = main_content_dim + next_content_dim
                end_line = start_line + i + 1

            # <Loop B> Layout flexible children and allocate empty space
            # In order to position the elements in the main axis, we have two
            # controls. The space between the beginning and the first element
            # and the space between each two elements.
            leading_main_dim = 0.0
            between_main_dim = 0.0

            # The remaining available space that needs to be allocated
            remaining_main_dim = 0.0
            if getattr(self._layout, dimension(main_axis)) is not None:
                remaining_main_dim = defined_main_dim - main_content_dim
            else:
                remaining_main_dim = self._bound_axis(main_axis, max(main_content_dim, 0)) - main_content_dim

            # If there are flexible children in the mix, they are going to fill the
            # remaining space
            if flexible_children_count != 0:
                flexible_main_dim = remaining_main_dim / total_flexible

                # Iterate over every child in the axis. If the flex share of remaining
                # space doesn't meet min/max bounds, remove this child from flex
                # calculations.
                for child in self.children[start_line:end_line]:
                    if child._is_flex:
                        base_main_dim = flexible_main_dim * child.flex + child._padding_and_border_for_axis(main_axis)
                        bound_main_dim = child._bound_axis(main_axis, base_main_dim)

                        if base_main_dim != bound_main_dim:
                            remaining_main_dim = remaining_main_dim - bound_main_dim
                            total_flexible = total_flexible - child.flex

                if total_flexible != 0:
                    flexible_main_dim = remaining_main_dim / total_flexible
                elif remaining_main_dim > 0:
                    flexible_main_dim = float('inf')
                else:
                    flexible_main_dim = float('-inf')

                # The non flexible children can overflow the container, in this case
                # we should just assume that there is no space available.
                if flexible_main_dim < 0.0:
                    flexible_main_dim = 0.0

                # We iterate over the full array and only apply the action on flexible
                # children. This is faster than actually allocating a new array that
                # contains only flexible children.
                for child in self.children[start_line:end_line]:
                    if child._is_flex:
                        # At this point we know the final size of the element in the main
                        # dimension
                        setattr(child._layout, dimension(main_axis), child._bound_axis(main_axis,
                            flexible_main_dim * child.flex + child._padding_and_border_for_axis(main_axis))
                        )

                        max_width = None
                        if self._dimension_is_defined(ROW):
                            max_width = getattr(self._layout, dimension(ROW)) - self._padding_and_border_for_axis(ROW)
                        elif main_axis != ROW:
                            try:
                                max_width = parent_max_width - self._margin_for_axis(ROW) - self._padding_and_border_for_axis(ROW)
                            except TypeError:
                                pass

                        # And we recursively call the layout algorithm for this child
                        child._calculate_layout(max_width)

            # We use justify_content to figure out how to allocate the remaining
            # space available
            else:
                justify_content = self.justify_content
                if justify_content == CENTER:
                    leading_main_dim = remaining_main_dim / 2.0
                elif justify_content == FLEX_END:
                    leading_main_dim = remaining_main_dim
                elif justify_content == SPACE_BETWEEN:
                    remaining_main_dim = max(remaining_main_dim, 0)
                    if flexible_children_count + non_flexible_children_count - 1 != 0:
                        between_main_dim = remaining_main_dim / (flexible_children_count + non_flexible_children_count - 1)
                    else:
                        between_main_dim = 0
                elif (justify_content == SPACE_AROUND):
                    # Space on the edges is half of the space between elements
                    between_main_dim = remaining_main_dim / (flexible_children_count + non_flexible_children_count)
                    leading_main_dim = between_main_dim / 2.0

            # <Loop C> Position elements in the main axis and compute dimensions

            # At this point, all the children have their dimensions set. We need to
            # find their position. In order to do that, we accumulate data in
            # variables that are also useful to compute the total dimensions of the
            # container!
            cross_dim = 0.0
            main_dim = leading_main_dim + self._padding_and_border(leading(main_axis))
            for child in self.children[start_line:end_line]:
                if child.position == ABSOLUTE and child._position_is_defined(leading(main_axis)):
                    # In case the child is position absolute and has left/top being
                    # defined, we override the position to whatever the user said
                    # (and margin/border).
                    setattr(
                        child._layout,
                        position(main_axis),
                        getattr(child, leading(main_axis)) + getattr(self, 'border_' + leading(main_axis) + '_width') + getattr(child, 'margin_' + leading(main_axis))
                    )
                else:
                    # If the child is position absolute (without top/left) or relative,
                    # we put it at the current accumulated offset.
                    setattr(
                        child._layout,
                        position(main_axis),
                        getattr(child._layout, position(main_axis)) + main_dim
                    )

                # Now that we placed the element, we need to update the variables
                # We only need to do that for relative elements. Absolute elements
                # do not take part in that phase.
                if child.position == RELATIVE:
                    # The main dimension is the sum of all the elements dimension plus
                    # the spacing.
                    main_dim = main_dim + between_main_dim + child._dimension_with_margin(main_axis)
                    # The cross dimension is the max of the elements dimension since there
                    # can only be one element in that cross dimension.
                    cross_dim = max(cross_dim, child._bound_axis(cross_axis, child._dimension_with_margin(cross_axis)))

            container_main_axis = getattr(self._layout, dimension(main_axis))
            # If the user didn't specify a width or height, and it has not been set
            # by the container, then we set it via the children.
            if container_main_axis is None:
                container_main_axis = max(
                    # We're missing the last padding at this point to get the final
                    # dimension
                    self._bound_axis(main_axis, main_dim + self._padding_and_border(trailing(main_axis))),
                    # We can never assign a width smaller than the padding and borders
                    self._padding_and_border_for_axis(main_axis)
                )

            container_cross_axis = getattr(self._layout, dimension(cross_axis))
            if getattr(self._layout, dimension(cross_axis)) is None:
                container_cross_axis = max(
                    # For the cross dim, we add both sides at the end because the value
                    # is aggregate via a max function. Intermediate negative values
                    # can mess this computation otherwise
                    self._bound_axis(cross_axis, cross_dim + self._padding_and_border_for_axis(cross_axis)),
                    self._padding_and_border_for_axis(cross_axis)
                )

            # <Loop D> Position elements in the cross axis
            for child in self.children[start_line:end_line]:
                if child.position == ABSOLUTE and child._position_is_defined(leading(cross_axis)):
                    # In case the child is absolutely positionned and has a
                    # top/left/bottom/right being set, we override all the previously
                    # computed positions to set it correctly.
                    setattr(
                        child._layout,
                        position(cross_axis),
                        getattr(child, leading(cross_axis)) + getattr(self, 'border_' + leading(cross_axis) + '_width') + getattr(child, 'margin_' + leading(cross_axis))
                    )

                else:
                    leading_cross_dim = self._padding_and_border(leading(cross_axis))

                    # For a relative children, we're either using align_items (parent) or
                    # align_self (child) in order to determine the position in the cross axis
                    if child.position == RELATIVE:
                        align_item = self._align_item(child)
                        if align_item == STRETCH:
                            # You can only stretch if the dimension has not already been set
                            # previously.
                            if not child._dimension_is_defined(cross_axis):
                                setattr(
                                    child._layout,
                                    dimension(cross_axis),
                                    max(
                                        child._bound_axis(cross_axis,
                                            container_cross_axis
                                            - self._padding_and_border_for_axis(cross_axis)
                                            - child._margin_for_axis(cross_axis)
                                        ),
                                        # You never want to go smaller than padding
                                        child._padding_and_border_for_axis(cross_axis)
                                    )
                                )
                        elif align_item != FLEX_START:
                            # The remaining space between the parent dimensions+padding and child
                            # dimensions+margin.
                            remaining_cross_dim = container_cross_axis - self._padding_and_border_for_axis(cross_axis) - child._dimension_with_margin(cross_axis)

                            if align_item == CENTER:
                                leading_cross_dim = leading_cross_dim + remaining_cross_dim / 2
                            else: # FLEX_END
                                leading_cross_dim = leading_cross_dim + remaining_cross_dim

                    # And we apply the position
                    setattr(
                        child._layout,
                        position(cross_axis),
                        getattr(child._layout, position(cross_axis)) + lines_cross_dim + leading_cross_dim
                    )

            lines_cross_dim = lines_cross_dim + cross_dim
            lines_main_dim = max(lines_main_dim, main_dim)
            start_line = end_line

        # If the user didn't specify a width or height, and it has not been set
        # by the container, then we set it via the children.
        if getattr(self._layout, dimension(main_axis)) is None:
            setattr(
                self._layout,
                dimension(main_axis),
                max(
                    # We're missing the last padding at this point to get the final
                    # dimension
                    self._bound_axis(main_axis, lines_main_dim + self._padding_and_border(trailing(main_axis))),
                    # We can never assign a width smaller than the padding and borders
                    self._padding_and_border_for_axis(main_axis)
                )
            )

        if getattr(self._layout, dimension(cross_axis)) is None:
            setattr(
                self._layout,
                dimension(cross_axis),
                max(
                    # For the cross dim, we add both sides at the end because the value
                    # is aggregate via a max function. Intermediate negative values
                    # can mess this computation otherwise
                    self._bound_axis(cross_axis, lines_cross_dim + self._padding_and_border_for_axis(cross_axis)),
                    self._padding_and_border_for_axis(cross_axis)
                )
            )

        # <Loop E> Calculate dimensions for absolutely positioned elements
        for child in self.children:
            if child.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets for the axis are defined (either both
                # left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self._layout, dimension(axis)) is not None and
                            not child._dimension_is_defined(axis) and
                            child._position_is_defined(leading(axis)) and
                            child._position_is_defined(trailing(axis))):
                        setattr(
                            child._layout,
                            dimension(axis),
                            max(
                                child._bound_axis(axis,
                                    getattr(self._layout, dimension(axis))
                                    - self._padding_and_border_for_axis(axis)
                                    - child._margin_for_axis(axis)
                                    - getattr(child, leading(axis))
                                    - getattr(child, trailing(axis))
                                ),
                                # You never want to go smaller than padding
                                child._padding_and_border_for_axis(axis)
                            )
                        )
                for axis in [ROW, COLUMN]:
                    if child._position_is_defined(trailing(axis)) and not child._position_is_defined(leading(axis)):
                        setattr(
                            child._layout,
                            leading(axis),
                            getattr(self._layout, dimension(axis)) - getattr(child._layout, dimension(axis)) - getattr(child, trailing(axis))
                        )

