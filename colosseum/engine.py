from .constants import (
    AUTO,
    ABSOLUTE,
    INLINE, INLINE_BLOCK, BLOCK, LIST_ITEM, TABLE,
    THIN, MEDIUM, THICK,
    LTR,
)
from .dimensions import Box


def is_block_level_element(node):
    # 9.2.1 P1
    return (
        node.style.display is BLOCK
        or node.style.display is LIST_ITEM
        or node.style.display is TABLE
    )


def is_inline_block_element(node):
    return node.style.display is INLINE_BLOCK


def is_inline_element(node):
    return node.style.display is INLINE


def is_floating_element(node):
    return node.style.float_ is not None


def is_absolute_positioned_element(node):
    return node.style.position is ABSOLUTE


def is_replaced_element(node):
    return node.intrinsic.is_replaced


def in_normal_flow(node):
    return True  # FIXME


class Viewport:
    def __init__(self, display, root):
        self.display = display
        self.children = [root]
        self.layout = self.display


def layout(display, node):
    containing_block = Viewport(display, node)
    font = None  # FIXME - default font
    # 10.1 1
    layout_box(display, node, containing_block, containing_block, font)


def block_contain(nodes):
    anon_block = None
    containers = []
    for node in nodes:
        if node.style.display is BLOCK:
            if anon_block:
                containers.append(anon_block)
                anon_block = None
            containers.append(node)
        else:
            if anon_block:
                anon_block.append(node)
            else:
                anon_block = [node]

    return containers


def layout_box(display, node, containing_block, viewport, font):

    # Copy margin, border and padding attributes to the layout
    horizontal = {
        'display': display,
        'font': font,
        'size': containing_block.layout.content_width
    }

    vertical = {
        'display': display,
        'font': font,
        'size': containing_block.layout.content_height
    }
    node.layout.margin_top = calculate_size(node.style.margin_top, vertical)
    node.layout.margin_right = calculate_size(node.style.margin_right, horizontal)
    node.layout.margin_bottom = calculate_size(node.style.margin_bottom, vertical)
    node.layout.margin_left = calculate_size(node.style.margin_left, horizontal)

    node.layout.border_top_width = calculate_size(node.style.border_top_width, horizontal)
    node.layout.border_right_width = calculate_size(node.style.border_right_width, vertical)
    node.layout.border_bottom_width = calculate_size(node.style.border_bottom_width, horizontal)
    node.layout.border_left_width = calculate_size(node.style.border_left_width, vertical)

    node.layout.padding_top = calculate_size(node.style.padding_top, horizontal)
    node.layout.padding_right = calculate_size(node.style.padding_right, vertical)
    node.layout.padding_bottom = calculate_size(node.style.padding_bottom, horizontal)
    node.layout.padding_left = calculate_size(node.style.padding_left, vertical)

    calculate_width_and_margins(node, horizontal)
    calculate_height_and_margins(node, vertical)


def calculate_size(value, context):
    if value is AUTO:
        return value
    if value is THIN or value is MEDIUM or value is THICK:
        return display.fixed_size(value)
    if value == 0:
        return value
    return value.px(**context)


###########################################################################
# Section 10.3: Calculating widths and margins
###########################################################################
def calculate_width_and_margins(node, context):
    "Implements S10.3"
    if is_floating_element(node):
        if is_replaced_element(node):  # 10.3.6
            calculate_floating_replaced_width(node, context)
        else:  # 10.3.5
            calculate_floating_non_replaced_width(node, context)
    elif is_absolute_positioned_element(node):
        if is_replaced_element(node):  # 10.3.8
            calculate_absolute_position_replaced_width(node, context)
        else:  # 10.3.7
            calculate_absolute_position_non_replaced_width(node, context)
    elif is_inline_element(node):
        if is_replaced_element(node):  # 10.3.2
            calculate_inline_replaced_width(node, context)
        else:  # 10.3.1
            calculate_inline_non_replaced_width(node, context)
    elif in_normal_flow(node):
        if is_block_level_element(node):
            if is_replaced_element(node):  # 10.3.4
                calculate_block_replaced_normal_flow_width(node, context)
            else:  # 10.3.3
                calculate_block_non_replaced_normal_flow_width(node, context)
        elif is_inline_block_element(node):
            if is_replaced_element(node):  # 10.3.10
                calculate_inline_block_replaced_normal_flow_width(node, context)
            else:  # 10.3.9
                calculate_inline_block_non_replaced_normal_flow_width(node, context)
        else:
            raise Exception("Unknown normal flow width calculation")
    else:
        raise Exception("Unknown width calculation")


def calculate_inline_non_replaced_width(node, context):
    "Implements S10.3.1"
    if node.layout.margin_left == AUTO:  # P1
        node.layout.margin_left = 0

    if node.layout.margin_right == AUTO:  # P1
        node.layout.margin_right = 0

    # Use the actual width of the node.
    node.layout.content_width = node.intrinsic.width


def calculate_inline_replaced_width(node, context):
    "Implements S10.3.2"
    if node.layout.margin_left == AUTO:  # P1
        node.layout.margin_left = 0

    if node.layout.margin_right == AUTO:  # P1
        node.layout.margin_right = 0

    if node.style.width is AUTO:
        width = None
        if node.style.height is AUTO:
            if node.intrinsic.width is not None:  # P2
                width = node.intrinsic.width
            elif node.intrinsic.height is not None:  # P3
                width = node.intrinsic.height * node.intrinsic.ratio
            elif node.intrinsic.ratio is not None:  # P4
                width = (
                    context['size']
                    - node.layout.margin_left
                    - node.layout.border_left_width
                    - node.layout.padding_left
                    - node.layout.padding_right
                    - node.layout.border_right_width
                    - node.layout.margin_right
                )

        if width is None:
            if node.intrinsic.width is not None:  # P5
                width = node.intrinsic.width
            else:  # P6
                width = 300

        node.layout.content_width = width
    else:
        node.layout.content_width = node.style.width.px(**context)


def calculate_block_non_replaced_normal_flow_width(node, context):
    "Implements S10.3.3"
    if node.style.width is not AUTO:  # P2
        node_width = node.style.width.px(**context)
        size = (
            node.layout.border_left_width
            + node.layout.padding_left
            + node_width
            + node.layout.padding_right
            + node.layout.border_right_width
        )
        if node.layout.margin_left is not AUTO:
            size += node.layout.margin_left
        if node.layout.margin_right is not AUTO:
            size += node.layout.margin_right
        if size > context['size']:
            if node.layout.margin_left is AUTO:
                node.layout.margin_left = 0
            if node.layout.margin_right is AUTO:
                node.layout.margin_right = 0

    if (node.layout.margin_left is not AUTO
            and node.style.width is not AUTO
            and node.layout.margin_right is not AUTO):  # P3
        if node.style.direction is LTR:
            node.layout.margin_right = (
                context['size']
                - node.layout.margin_left
                - node.layout.border_left_width
                - node.layout.padding_left
                - node_width
                - node.layout.padding_right
                - node.layout.border_right_width
            )
            node.layout.content_width = node_width
        else:
            node.layout.margin_left = (
                context['size']
                - node.layout.border_left_width
                - node.layout.padding_left
                - node_width
                - node.layout.padding_right
                - node.layout.border_right_width
                - node.layout.margin_right
            )
            node.layout.content_width = node_width

    elif (node.layout.margin_left is AUTO
            and node.style.width is not AUTO
            and node.layout.margin_right is not AUTO):  # P4
        node.layout.margin_left = (
            context['size']
            - node.layout.border_left_width
            - node.layout.padding_left
            - node_width
            - node.layout.padding_right
            - node.layout.border_right_width
            - node.layout.margin_right
        )
        node.layout.content_width = node_width

    elif (node.layout.margin_left is not AUTO
            and node.style.width is AUTO
            and node.layout.margin_right is not AUTO):  # P4
        node.layout.content_width = (
            context['size']
            - node.layout.margin_left
            - node.layout.border_left_width
            - node.layout.padding_left
            - node.layout.padding_right
            - node.layout.border_right_width
            - node.layout.margin_right
        )

    elif (node.layout.margin_left is not AUTO
            and node.style.width is not AUTO
            and node.layout.margin_right is AUTO):  # P4
        node.layout.margin_right = (
            context['size']
            - node.layout.margin_left
            - node.layout.border_left_width
            - node.layout.padding_left
            - node_width
            - node.layout.padding_right
            - node.layout.border_right_width
        )
        node.layout.content_width = node_width

    elif node.style.width is AUTO:  # P5
        if node.layout.margin_left is AUTO:
            node.layout.margin_left = 0
        if node.layout.margin_right is AUTO:
            node.layout.margin_right = 0

        node.layout.content_width = (
            context['size']
            - node.layout.margin_left
            - node.layout.border_left_width
            - node.layout.padding_left
            - node.layout.padding_right
            - node.layout.border_right_width
            - node.layout.margin_right
        )

    elif node.layout.margin_left is AUTO and node.layout.margin_right is AUTO:
        avail_margin = (
            context['size']
            - node.layout.border_left_width
            - node.layout.padding_left
            - node_width
            - node.layout.padding_right
            - node.layout.border_right_width
        )
        node.layout.margin_left = avail_margin // 2
        node.layout.margin_right = avail_margin // 2

        node.layout.content_width = node_width
        node.layout.content_left = node.layout.margin_left + node.layout.border_left_width + node.layout.padding_left
    else:
        raise Exception('Unknown S10.3.3 layout case')


def calculate_block_replaced_normal_flow_width(node, context):
    "Implements S10.3.4"
    raise NotImplementedError("Section 10.3.4")


def calculate_floating_non_replaced_width(node, context):
    "Implements S10.3.5"
    raise NotImplementedError("Section 10.3.5")


def calculate_floating_replaced_width(node, context):
    "Implements S10.3.6"
    raise NotImplementedError("Section 10.3.6")


def calculate_absolute_position_non_replaced_width(node, context):
    "Implements S10.3.7"
    raise NotImplementedError("Section 10.3.7")


def calculate_absolute_position_replaced_width(node, context):
    "Implements S10.3.8"
    raise NotImplementedError("Section 10.3.8")


def calculate_inline_block_non_replaced_normal_flow_width(node, context):
    "Implements S10.3.9"
    raise NotImplementedError("Section 10.3.9")


def calculate_inline_block_replaced_normal_flow_width(node, context):
    "Implements S10.3.10"
    raise NotImplementedError("Section 10.3.10")


###########################################################################
# Section 10.6: Calculating heights and margins
###########################################################################
def calculate_height_and_margins(node, context):
    "Implements S10.6"
    if is_floating_element(node):
        if is_replaced_element(node):  # 10.6.6
            calculate_floating_replaced_height(node, context)
        else:  # 10.6.5
            calculate_floating_non_replaced_height(node, context)
    elif is_absolute_positioned_element(node):
        if is_replaced_element(node):  # 10.6.8
            calculate_absolute_position_replaced_height(node, context)
        else:  # 10.6.7
            calculate_absolute_position_non_replaced_height(node, context)
    elif is_inline_element(node):
        if is_replaced_element(node):  # 10.6.2
            calculate_inline_replaced_height(node, context)
        else:  # 10.6.1
            calculate_inline_non_replaced_height(node, context)
    elif in_normal_flow(node):
        if is_block_level_element(node):
            if is_replaced_element(node):  # 10.6.4
                calculate_block_replaced_normal_flow_height(node, context)
            else:  # 10.6.3
                calculate_block_non_replaced_normal_flow_height(node, context)
        elif is_inline_block_element(node):
            if is_replaced_element(node):  # 10.6.10
                calculate_inline_block_replaced_normal_flow_height(node, context)
            else:  # 10.6.9
                calculate_inline_block_non_replaced_normal_flow_height(node, context)
        else:
            raise Exception("Unknown normal flow width calculation")
    else:
        raise Exception("Unknown width calculation")


def calculate_inline_non_replaced_height(node, context):
    "Implements S10.6.1"
    raise NotImplementedError("Section 10.6.1")


def calculate_inline_replaced_height(node, context):
    "Implements S10.6.2"
    raise NotImplementedError("Section 10.6.2")


def calculate_block_non_replaced_normal_flow_height(node, context):
    "Implements S10.6.3"
    if node.layout.margin_top is AUTO:  # P2
        node.layout.margin_top = 0

    if node.layout.margin_bottom is AUTO: # P2
        node.layout.margin_bottom = 0

    if node.style.height is AUTO:
        raise NotImplementedError("Section 10.6.3 P2 (AUTO HEIGHT)")
    else:
        node.layout.content_height = node.style.height.px(**context)


def calculate_block_replaced_normal_flow_height(node, context):
    "Implements S10.6.4"
    raise NotImplementedError("Section 10.6.4")


def calculate_floating_non_replaced_height(node, context):
    "Implements S10.6.5"
    raise NotImplementedError("Section 10.6.5")


def calculate_floating_replaced_height(node, context):
    "Implements S10.6.6"
    raise NotImplementedError("Section 10.6.6")


def calculate_absolute_position_non_replaced_height(node, context):
    "Implements S10.6.7"
    raise NotImplementedError("Section 10.6.7")


def calculate_absolute_position_replaced_height(node, context):
    "Implements S10.6.8"
    raise NotImplementedError("Section 10.6.8")


def calculate_inline_block_non_replaced_normal_flow_height(node, context):
    "Implements S10.6.9"
    raise NotImplementedError("Section 10.6.9")


def calculate_inline_block_replaced_normal_flow_height(node, context):
    "Implements S10.6.10"
    raise NotImplementedError("Section 10.6.10")
