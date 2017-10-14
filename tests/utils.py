import json
import os
from unittest import TestCase, expectedFailure

from colosseum.constants import MEDIUM, THICK, THIN
from colosseum.declaration import CSS
from colosseum.dimensions import Box, Size
from colosseum.engine import layout


class Display:
    def __init__(self, dpi, width, height):
        self.dpi = dpi
        self.content_width = width
        self.content_height = height

    def fixed_size(self, value):
        return {
            THIN: 1,
            MEDIUM: 5,
            THICK: 10,
        }[value]


class TestNode:
    def __init__(self, style=None, children=None):
        self.parent = None
        self.children = []
        if children:
            for child in children:
                self.children.append(child)
                child.parent = self
        self.intrinsic = Size(self)
        self.layout = Box(self)
        self.style = style.copy(self) if style else CSS()


def build_document(data):
    node = TestNode()
    node.style.set(**data['style'])

    if 'children' in data:
        for child in data['children']:
            node.children.append(build_document(child))

    return node

def clean_layout(layout):
    clean = {
        'position': (round(layout['position'][0]), round(layout['position'][1])),
        'size': (round(layout['size'][0]), round(layout['size'][1])),
    }
    if 'children' in layout:
        clean['children'] = [
            clean_layout(child)
            for child in layout['children']
        ]
    return clean

def layout_summary(node):
    if node.layout:
        layout = {
            'position': (node.layout.absolute_content_left, node.layout.absolute_content_top),
            'size': (node.layout.content_width, node.layout.content_height),
        }
        if node.children:
            layout['children'] = [
                layout_summary(child)
                for child in node.children
            ]
    else:
        layout = 'NOT DISPLAYED'

    return layout


class LayoutTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.display = Display(dpi=96, width=640, height=480)

    def assertLayout(self, node, layout):
        self.assertEqual(layout_summary(node), layout)


class W3CTestCase(LayoutTestCase):
    @classmethod
    def find_tests(cls, filename, group):
        dirname = os.path.dirname(filename)
        data_dir = os.path.join(dirname, 'data')
        ref_dir = os.path.join(dirname, 'ref')

        # Read the not_implemented file.
        not_implemented_file = os.path.join(dirname, 'not_implemented')
        try:
            with open(not_implemented_file) as f:
                not_implemented = set(
                    'test_' + line.strip().replace('-', '_')
                    for line in f
                    if line.strip()
                )
        except IOError:
            not_implemented = set()

        # Closure for building test cases for a given input file.
        def make_test(data_filename):
            test_name = 'test_' + os.path.splitext(data_filename)[0].replace('-', '_')

            with open(os.path.join(data_dir, data_filename)) as f:
                input_data = json.load(f)

            # If the file has a reference file, use it;
            # otherwise it is it's own reference.
            if input_data['matches']:
                ref_filename = os.path.splitext(input_data['matches'])[0] + '.json'
            else:
                ref_filename = data_filename

            try:
                with open(os.path.join(ref_dir, ref_filename)) as f:
                    reference = json.load(f)
            except IOError:
                reference = {'error': 'REFERENCE DATA IS MISSING'}

            # The actual test method. Builds a document, lays it out,
            # and checks against the reference rendering.
            def test_method(self):
                root = build_document(input_data['test_case'])

                layout(self.display, root)

                self.assertLayout(root, clean_layout(reference))

            # Annotate the method with any helper text.
            if input_data['assert']:
                if input_data['help']:
                    test_method.__doc__ = "{}\n\n{}".format(
                        input_data['assert'],
                        '\n'.join('See {}'.format(h) for h in input_data['help'])
                    )
                else:
                    test_method.__doc__ = input_data['assert']
            else:
                if input_data['help']:
                    test_method.__doc__ = "Test {}\n\n{}".format(
                        os.path.splitext(data_filename)[0].replace('-', '_'),
                        '\n'.join('See {}'.format(h) for h in input_data['help'])
                    )

            # If the method is on the known not_implemented list,
            # decorate the method.
            if test_name in not_implemented:
                test_method = expectedFailure(test_method)

            return test_name, test_method

        # Find all the data files, and build a test case for each test group
        # that is represented there.
        tests = {}
        for data_filename in os.listdir(data_dir):
            if data_filename.startswith(group):
                test_name, test_method = make_test(data_filename)
                tests[test_name] = test_method

        return tests
