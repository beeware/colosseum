import argparse
import json
import os
from subprocess import check_output

from colosseum.declaration import _CSS_PROPERTIES
from selenium import webdriver


SCRIPT = """
    var el = arguments[0]
    var style = window.getComputedStyle(el)
    var style_obj = {}
    for (var i = 0; i < style.length; i++){
        style_obj[style[i]] = style.getPropertyValue(style[i])
    }
    return style_obj
"""

TEST_HARNESS_STUB = """import os
import json

from tests.utils import LayoutEngineTestCase, build_w3c_test


class %sTestCase(LayoutEngineTestCase):
"""


def _get_filtered_style(driver, element):
    """Get the style attributes we care about for a given element."""
    css = driver.execute_script(SCRIPT, element)
    return {k: v for k, v in css.items() if k in _CSS_PROPERTIES}


def _get_node_data(driver, element, x_offset, y_offset):
    """Recursively get node_data for an element and its children."""
    position = element.rect
    position['left'] = position['x'] - x_offset
    position['top'] = position['y'] - y_offset
    del position['x']
    del position['y']
    return {
        'style': _get_filtered_style(driver, element),
        'position': position,
        'children': [
            _get_node_data(driver, child, x_offset, y_offset)
            for child in element.find_elements_by_xpath("./*")
        ],
    }


class WrongStructureException(Exception):
    pass


class SuiteBuilder(object):
    def __init__(self, w3c_root, output_dir, browser, section):
        self.w3c_root = w3c_root
        self.output_dir = output_dir
        sha_bytes = check_output(('git', 'rev-parse', 'HEAD'), cwd=w3c_root)
        self.w3c_sha = sha_bytes.decode('utf8').strip()
        self.browser = browser
        self.section = section

    def fetch_single_test(self, driver, w3c_path):
        """Get the test data for a single test.

        Will raise WrongStructureException if the test does not have a)
        a body element with a single child, or b) a body element with
        two children, the first of which is a <p> (which is ignored).
        """
        url = "file://{}/{}".format(os.path.abspath(self.w3c_root), w3c_path)
        driver.get(url)
        body = driver.find_element_by_css_selector('body')
        body_children = body.find_elements_by_xpath("./*")
        if len(body_children) == 2 and body_children[0].tag_name == "p":
            root_element = body_children[1]
        elif len(body_children) == 1:
            root_element = body_children[0]
        else:
            raise WrongStructureException()
        location = root_element.location
        x_offset, y_offset = location['x'], location['y']

        return {
            'node_data': _get_node_data(driver, root_element, x_offset, y_offset),
            'w3c_path': w3c_path,
        }

    def run(self):
        """Run the test data generator."""
        # TODO: Run under multiple drivers and check result consistency
        driver = getattr(webdriver, self.browser)()
        try:
            if self.section is None:
                sections = [
                    d
                    for d in os.listdir(self.output_dir)
                    if os.path.isdir(os.path.join(self.output_dir, d))
                    and d != '__pycache__'
                ]
            else:
                sections = [self.section]

            for section in sections:
                section_dir = os.path.join(self.w3c_root, section)
                for dirpath, dirnames, filenames in os.walk(section_dir):
                    dirname = dirpath[len(self.w3c_root):]
                    print("Process directory {}...".format(dirname))
                    missing = []
                    present = []
                    for filename in filenames:
                        if '-ref.' not in filename and (
                                    filename.endswith(".htm")
                                    or filename.endswith('.html')
                                    or filename.endswith('.xht')
                                ):
                            try:
                                print("    Generating case for {}/{} ...".format(dirname, filename))
                                test_data = self.fetch_single_test(
                                    driver, os.path.join(dirname, filename)
                                )

                                try:
                                    os.makedirs(os.path.join(self.output_dir, dirname))
                                    with open(os.path.join(self.output_dir, dirname, '__init__.py'), 'w') as f:
                                        pass
                                except OSError:
                                    pass
                                result = os.path.join(
                                    self.output_dir,
                                    dirname,
                                    os.path.splitext(filename)[0]
                                ) + '.json'

                                with open(result, 'w') as f:
                                    json.dump(test_data, f, indent=4, sort_keys=True)

                                present.append(result[len(self.output_dir) + 1:])
                            except WrongStructureException:
                                print("    ... skipping because it doesn't fit the expected structure")
                                missing.append(filename)

                    if present:
                        testfile = os.path.join(self.output_dir, dirname, 'test_w3c.py')
                        if os.path.isfile(testfile):
                            testfile = os.path.join(self.output_dir, dirname, 'test_w3c_new.py')

                        with open(testfile, 'w') as f:
                            f.write(TEST_HARNESS_STUB % os.path.basename(dirname).replace('-', '').title())
                            for filename in present:
                                test_name = os.path.splitext(os.path.basename(filename))[0].replace('-', '_')
                                f.write("    test_%s = build_w3c_test('%s')\n" % (test_name, filename))

                        with open(os.path.join(self.output_dir, dirname, 'missing.json'), 'w') as f:
                            json.dump({
                                    'w3c_sha': self.w3c_sha,
                                    'missing': missing
                                }, f, indent=4, sort_keys=True)

        finally:
            driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='w3c_update',
        description='Update W3C CSS test suite reference data'
    )

    parser.add_argument(
        '-b', '--browser',
        help='The browser backend to use',
        default='Firefox'
    )

    parser.add_argument(
        '-o', '--output',
        help='The output directory',
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'w3c')
    )

    parser.add_argument(
        '-s', '--section',
        help='The top level test section to process',
        default=None
    )

    parser.add_argument(
        'source',
        metavar='<w3c source directory>',
        help='The path to the https://github.com/w3c/csswg-test checkout'
    )

    args = parser.parse_args()

    SuiteBuilder(
        w3c_root=args.source,
        output_dir=args.output,
        browser=args.browser,
        section=args.section
    ).run()
