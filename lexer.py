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
    '''

    def __init__(self):
        ''''''
        self.tables = []
        self.queries = []

    def extract(self, string):
        ''' Populate tables and queries from string. '''
        self.tables = []
        self.queries = []

        lines = string.splitlines()
        strings = []
        names = []

        for line in lines:

            # Start tracking lines
            if self.table_start(line):
                strings.append(line)
                continue

            if not strings:
                # Create query from line and tables
                if self.query(line, names):
                    self.queries.append(Query(line, self.tables))
                continue

            # Add lines and complete table
            strings.append(line)
            if self.table_end(line):
                table = Table('\n'.join(strings))
                self.tables.append(table)
                names.append(table.name)
                strings = []

        # Missing table end
        if strings:
            raise LexerError()

    def compute(self, string):
        ''''''
        tables = []
        return tables

    @staticmethod
    def table_start(string):
        ''' Check if string looks like it starts a table. '''
        pattern = re.compile(r'.*\(.*\).*=.*\{.*')
        return pattern.search(string)

    @staticmethod
    def table_end(string):
        ''' Check if string looks like it ends a table. '''
        return '}' in string

    @staticmethod
    def query(string, names):
        ''' Check if string looks like a query. '''
        return any(name in string for name in names)
