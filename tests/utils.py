import os
import json
from unittest import TestCase, expectedFailure

from colosseum.layout import CSS


STYLE = 'style'
CHILDREN = 'children'


class TestLayout:
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
    # Style dirtiness tracking.
    ######################################################################

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for child in self.node.children:
            child.layout.dirty = value


class TestNode:
    def __init__(self, style=None, children=None):
        self.parent = None
        self._children = []
        if children:
            for child in children:
                self.add(child)

        self.layout = TestLayout(self)
        if style:
            self._style = style.apply(self)
        else:
            self._style = CSS().apply(self)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value.apply(self)

    @property
    def children(self):
        return self._children

    def add(self, child):
        self._children.append(child)
        child.parent = self.parent
        if self.parent:
            self.parent.layout.dirty = True

    ######################################################################
    # Calculate layout
    ######################################################################

    def recompute(self):
        if self.layout.dirty:
            self.layout.reset()
            self.style.recompute(None)
            self.layout.dirty = False


class LayoutEngineTestCase(TestCase):
    ######################################################################
    # Utility methods
    ######################################################################

    def _add_children(self, node, children):
        for child_data in children:
            child = TestNode(style=CSS(**child_data[STYLE]))
            self._add_children(child, child_data.get(CHILDREN, []))
            node.children.append(child)

    def _assertLayout(self, node, layout):
        # Internal recursive method for checking a node's layout
        child_layouts = layout.pop(CHILDREN, [])
        self.assertEqual(node.layout, TestLayout(None, **layout))
        for child, child_layout in zip(node.children, child_layouts):
            self._assertLayout(child, child_layout)

    def assertLayout(self, node_data, layout):
        # Recursively create the node and children
        node = TestNode(style=CSS(**node_data[STYLE]))
        self._add_children(node, node_data.get(CHILDREN, []))

        # Compute the layout.
        node.recompute()
        # Recursively compare the layout
        self._assertLayout(node, layout)


def node_data(data):
    """
    Obtain a dict from definition['node_data'] that has the expected format
    of the `node_data` arg in `_LayoutEngineTest.assertLayout`
    """
    return {
        STYLE: data[STYLE],
        CHILDREN: [
            node_data(node) for node in data[CHILDREN]
        ]
    }


def layout(data):
    return {
        'width': data['position']['width'],
        'height': data['position']['height'],
        'left': data['position']['left'],
        'top': data['position']['top'],
        CHILDREN: [
            layout(node) for node in data[CHILDREN]
        ]
    }


def build_w3c_test(path, known_failure=True):
    def test(self):
        with open(os.path.join(os.path.dirname(__file__), 'w3c', path), 'r') as fd:
            definition = json.loads(fd.read())

            self.assertLayout(
                node_data(definition['node_data']),
                layout(definition['node_data'])
            )
    if known_failure:
        test = expectedFailure(test)

    return test
