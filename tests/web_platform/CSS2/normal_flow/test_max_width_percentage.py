from tests.utils import W3CTestCase


class TestMaxWidthPercentage(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "max-width-percentage-"))
