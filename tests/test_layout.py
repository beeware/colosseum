# Derived from https://github.com/facebook/css-layout
# Tests match hash: 2b6844f00acc3166ba9d57f49acebd0146e6007e in freakboy3742 minmax branch

try:
    from unittest import TestCase, expectedFailure
except ImportError:
    from unittest2 import TestCase, expectedFailure

from colosseum.nodes import CSSNode, Layout
from colosseum.constants import *

STYLE = 'style'
CHILDREN = 'children'


SMALL_WIDTH = 34.671875
SMALL_HEIGHT = 16
BIG_WIDTH = 172.421875
BIG_HEIGHT = 32
BIG_MIN_WIDTH = 100.453125
SMALL_TEXT = "small"
LONG_TEXT = "loooooooooong with space"


def text(value):
    def fn(width):
        if width is None or width != width:
            width = float('inf')

        # Constants for testing purposes between C/JS and other platforms
        # Comment this block of code if you want to use the browser to
        # generate proper sizes
        if value == SMALL_TEXT:
            return {
                WIDTH: min(SMALL_WIDTH, width),
                HEIGHT: SMALL_HEIGHT
            }

        if value == LONG_TEXT:
            return {
                WIDTH: BIG_WIDTH if width >= BIG_WIDTH else max(BIG_MIN_WIDTH, width),
                HEIGHT: SMALL_HEIGHT if width >= BIG_WIDTH else BIG_HEIGHT
            }

    # fn.toString = function() { return value; };
    return fn;


class LayoutEngineTest(TestCase):

    ######################################################################
    # Utility methods
    ######################################################################

    def _add_children(self, node, children):
        for child_data in children:
            child = CSSNode(**child_data[STYLE])
            self._add_children(child, child_data.get(CHILDREN, []))
            node.children.append(child)

    def _assertLayout(self, node, layout):
        # Internal recursive method for checking a node's layout
        child_layouts = layout.pop(CHILDREN, [])
        self.assertEqual(node.layout, Layout(**layout))
        for child, child_layout in zip(node.children, child_layouts):
            self._assertLayout(child, child_layout)

    def assertLayout(self, node_data, layout):
        # Recursively create the node and children
        node = CSSNode(**node_data[STYLE])
        self._add_children(node, node_data.get(CHILDREN, []))

        # Recursively compare the layout
        self._assertLayout(node, layout)

    ######################################################################
    # Layout tests
    ######################################################################
    def test_should_layout_a_single_node_with_width_and_height(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200}},
            {'width': 100, 'height': 200, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_children(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {STYLE: {'width': 500, 'height': 500}},
                    {STYLE: {'width': 250, 'height': 250}},
                    {STYLE: {'width': 125, 'height': 125}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 500, 'height': 500, 'top': 0, 'left': 0},
                    {'width': 250, 'height': 250, 'top': 500, 'left': 0},
                    {'width': 125, 'height': 125, 'top': 750, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_nested_children(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {
                        STYLE: {'width': 500, 'height': 500}
                    },
                    {
                        STYLE: {'width': 500, 'height': 500},
                        CHILDREN: [
                            {
                                STYLE: {'width': 250, 'height': 250}
                            },
                            {
                                STYLE: {'width': 250, 'height': 250}
                            }
                        ]
                    }
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 500, 'height': 500, 'top': 0, 'left': 0},
                    {
                        'width': 500, 'height': 500, 'top': 500, 'left': 0,
                        CHILDREN: [
                            {'width': 250, 'height': 250, 'top': 0, 'left': 0},
                            {'width': 250, 'height': 250, 'top': 250, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_margin(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'height': 200, 'margin': 10}
            },
            {'width': 100, 'height': 200, 'top': 10, 'left': 10}
        )

    def test_should_layout_node_with_several_children(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'margin': 10},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100, 'margin': 50}},
                    {STYLE: {'width': 100, 'height': 100, 'margin': 25}},
                    {STYLE: {'width': 100, 'height': 100, 'margin': 10}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 10, 'left': 10,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 50, 'left': 50},
                    {'width': 100, 'height': 100, 'top': 225, 'left': 25},
                    {'width': 100, 'height': 100, 'top': 360, 'left': 10}
                ]
            }
        )

    def test_should_layout_node_with_row_flex_direction(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 200}},
                    {STYLE: {'width': 300, 'height': 150}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 300, 'height': 150, 'top': 0, 'left': 100}
                ]
            }
        )

    def test_should_layout_node_based_on_children_main_dimensions(self):
        self.assertLayout(
            {
                STYLE: {'width': 300},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 200}},
                    {STYLE: {'width': 300, 'height': 150}}
                ]
            },
            {
                'width': 300, 'height': 350, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 300, 'height': 150, 'top': 200, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_just_flex(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 200}},
                    {STYLE: {'width': 100, 'flex': 1}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 100, 'height': 800, 'top': 200, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_flex_recursively(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {
                        STYLE: {'width': 1000, 'flex': 1}, CHILDREN: [
                            {
                                STYLE: {'width': 1000, 'flex': 1},
                                CHILDREN: [
                                    {STYLE: {'width': 1000, 'flex': 1}}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {
                                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                                CHILDREN: [
                                    {'width': 1000, 'height': 1000, 'top': 0, 'left': 0}
                                ]
                            }
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_targeted_margin(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'margin_top': 10, 'margin_left': 5},
                CHILDREN: [
                    {
                        STYLE: {'width': 100, 'height': 100, 'margin_top': 50, 'margin_left': 15, 'margin_bottom': 20}
                    },
                    {
                        STYLE: {'width': 100, 'height': 100, 'margin_left': 30}
                    }
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 10, 'left': 5,
                CHILDREN: [
                    {
                        'width': 100, 'height': 100, 'top': 50, 'left': 15
                    },
                    {
                        'width': 100, 'height': 100, 'top': 170, 'left': 30
                    }
                ]
            }
        )

    def test_should_layout_node_with_justify_content_flex_start(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'justify_content': 'flex-start'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_justify_content_flex_end(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'justify_content': 'flex-end'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 800, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 900, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_justify_content_space_between(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'justify_content': 'space-between'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 900, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_justify_content_space_around(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'justify_content': 'space-around'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 200, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 700, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_justify_content_center(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'justify_content': 'center'},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 400, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 500, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_flex_override_height(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {STYLE: {'width': 100, 'height': 100, 'flex': 1}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 1000, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_align_items_flex_start(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'align_items': 'flex-start'},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 100, 'height': 100, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_align_items_center(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'align_items': 'center'},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 100, 'top': 0, 'left': 400},
                    {'width': 100, 'height': 100, 'top': 100, 'left': 450}
                ]
            }
        )

    def test_should_layout_node_with_align_items_flex_end(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'align_items': 'flex-end'},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 100, 'top': 0, 'left': 800},
                    {'width': 100, 'height': 100, 'top': 100, 'left': 900}
                ]
            }
        )

    def test_should_layout_node_with_align_self_overrides_align_items(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'align_items': 'flex-end'},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 100}},
                    {STYLE: {'width': 100, 'height': 100, 'align_self': 'center'}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 100, 'top': 0, 'left': 800},
                    {'width': 100, 'height': 100, 'top': 100, 'left': 450}
                ]
            }
        )

    def test_should_layout_node_with_alignItem_stretch(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000, 'align_items': 'stretch'},
                CHILDREN: [
                    {STYLE: {'height': 100}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 1000, 'height': 100, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_empty_node(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_child_with_margin(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'margin': 5}}
                ]
            },
            {
                'width': 10, 'height': 10, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 5, 'left': 5}
                ]
            }
        )

    def test_should_not_shrink_children_if_not_enough_space(self):
        self.assertLayout(
            {
                STYLE: {'height': 100},
                CHILDREN: [
                    {STYLE: {'height': 100}},
                    {STYLE: {'height': 200}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 200, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_layout_for_center(self):
        self.assertLayout(
            {STYLE: {'justify_content': 'center'}},
            {'width': 0, 'height': 0, 'top': 0, 'left': 0}
        )

    def test_should_layout_flex_end_taking_into_account_margin(self):
        self.assertLayout(
            {
                STYLE: {'height': 100, 'justify_content': 'flex-end'},
                CHILDREN: [
                    {STYLE: {'margin_top': 10}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_layout_align_items_with_margin(self):
        self.assertLayout(
            {
                STYLE: {}, CHILDREN: [
                    {
                        STYLE: {'align_items': 'flex-end'},
                        CHILDREN: [
                            {STYLE: {'margin': 10}},
                            {STYLE: {'height': 100}}
                        ]
                    }
                ]
            },
            {
                'width': 20, 'height': 120, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 20, 'height': 120, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 0, 'height': 0, 'top': 10, 'left': 10},
                            {'width': 0, 'height': 100, 'top': 20, 'left': 20}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_flex_inside_of_an_empty_element(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_align_items_stretch_and_margin(self):
        self.assertLayout(
            {
                STYLE: {'align_items': 'stretch'},
                CHILDREN: [
                    {STYLE: {'margin_left': 10}}
                ]
            },
            {
                'width': 10, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 10}
                ]
            }
        )

    def test_should_layout_node_with_padding(self):
        self.assertLayout(
            {STYLE: {'padding': 5}},
            {'width': 10, 'height': 10, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_padding_and_a_child(self):
        self.assertLayout(
            {
                STYLE: {'padding': 5},
                CHILDREN: [
                    {STYLE: {}}
                ]
            },
            {
                'width': 10, 'height': 10, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 5, 'left': 5}
                ]
            }
        )

    def test_should_layout_node_with_padding_and_a_child_with_margin(self):
        self.assertLayout(
            {
                STYLE: {'padding': 5},
                CHILDREN: [
                    {STYLE: {'margin': 5}}
                ]
            },
            {
                'width': 20, 'height': 20, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 10, 'left': 10}
                ]
            }
        )

    def test_should_layout_node_with_padding_and_stretch(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'padding': 10, 'align_self': 'stretch'}}
                ]
            },
            {
                'width': 20, 'height': 20, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 20, 'height': 20, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_inner_and_outer_padding_and_stretch(self):
        self.assertLayout(
            {
                STYLE: {'padding': 50},
                CHILDREN: [
                    {STYLE: {'padding': 10, 'align_self': 'stretch'}}
                ]
            },
            {
                'width': 120, 'height': 120, 'top': 0, 'left': 0, CHILDREN: [
                    {'width': 20, 'height': 20, 'top': 50, 'left': 50}
                ]
            }
        )

    def test_should_layout_node_with_stretch_and_child_with_margin(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {'align_self': 'stretch'},
                        CHILDREN: [
                            {STYLE: {'margin': 16}}
                        ]
                    }
                ]
            },
            {
                'width': 32, 'height': 32, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 32, 'height': 32, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 0, 'height': 0, 'top': 16, 'left': 16}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_top_and_left(self):
        self.assertLayout(
            {STYLE: {'top': 5, 'left': 5}},
            {'width': 0, 'height': 0, 'top': 5, 'left': 5}
        )

    def test_should_layout_node_with_height_padding_and_space_around(self):
        self.assertLayout(
            {
                STYLE: {'height': 10, 'padding_top': 5, 'justify_content': 'space-around'},
                CHILDREN: [
                    {STYLE: {}}
                ]
            },
            {
                'width': 0, 'height': 10, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 7.5, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_bottom(self):
        self.assertLayout(
            {STYLE: {'bottom': 5}},
            {'width': 0, 'height': 0, 'top': -5, 'left': 0}
        )

    def test_should_layout_node_with_both_top_and_bottom(self):
        self.assertLayout(
            {STYLE: {'top': 10, 'bottom': 5}},
            {'width': 0, 'height': 0, 'top': 10, 'left': 0}
        )

    def test_should_layout_node_with_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {'width': 500, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'position': 'absolute', 'width': 50}},
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 500, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 250, 'height': 0, 'top': 0, 'left': 0},
                    {'width': 50, 'height': 0, 'top': 0, 'left': 250},
                    {'width': 250, 'height': 0, 'top': 0, 'left': 250}
                ]
            }
        )

    def test_should_layout_node_with_child_with_position_absolute_and_margin(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'margin_right': 15, 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_padding_and_align_self_center(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'padding_right': 12, 'align_self': 'center', 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 12, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_work_with_height_smaller_than_padding_bottom(self):
        self.assertLayout(
            {STYLE: {'height': 5, 'padding_bottom': 20}},
            {'width': 0, 'height': 20, 'top': 0, 'left': 0}
        )

    def test_should_work_with_width_smaller_than_padding_left(self):
        self.assertLayout(
            {STYLE: {'width': 5, 'padding_left': 20}},
            {'width': 20, 'height': 0, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_specified_width_and_stretch(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {},
                        CHILDREN: [
                            {STYLE: {'width': 400}}
                        ]
                    },
                    {
                        STYLE: {'width': 200, 'align_self': 'stretch'}
                    }
                ]
            },
            {
                'width': 400, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 400, 'height': 0, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 400, 'height': 0, 'top': 0, 'left': 0}
                        ]
                    },
                    {
                        'width': 200, 'height': 0, 'top': 0, 'left': 0
                    }
                ]
            }
        )

    def test_should_layout_node_with_padding_and_child_with_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {'padding': 5},
                CHILDREN: [
                    {STYLE: {'position': 'absolute'}}
                ]
            },
            {
                'width': 10, 'height': 10, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 5, 'left': 5}
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_top_and_left(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'height': 100}},
                    {STYLE: {'position': 'absolute', 'top': 10, 'left': 10}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 10, 'left': 10}
                ]
            }
        )

    def test_should_layout_node_with_padding_and_child_position_absolute_left(self):
        self.assertLayout(
            {
                STYLE: {'padding': 20}, CHILDREN: [
                    {STYLE: {'left': 5, 'position': 'absolute'}}
                ]
            },
            {
                'width': 40, 'height': 40, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 20, 'left': 5}
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_top_and_marginTop(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'top': 5, 'margin_top': 5, 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 10, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_left_and_margin_left(self):
        self.assertLayout(
            {STYLE: {}, CHILDREN: [
                {STYLE: {'left': 5, 'margin_left': 5, 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0, CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 10}
                ]
            }
        )

    def test_should_layout_node_with_space_around_and_child_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {'height': 200, 'justify_content': 'space-around'},
                CHILDREN: [
                    {STYLE: {'position': 'absolute'}},
                    {STYLE: {}}
                ]
            },
            {
                'width': 0, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 100, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_flex_and_main_margin(self):
        self.assertLayout(
            {
                STYLE: {'width': 700, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'margin_left': 5, 'flex': 1}}
                ]
            },
            {
                'width': 700, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 695, 'height': 0, 'top': 0, 'left': 5}
                ]
            }
        )

    def test_should_layout_node_with_multiple_flex_and_padding(self):
        self.assertLayout(
            {
                STYLE: {'width': 700, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'padding_right': 5, 'flex': 1}}
                ]
            },
            {
                'width': 700, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 347.5, 'height': 0, 'top': 0, 'left': 0},
                    {'width': 352.5, 'height': 0, 'top': 0, 'left': 347.5}
                ]
            }
        )

    def test_should_layout_node_with_multiple_flex_and_margin(self):
        self.assertLayout(
            {
                STYLE: {'width': 700, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'margin_left': 5, 'flex': 1}}
                ]
            },
            {
                'width': 700, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 347.5, 'height': 0, 'top': 0, 'left': 0},
                    {'width': 347.5, 'height': 0, 'top': 0, 'left': 352.5}
                ]
            }
        )

    def test_should_layout_node_with_flex_and_overflow(self):
        self.assertLayout(
            {
                STYLE: {'height': 300},
                CHILDREN: [
                    {STYLE: {'height': 600}},
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 0, 'height': 300, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 600, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 600, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_flex_and_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {'width': 600, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1, 'position': 'absolute'}}
                ]
            },
            {
                'width': 600, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_double_flex_and_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {'height': 500},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'flex': 1, 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 500, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 500, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 500, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_border_width(self):
        self.assertLayout(
            {STYLE: {'border_width': 5}},
            {'width': 10, 'height': 10, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_border_width_and_position_absolute_top(self):
        self.assertLayout(
            {
                STYLE: {'border_top_width': 1},
                CHILDREN: [
                    {STYLE: {'top': -1, 'position': 'absolute'}}
                ]
            },
            {
                'width': 0, 'height': 1, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_border_width_and_position_absolute_top_cross_axis(self):
        self.assertLayout(
            {
                STYLE: {'border_width': 1},
                CHILDREN: [
                    {STYLE: {'left': 5, 'position': 'absolute'}}
                ]
            },
            {
                'width': 2, 'height': 2, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 1, 'left': 6}
                ]
            }
        )

    def test_should_correctly_take_into_account_min_padding_for_stretch(self):
        self.assertLayout(
            {
                STYLE: {'width': 50},
                CHILDREN: [
                    {STYLE: {'margin_left': 20, 'padding': 20, 'align_self': 'stretch'}}
                ]
            },
            {
                'width': 50, 'height': 40, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 40, 'height': 40, 'top': 0, 'left': 20}
                ]
            }
        )

    def test_should_layout_node_with_negative_width(self):
        self.assertLayout(
            {
                STYLE: {'width': -31},
                CHILDREN: [
                    {STYLE: {'border_right_width': 5}}
                ]
            },
            {
                'width': 5, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 5, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_handle_negative_margin_and_min_padding_correctly(self):
        self.assertLayout(
            {
                STYLE: {'border_right_width': 1, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'margin_right': -8}}
                ]
            },
            {
                'width': 1, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_just_text(self):
        self.assertLayout(
            {STYLE: {'measure': text(SMALL_TEXT)}},
            {'width': SMALL_WIDTH, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_text_and_width(self):
        self.assertLayout(
            {STYLE: {'measure': text(SMALL_TEXT), 'width': 10}},
            {'width': 10, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_text_padding_and_margin(self):
        self.assertLayout(
            {STYLE: {'measure': text(LONG_TEXT)}},
            {'width': BIG_WIDTH, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0}
        )

    def test_should_layout_node_with_nested_align_self_stretch(self):
        self.assertLayout(
            {
                STYLE: {'width': 300},
                CHILDREN: [
                    {
                        STYLE: {'align_self': 'stretch'},
                        CHILDREN: [
                            {STYLE: {'align_self': 'stretch'}}
                        ]
                    }
                ]
            },
            {
                'width': 300, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 300, 'height': 0, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 300, 'height': 0, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_text_and_flex(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {'width': 500, 'flex_direction': 'row'},
                        CHILDREN: [
                            {STYLE: {'flex': 1, 'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 500, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 500, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 500, 'height': SMALL_HEIGHT, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_text_and_stretch(self):
        self.assertLayout(
            {
                STYLE: {'width': 130},
                CHILDREN: [
                    {
                        STYLE: {'align_self': 'stretch', 'align_items': 'stretch'},
                        CHILDREN: [
                            {STYLE: {'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 130, 'height': BIG_HEIGHT, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 130, 'height': BIG_HEIGHT, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 130, 'height': BIG_HEIGHT, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_text_stretch_and_width(self):
        self.assertLayout(
            {
                STYLE: {'width': 200},
                CHILDREN: [
                    {
                        STYLE: {'align_self': 'stretch', 'align_items': 'stretch'},
                        CHILDREN: [
                            {STYLE: {'width': 130, 'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 200, 'height': BIG_HEIGHT, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 200, 'height': BIG_HEIGHT, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 130, 'height': BIG_HEIGHT, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_node_with_text_bounded_by_parent(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'align_self': 'flex-start'},
                CHILDREN: [
                    {STYLE: {'measure': text(LONG_TEXT), 'align_self': 'flex-start'}}
                ]
            },
            {
                'width': 100, 'height': BIG_HEIGHT, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': BIG_MIN_WIDTH, 'height': BIG_HEIGHT, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_text_bounded_by_grand_parent(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'padding': 10, 'align_self': 'flex-start'},
                CHILDREN: [
                    {
                        STYLE: {'margin': 10, 'align_self': 'flex-start'},
                        CHILDREN: [
                            {STYLE: {'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 100, 'height': 40 + BIG_HEIGHT, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': BIG_MIN_WIDTH, 'height': BIG_HEIGHT, 'top': 20, 'left': 20,
                        CHILDREN: [
                            {'width': BIG_MIN_WIDTH, 'height': BIG_HEIGHT, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_space_between_when_remaining_space_is_negative(self):
        self.assertLayout(
            {
                STYLE: {'height': 100, 'justify_content': 'space-between'},
                CHILDREN: [
                    {STYLE: {'height': 900}},
                    {STYLE: {}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 900, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 900, 'left': 0}
                ]
            }
        )

    def test_should_layout_flex_end_when_remaining_space_is_negative(self):
        self.assertLayout(
            {
                STYLE: {'width': 200, 'flex_direction': 'row', 'justify_content': 'flex-end'},
                CHILDREN: [
                    {STYLE: {'width': 900}}
                ]
            },
            {
                'width': 200, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 900, 'height': 0, 'top': 0, 'left': -700}
                ]
            }
        )

    def test_should_layout_text_with_flex_direction_row(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {'width': 200, 'flex_direction': 'row'},
                        CHILDREN: [
                            {STYLE: {'margin': 20, 'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 200, 'height': SMALL_HEIGHT + 40, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 200, 'height': SMALL_HEIGHT + 40, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': BIG_WIDTH, 'height': SMALL_HEIGHT, 'top': 20, 'left': 20}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_with_text_and_margin(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {'width': 200},
                        CHILDREN: [
                            {STYLE: {'margin': 20, 'measure': text(LONG_TEXT)}}
                        ]
                    }
                ]
            },
            {
                'width': 200, 'height': BIG_HEIGHT + 40, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 200, 'height': BIG_HEIGHT + 40, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 160, 'height': BIG_HEIGHT, 'top': 20, 'left': 20}
                        ]
                    }
                ]
            }
        )

    def test_should_layout_with_position_absolute_top_left_bottom_right(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'height': 100},
                CHILDREN: [
                    {STYLE: {'position': 'absolute', 'top': 0, 'left': 0, 'bottom': 0, 'right': 0}}
                ]
            },
            {
                'width': 100, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 100, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_with_arbitrary_flex(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'height': 100, 'align_self': 'flex-start'},
                CHILDREN: [
                    {STYLE: {'flex': 2.5, 'align_self': 'flex-start'}},
                    {STYLE: {'flex': 7.5, 'align_self': 'flex-start'}}
                ]
            },
            {
                'width': 100, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 25, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 75, 'top': 25, 'left': 0}
                ]
            }
        )

    def test_should_layout_with_negative_flex(self):
        self.assertLayout(
            {
                STYLE: {'width': 100, 'height': 100, 'align_self': 'flex-start'},
                CHILDREN: [
                    {STYLE: {'flex': -2.5, 'align_self': 'flex-start'}},
                    {STYLE: {'flex': 0, 'align_self': 'flex-start'}}
                ]
            },
            {
                'width': 100, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_with_position_absolute_and_another_sibling(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'width': 50, 'height': 100}},
                    {STYLE: {'position': 'absolute', 'left': 0, 'right': 0}}
                ]
            },
            {
                'width': 50, 'height': 100, 'top': 0, 'left': 0, CHILDREN: [
                    {'width': 50, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 50, 'height': 0, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_calculate_height_properly_with_position_absolute_top_and_bottom(self):
        self.assertLayout(
            {
                STYLE: {'height': 100}, CHILDREN: [
                    {STYLE: {'position': 'absolute', 'top': 0, 'bottom': 20}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0, CHILDREN: [
                    {'width': 0, 'height': 80, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_with_complicated_position_absolute_and_justify_content_center_combo(self):
        self.assertLayout(
            {
                STYLE: {'width': 200, 'height': 200},
                CHILDREN: [
                    {
                        STYLE: {'position': 'absolute', 'justify_content': 'center', 'top': 0, 'left': 0, 'right': 0, 'bottom': 0},
                        CHILDREN: [
                            {STYLE: {'width': 100, 'height': 100}}
                        ]
                    }
                ]
            },
            {
                'width': 200, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 200, 'height': 200, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 100, 'height': 100, 'top': 50, 'left': 0}
                        ]
                    }
                ]
            }
        )

    def test_should_calculate_top_properly_with_position_absolute_bottom(self):
        self.assertLayout(
            {
                STYLE: {'height': 100},
                CHILDREN: [
                    {STYLE: {'position': 'absolute', 'bottom': 0}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 100, 'left': 0}
                ]
            }
        )

    def test_should_calculate_left_properly_with_position_absolute_right(self):
        self.assertLayout(
            {
                STYLE: {'width': 100},
                CHILDREN: [
                    {STYLE: {'position': 'absolute', 'right': 0}}
                ]
            },
            {
                'width': 100, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 100}
                ]
            }
        )

    def test_should_calculate_top_properly_with_position_absolute_bottom_and_height(self):
        self.assertLayout(
            {
                STYLE: {'height': 100},
                CHILDREN: [
                    {STYLE: {'height': 10, 'position': 'absolute', 'bottom': 0}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 10, 'top': 90, 'left': 0}
                ]
            }
        )

    def test_should_calculate_left_properly_with_position_absolute_right_and_width(self):
        self.assertLayout(
            {
                STYLE: {'width': 100},
                CHILDREN: [
                    {STYLE: {'width': 10, 'position': 'absolute', 'right': 0}}
                ]
            },
            {
                'width': 100, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 10, 'height': 0, 'top': 0, 'left': 90}
                ]
            }
        )

    def test_should_calculate_top_properly_with_position_absolute_right_width_and_no_parent_dimensions(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'height': 10, 'position': 'absolute', 'bottom': 0}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 10, 'top': -10, 'left': 0}
                ]
            }
        )

    def test_should_calculate_left_properly_with_position_absolute_right_width_and_no_parent_dimensions(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'width': 10, 'position': 'absolute', 'right': 0}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0, CHILDREN: [
                {'width': 10, 'height': 0, 'top': 0, 'left': -10}
                ]
            }
        )

    def test_should_layout_border_bottom_inside_of_justify_content_space_between_container(self):
        self.assertLayout(
            {
                STYLE: {'justify_content': 'space-between'},
                CHILDREN: [
                    {STYLE: {'border_bottom_width': 1}}
                ]
            },
            {
                'width': 0, 'height': 1, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 1, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_negative_margin_top_inside_of_justify_content_center_container(self):
        self.assertLayout(
            {
                STYLE: {'justify_content': 'center'},
                CHILDREN: [
                    {STYLE: {'margin_top': -6}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': -3, 'left': 0}
                ]
            }
        )

    def test_should_layout_positive_margin_top_inside_of_justify_content_center_container(self):
        self.assertLayout(
            {
                STYLE: {'justify_content': 'center'},
                CHILDREN: [
                    {STYLE: {'margin_top': 20}}
                ]
            },
            {
                'width': 0, 'height': 20, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 20, 'left': 0}
                ]
            }
        )

    def test_should_layout_border_bottom_and_flex_end_with_an_empty_child(self):
        self.assertLayout(
            {
                STYLE: {'border_bottom_width': 5, 'justify_content': 'flex-end'},
                CHILDREN: [
                    {STYLE: {}}
                ]
            },
            {
                'width': 0, 'height': 5, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_with_children_of_a_contain_with_left(self):
        self.assertLayout(
            {
                STYLE: {'width': 800},
                CHILDREN: [
                    {
                        STYLE: {'left': 5},
                        CHILDREN: [
                            {STYLE: {}}
                        ]
                    }
                ]
            },
            {
                'width': 800, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 800, 'height': 0, 'top': 0, 'left': 5,
                        CHILDREN: [
                            {'width': 800, 'height': 0, 'top': 0, 'left': 0}
                        ]
                    }
                ]
            }
        )

    # This behavior is very weird. The child has a width of 0 but somehow the
    # parent has a width of 500. Looks like a bug rather than a feature.
    # https://code.google.com/p/chromium/issues/detail?id=441768
    @expectedFailure
    def test_should_layout_with_flex_0_and_a_specific_width(self):
        self.assertLayout(
            {
                STYLE: {'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'width': 500, 'flex': 0}}
                ]
            },
            {
                'width': 500, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 0, 'top': 0, 'left': 0}
                ]
            }
        )

    @expectedFailure
    def test_should_layout_with_nested_padding(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {
                        STYLE: {},
                        CHILDREN: [
                            {STYLE: {}}
                        ]
                    },
                    {STYLE: {'padding': 5}}
                ]
            },
            {
                'width': 10, 'height': 10, 'top': 0, 'left': 0,
                CHILDREN: [
                    {
                        'width': 10, 'height': 0, 'top': 0, 'left': 0,
                        CHILDREN: [
                            {'width': 10, 'height': 0, 'top': 0, 'left': 0}
                        ]
                    },
                    {'width': 10, 'height': 10, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_flex_wrap(self):
        self.assertLayout(
            {
                STYLE: {'flex_wrap': 'wrap', 'flex_direction': 'row', 'width': 100},
                CHILDREN: [
                    {STYLE: {'width': 40, 'height': 10}},
                    {STYLE: {'width': 40, 'height': 10}},
                    {STYLE: {'width': 40, 'height': 10}}
                ]
            },
            {
                'width': 100, 'height': 20, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 40, 'height': 10, 'top': 0, 'left': 0},
                    {'width': 40, 'height': 10, 'top': 0, 'left': 40},
                    {'width': 40, 'height': 10, 'top': 10, 'left': 0}
                ]
            }
        )

    def test_should_layout_flex_wrap_with_a_line_bigger_than_container(self):
        self.assertLayout(
            {
                STYLE: {'height': 100, 'flex_wrap': 'wrap'},
                CHILDREN: [
                    {STYLE: {'height': 100}},
                    {STYLE: {'height': 200}}
                ]
            },
            {
                'width': 0, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 0, 'height': 100, 'top': 0, 'left': 0},
                    {'width': 0, 'height': 200, 'top': 0, 'left': 0}
                ]
            }
        )

    # The container should be width = 25 because the width of the two children
    # are 20 and 5. It's likely a bug in Chrome
    # https://code.google.com/p/chromium/issues/detail?id=247963#c16
    @expectedFailure
    def test_should_layout_flex_wrap_with_padding_and_borders(self):
        self.assertLayout(
            {
                STYLE: {'height': 100, 'flex_wrap': 'wrap'},
                CHILDREN: [
                    {STYLE: {'height': 500, 'padding_right': 20}},
                    {STYLE: {'border_left_width': 5}}
                ]
            },
            {
                'width': 20, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 20, 'height': 500, 'top': 0, 'left': 0},
                    {'width': 5, 'height': 0, 'top': 0, 'left': 20}
                ]
            }
        )

    @expectedFailure
    def test_should_layout_text_with_align_items_stretch(self):
        self.assertLayout(
            {STYLE: {'width': 80, 'padding': 7, 'align_items': 'stretch', 'measure': text(LONG_TEXT)}},
            {'width': 80, 'height': 68, 'top': 0, 'left': 0}
        )

    @expectedFailure
    def test_should_layout_node_with_text_and_position_absolute(self):
        self.assertLayout(
            {
                STYLE: {},
                CHILDREN: [
                    {STYLE: {'measure': text(LONG_TEXT)}}
                ]
            },
            {
                'width': 0, 'height': 0, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': BIG_HEIGHT, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_use_max_bounds(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'max_width': 90, 'max_height': 190}},
            {'width': 90, 'height': 190, 'top': 0, 'left': 0}
        )

    def test_should_use_min_bounds(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'min_width': 110, 'min_height': 210}},
            {'width': 110, 'height': 210, 'top': 0, 'left': 0}
        )

    def test_should_use_min_bounds_over_max_bounds(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'min_width': 110, 'max_width': 90, 'min_height': 210, 'max_height': 190}},
            {'width': 110, 'height': 210, 'top': 0, 'left': 0}
        )

    def test_should_use_min_bounds_over_max_bounds_and_natural_width(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'min_width': 90, 'max_width': 80, 'min_height': 190, 'max_height': 180}},
            {'width': 90, 'height': 190, 'top': 0, 'left': 0}
        )

    def test_should_ignore_negative_min_bounds(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'min_width': -10, 'min_height': -20}},
            {'width': 100, 'height': 200, 'top': 0, 'left': 0}
        )

    def test_should_ignore_negative_max_bounds(self):
        self.assertLayout(
            {STYLE: {'width': 100, 'height': 200, 'max_width': -10, 'max_height': -20}},
            {'width': 100, 'height': 200, 'top': 0, 'left': 0}
        )

    def test_should_use_padded_size_over_max_bounds(self):
        self.assertLayout(
            {STYLE: {'padding_top': 15, 'padding_bottom': 15, 'padding_left': 20, 'padding_right': 20, 'max_width': 30, 'max_height': 10}},
            {'width': 40, 'height': 30, 'top': 0, 'left': 0}
        )

    def test_should_use_min_size_over_padded_size(self):
        self.assertLayout(
            {STYLE: {'padding_top': 15, 'padding_bottom': 15, 'padding_left': 20, 'padding_right': 20, 'min_width': 50, 'min_height': 40}},
            {'width': 50, 'height': 40, 'top': 0, 'left': 0}
        )

    def test_should_override_flex_direction_size_with_min_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'flex': 1, 'min_width': 200}},
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 50, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 200, 'height': 200, 'top': 0, 'left': 50},
                    {'width': 50, 'height': 200, 'top': 0, 'left': 250}
                ]
            }
        )

    def test_should_not_override_flex_direction_size_within_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'flex': 1, 'min_width': 90, 'max_width': 110}},
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 100, 'height': 200, 'top': 0, 'left': 100},
                    {'width': 100, 'height': 200, 'top': 0, 'left': 200}
                ]
            }
        )

    def test_should_override_flex_direction_size_with_max_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200, 'flex_direction':'row'},
                CHILDREN: [
                    {STYLE: {'flex': 1}},
                    {STYLE: {'flex': 1, 'max_width': 60}},
                    {STYLE: {'flex': 1}}
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 120, 'height': 200, 'top': 0, 'left': 0},
                    {'width': 60, 'height': 200, 'top': 0, 'left': 120},
                    {'width': 120, 'height': 200, 'top': 0, 'left': 180}
                ]
            }
        )

    def test_should_pre_fill_child_size_within_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200},
                CHILDREN: [
                    {STYLE: {'flex': 1, 'min_width': 290, 'max_width': 310}},
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 300, 'height': 200, 'top': 0, 'left': 0},
                ]
            }
        )

    def test_should_pre_fill_child_size_within_max_bound(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200},
                CHILDREN: [
                    {STYLE: {'flex': 1, 'max_width': 290}},
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 290, 'height': 200, 'top': 0, 'left': 0},
                ]
            }
        )

    def test_should_pre_fill_child_size_within_min_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 300, 'height': 200},
                CHILDREN: [
                    {STYLE: {'flex': 1, 'min_width': 310}},
                ]
            },
            {
                'width': 300, 'height': 200, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 310, 'height': 200, 'top': 0, 'left': 0},
                ]
            }
        )

    def test_should_set_parents_size_based_on_bounded_children(self):
        self.assertLayout(
            {
                STYLE: {'min_width': 100, 'max_width': 300, 'min_height': 500, 'max_height': 700},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 300}},
                    {STYLE: {'width': 200, 'height': 300}},
                ]
            },
            {
                'width': 200, 'height': 600, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 300, 'top': 0, 'left': 0},
                    {'width': 200, 'height': 300, 'top': 300, 'left': 0},
                ]
            }
        )

    def test_should_set_parents_size_based_on_max_bounded_children(self):
        self.assertLayout(
            {
                STYLE: {'max_width': 100, 'max_height': 500},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 300}},
                    {STYLE: {'width': 200, 'height': 300}},
                ]
            },
            {
                'width': 100, 'height': 500, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 300, 'top': 0, 'left': 0},
                    {'width': 200, 'height': 300, 'top': 300, 'left': 0},
                ]
            }
        )

    def test_should_set_parents_size_based_on_min_bounded_children(self):
        self.assertLayout(
            {
                STYLE: {'min_width': 300, 'min_height': 700},
                CHILDREN: [
                    {STYLE: {'width': 200, 'height': 300}},
                    {STYLE: {'width': 200, 'height': 300}},
                ]
            },
            {
                'width': 300, 'height': 700, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 200, 'height': 300, 'top': 0, 'left': 0},
                    {'width': 200, 'height': 300, 'top': 300, 'left': 0},
                ]
            }
        )

    def test_should_keep_stretched_size_within_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'align_items': 'stretch'},
                CHILDREN: [
                    {STYLE: {'height': 100, 'min_height': 90, 'max_height': 110, 'min_width': 900, 'max_width': 1100}}
                ]
            },
            {
                'width': 1000, 'height': 100, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 1000, 'height': 100, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_keep_stretched_size_within_max_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'align_items': 'stretch'},
                CHILDREN: [
                    {STYLE: {'height': 100, 'max_height': 90, 'max_width': 900}}
                ]
            },
            {
                'width': 1000, 'height': 90, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 900, 'height': 90, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_keep_stretched_size_within_min_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'align_items': 'stretch'},
                CHILDREN: [
                    {STYLE: {'height': 100, 'min_height': 110, 'min_width': 1100}}
                ]
            },
            {
                'width': 1000, 'height': 110, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 1100, 'height': 110, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_keep_cross_axis_size_within_min_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'flex_direction': 'row'},
                CHILDREN: [
                    {STYLE: {'height': 100, 'min_height': 110, 'min_width': 100}}
                ]
            },
            {
                'width': 1000, 'height': 110, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 100, 'height': 110, 'top': 0, 'left': 0}
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_top_and_left_and_max_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {STYLE: {'position': 'absolute', 'top': 100, 'left': 100, 'bottom': 100, 'right': 100, 'max_width': 500, 'max_height': 600}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 500, 'height': 600, 'top': 100, 'left': 100},
                ]
            }
        )

    def test_should_layout_node_with_position_absolute_top_and_left_and_min_bounds(self):
        self.assertLayout(
            {
                STYLE: {'width': 1000, 'height': 1000},
                CHILDREN: [
                    {STYLE: {'position': 'absolute', 'top': 100, 'left': 100, 'bottom': 100, 'right': 100, 'min_width': 900, 'min_height': 1000}}
                ]
            },
            {
                'width': 1000, 'height': 1000, 'top': 0, 'left': 0,
                CHILDREN: [
                    {'width': 900, 'height': 1000, 'top': 100, 'left': 100},
                ]
            }
        )
