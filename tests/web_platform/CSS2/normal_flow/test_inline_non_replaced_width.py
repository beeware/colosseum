from tests.utils import W3CTestCase


class TestInlineNonReplacedWidth(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "inline-non-replaced-width-"))
