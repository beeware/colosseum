from tests.utils import W3CTestCase


class TestGridFirstLetter(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, "grid-first-letter-"))
