import re

from query_error import QueryError
from table_operator import TableOperator

class QueryNode:
    ''' A tree representation of a query. '''

    def __init__(self):
        ''''''
        self.string = ''

        # The computed table
        self.table = None

        # The range to prune from the parent
        self.start = 0
        self.end = 0

        # The child nodes
        self.nodes = []

    def parse(self, tables):
        ''' Parse string to create child nodes. '''
        self.string = self.string.strip()

        # Check if node is a known table
        for table in tables:
            if self.string != table.name:
                continue
            self.table = table
            return

        # Create child nodes
        for i in range(2):
            node = self.extract(self.string)
            if not node:
                break
            self.string = self.string[:node.start] + self.string[node.end:]
            self.string = self.string.strip()
            self.nodes.append(node)

        if not self.nodes or len(self.nodes) > 2:
            raise QueryError('Bad Query: {}'.format(self.string))

        # Parse child nodes
        for node in self.nodes:
            node.parse(tables)

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
