from tests.utils import W3CTestCase


class TestFlexbox_FlexNaturalMixedBasisAuto(W3CTestCase):
    vars().update(
        W3CTestCase.find_tests(__file__, "flexbox_flex-natural-mixed-basis-auto")
    )
