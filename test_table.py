import unittest

from relational_operator import RelationalOperator
from table import Table
from table_error import TableError

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

    def test_init3(self):
        string = '''
            Employ_ees (@Name_, _Wealth) = {
                Jaan_Soulier, $32000
                Alice, -64000
                Bob, _7200
            }
        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employ_ees')
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], '@Name_')
        self.assertEqual(table.columns[1], '_Wealth')
        self.assertEqual(table.rows[0][0], 'Jaan_Soulier')
        self.assertEqual(table.rows[0][1], '$32000')
        self.assertEqual(table.rows[1][0], 'Alice')
        self.assertEqual(table.rows[1][1], -64000)
        self.assertEqual(table.rows[2][0], 'Bob')
        self.assertEqual(table.rows[2][1], '_7200')

    def test_init5(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, Jaan Soulier, 32
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
                2, Alice, 28
                3, Bob, 29
                4, Mo
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init7(self):
        string = '''
            Employees (ID, Name Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init8(self):
        string = '''
            Employees Employees (ID, Name Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init9(self):
        string = '''
            Employees () = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29  }
        '''
        with self.assertRaises(TableError):
            Table(string)

    def test_init10(self):
        string = '''
            Employees (ID, Name, Age) = {
            }
        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employees')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 0)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')

    def test_init11(self):
        string = '''
            Employees () = {
            }
        '''
        table = Table(string)
        self.assertEqual(table.name, 'Employees')
        self.assertEqual(len(table.columns), 0)
        self.assertEqual(len(table.rows), 0)

    def test_selection1(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.selection(Table(string), 'ID', RelationalOperator.GREATER_EQUAL, 2)
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
        table = Table.selection(Table(string), 'ID', RelationalOperator.EQUAL, 0)
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
        table = Table.projection(Table(string), ['Dept'])
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 0)
        self.assertEqual(len(table.rows), 0)

    def test_projection2(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.projection(Table(string), ['ID', 'Name'])
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.rows[0][0], 1)
        self.assertEqual(table.rows[1][0], 2)
        self.assertEqual(table.rows[2][0], 3)
        self.assertEqual(table.rows[0][1], 'John')
        self.assertEqual(table.rows[1][1], 'Alice')
        self.assertEqual(table.rows[2][1], 'Bob')

    def test_projection3(self):
        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.projection(Table(string), ['ID', 'Name', 'Age'])
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns[0], 'ID')
        self.assertEqual(table.columns[1], 'Name')
        self.assertEqual(table.columns[2], 'Age')
        self.assertEqual(table.rows[0][0], 1)
        self.assertEqual(table.rows[1][0], 2)
        self.assertEqual(table.rows[2][0], 3)
        self.assertEqual(table.rows[0][1], 'John')
        self.assertEqual(table.rows[1][1], 'Alice')
        self.assertEqual(table.rows[2][1], 'Bob')
        self.assertEqual(table.rows[0][2], 32)
        self.assertEqual(table.rows[1][2], 28)
        self.assertEqual(table.rows[2][2], 29)

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

    def test_cross_join2(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Name, Budget) = {
            }
        '''
        table = Table.cross_join(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 6)
        self.assertEqual(len(table.rows), 0)

    def test_cross_join3(self):
        string1 = '''
            Employees () = {
            }
        '''
        string2 = '''
            Department (Name, Budget) = {
            }
        '''
        table = Table.cross_join(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table.rows), 0)

    def test_natural_join1(self):
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
        table = Table.natural_join(Table(string1), Table(string2), 'Dept', RelationalOperator.EQUAL, 'Name')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 30000])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance', 20000])
        self.assertEqual(table.rows[2], [3, 'Bob', 29, 'HR', 25000])

    def test_natural_join2(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Dept, ID) = {
                Finance, 2
                Sales, 1
                HR, 3
            }
        '''
        table = Table.natural_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 4)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales'])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance'])
        self.assertEqual(table.rows[2], [3, 'Bob', 29, 'HR'])

    def test_natural_join3(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (VP, Budget) = {
                Finance, 20000
                Sales, 30000
                HR, 25000
            }
        '''
        table = Table.natural_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 6)
        self.assertEqual(len(table.rows), 0)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'VP', 'Budget'])

    def test_natural_join4(self):
        string1 = '''
            Student (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Takes (ID, Course) = {
                1, Math
                1, Physics
                1, Network
                2, Network
                3, Math
            }
        '''
        table = Table.natural_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 4)
        self.assertEqual(len(table.rows), 5)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Course'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Math'])
        self.assertEqual(table.rows[1], [1, 'John', 32, 'Physics'])
        self.assertEqual(table.rows[2], [1, 'John', 32, 'Network'])
        self.assertEqual(table.rows[3], [2, 'Alice', 28, 'Network'])
        self.assertEqual(table.rows[4], [3, 'Bob', 29, 'Math'])

    def test_left_outer_join(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Dept, Budget) = {
                Finance, 20000
                Sales, 30000
                IT, 25000
            }
        '''
        table = Table.left_outer_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 30000])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance', 20000])
        self.assertEqual(table.rows[2], [3, 'Bob', 29, 'HR', ''])

    def test_right_outer_join(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Dept, Budget) = {
                Finance, 20000
                Sales, 30000
                IT, 25000
            }
        '''
        table = Table.right_outer_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 30000])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance', 20000])
        self.assertEqual(table.rows[2], ['', '', '', 'IT', 25000])

    def test_full_outer_join1(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Department (Dept, Budget) = {
                Finance, 20000
                Sales, 30000
                IT, 25000
            }
        '''
        table = Table.full_outer_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 4)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 30000])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance', 20000])
        self.assertEqual(table.rows[2], [3, 'Bob', 29, 'HR', ''])
        self.assertEqual(table.rows[3], ['', '', '', 'IT', 25000])

    def test_full_outer_join2(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                1, John, 32, Sales
                2, Alice, 28, Finance
                3, Bob, 29, HR
                4, Joe, 29, Marketing
                5, Billy, 29, Testing
                6, Max, 29, Research
            }
        '''
        string2 = '''
            Department (Dept, Budget) = {
                Finance, 20000
                Sales, 30000
                IT, 25000
                Support, 45000
            }
        '''
        table = Table.full_outer_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 8)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [1, 'John', 32, 'Sales', 30000])
        self.assertEqual(table.rows[1], [2, 'Alice', 28, 'Finance', 20000])
        self.assertEqual(table.rows[2], [3, 'Bob', 29, 'HR', ''])
        self.assertEqual(table.rows[3], [4, 'Joe', 29, 'Marketing', ''])
        self.assertEqual(table.rows[4], [5, 'Billy', 29, 'Testing', ''])
        self.assertEqual(table.rows[5], [6, 'Max', 29, 'Research', ''])
        self.assertEqual(table.rows[6], ['', '', '', 'IT', 25000])
        self.assertEqual(table.rows[7], ['', '', '', 'Support', 45000])

    def test_full_outer_join3(self):
        string1 = '''
            Employees (ID, Name, Age, Dept) = {
                3, Bob, 29, HR
                4, Joe, 29, Marketing
                5, Billy, 29, Testing
                6, Max, 29, Research
            }
        '''
        string2 = '''
            Department (Dept, Budget) = {
                IT, 25000
                Support, 45000
            }
        '''
        table = Table.full_outer_join(Table(string1), Table(string2), '', RelationalOperator.NONE, '')
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 5)
        self.assertEqual(len(table.rows), 6)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age', 'Dept', 'Budget'])
        self.assertEqual(table.rows[0], [3, 'Bob', 29, 'HR', ''])
        self.assertEqual(table.rows[1], [4, 'Joe', 29, 'Marketing', ''])
        self.assertEqual(table.rows[2], [5, 'Billy', 29, 'Testing', ''])
        self.assertEqual(table.rows[3], [6, 'Max', 29, 'Research', ''])
        self.assertEqual(table.rows[4], ['', '', '', 'IT', 25000])
        self.assertEqual(table.rows[5], ['', '', '', 'Support', 45000])

    def test_union1(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                4, Max, 33
                5, Mo, 27
            }
        '''
        table = Table.union(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 5)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])
        self.assertEqual(table.rows[3], [4, 'Max', 33])
        self.assertEqual(table.rows[4], [5, 'Mo', 27])

    def test_union2(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name) = {
                1, John
                2, Alice
                3, Bob
            }
        '''
        with self.assertRaises(TableError):
            Table.union(Table(string1), Table(string2))

    def test_union3(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.union(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_union4(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
            }
        '''
        table = Table.union(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_intersection1(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                4, Max, 33
                5, Mo, 27
            }
        '''
        table = Table.intersection(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])

    def test_intersection2(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                4, Alex, 31
                5, Max, 33
                6, Mo, 27
            }
        '''
        table = Table.intersection(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 0)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])

    def test_intersection3(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.union(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_minus1(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                4, Max, 33
                5, Mo, 27
            }
        '''
        table = Table.minus(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [2, 'Alice', 28])
        self.assertEqual(table.rows[1], [3, 'Bob', 29])

    def test_minus2(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                4, Alex, 31
                4, Max, 33
                5, Mo, 27
            }
        '''
        table = Table.minus(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_minus3(self):
        string1 = '''
            Employees1 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        string2 = '''
            Employees2 (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table.minus(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 0)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])

    def test_division1(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept) = {
                1, John, 32, Finance
                1, John, 32, Sales
                1, John, 32, HR
                2, Alice, 28, Finance
                2, Alice, 28, Sales
                2, Alice, 28, HR
                3, Bob, 29, Finance
                3, Bob, 29, Sales
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Employees2 (Dept) = {
                Finance
                Sales
                HR
            }
        '''
        table = Table.division(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_division2(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept, City) = {
                1, John, 32, Finance, Ottawa
                1, John, 32, Sales, Toronto
                1, John, 32, HR, Vancouver
                2, Alice, 28, Finance, Ottawa
                2, Alice, 28, Sales, Toronto
                2, Alice, 28, HR, Vancouver
                3, Bob, 29, Finance, Ottawa
                3, Bob, 29, Sales, Toronto
                3, Bob, 29, HR, Vancouver
            }
        '''
        string2 = '''
            Employees2 (Dept, City) = {
                Finance, Ottawa
                Sales, Toronto
                HR, Vancouver
            }
        '''
        table = Table.division(Table(string1), Table(string2))
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 3)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])
        self.assertEqual(table.rows[2], [3, 'Bob', 29])

    def test_division3(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept) = {
                1, John, 32, Finance
                1, John, 32, Sales
                1, John, 32, HR
                2, Alice, 28, Finance
                2, Alice, 28, Sales
                2, Alice, 28, HR
                3, Bob, 29, Finance
            }
        '''
        string2 = '''
            Employees1 (Dept) = {
                Finance
                Sales
                HR
            }
        '''
        table = Table.division(Table(string1), Table(string2))
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.columns, ['ID', 'Name', 'Age'])
        self.assertEqual(table.rows[0], [1, 'John', 32])
        self.assertEqual(table.rows[1], [2, 'Alice', 28])

    def test_division4(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept, City) = {
                1, John, 32, Finance, Ottawa
                1, John, 32, Sales, Toronto
                1, John, 32, HR, Vancouver
                2, Alice, 28, Finance, Ottawa
                2, Alice, 28, Sales, Toronto
                2, Alice, 28, HR, Vancouver
                3, Bob, 29, Finance, Ottawa
                3, Bob, 29, Sales, Toronto
                3, Bob, 29, HR, Vancouver
            }
        '''
        string2 = '''
            Employees1 (Dept, Not_City) = {
                Finance, Ottawa
                Sales, Toronto
                HR, Vancouver
            }
        '''
        with self.assertRaises(TableError):
            Table.division(Table(string1), Table(string2))

    def test_division5(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept) = {
                1, John, 32, Finance
                1, John, 32, Sales
                1, John, 32, HR
                2, Alice, 28, Finance
                2, Alice, 28, Sales
                2, Alice, 28, HR
                3, Bob, 29, Finance
                3, Bob, 29, Sales
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Employees2 (Dept) = {
                Finance
                Sales
                IT
            }
        '''
        with self.assertRaises(TableError):
            Table.division(Table(string1), Table(string2))

    def test_division6(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept) = {
                1, John, 32, Finance
                2, Alice, 28, Sales
                3, Bob, 29, HR
                1, John, 32, Finance
                2, Alice, 28, Sales
                3, Bob, 29, HR
                1, John, 32, Finance
                2, Alice, 28, Sales
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Employees2 (Dept) = {
                Finance
                Sales
                HR
            }
        '''
        with self.assertRaises(TableError):
            Table.division(Table(string1), Table(string2))

    def test_division7(self):
        string1 = '''
            Employees1 (ID, Name, Age, Dept) = {
                1, John, 32, Finance
                1, John, 32, Finance
                1, John, 32, Finance
                2, Alice, 28, Sales
                2, Alice, 28, Sales
                2, Alice, 28, Sales
                3, Bob, 29, HR
                3, Bob, 29, HR
                3, Bob, 29, HR
            }
        '''
        string2 = '''
            Employees2 (Dept) = {
                Finance
                Sales
                HR
            }
        '''
        with self.assertRaises(TableError):
            Table.division(Table(string1), Table(string2))
