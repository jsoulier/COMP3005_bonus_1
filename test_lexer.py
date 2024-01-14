import unittest

from lexer_error import LexerError
from lexer import Lexer

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
        string = '''
        '''
        lexer = Lexer()
        lexer.extract(string)
        self.assertEqual(len(lexer.tables), 0)
        self.assertEqual(len(lexer.queries), 0)

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
        '''
        lexer = Lexer()
        with self.assertRaises(LexerError):
            lexer.extract(string)

    def test_extract4(self):
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

    def test_compute1(self):
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
        tables = lexer.compute(string)
        self.assertEqual(tables[0].name, '')
        self.assertEqual(len(tables[0].columns), 1)
        self.assertEqual(len(tables[0].rows), 2)
        self.assertEqual(tables[0].rows[0], [1])
        self.assertEqual(tables[0].rows[1], [2])

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
