from tests.utils import W3CTestCase

class TestLtrSpanOnly(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'ltr-span-only'))

