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
        root = QueryNode('   pi name(   pi name   ,email (  Employees  )  )  ')
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

    def test_parse2(self):
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

    def test_parse3(self):
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

    def test_parse4(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('select ID > 1 (Employees)')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['ID', '1'])
        self.assertEqual(len(root.nodes), 1)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

    def test_parse5(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        root = QueryNode('select ID>1 (Employees)')
        root.parse([Table(string)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['ID', '1'])
        self.assertEqual(len(root.nodes), 1)
        self.assertTrue(root.nodes[0].table)
        self.assertFalse(root.nodes[0].table_operator)
        self.assertFalse(root.nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes)

    def test_parse6(self):
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
        root = QueryNode('(Employees) {} (Department)'.format(TableOperator.CROSS_JOIN))
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

    def test_parse7(self):
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
        root = QueryNode('select ID > 1 ((Employees) {} (Department))'.format(TableOperator.CROSS_JOIN))
        root.parse([Table(string1), Table(string2)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.SELECTION)
        self.assertEqual(root.relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.parameters, ['ID', '1'])
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

    def test_parse8(self):
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
        root = QueryNode('(select ID > 1 (Employees)) {} Name = Dept (Department)'.format(TableOperator.NATURAL_JOIN))
        root.parse([Table(string1), Table(string2)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.NATURAL_JOIN)
        self.assertEqual(root.relational_operator, RelationalOperator.EQUAL2)
        self.assertEqual(root.parameters, ['Name', 'Dept'])
        self.assertEqual(len(root.nodes), 2)
        self.assertFalse(root.nodes[0].table)
        self.assertEqual(root.nodes[0].table_operator, TableOperator.SELECTION)
        self.assertEqual(root.nodes[0].relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.nodes[0].parameters, ['ID', '1'])
        self.assertEqual(len(root.nodes[0].nodes), 1)
        self.assertTrue(root.nodes[0].nodes[0].table)
        self.assertFalse(root.nodes[0].nodes[0].table_operator)
        self.assertFalse(root.nodes[0].nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes[0].nodes)
        self.assertTrue(root.nodes[1].table)
        self.assertFalse(root.nodes[1].table_operator)
        self.assertFalse(root.nodes[1].relational_operator)
        self.assertFalse(root.nodes[1].parameters)
        self.assertFalse(root.nodes[1].nodes)

    def test_parse9(self):
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
        root = QueryNode('(select ID > 1 (Employees)) {} (Department)'.format(TableOperator.NATURAL_JOIN))
        root.parse([Table(string1), Table(string2)])
        self.assertFalse(root.table)
        self.assertEqual(root.table_operator, TableOperator.NATURAL_JOIN)
        self.assertEqual(root.relational_operator, RelationalOperator.NONE)
        self.assertEqual(root.parameters, [])
        self.assertEqual(len(root.nodes), 2)
        self.assertFalse(root.nodes[0].table)
        self.assertEqual(root.nodes[0].table_operator, TableOperator.SELECTION)
        self.assertEqual(root.nodes[0].relational_operator, RelationalOperator.GREATER)
        self.assertEqual(root.nodes[0].parameters, ['ID', '1'])
        self.assertEqual(len(root.nodes[0].nodes), 1)
        self.assertTrue(root.nodes[0].nodes[0].table)
        self.assertFalse(root.nodes[0].nodes[0].table_operator)
        self.assertFalse(root.nodes[0].nodes[0].relational_operator)
        self.assertFalse(root.nodes[0].nodes[0].parameters)
        self.assertFalse(root.nodes[0].nodes[0].nodes)
        self.assertTrue(root.nodes[1].table)
        self.assertFalse(root.nodes[1].table_operator)
        self.assertFalse(root.nodes[1].relational_operator)
        self.assertFalse(root.nodes[1].parameters)
        self.assertFalse(root.nodes[1].nodes)

    def test_compute1(self):
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

    def test_compute2(self):
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
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name'])
        self.assertEqual(table.rows[0][0], 1)
        self.assertEqual(table.rows[1][0], 2)
        self.assertEqual(table.rows[2][0], 3)
        self.assertEqual(table.rows[0][1], 'John')
        self.assertEqual(table.rows[1][1], 'Alice')
        self.assertEqual(table.rows[2][1], 'Bob')

    def test_compute3(self):
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
        root = QueryNode('(Employees) {} (Department)'.format(TableOperator.CROSS_JOIN))
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

    def test_pair(self):
        self.assertEqual(QueryNode.pair('()'), 1)
        self.assertEqual(QueryNode.pair('(  )'), 3)
        self.assertEqual(QueryNode.pair('(     ()   )'), 11)
        self.assertEqual(QueryNode.pair('(     ()   )  ()'), 11)
        self.assertEqual(QueryNode.pair('pi name (Employees)'), 18)
        self.assertEqual(QueryNode.pair(' pi name   (Employees)   '), 21)
        self.assertEqual(QueryNode.pair(' pi name   ( pi name ( Employees)     )   '), 38)
        with self.assertRaises(QueryError):
            self.assertEqual(QueryNode.pair(''), 0)
        with self.assertRaises(QueryError):
            self.assertEqual(QueryNode.pair(')'), 0)
        with self.assertRaises(QueryError):
            self.assertEqual(QueryNode.pair(')()'), 0)

    def test_extract(self):
        string1 = '( string )'
        string2 = '( string string )'
        string3 = '( string ( string) )'
        string4 = '( string ) string'
        string5 = ' string ( string ) '
        string6 = ' string ( string )string '
        node1 = QueryNode.extract(string1)
        node2 = QueryNode.extract(string2)
        node3 = QueryNode.extract(string3)
        node4 = QueryNode.extract(string4)
        node5 = QueryNode.extract(string5)
        node6 = QueryNode.extract(string6)
        self.assertEqual(node1.string, 'string')
        self.assertEqual(node2.string, 'string string')
        self.assertEqual(node3.string, 'string ( string)')
        self.assertEqual(node4.string, 'string')
        self.assertEqual(node5.string, 'string')
        self.assertEqual(node6.string, 'string')
        self.assertEqual(string1[:node1.start] + string1[node1.end:], '')
        self.assertEqual(string2[:node2.start] + string2[node2.end:], '')
        self.assertEqual(string3[:node3.start] + string3[node3.end:], '')
        self.assertEqual(string4[:node4.start] + string4[node4.end:], ' string')
        self.assertEqual(string5[:node5.start] + string5[node5.end:], ' string  ')
        self.assertEqual(string6[:node6.start] + string6[node6.end:], ' string string ')
