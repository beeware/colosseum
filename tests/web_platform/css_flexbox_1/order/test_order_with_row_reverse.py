from tests.utils import W3CTestCase


class TestOrderWithRowReverse(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "order-with-row-reverse"))
