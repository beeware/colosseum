from tests.utils import W3CTestCase

class TestFlexibleOrder(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'Flexible-order'))

