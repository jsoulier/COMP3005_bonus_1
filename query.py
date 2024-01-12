import re

from error import QueryError
from misc import Misc

class Query:
    """ A tree representation of a query. """

    def __init__(self, string, tables):
        """"""
        pass

    @staticmethod
    def search(word):
        """"""
        pattern = r'(^|\s|\))' + re.escape(word) + r'($|\s|\()'
