import unittest

from table_element import TableElement

class TestTableElement(unittest.TestCase):

    def test_convert(self):
        self.assertTrue(isinstance(TableElement.convert('string'), str))
        self.assertTrue(isinstance(TableElement.convert('1'), int))
        self.assertTrue(isinstance(TableElement.convert('1.5'), float))
        self.assertTrue(isinstance(TableElement.convert(1), int))
        self.assertTrue(isinstance(TableElement.convert(1.5), float))

    def test_compare(self):
        self.assertEqual(TableElement('string'), 'string')
        self.assertEqual(TableElement('1'), '1')
        self.assertEqual(TableElement('1'), 1)
        self.assertEqual(TableElement(1), '1')
        self.assertEqual(TableElement(1), 1)
        self.assertEqual(TableElement('1.5'), '1.5')
        self.assertEqual(TableElement(1.5), '1.5')
        self.assertEqual(TableElement('1.5'), 1.5)
        self.assertEqual(TableElement(1.5), 1.5)
        self.assertEqual(TableElement('1.0'), '1')
        self.assertEqual(TableElement('1'), '1.0')
        self.assertEqual(TableElement('1.0'), 1)
        self.assertEqual(TableElement('1'), 1.0)
        self.assertEqual(TableElement(1.0), '1')
        self.assertEqual(TableElement(1), '1.0')
        self.assertEqual(TableElement(1.0), 1)
        self.assertEqual(TableElement(1), 1.0)
        self.assertNotEqual(TableElement('string'), '')
        self.assertEqual([TableElement('1')], [TableElement('1')])
        self.assertEqual([TableElement('1')], [TableElement(1)])
        self.assertEqual([TableElement(1)], [TableElement('1')])
        self.assertEqual([TableElement(1)], [TableElement(1)])
        self.assertEqual([TableElement('string')], [TableElement('string')])
        self.assertEqual([TableElement('string')], ['string'])
