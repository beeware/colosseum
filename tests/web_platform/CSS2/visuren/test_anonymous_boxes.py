from tests.utils import W3CTestCase


class TestAnonymousBoxes(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "anonymous-boxes-"))
