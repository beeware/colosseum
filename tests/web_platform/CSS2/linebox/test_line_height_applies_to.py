from tests.utils import W3CTestCase


class TestLineHeightAppliesTo(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "line-height-applies-to-"))
