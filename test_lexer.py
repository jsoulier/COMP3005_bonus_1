import unittest

from lexer_error import LexerError
from lexer import Lexer

class TestLexer(unittest.TestCase):

    def test_is_table(self):
        self.assertTrue(Lexer.is_table('=(){'))
        self.assertTrue(Lexer.is_table(' = ( )  { '))
        self.assertTrue(Lexer.is_table('string=(string){string'))
        self.assertTrue(Lexer.is_table(' string = (string) { string'))
        self.assertFalse(Lexer.is_table('(){'))
        self.assertFalse(Lexer.is_table('(=){'))
        self.assertFalse(Lexer.is_table('({)='))
        self.assertFalse(Lexer.is_table('=({'))

    def test_is_query(self):
        self.assertTrue(Lexer.is_query('string', ['string']))
        self.assertTrue(Lexer.is_query(' string', ['string']))
        self.assertTrue(Lexer.is_query('string ', ['string']))
        self.assertTrue(Lexer.is_query('stringstring', ['string']))
        self.assertTrue(Lexer.is_query('select ID > 2 (string)', ['string']))
        self.assertTrue(Lexer.is_query(' select ID> 2(string )', ['string']))
        self.assertFalse(Lexer.is_query('', ['string']))
        self.assertFalse(Lexer.is_query('select ', ['string']))
        self.assertFalse(Lexer.is_query(' select ID> 2()', ['string']))
