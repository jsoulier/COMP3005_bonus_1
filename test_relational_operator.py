import unittest

from relational_operator import RelationalOperator

class TestRelationalOperator(unittest.TestCase):

    def test_within(self):
        self.assertFalse(RelationalOperator.NONE.within(''))
        self.assertFalse(RelationalOperator.NONE.within('='))
        self.assertTrue(RelationalOperator.EQUAL1.within('=='))
        self.assertTrue(RelationalOperator.EQUAL2.within('='))
        self.assertTrue(RelationalOperator.EQUAL2.within('= '))
        self.assertTrue(RelationalOperator.EQUAL2.within(' ='))

    def test_bool(self):
        self.assertTrue(RelationalOperator.EQUAL1)
        self.assertFalse(RelationalOperator.NONE)
