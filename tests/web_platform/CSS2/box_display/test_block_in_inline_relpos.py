from tests.utils import W3CTestCase


class TestBlockInInlineRelpos(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "block-in-inline-relpos-"))
