from tests.utils import W3CTestCase


class TestAbsolutePositioningGridContainerContainingBlock(W3CTestCase):
    vars().update(
        W3CTestCase.find_tests(
            __file__, "absolute-positioning-grid-container-containing-block-"
        )
    )
