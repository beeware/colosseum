from tests.utils import W3CTestCase


class TestRtlSpanOnly(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "rtl-span-only"))
