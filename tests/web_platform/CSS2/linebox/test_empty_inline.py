from tests.utils import W3CTestCase

class TestEmptyInline(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'empty-inline-'))

