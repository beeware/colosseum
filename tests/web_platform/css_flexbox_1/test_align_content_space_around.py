from tests.utils import W3CTestCase


class TestAlignContent_SpaceAround(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "align-content_space-around"))
