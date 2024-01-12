import unittest

from query import Query
from table import Table

class TestQuery(unittest.TestCase):

    def test_init1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        query = Query('select ID>1(Employees)', [Table(string)])
