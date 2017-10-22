from tests.utils import W3CTestCase

class TestBidiUnicodeBidi(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'bidi-unicode-bidi-'))

