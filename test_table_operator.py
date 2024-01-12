import unittest

from table_operator import TableOperator

class TestTableOperator(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(TableOperator.SELECTION, 'select')
        self.assertEqual(TableOperator.PROJECTION, 'pi')
        self.assertNotEqual(TableOperator.SELECTION, 'select2')
        self.assertNotEqual(TableOperator.PROJECTION, '2pi')
        self.assertEqual(TableOperator.SELECTION, TableOperator.SELECTION)
        self.assertNotEqual(TableOperator.SELECTION, TableOperator.PROJECTION)
        self.assertNotEqual(TableOperator.SELECTION, TableOperator.NONE)

    def test_bool(self):
        self.assertTrue(TableOperator.SELECTION)
        self.assertFalse(TableOperator.NONE)
