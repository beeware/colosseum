from tests.utils import W3CTestCase


class TestJustifyContent_FlexEnd(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "justify-content_flex-end"))
