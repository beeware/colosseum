from tests.utils import W3CTestCase

class TestGridContentDistribution(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'grid-content-distribution-'))

