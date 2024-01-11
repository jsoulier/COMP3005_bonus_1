import unittest

from table import Table

class TestTable(unittest.TestCase):
    
    def test1(self):
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

    def test2(self):
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
