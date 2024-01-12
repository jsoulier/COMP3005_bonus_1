import re

from query_error import QueryError
from table_operator import TableOperator

class QueryNode:
    ''' A tree representation of a query node. '''

    def __init__(self):
        ''''''
        self.string = ''
        self.tables = []

        # The computed table
        self.table = None

        # The range to prune from the parent
        self.start = 0
        self.end = 0

        # The child nodes
        self.nodes = []

    def parse(self):
        ''''''
        self.string = self.string.strip()

        # Check if node is a known table
        for table in self.tables:
            if self.string != table.name:
                continue
            self.table = table
            return

        # We should have at least one node
        node1 = self.extract(self.string)
        if not node1:
            raise QueryError('Bad Query: {}'.format(node1))
        self.string = self.string[:node1.start] + self.string[node1.end:]
        self.nodes.append(node1)

        # Check for a second node
        node2 = self.extract(self.string)
        if node2:
            self.string = self.string[:node2.start] + self.string[node2.end:]
            self.nodes.append(node2)

        self.string = self.string.strip()

        # Deduce table operator here

        # Parse child nodes
        for node in self.nodes:
            node.tables = self.tables
            node.parse()

    @classmethod
    def extract(cls, string):
        ''' Extract a node from a string. '''
        node = QueryNode()
        node.start = string.find('(')
        if node.start == -1:
            return None
        node.end = cls.pair(string) + 1
        # Create a substring from the parentheses
        node.string = string[node.start + 1:node.end - 1]
        node.string = node.string.strip()
        return node

    @staticmethod
    def pair(string):
        ''' Find the index of the parenthesis matching the first one. '''
        count = 0
        for i, char in enumerate(string):
            if char == '(':
                count += 1
                continue
            if char != ')':
                continue
            count -= 1
            if not count:
                return i
            # If there is a closing parenthesis before an opening one
            if count < 0:
                break
        raise QueryError('Unmatched Parentheses: {}'.format(string))

    @staticmethod
    def search(string1, string2):
        ''' Search for the first occurrence of string2 in string1. '''
        # Check if the string is surrounded by spaces, parentheses, or boundaries
        pattern = r'(^|\s|\()' + re.escape(string2) + r'($|\s|\))'
        result = re.search(pattern, string1)
        if not result:
            return len(string1)
        # Get the position of the string, not the position of the match
        return result.start(1) + result.group().find(string2)
