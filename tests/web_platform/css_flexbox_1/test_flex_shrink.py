from tests.utils import W3CTestCase

class TestFlexShrink(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'flex-shrink-'))

