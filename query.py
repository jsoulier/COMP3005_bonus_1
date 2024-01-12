from query_node import QueryNode

class Query:
    ''' A wrapper for a root QueryNode. '''

    def __init__(self):
        ''''''

    def compute(self, string, tables):
        ''' Compute the result of the query. '''
        root = QueryNode(string)
        # Create binary tree-like structure of nodes
        root.parse(tables)
        # Compute the table
        return root.compute()
