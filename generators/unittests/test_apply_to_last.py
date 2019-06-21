import unittest
from generators import apply_to_last

class Test_apply_to_last(unittest.TestCase):
    def test_apply_to_last_basic(self):
        self.assertEqual(
            list(apply_to_last(range(10), lambda i:i*2)),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 18],
            'invalid output of basic usage'
        )
    def test_apply_to_last_input_validation(self):
        with self.assertRaises(AssertionError):
            list(apply_to_last([1, 2, 3], [1, 2, 3]))
        with self.assertRaises(AssertionError):
            list(apply_to_last(3, lambda i:None))
    def test_apply_to_last_of_empty_iterator(self):
        l = []
        list(apply_to_last(range(0), l.append))
        self.assertEqual(l, [], 'apply_to_last should not actually do anything with l')
    def test_apply_to_last_of_single_iterator(self):
        l = []
        list(apply_to_last(range(1), l.append))
        self.assertEqual(l, [0], 'apply_to_last should have appended one item')

if __name__ == '__main__':
    unittest.main(verbosity=2)
