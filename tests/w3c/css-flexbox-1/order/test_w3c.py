import os
import json

from tests.utils import LayoutEngineTestCase, build_w3c_test


class OrderTestCase(LayoutEngineTestCase):
    test_order_with_column_reverse = build_w3c_test('css-flexbox-1/order/order-with-column-reverse.json')
    test_order_with_row_reverse = build_w3c_test('css-flexbox-1/order/order-with-row-reverse.json')
