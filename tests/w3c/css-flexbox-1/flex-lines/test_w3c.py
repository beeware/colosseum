import os
import json

from tests.utils import LayoutEngineTestCase, build_w3c_test


class FlexlinesTestCase(LayoutEngineTestCase):
    test_multi_line_wrap_reverse_column_reverse = build_w3c_test('css-flexbox-1/flex-lines/multi-line-wrap-reverse-column-reverse.json')
    test_multi_line_wrap_reverse_row_reverse = build_w3c_test('css-flexbox-1/flex-lines/multi-line-wrap-reverse-row-reverse.json')
    test_multi_line_wrap_with_column_reverse = build_w3c_test('css-flexbox-1/flex-lines/multi-line-wrap-with-column-reverse.json')
    test_multi_line_wrap_with_row_reverse = build_w3c_test('css-flexbox-1/flex-lines/multi-line-wrap-with-row-reverse.json')
