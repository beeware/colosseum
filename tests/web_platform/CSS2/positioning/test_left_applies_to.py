from tests.utils import W3CTestCase

class TestLeftAppliesTo(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'left-applies-to-'))

