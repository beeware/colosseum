from tests.utils import W3CTestCase


class TestGridLayoutBasic(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "grid-layout-basic"))
