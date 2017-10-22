from tests.utils import W3CTestCase

class TestReplacedIntrinsic(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'replaced-intrinsic-'))

