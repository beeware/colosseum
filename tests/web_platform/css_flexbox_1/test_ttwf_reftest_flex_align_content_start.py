from tests.utils import W3CTestCase


class TestTtwfReftestFlexAlignContentStart(W3CTestCase):
    vars().update(
        W3CTestCase.find_tests(__file__, "ttwf-reftest-flex-align-content-start")
    )
