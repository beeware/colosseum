import json
import os
from unittest import TestCase, expectedFailure

from colosseum.constants import BLOCK, HTML4, MEDIUM, THICK, THIN
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
    def __init__(self, name=None,style=None, children=None):
        self.name = name if name else 'div'
        self.parent = None
        self.children = []
        if children:
            for child in children:
                self.children.append(child)
                child.parent = self
        self.intrinsic = Size(self)
        self.layout = Box(self)
        self.style = style.copy(self) if style else CSS()

    def __repr__(self):
        return '<{}:{} {}>'.format(self.name, id(self), str(self.layout))


def build_document(data):
    if 'tag' in data:
        node = TestNode(name=data['tag'])
        node.style.set(**data['style'])

        if 'children' in data:
            for child in data['children']:
                subdocument = build_document(child)
                if subdocument:
                    node.children.append(subdocument)
    else:
        node = None
    #     # TODO - add proper handling for anonymous boxes.
    #     node = TestNode(name='<anon>')
    #     node.intrinsic.width = ...
    #     node.intrinsic.height = ...
    return node


def layout_summary(node):
    if node.layout:
        layout = {
            'content': {
                'position': (node.layout.absolute_content_left, node.layout.absolute_content_top),
                'size': (node.layout.content_width, node.layout.content_height),
            },
            'padding_box': {
                'position': (node.layout.absolute_padding_box_left, node.layout.absolute_padding_box_top),
                'size': (node.layout.padding_box_width, node.layout.padding_box_height),
            },
            'border_box': {
                'position': (node.layout.absolute_border_box_left, node.layout.absolute_border_box_top),
                'size': (node.layout.border_box_width, node.layout.border_box_height),
            },
        }
        children = []
        for child in node.children:
            sublayout = layout_summary(child)
            if sublayout:
                children.append(sublayout)
        if children:
            layout['children'] = children
    else:
        layout = None
    #     # TODO - add proper handling for anonymous boxes.
    #     layout = 'NOT DISPLAYED'

    return layout


def clean_reference(reference):
    if 'tag' in reference:
        cleaned = {
            key: {
                'position': (reference[key]['position'][0], reference[key]['position'][1]),
                'size': (reference[key]['size'][0], reference[key]['size'][1]),
            }
            for key in ['content', 'padding_box', 'border_box']
        }

        children = []
        for child in reference.get('children', []):
            subreference = clean_reference(child)
            if subreference:
                children.append(subreference)
        if children:
            cleaned['children'] = children

    else:
        cleaned = None
    #     # TODO - add proper handling for anonymous boxes.
    #     cleaned = {
    #         'text': reference.get('text', '???')
    #     }

    return cleaned


def output_layout(layout, depth=1):
    return ('  ' * depth
        + '* {n[content][size][0]}x{n[content][size][1]}'
          ' @ ({n[content][position][0]}, {n[content][position][1]})'
          '\n'.format(n=layout)
        # + '  ' * depth
        # + '  {n[padding_box][size][0]}x{n[padding_box][size][1]}'
        #   ' @ ({n[padding_box][position][0]}, {n[padding_box][position][1]})'
        #   '\n'.format(n=layout)
        # + '  ' * depth
        # + '  {n[border_box][size][0]}x{n[border_box][size][1]}'
        #   ' @ ({n[border_box][position][0]}, {n[border_box][position][1]})'
        #   '\n'.format(n=layout)
        # + '  ' * depth
        # + '  {n[margin_box][size][0]}x{n[margin_box][size][1]}'
        #   ' @ ({n[margin_box][position][0]}, {n[margin_box][position][1]})'
        #   '\n'.format(n=layout)
        + ''.join(
                output_layout(child, depth=depth + 1)
                for child in layout.get('children', [])
            ) if layout else ''
        + ('\n' if layout and layout.get('children', None) and depth > 1 else '')
    )


class LayoutTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.display = Display(dpi=96, width=640, height=480)

    def layout_node(self, node):
        root = TestNode(style=CSS(display=BLOCK), children=[node])
        layout(self.display, root)

    def assertLayout(self, node, reference, extra=''):
        self.assertEqual(
            layout_summary(node),
            reference,
            '\n\nExpected:\n{}Actual:\n{}{}'.format(
                output_layout(reference),
                output_layout(layout_summary(node)),
                extra
            )
        )


class W3CTestCase(LayoutTestCase):
    @classmethod
    def find_tests(cls, test_filename, group):
        dirname = os.path.dirname(test_filename)
        data_dir = os.path.join(dirname, 'data')
        ref_dir = os.path.join(dirname, 'ref')

        # Read the not_implemented file.
        expected_failures = set()
        not_implemented_file = os.path.join(dirname, 'not_implemented')
        try:
            with open(not_implemented_file) as f:
                expected_failures.update({
                    'test_' + line.strip().replace('-', '_')
                    for line in f
                    if line.strip()
                })
        except IOError:
            pass

        not_compliant = os.path.join(dirname, 'not_compliant')
        try:
            with open(not_compliant) as f:
                expected_failures.update({
                    'test_' + line.strip().replace('-', '_')
                    for line in f
                    if line.strip()
                })
        except IOError:
            pass

        # Read the not_valid test file.
        ignore = set()
        not_valid_file = os.path.join(dirname, 'not_valid')
        try:
            with open(not_valid_file) as f:
                ignore.update({
                    'test_' + line.strip().replace('-', '_')
                    for line in f
                    if line.strip()
                })
        except IOError:
            pass

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

            extra = []
            if input_data['help']:
                extra.append('\n'.join('See {}'.format(h) for h in input_data['help']))
                extra.append('')

            extra.append(
                'Test: http://test.csswg.org/harness/test/{}_dev/single/{}/'.format(
                    css_test_module,
                    css_test_name
                )
            )

            # The actual test method. Builds a document, lays it out,
            # and checks against the reference rendering.
            def test_method(self):
                root = build_document(input_data['test_case'])

                layout(self.display, root, standard=HTML4)

                self.assertLayout(
                    root,
                    clean_reference(reference),
                    '\n' + '\n'.join(extra)
                )

            # Annotate the method with any helper text.
            doc = []
            if input_data['assert']:
                doc.append(input_data['assert'])
            else:
                doc.append('Test ' + os.path.splitext(filename)[0].replace('-', '_'))

            doc.append('')
            doc.extend(extra)

            test_method.__doc__ = '\n'.join(doc)

            # If the method is on the expected_failures list,
            # decorate the method.
            if test_name in expected_failures:
                test_method = expectedFailure(test_method)

            return test_name, test_method

        # Find all the data files, and build a test case for each test group
        # that is represented there. Exclude any test that is explicitly
        # on the ignore list.
        tests = {}
        for filename in os.listdir(data_dir):
            if group.endswith('-'):
                found = '-'.join(filename.split('-')[:-1]) == group[:-1]
            else:
                found = filename == group
            if found:

                test_name, test_method = make_test(dirname, filename)
                if test_name not in ignore:
                    tests[test_name] = test_method

        return tests
