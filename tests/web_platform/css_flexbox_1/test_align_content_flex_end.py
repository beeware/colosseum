from tests.utils import W3CTestCase


class TestAlignContent_FlexEnd(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "align-content_flex-end"))
