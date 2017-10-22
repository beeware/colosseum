from tests.utils import W3CTestCase

class TestTopAppliesTo(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'top-applies-to-'))

