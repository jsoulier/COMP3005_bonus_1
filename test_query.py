import unittest

from query import Query
from query_error import QueryError
from table import Table
from table_operator import TableOperator

class TestQuery(unittest.TestCase):

    def test_compute1(self):
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
        tables = [Table(string1), Table(string2)]
        query = Query()
        query.compute('pi Name (Employees)', tables)
        query.compute('pi Name Employees', tables)
        query.compute('pi Name (pi Name, Age (Employees))', tables)
        query.compute('select ID > 1 (Employees)', tables)
        query.compute('select ID>1 (Employees)', tables)
        query.compute('(Employees) {} Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query.compute('   pi Name(   pi Name   ,Age (  Employees  )  )  ', tables)
        query.compute('pi Name (pi Name, Email Employees)', tables)

    def test_compute2(self):
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
        tables = [Table(string1), Table(string2)]
        query = Query()
        with self.assertRaises(QueryError):
            query.compute('select ID > 1 1 (Employees)', tables)
        with self.assertRaises(QueryError):
            query.compute('pi Name (Employees)(Employees)', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} (Employees)(Employees)'.format(TableOperator.CROSS_JOIN), tables)
        # with self.assertRaises(QueryError):
        #     query.compute('(Employees)(Employees) {}'.format(TableOperator.CROSS_JOIN), tables)
        # with self.assertRaises(QueryError):
        #     query.compute('{} (Employees)(Employees)'.format(TableOperator.CROSS_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('pi Name (pi Name, Email (Employees)(Employees))', tables)
        with self.assertRaises(QueryError):
            query.compute('pi Name (pi Name, Email (string))', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name = (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name Name = (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) Name {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        with self.assertRaises(QueryError):
            query.compute('pi (Employees) Name', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi Name', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees)(Employees) pi Name', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi (Employees) Name', tables)
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi Name (Employees)', tables)

    def test_compute3(self):
        string1 = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
        '''
        string2 = '''
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
        '''
        tables = [Table(string1), Table(string2)]
        query = Query()
        table = query.compute('(pi sid, cname Stud_Course) / (pi cname Course)', tables)
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 1)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.rows[0], [1])
        self.assertEqual(table.rows[1], [2])

    def test_compute4(self):
        string1 = '''
            Stud_Course (id, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
        '''
        string2 = '''
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
        '''
        string3 = '''
            Student (id, name, email, Dept) = {
                1, Alex, a@c, Sales
                2, John, j@c, Finance
                3, Mo, m@c, HR
            }
        '''
        tables = [Table(string1), Table(string2), Table(string3)]
        query = Query()
        table = query.compute('((pi id, cname Stud_Course) / (pi cname (Course))) {} Student'.format(TableOperator.NATURAL_JOIN), tables)
        self.assertEqual(table.name, '')
        self.assertEqual(len(table.columns), 4)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.rows[0], [1, 'Alex', 'a@c', 'Sales'])
        self.assertEqual(table.rows[1], [2, 'John', 'j@c', 'Finance'])

    def test_parenthesize(self):
        self.assertEqual(Query.parenthesize(' string ', 'string'), ' (string) ')
        self.assertEqual(Query.parenthesize('string ', 'string'), '(string) ')
        self.assertEqual(Query.parenthesize(' string', 'string'), ' (string)')
        self.assertEqual(Query.parenthesize('string', 'string'), '(string)')
        self.assertEqual(Query.parenthesize('(string', 'string'), '((string)')
        self.assertEqual(Query.parenthesize('string)', 'string'), '(string))')
        self.assertEqual(Query.parenthesize('(string)', 'string'), '(string)')
        self.assertEqual(Query.parenthesize('( string )', 'string'), '( string )')
        self.assertEqual(Query.parenthesize(' string string ', 'string'), ' (string) (string) ')
        self.assertEqual(Query.parenthesize(' stringstring ', 'string'), ' stringstring ')
        self.assertEqual(Query.parenthesize('string2string', 'string'), 'string2string')
        self.assertEqual(Query.parenthesize(' string2 string', 'string'), ' string2 (string)')
        self.assertEqual(Query.parenthesize(' string (string)', 'string'), ' (string) (string)')
        self.assertEqual(Query.parenthesize(' string ( string )', 'string'), ' (string) ( string )')
        self.assertEqual(Query.parenthesize(' string (string )', 'string'), ' (string) (string )')
        self.assertEqual(Query.parenthesize(' string ( string)', 'string'), ' (string) ( string)')

    def test_occurrences(self):
        self.assertEqual(Query.occurrences(' string', 'string'), [1])
        self.assertEqual(Query.occurrences('string', 'string'), [0])
        self.assertEqual(Query.occurrences('stringstring', 'string'), [])
        self.assertEqual(Query.occurrences('stringstring string', 'string'), [13])
        self.assertEqual(Query.occurrences('string string', 'string'), [0, 7])
        self.assertEqual(Query.occurrences(' sstring', 'string'), [])
        self.assertEqual(Query.occurrences('', 'string'), [])
        self.assertEqual(Query.occurrences(' strsing', 'string'), [])
        self.assertEqual(Query.occurrences('string', ''), [])
