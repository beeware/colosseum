from tests.utils import W3CTestCase

class TestRtlIb(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'rtl-ib'))

