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
        'position': (
            int(round(layout['position'][0])), int(round(layout['position'][1]))
        ),
        'size': (
            int(round(layout['size'][0])), int(round(layout['size'][1]))
        ),
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
    def find_tests(cls, test_filename, group):
        dirname = os.path.dirname(test_filename)
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
        def make_test(test_dir, filename):
            css_test_name = os.path.splitext(filename)[0]
            css_test_module = os.path.basename(os.path.dirname(test_dir))
            if css_test_module == 'CSS2':
                css_test_module = 'css21'
            test_name = 'test_' + css_test_name.replace('-', '_')

            with open(os.path.join(data_dir, filename)) as f:
                input_data = json.load(f)

            with open(os.path.join(ref_dir, filename)) as f:
                reference = json.load(f)

            # The actual test method. Builds a document, lays it out,
            # and checks against the reference rendering.
            def test_method(self):
                root = build_document(input_data['test_case'])

                layout(self.display, root)

                self.assertLayout(root, clean_layout(reference))

            # Annotate the method with any helper text.
            doc = []
            if input_data['assert']:
                doc.append(input_data['assert'])
            else:
                doc.append('Test ' + os.path.splitext(filename)[0].replace('-', '_'))

            doc.append('')
            if input_data['help']:
                doc.append('\n'.join('See {}'.format(h) for h in input_data['help']))

            doc.append('')
            doc.append(
                'Test: http://test.csswg.org/harness/test/{}_dev/single/{}/'.format(
                    css_test_module,
                    css_test_name
                )
            )

            test_method.__doc__ = '\n'.join(doc)

            # If the method is on the known not_implemented list,
            # decorate the method.
            if test_name in not_implemented:
                test_method = expectedFailure(test_method)

            return test_name, test_method

        # Find all the data files, and build a test case for each test group
        # that is represented there.
        tests = {}
        for filename in os.listdir(data_dir):
            if group.endswith('-'):
                found = '-'.join(filename.split('-')[:-1]) == group[:-1]
            else:
                found = filename == group
            if found:

                test_name, test_method = make_test(dirname, filename)
                tests[test_name] = test_method

        return tests
