
class Size:
    """Representation of the size of a node in the DOM.

    Whenever a size attribute is altered, it marks the
    layout of the node as dirty.

    width: The width of the node.
    height: The height of the node.
    exact_width: If True, the width is exact. If False,
        the width is the minimum allowed width.
    exact_height: If True, the height is exact. If False,
        the height is the minimum allowed width.
    ratio: The height between height and width. width = height * ratio
    """
    def __init__(self, node):
        self._node = node
        self._width = None
        self._height = None
        self._exact_width = True
        self._exact_height = True

        self._ratio = None
        self._is_replaced = False

    @property
    def dirty(self):
        return self._node.layout.dirty

    @dirty.setter
    def dirty(self, value):
        self._node.layout.dirty = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._width != value:
            self._width = value
            self.dirty = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._height != value:
            self._height = value
            self.dirty = True

    @property
    def exact_width(self):
        return self._exact_width

    @exact_width.setter
    def exact_width(self, value):
        if self._exact_width != value:
            self._exact_width = value
            self.dirty = True

    @property
    def exact_height(self):
        return self._exact_height

    @exact_height.setter
    def exact_height(self, value):
        if self._exact_height != value:
            self._exact_height = value
            self.dirty = True

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        if self._ratio != value:
            self._ratio = value
            self.dirty = True

    @property
    def is_replaced(self):
        return self._is_replaced

    @is_replaced.setter
    def is_replaced(self, value):
        if self._is_replaced != value:
            self._is_replaced = value
            self.dirty = True


class Box:
    """Describe the layout of a box displaying a node in the DOM.

    Stored properties
    ~~~~~~~~~~~~~~~~~
    visible: The node is included in rendering, and is visible. A value of
        False indicates the node takes up space, but is not rendered.

    content_width: The width of the content box
    content_height: The height of the content box
    content_top: The top position of the content box, relative to the block container
    content_left: The left position of the content box, relative to the block container

    origin_top: The absolute position of the top of the block container
    origin_left: The absolute position of the left of the block container

    margin_top: The top margin of the box
    margin_right: The right margin of the box
    margin_bottom: The bottom margin of the box
    margin_left: The left margin of the box

    collapse_top: The top-most extent of the collapsed margin box.
    collapse_right: The right-most extent of the collapsed margin box.
    collapse_bottom: The bottom-most extent of the collapsed margin box.
    collapse_left: The left-most extent of the collapsed margin box.

    padding_top: The top padding of the box
    padding_right: The right padding of the box
    padding_bottom: The bottom padding of the box
    padding_left: The left padding of the box

    border_top_width: The width of the top border of the box
    border_right_width: The width of the right border of the box
    border_bottom_width: The width of the bottom border of the box
    border_left_width: The width of the left border of the box

    Computed properties
    ~~~~~~~~~~~~~~~~~~~
    border_box_width: The width of the border box.
    border_box_height: The height of the border box.
    border_box_top: The position of the top of the border box, relative to the block container.
    border_box_right: The position of the right of the border box, relative to the block container.
    border_box_bottom: The position of the bottom of the border box, relative to the block container.
    border_box_left: The position of the left of the border box, relative to the block container.
    absolute_border_box_top: The absolute position of the top of the border box.
    absolute_border_box_right: The absolute position of the right of the border box.
    absolute_border_box_bottom: The absolute position of the bottom of the border box.
    absolute_border_box_left: The absolute position of the left of the border box.

    padding_box_width: The width of the padding box.
    padding_box_height: The height of the padding box.
    padding_box_top: The position of the top of the padding box, relative to the block container.
    padding_box_right: The position of the right of the padding box, relative to the block container.
    padding_box_bottom: The position of the bottom of the padding box, relative to the block container.
    padding_box_left: The position of the left of the padding box, relative to the block container.
    absolute_padding_box_top: The absolute position of the top of the padding box.
    absolute_padding_box_right: The absolute position of the right of the padding box.
    absolute_padding_box_bottom: The absolute position of the bottom of the padding box.
    absolute_padding_box_left: The absolute position of the left of the padding box.

    content_bottom: The bottom position of the box, relative to the block container
    content_right: The right position of the box, relative to the block container

    absolute_content_top: The absolute position of the top of the content box.
    absolute_content_left: The absolute position of the top of the content box.
    absolute_content_bottom: The bottom position of the box, relative to the block container
    absolute_content_right: The right position of the box, relative to the block container

    """
    def __init__(self, node):
        self.node = node
        self._reset()

    def __repr__(self):
        return '<Box (%sx%s @ %s,%s)>' % (
            self.content_width, self.content_height,
            self.absolute_content_left, self.absolute_content_top,
        )

    # def __eq__(self, value):
    #     return all([
    #         self._width == value._width,
    #         self._height == value._height,
    #         self._absolute_margin_top == value._absolute_margin_top,
    #         self._absolute_margin_left == value._absolute_margin_left
    #     ])

    def _reset(self):
        # Some properties describing whether this node exists in
        # layout *at all*.
        self.visible = True

        # Set the core properties directly;
        # this primes storage for the later calculations

        # Width and height of the content box.
        self.content_width = 0
        self.content_height = 0

        # Box position, relative to the containing box
        self._content_top = 0
        self._content_left = 0

        # Set and initial value for the origin that is
        # guaranteed to be != any actual value
        self.__origin_top = None
        self.__origin_left = None

        # Margins of the box
        self._margin_top = 0
        self._margin_right = 0
        self._margin_bottom = 0
        self._margin_left = 0

        # Collapse extents of the box
        self._collapse_top = 0
        self._collapse_right = 0
        self._collapse_bottom = 0
        self._collapse_left = 0

        # Border of the box
        self.border_top_width = 0
        self.border_right_width = 0
        self.border_bottom_width = 0
        self.border_left_width = 0

        # Padding of the box
        self.padding_top = 0
        self.padding_right = 0
        self.padding_bottom = 0
        self.padding_left = 0

        # Current state of layout calculations
        self._dirty = True

        # Set the origin via properties; this forces the calculation of
        # absolute positions.
        self._origin_top = 0
        self._origin_left = 0

    def reset(self):
        self._reset()
        for child in self.node.children:
            if child.layout:
                child.layout.reset()

    ######################################################################
    # Origin handling
    ######################################################################
    @property
    def _origin_top(self):
        return self.__origin_top

    @_origin_top.setter
    def _origin_top(self, value):
        if value != self.__origin_top:
            self.__origin_top = value
            for child in self.node.children:
                if child.layout:
                    child.layout._origin_top = self.absolute_content_top

    @property
    def _origin_left(self):
        return self.__origin_left

    @_origin_left.setter
    def _origin_left(self, value):
        if value != self.__origin_left:
            self.__origin_left = value
            for child in self.node.children:
                if child.layout:
                    child.layout._origin_left = self.absolute_content_left

    ######################################################################
    # Core properties
    ######################################################################
    @property
    def content_top(self):
        return self._content_top

    @content_top.setter
    def content_top(self, value):
        if value != self._content_top:
            self._content_top = value
            for child in self.node.children:
                if child.layout:
                    child.layout._origin_top = self.absolute_content_top

    @property
    def content_left(self):
        return self._content_left

    @content_left.setter
    def content_left(self, value):
        if value != self._content_left:
            self._content_left = value
            for child in self.node.children:
                if child.layout:
                    child.layout._origin_left = self.absolute_content_left

    @property
    def margin_top(self):
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        if value != self._margin_top:
            self._margin_top = value
            self.collapse_top = value

    @property
    def margin_right(self):
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value):
        if value != self._margin_right:
            self._margin_right = value
            self.collapse_right = value

    @property
    def margin_bottom(self):
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value):
        if value != self._margin_bottom:
            self._margin_bottom = value
            self.collapse_bottom = value

    @property
    def margin_left(self):
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value):
        if value != self._margin_left:
            self._margin_left = value
            self.collapse_left = value

    @property
    def collapse_top(self):
        return self._collapse_top

    @collapse_top.setter
    def collapse_top(self, value):
        if isinstance(value, int) and value > self._collapse_top:
            self._collapse_top = value

    @property
    def collapse_right(self):
        return self._collapse_right

    @collapse_right.setter
    def collapse_right(self, value):
        if isinstance(value, int) and value > self._collapse_right:
            self._collapse_right = value

    @property
    def collapse_bottom(self):
        return self._collapse_bottom

    @collapse_bottom.setter
    def collapse_bottom(self, value):
        if isinstance(value, int) and value > self._collapse_bottom:
            self._collapse_bottom = value

    @property
    def collapse_left(self):
        return self._collapse_left

    @collapse_left.setter
    def collapse_left(self, value):
        if isinstance(value, int) and value > self._collapse_left:
            self._collapse_left = value

    ######################################################################
    # Border box dimensions
    ######################################################################
    @property
    def border_box_top(self):
        return self._content_top - self.padding_top - self.border_top_width

    @property
    def border_box_right(self):
        return (
            self._content_left
            + self.content_width
            + self.padding_right
            + self.border_right_width
        )

    @property
    def border_box_bottom(self):
        return (
            self._content_top
            + self.content_height
            + self.padding_bottom
            + self.border_bottom_width
        )

    @property
    def border_box_left(self):
        return self._content_left - self.padding_left - self.border_left_width

    @property
    def border_box_width(self):
        return (
            self.border_left_width
            + self.padding_left
            + self.content_width
            + self.padding_right
            + self.border_right_width
        )

    @property
    def border_box_height(self):
        return (
            self.border_top_width
            + self.padding_top
            + self.content_height
            + self.padding_bottom
            + self.border_bottom_width
        )

    @property
    def absolute_border_box_top(self):
        return (
            self.__origin_top + self._content_top
            - self.padding_top
            - self.border_top_width
        )

    @property
    def absolute_border_box_right(self):
        return (
            self.__origin_left + self._content_left
            + self.content_width
            + self.padding_right
            + self.border_right_width
        )

    @property
    def absolute_border_box_bottom(self):
        return (
            self.__origin_top + self._content_top
            + self.content_height
            + self.padding_bottom
            + self.border_bottom_width
        )

    @property
    def absolute_border_box_left(self):
        return (
            self.__origin_left + self._content_left
            - self.padding_left
            - self.border_left_width
        )

    ######################################################################
    # Padding box dimensions
    ######################################################################
    @property
    def padding_box_top(self):
        return self._content_top - self.padding_top

    @property
    def padding_box_right(self):
        return self._content_left + self.content_width + self.padding_right

    @property
    def padding_box_bottom(self):
        return self._content_top + self.content_height + self.padding_bottom

    @property
    def padding_box_left(self):
        return self._content_left - self.padding_left

    @property
    def padding_box_width(self):
        return self.padding_left + self.content_width + self.padding_right

    @property
    def padding_box_height(self):
        return self.padding_top + self.content_height + self.padding_bottom

    @property
    def absolute_padding_box_top(self):
        return self.__origin_top + self._content_top - self.padding_top

    @property
    def absolute_padding_box_right(self):
        return self.__origin_left + self._content_left + self.content_width + self.padding_right

    @property
    def absolute_padding_box_bottom(self):
        return self.__origin_top + self._content_top + self.content_height + self.padding_bottom

    @property
    def absolute_padding_box_left(self):
        return self.__origin_left + self._content_left - self.padding_left

    ######################################################################
    # Content box dimensions
    ######################################################################
    @property
    def content_bottom(self):
        return self._content_top + self.content_height

    @property
    def content_right(self):
        return self._content_left + self.content_width

    @property
    def absolute_content_top(self):
        return self.__origin_top + self._content_top

    @property
    def absolute_content_right(self):
        return self.__origin_left + self._content_left + self.content_width

    @property
    def absolute_content_bottom(self):
        return self.__origin_top + self._content_top + self.content_height

    @property
    def absolute_content_left(self):
        return self.__origin_left + self._content_left

    ######################################################################
    # Layout dirtiness tracking.
    #
    # If dirty == True, the layout is known to be invalid.
    # If dirty == False, the layout is known to be good.
    # If dirty is None, the layout is currently being evaluated.
    ######################################################################
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        if value != self._dirty:
            self._dirty = value
            for child in self.node.children:
                if child.layout:
                    child.layout.dirty = value
