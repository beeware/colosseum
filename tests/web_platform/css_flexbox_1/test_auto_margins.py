from tests.utils import W3CTestCase

class TestAutoMargins(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'auto-margins-'))

