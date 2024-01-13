import re

from query_node import QueryNode

class Query:
    ''' A wrapper for a root QueryNode. '''

    def compute(self, string, tables):
        ''''''
        # Surround table names with parentheses for easier parsing
        for table in tables:
            string = self.parenthesize(string, table.name)

        # Parse and compute the query
        root = QueryNode(string)
        root.parse(tables)
        return root.compute()

    @staticmethod
    def parenthesize(string1, string2):
        ''' Surround string2 occurrences in string1 with parentheses. '''
        pattern1 = re.compile(r'\b' + string2 + r'\b')
        pattern2 = re.compile(r'\([^)]*' + string2 + r'[^)]*\)')
        # Check if surrounded by whitespace and not surrounded by parentheses
        if pattern1.search(string1) and not pattern2.search(string1):
            return pattern1.sub('({})'.format(string2), string1)
        return string1
