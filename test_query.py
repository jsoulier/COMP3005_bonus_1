import unittest

from query import Query
from query_node_type import QueryNodeType
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
        self.assertEqual(query1.root.nodes[0].type, QueryNodeType.TABLE_OPERATOR)
        self.assertEqual(query1.root.nodes[1].type, QueryNodeType.GROUP)
        self.assertEqual(query1.root.nodes[1].nodes[0].type, QueryNodeType.TABLE)
        self.assertEqual(query2.root.nodes[0].type, QueryNodeType.TABLE_OPERATOR)
        self.assertEqual(query2.root.nodes[1].type, QueryNodeType.GROUP)
        self.assertEqual(query2.root.nodes[1].nodes[0].type, QueryNodeType.TABLE_OPERATOR)
        self.assertEqual(query2.root.nodes[1].nodes[1].type, QueryNodeType.GROUP)
        self.assertEqual(query2.root.nodes[1].nodes[1].nodes[0].type, QueryNodeType.TABLE)
