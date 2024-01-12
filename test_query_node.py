import unittest

from query_error import QueryError
from query_node import QueryNode
from query_node_type import QueryNodeType
from table import Table

class TestQueryNode(unittest.TestCase):

    def test_search1(self):
        self.assertEqual(QueryNode.search(' string ', 'string'), 1)
        self.assertEqual(QueryNode.search('string ', 'string'), 0)
        self.assertEqual(QueryNode.search(' string', 'string'), 1)
        self.assertEqual(QueryNode.search('(string', 'string'), 1)
        self.assertEqual(QueryNode.search(' string2 ', 'string'), 9)
        self.assertEqual(QueryNode.search('string2 ', 'string'), 8)
        self.assertEqual(QueryNode.search(' string2', 'string'), 8)
        self.assertEqual(QueryNode.search('(string2', 'string'), 8)

    def test_create1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        self.assertEqual(QueryNode.create('Employees', [Table(string)]).type, QueryNodeType.TABLE)
        self.assertEqual(QueryNode.create('pi name (Employees)', [Table(string)]).type, QueryNodeType.TABLE_OPERATOR)
        self.assertEqual(QueryNode.create('(Employees)', [Table(string)]).type, QueryNodeType.GROUP)

    def test_pair1(self):
        self.assertEqual(QueryNode.pair('()'), 1)
        self.assertEqual(QueryNode.pair('(  )'), 3)
        self.assertEqual(QueryNode.pair('(     ()   )'), 11)
        self.assertEqual(QueryNode.pair('(     ()   )  ()'), 11)
        with self.assertRaises(QueryError):
            self.assertEqual(QueryNode.pair(''), 0)
            self.assertEqual(QueryNode.pair(')'), 0)
            self.assertEqual(QueryNode.pair(')()'), 0)
        self.assertEqual(QueryNode.pair('pi name (Employees)'), 18)
