import os
import json

from tests.utils import LayoutEngineTestCase, build_w3c_test


class ReferenceTestCase(LayoutEngineTestCase):
    test_flex_vertical_align_effect = build_w3c_test('css-flexbox-1/reference/flex-vertical-align-effect.json')
