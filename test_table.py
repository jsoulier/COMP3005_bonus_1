import unittest
import operator

from table_error import TableError
from table import Table

class TestTable(unittest.TestCase):

    def test_init1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employees')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')
        self.assertEqual(table.rows[0][0], 1)
        self.assertEqual(table.rows[0][1], 'John')
        self.assertEqual(table.rows[0][2], 32)
        self.assertEqual(table.rows[1][0], 2)
        self.assertEqual(table.rows[1][1], 'Alice')
        self.assertEqual(table.rows[1][2], 28)
        self.assertEqual(table.rows[2][0], 3)
        self.assertEqual(table.rows[2][1], 'Bob')
        self.assertEqual(table.rows[2][2], 29)

    def test_init2(self):
        string = '''
            Employees (Name, Wealth) = {
                John, 32000
                Alice, -64000
                Bob, 7200
            }
        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employees')
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'Name')
        self.assertEqual(table.columns[1], 'Wealth')
        self.assertEqual(table.rows[0][0], 'John')
        self.assertEqual(table.rows[0][1], 32000)
        self.assertEqual(table.rows[1][0], 'Alice')
        self.assertEqual(table.rows[1][1], -64000)
        self.assertEqual(table.rows[2][0], 'Bob')
        self.assertEqual(table.rows[2][1], 7200)

    def test_init3(self):
        string = '''
          Employees (   ID,Name, Age  ) =    {   

             1, John,    32
                  2,        Alice,      28

                3,   Bob, 29   


            }

        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employees')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')
        self.assertEqual(table.rows[0][0], 1)
        self.assertEqual(table.rows[0][1], 'John')
        self.assertEqual(table.rows[0][2], 32)
        self.assertEqual(table.rows[1][0], 2)
        self.assertEqual(table.rows[1][1], 'Alice')
        self.assertEqual(table.rows[1][2], 28)
        self.assertEqual(table.rows[2][0], 3)
        self.assertEqual(table.rows[2][1], 'Bob')
        self.assertEqual(table.rows[2][2], 29)

    def test_init4(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, Jaan_Soulier, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        Table(string)

    def test_init5(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32;
                2, Alice, 28
                3, Bob, 29
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init6(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, $28
                3, Bob, 29
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init7(self):
        string = '''
            Employees (ID, &Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_selection1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.selection(Table(string), 'ID', operator.ge, 2)
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

    def test_selection2(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.selection(Table(string), 'ID', operator.eq, 0)
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 0)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')

    def test_projection1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.projection(Table(string), ['ID', 'Name'])
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 1)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'Age')
        self.assertEqual(table.rows[0][0], 32)
        self.assertEqual(table.rows[1][0], 28)
        self.assertEqual(table.rows[2][0], 29)

    def test_projection2(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.projection(Table(string), ['ID', 'Name', 'Age'])
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 0)
        self.assertEqual(len(table.rows), 0)

    def test_cross_join1(self):
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
        table = Table.cross_join(Table(string1), Table(string2))
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
