import re

from lexer_error import LexerError
from query import Query
from query_error import QueryError
from table import Table
from table_error import TableError

class Lexer:
    '''
    A parser for tables and queries.
    Consists of:
        - tables (Table)
        - queries (Query)
    Parses a document and extracts tables and queries.
    Each query is computed immediately to allow for the reassigning of table
    names later in the document.
    '''

    def compute(self, string):
        pass

    @staticmethod
    def is_table(string):
        ''' Check if string looks like a table header. '''
        pattern = re.compile(r'.*=.*\(.*\).*\{.*')
        return bool(pattern.match(string))

    @staticmethod
    def is_query(string, names):
        ''' Check if string looks like a query. '''
        return any(name in string for name in names)
