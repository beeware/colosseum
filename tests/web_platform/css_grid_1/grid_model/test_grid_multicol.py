from tests.utils import W3CTestCase

class TestGridMulticol(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'grid-multicol-'))

