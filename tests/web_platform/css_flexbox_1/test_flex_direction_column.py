from tests.utils import W3CTestCase


class TestFlexDirection_Column(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "flex-direction_column"))
