from tests.utils import W3CTestCase


class TestInlineBlockReplacedHeight(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "inline-block-replaced-height-"))
