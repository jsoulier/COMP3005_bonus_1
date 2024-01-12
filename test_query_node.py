import unittest

from query_error import QueryError
from query_node import QueryNode

class TestQueryNode(unittest.TestCase):

    def test_search1(self):
        self.assertTrue(QueryNode.search(' string ', 'string'))
        self.assertTrue(QueryNode.search('string ', 'string'))
        self.assertTrue(QueryNode.search(' string', 'string'))
        self.assertTrue(QueryNode.search('(string', 'string'))
        self.assertFalse(QueryNode.search(' string2 ', 'string'))
        self.assertFalse(QueryNode.search('string2 ', 'string'))
        self.assertFalse(QueryNode.search(' string2', 'string'))
        self.assertFalse(QueryNode.search('(string2', 'string'))

    def test_pair1(self):
        self.assertEqual(QueryNode.pair(')'), 0)
        self.assertEqual(QueryNode.pair('  )'), 2)
        self.assertEqual(QueryNode.pair('     ()   )'), 10)
        self.assertEqual(QueryNode.pair('     ()   )  ()'), 10)
        with self.assertRaises(QueryError):
            self.assertEqual(QueryNode.pair(''), 0)
            self.assertEqual(QueryNode.pair('('), 0)
            self.assertEqual(QueryNode.pair('()()'), 0)

