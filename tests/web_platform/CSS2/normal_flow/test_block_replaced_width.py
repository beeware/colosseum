from tests.utils import W3CTestCase


class TestBlockReplacedWidth(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "block-replaced-width-"))
