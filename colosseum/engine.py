from .constants import (
    ABSOLUTE, RELATIVE,
    ROW, COLUMN,
    FLEX_START, FLEX_END,
    AUTO, CENTER, STRETCH, SPACE_BETWEEN, SPACE_AROUND,
    WRAP
)
from .utils import dimension, leading, position, trailing


class Layout:
    def __init__(self, node, width=None, height=None, top=0, left=0):
        self.node = node
        self.width = width
        self.height = height
        self.top = top
        self.left = left

        self._dirty = True

    def __repr__(self):
        return '<Layout (%sx%s @ %s,%s)>' % (self.width, self.height, self.left, self.top)

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

    ######################################################################
    # Layout dirtiness tracking.
    #
    # If dirty == True, the layout is known to be invalid.
    # If dirty == False, the layout is known to be good.
    # If dirty is None, the layout is currently being re-evaluated.
    ######################################################################
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for child in self.node.children:
            child.layout.dirty = value


######################################################################
# Internal helpers for computing layout
######################################################################

def dimension_is_defined(style, axis):
    value = getattr(style, dimension(axis))
    return value is not None and value > 0


def position_is_defined(style, position):
    return getattr(style, position) is not None


def padding_and_border(style, position):
    return getattr(style, 'padding_' + position) + getattr(style, 'border_' + position + '_width')


def padding_and_border_for_axis(style, axis):
    return padding_and_border(style, leading(axis)) + padding_and_border(style, trailing(axis))


def margin_for_axis(style, axis):
    return getattr(style, 'margin_' + leading(axis)) + getattr(style, 'margin_' + trailing(axis))


def is_flex(style):
    return style.position == RELATIVE and style.flex is not None and style.flex > 0


def bound_axis(style, axis, value):
    minValue = {
        ROW: style.min_width,
        COLUMN: style.min_height,
    }[axis]

    maxValue = {
        ROW: style.max_width,
        COLUMN: style.max_height,
    }[axis]

    boundValue = value
    if maxValue is not None and maxValue >= 0 and boundValue > maxValue:
        boundValue = maxValue

    if minValue is not None and minValue >= 0 and boundValue < minValue:
        boundValue = minValue

    return boundValue


def dimension_with_margin(node, axis):
    return (
        getattr(node.layout, dimension(axis)) +
        getattr(node.style, 'margin_' + leading(axis)) +
        getattr(node.style, 'margin_' + trailing(axis))
    )


def align_item(style, child_style):
    if child_style.align_self != AUTO:
        return child_style.align_self

    return style.align_items


def relative_position(style, axis):
    lead = getattr(style, leading(axis))
    if lead is not None:
        return lead
    value = getattr(style, trailing(axis))
    return -value if value is not None else 0


def set_dimension_from_style(node, style, axis):
    # The parent already computed us a width or height. We just skip it
    if getattr(node.layout, dimension(axis)) is not None:
        return

    # We only run if there's a width or height defined
    if not dimension_is_defined(style, axis):
        return

    # The dimensions can never be smaller than the padding and border
    maxLayoutDimension = max(
        bound_axis(style, axis, getattr(style, dimension(axis))),
        padding_and_border_for_axis(style, axis)
    )
    setattr(node.layout, dimension(axis), maxLayoutDimension)


class BoxModelEngine:
    def __init__(self, node):
        super().__init__()
        self.node = node

    def compute(self, parent_max_width=None):
        for child in self.node.children:
            child.layout.reset()

        main_axis = self.node.style.flex_direction
        cross_axis = COLUMN if main_axis == ROW else ROW

        # Handle width and height style attributes
        set_dimension_from_style(self.node, self.node.style, main_axis)
        set_dimension_from_style(self.node, self.node.style, cross_axis)

        # The position is set by the parent, but we need to complete it with a
        # delta composed of the margin and left/top/right/bottom
        setattr(
            self.node.layout,
            leading(main_axis),
            (
                getattr(self.node.layout, leading(main_axis)) +
                getattr(self.node.style, 'margin_' + leading(main_axis)) +
                relative_position(self.node.style, main_axis)
            )
        )
        setattr(
            self.node.layout,
            leading(cross_axis),
            (
                getattr(self.node.layout, leading(cross_axis)) +
                getattr(self.node.style, 'margin_' + leading(cross_axis)) +
                relative_position(self.node.style, cross_axis)
            )
        )

        if self.node.style.measure:
            width = None
            if dimension_is_defined(self.node.style, ROW):
                width = self.node.style.width
            elif getattr(self.node.layout, dimension(ROW)) is not None:
                width = getattr(self.node.layout, dimension(ROW))
            else:
                try:
                    width = parent_max_width - margin_for_axis(self.node.style, ROW)
                except TypeError:
                    pass

            if width:
                width = width - padding_and_border_for_axis(self.node.style, ROW)

            # We only need to give a dimension for the text if we haven't got any
            # for it computed yet. It can either be from the style attribute or because
            # the element is flexible.
            row_undefined = not dimension_is_defined(self.node.style, ROW) and getattr(self.node.layout, dimension(ROW)) is None
            column_undefined = (
                not dimension_is_defined(self.node.style, COLUMN)
                and getattr(self.node.layout, dimension(COLUMN)) is None
            )

            # Let's not measure the text if we already know both dimensions
            if row_undefined or column_undefined:
                measureDim = self.node.style.measure(width)
                if row_undefined:
                    self.node.layout.width = measureDim['width'] + padding_and_border_for_axis(self.node.style, ROW)
                if column_undefined:
                    self.node.layout.height = measureDim['height'] + padding_and_border_for_axis(self.node.style, COLUMN)
            return

        # Pre-fill some dimensions straight from the parent
        for i, child in enumerate(self.node.children):
            # Pre-fill cross axis dimensions when the child is using stretch before
            # we call the recursive layout pass
            if (align_item(self.node.style, child.style) == STRETCH and
                    child.style.position == RELATIVE and
                    getattr(self.node.layout, dimension(cross_axis)) is not None and
                    not dimension_is_defined(child.style, cross_axis)):
                setattr(
                    child.layout,
                    dimension(cross_axis),
                    max(
                        bound_axis(
                            child.style,
                            cross_axis,
                            getattr(self.node.layout, dimension(cross_axis))
                            - padding_and_border_for_axis(self.node.style, cross_axis)
                            - margin_for_axis(child.style, cross_axis)
                        ),
                        # You never want to go smaller than padding
                        padding_and_border_for_axis(child.style, cross_axis)
                    )
                )

            elif child.style.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets
                # for the axis are defined (either both left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self.node.layout, dimension(axis)) is not None and
                            not dimension_is_defined(child.style, axis) and
                            position_is_defined(child.style, leading(axis)) and
                            position_is_defined(child.style, trailing(axis))):
                        setattr(
                            child.layout,
                            dimension(axis),
                            max(
                                bound_axis(
                                    child.style,
                                    axis,
                                    getattr(self.node.layout, dimension(axis))
                                    - padding_and_border_for_axis(self.node.style, axis)
                                    - margin_for_axis(child.style, axis)
                                    - getattr(child.style, leading(axis))
                                    - getattr(child.style, trailing(axis))
                                ),
                                # You never want to go smaller than padding
                                padding_and_border_for_axis(child.style, axis)
                            )
                        )

        defined_main_dim = None
        if getattr(self.node.layout, dimension(main_axis)) is not None:
            defined_main_dim = (
                getattr(self.node.layout, dimension(main_axis)) -
                padding_and_border_for_axis(self.node.style, main_axis)
            )

        # We want to execute the next two loops one per line with flex-wrap
        start_line = 0
        end_line = 0
        # int nextOffset = 0;
        already_computed_next_layout = False
        # We aggregate the total dimensions of the container in those two variables
        lines_cross_dim = 0.0
        lines_main_dim = 0.0

        while end_line < len(self.node.children):
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

            for i, child in enumerate(self.node.children[start_line:]):
                next_content_dim = 0

                # If it's a flexible child, accumulate the size that the child potentially
                # contributes to the row
                if is_flex(child.style):
                    flexible_children_count = flexible_children_count + 1
                    total_flexible = total_flexible + child.style.flex

                    # Even if we don't know its exact size yet, we already know the padding,
                    # border and margin. We'll use this partial information, which represents
                    # the smallest possible size for the child, to compute the remaining
                    # available space.
                    next_content_dim = (
                        padding_and_border_for_axis(child.style, main_axis) +
                        margin_for_axis(child.style, main_axis)
                    )

                else:
                    max_width = None
                    if main_axis != ROW:
                        try:
                            max_width = (
                                parent_max_width -
                                margin_for_axis(self.node.style, ROW) -
                                padding_and_border_for_axis(self.node.style, ROW)
                            )
                        except TypeError:
                            pass

                        if dimension_is_defined(self.node.style, ROW):
                            max_width = (
                                getattr(self.node.layout, dimension(ROW)) -
                                padding_and_border_for_axis(self.node.style, ROW)
                            )

                    # This is the main recursive call. We layout non flexible children.
                    if not already_computed_next_layout:
                        child.style.apply(max_width)

                    # Absolute positioned elements do not take part of the layout, so we
                    # don't use them to compute main_content_dim
                    if child.style.position == RELATIVE:
                        non_flexible_children_count = non_flexible_children_count + 1
                        # At this point we know the final size and margin of the element.
                        next_content_dim = dimension_with_margin(child, main_axis)

                # The element we are about to add would make us go to the next line
                if (self.node.style.flex_wrap == WRAP and
                        getattr(self.node.layout, dimension(main_axis)) is not None and
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
            if getattr(self.node.layout, dimension(main_axis)) is not None:
                remaining_main_dim = defined_main_dim - main_content_dim
            else:
                remaining_main_dim = bound_axis(
                    self.node.style, main_axis, max(main_content_dim, 0)
                ) - main_content_dim

            # If there are flexible children in the mix, they are going to fill the
            # remaining space
            if flexible_children_count != 0:
                flexible_main_dim = remaining_main_dim / total_flexible

                # Iterate over every child in the axis. If the flex share of remaining
                # space doesn't meet min/max bounds, remove this child from flex
                # calculations.
                for child in self.node.children[start_line:end_line]:
                    if is_flex(child.style):
                        base_main_dim = (
                            flexible_main_dim * child.style.flex +
                            padding_and_border_for_axis(child.style, main_axis)
                        )
                        bound_main_dim = bound_axis(child.style, main_axis, base_main_dim)

                        if base_main_dim != bound_main_dim:
                            remaining_main_dim = remaining_main_dim - bound_main_dim
                            total_flexible = total_flexible - child.style.flex

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
                for child in self.node.children[start_line:end_line]:
                    if is_flex(child.style):
                        # At this point we know the final size of the element in the main
                        # dimension
                        setattr(
                            child.layout,
                            dimension(main_axis),
                            bound_axis(
                                child.style,
                                main_axis,
                                (
                                    flexible_main_dim * child.style.flex +
                                    padding_and_border_for_axis(child.style, main_axis)
                                )
                            )
                        )

                        max_width = None
                        if dimension_is_defined(self.node.style, ROW):
                            max_width = (
                                getattr(self.node.layout, dimension(ROW)) -
                                padding_and_border_for_axis(self.node.style, ROW)
                            )
                        elif main_axis != ROW:
                            try:
                                max_width = (
                                    parent_max_width -
                                    margin_for_axis(self.node.style, ROW) -
                                    padding_and_border_for_axis(self.node.style, ROW)
                                )
                            except TypeError:
                                pass

                        # And we recursively call the layout algorithm for this child
                        child.style.apply(max_width)

            # We use justify_content to figure out how to allocate the remaining
            # space available
            else:
                justify_content = self.node.style.justify_content
                if justify_content == CENTER:
                    leading_main_dim = remaining_main_dim / 2.0
                elif justify_content == FLEX_END:
                    leading_main_dim = remaining_main_dim
                elif justify_content == SPACE_BETWEEN:
                    remaining_main_dim = max(remaining_main_dim, 0)
                    if flexible_children_count + non_flexible_children_count - 1 != 0:
                        between_main_dim = remaining_main_dim / (
                            flexible_children_count + non_flexible_children_count - 1
                        )
                    else:
                        between_main_dim = 0
                elif justify_content == SPACE_AROUND:
                    # Space on the edges is half of the space between elements
                    between_main_dim = remaining_main_dim / (
                        flexible_children_count + non_flexible_children_count
                    )
                    leading_main_dim = between_main_dim / 2.0

            # <Loop C> Position elements in the main axis and compute dimensions

            # At this point, all the children have their dimensions set. We need to
            # find their position. In order to do that, we accumulate data in
            # variables that are also useful to compute the total dimensions of the
            # container!
            cross_dim = 0.0
            main_dim = leading_main_dim + padding_and_border(self.node.style, leading(main_axis))
            for child in self.node.children[start_line:end_line]:
                if child.style.position == ABSOLUTE and position_is_defined(child.style, leading(main_axis)):
                    # In case the child is position absolute and has left/top being
                    # defined, we override the position to whatever the user said
                    # (and margin/border).
                    setattr(
                        child.layout,
                        position(main_axis),
                        (
                            getattr(child.style, leading(main_axis)) +
                            getattr(self.node.style, 'border_' + leading(main_axis) + '_width') +
                            getattr(child.style, 'margin_' + leading(main_axis))
                        )
                    )
                else:
                    # If the child is position absolute (without top/left) or relative,
                    # we put it at the current accumulated offset.
                    setattr(
                        child.layout,
                        position(main_axis),
                        getattr(child.layout, position(main_axis)) + main_dim
                    )

                # Now that we placed the element, we need to update the variables
                # We only need to do that for relative elements. Absolute elements
                # do not take part in that phase.
                if child.style.position == RELATIVE:
                    # The main dimension is the sum of all the elements dimension plus
                    # the spacing.
                    main_dim = main_dim + between_main_dim + dimension_with_margin(child, main_axis)
                    # The cross dimension is the max of the elements dimension since there
                    # can only be one element in that cross dimension.
                    cross_dim = max(
                        cross_dim,
                        bound_axis(
                            child.style,
                            cross_axis,
                            dimension_with_margin(child, cross_axis)
                        )
                    )

            container_main_axis = getattr(self.node.layout, dimension(main_axis))
            # If the user didn't specify a width or height, and it has not been set
            # by the container, then we set it via the children.
            if container_main_axis is None:
                container_main_axis = max(
                    # We're missing the last padding at this point to get the final
                    # dimension
                    bound_axis(
                        self.node.style,
                        main_axis,
                        main_dim + padding_and_border(self.node.style, trailing(main_axis))
                    ),
                    # We can never assign a width smaller than the padding and borders
                    padding_and_border_for_axis(self.node.style, main_axis)
                )

            container_cross_axis = getattr(self.node.layout, dimension(cross_axis))
            if getattr(self.node.layout, dimension(cross_axis)) is None:
                container_cross_axis = max(
                    # For the cross dim, we add both sides at the end because the value
                    # is aggregate via a max function. Intermediate negative values
                    # can mess this computation otherwise
                    bound_axis(
                        self.node.style,
                        cross_axis,
                        cross_dim + padding_and_border_for_axis(self.node.style, cross_axis)
                    ),
                    padding_and_border_for_axis(self.node.style, cross_axis)
                )

            # <Loop D> Position elements in the cross axis
            for child in self.node.children[start_line:end_line]:
                if child.style.position == ABSOLUTE and position_is_defined(child.style, leading(cross_axis)):
                    # In case the child is absolutely positionned and has a
                    # top/left/bottom/right being set, we override all the previously
                    # computed positions to set it correctly.
                    setattr(
                        child.layout,
                        position(cross_axis),
                        (
                            getattr(child.style, leading(cross_axis)) +
                            getattr(self.node.style, 'border_' + leading(cross_axis) + '_width') +
                            getattr(child.style, 'margin_' + leading(cross_axis))
                        )
                    )

                else:
                    leading_cross_dim = padding_and_border(self.node.style, leading(cross_axis))

                    # For a relative children, we're either using align_items (parent) or
                    # align_self (child) in order to determine the position in the cross axis
                    if child.style.position == RELATIVE:
                        item_alignment = align_item(self.node.style, child.style)
                        if item_alignment == STRETCH:
                            # You can only stretch if the dimension has not already been set
                            # previously.
                            if not dimension_is_defined(child.style, cross_axis):
                                setattr(
                                    child.layout,
                                    dimension(cross_axis),
                                    max(
                                        bound_axis(
                                            child.style,
                                            cross_axis,
                                            (
                                                container_cross_axis -
                                                padding_and_border_for_axis(self.node.style, cross_axis) -
                                                margin_for_axis(child.style, cross_axis)
                                            )
                                        ),
                                        # You never want to go smaller than padding
                                        padding_and_border_for_axis(child.style, cross_axis)
                                    )
                                )

                        elif item_alignment != FLEX_START:
                            # The remaining space between the parent dimensions+padding and child
                            # dimensions+margin.
                            remaining_cross_dim = (
                                container_cross_axis -
                                padding_and_border_for_axis(self.node.style, cross_axis) -
                                dimension_with_margin(child, cross_axis)
                            )

                            if item_alignment == CENTER:
                                leading_cross_dim = leading_cross_dim + remaining_cross_dim / 2
                            else:  # FLEX_END
                                leading_cross_dim = leading_cross_dim + remaining_cross_dim

                    # And we apply the position
                    setattr(
                        child.layout,
                        position(cross_axis),
                        (
                            getattr(child.layout, position(cross_axis)) +
                            lines_cross_dim +
                            leading_cross_dim
                        )
                    )

            lines_cross_dim = lines_cross_dim + cross_dim
            lines_main_dim = max(lines_main_dim, main_dim)
            start_line = end_line

        # If the user didn't specify a width or height, and it has not been set
        # by the container, then we set it via the children.
        if getattr(self.node.layout, dimension(main_axis)) is None:
            setattr(
                self.node.layout,
                dimension(main_axis),
                max(
                    # We're missing the last padding at this point to get the final
                    # dimension
                    bound_axis(
                        self.node.style,
                        main_axis,
                        lines_main_dim + padding_and_border(self.node.style, trailing(main_axis))
                    ),
                    # We can never assign a width smaller than the padding and borders
                    padding_and_border_for_axis(self.node.style, main_axis)
                )
            )

        if getattr(self.node.layout, dimension(cross_axis)) is None:
            setattr(
                self.node.layout,
                dimension(cross_axis),
                max(
                    # For the cross dim, we add both sides at the end because the value
                    # is aggregate via a max function. Intermediate negative values
                    # can mess this computation otherwise
                    bound_axis(
                        self.node.style,
                        cross_axis,
                        lines_cross_dim + padding_and_border_for_axis(self.node.style, cross_axis)
                    ),
                    padding_and_border_for_axis(self.node.style, cross_axis)
                )
            )

        # <Loop E> Calculate dimensions for absolutely positioned elements
        for child in self.node.children:
            if child.style.position == ABSOLUTE:
                # Pre-fill dimensions when using absolute position and both offsets
                # for the axis are defined (either both left and right or top and bottom).
                for axis in [ROW, COLUMN]:
                    if (getattr(self.node.layout, dimension(axis)) is not None and
                            not dimension_is_defined(child.style, axis) and
                            position_is_defined(child.style, leading(axis)) and
                            position_is_defined(child.style, trailing(axis))):
                        setattr(
                            child.layout,
                            dimension(axis),
                            max(
                                bound_axis(
                                    child.style,
                                    axis,
                                    (
                                        getattr(self.node.layout, dimension(axis)) -
                                        padding_and_border_for_axis(self.node.style, axis) -
                                        margin_for_axis(child.style, axis) -
                                        getattr(child.style, leading(axis)) -
                                        getattr(child.style, trailing(axis))
                                    )
                                ),
                                # You never want to go smaller than padding
                                padding_and_border_for_axis(child.style, axis)
                            )
                        )
                for axis in [ROW, COLUMN]:
                    if (position_is_defined(child.style, trailing(axis))
                            and not position_is_defined(child.style, leading(axis))):
                        setattr(
                            child.layout,
                            leading(axis),
                            (
                                getattr(self.node.layout, dimension(axis)) -
                                getattr(child.layout, dimension(axis)) -
                                getattr(child.style, trailing(axis))
                            )
                        )
