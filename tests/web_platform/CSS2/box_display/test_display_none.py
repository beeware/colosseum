from tests.utils import W3CTestCase


class TestDisplayNone(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "display-none-"))
