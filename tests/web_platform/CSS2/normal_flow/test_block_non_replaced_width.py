from tests.utils import W3CTestCase


class TestBlockNonReplacedWidth(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "block-non-replaced-width-"))
