import unittest

from lexer import Lexer
from lexer_error import LexerError
from table_operator import TableOperator

class TestLexer(unittest.TestCase):

    def test_extract1(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
            (pi sid, cname Stud_Course) / (pi cname Course)
        '''
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 2)
        self.assertEqual(len(lexer.queries), 1)
        self.assertEqual(lexer.tables[0].name, 'Stud_Course')
        self.assertEqual(len(lexer.tables[0].columns), 3)
        self.assertEqual(len(lexer.tables[0].rows), 7)
        self.assertEqual(lexer.tables[0].columns, ['sid', 'cname', 'mark'])
        self.assertEqual(lexer.tables[0].rows[0], [1, 'Math', 3])
        self.assertEqual(lexer.tables[0].rows[1], [1, 'Physics', 2])
        self.assertEqual(lexer.tables[0].rows[2], [1, 'Network', 3])
        self.assertEqual(lexer.tables[0].rows[3], [2, 'Math', 3])
        self.assertEqual(lexer.tables[0].rows[4], [2, 'Physics', 2])
        self.assertEqual(lexer.tables[0].rows[5], [2, 'Network', 3])
        self.assertEqual(lexer.tables[0].rows[6], [3, 'Network', 3])
        self.assertEqual(lexer.tables[1].name, 'Course')
        self.assertEqual(len(lexer.tables[1].columns), 2)
        self.assertEqual(len(lexer.tables[1].rows), 3)
        self.assertEqual(lexer.tables[1].columns, ['cname', 'Hours'])
        self.assertEqual(lexer.tables[1].rows[0], ['Math', 3])
        self.assertEqual(lexer.tables[1].rows[1], ['Physics', 2])
        self.assertEqual(lexer.tables[1].rows[2], ['Network', 3])
        self.assertEqual(lexer.queries[0].string, '(pi sid, cname Stud_Course) / (pi cname Course)')

    def test_extract2(self):
        string = ''
        string += '                                                             \n'
        string += '                                                             \n'
        string += 'Stud_Course (id, cname, mark) = {                            \n'
        string += '                                                             \n'
        string += '    1, Math, 3                                               \n'
        string += '    1, Physics, 2                                            \n'
        string += '    1, Network, 3                                            \n'
        string += '    2, Math, 3                                               \n'
        string += '    2, Physics, 2                                            \n'
        string += '                                                             \n'
        string += '    2, Network, 3                                            \n'
        string += '    3, Network, 3                                            \n'
        string += '}                                                            \n'
        string += '                                                             \n'
        string += 'Course (cname, Hours) = {                                    \n'
        string += '                                                             \n'
        string += '    Math, 3                                                  \n'
        string += '    Physics, 2                                               \n'
        string += '                                                             \n'
        string += '    Network, 3                                               \n'
        string += '}                                                            \n'
        string += '(pi id, cname Stud_Course) / (pi cname Course)               \n'
        string += '                                                             \n'
        string += 'Student (id, name, email, Dept) = {                          \n'
        string += '    1, Alex, a@c, Sales                                      \n'
        string += '                                                             \n'
        string += '    2, John, j@c, Finance                                    \n'
        string += '                                                             \n'
        string += '    3, Mo, m@c, HR                                           \n'
        string += '}                                                            \n'
        string += '                                                             \n'
        string += '((pi id, cname Stud_Course) / (pi cname (Course))) {} Student\n'.format(TableOperator.NATURAL_JOIN)
        string += '                                                             \n'
        string += '                                                             \n'
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 3)
        self.assertEqual(len(lexer.queries), 2)
        self.assertEqual(lexer.tables[0].name, 'Stud_Course')
        self.assertEqual(len(lexer.tables[0].columns), 3)
        self.assertEqual(len(lexer.tables[0].rows), 7)
        self.assertEqual(lexer.tables[0].columns, ['id', 'cname', 'mark'])
        self.assertEqual(lexer.tables[0].rows[0], [1, 'Math', 3])
        self.assertEqual(lexer.tables[0].rows[1], [1, 'Physics', 2])
        self.assertEqual(lexer.tables[0].rows[2], [1, 'Network', 3])
        self.assertEqual(lexer.tables[0].rows[3], [2, 'Math', 3])
        self.assertEqual(lexer.tables[0].rows[4], [2, 'Physics', 2])
        self.assertEqual(lexer.tables[0].rows[5], [2, 'Network', 3])
        self.assertEqual(lexer.tables[0].rows[6], [3, 'Network', 3])
        self.assertEqual(lexer.tables[1].name, 'Course')
        self.assertEqual(len(lexer.tables[1].columns), 2)
        self.assertEqual(len(lexer.tables[1].rows), 3)
        self.assertEqual(lexer.tables[1].columns, ['cname', 'Hours'])
        self.assertEqual(lexer.tables[1].rows[0], ['Math', 3])
        self.assertEqual(lexer.tables[1].rows[1], ['Physics', 2])
        self.assertEqual(lexer.tables[1].rows[2], ['Network', 3])
        self.assertEqual(lexer.tables[2].name, 'Student')
        self.assertEqual(len(lexer.tables[2].columns), 4)
        self.assertEqual(len(lexer.tables[2].rows), 3)
        self.assertEqual(lexer.tables[2].rows[0], [1, 'Alex', 'a@c', 'Sales'])
        self.assertEqual(lexer.tables[2].rows[1], [2, 'John', 'j@c', 'Finance'])
        self.assertEqual(lexer.tables[2].rows[2], [3, 'Mo', 'm@c', 'HR'])
        self.assertEqual(lexer.queries[0].string, '(pi id, cname Stud_Course) / (pi cname Course)')
        self.assertEqual(lexer.queries[1].string, '((pi id, cname Stud_Course) / (pi cname (Course))) {} Student'.format(TableOperator.NATURAL_JOIN))

    def test_extract3(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
        '''
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 2)
        self.assertEqual(len(lexer.queries), 0)

    def test_extract4(self):
        string = '''
        '''
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 0)
        self.assertEqual(len(lexer.queries), 0)

    def test_extract5(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Stud_Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
        '''
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 1)
        self.assertEqual(len(lexer.queries), 0)
        self.assertEqual(lexer.tables[0].name, 'Stud_Course')
        self.assertEqual(len(lexer.tables[0].columns), 2)
        self.assertEqual(len(lexer.tables[0].rows), 3)
        self.assertEqual(lexer.tables[0].columns, ['cname', 'Hours'])
        self.assertEqual(lexer.tables[0].rows[0], ['Math', 3])
        self.assertEqual(lexer.tables[0].rows[1], ['Physics', 2])
        self.assertEqual(lexer.tables[0].rows[2], ['Network', 3])

    def test_extract6(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
        '''
        lexer = Lexer()
        with self.assertRaises(LexerError):
            lexer.extract(string)

    def test_extract7(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            (pi sid, cname Stud_Course) / (pi cname Course)
        '''
        lexer = Lexer()
        with self.assertRaises(LexerError):
            lexer.extract(string)

    def test_extract8(self):
        string = '''
            Stud_Course (id, cname, mark) = {
                1, Math
            }
        '''
        lexer = Lexer()
        with self.assertRaises(LexerError):
            lexer.extract(string)

    def test_compute1(self):
        string = '''
            Stud_Course (id, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
            (pi id, cname Stud_Course) / (pi cname Course)
        '''
        lexer = Lexer()
        tables = lexer.compute(string)
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].name, '')
        self.assertEqual(len(tables[0].columns), 1)
        self.assertEqual(len(tables[0].rows), 2)
        self.assertEqual(tables[0].columns, ['id'])
        self.assertEqual(tables[0].rows[0], [1])
        self.assertEqual(tables[0].rows[1], [2])

    def test_compute2(self):
        string = ''
        string += '                                                             \n'
        string += '                                                             \n'
        string += 'Stud_Course (id, cname, mark) = {                            \n'
        string += '                                                             \n'
        string += '    1, Math, 3                                               \n'
        string += '    1, Physics, 2                                            \n'
        string += '    1, Network, 3                                            \n'
        string += '    2, Math, 3                                               \n'
        string += '    2, Physics, 2                                            \n'
        string += '                                                             \n'
        string += '    2, Network, 3                                            \n'
        string += '    3, Network, 3                                            \n'
        string += '}                                                            \n'
        string += '                                                             \n'
        string += 'Course (cname, Hours) = {                                    \n'
        string += '                                                             \n'
        string += '    Math, 3                                                  \n'
        string += '    Physics, 2                                               \n'
        string += '                                                             \n'
        string += '    Network, 3                                               \n'
        string += '}                                                            \n'
        string += '(pi id, cname Stud_Course) / (pi cname Course)               \n'
        string += '                                                             \n'
        string += 'Student (id, name, email, Dept) = {                          \n'
        string += '    1, Alex, a@c, Sales                                      \n'
        string += '                                                             \n'
        string += '    2, John, j@c, Finance                                    \n'
        string += '                                                             \n'
        string += '    3, Mo, m@c, HR                                           \n'
        string += '}                                                            \n'
        string += '                                                             \n'
        string += '((pi id, cname Stud_Course) / (pi cname (Course))) {} Student\n'.format(TableOperator.NATURAL_JOIN)
        string += '                                                             \n'
        string += '                                                             \n'
        lexer = Lexer()
        tables = lexer.compute(string)
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0].name, '')
        self.assertEqual(len(tables[0].columns), 1)
        self.assertEqual(len(tables[0].rows), 2)
        self.assertEqual(tables[0].columns, ['id'])
        self.assertEqual(tables[0].rows[0], [1])
        self.assertEqual(tables[0].rows[1], [2])
        self.assertEqual(tables[1].name, '')
        self.assertEqual(len(tables[1].columns), 4)
        self.assertEqual(len(tables[1].rows), 2)
        self.assertEqual(tables[1].columns, ['id', 'name', 'email', 'Dept'])
        self.assertEqual(tables[1].rows[0], [1, 'Alex', 'a@c', 'Sales'])
        self.assertEqual(tables[1].rows[1], [2, 'John', 'j@c', 'Finance'])

    def test_compute3(self):
        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Stud_Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
            pi cname Stud_Course
        '''
        lexer = Lexer()
        tables = lexer.compute(string)
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].name, '')
        self.assertEqual(len(tables[0].columns), 1)
        self.assertEqual(len(tables[0].rows), 3)
        self.assertEqual(tables[0].columns, ['cname'])
        self.assertEqual(tables[0].rows[0], ['Math'])
        self.assertEqual(tables[0].rows[1], ['Physics'])
        self.assertEqual(tables[0].rows[2], ['Network'])

    def test_compute4(self):
        string = '''
            Stud_Course (id, cname, mark) = {
                1, Math, 3
            }
            (pi id, cname Stud_Course) / (pi cname Course)
        '''
        lexer = Lexer()
        with self.assertRaises(LexerError):
            lexer.compute(string)

    def test_table_start(self):
        self.assertTrue(Lexer.table_start('()={'))
        self.assertTrue(Lexer.table_start('  ( )=  { '))
        self.assertTrue(Lexer.table_start('string(string)={string'))
        self.assertTrue(Lexer.table_start(' string (string) = { string'))
        self.assertFalse(Lexer.table_start('(){'))
        self.assertFalse(Lexer.table_start('(=){'))
        self.assertFalse(Lexer.table_start('({)='))
        self.assertFalse(Lexer.table_start('=({'))

    def test_query(self):
        self.assertTrue(Lexer.query('string', ['string']))
        self.assertTrue(Lexer.query(' string', ['string']))
        self.assertTrue(Lexer.query('string ', ['string']))
        self.assertTrue(Lexer.query('stringstring', ['string']))
        self.assertTrue(Lexer.query('select ID > 2 (string)', ['string']))
        self.assertTrue(Lexer.query(' select ID> 2(string )', ['string']))
        self.assertFalse(Lexer.query('', ['string']))
        self.assertFalse(Lexer.query('select ', ['string']))
        self.assertFalse(Lexer.query(' select ID> 2()', ['string']))
