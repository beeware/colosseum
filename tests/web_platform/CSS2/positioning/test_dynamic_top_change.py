from tests.utils import W3CTestCase

class TestDynamicTopChange(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'dynamic-top-change-'))

