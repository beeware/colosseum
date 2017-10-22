from tests.utils import W3CTestCase

class TestInlineBlock(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'inline-block-'))

