from tests.utils import W3CTestCase


class TestDisplayGrid(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "display-grid"))
