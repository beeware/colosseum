from tests.utils import W3CTestCase

class TestBlockInInlineNested(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'block-in-inline-nested-'))

