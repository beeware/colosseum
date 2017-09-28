from .constants import (
    BLOCK, LIST_ITEM, TABLE,
    INLINE, INLINE_TABLE, INLINE_BLOCK
)

class Size:
    """Representation of the size of a node in the DOM.

    Whenever a size attribute is altered, it marks the
    layout of the node as dirty.

    width: The width of the node.
    height: The height of the node.
    """
    def __init__(self, node):
        self._node = node
        self._width = None
        self._height = None

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


class Box:
    """Describe the layout of a box displaying a node in the DOM.

    Stored properties
    ~~~~~~~~~~~~~~~~~
    width: The content width of the box
    height: The content height of the box
    top: The top position of the content box, relative to the containing block
    left: The left position of the content box, relative to the containing block

    origin_top: The absolute position of the top of the containing block
    origin_left: The absolute position of the left of the containing block

    Computed properties
    ~~~~~~~~~~~~~~~~~~~
    Computed properties are automatically updated whenever a stored
    property changes.

    bottom: The bottom position of the box, relative to the containing box
    right: The right position of the box, relative to the containing box
    absolute_top: The absolute position of the top of the box.
    absolute_left: The absolute position of the left of the box.

    """
    def __init__(self, node, width=10, height=16, top=0, left=0):
        self.node = node

        # Set the core properties directly;
        # this primes storage for the later calculations

        # Width and height of the box
        self._width = width
        self._height = height

        # Box position, relative to the containing box
        self._top = top
        self._left = left

        # Origin of the containing box, in absolute coordinates.
        self._origin_top = None
        self._origin_left = None

        # Current state of layout calculations
        self._dirty = True

        # Set the origin via properties; this forces the calculation of
        # absolute positions.
        self.origin_top = 0
        self.origin_left = 0

    def __repr__(self):
        return '<Box (%sx%s @ %s,%s)>' % (self._width, self._height, self._absolute_left, self._absolute_top)

    def __eq__(self, value):
        return all([
            self._width == value._width,
            self._height == value._height,
            self._absolute_top == value._absolute_top,
            self._absolute_left == value._absolute_left
        ])

    def reset(self):
        self._dirty = True
        self._width = None
        self._height = None
        self._top = 0
        self._left = 0

    ######################################################################
    # Core properties
    ######################################################################
    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        if value != self._top:
            self._top = value
            self._absolute_top = value + self._origin_top
            for child in self.node.children:
                child.layout.origin_top = self._absolute_top
            self._dirty = True

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if value != self._left:
            self._left = value
            self._absolute_left = value + self._origin_left
            for child in self.node.children:
                child.layout.origin_left = self._absolute_left
            self._dirty = True

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
    def origin_top(self):
        return self._origin_top

    @origin_top.setter
    def origin_top(self, value):
        if value != self._origin_top:
            self._origin_top = value
            self._absolute_top = value + self._top
            for child in self.node.children:
                child.layout.origin_top = self._absolute_top
            self._dirty = True

    @property
    def origin_left(self):
        return self._origin_left

    @origin_left.setter
    def origin_left(self, value):
        if value != self._origin_left:
            self._origin_left = value
            self._absolute_left = value + self._left
            for child in self.node.children:
                child.layout.origin_left = self._absolute_left
            self._dirty = True

    ######################################################################
    # Relative dimensions
    ######################################################################
    @property
    def bottom(self):
        return self._top + self._height

    @property
    def right(self):
        return self._left + self._width

    ######################################################################
    # Absolute dimensions
    ######################################################################
    @property
    def absolute_top(self):
        return self._absolute_top

    @property
    def absolute_left(self):
        return self._absolute_left

    @property
    def absolute_bottom(self):
        return self._absolute_top + self._height

    @property
    def absolute_right(self):
        return self._absolute_left + self._width

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
                child.layout.dirty = value

    ######################################################################

    # @property
    # def containing_block(self):
    #     if self._node.parent:
    #         return self._node.parent.layout

    # @property
    # def is_block_box(self):
    #     return self.node.style.display in (BLOCK, LIST_ITEM, TABLE)

    # @property
    # def is_inline_box(self):
    #     return self.node.style.display in (INLINE, INLINE_TABLE, INLINE_BLOCK)

    # @property
    # def is_positioned(self):
    #     return self.node.style.position != STATIC

    # ######################################################################

    # @property
    # def display(self):
    #     if (self.node.style.position in (ABSOLUTE, FIXED)  # 9.7, point 2
    #             or self.node.style.float is not None  # 9.7, point 3:
    #             or self.node.parent is None):  # 9.7, point 4:
    #         if self.node.style.display == INLINE_TABLE:
    #             return TABLE
    #         elif self.node.style.display in (
    #                 INLINE, TABLE_ROW_GROUP, TABLE_COLUMN, TABLE_COLUMN_GROUP,
    #                 TABLE_HEADER_GROUP, TABLE_FOOTER_GROUP, TABLE_ROW,
    #                 TABLE_CELL, TABLE_CAPTION, INLINE_BLOCK):
    #             return BLOCK
    #     return self.node.style.display

    # @property
    # def position(self):
    #     if self.node.style.display is None:
    #         return None  # 9.7, point 1
    #     return self.node.style.position

    # @property
    # def float(self):
    #     if self.node.style.display is None:
    #         return None  # 9.7, point 1
    #     elif self.node.style.position in (ABSOLUTE, FIXED):
    #         return None  # 9.7, point 2
    #     return self.node.style.float
