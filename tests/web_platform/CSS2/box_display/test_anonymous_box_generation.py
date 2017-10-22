from tests.utils import W3CTestCase

class TestAnonymousBoxGeneration(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'anonymous-box-generation-'))

