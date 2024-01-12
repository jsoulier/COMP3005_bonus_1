import unittest

from query_error import QueryError
from query_node import QueryNode
from relational_operator import RelationalOperator
from table import Table
from table_operator import TableOperator

class TestQueryNode(unittest.TestCase):

    def test_parse(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root1 = QueryNode('pi name (Employees)')
        root2 = QueryNode('pi name (pi name, email (Employees))')
        root3 = QueryNode('select id > 1 (Employees)')
        root4 = QueryNode('pi name Employees')
        root5 = QueryNode('pi name (pi name, email Employees)')
        root6 = QueryNode('pi name (Employees)(Employees)')
        root7 = QueryNode('pi name (pi name, email (Employees)(Employees))')
        root8 = QueryNode('pi name (pi name, email (string))')
        root1.parse([Table(string)])
        root2.parse([Table(string)])
        root3.parse([Table(string)])
        with self.assertRaises(QueryError):
            root4.parse([Table(string)])
            root5.parse([Table(string)])
            root6.parse([Table(string)])
            root7.parse([Table(string)])
            root8.parse([Table(string)])

    def test_parse_projection(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('pi name (Employees)')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.relational_operator)
        self.assertEqual(root.parameters, ['name'])
        self.assertEqual(len(root.nodes), 1)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

    def test_parse_projection_projection(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('pi name (pi name, email (Employees))')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.relational_operator)
        self.assertEqual(root.parameters, ['name'])
        self.assertEqual(len(root.nodes), 1)
        self.assertFalse(root.nodes[0].table)
        self.assertEqual(root.nodes[0].table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertEqual(root.nodes[0].parameters, ['name', 'email'])
        self.assertEqual(len(root.nodes[0].nodes), 1)
        self.assertTrue(root.nodes[0].nodes[0].table)
        self.assertFalse(root.nodes[0].nodes[0].table_operator)
        self.assertFalse(root.nodes[0].nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes[0].nodes)

    def test_parse_robustness(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('   pi name(   pi name   , email (  Employees  )  )  ')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.PROJECTION)
        self.assertFalse(root.relational_operator)
        self.assertEqual(root.parameters, ['name'])
        self.assertEqual(len(root.nodes), 1)
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

    def test_parse_selection(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('select id > 1 (Employees)')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['id', '1'])
        self.assertEqual(len(root.nodes), 1)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

    def test_parse_cross_join(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Name, Budget) = {
                Finance, 20000
                Sales, 30000
                HR, 25000
            }
        '''
        root = QueryNode('(Employees) {} (Department)'.format(TableOperator.CROSS_JOIN.symbol()))
        root.parse([Table(string1), Table(string2)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.CROSS_JOIN)
        self.assertFalse(root.relational_operator)
        self.assertFalse(root.parameters)
        self.assertEqual(len(root.nodes), 2)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)
        self.assertTrue(root.nodes[1].table)
        self.assertFalse(root.nodes[1].table_operator)
        self.assertFalse(root.nodes[1].relational_operator)
        self.assertFalse(root.nodes[1].parameters)
        self.assertFalse(root.nodes[1].nodes)

    def test_parse_selection_cross_join(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Name, Budget) = {
                Finance, 20000
                Sales, 30000
                HR, 25000
            }
        '''
        root = QueryNode('select id > 1 ((Employees) {} (Department))'.format(TableOperator.CROSS_JOIN.symbol()))
        root.parse([Table(string1), Table(string2)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['id', '1'])
        self.assertEqual(len(root.nodes), 1)
        self.assertFalse(root.nodes[0].table)
        self.assertEqual(root.nodes[0].table_operator, TableOperator.CROSS_JOIN)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertEqual(len(root.nodes[0].nodes), 2)
        self.assertTrue(root.nodes[0].nodes[0].table)
        self.assertFalse(root.nodes[0].nodes[0].table_operator)
        self.assertFalse(root.nodes[0].nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes[0].nodes)
        self.assertTrue(root.nodes[0].nodes[1].table)
        self.assertFalse(root.nodes[0].nodes[1].table_operator)
        self.assertFalse(root.nodes[0].nodes[1].relational_operator)
        self.assertFalse(root.nodes[0].nodes[1].parameters)
        self.assertFalse(root.nodes[0].nodes[1].nodes)

    def test_compute_selection(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('select ID >= 2 (Employees)')
        root.parse([Table(string)])
        table = root.compute()
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')
        self.assertEqual(table.rows[0][0], 2)
        self.assertEqual(table.rows[0][1], 'Alice')
        self.assertEqual(table.rows[0][2], 28)
        self.assertEqual(table.rows[1][0], 3)
        self.assertEqual(table.rows[1][1], 'Bob')
        self.assertEqual(table.rows[1][2], 29)

    def test_compute_projection(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('pi ID, Name (Employees)')
        root.parse([Table(string)])
        table = root.compute()
        self.assertEqual(len(table.columns), 1)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'Age')
        self.assertEqual(table.rows[0][0], 32)
        self.assertEqual(table.rows[1][0], 28)
        self.assertEqual(table.rows[2][0], 29)

    def test_compute_cross_join(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Name, Budget) = {
                Finance, 20000
                Sales, 30000
                HR, 25000
            }
        '''
        root = QueryNode('(Employees) {} (Department)'.format(TableOperator.CROSS_JOIN.symbol()))
        root.parse([Table(string1), Table(string2)])
        table = root.compute()
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 6)
        self.assertEqual(len(table.rows), 9)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Name', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 'Finance', 20000])
        self.assertEqual(table.rows[1], [1, 'John', 32, 'Sales', 'Sales', 30000])
        self.assertEqual(table.rows[2], [1, 'John', 32, 'Sales', 'HR', 25000])
        self.assertEqual(table.rows[3], [2, 'Alice', 28, 'Finance', 'Finance', 20000])
        self.assertEqual(table.rows[4], [2, 'Alice', 28, 'Finance', 'Sales', 30000])
        self.assertEqual(table.rows[5], [2, 'Alice', 28, 'Finance', 'HR', 25000])
        self.assertEqual(table.rows[6], [3, 'Bob', 29, 'HR', 'Finance', 20000])
        self.assertEqual(table.rows[7], [3, 'Bob', 29, 'HR', 'Sales', 30000])
        self.assertEqual(table.rows[8], [3, 'Bob', 29, 'HR', 'HR', 25000])

    def test_search(self):
        self.assertEqual(QueryNode.search(' string ', 'string'), 1)
        self.assertEqual(QueryNode.search('string ', 'string'), 0)
        self.assertEqual(QueryNode.search(' string', 'string'), 1)
        self.assertEqual(QueryNode.search('(string', 'string'), 1)
        self.assertEqual(QueryNode.search(' string2 ', 'string'), 9)
        self.assertEqual(QueryNode.search('string2 ', 'string'), 8)
        self.assertEqual(QueryNode.search(' string2', 'string'), 8)
        self.assertEqual(QueryNode.search('(string2', 'string'), 8)

    def test_pair(self):
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
