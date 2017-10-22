from tests.utils import W3CTestCase

class TestFrUnitWithPercentage(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'fr-unit-with-percentage'))

