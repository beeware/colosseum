from tests.utils import W3CTestCase


class TestCssFlexboxColumnReverseWrapReverse(W3CTestCase):
    vars().update(
        W3CTestCase.find_tests(__file__, "css-flexbox-column-reverse-wrap-reverse")
    )
