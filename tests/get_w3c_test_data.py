from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from time import time
from subprocess import check_output
from os import chdir
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
    

class TestDataGetter(object):
    tests = [
        ('css-flexbox-1/align-content-001.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content-002.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content-003.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content-004.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content-005.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content-006.htm', 'div#flexbox'),
        ('css-flexbox-1/align-content_center.html', 'div#test'),
        ('css-flexbox-1/align-content_flex-end.html', 'div#test'),
        ('css-flexbox-1/align-content_flex-start.html', 'div#test'),
    ]

    def __init__(self, w3c_root, output_dir):
        self.w3c_root = w3c_root
        self.output_dir = output_dir
        sha_bytes = check_output(('git', 'rev-parse', 'HEAD'), cwd=w3c_root)
        self.w3c_sha = sha_bytes.decode('utf8').strip()
    
    def fetch_single_test(self, driver, w3c_path, root_selector):
        url = "file://{}/{}".format(abspath(self.w3c_root), w3c_path)
        driver.get(url)
        root_element = driver.find_elements_by_css_selector(root_selector)[0]
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
            for path, selector in self.tests:
                print("Generating {}".format(path))
                test_data = self.fetch_single_test(driver, path, selector)
                path = join(self.output_dir, path.replace('/', '_')) + '.json'
                with open(path, 'w') as f:
                    json.dump(test_data, f, indent=4, sort_keys=True)
        finally:
            driver.close()

def main():
    output_dir = join(split(__file__)[0], 'w3c_test_data')
    data = TestDataGetter(argv[1], output_dir).run()
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()
