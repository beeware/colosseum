from tests.utils import W3CTestCase


class TestTableInInline(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'table-in-inline-'))
