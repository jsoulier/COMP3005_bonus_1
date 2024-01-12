import unittest

from table_element import TableElement

class TestTableElement(unittest.TestCase):

    def test1(self):
        self.assertEqual(TableElement("string"), "string")
        self.assertEqual(TableElement("1"), "1")
        self.assertEqual(TableElement("1"), 1)
        self.assertEqual(TableElement(1), "1")
        self.assertEqual(TableElement(1), 1)
        self.assertEqual(TableElement("1.5"), "1.5")
        self.assertEqual(TableElement(1.5), "1.5")
        self.assertEqual(TableElement("1.5"), 1.5)
        self.assertEqual(TableElement(1.5), 1.5)
        self.assertEqual(TableElement("1.0"), "1")
        self.assertEqual(TableElement("1"), "1.0")
        self.assertEqual(TableElement("1.0"), 1)
        self.assertEqual(TableElement("1"), 1.0)
        self.assertEqual(TableElement(1.0), "1")
        self.assertEqual(TableElement(1), "1.0")
        self.assertEqual(TableElement(1.0), 1)
        self.assertEqual(TableElement(1), 1.0)
        self.assertNotEqual(TableElement("string"), "")
