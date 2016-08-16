from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from time import time
from subprocess import check_output
from os import chdir, listdir
from os.path import abspath, join, split
from sys import argv

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
        'children': [_get_node_data(driver, child, x_offset, y_offset) 
                     for child in element.find_elements_by_xpath("./*")],
    }

def get_test_data(driver, url, root_selector, w3c_root, w3c_path, w3c_sha):
    url = "file://{}/{}".format(w3c_root, w3c_path)


class WrongStructureException(Exception):
    pass
    

class TestDataGetter(object):
    def __init__(self, w3c_root, output_dir):
        self.w3c_root = w3c_root
        self.output_dir = output_dir
        sha_bytes = check_output(('git', 'rev-parse', 'HEAD'), cwd=w3c_root)
        self.w3c_sha = sha_bytes.decode('utf8').strip()
    
    def fetch_single_test(self, driver, w3c_path):
        url = "file://{}/{}".format(abspath(self.w3c_root), w3c_path)
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
            'capabilities': driver.capabilities,
            'node_data': _get_node_data(driver, root_element, x_offset, y_offset),
            'stored_time': time(),
            'w3c_path': w3c_path,
            'w3c_sha': self.w3c_sha,
        }

    def run(self):
        driver = webdriver.Firefox()
        try:
            for path in listdir(join(self.w3c_root, "css-flexbox-1")):
                if not (path.endswith(".htm") or path.endswith('.html')) or 'ref' in path:
                    continue
                try:
                    test_data = self.fetch_single_test(
                        driver, join('css-flexbox-1', path)
                    )
                    print("Generating case for {}".format(path))
                except WrongStructureException:
                    print("Skipping {} because it doesn't fit the expected"
                          "structure".format(path))
                    continue
                path = join(self.output_dir, path.replace('/', '_')) + '.json'
                with open(path, 'w') as f:
                    json.dump(test_data, f, indent=4, sort_keys=True)
        finally:
            driver.close()

def main():
    output_dir = join(split(__file__)[0], 'w3c_test_data')
    data = TestDataGetter(argv[1], output_dir).run()

if __name__ == "__main__":
    main()
