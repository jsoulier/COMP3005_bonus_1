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
        query1 = Query('pi name (Employees)', [Table(string)])
        query2 = Query('pi name (pi name, email (Employees))', [Table(string)])
        self.assertEqual(query1.root.string, 'pi name')
        self.assertEqual(query1.root.nodes[0].string, 'Employees')
        self.assertEqual(query2.root.string, 'pi name')
        self.assertEqual(query2.root.nodes[0].string, 'pi name, email')
        self.assertEqual(query2.root.nodes[0].nodes[0].string, 'Employees')
