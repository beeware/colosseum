from tests.utils import W3CTestCase


class TestFlexbox_TableFixedLayout(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "flexbox_table-fixed-layout"))
