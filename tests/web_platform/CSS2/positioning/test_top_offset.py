from tests.utils import W3CTestCase


class TestTopOffset(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "top-offset-"))
