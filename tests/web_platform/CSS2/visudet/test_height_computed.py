from tests.utils import W3CTestCase

class TestHeightComputed(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'height-computed-'))

