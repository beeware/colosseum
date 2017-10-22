from tests.utils import W3CTestCase

class TestBidiDirection(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'bidi-direction-'))

