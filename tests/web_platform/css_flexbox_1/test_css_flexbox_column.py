from tests.utils import W3CTestCase


class TestCssFlexboxColumn(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "css-flexbox-column"))
