import re

from query_node import QueryNode
from query_node_type import QueryNodeType

class Query:
    """ A tree representation of a query. """

    def __init__(self, string, tables):
        """"""
        self.root = QueryNode(string, tables, QueryNodeType.ROOT)
