import re

from query_error import QueryError
from query_node_type import QueryNodeType
from table_operator import TableOperator

class QueryNode:
    """ A tree representation of a query node. """

    def __init__(self, string, tables, type):
        """"""
        self.string = ''
        self.tables = tables
        self.type = type

        # May be used depending on type
        self.start = len(string)
        self.end = len(string)
        self.table = None
        self.table_operator = TableOperator.NONE
        self.increment = 0

        self.nodes = []

        # Only root automatically populates children
        if self.type == QueryNodeType.ROOT:
            self.populate(string)

    def populate(self, string):
        """"""

        if not string:
            return

        # Discard unwanted data
        string = string.strip()
        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        string = string.strip()

        if self.type == QueryNodeType.TABLE_OPERATOR:
            string = string[self.increment:]

        if self.type == QueryNodeType.TABLE:
            return

        node1 = None
        node2 = self.create(string, self.tables)

        while 1:
            node1 = node2
            if node1.type == QueryNodeType.NONE:
                break
            self.nodes.append(node1)
            if node1.type == QueryNodeType.TABLE:
                node1.end = node1.start + len(node1.table.name)
                break
            if node1.type == QueryNodeType.TABLE_OPERATOR:
                node2 = self.create(string[node1.start + node1.increment:], self.tables)
                node2.start += node1.increment
                node1.end = node2.start
                continue
            if node1.type == QueryNodeType.GROUP:
                node1.end = self.pair(string[node1.start:]) + node1.start + 1
                node2 = self.create(string[node1.end:], self.tables)
                continue

        for node in self.nodes:
            # if not string[node.start:node.end]:
            #     print("start={}, end={}".format(node.start, node.end))
            #     print(string)
            #     print(string[node.start:node.end])
            #     print(node.type)
            #     raise AssertionError
            node.populate(string[node.start:node.end])

    def __lt__(self, other):
        """ Sort by position in string. """
        return self.start < other.start

    @staticmethod
    def pair(string):
        """ Find the index of the matching parenthesis. """
        count = 0
        for i, char in enumerate(string):
            if char == '(':
                count += 1
                continue
            if char == ')':
                count -= 1
                if not count:
                    return i
                if count < 0:
                    break
        raise QueryError('Unmatched Parentheses: {}'.format(string))

    @classmethod
    def create(cls, string, tables):
        """ Create the outmost query from a string. """
        # Starts breaking the recursive loop
        if not string:
            return QueryNode(string, tables, QueryNodeType.NONE)

        table = QueryNode(string, tables, QueryNodeType.TABLE)
        table_operator = QueryNode(string, tables, QueryNodeType.TABLE_OPERATOR)
        group = QueryNode(string, tables, QueryNodeType.GROUP)

        # Find the first table
        for i in tables:
            if not i.name:
                continue
            result = cls.search(string, i.name)
            if result > table.start:
                continue
            table.table = i
            table.start = result

        # Find the first TableOperator
        for i in TableOperator:
            for j in i.strings:
                result = cls.search(string, j)
                if result > table_operator.start:
                    continue
                table_operator.table_operator = i
                table_operator.increment = len(j)
                table_operator.start = result

        # Find the first parenthesis
        group.start = string.find('(')
        if group.start == -1:
            group.start = len(string)

        # Find the first query
        result = sorted([table, table_operator, group])[0]
        return result

    @staticmethod
    def search(string1, string2):
        """ Search for the first occurrence of the modified string2 in string1. """
        # Check if the string is surrounded by spaces, parentheses, or at one of the ends
        pattern = r'(^|\s|\()' + re.escape(string2) + r'($|\s|\))'
        result = re.search(pattern, string1)
        if not result:
            return len(string1)
        # If the found string starts with a character, get the actual index to the string
        return result.start(1) + result.group().find(string2)
