import unittest

from relational_operator import RelationalOperator

class TestRelationalOperator(unittest.TestCase):

    def test_within(self):
        self.assertFalse(RelationalOperator.NONE.within(''))
        self.assertFalse(RelationalOperator.NONE.within('='))
        self.assertTrue(RelationalOperator.EQUAL1.within('=='))
        self.assertFalse(RelationalOperator.EQUAL1.within('='))
        self.assertFalse(RelationalOperator.EQUAL1.within(' ='))
        self.assertFalse(RelationalOperator.EQUAL1.within('= '))
        self.assertTrue(RelationalOperator.EQUAL2.within('='))
        self.assertTrue(RelationalOperator.EQUAL2.within('= '))
        self.assertTrue(RelationalOperator.EQUAL2.within(' ='))

    def test_bool(self):
        self.assertFalse(RelationalOperator.NONE)
        self.assertTrue(RelationalOperator.EQUAL1)
        self.assertTrue(RelationalOperator.NOT_EQUAL)
        self.assertTrue(RelationalOperator.LESS_EQUAL1)
        self.assertTrue(RelationalOperator.LESS_EQUAL2)
        self.assertTrue(RelationalOperator.GREATER_EQUAL1)
        self.assertTrue(RelationalOperator.GREATER_EQUAL2)
        self.assertTrue(RelationalOperator.EQUAL2)
        self.assertTrue(RelationalOperator.LESS)
        self.assertTrue(RelationalOperator.GREATER)
        self.assertTrue(RelationalOperator.LESS_EQUAL)
        self.assertTrue(RelationalOperator.GREATER_EQUAL)
        self.assertTrue(RelationalOperator.EQUAL)
