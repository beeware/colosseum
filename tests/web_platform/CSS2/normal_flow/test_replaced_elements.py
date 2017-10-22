from tests.utils import W3CTestCase

class TestReplacedElements(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'replaced-elements-'))

