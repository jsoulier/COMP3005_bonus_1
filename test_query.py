import unittest

from query import Query
from query_error import QueryError
from table import Table
from table_operator import TableOperator

class TestQuery(unittest.TestCase):

    def test_parse1(self):
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
        query = Query()
        query.compute('pi Name (Employees)', [Table(string1), Table(string2)])
        query.compute('pi Name Employees', [Table(string1), Table(string2)])
        query.compute('pi Name (pi Name, Age (Employees))', [Table(string1), Table(string2)])
        query.compute('select ID > 1 (Employees)', [Table(string1), Table(string2)])
        query.compute('(Employees) {} Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        query.compute('   pi Name(   pi Name   ,Age (  Employees  )  )  ', [Table(string1), Table(string2)])

    def test_parse2(self):
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
        query = Query()
        with self.assertRaises(QueryError):
            query.compute('select ID > 1 1 (Employees)', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('pi Name (pi Name, Email Employees)', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('pi Name (Employees)(Employees)', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('pi Name (pi Name, Email (Employees)(Employees))', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('pi Name (pi Name, Email (string))', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} = Name Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name = (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name Name = (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) {} Name Name = Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) Name {} = Name (Department)'.format(TableOperator.NATURAL_JOIN), [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('pi (Employees) Name', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi Name', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees)(Employees) pi Name', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi (Employees) Name', [Table(string1), Table(string2)])
        with self.assertRaises(QueryError):
            query.compute('(Employees) pi Name (Employees)', [Table(string1), Table(string2)])

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
