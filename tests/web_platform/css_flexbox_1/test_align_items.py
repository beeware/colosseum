from tests.utils import W3CTestCase


class TestAlignItems(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "align-items-"))
