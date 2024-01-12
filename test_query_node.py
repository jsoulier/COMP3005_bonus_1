import unittest

from query_error import QueryError
from query_node import QueryNode
from relational_operator import RelationalOperator
from table import Table
from table_operator import TableOperator

class TestQueryNode(unittest.TestCase):

    def test_parse1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root1 = QueryNode()
        root2 = QueryNode()
        root3 = QueryNode()
        root4 = QueryNode()
        root5 = QueryNode()
        root6 = QueryNode()
        root7 = QueryNode()
        root8 = QueryNode()
        root1.string = 'pi name (Employees)'
        root2.string = 'pi name (pi name, email (Employees))'
        root3.string = 'select id > 1 (Employees)'
        root4.string = 'pi name Employees'
        root5.string = 'pi name (pi name, email Employees)'
        root6.string = 'pi name (Employees)(Employees)'
        root7.string = 'pi name (pi name, email (Employees)(Employees))'
        root8.string = 'pi name (pi name, email (string))'
        root1.parse([Table(string)])
        root2.parse([Table(string)])
        root3.parse([Table(string)])
        with self.assertRaises(QueryError):
            root4.parse([Table(string)])
            root5.parse([Table(string)])
            root6.parse([Table(string)])
            root7.parse([Table(string)])
            root8.parse([Table(string)])

    def test_parse2(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode()
        root.string = 'pi name (Employees)'
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.relational_operator)
        self.assertEqual(root.parameters, ['name'])
        self.assertTrue(root.nodes)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

    def test_parse3(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode()
        root.string = 'pi name (pi name, email (Employees))'
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.relational_operator)
        self.assertEqual(root.parameters, ['name'])
        self.assertTrue(root.nodes)
        self.assertFalse(root.nodes[0].table)
        self.assertEqual(root.nodes[0].table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertEqual(root.nodes[0].parameters, ['name', 'email'])
        self.assertTrue(root.nodes[0].nodes)
        self.assertTrue(root.nodes[0].nodes[0].table)
        self.assertFalse(root.nodes[0].nodes[0].table_operator)
        self.assertFalse(root.nodes[0].nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes[0].nodes)

    def test_parse4(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode()
        root.string = 'select id > 1 (Employees)'
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['id', '1'])
        self.assertTrue(root.nodes)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

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
