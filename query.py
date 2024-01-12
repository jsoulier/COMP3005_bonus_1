import re

from query_node import QueryNode

class Query:
    ''' A tree representation of a query. '''

    def __init__(self, string, tables):
        ''''''
        self.root = QueryNode()
        self.root.string = string
        self.root.tables = tables
        self.root.parse()
