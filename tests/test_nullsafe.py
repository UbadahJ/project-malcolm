import unittest

from utils.nullsafe import *


class TestNullSafe(unittest.TestCase):
    def test_ifnone(self):
        self.assertEqual(ifnone(None, True), True)
        self.assertEqual(ifnone(False, True), False)

    def test_notnone(self):
        self.assertIsNotNone(notnone("str"))
        with self.assertRaises(AssertionError):
            notnone(None)

    def test_asserttype(self):
        self.assertEqual(type(asserttype(str, "Testing")), str)
        with self.assertRaises(AssertionError):
            asserttype(str, b"")

    def test_assertsequencetype(self):
        with self.assertRaises(AssertionError):
            assertsequencetype(str, ['str', None, 123])
        self.assertEqual(assertsequencetype(str, ['data']), ['data'])
        self.assertEqual(assertsequencetype(list, [[]]), [[]])


if __name__ == '__main__':
    unittest.main()
