import re

from query_error import QueryError
from query_node_type import QueryNodeType
from table_operator import TableOperator

class QueryNode:
    """ A tree representation of a query node. """

    def __init__(self, string, tables, type):
        """"""
        self.string = string
        self.tables = tables
        self.type = type

        self.start = len(string)
        self.end = len(string)
        self.table = None
        self.table_operator = TableOperator.NONE
        self.table_operator_string = ""

        self.node1 = None
        self.node2 = None
        self.node3 = None

    def populate(self):
        """"""
        self.node1 = self.next(self.string)
        if self.node1.type == QueryNodeType.TABLE:
            pass

        if self.node1.type == QueryNodeType.TABLE_OPERATOR:
            pass

        if self.node1.type == QueryNodeType.GROUP:
            pass

    @staticmethod
    def pair(string):
        """ Find the index of the matching parenthesis. """
        count = 1
        for i, char in enumerate(string):
            if char == '(':
                count += 1
                continue
            if char == ')':
                count -= 1
                if not count:
                    return i
        raise QueryError('Unmatched Parentheses: {}'.format(string))

    def next(self, string):
        """"""
        table = QueryNode(string, self.tables, QueryNodeType.TABLE)
        table_operator = QueryNode(string, self.tables, QueryNodeType.TABLE_OPERATOR)
        group = QueryNode(string, self.tables, QueryNodeType.GROUP)

        # Find the first table
        for i in self.tables:
            if not i.name:
                continue
            result = self.search(string, i.name)
            if not result:
                continue
            if result.start(1) > table.start:
                continue
            table.table = i
            table.start = result.start(1)

        # Find the first TableOperator
        for i in TableOperator:
            for j in i.strings:
                result = self.search(string, j)
                if not result:
                    continue
                if result.start(1) > table_operator.start:
                    continue
                table_operator.table_operator = i
                table_operator.table_operator_string = j
                table_operator.start = result.start(1)

        # Find the first parenthesis
        group.start = string.find('(')
        if group.start == -1:
            group.start = len(string)

        result = sorted([table, table_operator, group])[0]
        return result
    
    def __lt__(self, other):
        """"""
        return self.start < other.start

    @staticmethod
    def search(string1, string2):
        """ Search for the first occurrence of the modified string2 in string1. """
        pattern = r'(^|\s|\()' + re.escape(string2) + r'($|\s|\))'
        return re.search(pattern, string1)
