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
        self.assertFalse(TableOperator.NONE)
        self.assertTrue(TableOperator.SELECTION)
        self.assertTrue(TableOperator.PROJECTION)
        self.assertTrue(TableOperator.CROSS_JOIN)
        self.assertTrue(TableOperator.NATURAL_JOIN)
        self.assertTrue(TableOperator.LEFT_OUTER_JOIN)
        self.assertTrue(TableOperator.RIGHT_OUTER_JOIN)
        self.assertTrue(TableOperator.FULL_OUTER_JOIN)
        self.assertTrue(TableOperator.UNION)
        self.assertTrue(TableOperator.INTERSECTION)
        self.assertTrue(TableOperator.MINUS)
        self.assertTrue(TableOperator.DIVISION)

    def test_left_outer_join(self):
        self.assertFalse(TableOperator.NATURAL_JOIN.left_outer_join())
        self.assertTrue(TableOperator.LEFT_OUTER_JOIN.left_outer_join())
        self.assertFalse(TableOperator.RIGHT_OUTER_JOIN.left_outer_join())
        self.assertTrue(TableOperator.FULL_OUTER_JOIN.left_outer_join())

    def test_right_outer_join(self):
        self.assertFalse(TableOperator.NATURAL_JOIN.right_outer_join())
        self.assertFalse(TableOperator.LEFT_OUTER_JOIN.right_outer_join())
        self.assertTrue(TableOperator.RIGHT_OUTER_JOIN.right_outer_join())
        self.assertTrue(TableOperator.FULL_OUTER_JOIN.right_outer_join())

    def test_parametrize(self):
        self.assertTrue(TableOperator.NONE.parametrize(0))
        self.assertFalse(TableOperator.NONE.parametrize(1))
        self.assertFalse(TableOperator.SELECTION.parametrize(0))
        self.assertFalse(TableOperator.SELECTION.parametrize(0))
        self.assertTrue(TableOperator.SELECTION.parametrize(2))
        self.assertFalse(TableOperator.PROJECTION.parametrize(0))
        self.assertTrue(TableOperator.PROJECTION.parametrize(1))
        self.assertTrue(TableOperator.PROJECTION.parametrize(2))
        self.assertTrue(TableOperator.CROSS_JOIN.parametrize(0))
        self.assertFalse(TableOperator.CROSS_JOIN.parametrize(1))
        self.assertFalse(TableOperator.CROSS_JOIN.parametrize(2))
        self.assertTrue(TableOperator.NATURAL_JOIN.parametrize(0))
        self.assertFalse(TableOperator.NATURAL_JOIN.parametrize(1))
        self.assertTrue(TableOperator.NATURAL_JOIN.parametrize(2))
        self.assertTrue(TableOperator.LEFT_OUTER_JOIN.parametrize(0))
        self.assertFalse(TableOperator.LEFT_OUTER_JOIN.parametrize(1))
        self.assertTrue(TableOperator.LEFT_OUTER_JOIN.parametrize(2))
        self.assertTrue(TableOperator.RIGHT_OUTER_JOIN.parametrize(0))
        self.assertFalse(TableOperator.RIGHT_OUTER_JOIN.parametrize(1))
        self.assertTrue(TableOperator.RIGHT_OUTER_JOIN.parametrize(2))
        self.assertTrue(TableOperator.FULL_OUTER_JOIN.parametrize(0))
        self.assertFalse(TableOperator.FULL_OUTER_JOIN.parametrize(1))
        self.assertTrue(TableOperator.FULL_OUTER_JOIN.parametrize(2))
        self.assertTrue(TableOperator.UNION.parametrize(0))
        self.assertFalse(TableOperator.UNION.parametrize(1))
        self.assertFalse(TableOperator.UNION.parametrize(2))
        self.assertTrue(TableOperator.INTERSECTION.parametrize(0))
        self.assertFalse(TableOperator.INTERSECTION.parametrize(1))
        self.assertFalse(TableOperator.INTERSECTION.parametrize(2))
        self.assertTrue(TableOperator.MINUS.parametrize(0))
        self.assertFalse(TableOperator.MINUS.parametrize(1))
        self.assertFalse(TableOperator.MINUS.parametrize(2))
        self.assertTrue(TableOperator.DIVISION.parametrize(0))
        self.assertFalse(TableOperator.DIVISION.parametrize(1))
        self.assertFalse(TableOperator.DIVISION.parametrize(2))
