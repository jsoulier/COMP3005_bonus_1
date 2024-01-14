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
        query1 = Query('pi Name (Employees)', tables)
        query2 = Query('pi Name Employees', tables)
        query3 = Query('pi Name (pi Name, Age (Employees))', tables)
        query4 = Query('select ID > 1 (Employees)', tables)
        query5 = Query('select ID>1 (Employees)', tables)
        query6 = Query('(Employees) {} Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query7 = Query('   pi Name(   pi Name   ,Age (  Employees  )  )  ', tables)
        query8 = Query('pi Name (pi Name, Email Employees)', tables)
        query1.compute()
        query2.compute()
        query3.compute()
        query4.compute()
        query5.compute()
        query6.compute()
        query7.compute()
        query8.compute()

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
        query00 = Query('select ID > 1 1 (Employees)', tables)
        query01 = Query('(Employees) select ID > 1', tables)
        query02 = Query('select ID > = 1 (Employees)', tables)
        query03 = Query('pi Name (Employees)(Employees)', tables)
        query04 = Query('(Employees) {} (Employees)(Employees)'.format(TableOperator.CROSS_JOIN), tables)
        query05 = Query('(Employees)(Employees) {}'.format(TableOperator.CROSS_JOIN), tables)
        query06 = Query('{} (Employees)(Employees)'.format(TableOperator.CROSS_JOIN), tables)
        query07 = Query('{} (Employees) {} (Employees)'.format(TableOperator.CROSS_JOIN, TableOperator.CROSS_JOIN), tables)
        query08 = Query('(Employees) {} (Employees) {}'.format(TableOperator.CROSS_JOIN, TableOperator.CROSS_JOIN), tables)
        query09 = Query('pi Name (pi Name, Email (Employees)(Employees))', tables)
        query10 = Query('pi Name (pi Name, Email (string))', tables)
        query11 = Query('(Employees) {} Name = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query12 = Query('(Employees) {} = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query13 = Query('(Employees) {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query14 = Query('(Employees) {} Name = (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query15 = Query('(Employees) {} Name Name = (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query16 = Query('(Employees) {} Name Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query17 = Query('(Employees) Name {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), tables)
        query18 = Query('pi (Employees) Name', tables)
        query19 = Query('(Employees) pi Name', tables)
        query20 = Query('(Employees)(Employees) pi Name', tables)
        query21 = Query('(Employees) pi (Employees) Name', tables)
        query22 = Query('(Employees) pi Name (Employees)', tables)
        with self.assertRaises(QueryError):
            query00.compute()
        with self.assertRaises(QueryError):
            query01.compute()
        with self.assertRaises(QueryError):
            query02.compute()
        with self.assertRaises(QueryError):
            query03.compute()
        with self.assertRaises(QueryError):
            query04.compute()
        with self.assertRaises(QueryError):
            query05.compute()
        with self.assertRaises(QueryError):
            query06.compute()
        with self.assertRaises(QueryError):
            query07.compute()
        with self.assertRaises(QueryError):
            query08.compute()
        with self.assertRaises(QueryError):
            query09.compute()
        with self.assertRaises(QueryError):
            query10.compute()
        with self.assertRaises(QueryError):
            query11.compute()
        with self.assertRaises(QueryError):
            query12.compute()
        with self.assertRaises(QueryError):
            query13.compute()
        with self.assertRaises(QueryError):
            query14.compute()
        with self.assertRaises(QueryError):
            query15.compute()
        with self.assertRaises(QueryError):
            query16.compute()
        with self.assertRaises(QueryError):
            query17.compute()
        with self.assertRaises(QueryError):
            query18.compute()
        with self.assertRaises(QueryError):
            query19.compute()
        with self.assertRaises(QueryError):
            query20.compute()
        with self.assertRaises(QueryError):
            query21.compute()
        with self.assertRaises(QueryError):
            query22.compute()

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
        query = Query('(pi sid, cname Stud_Course) / (pi cname Course)', tables)
        table = query.compute()
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
        query = Query('((pi id, cname Stud_Course) / (pi cname (Course))) {} Student'.format(TableOperator.NATURAL_JOIN), tables)
        table = query.compute()
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
