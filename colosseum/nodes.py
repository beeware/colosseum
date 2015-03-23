from __future__ import print_function, absolute_import, division, unicode_literals

from .constants import *


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

    def copy(self, layout):
        self.width = layout.width
        self.height = layout.height
        self.top = layout.top
        self.left = layout.width


class ChildList(list):
    def __init__(self, parent):
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


class CSSNode(object):

    def __init__(self,
                width=None, height=None, top=None, bottom=None, left=None, right=None,
                position=RELATIVE,
                flexDirection=COLUMN, flexWrap=NOWRAP, flex=None,
                margin=None, marginTop=0, marginBottom=0, marginLeft=0, marginRight=0,
                padding=None, paddingTop=0, paddingBottom=0, paddingLeft=0, paddingRight=0,
                borderWidth=None, borderTopWidth=0, borderBottomWidth=0, borderRightWidth=0, borderLeftWidth=0,
                justifyContent=FLEX_START, alignItems=STRETCH, alignSelf=AUTO,
                measure=None
            ):

        self._width = width
        self._height = height

        self._position = position

        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right

        self._flexDirection = flexDirection
        self._flexWrap = flexWrap
        self._flex = flex

        if margin:
            try:
                if len(margin) == 4:
                    self._marginTop = margin[0]
                    self._marginRight = margin[1]
                    self._marginBottom = margin[2]
                    self._marginLeft = margin[3]
                elif len(margin) == 3:
                    self._marginTop = margin[0]
                    self._marginRight = margin[1]
                    self._marginBottom = margin[2]
                    self._marginLeft = margin[3]
                elif len(margin) == 2:
                    self._marginTop = margin[0]
                    self._marginRight = margin[1]
                    self._marginBottom = margin[0]
                    self._marginLeft = margin[1]
                elif len(margin) == 1:
                    self._marginTop = margin[0]
                    self._marginRight = margin[0]
                    self._marginBottom = margin[0]
                    self._marginLeft = margin[0]
                else:
                    raise Exception('Invalid margin definition')
            except TypeError:
                self._marginTop = margin
                self._marginRight = margin
                self._marginBottom = margin
                self._marginLeft = margin
        else:
            self._marginTop = marginTop
            self._marginRight = marginRight
            self._marginBottom = marginBottom
            self._marginLeft = marginLeft

        if padding:
            try:
                if len(padding) == 4:
                    self._paddingTop = padding[0]
                    self._paddingRight = padding[1]
                    self._paddingBottom = padding[2]
                    self._paddingLeft = padding[3]
                elif len(padding) == 3:
                    self._paddingTop = padding[0]
                    self._paddingRight = padding[1]
                    self._paddingBottom = padding[2]
                    self._paddingLeft = padding[3]
                elif len(padding) == 2:
                    self._paddingTop = padding[0]
                    self._paddingRight = padding[1]
                    self._paddingBottom = padding[0]
                    self._paddingLeft = padding[1]
                elif len(padding) == 1:
                    self._paddingTop = padding[0]
                    self._paddingRight = padding[0]
                    self._paddingBottom = padding[0]
                    self._paddingLeft = padding[0]
                else:
                    raise Exception('Invalid padding definition')
            except TypeError:
                self._paddingTop = padding
                self._paddingRight = padding
                self._paddingBottom = padding
                self._paddingLeft = padding
        else:
            self._paddingTop = paddingTop
            self._paddingRight = paddingRight
            self._paddingBottom = paddingBottom
            self._paddingLeft = paddingLeft

        if borderWidth:
            try:
                if len(borderWidth) == 4:
                    self._borderTopWidth = borderWidth[0]
                    self._borderRightWidth = borderWidth[1]
                    self._borderBottomWidth = borderWidth[2]
                    self._borderLeftWidth = borderWidth[3]
                elif len(borderWidth) == 3:
                    self._borderTopWidth = borderWidth[0]
                    self._borderRightWidth = borderWidth[1]
                    self._borderBottomWidth = borderWidth[2]
                    self._borderLeftWidth = borderWidth[3]
                elif len(borderWidth) == 2:
                    self._borderTopWidth = borderWidth[0]
                    self._borderRightWidth = borderWidth[1]
                    self._borderBottomWidth = borderWidth[0]
                    self._borderLeftWidth = borderWidth[1]
                elif len(borderWidth) == 1:
                    self._borderTopWidth = borderWidth[0]
                    self._borderRightWidth = borderWidth[0]
                    self._borderBottomWidth = borderWidth[0]
                    self._borderLeftWidth = borderWidth[0]
                else:
                    raise Exception('Invalid borderWidth definition')
            except TypeError:
                self._borderTopWidth = borderWidth
                self._borderRightWidth = borderWidth
                self._borderBottomWidth = borderWidth
                self._borderLeftWidth = borderWidth
        else:
            self._borderTopWidth = borderTopWidth
            self._borderLeftWidth = borderLeftWidth
            self._borderBottomWidth = borderBottomWidth
            self._borderRightWidth = borderRightWidth


        self._justifyContent = justifyContent
        self._alignItems = alignItems
        self._alignSelf = alignSelf

        self.measure = measure

        self._parent = None
        self.children = ChildList(self)

        self._dirty = True
        self._layout = Layout()

    ######################################################################
    # Style properties
    ######################################################################

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for child in self.children:
            child.dirty = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value != self._width:
            self._width = value
            self.dirty = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value != self._height:
            self._height = value
            self.dirty = True

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value != self._position:
            self._position = value
            self.dirty = True

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        if value != self._top:
            self._top = value
            self.dirty = True

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        if value != self._bottom:
            self._bottom = value
            self.dirty = True

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if value != self._left:
            self._left = value
            self.dirty = True

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if value != self._right:
            self._right = value
            self.dirty = True

    @property
    def flexDirection(self):
        return self._flexDirection

    @flexDirection.setter
    def flexDirection(self, value):
        if value != self._flexDirection:
            self._flexDirection = value
            self.dirty = True

    @property
    def flexWrap(self):
        return self._flexWrap

    @flexWrap.setter
    def flexWrap(self, value):
        if value != self._flexWrap:
            self._flexWrap = value
            self.dirty = True

    @property
    def flex(self):
        return self._flex

    @flex.setter
    def flex(self, value):
        if value != self._flex:
            self._flex = value
            self.dirty = True

    @property
    def marginTop(self):
        return self._marginTop

    @marginTop.setter
    def marginTop(self, value):
        if value != self._marginTop:
            self._marginTop = value
            self.dirty = True

    @property
    def marginRight(self):
        return self._marginRight

    @marginRight.setter
    def marginRight(self, value):
        if value != self._marginRight:
            self._marginRight = value
            self.dirty = True

    @property
    def marginBottom(self):
        return self._marginBottom

    @marginBottom.setter
    def marginBottom(self, value):
        if value != self._marginBottom:
            self._marginBottom = value
            self.dirty = True

    @property
    def marginLeft(self):
        return self._marginLeft

    @marginLeft.setter
    def marginLeft(self, value):
        if value != self._marginLeft:
            self._marginLeft = value
            self.dirty = True

    @property
    def paddingTop(self):
        return self._paddingTop

    @paddingTop.setter
    def paddingTop(self, value):
        if value != self._paddingTop:
            self._paddingTop = value
            self.dirty = True

    @property
    def paddingRight(self):
        return self._paddingRight

    @paddingRight.setter
    def paddingRight(self, value):
        if value != self._paddingRight:
            self._paddingRight = value
            self.dirty = True

    @property
    def paddingBottom(self):
        return self._paddingBottom

    @paddingBottom.setter
    def paddingBottom(self, value):
        if value != self._paddingBottom:
            self._paddingBottom = value
            self.dirty = True

    @property
    def paddingLeft(self):
        return self._paddingLeft

    @paddingLeft.setter
    def paddingLeft(self, value):
        if value != self._paddingLeft:
            self._paddingLeft = value
            self.dirty = True


    @property
    def borderTopWidth(self):
        return self._borderTopWidth

    @borderTopWidth.setter
    def borderTopWidth(self, value):
        if value != self._borderTopWidth:
            self._borderTopWidth = value
            self.dirty = True

    @property
    def borderRightWidth(self):
        return self._borderRightWidth

    @borderRightWidth.setter
    def borderRightWidth(self, value):
        if value != self._borderRightWidth:
            self._borderRightWidth = value
            self.dirty = True

    @property
    def borderBottomWidth(self):
        return self._borderBottomWidth

    @borderBottomWidth.setter
    def borderBottomWidth(self, value):
        if value != self._borderBottomWidth:
            self._borderBottomWidth = value
            self.dirty = True

    @property
    def borderLeftWidth(self):
        return self._borderLeftWidth

    @borderLeftWidth.setter
    def borderLeftWidth(self, value):
        if value != self._borderLeftWidth:
            self._borderLeftWidth = value
            self.dirty = True


    @property
    def justifyContent(self):
        return self._justifyContent

    @justifyContent.setter
    def justifyContent(self, value):
        if value != self._justifyContent:
            self._justifyContent = value
            self.dirty = True

    @property
    def alignItems(self):
        return self._alignItems

    @alignItems.setter
    def alignItems(self, value):
        if value != self._alignItems:
            self._alignItems = value
            self.dirty = True

    @property
    def alignSelf(self):
        return self._alignSelf

    @alignSelf.setter
    def alignSelf(self, value):
        if value != self._alignSelf:
            self._alignSelf = value
            self.dirty = True

    ######################################################################
    # Style query helpers
    ######################################################################

    def dimension_is_defined(self, axis):
        value = getattr(self, dimension(axis))
        return value is not None and value > 0

    def position_is_defined(self, position):
        return getattr(self, position) is not None

    def padding_and_border(self, position):
        return getattr(self, 'padding' + position.title()) + getattr(self, 'border' + position.title() + 'Width')

    def margin(self, position):
        return getattr(self, 'margin' + position.title())

    def margin_for_axis(self, axis):
        return self.margin(leading(axis)) + self.margin(trailing(axis))

    def padding_and_border_for_axis(self, axis):
        return self.padding_and_border(leading(axis)) + self.padding_and_border(trailing(axis))

    def relative_position(self, axis):
        lead = getattr(self, leading(axis))
        if lead is not None:
            return lead
        value = getattr(self, trailing(axis))
        return -value if value is not None else 0

    def align_item(self, child):
        if child.alignSelf != AUTO:
            return child.alignSelf

        return self.alignItems

    def dimension_with_margin(self, axis):
        return getattr(self._layout, dimension(axis)) + self.margin(leading(axis)) + self.margin(trailing(axis))

    @property
    def is_flex(self):
        return self.position == RELATIVE and self.flex is not None and self.flex > 0

    def _set_dimension_from_style(self, axis):
        # The parent already computed us a width or height. We just skip it
        if getattr(self._layout, dimension(axis)) is not None:
            return

        # We only run if there's a width or height defined
        if not self.dimension_is_defined(axis):
            return

        # The dimensions can never be smaller than the padding and border
        maxLayoutDimension = max(
            getattr(self, dimension(axis)),
            self.padding_and_border_for_axis(axis)
        )
        setattr(self._layout, dimension(axis), maxLayoutDimension)

    ######################################################################
    # Calculate and retrieve layout
    ######################################################################

    @property
    def layout(self):
        if self._dirty:
            self._layout.reset()
            self._calculate_layout(None)
            self.dirty = False
        return self._layout

    def _calculate_layout(self, parent_max_width=None):
        for child in self.children:
            child._layout.reset()

        main_axis = self.flexDirection
        cross_axis = COLUMN if main_axis == ROW else ROW

        # Handle width and height style attributes
        self._set_dimension_from_style(main_axis)
        self._set_dimension_from_style(cross_axis)

        # The position is set by the parent, but we need to complete it with a
        # delta composed of the margin and left/top/right/bottom
        setattr(
            self._layout,
            leading(main_axis),
            getattr(self._layout, leading(main_axis)) + self.margin(leading(main_axis)) + self.relative_position(main_axis)
        )
        setattr(
            self._layout,
            leading(cross_axis),
            getattr(self._layout, leading(cross_axis)) + self.margin(leading(cross_axis)) + self.relative_position(cross_axis)
        )

        if self.measure:
            width = None
            if self.dimension_is_defined(ROW):
                width = self.width
            elif getattr(self._layout, dimension(ROW)) is not None:
                width = getattr(self._layout, dimension(ROW))
            else:
                try:
                    width = parent_max_width - self.margin_for_axis(ROW)
                except TypeError:
                    pass

            if width:
                width = width - self.padding_and_border_for_axis(ROW)

            # We only need to give a dimension for the text if we haven't got any
            # for it computed yet. It can either be from the style attribute or because
            # the element is flexible.
            isRowUndefined = not self.dimension_is_defined(ROW) and getattr(self._layout, dimension(ROW)) is None
            isColumnUndefined = not self.dimension_is_defined(COLUMN) and getattr(self._layout, dimension(COLUMN)) is None

            # Let's not measure the text if we already know both dimensions
            if isRowUndefined or isColumnUndefined:
                measureDim = self.measure(width)
                if (isRowUndefined):
                    self._layout.width = measureDim['width'] + self.padding_and_border_for_axis(ROW)
                if (isColumnUndefined):
                    self._layout.height = measureDim['height'] + self.padding_and_border_for_axis(COLUMN)
            return

        # Pre-fill some dimensions straight from the parent
        for i, child in enumerate(self.children):
            # Pre-fill cross axis dimensions when the child is using stretch before
            # we call the recursive layout pass
            if (self.align_item(child) == STRETCH and
                    child.position == RELATIVE and
                    getattr(self._layout, dimension(cross_axis)) is not None and
                    not child.dimension_is_defined(cross_axis)):
                setattr(
                    child._layout,
                    dimension(cross_axis),
                    max(
                        getattr(self._layout, dimension(cross_axis)) - self.padding_and_border_for_axis(cross_axis) - child.margin_for_axis(cross_axis),
                        # You never want to go smaller than padding
                        child.padding_and_border_for_axis(cross_axis)
                    )
                )

            elif child.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets for the axis are defined (either both
                # left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self._layout, dimension(axis)) is not None and
                            not child.dimension_is_defined(axis) and
                            child.position_is_defined(leading(axis)) and
                            child.position_is_defined(trailing(axis))):
                        setattr(
                            child._layout,
                            dimension(axis),
                            max(
                                getattr(self._layout, dimension(axis)) - self.padding_and_border_for_axis(axis) - child.margin_for_axis(axis) - getattr(child, leading(axis)) - getattr(child, trailing(axis)),
                                # You never want to go smaller than padding
                                child.padding_and_border_for_axis(axis)
                            )
                        )

        defined_main_dim = None
        if getattr(self._layout, dimension(main_axis)) is not None:
            defined_main_dim = getattr(self._layout, dimension(main_axis)) - self.padding_and_border_for_axis(main_axis)

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

                # It only makes sense to consider a child flexible if we have a computed
                # dimension for the self.
                if getattr(self._layout, dimension(main_axis)) is not None and child.is_flex:
                    flexible_children_count = flexible_children_count + 1
                    total_flexible = total_flexible + child.flex

                    # Even if we don't know its exact size yet, we already know the padding,
                    # border and margin. We'll use this partial information to compute the
                    # remaining space.
                    next_content_dim = child.padding_and_border_for_axis(main_axis) + child.margin_for_axis(main_axis)

                else:
                    maxWidth = None;
                    if main_axis != ROW:
                        try:
                            maxWidth = parent_max_width - self.margin_for_axis(ROW) - self.padding_and_border_for_axis(ROW)
                        except TypeError:
                            pass

                        if self.dimension_is_defined(ROW):
                            maxWidth = getattr(self._layout, dimension(ROW)) - self.padding_and_border_for_axis(ROW)

                    # This is the main recursive call. We layout non flexible children.
                    if not already_computed_next_layout:
                        child._calculate_layout(maxWidth)

                    # Absolute positioned elements do not take part of the layout, so we
                    # don't use them to compute main_content_dim
                    if child.position == RELATIVE:
                        non_flexible_children_count = non_flexible_children_count + 1
                        # At this point we know the final size and margin of the element.
                        next_content_dim = child.dimension_with_margin(main_axis)

                # The element we are about to add would make us go to the next line
                if (self.flexWrap == WRAP and
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
                remaining_main_dim = max(main_content_dim, 0) - main_content_dim

            # If there are flexible children in the mix, they are going to fill the
            # remaining space
            if flexible_children_count != 0:
                flexible_main_dim = remaining_main_dim / total_flexible

                # The non flexible children can overflow the container, in this case
                # we should just assume that there is no space available.
                if (flexible_main_dim < 0.0):
                    flexible_main_dim = 0.0

                # We iterate over the full array and only apply the action on flexible
                # children. This is faster than actually allocating a new array that
                # contains only flexible children.
                for i, child in enumerate(self.children[start_line:end_line]):
                    if child.is_flex:
                        # At this point we know the final size of the element in the main
                        # dimension
                        setattr(
                            child._layout,
                            dimension(main_axis),
                            flexible_main_dim * child.flex + child.padding_and_border_for_axis(main_axis)
                        )

                        maxWidth = None
                        if self.dimension_is_defined(ROW):
                            maxWidth = getattr(self._layout, dimension(ROW)) - self.padding_and_border_for_axis(ROW)
                        elif main_axis != ROW:
                            try:
                                maxWidth = parent_max_width - self.margin_for_axis(ROW) - self.padding_and_border_for_axis(ROW)
                            except TypeError:
                                pass

                        # And we recursively call the layout algorithm for this child
                        child._calculate_layout(maxWidth)

            # We use justifyContent to figure out how to allocate the remaining
            # space available
            else:
                justifyContent = self.justifyContent
                if justifyContent == CENTER:
                    leading_main_dim = remaining_main_dim / 2.0
                elif justifyContent == FLEX_END:
                    leading_main_dim = remaining_main_dim
                elif justifyContent == SPACE_BETWEEN:
                    remaining_main_dim = max(remaining_main_dim, 0)
                    if flexible_children_count + non_flexible_children_count - 1 != 0:
                        between_main_dim = remaining_main_dim / (flexible_children_count + non_flexible_children_count - 1)
                    else:
                        between_main_dim = 0
                elif (justifyContent == SPACE_AROUND):
                    # Space on the edges is half of the space between elements
                    between_main_dim = remaining_main_dim / (flexible_children_count + non_flexible_children_count)
                    leading_main_dim = between_main_dim / 2.0

            # <Loop C> Position elements in the main axis and compute dimensions

            # At this point, all the children have their dimensions set. We need to
            # find their position. In order to do that, we accumulate data in
            # variables that are also useful to compute the total dimensions of the
            # container!
            cross_dim = 0.0
            main_dim = leading_main_dim + self.padding_and_border(leading(main_axis))
            for child in self.children[start_line:end_line]:
                if child.position == ABSOLUTE and child.position_is_defined(leading(main_axis)):
                    # In case the child is position absolute and has left/top being
                    # defined, we override the position to whatever the user said
                    # (and margin/border).
                    setattr(
                        child._layout,
                        position(main_axis),
                        getattr(child, leading(main_axis)) + getattr(self, 'border' + leading(main_axis).title() + 'Width') + child.margin(leading(main_axis))
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
                    main_dim = main_dim + between_main_dim + child.dimension_with_margin(main_axis)
                    # The cross dimension is the max of the elements dimension since there
                    # can only be one element in that cross dimension.
                    cross_dim = max(cross_dim, child.dimension_with_margin(cross_axis))

            containerMainAxis = getattr(self._layout, dimension(main_axis))
            # If the user didn't specify a width or height, and it has not been set
            # by the container, then we set it via the children.
            if containerMainAxis is None:
                containerMainAxis = max(
                    # We're missing the last padding at this point to get the final
                    # dimension
                    main_dim + self.padding_and_border(trailing(main_axis)),
                    # We can never assign a width smaller than the padding and borders
                    self.padding_and_border_for_axis(main_axis)
                )

            containerCrossAxis = getattr(self._layout, dimension(cross_axis))
            if getattr(self._layout, dimension(cross_axis)) is None:
                containerCrossAxis = max(
                    # For the cross dim, we add both sides at the end because the value
                    # is aggregate via a max function. Intermediate negative values
                    # can mess this computation otherwise
                    cross_dim + self.padding_and_border_for_axis(cross_axis),
                    self.padding_and_border_for_axis(cross_axis)
                )

            # <Loop D> Position elements in the cross axis

            for child in self.children[start_line:end_line]:
                if child.position == ABSOLUTE and child.position_is_defined(leading(cross_axis)):
                    # In case the child is absolutely positionned and has a
                    # top/left/bottom/right being set, we override all the previously
                    # computed positions to set it correctly.
                    setattr(
                        child._layout,
                        position(cross_axis),
                        getattr(child, leading(cross_axis)) + getattr(self, 'border' + leading(cross_axis).title() + 'Width') + child.margin(leading(cross_axis))
                    )

                else:
                    leadingCrossDim = self.padding_and_border(leading(cross_axis))

                    # For a relative children, we're either using alignItems (parent) or
                    # alignSelf (child) in order to determine the position in the cross axis
                    if child.position == RELATIVE:
                        alignItem = self.align_item(child)
                        if alignItem == STRETCH:
                            # You can only stretch if the dimension has not already been set
                            # previously.
                            if not child.dimension_is_defined(cross_axis):
                                setattr(
                                    child._layout,
                                    dimension(cross_axis),
                                    max(
                                        containerCrossAxis - self.padding_and_border_for_axis(cross_axis) - child.margin_for_axis(cross_axis),
                                        # You never want to go smaller than padding
                                        child.padding_and_border_for_axis(cross_axis)
                                    )
                                )
                        elif alignItem != FLEX_START:
                            # The remaining space between the parent dimensions+padding and child
                            # dimensions+margin.
                            remainingCrossDim = containerCrossAxis - self.padding_and_border_for_axis(cross_axis) - child.dimension_with_margin(cross_axis)

                            if alignItem == CENTER:
                                leadingCrossDim = leadingCrossDim + remainingCrossDim / 2
                            else: # FLEX_END
                                leadingCrossDim = leadingCrossDim + remainingCrossDim

                    # And we apply the position
                    setattr(
                        child._layout,
                        position(cross_axis),
                        getattr(child._layout, position(cross_axis)) + lines_cross_dim + leadingCrossDim
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
                    lines_main_dim + self.padding_and_border(trailing(main_axis)),
                    # We can never assign a width smaller than the padding and borders
                    self.padding_and_border_for_axis(main_axis)
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
                    lines_cross_dim + self.padding_and_border_for_axis(cross_axis),
                    self.padding_and_border_for_axis(cross_axis)
                )
            )

        # <Loop E> Calculate dimensions for absolutely positioned elements
        for child in self.children:
            if child.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets for the axis are defined (either both
                # left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self._layout, dimension(axis)) is not None and
                            not child.dimension_is_defined(axis) and
                            child.position_is_defined(leading(axis)) and
                            child.position_is_defined(trailing(axis))):
                        setattr(
                            child._layout,
                            dimension(axis),
                            max(
                                getattr(self._layout, dimension(axis)) - self.padding_and_border_for_axis(axis) - child.margin_for_axis(axis) - getattr(child, leading(axis)) - getattr(child, trailing(axis)),
                                # You never want to go smaller than padding
                                child.padding_and_border_for_axis(axis)
                            )
                        )
                for axis in [ROW, COLUMN]:
                    if child.position_is_defined(trailing(axis)) and not child.position_is_defined(leading(axis)):
                        setattr(
                            child._layout,
                            leading(axis),
                            getattr(self._layout, dimension(axis)) - getattr(child._layout, dimension(axis)) - getattr(child, trailing(axis))
                        )

