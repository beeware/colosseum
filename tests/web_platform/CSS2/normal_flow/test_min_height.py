from tests.utils import W3CTestCase


class TestMinHeight(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "min-height-"))
