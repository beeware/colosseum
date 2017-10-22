from tests.utils import W3CTestCase

class TestBidiTable(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'bidi-table-'))

