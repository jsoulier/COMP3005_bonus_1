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
    Handles table and query exceptions and passes back the offending string.
    '''

    def __init__(self):
        ''''''
        self.tables = []
        self.queries = []

    def extract(self, string):
        ''' Populate tables and queries. '''
        self.tables = []
        self.queries = []

        # Keep track of table lines and names
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
                string = '\n'.join(strings)

                # Pass back exceptions to user
                try:
                    table = Table(string)
                except TableError:
                    raise LexerError('Bad Table Formatting: {}'.format(string))
                except:
                    raise LexerError('Unknown Error: {}'.format(string))

                # Reset tracking
                self.tables.append(table)
                names.append(table.name)
                strings = []

        # Missing table end
        if strings:
            raise LexerError('Unmatched Parenthesis')

    def compute(self, string):
        ''' Compute tables. '''
        tables = []

        # Extract and compute tables
        self.extract(string)
        for query in self.queries:

            # Pass back exceptions to user
            try:
                tables.append(query.compute())
            except QueryError:
                raise LexerError('Bad Query Formatting: {}'.format(query.string))
            except TableError:
                raise LexerError('Invalid Table Operation: {}'.format(query.string))
            except:
                raise LexerError('Unknown Error: {}'.format(query.string))

        return tables

    @staticmethod
    def table_start(string):
        ''' Check if string starts a table. '''
        pattern = re.compile(r'.*\(.*\).*=.*\{.*')
        return pattern.search(string)

    @staticmethod
    def table_end(string):
        ''' Check if string ends a table. '''
        return '}' in string

    @staticmethod
    def query(string, names):
        ''' Check if string is a query. '''
        return any(name in string for name in names)
