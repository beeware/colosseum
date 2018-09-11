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
        node.style.set(**{
            attr: value
            for attr, value in data['style'].items()
            if hasattr(node.style, attr)
        })

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


def summarize(node):
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
        if node.name:
            layout['tag'] = node.name
        children = []
        for child in node.children:
            sublayout = summarize(child)
            if sublayout:
                children.append(sublayout)
        if children:
            layout['children'] = children
    else:
        layout = None
    #     # TODO - add proper handling for anonymous boxes.
    #     layout = 'NOT DISPLAYED'

    return layout


def clean_layout(layout):
    if 'tag' in layout:
        cleaned = {
            key: {
                'position': (layout[key]['position'][0], layout[key]['position'][1]),
                'size': (layout[key]['size'][0], layout[key]['size'][1]),
            }
            for key in ['content', 'padding_box', 'border_box']
        }
        children = []
        for child in layout.get('children', []):
            sublayout = clean_layout(child)
            if sublayout:
                children.append(sublayout)
        if children:
            cleaned['children'] = children

    else:
        cleaned = None
    #     # TODO - add proper handling for anonymous boxes.
    #     cleaned = {
    #         'text': layout.get('text', '???')
    #     }

    return cleaned


def output_layout(layout, depth=1):
    if 'tag' in layout:
        return ('  ' * depth
            + '* {tag}{n[content][size][0]}x{n[content][size][1]}'
              ' @ ({n[content][position][0]}, {n[content][position][1]})'
              '\n'.format(
                    n=layout,
                    tag=('<' + layout['tag'] + '> ') if 'tag' in layout else '',
                    # text=(": '" + layout['text'] + "'") if 'text' in layout else ''
                )
            # + '  ' * depth
            # + '  padding: {n[padding_box][size][0]}x{n[padding_box][size][1]}'
            #   ' @ ({n[padding_box][position][0]}, {n[padding_box][position][1]})'
            #   '\n'.format(n=layout)
            # + '  ' * depth
            # + '  border: {n[border_box][size][0]}x{n[border_box][size][1]}'
            #   ' @ ({n[border_box][position][0]}, {n[border_box][position][1]})'
            #   '\n'.format(n=layout)
            + ''.join(
                    output_layout(child, depth=depth + 1)
                    for child in layout.get('children', [])
                ) if layout else ''
            + ('\n' if layout and layout.get('children', None) and depth > 1 else '')
        )
    else:
        return ('  ' * depth
            + "* '{text}'\n".format(text=layout['text'].strip())
        )


class LayoutTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.display = Display(dpi=96, width=1024, height=768)

    def layout_node(self, node):
        root = TestNode(style=CSS(display=BLOCK), children=[node])
        layout(self.display, root)

    def _assertLayout(self, actual, expected, output, depth=0):
        found_problem = False
        tag = ('<' + expected['tag'] + '> ') if 'tag' in expected else ''
        output.append(
            '    '
            + '    ' * depth
            + '* {tag}{n[size][0]}x{n[size][1]}'
              ' @ ({n[position][0]}, {n[position][1]})'.format(
                    n=expected['content'],
                    tag=tag,
                    text=(": '" + expected['text'] + "'") if 'text' in expected else ''
            )
        )

        content_match = (
            expected['content']['size'][0] == actual.layout.content_width
            and expected['content']['size'][1] == actual.layout.content_height
            and expected['content']['position'][0] == actual.layout.absolute_content_left
            and expected['content']['position'][1] == actual.layout.absolute_content_top
        )
        if not content_match:
            found_problem = True
            output.append(
                '>>  '
                + '    ' * depth
                + ' ' * len(tag)
                + '  {n.content_width}x{n.content_height}'
                  ' @ ({n.absolute_content_left}, {n.absolute_content_top})'.format(
                        n=actual.layout
                    )
            )

        output.append(
            '    '
            + '    ' * depth
            + ' ' * len(tag)
            + '  padding: {n[size][0]}x{n[size][1]}'
              ' @ ({n[position][0]}, {n[position][1]})'.format(
                    n=expected['padding_box']
                )
        )

        content_match = (
            expected['padding_box']['size'][0] == actual.layout.padding_box_width
            and expected['padding_box']['size'][1] == actual.layout.padding_box_height
            and expected['padding_box']['position'][0] == actual.layout.absolute_padding_box_left
            and expected['padding_box']['position'][1] == actual.layout.absolute_padding_box_top
        )
        if not content_match:
            found_problem = True
            output.append(
                '>>  '
                + '    ' * depth
                + ' ' * len(tag)
                + '  padding: {n.padding_box_width}x{n.padding_box_height}'
                  ' @ ({n.absolute_padding_box_left}, {n.absolute_padding_box_top})'.format(
                        n=actual.layout
                    )
            )

        output.append(
            '    '
            + '    ' * depth
            + ' ' * len(tag)
            + '  border: {n[size][0]}x{n[size][1]}'
              ' @ ({n[position][0]}, {n[position][1]})'.format(
                    n=expected['border_box']
                )
        )

        content_match = (
            expected['border_box']['size'][0] == actual.layout.border_box_width
            and expected['border_box']['size'][1] == actual.layout.border_box_height
            and expected['border_box']['position'][0] == actual.layout.absolute_border_box_left
            and expected['border_box']['position'][1] == actual.layout.absolute_border_box_top
        )
        if not content_match:
            found_problem = True
            output.append(
                '>>  '
                + '    ' * depth
                + ' ' * len(tag)
                + '  border: {n.border_box_width}x{n.border_box_height}'
                  ' @ ({n.absolute_border_box_left}, {n.absolute_border_box_top})'.format(
                        n=actual.layout
                    )
            )

        expected_children = expected.pop('children', [])
        n_actual = len(actual.children)
        n_expected = len(expected_children)
        if n_actual == n_expected:
            for actual_child, expected_child in zip(actual.children, expected_children):
                child_problem = self._assertLayout(actual_child, expected_child, output, depth=depth+1)
                found_problem = found_problem or child_problem
        else:
            found_problem = True
            output.append(
                '>>  '
                + '    ' * depth
                + '  Found {} children, expected {}'.format(
                n_actual, n_expected
            ))

        return found_problem

    def assertLayout(self, actual, expected, extra=''):
        output = ['\n', '~' * 80]
        problems = self._assertLayout(actual, expected, output)

        output.append('~' * 80)
        output.append(extra)
        if problems:
            self.fail('\n'.join(output))


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
                    reference,
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
                found = '-'.join(filename.split('.')[:-1]) == group
            if found:

                test_name, test_method = make_test(dirname, filename)
                if test_name not in ignore:
                    tests[test_name] = test_method

        return tests
