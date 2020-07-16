import unittest

from utils.collections import contains, first, last, empty, flatten, flatten_bytes


class TestCollections(unittest.TestCase):

    def test_first(self):
        self.assertEqual(first([x for x in range(10)]), 0)
        self.assertEqual(first([]), None)

    def test_last(self):
        self.assertEqual(last([x for x in range(10)]), 9)
        self.assertEqual(last([]), None)

    def empty(self):
        self.assertFalse(empty([x for x in range(10)]))
        self.assertTrue(empty([]))

    def test_contains(self):
        self.assertFalse(contains(['abc', ['dfg'], ['hij', [None]]], None))
        self.assertFalse(contains([], None))
        self.assertFalse(contains([[[[[[['abc', ['dfg'], ['hij', []]]]]]]]], None))
        self.assertTrue(contains([None], None))

    def test_contains_recursive(self):
        self.assertTrue(contains(['abc', ['dfg'], ['hij', [None]]], None, recursive=True))
        self.assertFalse(contains([], None, recursive=True))
        self.assertFalse(contains([[[[[[['abc', ['dfg'], ['hij', []]]]]]]]], None, recursive=True))
        self.assertTrue(contains([None], None, recursive=True))

    def test_flatten(self):
        self.assertEqual(flatten(['x', ['y'], ['z']]), ['x', 'y', 'z'])
        self.assertEqual(flatten(['x', 'y', 'z']), ['x', 'y', 'z'])
        self.assertEqual(flatten([]), [])

    def test_flatten_bytes(self):
        self.assertEqual(flatten_bytes([b'Testing', [b'O', b'n', b'e'], b'Two', b'Three']),
                         ([b'Testing', b'One', b'Two', b'Three']))

if __name__ == '__main__':
    unittest.main()
