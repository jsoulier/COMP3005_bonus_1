import unittest

from query import Query
from table import Table
from table_operator import TableOperator

class TestQuery(unittest.TestCase):

    def test_init1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        query = Query('pi name (Employee)', [Table(string)])
        # self.assertEqual(query.table_operator, TableOperator.PROJECTION)



        # query = Query('pi name (pi name, email (Employees))', [Table(string)])
