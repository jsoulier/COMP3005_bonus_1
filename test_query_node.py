import unittest

from query_error import QueryError
from query_node import QueryNode

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

    def test_extract(self):
        node1 = QueryNode.extract('( string )')
        node2 = QueryNode.extract('( string string )')
        node3 = QueryNode.extract('( string ( string) )')
        node4 = QueryNode.extract('( string ) string')
        node5 = QueryNode.extract(' string ( string ) ')
        node6 = QueryNode.extract(' string ( string ) string ')
        self.assertEqual(node1.string, 'string')
        self.assertEqual(node2.string, 'string string')
        self.assertEqual(node3.string, 'string ( string)')
        self.assertEqual(node4.string, 'string')
        self.assertEqual(node5.string, 'string')
        self.assertEqual(node6.string, 'string')
