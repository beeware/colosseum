from tests.utils import W3CTestCase


class TestTtwfReftestFlexWrapReverse(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "ttwf-reftest-flex-wrap-reverse"))
