from query_node import QueryNode

class Query:
    ''' A wrapper for a QueryNode. '''

    def __init__(self, string, tables):
        ''''''
        self.root = QueryNode()
        self.root.string = string
        self.root.parse(tables)
        self.root.compute()
