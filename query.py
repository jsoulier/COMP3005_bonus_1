from query_node import QueryNode

class Query:
    ''' A wrapper for a root QueryNode. '''

    def compute(self, string, tables):
        ''' Compute the result of the query. '''
        root = QueryNode(string)
        root.parse(tables)
        return root.compute()
